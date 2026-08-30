Examples Gallery
================

.. meta::
   :description: Runnable domonic examples for Python HTML generation, BeautifulSlop scraping, diffdom, Web APIs, SVG, MathML, RSS, Atom, ODF, sockets, games, htmx, workers and templates.
   :keywords: domonic examples, Python HTML examples, BeautifulSlop example, diffdom example, Web API Python examples, SVG Python example, RSS Python example

The fastest way to learn domonic is to copy a small example, run it, then change
one thing. The repository keeps examples small and focused so each file shows a
particular feature.

HTML and Templates
------------------

- `examples/boilerplate.py <https://github.com/byteface/domonic/blob/master/examples/boilerplate.py>`_
- `examples/grid.py <https://github.com/byteface/domonic/blob/master/examples/grid.py>`_
- `examples/templates/loading_templates.py <https://github.com/byteface/domonic/blob/master/examples/templates/loading_templates.py>`_
- `examples/declarative_shadow_dom.py <https://github.com/byteface/domonic/blob/master/examples/declarative_shadow_dom.py>`_
- `examples/speculation_rules.py <https://github.com/byteface/domonic/blob/master/examples/speculation_rules.py>`_
- `examples/validity_state.py <https://github.com/byteface/domonic/blob/master/examples/validity_state.py>`_

Parsing, Scraping, and DOM Querying
-----------------------------------

- `examples/beautifulslop.py <https://github.com/byteface/domonic/blob/master/examples/beautifulslop.py>`_
- `examples/xpathtest.py <https://github.com/byteface/domonic/blob/master/examples/xpathtest.py>`_
- `examples/parsing/page.py <https://github.com/byteface/domonic/blob/master/examples/parsing/page.py>`_
- `examples/parsing/codemirror.py <https://github.com/byteface/domonic/blob/master/examples/parsing/codemirror.py>`_

DOM Diffing and Live Updates
----------------------------

- `examples/diffdom.py <https://github.com/byteface/domonic/blob/master/examples/diffdom.py>`_
- `examples/sockets/diffdom_socket.py <https://github.com/byteface/domonic/blob/master/examples/sockets/diffdom_socket.py>`_
- `examples/sockets/events_test.py <https://github.com/byteface/domonic/blob/master/examples/sockets/events_test.py>`_

Web APIs
--------

- `examples/file_api.py <https://github.com/byteface/domonic/blob/master/examples/file_api.py>`_
- `examples/web_crypto.py <https://github.com/byteface/domonic/blob/master/examples/web_crypto.py>`_
- `examples/messaging.py <https://github.com/byteface/domonic/blob/master/examples/messaging.py>`_
- `examples/webworkers.py <https://github.com/byteface/domonic/blob/master/examples/webworkers.py>`_
- `examples/scheduler_api.py <https://github.com/byteface/domonic/blob/master/examples/scheduler_api.py>`_
- `examples/webmcp_form.py <https://github.com/byteface/domonic/blob/master/examples/webmcp_form.py>`_

SVG, XML, MathML, and Feeds
---------------------------

- `examples/svg.html <https://github.com/byteface/domonic/blob/master/examples/svg.html>`_
- `examples/mathml.py <https://github.com/byteface/domonic/blob/master/examples/mathml.py>`_
- `examples/rss_feed.py <https://github.com/byteface/domonic/blob/master/examples/rss_feed.py>`_
- `examples/atom_feed.py <https://github.com/byteface/domonic/blob/master/examples/atom_feed.py>`_
- `examples/odf_content.py <https://github.com/byteface/domonic/blob/master/examples/odf_content.py>`_

Games and Interactive Demos
---------------------------

- `examples/games/hangman.py <https://github.com/byteface/domonic/blob/master/examples/games/hangman.py>`_
- `examples/games/rockpaperscissors.py <https://github.com/byteface/domonic/blob/master/examples/games/rockpaperscissors.py>`_
- `examples/ken/sf2.py <https://github.com/byteface/domonic/blob/master/examples/ken/sf2.py>`_
- `examples/keyboard/keyboard.py <https://github.com/byteface/domonic/blob/master/examples/keyboard/keyboard.py>`_

Benchmarks
----------

- `scripts/benchmark_parsers.py <https://github.com/byteface/domonic/blob/master/scripts/benchmark_parsers.py>`_
- `scripts/benchmark_bs4.py <https://github.com/byteface/domonic/blob/master/scripts/benchmark_bs4.py>`_

Run an Example
--------------

From the repo root:

.. code-block:: bash

   python examples/beautifulslop.py
   python examples/diffdom.py
   python examples/web_crypto.py

Server-backed examples usually list their framework dependency in the file.
Install the relevant package, then run the script from the repo root.

