"""
    test_domonic
    ~~~~~~~~~~~~
    domonic core tests for __init__.py at the root of the domonic package

    (previously no tests. was using examples/parsing/page.py to drive dev)

"""

import unittest
# import requests
# from mock import patch

# from domonic.dom import *
from domonic import domonic


class TestCase(unittest.TestCase):
    """ Tests for the domonic """

    def test_load(self):
        t1 = domonic.load('<html></html>')
        print(t1)

    def test_loads(self):
        # t1 = domonic.loads('<html></html>')
        # print(t1)
        pass

    def parse(self):
        t1 = domonic.parse('<html></html>')
        assert t1 == "html(),"  # hmm wondering if parse is correct term. as returns pyml strings

        # t2 = domonic.parse('<html><body></body></html>')
        # print(t2)
        # t3 = domonic.parse('<html><body><p></p></body></html>')
        # print(t3)

        pass

    def evaluate(self):
        t1 = domonic.evaluate('<html></html>')
        print(t1)




if __name__ == '__main__':
    unittest.main()
