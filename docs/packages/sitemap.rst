sitemap
=================

domonic can help create a sitemap or sitemap index for your website.

A sitemap contains URLs for your website. A sitemap index contains a list of sitemap files.

Below are examples of creating sitemaps with Python and domonic.

Creating a sitemap index
--------------------------------

A sitemap index contains a list of sitemaps. A minimal one might look something like this:

.. code-block :: xml

	<?xml version="1.0" encoding="UTF-8"?>
	<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
	<sitemap>
		<loc>http://www.example.com/sitemap1.xml.gz</loc>
		<lastmod>2004-10-01T18:23:17+00:00</lastmod>
	</sitemap>
	</sitemapindex>

With domonic, we can create one in a few different ways depending on our needs.

.. code-block :: python

	from domonic.html import render
	from domonic.xml.sitemap import lastmod, loc, sitemap, sitemapindex

	doc = sitemapindex(
 		sitemap(
			loc("https://xyz.net/sitemap1.xml"),
			lastmod("2021-07-08T13:12:16+00:00"),
     	)
	)

	render(f"{doc}", "sitemap.xml")


Creating a sitemap
--------------------------------

A sitemap contains URLs for your website and is limited to 50,000 URLs.

A minimal one might look something like this:

 .. code-block :: xml

	<?xml version="1.0" encoding="UTF-8"?>
	<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
	<url>
		<loc>https://xyz.net/</loc>
		<lastmod>2004-10-01T18:23:17+00:00</lastmod>
		<changefreq>monthly</changefreq>
		<priority>0.8</priority>
	</url>
	</urlset>

With domonic, we can create one in a few different ways depending on our needs.

.. code-block :: python

	from domonic.html import render
	from domonic.xml.sitemap import changefreq, lastmod, loc, priority, url, urlset

	doc = urlset(
		url(
			loc("https://xyz.net"),
			lastmod("2021-07-08T13:12:16+00:00"),
			changefreq("weekly"),
			priority(0.5),
		)
	)

	# Use an f-string to prettify the document.
	render(f"{doc}", "sitemap1.xml")


utils
----------------

domonic also has helpers for quickly creating sitemaps with default values.

.. code-block :: python

	mypages = []
	sm = sitemap_from_urls(mypages)
	print(sm)


You will often want a little more control, so use any DOM manipulation methods you like.

Here's some more examples.


Creating a sitemap from scratch
-------------------------------

.. code-block :: python

	sm = urlset()
	sm += url(loc('https://abc.net/sitemap.xml'), lastmod('2020-07-08T13:12:16+00:00'))

	print(sm)


Namespaced tags
----------------

There are a few options for creating namespaced tags such as ``image:image``, ``image:loc``, and ``image:caption``.

Use ``globals()`` to get them by name, because ``:`` is not valid in Python variable names:

.. code-block :: python

	str(globals()["image:license"]())  # returns '<image:license></image:license>'

Or use ``create_ns_element``:

.. code-block :: python

	from domonic.xml.sitemap import create_ns_element

	vt = create_ns_element("video:title")
	print(str(vt))

You can also use an underscore instead of a colon.

.. code-block :: python

	from domonic.xml.sitemap import *
	print(geo_placename())


Formatting
----------------

You can format with the normal Python methods recognized by domonic:

.. code-block :: python

	print(f"{sm}")    # Calls __format__ and prettifies the XML.
	print(f"{sm!s}")  # Calls str without prettifying.
	print(f"{sm!r}")  # Shows the object repr.
	# print(f"{sm!a}")
	


More
----------------

For more information on sitemaps, see:

https://www.sitemaps.org/protocol.html


.. automodule:: domonic.xml.sitemap
   :members:
   :noindex:
   :exclude-members: image:image, image:loc, image:caption, image:title, image:geo_location, image:license
