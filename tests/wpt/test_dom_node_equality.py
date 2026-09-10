"""Ported from wpt/dom/nodes/Node-isEqualNode.html
https://dom.spec.whatwg.org/#dom-node-isequalnode
"""

import unittest

import pytest

from domonic.dom import Document
from tests.wpt._harness import assert_false, assert_true

document = Document()
impl = document.implementation


class NodeIsEqualNode(unittest.TestCase):
    def test_doctypes_compared_on_name_public_id_system_id(self):
        d1 = impl.createDocumentType("qualifiedName", "publicId", "systemId")
        d2 = impl.createDocumentType("qualifiedName", "publicId", "systemId")
        d3 = impl.createDocumentType("qualifiedName2", "publicId", "systemId")
        d4 = impl.createDocumentType("qualifiedName", "publicId2", "systemId")
        d5 = impl.createDocumentType("qualifiedName", "publicId", "systemId3")
        assert_true(d1.isEqualNode(d1), "self-comparison")
        assert_true(d1.isEqualNode(d2), "same properties")
        assert_false(d1.isEqualNode(d3), "different name")
        assert_false(d1.isEqualNode(d4), "different public ID")
        assert_false(d1.isEqualNode(d5), "different system ID")

    def test_elements_compared_on_namespace_prefix_localname_attr_count(self):
        e1 = document.createElementNS("namespace", "prefix:localName")
        e2 = document.createElementNS("namespace", "prefix:localName")
        e3 = document.createElementNS("namespace2", "prefix:localName")
        e4 = document.createElementNS("namespace", "prefix2:localName")
        e5 = document.createElementNS("namespace", "prefix:localName2")
        e6 = document.createElementNS("namespace", "prefix:localName")
        e6.setAttribute("foo", "bar")
        assert_true(e1.isEqualNode(e1), "self-comparison")
        assert_true(e1.isEqualNode(e2), "same properties")
        assert_false(e1.isEqualNode(e3), "different namespace")
        assert_false(e1.isEqualNode(e4), "different prefix")
        assert_false(e1.isEqualNode(e5), "different local name")
        assert_false(e1.isEqualNode(e6), "different number of attributes")

    @pytest.mark.xfail(
        reason="domonic has no namespaced-attribute support: setAttributeNS() "
        "ignores the namespace and stores the qualified name as a plain attr",
        strict=True,
    )
    def test_elements_compared_on_attribute_namespace_localname_value(self):
        e1 = document.createElement("element")
        e1.setAttributeNS("namespace", "prefix:localName", "value")
        e2 = document.createElement("element")
        e2.setAttributeNS("namespace", "prefix:localName", "value")
        e3 = document.createElement("element")
        e3.setAttributeNS("namespace2", "prefix:localName", "value")
        e4 = document.createElement("element")
        e4.setAttributeNS("namespace", "prefix2:localName", "value")
        e5 = document.createElement("element")
        e5.setAttributeNS("namespace", "prefix:localName2", "value")
        e6 = document.createElement("element")
        e6.setAttributeNS("namespace", "prefix:localName", "value2")
        assert_true(e1.isEqualNode(e1), "self-comparison")
        assert_true(e1.isEqualNode(e2), "attribute with same properties")
        assert_false(e1.isEqualNode(e3), "attribute with different namespace")
        assert_true(e1.isEqualNode(e4), "attribute with different prefix")
        assert_false(e1.isEqualNode(e5), "attribute with different local name")
        assert_false(e1.isEqualNode(e6), "attribute with different value")

    def test_processing_instructions_compared_on_target_and_data(self):
        p1 = document.createProcessingInstruction("target", "data")
        p2 = document.createProcessingInstruction("target", "data")
        p3 = document.createProcessingInstruction("target2", "data")
        p4 = document.createProcessingInstruction("target", "data2")
        assert_true(p1.isEqualNode(p1), "self-comparison")
        assert_true(p1.isEqualNode(p2), "same properties")
        assert_false(p1.isEqualNode(p3), "different target")
        assert_false(p1.isEqualNode(p4), "different data")

    def test_text_nodes_compared_on_data(self):
        t1 = document.createTextNode("data")
        t2 = document.createTextNode("data")
        t3 = document.createTextNode("data2")
        assert_true(t1.isEqualNode(t1), "self-comparison")
        assert_true(t1.isEqualNode(t2), "same properties")
        assert_false(t1.isEqualNode(t3), "different data")

    def test_comments_compared_on_data(self):
        c1 = document.createComment("data")
        c2 = document.createComment("data")
        c3 = document.createComment("data2")
        assert_true(c1.isEqualNode(c1), "self-comparison")
        assert_true(c1.isEqualNode(c2), "same properties")
        assert_false(c1.isEqualNode(c3), "different data")

    def test_document_fragments_not_compared_on_properties(self):
        f1 = document.createDocumentFragment()
        f2 = document.createDocumentFragment()
        assert_true(f1.isEqualNode(f1), "self-comparison")
        assert_true(f1.isEqualNode(f2), "same properties")

    def test_node_equality_tests_descendant_equality_too(self):
        for factory in (
            lambda: document.createElement("foo"),
            lambda: document.createDocumentFragment(),
        ):
            a = factory()
            b = factory()
            a.appendChild(document.createComment("data"))
            assert_false(a.isEqualNode(b))
            b.appendChild(document.createComment("data"))
            assert_true(a.isEqualNode(b))


if __name__ == "__main__":
    unittest.main()
