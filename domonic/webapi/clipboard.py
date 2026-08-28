"""
domonic.webapi.clipboard
====================================

https://developer.mozilla.org/en-US/docs/Web/API/Clipboard

"""

from __future__ import annotations

import sys
from copy import deepcopy
from typing import Any

mac = sys.platform == "darwin"
windows = sys.platform == "win32"
linux = sys.platform == "linux"

try:
    import pyperclip
except ImportError:  # pragma: no cover - optional dependency
    pyperclip = None


_clipboard_fallback: dict[str, Any] = {"text/plain": ""}


class ClipboardItem:
    """Container for clipboard data keyed by MIME type."""

    def __init__(self, items: dict[str, Any], options: dict[str, Any] | None = None):
        options = options or {}
        self._items = dict(items)
        self.presentationStyle = options.get("presentationStyle", "unspecified")

    @property
    def types(self) -> list[str]:
        return list(self._items.keys())

    def getType(self, type: str) -> Any:
        if type not in self._items:
            raise KeyError(type)
        return self._items[type]

    @staticmethod
    def supports(type: str) -> bool:
        return type in {
            "text/plain",
            "text/html",
            "image/png",
            "image/jpeg",
            "image/gif",
            "application/octet-stream",
        }


class Clipboard:
    """
    Read and write text, HTML, image, buffer, and MIME-keyed clipboard data.
    """

    def __init__(self):
        self._data = _clipboard_fallback

    def writeText(self, data):
        """
        Writes the given text to the clipboard.
        """
        text = str(data)
        self._write_type("text/plain", text)
        if pyperclip is not None:
            try:
                pyperclip.copy(text)
            except Exception:
                return text
        return text

    def readText(self):
        if pyperclip is not None:
            try:
                return pyperclip.paste()
            except Exception:
                return self._read_type("text/plain", "")
        return self._read_type("text/plain", "")

    def write(self, data):
        if isinstance(data, ClipboardItem):
            data = [data]
        if isinstance(data, (list, tuple)):
            merged = {}
            for item in data:
                if isinstance(item, ClipboardItem):
                    for mime_type in item.types:
                        merged[mime_type] = item.getType(mime_type)
                elif isinstance(item, dict):
                    merged.update(item)
                else:
                    raise TypeError(
                        "Clipboard.write() expects ClipboardItem or dict items"
                    )
            self._data.clear()
            self._data.update(deepcopy(merged))
            return data
        if isinstance(data, dict):
            self._data.clear()
            self._data.update(deepcopy(data))
            return data
        return self.writeText(data)

    def read(self):
        return [ClipboardItem(deepcopy(self._data))]

    def writeHTML(self, data):
        return self._write_type("text/html", str(data))

    def readHTML(self):
        return self._read_type("text/html", "")

    def writeImage(self, data):
        return self._write_type("image/png", data)

    def readImage(self):
        return self._read_type("image/png", None)

    def writeBuffer(self, data):
        return self._write_type("application/octet-stream", bytes(data))

    def readBuffer(self):
        return self._read_type("application/octet-stream", b"")

    def writeData(self, data, type: str = "text/plain"):
        if type == "text/plain":
            return self.writeText(data)
        return self._write_type(type, data)

    def readData(self, type: str = "text/plain"):
        if type == "text/plain":
            return self.readText()
        return self._read_type(type, None)

    def _write_type(self, type: str, data):
        self._data[type] = data
        return data

    def _read_type(self, type: str, default=None):
        return self._data.get(type, default)


# class ClipboardData:
#     def __init__(self):
#         self.data = None
