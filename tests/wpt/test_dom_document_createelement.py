"""Ported from wpt/dom/nodes/Document-createElement.html
https://dom.spec.whatwg.org/#dom-document-createelement

Only the name-validation rows are ported. domonic's ``createElement`` is a
``@staticmethod`` with no owning HTML document, so it does not ASCII-case the
``tagName`` / ``localName`` the way the spec's HTML-document path does -- those
rows (and the namespace/prefix rows that depend on them) are a tracked
deviation, see ``tests/wpt/README.md``.

domonic is also deliberately a little stricter than the browser here: because
it serialises to text, a name containing ``< > & " ' /`` or whitespace is
unusable (it used to emit unparseable markup such as ``<a b></a b>``), so those
throw ``InvalidCharacterError`` even though a browser keeps a few of them
(e.g. ``"f<oo"``) as a live DOM node.
"""

import unittest

from domonic.dom import Document, DOMException
from tests.wpt._harness import assert_throws_dom

document = Document()

# a subset of the upstream ``invalid`` array that domonic agrees is invalid
INVALID = ["", "1foo", "1:foo", "fo o", "-foo", ".foo", "<foo", "foo>", "<foo>"]

# names the upstream ``valid`` array lists that domonic also accepts
VALID = ["foo", "f1oo", "foo1", "foo:bar", "xml", "xmlns", "xmlfoo", "svg", "math", "FOO", "x_1"]


class DocumentCreateElement(unittest.TestCase):
    def test_invalid_names_throw_invalid_character_error(self):
        for name in INVALID:
            assert_throws_dom("InvalidCharacterError", lambda name=name: document.createElement(name))

    def test_valid_names_are_accepted(self):
        for name in VALID:
            el = document.createElement(name)
            self.assertEqual(el.nodeType, 1)

    def test_created_element_is_in_the_html_namespace(self):
        el = document.createElement("foo")
        self.assertEqual(el.namespaceURI, "http://www.w3.org/1999/xhtml")
        self.assertIsNone(el.prefix)

    def test_createelementns_rejects_a_multi_colon_qualified_name(self):
        with self.assertRaises(DOMException) as ctx:
            document.createElementNS("urn:x", "a:b:c")
        self.assertEqual(ctx.exception.name, "InvalidCharacterError")


if __name__ == "__main__":
    unittest.main()
