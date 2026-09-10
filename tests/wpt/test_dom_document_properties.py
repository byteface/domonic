"""Ported from wpt/dom/nodes/Document-characterSet-normalization.html,
wpt/dom/nodes/Document-contentType/ and the compatMode / URL checks in
wpt/html/dom/documents/.
https://dom.spec.whatwg.org/#document
"""

import unittest

from domonic.dom import Document

document = Document()


class DocumentMetadata(unittest.TestCase):
    def test_compat_mode_is_standards(self):
        self.assertEqual(document.compatMode, "CSS1Compat")

    def test_content_type_is_text_html_for_an_html_document(self):
        self.assertEqual(document.contentType, "text/html")

    def test_content_type_is_application_xml_for_an_xml_document(self):
        xml_doc = document.implementation.createDocument("", "root", None)
        self.assertEqual(xml_doc.contentType, "application/xml")

    def test_character_set_aliases_agree(self):
        self.assertEqual(document.characterSet, "UTF-8")
        self.assertEqual(document.charset, "UTF-8")
        self.assertEqual(document.inputEncoding, "UTF-8")

    def test_ready_state_is_complete(self):
        self.assertEqual(document.readyState, "complete")

    def test_document_uri_matches_url(self):
        self.assertEqual(document.documentURI, document.URL)

    def test_hidden_tracks_visibility_state(self):
        self.assertFalse(document.hidden)
        self.assertEqual(document.visibilityState, "visible")


if __name__ == "__main__":
    unittest.main()
