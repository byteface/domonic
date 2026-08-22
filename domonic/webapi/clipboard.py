"""
domonic.webapi.clipboard
====================================

TODO - make this clipboard same as the webapi and make it work for linux, mac and windows

https://developer.mozilla.org/en-US/docs/Web/API/Clipboard

"""

import sys

mac = sys.platform == "darwin"
windows = sys.platform == "win32"
linux = sys.platform == "linux"

try:
    import pyperclip
except ImportError:  # pragma: no cover - optional dependency
    pyperclip = None


_clipboard_fallback = ""


class Clipboard:
    """
    The Clipboard API provides the ability to respond to clipboard commands (cut, copy, and paste) as well as to asynchronously read from and write to the system clipboard.
    """

    def __init__(self):
        pass

    def writeText(self, data):
        """
        Writes the given text to the clipboard.
        """
        global _clipboard_fallback
        _clipboard_fallback = data
        if pyperclip is not None:
            pyperclip.copy(data)
        return data

    def readText(self):
        if pyperclip is not None:
            return pyperclip.paste()
        return _clipboard_fallback

    def write(self, data):
        return self.writeText(data)

    def read(self):
        return self.readText()

    def writeHTML(self, data):
        pass

    def readHTML(self):
        pass

    def writeImage(self, data):
        pass

    def readImage(self):
        pass

    def writeBuffer(self, data):
        pass

    def readBuffer(self):
        pass

    def writeData(self, data):
        return self.writeText(data)

    def readData(self):
        return self.readText()


# class ClipboardData:
#     def __init__(self):
#         self.data = None
