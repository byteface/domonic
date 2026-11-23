"""
domonic._cookies
================

The cookies a page's scripts see: ``document.cookie`` and ``window.cookieStore``
(https://html.spec.whatwg.org/#dom-document-cookie, RFC 6265).

A document showing in a window on an http(s) URL reads and writes its window's
cookie jar -- the one the window's navigations and ``fetch()`` send -- so a
cookie the server sets is visible to the page (unless it is HttpOnly) and one
the page sets goes with the next request. Any other document (no window, or
``about:blank``) keeps its own ``name -> value`` dict, as before.
"""

from __future__ import annotations

import email.utils
import http.cookiejar
import time
import urllib.parse
from collections.abc import Iterator, Mapping, MutableMapping
from typing import Any


def window_jar(document: Any) -> Any:
    """The cookie jar ``document`` reads and writes, or ``None`` when it keeps
    its own dict."""
    window = getattr(document, "defaultView", None)
    session_of = getattr(window, "_http_session", None)
    if not callable(session_of) or getattr(window, "document", None) is not document:
        return None
    if urllib.parse.urlsplit(str(getattr(document, "URL", "") or "")).scheme.lower() not in ("http", "https"):
        return None
    try:
        return session_of().cookies
    except ModuleNotFoundError:  # no requests: nothing is sent anyway
        return None


def _http_only(cookie: http.cookiejar.Cookie) -> bool:
    return any(str(key).lower() == "httponly" for key in (getattr(cookie, "_rest", None) or {}))


def _attribute(cookie: http.cookiejar.Cookie, name: str) -> Any:
    for key, value in (getattr(cookie, "_rest", None) or {}).items():
        if str(key).lower() == name:
            return value
    return None


def _hosts(url: str) -> tuple[str, str]:
    """The request host, and the one ``http.cookiejar`` files host-only
    cookies under (a dotless host gets ``.local``)."""
    host = (urllib.parse.urlsplit(url).hostname or "").lower()
    return host, host if "." in host else host + ".local"


def _path_matches(request_path: str, cookie_path: str) -> bool:
    """RFC 6265 5.1.4 path-match."""
    cookie_path = cookie_path or "/"
    if request_path == cookie_path:
        return True
    if not request_path.startswith(cookie_path):
        return False
    return cookie_path.endswith("/") or request_path[len(cookie_path)] == "/"


def _default_path(url: str) -> str:
    """RFC 6265 5.1.4 default-path: the URL's directory."""
    path = urllib.parse.urlsplit(url).path
    if not path.startswith("/") or path.count("/") == 1:
        return "/"
    return path[: path.rfind("/")]


def _domain_matches(cookie: http.cookiejar.Cookie, host: str, filed_host: str) -> bool:
    domain = str(cookie.domain or "").lower()
    if not (cookie.domain_specified or domain.startswith(".")):
        return domain in (host, filed_host)  # host-only
    bare = domain.lstrip(".")
    return any(name == bare or name.endswith("." + bare) for name in (host, filed_host))


def visible_cookies(jar: Any, url: str) -> list[http.cookiejar.Cookie]:
    """The cookies a script on ``url`` sees, longest path first (RFC 6265
    5.4): matching domain and path, unexpired, Secure ones only on https,
    never HttpOnly ones."""
    host, filed_host = _hosts(url)
    parts = urllib.parse.urlsplit(url)
    path = parts.path or "/"
    https = parts.scheme.lower() == "https"
    found = [
        cookie
        for cookie in jar
        if not cookie.is_expired()
        and not _http_only(cookie)
        and (https or not cookie.secure)
        and _domain_matches(cookie, host, filed_host)
        and _path_matches(path, cookie.path)
    ]
    found.sort(key=lambda cookie: -len(cookie.path or ""))
    return found


def _store(
    jar: Any,
    url: str,
    name: str,
    value: str,
    *,
    domain: str | None,
    path: str | None,
    expires: float | None,
    secure: bool,
    same_site: str | None,
) -> None:
    """Store a cookie a script set (RFC 6265 5.3), or drop it the way a
    browser does: a Domain that isn't this site's, a Secure cookie from an
    http page, one that would replace an HttpOnly cookie. An expiry in the
    past deletes the cookie."""
    host, filed_host = _hosts(url)
    if domain:
        domain = domain.strip().lstrip(".").lower()
    if domain:
        if not (host == domain or host.endswith("." + domain)) or ("." not in domain and domain != host):
            return
        cookie_domain, specified = "." + domain, True
    else:
        cookie_domain, specified = filed_host, False
    if not path or not path.startswith("/"):
        path = _default_path(url)
    if secure and urllib.parse.urlsplit(url).scheme.lower() != "https":
        return
    for existing in jar:
        if (existing.name, existing.domain, existing.path) == (name, cookie_domain, path) and _http_only(existing):
            return
    if expires is not None and expires <= time.time():
        try:
            jar.clear(cookie_domain, path, name)
        except KeyError:
            pass
        return
    jar.set_cookie(
        http.cookiejar.Cookie(
            version=0,
            name=name,
            value=value,
            port=None,
            port_specified=False,
            domain=cookie_domain,
            domain_specified=specified,
            domain_initial_dot=specified,
            path=path,
            path_specified=True,
            secure=secure,
            expires=int(expires) if expires is not None else None,
            discard=expires is None,
            comment=None,
            comment_url=None,
            rest={"SameSite": same_site} if same_site else {},
        )
    )


def _parse_set_cookie(text: str) -> tuple[str, str, dict[str, str]] | None:
    """``name``, ``value`` and the lower-cased attributes of a
    ``document.cookie`` assignment (RFC 6265 5.2), or ``None`` without a
    ``name=``."""
    pair, *attributes = str(text).split(";")
    if "=" not in pair:
        return None
    name, value = (part.strip(" \t") for part in pair.split("=", 1))
    if not name:
        return None
    parsed: dict[str, str] = {}
    for attribute in attributes:
        key, _, attribute_value = attribute.partition("=")
        parsed[key.strip().lower()] = attribute_value.strip()
    return name, value, parsed


def _expiry(attributes: Mapping[str, str]) -> float | None:
    """Seconds since the epoch the cookie expires at; ``Max-Age`` wins over
    ``Expires``, and ``None`` is a session cookie."""
    max_age = attributes.get("max-age")
    if max_age is not None and max_age.lstrip("-").isdigit():
        seconds = int(max_age)
        return time.time() + seconds if seconds > 0 else 0.0
    if attributes.get("expires"):
        try:
            return email.utils.parsedate_to_datetime(attributes["expires"]).timestamp()
        except (TypeError, ValueError):
            return None  # an unparseable date is ignored (RFC 6265 5.2.1)
    return None


class DocumentCookies(MutableMapping[str, Any]):
    """``name -> cookie`` for ``document``: its window's jar (see the module
    docstring) as Cookie Store items, or its own dict. ``CookieStore`` and
    ``document.cookie`` both go through it."""

    def __init__(self, document: Any) -> None:
        self._document = document

    def _jar(self) -> Any:
        return window_jar(self._document)

    def _url(self) -> str:
        return str(getattr(self._document, "URL", "") or "")

    def _own(self) -> dict[str, Any]:
        return self._document._cookie_store

    # -- document.cookie -----------------------------------------------------

    def cookie_string(self) -> str:
        jar = self._jar()
        if jar is None:
            pairs = []
            for name, value in self._own().items():
                if isinstance(value, dict):
                    value = value.get("value", "")
                pairs.append(f"{name}={value}")
            return "; ".join(pairs)
        return "; ".join(
            f"{cookie.name}={'' if cookie.value is None else cookie.value}"
            for cookie in visible_cookies(jar, self._url())
        )

    def set_cookie_string(self, text: str) -> None:
        parsed = _parse_set_cookie(text)
        if parsed is None:
            return
        name, value, attributes = parsed
        jar = self._jar()
        if jar is None:
            self._own()[name] = value
            return
        if "httponly" in attributes:
            return  # only the server can set those
        _store(
            jar,
            self._url(),
            name,
            value,
            domain=attributes.get("domain"),
            path=attributes.get("path"),
            expires=_expiry(attributes),
            secure="secure" in attributes,
            same_site=attributes.get("samesite"),
        )

    # -- the mapping (Cookie Store items) ------------------------------------

    def __getitem__(self, name: str) -> Any:
        jar = self._jar()
        if jar is None:
            return self._own()[name]
        for cookie in visible_cookies(jar, self._url()):
            if cookie.name == name:
                return {
                    "name": cookie.name,
                    "value": "" if cookie.value is None else cookie.value,
                    "domain": str(cookie.domain).lstrip(".") if cookie.domain_specified else None,
                    "path": cookie.path,
                    "expires": cookie.expires * 1000 if cookie.expires else None,
                    "secure": bool(cookie.secure),
                    "sameSite": str(_attribute(cookie, "samesite") or "lax").lower(),
                    "partitioned": False,
                }
        raise KeyError(name)

    def __setitem__(self, name: str, value: Any) -> None:
        jar = self._jar()
        if jar is None:
            self._own()[name] = value
            return
        item = dict(value) if isinstance(value, Mapping) else {"value": value}
        expires = item.get("expires")
        _store(
            jar,
            self._url(),
            name,
            str(item.get("value", "")),
            domain=item.get("domain"),
            path=item.get("path") or "/",
            expires=float(expires) / 1000 if expires is not None else None,
            secure=bool(item.get("secure", False)),
            same_site=item.get("sameSite"),
        )

    def __delitem__(self, name: str) -> None:
        jar = self._jar()
        if jar is None:
            del self._own()[name]
            return
        matches = [cookie for cookie in visible_cookies(jar, self._url()) if cookie.name == name]
        if not matches:
            raise KeyError(name)
        for cookie in matches:
            jar.clear(cookie.domain, cookie.path, cookie.name)

    def __iter__(self) -> Iterator[str]:
        jar = self._jar()
        if jar is None:
            return iter(list(self._own()))
        names: list[str] = []
        for cookie in visible_cookies(jar, self._url()):
            if cookie.name not in names:
                names.append(cookie.name)
        return iter(names)

    def __len__(self) -> int:
        return sum(1 for _ in self)
