sitemap
=================

domonic can help create a sitemap or sitemapindex for your website.

A sitemap contains a list of urls for your website. Whereas a sitemap index contains a list of sitemaps.

You can see below How to make sitemaps with python and domonic.

creating a sitemapindex
--------------------------------

A sitemap index contains a list of sitemaps. A minimal one might look something like this:

.. code-block :: xml

	'<?xml version="1.0" encoding="UTF-8"?>'
	<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
	<sitemap>
		<loc>http://www.example.com/sitemap1.xml.gz</loc>
		<lastmod>2004-10-01T18:23:17+00:00</lastmod>
	</sitemap>
	</sitemapindex>

With domonic we can create one in a number ways depending on our needs.

.. code-block :: python

	from domonic.xml.sitemap import sitemapindex, sitemap, url, loc, lastmod, changefreq, priority

	doc = sitemapindex(
 		sitemap(
			loc(https://xyz.net/sitemap1.xml)
			lastmod('2021-07-08T13:12:16+00:00')  # pass a date as string. if no data is passed the current date is used
     	)
	)

	render(f"{doc}", 'sitemap.xml')


Create a sitemap
--------------------------------

A sitemap contains a list of urls for your website and is limited to 50,000 urls.

A minimal one might look something like this:

 .. code-block :: xml

	'<?xml version="1.0" encoding="UTF-8"?>'
	<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
	<url>
		<loc>https://xyz.net/</loc>
		<lastmod>2004-10-01T18:23:17+00:00</lastmod>
		<changefreq>monthly</changefreq>
		<priority>0.8</priority>
	</url>
	</urlset>

With domonic we can create one in a number ways depending on our needs.

.. code-block :: python

	from domonic.xml.sitemap import sitemapindex, sitemap, url, loc, lastmod, changefreq, priority

	doc = urlset(
		url(
			loc('https://xyz.net')
			lastmod('2021-07-08T13:12:16+00:00')  # pass a date as string. if no data is passed the current date is used
			changefreq('weekly')
			priority(0.5)
		)
	)

	# use f-string to call format on the doc to prettify
	render(f"{doc}", 'sitemap1.xml')


utils
----------------

domonic also has some utils for quickly creating sitemaps with default values.

.. code-block :: python

	mypages = []
	sm = sitemap_from_urls(mypages)
	print(sm)


but you will likely want a little more control. So use any dom manipulating methods you like.

Here's some more examples.


## creating a sitemap from scratch

.. code-block :: python

	sm = urlset()
	sm += url(loc('https://abc.net/sitemap.xml'), lastmod('2020-07-08T13:12:16+00:00'))

	print(sm)


formatting
----------------

You can format with following normal python methods which are regonised by domonic:

.. code-block :: python

	print(f"{sm}") # f string will call __format__ and run through a prettify
	print(f"{sm!s}") # str will not be prettified
	print(f"{sm!r}") # r show the ojbect as a repr
	# print(f"{sm!a}")
	


more
----------------

For more infor on sitemaps see...

https://www.sitemaps.org/protocol.html



.. automodule:: domonic.xml.sitemap
    :members:
    :noindex:
