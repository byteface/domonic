"""
domonic.webapi.url
====================================
https://developer.mozilla.org/en-US/docs/Web/API/URL
"""

from __future__ import annotations

import os
import urllib.parse
from typing import Any, Callable, Iterable, Iterator

ParamInput = str | dict[str, Any] | Iterable[tuple[str, Any]] | None


class URL:
    """a-tag extends from URL"""

    def _get_href_value(self) -> str:
        getter = getattr(self, "getAttribute", None)
        if callable(getter):
            href = getter("href")
            if href is not None:
                return href
        return getattr(self, "_url_href", "") or ""

    def _set_href_value(self, href: str) -> None:
        object.__setattr__(self, "_url_href", href or "")
        setter = getattr(self, "setAttribute", None)
        if callable(setter):
            setter("href", href or "")

    def _load_from_href(self, href: str, base: str | None = None) -> None:
        href = href or ""
        if base is not None:
            href = urllib.parse.urljoin(str(base), href)
        parsed = urllib.parse.urlsplit(href)
        object.__setattr__(self, "url", parsed)
        object.__setattr__(self, "_url_href", href)
        object.__setattr__(self, "_URL__protocol", parsed.scheme)
        object.__setattr__(self, "_URL__username", parsed.username or "")
        object.__setattr__(self, "_URL__password", parsed.password or "")
        object.__setattr__(self, "_URL__hostname", parsed.hostname)
        try:
            port = parsed.port
        except ValueError:
            port = None
        object.__setattr__(self, "_URL__port", port)
        object.__setattr__(self, "_URL__pathname", parsed.path)
        object.__setattr__(self, "_URL__search", parsed.query)
        object.__setattr__(
            self, "_URL__hash", f"#{parsed.fragment}" if parsed.fragment else ""
        )
        object.__setattr__(
            self,
            "_searchParams",
            URLSearchParams(parsed.query, _update=self._search_params_changed),
        )
        object.__setattr__(self, "_url_state_source", href)

    def _search_params_changed(self, params: URLSearchParams) -> None:
        object.__setattr__(self, "_URL__search", params.toString())
        self.__update__()

    def _ensure_url_state(self) -> None:
        href = self._get_href_value()
        if getattr(self, "_url_state_source", None) != href:
            self._load_from_href(href)

    def __update__(self) -> None:
        try:
            self._ensure_url_state()
            new: dict[str, Any] = {
                "protocol": self.protocol,
                "hostname": self.hostname,
                "href": self.href,
                "port": self.port,
                "host": self.host,
                "pathname": self.pathname,
                "hash": self.hash,
                "search": self.search,
                "_searchParams": self._searchParams,
            }
            # NOTE - rebuild happening here
            query = new["search"] or ""
            if query and not query.startswith("?"):
                query = "?" + query
            userinfo = ""
            if self.username:
                userinfo = urllib.parse.quote(self.username, safe="")
                if self.password:
                    userinfo += ":" + urllib.parse.quote(self.password, safe="")
                userinfo += "@"
            scheme = new["protocol"] + "://" if new["protocol"] else ""
            self.url = urllib.parse.urlsplit(
                scheme + userinfo + new["host"] + new["pathname"] + query + new["hash"]
            )

            self._set_href_value(self.url.geturl())
            object.__setattr__(self, "_url_state_source", self.url.geturl())

        except Exception:  # as e:
            return

    def __init__(
        self, url: str = "", base: str | None = None, *args: Any, **kwargs: Any
    ) -> None:
        """URL

        builds a url

        Args:
            url (str): a url
        """
        if args and base is None:
            base = args[0]
        if "base" in kwargs and base is None:
            base = kwargs["base"]
        self._load_from_href(url, base)

    @property
    def href(self) -> str:
        return self._get_href_value()

    @href.setter
    def href(self, href: str) -> None:
        self._load_from_href(href)
        self._set_href_value(href)

    @property
    def searchParams(self) -> URLSearchParams:
        self._ensure_url_state()
        return self._searchParams

    @property
    def origin(self) -> str:
        self._ensure_url_state()
        if not self.protocol or not self.host:
            return ""
        return f"{self.protocol}://{self.host}"

    def toString(self) -> str:
        return str(self.href)

    @staticmethod
    def canParse(url: str, base: str | None = None) -> bool:
        try:
            URL(url, base)
            parsed = urllib.parse.urlsplit(urllib.parse.urljoin(base or "", url))
            return bool(parsed.scheme or base)
        except Exception:
            return False

    @staticmethod
    def parse(url: str, base: str | None = None) -> URL | None:
        return URL(url, base) if URL.canParse(url, base) else None

    @staticmethod
    def createObjectURL(obj: Any) -> str:
        from domonic.webapi.file import createObjectURL

        return createObjectURL(obj)

    @staticmethod
    def revokeObjectURL(url: str) -> None:
        from domonic.webapi.file import revokeObjectURL

        revokeObjectURL(url)

    @property
    def protocol(self) -> str:
        self._ensure_url_state()
        return self.__protocol

    @protocol.setter
    def protocol(self, p: str):
        self.__protocol = (p or "").rstrip(":")
        self.__update__()

    @property
    def hostname(self) -> str | None:
        self._ensure_url_state()
        return self.__hostname

    @hostname.setter
    def hostname(self, h: str):
        if h is None:
            return
        if ":" in h:
            h = h.split(":")[0]
        self.__hostname = h
        self.__update__()

    @property
    def port(self) -> int | None:
        self._ensure_url_state()
        return self.__port

    @port.setter
    def port(self, p: int | str | None):
        if p in ("", None):
            self.__port = None
        else:
            self.__port = int(p)
        self.__update__()

    @property
    def username(self) -> str:
        self._ensure_url_state()
        return self.__username

    @username.setter
    def username(self, value: str):
        self.__username = "" if value is None else str(value)
        self.__update__()

    @property
    def password(self) -> str:
        self._ensure_url_state()
        return self.__password

    @password.setter
    def password(self, value: str):
        self.__password = "" if value is None else str(value)
        self.__update__()

    @property
    def host(self) -> str | None:
        self._ensure_url_state()
        if self.hostname is None:
            return None
        if self.port is not None:
            return self.hostname + ":" + str(self.port)
        else:
            return self.hostname

    @host.setter
    def host(self, h: str):
        if h is None:
            return
        p = self.port
        if ":" in h:
            p = int(h.split(":")[1])
            h = h.split(":")[0]
        self.__host = h
        self.hostname = h
        self.port = p
        self.__update__()

    @property
    def pathname(self) -> str:
        self._ensure_url_state()
        return self.__pathname

    @pathname.setter
    def pathname(self, p: str):
        if p is None:
            p = ""
        elif p and not str(p).startswith("/"):
            p = "/" + str(p)
        self.__pathname = p
        self.__update__()

    @property
    def search(self) -> str:
        self._ensure_url_state()
        if not self.__search:
            return ""
        return self.__search if self.__search.startswith("?") else "?" + self.__search

    @search.setter
    def search(self, value: str):
        if value is None:
            value = ""
        self.__search = value if value == "" else value.lstrip("?")
        self._searchParams = URLSearchParams(
            self.__search, _update=self._search_params_changed
        )
        self.__update__()

    @property
    def hash(self) -> str:
        """ " hash Sets or returns the anchor part (#) of a URL"""
        self._ensure_url_state()
        return self.__hash

    @hash.setter
    def hash(self, h: str):
        if h is None or h == "":
            self.__hash = ""
        else:
            self.__hash = h if str(h).startswith("#") else "#" + str(h)
        self.__update__()

        # @property
        # def origin(self):
        """# origin    Returns the protocol, hostname and port number of a URL Location"""

    def __str__(self) -> str:
        return str(self.href)

    # NOTE - node -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    @staticmethod
    def domainToASCII(domain: str) -> str:
        """Return the Punycode ASCII serialization of a domain."""
        try:
            return str(domain).encode("idna").decode("ascii")
        except Exception:
            return ""

    @staticmethod
    def domainToUnicode(domain: str) -> str:
        """Return the Unicode serialization of a domain."""
        try:
            return str(domain).encode("ascii").decode("idna")
        except Exception:
            return ""

    @staticmethod
    def fileURLToPath(url: str | URL) -> str:
        """Return a local filesystem path for a ``file:`` URL."""
        href = url.href if isinstance(url, URL) else str(url)
        parsed = urllib.parse.urlsplit(href)
        if parsed.scheme and parsed.scheme != "file":
            raise ValueError("URL must use the file: protocol")
        path = urllib.parse.unquote(parsed.path)
        if parsed.netloc and parsed.netloc not in ("localhost", ""):
            path = "//" + parsed.netloc + path
        return path

    @staticmethod
    def pathToFileURL(path: str) -> URL:
        """Return a file URL for a local filesystem path."""
        absolute = os.path.abspath(path)
        return URL("file://" + urllib.parse.quote(absolute))


class URLSearchParams:
    """[utility methods to work with the query string of a URL]"""

    def __init__(
        self,
        paramString: ParamInput = "",
        _update: Callable[[URLSearchParams], Any] | None = None,
    ):
        """[Returns a URLSearchParams object instance.]

        Args:
            paramString ([type]): [ i.e. q=URLUtils.searchParams&topic=api]
        """
        self._update = _update
        if paramString is None:
            paramString = ""

        if isinstance(paramString, str):
            if paramString.startswith("?"):
                paramString = paramString[1 : len(paramString)]

            self.params: dict[str, list[str]] = {}
            for key, value in urllib.parse.parse_qsl(
                paramString, keep_blank_values=True
            ):
                self.params.setdefault(key, []).append(value)
        elif isinstance(paramString, dict):
            self.params = {
                str(key): (
                    [str(item) for item in value]
                    if isinstance(value, list)
                    else [str(value)]
                )
                for key, value in paramString.items()
            }
        elif hasattr(paramString, "__iter__"):
            self.params = {}
            for key, value in paramString:
                self.params.setdefault(str(key), []).append(str(value))
        else:
            raise TypeError(
                f"Malformed paramString.  Must be a string or a dict with dict like items. Got: {paramString}"
            )

    def _changed(self) -> None:
        if self._update is not None:
            self._update(self)

    def __iter__(self) -> Iterator[tuple[str, list[str]]]:
        for attr in self.params.items():
            yield attr

    def append(self, key: str, value: str) -> None:
        """Appends a specified key/value pair as a new search parameter"""
        self.params.setdefault(str(key), []).append(str(value))  # [key]=value
        self._changed()

    def delete(self, key: str, value: str | None = None) -> None:
        """Deletes the given search parameter, and its associated value, from the list of all search parameters."""
        key = str(key)
        if value is None:
            self.params.pop(key, None)
        else:
            value = str(value)
            values = [item for item in self.params.get(key, []) if item != value]
            if values:
                self.params[key] = values
            else:
                self.params.pop(key, None)
        self._changed()

    def has(self, key: str, value: str | None = None) -> bool:
        """Returns a Boolean indicating if such a given parameter exists."""
        key = str(key)
        if value is None:
            return key in self.params
        return str(value) in self.params.get(key, [])

    def entries(self) -> Iterable[tuple[str, list[str]]]:
        """Returns an iterator allowing iteration through all key/value pairs contained in this object."""
        return self.params.items()

    def pairs(self) -> Iterable[tuple[str, str]]:
        """Returns each key/value pair, including duplicates."""
        for key, values in self.params.items():
            for value in values:
                yield key, value

    def forEach(self, func: Callable[..., Any]) -> None:
        """Allows iteration through all values contained in this object via a callback function."""
        for key, value in self.pairs():
            try:
                func(value, key, self)
            except TypeError:
                func(key, value)

    def keys(self) -> Iterable[str]:
        """Returns an iterator allowing iteration through all keys of the key/value pairs contained in this object."""
        return self.params.keys()

    def get(self, key: str) -> str | None:
        """Returns the first value associated with the given search parameter."""
        try:
            values = self.params.get(key, None)
            return values[0] if values else None
        except Exception:
            return None

    def sort(self) -> None:
        """Sorts all key/value pairs, if any, by their keys."""
        self.params = dict(sorted(self.params.items()))
        self._changed()

    @property
    def size(self) -> int:
        return sum(len(values) for values in self.params.values())

    def values(self) -> Iterable[list[str]]:
        """Returns an iterator allowing iteration through all values of the key/value pairs
        contained in this object."""
        return self.params.values()

    def toString(self) -> str:
        """Returns a string containing a query string suitable for use in a URL."""
        # return '&'.join([str(x) for x in self.params])
        return urllib.parse.urlencode(self.params, doseq=True)
        # return str(self.params)

    def set(self, key: str, value: str) -> None:
        """Sets the value associated with a given search parameter to the given value.
        If there are several values, the others are deleted."""
        self.params[str(key)] = [str(value)]
        self._changed()

    def getAll(self, key: str) -> list[str]:
        """Returns all the values associated with a given search parameter."""
        return self.params.get(key, [])

    def __str__(self) -> str:
        return urllib.parse.urlencode(self.params, doseq=True)
