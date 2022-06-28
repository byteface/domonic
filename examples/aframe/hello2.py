import sys

sys.path.insert(0, "../..")

from domonic.CDN import *
from domonic.constants.color import *
from domonic.html import *
from domonic.javascript import *
from domonic.xml.aframe import *

_scripts = script(
    """
	//alert('hi world!')
"""
)

spheres = []
for loop in range(1000):
    rand = lambda x: -(x) + Math.random() * (x * 2)
    r = Math.random() * 2
    s = sphere(_position=f"{rand(20)} {rand(20)} {rand(20)}", _radius=f"{r}", _color=Color.random_hex())
    spheres.append(s)

_scene = scene(*spheres, sky(_color=Color.paleskyblue))

_webpage = html(head(), body(script(_src=CDN_JS.AFRAME_1_2), str(_scene), _scripts))

render(_webpage, "hello2.html")
