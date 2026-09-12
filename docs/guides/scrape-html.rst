Scrape HTML
===========

.. meta::
   :description: Scrape HTML with Python using domonic, BeautifulSlop, CSS selectors, XPath, find_all, get_text, and parser backends.
   :keywords: Python web scraping, Beautiful Soup alternative, bs4 compatible, CSS selector scraping, XPath scraping, parse HTML Python

Use domonic when you want to parse real HTML, query it with CSS selectors or
XPath, mutate the tree, and render the result back out.

Fetch And Query
---------------

``domonic.scrape()`` pulls a URL and hands back a parsed DOM, ready to query.

.. code-block:: python

   from domonic import scrape

   page = scrape("https://example.com")
   print(page.querySelector("h1").textContent)

The argument is a URL string or a ``domonic.webapi.fetch.Request``, so you can
build the request up front when you need more control:

.. code-block:: python

   from domonic.webapi.fetch import Request

   req = Request("https://example.com/api", init={"method": "POST", "json": {"q": "x"}})
   data = scrape(req, to="json")

What you get back
~~~~~~~~~~~~~~~~~~

By default the return value is the parsed DOM. ``to=`` swaps it for something
else:

- ``to="text"`` -- the raw response body
- ``to="json"`` -- the body decoded as JSON
- ``to="pyml"`` -- the body as PyML
- ``to="dom"`` -- the parsed DOM (the default)

``selector=`` runs a CSS query against the DOM and returns the first match (or
``None``); ``all=True`` returns every match as a list.

.. code-block:: python

   heading = scrape("https://example.com", selector="h1")
   links = scrape("https://example.com", selector="a[href]", all=True)
   markup = scrape("https://example.com", to="text")

The response
~~~~~~~~~~~~

``response=True`` returns ``(response, result)``. ``response`` is a
``domonic.webapi.fetch.Response`` -- ``.status``, ``.statusText``, ``.headers``,
``.ok``, ``.url``, ``.redirected``, plus ``.text()`` and ``.json()``.

.. code-block:: python

   response, page = scrape("https://example.com", response=True)
   print(response.status, response.headers.get("content-type"))

Many URLs at once
~~~~~~~~~~~~~~~~~~

Pass an iterable of URLs or ``Request`` objects and ``scrape()`` fetches them
concurrently through a thread pool (``domonic.webapi.fetch.fetch_pooled``). The
result is a list of whatever a single URL would have returned, in the same order
as the input.

.. code-block:: python

   for page in scrape(["https://example.com", "https://iana.org"]):
       print(page.querySelector("title").textContent)

   # with response=True, each item is a (response, result) pair
   for response, page in scrape(urls, selector="h1", response=True):
       print(response.status, page.textContent)

Parser and request options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``parser=`` picks the backend used to build the DOM, exactly as in
``parseString`` (see `Choose a Parser`_ below).

``method``, ``headers`` and any keyword argument that names a ``Request`` field
(``body``, ``json``, ``credentials``, ``redirect``, ``mode``, ...) build the
request. ``params``, ``timeout`` (default 30 seconds) and everything else are
forwarded to ``requests``.

.. code-block:: python

   page = scrape(
       "https://example.com",
       parser="selectolax",
       headers={"User-Agent": "domonic"},
       params={"q": "python"},
       timeout=10,
   )

   data = scrape("https://example.com/api", to="json", method="POST", json={"q": "python"})

A single-URL fetch that fails raises the underlying exception; in a batch, the
first failure is raised.

Parse To A DOM
--------------

Start with ``domonic.parseString()`` when you want a normal domonic document
tree. Parsed nodes support the same DOM methods as nodes created with
``domonic.html`` tags.

.. code-block:: python

   from domonic import domonic

   markup = """
   <main>
     <article class="post">
       <h1>Release</h1>
       <a href="/docs" class="external">Docs</a>
       <a href="/api">API</a>
     </article>
   </main>
   """

   page = domonic.parseString(markup, parser="html.parser")

   article = page.querySelector("article.post")
   print(article.querySelector("h1").textContent)
   # Release

   for link in page.querySelectorAll("article a"):
       print(link.textContent, link.getAttribute("href"))
   # Docs /docs
   # API /api

   article.setAttribute("data-seen", "yes")
   print(article.getAttribute("data-seen"))
   # yes

CSS Selectors
-------------

.. code-block:: python

   page = domonic.parseString(markup, parser="html.parser")

   print(page.querySelector("article.post > h1").textContent)
   # Release
   print([a.getAttribute("href") for a in page.querySelectorAll('a[href^="/"]')])
   # ['/docs', '/api']
   print(page.querySelectorAll("article a.external"))
   # [<a href="/docs" class="external">]

XPath
-----

.. code-block:: python

   from domonic import domonic
   from domonic.webapi.xpath import XPathEvaluator, XPathResult

   page = domonic.parseString(markup, parser="html.parser")
   evaluator = XPathEvaluator()
   expression = evaluator.createExpression("//article//a")
   result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)

   for node in result.nodes:
       print(node.textContent, node.getAttribute("href"))
   # Docs /docs
   # API /api

Clean a Page
------------

.. code-block:: python

   from domonic import domonic

   page = domonic.parseString(markup, parser="html.parser")

   for node in page.querySelectorAll("script, style, aside, nav"):
       node.remove()

   print(page.textContent.strip())

Choose a Parser
---------------

``html.parser`` is built in. Use it first when you want no extra dependency.
Install optional native parsers when you want faster repair or larger-page work.

.. code-block:: bash

   python -m pip install selectolax
   python -m pip install turbohtml
   python -m pip install markupever lxml
   python -m pip install html5-parser lxml

.. code-block:: python

   from domonic import domonic

   page = domonic.parseString(markup, parser="markupever")
   print(page.querySelector("h1").textContent)

Beautiful Soup Style
--------------------

``BeautifulSlop`` is the compatibility layer for Beautiful Soup style code. Use
it when you are porting BS4 examples or want familiar ``find()``,
``find_all()``, ``select()``, ``select_one()``, and ``get_text()`` helpers. It
still returns ordinary domonic DOM nodes.

.. code-block:: python

   from domonic.bs4 import BeautifulSlop

   soup = BeautifulSlop(markup, "html.parser")

   for link in soup.find_all("a", href=True):
       print(link.text, link["href"])
   # Docs /docs
   # API /api

   soup.find("article").setAttribute("data-seen", "yes")
   print(soup.querySelector("article").getAttribute("data-seen"))
   # yes

CLI Scraping
------------

.. code-block:: bash

   domonic -q https://example.com 'a[href]' --attr href
   # https://iana.org/domains/example

   domonic -q https://example.com 'h1' --text --first --parser selectolax
   # Example Domain

   domonic -x https://example.com '//a' --count --parser selectolax
   # 1

Next Steps
----------

- :doc:`../packages/bs4` for the full BeautifulSlop compatibility API
- :doc:`../packages/html` for parser names and DOM rendering
- :doc:`../packages/webapi` for XPath, URL, fetch, and XHR helpers
- :doc:`parser-performance` for parser benchmark commands
- :doc:`examples` for runnable scraping and parsing example files
