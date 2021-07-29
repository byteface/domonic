"""
    domonic.svg
    ====================================
    Generate SVG with python 3

    WARNING - totally not tested. except circle. I just assumed it would work...

    # https://www.w3.org/TR/SVG2/eltindex.html

"""

from domonic.html import tag
from domonic.dom import Element, Node


svg_tags = [
            "svg", "animate", "animateMotion", "animateTransform", "circle", "clipPath", "defs", "desc", "ellipse", "image",
            "line", "linearGradient", "marker", "mask", "mpath", "pattern", "polygon", "polyline", "radialGradient", "tspan", "path",
            "rect", "stop", "switch", "symbol", "text", "textPath", "title", "use", "view", "feBlend", "feColorMatrix", "feComponentTransfer",
            "feComposite", "feConvolveMatrix", "feDiffuseLighting", "feDisplacementMap", "feGaussianBlur", "feImage", "feMerge",
            "feMorphology", "feOffset", "feSpecularLighting", "feTile", "feTurbulence", "feDistantLight", "fePointLight", "feSpotLight",
            "feDropShadow", "discard", "feDistantLight", "feFlood", "feFuncA", "feFuncB", "feFuncG", "feFuncR", "feMergeNode", "foreignObject",
            "unknown", "cursor", "hatchpath", "altGlyph", "tref", "tspan", "altGlyphDef", "altGlyphItem", "glyph", "glyphRef", "solidcolor",
            "hatch", "font", "hkern", "vkern", "animateColor", "g"]


def svg_init(self, *args, **kwargs):
    tag.__init__(self, *args, **kwargs)
    Element.__init__(self, *args, **kwargs)


svg = type('svg', (tag, Element), {'name': 'svg', '__init__': svg_init})

animate = type('animate', (tag, Element), {'name': 'animate', '__init__': svg_init})
animateMotion = type('animateMotion', (tag, Element), {'name': 'animateMotion', '__init__': svg_init})
animateTransform = type('animateTransform', (tag, Element), {'name': 'animateTransform', '__init__': svg_init})
circle = type('circle', (tag, Element), {'name': 'circle', '__init__': svg_init})
clipPath = type('clipPath', (tag, Element), {'name': 'clipPath', '__init__': svg_init})
defs = type('defs', (tag, Element), {'name': 'defs', '__init__': svg_init})
desc = type('desc', (tag, Element), {'name': 'desc', '__init__': svg_init})
ellipse = type('ellipse', (tag, Element), {'name': 'ellipse', '__init__': svg_init})
g = type('g', (tag, Element), {'name': 'g', '__init__': svg_init})
image = type('image', (tag, Element), {'name': 'image', '__init__': svg_init})
line = type('line', (tag, Element), {'name': 'line', '__init__': svg_init})
linearGradient = type('linearGradient', (tag, Element), {'name': 'linearGradient', '__init__': svg_init})
marker = type('marker', (tag, Element), {'name': 'marker', '__init__': svg_init})
mask = type('mask', (tag, Element), {'name': 'mask', '__init__': svg_init})
mpath = type('mpath', (tag, Element), {'name': 'mpath', '__init__': svg_init})
pattern = type('pattern', (tag, Element), {'name': 'pattern', '__init__': svg_init})
polygon = type('polygon', (tag, Element), {'name': 'polygon', '__init__': svg_init})
polyline = type('polyline', (tag, Element), {'name': 'polyline', '__init__': svg_init})
radialGradient = type('radialGradient', (tag, Element), {'name': 'radialGradient', '__init__': svg_init})

tspan = type('tspan', (tag, Element), {'name': 'tspan', '__init__': svg_init})
path = type('path', (tag, Element), {'name': 'path', '__init__': svg_init})
rect = type('rect', (tag, Element), {'name': 'rect', '__init__': svg_init})
stop = type('stop', (tag, Element), {'name': 'stop', '__init__': svg_init})
switch = type('switch', (tag, Element), {'name': 'switch', '__init__': svg_init})
symbol = type('symbol', (tag, Element), {'name': 'symbol', '__init__': svg_init})
text = type('text', (tag, Element), {'name': 'text', '__init__': svg_init})
textPath = type('textPath', (tag, Element), {'name': 'textPath', '__init__': svg_init})
title = type('title', (tag, Element), {'name': 'title', '__init__': svg_init})
use = type('use', (tag, Element), {'name': 'use', '__init__': svg_init})
view = type('view', (tag, Element), {'name': 'view', '__init__': svg_init})

feBlend = type('feBlend', (tag, Element), {'name': 'feBlend', '__init__': svg_init})
feColorMatrix = type('feColorMatrix', (tag, Element), {'name': 'feColorMatrix', '__init__': svg_init})
feComponentTransfer = type('feComponentTransfer', (tag, Element), {'name': 'feComponentTransfer', '__init__': svg_init})
feComposite = type('feComposite', (tag, Element), {'name': 'feComposite', '__init__': svg_init})
feConvolveMatrix = type('feConvolveMatrix', (tag, Element), {'name': 'feConvolveMatrix', '__init__': svg_init})
feDiffuseLighting = type('feDiffuseLighting', (tag, Element), {'name': 'feDiffuseLighting', '__init__': svg_init})
feDisplacementMap = type('feDisplacementMap', (tag, Element), {'name': 'feDisplacementMap', '__init__': svg_init})
feGaussianBlur = type('feGaussianBlur', (tag, Element), {'name': 'feGaussianBlur', '__init__': svg_init})
feImage = type('feImage', (tag, Element), {'name': 'feImage', '__init__': svg_init})
feMerge = type('feMerge', (tag, Element), {'name': 'feMerge', '__init__': svg_init})
feMorphology = type('feMorphology', (tag, Element), {'name': 'feMorphology', '__init__': svg_init})
feOffset = type('feOffset', (tag, Element), {'name': 'feOffset', '__init__': svg_init})
feSpecularLighting = type('feSpecularLighting', (tag, Element), {'name': 'feSpecularLighting', '__init__': svg_init})
feTile = type('feTile', (tag, Element), {'name': 'feTile', '__init__': svg_init})
feTurbulence = type('feTurbulence', (tag, Element), {'name': 'feTurbulence', '__init__': svg_init})
feDistantLight = type('feDistantLight', (tag, Element), {'name': 'feDistantLight', '__init__': svg_init})
fePointLight = type('fePointLight', (tag, Element), {'name': 'fePointLight', '__init__': svg_init})
feSpotLight = type('feSpotLight', (tag, Element), {'name': 'feSpotLight', '__init__': svg_init})

feDropShadow = type('feDropShadow', (tag, Element), {'name': 'feDropShadow', '__init__': svg_init})
discard = type('discard', (tag, Element), {'name': 'discard', '__init__': svg_init})
feDistantLight = type('feDistantLight', (tag, Element), {'name': 'feDistantLight', '__init__': svg_init})
feFlood = type('feFlood', (tag, Element), {'name': 'feFlood', '__init__': svg_init})
feFuncA = type('feFuncA', (tag, Element), {'name': 'feFuncA', '__init__': svg_init})
feFuncB = type('feFuncB', (tag, Element), {'name': 'feFuncB', '__init__': svg_init})
feFuncG = type('feFuncG', (tag, Element), {'name': 'feFuncG', '__init__': svg_init})
feFuncR = type('feFuncR', (tag, Element), {'name': 'feFuncR', '__init__': svg_init})
feMergeNode = type('feMergeNode', (tag, Element), {'name': 'feMergeNode', '__init__': svg_init})
foreignObject = type('foreignObject', (tag, Element), {'name': 'foreignObject', '__init__': svg_init})
unknown = type('unknown', (tag, Element), {'name': 'unknown', '__init__': svg_init})

cursor = type('cursor', (tag, Element), {'name': 'cursor', '__init__': svg_init})
hatchpath = type('hatchpath', (tag, Element), {'name': 'hatchpath', '__init__': svg_init})
altGlyph = type('altGlyph', (tag, Element), {'name': 'altGlyph', '__init__': svg_init})
tref = type('tref', (tag, Element), {'name': 'tref', '__init__': svg_init})
tspan = type('tspan', (tag, Element), {'name': 'tspan', '__init__': svg_init})
altGlyphDef = type('altGlyphDef', (tag, Element), {'name': 'altGlyphDef', '__init__': svg_init})
altGlyphItem = type('altGlyphItem', (tag, Element), {'name': 'altGlyphItem', '__init__': svg_init})
glyph = type('glyph', (tag, Element), {'name': 'glyph', '__init__': svg_init})
glyphRef = type('glyphRef', (tag, Element), {'name': 'glyphRef', '__init__': svg_init})
solidcolor = type('solidcolor', (tag, Element), {'name': 'solidcolor', '__init__': svg_init})
hatch = type('hatch', (tag, Element), {'name': 'hatch', '__init__': svg_init})
font = type('font', (tag, Element), {'name': 'font', '__init__': svg_init})
hkern = type('hkern', (tag, Element), {'name': 'hkern', '__init__': svg_init})
vkern = type('vkern', (tag, Element), {'name': 'vkern', '__init__': svg_init})
animateColor = type('animateColor', (tag, Element), {'name': 'animateColor', '__init__': svg_init})


# TODO --

# _filter # builtin
# _set # builtin

# are these obs or new?
# meshgradient 🗑️?
# mesh 🗑️?
# meshpatch 🗑️?
# meshrow 🗑️?

#  - dashed... may need custom tag after all to handle the dash for full coverage
# TODO - test create dashed tags
# missing-glyph
# color-profile
# font-face
# font-face-format
# font-face-name
# font-face-src
# font-face-uri

# NOTE - already tags in HTML package
# a
# audio
# canvas
# video
# metadata
# script
# style
# iframe
