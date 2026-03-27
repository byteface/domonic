"""
    domonic.svg
    ====================================
    Generate SVG with python 3

    WARNING - mostly lightly tested. keep expanding coverage as support improves.

    # https://www.w3.org/TR/SVG2/eltindex.html

"""

from __future__ import annotations

from typing import Any

from domonic.dom import Element
from domonic.html import a, audio, canvas, iframe, script, style, video

SVG_NAMESPACE = "http://www.w3.org/2000/svg"


class SVGElement(Element):
    """Base SVG element that keeps the SVG namespace on direct constructors."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.namespaceURI = SVG_NAMESPACE


svg_tags = [
    "svg",
    "animate",
    "animateMotion",
    "animateTransform",
    "circle",
    "clipPath",
    "defs",
    "desc",
    "ellipse",
    "filter",
    "image",
    "line",
    "linearGradient",
    "marker",
    "mask",
    "metadata",
    "missing-glyph",
    "mpath",
    "pattern",
    "polygon",
    "polyline",
    "radialGradient",
    "tspan",
    "path",
    "rect",
    "stop",
    "switch",
    "symbol",
    "text",
    "textPath",
    "title",
    "use",
    "view",
    "feBlend",
    "feColorMatrix",
    "feComponentTransfer",
    "feComposite",
    "feConvolveMatrix",
    "feDiffuseLighting",
    "feDisplacementMap",
    "feGaussianBlur",
    "feImage",
    "feMerge",
    "feMorphology",
    "feOffset",
    "feSpecularLighting",
    "feTile",
    "feTurbulence",
    "feDistantLight",
    "fePointLight",
    "feSpotLight",
    "feDropShadow",
    "discard",
    "feDistantLight",
    "feFlood",
    "feFuncA",
    "feFuncB",
    "feFuncG",
    "feFuncR",
    "feMergeNode",
    "foreignObject",
    "unknown",
    "cursor",
    "hatchpath",
    "altGlyph",
    "tref",
    "tspan",
    "altGlyphDef",
    "altGlyphItem",
    "glyph",
    "glyphRef",
    "solidcolor",
    "hatch",
    "font",
    "hkern",
    "vkern",
    "animateColor",
    "g",
]


# def svg_init(self, *args, **kwargs):
#     tag.__init__(self, *args, **kwargs)
#     Element.__init__(self, *args, **kwargs)


svg = type("svg", (SVGElement,), {"name": "svg"})

animate = type("animate", (SVGElement,), {"name": "animate"})
animateMotion = type("animateMotion", (SVGElement,), {"name": "animateMotion"})
animateTransform = type("animateTransform", (SVGElement,), {"name": "animateTransform"})
circle = type("circle", (SVGElement,), {"name": "circle"})
clipPath = type("clipPath", (SVGElement,), {"name": "clipPath"})
defs = type("defs", (SVGElement,), {"name": "defs"})
desc = type("desc", (SVGElement,), {"name": "desc"})
ellipse = type("ellipse", (SVGElement,), {"name": "ellipse"})
filter = type("filter", (SVGElement,), {"name": "filter"})
g = type("g", (SVGElement,), {"name": "g"})
image = type("image", (SVGElement,), {"name": "image"})
line = type("line", (SVGElement,), {"name": "line"})
linearGradient = type("linearGradient", (SVGElement,), {"name": "linearGradient"})
marker = type("marker", (SVGElement,), {"name": "marker"})
mask = type("mask", (SVGElement,), {"name": "mask"})
metadata = type("metadata", (SVGElement,), {"name": "metadata"})
mpath = type("mpath", (SVGElement,), {"name": "mpath"})
pattern = type("pattern", (SVGElement,), {"name": "pattern"})
polygon = type("polygon", (SVGElement,), {"name": "polygon"})
polyline = type("polyline", (SVGElement,), {"name": "polyline"})
radialGradient = type("radialGradient", (SVGElement,), {"name": "radialGradient"})

tspan = type("tspan", (SVGElement,), {"name": "tspan"})
path = type("path", (SVGElement,), {"name": "path"})
rect = type("rect", (SVGElement,), {"name": "rect"})
stop = type("stop", (SVGElement,), {"name": "stop"})
switch = type("switch", (SVGElement,), {"name": "switch"})
symbol = type("symbol", (SVGElement,), {"name": "symbol"})
text = type("text", (SVGElement,), {"name": "text"})
textPath = type("textPath", (SVGElement,), {"name": "textPath"})
title = type("title", (SVGElement,), {"name": "title"})
use = type("use", (SVGElement,), {"name": "use"})
view = type("view", (SVGElement,), {"name": "view"})

feBlend = type("feBlend", (SVGElement,), {"name": "feBlend"})
feColorMatrix = type("feColorMatrix", (SVGElement,), {"name": "feColorMatrix"})
feComponentTransfer = type("feComponentTransfer", (SVGElement,), {"name": "feComponentTransfer"})
feComposite = type("feComposite", (SVGElement,), {"name": "feComposite"})
feConvolveMatrix = type("feConvolveMatrix", (SVGElement,), {"name": "feConvolveMatrix"})
feDiffuseLighting = type("feDiffuseLighting", (SVGElement,), {"name": "feDiffuseLighting"})
feDisplacementMap = type("feDisplacementMap", (SVGElement,), {"name": "feDisplacementMap"})
feGaussianBlur = type("feGaussianBlur", (SVGElement,), {"name": "feGaussianBlur"})
feImage = type("feImage", (SVGElement,), {"name": "feImage"})
feMerge = type("feMerge", (SVGElement,), {"name": "feMerge"})
feMorphology = type("feMorphology", (SVGElement,), {"name": "feMorphology"})
feOffset = type("feOffset", (SVGElement,), {"name": "feOffset"})
feSpecularLighting = type("feSpecularLighting", (SVGElement,), {"name": "feSpecularLighting"})
feTile = type("feTile", (SVGElement,), {"name": "feTile"})
feTurbulence = type("feTurbulence", (SVGElement,), {"name": "feTurbulence"})
feDistantLight = type("feDistantLight", (SVGElement,), {"name": "feDistantLight"})
fePointLight = type("fePointLight", (SVGElement,), {"name": "fePointLight"})
feSpotLight = type("feSpotLight", (SVGElement,), {"name": "feSpotLight"})

feDropShadow = type("feDropShadow", (SVGElement,), {"name": "feDropShadow"})
discard = type("discard", (SVGElement,), {"name": "discard"})
feDistantLight = type("feDistantLight", (SVGElement,), {"name": "feDistantLight"})
feFlood = type("feFlood", (SVGElement,), {"name": "feFlood"})
feFuncA = type("feFuncA", (SVGElement,), {"name": "feFuncA"})
feFuncB = type("feFuncB", (SVGElement,), {"name": "feFuncB"})
feFuncG = type("feFuncG", (SVGElement,), {"name": "feFuncG"})
feFuncR = type("feFuncR", (SVGElement,), {"name": "feFuncR"})
feMergeNode = type("feMergeNode", (SVGElement,), {"name": "feMergeNode"})
foreignObject = type("foreignObject", (SVGElement,), {"name": "foreignObject"})
unknown = type("unknown", (SVGElement,), {"name": "unknown"})

cursor = type("cursor", (SVGElement,), {"name": "cursor"})
hatchpath = type("hatchpath", (SVGElement,), {"name": "hatchpath"})
altGlyph = type("altGlyph", (SVGElement,), {"name": "altGlyph"})
tref = type("tref", (SVGElement,), {"name": "tref"})
tspan = type("tspan", (SVGElement,), {"name": "tspan"})
altGlyphDef = type("altGlyphDef", (SVGElement,), {"name": "altGlyphDef"})
altGlyphItem = type("altGlyphItem", (SVGElement,), {"name": "altGlyphItem"})
glyph = type("glyph", (SVGElement,), {"name": "glyph"})
glyphRef = type("glyphRef", (SVGElement,), {"name": "glyphRef"})
solidcolor = type("solidcolor", (SVGElement,), {"name": "solidcolor"})
hatch = type("hatch", (SVGElement,), {"name": "hatch"})
font = type("font", (SVGElement,), {"name": "font"})
hkern = type("hkern", (SVGElement,), {"name": "hkern"})
vkern = type("vkern", (SVGElement,), {"name": "vkern"})
animateColor = type("animateColor", (SVGElement,), {"name": "animateColor"})
missing_glyph = type("missing_glyph", (SVGElement,), {"name": "missing-glyph"})


def create_element(name: str = "custom_svg_tag", *args: Any, **kwargs: Any) -> Element:
    """
    A method for creating SVG tags, including custom or hyphenated ones.
    """
    normalized_name = str(name).strip()
    if not normalized_name:
        normalized_name = "custom_svg_tag"
        name = "custom_svg_tag"

    if normalized_name in svg_tags:
        tag_name = normalized_name.replace("-", "_")
        return globals()[tag_name](*args, **kwargs)

    custom_svg_tag = type("custom_svg_tag", (SVGElement,), {"name": name})
    new_tag = custom_svg_tag(*args, **kwargs)
    new_tag.name = name
    return new_tag


# TODO --
# _set # builtin

# are these obs or new?
# meshgradient 🗑️?
# mesh 🗑️?
# meshpatch 🗑️?
# meshrow 🗑️?

# TODO - just use underscores for these tags?
# color-profile
# font-face
# font-face-format
# font-face-name
# font-face-src
# font-face-uri
