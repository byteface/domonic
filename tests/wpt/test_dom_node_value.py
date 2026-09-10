"""Ported from wpt/dom/nodes/Node-nodeValue.html
https://dom.spec.whatwg.org/#dom-node-nodevalue
"""

import unittest

from domonic.dom import Document
from tests.wpt._harness import assert_equals

document = Document()


class NodeNodeValue(unittest.TestCase):
    def test_text_node_value(self):
        t = document.createTextNode("A span!")
        assert_equals(t.nodeValue, "A span!")
        assert_equals(t.data, "A span!")
        t.nodeValue = "test again"
        assert_equals(t.nodeValue, "test again")
        assert_equals(t.data, "test again")
        t.nodeValue = None
        assert_equals(t.nodeValue, "")
        assert_equals(t.data, "")

    def test_comment_node_value(self):
        c = document.createComment("A comment!")
        assert_equals(c.nodeValue, "A comment!")
        assert_equals(c.data, "A comment!")
        c.nodeValue = "test again"
        assert_equals(c.nodeValue, "test again")
        assert_equals(c.data, "test again")
        c.nodeValue = None
        assert_equals(c.nodeValue, "")
        assert_equals(c.data, "")

    def test_processing_instruction_node_value(self):
        p = document.createProcessingInstruction("pi", "A PI!")
        assert_equals(p.nodeValue, "A PI!")
        assert_equals(p.data, "A PI!")
        p.nodeValue = "test again"
        assert_equals(p.nodeValue, "test again")
        assert_equals(p.data, "test again")
        p.nodeValue = None
        assert_equals(p.nodeValue, "")
        assert_equals(p.data, "")

    def test_element_node_value_is_null_and_setter_is_a_noop(self):
        el = document.createElement("a")
        assert_equals(el.nodeValue, None)
        el.nodeValue = "foo"
        assert_equals(el.nodeValue, None)

    def test_document_node_value_is_null_and_setter_is_a_noop(self):
        assert_equals(document.nodeValue, None)
        document.nodeValue = "foo"
        assert_equals(document.nodeValue, None)

    def test_document_fragment_node_value_is_null_and_setter_is_a_noop(self):
        frag = document.createDocumentFragment()
        assert_equals(frag.nodeValue, None)
        frag.nodeValue = "foo"
        assert_equals(frag.nodeValue, None)

    def test_doctype_node_value_is_null_and_setter_is_a_noop(self):
        dt = document.implementation.createDocumentType("html", "", "")
        assert_equals(dt.nodeValue, None)
        dt.nodeValue = "foo"
        assert_equals(dt.nodeValue, None)


if __name__ == "__main__":
    unittest.main()
