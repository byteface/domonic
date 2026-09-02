"""
domonic.webapi.credentials
====================================
https://developer.mozilla.org/en-US/docs/Web/API/Credential_Management_API
"""

from __future__ import annotations

from typing import Any


def _create_promise():
    from domonic.javascript import Promise

    return Promise()


class Credential:
    """Base Credential Management API credential."""

    def __init__(self, id: str, type: str = "generic", **kwargs: Any) -> None:
        self.id = str(id)
        self.type = str(type)
        for key, value in kwargs.items():
            setattr(self, key, value)


class PasswordCredential(Credential):
    """Password credential with username, password, and optional display data."""

    def __init__(self, data: dict[str, Any]) -> None:
        super().__init__(
            data.get("id", data.get("name", "")),
            "password",
            name=data.get("name"),
            password=data.get("password"),
            iconURL=data.get("iconURL"),
        )


class FederatedCredential(Credential):
    """Federated credential for identity-provider backed sign-in."""

    def __init__(self, data: dict[str, Any]) -> None:
        super().__init__(
            data.get("id", ""),
            "federated",
            name=data.get("name"),
            provider=data.get("provider"),
            protocol=data.get("protocol"),
            iconURL=data.get("iconURL"),
        )


class CredentialsContainer:
    """In-memory Credential Management API container."""

    def __init__(self) -> None:
        self._credentials: dict[tuple[str, str], Credential] = {}
        self._silent_access_prevented = False

    def create(self, options: dict[str, Any] | None = None):
        """Return a Promise resolving with a new credential or ``None``."""
        options = options or {}
        credential: Credential | None = None
        if isinstance(options, Credential):
            credential = options
        elif "password" in options:
            credential = PasswordCredential(options["password"])
        elif "federated" in options:
            credential = FederatedCredential(options["federated"])
        return _create_promise().resolve(credential)

    def get(self, options: dict[str, Any] | None = None):
        """Return a Promise resolving with the matching credential or ``None``."""
        options = options or {}
        mediation = options.get("mediation")
        if self._silent_access_prevented and mediation in (None, "silent"):
            return _create_promise().resolve(None)

        wanted_id = options.get("id")
        wanted_types = []
        if options.get("password"):
            wanted_types.append("password")
        if options.get("federated"):
            wanted_types.append("federated")
        if not wanted_types:
            wanted_types = ["password", "federated", "generic"]

        for credential in self._credentials.values():
            if credential.type not in wanted_types:
                continue
            if wanted_id is not None and credential.id != str(wanted_id):
                continue
            return _create_promise().resolve(credential)
        return _create_promise().resolve(None)

    def preventSilentAccess(self):
        """Prevent future silent credential access and resolve an empty Promise."""
        self._silent_access_prevented = True
        return _create_promise().resolve(None)

    requireUserMediation = preventSilentAccess

    def store(self, credential: Credential):
        """Store a credential and return a Promise resolving with it."""
        if not isinstance(credential, Credential):
            raise TypeError("CredentialsContainer.store() expects a Credential")
        self._credentials[(credential.type, credential.id)] = credential
        self._silent_access_prevented = False
        return _create_promise().resolve(credential)
