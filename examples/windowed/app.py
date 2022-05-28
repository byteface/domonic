# -*- coding: utf-8 -*-

import sys

sys.path.insert(0, "../..")

from domonic import *
from domonic.html import *
from domonic.dQuery import º
from domonic.components import Input

# create some vars to pass into the templates
APPNAME = "pixl"

# TOOLBAR_COLUMNS = 1

# https://materialdesignicons.com/

# wand
# crop
# slice : mdi-box-cutter,
# airbrush
# rubber stamp
# history brush
# blur
# dodge
# path
# "marquee" : mdi-select
# "wand" :
# "notes" :
# "move" : "mdi-arrow-all",
# bg/fg color
# stroke/fill color
# bw / reset / swap / no-color
# size, shape
# pressure, tilt
# snap to grid

tools = {
    "selection": "mdi-cursor-default",
    "subselection": "mdi-cursor-default-outline",
    "transform": "mdi-vector-square",
    "lasso": "mdi-lasso",
    "pen": "mdi-fountain-pen-tip",
    "text": "mdi-format-text",
    "line": "mdi-vector-line",
    "rectangle": "mdi-rectangle-outline",
    "pencil": "mdi-pencil",
    "brush": "mdi-brush",
    "ink": "mdi-feather",
    "bucket": "mdi-format-paint",
    "eyedropper": "mdi-eyedropper",
    "eraser": "mdi-eraser",
    "hand": "mdi-hand-left",
    "zoom": "mdi-magnify",
}

# render the toolbars
render(domonic.loads("templates/toolbar.pyml", tools=tools, APPNAME=APPNAME), "toolbar.html")

# render a panel
render(domonic.loads("templates/panel.pyml", somedata={}, APPNAME=APPNAME), "panel.html")

# create the main page
render(domonic.loads("templates/index.pyml", tools=tools, APPNAME=APPNAME), "index.html")


try:
    import os
    import webbrowser

    webbrowser.open("file://" + os.path.realpath(".") + "/index.html")
except Exception as e:
    print("view index.html in the browser")
    pass
