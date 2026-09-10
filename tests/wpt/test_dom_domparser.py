"""Ported from wpt/domparsing/DOMParser-parseFromString-html.html,
DOMParser-parseFromString-xml.html and XMLSerializer-serializeToString.html.
https://html.spec.whatwg.org/multipage/dynamic-markup-insertion.html#dom-domparser-parsefromstring

domonic's HTML branch goes through html5lib and upper-cases parsed HTML tag
names (a tracked deviation); the assertions here compare case-insensitively.
"""

import unittest

from domonic.dom import DOMParser, XMLSerializer

parser = DOMParser()
serializer = XMLSerializer()


class ParseHTML(unittest.TestCase):
    def test_returns_a_full_document(self):
        doc = parser.parseFromString(
            "<html><head><title>T</title></head><body><p>hi</p></body></html>",
            "text/html",
        )
        self.assertEqual(doc.title, "T")
        self.assertIsNotNone(doc.body)
        self.assertEqual(doc.querySelector("p").textContent, "hi")

    def test_implied_elements_are_created(self):
        doc = parser.parseFromString("<p>bare</p>", "text/html")
        self.assertEqual(doc.querySelector("p").textContent, "bare")
        self.assertIsNotNone(doc.body)


class ParseXML(unittest.TestCase):
    def test_valid_xml_round_trips(self):
        doc = parser.parseFromString('<root><child a="1">text</child></root>', "application/xml")
        self.assertEqual(doc.documentElement.tagName, "root")
        self.assertEqual(doc.documentElement.firstChild.getAttribute("a"), "1")

    def test_malformed_xml_yields_a_parsererror_document_not_an_exception(self):
        doc = parser.parseFromString("<root><unclosed></root>", "application/xml")
        self.assertIn("parsererror", doc.documentElement.tagName.lower())
        self.assertIn("error", doc.documentElement.textContent.lower())


class Serialize(unittest.TestCase):
    def test_serializes_an_element_to_markup(self):
        doc = parser.parseFromString("<div><span>x</span></div>", "text/html")
        out = serializer.serializeToString(doc.querySelector("div"))
        self.assertEqual(out.lower(), "<div><span>x</span></div>")


if __name__ == "__main__":
    unittest.main()
