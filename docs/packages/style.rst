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
	print(computed.getPropertyValue("color"))        # rgb(0, 0, 255)  (inline wins)
	print(computed.getPropertyValue("padding-top"))  # 8px   (.card, shorthand expanded)
	print(computed.getPropertyValue("font-weight"))  # 700   (#hero; keyword -> number)
	print(computed.getPropertyValue("display"))      # inline (initial value)

Like a browser, the computed values are **used values**: colours are reported
as ``rgb()`` / ``rgba()``, ``em`` / ``rem`` / ``pt`` / ``cm`` lengths and
``calc()`` are resolved to ``px`` (against the element's font-size and the
containing block where one can be found without full layout), ``currentColor``
resolves to the element's ``color``, ``font-weight`` keywords become numbers,
an out-of-flow ``display: inline`` blockifies, and ``inherit`` / ``initial`` /
``unset`` are resolved. ``%`` values that need layout, and a ``transform``
list, are reported the browser way too:

.. code-block :: python

	from domonic.dom import document
	from domonic.style import ComputedStyleDeclaration

	outer = document.createElement("div")
	outer.setAttribute("style", "font-size: 20px; width: 400px")
	inner = document.createElement("p")
	inner.setAttribute("style", "margin: 1em; width: 50%; transform: rotate(90deg)")
	outer.appendChild(inner)
	document.createElement("div").appendChild(outer)

	c = ComputedStyleDeclaration(inner)
	c.getPropertyValue("margin")     # 20px       (1em of the 20px font-size)
	c.getPropertyValue("width")      # 200px      (50% of the 400px container)
	c.getPropertyValue("transform")  # matrix(0, 1, -1, 0, 0, 0)

Pass a pseudo-element to read its style: ``window.getComputedStyle(el,
"::before")``.

The cascade understands modern selector specificity: ``:where()`` contributes
zero, ``:is()`` / ``:not()`` / ``:has()`` take the specificity of their most
specific argument, and ``@layer`` order is respected (later layers win, and an
unlayered rule beats any layer).

.. code-block :: python

	page = domonic.parseString(
	    "<html><head><style>"
	    "@layer base, theme;"
	    "@layer theme { p { color: blue } }"
	    "@layer base { p { color: red } }"
	    "</style></head><body><p>hi</p></body>"
	)
	p = page.querySelector("p")
	window.getComputedStyle(p).getPropertyValue("color")   # rgb(0, 0, 255)  (theme layer is later)

CSS custom properties and ``var()``
-----------------------------------

``var()`` references are substituted when computing a value. Custom properties
inherit, so a ``--token`` declared on ``:root`` (or any ancestor, inline or via
a rule) resolves on a descendant.

.. code-block :: python

	from domonic.html import div

	box = div("x", _style="--pad: 12px; padding: var(--pad)")
	window.getComputedStyle(box).getPropertyValue("padding")   # 12px

``CSS.registerProperty()`` registers a custom property with a syntax, an
initial value, and inheritance behaviour, matching the CSS Properties and
Values API.

.. code-block :: python

	from domonic.style import CSS

	CSS.registerProperty({
	    "name": "--brand",
	    "syntax": "<color>",
	    "inherits": True,
	    "initialValue": "rebeccapurple",
	})
	# --brand now resolves to rebeccapurple on any element until overridden

CSS Typed OM
------------

The numeric-value core of CSS Typed OM is available: ``CSSUnitValue`` /
``CSSKeywordValue`` (via ``CSSStyleValue.parse``), the ``CSS.px()`` / ``em()``
/ ``rem()`` / ``percent()`` / ``deg()`` / ``s()`` / ``fr()`` factories, and
``element.attributeStyleMap`` / ``element.computedStyleMap()``.

.. code-block :: python

	from domonic.style import CSS
	from domonic.html import div

	CSS.px(10) + CSS.px(5)          # CSSUnitValue 15px
	CSS.px(96).to("in")            # CSSUnitValue 1in

	el = div(_style="width: 10px")
	el.attributeStyleMap.get("width")        # CSSUnitValue 10px
	el.attributeStyleMap.set("height", CSS.px(20))

constructable stylesheets
-------------------------

``new CSSStyleSheet({media, disabled})`` and ``sheet.replaceSync(cssText)``
build a stylesheet in code; adding it to ``document.adoptedStyleSheets`` (or a
shadow root's) feeds it into ``getComputedStyle``.

.. code-block :: python

	from domonic.dom import Document
	from domonic.style import CSSStyleSheet

	doc = Document()
	sheet = CSSStyleSheet()
	sheet.replaceSync(".hl { color: rebeccapurple }")
	doc.adoptedStyleSheets = [sheet]

media queries
-------------

``window.matchMedia(query)`` evaluates width / height / orientation, the range
syntax (``(width >= 600px)``, ``(400px <= width <= 900px)``), ``resolution``
(from ``window.devicePixelRatio``), and the discrete preference features
(``prefers-color-scheme``, ``prefers-reduced-motion``, ``hover``, ``pointer``,
...). Override a preference for the session via ``window.mediaFeatures``.

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
