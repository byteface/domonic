"""
    test_sitemap
    ~~~~~~~~~~~~
"""

import unittest
from datetime import datetime

from domonic import domonic
from domonic.decorators import silence
from domonic.xml.sitemap import *


class TestCase(unittest.TestCase):

    # @silence
    def test_sitemap(self):

        # a sitemap index contains a list of sitemaps .i.e
        doc = sitemapindex(sitemap(loc("https://x.net/egypt/post-sitemap.xml"), lastmod("2021-07-08T13:12:16+00:00")))

        print(doc)
        print(str(doc))

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

        print(doc)
        print(str(doc))

    def test_sitemapindex(self):

        from domonic.xml.sitemap import sitemap, sitemapindex, url, urlset

        # sm = sitemapindex()
        # sm.addChild(sitemap(loc('https://abd.net/sitemap1.xml'), lastmod(datetime.datetime.now())))
        # sm.addChild(sitemap(loc('https://abd.net/sitemap2.xml'), lastmod(datetime.datetime.now())))
        # sm.addChild(sitemap(loc('https://abd.net/sitemap3.xml'), lastmod(datetime.datetime.now())))
        # print(f"{sm!s}")
        # print(f"{sm!r}")

        sm = sitemapindex()
        sm += sitemap(loc("https://abd.net/sitemap1.xml"), lastmod(str(datetime.datetime.now())))
        sm += sitemap(loc("https://abd.net/sitemap2.xml"), lastmod(str(datetime.datetime.now())))
        sm += sitemap(loc("https://abd.net/sitemap3.xml"), lastmod(str(datetime.datetime.now())))

        print(f"{sm!s}")
        print(f"{sm!r}")
        # print(f"{sm!a}")
        print(f"{sm}")


    def test_namespaced_tags(self):
        self.assertEqual(str(globals()["image:image"]()), '<image:image></image:image>')
        self.assertEqual(str(globals()["image:loc"]()), '<image:loc></image:loc>')
        self.assertEqual(str(globals()["image:caption"]()), '<image:caption></image:caption>')
        self.assertEqual(str(globals()["image:title"]()), '<image:title></image:title>')
        self.assertEqual(str(globals()["image:geo_location"]()), '<image:geo_location></image:geo_location>')
        self.assertEqual(str(globals()["image:license"]()), '<image:license></image:license>')

        self.assertEqual(str(create_ns_element("image:image")), '<image:image></image:image>')
        self.assertEqual(str(create_ns_element("image:loc")), '<image:loc></image:loc>')
        self.assertEqual(str(create_ns_element("image:title")), '<image:title></image:title>')
        self.assertEqual(str(create_ns_element("image:caption")), '<image:caption></image:caption>')
        self.assertEqual(str(create_ns_element("image:geo_location")), '<image:geo_location></image:geo_location>')
        self.assertEqual(str(create_ns_element("image:license")), '<image:license></image:license>')

        # Testing other namespaces (video, news, geo, atom, xhtml, mobile)
        self.assertEqual(str(globals()["video:video"]()), '<video:video></video:video>')
        self.assertEqual(str(globals()["video:title"]()), '<video:title></video:title>')
        self.assertEqual(str(globals()["news:news"]()), '<news:news></news:news>')
        self.assertEqual(str(globals()["geo:geo"]()), '<geo:geo></geo:geo>')
        self.assertEqual(str(globals()["atom:link"]()), '<atom:link></atom:link>')
        self.assertEqual(str(globals()["xhtml:link"]()), '<xhtml:link></xhtml:link>')
        self.assertEqual(str(globals()["mobile:mobile"]()), '<mobile:mobile></mobile:mobile>')


    @silence
    def test_loadsitemap(self):
        from domonic.xml.sitemap import get_sitemap

        # sm = get_sitemap('https://x.net/sitemap.xml')
        sm = get_sitemap("https://x.net/merchants/ar/sitemap_index.xml")
        print(sm)


    @silence
    def test_parse_sitemapindex(self):
        # pass
        # https://x.net/merchants/ar/page-sitemap.xml
        from domonic.xml.sitemap import get_sitemap

        sm = get_sitemap("https://x.net/merchants/ar/page-sitemap.xml")
        print(sm)
        # pass

    @silence
    def test_element_class(self):
        # could the existing framework have been used. i.e.
        # from domonic.dom import Document
        # sitemapindex = Document.createElement('sitemapindex') # TODO - should createElementClass be a method of domonic Document?
        pass


if __name__ == "__main__":
    unittest.main()
