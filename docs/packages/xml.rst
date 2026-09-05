xml
===

.. meta::
   :description: Generate XML, RSS, Atom, ODF, MathML and namespaced XML documents with Python using domonic.
   :keywords: Python XML, RSS feed Python, Atom feed Python, ODF XML Python, MathML Python, namespaced XML, XML generator

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
	print(expression)
	# <math><mrow><mi>x</mi><mo>=</mo><mn>1</mn></mrow></math>

RSS
---

RSS helpers include namespaced constructors for common feed extensions such as
Atom, Dublin Core, Media RSS, content, and syndication metadata.

.. code-block :: python

	import domonic.xml.rss as rss

	feed = rss.rss(
		rss.channel(
			rss.title("domonic updates"),
			rss.description("Python DOM, HTML, SVG, XML and Web API releases"),
			rss.link("https://example.com/"),
			rss.atom_link(_href="https://example.com/feed.xml", _rel="self"),
		),
		xmlns_atom=rss.XMLNS_ATOM,
	)
	print(feed)
	# <rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel><title>domonic updates</title><description>Python DOM, HTML, SVG, XML and Web API releases</description><link>https://example.com/</link><atom:link href="https://example.com/feed.xml" rel="self"></atom:link></channel></rss>

Atom
----

Atom feeds use the same alias pattern as HTML/SVG: namespaced tags can be
constructed with Python-friendly names and are rendered with their XML names.

.. code-block :: python

	import domonic.xml.atom as atom

	feed = atom.feed(
		atom.title("domonic"),
		atom.link(_href="https://example.com/"),
		atom.updated("2026-08-30T00:00:00Z"),
		_xmlns=atom.XMLNS,
	)
	print(feed)
	# <feed xmlns="http://www.w3.org/2005/Atom"><title>domonic</title><link href="https://example.com/"></link><updated>2026-08-30T00:00:00Z</updated></feed>

ODF
---

ODF helpers cover common ``office:``, ``text:``, ``table:``, ``draw:``,
``style:``, ``fo:``, ``svg:``, and ``xlink:`` namespaced elements and
attributes.

.. code-block :: python

	import domonic.xml.odf as odf

	# office_document_content already declares every odf:* namespace it needs,
	# so there's no need to pass xmlns_office / xmlns_text kwargs yourself.
	document = odf.office_document_content(
		odf.office_body(odf.office_text(odf.text_p("Hello ODF"))),
	)
	print(document)
	# <office:document-content xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" ...><office:body><office:text><text:p>Hello ODF</text:p></office:text></office:body></office:document-content>

Namespaced Attributes
---------------------

Python keyword arguments cannot contain ``:`` or ``-``, so use explicit
``**{...}`` dictionaries for exact XML attribute names when needed.

.. code-block :: python

	import domonic.xml.rss as rss

	enclosure = rss.enclosure(
		**{
			"_url": "https://example.com/audio.mp3",
			"_type": "audio/mpeg",
			"_length": "12345",
		}
	)
	print(enclosure)
	# <enclosure url="https://example.com/audio.mp3" type="audio/mpeg" length="12345"></enclosure>

Examples
--------

- :doc:`../guides/examples`
- `examples/mathml.py <https://github.com/byteface/domonic/blob/master/examples/mathml.py>`_
- `examples/rss_feed.py <https://github.com/byteface/domonic/blob/master/examples/rss_feed.py>`_
- `examples/atom_feed.py <https://github.com/byteface/domonic/blob/master/examples/atom_feed.py>`_
- `examples/odf_content.py <https://github.com/byteface/domonic/blob/master/examples/odf_content.py>`_
