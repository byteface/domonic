"""
domonic.webapi.streams
====================================
https://developer.mozilla.org/en-US/docs/Web/API/Streams_API
"""

from __future__ import annotations

import zlib
from collections import deque
from contextlib import suppress
from typing import Any, Optional

_FORMAT_WBITS = {
    "gzip": zlib.MAX_WBITS | 16,
    "deflate": zlib.MAX_WBITS,
    "deflate-raw": -zlib.MAX_WBITS,
}


def _normalize_format(format: str) -> str:
    normalized = str(format).lower()
    if normalized not in _FORMAT_WBITS:
        supported = ", ".join(sorted(_FORMAT_WBITS))
        raise TypeError(
            f"Unsupported compression format: {format!r}. Expected one of: {supported}"
        )
    return normalized


def _coerce_bytes(chunk: Any) -> bytes:
    if chunk is None:
        return b""
    if isinstance(chunk, bytes):
        return chunk
    if isinstance(chunk, bytearray):
        return bytes(chunk)
    if isinstance(chunk, memoryview):
        return chunk.tobytes()
    if isinstance(chunk, str):
        return chunk.encode("utf-8")

    blob_bytes = getattr(chunk, "bytes", None)
    if callable(blob_bytes):
        return blob_bytes()

    buffer = getattr(chunk, "buffer", None)
    if buffer is not None:
        nested = getattr(buffer, "buffer", buffer)
        with suppress(TypeError):
            return bytes(nested)

    return bytes(chunk)


def _join_chunks(chunks):
    if not chunks:
        return b""
    try:
        return b"".join(_coerce_bytes(chunk) for chunk in chunks)
    except (TypeError, ValueError):
        return "".join(str(chunk) for chunk in chunks)


def _compress_bytes(format: str, chunk: Any) -> bytes:
    compressor = zlib.compressobj(wbits=_FORMAT_WBITS[_normalize_format(format)])
    return compressor.compress(_coerce_bytes(chunk)) + compressor.flush()


def _decompress_bytes(format: str, chunk: Any) -> bytes:
    decompressor = zlib.decompressobj(wbits=_FORMAT_WBITS[_normalize_format(format)])
    return decompressor.decompress(_coerce_bytes(chunk)) + decompressor.flush()


# ---------------------------------------------------------------------------
# Queuing strategies + shared helpers
# ---------------------------------------------------------------------------

_EMPTY = (None, b"", "")


def _strategy_high_water_mark(strategy, default: float = 1) -> float:
    if strategy is None:
        return default
    if isinstance(strategy, dict):
        return strategy.get("highWaterMark", default)
    return getattr(strategy, "highWaterMark", default)


def _strategy_size_fn(strategy):
    if strategy is None:
        return None
    if isinstance(strategy, dict):
        return strategy.get("size")
    return getattr(strategy, "size", None)


def _is_strategy(obj) -> bool:
    if obj is None:
        return False
    if isinstance(obj, dict):
        return "highWaterMark" in obj or "size" in obj
    return hasattr(obj, "highWaterMark")


def _high_water_mark_from_options(options, keyword) -> float:
    hwm = keyword
    if isinstance(options, dict):
        hwm = options.get("highWaterMark", hwm)
    elif options is not None:
        hwm = options
    if hwm is None:
        raise TypeError(
            "Failed to construct queuing strategy: required member highWaterMark is undefined"
        )
    return hwm


class CountQueuingStrategy:
    """
    https://developer.mozilla.org/en-US/docs/Web/API/CountQueuingStrategy

    Every chunk counts as ``1`` towards the high water mark, so the queue is
    measured by the number of buffered chunks.
    """

    def __init__(self, options=None, *, highWaterMark=None):
        self.highWaterMark = _high_water_mark_from_options(options, highWaterMark)

    def size(self, chunk: Any = None) -> int:
        return 1

    def __repr__(self) -> str:
        return f"<CountQueuingStrategy highWaterMark={self.highWaterMark}>"


class ByteLengthQueuingStrategy:
    """
    https://developer.mozilla.org/en-US/docs/Web/API/ByteLengthQueuingStrategy

    Each chunk contributes its ``byteLength`` (falling back to ``len()``)
    towards the high water mark, so the queue is measured in bytes.
    """

    def __init__(self, options=None, *, highWaterMark=None):
        self.highWaterMark = _high_water_mark_from_options(options, highWaterMark)

    def size(self, chunk: Any) -> int:
        if chunk is None:
            return 0
        for attr in ("byteLength", "nbytes"):
            value = getattr(chunk, attr, None)
            if isinstance(value, int):
                return value
        try:
            return len(_coerce_bytes(chunk))
        except (TypeError, ValueError):
            try:
                return len(chunk)
            except TypeError:
                return 0

    def __repr__(self) -> str:
        return f"<ByteLengthQueuingStrategy highWaterMark={self.highWaterMark}>"


def _abort_exception(signal) -> BaseException:
    reason = getattr(signal, "reason", None)
    if isinstance(reason, BaseException):
        return reason
    return RuntimeError(str(reason) if reason else "The operation was aborted")


def _looks_like_underlying_source(obj) -> bool:
    if obj is None or isinstance(obj, (bytes, bytearray, memoryview, str)):
        return False
    if isinstance(obj, dict):
        return bool({"start", "pull", "cancel", "type"} & set(obj))
    if callable(obj):
        return False
    return any(
        callable(getattr(obj, name, None)) for name in ("start", "pull", "cancel")
    )


# ---------------------------------------------------------------------------
# ReadableStream
# ---------------------------------------------------------------------------


class ReadableStreamDefaultController:
    """
    https://developer.mozilla.org/en-US/docs/Web/API/ReadableStreamDefaultController

    Handed to an underlying source's ``start``/``pull`` callbacks so it can
    ``enqueue`` chunks, ``close`` the stream or ``error`` it.
    """

    def __init__(self, stream: "ReadableStream"):
        self._stream = stream

    @property
    def desiredSize(self):
        state = self._stream._state
        if state == "errored":
            return None
        if state == "closed":
            return 0
        return self._stream._high_water_mark - self._stream._queue_total_size

    def enqueue(self, chunk: Any):
        self._stream._enqueue(chunk)

    def close(self):
        self._stream._close_from_controller()

    def error(self, reason: Any = None):
        self._stream._error(reason)


class ReadableStreamDefaultReader:
    """
    https://developer.mozilla.org/en-US/docs/Web/API/ReadableStreamDefaultReader

    ``read()`` returns ``{"value": chunk, "done": bool}`` like the browser API
    and the reader is also a plain Python iterator over its chunks.
    """

    def __init__(self, stream: "ReadableStream", mode: Optional[str] = None):
        if stream._reader is not None:
            raise TypeError("ReadableStream is already locked to a reader")
        if mode not in (None, "", "default"):
            raise TypeError(f"Unsupported reader mode: {mode!r}")
        self._stream = stream
        stream._reader = self

    @property
    def closed(self) -> bool:
        stream = self._stream
        if stream is None:
            return True
        return stream._state != "readable" and not stream._queue

    def read(self) -> dict:
        stream = self._stream
        if stream is None:
            raise TypeError("This readable stream reader has been released")
        stream._disturbed = True
        while not stream._queue and stream._state == "readable":
            if not stream._pump():
                break
        if stream._queue:
            return {"value": stream._dequeue(), "done": False}
        if stream._state == "errored":
            raise stream._error_to_raise
        return {"value": None, "done": True}

    def cancel(self, reason: Any = None):
        if self._stream is None:
            raise TypeError("This readable stream reader has been released")
        return self._stream.cancel(reason)

    def releaseLock(self):
        if self._stream is not None:
            self._stream._reader = None
            self._stream = None

    def __iter__(self):
        return self

    def __next__(self):
        result = self.read()
        if result["done"]:
            raise StopIteration
        return result["value"]


class ReadableStream:
    """
    https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream

    Two construction styles are supported:

    * a raw value (``bytes``/``str``/callable) for quick, synchronous examples
      -- ``getReader()`` then hands that value straight back, and ``read(size)``
      slices it;
    * an underlying source ``dict``/object with ``start``/``pull``/``cancel``
      callbacks -- ``getReader()`` returns a
      :class:`ReadableStreamDefaultReader`, ``pull`` is driven by backpressure
      derived from an optional queuing strategy, and ``cancel``/``tee`` work as
      in the browser.
    """

    def __init__(self, *args, strategy=None, queuingStrategy=None):
        self.__args = args
        self._chunks = []
        self._queue = deque()
        self._queue_total_size = 0
        self._state = "readable"  # readable | closed | errored
        self._stored_error: Optional[BaseException] = None
        self._reader = None
        self._disturbed = False
        self._legacy_pulled = False
        self.readable = self

        source = args[0] if args else None
        if _looks_like_underlying_source(source):
            self._legacy = False
            self._source = source
        else:
            self._legacy = True
            self._source = None

        chosen = strategy or queuingStrategy
        if chosen is None and not self._legacy and len(args) > 1 and _is_strategy(args[1]):
            chosen = args[1]
        self._strategy = chosen
        self._high_water_mark = _strategy_high_water_mark(chosen, 1)
        self._size_fn = _strategy_size_fn(chosen)

        self._controller = ReadableStreamDefaultController(self)
        if not self._legacy:
            self._call_source("start", self._controller)
            self._fill_queue()

    # -- underlying source plumbing ----------------------------------------

    def _call_source(self, name, *call_args):
        src = self._source
        if src is None:
            return None
        fn = src.get(name) if isinstance(src, dict) else getattr(src, name, None)
        if callable(fn):
            return fn(*call_args)
        return None

    def _chunk_size(self, chunk) -> float:
        if self._size_fn is None:
            return 1
        try:
            return self._size_fn(chunk)
        except TypeError:
            return self._size_fn()

    def _enqueue(self, chunk):
        if self._state != "readable":
            raise TypeError("Cannot enqueue a chunk into a stream that is not readable")
        self._queue.append(chunk)
        self._queue_total_size += self._chunk_size(chunk)

    def _dequeue(self):
        chunk = self._queue.popleft()
        self._queue_total_size -= self._chunk_size(chunk)
        if self._queue_total_size < 0 or not self._queue:
            self._queue_total_size = sum(self._chunk_size(c) for c in self._queue)
        self._fill_queue()
        return chunk

    def _close_from_controller(self):
        if self._state == "readable":
            self._state = "closed"

    def _error(self, reason=None):
        self._state = "errored"
        if isinstance(reason, BaseException):
            self._stored_error = reason
        else:
            self._stored_error = RuntimeError(
                str(reason) if reason is not None else "The stream errored"
            )
        self._queue.clear()
        self._queue_total_size = 0

    @property
    def _error_to_raise(self) -> BaseException:
        error = self._stored_error
        return error if error is not None else RuntimeError("The stream errored")

    def _legacy_value(self):
        if self._chunks:
            output = _join_chunks(self._chunks)
            self._chunks = []
            return output
        if self.__args and callable(self.__args[0]):
            return self.__args[0]()
        if self.__args:
            return self.__args[0]
        return b""

    def _pump(self) -> bool:
        """Make an effort to get at least one chunk queued. Returns progress."""
        if self._queue:
            return True
        if self._state != "readable":
            return False
        if self._legacy:
            if self._legacy_pulled:
                return False
            self._legacy_pulled = True
            value = self._legacy_value()
            self._state = "closed"
            if value not in _EMPTY:
                self._queue.append(value)
                self._queue_total_size += self._chunk_size(value)
                return True
            return False
        before = len(self._queue)
        self._call_source("pull", self._controller)
        return len(self._queue) > before

    def _fill_queue(self):
        """Pull from the source while backpressure allows (desiredSize > 0)."""
        if self._legacy:
            return
        guard = 0
        while (
            self._state == "readable"
            and (self._high_water_mark - self._queue_total_size) > 0
        ):
            before = len(self._queue)
            self._call_source("pull", self._controller)
            guard += 1
            if len(self._queue) == before or guard > 10000:
                break

    def _drain(self) -> list:
        parts = []
        while True:
            while not self._queue and self._state == "readable":
                if not self._pump():
                    break
            if not self._queue:
                break
            parts.append(self._dequeue())
        if self._state == "errored":
            raise self._error_to_raise
        return parts

    # -- public API ------------------------------------------------------

    @property
    def locked(self) -> bool:
        """
        https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream/locked
        """
        return self._reader is not None

    def getReader(self, options=None):
        """
        https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream/getReader
        """
        if self._legacy and options is None:
            if self.__args:
                first = self.__args[0]
                return first() if callable(first) else first
            return self.read
        mode = options.get("mode") if isinstance(options, dict) else None
        return ReadableStreamDefaultReader(self, mode=mode)

    def write(self, chunk):
        self._chunks.append(chunk)
        return chunk

    def read(self, size=None):
        if self._chunks:
            output = _join_chunks(self._chunks)
            self._chunks = []
        elif not self._legacy:
            parts = self._drain()
            output = _join_chunks(parts) if parts else b""
        elif self.__args and callable(self.__args[0]):
            output = self.__args[0]()
        elif self.__args:
            output = self.__args[0]
        else:
            output = b""

        if size is None or size >= len(output):
            return output

        remainder = output[size:]
        if remainder:
            self._chunks.append(remainder)
        return output[:size]

    def cancel(self, reason: Any = None):
        """
        https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream/cancel
        """
        self._disturbed = True
        if self._state == "errored":
            raise self._error_to_raise
        self._queue.clear()
        self._queue_total_size = 0
        self._legacy_pulled = True
        self._chunks = []
        self._state = "closed"
        return self._call_source("cancel", reason)

    def tee(self):
        """
        https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream/tee
        """
        if self._legacy and not self._legacy_pulled and not self._chunks:
            value = self._legacy_value()
            self._legacy_pulled = True
            self._state = "closed"
            chunks = [] if value in _EMPTY else [value]
        else:
            chunks = self._drain()
        return (
            ReadableStream._from_iterable(chunks),
            ReadableStream._from_iterable(list(chunks)),
        )

    @classmethod
    def _from_iterable(cls, items) -> "ReadableStream":
        buffered = list(items)

        def start(controller):
            for item in buffered:
                controller.enqueue(item)
            controller.close()

        return cls({"start": start})

    def __iter__(self):
        return iter(ReadableStreamDefaultReader(self))

    def pipeThrough(self, transform, options=None):
        """
        https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream/pipeThrough
        """
        if len(self.__args) > 1 and callable(self.__args[1]):
            return self.__args[1](transform, options)

        if hasattr(transform, "write"):
            transform.write(self.read())
            if hasattr(transform, "close"):
                transform.close()
            return getattr(transform, "readable", transform)

        if hasattr(transform, "transform"):
            return ReadableStream(transform.transform(self.read()))

        if callable(transform):
            return transform(self.read())

        raise TypeError("pipeThrough() expects a transform stream or callable")

    def pipeTo(self, dest, options=None):
        """
        https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream/pipeTo
        """
        if len(self.__args) > 2 and callable(self.__args[2]):
            return self.__args[2](dest, options)

        signal = options.get("signal") if isinstance(options, dict) else None
        if signal is not None and getattr(signal, "aborted", False):
            self.cancel(getattr(signal, "reason", None))
            raise _abort_exception(signal)

        data = self.read()
        if hasattr(dest, "write"):
            result = dest.write(data)
            if hasattr(dest, "close"):
                dest.close()
            return result

        if callable(dest):
            return dest(data)

        raise TypeError("pipeTo() expects a writable stream or callable")


class WritableStreamDefaultWriter:
    """
    https://developer.mozilla.org/en-US/docs/Web/API/WritableStreamDefaultWriter
    """

    def __init__(self, stream: "WritableStream"):
        self._stream = stream

    @property
    def desiredSize(self):
        return None if self._stream is None else self._stream.desiredSize

    @property
    def closed(self) -> bool:
        return self._stream is None or self._stream.closed

    @property
    def ready(self) -> bool:
        return self._stream is not None and not self._stream.aborted

    def write(self, chunk):
        if self._stream is None:
            raise TypeError("This writable stream writer has been released")
        return self._stream.write(chunk)

    def close(self):
        if self._stream is None:
            raise TypeError("This writable stream writer has been released")
        return self._stream.close()

    def abort(self, reason: Any = None):
        if self._stream is None:
            raise TypeError("This writable stream writer has been released")
        return self._stream.abort(reason)

    def releaseLock(self):
        self._stream = None


class WritableStream:
    """
    https://developer.mozilla.org/en-US/docs/Web/API/WritableStream
    """

    def __init__(self, sink=None, strategy=None):
        self.sink = sink
        self._chunks = []
        self.closed = False
        self.aborted = False
        self.writable = self
        self._strategy = strategy
        self._high_water_mark = _strategy_high_water_mark(strategy, 1)
        self._size_fn = _strategy_size_fn(strategy)
        self._queue_total_size = 0

    @property
    def desiredSize(self):
        """
        https://developer.mozilla.org/en-US/docs/Web/API/WritableStreamDefaultWriter/desiredSize
        """
        if self.aborted:
            return None
        if self.closed:
            return 0
        return self._high_water_mark - self._queue_total_size

    def getWriter(self):
        """
        https://developer.mozilla.org/en-US/docs/Web/API/WritableStream/getWriter
        """
        return WritableStreamDefaultWriter(self)

    def write(self, chunk):
        if self.aborted:
            raise ValueError("Cannot write to an aborted WritableStream")
        if self.closed:
            raise ValueError("Cannot write to a closed WritableStream")

        if hasattr(self.sink, "write"):
            return self.sink.write(chunk)
        if callable(self.sink):
            return self.sink(chunk)

        self._chunks.append(chunk)
        if self._size_fn is not None:
            with suppress(TypeError, ValueError):
                self._queue_total_size += self._size_fn(chunk)
        else:
            self._queue_total_size += 1
        return chunk

    def close(self):
        self.closed = True
        return None

    def abort(self, reason: Any = None):
        """
        https://developer.mozilla.org/en-US/docs/Web/API/WritableStream/abort
        """
        self.aborted = True
        self.closed = True
        self._chunks = []
        self._queue_total_size = 0
        if hasattr(self.sink, "abort"):
            return self.sink.abort(reason)
        return None

    def read(self, size=None):
        output = _join_chunks(self._chunks)
        self._chunks = []
        self._queue_total_size = 0
        if size is None or size >= len(output):
            return output
        self._chunks.append(output[size:])
        return output[:size]


class TransformStream(ReadableStream):
    """
    https://developer.mozilla.org/en-US/docs/Web/API/TransformStream
    """

    def __init__(self, transformer=None):
        super().__init__()
        self.transformer = transformer
        self.readable = self
        self.writable = self

    def transform(self, chunk):
        if hasattr(self.transformer, "transform"):
            return self.transformer.transform(chunk)
        if callable(self.transformer):
            return self.transformer(chunk)
        return chunk

    def write(self, chunk):
        output = self.transform(chunk)
        if output is not None:
            self._chunks.append(output)
        return output

    def close(self):
        if hasattr(self.transformer, "flush"):
            output = self.transformer.flush()
            if output is not None:
                self._chunks.append(output)
            return output
        return None


class CompressionStream(TransformStream):
    """
    https://developer.mozilla.org/en-US/docs/Web/API/CompressionStream
    """

    def __init__(self, format):
        super().__init__()
        self.format = _normalize_format(format)
        self._compressor = zlib.compressobj(wbits=_FORMAT_WBITS[self.format])
        self._closed = False

    def compress(self, chunk):
        return _compress_bytes(self.format, chunk)

    transform = compress

    def write(self, chunk):
        if self._closed:
            raise ValueError("Cannot write to a closed CompressionStream")
        output = self._compressor.compress(_coerce_bytes(chunk))
        if output:
            self._chunks.append(output)
        return output

    def close(self):
        if self._closed:
            return b""
        self._closed = True
        output = self._compressor.flush()
        if output:
            self._chunks.append(output)
        return output


class DecompressionStream(TransformStream):
    """
    https://developer.mozilla.org/en-US/docs/Web/API/DecompressionStream
    """

    def __init__(self, format):
        super().__init__()
        self.format = _normalize_format(format)
        self._decompressor = zlib.decompressobj(wbits=_FORMAT_WBITS[self.format])
        self._closed = False

    def decompress(self, chunk):
        return _decompress_bytes(self.format, chunk)

    transform = decompress

    def write(self, chunk):
        if self._closed:
            raise ValueError("Cannot write to a closed DecompressionStream")
        output = self._decompressor.decompress(_coerce_bytes(chunk))
        if output:
            self._chunks.append(output)
        return output

    def close(self):
        if self._closed:
            return b""
        self._closed = True
        output = self._decompressor.flush()
        if output:
            self._chunks.append(output)
        return output
