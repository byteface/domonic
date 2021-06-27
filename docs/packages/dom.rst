Domonic: DOM
============

The DOM is gradually evolving...


createElement
----------------
Here's an exmaple of creating your own elements using the DOM API

.. code-block :: python

	from domonic.dom import *

	site = html()
	el = document.createElement('myelement')
	site.appendChild(el)
	print(site)



See the examples folder for other uses of a python virtual DOM.

A full list of available methods are below...


.. automodule:: domonic.dom
    :members:
    :noindex:

.. automodule:: domonic.events
    :members:
    :noindex: