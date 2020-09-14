Domonic: x3d
=================

If using x3d you must use 'append' rather than 'html' when adding children 'inline' when templating.

This is because they are 'Nodes' not 'Elements' so won't inherit that custom innerHTML shortcut.

Instead they currently Mixin the 'ParentNode' which grants them 'append' and 'prepend' methods 

See below...

.. code-block :: python

	from domonic.x3d import *

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


.. automodule:: domonic.x3d
    :members:
    :noindex:

