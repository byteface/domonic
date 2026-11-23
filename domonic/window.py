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
import urllib.parse
from typing import Any, Callable

from domonic import _reflect as _r
from domonic._cookies import DocumentCookies
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
from domonic.webapi.performance import performance
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


class _MediaContext:
    """What a media query is evaluated against."""

    __slots__ = ("width", "height", "features", "resolution", "media_type")

    def __init__(self, width: float, height: float, features: dict, resolution: float, media_type: str) -> None:
        self.width = float(width)
        self.height = float(height)
        self.features = features
        self.resolution = float(resolution or 1.0)
        self.media_type = media_type or "screen"


_MEDIA_TYPES = frozenset({"all", "screen", "print", "speech", "tty", "tv", "projection", "handheld", "braille",
                          "embossed", "aural"})  # fmt: skip
#: range features -> how to read their value (a length, number, ratio or resolution)
_RANGE_FEATURES = {
    "width": "length", "height": "length", "device-width": "length", "device-height": "length",
    "aspect-ratio": "ratio", "device-aspect-ratio": "ratio", "resolution": "resolution",
    "color": "number", "color-index": "number", "monochrome": "number",
}  # fmt: skip
#: discrete features this evaluator answers itself (the rest come from ``features``)
_STATIC_FEATURES = {"grid": "0", "scan": "progressive", "overflow-block": "scroll", "overflow-inline": "scroll",
                    "dynamic-range": "standard", "video-dynamic-range": "standard"}  # fmt: skip


def _media_feature_value(name: str, context: "_MediaContext") -> "float | str | None":
    if name in ("width", "device-width"):
        return context.width
    if name in ("height", "device-height"):
        return context.height
    if name in ("aspect-ratio", "device-aspect-ratio"):
        return context.width / context.height if context.height else float("inf")
    if name == "resolution":
        return context.resolution
    if name == "color":
        return 8.0
    if name in ("color-index", "monochrome"):
        return 0.0
    if name == "orientation":
        return "landscape" if context.width > context.height else "portrait"
    if name in context.features:
        return str(context.features[name]).lower()
    return _STATIC_FEATURES.get(name)


def _media_value(text: str, kind: str, context: "_MediaContext") -> "float | None":
    """A media feature value as a number: px for a length, dppx for a
    resolution, a quotient for a ratio."""
    text = text.strip()
    if kind == "ratio":
        parts = _split_top_level(text, "/")
        if len(parts) > 2:
            return None
        numbers = [_media_value(part, "number", context) for part in parts]
        if None in numbers:
            return None
        values = [float(number or 0.0) for number in numbers]
        if len(values) == 1:
            return values[0]
        return values[0] / values[1] if values[1] else float("inf")
    if kind == "resolution":
        match = re.fullmatch(r"([+-]?(?:\d+\.?\d*|\.\d+))(dppx|x|dpi|dpcm)", text)
        if match:
            number = float(match.group(1))
            return number / {"dppx": 1.0, "x": 1.0, "dpi": 96.0, "dpcm": 96.0 / 2.54}[match.group(2)]
        return None
    from domonic.style import _eval_math

    result = _eval_math(text, em_px=16.0, rem_px=16.0, viewport=(context.width, context.height))
    if result is None:
        return None
    number, is_length = result
    if kind == "length":
        return number if is_length or number == 0 else None
    return None if is_length else number


_RANGE_OPS = {"<": lambda a, b: a < b, "<=": lambda a, b: a <= b, ">": lambda a, b: a > b,
              ">=": lambda a, b: a >= b, "=": lambda a, b: abs(a - b) < 1e-9}  # fmt: skip
_RANGE_RE = re.compile(r"(<=|>=|<|>|=)")
_FLIPPED = {"<": ">", "<=": ">=", ">": "<", ">=": "<=", "=": "="}


def _evaluate_media_feature(text: str, context: "_MediaContext") -> "bool | None":
    """``( <media-feature> )``'s value: True, False, or None for unknown."""
    if ":" in text and not _RANGE_RE.search(text.split(":", 1)[0]):
        name, value = (part.strip() for part in text.split(":", 1))
        prefix = ""
        if name.startswith(("min-", "max-")) and name[4:] in _RANGE_FEATURES:
            prefix, name = name[:4], name[4:]
        if name in _RANGE_FEATURES:
            actual = _media_feature_value(name, context)
            target = _media_value(value, _RANGE_FEATURES[name], context)
            if target is None or actual is None:
                return None
            return _RANGE_OPS[{"min-": ">=", "max-": "<=", "": "="}[prefix]](actual, target)
        if prefix:
            return None
        actual = _media_feature_value(name, context)
        if actual is None:
            return None
        return str(actual) == value
    pieces = [piece.strip() for piece in _RANGE_RE.split(text)]
    if len(pieces) == 1:
        # boolean context: (color), (hover), (prefers-reduced-motion)
        name = pieces[0]
        actual = _media_feature_value(name, context)
        if actual is None:
            return None
        if isinstance(actual, float):
            return actual != 0
        return actual not in ("none", "no-preference", "0")
    if len(pieces) == 3:
        left, op, right = pieces
        if left in _RANGE_FEATURES:
            name, value, op = left, right, op
        elif right in _RANGE_FEATURES:
            name, value, op = right, left, _FLIPPED[op]  # (1000px < width) is (width > 1000px)
        else:
            return None
        actual = _media_feature_value(name, context)
        target = _media_value(value, _RANGE_FEATURES[name], context)
        if actual is None or target is None:
            return None
        return _RANGE_OPS[op](actual, target)
    if len(pieces) == 5:
        low, low_op, name, high_op, high = pieces
        if name not in _RANGE_FEATURES or (low_op[0] != high_op[0]) or "=" == low_op:
            return None
        actual = _media_feature_value(name, context)
        low_value = _media_value(low, _RANGE_FEATURES[name], context)
        high_value = _media_value(high, _RANGE_FEATURES[name], context)
        if actual is None or low_value is None or high_value is None:
            return None
        return _RANGE_OPS[_FLIPPED[low_op]](actual, low_value) and _RANGE_OPS[high_op](actual, high_value)
    return None


def _evaluate_media_condition(text: str, context: "_MediaContext") -> "bool | None":
    """A ``<media-condition>`` in three-valued logic (True / False / None)."""
    text = text.strip()
    if text.startswith("not ") or text.startswith("not("):
        negated = _evaluate_media_condition(text[3:], context)
        return None if negated is None else not negated
    for word, combine in ((" or ", any), (" and ", all)):
        parts = _split_top_level(text, word)
        if len(parts) > 1:
            values = [_evaluate_media_condition(part, context) for part in parts]
            if combine is any:
                return True if True in values else (None if None in values else False)
            return False if False in values else (None if None in values else True)
    if text.startswith("(") and text.endswith(")"):
        inner = text[1:-1].strip()
        if (
            inner.startswith("(")
            or inner.startswith("not ")
            or _split_top_level(inner, " and ")[1:]
            or (_split_top_level(inner, " or ")[1:])
        ):
            return _evaluate_media_condition(inner, context)
        return _evaluate_media_feature(inner, context)
    return None  # (general-enclosed: unknown)


def _evaluate_media_query(query: str, context: "_MediaContext") -> "bool | None":
    query = " ".join(query.split())
    if not query:
        return None
    words = query.split(" ", 2)
    negate = False
    if words[0] in ("not", "only") and len(words) > 1 and words[1] in _MEDIA_TYPES:
        negate = words[0] == "not"
        query = query.split(" ", 1)[1]
        words = query.split(" ", 2)
    if words[0] in _MEDIA_TYPES:
        media_type = words[0]
        result: "bool | None" = media_type == "all" or media_type == context.media_type
        rest = query[len(media_type) :].strip()
        if rest:
            if not rest.startswith("and "):
                return None
            condition = _evaluate_media_condition(rest[4:], context)
            result = None if condition is None else (result and condition)
        if result is None:
            return None
        return not result if negate else result
    return _evaluate_media_condition(query, context)


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


def _url_origin(url: str | None) -> str | None:
    """``scheme://host[:port]`` of an http(s) URL, else ``None``."""
    parts = urllib.parse.urlsplit(url or "")
    if parts.scheme.lower() not in ("http", "https") or not parts.hostname:
        return None
    return f"{parts.scheme.lower()}://{parts.netloc.rsplit('@', 1)[-1].lower()}"


def _referrer_header(referrer: str | None, target: str, policy: str = "") -> str | None:
    """The ``Referer`` a browser sends from ``referrer`` to ``target`` under
    referrer ``policy`` (https://w3c.github.io/webappsec-referrer-policy/).
    The default, strict-origin-when-cross-origin, sends the full URL (no
    fragment or credentials) to the same origin, the origin elsewhere, and
    nothing from https to http."""
    origin = _url_origin(referrer)
    if origin is None or referrer is None or policy == "no-referrer":
        return None
    parts = urllib.parse.urlsplit(referrer)
    full = urllib.parse.urlunsplit((parts.scheme, parts.netloc.rsplit("@", 1)[-1], parts.path, parts.query, ""))
    same_origin = origin == _url_origin(target)
    downgrade = referrer.lower().startswith("https:") and target.lower().startswith("http:")
    if policy == "unsafe-url":
        return full
    if policy == "origin":
        return origin + "/"
    if policy == "same-origin":
        return full if same_origin else None
    if policy == "origin-when-cross-origin":
        return full if same_origin else origin + "/"
    if policy == "no-referrer-when-downgrade":
        return None if downgrade else full
    if downgrade:
        return None
    if policy == "strict-origin":
        return origin + "/"
    return full if same_origin else origin + "/"


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
        """Whether a media query list matches (Media Queries 4): media types,
        ``and`` / ``or`` / ``not``, every range form (``(width >= 600px)``,
        ``(1000px < width)``, ``(400px <= width <= 900px)``), ``calc()`` and
        ratios in values, and the discrete features from ``features``. An
        unknown feature is unknown, not false: ``not (unknown)`` doesn't
        match either."""
        if not media:
            return False
        context = _MediaContext(width or 0, height or 0, features or cls.DEFAULT_FEATURES, resolution, media_type)
        return any(_evaluate_media_query(query, context) is True for query in _split_top_level(media.lower(), ","))

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


# what a browser accepts when it navigates (https://fetch.spec.whatwg.org/#fetching)
_NAVIGATION_ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"


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
        self._user_agent: str | None = None
        # the user's preferred languages, most preferred first
        # (https://html.spec.whatwg.org/#dom-navigator-languages)
        self.languages: list[str] = ["en-US", "en"]

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
        """The ``User-Agent`` header the window sends. Read-only in a browser;
        here it can be set, and the window's requests send the new value."""
        if self._user_agent is not None:
            return self._user_agent
        return f"domonic/{self.appName} ({self.platform})"

    @userAgent.setter
    def userAgent(self, value: str) -> None:
        self._user_agent = None if value is None else str(value)

    @property
    def language(self) -> str:
        """The most preferred of ``languages``."""
        return self.languages[0] if self.languages else "en-US"

    def _accept_language(self) -> str:
        """``languages`` as an ``Accept-Language`` value, weighted the way
        Chrome weights them: ``en-US,en;q=0.9``."""
        values = []
        for index, tag in enumerate(self.languages or [self.language]):
            weight = max(1.0 - index / 10, 0.1)
            values.append(tag if index == 0 else f"{tag};q={weight:g}")
        return ",".join(values)

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
        # a new browsing context starts on about:blank (HTML: creating a new browsing context)
        self._location: Location = Location(url or "about:blank")
        self._document: Document = doc if doc is not None else document
        self.attach(self._document)
        self._document.URL = self._location.href
        self._console: Console = Console()
        self.cookieStore: CookieStore = CookieStore(DocumentCookies(self._document))
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
            self.cookieStore = CookieStore(DocumentCookies(self._document))

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

    def _http_session(self) -> Any:
        """One ``requests.Session`` per window, so cookies a page sets (a
        login, say) are sent with the window's later navigations."""
        session = self.__dict__.get("_requests_session")
        if session is None:
            import requests

            session = requests.Session()
            self.__dict__["_requests_session"] = session
        return session

    def _default_headers(self, accept: str) -> dict[str, str]:
        """The headers a browser adds to every request it makes
        (https://fetch.spec.whatwg.org/#fetching): ``User-Agent`` from
        ``navigator.userAgent``, ``Accept`` for what is being fetched, and
        ``Accept-Language`` from ``navigator.languages``."""
        return {
            "User-Agent": self._navigator.userAgent,
            "Accept": accept,
            "Accept-Language": self._navigator._accept_language(),
        }

    def _fetch_document(
        self,
        url: str,
        method: str = "GET",
        data: Any = None,
        files: Any = None,
        headers: dict[str, str] | None = None,
        referrer: str | None = None,
    ) -> Document | None:
        """Load ``url`` as a document, or ``None`` when it can't be loaded (not
        http(s), a network error, an error status). After a redirect
        ``page.URL`` is where it ended up."""
        if urllib.parse.urlsplit(url).scheme.lower() not in ("http", "https"):
            return None
        try:
            import requests  # noqa: F401
        except ModuleNotFoundError:
            return None

        request_headers: dict[str, str] = self._default_headers(_NAVIGATION_ACCEPT)
        request_headers["Upgrade-Insecure-Requests"] = "1"
        referer = _referrer_header(referrer, url)
        if referer:
            request_headers["Referer"] = referer
        if method.upper() != "GET":
            request_headers["Origin"] = _url_origin(referrer) or "null"
        request_headers.update(headers or {})
        try:
            response = self._http_session().request(
                method, url, data=data, files=files, headers=request_headers, timeout=5
            )
            response.raise_for_status()
        except Exception:
            return None

        # always a Document, as scrape() does: a response that is only a fragment
        # (<p>...</p>) would otherwise come back as that element
        page = domonic.parseString(response.text, document=True)
        if page is not None:
            final_url = url
            if getattr(response, "history", None):  # redirected
                final_url = str(response.url)
                fragment = urllib.parse.urlsplit(url).fragment
                if fragment and "#" not in final_url:  # a redirect keeps the request's fragment
                    final_url += "#" + fragment
            page.URL = final_url
        return page

    def fetch(self, input: Any, init: Any = None, **kwargs: Any) -> Promise:  # type: ignore[override]
        """``fetch()`` as the page calls it
        (https://fetch.spec.whatwg.org/#fetch-method): a ``Promise`` for a
        :class:`domonic.webapi.fetch.Response`.

        A relative URL resolves against the document's base URL. The
        window's cookies go with the request, and cookies the response sets
        are kept, when its ``credentials`` say so: ``"same-origin"`` (the
        default) for the page's own origin, ``"include"`` for any,
        ``"omit"`` never. ``Referer`` follows the request's referrer policy;
        ``Origin`` goes with a cross-origin or non-GET request. Other keyword
        arguments go to ``requests``.
        """
        from domonic.webapi import fetch as fetch_api

        request = fetch_api.Request(input, init=init)
        page_url = str(getattr(self._document, "URL", "") or "")
        request.url = _r.join_url(_r.base_url_of(self._document), request.url)
        page_origin = _url_origin(page_url)
        target_origin = _url_origin(request.url)
        same_origin = page_origin is not None and page_origin == target_origin

        for name, value in self._default_headers("*/*").items():
            if not request.headers.has(name):
                request.headers.set(name, value)
        if not request.headers.has("referer"):
            referrer = page_url if request.referrer == "about:client" else str(request.referrer or "")
            if referrer and _url_origin(referrer) != page_origin:
                referrer = page_url  # a script may only claim a referrer on its own origin
            referer = _referrer_header(referrer, request.url, str(request.referrerPolicy or ""))
            if referer:
                request.headers.set("Referer", referer)
        if not request.headers.has("origin") and (
            (target_origin is not None and not same_origin and request.mode == "cors")
            or request.method not in ("GET", "HEAD")
        ):
            no_referrer = request.referrerPolicy == "no-referrer"
            request.headers.set("Origin", "null" if no_referrer or page_origin is None else page_origin)

        session = None
        if request.credentials == "include" or (request.credentials == "same-origin" and same_origin):
            try:
                session = self._http_session()
            except ModuleNotFoundError:
                session = None
        promise = fetch_api._fetch(request, kwargs, session=session)
        response = promise.data if promise.state == "fulfilled" else None
        if isinstance(response, fetch_api.Response) and target_origin is not None:
            response.type = "basic" if same_origin else "cors"
        return promise

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
        # about:blank / about:srcdoc are potentially trustworthy (Secure Contexts 3.1)
        if href.split("#", 1)[0] in ("about:blank", "about:srcdoc"):
            return True
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
        self._navigate(self._normalize_url(value))

    def _navigate(
        self,
        href: str,
        *,
        method: str = "GET",
        data: Any = None,
        files: Any = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        """Navigate to ``href`` (https://html.spec.whatwg.org/#navigate): what
        ``location = url``, a link click and a form submission do.

        A change of fragment only stays on the document and fires
        ``hashchange``. Anything else loads the response (a GET, or a form's
        POST) as the new document; when the load fails the old document stays.
        """
        previous_href = self._location.href
        if getattr(self._history, "skip_update", False) is False:
            self._history._update(href)
        self._location = Location(href)
        self._document.URL = href
        self._document.referrer = previous_href or ""
        same_document = previous_href.split("#", 1)[0] == href.split("#", 1)[0]
        if previous_href != href and same_document:
            self.dispatchEvent(HashChangeEvent("hashchange", {"oldURL": previous_href, "newURL": href}))
        if same_document and "#" in href and method.upper() == "GET":
            return  # a fragment navigation: the document stays

        loaded_document = self._fetch_document(
            href, method=method, data=data, files=files, headers=headers, referrer=previous_href
        )
        if loaded_document is None:
            return
        final_url = str(getattr(loaded_document, "URL", "") or href)
        if final_url != href:  # redirected: the window ends up at the final URL
            self._location = Location(final_url)
            entry = self._history._current_entry()
            if entry is not None and getattr(self._history, "skip_update", False) is False:
                entry.url = final_url
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
        """Stop loading (https://html.spec.whatwg.org/#dom-window-stop): a
        parse in progress via ``document.write()`` ignores further input;
        ``document.close()`` still finalises what has landed."""
        self._stopped = True
        document = getattr(self, "_document", None)
        session = document.__dict__.get("_parser_session") if document is not None else None
        if session is not None:
            session.abort()
        return None


window = Window()
alert = window.alert
confirm = window.confirm
prompt = window.prompt
