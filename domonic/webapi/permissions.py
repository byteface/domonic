"""
domonic.webapi.permissions
====================================
https://developer.mozilla.org/en-US/docs/Web/API/Permissions
"""

from __future__ import annotations

from typing import Any

from domonic.events import Event, EventTarget

_VALID_STATES = {"granted", "denied", "prompt"}


def _permission_name(descriptor: Any) -> str:
    if isinstance(descriptor, str):
        return descriptor
    if isinstance(descriptor, dict):
        return str(descriptor.get("name", ""))
    return str(getattr(descriptor, "name", ""))


class PermissionStatus(EventTarget):
    """
    The PermissionStatus interface represents the current state of a permission.
    """

    def __init__(self, status="prompt", name: str | None = None):
        super().__init__()
        self.name = name
        self.onchange = None
        self.status = status

    def __str__(self):
        return self.status

    def __repr__(self):
        return self.status

    @property
    def state(self):
        """
        The state of the permission.
        state replaces status
        """
        return self.status

    @state.setter
    def state(self, value):
        if value not in _VALID_STATES:
            raise TypeError("Permission state must be granted, denied, or prompt")
        previous = getattr(self, "status", None)
        self.status = value
        if previous is not None and previous != value:
            self.dispatchEvent(Event("change"))


class Permissions:
    def __init__(self, defaults: dict[str, str] | None = None):
        self._states = dict(defaults or {})

    def query(self, PermissionDescriptor):
        """
        Return a PermissionStatus for the specified descriptor.
        """
        name = _permission_name(PermissionDescriptor)
        return PermissionStatus(self._states.get(name, "prompt"), name=name)

    def request(self, PermissionDescriptor):
        """
        Mark a permission as granted and return its PermissionStatus.
        """
        name = _permission_name(PermissionDescriptor)
        state = "denied" if not name else "granted"
        self._states[name] = state
        return PermissionStatus(state, name=name)

    def revoke(self, PermissionDescriptor):
        """Reset a permission to ``prompt`` and return its PermissionStatus."""
        name = _permission_name(PermissionDescriptor)
        self._states[name] = "prompt"
        return PermissionStatus("prompt", name=name)

    def requestAll(self, descriptors: list[Any] | None = None):
        """
        Request all supplied permissions and return a name-to-status mapping.
        """
        descriptors = descriptors or [{"name": name} for name in self._states]
        return {
            _permission_name(descriptor): self.request(descriptor)
            for descriptor in descriptors
        }

    def revokeAll(self):
        """Reset all known permissions to ``prompt``."""
        for name in list(self._states):
            self._states[name] = "prompt"
        return {name: PermissionStatus("prompt", name=name) for name in self._states}
