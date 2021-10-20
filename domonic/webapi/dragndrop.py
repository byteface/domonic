"""
    domonic.webapi.dragndrop
    ====================================
    https://developer.mozilla.org/en-US/docs/Web/API/HTML_Drag_and_Drop_API
"""

from domonic.events import DragEvent


class DataTransfer:

    def __init__(self):
        self.data = {}
        self.types = []
        self.files = []
        self.items = []
        self.dropEffect = ""
        self.effectAllowed = ""

    def clearData(self, type):
        self.data[type] = ""
        self.types.remove(type)

    def getData(self, type):
        return self.data[type]

    def setData(self, type, data):
        self.data[type] = data
        self.types.append(type)

    def setDragImage(self, image, x, y):
        pass

    def addElement(self, element):
        self.items.append(element)

    # def addFile(self, file):
    #     self.files.append(file)


# class DataTransferItem:

#     def __init__(self, type, data):
#         self.type = type
#         self.data = data

#     def getAsString(self):
#         return self.data

#     def getAsFile(self):
#         return self.data

#     def getAsFileSystemHandle(self):
#         return self.data

#     def webkitGetAsEntry(self):
#         return self.data
