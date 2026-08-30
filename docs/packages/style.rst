styles
===================

.. meta::
   :description: Python CSSOM and style attribute examples for setting inline styles, CSS custom properties, and stylesheet-like data with domonic.
   :keywords: Python CSS, CSSOM, style attribute, inline style, CSS custom properties, server-side HTML styles

domonic supports browser-style inline CSS through the ``style`` attribute and a
CSSOM-like ``CSSStyleDeclaration`` surface.

Styling Elements
----------------

Style properties are converted from JavaScript-style camelCase to CSS property
names when the element renders.

.. code-block :: python

	from domonic.html import div

	mytag = div("hi", _id="test")
	mytag.style.backgroundColor = "black"
	mytag.style.fontSize = "12px"
	print(mytag)
	# <div id="test" style="background-color:black;font-size:12px;">hi</div>

CSS Custom Properties
---------------------

Use ``setProperty`` when the CSS name is not a Python identifier.

.. code-block :: python

	from domonic.html import div

	panel = div("Dashboard")
	panel.style.setProperty("--accent", "#0ea5e9")
	panel.style.setProperty("border-inline-start", "4px solid var(--accent)")

	print(panel)

Read and Remove Styles
----------------------

.. code-block :: python

	from domonic.html import div

	box = div("Status")
	box.style.display = "grid"
	box.style.gap = "0.5rem"

	print(box.style.getPropertyValue("display"))
	box.style.removeProperty("gap")
	print(box)

Style Generated HTML
--------------------

.. code-block :: python

	from domonic.html import article, h2, p

	card = article(h2("Release notes"), p("DOM, Web API, and parser updates."))
	card.style.maxWidth = "42rem"
	card.style.padding = "1rem"
	card.style.border = "1px solid #ddd"

	print(card)

stylesheets
-----------

.. code-block :: python

	from domonic.window import window

	window.location = "https://example.com"
	print(window.document.stylesheets)

.. automodule:: domonic.style
    :members:
    :noindex:
