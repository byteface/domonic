"""
domonic.webapi.notifications
====================================
https://developer.mozilla.org/en-US/docs/Web/API/Notifications_API
"""

from __future__ import annotations

import time
from typing import Any

from domonic.events import Event, EventTarget


def _create_promise():
    from domonic.javascript import Promise

    return Promise()


class Notification(EventTarget):
    """Browser-style notification object without platform side effects."""

    permission = "default"
    maxActions = 2

    def __init__(self, title: str, options: dict[str, Any] | None = None) -> None:
        super().__init__()
        options = dict(options or {})
        self.title = str(title)
        self.dir = str(options.get("dir", "auto"))
        self.lang = str(options.get("lang", ""))
        self.body = str(options.get("body", ""))
        self.tag = str(options.get("tag", ""))
        self.icon = str(options.get("icon", ""))
        self.badge = str(options.get("badge", ""))
        self.image = str(options.get("image", ""))
        self.data = options.get("data")
        self.vibrate = options.get("vibrate")
        self.timestamp = int(options.get("timestamp", time.time() * 1000))
        self.renotify = bool(options.get("renotify", False))
        self.requireInteraction = bool(options.get("requireInteraction", False))
        self.silent = bool(options.get("silent", False))
        self.actions = list(options.get("actions", []))[: self.maxActions]
        self.onclick = None
        self.onclose = None
        self.onerror = None
        self.onshow = None
        self.closed = False

    @classmethod
    def requestPermission(cls, callback=None, permission: str | None = None):
        """Resolve with the configured permission."""
        if permission is None:
            permission = "granted" if cls.permission == "default" else cls.permission
        cls.setPermission(permission)
        if callback is not None:
            callback(cls.permission)
        return _create_promise().resolve(cls.permission)

    @classmethod
    def setPermission(cls, permission: str) -> str:
        if permission not in {"default", "granted", "denied"}:
            raise ValueError(
                "Notification permission must be default, granted, or denied"
            )
        cls.permission = permission
        return cls.permission

    def show(self) -> bool:
        if self.permission == "denied":
            self.dispatchEvent(Event("error"))
            return False
        self.closed = False
        self.dispatchEvent(Event("show"))
        return True

    def close(self) -> None:
        if not self.closed:
            self.closed = True
            self.dispatchEvent(Event("close"))
        return None

    def click(self) -> None:
        self.dispatchEvent(Event("click"))
        return None

    def toJSON(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "body": self.body,
            "tag": self.tag,
            "data": self.data,
            "timestamp": self.timestamp,
            "silent": self.silent,
            "closed": self.closed,
        }


__all__ = ["Notification"]
