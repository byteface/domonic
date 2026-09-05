x3d
=================

.. meta::
   :description: Generate X3D and A-Frame scenes with Python, including 3D shapes, routes, interpolators, WebVR-style markup, and domonic XML tags.
   :keywords: Python X3D, A-Frame Python, 3D HTML, WebVR Python, X3DOM, generate 3D scene, XML 3D

When using X3D, use ``append`` rather than ``html`` when adding children inline while templating.

This is because they are nodes, not HTML elements, so they do not inherit the custom ``innerHTML`` shortcut.

Instead they currently mix in ``ParentNode``, which provides ``append`` and ``prepend`` methods.

For example:

.. code-block :: python

	from domonic.xml.x3d import *

	print(x3d(_width='500px', _height='400px').append(
		scene(
	        transform(_DEF="ball").append(
		        shape(
		            appearance(
		                material(_diffuseColor='1 0 0')
		            ),
		            sphere()
		        )
	        ),
	    	timeSensor(_DEF="time", _cycleInterval="2", _loop="true"),
	    	PositionInterpolator(_DEF="move", _key="0 0.5 1", _keyValue="0 0 0  0 3 0  0 0 0"),
	    	Route(_fromNode="time", _fromField ="fraction_changed", _toNode="move", _toField="set_fraction"),
	    	Route(_fromNode="move", _fromField ="value_changed", _toNode="ball", _toField="translation")
	    )
	))
	# <x3d width="500px" height="400px"><scene><transform DEF="ball"><shape><appearance><material diffuseColor="1 0 0"></material></appearance><sphere></sphere></shape></transform><timeSensor DEF="time" cycleInterval="2" loop="true"></timeSensor><PositionInterpolator DEF="move" key="0 0.5 1" keyValue="0 0 0  0 3 0  0 0 0"></PositionInterpolator><Route fromNode="time" fromField="fraction_changed" toNode="move" toField="set_fraction"></Route><Route fromNode="move" fromField="value_changed" toNode="ball" toField="translation"></Route></scene></x3d>

Alternatively, put them directly in the first parameter and move keyword arguments to the end.


A-Frame
----------------

A-Frame is similar, and its tags can be used if you import the JavaScript runtime.


.. code-block :: python

	from domonic.html import *
	from domonic.xml.aframe import *
	from domonic.CDN import *

	_scene = scene(
		box(_position="-1 0.5 -3", _rotation="0 45 0", _color="#4CC3D9"),
		sphere(_position="0 1.25 -5", _radius="1.25", _color="#EF2D5E"),
		cylinder(_position="1 0.75 -3", _radius="0.5", _height="1.5", _color="#FFC65D"),
		plane(_position="0 0 -4", _rotation="-90 0 0", _width="4", _height="4", _color="#7BC8A4"),
		sky(_color="#ECECEC")
		)

	_webpage = html(head(),body(
		script(_src=CDN_JS.AFRAME), # Import A-Frame before using the scene.
		str(_scene)
		)
	)

	render( _webpage, 'hello.html' )
	# writes hello.html:
	# <html><head></head><body><script src="https://cdn.jsdelivr.net/npm/aframe@1.8.0/dist/aframe-v1.8.0.min.js"></script><a-scene><box position="-1 0.5 -3" rotation="0 45 0" color="#4CC3D9"></box><sphere position="0 1.25 -5" radius="1.25" color="#EF2D5E"></sphere><cylinder position="1 0.75 -3" radius="0.5" height="1.5" color="#FFC65D"></cylinder><plane position="0 0 -4" rotation="-90 0 0" width="4" height="4" color="#7BC8A4"></plane><sky color="#ECECEC"></sky></a-scene></body></html>



.. automodule:: domonic.xml.x3d
    :members:
    :noindex:


.. automodule:: domonic.xml.aframe
    :members:
    :noindex:
