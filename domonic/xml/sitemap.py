"""
    domonic.sitemap
    ====================================

    generate or load sitemaps

    warning - when using image and video tags from this package they will be namespaced i.e <image:image> and <video:video>
    so i'd advise to only import them within the def that you use them in to avoid conflict with html.image

"""

import datetime

from domonic.dom import Element, Document

# __all__ = ['sitemap', 'url', 'lastmod']

sitemap_tags = ["sitemapindex", "sitemap", "urlset", "url", "loc", "lastmod", "changefreq", "priority",
                "image:image", "image:loc"]

sitemap_attributes = ["xmlns", "xmlns:xsi", "xsi:schemaLocation",
                      "xmlns:xhtml", "xmlns:xlink", "xmlns:atom", "xmlns:geo"]
# sitemap_change_frequencies = ['always', 'hourly', 'daily', 'weekly', 'monthly', 'yearly', 'never']

XMLNS: str = 'http://www.sitemaps.org/schemas/sitemap/0.9'
XMLNS_XSI: str = 'http://www.w3.org/2001/XMLSchema-instance'
SCHEMA_SITEINDEX: str = 'http://www.sitemaps.org/schemas/sitemap/0.9/siteindex.xsd'
SCHEMA_SITEMAP: str = 'http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd'
#     xmlns="http://www.google.com/schemas/sitemap-image/1.1"
#     xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">


def sitemap_format(self, *args, **kwargs):
    """ attempts to prettify the output of the sitemap. """
    outp = f"<{self.name}{self.__attributes__}>{self.content}</{self.name}>"
    from domonic.xml import prettify
    return prettify(outp)


sitemapindex = type('sitemapindex', (Document,), {
    'name': 'sitemapindex',
    'xmlns': XMLNS,
    'xmlns:xsi': XMLNS_XSI,
    'xsi:schemaLocation': SCHEMA_SITEINDEX,
    '__format__': sitemap_format})

sitemap = type('sitemap', (Element,), {'name': 'sitemap'})

urlset = type('urlset', (Element,), {
    'name': 'urlset',
    'xmlns:xsi': XMLNS_XSI,
    'xsi:schemaLocation': SCHEMA_SITEMAP,
    'xmlns': XMLNS})


url = type('url', (Element,), {'name': 'url'})
loc = type('loc', (Element,), {'name': 'loc'})
lastmod = type('lastmod', (Element,), {'name': 'lastmod'})
changefreq = type('changefreq', (Element,), {'name': 'changefreq'})
priority = type('priority', (Element,), {'name': 'priority'})


def sitemapindex_from_urls(urls):
    """
    Create a sitemap index from a list of urls.

    WARNING:
    there's a difference between a sitemap index and a sitemap.
    make sure you know what you want.

    # i.e

    # <?xml version="1.0" encoding="UTF-8"?>
    # <sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    # 	<sitemap>
    # 		<loc>https://xyz.com/sitemap1.xml</loc>
    # 		<lastmod>2021-07-08T13:12:16+00:00</lastmod>
    # 	</sitemap>
    # </sitemapindex>

    """
    sitemap_index = sitemapindex()
    for url in urls:
        sitemap_index.append(sitemap(loc(url), lastmod(datetime.datetime.now())))


def sitemap_from_urls(urls):
    """
    Create a sitemap from a list of urls.add()

    Note: This won't allow you to add priority or changefreq of the urls. or add images etc
    tho u could loop the nodes afterwards and do that.

    WARNING:
    there's a difference between a sitemap index and a sitemap.
    make sure you know what you want.

    """
    sitemap = urlset()
    for url in urls:
        sitemap.append(url(loc(url), lastmod(datetime.datetime.now())))
    return sitemap


def get_sitemap(path: str, *args, **kwargs):
    # use requests to downlaod a sitemap
    import requests
    r = requests.get(path)
    import domonic
    some_sitemap = domonic.domonic.parseString(r.text)
    return some_sitemap


globals()['image:image'] = type('image:image', (Element,), {
    'name': 'image',
    'ns': 'image'})

globals()['image:loc'] = type('image:loc', (Element,), {
    'name': 'loc',
    'ns': 'image'})
