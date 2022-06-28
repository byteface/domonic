import sys

sys.path.insert(0, "../..")

import os

from domonic.CDN import *
from domonic.html import *
from domonic.xml.aframe import *

_scripts = script(
    """
	//alert('yo world!')
"""
)

_scene = scene(
    box(_position="-1 0.5 -3", _rotation="0 45 0", _color="#4CC3D9"),
    sphere(_position="0 1.25 -5", _radius="1.25", _color="#EF2D5E"),
    cylinder(_position="1 0.75 -3", _radius="0.5", _height="1.5", _color="#FFC65D"),
    plane(_position="0 0 -4", _rotation="-90 0 0", _width="4", _height="4", _color="#7BC8A4"),
    sky(_color="#ECECEC"),
)

_webpage = html(
    head(),
    body(
        link(_rel="stylesheet", _type="text/css", _href=CDN_CSS.MARX),
        script(_src=CDN_JS.AFRAME_1_2),
        str(_scene),
        _scripts,
    ),
)

render(_webpage, "hello.html")
