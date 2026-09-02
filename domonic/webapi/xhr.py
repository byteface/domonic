"""
domonic.webapi.XMLHttpRequest
====================================
https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest
"""

from __future__ import annotations

import json
import urllib.parse
from types import SimpleNamespace
from typing import Any, Callable, Iterable

from domonic.javascript import Global
from domonic.webapi.fetch import Headers


class XMLHttpRequest:
    """Small synchronous XMLHttpRequest implementation backed by requests."""

    UNSENT = 0
    OPENED = 1
    HEADERS_RECEIVED = 2
    LOADING = 3
    DONE = 4

    def __init__(
        self,
        url: str | None = None,
        responseType: str | None = "",
        withCredentials: bool = False,
        timeout: int = 0,
        onload: Callable[..., Any] | None = None,
        onerror: Callable[..., Any] | None = None,
        onprogress: Callable[..., Any] | None = None,
        ontimeout: Callable[..., Any] | None = None,
        onreadystatechange: Callable[..., Any] | None = None,
        onabort: Callable[..., Any] | None = None,
        onloadend: Callable[..., Any] | None = None,
        onloadstart: Callable[..., Any] | None = None,
    ) -> None:
        self.url = url or ""
        self.method = "GET"
        self.async_ = True
        self.user: str | None = None
        self.password: str | None = None
        self.responseType = responseType or ""
        self.withCredentials = withCredentials
        self.timeout = timeout
        self.onload = onload
        self.onerror = onerror
        self.onprogress = onprogress
        self.ontimeout = ontimeout
        self.onreadystatechange = onreadystatechange
        self.onabort = onabort
        self.onloadend = onloadend
        self.onloadstart = onloadstart
        self.readyState = self.UNSENT
        self.response = None
        self.responseText = ""
        self.responseURL = ""
        self.responseXML = None
        self.status = 0
        self.statusText = ""
        self.upload = SimpleNamespace()
        self._request_headers = Headers()
        self._response_headers = Headers()
        self._listeners: dict[str, list[Callable[[Any], Any]]] = {}
        self._aborted = False
        self._override_mime_type: str | None = None

    def addEventListener(self, event_type: str, callback: Callable[[Any], Any]) -> None:
        self._listeners.setdefault(str(event_type), []).append(callback)

    def removeEventListener(
        self, event_type: str, callback: Callable[[Any], Any]
    ) -> None:
        listeners = self._listeners.get(str(event_type), [])
        if callback in listeners:
            listeners.remove(callback)

    def _event(self, event_type: str, **kwargs: Any) -> SimpleNamespace:
        event = SimpleNamespace(type=event_type, target=self, currentTarget=self)
        for key, value in kwargs.items():
            setattr(event, key, value)
        return event

    def _dispatch(self, event_type: str, **kwargs: Any) -> None:
        event = self._event(event_type, **kwargs)
        handler = getattr(self, "on" + event_type, None)
        if callable(handler):
            handler(event)
        for callback in list(self._listeners.get(event_type, [])):
            callback(event)

    def _set_ready_state(self, ready_state: int) -> None:
        self.readyState = ready_state
        self._dispatch("readystatechange")

    def open(
        self,
        method: str,
        url: str,
        async_: bool = True,
        user: str | None = None,
        password: str | None = None,
    ) -> None:
        self.method = str(method or "GET").upper()
        self.url = str(url)
        self.async_ = async_
        self.user = user
        self.password = password
        self._aborted = False
        self.response = None
        self.responseText = ""
        self.status = 0
        self.statusText = ""
        self._response_headers = Headers()
        self._set_ready_state(self.OPENED)

    def setRequestHeader(self, name: str, value: Any) -> None:
        if self.readyState != self.OPENED:
            raise RuntimeError("setRequestHeader() must be called after open()")
        self._request_headers.append(name, value)

    def getResponseHeader(self, name: str) -> str | None:
        return self._response_headers.get(name)

    def getAllResponseHeaders(self) -> str:
        return "\r\n".join(
            f"{name}: {value}" for name, value in self._response_headers.entries()
        )

    def overrideMimeType(self, mime: str) -> None:
        self._override_mime_type = str(mime)

    def abort(self) -> None:
        self._aborted = True
        self.status = 0
        self.statusText = ""
        self.response = None
        self.responseText = ""
        self._set_ready_state(self.DONE)
        self._dispatch("abort")
        self._dispatch("loadend")

    def _coerce_response(self, response: Any) -> Any:
        content = getattr(response, "content", None)
        text = getattr(response, "text", None)
        if content is None and text is not None:
            content = str(text).encode("utf-8")
        if text is None and content is not None:
            text = bytes(content).decode(getattr(response, "encoding", None) or "utf-8")

        response_type = self.responseType or "text"
        if response_type == "json":
            return json.loads(text or "null")
        if response_type in ("arraybuffer", "blob"):
            return content or b""
        if response_type == "document":
            try:
                from domonic import domonic

                return domonic.parseString(text or "")
            except Exception:
                return text or ""
        return text or ""

    def send(self, body: Any = None, **kwargs: Any) -> None:
        if self.readyState != self.OPENED:
            raise RuntimeError("send() must be called after open()")
        if self._aborted:
            return

        self._dispatch("loadstart")
        timeout_seconds = (
            self.timeout / 1000 if self.timeout else kwargs.pop("timeout", None)
        )
        try:
            import requests

            response = requests.request(
                self.method,
                self.url,
                data=body,
                headers=self._request_headers.toObject(),
                timeout=timeout_seconds,
                auth=(self.user, self.password) if self.user is not None else None,
                **kwargs,
            )
            if self._aborted:
                return

            self.responseURL = getattr(response, "url", self.url)
            self.status = int(getattr(response, "status_code", 0) or 0)
            self.statusText = str(getattr(response, "reason", "") or "")
            self._response_headers = Headers(getattr(response, "headers", None))
            self._set_ready_state(self.HEADERS_RECEIVED)
            self._set_ready_state(self.LOADING)

            self.response = self._coerce_response(response)
            self.responseText = self.response if isinstance(self.response, str) else ""
            loaded = len(getattr(response, "content", b"") or self.responseText)
            self._dispatch(
                "progress", loaded=loaded, total=loaded, lengthComputable=True
            )
            self._set_ready_state(self.DONE)
            self._dispatch("load")
            self._dispatch("loadend")
        except TimeoutError as exc:
            self._set_ready_state(self.DONE)
            self._dispatch("timeout", error=exc)
            self._dispatch("loadend")
        except Exception as exc:
            self._set_ready_state(self.DONE)
            self._dispatch("error", error=exc)
            self._dispatch("loadend")


class FormData:
    """Python representation of the browser FormData collection."""

    def __init__(self, form: Any = None):
        self._entries: list[tuple[str, Any, str | None]] = []
        self._formobj = None
        if form is None:
            return

        if isinstance(form, str):
            import domonic

            page = domonic.domonic.parseString(form)
            form = page.querySelector("form") if page is not None else None
        if form is None:
            return
        if getattr(form, "nodeName", "").lower() != "form":
            raise TypeError("FormData requires a form element or form HTML string")

        self._formobj = form
        self._parse_form(form)

    @staticmethod
    def _control_name(control: Any) -> str | None:
        getter = getattr(control, "getAttribute", None)
        name = getter("name") if callable(getter) else getattr(control, "name", None)
        if name in (None, ""):
            return None
        return str(name)

    @staticmethod
    def _control_value(control: Any) -> Any:
        getter = getattr(control, "getAttribute", None)
        value = getter("value") if callable(getter) else None
        if value is None:
            value = getattr(control, "value", None)
        if value is None:
            value = getattr(control, "nodeValue", None)
        return value

    @staticmethod
    def _control_type(control: Any) -> str:
        getter = getattr(control, "getAttribute", None)
        value = getter("type") if callable(getter) else getattr(control, "type", "")
        return str(value or "").lower()

    @staticmethod
    def _is_checked(control: Any) -> bool:
        getter = getattr(control, "getAttribute", None)
        checked = (
            getter("checked") if callable(getter) else getattr(control, "checked", None)
        )
        return bool(checked)

    @staticmethod
    def _is_selected(control: Any) -> bool:
        getter = getattr(control, "getAttribute", None)
        selected = (
            getter("selected")
            if callable(getter)
            else getattr(control, "selected", None)
        )
        return bool(selected)

    def _walk(self, node: Any, seen: set[int] | None = None) -> Iterable[Any]:
        if seen is None:
            seen = set()
        node_id = id(node)
        if node_id in seen:
            return
        seen.add(node_id)
        for child in node:
            node_name = getattr(child, "nodeName", "").lower()
            yield child
            if node_name not in (
                "button",
                "input",
                "option",
                "select",
                "textarea",
                "#text",
            ):
                yield from self._walk(child, seen)

    def _parse_form(self, form: Any) -> None:
        for control in self._walk(form):
            node_name = getattr(control, "nodeName", "").lower()
            if node_name == "#text":
                continue
            name = self._control_name(control)
            if name is None:
                continue

            control_type = self._control_type(control)
            if node_name == "input":
                if control_type == "file":
                    for file in getattr(control, "files", []) or []:
                        self.append(name, file)
                    continue
                if control_type in ("checkbox", "radio") and not self._is_checked(
                    control
                ):
                    continue
                if control_type in ("submit", "button", "reset", "image"):
                    continue
                self.append(name, self._control_value(control))
            elif node_name == "textarea":
                self.append(name, self._control_value(control))
            elif node_name == "select":
                multiple = getattr(control, "getAttribute", lambda key: None)(
                    "multiple"
                )
                options = list(
                    getattr(control, "getElementsByTagName", lambda key: [])("option")
                )
                selected = [option for option in options if self._is_selected(option)]
                if multiple:
                    for option in selected:
                        self.append(name, self._control_value(option))
                elif selected:
                    self.append(name, self._control_value(selected[0]))
                else:
                    self.append(name, self._control_value(control))
            elif node_name == "button" and control_type not in (
                "submit",
                "button",
                "reset",
            ):
                self.append(name, self._control_value(control))

    def __str__(self) -> str:
        return self.toString()

    def toString(self) -> str:
        """Returns a URL-encoded string representing the FormData object."""
        pairs = []
        for name, value, filename in self._entries:
            if filename is not None:
                value = filename
            pairs.append((name, "" if value is None else str(value)))
        return urllib.parse.urlencode(pairs)

    def append(self, name: str, value: Any, filename: str | None = None) -> None:
        """Append a new value onto an existing key, or add the key."""
        from domonic.webapi.file import Blob, File

        if filename is None and isinstance(value, File):
            filename = value.name
        elif filename is None and isinstance(value, Blob):
            filename = "blob"
        self._entries.append((str(name), value, filename))

    def delete(self, name: str) -> None:
        """Delete every key/value pair for ``name``."""
        name = str(name)
        self._entries = [entry for entry in self._entries if entry[0] != name]

    def entries(self) -> Iterable[tuple[str, Any]]:
        """Return all key/value pairs."""
        return iter((name, value) for name, value, _ in self._entries)

    def entryDetails(self) -> Iterable[tuple[str, Any, str | None]]:
        """Return key/value/filename triples for integrations that need file metadata."""
        return iter(self._entries)

    def get(self, name: str) -> Any:
        """Return the first value associated with ``name``."""
        name = str(name)
        for key, value, _ in self._entries:
            if key == name:
                return value
        return None

    def getAll(self, name: str) -> list[Any]:
        """Return all values associated with ``name``."""
        name = str(name)
        return [value for key, value, _ in self._entries if key == name]

    def has(self, name: str) -> bool:
        """Return whether the collection contains ``name``."""
        name = str(name)
        return any(key == name for key, _, _ in self._entries)

    def keys(self) -> Iterable[str]:
        """Return an iterator over all keys."""
        return iter(name for name, _, _ in self._entries)

    def set(self, name: str, value: Any, filename: str | None = None) -> None:
        """Set ``name`` to one value, replacing any existing values."""
        self.delete(name)
        self.append(name, value, filename)

    def values(self) -> Iterable[Any]:
        """Return an iterator over all values."""
        return iter(value for _, value, _ in self._entries)

    def forEach(self, callback: Callable[[Any, str, FormData], Any]) -> None:
        for name, value in self.entries():
            callback(value, name, self)
