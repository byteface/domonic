Parser Performance
==================

.. meta::
   :description: Choose the fastest domonic HTML parser backend, benchmark BeautifulSlop against Beautiful Soup, compare turbohtml, markupever, lxml, html.parser, selectolax, html5_parser and html5lib.
   :keywords: Python HTML parser benchmark, BeautifulSoup alternative, turbohtml parser, lxml parser, markupever parser, selectolax parser, html.parser, BeautifulSlop benchmark

domonic can parse with several backends. The best parser depends on whether you
care about zero dependencies, malformed HTML repair, raw parse time, or repeated
query performance.

Parser Choices
--------------

.. list-table::
   :header-rows: 1

   * - Parser
     - Install
     - Use When
   * - ``selectolax``
     - ``python -m pip install selectolax``
     - You want the fastest native parser on the bundled large-page benchmark.
   * - ``turbohtml``
     - ``python -m pip install turbohtml``
     - You want native WHATWG parsing adapted directly into domonic.
   * - ``lxml_html``
     - ``python -m pip install lxml``
     - You want a fast lxml-backed parser and direct lxml DOM adaptation.
   * - ``markupever``
     - ``python -m pip install markupever lxml``
     - You want fast Rust-powered HTML repair.
   * - ``html5_parser``
     - ``python -m pip install html5-parser lxml``
     - You want a native HTML5 parser adapted into domonic.
   * - ``html.parser``
     - Built into Python
     - You want no external dependency.
   * - ``html5lib``
     - Bundled with domonic
     - You want broad Python compatibility.
   * - ``expat``
     - Built into Python
     - You are parsing XML-like input.

Pick a Parser
-------------

.. code-block:: python

   from domonic import domonic

   page = domonic.parseString("<main><h1>Hello</h1></main>", parser="html.parser")
   print(page.querySelector("h1").textContent)

Set a Default
-------------

.. code-block:: python

   from domonic import domonic

   domonic.set_default_parser("selectolax")
   page = domonic.parseString("<p>Hello</p>")

Benchmark Locally
-----------------

Run the parser benchmark from the repo root:

.. code-block:: bash

   python scripts/benchmark_parsers.py --iterations 7

Compare BeautifulSlop with Beautiful Soup:

.. code-block:: bash

   python scripts/benchmark_bs4.py --iterations 7

On the bundled large-page benchmark, the current parse-speed order is generally
``selectolax``, ``turbohtml``, ``lxml_html``, ``markupever``,
``html5_parser``, then ``html.parser``. ``html5lib`` and ``justhtml`` are useful
compatibility fallbacks rather than speed picks. ``expat`` is for XML-like input
and is expected to fail on many real-world HTML pages.

The important practical distinction is parse-only versus parse-plus-query.
BeautifulSlop is built to win query-heavy workflows because it keeps a real
domonic DOM and avoids a second wrapped tree.

Next Steps
----------

- :doc:`scrape-html` for BeautifulSlop, CSS selectors, and XPath examples
- :doc:`../packages/bs4` for the full BeautifulSlop API
- :doc:`../packages/html` for parser integration details
- `scripts/benchmark_parsers.py <https://github.com/byteface/domonic/blob/master/scripts/benchmark_parsers.py>`_
- `scripts/benchmark_bs4.py <https://github.com/byteface/domonic/blob/master/scripts/benchmark_bs4.py>`_
