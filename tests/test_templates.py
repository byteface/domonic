"""
    test_templates
    ~~~~~~~~~~~~
    tests for templates
"""

import unittest
# import json
# import requests
# from mock import patch

from domonic.html import *
from domonic.templates import status_page

class TestCase(unittest.TestCase):

    def test_404(self):
        p = status_page(404)
        print(p)
        # self.assertEqual(p.status, 404)

    def test_401(self):
        # BUG - notice it tabs in due to being parent of <html>
        p = status_page(401, False)
        print(p)
        # self.assertEqual(p.status, 404)




if __name__ == '__main__':
    unittest.main()
