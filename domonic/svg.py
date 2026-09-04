"""
domonic.svg
===========

SVG tag constructors and SVG-aware DOM elements for domonic.

The SVG surface is designed to participate in the same tree, event, and
rendering model as the rest of the library rather than living in a separate
mini-framework.
"""

from __future__ import annotations

import re
from typing import Any

from domonic.dom import DOMMatrix, DOMPoint, DOMRect, Element

SVG_NAMESPACE = "http://www.w3.org/2000/svg"
_NUMBER_RE = re.compile(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?")


def _svg_number(value: Any, default: float = 0.0) -> float:
    if value is None:
        return default
    match = _NUMBER_RE.search(str(value))
    return float(match.group(0)) if match else default


def _svg_points(value: Any) -> list[tuple[float, float]]:
    numbers = [
        _svg_number(item)
        for item in re.split(r"[\s,]+", str(value or "").strip())
        if item
    ]
    return list(zip(numbers[0::2], numbers[1::2]))


class SVGPoint(DOMPoint):
    """SVGPoint-compatible wrapper backed by domonic's DOMPoint."""

    def matrixTransform(self, matrix: Any) -> DOMPoint:
        return DOMMatrix.fromMatrix(matrix).transformPoint(self)


class SVGElement(Element):
    """Base SVG element that keeps the SVG namespace on direct constructors."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.namespaceURI = SVG_NAMESPACE

    @property
    def ownerSVGElement(self) -> "SVGElement | None":
        current = getattr(self, "parentNode", None)
        while isinstance(current, Element):
            if (
                isinstance(current, SVGElement)
                and current.namespaceURI == SVG_NAMESPACE
                and getattr(current, "name", None) == "svg"
            ):
                return current
            current = getattr(current, "parentNode", None)
        return None

    @property
    def viewportElement(self) -> "SVGElement | None":
        return self.ownerSVGElement

    def createSVGPoint(self, x: float = 0, y: float = 0) -> SVGPoint:
        return SVGPoint(x, y)

    def createSVGMatrix(self) -> DOMMatrix:
        return DOMMatrix()

    # getBBox / getCTM / getScreenCTM / getComputedTextLength /
    # getTransformToElement are inherited from ``domonic.dom.Element``, which
    # carries the full SVG geometry + text-measurement implementation.


_SVG_2_TAGS = [
    "svg",
    "a",
    "animate",
    "animateMotion",
    "animateTransform",
    "audio",
    "canvas",
    "circle",
    "clipPath",
    "defs",
    "desc",
    "discard",
    "ellipse",
    "feBlend",
    "feColorMatrix",
    "feComponentTransfer",
    "feComposite",
    "feConvolveMatrix",
    "feDiffuseLighting",
    "feDisplacementMap",
    "feDistantLight",
    "feDropShadow",
    "feFlood",
    "feFuncA",
    "feFuncB",
    "feFuncG",
    "feFuncR",
    "feGaussianBlur",
    "feImage",
    "feMerge",
    "feMergeNode",
    "feMorphology",
    "feOffset",
    "fePointLight",
    "feSpecularLighting",
    "feSpotLight",
    "feTile",
    "feTurbulence",
    "filter",
    "foreignObject",
    "g",
    "iframe",
    "image",
    "line",
    "linearGradient",
    "marker",
    "mask",
    "metadata",
    "mpath",
    "path",
    "pattern",
    "polygon",
    "polyline",
    "radialGradient",
    "rect",
    "script",
    "set",
    "stop",
    "style",
    "switch",
    "symbol",
    "text",
    "textPath",
    "title",
    "tspan",
    "unknown",
    "use",
    "video",
    "view",
]

_SVG_LEGACY_TAGS = [
    "altGlyph",
    "altGlyphDef",
    "altGlyphItem",
    "animateColor",
    "color-profile",
    "cursor",
    "font",
    "font-face",
    "font-face-format",
    "font-face-name",
    "font-face-src",
    "font-face-uri",
    "glyph",
    "glyphRef",
    "hatch",
    "hatchpath",
    "hkern",
    "missing-glyph",
    "solidcolor",
    "tref",
    "vkern",
]

svg_tags = list(dict.fromkeys(_SVG_2_TAGS + _SVG_LEGACY_TAGS))
_SVG_TAG_LOOKUP = frozenset(svg_tags)
_PYTHON_NAME_TO_TAG = {tag_name.replace("-", "_"): tag_name for tag_name in svg_tags}


def _svg_class_name(tag_name: str) -> str:
    return tag_name.replace("-", "_")


def _make_svg_constructor(tag_name: str) -> type[SVGElement]:
    return type(_svg_class_name(tag_name), (SVGElement,), {"name": tag_name})


for _tag_name in svg_tags:
    globals()[_svg_class_name(_tag_name)] = _make_svg_constructor(_tag_name)


def create_element(
    name: str = "custom_svg_tag", *args: Any, **kwargs: Any
) -> SVGElement:
    """
    A method for creating SVG tags, including custom or hyphenated ones.
    """
    normalized_name = str(name).strip()
    if not normalized_name:
        normalized_name = "custom_svg_tag"

    tag_name = normalized_name
    if tag_name not in _SVG_TAG_LOOKUP:
        tag_name = _PYTHON_NAME_TO_TAG.get(normalized_name, normalized_name)

    if tag_name in _SVG_TAG_LOOKUP:
        return globals()[_svg_class_name(tag_name)](*args, **kwargs)

    custom_svg_tag = type("custom_svg_tag", (SVGElement,), {"name": normalized_name})
    new_tag = custom_svg_tag(*args, **kwargs)
    new_tag.name = normalized_name
    return new_tag


__all__ = [
    "SVG_NAMESPACE",
    "SVGElement",
    "SVGPoint",
    "create_element",
    "svg_tags",
    *[_svg_class_name(tag_name) for tag_name in svg_tags],
]
