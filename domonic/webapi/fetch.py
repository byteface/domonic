"""
domonic.webapi.fetch
====================================
https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
"""

from __future__ import annotations

import copy
import json as jsonlib
import threading
import urllib.parse
from collections.abc import Callable, Iterable, Mapping, Sequence
from multiprocessing.pool import ThreadPool as Pool
from typing import Any

from domonic.javascript import Promise

_MISSING = object()


class FetchedSet:
    """Container returned by the batch fetch helpers."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.results: list[Any] = list(args)

    def __getitem__(self, index: int) -> Any:
        return self.results[index]

    def __iter__(self):
        return iter(self.results)

    def __len__(self) -> int:
        return len(self.results)

    def append(self, result: Any) -> None:
        self.results.append(result)

    def oncomplete(self, func: Callable[[list[Any]], Any]) -> Any:
        """Run ``func`` once all results have been collected."""
        return func(self.results)


class Headers:
    """Case-insensitive Fetch ``Headers`` collection."""

    def __init__(self, init: Any = None) -> None:
        self.headers: dict[str, list[str]] = {}
        if init is not None:
            self._fill(init)

    @staticmethod
    def _normalize_name(name: Any) -> str:
        name = str(name).strip().lower()
        if not name:
            raise ValueError("Header name cannot be empty")
        if ":" in name or any(ord(char) < 33 for char in name):
            raise ValueError(f"Invalid header name: {name!r}")
        return name

    @staticmethod
    def _normalize_value(value: Any) -> str:
        return str(value).strip()

    def _fill(self, init: Any) -> None:
        if isinstance(init, Headers):
            for name, value in init.raw_items():
                self.append(name, value)
            return

        if isinstance(init, str):
            for line in init.replace("\r\n", "\n").split("\n"):
                if not line or ":" not in line:
                    continue
                name, value = line.split(":", 1)
                self.append(name, value)
            return

        if isinstance(init, Mapping):
            for name, value in init.items():
                if isinstance(value, Sequence) and not isinstance(
                    value, (str, bytes, bytearray)
                ):
                    for item in value:
                        self.append(name, item)
                else:
                    self.set(name, value)
            return

        for name, value in init:
            self.append(name, value)

    def append(self, name: str, value: Any) -> None:
        name = self._normalize_name(name)
        self.headers.setdefault(name, []).append(self._normalize_value(value))

    def delete(self, name: str) -> None:
        self.headers.pop(self._normalize_name(name), None)

    def get(self, name: str, default: Any = None) -> str | Any:
        values = self.headers.get(self._normalize_name(name))
        if values is None:
            return default
        return ", ".join(values)

    def getSetCookie(self) -> list[str]:
        return list(self.headers.get("set-cookie", []))

    def has(self, name: str) -> bool:
        return self._normalize_name(name) in self.headers

    def set(self, name: str, value: Any) -> None:
        self.headers[self._normalize_name(name)] = [self._normalize_value(value)]

    def keys(self) -> list[str]:
        return list(self.headers.keys())

    def values(self) -> list[str]:
        return [", ".join(values) for values in self.headers.values()]

    def entries(self) -> list[tuple[str, str]]:
        return [(name, ", ".join(values)) for name, values in self.headers.items()]

    def raw_items(self) -> list[tuple[str, str]]:
        return [
            (name, value) for name, values in self.headers.items() for value in values
        ]

    def forEach(self, callback: Callable[..., Any], thisArg: Any = None) -> None:
        for name, value in self.entries():
            callback(value, name, self)

    def map(self, callback: Callable[..., Any], thisArg: Any = None) -> list[Any]:
        return [callback(value, name, self) for name, value in self.entries()]

    def filter(self, callback: Callable[..., Any], thisArg: Any = None) -> list[Any]:
        return [
            (name, value)
            for name, value in self.entries()
            if callback(value, name, self)
        ]

    def reduce(self, callback: Callable[..., Any], initialValue: Any) -> Any:
        result = initialValue
        for name, value in self.entries():
            result = callback(result, value, name, self)
        return result

    def toString(self) -> str:
        return str(self.toObject())

    def toObject(self) -> dict[str, str]:
        return dict(self.entries())

    def toJSON(self) -> dict[str, str]:
        return self.toObject()

    def copy(self) -> Headers:
        return Headers(self)

    def __str__(self) -> str:
        return self.toString()

    def __repr__(self) -> str:
        return self.toString()

    def __iter__(self):
        return iter(self.entries())

    def __len__(self) -> int:
        return len(self.headers)

    def __getitem__(self, key: str) -> str:
        value = self.get(key)
        if value is None:
            raise KeyError(key)
        return value

    def __setitem__(self, key: str, value: Any) -> None:
        self.set(key, value)

    def __delitem__(self, key: str) -> None:
        self.delete(key)

    def __contains__(self, key: str) -> bool:
        return self.has(key)


class _BodyMixin:
    body: Any
    bodyUsed: bool

    def _init_body(self, body: Any = None) -> None:
        self.body = body
        self.bodyUsed = False

    def _clone_body(self) -> Any:
        return copy.deepcopy(self.body)

    def _consume_body(self) -> Any:
        self.bodyUsed = True
        return self.body

    def _body_as_bytes(self) -> bytes:
        body = self._consume_body()
        if body is None:
            return b""
        if isinstance(body, bytes):
            return body
        if isinstance(body, bytearray):
            return bytes(body)
        if isinstance(body, memoryview):
            return body.tobytes()
        if hasattr(body, "arrayBuffer") and callable(body.arrayBuffer):
            return body.arrayBuffer()
        if isinstance(body, str):
            return body.encode("utf-8")
        return jsonlib.dumps(body).encode("utf-8")

    def arrayBuffer(self) -> bytes:
        return self._body_as_bytes()

    def bytes(self) -> bytes:
        return self._body_as_bytes()

    def blob(self) -> Any:
        body = self._consume_body()
        from domonic.webapi.file import Blob

        return body if isinstance(body, Blob) else Blob([body])

    def formData(self) -> Any:
        body = self._consume_body()
        if isinstance(body, Mapping):
            return dict(body)
        if hasattr(body, "text") and callable(body.text):
            text = body.text()
            return {
                key: values[0] if len(values) == 1 else values
                for key, values in urllib.parse.parse_qs(
                    text, keep_blank_values=True
                ).items()
            }
        text = self.text()
        return {
            key: values[0] if len(values) == 1 else values
            for key, values in urllib.parse.parse_qs(
                text, keep_blank_values=True
            ).items()
        }

    def json(self) -> Any:
        body = self._consume_body()
        if body is None:
            return None
        if isinstance(body, (Mapping, list, tuple)):
            return body
        if hasattr(body, "text") and callable(body.text):
            body = body.text()
        if isinstance(body, (bytes, bytearray, memoryview)):
            body = bytes(body).decode("utf-8")
        return jsonlib.loads(str(body))

    def text(self) -> str:
        body = self._consume_body()
        if body is None:
            return ""
        if isinstance(body, bytes):
            return body.decode("utf-8")
        if isinstance(body, bytearray):
            return bytes(body).decode("utf-8")
        if isinstance(body, memoryview):
            return body.tobytes().decode("utf-8")
        if hasattr(body, "text") and callable(body.text):
            return body.text()
        if isinstance(body, (Mapping, list, tuple)):
            return jsonlib.dumps(body)
        return str(body)


class _ResponseJSONDescriptor:
    def __get__(self, instance: Response | None, owner: type[Response]):
        if instance is None:
            return owner._json_response
        return instance._json_body


class Response(_BodyMixin):
    """Fetch ``Response`` object."""

    def __init__(
        self,
        url: Any = None,
        status: int | Mapping[str, Any] | None = None,
        statusText: str | None = None,
        headers: Any = None,
        body: Any = None,
        *,
        init: Mapping[str, Any] | None = None,
        type: str = "default",
        redirected: bool = False,
    ) -> None:
        if isinstance(status, Mapping) and statusText is None and headers is None:
            body = url
            init = {**status, **(init or {})}
            url = init.pop("url", "")
            status = None

        if status is None and statusText is None and headers is None and body is None:
            body = url
            url = ""

        init = dict(init or {})
        body = init.pop("body", body)
        url = init.pop("url", url)
        status = init.pop("status", status)
        statusText = init.pop("statusText", statusText)
        headers = init.pop("headers", headers)
        type = init.pop("type", type)
        redirected = init.pop("redirected", redirected)

        self.url = "" if url is None else str(url)
        # the Mapping form of ``status`` is unpacked into ``init`` above, so by
        # here it is only ever an int-like or None
        self.status = 200 if status is None else int(status)  # type: ignore[arg-type]
        self.statusText = "" if statusText is None else str(statusText)
        self.headers = Headers(headers)
        self.type = str(type)
        self.redirected = bool(redirected)
        self._init_body(body)

    @property
    def ok(self) -> bool:
        return 200 <= self.status <= 299

    def clone(self) -> Response:
        if self.bodyUsed:
            raise TypeError("Cannot clone a Response whose body has already been used")
        return Response(
            url=self.url,
            status=self.status,
            statusText=self.statusText,
            headers=self.headers.copy(),
            body=self._clone_body(),
            type=self.type,
            redirected=self.redirected,
        )

    @classmethod
    def error(cls) -> Response:
        return cls(
            url="", status=0, statusText="", headers=None, body=None, type="error"
        )

    @classmethod
    def redirect(cls, url: str, status: int = 302) -> Response:
        if status not in (301, 302, 303, 307, 308):
            raise ValueError("Response.redirect status must be a redirect status")
        return cls(
            url="",
            status=status,
            statusText="",
            headers={"Location": str(url)},
            body=None,
            type="default",
            redirected=True,
        )

    @classmethod
    def _json_response(
        cls, data: Any, init: Mapping[str, Any] | None = None
    ) -> Response:
        init = dict(init or {})
        headers = Headers(init.pop("headers", None))
        if not headers.has("content-type"):
            headers.set("content-type", "application/json")
        return cls(
            url=init.pop("url", ""),
            status=init.pop("status", 200),
            statusText=init.pop("statusText", ""),
            headers=headers,
            body=jsonlib.dumps(data),
            init=init,
        )

    def _json_body(self) -> Any:
        return _BodyMixin.json(self)

    json = _ResponseJSONDescriptor()

    def __str__(self) -> str:
        return self.text()

    def __repr__(self) -> str:
        return f"<Response [{self.status}]>"

    def __iter__(self):
        return iter(self.body)

    def __getitem__(self, key: Any) -> Any:
        return self.body[key]

    def __setitem__(self, key: Any, value: Any) -> None:
        self.body[key] = value

    def __delitem__(self, key: Any) -> None:
        del self.body[key]

    def __contains__(self, key: Any) -> bool:
        return key in self.body


class Request(_BodyMixin):
    """Fetch ``Request`` object."""

    # Declared up front so reading ``original.<field>`` while the same field is
    # still being assigned in __init__ does not leave mypy unable to infer it.
    url: str
    method: str
    headers: "Headers"
    mode: Any
    credentials: Any
    cache: Any
    redirect: Any
    referrer: Any
    referrerPolicy: Any
    integrity: Any
    keepalive: bool
    signal: Any
    destination: Any
    priority: Any
    duplex: Any

    def __init__(
        self,
        url: Any = None,
        method: str | Mapping[str, Any] | None = None,
        headers: Any = None,
        body: Any = None,
        mode: str | None = None,
        credentials: str | None = None,
        cache: str | None = None,
        *,
        init: Mapping[str, Any] | None = None,
        redirect: str | None = None,
        referrer: str | None = None,
        referrerPolicy: str | None = None,
        integrity: str | None = None,
        keepalive: bool | None = None,
        signal: Any = None,
        destination: str = "",
        priority: str | None = None,
        duplex: str | None = None,
    ) -> None:
        original: Request | None = url if isinstance(url, Request) else None
        if isinstance(method, Mapping):
            init = {**method, **(init or {})}
            method = None
        init = dict(init or {})

        self.url = (
            original.url
            if original is not None
            else str(init.pop("url", "" if url is None else url))
        )
        self.method = str(
            init.pop("method", method or (original.method if original else "GET"))
        ).upper()
        headers = init.pop(
            "headers", headers or (original.headers if original else None)
        )
        json_body = init.pop("json", _MISSING)
        body = init.pop(
            "body", body if body is not None else (original.body if original else None)
        )
        self.headers = Headers(headers)
        if json_body is not _MISSING and body is None:
            body = jsonlib.dumps(json_body)
            if not self.headers.has("content-type"):
                self.headers.set("content-type", "application/json")

        self.mode = init.pop("mode", mode or (original.mode if original else "cors"))
        self.credentials = init.pop(
            "credentials",
            credentials or (original.credentials if original else "same-origin"),
        )
        self.cache = init.pop(
            "cache", cache or (original.cache if original else "default")
        )
        self.redirect = init.pop(
            "redirect", redirect or (original.redirect if original else "follow")
        )
        self.referrer = init.pop(
            "referrer", referrer or (original.referrer if original else "about:client")
        )
        self.referrerPolicy = init.pop(
            "referrerPolicy",
            referrerPolicy or (original.referrerPolicy if original else ""),
        )
        self.integrity = init.pop(
            "integrity", integrity or (original.integrity if original else "")
        )
        self.keepalive = bool(
            init.pop("keepalive", keepalive if keepalive is not None else False)
        )
        self.signal = init.pop(
            "signal", signal or (original.signal if original else None)
        )
        self.destination = init.pop(
            "destination", destination or (original.destination if original else "")
        )
        self.priority = init.pop(
            "priority", priority or (original.priority if original else "auto")
        )
        self.duplex = init.pop(
            "duplex", duplex or (original.duplex if original else None)
        )

        if self.method in ("GET", "HEAD") and body is not None:
            raise TypeError("Request with GET/HEAD method cannot have a body")
        self._init_body(body)

    def clone(self) -> Request:
        if self.bodyUsed:
            raise TypeError("Cannot clone a Request whose body has already been used")
        return Request(
            self.url,
            method=self.method,
            headers=self.headers.copy(),
            body=self._clone_body(),
            mode=self.mode,
            credentials=self.credentials,
            cache=self.cache,
            redirect=self.redirect,
            referrer=self.referrer,
            referrerPolicy=self.referrerPolicy,
            integrity=self.integrity,
            keepalive=self.keepalive,
            signal=self.signal,
            destination=self.destination,
            priority=self.priority,
            duplex=self.duplex,
        )

    def __repr__(self) -> str:
        return f"<Request [{self.method} {self.url}]>"


def _normalize_urls(urls: str | Iterable[str]) -> list[str]:
    if isinstance(urls, str):
        return [urls]
    return list(urls)


def _requests_kwargs(request: Request, kwargs: Mapping[str, Any]) -> dict[str, Any]:
    request_kwargs = dict(kwargs)
    request_kwargs.setdefault("headers", request.headers.toObject())
    if request.method not in ("GET", "HEAD") and request.body is not None:
        body = request.body
        if hasattr(body, "arrayBuffer") and callable(body.arrayBuffer):
            body = body.arrayBuffer()
        request_kwargs.setdefault("data", body)
    if request.redirect == "manual":
        request_kwargs.setdefault("allow_redirects", False)
    elif request.redirect == "follow":
        request_kwargs.setdefault("allow_redirects", True)
    return request_kwargs


def _response_from_requests(response: Any) -> Response:
    return Response(
        url=getattr(response, "url", ""),
        status=getattr(response, "status_code", None),
        statusText=getattr(response, "reason", ""),
        headers=getattr(response, "headers", None),
        body=getattr(response, "content", getattr(response, "text", None)),
        redirected=bool(getattr(response, "history", [])),
    )


def fetch(
    input: str | Request, init: Mapping[str, Any] | None = None, **kwargs: Any
) -> Promise:
    """Fetch a resource and return a domonic ``Promise`` fulfilled with ``Response``."""
    promise = Promise()
    request = input if isinstance(input, Request) else Request(input, init=init)

    if str(request.url).startswith("blob:"):
        from domonic.webapi.file import resolveObjectURL

        blob = resolveObjectURL(request.url)
        if blob is None:
            return promise.reject(FileNotFoundError(request.url))
        return promise.resolve(
            Response(
                url=request.url,
                status=200,
                statusText="OK",
                headers={"Content-Type": blob.type},
                body=blob,
            )
        )

    if str(request.url).startswith("data:"):
        from domonic.webapi.file import parse_data_url

        blob = parse_data_url(request.url)
        if blob is None:
            return promise.reject(ValueError("Invalid data URL"))
        return promise.resolve(
            Response(
                url=request.url,
                status=200,
                statusText="OK",
                headers={"Content-Type": blob.type},
                body=blob,
            )
        )

    signal = request.signal
    if signal is not None and getattr(signal, "aborted", False):
        return promise.reject(getattr(signal, "reason", RuntimeError("Fetch aborted")))

    try:
        import requests

        response = requests.request(
            request.method, request.url, **_requests_kwargs(request, kwargs)
        )
        if request.redirect == "error" and 300 <= response.status_code <= 399:
            return promise.reject(RuntimeError("Fetch redirect blocked"))
        return promise.resolve(_response_from_requests(response))
    except Exception as exc:
        return promise.reject(exc)


def _resolve_fetch_result(
    promise: Promise,
    callback_function: Callable[[Any], Any] | None = None,
    error_handler: Callable[[Any], Any] | None = None,
) -> Any:
    if promise.state == "rejected":
        if error_handler is not None:
            promise.catch(error_handler)
        return promise.data
    if callback_function is not None:
        promise.then(callback_function)
    return promise.data


def fetch_set(
    urls: str | Iterable[str],
    callback_function: Callable[[Any], Any] | None = None,
    error_handler: Callable[[Any], Any] | None = None,
    **kwargs: Any,
) -> FetchedSet:
    """Fetch a set of URLs sequentially and return their results."""
    fetched = FetchedSet()
    for url in _normalize_urls(urls):
        fetched.append(
            _resolve_fetch_result(
                fetch(url, **kwargs), callback_function, error_handler
            )
        )
    return fetched


def fetch_threaded(
    urls: str | Iterable[str],
    callback_function: Callable[[Any], Any] | None = None,
    error_handler: Callable[[Any], Any] | None = None,
    **kwargs: Any,
) -> FetchedSet:
    """Fetch a set of URLs concurrently using threads."""
    url_list = _normalize_urls(urls)
    results: list[Any] = [None] * len(url_list)

    def worker(index: int, url: str) -> None:
        results[index] = _resolve_fetch_result(
            fetch(url, **kwargs), callback_function, error_handler
        )

    jobs = [
        threading.Thread(target=worker, args=(index, url), daemon=True)
        for index, url in enumerate(url_list)
    ]
    for job in jobs:
        job.start()
    for job in jobs:
        job.join()
    return FetchedSet(*results)


def fetch_pooled(
    urls: str | Iterable[str],
    callback_function: Callable[[Any], Any] | None = None,
    error_handler: Callable[[Any], Any] | None = None,
    **kwargs: Any,
) -> FetchedSet:
    """Fetch a set of URLs using a thread pool."""
    url_list = _normalize_urls(urls)

    def worker(url: str) -> Any:
        return _resolve_fetch_result(
            fetch(url, **kwargs), callback_function, error_handler
        )

    pool = Pool()
    try:
        return FetchedSet(*pool.map(worker, url_list))
    finally:
        pool.close()
        pool.join()
