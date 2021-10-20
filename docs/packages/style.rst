styles
===================

domonic supports the style attribute.

Styling Elements
----------------

Styling gets passed to the style tag on render.

.. code-block :: python

	mytag = div("hi", _id="test")
	mytag.style.backgroundColor = "black"
	mytag.style.fontSize = "12px"
	print(mytag)
	# <div id="test" style="background-color:black;font-size:12px;">hi</div>


CSSOM is also stubbed out. See the styles.py class. Feel free to make a PR


.. automodule:: domonic.style
    :members:
    :noindex:
