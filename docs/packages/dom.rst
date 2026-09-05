dom
============

.. meta::
   :description: Python DOM implementation with Document, Node, Element, querySelectorAll, XPath, events, MutationObserver, forms, validation, and server-side DOM manipulation.
   :keywords: Python DOM, Document object model Python, querySelectorAll Python, DOM nodes, MutationObserver Python, server-side DOM, HTML parser

domonic's DOM aims to be useful as an actual platform surface, not just a tree of helper objects.

That is intentional. A Python developer can practise the browser DOM API in
Python: ``createElement()``, ``appendChild()``, ``removeChild()``,
``querySelector()``, ``querySelectorAll()``, ``parentNode``, ``childNodes`` and
``textContent`` are the same concepts used in JavaScript in the browser.

For JavaScript developers, this means domonic DOM code is recognisable even
inside Python. You can parse or generate markup, then keep using familiar
operations such as ``querySelector()``, ``appendChild()``, ``removeChild()``,
``setAttribute()`` and ``dispatchEvent()``.

To use the DOM, either reference your own root ``html`` node or import the global ``document`` from ``domonic.dom``.

.. code-block :: python

	# Access the document via the html tag.
	mydom = html()
	# mydom.getElementbyID...

	# Or import the document global.
	from domonic.dom import document
	# document.createElement...
	print(document)


The last ``html()`` created becomes the active ``document``. You can also set it manually, but it must be a ``Document`` instance. Before an ``html`` class is created, domonic keeps an empty document around so static methods are available.

Remember that Python globals are module-local. Import ``document`` again after creating an ``html`` root if another module or function needs the updated document:

.. code-block :: python

	print(document)
	d = html(body("Hello"))
	print(document)  # no change
	print('body1', d.doctype)
	print('body2', domonic.dom.document.doctype)
	print('body3', document.doctype)
	from domonic.dom import document  # Re-import to get the updated document.
	print('body4', document.doctype)

Notice that before re-importing it was still the previous object.

In most cases, use your own root node directly. The global ``document`` is useful when you need access from a different module.


createElement
----------------
Here's an example of creating your own elements using the DOM API:

.. code-block :: python

	from domonic.html import html
	from domonic.dom import document

	site = html()
	el = document.createElement('myelement')
	site.appendChild(el)
	print(site)
	# <html><myelement></myelement></html>


querySelectorAll
----------------

``querySelectorAll`` and ``querySelector`` are useful for finding elements in the DOM.

These use familiar CSS selector strings, so the same selectors can be reused in
browser JavaScript, tests, scraping scripts, and domonic server-side rendering.

.. code-block :: python

	from domonic import domonic

	mysite = domonic.parseString(
	    '<div>'
	    '<button class="fa-twitter">Follow</button>'
	    '<a href="#services">Services</a>'
	    '<a rel="nofollow" href="https://twitter.com/technology">Twitter</a>'
	    '</div>'
	)

	mysite.querySelectorAll('button')             # [<button class="fa-twitter">]
	mysite.querySelectorAll('.fa-twitter')        # [<button class="fa-twitter">]
	mysite.querySelectorAll("a[rel=nofollow]")            # [<a rel="nofollow" ...>]
	mysite.querySelectorAll("a[href='#services']")        # [<a href="#services">]
	mysite.querySelectorAll("a[href$='technology']")      # [<a rel="nofollow" ...>]

	somelinks = mysite.querySelectorAll("a[href*='twitter']")
	for l in somelinks:
		print(l.href)
	# https://twitter.com/technology

See the examples folder for other uses of the Python virtual DOM.


Serialising: str() vs innerHTML / outerHTML
-------------------------------------------

``str(node)`` produces domonic's authoring-style markup: void elements are
self-closed (``<br/>``), boolean attributes render bare (``checked``), and
``<`` / ``>`` are escaped inside attribute values. This is stable and is what
most server-side rendering wants.

``innerHTML``, ``outerHTML`` and ``getHTML()`` instead follow the WHATWG HTML
fragment serialisation algorithm, so their output is byte-compatible with a
browser: ``<br>`` (no slash), ``checked=""``, and only ``&``, ``"`` and the
non-breaking space escaped in attribute values. Reach for these when a port or
a test diffs against real browser output.

.. code-block :: python

	from domonic.html import div, br, input as input_

	el = div(input_(_type="checkbox", _checked=""), br(), _title="a<b>")

	str(el)
	# <div title="a&lt;b&gt;"><input type="checkbox" checked/><br/></div>

	el.outerHTML
	# <div title="a<b>"><input type="checkbox" checked=""><br></div>

Rendering behaviour of ``str(node)`` is configurable through ``DOMConfig``
(below); the fragment serialisation is not.

``<script>`` / ``<style>`` and the other HTML "raw text" elements are always
serialised verbatim in every one of these forms -- their text content is
never entity-escaped, matching a browser (escaping it would change what the
script actually executes):

.. code-block :: python

	from domonic.dom import DOMParser

	doc = DOMParser().parseFromString(
	    '<html><body><script>if (a && b) x("y");</script></body></html>'
	)
	print(str(doc.body))
	# <body><script>if (a && b) x("y");</script></body>


tagName, nodeName and localName
--------------------------------

Per the DOM spec, an HTML element's ``tagName`` / ``nodeName`` are
upper-cased when the element came from parsing HTML (SVG, MathML, and XML
keep their original case); ``localName`` is always lower-case:

.. code-block :: python

	from domonic import domonic

	page = domonic.parseString("<div><p>hi</p><svg><circle/></svg></div>")
	page.tagName                          # 'DIV'
	page.querySelector("p").tagName       # 'P'
	page.querySelector("p").localName     # 'p'
	page.querySelector("svg").tagName     # 'svg'  (SVG keeps its case)

Elements you build yourself (``div()``, ``document.createElement(...)``) are
not associated with an HTML document the way a parsed tree is, so their
``tagName`` stays lower-case:

.. code-block :: python

	from domonic.html import div

	div().tagName   # 'div'


dataset
-------

``element.dataset`` reflects an element's ``data-*`` attributes both as a
mapping and as JavaScript-style attribute access:

.. code-block :: python

	from domonic.html import div

	el = div()
	el.dataset.userId = "42"       # same as el.setAttribute("data-user-id", "42")
	print(el)                      # <div data-user-id="42"></div>
	print(el.dataset.userId)       # '42'
	print(el.dataset["userId"])    # '42'
	print(el.dataset.missing)      # None (JS: undefined)


DOMConfig
----------------

``DOMConfig`` controls rendering options on the DOM.

For example, here we set several flags away from their defaults:

.. code-block :: python

	from domonic.html import *
	from domonic.dom import DOMConfig
	DOMConfig.GLOBAL_AUTOESCAPE = True
	DOMConfig.HTMX_ENABLED = True
	DOMConfig.RENDER_OPTIONAL_CLOSING_TAGS = False
	print(html(head(),body(div(h1('heading'),div(button('hi & hack',_get='/get_hi'))))))
	# <html><head><body><div><h1>heading</h1><div><button data-hx-get="/get_hi">hi &amp; hack</button></div></div>

When ``DOMConfig.HTMX_ENABLED`` is set (as above), domonic maps HTMX-style
shortcut attributes to the configurable ``data-hx-`` secondary prefix
recognised by HTMX -- the rest of the examples on this page assume it stays
set:

.. code-block :: python

	button(
	    "Save",
	    _post="/items",
	    _target="#items",
	    _swap_oob=True,
	    **{"_on:click": "this.classList.add('busy')"},
	)
	# <button data-hx-post="/items" data-hx-target="#items" data-hx-swap-oob="true" data-hx-on:click="this.classList.add('busy')">Save</button>

HTMX 4 explicit inheritance can be written with the literal attribute spelling
or with ``__inherited`` as a Python-friendly suffix:

.. code-block :: python

	div(_confirm__inherited="Are you sure?", _headers__inherited='{"X-CSRF": "token"}')
	# <div data-hx-confirm:inherited="Are you sure?" data-hx-headers:inherited="{&quot;X-CSRF&quot;: &quot;token&quot;}"></div>

HTMX 4 attributes and popular extension attributes are available as shortcuts,
including ``_query``, ``_pending``, ``_status``, ``_ignore``, ``_morph_skip``,
``_morph_skip_children``, ``_preload``, ``_live``, ``_optimistic``,
``_targets``, ``_download``, and ``_multipart``.

``<hx-partial>`` responses can be generated with ``hx_partial``:

.. code-block :: python

	hx_partial(div("New message"), **{"_hx-target": "#messages", "_hx-swap": "beforeend"})
	# <hx-partial hx-target="#messages" hx-swap="beforeend"><div>New message</div></hx-partial>

Raw HTMX attributes can still be emitted by spelling the attribute explicitly:

.. code-block :: python

	button("Load", **{"_hx-get": "/items"})
	# <button hx-get="/items">Load</button>

Legacy SSE and WebSocket extension spellings are still supported for existing
HTMX 2 integrations:

.. code-block :: python

	div(_ext="sse", _sse_connect="/events", _sse_swap="message")
	# <div data-hx-ext="sse" sse-connect="/events" sse-swap="message"></div>

ValidityState
----------------

Form controls expose ``validity``, ``validationMessage``, ``willValidate``,
``checkValidity()``, ``reportValidity()``, and ``setCustomValidity()`` for
server-side constraint checks.

.. code-block :: python

	from domonic.html import input

	email = input(_type="email", _required=True, _value="not-an-email")
	print(email.validity.typeMismatch)
	# True
	print(email.validationMessage)
	# Please enter a valid value.


Render Caching
----------------

``DOMConfig.RENDER_CACHE_ENABLED`` caches ``str(node)``'s rendered output per
node. It is off by default -- turning it on is a pure opt-in with no other
behaviour change.

.. code-block :: python

	from domonic.html import div, p
	from domonic.dom import DOMConfig

	DOMConfig.RENDER_CACHE_ENABLED = True

	page = div(p("hello", _class="intro"))
	first = str(page)   # walks the tree and renders, as normal
	second = str(page)  # returns the cached string -- no re-render

The cache is invalidated automatically by the same mutation tracking
``MutationObserver`` already relies on, so ``appendChild()``,
``removeChild()``, ``setAttribute()``, ``textContent`` assignment and
``.style`` changes anywhere in the subtree all correctly force a fresh
render on the next ``str()`` call:

.. code-block :: python

	page.querySelector("p").setAttribute("id", "x")
	print(str(page))
	# <div><p class="intro" id="x">hello</p></div>

A change to a rendering-relevant ``DOMConfig`` flag (``GLOBAL_AUTOESCAPE``,
``RENDER_OPTIONAL_CLOSING_TAGS``, ``HTMX_ENABLED``, ``ALPINE_ENABLED``,
``ATTRIBUTE_QUOTES``, ...) also invalidates every cached render, even with no
tree mutation at all, since it changes what the *same* tree should render as.

This is a real win specifically for **read-heavy, write-light** trees --
something rendered many times between occasional changes (a cached page, a
dashboard, a report). It does not speed up a mutate-then-render-immediately
pattern: any change still costs a full render on the next ``str()`` call,
the same as with the flag off.


DOMMatrix
----------------

``DOMMatrix`` / ``DOMPoint`` / ``DOMRect`` implement the CSS/SVG geometry
interfaces: 2D and 3D affine transforms, composition, inversion, and
transforming points. Composition follows the spec's post-multiply rule --
``a.multiplySelf(b)`` (and chaining ``a.translateSelf(...).rotateSelf(...)``)
transforms a point as ``a.transformPoint(b.transformPoint(p))``, so the
*last*-chained operation is the one applied to the point first:

.. code-block :: python

	from domonic.dom import DOMMatrix, DOMPoint

	m = DOMMatrix().translateSelf(10, 0).rotateSelf(90)
	print(m.toString())
	# matrix(0, 1, -1, 0, 10, 0)

	p = m.transformPoint(DOMPoint(1, 0))
	print(p.x, p.y)
	# 10.0 1.0  (rotate is applied first, then the translate)

``getComputedStyle(el).getPropertyValue("transform")`` uses the same matrix
type, composing a CSS ``transform`` list the way a browser does -- see
:doc:`style`.


The full list of available DOM methods are listed below...


.. automodule:: domonic.dom
    :members:
    :noindex:

.. automodule:: domonic.events
    :members:
    :noindex:
