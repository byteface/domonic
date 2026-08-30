Parser Performance
==================

.. meta::
   :description: Choose the fastest domonic HTML parser backend, benchmark BeautifulSlop against Beautiful Soup, compare markupever, lxml, html.parser, selectolax, html5_parser and html5lib.
   :keywords: Python HTML parser benchmark, BeautifulSoup alternative, lxml parser, markupever parser, selectolax parser, html.parser, BeautifulSlop benchmark

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
   * - ``markupever``
     - ``python -m pip install markupever lxml``
     - You want fast HTML repair and strong parse-plus-query results.
   * - ``lxml_html``
     - ``python -m pip install lxml``
     - You want a fast lxml-backed parser and direct lxml DOM adaptation.
   * - ``html.parser``
     - Built into Python
     - You want no external dependency.
   * - ``selectolax``
     - ``python -m pip install selectolax lxml``
     - You want a native parser adapted into domonic.
   * - ``html5_parser``
     - ``python -m pip install html5-parser lxml``
     - You want a native HTML5 parser adapted into domonic.
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

   domonic.set_default_parser("markupever")
   page = domonic.parseString("<p>Hello</p>")

Benchmark Locally
-----------------

Run the parser benchmark from the repo root:

.. code-block:: bash

   python scripts/benchmark_parsers.py --iterations 7

Compare BeautifulSlop with Beautiful Soup:

.. code-block:: bash

   python scripts/benchmark_bs4.py --iterations 7

The important practical distinction is parse-only versus parse-plus-query. Raw
parsing can be faster in Beautiful Soup with lxml, while BeautifulSlop is built
to win query-heavy workflows because it keeps a real domonic DOM and avoids a
second wrapped tree.

