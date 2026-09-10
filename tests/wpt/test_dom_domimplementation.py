"""Ported from wpt/dom/nodes/DOMImplementation-createHTMLDocument.html and
DOMImplementation-createDocumentType.html.
https://dom.spec.whatwg.org/#dom-domimplementation-createhtmldocument

domonic's ``HTMLDocument`` *is* the ``<html>`` root element (``documentElement``
is the document itself), so the exact ``childNodes`` shape from the upstream
tests -- ``[doctype, <html>]`` with ``<html>`` holding ``[<head>, <body>]`` --
does not apply; the structural assertions here follow domonic's flattened tree.
The serialisation assertion guards a real bug that was fixed: it used to emit
``<html><html>...``.
"""

import unittest

from domonic.dom import Document

impl = Document().implementation


class CreateHTMLDocument(unittest.TestCase):
    def test_has_an_html_doctype(self):
        doc = impl.createHTMLDocument("t")
        self.assertEqual(doc.doctype.name, "html")
        self.assertEqual(doc.doctype.publicId, "")
        self.assertEqual(doc.doctype.systemId, "")

    def test_has_html_head_and_body(self):
        doc = impl.createHTMLDocument("t")
        self.assertEqual(doc.documentElement.tagName.lower(), "html")
        self.assertIsNotNone(doc.head)
        self.assertIsNotNone(doc.body)
        self.assertEqual(doc.head.tagName.lower(), "head")
        self.assertEqual(doc.body.tagName.lower(), "body")

    def test_title_argument_becomes_a_title_element(self):
        doc = impl.createHTMLDocument("MyTitle")
        self.assertEqual(doc.head.firstChild.tagName.lower(), "title")
        self.assertEqual(doc.head.firstChild.textContent, "MyTitle")
        self.assertEqual(doc.title, "MyTitle")

    def test_no_title_argument_means_no_title_element(self):
        doc = impl.createHTMLDocument()
        self.assertEqual([c.tagName.lower() for c in doc.head.childNodes], [])

    def test_empty_title_argument_still_creates_a_title_element(self):
        doc = impl.createHTMLDocument("")
        self.assertEqual([c.tagName.lower() for c in doc.head.childNodes], ["title"])

    def test_serialises_to_well_formed_html(self):
        doc = impl.createHTMLDocument("Hi")
        self.assertEqual(
            str(doc),
            "<!DOCTYPE html><html><head><title>Hi</title></head><body></body></html>",
        )


class CreateDocumentType(unittest.TestCase):
    def test_carries_name_public_id_system_id(self):
        dt = impl.createDocumentType("svg", "pub", "sys")
        self.assertEqual((dt.name, dt.publicId, dt.systemId), ("svg", "pub", "sys"))
        self.assertEqual(dt.nodeType, 10)
        self.assertEqual(dt.nodeName, "svg")

    def test_two_with_the_same_fields_are_equal_but_not_identical(self):
        a = impl.createDocumentType("html", "", "")
        b = impl.createDocumentType("html", "", "")
        self.assertIsNot(a, b)
        self.assertTrue(a.isEqualNode(b))


if __name__ == "__main__":
    unittest.main()
