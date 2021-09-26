"""
    domonic.sitemap
    ====================================

    generate or load sitemaps

    warning - when using image and video tags from this package they will be namespaced i.e <image:image> and <video:video>
    so i'd advise to only import them within the def that you use them in to avoid conflict with html.image

"""

import datetime

from domonic.html import tag  # , closed_tag
from domonic.dom import Element, Document

# __all__ = ['sitemap', 'url', 'lastmod']

sitemap_tags = ["sitemapindex", "sitemap", "urlset", "url", "loc", "lastmod", "changefreq", "priority", 
                "image:image", "image:loc"]

sitemap_attributes = ["xmlns", "xmlns:xsi", "xsi:schemaLocation",
                      "xmlns:xhtml", "xmlns:xlink", "xmlns:atom", "xmlns:geo"]
# sitemap_change_frequencies = ['always', 'hourly', 'daily', 'weekly', 'monthly', 'yearly', 'never']

XMLNS = 'http://www.sitemaps.org/schemas/sitemap/0.9'
XMLNS_XSI = 'http://www.w3.org/2001/XMLSchema-instance'
SCHEMA_SITEINDEX = 'http://www.sitemaps.org/schemas/sitemap/0.9/siteindex.xsd'
SCHEMA_SITEMAP = 'http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd'
#     xmlns="http://www.google.com/schemas/sitemap-image/1.1"
#     xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">


def sitemap_init(self, *args, **kwargs):
    tag.__init__(self, *args, **kwargs)
    Element.__init__(self, *args, **kwargs)


def sitemap_format(self, *args, **kwargs):
    """ attempts to prettify the output of the sitemap. """
    outp = f"<{self.name}{self.__attributes__}>{self.content}</{self.name}>"
    from domonic.xml import prettify
    return prettify(outp)


sitemapindex = type('sitemapindex', (tag, Document), {
    'name': 'sitemapindex',
    'xmlns': XMLNS,
    'xmlns:xsi': XMLNS_XSI,
    'xsi:schemaLocation': SCHEMA_SITEINDEX,
    '__init__': sitemap_init,
    '__format__': sitemap_format})

sitemap = type('sitemap', (tag, Element), {'name': 'sitemap', '__init__': sitemap_init})

urlset = type('urlset', (tag, Element), {
    'name': 'urlset',
    'xmlns:xsi': XMLNS_XSI,
    'xsi:schemaLocation': SCHEMA_SITEMAP,
    'xmlns': XMLNS,
    '__init__': sitemap_init})


def url_init(self, *args, **kwargs):
    # validate kwargs
    # if 'xmlns' in kwargs:
    #     if kwargs['xmlns'] not in sitemap_attributes:
    #         raise ValueError("xmlns attribute not valid")
    # if 'lastmod' in kwargs:
    #     if not isinstance(kwargs['lastmod'], datetime.datetime):
    #         raise ValueError("lastmod must be a datetime object")
    # else:
    #     kwargs['lastmod'] = datetime.datetime.now()

    # if lastmod is a datetime convert it to an lastmod object
    # if 'lastmod' in kwargs:
    #     if not isinstance(kwargs['lastmod'], datetime.datetime):
    #         kwargs['lastmod'] = lastmod(datetime.datetime.now())
    #     else:
    #         kwargs['lastmod'] = lastmod(kwargs['lastmod'])

    # if 'priority' in kwargs:
    #     if kwargs['priority'] not in range(0, 1):
    #         raise ValueError("priority must be between 0 and 1")

    # if 'changefreq' in kwargs:
    #     if kwargs['changefreq'] not in ('always', 'hourly', 'daily', 'weekly', 'monthly', 'yearly', 'never'):
    #         raise ValueError("changefreq must be one of: always, hourly, daily, weekly, monthly, yearly, never")

    # if 'loc' in kwargs:
    #     if not isinstance(kwargs['loc'], str):
    #         raise ValueError("loc must be a string")
        # escape the loc string ?
        # kwargs['loc'] = kwargs['loc'].replace('&', '&amp;')
        # kwargs['loc'] = kwargs['loc'].replace('<', '&lt;')
        # kwargs['loc'] = kwargs['loc'].replace('>', '&gt;')
        # kwargs['loc'] = kwargs['loc'].replace('"', '&quot;')
        # kwargs['loc'] = kwargs['loc'].replace("'", '&apos;')

    tag.__init__(self, *args, **kwargs)
    Element.__init__(self, *args, **kwargs)


url = type('url', (tag, Element), {
    'name': 'url',
    # loc = loc
    # lastmod = lastmod
    # changefreq = changefreq
    # priority = priority
    '__init__': sitemap_init})

loc = type('loc', (tag, Element), {'name': 'loc', '__init__': sitemap_init})
lastmod = type('lastmod', (tag, Element), {'name': 'lastmod', '__init__': sitemap_init})
changefreq = type('changefreq', (tag, Element), {'name': 'changefreq', '__init__': sitemap_init})
priority = type('priority', (tag, Element), {'name': 'priority', '__init__': sitemap_init})


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
    # if r.status_code == 200:
    #     return r.text
    # else:
    #     raise ValueError("Could not get sitemap")

    import domonic
    some_sitemap = domonic.domonic.parseString(r.text)
    # print('RES:', some_sitemap)
    # print('RES:', type(some_sitemap))
    # print('RES:', str(some_sitemap))
    # print( some_sitemap.getElementByTagName('sitemap') )
    # return some_sitemap
    return some_sitemap


# def submit_sitemap(sitemap_url: str, search_engine_url: str):
#     """
#     submit a sitemap to a search engine.

#     """
#     import requests
#     r = requests.get(search_engine_url + '/ping?sitemap=' + sitemap_url)
#     print(r.text)



# a regular site map

# <?xml version="1.0" encoding="UTF-8"?>
# <?xml-stylesheet type="text/xsl" href="seo/css/main-sitemap.xsl"?>
# <urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
# xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" 
# xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd http://www.google.com/schemas/sitemap-image/1.1 http://www.google.com/schemas/sitemap-image/1.1/sitemap-image.xsd" 
# xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
	# <url>


# note on namespaces

# <image:image>
# <image:image>

# represent that image node as a python class?
# image(_namespace="http://www.google.com/schemas/sitemap-image/1.1", )

globals()['image:image'] = type('image:image', (tag, Element), {
    'name': 'image',
    'ns': 'image',
    '__init__': sitemap_init})

globals()['image:loc'] = type('image:loc', (tag, Element), {
    'name': 'loc',
    'ns': 'image',
    '__init__': sitemap_init})


#image tag example

# <urlset
#     xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
#     xmlns="http://www.google.com/schemas/sitemap-image/1.1"
#     xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">
    #     <image:image>
    #       <image:loc>http://e.com/img.png</image:loc>
    #       <image:caption>Stunning Men's Hats</image:caption>
    #       <image:geo_location>Boise, Idaho, USA</image:geo_location>
    #       <image:title>Men's Hat Image</image:title>
    #    </image:image>
# </urlset>
