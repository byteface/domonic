Domonic: DOM
============


createElement
----------------
to create your own elements use the DOM API

.. code-block :: python

	from domonic.dom import *

	site = html()
	el = document.createElement('myelement')
	site.appendChild(el)
	print(site)


addEventlisteners recently been started. There's several more DOM methods. Check code to see what's currently implemented.
