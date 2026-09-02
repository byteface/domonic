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

Which Backend Ran
-----------------

With ``parser="auto"`` (the default) the fastest installed backend that can
parse the input is used, in the order ``selectolax``, ``turbohtml``,
``lxml_html``, ``html5_parser``, ``markupever``, ``html.parser``, ``justhtml``,
``html5lib`` (then ``expat`` as a last resort for XML-like input). Backends
that are not installed, or that raise on the input, are skipped silently -- so
on a machine with only ``html5lib`` available you are always on ``html5lib``
with no signal. To see which backend actually handled a parse:

.. code-block:: python

   from domonic import domonic

   domonic.parseString("<p>Hello</p>")
   domonic.get_active_parser()          # -> "selectolax" (or whatever ran)

Or enable the logger for a running commentary of what was skipped:

.. code-block:: python

   import logging

   logging.getLogger("domonic.parser").setLevel(logging.DEBUG)
   logging.basicConfig()

When a parser choice is suspected, install the alternative and pass ``parser=``
explicitly to compare, rather than relying on ``auto``.

Benchmark Locally
-----------------

Run the parser benchmark from the repo root:

.. code-block:: bash

   python scripts/benchmark_parsers.py --iterations 7

Compare BeautifulSlop with Beautiful Soup across every fixture shape (tiny,
large, wide/flat, deeply nested, table-heavy, malformed) and the full API
surface -- CSS selection, ``find`` / ``find_all``, navigation, mutation,
serialization, text and attribute access:

.. code-block:: bash

   python scripts/make_bench_fixtures.py     # once, to generate the synthetic fixtures
   python scripts/benchmark_bs4.py --all-pages --mem --report benchmarks/REPORT.md

Add ``--check`` for a correctness-parity-only pass (exit code is non-zero on a
real mismatch). The committed ``benchmarks/REPORT.md`` is the last full run.

On the bundled large-page benchmark, the current parse-speed order is generally
``selectolax``, ``turbohtml``, ``lxml_html``, ``html5_parser``, ``markupever``,
``html.parser``, ``justhtml``, then ``html5lib``. ``justhtml`` and ``html5lib``
build a domonic tree in pure Python so they trail the native parsers, but both
adapters walk their parser's native tree directly now rather than re-parsing.
``expat`` is for XML-like input and is expected to fail on many real-world HTML
pages.

``html.parser`` is the stdlib tokenizer with no HTML5 tree construction. The
adapter closes an open ``<li>``, ``<dt>``, ``<dd>`` or ``<p>`` on the matching
start tag, but it does not run the full implied-tag or adoption-agency
algorithm, so deeply malformed markup (mis-nested inline formatting, tables
without ``<tbody>``/``<tr>``) still comes out differently from ``html5lib``. Use
a real tree-building backend when input HTML cannot be trusted.

Whitespace fidelity
-------------------

``html5lib``, ``html.parser``, ``lxml_html``, ``selectolax``, ``turbohtml`` and
``justhtml`` keep whitespace-only text nodes, so whitespace between inline
elements (``<b>x</b> <i>y</i>``) survives the parse -- Markdown converters and
anything that reflows inline content depend on this. ``markupever`` currently
loses it: its adapter round-trips through the ``markupever`` serializer, which
re-indents and drops the original whitespace nodes.

The important practical distinction is parse-only versus parse-plus-query.
BeautifulSlop is built to win query-heavy workflows because it keeps a real
domonic DOM and avoids a second wrapped tree.

``querySelector`` / ``querySelectorAll`` resolve descendant and child
combinators, classes, attribute selectors and simple pseudo-classes with a
native engine (shared with BeautifulSlop); only selectors it cannot handle
(``+``, ``~``, complex pseudo-classes) fall back to the slower
cssselect -> XPath path.

Next Steps
----------

- :doc:`scrape-html` for BeautifulSlop, CSS selectors, and XPath examples
- :doc:`../packages/bs4` for the full BeautifulSlop API
- :doc:`../packages/html` for parser integration details
- `scripts/benchmark_parsers.py <https://github.com/byteface/domonic/blob/master/scripts/benchmark_parsers.py>`_
- `scripts/benchmark_bs4.py <https://github.com/byteface/domonic/blob/master/scripts/benchmark_bs4.py>`_
