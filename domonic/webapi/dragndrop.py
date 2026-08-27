"""
domonic.webapi.dragndrop
====================================
https://developer.mozilla.org/en-US/docs/Web/API/HTML_Drag_and_Drop_API
"""

from domonic.events import DragEvent
from domonic.webapi.file import File, FileList


class DataTransfer:
    def __init__(self):
        self.data = {}
        self.types = []
        self.files = FileList()
        self.items = DataTransferItemList(self)
        self.dropEffect = ""
        self.effectAllowed = ""
        self.dragImage = None
        self.dragImageX = 0
        self.dragImageY = 0
        self.dragElement = None

    @property
    def length(self) -> int:
        return len(self.data)

    def _sync_files_type(self) -> None:
        if self.files.length and "Files" not in self.types:
            self.types.append("Files")
        elif not self.files.length and "Files" in self.types:
            self.types.remove("Files")

    def clearData(self, type=None):
        if type is None:
            self.data = {}
            self.types = ["Files"] if self.files.length else []
            self.items[:] = [item for item in self.items if item.kind == "file"]
            return
        if type in self.data:
            self.data.pop(type, None)
        if type in self.types:
            self.types.remove(type)
        self.items[:] = [
            item
            for item in self.items
            if not (item.kind == "string" and item.type == type)
        ]

    def getData(self, type):
        return self.data.get(type, "")

    def setData(self, type, data):
        data = str(data)
        self.data[type] = data
        if type not in self.types:
            self.types.append(type)
        for item in self.items:
            if item.kind == "string" and item.type == type:
                item._data = data
                return
        list.append(self.items, DataTransferItem(data, type))

    def setDragImage(self, image, x, y):
        self.dragImage = image
        self.dragImageX = int(x)
        self.dragImageY = int(y)

    def addElement(self, element):
        self.dragElement = element
        return element

    def addFile(self, file):
        return self.items.add(file)


class DataTransferItem:
    def __init__(self, data, type: str | None = None):
        self.kind = "file" if isinstance(data, File) else "string"
        self.type = type or getattr(data, "type", "text/plain")
        self._data = data

    def getAsString(self, callback=None):
        if self.kind == "file":
            return None
        value = str(self._data)
        if callback is not None:
            callback(value)
        return value

    def getAsFile(self):
        return self._data if self.kind == "file" else None

    def getAsFileSystemHandle(self):
        return self.getAsFile()

    def webkitGetAsEntry(self):
        return self.getAsFile()


class DataTransferItemList(list):
    def __init__(self, owner: DataTransfer):
        super().__init__()
        self._owner = owner

    @property
    def length(self) -> int:
        return len(self)

    def add(self, data, type: str | None = None):
        item = data if isinstance(data, DataTransferItem) else DataTransferItem(data, type)
        self.append(item)
        if item.kind == "file":
            self._owner.files.append(item.getAsFile())
            self._owner._sync_files_type()
        else:
            self._owner.data[item.type] = item.getAsString()
            if item.type not in self._owner.types:
                self._owner.types.append(item.type)
        return item

    def clear(self):
        super().clear()
        self._owner.files = FileList()
        self._owner.data = {}
        self._owner.types = []

    def item(self, index: int):
        try:
            return self[int(index)]
        except (IndexError, TypeError, ValueError):
            return None

    def remove(self, index: int):
        try:
            item = self.pop(int(index))
        except (IndexError, TypeError, ValueError):
            return None
        if item.kind == "file":
            self._owner.files = FileList(
                file for file in self._owner.files if file is not item.getAsFile()
            )
            self._owner._sync_files_type()
        elif item.type in self._owner.data:
            self._owner.data.pop(item.type, None)
            if item.type in self._owner.types:
                self._owner.types.remove(item.type)
        return item
