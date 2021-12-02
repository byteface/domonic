"""
    domonic.svg
    ====================================
    Generate SVG with python 3

    WARNING - totally not tested. except circle. I just assumed it would work...

    # https://www.w3.org/TR/SVG2/eltindex.html

"""

# from domonic.html import tag
from domonic.dom import Element


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
    "image",
    "line",
    "linearGradient",
    "marker",
    "mask",
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


svg = type('svg', (Element,), {'name': 'svg'})

animate = type('animate', (Element,), {'name': 'animate'})
animateMotion = type('animateMotion', (Element,), {'name': 'animateMotion'})
animateTransform = type('animateTransform', (Element,), {'name': 'animateTransform'})
circle = type('circle', (Element,), {'name': 'circle'})
clipPath = type('clipPath', (Element,), {'name': 'clipPath'})
defs = type('defs', (Element,), {'name': 'defs'})
desc = type('desc', (Element,), {'name': 'desc'})
ellipse = type('ellipse', (Element,), {'name': 'ellipse'})
g = type('g', (Element,), {'name': 'g'})
image = type('image', (Element,), {'name': 'image'})
line = type('line', (Element,), {'name': 'line'})
linearGradient = type('linearGradient', (Element,), {'name': 'linearGradient'})
marker = type('marker', (Element,), {'name': 'marker'})
mask = type('mask', (Element,), {'name': 'mask'})
mpath = type('mpath', (Element,), {'name': 'mpath'})
pattern = type('pattern', (Element,), {'name': 'pattern'})
polygon = type('polygon', (Element,), {'name': 'polygon'})
polyline = type('polyline', (Element,), {'name': 'polyline'})
radialGradient = type('radialGradient', (Element,), {'name': 'radialGradient'})

tspan = type('tspan', (Element,), {'name': 'tspan'})
path = type('path', (Element,), {'name': 'path'})
rect = type('rect', (Element,), {'name': 'rect'})
stop = type('stop', (Element,), {'name': 'stop'})
switch = type('switch', (Element,), {'name': 'switch'})
symbol = type('symbol', (Element,), {'name': 'symbol'})
text = type('text', (Element,), {'name': 'text'})
textPath = type('textPath', (Element,), {'name': 'textPath'})
title = type('title', (Element,), {'name': 'title'})
use = type('use', (Element,), {'name': 'use'})
view = type('view', (Element,), {'name': 'view'})

feBlend = type('feBlend', (Element,), {'name': 'feBlend'})
feColorMatrix = type('feColorMatrix', (Element,), {'name': 'feColorMatrix'})
feComponentTransfer = type('feComponentTransfer', (Element,), {'name': 'feComponentTransfer'})
feComposite = type('feComposite', (Element,), {'name': 'feComposite'})
feConvolveMatrix = type('feConvolveMatrix', (Element,), {'name': 'feConvolveMatrix'})
feDiffuseLighting = type('feDiffuseLighting', (Element,), {'name': 'feDiffuseLighting'})
feDisplacementMap = type('feDisplacementMap', (Element,), {'name': 'feDisplacementMap'})
feGaussianBlur = type('feGaussianBlur', (Element,), {'name': 'feGaussianBlur'})
feImage = type('feImage', (Element,), {'name': 'feImage'})
feMerge = type('feMerge', (Element,), {'name': 'feMerge'})
feMorphology = type('feMorphology', (Element,), {'name': 'feMorphology'})
feOffset = type('feOffset', (Element,), {'name': 'feOffset'})
feSpecularLighting = type('feSpecularLighting', (Element,), {'name': 'feSpecularLighting'})
feTile = type('feTile', (Element,), {'name': 'feTile'})
feTurbulence = type('feTurbulence', (Element,), {'name': 'feTurbulence'})
feDistantLight = type('feDistantLight', (Element,), {'name': 'feDistantLight'})
fePointLight = type('fePointLight', (Element,), {'name': 'fePointLight'})
feSpotLight = type('feSpotLight', (Element,), {'name': 'feSpotLight'})

feDropShadow = type('feDropShadow', (Element,), {'name': 'feDropShadow'})
discard = type('discard', (Element,), {'name': 'discard'})
feDistantLight = type('feDistantLight', (Element,), {'name': 'feDistantLight'})
feFlood = type('feFlood', (Element,), {'name': 'feFlood'})
feFuncA = type('feFuncA', (Element,), {'name': 'feFuncA'})
feFuncB = type('feFuncB', (Element,), {'name': 'feFuncB'})
feFuncG = type('feFuncG', (Element,), {'name': 'feFuncG'})
feFuncR = type('feFuncR', (Element,), {'name': 'feFuncR'})
feMergeNode = type('feMergeNode', (Element,), {'name': 'feMergeNode'})
foreignObject = type('foreignObject', (Element,), {'name': 'foreignObject'})
unknown = type('unknown', (Element,), {'name': 'unknown'})

cursor = type('cursor', (Element,), {'name': 'cursor'})
hatchpath = type('hatchpath', (Element,), {'name': 'hatchpath'})
altGlyph = type('altGlyph', (Element,), {'name': 'altGlyph'})
tref = type('tref', (Element,), {'name': 'tref'})
tspan = type('tspan', (Element,), {'name': 'tspan'})
altGlyphDef = type('altGlyphDef', (Element,), {'name': 'altGlyphDef'})
altGlyphItem = type('altGlyphItem', (Element,), {'name': 'altGlyphItem'})
glyph = type('glyph', (Element,), {'name': 'glyph'})
glyphRef = type('glyphRef', (Element,), {'name': 'glyphRef'})
solidcolor = type('solidcolor', (Element,), {'name': 'solidcolor'})
hatch = type('hatch', (Element,), {'name': 'hatch'})
font = type('font', (Element,), {'name': 'font'})
hkern = type('hkern', (Element,), {'name': 'hkern'})
vkern = type('vkern', (Element,), {'name': 'vkern'})
animateColor = type('animateColor', (Element,), {'name': 'animateColor'})

# TODO --
# _filter # builtin
# _set # builtin

# are these obs or new?
# meshgradient 🗑️?
# mesh 🗑️?
# meshpatch 🗑️?
# meshrow 🗑️?

# TODO - just use underscores for these tags?
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
