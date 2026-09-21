"""
domonic.layout
==============

The CSS/layout boundary: a clean seam between domonic's CSSOM (cascade,
inheritance, ``getComputedStyle``) and any future layout engine.

``layout_style(element)`` reads an element's cascaded style and returns it as
a small set of typed values -- lengths already resolved to CSS pixels, but
percentages, ``auto``, and anything layout-dependent (intrinsic sizing, an
unexpanded ``repeat()``/``minmax()`` track, a named grid line) left exactly
as CSS specified them. It builds on ``domonic.style.ComputedStyleDeclaration``
for the cascade itself, but reads the *cascaded* value rather than the
*used* value ``getComputedStyle`` reports -- ``getComputedStyle`` already
guesses at a containing block to turn ``%`` into a px string, which is
precisely the premature resolution a layout engine needs to do for itself.

This module has no opinion on what a layout engine does with these values --
that binding (Taffy or otherwise) lives outside domonic. Its other half is
the geometry hand-back: ``set_layout_box``/``get_layout_box`` give a layout
engine a place to store the box it computed for an element, and
``Element.getBoundingClientRect``/``clientWidth``/``offsetWidth`` and friends
in ``domonic.dom`` consult it before falling back to their existing
heuristics -- so nothing changes for code that never attaches an engine.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Union

from . import _cssom
from .style import (
    ComputedStyleDeclaration,
    _BORDER_WIDTH_KEYWORD_PX,
    _BORDER_WIDTH_TO_STYLE,
    _eval_calc_to_px,
    _expand_var_references,
    _length_string_to_px,
)

__all__ = [
    "Auto",
    "AUTO",
    "Length",
    "Percent",
    "Fr",
    "Keyword",
    "Ratio",
    "GridLine",
    "GridSpan",
    "Edges",
    "Gap",
    "LayoutValue",
    "LayoutStyle",
    "layout_style",
    "LayoutBox",
    "get_layout_box",
    "set_layout_box",
    "clear_layout_box",
]


# -- typed values -----------------------------------------------------------
#
# Every layout-relevant CSS value domonic exposes comes back as one of these
# instead of a raw string, so a layout engine adapter can dispatch on type
# instead of re-parsing CSS text.


class Auto:
    """Sentinel for the CSS ``auto`` keyword. Use the module-level ``AUTO``."""

    _instance: "Auto | None" = None

    def __new__(cls) -> "Auto":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self) -> str:
        return "AUTO"


AUTO = Auto()


@dataclass(frozen=True)
class Length:
    """An absolute length, already resolved to CSS pixels."""

    px: float


@dataclass(frozen=True)
class Percent:
    """A percentage, as a 0.0-1.0 fraction (``50%`` -> ``Percent(0.5)``)."""

    fraction: float


@dataclass(frozen=True)
class Fr:
    """A ``<flex-value>fr`` grid track size, e.g. ``1fr`` -> ``Fr(1.0)``."""

    value: float


@dataclass(frozen=True)
class Keyword:
    """A CSS keyword or function domonic does not resolve further.

    Covers plain keywords (``block``, ``nowrap``, ``thin``), intrinsic sizing
    (``min-content``, ``max-content``, ``fit-content(20px)``), and an
    unexpanded grid track function (``repeat(2, 1fr)``, ``minmax(10px, 1fr)``)
    -- all of these need either layout or a fuller CSS Grid implementation
    than domonic carries, so they are handed on verbatim.
    """

    value: str


@dataclass(frozen=True)
class Ratio:
    """A resolved ``aspect-ratio``, e.g. ``16 / 9`` -> ``Ratio(16.0, 9.0)``."""

    width: float
    height: float


@dataclass(frozen=True)
class GridLine:
    """A resolved numbered grid line, e.g. ``grid-column-start: 2``."""

    line: int


@dataclass(frozen=True)
class GridSpan:
    """``span N`` in a grid-column/grid-row longhand."""

    count: int


LayoutValue = Union[Auto, Length, Percent, Fr, Keyword]


@dataclass(frozen=True)
class Edges:
    """Four-sided values -- margin, padding, border-width, or inset."""

    top: Any
    right: Any
    bottom: Any
    left: Any


@dataclass(frozen=True)
class Gap:
    """``row-gap``/``column-gap`` (also settable together via ``gap``)."""

    row: Any
    column: Any


# -- parsing: cascaded CSS text -> typed values ------------------------------

_PERCENT_RE = re.compile(r"^([+-]?(?:\d+\.?\d*|\.\d+))%$")
_FR_RE = re.compile(r"^([+-]?(?:\d+\.?\d*|\.\d+))fr$", re.I)
_SPAN_RE = re.compile(r"^span\s+(\d+)$", re.I)
_INT_RE = re.compile(r"^[+-]?\d+$")
_RATIO_RE = re.compile(r"^([+-]?(?:\d+\.?\d*|\.\d+))\s*/\s*([+-]?(?:\d+\.?\d*|\.\d+))$")
_NUMBER_RE = re.compile(r"^[+-]?(?:\d+\.?\d*|\.\d+)$")
_TRACK_FUNCTION_PREFIXES = ("repeat(", "minmax(", "fit-content(")


def _parse_length_or_percent(
    raw: "str | None",
    computed: ComputedStyleDeclaration,
    *,
    allow_percent: bool = True,
    allow_auto: bool = True,
) -> Any:
    """A single ``<length-percentage>`` (or ``auto``) token -> a typed value.

    Resolves absolute units and font-relative units (``em``/``rem``) to px
    using the element's own cascade, exactly as ``getComputedStyle`` would --
    but a percentage stays a ``Percent``, ``auto`` stays ``AUTO``, and
    anything else domonic doesn't resolve (``none``, ``thin``, a ``calc()``
    mixing in a ``%``) is handed back as a ``Keyword`` rather than dropped.
    """
    text = (raw or "").strip()
    if not text:
        return Keyword("")
    low = text.lower()
    if low == "auto":
        return AUTO if allow_auto else Keyword(text)
    percent_match = _PERCENT_RE.match(text)
    if percent_match:
        if allow_percent:
            return Percent(float(percent_match.group(1)) / 100.0)
        return Keyword(text)
    if "calc(" in low:
        # this reads the raw cascaded string, not getComputedStyle's own
        # resolved accessors (which already expand var() -- see
        # _compute_property_value), so a var() reference is still literal
        # text here and needs expanding before the evaluator below can make
        # sense of it.
        if "var(" in text:
            text = _expand_var_references(text, computed._custom_property).strip()
            low = text.lower()
        if "%" in text:
            # mixes a percentage in -- needs the containing block, which is
            # layout's job, not the cascade's.
            return Keyword(text)
        px = _eval_calc_to_px(text, em_px=computed._font_size_px(), rem_px=computed._root_font_size_px())
        return Length(px) if px is not None else Keyword(text)
    px = _length_string_to_px(
        text,
        em_px=computed._font_size_px(),
        rem_px=computed._root_font_size_px(),
        percent_px=None,
    )
    if px is not None:
        return Length(px)
    return Keyword(text)


def _parse_aspect_ratio(raw: "str | None") -> Any:
    text = (raw or "").strip().lower()
    if not text or text == "auto":
        return AUTO
    # the combined ``auto <ratio>`` / ``<ratio> auto`` syntax -- take the
    # ratio half, the ``auto`` half only matters once layout is involved.
    ratio_text = " ".join(p for p in text.split() if p != "auto") or text
    match = _RATIO_RE.match(ratio_text)
    if match:
        return Ratio(float(match.group(1)), float(match.group(2)))
    if _NUMBER_RE.match(ratio_text):
        return Ratio(float(ratio_text), 1.0)
    return Keyword(text)


def _parse_grid_line(raw: "str | None") -> Any:
    text = (raw or "").strip()
    if not text or text.lower() == "auto":
        return AUTO
    span_match = _SPAN_RE.match(text)
    if span_match:
        return GridSpan(int(span_match.group(1)))
    if _INT_RE.match(text):
        return GridLine(int(text))
    # a named line / custom-ident -- resolving it needs the template this
    # line sits in, which is layout's job.
    return Keyword(text)


def _split_track_list(text: str) -> list[str]:
    """Split a track list on whitespace, ignoring whitespace inside a
    function call (``repeat(2, 1fr)``, ``minmax(10px, 1fr)``)."""
    tokens = []
    depth = 0
    current = ""
    for char in text:
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        if char.isspace() and depth == 0:
            if current:
                tokens.append(current)
                current = ""
            continue
        current += char
    if current:
        tokens.append(current)
    return tokens


def _parse_track_size(token: str, computed: ComputedStyleDeclaration) -> Any:
    low = token.lower()
    if low == "auto":
        return AUTO
    fr_match = _FR_RE.match(token)
    if fr_match:
        return Fr(float(fr_match.group(1)))
    if low.startswith(_TRACK_FUNCTION_PREFIXES):
        return Keyword(token)
    return _parse_length_or_percent(token, computed)


def _parse_track_list(raw: "str | None", computed: ComputedStyleDeclaration) -> list:
    text = (raw or "").strip()
    if not text or text.lower() == "none":
        return []
    return [_parse_track_size(token, computed) for token in _split_track_list(text)]


def _parse_number(raw: "str | None", default: float) -> Any:
    text = (raw or "").strip()
    if not text:
        return default
    try:
        return float(text)
    except ValueError:
        return Keyword(text)


# -- LayoutStyle --------------------------------------------------------------


@dataclass(frozen=True)
class LayoutStyle:
    """Layout-ready cascaded values for one element, one property per Taffy
    ``Style`` field. Nothing here has been resolved against a containing
    block, an intrinsic content size, or a grid's actual track count --
    that's a layout engine's job. Construct via ``layout_style(element)``."""

    display: Keyword
    position: Keyword
    boxSizing: Keyword
    overflowX: Keyword
    overflowY: Keyword
    aspectRatio: Any

    inset: Edges
    width: Any
    height: Any
    minWidth: Any
    minHeight: Any
    maxWidth: Any
    maxHeight: Any

    margin: Edges
    padding: Edges
    borderWidth: Edges
    gap: Gap

    flexDirection: Keyword
    flexWrap: Keyword
    flexGrow: Any
    flexShrink: Any
    flexBasis: Any
    alignItems: Keyword
    alignSelf: Keyword
    alignContent: Keyword
    justifyContent: Keyword
    justifySelf: Keyword

    gridAutoFlow: Keyword
    gridAutoColumns: list
    gridAutoRows: list
    gridTemplateColumns: list
    gridTemplateRows: list
    gridColumnStart: Any
    gridColumnEnd: Any
    gridRowStart: Any
    gridRowEnd: Any

    element: Any = field(repr=False, compare=False, default=None)

    @classmethod
    def from_computed(cls, computed: ComputedStyleDeclaration) -> "LayoutStyle":
        """Build a ``LayoutStyle`` from a ``ComputedStyleDeclaration`` the
        caller already has, instead of ``layout_style()`` building its own.

        Lets a caller that needs both a ``LayoutStyle`` (for layout) and the
        ``ComputedStyleDeclaration`` itself (for anything ``LayoutStyle``
        deliberately excludes, e.g. colours for painting) share one
        resolved cascade for the element instead of resolving it twice.

        Every field here comes from the raw cascade (``computed._resolved``)
        or the font-size chain -- nothing reads a ``LayoutBox`` (percentages
        and ``auto`` come back as typed placeholders, not used values), so
        the result is immutable for as long as *computed* itself is valid,
        including across a relayout. Cached on *computed* accordingly: a
        caller that (like a layout engine driving multiple passes) asks for
        the same element's ``LayoutStyle`` more than once against the same
        ``ComputedStyleDeclaration`` does the parsing once."""
        cached = computed.__dict__.get("_layout_style_cache")
        if cached is not None:
            return cached
        # the raw cascaded (author + inline, shorthand-expanded, inherited)
        # string for a longhand -- *not* getComputedStyle's used value.
        raw = computed._resolved.get

        def dim(name: str, **kwargs: Any) -> Any:
            return _parse_length_or_percent(raw(name), computed, **kwargs)

        def kw(name: str) -> Keyword:
            return Keyword((raw(name) or "").strip().lower())

        def edges(top: str, right: str, bottom: str, left: str, **kwargs: Any) -> Edges:
            return Edges(dim(top, **kwargs), dim(right, **kwargs), dim(bottom, **kwargs), dim(left, **kwargs))

        def border_width_dim(name: str) -> Any:
            # a side's used border-width is 0 whenever its border-style is
            # none/hidden, regardless of what border-width itself says; this
            # reads the raw cascade directly (unlike getComputedStyle, this
            # function has no other style-aware gate), so both that and the
            # thin/medium/thick keywords need resolving here explicitly.
            style_prop = _BORDER_WIDTH_TO_STYLE[name]
            if (raw(style_prop) or "").strip().lower() in ("none", "hidden"):
                return Length(0.0)
            keyword_px = _BORDER_WIDTH_KEYWORD_PX.get((raw(name) or "").strip().lower())
            if keyword_px is not None:
                return Length(keyword_px)
            return dim(name, allow_auto=False, allow_percent=False)

        def border_width_edges(top: str, right: str, bottom: str, left: str) -> Edges:
            return Edges(
                border_width_dim(top), border_width_dim(right), border_width_dim(bottom), border_width_dim(left)
            )

        def tracks(name: str) -> list:
            return _parse_track_list(raw(name), computed)

        def line(name: str) -> Any:
            return _parse_grid_line(raw(name))

        result = cls(
            display=Keyword(computed._computed_display(raw("display") or "inline")),
            position=kw("position"),
            boxSizing=kw("box-sizing"),
            overflowX=kw("overflow-x"),
            overflowY=kw("overflow-y"),
            aspectRatio=_parse_aspect_ratio(raw("aspect-ratio")),
            inset=edges("top", "right", "bottom", "left"),
            width=dim("width"),
            height=dim("height"),
            minWidth=dim("min-width"),
            minHeight=dim("min-height"),
            maxWidth=dim("max-width"),
            maxHeight=dim("max-height"),
            margin=edges("margin-top", "margin-right", "margin-bottom", "margin-left"),
            padding=edges("padding-top", "padding-right", "padding-bottom", "padding-left", allow_auto=False),
            borderWidth=border_width_edges(
                "border-top-width",
                "border-right-width",
                "border-bottom-width",
                "border-left-width",
            ),
            gap=Gap(
                dim("row-gap", allow_auto=False),
                dim("column-gap", allow_auto=False),
            ),
            flexDirection=kw("flex-direction"),
            flexWrap=kw("flex-wrap"),
            flexGrow=_parse_number(raw("flex-grow"), 0.0),
            flexShrink=_parse_number(raw("flex-shrink"), 1.0),
            flexBasis=dim("flex-basis"),
            alignItems=kw("align-items"),
            alignSelf=kw("align-self"),
            alignContent=kw("align-content"),
            justifyContent=kw("justify-content"),
            justifySelf=kw("justify-self"),
            gridAutoFlow=kw("grid-auto-flow"),
            gridAutoColumns=tracks("grid-auto-columns"),
            gridAutoRows=tracks("grid-auto-rows"),
            gridTemplateColumns=tracks("grid-template-columns"),
            gridTemplateRows=tracks("grid-template-rows"),
            gridColumnStart=line("grid-column-start"),
            gridColumnEnd=line("grid-column-end"),
            gridRowStart=line("grid-row-start"),
            gridRowEnd=line("grid-row-end"),
            element=computed._element,
        )
        computed.__dict__["_layout_style_cache"] = result
        return result


def layout_style(element: Any, computed: "ComputedStyleDeclaration | None" = None) -> LayoutStyle:
    """Layout-ready cascaded style for *element*.

    Runs the same cascade ``getComputedStyle`` does (author rules, inline
    style, inheritance, initial values) but stops short of used-value
    resolution: percentages, ``auto``, and anything layout-dependent come
    back as typed placeholders instead of a guessed px string. Works on a
    detached element -- by default it builds its own
    ``ComputedStyleDeclaration`` rather than going through
    ``window.getComputedStyle``.

    Pass an already-resolved *computed* (e.g. one also needed for something
    ``LayoutStyle`` excludes, like paint-only colours) to reuse it instead of
    resolving the element's cascade a second time -- ``getComputedStyle()``
    itself already caches per element, so this is also just
    ``LayoutStyle.from_computed(window.getComputedStyle(element))`` for a
    caller that has a window handy.
    """
    return LayoutStyle.from_computed(computed if computed is not None else ComputedStyleDeclaration(element))


# -- geometry hand-back -------------------------------------------------------


@dataclass(frozen=True)
class LayoutBox:
    """The box a layout engine computed for one element, in CSS pixels.

    ``x``/``y``/``width``/``height`` are the border box (what
    ``getBoundingClientRect``/``offsetWidth``/``offsetHeight`` report, and
    what any layout engine naturally produces per node); ``client_width``/
    ``client_height`` are the padding box (``clientWidth``/``clientHeight``);
    ``border_top``/``border_left`` are the resolved border widths
    (``clientTop``/``clientLeft``); ``margin_*`` are the resolved margins,
    used by ``getComputedStyle`` to report a real used pixel value for
    ``margin`` wherever it was ``auto``.

    ``content_width``/``content_height`` default to ``None`` rather than
    ``0.0``: leave them unset and ``getComputedStyle`` reports the concrete
    ``width``/``height`` geometry supplied by the layout engine for
    ``width:auto``/``height:auto``. Set them explicitly when the engine wants
    computed style to report a separate content size. Percentages on children
    resolve against an explicitly supplied parent content size when present,
    otherwise against the parent's concrete box size.
    """

    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    height: float = 0.0
    client_width: float = 0.0
    client_height: float = 0.0
    border_top: float = 0.0
    border_left: float = 0.0
    content_width: "float | None" = None
    content_height: "float | None" = None
    margin_top: float = 0.0
    margin_right: float = 0.0
    margin_bottom: float = 0.0
    margin_left: float = 0.0


def get_layout_box(element: Any) -> "LayoutBox | None":
    """The box a layout engine last computed for *element*, or ``None`` if
    none has been supplied yet (the caller should fall back to its own
    heuristic in that case)."""
    return getattr(element, "_layout_box", None)


def set_layout_box(element: Any, box: LayoutBox) -> None:
    """Attach the box a layout engine computed for *element*."""
    element._layout_box = box
    _cssom.bump_layout_epoch()


def clear_layout_box(element: Any) -> None:
    """Detach any layout box previously set on *element*."""
    if "_layout_box" in getattr(element, "__dict__", {}):
        del element.__dict__["_layout_box"]
        _cssom.bump_layout_epoch()
