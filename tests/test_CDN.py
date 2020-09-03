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


class domonicTestCase(unittest.TestCase):

    def test_domonic_CDN(self):
        myjs = script(_src=CDN_JS.JQUERY_3_5_1)
        print(myjs)

        # css
        mycss = link(_href=CDN_CSS.MARX)
        print(mycss)
        mycss = link(_rel="stylesheet", _href=CDN_JS.JQUERY_3_5_1)
        print(mycss)

        myimg = img(_src=CDN_IMG.PLACEHOLDER(100, 100))
        print(myimg)


if __name__ == '__main__':
    unittest.main()
