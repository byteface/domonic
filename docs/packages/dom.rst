dom
============

domonic's DOM aims to be useful as an actual platform surface, not just a tree of helper objects.

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

	from domonic.dom import *
	from domonic.dom import document

	site = html()
	el = document.createElement('myelement')
	site.appendChild(el)
	print(site)


querySelectorAll
----------------

``querySelectorAll`` and ``querySelector`` are useful for finding elements in the DOM.

.. code-block :: python

	mysite.querySelectorAll('button')
	mysite.querySelectorAll('.fa-twitter')
	mysite.querySelectorAll("a[rel=nofollow]")
	mysite.querySelectorAll("a[href='#services']")
	mysite.querySelectorAll("a[href$='technology']")

	somelinks = mysite.querySelectorAll("a[href*='twitter']")
	for l in somelinks:
		print(l.href)

See the examples folder for other uses of the Python virtual DOM.



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
	# <html><head></head><body><div><h1>heading</h1><div><button data-hx-get="/get_hi">hi & hack</button></div></div></body></html>

When ``HTMX_ENABLED`` is set, domonic maps HTMX-style shortcut attributes to
the configurable ``data-hx-`` secondary prefix recognised by HTMX:

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
	# <div data-hx-confirm:inherited="Are you sure?" data-hx-headers:inherited="{"X-CSRF": "token"}"></div>

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
	print(email.validationMessage)


The full list of available DOM methods are listed below...


.. automodule:: domonic.dom
    :members:
    :noindex:

.. automodule:: domonic.events
    :members:
    :noindex:
