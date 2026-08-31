Scrape HTML
===========

.. meta::
   :description: Scrape HTML with Python using domonic, BeautifulSlop, CSS selectors, XPath, find_all, get_text, and parser backends.
   :keywords: Python web scraping, Beautiful Soup alternative, bs4 compatible, CSS selector scraping, XPath scraping, parse HTML Python

Use domonic when you want to parse real HTML, query it with CSS selectors or
XPath, mutate the tree, and render the result back out.

Beautiful Soup Style
--------------------

``BeautifulSlop`` gives you familiar ``find()``, ``find_all()``, ``select()``,
``select_one()``, ``get_text()``, and mutation methods while returning ordinary
domonic DOM nodes.

.. code-block:: python

   from domonic.bs4 import BeautifulSlop

   markup = """
   <main>
     <article class="post">
       <h1>Release</h1>
       <a href="/docs" class="external">Docs</a>
       <a href="/api">API</a>
     </article>
   </main>
   """

   soup = BeautifulSlop(markup, "html.parser")

   for link in soup.find_all("a", href=True):
       print(link.text, link["href"])

   soup.find("article").setAttribute("data-seen", "yes")
   print(soup.querySelector("article").getAttribute("data-seen"))

CSS Selectors
-------------

.. code-block:: python

   from domonic.bs4 import BeautifulSlop

   soup = BeautifulSlop(markup, "html.parser")

   print(soup.select_one("article.post > h1").text)
   print([a["href"] for a in soup.select('a[href^="/"]')])
   print(soup.select("article a.external"))

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

Clean a Page
------------

.. code-block:: python

   from domonic.bs4 import BeautifulSlop

   soup = BeautifulSlop(markup, "html.parser")

   for node in soup.select("script, style, aside, nav"):
       node.decompose()

   print(soup.get_text(" ", strip=True))

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

   from domonic.bs4 import BeautifulSlop

   soup = BeautifulSlop(markup, "markupever")
   print(soup.find("h1").text)

CLI Scraping
------------

.. code-block:: bash

   domonic -q https://example.com 'a[href]' --attr href
   domonic -q https://example.com 'main h1' --text --first --parser selectolax
   domonic -x https://example.com '//a' --count --parser selectolax

Next Steps
----------

- :doc:`../packages/bs4` for the full BeautifulSlop compatibility API
- :doc:`../packages/html` for parser names and DOM rendering
- :doc:`../packages/webapi` for XPath, URL, fetch, and XHR helpers
- :doc:`parser-performance` for parser benchmark commands
- :doc:`examples` for runnable scraping and parsing example files
