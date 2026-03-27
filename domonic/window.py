"""
    domonic.window
    ====================================

    be mindful there are 2 types of window to be found in domonic:

        1. the javascript window - a window with only static js methods

        2. the domonic window (this one) - a window connected to other things i.e. dom

    You can extend or import either for your own purposes.

"""

from __future__ import annotations

import re
import sys
from typing import Any, Callable

from domonic import domonic
from domonic.dom import Document, Element, Location, document
from domonic.events import Event, EventTarget, FocusEvent, HashChangeEvent, PopStateEvent
from domonic.javascript import Window as JavaScriptWindow
from domonic.webapi.console import Console
from domonic.webapi.credentials import CredentialsContainer
from domonic.webapi.geo import Geolocation
from domonic.webapi.history import History
from domonic.webapi.netinfo import NetworkInformation
from domonic.webapi.webstorage import Storage


class MediaQueryList(EventTarget):
    """Minimal MediaQueryList implementation for Window.matchMedia()."""

    def __init__(self, media: str, *, width: int, height: int) -> None:
        super().__init__()
        self.media = media
        self.matches = self._evaluate(media, width=width, height=height)
        self.onchange: Callable[[Event], Any] | None = None

    @staticmethod
    def _evaluate(media: str, *, width: int, height: int) -> bool:
        if not media:
            return False
        text = media.strip().lower()
        if text in ("all", "screen"):
            return True

        checks: list[bool] = []
        for label, value in (("min-width", width), ("max-width", width), ("min-height", height), ("max-height", height)):
            match = re.search(rf"\({label}\s*:\s*(\d+)px\)", text)
            if not match:
                continue
            target = int(match.group(1))
            if label.startswith("min-"):
                checks.append(value >= target)
            else:
                checks.append(value <= target)

        orientation_match = re.search(r"\(orientation\s*:\s*(portrait|landscape)\)", text)
        if orientation_match:
            orientation = "landscape" if width >= height else "portrait"
            checks.append(orientation == orientation_match.group(1))

        return all(checks) if checks else False

    def addListener(self, callback: Callable[[Event], Any]) -> None:
        self.addEventListener("change", callback)

    def removeListener(self, callback: Callable[[Event], Any]) -> None:
        self.removeEventListener("change", callback)


class CustomElementRegistry:
    """The CustomElementRegistry interface provides methods for registering custom elements and querying registered elements.
    To get an instance of it, use the window.customElements property."""

    def __init__(self) -> None:
        self.store: dict[str, type] = {}

    def define(self, name: str, constructor: Callable[..., Any], options: dict[str, Any] | None = None) -> type:
        """Defines a new custom element."""
        if "-" not in name:
            raise ValueError("Invalid custom element name. Must contain hypen: " + name)
        from domonic.dom import Element
        from domonic.html import tag

        el = type(name, (tag, Element), {"name": name, "__init__": constructor})
        if options is not None and "extends" in options:
            el.extends = options["extends"]
        self.store[name] = el
        return el

    def get(self, name: str) -> type | None:
        """Returns the constructor for the named custom element, or None."""
        return self.store.get(name)

    def upgrade(self, root: Element | None = None) -> Element | None:
        return root

    def whenDefined(self, name: str) -> bool:
        return name in self.store


class Navigator:
    """Navigator"""

    cookieEnabled = False
    appName = "domonic"

    def __init__(self, *args, **kwargs):
        self.connection: NetworkInformation = NetworkInformation()
        self.credentials: CredentialsContainer = CredentialsContainer()
        self.geolocation: Geolocation = Geolocation()
        self.hid = None
        self.keyboard = None
        self.locks = None
        self.mediaCapabilities = None
        self.mediaSession = None
        self.mediaDevices = None
        self.presentation = None
        self.serial = None
        self.serviceWorker = None
        self.storage = None
        self.vendor = None
        self.webdriver = None
        self.xr = None
        self.buildID = None
        self.contacts = None
        self._screen = Screen()

    @property
    def onLine(self) -> bool:
        return True

    @property
    def platform(self) -> str:
        """Returns the platform"""
        if "darwin" in sys.platform:
            return "mac"
        if "linux" in sys.platform:
            return "linux"
        if "win32" in sys.platform:
            return "windows"
        return "unknown"

    @property
    def product(self) -> str:
        """Returns the product name"""
        return self.appName

    @property
    def userAgent(self) -> str:
        """Returns the user-agent header sent by the browser Navigator"""
        return f"domonic/{self.appName} ({self.platform})"

    @property
    def deviceMemory(self) -> float:
        return 1

    @property
    def doNotTrack(self):
        return "unspecified"

    @property
    def hardwareConcurrency(self):
        return 1

    @property
    def maxTouchPoints(self):
        return 1

    @staticmethod
    def registerProtocolHandler(scheme, url, title):
        return None

    @staticmethod
    def requestMediaKeySystemAccess(keySystem, supportedConfigurations):
        return None

    def canShare(self):
        return False

    def clearAppBadge(self):
        return None

    def getBattery(self):
        return {"charging": False, "chargingTime": 0, "dischargingTime": 0, "level": 1.0}

    @property
    def javaEnabled(self):
        return False

    def vibrate(self, pattern):
        return False


class Screen(EventTarget):
    # https://developer.mozilla.org/en-US/docs/Web/API/Screen

    def __init__(self):
        super().__init__()
        self.availLeft = 0
        self.availTop = 0
        self.availHeight = 768
        self.availWidth = 1024
        self.colorDepth = 24
        self.height = 768
        self.left = 0
        self.pixelDepth = 24
        self.top = 0
        self.width = 1024
        self.orientation = None

    @property
    def screenLeft(self) -> int:
        return self.left

    @property
    def screenTop(self) -> int:
        return self.top


class Window(JavaScriptWindow, EventTarget):
    def __init__(self):
        EventTarget.__init__(self)
        self.customElements = CustomElementRegistry()
        self._localStorage: Storage = Storage()
        self._sessionStorage: Storage = Storage()
        self._navigator: Navigator = Navigator()
        self._screen: Screen = self._navigator._screen
        self._document: Document = document
        self._document.defaultView = self
        self._location: Location = Location("https://eventual.technology")
        self._document.URL = self._location.href
        self._console: Console = Console()
        self._history: History = History(self)
        self._closed: bool = False
        self._focused: bool = True
        self._name: str = ""
        self._default_status: str = ""
        JavaScriptWindow.__init__(self)

    @staticmethod
    def _normalize_url(value: str | Location) -> str:
        href = value.href if isinstance(value, Location) else str(value)
        if href and "://" not in href:
            href = "https://" + href
        return href

    def _set_document(self, doc: Document) -> Document:
        self._document = doc
        self._document.defaultView = self
        return self._document

    def _fetch_document(self, url: str) -> Document | None:
        try:
            import requests
        except ModuleNotFoundError:
            return None

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
        except Exception:
            return None

        try:
            import html5lib
        except ModuleNotFoundError:
            html5lib = None

        if html5lib is not None:
            from html5lib import HTMLParser
            from domonic.ext.html5lib_ import getTreeBuilder

            parser = HTMLParser(tree=getTreeBuilder())
            page = parser.parse(response.text)
            page.URL = url
            return page

        try:
            from domonic.parsers import remove_doctype, remove_newlines, remove_tabs, remove_whitespace, remove_tags
        except Exception:
            return None

        content = remove_tags(response.text, ["js", "css", "#"])
        content = remove_doctype(content)
        content = remove_whitespace(content)
        content = remove_newlines(content)
        content = remove_tabs(content)
        page = domonic.parseString(content)
        if page is not None:
            page.URL = url
        return page

    @property
    def history(self) -> History:
        return self._history

    @property
    def console(self) -> Console:
        return self._console

    @property
    def localStorage(self) -> Storage:
        return self._localStorage

    @property
    def sessionStorage(self) -> Storage:
        return self._sessionStorage

    @property
    def document(self) -> Document:
        return self._document

    @document.setter
    def document(self, value: Document) -> None:
        self._set_document(value)

    @property
    def location(self) -> Location:
        return self._location

    @location.setter
    def location(self, value: str | Location) -> None:
        if value is None:
            return
        previous_href = self._location.href
        href = self._normalize_url(value)
        if getattr(self._history, "skip_update", False) is False:
            self._history._update(href)
        self._location = Location(href)
        self._document.URL = href
        if previous_href != href and previous_href.split("#", 1)[0] == href.split("#", 1)[0]:
            self.dispatchEvent(HashChangeEvent("hashchange", {"oldURL": previous_href, "newURL": href}))

        loaded_document = self._fetch_document(href)
        if loaded_document is not None:
            self._set_document(loaded_document)

    def blur(self):
        self._focused = False
        self.dispatchEvent(FocusEvent("blur", {"bubbles": False, "cancelable": False, "relatedTarget": None}))
        return None

    @property
    def closed(self) -> bool:
        return self._closed

    def close(self):
        self._closed = True
        self.dispatchEvent(Event("close"))
        return None

    def confirm(self, message: str):
        return True

    @property
    def defaultStatus(self):
        return self._default_status

    @defaultStatus.setter
    def defaultStatus(self, value=None):
        self._default_status = "" if value is None else str(value)

    def focus(self):
        self._focused = True
        self.dispatchEvent(FocusEvent("focus", {"bubbles": False, "cancelable": False, "relatedTarget": None}))
        return None

    def frameElement(self):
        return None

    def getComputedStyle(self, el, pseudo=None):
        return getattr(el, "style", None)

    def getSelection(self):
        return self.document.getSelection()

    @property
    def innerHeight(self):
        return self._screen.height

    @property
    def innerWidth(self):
        return self._screen.width

    def matchMedia(self, media_query_list):
        return MediaQueryList(media_query_list, width=self.innerWidth, height=self.innerHeight)

    def moveBy(self, x: int, y: int):
        self._screen.left += x
        self._screen.top += y

    def moveTo(self, x: int, y: int):
        self._screen.left = x
        self._screen.top = y

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def navigator(self):
        return self._navigator

    @property
    def screen(self) -> Screen:
        return self._screen

    @property
    def screenLeft(self) -> int:
        return self._screen.screenLeft

    @property
    def screenTop(self) -> int:
        return self._screen.screenTop


window = Window()
alert = window.alert
confirm = window.confirm
prompt = window.prompt
