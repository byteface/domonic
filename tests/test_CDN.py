"""
    test_domonic
    ~~~~~~~~~~~~
    unit tests for CDN
"""

import unittest

from domonic.CDN import CDN_CSS, CDN_FONT, CDN_IMG, CDN_JS
from domonic.html import img, link, script


class TestCase(unittest.TestCase):
    def test_domonic_CDN(self):
        myjs = script(_src=CDN_JS.JQUERY)
        assert str(myjs) == '<script src="https://code.jquery.com/jquery-4.0.0.min.js"></script>'
        mycss = link(_href=CDN_CSS.MARX)
        assert str(mycss) == '<link href="https://cdn.jsdelivr.net/npm/marx-css@5.3.0/css/marx.min.css"/>'
        myimg = img(_src=CDN_IMG.PLACEHOLDER(100, 100))
        assert str(myimg) == '<img src="//loremflickr.com/100/100"/>'
        assert CDN_IMG.PLACEHOLDER(100, 100, HTTP="https") == "https://loremflickr.com/100/100"
        assert CDN_IMG.PLACEHOLDER(100, 100, separator="x") == "//loremflickr.com/100x100"
        assert CDN_FONT.google("Open Sans") == "https://fonts.googleapis.com/css?family=Open+Sans"
        assert CDN_FONT.google(["Open Sans", "Roboto"]) == "https://fonts.googleapis.com/css?family=Open+Sans|Roboto"


if __name__ == "__main__":
    unittest.main()
