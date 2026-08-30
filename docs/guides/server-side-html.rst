Server-Side HTML
================

.. meta::
   :description: Build server-side rendered HTML with Python, domonic, FastAPI, Flask, Django, Starlette, Sanic, htmx, components, and templates.
   :keywords: Python server-side rendering, FastAPI HTML, Flask HTML, Django HTML, htmx Python, Python templates, HTML components

domonic elements are Python objects that render to HTML strings. That makes them
easy to return from any Python web framework.

Reusable Components
-------------------

.. code-block:: python

   from domonic.html import a, article, h2, p

   def card(title, body, href):
       return article(
           h2(title),
           p(body),
           a("Open", _href=href),
           _class="card",
       )

   print(card("Docs", "Read the domonic guide.", "/docs"))

FastAPI
-------

.. code-block:: python

   from fastapi import FastAPI
   from fastapi.responses import HTMLResponse

   from domonic.html import body, h1, html, main, p

   app = FastAPI()

   @app.get("/", response_class=HTMLResponse)
   def home():
       page = html(
           body(
               main(
                   h1("domonic + FastAPI"),
                   p("HTML generated with Python objects."),
               )
           )
       )
       return str(page)

Flask
-----

.. code-block:: python

   from flask import Flask

   from domonic.html import body, h1, html

   app = Flask(__name__)

   @app.route("/")
   def home():
       return str(html(body(h1("domonic + Flask"))))

htmx Attributes
---------------

Enable htmx shortcut attributes when you want to generate ``data-hx-*`` markup.

.. code-block:: python

   from domonic.dom import DOMConfig
   from domonic.html import button, div

   DOMConfig.HTMX_ENABLED = True

   fragment = div(
       button("Refresh", _get="/items", _target="#items", _swap="outerHTML"),
       div(_id="items"),
   )

   print(fragment)

Escape User Content
-------------------

When rendering user-controlled text, enable autoescape or sanitize HTML before
placing it into the DOM.

.. code-block:: python

   from domonic.dom import DOMConfig
   from domonic.html import p

   DOMConfig.GLOBAL_AUTOESCAPE = True
   print(p("<script>bad()</script>"))

Project Scaffolding
-------------------

.. code-block:: bash

   domonic -p myproject --server fastapi

Next Steps
----------

- :doc:`../packages/html` for tag constructors, attributes, htmx, and rendering
- :doc:`../packages/components` for reusable component patterns
- :doc:`../packages/servers` for FastAPI, Flask, Django, Sanic, Starlette and more
- :doc:`../packages/webapi` for Sanitizer, History, URL, Workers, Streams, and File API
- :doc:`examples` for runnable server-side examples
