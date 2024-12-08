"""
    domonic.sitemap
    ====================================

    generate or load sitemaps

    warning - when using image and video tags from this package they will be namespaced i.e <image:image> and <video:video>
    so i'd advise to only import them within the def that you use them in to avoid conflict with html.image

"""

import datetime

from domonic.dom import Document, Element

# __all__ = ['sitemap', 'url', 'lastmod']

sitemap_tags = [
    "sitemapindex",
    "sitemap",
    "urlset",
    "url",
    "loc",
    "lastmod",
    "changefreq",
    "priority",
    "image:image",
    "image:loc",
    "image:caption",
    "image:title",
    "image:geo_location",
    "image:license",
    "video:video",
    "video:loc",
    "video:caption",
    "video:title",
    "video:thumbnail_loc",
    "geo:geo",
    "geo:location",
    "atom:entry",
    "atom:link",
    "xhtml:link",
    "mobile:mobile"
]

sitemap_attributes = [
    "xmlns",
    "xmlns:xsi",
    "xsi:schemaLocation",
    "xmlns:xhtml",
    "xmlns:xlink",
    "xmlns:atom",
    "xmlns:geo",
]
# sitemap_change_frequencies = ['always', 'hourly', 'daily', 'weekly', 'monthly', 'yearly', 'never']

XMLNS: str = "http://www.sitemaps.org/schemas/sitemap/0.9"
XMLNS_XSI: str = "http://www.w3.org/2001/XMLSchema-instance"
SCHEMA_SITEINDEX: str = "http://www.sitemaps.org/schemas/sitemap/0.9/siteindex.xsd"
SCHEMA_SITEMAP: str = "http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd"
#     xmlns="http://www.google.com/schemas/sitemap-image/1.1"
#     xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">


def sitemap_format(self, *args, **kwargs):
    """attempts to prettify the output of the sitemap."""
    outp = f"<{self.name}{self.__attributes__}>{self.content}</{self.name}>"
    from domonic.xml import prettify

    return prettify(outp)


sitemapindex = type(
    "sitemapindex",
    (Document,),
    {
        "name": "sitemapindex",
        "xmlns": XMLNS,
        "xmlns:xsi": XMLNS_XSI,
        "xsi:schemaLocation": SCHEMA_SITEINDEX,
        "__format__": sitemap_format,
    },
)

sitemap = type("sitemap", (Element,), {"name": "sitemap"})

urlset = type(
    "urlset",
    (Element,),
    {
        "name": "urlset",
        "xmlns:xsi": XMLNS_XSI,
        "xsi:schemaLocation": SCHEMA_SITEMAP,
        "xmlns": XMLNS,
    },
)


url = type("url", (Element,), {"name": "url"})
loc = type("loc", (Element,), {"name": "loc"})
lastmod = type("lastmod", (Element,), {"name": "lastmod"})
changefreq = type("changefreq", (Element,), {"name": "changefreq"})
priority = type("priority", (Element,), {"name": "priority"})


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
    """ 
    Download a sitemap
    """
    import requests

    r = requests.get(path)
    import domonic

    some_sitemap = domonic.domonic.parseString(r.text)
    return some_sitemap


# image
image_image = globals()["image:image"] = type("image:image", (Element,), {"name": "image:image", "ns": "image"})
image_loc = globals()["image:loc"] = type("image:loc", (Element,), {"name": "image:loc", "ns": "image"})
image_caption = globals()["image:caption"] = type("image:caption", (Element,), {"name": "image:caption", "ns": "image"})
image_title = globals()["image:title"] = type("image:title", (Element,), {"name": "image:title", "ns": "image"})
image_geo_location = globals()["image:geo_location"] = type("image:geo_location", (Element,), {"name": "image:geo_location", "ns": "image"})
image_license = globals()["image:license"] = type("image:license", (Element,), {"name": "image:license", "ns": "image"})

# video
video_video = globals()["video:video"] = type("video:video", (Element,), {"name": "video:video", "ns": "video"})
video_content_loc = globals()["video:content_loc"] = type("video:content_loc", (Element,), {"name": "video:content_loc", "ns": "video"})
video_thumbnail_loc = globals()["video:thumbnail_loc"] = type("video:thumbnail_loc", (Element,), {"name": "video:thumbnail_loc", "ns": "video"})
video_title = globals()["video:title"] = type("video:title", (Element,), {"name": "video:title", "ns": "video"})
video_description = globals()["video:description"] = type("video:description", (Element,), {"name": "video:description", "ns": "video"})
video_duration = globals()["video:duration"] = type("video:duration", (Element,), {"name": "video:duration", "ns": "video"})
video_publication_date = globals()["video:publication_date"] = type("video:publication_date", (Element,), {"name": "video:publication_date", "ns": "video"})
video_tags = globals()["video:tags"] = type("video:tags", (Element,), {"name": "video:tags", "ns": "video"})
video_category = globals()["video:category"] = type("video:category", (Element,), {"name": "video:category", "ns": "video"})
video_rating = globals()["video:rating"] = type("video:rating", (Element,), {"name": "video:rating", "ns": "video"})
video_view_count = globals()["video:view_count"] = type("video:view_count", (Element,), {"name": "video:view_count", "ns": "video"})
video_price = globals()["video:price"] = type("video:price", (Element,), {"name": "video:price", "ns": "video"})
video_price_currency = globals()["video:price_currency"] = type("video:price_currency", (Element,), {"name": "video:price_currency", "ns": "video"})

# news
news_news = globals()["news:news"] = type("news:news", (Element,), {"name": "news:news", "ns": "news"})
news_publication_date = globals()["news:publication_date"] = type("news:publication_date", (Element,), {"name": "news:publication_date", "ns": "news"})
news_title = globals()["news:title"] = type("news:title", (Element,), {"name": "news:title", "ns": "news"})
news_keywords = globals()["news:keywords"] = type("news:keywords", (Element,), {"name": "news:keywords", "ns": "news"})
news_stock_tickers = globals()["news:stock_tickers"] = type("news:stock_tickers", (Element,), {"name": "news:stock_tickers", "ns": "news"})

# geo
geo_geo = globals()["geo:geo"] = type("geo:geo", (Element,), {"name": "geo:geo", "ns": "geo"})
geo_place_name = globals()["geo:place_name"] = type("geo:place_name", (Element,), {"name": "geo:place_name", "ns": "geo"})
geo_country = globals()["geo:country"] = type("geo:country", (Element,), {"name": "geo:country", "ns": "geo"})

# atom
atom_link = globals()["atom:link"] = type("atom:link", (Element,), {"name": "atom:link", "ns": "atom"})

# xhtml
xhtml_link = globals()["xhtml:link"] = type("xhtml:link", (Element,), {"name": "xhtml:link", "ns": "xhtml"})

# mobile
mobile_mobile = globals()["mobile:mobile"] = type("mobile:mobile", (Element,), {"name": "mobile:mobile", "ns": "mobile"})

def create_ns_element(tag_name, **attributes):
    """Factory function to create elements dynamically."""
    if tag_name in globals():
        return globals()[tag_name](**attributes)
    raise ValueError(f"Tag '{tag_name}' is not defined in globals().")
