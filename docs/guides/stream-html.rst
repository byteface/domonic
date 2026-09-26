Stream HTML
===========

.. meta::
   :description: Stream HTML with Python in both directions: parse a page as it downloads with document.write() and MutationObserver, and send a page as it renders with stream().
   :keywords: Python streaming HTML parser, incremental HTML parsing Python, document.write Python, MutationObserver Python, streaming HTML response Python, chunked HTML rendering

Both directions: parse a page while it downloads, and send a page while it
renders.

In
--

Parse a page while it downloads, look at what has landed, and stop early.
This is the browser's own model, so there is nothing new to learn:
``document.open()`` starts the parser, ``document.write()`` feeds it,
``MutationObserver`` reports nodes as they arrive, ``document.readyState``
tracks progress and ``window.stop()`` aborts.

Scripts out of the head, then stop:

.. code-block :: python

	from domonic.dom import HTMLDocument, MutationObserver
	from domonic.window import Window

	doc = HTMLDocument()
	win = Window()
	win.attach(doc)

	def landed(records, observer):
	    for record in records:
	        for node in record.addedNodes:
	            if node.nodeName.lower() == "script" and node.getAttribute("src"):
	                print(node.getAttribute("src"))
	            if node.nodeName.lower() == "body":
	                win.stop()          # the head is done, drop the rest

	MutationObserver(landed).observe(doc, {"childList": True, "subtree": True})

	doc.open()
	for chunk in response.iter_content(16384):
	    doc.write(chunk)                # records are delivered after each write
	doc.close()

What you get:

- Between writes the document is live. ``querySelector``, ``getElementById``
  and ``str(doc)`` all see what has been parsed so far.
- Observer records arrive after each write, one per parent that gained
  children, text nodes included.
- ``readyState`` moves ``loading`` -> ``interactive`` -> ``complete``, with
  ``readystatechange`` on the document, ``DOMContentLoaded`` at
  ``interactive`` and ``load`` on the window at ``complete``.
- Chunks can be text or bytes of any size. Bytes are decoded the way a
  browser decodes a page (byte order mark, then the ``<meta charset>`` in the
  first kilobyte, else UTF-8 or windows-1252), a character split across two
  chunks is carried over, and ``document.characterSet`` reports the result.
  A run of text at the very end of a chunk lands with the next tag or at
  ``close()``, since the tokenizer cannot know the run is over.
- After ``window.stop()`` further writes are ignored and ``close()`` still
  finalises what has landed.

``write()`` without ``open()`` opens the document for you, which empties it,
as in a browser. Everything written after that accumulates until ``close()``.

Huge pages
~~~~~~~~~~

Streaming means the source never has to be in memory at once, but every node
that lands is a Python object, and the tree, not the source, is what a big
page costs. To keep memory flat, take what you need from each finished
element as it lands and drop it. The parser only ever appends to the last
open element, so under any parent every child but the last has finished:

.. code-block :: python

	import gc

	def landed(records, observer):
	    for record in records:
	        for node in list(record.target.childNodes)[:-1]:
	            handle(node)        # read what you want out of it
	            node.remove()

	MutationObserver(landed).observe(doc, {"childList": True, "subtree": True})
	doc.open()
	for chunk in response.iter_content(16384):
	    doc.write(chunk)
	    gc.collect()                # dropped nodes are reference cycles; collect them now
	doc.close()

Removing a finished node is safe while its parent is still open. The
``gc.collect()`` matters: parent and child reference each other, so a dropped
subtree waits for the cyclic collector, which otherwise gets to it late.

Which parser does the work follows :func:`domonic.set_default_parser`:

- ``html5lib`` (the default, and what ``auto`` means here): the bundled
  WHATWG tree builder, so the partial tree is the one a browser would have,
  implied elements, foster parenting and the adoption agency included.
- ``html.parser``: the standard library tokenizer. Nothing to install, but
  no HTML5 tree repair beyond implied table sections and paragraph closing.

The other backends cannot stream: the native ones (``selectolax``,
``turbohtml``, ``markupever``, ``html5_parser``) only hand back a tree once
the whole input is parsed, and libxml2 (``lxml_html``) holds most of a page
back until the parser is closed. Asking for any of them here means html5lib.
For markup you already hold in memory they remain the fast path through
:func:`domonic.parseString` (see :doc:`parser-performance`).

Out
---

Every node has ``stream()``: it yields the rendered HTML in chunks, and
``str(node)`` is just ``"".join(node.stream())``. A generator passed as a
child is only run as the stream reaches it, so a large page can start going
out before its rows exist.

.. code-block :: python

	from fastapi.responses import StreamingResponse
	from domonic.html import body, html, table, td, tr

	def rows():
	    for index in range(50000):
	        yield tr(td(f"Row {index}"), td(f"Data {index}"))

	page = html(body(table(rows())))
	response = StreamingResponse(page.stream(), media_type="text/html")

The same iterator writes a large file without holding it in memory. More on
rendering, including the memory benchmark, in :doc:`../packages/html`.
