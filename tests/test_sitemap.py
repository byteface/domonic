"""
test_sitemap
~~~~~~~~~~~~
"""

import unittest
from datetime import datetime
from unittest.mock import patch

from domonic import domonic
from domonic.decorators import silence
from domonic.xml.sitemap import *


def _debug_print(*args, **kwargs):
    return None


class TestCase(unittest.TestCase):

    # @silence
    def test_sitemap(self):

        # a sitemap index contains a list of sitemaps .i.e
        doc = sitemapindex(
            sitemap(
                loc("https://x.net/egypt/post-sitemap.xml"),
                lastmod("2021-07-08T13:12:16+00:00"),
            )
        )

        _debug_print(doc)
        _debug_print(str(doc))

        doc = sitemap(
            url(
                loc("https://xyz.net"),
                lastmod(
                    "2021-07-08T13:12:16+00:00"
                ),  # pass a date as string. if no data is passed the current date is used
                changefreq("weekly"),
                priority(0.5),
            )
        )

        _debug_print(doc)
        _debug_print(str(doc))

    def test_sitemapindex(self):

        from domonic.xml.sitemap import sitemap, sitemapindex, url, urlset

        # sm = sitemapindex()
        # sm.addChild(sitemap(loc('https://abd.net/sitemap1.xml'), lastmod(datetime.datetime.now())))
        # sm.addChild(sitemap(loc('https://abd.net/sitemap2.xml'), lastmod(datetime.datetime.now())))
        # sm.addChild(sitemap(loc('https://abd.net/sitemap3.xml'), lastmod(datetime.datetime.now())))
        # print(f"{sm!s}")
        # print(f"{sm!r}")

        sm = sitemapindex()
        sm += sitemap(
            loc("https://abd.net/sitemap1.xml"), lastmod(str(datetime.datetime.now()))
        )
        sm += sitemap(
            loc("https://abd.net/sitemap2.xml"), lastmod(str(datetime.datetime.now()))
        )
        sm += sitemap(
            loc("https://abd.net/sitemap3.xml"), lastmod(str(datetime.datetime.now()))
        )

        _debug_print(f"{sm!s}")
        _debug_print(f"{sm!r}")
        # print(f"{sm!a}")
        _debug_print(f"{sm}")

    def test_namespaced_tags(self):
        self.assertEqual(str(globals()["image:image"]()), "<image:image></image:image>")
        self.assertEqual(str(globals()["image:loc"]()), "<image:loc></image:loc>")
        self.assertEqual(
            str(globals()["image:caption"]()), "<image:caption></image:caption>"
        )
        self.assertEqual(str(globals()["image:title"]()), "<image:title></image:title>")
        self.assertEqual(
            str(globals()["image:geo_location"]()),
            "<image:geo_location></image:geo_location>",
        )
        self.assertEqual(
            str(globals()["image:license"]()), "<image:license></image:license>"
        )

        self.assertEqual(
            str(create_ns_element("image:image")), "<image:image></image:image>"
        )
        self.assertEqual(str(create_ns_element("image:loc")), "<image:loc></image:loc>")
        self.assertEqual(
            str(create_ns_element("image:title")), "<image:title></image:title>"
        )
        self.assertEqual(
            str(create_ns_element("image:caption")), "<image:caption></image:caption>"
        )
        self.assertEqual(
            str(create_ns_element("image:geo_location")),
            "<image:geo_location></image:geo_location>",
        )
        self.assertEqual(
            str(create_ns_element("image:license")), "<image:license></image:license>"
        )

        # Testing other namespaces (video, news, geo, atom, xhtml, mobile)
        self.assertEqual(str(globals()["video:video"]()), "<video:video></video:video>")
        self.assertEqual(str(globals()["video:title"]()), "<video:title></video:title>")
        self.assertEqual(str(globals()["news:news"]()), "<news:news></news:news>")
        self.assertEqual(str(globals()["geo:geo"]()), "<geo:geo></geo:geo>")
        self.assertEqual(str(globals()["atom:link"]()), "<atom:link></atom:link>")
        self.assertEqual(str(globals()["xhtml:link"]()), "<xhtml:link></xhtml:link>")
        self.assertEqual(
            str(globals()["mobile:mobile"]()), "<mobile:mobile></mobile:mobile>"
        )

    @silence
    def test_loadsitemap(self):
        from domonic.xml.sitemap import get_sitemap

        xml = """<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://x.net/merchants/ar/page-sitemap.xml</loc>
    <lastmod>2021-07-08T13:12:16+00:00</lastmod>
  </sitemap>
</sitemapindex>"""
        with patch("domonic.xml.sitemap._get_sitemap_text", return_value=xml):
            sm = get_sitemap("https://x.net/merchants/ar/sitemap_index.xml")
        _debug_print(sm)
        self.assertIsNotNone(sm)
        self.assertIn(getattr(sm, "tagName", None), ("sitemapindex", "xml", "html"))
        if getattr(sm, "tagName", None) in ("xml", "html"):
            self.assertEqual(len(sm.getElementsByTagName("sitemapindex")), 1)
        self.assertEqual(len(sm.getElementsByTagName("sitemap")), 1)

    @silence
    def test_parse_sitemapindex(self):
        from domonic.xml.sitemap import get_sitemap

        xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://x.net/merchants/ar/example</loc>
    <lastmod>2021-07-08T13:12:16+00:00</lastmod>
  </url>
</urlset>"""
        with patch("domonic.xml.sitemap._get_sitemap_text", return_value=xml):
            sm = get_sitemap("https://x.net/merchants/ar/page-sitemap.xml")
        _debug_print(sm)
        self.assertIsNotNone(sm)
        self.assertIn(getattr(sm, "tagName", None), ("urlset", "xml", "html"))
        if getattr(sm, "tagName", None) in ("xml", "html"):
            self.assertEqual(len(sm.getElementsByTagName("urlset")), 1)
        self.assertEqual(len(sm.getElementsByTagName("url")), 1)

    @silence
    def test_element_class(self):
        index = sitemapindex(
            sitemap(
                loc("https://example.com/sitemap.xml"),
                lastmod("2026-08-28T00:00:00+00:00"),
            )
        )
        urls = urlset(
            url(
                loc("https://example.com/"),
                changefreq("daily"),
                priority(1.0),
            )
        )

        self.assertEqual(index.tagName, "sitemapindex")
        self.assertEqual(index.querySelector("loc").text, "https://example.com/sitemap.xml")
        self.assertIn("<sitemapindex", str(index))

        self.assertEqual(urls.tagName, "urlset")
        self.assertEqual(urls.querySelector("changefreq").text, "daily")
        self.assertIn("<priority>1.0</priority>", str(urls))


if __name__ == "__main__":
    unittest.main()
