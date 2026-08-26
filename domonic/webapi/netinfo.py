"""
domonic.webapi.netinfo
====================================
https://developer.mozilla.org/en-US/docs/Web/API/Network_Information_API
"""

from __future__ import annotations

from typing import Any

from domonic.events import Event, EventTarget


class NetworkInformation(EventTarget):
    """Small mutable Network Information API object."""

    def __init__(self, options: dict[str, Any] | None = None):
        super().__init__()
        options = options or {}
        self.type = options.get("type", "unknown")
        self.downlinkMax = options.get("downlinkMax", None)
        self.effectiveType = options.get("effectiveType", "4g")
        self.rtt = options.get("rtt", 0)
        self.saveData = options.get("saveData", False)
        self.downlink = options.get("downlink", 10)
        self.onchange = None

    def update(self, **kwargs):
        """Update connection fields and dispatch ``change`` when anything changed."""
        changed = False
        for key, value in kwargs.items():
            if not hasattr(self, key):
                raise AttributeError(key)
            if getattr(self, key) != value:
                setattr(self, key, value)
                changed = True
        if changed:
            self.dispatchEvent(Event("change"))
        return self

    def __str__(self):
        return (
            "type: {}, downlinkMax: {}, effectiveType: {}, rtt: {}, "
            "saveData: {}, downlink: {}"
        ).format(
            self.type,
            self.downlinkMax,
            self.effectiveType,
            self.rtt,
            self.saveData,
            self.downlink,
        )
