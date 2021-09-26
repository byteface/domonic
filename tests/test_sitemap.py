"""
    test_sitemap
    ~~~~~~~~~~~~
"""

import unittest
# import requests
# from mock import patch

from datetime import datetime

from domonic import domonic
from domonic.xml.sitemap import *
from domonic.decorators import silence


class TestCase(unittest.TestCase):

    # @silence
    def test_sitemap(self):

        # a sitemap index contains a list of sitemaps .i.e
        doc = sitemapindex(
            sitemap(
                loc('https://x.net/egypt/post-sitemap.xml'),
                lastmod('2021-07-08T13:12:16+00:00')
            )
        )

        print(doc)
        print(str(doc))

        doc = sitemap(
            url(
                loc('https://xyz.net'),
                lastmod('2021-07-08T13:12:16+00:00'),  # pass a date as string. if no data is passed the current date is used
                changefreq('weekly'),
                priority(0.5)
            )
        )

        print(doc)
        print(str(doc))

    def test_sitemapindex(self):

        from domonic.xml.sitemap import sitemapindex, sitemap, url, urlset

        # sm = sitemapindex()
        # sm.addChild(sitemap(loc('https://abd.net/sitemap1.xml'), lastmod(datetime.datetime.now())))
        # sm.addChild(sitemap(loc('https://abd.net/sitemap2.xml'), lastmod(datetime.datetime.now())))
        # sm.addChild(sitemap(loc('https://abd.net/sitemap3.xml'), lastmod(datetime.datetime.now())))

        # print(f"{sm!s}")
        # print(f"{sm!r}")

        sm = sitemapindex()
        sm += sitemap(loc('https://abd.net/sitemap1.xml'), lastmod(str(datetime.datetime.now())))
        sm += sitemap(loc('https://abd.net/sitemap2.xml'), lastmod(str(datetime.datetime.now())))
        sm += sitemap(loc('https://abd.net/sitemap3.xml'), lastmod(str(datetime.datetime.now())))

        print(f"{sm!s}")
        print(f"{sm!r}")
        # print(f"{sm!a}")
        print(f"{sm}")

    @silence
    def test_loadsitemap(self):
        from domonic.xml.sitemap import get_sitemap
        # sm = get_sitemap('https://x.net/sitemap.xml')
        sm = get_sitemap('https://x.net/merchants/ar/sitemap_index.xml')
        print(sm)

    @silence
    def test_parse_sitemapindex(self):
        # pass
        # https://x.net/merchants/ar/page-sitemap.xml
        from domonic.xml.sitemap import get_sitemap
        sm = get_sitemap('https://x.net/merchants/ar/page-sitemap.xml')
        print(sm)
        # pass

    @silence
    def test_element_class(self):
        # could the existing framework have been used. i.e.
        # from domonic.dom import Document
        # sitemapindex = Document.createElement('sitemapindex') # TODO - should createElementClass be a method of domonic Document?
        pass


if __name__ == '__main__':
    unittest.main()
