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

Shorthand and longhand
----------------------

Shorthand properties expand to their longhands and reconstruct from them, the
way a browser's CSSOM does.

.. code-block :: python

	from domonic.html import div

	box = div()
	box.style.border = "1px solid red"
	print(box.style.getPropertyValue("border-width"))   # 1px
	print(box.style.getPropertyValue("border-color"))   # red

	box.style.setProperty("margin-top", "10px")
	box.style.setProperty("margin-bottom", "10px")
	box.style.setProperty("margin-left", "10px")
	box.style.setProperty("margin-right", "5px")
	print(box.style.getPropertyValue("margin"))         # 10px 10px 10px 5px
	print(box.style.cssText)                            # margin: 10px 10px 10px 5px;

getComputedStyle
----------------

``window.getComputedStyle(element)`` returns a **read-only** declaration
resolved through a light cascade: matching author rules from
``document.styleSheets`` (by specificity, then source order, with
``!important`` on top), then the inline ``style`` attribute, then inherited
values from the parent, then each property's initial value.

.. code-block :: python

	from domonic import domonic
	from domonic.window import window

	page = domonic.parseString(
	    "<html><head><style>.card{color:red;padding:8px}"
	    "#hero{font-weight:bold}</style></head>"
	    "<body><div id='hero' class='card' style='color:blue'>hi</div></body>"
	)
	hero = page.querySelector("#hero")
	computed = window.getComputedStyle(hero)
	print(computed.getPropertyValue("color"))        # blue  (inline wins)
	print(computed.getPropertyValue("padding-top"))  # 8px   (.card, shorthand expanded)
	print(computed.getPropertyValue("font-weight"))  # bold  (#hero)
	print(computed.getPropertyValue("display"))      # inline (initial value)

stylesheets
-----------

``document.styleSheets`` (DOM spelling) and ``document.stylesheets`` both work.

.. code-block :: python

	from domonic import domonic

	page = domonic.parseString(
	    "<html><head><style>p { color: green }</style></head><body></body></html>"
	)
	sheet = page.styleSheets[0]
	print(sheet.cssRules[0].selectorText)   # p

Related Examples and Guides
---------------------------

- :doc:`../guides/server-side-html`
- :doc:`html`
- `examples/boilerplate.py <https://github.com/byteface/domonic/blob/master/examples/boilerplate.py>`_
- `examples/declarative_shadow_dom.py <https://github.com/byteface/domonic/blob/master/examples/declarative_shadow_dom.py>`_

.. automodule:: domonic.style
    :members:
    :noindex:
