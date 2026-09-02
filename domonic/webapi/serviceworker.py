"""
domonic.dom.serviceworker
====================================
https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API
"""

from __future__ import annotations

from typing import Any
from urllib.parse import urljoin

from domonic.events import Event, EventTarget, MessageEvent


def _create_promise():
    from domonic.javascript import Promise

    return Promise()


def _scope_from_script(scriptURL: str) -> str:
    if "/" not in scriptURL:
        return "/"
    return scriptURL.rsplit("/", 1)[0] + "/"


class ServiceWorker(EventTarget):
    """Registered service worker script handle."""

    INSTALLING = "installing"
    INSTALLED = "installed"
    ACTIVATING = "activating"
    ACTIVATED = "activated"
    REDUNDANT = "redundant"

    def __init__(self, scriptURL: str, state: str = ACTIVATED) -> None:
        super().__init__()
        self.scriptURL = scriptURL
        self.state = state
        self.onstatechange = None
        self.onerror = None

    def postMessage(self, message, transfer=None) -> None:
        self.dispatchEvent(
            MessageEvent(
                "message",
                {"data": message, "source": self, "ports": transfer or []},
            )
        )
        return None

    def _set_state(self, state: str) -> None:
        if self.state == state:
            return None
        self.state = state
        self.dispatchEvent(Event("statechange"))
        return None


class ServiceWorkerRegistration(EventTarget):
    """Service worker registration for a scope."""

    def __init__(
        self,
        scope: str,
        scriptURL: str,
        container: "ServiceWorkerContainer | None" = None,
    ) -> None:
        super().__init__()
        self.scope = scope
        self.installing = None
        self.waiting = None
        self.active = ServiceWorker(scriptURL)
        self.onupdatefound = None
        self._container = container

    def update(self):
        self.installing = ServiceWorker(self.active.scriptURL, ServiceWorker.INSTALLING)
        self.dispatchEvent(Event("updatefound"))
        self.installing._set_state(ServiceWorker.INSTALLED)
        self.waiting = self.installing
        self.installing = None
        return _create_promise().resolve(self)

    def unregister(self):
        if self.active is not None:
            self.active._set_state(ServiceWorker.REDUNDANT)
        if self._container is not None:
            self._container._registrations.pop(self.scope, None)
            if self._container.controller is self.active:
                self._container.controller = None
        return _create_promise().resolve(True)


class ServiceWorkerContainer(EventTarget):
    """In-memory ServiceWorkerContainer implementation."""

    def __init__(self, baseURL: str = "https://eventual.technology/") -> None:
        super().__init__()
        self.controller: Any = None
        self.oncontrollerchange = None
        self.onmessage = None
        self.onmessageerror = None
        self._baseURL = baseURL
        self._registrations: dict[str, ServiceWorkerRegistration] = {}

    @property
    def ready(self):
        registration = next(iter(self._registrations.values()), None)
        return _create_promise().resolve(registration)

    def register(self, scriptURL: str, options: dict | None = None):
        options = options or {}
        absolute_script = urljoin(self._baseURL, scriptURL)
        scope = options.get("scope") or _scope_from_script(scriptURL)
        registration = ServiceWorkerRegistration(scope, absolute_script, self)
        self._registrations[scope] = registration
        previous = self.controller
        self.controller = registration.active
        if previous is not self.controller:
            self.dispatchEvent(Event("controllerchange"))
        return _create_promise().resolve(registration)

    def getRegistration(self, clientURL: str | None = None):
        if clientURL is None:
            registration = next(iter(self._registrations.values()), None)
        else:
            registration = None
            for scope, candidate in self._registrations.items():
                absolute_client = urljoin(self._baseURL, clientURL)
                absolute_scope = urljoin(self._baseURL, scope)
                if clientURL.startswith(scope) or absolute_client.startswith(
                    absolute_scope
                ):
                    registration = candidate
                    break
        return _create_promise().resolve(registration)

    def getRegistrations(self):
        return _create_promise().resolve(list(self._registrations.values()))

    def startMessages(self) -> None:
        return None

    def postMessage(self, message, transfer=None) -> None:
        if self.controller is not None:
            self.controller.postMessage(message, transfer)
        return None


__all__ = [
    "ServiceWorker",
    "ServiceWorkerContainer",
    "ServiceWorkerRegistration",
]
