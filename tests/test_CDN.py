"""
    test_domonic
    ~~~~~~~~~~~~
    unit tests for CDN
"""

import unittest

from domonic.CDN import CDN_CSS, CDN_IMG, CDN_JS
from domonic.html import img, link, script


class TestCase(unittest.TestCase):
    def test_domonic_CDN(self):
        myjs = script(_src=CDN_JS.JQUERY)
        assert str(myjs) == '<script src="https://code.jquery.com/jquery-3.6.4.min.js"></script>'
        mycss = link(_href=CDN_CSS.MARX)
        assert str(mycss) == '<link href="https://unpkg.com/marx-css/css/marx.min.css"/>'
        myimg = img(_src=CDN_IMG.PLACEHOLDER(100, 100))
        assert str(myimg) == '<img src="://loremflickr.com/100/100"/>'


if __name__ == "__main__":
    unittest.main()
