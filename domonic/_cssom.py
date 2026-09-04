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

from typing import Callable

# --- inheritance ----------------------------------------------------------
# CSS properties that inherit from the parent element by default.
INHERITED_PROPERTIES: frozenset[str] = frozenset(
    {
        "azimuth", "border-collapse", "border-spacing", "caption-side", "color",
        "cursor", "direction", "empty-cells", "font", "font-family",
        "font-feature-settings", "font-kerning", "font-language-override",
        "font-optical-sizing", "font-size", "font-size-adjust", "font-stretch",
        "font-style", "font-synthesis", "font-variant", "font-variant-alternates",
        "font-variant-caps", "font-variant-east-asian", "font-variant-ligatures",
        "font-variant-numeric", "font-variant-position", "font-variation-settings",
        "font-weight", "hanging-punctuation", "hyphens", "image-rendering",
        "letter-spacing", "line-break", "line-height", "list-style",
        "list-style-image", "list-style-position", "list-style-type", "orphans",
        "overflow-wrap", "paint-order", "pointer-events", "quotes",
        "ruby-position", "tab-size", "text-align", "text-align-last",
        "text-combine-upright", "text-decoration-skip-ink", "text-indent",
        "text-justify", "text-orientation", "text-rendering", "text-shadow",
        "text-transform", "text-underline-offset", "text-underline-position",
        "visibility", "white-space", "widows", "word-break", "word-spacing",
        "word-wrap", "writing-mode",
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
}

# --- shorthand -> longhand ---------------------------------------------
# Order matters for reconstruction (values are emitted in this order).
SHORTHANDS: dict[str, tuple[str, ...]] = {
    "margin": ("margin-top", "margin-right", "margin-bottom", "margin-left"),
    "padding": ("padding-top", "padding-right", "padding-bottom", "padding-left"),
    "inset": ("top", "right", "bottom", "left"),
    "border-width": (
        "border-top-width", "border-right-width",
        "border-bottom-width", "border-left-width",
    ),
    "border-style": (
        "border-top-style", "border-right-style",
        "border-bottom-style", "border-left-style",
    ),
    "border-color": (
        "border-top-color", "border-right-color",
        "border-bottom-color", "border-left-color",
    ),
    "border-radius": (
        "border-top-left-radius", "border-top-right-radius",
        "border-bottom-right-radius", "border-bottom-left-radius",
    ),
    "border-top": (
        "border-top-width", "border-top-style", "border-top-color",
    ),
    "border-right": (
        "border-right-width", "border-right-style", "border-right-color",
    ),
    "border-bottom": (
        "border-bottom-width", "border-bottom-style", "border-bottom-color",
    ),
    "border-left": (
        "border-left-width", "border-left-style", "border-left-color",
    ),
    "border": (
        "border-top-width", "border-right-width", "border-bottom-width",
        "border-left-width", "border-top-style", "border-right-style",
        "border-bottom-style", "border-left-style", "border-top-color",
        "border-right-color", "border-bottom-color", "border-left-color",
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
        "font-style", "font-variant", "font-weight", "font-stretch",
        "font-size", "line-height", "font-family",
    ),
    "list-style": (
        "list-style-type", "list-style-position", "list-style-image",
    ),
    "text-decoration": (
        "text-decoration-line", "text-decoration-style", "text-decoration-color",
    ),
    "columns": ("column-width", "column-count"),
    "column-rule": (
        "column-rule-width", "column-rule-style", "column-rule-color",
    ),
    "background": (
        "background-image", "background-position", "background-size",
        "background-repeat", "background-origin", "background-clip",
        "background-attachment", "background-color",
    ),
    "transition": (
        "transition-property", "transition-duration",
        "transition-timing-function", "transition-delay",
    ),
    "animation": (
        "animation-duration", "animation-timing-function", "animation-delay",
        "animation-iteration-count", "animation-direction",
        "animation-fill-mode", "animation-play-state", "animation-name",
    ),
    "grid-template": (
        "grid-template-rows", "grid-template-columns", "grid-template-areas",
    ),
    "grid-column": ("grid-column-start", "grid-column-end"),
    "grid-row": ("grid-row-start", "grid-row-end"),
    "grid-area": (
        "grid-row-start", "grid-column-start", "grid-row-end", "grid-column-end",
    ),
}

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
    parts = value.split()
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
        "none", "hidden", "dotted", "dashed", "solid", "double", "groove",
        "ridge", "inset", "outset",
    }
)
_BORDER_WIDTH_KEYWORDS = frozenset({"thin", "medium", "thick"})
_FONT_STYLE_KEYWORDS = frozenset({"italic", "oblique"})
_FONT_VARIANT_KEYWORDS = frozenset({"small-caps"})
_FONT_WEIGHT_KEYWORDS = frozenset(
    {"bold", "bolder", "lighter", "100", "200", "300", "400", "500", "600",
     "700", "800", "900"}
)
_FONT_STRETCH_KEYWORDS = frozenset(
    {"ultra-condensed", "extra-condensed", "condensed", "semi-condensed",
     "semi-expanded", "expanded", "extra-expanded", "ultra-expanded"}
)
_GLOBAL_KEYWORDS = frozenset({"inherit", "initial", "unset", "revert", "revert-layer"})


def _looks_like_length(token: str) -> bool:
    token = token.strip().lower()
    if token in _BORDER_WIDTH_KEYWORDS:
        return True
    return bool(token) and (token[0].isdigit() or token[0] in "+-.") and (
        token.endswith(
            ("px", "em", "rem", "%", "vh", "vw", "vmin", "vmax", "pt", "pc",
             "ex", "ch", "cm", "mm", "in", "q", "fr", "0", "1", "2", "3", "4",
             "5", "6", "7", "8", "9")
        )
    )


def expand_shorthand(name: str, value: str) -> list[tuple[str, str]] | None:
    """Expand ``name: value`` (a shorthand) into ``[(longhand, value), ...]``.

    Returns ``None`` if the shorthand is not understood well enough to split
    (the caller then keeps only the shorthand entry).
    """
    value = value.strip()
    longs = SHORTHANDS.get(name)
    if not longs:
        return None
    lower = value.lower()
    if lower in _GLOBAL_KEYWORDS:
        return [(long, value) for long in longs]

    if name in BOX_SHORTHANDS or name in RADIUS_SHORTHANDS:
        if "/" in value:  # elliptical border-radius - keep as-is
            return None
        top, right, bottom, left = expand_box_values(value)
        return list(zip(longs, (top, right, bottom, left)))

    if name in ("border", "border-top", "border-right", "border-bottom", "border-left",
                "outline", "column-rule"):
        width = style = color = None
        for token in value.split():
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
        parts = value.split()
        grow, shrink, basis = "1", "1", "0%"
        nums = [p for p in parts if p.replace(".", "", 1).isdigit()]
        non_nums = [p for p in parts if p not in nums]
        if len(nums) >= 1:
            grow = nums[0]
        if len(nums) >= 2:
            shrink = nums[1]
        if non_nums:
            basis = non_nums[0]
        elif len(parts) == 1 and parts[0].replace(".", "", 1).isdigit():
            basis = "0%"
        return [("flex-grow", grow), ("flex-shrink", shrink), ("flex-basis", basis)]

    if name in ("overflow", "gap", "place-content", "place-items", "place-self",
                "flex-flow", "columns", "grid-column", "grid-row"):
        parts = value.split()
        if len(parts) == 1:
            return [(long, parts[0]) for long in longs]
        if len(parts) == len(longs):
            return list(zip(longs, parts))
        return None

    if name == "list-style":
        type_ = position = image = None
        for token in value.split():
            tl = token.lower()
            if tl in ("inside", "outside"):
                position = token
            elif tl == "none" or tl.startswith("url(") or "url(" in tl:
                image = token
            else:
                type_ = token
        return [
            ("list-style-type", type_ or "disc"),
            ("list-style-position", position or "outside"),
            ("list-style-image", image or "none"),
        ]

    if name == "text-decoration":
        line = style = color = None
        line_kw = {"none", "underline", "overline", "line-through", "blink"}
        style_kw = {"solid", "double", "dotted", "dashed", "wavy"}
        for token in value.split():
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
        # [ style || variant || weight || stretch ]? size [ / line-height ]? family
        tokens = value.split()
        style = variant = weight = stretch = "normal"
        size = line_height = ""
        family_start = 0
        for i, token in enumerate(tokens):
            tl = token.lower()
            if tl in _FONT_STYLE_KEYWORDS:
                style = token
            elif tl in _FONT_VARIANT_KEYWORDS:
                variant = token
            elif tl in _FONT_WEIGHT_KEYWORDS:
                weight = token
            elif tl in _FONT_STRETCH_KEYWORDS:
                stretch = token
            elif tl == "normal":
                continue
            else:
                # first non-keyword token is the size (optionally size/line-height)
                if "/" in token:
                    size, _, line_height = token.partition("/")
                else:
                    size = token
                family_start = i + 1
                break
        family = " ".join(tokens[family_start:]) or "inherit"
        return [
            ("font-style", style),
            ("font-variant", variant),
            ("font-weight", weight),
            ("font-stretch", stretch),
            ("font-size", size or "medium"),
            ("line-height", line_height or "normal"),
            ("font-family", family),
        ]

    # transition / animation / background / grid-template / grid-area:
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

    if name in BOX_SHORTHANDS or name in RADIUS_SHORTHANDS:
        vals = [get(long) for long in longs]
        if any(v == "" for v in vals):
            return ""
        return collapse_box_values(*vals)

    if name in ("border-top", "border-right", "border-bottom", "border-left",
                "outline", "column-rule"):
        prefix = "border" if name.startswith("border") else name
        parts = [get(f"{prefix}-{p}") for p in ("width", "style", "color")]
        if any(p == "" for p in parts):
            return ""
        return " ".join(p for p in parts if p and p != "currentcolor" and p != "medium") or parts[1]

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

    if name in ("overflow", "gap", "flex-flow", "place-content", "place-items",
                "place-self", "columns", "grid-column", "grid-row"):
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

