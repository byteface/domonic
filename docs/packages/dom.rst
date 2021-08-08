Domonic: DOM
============

The DOM is gradually evolving...


createElement
----------------
Here's an exmaple of creating your own elements using the DOM API

.. code-block :: python

	from domonic.dom import *
	from domonic.dom import document

	site = html()
	el = document.createElement('myelement')
	site.appendChild(el)
	print(site)


querySelectorAll
----------------
NOTE ... (this still in dev.)

.. code-block :: python

	mysite.querySelectorAll('button')  # *note - still in dev. use getElementsBySelector for more complex selectors
	# mysite.getElementsBySelector


To use the DOM either reference your root 'html' node or import the dom modules global 'document'

.. code-block :: python

	# access the document via the html tag
	mydom = html()
	# mydom.getElementbyID...

	# or by importing the document global
	from domonic.dom import document
	# document.createElement...
	print(document)


The last 'html()' you created will always be the 'document'. You can also set it manually but it needs to ne a Document instance. 
Before a 'html' class is created there is an empty document so that static methods can be available.

*a note on globals*
Remember python globals are only to that module (unlike other langs). So you will have to import document explicitly when you need it (per method call)

See the examples folder for other uses of a python virtual DOM.


The full list of available DOM methods are listed below...


.. automodule:: domonic.dom
    :members:
    :noindex:

.. automodule:: domonic.events
    :members:
    :noindex: