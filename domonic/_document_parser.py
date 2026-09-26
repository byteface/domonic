"""
domonic._document_parser
====================================

The parser session behind ``document.open()`` / ``document.write()`` /
``document.close()`` (https://html.spec.whatwg.org/#dynamic-markup-insertion).

Markup handed to ``write()`` is parsed straight into the document, chunk by
chunk. Between writes the document is live: queries see everything parsed so
far, ``MutationObserver`` records for the nodes that landed are delivered
after each write, and ``window.stop()`` drops whatever has not arrived yet.
``close()`` finishes the parse.

Two engines can drive it, chosen with :func:`domonic.set_default_parser`:

- ``html5lib`` (the default, and what ``auto`` or any other backend name
  means here): the bundled WHATWG tree builder, so the partial tree is the
  one a browser would have, implied elements, foster parenting and the
  adoption agency included. It runs on a worker thread that is parked
  between writes.
- ``html.parser``: the standard library tokenizer. No dependency, no HTML5
  tree construction beyond the implied elements the adapter adds itself.

lxml is deliberately not here: libxml2's push parser holds most of a page
back until the parser is closed, so it cannot stream.
"""

from __future__ import annotations

import codecs
import logging
import queue
import threading
from typing import Any, Callable

from domonic.ext._encoding import PRESCAN_BYTES, bom_encoding, sniff_encoding, whatwg_name
from domonic.ext._rawdom import (
    _RECORD_LOCK,
    HTML_NAMESPACE,
    _freeze_args,
    _invalidate_indexes,
    _live_append,
    _set_attribute_raw,
)
from domonic.ext.html_parser_ import DomonicHTMLParser

_LOGGER = logging.getLogger("domonic.parser")

Recorder = Callable[[Any, Any], None]


def _appender(recorder: Recorder | None) -> Callable[[Any, Any], None]:
    """The insertion primitive for the stdlib tree logic: plain, or also
    telling ``recorder`` what landed (for MutationObserver)."""
    if recorder is None:
        return _live_append

    def append_and_record(parent: Any, child: Any) -> None:
        _live_append(parent, child)
        recorder(parent, child)

    return append_and_record


# ---------------------------------------------------------------------------
# stdlib engine


class _DocumentParser(DomonicHTMLParser):
    """The stdlib adapter building straight into a document (its ``root``),
    plus two things the adapter's fragment mode never sees: the doctype, and
    the ``<html>`` tag, which is the document itself when the document is an
    ``HTMLDocument`` (domonic's ``HTMLDocument`` *is* the root html element,
    which is also what ``parseString`` hands back for a whole page)."""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        root = self.root
        if tag.lower() == "html" and len(self.stack) == 1 and getattr(root, "name", "") == "html":
            from domonic.dom import Element

            if isinstance(root, Element):
                for name, value in attrs:
                    _set_attribute_raw(root, name, "" if value is None else value)
            self.stack.append(root)
            self.namespace_stack.append(HTML_NAMESPACE)
            return
        super().handle_starttag(tag, attrs)

    def handle_decl(self, decl: str) -> None:
        parts = decl.split()
        if len(parts) >= 2 and parts[0].lower() == "doctype":
            self.set_doctype(parts[1])

    def set_doctype(self, name: str, public_id: str | None = None, system_id: str | None = None) -> None:
        from domonic.dom import DocumentType

        self.root.doctype = DocumentType(str(name).lower(), public_id or "", system_id or "")


class _StdlibEngine:
    name = "html.parser"

    def __init__(self, document: Any) -> None:
        self.parser = _DocumentParser(root=document)

    @property
    def open_elements(self) -> list[Any]:
        return self.parser.stack

    def feed(self, text: str, recorder: Recorder | None) -> None:
        self.parser._append = _appender(recorder)
        self.parser.feed(text)

    def close(self) -> None:
        self.parser.close()
        for node in self.parser.stack:
            _freeze_args(node)

    def abort(self) -> None:
        self.close()


# ---------------------------------------------------------------------------
# html5lib engine: the spec tree builder on a worker thread


class _HandoffStream:
    """A file-like whose ``read()`` blocks until the writer supplies data.
    ``write()`` returns once the parser thread has consumed everything and is
    parked in ``read()`` again (or has finished), so between writes only the
    main thread touches the tree."""

    def __init__(self) -> None:
        self._queue: queue.Queue[str | None] = queue.Queue()
        self._parked = threading.Event()
        self._buffer = ""
        self._eof = False

    def read(self, size: int = -1) -> str:
        while not self._buffer and not self._eof:
            self._parked.set()
            item = self._queue.get()
            if item is None:
                self._eof = True
            else:
                self._buffer += item
        if size is None or size < 0:
            out, self._buffer = self._buffer, ""
        else:
            out, self._buffer = self._buffer[:size], self._buffer[size:]
        return out

    def wait_parked(self) -> None:
        self._parked.wait()

    def write(self, text: str) -> None:
        self._parked.clear()
        self._queue.put(text)
        self._parked.wait()

    def close(self) -> None:
        self._parked.clear()
        self._queue.put(None)

    def finished(self) -> None:
        self._parked.set()


class _Html5libEngine:
    name = "html5lib"

    def __init__(self, document: Any) -> None:
        from html5lib import HTMLParser

        from domonic.ext.html5lib_ import _recording, getTreeBuilder

        self._parser = HTMLParser(tree=getTreeBuilder(target=document))
        self._stream = _HandoffStream()
        self._recorder: Recorder | None = None
        self._error: BaseException | None = None
        self._done = False

        def run() -> None:
            _recording.hook = self._hook
            try:
                self._parser.parse(self._stream)
            except BaseException as exc:  # surfaced on the next write / close
                self._error = exc
            finally:
                _recording.hook = None
                self._done = True
                self._stream.finished()

        self._thread = threading.Thread(target=run, name="domonic-html5lib-stream", daemon=True)
        self._thread.start()
        self._stream.wait_parked()

    def _hook(self, parent: Any, child: Any) -> None:
        recorder = self._recorder
        if recorder is not None:
            recorder(parent, child)

    @property
    def open_elements(self) -> list[Any]:
        return [node.element for node in self._parser.tree.openElements]

    def _check(self) -> None:
        if self._error is not None:
            error, self._error = self._error, None
            raise error

    def feed(self, text: str, recorder: Recorder | None) -> None:
        if self._done:
            return
        self._recorder = recorder
        self._stream.write(text)
        self._check()

    def close(self) -> None:
        if not self._done:
            self._stream.close()
            self._thread.join()
        self._check()

    def abort(self) -> None:
        # EOF now: html5lib closes what is open and the tree stands as it is
        self.close()


# ---------------------------------------------------------------------------
# the session


_ENGINES: dict[str, type] = {
    "html5lib": _Html5libEngine,
    "html.parser": _StdlibEngine,
    "html_parser": _StdlibEngine,
}


def _select_engine(document: Any, requested: str | None) -> Any:
    if requested is None:
        try:
            from domonic import domonic as api  # ``set_default_parser`` stores the choice on the class

            requested = getattr(api, "DEFAULT_PARSER", None) or "auto"
        except Exception:
            requested = "auto"
    name = str(requested).lower()
    engine = _ENGINES.get(name, _Html5libEngine)(document)
    _LOGGER.debug("document.open: streaming with %s", engine.name)
    return engine


class DocumentParserSession:
    def __init__(self, document: Any, parser: str | None = None) -> None:
        self.document = document
        self.engine = _select_engine(document, parser)
        self.closed = False
        self.aborted = False
        self._decoder: Any = None
        self._pending = b""  # bytes held back until there is enough to sniff the encoding
        self.encoding: str | None = None
        self._added: list[tuple[Any, Any]] = []

    # -- input -----------------------------------------------------------

    def write(self, data: Any) -> None:
        """Feed a ``str`` or ``bytes`` chunk. Bytes are decoded the way a
        browser decodes a page (byte order mark, then ``<meta charset>`` in
        the first kilobyte, else UTF-8 or windows-1252), and a character
        split across chunks is carried over."""
        if self.closed or self.aborted:
            return
        if isinstance(data, (bytes, bytearray, memoryview)):
            text = self._decode(bytes(data), final=False)
        else:
            text = str(data)
        if text:
            self._feed(text)

    def _decode(self, chunk: bytes, final: bool) -> str:
        if self._decoder is None:
            self._pending += chunk
            if len(self._pending) < PRESCAN_BYTES and not final:
                return ""
            data, self._pending = self._pending, b""
            self.encoding = sniff_encoding(data)
            self.document.__dict__["_characterSet"] = whatwg_name(self.encoding)
            self._decoder = codecs.getincrementaldecoder(self.encoding)(errors="replace")
            _, bom_length = bom_encoding(data)
            chunk = data[bom_length:]
        return self._decoder.decode(chunk, final)

    def close(self) -> None:
        """Finish the parse: flush the decoder and the engine, close every
        element still open, and run a final checkpoint."""
        if self.closed:
            return
        if not self.aborted and (self._pending or self._decoder is not None):
            tail = self._decode(b"", final=True)
            if tail:
                self._feed(tail)
        self.closed = True
        with _RECORD_LOCK:
            self.engine.close()
        self._checkpoint()

    def abort(self) -> None:
        """``window.stop()``: ignore any further input. ``close()`` still
        finalises what has already landed."""
        if self.aborted or self.closed:
            return
        self.aborted = True
        with _RECORD_LOCK:
            self.engine.abort()
        self._checkpoint()

    # -- parsing ---------------------------------------------------------

    def _feed(self, text: str) -> None:
        from domonic.dom import MutationObserver

        # Only pay for recording insertions while someone is observing.
        recorder = self._record if MutationObserver._all_observers else None
        with _RECORD_LOCK:  # no other thread's parse may record while raw nodes are made here
            self.engine.feed(text, recorder)
        self._checkpoint()

    def _record(self, parent: Any, child: Any) -> None:
        self._added.append((parent, child))

    def _checkpoint(self) -> None:
        """Make the partial document safe to observe: caches that raw
        insertion bypassed are dropped, ``documentElement`` is resolved, and
        the insertions since the last checkpoint reach observers, batched per
        parent in document order."""
        from domonic.dom import Element, MutationObserver, MutationRecord, _deliver_mutation_records

        document = self.document
        _invalidate_indexes()
        for node in self.engine.open_elements:  # only the open elements can still gain children
            node.__dict__["_render_cache_dirty"] = True
        document.__dict__["_render_cache_dirty"] = True
        if document.__dict__.get("documentElement") is None:
            if getattr(document, "name", "") == "html":
                document.__dict__["documentElement"] = document
            else:
                for child in document.__dict__.get("args") or ():
                    if isinstance(child, Element):
                        document.__dict__["documentElement"] = child
                        break
        if not self._added:
            return
        added = self._added
        self._added = []
        observers = list(MutationObserver._all_observers)
        if not observers:
            return
        groups: dict[int, tuple[Any, list[Any]]] = {}
        for parent, child in added:
            entry = groups.get(id(parent))
            if entry is None:
                entry = groups[id(parent)] = (parent, [])
            entry[1].append(child)
        # One delivery per write: every parent's record is queued first, then
        # each interested observer's callback runs once with all of them.
        queued = False
        for parent, nodes in groups.values():
            record = MutationRecord("childList", parent, addedNodes=nodes, removedNodes=())
            for observer in observers:
                if observer._enqueue_if_observing(record):
                    queued = True
        if queued:
            _deliver_mutation_records()
