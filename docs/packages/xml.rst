xml
===

The ``domonic.xml`` package contains focused builders for XML-based formats
that benefit from namespaced tag constructors.

MathML
------

MathML tags live in ``domonic.xml.mathml`` and now use the browser-style
``MathMLElement`` interface.

.. code-block :: python

	from domonic.dom import MathMLElement
	from domonic.xml.mathml import math_, mi, mo, mn, mrow

	expression = math_(mrow(mi("x"), mo("="), mn("1")))
	assert isinstance(expression, MathMLElement)

RSS
---

RSS helpers include namespaced constructors for common feed extensions such as
Atom, Dublin Core, Media RSS, content, and syndication metadata.

.. code-block :: python

	import domonic.xml.rss as rss

	feed = rss.rss(
		rss.channel(
			rss.title("domonic updates"),
			rss.atom_link(_href="https://example.com/feed.xml", _rel="self"),
		),
		xmlns_atom=rss.XMLNS_ATOM,
	)

Atom
----

Atom feeds use the same alias pattern as HTML/SVG: namespaced tags can be
constructed with Python-friendly names and are rendered with their XML names.

.. code-block :: python

	import domonic.xml.atom as atom

	feed = atom.feed(
		atom.title("domonic"),
		atom.link(_href="https://example.com/"),
		_xmlns=atom.XMLNS,
	)

ODF
---

ODF helpers cover common ``office:``, ``text:``, ``table:``, ``draw:``,
``style:``, ``fo:``, ``svg:``, and ``xlink:`` namespaced elements and
attributes.

.. code-block :: python

	import domonic.xml.odf as odf

	document = odf.office_document_content(
		odf.office_body(odf.office_text(odf.text_p("Hello ODF"))),
		xmlns_office=odf.OFFICE,
		xmlns_text=odf.TEXT,
	)

Examples
--------

See ``examples/mathml.py``, ``examples/rss_feed.py``, ``examples/atom_feed.py``,
and ``examples/odf_content.py`` for complete renderable files.

