"""
domonic.webapi.cookiestore
====================================
https://developer.mozilla.org/en-US/docs/Web/API/Cookie_Store_API
"""

from __future__ import annotations

import time
from typing import Any

from domonic.events import Event, EventTarget


def _create_promise():
    from domonic.javascript import Promise

    return Promise()


class CookieListItem(dict):
    """Dictionary-like Cookie Store API item with attribute access."""

    def __init__(self, name: str, value: str = "", **kwargs: Any) -> None:
        super().__init__(name=str(name), value=str(value), **kwargs)
        self.__dict__ = self


class CookieChangeEvent(Event):
    """Event fired when cookies are changed or deleted."""

    def __init__(
        self,
        _type: str = "change",
        options: dict[str, Any] | None = None,
    ) -> None:
        options = options or {}
        self.changed = options.get("changed", [])
        self.deleted = options.get("deleted", [])
        super().__init__(_type, options)


class CookieStore(EventTarget):
    """In-memory Cookie Store API backed by a dictionary."""

    def __init__(self, store: dict[str, Any] | None = None) -> None:
        super().__init__()
        self.onchange = None
        self._store = store if store is not None else {}

    def get(self, name_or_options: str | dict[str, Any]):
        """Return a Promise resolving with the first matching cookie or ``None``."""
        name = self._name_from(name_or_options)
        item = self._item(name) if name in self._store else None
        return _create_promise().resolve(item)

    def getAll(self, name_or_options: str | dict[str, Any] | None = None):
        """Return a Promise resolving with all matching cookies."""
        if name_or_options is None:
            items = [self._item(name) for name in self._store]
        else:
            name = self._name_from(name_or_options)
            items = [self._item(name)] if name in self._store else []
        return _create_promise().resolve(items)

    def set(self, name_or_options: str | dict[str, Any], value: str | None = None):
        """Set a cookie and return a resolved Promise."""
        item = self._coerce_item(name_or_options, value)
        self._store[item["name"]] = dict(item)
        self.dispatchEvent(CookieChangeEvent("change", {"changed": [item]}))
        return _create_promise().resolve(None)

    def delete(self, name_or_options: str | dict[str, Any]):
        """Delete a cookie by name and return a resolved Promise."""
        name = self._name_from(name_or_options)
        deleted = []
        if name in self._store:
            deleted.append(self._item(name))
            del self._store[name]
        if deleted:
            self.dispatchEvent(CookieChangeEvent("change", {"deleted": deleted}))
        return _create_promise().resolve(None)

    def _coerce_item(
        self, name_or_options: str | dict[str, Any], value: str | None
    ) -> CookieListItem:
        if isinstance(name_or_options, dict):
            data = dict(name_or_options)
            name = data.pop("name")
            cookie_value = data.pop("value", value if value is not None else "")
        else:
            data = {}
            name = name_or_options
            cookie_value = "" if value is None else value
        return CookieListItem(
            name,
            cookie_value,
            domain=data.get("domain"),
            expires=data.get("expires"),
            path=data.get("path", "/"),
            sameSite=data.get("sameSite", "strict"),
            secure=bool(data.get("secure", False)),
            partitioned=bool(data.get("partitioned", False)),
            created=data.get("created", time.time()),
        )

    @staticmethod
    def _name_from(name_or_options: str | dict[str, Any]) -> str:
        if isinstance(name_or_options, dict):
            return str(name_or_options.get("name", ""))
        return str(name_or_options)

    def _item(self, name: str) -> CookieListItem:
        raw = self._store[name]
        if isinstance(raw, dict):
            data = dict(raw)
            return CookieListItem(data.pop("name", name), data.pop("value", ""), **data)
        return CookieListItem(name, raw)


__all__ = ["CookieChangeEvent", "CookieListItem", "CookieStore"]
