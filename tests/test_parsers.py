"""
test_parsers
~~~~~~~~~~~~
"""

import unittest

from domonic.parsers import create_element


class TestParsers(unittest.TestCase):
    def test_create_element_passes_args_to_html_tags(self):
        self.assertEqual(
            str(create_element("div", "hello", _id="x")), '<div id="x">hello</div>'
        )

    def test_create_element_passes_args_to_sitemap_tags(self):
        self.assertEqual(
            str(create_element("loc", "https://example.com")),
            "<loc>https://example.com</loc>",
        )

    def test_create_element_falls_back_to_custom_html_tags(self):
        self.assertEqual(
            str(create_element("my-widget", "ok", **{"_data-id": "7"})),
            '<my-widget data-id="7">ok</my-widget>',
        )


if __name__ == "__main__":
    unittest.main()
