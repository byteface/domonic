"""
domonic.window
==============

The DOM-connected ``Window`` implementation for domonic.

Be mindful that domonic has two window-shaped surfaces:

1. ``domonic.javascript.Window`` for JavaScript-style globals and timer helpers
2. ``domonic.window.Window`` for a browsing-context style object connected to
   ``document``, history, storage, media queries, and custom elements
"""

from __future__ import annotations

import re
import sys
import threading
import time
from typing import Any, Callable

from domonic import domonic
from domonic.dom import Document, Element, Location, document
from domonic.events import (
    CloseEvent,
    Event,
    EventTarget,
    FocusEvent,
    HashChangeEvent,
    MessageEvent,
    PopStateEvent,
)
from domonic.javascript import Promise
from domonic.javascript import Window as JavaScriptWindow
from domonic.javascript import performance
from domonic.webapi.clipboard import Clipboard
from domonic.webapi.console import Console
from domonic.webapi.cookiestore import CookieStore
from domonic.webapi.credentials import CredentialsContainer
from domonic.webapi.crypto import Crypto
from domonic.webapi.cssfontloading import FontFaceSet
from domonic.webapi.gamepad import Gamepad, GamepadManager
from domonic.webapi.geo import Geolocation
from domonic.webapi.history import History
from domonic.webapi.mediacapabilities import MediaCapabilities
from domonic.webapi.mediadevices import MediaDevices
from domonic.webapi.mediasession import MediaSession
from domonic.webapi.netinfo import NetworkInformation
from domonic.webapi.notifications import Notification
from domonic.webapi.permissions import Permissions
from domonic.webapi.scheduler import Scheduler
from domonic.webapi.serviceworker import ServiceWorkerContainer
from domonic.webapi.webstorage import Storage


def _split_top_level(text: str, separator: str) -> list[str]:
    """Split ``text`` on ``separator`` only where parenthesis depth is zero."""
    parts: list[str] = []
    depth = 0
    start = 0
    i = 0
    step = len(separator)
    while i < len(text):
        char = text[i]
        if char == "(":
            depth += 1
        elif char == ")":
            depth = max(depth - 1, 0)
        elif depth == 0 and text[i : i + step] == separator:
            parts.append(text[start:i].strip())
            start = i + step
            i += step
            continue
        i += 1
    parts.append(text[start:].strip())
    return [p for p in parts if p]


class MediaQueryList(EventTarget):
    """Result object returned by ``Window.matchMedia()``.

    It exposes the media query string, the current match state, and ``change``
    listeners in the familiar browser style.
    """

    #: default answers for the discrete preference / capability media features,
    #: matching a typical desktop browser. ``Window`` copies this onto each
    #: instance as ``window.mediaFeatures`` so it can be overridden per session
    #: (e.g. ``window.mediaFeatures["prefers-color-scheme"] = "dark"``).
    DEFAULT_FEATURES: dict[str, str] = {
        "prefers-color-scheme": "light",
        "prefers-reduced-motion": "no-preference",
        "prefers-reduced-transparency": "no-preference",
        "prefers-reduced-data": "no-preference",
        "prefers-contrast": "no-preference",
        "forced-colors": "none",
        "inverted-colors": "none",
        "hover": "hover",
        "any-hover": "hover",
        "pointer": "fine",
        "any-pointer": "fine",
        "update": "fast",
        "scripting": "enabled",
        "color-gamut": "srgb",
        "display-mode": "browser",
    }

    def __init__(
        self,
        media: str,
        *,
        width: int,
        height: int,
        features: "dict[str, str] | None" = None,
        resolution: float = 1.0,
        media_type: str = "screen",
    ) -> None:
        super().__init__()
        self.media = media
        self._features = features if features is not None else dict(self.DEFAULT_FEATURES)
        self._resolution = resolution
        self._media_type = media_type
        self.matches = self._evaluate(
            media,
            width=width,
            height=height,
            features=self._features,
            resolution=resolution,
            media_type=media_type,
        )
        self.onchange: Callable[[Event], Any] | None = None

    @staticmethod
    def _to_px(number: str, unit: str) -> float:
        try:
            value = float(number)
        except ValueError:
            return 0.0
        return value * {"em": 16.0, "rem": 16.0, "pt": 96.0 / 72.0}.get(unit, 1.0)

    @classmethod
    def _evaluate(
        cls,
        media: str,
        *,
        width: int,
        height: int,
        features: "dict[str, str] | None" = None,
        resolution: float = 1.0,
        media_type: str = "screen",
    ) -> bool:
        if not media:
            return False
        features = features or cls.DEFAULT_FEATURES
        text = media.strip().lower()
        if "," in text:
            return any(
                cls._evaluate(
                    part, width=width, height=height, features=features, resolution=resolution, media_type=media_type
                )
                for part in _split_top_level(text, ",")
            )
        if " and " in text:
            return all(
                cls._evaluate(
                    part, width=width, height=height, features=features, resolution=resolution, media_type=media_type
                )
                for part in _split_top_level(text, " and ")
            )
        if text.startswith("not "):
            return not cls._evaluate(
                text[4:].strip(),
                width=width,
                height=height,
                features=features,
                resolution=resolution,
                media_type=media_type,
            )
        if text.startswith("only "):
            text = text[5:].strip()
        if text == "all":
            return True
        # A named media type (``screen``, ``print``) only matches when it is
        # the one currently rendering -- domonic itself has no paged/print
        # pipeline, so ``media_type`` defaults to ``"screen"`` and stays that
        # way unless a host that does implement one (e.g. a renderer with an
        # actual print mode) overrides ``window.mediaType``. Previously this
        # returned ``True`` for either unconditionally, so ``@media print``
        # rules applied outside of any print context.
        if text in ("screen", "print"):
            return text == media_type
        if text in ("speech", "tty", "tv", "projection", "handheld", "braille"):
            return False

        # (orientation: portrait|landscape)
        orientation_match = re.search(r"\(\s*orientation\s*:\s*(portrait|landscape)\s*\)", text)
        if orientation_match:
            orientation = "landscape" if width >= height else "portrait"
            return orientation == orientation_match.group(1)

        # discrete feature: (prefers-color-scheme: dark), (hover: none), ...
        discrete = re.search(r"\(\s*([a-z-]+)\s*:\s*([a-z-]+)\s*\)", text)
        if discrete and discrete.group(1) in features:
            return features[discrete.group(1)] == discrete.group(2)
        # boolean feature form: (pointer), (prefers-reduced-motion)
        boolean = re.fullmatch(r"\(\s*([a-z-]+)\s*\)", text)
        if boolean and boolean.group(1) in features:
            return features[boolean.group(1)] not in ("none", "no-preference")

        # resolution: (min-resolution: 2dppx), (resolution >= 150dpi)
        res_match = re.search(
            r"\(\s*(min-|max-)?resolution\s*(:|<=|>=|<|>)?\s*([\d.]+)(dppx|dpi|x)\s*\)",
            text,
        )
        if res_match:
            bound, cmp, number, unit = res_match.groups()
            target = float(number) / (96.0 if unit == "dpi" else 1.0)
            if bound == "min-" or cmp in (">=", ">"):
                return resolution >= target
            if bound == "max-" or cmp in ("<=", "<"):
                return resolution <= target
            return abs(resolution - target) < 1e-9

        # width / height -- (min-width: Npx) / (max-height: Npx) prefix form and
        # the range form (width >= Npx), (400px <= width <= 900px)
        checks: list[bool] = []
        for axis_name, axis in (("width", width), ("height", height)):
            for m in re.finditer(
                rf"\(\s*(min-|max-)?{axis_name}\s*(:|<=|>=|<|>|=)\s*([\d.]+)([a-z%]*)\s*\)",
                text,
            ):
                bound, cmp, number, unit = m.groups()
                target = cls._to_px(number, unit)
                if bound == "min-":
                    checks.append(axis >= target)
                elif bound == "max-":
                    checks.append(axis <= target)
                elif cmp == ">=":
                    checks.append(axis >= target)
                elif cmp == ">":
                    checks.append(axis > target)
                elif cmp == "<=":
                    checks.append(axis <= target)
                elif cmp == "<":
                    checks.append(axis < target)
                else:
                    checks.append(axis == target)
            # double-ended range: (400px <= width <= 900px)
            for m in re.finditer(
                rf"\(\s*([\d.]+)([a-z%]*)\s*(<=?|>=?)\s*{axis_name}\s*" rf"(<=?|>=?)\s*([\d.]+)([a-z%]*)\s*\)",
                text,
            ):
                lo, lounit, locmp, hicmp, hi, hiunit = m.groups()
                lo_px, hi_px = cls._to_px(lo, lounit), cls._to_px(hi, hiunit)
                checks.append(
                    (axis >= lo_px if locmp == "<=" else axis > lo_px)
                    and (axis <= hi_px if hicmp == "<=" else axis < hi_px)
                )

        return all(checks) if checks else False

    def _set_viewport(self, *, width: int, height: int) -> None:
        previous = self.matches
        self.matches = self._evaluate(
            self.media,
            width=width,
            height=height,
            features=self._features,
            resolution=self._resolution,
            media_type=self._media_type,
        )
        if self.matches != previous:
            event = Event("change", {"bubbles": False, "cancelable": False})
            event.matches = self.matches
            event.media = self.media
            self.dispatchEvent(event)

    def addListener(self, callback: Callable[[Event], Any]) -> None:
        self.addEventListener("change", callback)

    def removeListener(self, callback: Callable[[Event], Any]) -> None:
        self.removeEventListener("change", callback)


class IdleDeadline:
    """Small object passed to ``requestIdleCallback`` callbacks."""

    def __init__(self, *, did_timeout: bool = False, budget_ms: float = 50.0) -> None:
        self.didTimeout = did_timeout
        self._deadline = time.monotonic() + (budget_ms / 1000)

    def timeRemaining(self) -> float:
        return max(0.0, (self._deadline - time.monotonic()) * 1000)


class CustomElementRegistry:
    """Registry for defining and upgrading custom elements.

    Access this through ``window.customElements`` to register custom element
    classes, wait for definitions, and upgrade parsed trees against the
    registry.
    """

    def __init__(self) -> None:
        self.store: dict[str, type[Element]] = {}
        self._constructors: dict[Any, str] = {}
        self._when_defined: dict[str, list[Promise]] = {}

    @staticmethod
    def _validate_name(name: str) -> str:
        normalized = str(name).strip().lower()
        if not normalized or "-" not in normalized:
            raise ValueError("Invalid custom element name. Must contain hyphen: " + str(name))
        if not re.fullmatch(r"[a-z][.0-9_a-z-]*-[.0-9_a-z-]*", normalized):
            raise ValueError("Invalid custom element name: " + str(name))
        if normalized in {
            "annotation-xml",
            "color-profile",
            "font-face",
            "font-face-src",
            "font-face-uri",
            "font-face-format",
            "font-face-name",
            "missing-glyph",
        }:
            raise ValueError("Reserved custom element name: " + normalized)
        return normalized

    @staticmethod
    def _coerce_constructor(
        name: str,
        constructor: Callable[..., Any],
        options: dict[str, Any] | None = None,
    ) -> type[Element]:
        if not isinstance(constructor, type):
            raise TypeError("constructor must be a class")
        if issubclass(constructor, Element):
            if getattr(constructor, "name", None) in (None, ""):
                setattr(constructor, "name", name)
            return constructor
        attrs = {"name": name}
        if options is not None and "extends" in options:
            attrs["extends"] = options["extends"]
        return type(name.replace("-", "_"), (constructor, Element), attrs)

    def define(
        self,
        name: str,
        constructor: Callable[..., Any],
        options: dict[str, Any] | None = None,
    ) -> type:
        """Defines a new custom element."""
        normalized = self._validate_name(name)
        if normalized in self.store:
            raise ValueError("Custom element already defined: " + normalized)
        if constructor in self._constructors:
            raise ValueError("Custom element constructor already defined: " + self._constructors[constructor])

        element_class = self._coerce_constructor(normalized, constructor, options)
        if options is not None and "extends" in options:
            # not a generic Element attribute -- bookkeeping this registry
            # reads back with getattr(candidate, "extends", "")
            setattr(element_class, "extends", options["extends"])
            # A customized built-in keeps its host tag name (``<button is="...">``);
            # only autonomous elements take the hyphenated name as their tag.
            if getattr(element_class, "name", None) in (None, "", normalized):
                element_class.name = options["extends"]
        else:
            element_class.name = normalized
        self.store[normalized] = element_class
        self._constructors[constructor] = normalized
        for promise in self._when_defined.pop(normalized, []):
            promise.resolve(element_class)
        return element_class

    def get(self, name: str) -> type | None:
        """Returns the constructor for the named custom element, or None."""
        return self.store.get(str(name).strip().lower())

    def getName(self, constructor: type) -> str | None:
        return self._constructors.get(constructor)

    def _upgrade_element(self, element: Element) -> Element:
        name = str(getattr(element, "tagName", getattr(element, "name", ""))).strip().lower()
        constructor = self.store.get(name)
        if constructor is None:
            # Customized built-in: <button is="fancy-button"> upgrades to the
            # class registered as "fancy-button" with options {"extends": "button"}.
            getter = getattr(element, "getAttribute", None)
            is_name = (getter("is") or "").strip().lower() if callable(getter) else ""
            if is_name:
                candidate = self.store.get(is_name)
                if candidate is not None and str(getattr(candidate, "extends", "")).strip().lower() == name:
                    constructor = candidate
        if constructor is None or isinstance(element, constructor):
            return element
        old_document = element.ownerDocument if isinstance(element.ownerDocument, Document) else None
        element.__class__ = constructor
        element.name = name
        element._custom_element_name = name
        if hasattr(constructor, "observedAttributes"):
            element.observedAttributes = getattr(constructor, "observedAttributes")
        if isinstance(old_document, Document) and getattr(element, "isConnected", False):
            callback = getattr(element, "connectedCallback", None)
            if callable(callback) and not getattr(element, "_custom_element_connected", False):
                element._custom_element_connected = True
                callback()
        return element

    def upgrade(self, root: Element | None = None) -> Element | None:
        if root is None:
            return None
        self._upgrade_element(root)
        for child in getattr(root, "childNodes", []):
            if isinstance(child, Element):
                self.upgrade(child)
        return root

    def whenDefined(self, name: str) -> Promise:
        normalized = self._validate_name(name)
        constructor = self.store.get(normalized)
        promise = Promise()
        if constructor is not None:
            promise.resolve(constructor)
            return promise
        self._when_defined.setdefault(normalized, []).append(promise)
        return promise


class Navigator:
    """Minimal browsing-environment navigator object."""

    cookieEnabled = False
    appName = "domonic"

    def __init__(self, *args, **kwargs):
        self.clipboard: Clipboard = Clipboard()
        self.connection: NetworkInformation = NetworkInformation()
        self.credentials: CredentialsContainer = CredentialsContainer()
        self.geolocation: Geolocation = Geolocation()
        self._gamepads: GamepadManager = GamepadManager()
        self.hid = None
        self.keyboard = None
        self.locks = None
        self.mediaCapabilities: MediaCapabilities = MediaCapabilities()
        self.mediaSession: MediaSession = MediaSession()
        self.mediaDevices: MediaDevices = MediaDevices()
        self.presentation = None
        self.permissions: Permissions = Permissions()
        self.serial = None
        self.serviceWorker: ServiceWorkerContainer = ServiceWorkerContainer()
        self.storage = None
        self.vendor = None
        self.webdriver = None
        self.xr = None
        self.buildID = None
        self.contacts = None
        self._screen = Screen()

    @property
    def gamepads(self) -> GamepadManager:
        return self._gamepads

    def getGamepads(self) -> list[Gamepad | None]:
        return self._gamepads.getGamepads()

    def connectGamepad(self, gamepad: Gamepad, index: int | None = None) -> Gamepad:
        return self._gamepads.connect(gamepad, index)

    def disconnectGamepad(self, gamepad: Gamepad | int) -> Gamepad | None:
        return self._gamepads.disconnect(gamepad)

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
        return {
            "charging": False,
            "chargingTime": 0,
            "dischargingTime": 0,
            "level": 1.0,
        }

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
    def __init__(
        self,
        *,
        doc: Document | None = None,
        opener: "Window | None" = None,
        parent: "Window | None" = None,
        url: str | None = None,
    ):
        EventTarget.__init__(self)
        # Optional native/backend host.  Headless Domonic leaves this as None;
        # renderers such as Chromonic attach a real OS-window implementation.
        self._host = None
        self.customElements = CustomElementRegistry()
        self._localStorage: Storage = Storage()
        self._sessionStorage: Storage = Storage()
        self._navigator: Navigator = Navigator()
        self._navigator.gamepads.eventTarget = self
        self._screen: Screen = self._navigator._screen
        self._location: Location = Location(url or "https://eventual.technology")
        self._document: Document = doc if doc is not None else document
        self.attach(self._document)
        self._document.URL = self._location.href
        self._console: Console = Console()
        self.cookieStore: CookieStore = CookieStore(self._document._cookie_store)
        self.crypto: Crypto = Crypto()
        self.FontFaceSet = FontFaceSet
        self.Notification = Notification
        self.scheduler: Scheduler = Scheduler()
        self._history: History = History(self)
        self._closed: bool = False
        self._focused: bool = True
        self._name: str = ""
        self._default_status: str = ""
        self._status: str = ""
        self._opener = opener
        self._parent = parent if parent is not None else self
        self._top = getattr(self._parent, "top", self._parent) if parent is not None else self
        self._outer_width = self._screen.width
        self._outer_height = self._screen.height
        self._scroll_x = 0
        self._scroll_y = 0
        self._stopped = False
        self._media_query_lists: list[MediaQueryList] = []
        #: discrete media-feature answers used by ``matchMedia`` -- override e.g.
        #: ``window.mediaFeatures["prefers-color-scheme"] = "dark"``
        self.mediaFeatures: dict[str, str] = dict(MediaQueryList.DEFAULT_FEATURES)
        #: the media type ``matchMedia``/``@media`` rules evaluate a named
        #: media-type token against (``"screen"``, ``"print"``, ...). domonic
        #: has no print/paged-media pipeline of its own, so this is always
        #: interactive/"screen" rendering by default; a host that does
        #: implement one can override it, e.g. ``window.mediaType = "print"``
        #: while producing print output.
        self.mediaType: str = "screen"
        self._microtask_queue: list[Callable[[], Any]] = []
        self._running_microtasks = False
        self._next_animation_frame_id = 1
        self._animation_frame_timers: dict[int, threading.Timer] = {}
        self._next_idle_callback_id = 1
        self._idle_callback_timers: dict[int, threading.Timer] = {}
        JavaScriptWindow.__init__(self)

    @staticmethod
    def _normalize_url(value: str | Location) -> str:
        href = value.href if isinstance(value, Location) else str(value)
        if href and not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", href):
            href = "https://" + href
        return href

    def _set_document(self, doc: Document, referrer: str | None = None) -> Document:
        previous_document = getattr(self, "_document", None)
        self.attach(doc)
        self._document.URL = self._location.href
        if hasattr(self, "cookieStore"):
            self.cookieStore = CookieStore(self._document._cookie_store)

        if referrer is not None:
            self._document.referrer = referrer
        elif previous_document is not None:
            self._document.referrer = getattr(previous_document, "URL", "") or ""

        return self._document

    def attach(self, document: Document) -> Document:
        """Attach ``document`` to this browsing context and return it."""
        previous_document = getattr(self, "_document", None)
        if previous_document is not None and previous_document is not document:
            if getattr(previous_document, "defaultView", None) is self:
                previous_document.defaultView = None

        previous_window = getattr(document, "defaultView", None)
        if previous_window is not None and previous_window is not self:
            if getattr(previous_window, "_document", None) is document:
                previous_window._document = None
            document.defaultView = None

        self._document = document
        document.defaultView = self
        return document

    @property
    def native(self):
        """Return the attached native/backend host, if one exists.

        Browser-standard behaviour remains on this Window.  Host-specific
        extensions (opacity, decoration, always-on-top, etc.) live behind
        ``window.native`` so Domonic does not grow renderer-specific APIs.
        """
        return self._host

    def attach_host(self, host):
        """Attach an optional native window host and return it."""
        if host is self._host:
            return host

        previous = self._host
        self._host = None
        if previous is not None:
            detach = getattr(previous, "detach", None)
            if callable(detach):
                detach(self)

        self._host = host
        if host is not None:
            attach = getattr(host, "attach", None)
            if callable(attach):
                try:
                    attach(self)
                except Exception:
                    self._host = None
                    raise
        return host

    def detach_host(self):
        """Detach and return the current native host, if any."""
        host = self._host
        self._host = None
        if host is not None:
            detach = getattr(host, "detach", None)
            if callable(detach):
                detach(self)
        return host

    def _set_viewport(
        self,
        width: int,
        height: int,
        *,
        outer_width: int | None = None,
        outer_height: int | None = None,
        dispatch: bool = True,
    ) -> None:
        """Update viewport/native size state without commanding a host.

        This is deliberately separate from ``resizeTo``.  A browser shell can
        have native chrome (Chromonic's toolbar is one example), so its OS
        window and the page viewport do not necessarily have the same height.
        """
        width = max(0, int(width))
        height = max(0, int(height))
        changed = width != self._screen.width or height != self._screen.height

        self._screen.width = width
        self._screen.height = height
        self._screen.availWidth = width
        self._screen.availHeight = height

        if outer_width is not None:
            self._outer_width = max(0, int(outer_width))
        if outer_height is not None:
            self._outer_height = max(0, int(outer_height))

        if changed:
            self._update_media_queries()
            if dispatch:
                self.dispatchEvent(Event("resize", {"bubbles": False, "cancelable": False}))

    # Host notifications.  These never call back into the host, which keeps
    # public commands and native callbacks from recursively triggering each
    # other.
    def _host_resized(
        self,
        width: int,
        height: int,
        *,
        outer_width: int | None = None,
        outer_height: int | None = None,
    ) -> None:
        self._set_viewport(
            width,
            height,
            outer_width=outer_width,
            outer_height=outer_height,
        )

    def _host_moved(self, x: int, y: int) -> None:
        self._screen.left = int(x)
        self._screen.top = int(y)

    def _host_scale_changed(self, xscale: float, yscale: float | None = None) -> None:
        # devicePixelRatio is scalar in the browser API.  GLFW normally reports
        # equal X/Y scale; use X as the canonical value and keep the pair on
        # the host itself if a backend needs both.
        self.devicePixelRatio = float(xscale or 1.0)
        self._update_media_queries()

    def _host_focused(self, *, dispatch: bool = True) -> None:
        changed = not self._focused
        self._focused = True
        if dispatch and changed:
            self.dispatchEvent(FocusEvent("focus", {"bubbles": False, "cancelable": False, "relatedTarget": None}))

    def _host_blurred(self, *, dispatch: bool = True) -> None:
        changed = self._focused
        self._focused = False
        if dispatch and changed:
            self.dispatchEvent(FocusEvent("blur", {"bubbles": False, "cancelable": False, "relatedTarget": None}))

    def _host_closed(self, *, dispatch: bool = True) -> None:
        if self._closed:
            return
        self._closed = True
        if dispatch:
            self.dispatchEvent(
                CloseEvent(
                    "close",
                    {
                        "bubbles": False,
                        "cancelable": False,
                        "code": 1000,
                        "reason": "",
                        "wasClean": True,
                    },
                )
            )

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

        page = domonic.parseString(response.text)
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
    def clientInformation(self) -> Navigator:
        return self.navigator

    @property
    def frames(self):
        return self

    @property
    def length(self) -> int:
        return 0

    @property
    def opener(self):
        return self._opener

    @opener.setter
    def opener(self, value) -> None:
        self._opener = value

    @property
    def origin(self) -> str:
        from domonic.webapi.url import URL

        return URL(self.location.href or "").origin

    @property
    def parent(self):
        return self._parent

    @property
    def performance(self):
        return performance

    @property
    def self(self):
        return self

    @property
    def top(self):
        return self._top

    @property
    def window(self):
        return self

    @property
    def isSecureContext(self) -> bool:
        href = self.location.href or ""
        return href.startswith(("https:", "wss:", "file:")) or href.startswith(("http://localhost", "http://127.0.0.1"))

    @property
    def localStorage(self) -> Storage:  # type: ignore[override]
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

    @property  # type: ignore[override]
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
        self._document.referrer = previous_href or ""
        if previous_href != href and previous_href.split("#", 1)[0] == href.split("#", 1)[0]:
            self.dispatchEvent(HashChangeEvent("hashchange", {"oldURL": previous_href, "newURL": href}))

        loaded_document = self._fetch_document(href)
        if loaded_document is not None:
            self._set_document(loaded_document, referrer=previous_href)

    def blur(self):
        host_blur = getattr(self._host, "blur", None)
        if callable(host_blur):
            host_blur()
            return None
        # Preserve Domonic's existing headless behaviour: an explicit blur()
        # call dispatches even if a caller repeats it.  Native host callbacks
        # themselves are de-duplicated by _host_blurred().
        self._focused = False
        self.dispatchEvent(FocusEvent("blur", {"bubbles": False, "cancelable": False, "relatedTarget": None}))
        return None

    @property
    def closed(self) -> bool:
        return self._closed

    def close(self):
        host_close = getattr(self._host, "close", None)
        if callable(host_close):
            host_close()
            # Hosts normally notify via _host_closed(); keep this synchronous
            # even for a minimal backend that does not.
            if not self._closed:
                self._host_closed()
            return None
        self._host_closed()
        return None

    def confirm(self, message: str):
        return True

    @property
    def defaultStatus(self):
        return self._default_status

    @defaultStatus.setter
    def defaultStatus(self, value=None):
        self._default_status = "" if value is None else str(value)

    def dump(self, message: Any = ""):
        print(message)
        return None

    def find(
        self,
        string: str,
        case_sensitive: bool = False,
        backwards: bool = False,
        wrap: bool = False,
    ):
        text = self.document.textContent or ""
        needle = str(string)
        if not case_sensitive:
            text = text.lower()
            needle = needle.lower()
        return needle in text

    def focus(self):
        host_focus = getattr(self._host, "focus", None)
        if callable(host_focus):
            host_focus()
            return None
        # Preserve Domonic's existing headless behaviour: explicitly calling
        # focus() dispatches a focus event even if the virtual window started
        # focused.  Native host callbacks themselves are de-duplicated.
        self._focused = True
        self.dispatchEvent(FocusEvent("focus", {"bubbles": False, "cancelable": False, "relatedTarget": None}))
        return None

    def frameElement(self):
        return None

    def getComputedStyle(self, el, pseudo=None):
        """Return a read-only ``CSSStyleDeclaration`` resolved through a light
        cascade: matching author rules (by specificity / order / ``!important``),
        then inline styles, then inherited values, then each property's initial
        value."""
        try:
            from domonic.style import ComputedStyleDeclaration

            return ComputedStyleDeclaration(el, pseudo)
        except Exception:
            return getattr(el, "style", None)

    def getSelection(self):
        return self.document.getSelection()

    @property
    def innerHeight(self):
        return self._screen.height

    @property
    def innerWidth(self):
        return self._screen.width

    def _update_media_queries(self) -> None:
        resolution = float(getattr(self, "devicePixelRatio", 1.0) or 1.0)
        for query in list(self._media_query_lists):
            query._resolution = resolution
            query._set_viewport(width=self.innerWidth, height=self.innerHeight)

    def matchMedia(self, media_query_list):
        query = MediaQueryList(
            media_query_list,
            width=self.innerWidth,
            height=self.innerHeight,
            features=self.mediaFeatures,
            resolution=float(getattr(self, "devicePixelRatio", 1.0) or 1.0),
            media_type=self.mediaType,
        )
        self._media_query_lists.append(query)
        return query

    def cancelAnimationFrame(self, request_id: int):
        host_cancel = getattr(self._host, "cancel_animation_frame", None)
        if callable(host_cancel):
            host_cancel(request_id)
            return None
        timer = self._animation_frame_timers.pop(request_id, None)
        if timer is not None:
            timer.cancel()
        return None

    def cancelIdleCallback(self, callback_id: int):
        timer = self._idle_callback_timers.pop(callback_id, None)
        if timer is not None:
            timer.cancel()
        return None

    def moveBy(self, x: int, y: int):
        return self.moveTo(self.screenLeft + int(x), self.screenTop + int(y))

    def moveTo(self, x: int, y: int):
        host_move = getattr(self._host, "move_to", None)
        if callable(host_move):
            host_move(int(x), int(y))
            return None
        self._host_moved(int(x), int(y))
        return None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def navigator(self):
        return self._navigator

    def open(
        self,
        url: str = "",
        target: str = "_blank",
        features: str = "",
        replace: bool = False,
    ):
        target_window = None
        if target == "_self" or (self.name and target == self.name):
            target_window = self
        elif target == "_parent":
            target_window = self.parent
        elif target == "_top":
            target_window = self.top
        if target_window is not None:
            if url:
                target_window.location = url
            return target_window

        host_open = getattr(self._host, "open_window", None)
        if callable(host_open):
            child = host_open(
                url=url,
                target=target,
                features=features,
                replace=replace,
                opener=self,
            )
            if child is not None:
                return child

        child = Window(doc=Document(), opener=self, parent=self, url="about:blank")
        if url:
            child.location = url
        return child

    @property
    def outerHeight(self):
        return self._outer_height

    @property
    def outerWidth(self):
        return self._outer_width

    @property
    def pageXOffset(self):
        return self.scrollX

    @property
    def pageYOffset(self):
        return self.scrollY

    def postMessage(self, message: Any, targetOrigin: str = "*", transfer: list[Any] | None = None):
        if targetOrigin not in ("*", "/") and targetOrigin != self.origin:
            return None
        event = MessageEvent(
            "message",
            {
                "data": message,
                "origin": self.origin,
                "source": self,
                "ports": transfer or [],
                "bubbles": False,
                "cancelable": False,
            },
        )
        self.dispatchEvent(event)
        return None

    def print(self):
        self.dispatchEvent(Event("beforeprint", {"bubbles": False, "cancelable": False}))
        self.dispatchEvent(Event("afterprint", {"bubbles": False, "cancelable": False}))
        return None

    def queueMicrotask(self, callback: Callable[[], Any]):
        if not callable(callback):
            raise TypeError("queueMicrotask callback must be callable")
        self._microtask_queue.append(callback)
        if self._running_microtasks:
            return None
        self._running_microtasks = True
        try:
            while self._microtask_queue:
                self._microtask_queue.pop(0)()
        finally:
            self._running_microtasks = False
        return None

    def requestAnimationFrame(self, callback: Callable[[float], Any]) -> int:  # type: ignore[override]
        if not callable(callback):
            raise TypeError("requestAnimationFrame callback must be callable")

        host_request = getattr(self._host, "request_animation_frame", None)
        if callable(host_request):
            return host_request(callback)

        request_id = self._next_animation_frame_id
        self._next_animation_frame_id += 1

        def run():
            self._animation_frame_timers.pop(request_id, None)
            callback(self.performance.now())

        timer = threading.Timer(1 / 60, run)
        timer.daemon = True
        self._animation_frame_timers[request_id] = timer
        timer.start()
        return request_id

    def requestIdleCallback(
        self,
        callback: Callable[[IdleDeadline], Any],
        options: dict[str, Any] | None = None,
    ) -> int:
        if not callable(callback):
            raise TypeError("requestIdleCallback callback must be callable")
        options = options or {}
        timeout = options.get("timeout")
        delay = 0.01
        did_timeout = False
        if isinstance(timeout, (int, float)) and timeout <= 0:
            delay = 0
            did_timeout = True
        callback_id = self._next_idle_callback_id
        self._next_idle_callback_id += 1

        def run():
            self._idle_callback_timers.pop(callback_id, None)
            callback(IdleDeadline(did_timeout=did_timeout))

        timer = threading.Timer(delay, run)
        timer.daemon = True
        self._idle_callback_timers[callback_id] = timer
        timer.start()
        return callback_id

    def resizeBy(self, x: int, y: int):
        return self.resizeTo(self.outerWidth + int(x), self.outerHeight + int(y))

    def resizeTo(self, width: int, height: int):
        width = max(0, int(width))
        height = max(0, int(height))
        host_resize = getattr(self._host, "resize", None)
        if callable(host_resize):
            host_resize(width, height)
            return None
        self._set_viewport(
            width,
            height,
            outer_width=width,
            outer_height=height,
        )
        return None

    @property
    def screen(self) -> Screen:  # type: ignore[override]
        return self._screen

    @property
    def screenX(self) -> int:
        return self.screenLeft

    @property
    def screenY(self) -> int:
        return self.screenTop

    @property
    def screenLeft(self) -> int:
        return self._screen.screenLeft

    @property
    def screenTop(self) -> int:
        return self._screen.screenTop

    def _parse_scroll_args(self, x=0, y=0, **options) -> tuple[int, int]:
        if isinstance(x, dict):
            options = x
            x = options.get("left", options.get("x", self.scrollX))
            y = options.get("top", options.get("y", self.scrollY))
        else:
            x = options.get("left", x)
            y = options.get("top", y)
        return int(x or 0), int(y or 0)

    def scroll(self, x=0, y=0, **options):
        return self.scrollTo(x, y, **options)

    def scrollBy(self, x=0, y=0, **options):
        x, y = self._parse_scroll_args(x, y, **options)
        return self.scrollTo(self.scrollX + x, self.scrollY + y)

    def scrollByLines(self, lines: int):
        return self.scrollBy(0, int(lines) * 40)

    def scrollByPages(self, pages: int):
        return self.scrollBy(0, int(pages) * self.innerHeight)

    def scrollTo(self, x=0, y=0, **options):
        x, y = self._parse_scroll_args(x, y, **options)
        x = max(0, x)
        y = max(0, y)
        changed = x != self._scroll_x or y != self._scroll_y
        self._scroll_x = x
        self._scroll_y = y
        if changed:
            self.dispatchEvent(Event("scroll", {"bubbles": False, "cancelable": False}))
            self.dispatchEvent(Event("scrollend", {"bubbles": False, "cancelable": False}))
        return None

    @property
    def scrollX(self):
        return self._scroll_x

    @property
    def scrollY(self):
        return self._scroll_y

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value=None):
        self._status = "" if value is None else str(value)

    def stop(self):
        self._stopped = True
        return None


window = Window()
alert = window.alert
confirm = window.confirm
prompt = window.prompt
