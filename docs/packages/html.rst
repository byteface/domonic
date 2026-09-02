html
=============

.. meta::
   :description: Generate HTML with Python using domonic tags, attributes, templates, parsers, htmx attributes, import maps, forms, and server-side rendering.
   :keywords: Python HTML generator, HTML tags Python, server-side rendering Python, htmx Python, parse HTML Python, PyML, static site generator

With domonic, you can create clean ``<html>`` straight out of the box.

The API is designed to teach and reuse real HTML vocabulary. Tags are Python
classes named after HTML elements, so learning ``div()``, ``section()``,
``article()``, ``form()``, ``input()`` and ``button()`` in domonic also teaches
the names you will see in browser markup.

.. code-block :: python
    
    mydom = html(body(h1('Hello, World!')))
    print(f"{mydom}")


.. code-block :: html

    <!DOCTYPE html>
    <html>
        <body>
            <h1>Hello, World!</h1>
        </body>
    </html>


rendering
----------------

Cast ``str()`` on any element to render it.

.. code-block :: python

    el_string = str(div())
    print(el_string)


There is also a ``render`` method that takes PyML and an optional output file.

.. code-block :: python
    
    from domonic.html import *

    page = div(span('Hello World'))
    render(page, 'index.html')

For large responses or reports, every node also has ``stream()``. It yields
HTML chunks on demand, while ``str(node)`` remains equivalent to
``"".join(node.stream())``.

.. code-block :: python

    from fastapi.responses import StreamingResponse
    from domonic.html import body, html, table, td, tr

    def rows():
        for index in range(50000):
            yield tr(td(f"Row {index}"), td(f"Data {index}"))

    page = html(body(table(rows())))

    # ASGI frameworks can send the first chunks before every row is rendered.
    response = StreamingResponse(page.stream(), media_type="text/html")

Write streamed output directly to disk when building large static files:

.. code-block :: python

    with open("report.html", "w") as f:
        for chunk in page.stream():
            f.write(chunk)

Benchmark streaming memory locally:

.. code-block :: bash

    python scripts/benchmark_streaming.py --rows 10000 --iterations 5


templating
----------------

.. code-block :: python

  from domonic.html import *

    output = render( 
        html(
            head(
                style(),
                script(),
            ),
            body(
                div("hello world"),
                a("this is a link", _href="http://www.somesite.com", _style="font-size:10px;"),
                ol(''.join([f'{li()}' for thing in range(5)])),
                h1("test", _class="test"),
            )
        )
    )

.. code-block :: html

  <html><head><style></style><script></script></head><body><div>hello world</div><a href="http://www.somesite.com" style="font-size:10px;">this is a link</a><ol><li></li><li></li><li></li><li></li><li></li></ol><h1 class="test">test</h1></body></html>


Take a look in tests/test_html.py at the bootstrap5 alpha examples. All tests passed on several templates.


usage
----------------

.. code-block :: python

    print(html(body(h1('Hello, World!'))))

.. code-block :: html

	<html><body><h1>Hello, World!</h1></body></html>


attributes
----------------
Prepend attributes with an underscore to avoid clashing with Python keywords.

The rendered output is normal HTML, so the attribute names you use here are the
same ones you will inspect in browser developer tools.

.. code-block :: python

	test = label(_class='classname', _for="someinput")
	print(test)

.. code-block :: html

	<label class="classname" for="someinput"></label>


lists
----------------
Use a list comprehension and join it to strip the square brackets.

.. code-block :: python

	ul(''.join([f'{li()}' for thing in range(5)])),

.. code-block :: html

	<ul><li></li><li></li><li></li><li></li></ul>


data-tags
----------------
Python does not allow hyphens in parameter names, so use variable keyword argument syntax for custom data attributes.

.. code-block :: python

	div("test", **{"_data-test":"test"} )

Remember to prepend the underscore.


script tags
----------------

Load from a source:

.. code-block :: python

	script(_src="/docs/5.0/dist/js/bootstrap.bundle.min.js", _integrity="sha384-1234", _crossorigin="anonymous"),

Or use inline JavaScript:

.. code-block :: python

	script("""
    let itbe = ""
    """),


style tags
----------------

Load from a source:

.. code-block :: python

	link(_href="/docs/5.0/dist/css/bootstrap.min.css", _rel="stylesheet", __integrity="sha384-12345", __crossorigin="anonymous"),

Or use inline CSS:

.. code-block :: python

    style("""
    .bd-placeholder-img {
        font-size: 1.125rem;
        text-anchor: middle;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
    }
    @media (min-width: 768px) {
    .bd-placeholder-img-lg {
        font-size: 3.5rem;
    }
    }
    """),


Create Elements
----------------

To create your own custom elements, use ``create_element``.

.. code-block :: python

    from domonic.html import *
    create_element('custom_el', div('some content'), _id="test")

Custom element names can include hyphens, which makes them useful for emitting
web-component style markup.

.. code-block :: python

    from domonic.html import *

    card = create_element(
        "profile-card",
        template(
            style(".card { border: 1px solid #ccc; padding: 1rem; }"),
            article(slot(_name="name"), slot(), _class="card"),
            _shadowrootmode="open",
        ),
        strong("byteface", _slot="name"),
        "Server-rendered Declarative Shadow DOM.",
    )

    print(card)

.. code-block :: html

    <profile-card><template shadowrootmode="open"><style>.card { border: 1px solid #ccc; padding: 1rem; }</style><article class="card"><slot name="name"></slot><slot></slot></article></template><strong slot="name">byteface</strong>Server-rendered Declarative Shadow DOM.</profile-card>

See ``examples/declarative_shadow_dom.py`` for a complete page.


You can also use the DOM API:

.. code-block :: python

	from domonic.dom import *
	from domonic.html import *

	site = html()
	el = document.createElement('myelement')
	site.appendChild(el)
	print(site)


For more information about the DOM API, navigate to the DOM section.


Custom Elements Registry
--------------------------------

``window.customElements`` implements the ``CustomElementRegistry`` API. Register
a class, then ``createElement`` and the HTML parsers return upgraded instances
and run the lifecycle callbacks (``connectedCallback``,
``disconnectedCallback``, ``attributeChangedCallback`` for names listed in
``observedAttributes``, and ``adoptedCallback``).

.. code-block :: python

    from domonic.dom import Document, HTMLElement
    from domonic.window import window

    class WordCount(HTMLElement):
        observedAttributes = ("for",)

        def connectedCallback(self):
            self.textContent = "0 words"

        def attributeChangedCallback(self, name, old, new):
            ...

    window.customElements.define("word-count", WordCount)

    doc = Document()
    el = doc.createElement("word-count")        # -> WordCount instance

    from domonic import domonic
    page = domonic.parseString("<word-count></word-count>")  # also upgrades

``customElements.get()``, ``customElements.getName()`` and
``customElements.whenDefined()`` (which returns a ``Promise``) are available,
and ``customElements.upgrade(root)`` upgrades an already-built subtree.

**Customized built-in elements** are supported through the ``is`` attribute.
Pass ``{"extends": "<tag>"}`` when defining, then create the host element with
``is_=``, ``**{"is": ...}``, or the ``createElement(tag, options)`` dict form:

.. code-block :: python

    class FancyButton(HTMLElement):
        def connectedCallback(self):
            self.classList.add("fancy")

    window.customElements.define("fancy-button", FancyButton, {"extends": "button"})

    doc.createElement("button", is_="fancy-button")        # -> FancyButton
    doc.createElement("button", {"is": "fancy-button"})    # DOM options form
    # <button is="fancy-button"> in parsed HTML upgrades too

**Shadow DOM.** ``element.attachShadow({"mode": "open"})`` returns a
``ShadowRoot``; ``<slot>`` elements expose ``assignedNodes()`` /
``assignedElements()`` and fire ``slotchange``. For server-side rendering, emit
Declarative Shadow DOM with a ``<template shadowrootmode="open">`` child (see the
``profile-card`` example above).


Decorators
--------------------------------

You can use decorators to wrap elements around function results.

.. code-block :: python

	from domonic.decorators import el

	@el(html)
	@el(body)
	@el(div)
	def test():
		return 'hi!'

	print(test())
	# <html><body><div>hi!</div></body></html>


Magic methods
--------------------------------

**Multiply**

You can quickly clone nodes with a multiplier which will return a list...

.. code-block :: python

	from domonic.html import *
	mydivs = div()*100

You need to render them yourself by iterating and calling ``str``:

.. code-block :: python

    print(''.join([str(c) for c in mydivs]))


**Divide**

A divisor also creates more but will instead call render and give a list of strings...

.. code-block :: python

	from domonic.html import *
	print(div()/100)

This means they are rendered strings and cannot be edited as nodes.

You can convert them back by parsing and then calling ``domonify``:

.. code-block :: python

    mylist = li()/10
    myobj = domonic.domonify(domonic.parse(mylist))
    print(myobj)


**OR**

If the other value is truthy, it is returned. Otherwise, the element returns itself.

.. code-block :: python

    from domonic.html import *
    print(div() | False)
    print(div() | True)


Another way is to use a ternary expression:

.. code-block :: python

	mything = div() if True else span(_class="warning")


**In place add/minus**

You can add to or remove from the children of a Node with the in-place operators...

.. code-block :: python

    myorderedlist = ol()
    myorderedlist += str(li() / 10)
    print(myorderedlist)


This also works for text nodes but be aware they will be irreversibly flattened if you render...

.. code-block :: python

    a1 = button()
    a1 += "hi"
    a1 += "how"
    a1 += ["are", "you", "today"]
    print(a1)
    a1 -= "hi"
    print(a1)


Pass a dictionary to the right shift operator to add or update an attribute. Remember the leading underscore on attribute names.

.. code-block :: python

        a1 = img()
        a1 >> {'_src': "http://www.someurl.com"}
        print(a1)


Access an element's children as if it were a list:

.. code-block :: python

        mylist = ul(li(1), li(2), li(3))
        print(mylist[1])


Unpack children:

.. code-block :: python

        mylist = ul(li(), li(), li())
        print(*mylist)
        a1, b1, c1 = ul(li(1), li(2), li(3))
        print(a1)
        a1, b1, c1, d1, e1 = button() * 5
        print(a1, b1, c1, d1, e1)



f-strings
----------------

To pretty-print a domonic DOM, use an f-string:

.. code-block :: python
    
    print(f"{mydom}")

.. code-block :: html

    <!DOCTYPE html>
    <html>
        <body>
            <h1>Hello, World!</h1>
        </body>
    </html>

This calls the tag's ``__format__`` method.

This gives you a few ways to control output from domonic.

.. code-block :: python
    
    print(f"{mydom}")       # Pretty HTML through mydom.__format__("")
    
    print(f"{mydom!s}")     # str(mydom): compact HTML
    
    print(f"{mydom!r}")     # repr(mydom): Python/debug representation
    
    print(f"{mydom!a}")     # ascii(mydom): escaped non-ASCII representation
    
    print(str(mydom))       # Compact HTML

    print(mydom.__format__(''))  # Explicit pretty formatter call


If the built-in formatter is not enough, you can also use libraries that work with Beautiful Soup:

.. code-block :: python

	output = render(html(body(h1('Hello, World!'))))
	from html5print import HTMLBeautifier
	print(HTMLBeautifier.beautify(output, 4))


For outputting PyML to a string, use ``__pyml__()``.

You can also use this VS Code plugin on ``.pyml`` files:

https://marketplace.visualstudio.com/items?itemName=mgesbert.indent-nested-dictionary



Quotes around attributes
--------------------------------

The quotes around attributes can be controlled with the ``DOMConfig.ATTRIBUTE_QUOTES`` flag.

By default, everything is double quoted on render.

Set the flag to ``None`` to skip quotes when the value is not a string.

Alternatively, set it to a single quotation mark or to ``False`` to control quoting yourself.

Examples provided below.

.. code-block:: python

    >>> from domonic.html import *
    >>> from domonic.dom import DOMConfig
    >>> print(body(test="123"))
    # <body test="123"></body>
    >>> print(body(test=123))
    # <body test="123"></body>
    >>> DOMConfig.ATTRIBUTE_QUOTES = None
    >>> print(body(test=123))
    # <body test=123></body>
    >>> print(body(test="123"))
    # <body test="123"></body>
    >>> DOMConfig.ATTRIBUTE_QUOTES = "'"
    >>> print(body(test="123"))
    # <body test='123'></body>
    >>> DOMConfig.ATTRIBUTE_QUOTES = True
    >>> print(body(test="123"))
    # <body test="123"></body>
    >>> print(body(test=123))
    # <body test="123"></body>
    >>> DOMConfig.ATTRIBUTE_QUOTES = False
    >>> print(body(test="123"))
    # <body test=123></body>
    >>> print(body(test="TEXT"))
    # <body test=TEXT></body>



Loading .pyml templates
--------------------------------

.. code-block:: python

    div("Hello World")
    #<div>Hello tabs</div>


``loads`` imports a PyML file and turns it into a program.

This example loads a template and passes parameters for rendering:

.. code-block :: python

    from domonic import loads
    from domonic.html import *

    # Create some variables. These are referenced in the template file.
    brand = "MyBrand"
    links = ['one', 'two', 'three']

    # Load a template and pass it some data.
    webpage = domonic.loads('templates/webpage.com.pyml', links=links, brand=brand)

    render(webpage, 'webpage.html')


``load`` is different from ``loads``: it takes HTML strings and converts them to a program.

.. code-block :: python

    from domonic.dQuery import º

    webpage = domonic.load('<html><head></head><body id="test"></body></html>')
    º(webpage)
    º('#test').append(div("Hello World"))
    render(webpage, 'webpage2.html')


``loads`` is intentionally basic and works best with simple HTML.


Notes on templating
--------------------------------

You can create a ``div`` with content like this:

.. code-block :: python

    div("some content")

Python does not allow keyword arguments before positional arguments, so this will not work:

.. code-block :: python

    div(_class="container", p("Some content") )

Python will complain that the parameters are in the wrong order. Put content before attributes:

.. code-block :: python

    div( p("Some content"), _class="container")

That can get awkward when a ``div`` gets long.

You can get around this by using ``html``, which is available on every ``Element``:

.. code-block :: python

    div( _class="container" ).html("Some content")

This is not like jQuery's ``html`` function, which returns only inner content. Use ``innerHTML`` for that.

It is used specifically for rendering.


Common Errors
--------------------------------

If a template's syntax is incorrect, it will not work.

There is a small learning curve in getting ``.pyml`` templates correct. Usually the issue is one of these:

- a missing comma between tags
- a missing underscore on an attribute
- parameters in the wrong order

Use this reference when starting out:


.. code-block :: python

    IndexError: list index out of range
    # You most likely forgot an underscore on an attribute.

    SyntaxError: invalid syntax
    # You are missing a comma between attributes.

    SyntaxError: positional argument follows keyword argument
    # Pass strings and child nodes first, then attributes.

    TypeError: unsupported operand type(s) for ** or pow(): 'str' and 'dict'
    # You are missing a comma before **{}.


Parsing
--------------------------------

https://github.com/byteface/domonic/issues/28


Basic usage:

.. code-block:: python

   from domonic import domonic
   domonic.parseString('<somehtml...')


An example using ``html5lib`` directly:

.. code-block :: python

    import requests
    import html5lib
    from domonic.ext.html5lib_ import getTreeBuilder


    r = requests.get("https://google.com", timeout=30)
    parser = html5lib.HTMLParser(tree=getTreeBuilder())
    page = parser.parse(r.text)

    # print the page with formatting
    # print(f'{page}')

    '''
    links = page.getElementsByTagName('a')
    for l in links:
        try:
            print(l.href)
        except Exception as e:
            # no href on this tag
            pass
    '''

    # turn the downloaded site into .pyml ;)
    print(page.__pyml__())

You can also choose a parser directly through ``domonic.parseString()``:

.. code-block:: python

    from domonic import domonic

    page = domonic.parseString("<p>Hello World!</p>", parser="selectolax")
    page = domonic.parseString("<p>Hello World!</p>", parser="turbohtml")
    page = domonic.parseString("<p>Hello World!</p>", parser="lxml_html")
    page = domonic.parseString("<p>Hello World!</p>", parser="markupever")
    page = domonic.parseString("<p>Hello World!</p>", parser="html5_parser")
    page = domonic.parseString("<p>Hello World!</p>", parser="html.parser")
    print(page.querySelector("p").text)

Supported parser names are ``auto``, ``html.parser``, ``html_parser``, ``html5_parser``, ``html5lib``, ``lxml_html``, ``justhtml``, ``markupever``, ``selectolax``, ``turbohtml``, and ``expat``.

``html.parser`` uses Python's standard library and has no external dependency.

Parser Choices
--------------

Choose a parser based on the job:

.. code-block:: python

    from domonic import domonic

    domonic.set_default_parser("html.parser")
    page = domonic.parseString("<article><h1>Hello</h1></article>")

    assert page.querySelector("h1").text == "Hello"

The current practical parser order for large HTML pages is:

- ``selectolax``: fastest native parser in the bundled benchmark, adapted directly into domonic
- ``turbohtml``: fast native WHATWG parser, adapted directly into domonic
- ``lxml_html``: fast lxml-backed HTML parsing and DOM adaptation
- ``markupever``: fast Rust-powered HTML repair, adapted through lxml
- ``html5_parser``: fast HTML5 parser, adapted through lxml
- ``html.parser``: Python standard library, no external dependency
- ``html5lib``: bundled Python parser with broad compatibility
- ``justhtml``: pure-Python alternative
- ``expat``: useful for XML-like input

Install optional native parsers as needed:

.. code-block:: bash

    python -m pip install selectolax
    python -m pip install turbohtml
    python -m pip install lxml
    python -m pip install markupever lxml
    python -m pip install html5-parser lxml

For a quick parse, try the window module:

.. code-block :: python

    from domonic.window import *
    window.location = "http://www.google.com"
    print(window.document.title)

Related Examples and Guides
---------------------------

- :doc:`../guides/server-side-html`
- :doc:`../guides/scrape-html`
- :doc:`../guides/examples`
- `examples/boilerplate.py <https://github.com/byteface/domonic/blob/master/examples/boilerplate.py>`_
- `examples/grid.py <https://github.com/byteface/domonic/blob/master/examples/grid.py>`_
- `examples/declarative_shadow_dom.py <https://github.com/byteface/domonic/blob/master/examples/declarative_shadow_dom.py>`_
- `examples/speculation_rules.py <https://github.com/byteface/domonic/blob/master/examples/speculation_rules.py>`_

.. automodule:: domonic.html
    :members:
    :noindex:
