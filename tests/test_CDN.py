"""
    test_domonic
    ~~~~~~~~~~~~
    unit tests for css
"""

import unittest
# import json
# import requests
# from mock import patch

from domonic.html import *
from domonic.CDN import *


class TestCase(unittest.TestCase):

    def test_domonic_CDN(self):
        myjs = script(_src=CDN_JS.JQUERY_3_5_1)
        assert str(myjs) == '<script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>'
        mycss = link(_href=CDN_CSS.MARX)
        assert str(mycss) == '<link href="https://unpkg.com/marx-css/css/marx.min.css" />'
        mycss = link(_rel="stylesheet", _href=CDN_JS.JQUERY_3_5_1)
        assert str(mycss) == '<link rel="stylesheet" href="https://code.jquery.com/jquery-3.5.1.min.js" />'
        myimg = img(_src=CDN_IMG.PLACEHOLDER(100, 100))
        assert str(myimg) == '<img src="://loremflickr.com/100/100" />'


if __name__ == '__main__':
    unittest.main()
