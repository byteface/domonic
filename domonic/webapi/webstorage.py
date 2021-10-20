"""
    domonic.webapi.webstorage
    ====================================
    https://developer.mozilla.org/en-US/docs/Web/API/Storage
"""

from domonic.events import StorageEvent


class Storage():

    def __init__(self, filepath=None):
        """[localstorage. destroys on each session unless you pass the optional filepath]

        Args:
            filepath ([type], optional): [filepath]. give us a file to write to
        """
        self.storage = {}
        self.has_file = False
        if filepath:
            self.filepath = filepath
            self.has_file = True
        # check if file exists. if so load it in . if not create it
        if filepath:
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    self.storage = json.load(f)
            else:
                with open(filepath, 'w') as f:
                    json.dump(self.storage, f)

    def __getitem__(self, key):
        return self.storage[key]

    def __setitem__(self, key, value):
        self.storage[key] = value
        if self.has_file:
            self._save()

    def __len__(self):
        return len(self.storage.keys())

    @property
    def length(self):
        """ Returns an integer representing the number of data items stored in the Storage object. """
        return len(self.storage.keys())

    def _save(self):
        if self.has_file:
            with open(self.filepath, 'w') as f:
                json.dump(self.storage, f)
            return True
        return False

    def setItem(self, keyName, keyValue):
        """ Adds that key to the storage, or update that key's value if it already exists """
        self.storage[keyName] = keyValue
        self._update_file()

    def getItem(self, keyName):
        """ Returns the value of the specified key name Storage """
        return self.storage.get(keyName, None)

    def key(self, keyName):
        """ Returns the value of the key if it exists, otherwise returns None """
        return self.storage.get(keyName, None)

    def removeItem(self, keyName):
        """ Removes the key and its value from the storage """
        if keyName in self.storage:
            del self.storage[keyName]
            self._update_file()

    def clear(self):
        """ Removes all items from the storage """
        self.storage = {}
        