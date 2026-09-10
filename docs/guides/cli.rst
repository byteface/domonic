Command Line
============

.. meta::
   :description: The domonic command line tool -- query URLs, local files or piped HTML with CSS selectors or XPath, extract text and attributes, evaluate pyml, and scaffold projects.
   :keywords: domonic CLI, query HTML command line, CSS selector CLI, XPath CLI, scrape URL terminal, pyml evaluate, scaffold Python project

``domonic`` ships a command line tool for working with HTML without writing a
script: query a URL, a local file or piped input with CSS or XPath, pull out
text or attributes, evaluate ``pyml``, or scaffold a project.

Install
-------

``pipx`` keeps the executable isolated and on your shell path:

.. code-block:: bash

   brew install pipx
   pipx ensurepath
   pipx install domonic

``pip install domonic`` also installs the command; ``pipx`` just avoids adding
domonic to a project environment only for its CLI.

.. code-block:: bash

   domonic -h          # help
   domonic -v          # version

Query a URL
-----------

CSS selectors with ``-q``, XPath with ``-x``:

.. code-block:: bash

   domonic -q https://example.com 'a'
   domonic -x https://example.com '//a'

   # pin a parser backend
   domonic -q https://example.com 'a' --parser selectolax
   domonic -x https://example.com '//a' --parser selectolax

Shape the output
----------------

.. list-table::
   :header-rows: 1

   * - Flag
     - Effect
   * - ``--text``
     - print each match's text content instead of its markup
   * - ``--attr NAME``
     - print the ``NAME`` attribute of each match
   * - ``--first``
     - only the first match
   * - ``--count``
     - just the number of matches
   * - ``--parser NAME``
     - parse with a specific backend (see :doc:`parser-performance`)

.. code-block:: bash

   domonic -q https://example.com 'h1' --text
   domonic -q https://example.com 'a' --attr href
   domonic -q https://example.com 'a' --first
   domonic -x https://example.com '//a' --count

Local files
-----------

.. code-block:: bash

   domonic --xpath-file ./page.html '//title'
   domonic --query-file ./page.html 'a.cta' --parser selectolax

Pipes
-----

Read HTML from stdin by omitting the URL:

.. code-block:: bash

   curl -s https://example.com | domonic -x '//a' --count
   cat page.html | domonic -q 'a.cta' --attr href --parser selectolax

Evaluate pyml
-------------

``-e`` renders a domonic expression to markup:

.. code-block:: bash

   domonic -e 'html(head(), body(h1("hello")))'

Scaffold a project
------------------

``-p`` creates a starter project; ``--server`` picks the framework:

.. code-block:: bash

   domonic -p myproject
   domonic -p myproject --server fastapi

See :doc:`server-side-html` for what the scaffold gives you.
