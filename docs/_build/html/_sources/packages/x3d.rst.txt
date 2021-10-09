x3d
=================

If using x3d you must use 'append' rather than 'html' when adding children 'inline' when templating.

This is because they are 'Nodes' not 'Elements' so won't inherit that custom innerHTML shortcut.

Instead they currently Mixin the 'ParentNode' which grants them 'append' and 'prepend' methods 

See below...

.. code-block :: python

	from domonic.xml.x3d import *

	x3d(_width='500px', _height='400px').append(
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
	)

Alternatively you can just put them directly in the first parameter and move your kwargs to the end.


### aframe

aframe is a simliar library and its tags can be used if you import the js


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
		script(_src=CDN_JS.AFRAME_1_2), # < NOTICE you need to import aframe to use it
		str(_scene)
		)
	)

	render( _webpage, 'hello.html' )



.. automodule:: domonic.xml.x3d
    :members:
    :noindex:


.. automodule:: domonic.xml.aframe
    :members:
    :noindex:
