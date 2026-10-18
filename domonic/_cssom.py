"""
domonic._cssom
==============

Internal support module for :mod:`domonic.style`. A data-driven registry of CSS
properties: their initial values, whether they inherit, and how shorthand
properties map to their longhand components.

Used by :class:`domonic.style.CSSStyleDeclaration` for shorthand expansion /
reconstruction and by ``window.getComputedStyle`` for initial / inherited
value resolution. Kept deliberately small and declarative - it does not try to
mirror every property a browser knows, only the ones worth resolving.
"""

from __future__ import annotations

import re
from typing import Callable

# --- inheritance ----------------------------------------------------------
# CSS properties that inherit from the parent element by default.
INHERITED_PROPERTIES: frozenset[str] = frozenset(
    {
        "azimuth",
        "border-collapse",
        "border-spacing",
        "caption-side",
        "color",
        "cursor",
        "direction",
        "empty-cells",
        "font",
        "font-family",
        "font-feature-settings",
        "font-kerning",
        "font-language-override",
        "font-optical-sizing",
        "font-size",
        "font-size-adjust",
        "font-stretch",
        "font-style",
        "font-synthesis",
        "font-variant",
        "font-variant-alternates",
        "font-variant-caps",
        "font-variant-east-asian",
        "font-variant-ligatures",
        "font-variant-numeric",
        "font-variant-position",
        "font-variation-settings",
        "font-weight",
        "hanging-punctuation",
        "hyphens",
        "image-rendering",
        "letter-spacing",
        "line-break",
        "line-height",
        "list-style",
        "list-style-image",
        "list-style-position",
        "list-style-type",
        "orphans",
        "overflow-wrap",
        "paint-order",
        "pointer-events",
        "quotes",
        "ruby-position",
        "tab-size",
        "text-align",
        "text-align-last",
        "text-combine-upright",
        "text-decoration-skip-ink",
        "text-indent",
        "text-justify",
        "text-orientation",
        "text-rendering",
        "text-shadow",
        "text-transform",
        "text-underline-offset",
        "text-underline-position",
        "visibility",
        "white-space",
        "widows",
        "word-break",
        "word-spacing",
        "word-wrap",
        "writing-mode",
        "accent-color",
        "caret-color",
        "color-scheme",
        "text-wrap",
        "text-wrap-mode",
        "text-wrap-style",
        "font-variant-emoji",
        "-webkit-text-fill-color",
        "-webkit-text-stroke-color",
        "-webkit-text-stroke-width",
        "text-emphasis-style",
        "text-emphasis-color",
        "text-emphasis-position",
        "word-break",
        # custom properties inherit
    }
)

# --- initial values -----------------------------------------------------
# Only properties with a non-empty, meaningful initial value are listed. Any
# property not here resolves its initial value to "" (good enough for a
# non-layout engine).
INITIAL_VALUES: dict[str, str] = {
    "align-content": "normal",
    "align-items": "normal",
    "align-self": "auto",
    "animation-delay": "0s",
    "animation-direction": "normal",
    "animation-duration": "0s",
    "animation-fill-mode": "none",
    "animation-iteration-count": "1",
    "animation-name": "none",
    "animation-play-state": "running",
    "animation-timing-function": "ease",
    "appearance": "none",
    "background-attachment": "scroll",
    "background-clip": "border-box",
    "background-color": "rgba(0, 0, 0, 0)",
    "background-image": "none",
    "background-origin": "padding-box",
    "background-position": "0% 0%",
    "background-repeat": "repeat",
    "background-size": "auto",
    "border-bottom-color": "currentcolor",
    "border-bottom-left-radius": "0px",
    "border-bottom-right-radius": "0px",
    "border-bottom-style": "none",
    "border-bottom-width": "medium",
    "border-collapse": "separate",
    "border-image-outset": "0",
    "border-image-repeat": "stretch",
    "border-image-slice": "100%",
    "border-image-source": "none",
    "border-image-width": "1",
    "border-left-color": "currentcolor",
    "border-left-style": "none",
    "border-left-width": "medium",
    "border-right-color": "currentcolor",
    "border-right-style": "none",
    "border-right-width": "medium",
    "border-spacing": "0px",
    "border-top-color": "currentcolor",
    "border-top-left-radius": "0px",
    "border-top-right-radius": "0px",
    "border-top-style": "none",
    "border-top-width": "medium",
    "bottom": "auto",
    "box-sizing": "content-box",
    "caption-side": "top",
    "clear": "none",
    "color": "rgb(0, 0, 0)",
    "column-count": "auto",
    "column-gap": "normal",
    "column-width": "auto",
    "cursor": "auto",
    "direction": "ltr",
    "display": "inline",
    "empty-cells": "show",
    "flex-basis": "auto",
    "flex-direction": "row",
    "flex-grow": "0",
    "flex-shrink": "1",
    "flex-wrap": "nowrap",
    "float": "none",
    "font-family": "",
    "font-size": "medium",
    "font-stretch": "normal",
    "font-style": "normal",
    "font-variant": "normal",
    "font-weight": "normal",
    "grid-auto-columns": "auto",
    "grid-auto-flow": "row",
    "grid-auto-rows": "auto",
    "grid-column-end": "auto",
    "grid-column-start": "auto",
    "grid-row-end": "auto",
    "grid-row-start": "auto",
    "grid-template-areas": "none",
    "grid-template-columns": "none",
    "grid-template-rows": "none",
    "height": "auto",
    "hyphens": "manual",
    "justify-content": "normal",
    "justify-items": "legacy",
    "justify-self": "auto",
    "left": "auto",
    "letter-spacing": "normal",
    "line-height": "normal",
    "list-style-image": "none",
    "list-style-position": "outside",
    "list-style-type": "disc",
    "margin-bottom": "0px",
    "margin-left": "0px",
    "margin-right": "0px",
    "margin-top": "0px",
    "max-height": "none",
    "max-width": "none",
    "min-height": "auto",
    "min-width": "auto",
    "object-fit": "fill",
    "object-position": "50% 50%",
    "opacity": "1",
    "order": "0",
    "outline-color": "currentcolor",
    "outline-offset": "0px",
    "outline-style": "none",
    "outline-width": "medium",
    "overflow-x": "visible",
    "overflow-y": "visible",
    "padding-bottom": "0px",
    "padding-left": "0px",
    "padding-right": "0px",
    "padding-top": "0px",
    "pointer-events": "auto",
    "position": "static",
    "resize": "none",
    "right": "auto",
    "row-gap": "normal",
    "table-layout": "auto",
    "text-align": "start",
    "text-decoration-color": "currentcolor",
    "text-decoration-line": "none",
    "text-decoration-style": "solid",
    "text-indent": "0px",
    "text-transform": "none",
    "top": "auto",
    "transform": "none",
    "transform-origin": "50% 50%",
    "transition-delay": "0s",
    "transition-duration": "0s",
    "transition-property": "all",
    "transition-timing-function": "ease",
    "vertical-align": "baseline",
    "visibility": "visible",
    "white-space": "normal",
    "width": "auto",
    "word-break": "normal",
    "word-spacing": "normal",
    "writing-mode": "horizontal-tb",
    "z-index": "auto",
    # (CSS Values / the property specs' "Initial" lines)
    "accent-color": "auto",
    "aspect-ratio": "auto",
    "backdrop-filter": "none",
    "backface-visibility": "visible",
    "box-shadow": "none",
    "break-after": "auto",
    "break-before": "auto",
    "break-inside": "auto",
    "caret-color": "auto",
    "clip-path": "none",
    "color-scheme": "normal",
    "column-fill": "balance",
    "column-span": "none",
    "contain": "none",
    "container-name": "none",
    "container-type": "normal",
    "content": "normal",
    "content-visibility": "visible",
    "counter-increment": "none",
    "counter-reset": "none",
    "counter-set": "none",
    "filter": "none",
    "isolation": "auto",
    "mask-image": "none",
    "mix-blend-mode": "normal",
    "perspective": "none",
    "quotes": "auto",
    "rotate": "none",
    "scale": "none",
    "scroll-behavior": "auto",
    "text-overflow": "clip",
    "text-wrap-mode": "wrap",
    "text-wrap-style": "auto",
    "touch-action": "auto",
    "transform-style": "flat",
    "translate": "none",
    "user-select": "auto",
    "will-change": "auto",
}

# --- shorthand -> longhand ---------------------------------------------
# Order matters for reconstruction (values are emitted in this order).
SHORTHANDS: dict[str, tuple[str, ...]] = {
    "margin": ("margin-top", "margin-right", "margin-bottom", "margin-left"),
    "padding": ("padding-top", "padding-right", "padding-bottom", "padding-left"),
    "inset": ("top", "right", "bottom", "left"),
    "border-width": (
        "border-top-width",
        "border-right-width",
        "border-bottom-width",
        "border-left-width",
    ),
    "border-style": (
        "border-top-style",
        "border-right-style",
        "border-bottom-style",
        "border-left-style",
    ),
    "border-color": (
        "border-top-color",
        "border-right-color",
        "border-bottom-color",
        "border-left-color",
    ),
    "border-radius": (
        "border-top-left-radius",
        "border-top-right-radius",
        "border-bottom-right-radius",
        "border-bottom-left-radius",
    ),
    "border-top": (
        "border-top-width",
        "border-top-style",
        "border-top-color",
    ),
    "border-right": (
        "border-right-width",
        "border-right-style",
        "border-right-color",
    ),
    "border-bottom": (
        "border-bottom-width",
        "border-bottom-style",
        "border-bottom-color",
    ),
    "border-left": (
        "border-left-width",
        "border-left-style",
        "border-left-color",
    ),
    "border": (
        "border-top-width",
        "border-right-width",
        "border-bottom-width",
        "border-left-width",
        "border-top-style",
        "border-right-style",
        "border-bottom-style",
        "border-left-style",
        "border-top-color",
        "border-right-color",
        "border-bottom-color",
        "border-left-color",
    ),
    "outline": ("outline-width", "outline-style", "outline-color"),
    "overflow": ("overflow-x", "overflow-y"),
    "gap": ("row-gap", "column-gap"),
    "place-content": ("align-content", "justify-content"),
    "place-items": ("align-items", "justify-items"),
    "place-self": ("align-self", "justify-self"),
    "flex": ("flex-grow", "flex-shrink", "flex-basis"),
    "flex-flow": ("flex-direction", "flex-wrap"),
    "font": (
        "font-style",
        "font-variant",
        "font-weight",
        "font-stretch",
        "font-size",
        "line-height",
        "font-family",
    ),
    "list-style": (
        "list-style-type",
        "list-style-position",
        "list-style-image",
    ),
    "text-decoration": (
        "text-decoration-line",
        "text-decoration-style",
        "text-decoration-color",
    ),
    "columns": ("column-width", "column-count"),
    "column-rule": (
        "column-rule-width",
        "column-rule-style",
        "column-rule-color",
    ),
    "background": (
        "background-image",
        "background-position",
        "background-size",
        "background-repeat",
        "background-origin",
        "background-clip",
        "background-attachment",
        "background-color",
    ),
    "transition": (
        "transition-property",
        "transition-duration",
        "transition-timing-function",
        "transition-delay",
    ),
    "animation": (
        "animation-duration",
        "animation-timing-function",
        "animation-delay",
        "animation-iteration-count",
        "animation-direction",
        "animation-fill-mode",
        "animation-play-state",
        "animation-name",
    ),
    "grid-template": (
        "grid-template-rows",
        "grid-template-columns",
        "grid-template-areas",
    ),
    "grid": (
        "grid-template-rows",
        "grid-template-columns",
        "grid-template-areas",
        "grid-auto-rows",
        "grid-auto-columns",
        "grid-auto-flow",
    ),
    "grid-column": ("grid-column-start", "grid-column-end"),
    "grid-row": ("grid-row-start", "grid-row-end"),
    "grid-area": (
        "grid-row-start",
        "grid-column-start",
        "grid-row-end",
        "grid-column-end",
    ),
}

# CSS Cascade 4 3.2 ``all``: every property but ``direction``, ``unicode-bidi``
# and custom properties -- here, every longhand this module knows of. Its only
# values are the CSS-wide keywords (``button { all: unset }``).
SHORTHANDS["all"] = tuple(
    sorted(
        (set(INITIAL_VALUES) | set(INHERITED_PROPERTIES) | {long for longs in SHORTHANDS.values() for long in longs})
        - set(SHORTHANDS)
        - {"all", "direction", "unicode-bidi"}
    )
)

#: longhand property -> the shorthand(s) that include it
LONGHAND_TO_SHORTHANDS: dict[str, tuple[str, ...]] = {}
for _short, _longs in SHORTHANDS.items():
    for _long in _longs:
        LONGHAND_TO_SHORTHANDS.setdefault(_long, ())
        LONGHAND_TO_SHORTHANDS[_long] += (_short,)

#: box shorthands whose longhands follow the top/right/bottom/left 1-4 value rule
BOX_SHORTHANDS: frozenset[str] = frozenset(
    {"margin", "padding", "inset", "border-width", "border-style", "border-color"}
)
#: radius shorthand uses TL/TR/BR/BL order but the same 1-4 value collapsing
RADIUS_SHORTHANDS: frozenset[str] = frozenset({"border-radius"})

# ``flex-flow`` is unusual among the two-longhand shorthands below: either
# component may be omitted, and its direction/wrap keywords occupy disjoint
# value spaces.  A lone value therefore cannot simply be copied to both
# longhands as it can for ``overflow`` or ``gap``.
_FLEX_DIRECTION_KEYWORDS: frozenset[str] = frozenset(
    {"row", "row-reverse", "column", "column-reverse"}
)
_FLEX_WRAP_KEYWORDS: frozenset[str] = frozenset({"nowrap", "wrap", "wrap-reverse"})


def is_shorthand(name: str) -> bool:
    return name in SHORTHANDS


def longhands_for(name: str) -> tuple[str, ...]:
    return SHORTHANDS.get(name, ())


# CSS Properties and Values API (@property / CSS.registerProperty) registrations,
# keyed by custom-property name. Each value is
# {"syntax": str, "inherits": bool, "initialValue": str | None}.
REGISTERED_PROPERTIES: dict[str, dict] = {}


def register_property(
    name: str,
    *,
    syntax: str = "*",
    inherits: bool = False,
    initial_value: str | None = None,
) -> None:
    """Record a registered custom property (last registration wins, matching
    ``@property`` cascade order; ``CSS.registerProperty`` enforces uniqueness
    itself)."""
    REGISTERED_PROPERTIES[name] = {
        "syntax": syntax,
        "inherits": bool(inherits),
        "initialValue": initial_value,
    }


def registered_property(name: str) -> dict | None:
    return REGISTERED_PROPERTIES.get(name)


def inherits(name: str) -> bool:
    registration = REGISTERED_PROPERTIES.get(name)
    if registration is not None:
        return registration["inherits"]
    # An unregistered custom property inherits by default.
    return name in INHERITED_PROPERTIES or name.startswith("--")


def initial_value(name: str) -> str:
    registration = REGISTERED_PROPERTIES.get(name)
    if registration is not None and registration["initialValue"] is not None:
        return registration["initialValue"]
    return INITIAL_VALUES.get(name, "")


def expand_box_values(value: str) -> tuple[str, str, str, str]:
    """Expand a 1-4 token box value into (top, right, bottom, left)."""
    parts = _tokens(value)
    if len(parts) == 1:
        return parts[0], parts[0], parts[0], parts[0]
    if len(parts) == 2:
        return parts[0], parts[1], parts[0], parts[1]
    if len(parts) == 3:
        return parts[0], parts[1], parts[2], parts[1]
    return parts[0], parts[1], parts[2], parts[3]


def collapse_box_values(top: str, right: str, bottom: str, left: str) -> str:
    """Collapse (top, right, bottom, left) back to the shortest equivalent."""
    if not all((top, right, bottom, left)):
        return ""
    if left == right:
        if top == bottom:
            return top if top == right else f"{top} {right}"
        return f"{top} {right} {bottom}"
    return f"{top} {right} {bottom} {left}"


_BORDER_STYLE_KEYWORDS = frozenset(
    {
        "none",
        "hidden",
        "dotted",
        "dashed",
        "solid",
        "double",
        "groove",
        "ridge",
        "inset",
        "outset",
    }
)
_BORDER_WIDTH_KEYWORDS = frozenset({"thin", "medium", "thick"})
_FONT_STYLE_KEYWORDS = frozenset({"italic", "oblique"})
_FONT_VARIANT_KEYWORDS = frozenset({"small-caps"})
_FONT_WEIGHT_KEYWORDS = frozenset(
    {"bold", "bolder", "lighter", "100", "200", "300", "400", "500", "600", "700", "800", "900"}
)
_FONT_STRETCH_KEYWORDS = frozenset(
    {
        "ultra-condensed",
        "extra-condensed",
        "condensed",
        "semi-condensed",
        "semi-expanded",
        "expanded",
        "extra-expanded",
        "ultra-expanded",
    }
)
_GLOBAL_KEYWORDS = frozenset({"inherit", "initial", "unset", "revert", "revert-layer"})
#: CSS Fonts 4 system font keywords -> the size Blink gives them (its default
#: UI font, Arial, at the platform's system size)
_SYSTEM_FONTS = {
    "caption": "13px",
    "icon": "13px",
    "menu": "13px",
    "message-box": "13px",
    "small-caption": "11px",
    "status-bar": "13px",
}


_NUMBER_RE = re.compile(r"^[+-]?(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?$", re.I)


def _is_font_weight_number(token: str) -> bool:
    """A ``<number>`` font weight, 1 to 1000 (CSS Fonts 4 2.2) -- before a
    ``font`` shorthand's size, a bare number is the weight."""
    try:
        number = float(token)
    except ValueError:
        return False
    return 1 <= number <= 1000


def _has_top_level_comma(value: str) -> bool:
    depth = 0
    for char in value:
        if char == "(":
            depth += 1
        elif char == ")":
            depth = max(depth - 1, 0)
        elif char == "," and depth == 0:
            return True
    return False


def _split_ws_keep_funcs(value: str) -> list[str]:
    """Split on whitespace, but keep ``func(...)`` groups intact and emit a
    bare ``/`` as its own token."""
    tokens: list[str] = []
    buf: list[str] = []
    depth = 0
    for char in value.strip():
        if char == "(":
            depth += 1
            buf.append(char)
        elif char == ")":
            depth = max(depth - 1, 0)
            buf.append(char)
        elif depth == 0 and char.isspace():
            if buf:
                tokens.append("".join(buf))
                buf = []
        elif depth == 0 and char == "/":
            if buf:
                tokens.append("".join(buf))
                buf = []
            tokens.append("/")
        else:
            buf.append(char)
    if buf:
        tokens.append("".join(buf))
    return tokens


def _tokens(value: str) -> list[str]:
    """``value`` split on top-level whitespace: a function call
    (``rgba(0, 0, 0, .5)``, ``calc(50% - 10px)``) or a quoted string stays one
    token."""
    tokens: list[str] = []
    buf: list[str] = []
    depth = 0
    quote = None
    for char in value.strip():
        if quote is not None:
            buf.append(char)
            if char == quote:
                quote = None
        elif char in "\"'":
            quote = char
            buf.append(char)
        elif char == "(":
            depth += 1
            buf.append(char)
        elif char == ")":
            depth = max(depth - 1, 0)
            buf.append(char)
        elif depth == 0 and char.isspace():
            if buf:
                tokens.append("".join(buf))
                buf = []
        else:
            buf.append(char)
    if buf:
        tokens.append("".join(buf))
    return tokens


_MATH_FUNCTION_PREFIXES = ("calc(", "min(", "max(", "clamp(", "-webkit-calc(")


def _looks_like_length(token: str) -> bool:
    token = token.strip().lower()
    if token in _BORDER_WIDTH_KEYWORDS:
        return True
    if token.startswith(_MATH_FUNCTION_PREFIXES):
        return True  # (a math function in a length slot reads as a length)
    return (
        bool(token)
        and (token[0].isdigit() or token[0] in "+-.")
        and (
            token.endswith(
                (
                    "px",
                    "em",
                    "rem",
                    "%",
                    "vh",
                    "vw",
                    "vmin",
                    "vmax",
                    "pt",
                    "pc",
                    "ex",
                    "ch",
                    "cm",
                    "mm",
                    "in",
                    "q",
                    "fr",
                    "0",
                    "1",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "7",
                    "8",
                    "9",
                )
            )
        )
    )


def _split_top_level(text: str, separator: str) -> list[str]:
    """``text`` split at ``separator`` outside parens, brackets and strings."""
    parts: list[str] = []
    current: list[str] = []
    depth = 0
    quote = None
    for char in text:
        if quote is not None:
            current.append(char)
            if char == quote:
                quote = None
            continue
        if char in "\"'":
            quote = char
        elif char in "([":
            depth += 1
        elif char in ")]":
            depth -= 1
        elif char == separator and depth == 0:
            parts.append("".join(current).strip())
            current = []
            continue
        current.append(char)
    parts.append("".join(current).strip())
    return parts


_GRID_IDENT_RE = re.compile(r"^-?[A-Za-z_][\w-]*$")


def _is_grid_ident(token: str) -> bool:
    """A ``<custom-ident>`` grid line name (not ``auto``/``span``/a CSS-wide keyword)."""
    return bool(_GRID_IDENT_RE.match(token)) and token.lower() not in ("auto", "span") and (
        token.lower() not in _GLOBAL_KEYWORDS
    )


_GRID_TEMPLATE_TOKEN_RE = re.compile(r"\"[^\"]*\"|'[^']*'|\[[^\]]*\]|[^\s\"'\[(]+(?:\((?:[^()]|\([^()]*\))*\))?")


def _expand_grid_template(value: str) -> list[tuple[str, str]] | None:
    """CSS Grid 1 7.4 ``grid-template``: ``none``, ``<rows> / <columns>``, or
    rows written as area strings -- each with optional line names and a track
    size -- then an optional ``/ <columns>``."""
    text = value.strip()
    if text.lower() == "none":
        return [("grid-template-rows", "none"), ("grid-template-columns", "none"), ("grid-template-areas", "none")]
    parts = _split_top_level(text, "/")
    if len(parts) > 2 or not all(parts):
        return None
    if '"' not in parts[0] and "'" not in parts[0]:
        if len(parts) != 2:
            return None
        return [("grid-template-rows", parts[0]), ("grid-template-columns", parts[1]), ("grid-template-areas", "none")]
    # [ <line-names>? <string> <track-size>? <line-names>? ]+
    strings: list[str] = []
    tracks: list[str] = []
    pending_size = False
    for token in _GRID_TEMPLATE_TOKEN_RE.findall(parts[0]):
        if token[0] in "\"'":
            if pending_size:
                tracks.append("auto")
            strings.append('"' + token[1:-1] + '"')
            pending_size = True
        elif token.startswith("["):
            tracks.append(token)
        elif pending_size:
            tracks.append(token)
            pending_size = False
        else:
            return None  # a track size not after a string
    if pending_size:
        tracks.append("auto")
    return [
        ("grid-template-rows", " ".join(tracks)),
        ("grid-template-columns", parts[1] if len(parts) == 2 else "none"),
        ("grid-template-areas", " ".join(strings)),
    ]


def _expand_grid(value: str) -> list[tuple[str, str]] | None:
    """CSS Grid 1 7.8 ``grid``: a ``grid-template``, or one axis as
    ``auto-flow [dense]`` (with the implicit track size) and the other's
    explicit tracks; every omitted sub-property is reset."""
    parts = _split_top_level(value.strip(), "/")
    if len(parts) == 2 and any("auto-flow" in part.split() for part in parts):
        row_flow = "auto-flow" in parts[0].split()
        words = (parts[0] if row_flow else parts[1]).split()
        dense = "dense" in words
        size = " ".join(word for word in words if word not in ("auto-flow", "dense")) or "auto"
        flow = ("row" if row_flow else "column") + (" dense" if dense else "")
        return [
            ("grid-template-rows", "none" if row_flow else parts[0]),
            ("grid-template-columns", parts[1] if row_flow else "none"),
            ("grid-template-areas", "none"),
            ("grid-auto-rows", size if row_flow else "auto"),
            ("grid-auto-columns", "auto" if row_flow else size),
            ("grid-auto-flow", flow),
        ]
    template = _expand_grid_template(value)
    if template is None:
        return None
    return template + [("grid-auto-rows", "auto"), ("grid-auto-columns", "auto"), ("grid-auto-flow", "row")]


_BACKGROUND_REPEAT_KEYWORDS = frozenset({"repeat", "no-repeat", "repeat-x", "repeat-y", "space", "round"})
_BACKGROUND_ATTACHMENT_KEYWORDS = frozenset({"fixed", "local", "scroll"})
_BACKGROUND_BOX_KEYWORDS = frozenset({"border-box", "padding-box", "content-box", "text"})
_POSITION_KEYWORDS = frozenset({"left", "right", "top", "bottom", "center"})
_IMAGE_FUNCTIONS = ("url(", "image(", "image-set(", "-webkit-image-set(", "cross-fade(", "element(", "paint(")


def _is_position_part(token: str) -> bool:
    return token.lower() in _POSITION_KEYWORDS or _looks_like_length(token)


def _expand_background_layer(layer: str, final: bool) -> list[tuple[str, str]] | None:
    """One ``background`` layer: ``<image> || <position> [ / <size> ]? ||
    <repeat> || <attachment> || <box> || <box>``, plus ``<color>`` in the
    final layer. None if it doesn't parse."""
    tokens = _split_ws_keep_funcs(layer)
    image = position = size = attachment = origin = clip = color = None
    repeat: list[str] = []
    index = 0
    while index < len(tokens):
        token = tokens[index]
        low = token.lower()
        if _is_position_part(token):
            if position is not None:
                return None
            parts = [token]
            index += 1
            while index < len(tokens) and len(parts) < 4 and _is_position_part(tokens[index]):
                parts.append(tokens[index])
                index += 1
            position = " ".join(parts)
            if index < len(tokens) and tokens[index] == "/":
                index += 1
                sizes: list[str] = []
                if index < len(tokens) and tokens[index].lower() in ("cover", "contain"):
                    sizes.append(tokens[index].lower())
                    index += 1
                else:
                    while index < len(tokens) and len(sizes) < 2 and (
                        tokens[index].lower() == "auto" or _looks_like_length(tokens[index])
                    ):
                        sizes.append(tokens[index])
                        index += 1
                if not sizes:
                    return None
                size = " ".join(sizes)
            continue
        if token == "/":
            return None  # a size only follows a position
        if low in _BACKGROUND_REPEAT_KEYWORDS:
            if len(repeat) >= 2:
                return None
            repeat.append(token)
        elif low in _BACKGROUND_ATTACHMENT_KEYWORDS:
            attachment = token
        elif low in _BACKGROUND_BOX_KEYWORDS:
            if origin is None:
                origin = token
            elif clip is None:
                clip = token
            else:
                return None
        elif low == "none" or low.startswith(_IMAGE_FUNCTIONS) or "gradient(" in low:
            if image is not None:
                return None
            image = token
        else:
            if color is not None or not final:
                return None
            color = token
        index += 1
    pairs = [
        ("background-image", image or "none"),
        ("background-position", position or "0% 0%"),
        ("background-size", size or "auto"),
        ("background-repeat", " ".join(repeat) or "repeat"),
        ("background-origin", origin or "padding-box"),
        ("background-clip", clip or origin or "border-box"),
        ("background-attachment", attachment or "scroll"),
    ]
    return pairs + [("background-color", color or "transparent")]


def expand_shorthand(name: str, value: str) -> list[tuple[str, str]] | None:
    """Expand ``name: value`` (a shorthand) into ``[(longhand, value), ...]``.

    Returns ``None`` if the shorthand is not understood well enough to split
    (the caller then keeps only the shorthand entry).
    """
    value = value.strip()
    longs = SHORTHANDS.get(name)
    if not longs or not value:
        return None
    lower = value.lower()
    if lower in _GLOBAL_KEYWORDS:
        return [(long, value) for long in longs]

    if name in RADIUS_SHORTHANDS and "/" in value:
        # elliptical: <horizontal radii>{1,4} / <vertical radii>{1,4}, each
        # corner "<h> <v>" (CSS Backgrounds 3 5.1)
        halves = _split_top_level(value, "/")
        if len(halves) != 2 or not all(halves) or any(len(_tokens(half)) > 4 for half in halves):
            return None
        horizontal, vertical = expand_box_values(halves[0]), expand_box_values(halves[1])
        return [(long, h if h == v else f"{h} {v}") for long, h, v in zip(longs, horizontal, vertical)]

    if name in BOX_SHORTHANDS or name in RADIUS_SHORTHANDS:
        if len(_tokens(value)) > 4:
            return None
        top, right, bottom, left = expand_box_values(value)
        return list(zip(longs, (top, right, bottom, left)))

    if name in ("border", "border-top", "border-right", "border-bottom", "border-left", "outline", "column-rule"):
        width = style = color = None
        for token in _tokens(value):
            tl = token.lower()
            if tl in _BORDER_STYLE_KEYWORDS and style is None:
                style = token
            elif (_looks_like_length(token) or tl in _BORDER_WIDTH_KEYWORDS) and width is None:
                width = token
            else:
                color = token if color is None else f"{color} {token}"
        prefix = "border" if name == "border" else name
        if name == "border":
            # grouped by component then side, matching SHORTHANDS["border"] and
            # a browser's declaration-block enumeration order
            return [
                (f"border-{side}-{comp}", val)
                for comp, val in (
                    ("width", width or "medium"),
                    ("style", style or "none"),
                    ("color", color or "currentcolor"),
                )
                for side in ("top", "right", "bottom", "left")
            ]
        return [
            (f"{prefix}-width", width or "medium"),
            (f"{prefix}-style", style or "none"),
            (f"{prefix}-color", color or "currentcolor"),
        ]

    if name == "flex":
        if lower == "none":
            return [("flex-grow", "0"), ("flex-shrink", "0"), ("flex-basis", "auto")]
        if lower == "auto":
            return [("flex-grow", "1"), ("flex-shrink", "1"), ("flex-basis", "auto")]
        # [ <flex-grow> <flex-shrink>? || <flex-basis> ] (CSS Flexbox 1 7.2): an
        # omitted basis is 0%; a unitless zero after both factors is the
        # basis (0px), any other unitless third number is invalid
        parts = _tokens(value)
        grow = shrink = basis = None
        index = 0
        while index < len(parts):
            part = parts[index]
            if _NUMBER_RE.match(part):
                if grow is not None:
                    return None
                grow = part
                if index + 1 < len(parts) and _NUMBER_RE.match(parts[index + 1]):
                    index += 1
                    shrink = parts[index]
                    if index + 1 < len(parts) and _NUMBER_RE.match(parts[index + 1]):
                        index += 1
                        if float(parts[index]) != 0 or basis is not None:
                            return None
                        basis = "0px"
            elif basis is not None:
                return None
            else:
                basis = part
            index += 1
        if grow is None and basis is None:
            return None
        return [("flex-grow", grow or "1"), ("flex-shrink", shrink or "1"), ("flex-basis", basis or "0%")]

    if name in ("grid-column", "grid-row"):
        # <grid-line> [ / <grid-line> ]? -- the slash, not whitespace, is the
        # separator (each <grid-line> can itself contain a space: "span 3").
        parts = [p.strip() for p in _split_top_level(value, "/")]
        if len(parts) == 1:
            # no end line: a lone <custom-ident> sets the end too, else auto
            # (CSS Grid 1 8.4)
            return [(longs[0], parts[0]), (longs[1], parts[0] if _is_grid_ident(parts[0]) else "auto")]
        if len(parts) == 2 and all(parts):
            return list(zip(longs, parts))
        return None

    if name == "grid-area":
        # <grid-line> [ / <grid-line> ]{0,3}: an omitted column-start copies
        # the row-start if that is a <custom-ident>, an omitted row-end the
        # row-start, column-end the column-start; else auto (CSS Grid 1 8.4)
        parts = [p.strip() for p in _split_top_level(value, "/")]
        if len(parts) > 4 or not all(parts):
            return None
        while len(parts) < 4:
            source = parts[len(parts) - 2] if len(parts) >= 2 else parts[0]
            parts.append(source if _is_grid_ident(source) else "auto")
        return list(zip(longs, (parts[0], parts[1], parts[2], parts[3])))

    if name == "grid-template":
        return _expand_grid_template(value)

    if name == "grid":
        return _expand_grid(value)

    if name == "flex-flow":
        parts = _tokens(value)
        if len(parts) == 1:
            token = parts[0]
            token_lower = token.lower()
            if token_lower in _FLEX_DIRECTION_KEYWORDS:
                return [("flex-direction", token), ("flex-wrap", "nowrap")]
            if token_lower in _FLEX_WRAP_KEYWORDS:
                return [("flex-direction", "row"), ("flex-wrap", token)]

    if name == "columns":
        # <'column-width'> || <'column-count'>, either order: an integer is the
        # count (Multi-column 1 3.4)
        parts = _tokens(value)
        if not 1 <= len(parts) <= 2:
            return None
        width = count = None
        for part in parts:
            if re.fullmatch(r"[+-]?\d+", part):
                if count is not None:
                    return None
                count = part
            elif part.lower() == "auto":
                continue
            elif width is None:
                width = part
            else:
                return None
        return [("column-width", width or "auto"), ("column-count", count or "auto")]

    if name in ("place-content", "place-items", "place-self"):
        # <align value> <justify value>?, each one or two words (``safe center``,
        # ``first baseline``); an omitted second copies the first -- bar a
        # baseline place-content, whose justify-content is then ``start``
        words = _tokens(value)
        values: list[str] = []
        index = 0
        while index < len(words):
            word = words[index].lower()
            take = 2 if (word in ("safe", "unsafe") or (word in ("first", "last") and index + 1 < len(words))) else 1
            if name == "place-items" and word == "legacy" and index + 1 < len(words):
                take = 2
            values.append(" ".join(words[index : index + take]))
            index += take
        if not 1 <= len(values) <= 2:
            return None
        if len(values) == 1:
            second = values[0]
            if name == "place-content" and values[0].endswith("baseline"):
                second = "start"
            values.append(second)
        return list(zip(longs, values))

    if name in (
        "overflow",
        "gap",
        "flex-flow",
    ):
        parts = _tokens(value)
        if len(parts) == 1:
            return [(long, parts[0]) for long in longs]
        if len(parts) == len(longs):
            return list(zip(longs, parts))
        return None

    if name == "list-style":
        # <position> || <image> || <type>; a ``none`` sets whichever of image
        # and type is otherwise unset (both, alone) -- CSS Lists 3 3.6
        type_ = position = image = None
        nones = 0
        for token in _tokens(value):
            tl = token.lower()
            if tl in ("inside", "outside"):
                position = token
            elif tl == "none":
                nones += 1
            elif "(" in tl and not tl.startswith("symbols("):
                image = token
            else:
                type_ = token
        if nones:
            if image is None:
                image = "none"
                nones -= 1
            if type_ is None and (nones or image == "none"):
                type_ = "none"
        return [
            ("list-style-type", type_ or "disc"),
            ("list-style-position", position or "outside"),
            ("list-style-image", image or "none"),
        ]

    if name == "text-decoration":
        line = style = color = None
        line_kw = {"none", "underline", "overline", "line-through", "blink"}
        style_kw = {"solid", "double", "dotted", "dashed", "wavy"}
        for token in _tokens(value):
            tl = token.lower()
            if tl in line_kw:
                line = f"{line} {token}".strip() if line else token
            elif tl in style_kw:
                style = token
            else:
                color = token
        return [
            ("text-decoration-line", line or "none"),
            ("text-decoration-style", style or "solid"),
            ("text-decoration-color", color or "currentcolor"),
        ]

    if name == "font":
        system = _SYSTEM_FONTS.get(lower)
        if system is not None:
            # a system font keyword sets every longhand (CSS Fonts 4 2.8), to
            # what Blink resolves them to: its default UI font at system size
            return [
                ("font-style", "normal"),
                ("font-variant", "normal"),
                ("font-weight", "normal"),
                ("font-stretch", "normal"),
                ("font-size", system),
                ("line-height", "normal"),
                ("font-family", "Arial"),
            ]
        # [ style || variant || weight || stretch ]? size [ / line-height ]? family
        # (``/`` is its own token, spaced or not: ``1rem / 1.5``)
        tokens = _split_ws_keep_funcs(value)
        style = variant = weight = stretch = "normal"
        size = line_height = ""
        index = 0
        while index < len(tokens):
            token = tokens[index]
            tl = token.lower()
            if tl in _FONT_STYLE_KEYWORDS:
                style = token
            elif tl in _FONT_VARIANT_KEYWORDS:
                variant = token
            elif tl in _FONT_WEIGHT_KEYWORDS or _is_font_weight_number(tl):
                weight = token
            elif tl in _FONT_STRETCH_KEYWORDS:
                stretch = token
            elif tl != "normal":
                # the first other token is the size, then an optional / line-height
                size = token
                index += 1
                if index < len(tokens) and tokens[index] == "/":
                    line_height = tokens[index + 1] if index + 1 < len(tokens) else ""
                    index += 2
                break
            index += 1
        family = " ".join(tokens[index:]) or "inherit"
        return [
            ("font-style", style),
            ("font-variant", variant),
            ("font-weight", weight),
            ("font-stretch", stretch),
            ("font-size", size or "medium"),
            ("line-height", line_height or "normal"),
            ("font-family", family),
        ]

    if name == "background":
        # layers separated by top-level commas; only the final one may carry
        # the colour (CSS Backgrounds 3 3.10)
        layers = _split_top_level(value, ",")
        expanded = []
        for index, layer in enumerate(layers):
            pairs = _expand_background_layer(layer, final=index == len(layers) - 1) if layer else None
            if pairs is None:
                return None
            expanded.append(dict(pairs))
        if len(expanded) == 1:
            return list(expanded[0].items())
        return [
            (long, expanded[-1][long] if long == "background-color" else ", ".join(layer[long] for layer in expanded))
            for long in longs
        ]

    # transition / animation / grid-template / grid-area:
    # keep them as the shorthand only (round-trips correctly, just not split).
    return None


def build_shorthand(name: str, get: Callable[[str], str]) -> str:
    """Reconstruct a shorthand string from longhand values via ``get(longhand)``.

    Returns "" if the shorthand cannot be losslessly built (a longhand missing,
    or the components disagree in a way that has no shorthand form).
    """
    longs = SHORTHANDS.get(name)
    if not longs:
        return ""

    if name in RADIUS_SHORTHANDS:
        corners = [_tokens(get(long)) for long in longs]
        if any(not corner or len(corner) > 2 for corner in corners):
            return ""
        horizontal = [corner[0] for corner in corners]
        vertical = [corner[-1] for corner in corners]
        built = collapse_box_values(*horizontal)
        return built if horizontal == vertical else f"{built} / {collapse_box_values(*vertical)}"

    if name in BOX_SHORTHANDS:
        vals = [get(long) for long in longs]
        if any(v == "" for v in vals):
            return ""
        return collapse_box_values(*vals)

    if name in ("border-top", "border-right", "border-bottom", "border-left", "outline", "column-rule"):
        # longs is (<x>-width, <x>-style, <x>-color) for this exact shorthand
        parts = [get(long) for long in longs]
        if any(p == "" for p in parts):
            return ""
        return " ".join(p for p in parts if p and p not in ("currentcolor", "medium")) or parts[1]

    if name == "border":
        # only if all four sides are identical
        sides = ("top", "right", "bottom", "left")
        for comp in ("width", "style", "color"):
            side_vals = {get(f"border-{s}-{comp}") for s in sides}
            if len(side_vals) != 1 or "" in side_vals:
                return ""
        w = get("border-top-width")
        s = get("border-top-style")
        c = get("border-top-color")
        return " ".join(x for x in (w, s, c) if x and x not in ("medium", "currentcolor")) or s

    if name in ("grid-column", "grid-row"):
        start, end = (get(long) for long in longs)
        if start == "" or end == "":
            return ""
        if end == "auto":
            return start
        return f"{start} / {end}"

    if name in (
        "overflow",
        "gap",
        "flex-flow",
        "place-content",
        "place-items",
        "place-self",
        "columns",
    ):
        vals = [get(long) for long in longs]
        if any(v == "" for v in vals):
            return ""
        if len(set(vals)) == 1:
            return vals[0]
        return " ".join(vals)

    if name == "flex":
        g, s, b = (get("flex-grow"), get("flex-shrink"), get("flex-basis"))
        if "" in (g, s, b):
            return ""
        return " ".join((g, s, b))

    if name in ("list-style", "text-decoration"):
        vals = [get(long) for long in longs]
        vals = [v for v in vals if v and v not in ("disc", "outside", "none", "solid", "currentcolor")]
        joined = " ".join(get(long) for long in longs if get(long))
        return joined.strip()

    if name == "font":
        size = get("font-size")
        family = get("font-family")
        if not size or not family:
            return ""
        lh = get("line-height")
        pieces = []
        for comp in ("font-style", "font-variant", "font-weight", "font-stretch"):
            v = get(comp)
            if v and v != "normal":
                pieces.append(v)
        size_part = f"{size}/{lh}" if lh and lh != "normal" else size
        pieces.append(size_part)
        pieces.append(family)
        return " ".join(pieces)

    return ""


# --- colour normalisation ----------------------------------------------------
# The 148 CSS named colours -> (r, g, b). Used by ``window.getComputedStyle`` to
# report a used colour as ``rgb()`` / ``rgba()`` the way a browser does.
NAMED_COLORS: dict[str, tuple[int, int, int]] = {
    "aliceblue": (240, 248, 255),
    "antiquewhite": (250, 235, 215),
    "aqua": (0, 255, 255),
    "aquamarine": (127, 255, 212),
    "azure": (240, 255, 255),
    "beige": (245, 245, 220),
    "bisque": (255, 228, 196),
    "black": (0, 0, 0),
    "blanchedalmond": (255, 235, 205),
    "blue": (0, 0, 255),
    "blueviolet": (138, 43, 226),
    "brown": (165, 42, 42),
    "burlywood": (222, 184, 135),
    "cadetblue": (95, 158, 160),
    "chartreuse": (127, 255, 0),
    "chocolate": (210, 105, 30),
    "coral": (255, 127, 80),
    "cornflowerblue": (100, 149, 237),
    "cornsilk": (255, 248, 220),
    "crimson": (220, 20, 60),
    "cyan": (0, 255, 255),
    "darkblue": (0, 0, 139),
    "darkcyan": (0, 139, 139),
    "darkgoldenrod": (184, 134, 11),
    "darkgray": (169, 169, 169),
    "darkgreen": (0, 100, 0),
    "darkgrey": (169, 169, 169),
    "darkkhaki": (189, 183, 107),
    "darkmagenta": (139, 0, 139),
    "darkolivegreen": (85, 107, 47),
    "darkorange": (255, 140, 0),
    "darkorchid": (153, 50, 204),
    "darkred": (139, 0, 0),
    "darksalmon": (233, 150, 122),
    "darkseagreen": (143, 188, 143),
    "darkslateblue": (72, 61, 139),
    "darkslategray": (47, 79, 79),
    "darkslategrey": (47, 79, 79),
    "darkturquoise": (0, 206, 209),
    "darkviolet": (148, 0, 211),
    "deeppink": (255, 20, 147),
    "deepskyblue": (0, 191, 255),
    "dimgray": (105, 105, 105),
    "dimgrey": (105, 105, 105),
    "dodgerblue": (30, 144, 255),
    "firebrick": (178, 34, 34),
    "floralwhite": (255, 250, 240),
    "forestgreen": (34, 139, 34),
    "fuchsia": (255, 0, 255),
    "gainsboro": (220, 220, 220),
    "ghostwhite": (248, 248, 255),
    "gold": (255, 215, 0),
    "goldenrod": (218, 165, 32),
    "gray": (128, 128, 128),
    "green": (0, 128, 0),
    "greenyellow": (173, 255, 47),
    "grey": (128, 128, 128),
    "honeydew": (240, 255, 240),
    "hotpink": (255, 105, 180),
    "indianred": (205, 92, 92),
    "indigo": (75, 0, 130),
    "ivory": (255, 255, 240),
    "khaki": (240, 230, 140),
    "lavender": (230, 230, 250),
    "lavenderblush": (255, 240, 245),
    "lawngreen": (124, 252, 0),
    "lemonchiffon": (255, 250, 205),
    "lightblue": (173, 216, 230),
    "lightcoral": (240, 128, 128),
    "lightcyan": (224, 255, 255),
    "lightgoldenrodyellow": (250, 250, 210),
    "lightgray": (211, 211, 211),
    "lightgreen": (144, 238, 144),
    "lightgrey": (211, 211, 211),
    "lightpink": (255, 182, 193),
    "lightsalmon": (255, 160, 122),
    "lightseagreen": (32, 178, 170),
    "lightskyblue": (135, 206, 250),
    "lightslategray": (119, 136, 153),
    "lightslategrey": (119, 136, 153),
    "lightsteelblue": (176, 196, 222),
    "lightyellow": (255, 255, 224),
    "lime": (0, 255, 0),
    "limegreen": (50, 205, 50),
    "linen": (250, 240, 230),
    "magenta": (255, 0, 255),
    "maroon": (128, 0, 0),
    "mediumaquamarine": (102, 205, 170),
    "mediumblue": (0, 0, 205),
    "mediumorchid": (186, 85, 211),
    "mediumpurple": (147, 112, 219),
    "mediumseagreen": (60, 179, 113),
    "mediumslateblue": (123, 104, 238),
    "mediumspringgreen": (0, 250, 154),
    "mediumturquoise": (72, 209, 204),
    "mediumvioletred": (199, 21, 133),
    "midnightblue": (25, 25, 112),
    "mintcream": (245, 255, 250),
    "mistyrose": (255, 228, 225),
    "moccasin": (255, 228, 181),
    "navajowhite": (255, 222, 173),
    "navy": (0, 0, 128),
    "oldlace": (253, 245, 230),
    "olive": (128, 128, 0),
    "olivedrab": (107, 142, 35),
    "orange": (255, 165, 0),
    "orangered": (255, 69, 0),
    "orchid": (218, 112, 214),
    "palegoldenrod": (238, 232, 170),
    "palegreen": (152, 251, 152),
    "paleturquoise": (175, 238, 238),
    "palevioletred": (219, 112, 147),
    "papayawhip": (255, 239, 213),
    "peachpuff": (255, 218, 185),
    "peru": (205, 133, 63),
    "pink": (255, 192, 203),
    "plum": (221, 160, 221),
    "powderblue": (176, 224, 230),
    "purple": (128, 0, 128),
    "rebeccapurple": (102, 51, 153),
    "red": (255, 0, 0),
    "rosybrown": (188, 143, 143),
    "royalblue": (65, 105, 225),
    "saddlebrown": (139, 69, 19),
    "salmon": (250, 128, 114),
    "sandybrown": (244, 164, 96),
    "seagreen": (46, 139, 87),
    "seashell": (255, 245, 238),
    "sienna": (160, 82, 45),
    "silver": (192, 192, 192),
    "skyblue": (135, 206, 235),
    "slateblue": (106, 90, 205),
    "slategray": (112, 128, 144),
    "slategrey": (112, 128, 144),
    "snow": (255, 250, 250),
    "springgreen": (0, 255, 127),
    "steelblue": (70, 130, 180),
    "tan": (210, 180, 140),
    "teal": (0, 128, 128),
    "thistle": (216, 191, 216),
    "tomato": (255, 99, 71),
    "turquoise": (64, 224, 208),
    "violet": (238, 130, 238),
    "wheat": (245, 222, 179),
    "white": (255, 255, 255),
    "whitesmoke": (245, 245, 245),
    "yellow": (255, 255, 0),
    "yellowgreen": (154, 205, 50),
}

import re as _re  # noqa: E402

_HEX_RE = _re.compile(r"^#([0-9a-fA-F]{3,8})$")


def _hsl_to_rgb(h: float, s: float, ll: float) -> tuple[int, int, int]:
    h = (h % 360) / 360.0
    s = max(0.0, min(1.0, s))
    ll = max(0.0, min(1.0, ll))
    if s == 0:
        v = round(ll * 255)
        return (v, v, v)
    q = ll * (1 + s) if ll < 0.5 else ll + s - ll * s
    p = 2 * ll - q

    def hue(t: float) -> float:
        if t < 0:
            t += 1
        if t > 1:
            t -= 1
        if t < 1 / 6:
            return p + (q - p) * 6 * t
        if t < 1 / 2:
            return q
        if t < 2 / 3:
            return p + (q - p) * (2 / 3 - t) * 6
        return p

    return (
        round(hue(h + 1 / 3) * 255),
        round(hue(h) * 255),
        round(hue(h - 1 / 3) * 255),
    )


def _fmt_rgb(r: int, g: int, b: int, a: float | None) -> str:
    r, g, b = (max(0, min(255, int(round(c)))) for c in (r, g, b))
    if a is None or a >= 1:
        return f"rgb({r}, {g}, {b})"
    a = max(0.0, min(1.0, a))
    text = f"{round(a, 3):.3f}".rstrip("0").rstrip(".") or "0"
    return f"rgba({r}, {g}, {b}, {text})"


def normalize_color(value: str) -> str | None:
    """Return ``value`` as ``rgb()`` / ``rgba()``, or ``None`` if it is not a
    colour this resolver understands (leave it untouched)."""
    text = str(value).strip()
    low = text.lower()
    if low in ("", "currentcolor", "transparent"):
        return "rgba(0, 0, 0, 0)" if low == "transparent" else None
    if low in NAMED_COLORS:
        return _fmt_rgb(*NAMED_COLORS[low], None)

    hexmatch = _HEX_RE.match(text)
    if hexmatch:
        digits = hexmatch.group(1)
        if len(digits) in (3, 4):
            digits = "".join(c * 2 for c in digits)
        if len(digits) in (6, 8):
            r, g, b = (int(digits[i : i + 2], 16) for i in (0, 2, 4))
            a = int(digits[6:8], 16) / 255 if len(digits) == 8 else None
            return _fmt_rgb(r, g, b, a)
        return None

    func = _re.match(r"^(rgba?|hsla?)\(([^)]*)\)$", low)
    if not func:
        return None
    kind = func.group(1)
    parts = [p.strip() for p in _re.split(r"[,/]| (?=[^,])", func.group(2)) if p.strip()]
    if len(parts) < 3:
        return None

    def num(tok: str, scale: float = 1.0) -> float:
        tok = tok.strip()
        if tok.endswith("%"):
            return float(tok[:-1]) / 100.0 * scale
        return float(tok)

    try:
        alpha = num(parts[3]) if len(parts) >= 4 else None
        if kind.startswith("rgb"):
            channels = [num(parts[i], 255.0) if parts[i].endswith("%") else float(parts[i]) for i in range(3)]
            return _fmt_rgb(
                int(round(channels[0])),
                int(round(channels[1])),
                int(round(channels[2])),
                alpha,
            )
        h = float(_re.sub(r"deg$", "", parts[0]))
        s = num(parts[1])
        ll = num(parts[2])
        return _fmt_rgb(*_hsl_to_rgb(h, s, ll), alpha)
    except (ValueError, IndexError):
        return None


# --- style-resolution cache epochs -----------------------------------------
#
# Three independent, process-wide monotonic counters a cascade/computed-style
# cache uses to tell "have my inputs changed" from "recompute everything".
# They are kept separate because they change at very different rates: DOM
# structure and attributes (including inline ``style``) change constantly
# during ordinary use, while stylesheet rules are usually set up once and
# rarely touched again, and layout geometry only exists at all once a layout
# engine is attached. Folding all three into one counter would mean a single
# ``classList.toggle()`` forces every stylesheet's selectors to be re-parsed
# and re-indexed on the next style read, not just that element's cascade to
# be redone -- this module, ``domonic.dom``, and ``domonic.layout`` all import
# this leaf module, so it is the natural place for a counter all three reach.
_DOM_STYLE_EPOCH: int = 0
_STYLESHEET_EPOCH: int = 0
_LAYOUT_EPOCH: int = 0


def bump_dom_style_epoch() -> None:
    """Call whenever a DOM mutation could change what a selector matches or
    what an element inherits: an attribute (including inline ``style``)
    changing, or the tree shape around any element changing. Invalidates
    every element's cached cascade, but leaves stylesheets' parsed rule
    index alone."""
    global _DOM_STYLE_EPOCH
    _DOM_STYLE_EPOCH += 1


def dom_style_epoch() -> int:
    return _DOM_STYLE_EPOCH


def bump_stylesheet_epoch() -> None:
    """Call whenever a stylesheet's own rules change (``insertRule`` /
    ``deleteRule`` / ``replace`` / ``replaceSync``) -- invalidates every
    document's cached rule index (and, transitively, every cascade, since a
    changed rule can change what any element resolves to)."""
    global _STYLESHEET_EPOCH
    _STYLESHEET_EPOCH += 1


def stylesheet_epoch() -> int:
    return _STYLESHEET_EPOCH


def bump_layout_epoch() -> None:
    """Call whenever a layout engine attaches, replaces, or clears the box it
    computed for an element (``domonic.layout.set_layout_box`` /
    ``clear_layout_box``) -- invalidates every cached computed style, since
    ``width``/``height``/``margin`` etc. resolve differently once real
    geometry is available (see ``ComputedStyleDeclaration._to_used_length``)."""
    global _LAYOUT_EPOCH
    _LAYOUT_EPOCH += 1


def layout_epoch() -> int:
    return _LAYOUT_EPOCH


# --- declaration validity -------------------------------------------------
# A declaration whose value doesn't match its property's grammar is dropped at
# parse time, so an earlier valid one still applies (``white-space: pre-wrap;
# white-space: -o-pre-wrap`` keeps pre-wrap). Only the properties below are
# checked -- keyword-enumerated and number ones, where invalid values turn up
# in real stylesheets -- and anything holding var()/attr()/env() is judged
# only once substituted.

_DISPLAY_OUTSIDE = ("block", "inline")
_DISPLAY_INSIDE = ("flow", "flow-root", "table", "flex", "grid", "ruby", "math")
_DISPLAY_SINGLE = frozenset(
    {
        "none", "contents", "block", "inline", "inline-block", "flow", "flow-root", "list-item",
        "table", "inline-table", "table-row-group", "table-header-group", "table-footer-group",
        "table-row", "table-cell", "table-column-group", "table-column", "table-caption",
        "flex", "inline-flex", "grid", "inline-grid", "ruby", "ruby-text", "math",
        "-webkit-box", "-webkit-inline-box", "-webkit-flex", "-webkit-inline-flex",
    }
)  # fmt: skip
_DISPLAY_LEGACY = {
    ("block", "flow"): "block",
    ("inline", "flow"): "inline",
    ("block", "flow-root"): "flow-root",
    ("inline", "flow-root"): "inline-block",
    ("block", "table"): "table",
    ("inline", "table"): "inline-table",
    ("block", "flex"): "flex",
    ("inline", "flex"): "inline-flex",
    ("block", "grid"): "grid",
    ("inline", "grid"): "inline-grid",
    ("block", "ruby"): "block ruby",
    ("inline", "ruby"): "ruby",
    ("block", "math"): "block math",
    ("inline", "math"): "math",
}


def _display_multi_keyword(keywords: tuple) -> str | None:
    """The computed (legacy) keyword of a valid multi-keyword ``display``
    (CSS Display 3 2), in any order, or None when the combination is invalid."""
    if len(set(keywords)) != len(keywords):
        return None
    outside = [k for k in keywords if k in _DISPLAY_OUTSIDE]
    inside = [k for k in keywords if k in _DISPLAY_INSIDE]
    marker = [k for k in keywords if k == "list-item"]
    if len(outside) > 1 or len(inside) > 1 or len(outside) + len(inside) + len(marker) != len(keywords):
        return None
    inner = inside[0] if inside else "flow"
    outer = outside[0] if outside else ("inline" if inner == "ruby" else "block")
    if marker:
        if inner not in ("flow", "flow-root"):
            return None
        prefix = "" if outer == "block" else "inline "
        return prefix + ("list-item" if inner == "flow" else "flow-root list-item")
    return _DISPLAY_LEGACY[(outer, inner)]


#: every valid multi-keyword ``display`` -> what it computes to
DISPLAY_MULTI_KEYWORDS: dict[str, str] = {}
for _count in (2, 3):
    import itertools as _itertools

    for _keywords in _itertools.permutations(_DISPLAY_OUTSIDE + _DISPLAY_INSIDE + ("list-item",), _count):
        _legacy = _display_multi_keyword(_keywords)
        if _legacy is not None:
            DISPLAY_MULTI_KEYWORDS[" ".join(_keywords)] = _legacy

_OVERFLOW_KEYWORDS = frozenset({"visible", "hidden", "clip", "scroll", "auto", "overlay"})
_CONTENT_DISTRIBUTION = frozenset({"space-between", "space-around", "space-evenly", "stretch"})
_CONTENT_POSITION = frozenset({"center", "start", "end", "flex-start", "flex-end"})
_SELF_POSITION = frozenset({"center", "start", "end", "self-start", "self-end", "flex-start", "flex-end"})

#: property -> its keywords, for properties that take exactly one of them
_SINGLE_KEYWORD_PROPERTIES: dict[str, frozenset] = {
    "position": frozenset({"static", "relative", "absolute", "fixed", "sticky", "-webkit-sticky"}),
    "float": frozenset({"none", "left", "right", "inline-start", "inline-end"}),
    "clear": frozenset({"none", "left", "right", "both", "inline-start", "inline-end"}),
    "visibility": frozenset({"visible", "hidden", "collapse"}),
    "box-sizing": frozenset({"content-box", "border-box"}),
    "overflow-x": _OVERFLOW_KEYWORDS,
    "overflow-y": _OVERFLOW_KEYWORDS,
    "table-layout": frozenset({"auto", "fixed"}),
    "border-collapse": frozenset({"collapse", "separate"}),
    "empty-cells": frozenset({"show", "hide"}),
    "caption-side": frozenset({"top", "bottom"}),
    "flex-direction": frozenset({"row", "row-reverse", "column", "column-reverse"}),
    "flex-wrap": frozenset({"nowrap", "wrap", "wrap-reverse"}),
    "direction": frozenset({"ltr", "rtl"}),
    "writing-mode": frozenset(
        {"horizontal-tb", "vertical-rl", "vertical-lr", "sideways-rl", "sideways-lr", "lr", "lr-tb", "rl", "rl-tb",
         "tb", "tb-rl"}
    ),
    "text-align": frozenset(
        {"start", "end", "left", "right", "center", "justify", "match-parent", "justify-all", "-webkit-center",
         "-webkit-left", "-webkit-right", "-webkit-match-parent", "-webkit-auto"}
    ),
}  # fmt: skip
_WHITE_SPACE_LEGACY = frozenset({"normal", "pre", "nowrap", "pre-wrap", "pre-line", "break-spaces"})
_WHITE_SPACE_COLLAPSE = frozenset({"collapse", "preserve", "preserve-breaks", "preserve-spaces", "break-spaces"})
_INTEGER_RE = re.compile(r"^[+-]?\d+$")
_NON_NEGATIVE_LENGTH_RE = re.compile(r"^\+?(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?(?:px|em|rem|ex|ch|in|cm|mm|q|pt|pc|vw|vh|vmin|vmax|vi|vb|lh|rlh|cap|ic)?$", re.I)


def _alignment_valid(name: str, words: list[str]) -> bool:
    """CSS Box Alignment 3's grammars for justify-/align-content/-items/-self."""
    if not words or len(words) > 2:
        return False
    joined = " ".join(words)
    if joined in ("first baseline", "last baseline") or joined == "baseline":
        return name != "justify-content"
    if len(words) == 1:
        word = words[0]
        if word == "normal" or (word == "auto" and name.endswith("-self")):
            return True
        if word == "anchor-center" and name in ("align-self", "justify-self", "align-items", "justify-items"):
            return True
        if name.endswith("-content"):
            if word in _CONTENT_DISTRIBUTION or word in _CONTENT_POSITION:
                return True
        elif word == "stretch" or word in _SELF_POSITION:
            return True
        if word in ("left", "right") and name.startswith("justify") and name != "justify-items":
            return True
        return word in ("left", "right", "legacy") and name == "justify-items"
    first, second = words
    if name == "justify-items" and "legacy" in words:
        other = second if first == "legacy" else first
        return other in ("left", "right", "center")
    if first not in ("safe", "unsafe"):
        return False
    positions = _CONTENT_POSITION if name.endswith("-content") else _SELF_POSITION
    return second in positions or (second in ("left", "right") and name.startswith("justify"))


def is_invalid_declaration(name: str, value: str) -> bool:
    """Whether ``name: value`` is invalid at parse time for one of the
    properties checked here (see above); False for everything else."""
    low = value.strip().lower()
    if not low or low in _GLOBAL_KEYWORDS or "var(" in low or "attr(" in low or "env(" in low:
        return False
    keywords = _SINGLE_KEYWORD_PROPERTIES.get(name)
    if keywords is not None:
        return low not in keywords
    words = low.split()
    if name == "display":
        return not (low in _DISPLAY_SINGLE if len(words) == 1 else " ".join(words) in DISPLAY_MULTI_KEYWORDS)
    if name == "overflow":
        return not (1 <= len(words) <= 2 and all(word in _OVERFLOW_KEYWORDS for word in words))
    if name == "white-space":
        if len(words) == 1 and low in _WHITE_SPACE_LEGACY | _WHITE_SPACE_COLLAPSE | {"wrap"}:
            return False
        collapse = [word for word in words if word in _WHITE_SPACE_COLLAPSE]
        wrap = [word for word in words if word in ("wrap", "nowrap")]
        return not (len(words) == 2 and len(collapse) == 1 and len(wrap) == 1)
    if name in ("justify-content", "align-content", "align-items", "align-self", "justify-items", "justify-self"):
        return not _alignment_valid(name, words)
    if name == "grid-auto-flow":
        flow = [word for word in words if word in ("row", "column")]
        dense = [word for word in words if word == "dense"]
        return not (1 <= len(words) <= 2 and len(flow) <= 1 and len(dense) <= 1 and len(flow) + len(dense) == len(words))
    if name == "font-style":
        return not (low in ("normal", "italic", "oblique") or (words[0] == "oblique" and len(words) == 2))
    if name == "text-transform":
        cases = [word for word in words if word in ("capitalize", "uppercase", "lowercase")]
        others = [word for word in words if word in ("full-width", "full-size-kana")]
        if low in ("none", "math-auto"):
            return False
        return not (words and len(cases) <= 1 and len(set(others)) == len(others) and len(cases) + len(others) == len(words))
    if name == "opacity":
        number = low[:-1] if low.endswith("%") else low
        return not (_NUMBER_RE.match(number) or low.startswith(("calc(", "min(", "max(", "clamp(")))
    if name in ("z-index", "order"):
        return not ((low == "auto" and name == "z-index") or _INTEGER_RE.match(low) or low.startswith("calc("))
    if name in ("flex-grow", "flex-shrink"):
        return not ((_NUMBER_RE.match(low) and not low.startswith("-")) or low.startswith("calc("))
    if name == "border-spacing":
        # one or two non-negative lengths -- never a percentage (CSS 2.1 17.6.1)
        return not (1 <= len(words) <= 2 and all(_NON_NEGATIVE_LENGTH_RE.match(word) or word.startswith("calc(") for word in words))
    if name == "flex":
        return expand_shorthand(name, value) is None
    return False
