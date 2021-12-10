"""
    domonic.webapi.webstorage
    ====================================
    https://developer.mozilla.org/en-US/docs/Web/API/Storage
    
    TODO - add more than just json as options.
    TODO - i dont believe there's any unit tests for this.
    
"""

import os
import json

from domonic.events import StorageEvent


class Storage():

    def __init__(self, filepath: str=None) -> None:
        """[localstorage. destroys on each session unless you pass the optional filepath]

        Args:
            filepath ([str], optional): [filepath]. give us a file to write to
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

    def __getitem__(self, key: str) -> str:
        return self.storage[key]
    getItem = __getitem__

    def __setitem__(self, key: str, value: str) -> None:
        self.storage[key] = value
        if self.has_file:
            self._save()
    setItem = __setitem__
    
    def __getattr__(self, key: str) -> str:
        return self.storage.get(key, None)
    
    def __setattr__(self, key: str, value: str) -> None:
        if key == 'storage':
            self.__dict__[key] = value  # TODO - tests required. not sure this is correct. shouldn't it be self.storage = value?
        else:
            self.storage[key] = value
            self._save()

    def __len__(self) -> int:
        return len(self.storage.keys())

    @property
    def length(self) -> int:
        """ Returns an integer representing the number of data items stored in the Storage object. """
        return len(self)

    def _save(self) -> None:
        if self.has_file:
            with open(self.filepath, 'w') as f:
                json.dump(self.storage, f)
            return True
        return False

    def key(self, keyName: str) -> str:
        """[returns the value of the key or None if the key does not exist]

        Args:
            keyName (str): [key to get]

        Returns:
            str: [the key or None]
        """
        return self.storage.get(keyName, None)

    def removeItem(self, keyName: str) -> None:
        """[removes the key and its value from the storage]

        Args:
            keyName (str): [key to remove]
        """
        if keyName in self.storage:
            del self.storage[keyName]
            self._save()

    def clear(self) -> None:
        """ Removes all items from the storage """
        self.storage = {}
        self._save()
