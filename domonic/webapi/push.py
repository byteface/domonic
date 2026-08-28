"""
domonic.webapi.push
====================================
https://developer.mozilla.org/en-US/docs/Web/API/Push_API
"""

from __future__ import annotations

import base64
import secrets
import time
from typing import Any


def _base64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _coerce_key(value: Any) -> bytes | None:
    if value is None:
        return None
    if isinstance(value, bytes):
        return value
    if isinstance(value, bytearray):
        return bytes(value)
    if isinstance(value, memoryview):
        return value.tobytes()
    return str(value).encode("utf-8")


class PushSubscriptionOptions:
    """Options used to create a push subscription."""

    def __init__(
        self, userVisibleOnly: bool = False, applicationServerKey: Any = None
    ) -> None:
        self.userVisibleOnly = bool(userVisibleOnly)
        self.applicationServerKey = _coerce_key(applicationServerKey)


class PushSubscription:
    """Represents an application subscription to a push service."""

    def __init__(
        self,
        endpoint: str,
        options: PushSubscriptionOptions | dict[str, Any] | None = None,
        expirationTime: int | float | None = None,
        keys: dict[str, Any] | None = None,
        manager: "PushManager | None" = None,
    ) -> None:
        self.endpoint = str(endpoint)
        self.expirationTime = expirationTime
        self.options = (
            options
            if isinstance(options, PushSubscriptionOptions)
            else PushSubscriptionOptions(**(options or {}))
        )
        self._keys = {
            "p256dh": _coerce_key((keys or {}).get("p256dh")) or secrets.token_bytes(65),
            "auth": _coerce_key((keys or {}).get("auth")) or secrets.token_bytes(16),
        }
        self._manager = manager
        self._active = True

    def getKey(self, name: str) -> bytes | None:
        """Return a subscription key by name, usually ``p256dh`` or ``auth``."""
        key = self._keys.get(str(name))
        return bytes(key) if key is not None else None

    def toJSON(self) -> dict[str, Any]:
        """Return a JSON-serialisable subscription representation."""
        payload = {
            "endpoint": self.endpoint,
            "expirationTime": self.expirationTime,
            "keys": {name: _base64url(value) for name, value in self._keys.items()},
        }
        if self.options.applicationServerKey is not None:
            payload["options"] = {
                "userVisibleOnly": self.options.userVisibleOnly,
                "applicationServerKey": _base64url(self.options.applicationServerKey),
            }
        return payload

    def unsubscribe(self) -> bool:
        """Deactivate this subscription and detach it from its manager."""
        if not self._active:
            return False
        self._active = False
        if self._manager is not None and self._manager._subscription is self:
            self._manager._subscription = None
        return True


class PushManager:
    """Small in-memory Push API manager for modelling push subscriptions."""

    supportedContentEncodings = ["aes128gcm"]

    def __init__(self, permission: str = "prompt", endpoint_base: str | None = None):
        self.permission = permission
        self.endpoint_base = endpoint_base or "https://push.domonic.local"
        self._subscription: PushSubscription | None = None

    def getSubscription(self) -> PushSubscription | None:
        """Return the current subscription, if one exists."""
        return self._subscription

    def permissionState(self, options: dict[str, Any] | None = None) -> str:
        """Return ``granted``, ``denied`` or ``prompt`` for the current manager."""
        if self.permission not in {"granted", "denied", "prompt"}:
            return "prompt"
        return self.permission

    def subscribe(self, options: dict[str, Any] | None = None) -> PushSubscription:
        """Create and return a new push subscription."""
        if self.permissionState(options) == "denied":
            raise PermissionError("Push permission denied")

        subscription_options = PushSubscriptionOptions(**(options or {}))
        token = secrets.token_urlsafe(24)
        endpoint = f"{self.endpoint_base.rstrip('/')}/{token}"
        self._subscription = PushSubscription(
            endpoint,
            subscription_options,
            expirationTime=int(time.time() * 1000) + 90 * 24 * 60 * 60 * 1000,
            manager=self,
        )
        return self._subscription

    def unsubscribe(self) -> bool:
        """Unsubscribe the current subscription if one exists."""
        if self._subscription is None:
            return False
        return self._subscription.unsubscribe()


__all__ = ["PushManager", "PushSubscription", "PushSubscriptionOptions"]
