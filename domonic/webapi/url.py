"""
    domonic.webapi.url
    ====================================
    https://developer.mozilla.org/en-US/docs/Web/API/URL

    # TODO - move the unit tests for this class from javascript to webapi
    # TODO - untested

"""
from __future__ import annotations

import urllib.parse
from typing import Any, Callable, Iterable, Iterator

ParamInput = str | dict[str, Any] | Iterable[tuple[str, Any]]


class URL:
    """a-tag extends from URL"""

    def __update__(self) -> None:
        # print( "update URL:", type(self), self  )
        try:
            new = {
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
            self.url = urllib.parse.urlsplit(
                new["protocol"] + "://" + new["host"] + new["pathname"] + query + new["hash"]
            )

            self.href = self.url.geturl()

        except Exception:  # as e:
            # print('fails on props called by init as they dont exist yet')
            # print(e)
            pass

    def __init__(self, url: str = "", *args: Any, **kwargs: Any) -> None:  # TODO - relative to
        """URL

        builds a url

        Args:
            url (str): a url
        """
        self.url = urllib.parse.urlsplit(url)
        self.href = url  # self.url.geturl()
        self.protocol = self.url.scheme
        self.hostname = self.url.hostname
        self.port = self.url.port
        self.host = self.url.hostname
        self.pathname = self.url.path
        self.hash = ""
        self.search = self.url.query
        self._searchParams = URLSearchParams(self.url.query)

    @property
    def searchParams(self) -> str:
        return self._searchParams.toString()

    @property
    def origin(self) -> str:
        if not self.protocol or not self.host:
            return ""
        return f"{self.protocol}://{self.host}"

    def toString(self) -> str:
        return str(self.href)

    # def toJson

    # @property
    # def href(self):
    # TODO - check js vs tag. does js version remove query?. if so detect self.
    #     return self.href

    # @href.setter
    # def href(self, href:str):
    #     self.url = href
    #     self.href = href

    @property
    def protocol(self) -> str:
        return self.__protocol

    @protocol.setter
    def protocol(self, p: str):
        self.__protocol = p
        # if self.ready : self.__update__() # TODO - this instead of silent err?
        self.__update__()

    @property
    def hostname(self) -> str | None:
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
        return self.__port

    @port.setter
    def port(self, p: int | None):
        self.__port = p
        self.__update__()

    @property
    def host(self) -> str | None:
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
        return self.__pathname

    @pathname.setter
    def pathname(self, p: str):
        self.__pathname = p
        self.__update__()

    @property
    def search(self) -> str:
        if not self.__search:
            return ""
        return self.__search if self.__search.startswith("?") else "?" + self.__search

    @search.setter
    def search(self, value: str):
        if value is None:
            value = ""
        self.__search = value if value == "" else value.lstrip("?")
        self._searchParams = URLSearchParams(self.__search)
        self.__update__()

    @property
    def hash(self) -> str:
        """ " hash Sets or returns the anchor part (#) of a URL"""
        if "#" in self.href:
            return "#" + self.href.split("#")[1]
        # return ''
        return self.__hash

    @hash.setter
    def hash(self, h: str):
        self.__hash = h
        self.__update__()

        # @property
        # def origin(self):
        """# origin    Returns the protocol, hostname and port number of a URL Location"""

    def __str__(self) -> str:
        return str(self.href)

    # NOTE - node -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    # @staticmethod
    # def domainToASCII(domain: str):
    #     """[It returns the Punycode ASCII serialization of the domain.
    #     If domain is an invalid domain, the empty string is returned.]

    #     Args:
    #         domain (str): [description]
    #     """
    #     pass

    # @staticmethod
    # def domainToUnicode(domain: str):
    #     """[returns the Unicode serialization of the domain.
    #     If the domain is invalid, the empty string is returned]

    #     Args:
    #         domain (str): [description]
    #     """
    #     pass

    # @staticmethod
    # def fileURLToPath(url: str):
    #     """[ensures the correct decodings of percent-encoded characters as well as
    #     ensuring a cross-platform valid absolute path string.]

    #     Args:
    #         url (str): [The fully-resolved platform-specific file path.]
    #     """
    #     if url is None:
    #         return
    #     return urllib.parse.unquote(url)

    # @staticmethod
    # def format(URL, options):
    #     """[summary]

    #     Args:
    #         URL ([type]): [description]
    #         options ([type]): [description]
    #     """
    #     pass

    # @staticmethod
    # def pathToFileURL(path: str):
    #     """[summary]

    #     Args:
    #         path (str): [description]
    #     """
    #     pass

    # @staticmethod
    # def urlToHttpOptions(url: str):
    #     """[summary]

    #     Args:
    #         url (str): [description]
    #     """
    #     pass


class URLSearchParams:
    """[utility methods to work with the query string of a URL]"""

    def __init__(self, paramString: ParamInput):  # , **paramsObj):
        """[Returns a URLSearchParams object instance.]

        Args:
            paramString ([type]): [ i.e. q=URLUtils.searchParams&topic=api]
        """
        # TODO - escape
        # import ast
        # TODO - dont think i can do this cant urls params have duplicate keys?
        # self.params = ast.literal_eval(paramString)
        if isinstance(paramString, str):
            if paramString.startswith("?"):
                paramString = paramString[1 : len(paramString)]

            import urllib

            self.params: dict[str, list[str]] = urllib.parse.parse_qs(paramString)
        elif isinstance(paramString, dict):
            self.params = {
                str(key): value if isinstance(value, list) else [str(value)] for key, value in paramString.items()
            }
        elif hasattr(paramString, "__iter__"):
            self.params = {}
            for key, value in paramString:
                self.params.setdefault(str(key), []).append(str(value))
        else:
            raise TypeError(
                f"Malformed paramString.  Must be a string or a dict with dict like items. Got: {paramString}"
            )

    def __iter__(self) -> Iterator[tuple[str, list[str]]]:
        for attr in self.params.items():  # dir(self.params.items()):
            # if not attr.startswith("__"):
            yield attr

    def append(self, key: str, value: str) -> None:
        """Appends a specified key/value pair as a new search parameter"""
        # TODO - ordereddict?
        self.params.setdefault(key, []).append(value)  # [key]=value

    def delete(self, key: str) -> None:
        """Deletes the given search parameter, and its associated value, from the list of all search parameters."""
        del self.params[key]

    def has(self, key: str) -> bool:
        """Returns a Boolean indicating if such a given parameter exists."""
        return key in self.params

    def entries(self) -> Iterable[tuple[str, list[str]]]:
        """Returns an iterator allowing iteration through all key/value pairs contained in this object."""
        return self.params.items()

    def forEach(self, func: Callable[[str, list[str]], Any]) -> None:
        """Allows iteration through all values contained in this object via a callback function."""
        for key, value in self.params.items():
            func(key, value)

    def keys(self) -> Iterable[str]:
        """Returns an iterator allowing iteration through all keys of the key/value pairs contained in this object."""
        return self.params.keys()

    def get(self, key: str) -> str | None:
        """Returns the first value associated with the given search parameter."""
        try:
            return self.params.get(key, None)[0]
        except Exception:
            return None

    def sort(self) -> None:
        """Sorts all key/value pairs, if any, by their keys."""
        self.params = dict(sorted(self.params.items()))

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
        self.params[key] = [value]

    def getAll(self, key: str) -> list[str] | None:
        """Returns all the values associated with a given search parameter."""
        return self.params.get(key)

    def __str__(self) -> str:
        return urllib.parse.urlencode(self.params, doseq=True)
