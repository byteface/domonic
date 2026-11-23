"""
domonic._reflect
================

IDL attributes that reflect content attributes, as the HTML spec defines them:
https://html.spec.whatwg.org/multipage/common-dom-interfaces.html#reflecting-content-attributes-in-idl-attributes

Each class here is a descriptor declared in an element's class body, e.g.
``alt = _r.String("alt")`` on ``HTMLImageElement``. Reading it parses the
content attribute (``""`` / ``False`` / ``0`` when it is absent); writing it
sets the attribute. Assigning ``None`` removes the attribute, which is the
Pythonic reading of "unset" (JavaScript would store the string ``"null"``).

Private to ``domonic.dom``: nothing here imports the DOM at module level.
"""

from __future__ import annotations

import math
import re
from typing import Any, Generic, Iterable, TypeVar, overload
from urllib.parse import urljoin, urlsplit

T = TypeVar("T")

LONG_MIN = -(2**31)
LONG_MAX = 2**31 - 1

ASCII_WHITESPACE = "\t\n\f\r "

_INTEGER_RE = re.compile(r"[\t\n\f\r ]*([+-]?)([0-9]+)")
_FLOAT_RE = re.compile(r"[\t\n\f\r ]*([+-]?)([0-9]*)(?:\.([0-9]+))?(?:[eE]([+-]?[0-9]+))?")

# Schemes a relative reference can resolve against (a base such as
# ``about:blank`` cannot be a base, so a relative URL stays as written).
_HIERARCHICAL_SCHEMES = frozenset({"http", "https", "file", "ftp", "ws", "wss"})
_SPECIAL_SCHEMES = frozenset({"http", "https", "ftp", "ws", "wss"})


# -- parsing rules (https://html.spec.whatwg.org/#numbers) -------------------


def parse_integer(value: Any) -> int | None:
    """The HTML "rules for parsing integers": leading whitespace, an optional
    sign, then digits. Trailing junk is ignored; no digits is an error."""
    if value is None:
        return None
    match = _INTEGER_RE.match(str(value))
    if match is None:
        return None
    number = int(match.group(2))
    return -number if match.group(1) == "-" else number


def parse_non_negative_integer(value: Any) -> int | None:
    number = parse_integer(value)
    if number is None or number < 0:
        return None
    return number


def parse_float(value: Any) -> float | None:
    """The HTML "rules for parsing floating-point number values"."""
    if value is None:
        return None
    match = _FLOAT_RE.match(str(value))
    if match is None or not (match.group(2) or match.group(3)):
        return None
    sign, whole, fraction, exponent = match.groups()
    text = f"{sign}{whole or '0'}.{fraction or '0'}e{exponent or '0'}"
    try:
        number = float(text)
    except (ValueError, OverflowError):
        return None
    if math.isinf(number) or math.isnan(number):
        return None
    return number


def format_number(value: float) -> str:
    """A double as JavaScript's ``String(number)`` writes it (``1``, not ``1.0``)."""
    if value == int(value) and abs(value) < 1e21:
        return str(int(value))
    return repr(value)


def to_long(value: Any) -> int:
    """WebIDL ``long`` conversion, roughly: ``True`` -> 1, ``"7"`` -> 7, ``2.9`` -> 2."""
    try:
        number = float(value.strip(ASCII_WHITESPACE) or 0) if isinstance(value, str) else float(value)
    except ValueError:  # Number("abc") is NaN, which a long converts to 0
        return 0
    if math.isnan(number) or math.isinf(number):
        return 0
    return int(number)


def to_double(value: Any) -> float:
    number = float(value)
    if math.isnan(number) or math.isinf(number):
        raise TypeError("The provided double value is non-finite.")
    return number


# -- content attribute access ------------------------------------------------


def content_attribute(element: Any, name: str) -> Any:
    try:
        return element.getAttribute(name)
    except AttributeError:  # read before Node.__init__ set up kwargs
        return None


def has_content_attribute(element: Any, name: str) -> bool:
    try:
        return bool(element.hasAttribute(name))
    except AttributeError:
        return False


def as_string(value: Any) -> str:
    """A stored attribute value as the string a browser would see. domonic
    stores ``True`` / ``False`` for boolean-style attributes and renders them
    as ``"true"`` / ``"false"``, so they read back the same way."""
    if value is None:
        return ""
    if value is True:
        return "true"
    if value is False:
        return "false"
    return str(value)


def index_size_error(message: str) -> Exception:
    from domonic.dom import DOMException

    return DOMException(message, "IndexSizeError")


# -- URLs ---------------------------------------------------------------------


def document_base_url(element: Any) -> str:
    """The absolute base URL for ``element``'s document, or ``""`` when there
    is none to resolve against (a detached element, or a document without an
    http(s)/file URL)."""
    return base_url_of(getattr(element, "ownerDocument", None))


def base_url_of(document: Any) -> str:
    """``document``'s absolute base URL (its ``<base href>`` resolved against
    its URL), or ``""`` when it has none to resolve against."""
    if document is None:
        return ""
    page_url = str(getattr(document, "URL", "") or "")
    base_href = str(getattr(document, "baseURI", "") or "")
    if page_url and base_href:
        try:
            base = urljoin(page_url, base_href)
        except ValueError:
            base = page_url
    else:
        base = base_href or page_url
    if urlsplit(base).scheme.lower() not in _HIERARCHICAL_SCHEMES:
        return ""
    return base


def resolve_url(element: Any, value: str) -> str:
    """``value`` parsed against the document's base URL and serialised, or
    ``value`` unchanged when it cannot be resolved (HTML: reflecting a URL)."""
    return join_url(document_base_url(element), value)


def join_url(base: str, value: str) -> str:
    """``value`` resolved against ``base``; ``value`` as written when ``base``
    cannot serve as a base and ``value`` is not itself absolute."""
    if base and urlsplit(base).scheme.lower() not in _HIERARCHICAL_SCHEMES:
        base = ""
    reference = value.strip(ASCII_WHITESPACE)
    if not base and not urlsplit(reference).scheme:
        return value
    try:
        resolved = urljoin(base, reference) if base else reference
        parts = urlsplit(resolved)
    except ValueError:
        return value
    if parts.scheme.lower() in _SPECIAL_SCHEMES and parts.netloc and not parts.path:
        resolved = parts._replace(path="/").geturl()
    return resolved


def document_url(element: Any) -> str:
    document = getattr(element, "ownerDocument", None)
    return str(getattr(document, "URL", "") or "") if document is not None else ""


# -- descriptors ----------------------------------------------------------------


class Reflected(Generic[T]):
    """Base descriptor: ``attr`` is the content attribute's (lower-case) name."""

    __slots__ = ("attr",)

    def __init__(self, attr: str) -> None:
        self.attr = attr

    @overload
    def __get__(self, element: None, owner: Any = None) -> "Reflected[T]": ...

    @overload
    def __get__(self, element: object, owner: Any = None) -> T: ...

    def __get__(self, element: Any, owner: Any = None) -> Any:
        if element is None:
            return self
        return self.read(element)

    def __set__(self, element: Any, value: Any) -> None:
        if value is None:
            element.removeAttribute(self.attr)
            return
        self.write(element, value)

    def read(self, element: Any) -> T:
        raise NotImplementedError

    def write(self, element: Any, value: Any) -> None:
        element.setAttribute(self.attr, str(value))

    def __repr__(self) -> str:
        return f"<{type(self).__name__} reflecting {self.attr!r}>"


class String(Reflected[str]):
    """``DOMString``: the attribute's value, ``""`` when absent."""

    __slots__ = ()

    def read(self, element: Any) -> str:
        return as_string(content_attribute(element, self.attr))


class URL(Reflected[str]):
    """``USVString`` reflecting a URL: resolved against the document's base
    URL when there is one, otherwise the value as written."""

    __slots__ = ()

    def read(self, element: Any) -> str:
        value = content_attribute(element, self.attr)
        if value is None:
            return ""
        return resolve_url(element, as_string(value))


class FormAction(URL):
    """``formAction`` / ``form.action``: a missing or empty attribute is the
    document's URL (https://html.spec.whatwg.org/#dom-fs-action)."""

    __slots__ = ()

    def read(self, element: Any) -> str:
        value = content_attribute(element, self.attr)
        if value is None or as_string(value) == "":
            return document_url(element)
        return resolve_url(element, as_string(value))


class Boolean(Reflected[bool]):
    """``boolean``: true when the attribute is present, whatever its value."""

    __slots__ = ()

    def read(self, element: Any) -> bool:
        return has_content_attribute(element, self.attr)

    def write(self, element: Any, value: Any) -> None:
        if value:
            element.setAttribute(self.attr, "")
        else:
            element.removeAttribute(self.attr)


class Long(Reflected[int]):
    """``long`` (optionally "limited to only non-negative numbers")."""

    __slots__ = ("default", "non_negative")

    def __init__(self, attr: str, default: int = 0, non_negative: bool = False) -> None:
        super().__init__(attr)
        self.default = default
        self.non_negative = non_negative

    def read(self, element: Any) -> int:
        number = parse_integer(content_attribute(element, self.attr))
        if number is None or not LONG_MIN <= number <= LONG_MAX:
            return self.default
        if self.non_negative and number < 0:
            return self.default
        return number

    def write(self, element: Any, value: Any) -> None:
        number = to_long(value)
        if self.non_negative and number < 0:
            raise index_size_error(f"The value provided ({number}) is negative.")
        element.setAttribute(self.attr, str(number))


class UnsignedLong(Reflected[int]):
    """``unsigned long``, optionally "limited to only positive numbers"
    (``positive``; with ``fallback`` a 0 is replaced by the default instead of
    throwing) or clamped to a range (``clamp=(low, high)``)."""

    __slots__ = ("default", "positive", "fallback", "clamp")

    def __init__(
        self,
        attr: str,
        default: int = 0,
        positive: bool = False,
        fallback: bool = False,
        clamp: tuple[int, int] | None = None,
    ) -> None:
        super().__init__(attr)
        self.default = default
        self.positive = positive
        self.fallback = fallback
        self.clamp = clamp

    def read(self, element: Any) -> int:
        number = parse_non_negative_integer(content_attribute(element, self.attr))
        if number is None:
            return self.default
        if self.clamp is not None:
            low, high = self.clamp
            return max(low, min(high, number))
        low = 1 if self.positive else 0
        if not low <= number <= LONG_MAX:
            return self.default
        return number

    def write(self, element: Any, value: Any) -> None:
        number = to_long(value)
        if self.positive and number == 0 and not self.fallback:
            raise index_size_error("The value provided is 0, which is an invalid size.")
        low = 1 if self.positive else 0
        if not low <= number <= LONG_MAX:
            number = self.default
        element.setAttribute(self.attr, str(number))


class Double(Reflected[float]):
    """``double`` (optionally "limited to only positive numbers")."""

    __slots__ = ("default", "positive")

    def __init__(self, attr: str, default: float = 0.0, positive: bool = False) -> None:
        super().__init__(attr)
        self.default = default
        self.positive = positive

    def read(self, element: Any) -> float:
        number = parse_float(content_attribute(element, self.attr))
        if number is None or (self.positive and number <= 0):
            return self.default
        return number

    def write(self, element: Any, value: Any) -> None:
        number = to_double(value)
        if self.positive and number <= 0:
            return
        element.setAttribute(self.attr, format_number(number))


class Enumerated(Reflected[Any]):
    """An enumerated attribute "limited to only known values".

    ``keywords`` are the canonical keywords; ``aliases`` maps other accepted
    spellings (e.g. ``""``) to one. A missing attribute reads as ``missing``
    (``None`` for a nullable attribute such as ``crossOrigin``), an
    unrecognised value as ``invalid``.
    """

    __slots__ = ("keywords", "missing", "invalid")

    def __init__(
        self,
        attr: str,
        keywords: Iterable[str],
        missing: str | None = "",
        invalid: str = "",
        aliases: dict[str, str] | None = None,
    ) -> None:
        super().__init__(attr)
        table = {keyword.lower(): keyword for keyword in keywords}
        table.update({alias.lower(): keyword for alias, keyword in (aliases or {}).items()})
        self.keywords = table
        self.missing = missing
        self.invalid = invalid

    def read(self, element: Any) -> Any:
        value = content_attribute(element, self.attr)
        if value is None:
            return self.missing
        return self.keywords.get(as_string(value).lower(), self.invalid)


class TokenList(Reflected[Any]):
    """A ``DOMTokenList`` over the attribute (``relList``, ``sandbox``, ...).
    Assigning a string sets the attribute ([PutForwards=value])."""

    __slots__ = ("supported",)

    def __init__(self, attr: str, supported: Iterable[str] | None = None) -> None:
        super().__init__(attr)
        self.supported = frozenset(token.lower() for token in supported) if supported is not None else None

    def read(self, element: Any) -> Any:
        from domonic.dom import DOMTokenList

        return DOMTokenList(element, self.attr, self.supported)

    def write(self, element: Any, value: Any) -> None:
        element.setAttribute(self.attr, as_string(value))


# -- keyword tables -------------------------------------------------------------

REFERRER_POLICIES = (
    "",
    "no-referrer",
    "no-referrer-when-downgrade",
    "same-origin",
    "origin",
    "strict-origin",
    "origin-when-cross-origin",
    "strict-origin-when-cross-origin",
    "unsafe-url",
)
CROSS_ORIGIN = ("anonymous", "use-credentials")
FORM_ENCTYPES = ("application/x-www-form-urlencoded", "multipart/form-data", "text/plain")
FORM_METHODS = ("get", "post", "dialog")
FETCH_PRIORITIES = ("high", "low", "auto")
LOADING = ("lazy", "eager")
# rel tokens a user agent processes (https://html.spec.whatwg.org/#linkTypes)
HYPERLINK_REL_TOKENS = ("noreferrer", "noopener", "opener")
LINK_REL_TOKENS = (
    "alternate",
    "dns-prefetch",
    "expect",
    "icon",
    "manifest",
    "modulepreload",
    "next",
    "pingback",
    "preconnect",
    "prefetch",
    "preload",
    "search",
    "stylesheet",
)
SANDBOX_TOKENS = (
    "allow-downloads",
    "allow-forms",
    "allow-modals",
    "allow-orientation-lock",
    "allow-pointer-lock",
    "allow-popups",
    "allow-popups-to-escape-sandbox",
    "allow-presentation",
    "allow-same-origin",
    "allow-scripts",
    "allow-top-navigation",
    "allow-top-navigation-by-user-activation",
    "allow-top-navigation-to-custom-protocols",
)
# https://fetch.spec.whatwg.org/#concept-potential-destination
POTENTIAL_DESTINATIONS = (
    "fetch",
    "audio",
    "audioworklet",
    "document",
    "embed",
    "font",
    "frame",
    "iframe",
    "image",
    "json",
    "manifest",
    "object",
    "paintworklet",
    "report",
    "script",
    "serviceworker",
    "sharedworker",
    "style",
    "track",
    "video",
    "webidentity",
    "worker",
    "xslt",
)


def referrer_policy() -> Enumerated:
    return Enumerated("referrerpolicy", REFERRER_POLICIES)


def cross_origin() -> Enumerated:
    # nullable: no attribute is null; "" is the Anonymous state
    return Enumerated("crossorigin", CROSS_ORIGIN, missing=None, invalid="anonymous", aliases={"": "anonymous"})


def fetch_priority() -> Enumerated:
    return Enumerated("fetchpriority", FETCH_PRIORITIES, missing="auto", invalid="auto")


def loading() -> Enumerated:
    return Enumerated("loading", LOADING, missing="eager", invalid="eager")


def form_enctype(attr: str = "formenctype", missing: str = "") -> Enumerated:
    return Enumerated(attr, FORM_ENCTYPES, missing=missing, invalid="application/x-www-form-urlencoded")


def form_method(attr: str = "formmethod", missing: str = "") -> Enumerated:
    return Enumerated(attr, FORM_METHODS, missing=missing, invalid="get")


def install_keyword_alias(cls: type, keyword: str, descriptor: Reflected[Any]) -> None:
    """Expose ``descriptor`` under a Python keyword (``script.async``,
    ``link.as``): reachable with ``getattr`` the way a JS port spells it."""
    setattr(cls, keyword, descriptor)
