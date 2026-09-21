"""
domonic.svg
===========

SVG tag constructors and SVG-aware DOM elements for domonic.

The SVG surface participates in the same tree, event, and rendering model as
the rest of domonic. This module keeps the existing constructor API intact
while exposing a more browser-like SVG interface hierarchy.
"""

from __future__ import annotations

import re
from typing import Any

from domonic.dom import DOMMatrix, DOMPoint, DOMRect, Element

SVG_NAMESPACE = "http://www.w3.org/2000/svg"
_NUMBER_RE = re.compile(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?")


def _svg_number(value: Any, default: float = 0.0) -> float:
    """Parse the first SVG-style number from *value*.

    Kept for compatibility with code that may already import the private helper.
    """
    if value is None:
        return default
    match = _NUMBER_RE.search(str(value))
    return float(match.group(0)) if match else default


def _svg_points(value: Any) -> list[tuple[float, float]]:
    """Parse an SVG ``points`` attribute into ``(x, y)`` pairs.

    Kept for compatibility with code that may already import the private helper.
    """
    numbers = [_svg_number(item) for item in re.split(r"[\s,]+", str(value or "").strip()) if item]
    return list(zip(numbers[0::2], numbers[1::2]))


class SVGPoint(DOMPoint):
    """SVGPoint-compatible wrapper backed by domonic's DOMPoint."""

    def matrixTransform(self, matrix: Any) -> DOMPoint:
        return DOMMatrix.fromMatrix(matrix).transformPoint(self)


class SVGElement(Element):
    """Base interface for SVG elements.

    Existing domonic behaviour is intentionally preserved here: the historic
    ``createSVGPoint`` / ``createSVGMatrix`` conveniences remain available on
    every SVGElement even though browsers normally expose the factory methods
    on ``SVGSVGElement``.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.namespaceURI = SVG_NAMESPACE

    @property
    def ownerSVGElement(self) -> "SVGSVGElement | SVGElement | None":
        """Nearest ancestor ``<svg>`` element, or ``None`` for the outermost SVG."""
        current = getattr(self, "parentNode", None)
        while isinstance(current, Element):
            if (
                isinstance(current, SVGElement)
                and current.namespaceURI == SVG_NAMESPACE
                and str(getattr(current, "name", "")).lower() == "svg"
            ):
                return current
            current = getattr(current, "parentNode", None)
        return None

    @property
    def viewportElement(self) -> "SVGSVGElement | SVGElement | None":
        """Element establishing this element's nearest SVG viewport.

        For domonic's current SVG model this is the nearest ancestor ``<svg>``.
        """
        return self.ownerSVGElement

    # Compatibility: these historically existed on SVGElement in domonic.
    def createSVGPoint(self, x: float = 0, y: float = 0) -> SVGPoint:
        return SVGPoint(x, y)

    def createSVGMatrix(self) -> DOMMatrix:
        return DOMMatrix()

    def createSVGRect(self) -> DOMRect:
        return DOMRect()


class SVGGraphicsElement(SVGElement):
    """Base interface for SVG elements that directly participate in graphics.

    The actual geometry implementation remains in ``domonic.dom.Element`` so
    existing behaviour stays identical. These wrappers put the API on the
    browser-like SVG interface without changing the implementation underneath.
    """

    def getBBox(self, *args: Any, **kwargs: Any) -> DOMRect:
        return super().getBBox(*args, **kwargs)

    def getCTM(self) -> DOMMatrix:
        return super().getCTM()

    def getScreenCTM(self) -> DOMMatrix:
        return super().getScreenCTM()

    def getTransformToElement(self, element: Element) -> DOMMatrix:
        return super().getTransformToElement(element)


class SVGGeometryElement(SVGGraphicsElement):
    """Base interface for SVG geometry elements such as ``path`` and ``rect``.

    ``getTotalLength`` / ``getPointAtLength`` are intentionally not guessed at
    here. They require a shared path-length implementation in ``domonic.dom`` so
    all geometry, CTM and rendering consumers agree on the same numbers.
    """


class SVGTextContentElement(SVGGraphicsElement):
    """Base interface for SVG text-content elements."""

    def getNumberOfChars(self) -> int:
        return super().getNumberOfChars()

    def getComputedTextLength(self) -> float:
        return super().getComputedTextLength()

    def getSubStringLength(self, charnum: int = 0, nchars: int | None = None) -> float:
        return super().getSubStringLength(charnum, nchars)


class SVGSVGElement(SVGGraphicsElement):
    """Interface used by the root/nested ``<svg>`` element.

    Browser SVG factory methods belong here. The same methods remain on
    ``SVGElement`` for backwards compatibility with existing domonic code.
    """

    def createSVGPoint(self, x: float = 0, y: float = 0) -> SVGPoint:
        return SVGPoint(x, y)

    def createSVGMatrix(self) -> DOMMatrix:
        return DOMMatrix()

    def createSVGRect(self) -> DOMRect:
        return DOMRect()


# SVG 2 element names exposed by domonic today.
#
# NOTE: audio/canvas/iframe/video are retained here for compatibility with the
# existing public API. In browser SVG2 parsing they are HTML-namespace elements
# when embedded in SVG, but removing or changing these constructors would be a
# breaking change for domonic users.
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


# Browser-like interface grouping. These affect Python inheritance only; tag
# names, namespaces, serialization and constructor names remain unchanged.
_SVG_GEOMETRY_TAGS = frozenset(
    {
        "circle",
        "ellipse",
        "line",
        "path",
        "polygon",
        "polyline",
        "rect",
    }
)

_SVG_TEXT_CONTENT_TAGS = frozenset(
    {
        "text",
        "textPath",
        "tspan",
    }
)

_SVG_GRAPHICS_TAGS = frozenset(
    {
        "a",
        "foreignObject",
        "g",
        "image",
        "switch",
        "symbol",
        "use",
    }
)

_CUSTOM_SVG_CLASSES: dict[str, type[SVGElement]] = {}


def _svg_class_name(tag_name: str) -> str:
    return tag_name.replace("-", "_")


def _svg_base_class(tag_name: str) -> type[SVGElement]:
    if tag_name == "svg":
        return SVGSVGElement
    if tag_name in _SVG_GEOMETRY_TAGS:
        return SVGGeometryElement
    if tag_name in _SVG_TEXT_CONTENT_TAGS:
        return SVGTextContentElement
    if tag_name in _SVG_GRAPHICS_TAGS:
        return SVGGraphicsElement
    return SVGElement


def _make_svg_constructor(tag_name: str) -> type[SVGElement]:
    class_name = _svg_class_name(tag_name)
    base = _svg_base_class(tag_name)
    return type(
        class_name,
        (base,),
        {
            "name": tag_name,
            "__module__": __name__,
        },
    )


for _tag_name in svg_tags:
    globals()[_svg_class_name(_tag_name)] = _make_svg_constructor(_tag_name)


def create_element(name: str = "custom_svg_tag", *args: Any, **kwargs: Any) -> SVGElement:
    """Create an SVG element, including custom or hyphenated SVG tags.

    Existing public behaviour is preserved:

    * known names return the exported constructor class;
    * Python-safe aliases such as ``font_face`` resolve to ``font-face``;
    * unknown names remain SVG-namespaced custom elements.
    """
    normalized_name = str(name).strip()
    if not normalized_name:
        normalized_name = "custom_svg_tag"

    tag_name = normalized_name
    if tag_name not in _SVG_TAG_LOOKUP:
        tag_name = _PYTHON_NAME_TO_TAG.get(normalized_name, normalized_name)

    if tag_name in _SVG_TAG_LOOKUP:
        return globals()[_svg_class_name(tag_name)](*args, **kwargs)

    custom_svg_tag = _CUSTOM_SVG_CLASSES.get(normalized_name)
    if custom_svg_tag is None:
        custom_svg_tag = type(
            "custom_svg_tag",
            (SVGElement,),
            {
                "name": normalized_name,
                "__module__": __name__,
            },
        )
        _CUSTOM_SVG_CLASSES[normalized_name] = custom_svg_tag

    new_tag = custom_svg_tag(*args, **kwargs)
    new_tag.name = normalized_name
    return new_tag


__all__ = [
    "SVG_NAMESPACE",
    "SVGElement",
    "SVGGraphicsElement",
    "SVGGeometryElement",
    "SVGTextContentElement",
    "SVGSVGElement",
    "SVGPoint",
    "create_element",
    "svg_tags",
    *[_svg_class_name(tag_name) for tag_name in svg_tags],
]
