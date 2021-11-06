"""
    test_window
    ~~~~~~~~~~~~~~~~
"""

import unittest

# from domonic.dom import *
# from domonic.javascript import *
# from domonic.webapi import *
from domonic.window import *
from domonic.decorators import *

class TestCase(unittest.TestCase):

    @silence
    def test_window(self):
        window.location = "http://www.google.com"
        # print(window.document.body.innerHTML)
        print(window.document.title)


if __name__ == '__main__':
    unittest.main()
