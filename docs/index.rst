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

- HTML, SVG, DOM, events, CSSOM, geometry, observers, animation, and web APIs
- A JavaScript-like runtime surface for practical porting and scripting
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
   packages/dQuery
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
