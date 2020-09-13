"""
    domonic.svg
    ====================================
    Generate SVG with python 3

    WARNING - totally not tested. except circle. I just assumed it would work...

    # https://www.w3.org/TR/SVG2/eltindex.html

"""

from domonic.html import tag
from domonic.dom import Node


def svg_init(self, *args, **kwargs):
    tag.__init__(self, *args, **kwargs)
    Node.__init__(self, *args, **kwargs)


svg = type('svg', (tag, Node), {'name': 'svg', '__init__': svg_init})

animate = type('animate', (tag, Node), {'name': 'animate', '__init__': svg_init})
animateMotion = type('animateMotion', (tag, Node), {'name': 'animateMotion', '__init__': svg_init})
animateTransform = type('animateTransform', (tag, Node), {'name': 'animateTransform', '__init__': svg_init})
circle = type('circle', (tag, Node), {'name': 'circle', '__init__': svg_init})
clipPath = type('clipPath', (tag, Node), {'name': 'clipPath', '__init__': svg_init})
defs = type('defs', (tag, Node), {'name': 'defs', '__init__': svg_init})
desc = type('desc', (tag, Node), {'name': 'desc', '__init__': svg_init})
ellipse = type('ellipse', (tag, Node), {'name': 'ellipse', '__init__': svg_init})
g = type('g', (tag, Node), {'name': 'g', '__init__': svg_init})
image = type('image', (tag, Node), {'name': 'image', '__init__': svg_init})
line = type('line', (tag, Node), {'name': 'line', '__init__': svg_init})
linearGradient = type('linearGradient', (tag, Node), {'name': 'linearGradient', '__init__': svg_init})
marker = type('marker', (tag, Node), {'name': 'marker', '__init__': svg_init})
mask = type('mask', (tag, Node), {'name': 'mask', '__init__': svg_init})
mpath = type('mpath', (tag, Node), {'name': 'mpath', '__init__': svg_init})
pattern = type('pattern', (tag, Node), {'name': 'pattern', '__init__': svg_init})
polygon = type('polygon', (tag, Node), {'name': 'polygon', '__init__': svg_init})
polyline = type('polyline', (tag, Node), {'name': 'polyline', '__init__': svg_init})
radialGradient = type('radialGradient', (tag, Node), {'name': 'radialGradient', '__init__': svg_init})

tspan = type('tspan', (tag, Node), {'name': 'tspan', '__init__': svg_init})
path = type('path', (tag, Node), {'name': 'path', '__init__': svg_init})
rect = type('rect', (tag, Node), {'name': 'rect', '__init__': svg_init})
stop = type('stop', (tag, Node), {'name': 'stop', '__init__': svg_init})
switch = type('switch', (tag, Node), {'name': 'switch', '__init__': svg_init})
symbol = type('symbol', (tag, Node), {'name': 'symbol', '__init__': svg_init})
text = type('text', (tag, Node), {'name': 'text', '__init__': svg_init})
textPath = type('textPath', (tag, Node), {'name': 'textPath', '__init__': svg_init})
title = type('title', (tag, Node), {'name': 'title', '__init__': svg_init})
use = type('use', (tag, Node), {'name': 'use', '__init__': svg_init})
view = type('view', (tag, Node), {'name': 'view', '__init__': svg_init})

feBlend = type('feBlend', (tag, Node), {'name': 'feBlend', '__init__': svg_init})
feColorMatrix = type('feColorMatrix', (tag, Node), {'name': 'feColorMatrix', '__init__': svg_init})
feComponentTransfer = type('feComponentTransfer', (tag, Node), {'name': 'feComponentTransfer', '__init__': svg_init})
feComposite = type('feComposite', (tag, Node), {'name': 'feComposite', '__init__': svg_init})
feConvolveMatrix = type('feConvolveMatrix', (tag, Node), {'name': 'feConvolveMatrix', '__init__': svg_init})
feDiffuseLighting = type('feDiffuseLighting', (tag, Node), {'name': 'feDiffuseLighting', '__init__': svg_init})
feDisplacementMap = type('feDisplacementMap', (tag, Node), {'name': 'feDisplacementMap', '__init__': svg_init})
feGaussianBlur = type('feGaussianBlur', (tag, Node), {'name': 'feGaussianBlur', '__init__': svg_init})
feImage = type('feImage', (tag, Node), {'name': 'feImage', '__init__': svg_init})
feMerge = type('feMerge', (tag, Node), {'name': 'feMerge', '__init__': svg_init})
feMorphology = type('feMorphology', (tag, Node), {'name': 'feMorphology', '__init__': svg_init})
feOffset = type('feOffset', (tag, Node), {'name': 'feOffset', '__init__': svg_init})
feSpecularLighting = type('feSpecularLighting', (tag, Node), {'name': 'feSpecularLighting', '__init__': svg_init})
feTile = type('feTile', (tag, Node), {'name': 'feTile', '__init__': svg_init})
feTurbulence = type('feTurbulence', (tag, Node), {'name': 'feTurbulence', '__init__': svg_init})
feDistantLight = type('feDistantLight', (tag, Node), {'name': 'feDistantLight', '__init__': svg_init})
fePointLight = type('fePointLight', (tag, Node), {'name': 'fePointLight', '__init__': svg_init})
feSpotLight = type('feSpotLight', (tag, Node), {'name': 'feSpotLight', '__init__': svg_init})

feDropShadow = type('feDropShadow', (tag, Node), {'name': 'feDropShadow', '__init__': svg_init})
discard = type('discard', (tag, Node), {'name': 'discard', '__init__': svg_init})
feDistantLight = type('feDistantLight', (tag, Node), {'name': 'feDistantLight', '__init__': svg_init})
feFlood = type('feFlood', (tag, Node), {'name': 'feFlood', '__init__': svg_init})
feFuncA = type('feFuncA', (tag, Node), {'name': 'feFuncA', '__init__': svg_init})
feFuncB = type('feFuncB', (tag, Node), {'name': 'feFuncB', '__init__': svg_init})
feFuncG = type('feFuncG', (tag, Node), {'name': 'feFuncG', '__init__': svg_init})
feFuncR = type('feFuncR', (tag, Node), {'name': 'feFuncR', '__init__': svg_init})
feMergeNode = type('feMergeNode', (tag, Node), {'name': 'feMergeNode', '__init__': svg_init})
foreignObject = type('foreignObject', (tag, Node), {'name': 'foreignObject', '__init__': svg_init})
unknown = type('unknown', (tag, Node), {'name': 'unknown', '__init__': svg_init})

cursor = type('cursor', (tag, Node), {'name': 'cursor', '__init__': svg_init})
hatchpath = type('hatchpath', (tag, Node), {'name': 'hatchpath', '__init__': svg_init})
altGlyph = type('altGlyph', (tag, Node), {'name': 'altGlyph', '__init__': svg_init})
tref = type('tref', (tag, Node), {'name': 'tref', '__init__': svg_init})
tspan = type('tspan', (tag, Node), {'name': 'tspan', '__init__': svg_init})
altGlyphDef = type('altGlyphDef', (tag, Node), {'name': 'altGlyphDef', '__init__': svg_init})
altGlyphItem = type('altGlyphItem', (tag, Node), {'name': 'altGlyphItem', '__init__': svg_init})
glyph = type('glyph', (tag, Node), {'name': 'glyph', '__init__': svg_init})
glyphRef = type('glyphRef', (tag, Node), {'name': 'glyphRef', '__init__': svg_init})
solidcolor = type('solidcolor', (tag, Node), {'name': 'solidcolor', '__init__': svg_init})
hatch = type('hatch', (tag, Node), {'name': 'hatch', '__init__': svg_init})
font = type('font', (tag, Node), {'name': 'font', '__init__': svg_init})
hkern = type('hkern', (tag, Node), {'name': 'hkern', '__init__': svg_init})
vkern = type('vkern', (tag, Node), {'name': 'vkern', '__init__': svg_init})
animateColor = type('animateColor', (tag, Node), {'name': 'animateColor', '__init__': svg_init})

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
