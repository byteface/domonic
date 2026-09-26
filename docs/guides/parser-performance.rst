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
     - You want fast native HTML parsing with direct DOM adaptation.
   * - ``turbohtml``
     - ``python -m pip install turbohtml``
     - You want native WHATWG parsing adapted directly into domonic.
   * - ``tl``
     - ``python -m pip install tl-parser`` (Python 3.12+)
     - You want an opt-in Rust parser with direct raw DOM adaptation.
   * - ``reliq``
     - ``python -m pip install reliq``
     - You want native parsing with bulk raw DOM adaptation (explicit selection).
   * - ``lxml_html``
     - ``python -m pip install lxml``
     - You want a fast lxml-backed parser and direct lxml DOM adaptation.
   * - ``markupever``
     - ``python -m pip install markupever``
     - You want fast Rust-powered HTML5 repair, adapted directly into domonic.
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

The ``tl`` adapter uses the public API of ``tl-parser`` 0.7.12 and the shared
raw DOM constructors. It preserves tl's native recovery semantics, including
its interpretation of markup-like text inside script/style as tags. It is not
an HTML5 replacement and remains outside ``auto``. Leading PUBLIC/SYSTEM
doctypes are preserved separately from the native tree.

Pick a Parser
-------------

.. code-block:: python

   from domonic import domonic

   page = domonic.parseString("<main><h1>Hello</h1></main>", parser="html.parser")
   print(page.querySelector("h1").textContent)
   # Hello

Set a Default
-------------

.. code-block:: python

   from domonic import domonic

   domonic.set_default_parser("selectolax")
   page = domonic.parseString("<p>Hello</p>")

Registering Your Own Backend
----------------------------

Plug an external parser in by name with ``register_parser``. The callable is
invoked as ``parser(source, **options)`` and must return a domonic ``Node``.
``options`` currently carries ``document`` (bool) and ``debug`` (bool); accept
``**kwargs`` so a future option cannot break the call.

.. code-block:: python

   from domonic import domonic

   def my_backend(source, **options):
       tree = some_parser.parse(source, full_document=options.get("document", False))
       return adapt_to_domonic(tree)          # a domonic Document / Element

   domonic.register_parser("mybackend", my_backend)

   domonic.parseString(markup, parser="mybackend")   # by name
   domonic.set_default_parser("mybackend")            # or as the default

``register_parser("name", fn, auto=True)`` also places the backend at the front
of the ``parser="auto"`` cascade. A ``name`` that matches a built-in shadows it.
``unregister_parser("name")`` removes one; ``registered_parsers()`` lists them.

Because ``options`` is forwarded as keywords, a backend written this way keeps
working when ``parseString`` gains new options -- prefer it to monkeypatching
``domonic.parseString``, whose signature is not a stable API.

Which Backend Ran
-----------------

With ``parser="auto"`` (the default) the fastest installed backend that can
parse the input is used, in the order ``selectolax``, ``turbohtml``,
``markupever``, ``lxml_html``, ``html5_parser``, ``html.parser``, ``justhtml``,
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

The latest controlled large-page run (35 rounds with rotating backend order)
measured ``tl`` at 19.8 ms, ``turbohtml`` at 20.7 ms, ``reliq`` at 22.0 ms,
``selectolax`` at 28.8 ms, and ``lxml_html`` at 36.8 ms after shared raw DOM
and tl hot-path improvements.
These are local medians, not a universal ranking. Reliq's optimized adapter
uses checked native-array layouts in version 0.0.48; unrecognized layouts
use C conversion and other versions use the public API. It remains opt-in.
The main ``benchmarks/REPORT.md`` contains both controlled and GC-enabled results.

To isolate native parsing from DOM conversion:

.. code-block:: bash

   python scripts/benchmark_reliq.py --iterations 35 --interleave

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

``html5lib``, ``html.parser``, ``lxml_html``, ``selectolax``, ``turbohtml``,
``justhtml`` and ``markupever`` keep whitespace-only text nodes, so whitespace
between inline elements (``<b>x</b> <i>y</i>``) survives the parse -- Markdown
converters and anything that reflows inline content depend on this.

The important practical distinction is parse-only versus parse-plus-query.
BeautifulSlop is built to win query-heavy workflows because it keeps a real
domonic DOM and avoids a second wrapped tree. Walking a wide parent by
``nextSibling``, by ``children[i]``, or by index over a live
``getElementsByTagName`` collection is linear, not quadratic.

``querySelector`` / ``querySelectorAll`` resolve descendant, child, adjacent
(``+``) and general-sibling (``~``) combinators, classes, attribute selectors
and the common pseudo-classes (``:first-child``, ``:last-child``,
``:nth-child``, ``:not(...)``) with a native engine shared with BeautifulSlop.
Only the rarer pseudo-classes fall back to the slower cssselect -> XPath path.

Index-backed queries
--------------------

Read queries against an unchanged tree are served from lazily-built indexes
rather than a fresh walk, so repeated lookups over one parsed document are the
common fast path:

- ``getElementById`` builds an ``id -> element`` map on first use and answers in
  constant time thereafter.
- ``getElementsByTagName`` / ``-ClassName`` / ``-Name``, ``querySelector`` /
  ``querySelectorAll``, and BeautifulSlop's ``select`` / ``find`` / ``find_all``
  consult tag, class and attribute indexes built on the tree's root.
- ``find_all`` calls that reduce to a tag (or list of tags) plus
  attribute-presence filters (``find_all(["a", "span"])``,
  ``find_all("a", href=True)``) are served straight from those indexes with no
  per-element re-check.

The indexes are invalidated automatically. Any structural change
(``appendChild``, ``removeChild``, ``innerHTML =``, ...) or attribute change
(``setAttribute``, ``classList`` edits, ``el.id =``) made through the DOM API --
or through a BeautifulSlop mutation method -- marks them stale, and the next
query rebuilds. Results always reflect the current tree; the index is a cache,
never a snapshot. Trees that are only built and serialised, never queried, pay
nothing for the machinery.

Next Steps
----------

- :doc:`scrape-html` for BeautifulSlop, CSS selectors, and XPath examples
- :doc:`../packages/bs4` for the full BeautifulSlop API
- :doc:`../packages/html` for parser integration details
- `scripts/benchmark_parsers.py <https://github.com/byteface/domonic/blob/master/scripts/benchmark_parsers.py>`_
- `scripts/benchmark_bs4.py <https://github.com/byteface/domonic/blob/master/scripts/benchmark_bs4.py>`_
