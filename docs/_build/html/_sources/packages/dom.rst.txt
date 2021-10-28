dom
============

The DOM is gradually evolving...

To use the DOM either reference your root 'html' node or import the dom modules global 'document'

.. code-block :: python

	# access the document via the html tag
	mydom = html()
	# mydom.getElementbyID...

	# or by importing the document global
	from domonic.dom import document
	# document.createElement...
	print(document)


The last 'html()' created will always be the 'document'. You can set it manually but it needs to be a Document instance. Before a 'html' class is created it is just an empty document so that static methods can be available.

Remember python globals are only to that module (unlike other langs). so you will have to import document explicitly when you need it (per method call after setting it). i.e

.. code-block :: python

	print(document)
	d = html(body("Hello"))
	print(document)  # no change
	print('body1', d.doctype)
	print('body2', domonic.dom.document.doctype)
	print('body3', document.doctype)
	from domonic.dom import document  # re-import to get the updated document
	print('body4', document.doctype)

notice how before it was imported it was still just a class not an instance.

So in most cases just use your own root node and not document as it will be the only one that will be updated unless you import after any html node creation. The global is for when you need to access the document from a different module(file)


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

querySelectorAll and querySelector are useful for finding elements in the DOM.

.. code-block :: python

	mysite.querySelectorAll('button')
	mysite.querySelectorAll('.fa-twitter')
	mysite.querySelectorAll("a[rel=nofollow]")
	mysite.querySelectorAll("a[href='#services']")
	mysite.querySelectorAll("a[href$='technology']")

	somelinks = mysite.querySelectorAll("a[href*='twitter']")
	for l in somelinks:
		print(l.href)


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