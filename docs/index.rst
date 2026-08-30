domonic
=======

.. meta::
   :description: domonic is a Python DOM toolkit for HTML generation, SVG/XML, CSS selectors, XPath, Web APIs, and JavaScript-like scripting.
   :keywords: Python DOM, HTML generator, SVG, XML, JavaScript runtime, Web API, CSS selectors, XPath, HTML parser, server-side rendering, static site generator

.. image:: _static/domonic.jpg
  :width: 696
  :alt: domonic

A Python DOM that goes way beyond minidom
=========================================

Domonic is a Python library for generating, parsing, traversing, and manipulating real document trees with the broader web platform in mind.

It is also a practical way for Python developers to learn real HTML, DOM and
JavaScript-style APIs. The method names and mental model deliberately match the
browser platform: write ``div()``, query with ``querySelectorAll()``, move nodes
with ``appendChild()``, read ``textContent``, and use JavaScript-like helpers
such as ``Array``, ``Date``, ``Promise`` and ``URL`` from Python.

It works the other way too. If you are a JavaScript developer moving into
Python, domonic keeps familiar browser concepts close at hand: nodes,
selectors, events, URL parsing, JSON helpers, timers, promises, fetch-style
APIs, and DOM mutation all have Python equivalents with recognisable names.

- HTML, SVG, DOM, events, CSSOM, geometry, observers, animation, and web APIs
- A JavaScript-like runtime surface for practical porting and scripting
- diffDOM-style patch data for minimal server-side DOM updates
- BeautifulSlop for Beautiful Soup style querying over real domonic nodes
- CLI tools for querying pages with XPath and CSS selectors
- dQuery and d3 included as demanding consumers of the DOM, not just extras

The aim is to track the actual platform rather than invent a parallel helper API:

- `WHATWG DOM Standard <https://dom.spec.whatwg.org/>`_
- `HTML Standard <https://html.spec.whatwg.org/>`_
- `MDN Web APIs <https://developer.mozilla.org/en-US/docs/Web/API>`_

.. image:: https://pepy.tech/badge/domonic
    :target: https://pepy.tech/project/domonic

.. image:: https://img.shields.io/pypi/pyversions/domonic.svg
    :target: https://pypi.org/project/domonic/

.. image:: https://img.shields.io/pypi/l/domonic.svg
    :target: https://pypi.org/project/domonic/
    :alt: License Badge

.. image:: https://img.shields.io/pypi/v/domonic.svg
    :target: https://pypi.org/project/domonic/
    :alt: PyPI Version

Install
-------

.. code-block:: bash

   python3 -m pip install domonic
   python3 -m pip install --upgrade domonic

Quick Example
-------------

.. code-block:: python

   from domonic.html import *

   page = html(
       body(
           h1("Hello, World!"),
           a("docs", _href="https://domonic.readthedocs.io/")
       )
   )
   print(f"{page}")

.. code-block:: html

   <!DOCTYPE html>
   <html>
       <body>
           <h1>Hello, World!</h1>
           <a href="https://domonic.readthedocs.io/">docs</a>
       </body>
   </html>

DOM Example
-----------

.. code-block:: python

   from domonic.dom import document
   from domonic.html import html

   root = html()
   card = document.createElement("section")
   card.setAttribute("class", "card")
   root.appendChild(card)

   print(root.querySelectorAll(".card"))

Start Here
----------

Use these copy-paste starting points for common Python web, scraping, DOM, and
server-side rendering tasks.

Most examples intentionally use web-platform names. If you learn the domonic
version, you are learning vocabulary that transfers back to browser HTML,
JavaScript, CSS selectors, XPath, and Web APIs.

And if you already know browser JavaScript, the examples are designed to feel
approachable because they keep the DOM vocabulary you already use.

Generate HTML with Python:

.. code-block:: python

   from domonic.html import a, article, h1, p

   page = article(
       h1("domonic"),
       p("Generate HTML with Python objects."),
       a("Read more", _href="/docs", _class="cta"),
   )
   print(page)

Parse and query HTML:

.. code-block:: python

   from domonic import domonic

   page = domonic.parseString("<main><a href='/docs'>Docs</a></main>", parser="html.parser")
   print(page.querySelector("a").getAttribute("href"))

Use Beautiful Soup style scraping over real DOM nodes:

.. code-block:: python

   from domonic.bs4 import BeautifulSlop

   soup = BeautifulSlop("<article><a href='/api'>API</a></article>", "html.parser")
   for link in soup.find_all("a", href=True):
       print(link.text, link["href"])

Diff two DOM trees:

.. code-block:: python

   from domonic.diffdom import DiffDOM
   from domonic.html import div, p

   old = div(p("one"))
   new = div(p("two"))
   changes = DiffDOM().diff(old, new)
   print(changes)

Use browser Web APIs in Python:

.. code-block:: python

   from domonic.webapi.crypto import crypto
   from domonic.webapi.encoding import TextEncoder

   print(crypto.randomUUID())
   print(TextEncoder().encode("hello"))

Guides
------

.. toctree::
   :maxdepth: 1

   guides/index

The guide section includes task-focused walkthroughs for :doc:`guides/scrape-html`,
:doc:`guides/server-side-html`, :doc:`guides/live-dom-updates`,
:doc:`guides/parser-performance`, and :doc:`guides/examples`.

CLI
---

Query a remote page:

.. code-block:: bash

   domonic -x https://example.com '//title'
   domonic -q https://example.com 'a.cta' --attr href --first

Query a local file:

.. code-block:: bash

   domonic --xpath-file ./page.html '//a' --count
   domonic --query-file ./page.html 'a.cta' --text

Pipe HTML in directly:

.. code-block:: bash

   curl -s https://example.com | domonic -x '//a' --count
   cat page.html | domonic -q 'a.cta' --attr href

Create a project with a chosen server:

.. code-block:: bash

   domonic -p myproject --server fastapi

Package Guide
-------------

.. toctree::
   :maxdepth: 2

   packages/html
   packages/dom
   packages/events
   packages/animation
   packages/style
   packages/javascript
   packages/webapi
   packages/constants
   packages/bs4
   packages/dQuery
   packages/diffdom
   packages/d3
   packages/svg
   packages/xml
   packages/JSON
   packages/terminal
   packages/cmd
   packages/tween
   packages/geom
   packages/x3d
   packages/CDN
   packages/decorators
   packages/components
   packages/utils
   packages/servers
   packages/sitemap
   packages/autodocs
   contribute

Projects
--------

- `Blueberry <https://github.com/byteface/Blueberry/>`_: a browser-based file OS
- `ezcron <https://github.com/byteface/ezcron/>`_: a cron viewer
- `bombdisposer <https://github.com/byteface/bombdisposer/>`_: a basic game
- `htmlx <https://github.com/byteface/htmlx/tree/master/htmlx>`_: a lighter DOM-focused sibling project

Indices and Tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
