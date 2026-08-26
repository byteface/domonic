"""
domonic.webapi.webstorage
====================================
https://developer.mozilla.org/en-US/docs/Web/API/Storage

"""

import json
import os


class Storage:
    _reserved_attrs = {"storage", "filepath", "has_file"}

    def __init__(self, filepath: str | None = None) -> None:
        """Create an in-memory or JSON-backed Web Storage object.

        Args:
            filepath: Optional JSON file path used to persist values.
        """
        object.__setattr__(self, "storage", {})
        object.__setattr__(self, "has_file", False)
        if filepath:
            object.__setattr__(self, "filepath", filepath)
            object.__setattr__(self, "has_file", True)
            if os.path.exists(filepath):
                try:
                    with open(filepath, "r") as f:
                        data = json.load(f)
                except (json.JSONDecodeError, OSError):
                    data = {}
                if not isinstance(data, dict):
                    data = {}
                object.__setattr__(
                    self,
                    "storage",
                    {str(key): str(value) for key, value in data.items()},
                )
            else:
                parent = os.path.dirname(os.path.abspath(filepath))
                if parent:
                    os.makedirs(parent, exist_ok=True)
                with open(filepath, "w") as f:
                    json.dump(self.storage, f)

    def __getitem__(self, key: str) -> str | None:
        return self.getItem(key)

    def __setitem__(self, key: str, value: str) -> None:
        self.setItem(key, value)

    def __contains__(self, key: str) -> bool:
        return str(key) in self.storage

    def __iter__(self):
        return iter(self.storage)

    def __getattr__(self, key: str) -> str | None:
        return self.getItem(key)

    def __setattr__(self, key: str, value: str) -> None:
        if key in self._reserved_attrs:
            object.__setattr__(self, key, value)
            return None
        self.setItem(key, value)
        return None

    def __len__(self) -> int:
        return len(self.storage)

    @property
    def length(self) -> int:
        """Returns an integer representing the number of data items stored in the Storage object."""
        return len(self)

    def _save(self) -> None:
        if self.has_file:
            with open(self.filepath, "w") as f:
                json.dump(self.storage, f)
            return True
        return False

    def getItem(self, keyName: str) -> str | None:
        """Return the stored value for ``keyName`` or ``None``."""
        return self.storage.get(str(keyName), None)

    def setItem(self, keyName: str, value: str) -> None:
        """Store ``value`` under ``keyName`` using Web Storage string coercion."""
        self.storage[str(keyName)] = str(value)
        self._save()

    def key(self, index: int) -> str | None:
        """Return the key name at ``index`` or ``None`` when out of range."""
        try:
            return list(self.storage.keys())[int(index)]
        except (IndexError, TypeError, ValueError):
            return None

    def removeItem(self, keyName: str) -> None:
        """Remove ``keyName`` and its value from storage."""
        keyName = str(keyName)
        if keyName in self.storage:
            del self.storage[keyName]
            self._save()

    def clear(self) -> None:
        """Removes all items from the storage"""
        object.__setattr__(self, "storage", {})
        self._save()

    def keys(self):
        return self.storage.keys()

    def values(self):
        return self.storage.values()

    def items(self):
        return self.storage.items()

    def toJSON(self) -> dict[str, str]:
        return dict(self.storage)
