"""
domonic.webapi.file
====================================
https://developer.mozilla.org/en-US/docs/Web/API/File_API
"""

from __future__ import annotations

import base64
import mimetypes
import os
import time
import urllib.parse
import uuid
from collections.abc import Iterable
from contextlib import suppress
from typing import Any

from domonic.dom import DOMException
from domonic.events import Event, EventTarget, ProgressEvent


def _normalize_type(content_type: Any = "") -> str:
    content_type = str(content_type or "").strip().lower()
    if any(ord(char) < 0x20 or ord(char) > 0x7E for char in content_type):
        return ""
    return content_type


def _to_bytes(part: Any, endings: str = "transparent") -> bytes:
    if isinstance(part, Blob):
        return part.bytes()
    if isinstance(part, str):
        if endings == "native":
            part = part.replace("\r\n", "\n").replace("\n", "\n")
        return part.encode("utf-8")
    if isinstance(part, bytes):
        return part
    if isinstance(part, bytearray):
        return bytes(part)
    if isinstance(part, memoryview):
        return part.tobytes()
    if hasattr(part, "byteLength") and hasattr(part, "__getitem__"):
        return bytes(part[index] for index in range(part.byteLength))
    if hasattr(part, "buffer"):
        buffer = part.buffer
        if isinstance(buffer, bytes):
            return buffer
        if isinstance(buffer, bytearray):
            return bytes(buffer)
        if isinstance(buffer, memoryview):
            return buffer.tobytes()
        with suppress(TypeError):
            return bytes(buffer)
    if hasattr(part, "read"):
        data = part.read()
        return _to_bytes(data, endings)
    return str(part).encode("utf-8")


class Blob:
    """Immutable file-like byte sequence."""

    def __init__(
        self, blobParts: Iterable[Any] | None = None, options: dict[str, Any] | None = None
    ) -> None:
        options = dict(options or {})
        endings = options.get("endings", "transparent")
        self._buffer = b"".join(_to_bytes(part, endings) for part in (blobParts or []))
        self.type = _normalize_type(options.get("type", ""))

    @property
    def size(self) -> int:
        return len(self._buffer)

    def arrayBuffer(self) -> bytes:
        return self._buffer

    def bytes(self) -> bytes:
        return self._buffer

    def text(self, encoding: str = "utf-8", errors: str = "replace") -> str:
        return self._buffer.decode(encoding, errors)

    def slice(
        self, start: int | None = None, end: int | None = None, contentType: str = ""
    ) -> "Blob":
        size = self.size
        relative_start = 0 if start is None else int(start)
        relative_end = size if end is None else int(end)

        if relative_start < 0:
            relative_start = max(size + relative_start, 0)
        else:
            relative_start = min(relative_start, size)

        if relative_end < 0:
            relative_end = max(size + relative_end, 0)
        else:
            relative_end = min(relative_end, size)

        span = max(relative_end - relative_start, 0)
        return Blob(
            [self._buffer[relative_start : relative_start + span]],
            {"type": contentType},
        )

    def stream(self):
        from domonic.webapi.streams import ReadableStream

        return ReadableStream(lambda: self._buffer)

    def __bytes__(self) -> bytes:
        return self._buffer

    def __len__(self) -> int:
        return self.size

    def __repr__(self) -> str:
        return f"<Blob size={self.size} type={self.type!r}>"


class File(Blob):
    """A named ``Blob`` with last-modified metadata."""

    def __init__(
        self,
        fileBits: Iterable[Any] | None = None,
        fileName: str = "",
        options: dict[str, Any] | None = None,
    ) -> None:
        options = dict(options or {})
        fileName = str(fileName).replace("/", ":").replace("\\", ":")
        guessed_type = mimetypes.guess_type(fileName)[0] or ""
        if "type" not in options and guessed_type:
            options["type"] = guessed_type
        super().__init__(fileBits, options)
        self.name = fileName
        self.lastModified = int(options.get("lastModified", time.time() * 1000))
        self.webkitRelativePath = str(options.get("webkitRelativePath", ""))

    @property
    def lastModifiedDate(self):
        from datetime import datetime, timezone

        return datetime.fromtimestamp(self.lastModified / 1000, timezone.utc)

    @classmethod
    def fromPath(
        cls,
        path: str,
        *,
        name: str | None = None,
        type: str | None = None,
        lastModified: int | None = None,
    ) -> "File":
        with open(path, "rb") as handle:
            data = handle.read()
        options: dict[str, Any] = {}
        if type is not None:
            options["type"] = type
        if lastModified is not None:
            options["lastModified"] = lastModified
        return cls([data], name or os.path.basename(path), options)

    def __repr__(self) -> str:
        return f"<File name={self.name!r} size={self.size} type={self.type!r}>"


class FileList(list):
    """Array-like list of ``File`` objects."""

    def __init__(self, files: Iterable[File] | None = None) -> None:
        super().__init__(files or [])

    @property
    def length(self) -> int:
        return len(self)

    def item(self, index: int) -> File | None:
        try:
            return self[int(index)]
        except (IndexError, TypeError, ValueError):
            return None


class FileReader(EventTarget):
    """EventTarget-based reader for ``Blob`` and ``File`` contents."""

    EMPTY = 0
    LOADING = 1
    DONE = 2

    def __init__(self) -> None:
        super().__init__()
        self.readyState = self.EMPTY
        self.result: Any = None
        self.error: Any = None
        self.onloadstart = None
        self.onprogress = None
        self.onload = None
        self.onabort = None
        self.onerror = None
        self.onloadend = None

    def _dispatch(self, event_type: str, **options: Any) -> None:
        self.dispatchEvent(ProgressEvent(event_type, options))

    def _read(self, blob: Blob, producer) -> None:
        if self.readyState == self.LOADING:
            raise DOMException(DOMException.INVALID_STATE_ERR, "FileReader is loading")
        if not isinstance(blob, Blob):
            blob = Blob([blob])

        self.readyState = self.LOADING
        self.result = None
        self.error = None
        self._dispatch("loadstart", loaded=0, total=blob.size, lengthComputable=True)

        try:
            self.result = producer(blob)
            self._dispatch(
                "progress",
                loaded=blob.size,
                total=blob.size,
                lengthComputable=True,
            )
            self.readyState = self.DONE
            self._dispatch("load", loaded=blob.size, total=blob.size, lengthComputable=True)
        except Exception as exc:
            self.error = exc
            self.readyState = self.DONE
            self._dispatch("error", loaded=0, total=blob.size, lengthComputable=True)
        finally:
            self._dispatch(
                "loadend",
                loaded=blob.size,
                total=blob.size,
                lengthComputable=True,
            )

    def abort(self) -> None:
        if self.readyState != self.LOADING:
            self.result = None
            return
        self.result = None
        self.readyState = self.DONE
        self._dispatch("abort")
        self._dispatch("loadend")

    def readAsArrayBuffer(self, blob: Blob) -> None:
        self._read(blob, lambda value: value.arrayBuffer())

    def readAsBinaryString(self, blob: Blob) -> None:
        self._read(blob, lambda value: value.bytes().decode("latin-1"))

    def readAsText(self, blob: Blob, encoding: str = "utf-8") -> None:
        self._read(blob, lambda value: value.text(encoding))

    def readAsDataURL(self, blob: Blob) -> None:
        def producer(value: Blob) -> str:
            content_type = value.type or "application/octet-stream"
            payload = base64.b64encode(value.bytes()).decode("ascii")
            return f"data:{content_type};base64,{payload}"

        self._read(blob, producer)


class FileReaderSync:
    """Synchronous reader matching the worker-only browser API."""

    def readAsArrayBuffer(self, blob: Blob) -> bytes:
        return blob.arrayBuffer()

    def readAsBinaryString(self, blob: Blob) -> str:
        return blob.bytes().decode("latin-1")

    def readAsText(self, blob: Blob, encoding: str = "utf-8") -> str:
        return blob.text(encoding)

    def readAsDataURL(self, blob: Blob) -> str:
        content_type = blob.type or "application/octet-stream"
        payload = base64.b64encode(blob.bytes()).decode("ascii")
        return f"data:{content_type};base64,{payload}"


class _ObjectURLStore:
    _objects: dict[str, Blob] = {}

    @classmethod
    def create(cls, blob: Blob) -> str:
        if not isinstance(blob, Blob):
            raise TypeError("URL.createObjectURL() expects a Blob or File")
        object_url = f"blob:domonic/{uuid.uuid4()}"
        cls._objects[object_url] = blob
        return object_url

    @classmethod
    def revoke(cls, object_url: str) -> None:
        cls._objects.pop(str(object_url), None)

    @classmethod
    def get(cls, object_url: str) -> Blob | None:
        return cls._objects.get(str(object_url))


def createObjectURL(blob: Blob) -> str:
    return _ObjectURLStore.create(blob)


def revokeObjectURL(object_url: str) -> None:
    _ObjectURLStore.revoke(object_url)


def resolveObjectURL(object_url: str) -> Blob | None:
    return _ObjectURLStore.get(object_url)


def parse_data_url(url: str) -> Blob | None:
    if not str(url).startswith("data:"):
        return None
    header, _, data = str(url)[5:].partition(",")
    if not _:
        return None
    media_type, *params = header.split(";") if header else [""]
    if any(param.lower() == "base64" for param in params):
        payload = base64.b64decode(data)
    else:
        payload = urllib.parse.unquote_to_bytes(data)
    return Blob([payload], {"type": media_type})
