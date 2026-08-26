"""
domonic.webapi.webworkers
====================================
https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API
"""

from __future__ import annotations

import copy
import inspect
import os
import queue
import runpy
import threading
import traceback
from pathlib import Path
from typing import Any, Callable
from urllib.parse import unquote, urlparse

from domonic.events import ErrorEvent, EventTarget, MessageEvent
from domonic.webapi.scheduler import Scheduler, TaskController, TaskSignal


_STOP = object()
_CURRENT_SCOPE = threading.local()


def _clone_message(message: Any) -> Any:
    """Best-effort structured-clone stand-in for Python worker messages."""
    return copy.deepcopy(message)


def _transfer_list(transfer_or_options: Any = None) -> list[Any]:
    if transfer_or_options is None:
        return []
    if isinstance(transfer_or_options, dict) and "transfer" in transfer_or_options:
        return list(transfer_or_options.get("transfer") or [])
    return list(transfer_or_options or [])


def _resolve_script_path(
    script_url: str | os.PathLike[str],
    base: Path | None = None,
) -> Path:
    script = os.fspath(script_url)
    parsed = urlparse(script)
    if parsed.scheme and parsed.scheme != "file":
        raise ValueError("Worker only supports local Python script paths")
    if parsed.scheme == "file":
        path = Path(unquote(parsed.path))
    else:
        path = Path(script).expanduser()
    if not path.is_absolute() and base is not None:
        path = base / path
    return path.resolve()


def _call_worker_entry(
    entry: Callable[..., Any],
    scope: "DedicatedWorkerGlobalScope",
) -> Any:
    try:
        signature = inspect.signature(entry)
    except (TypeError, ValueError):
        return entry(scope)

    parameters = signature.parameters.values()
    accepts_scope = any(
        parameter.kind == inspect.Parameter.VAR_POSITIONAL
        or parameter.kind
        in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
        for parameter in parameters
    )
    if accepts_scope:
        return entry(scope)
    return entry()


def get_current_worker_scope() -> "DedicatedWorkerGlobalScope | None":
    """Return the worker scope for the current worker thread, when present."""
    return getattr(_CURRENT_SCOPE, "scope", None)


def _require_current_worker_scope() -> "DedicatedWorkerGlobalScope":
    scope = get_current_worker_scope()
    if scope is None:
        raise RuntimeError("No active WorkerGlobalScope in this thread")
    return scope


def postMessage(
    message: Any,
    transfer: list[Any] | dict[str, Any] | None = None,
) -> None:
    """Post a message from the current worker scope to its parent."""
    return _require_current_worker_scope().postMessage(message, transfer)


def close() -> None:
    """Close the current worker scope."""
    return _require_current_worker_scope().close()


def importScripts(*urls: str | os.PathLike[str]) -> None:
    """Import local Python scripts into the current worker scope."""
    return _require_current_worker_scope().importScripts(*urls)


class WorkerGlobalScope(EventTarget):
    """Base worker global scope.

    The scope is the object exposed to worker scripts as ``self`` and
    ``globalThis``. It shares domonic's ``EventTarget`` event machinery, so
    worker code can use ``onmessage`` or ``addEventListener("message", ...)``.
    """

    def __init__(
        self,
        worker: "Worker | None" = None,
        location: str = "",
        name: str = "",
        base_path: Path | None = None,
    ) -> None:
        super().__init__()
        self.self = self
        self.globalThis = self
        self.location = location
        self.name = name
        self.onmessage = None
        self.onmessageerror = None
        self.onerror = None
        self.scheduler = Scheduler()
        self._worker = worker
        self._closed = False
        self._base_path = base_path
        self._globals: dict[str, Any] = {}

    @property
    def closed(self) -> bool:
        return self._closed

    def _script_bindings(self) -> dict[str, Any]:
        return {
            "self": self,
            "globalThis": self,
            "postMessage": self.postMessage,
            "close": self.close,
            "importScripts": self.importScripts,
            "addEventListener": self.addEventListener,
            "removeEventListener": self.removeEventListener,
            "dispatchEvent": self.dispatchEvent,
            "scheduler": self.scheduler,
            "Scheduler": Scheduler,
            "TaskController": TaskController,
            "TaskSignal": TaskSignal,
        }

    def _sync_handlers_from_globals(self) -> None:
        for name in ("onmessage", "onmessageerror", "onerror"):
            if name in self._globals:
                setattr(self, name, self._globals[name])

    def _run_script(self, path: Path) -> None:
        self._base_path = path.parent
        initial_globals = self._script_bindings()
        initial_globals["__file__"] = str(path)
        self._globals = initial_globals
        self._globals = runpy.run_path(str(path), init_globals=initial_globals)
        self._sync_handlers_from_globals()

    def postMessage(
        self, message: Any, transfer: list[Any] | dict[str, Any] | None = None
    ) -> None:
        """Send a message to the owner context.

        ``WorkerGlobalScope`` itself has no owner channel. Dedicated workers
        override this method.
        """
        raise NotImplementedError("WorkerGlobalScope.postMessage() needs a worker")

    def close(self) -> None:
        """Close this worker scope and discard queued inbound messages."""
        if self._closed:
            return None
        self._closed = True
        if self._worker is not None:
            self._worker._close_from_scope()
        return None

    def importScripts(self, *urls: str | os.PathLike[str]) -> None:
        """Run local Python scripts in this worker's global environment."""
        base = self._base_path or Path.cwd()
        for url in urls:
            path = _resolve_script_path(url, base)
            if not path.is_file():
                raise FileNotFoundError(str(path))
            globals_for_script = dict(self._globals)
            globals_for_script.update(self._script_bindings())
            globals_for_script["__file__"] = str(path)
            imported = runpy.run_path(str(path), init_globals=globals_for_script)
            self._globals.update(imported)
            self._sync_handlers_from_globals()
        return None


class DedicatedWorkerGlobalScope(WorkerGlobalScope):
    """Global scope for a dedicated ``Worker``."""

    def postMessage(
        self, message: Any, transfer: list[Any] | dict[str, Any] | None = None
    ) -> None:
        """Send a message from the worker to its owner ``Worker`` object."""
        if self._worker is None:
            return None
        self._worker._post_from_scope(message, transfer)
        return None


class Worker(EventTarget):
    """Dedicated worker backed by a Python daemon thread.

    ``scriptURL`` can be a local Python file path or a callable. File workers
    receive browser-like globals such as ``self``, ``postMessage``, ``close``,
    ``addEventListener`` and ``importScripts``. Callable workers may accept the
    ``DedicatedWorkerGlobalScope`` as their first argument.

    Python cannot safely kill arbitrary running thread code. ``terminate()``
    closes the worker channel, discards queued messages and wakes the worker
    loop; a currently-running handler is allowed to return.
    """

    def __init__(
        self,
        scriptURL: str | os.PathLike[str] | Callable[..., Any],
        options: dict[str, Any] | None = None,
    ) -> None:
        super().__init__()
        options = options or {}
        self.scriptURL = scriptURL
        self.name = str(options.get("name", ""))
        self.type = str(options.get("type", "classic"))
        self.onerror = None
        self.onmessage = None
        self.onmessageerror = None
        self._inbound: queue.Queue[Any] = queue.Queue()
        self._closed = threading.Event()
        self._terminated = threading.Event()
        self._ready = threading.Event()

        self._entry = scriptURL
        self._script_path: Path | None = None
        location = ""
        base_path = None
        if not callable(scriptURL):
            self._script_path = _resolve_script_path(scriptURL)
            if not self._script_path.is_file():
                raise FileNotFoundError(str(self._script_path))
            location = self._script_path.as_uri()
            base_path = self._script_path.parent

        self._scope = DedicatedWorkerGlobalScope(
            self,
            location=location,
            name=self.name,
            base_path=base_path,
        )
        thread_name = self.name or (
            self._script_path.stem if self._script_path is not None else "callable"
        )
        self._thread = threading.Thread(
            target=self._run,
            name=f"Worker-{thread_name}",
            daemon=bool(options.get("daemon", True)),
        )
        self._thread.start()

    @property
    def closed(self) -> bool:
        return self._closed.is_set()

    @property
    def terminated(self) -> bool:
        return self._terminated.is_set()

    @property
    def scope(self) -> DedicatedWorkerGlobalScope:
        return self._scope

    def _run(self) -> None:
        _CURRENT_SCOPE.scope = self._scope
        try:
            if self._script_path is not None:
                self._scope._run_script(self._script_path)
            elif callable(self._entry):
                _call_worker_entry(self._entry, self._scope)
            self._ready.set()
            self._message_loop()
        except Exception as exc:
            self._ready.set()
            self._dispatch_error(exc)
        finally:
            self._scope._closed = True
            self._closed.set()
            if getattr(_CURRENT_SCOPE, "scope", None) is self._scope:
                del _CURRENT_SCOPE.scope

    def _message_loop(self) -> None:
        while not self._scope.closed and not self._terminated.is_set():
            item = self._inbound.get()
            if item is _STOP:
                break
            self._scope._sync_handlers_from_globals()
            try:
                self._scope.dispatchEvent(item)
            except Exception as exc:
                self._dispatch_error(exc)

    def _clear_inbound(self) -> None:
        while True:
            try:
                self._inbound.get_nowait()
            except queue.Empty:
                return

    def _safe_dispatch(self, event: MessageEvent | ErrorEvent) -> None:
        try:
            self.dispatchEvent(event)
        except Exception:
            return None
        return None

    def _dispatch_error(self, error: Exception) -> None:
        traceback_entry = traceback.extract_tb(error.__traceback__)[-1:]
        frame = traceback_entry[0] if traceback_entry else None
        event = ErrorEvent(
            "error",
            {
                "message": str(error),
                "filename": frame.filename if frame is not None else None,
                "lineno": frame.lineno if frame is not None else 0,
                "colno": frame.colno if frame is not None else 0,
                "error": error,
                "bubbles": False,
                "cancelable": True,
            },
        )
        self._safe_dispatch(event)

    def _dispatch_scope_messageerror(
        self, message: Any, error: Exception, source: Any, ports: list[Any]
    ) -> None:
        event = MessageEvent(
            "messageerror",
            {
                "data": message,
                "origin": "",
                "source": source,
                "ports": ports,
                "error": error,
                "bubbles": False,
                "cancelable": False,
            },
        )
        event.error = error
        self._inbound.put(event)

    def _dispatch_parent_messageerror(
        self, message: Any, error: Exception, source: Any, ports: list[Any]
    ) -> None:
        event = MessageEvent(
            "messageerror",
            {
                "data": message,
                "origin": "",
                "source": source,
                "ports": ports,
                "error": error,
                "bubbles": False,
                "cancelable": False,
            },
        )
        event.error = error
        self._safe_dispatch(event)

    def _post_from_scope(
        self, message: Any, transfer: list[Any] | dict[str, Any] | None = None
    ) -> None:
        if self.closed or self.terminated:
            return None
        ports = _transfer_list(transfer)
        try:
            data = _clone_message(message)
        except Exception as exc:
            self._dispatch_parent_messageerror(message, exc, self._scope, ports)
            return None
        event = MessageEvent(
            "message",
            {
                "data": data,
                "origin": "",
                "source": self._scope,
                "ports": ports,
                "bubbles": False,
                "cancelable": False,
            },
        )
        self._safe_dispatch(event)
        return None

    def _close_from_scope(self) -> None:
        self._scope._closed = True
        self._closed.set()
        self._clear_inbound()
        self._inbound.put(_STOP)
        return None

    def postMessage(
        self, message: Any, transfer: list[Any] | dict[str, Any] | None = None
    ) -> None:
        """Send a message to the worker's inner scope."""
        if self.closed or self.terminated:
            return None
        ports = _transfer_list(transfer)
        try:
            data = _clone_message(message)
        except Exception as exc:
            self._dispatch_scope_messageerror(message, exc, self, ports)
            return None
        event = MessageEvent(
            "message",
            {
                "data": data,
                "origin": "",
                "source": self,
                "ports": ports,
                "bubbles": False,
                "cancelable": False,
            },
        )
        self._inbound.put(event)
        return None

    def terminate(self) -> None:
        """Close the worker channel and discard pending work."""
        if self._terminated.is_set():
            return None
        self._terminated.set()
        self._scope._closed = True
        self._closed.set()
        self._clear_inbound()
        self._inbound.put(_STOP)
        return None

    def join(self, timeout: float | None = None) -> bool:
        """Wait for the worker thread to finish; return ``True`` when stopped."""
        self._thread.join(timeout)
        return not self._thread.is_alive()


__all__ = [
    "DedicatedWorkerGlobalScope",
    "Worker",
    "WorkerGlobalScope",
    "close",
    "get_current_worker_scope",
    "importScripts",
    "postMessage",
]
