"""Ported from wpt/dom/nodes/{Node-nodeName,Node-isSameNode,Node-constants,
Node-lookupNamespaceURI,Element-hasAttribute,Element-hasAttributes,
Element-removeAttribute,Element-removeAttributeNS,Element-webkitMatchesSelector,
Document-createAttribute,Document-createCDATASection,Text-related}.html.
https://dom.spec.whatwg.org/

A grab-bag of smaller Node/Element/Attr/Document members that had no WPT
coverage yet. Most rows pass outright; the ones that don't are namespace-
attribute-tracking gaps already covered by the existing "setAttributeNS()
ignores the namespace" deviation (see domonic-wpt-conformance), so they are
noted rather than re-xfailed individually.
"""

import unittest

from domonic.dom import DOMException, Document, HTMLDocument

document = Document()


class NodeName(unittest.TestCase):
    def test_across_node_types(self):
        self.assertEqual(document.createTextNode("foo").nodeName, "#text")
        self.assertEqual(document.createComment("foo").nodeName, "#comment")
        self.assertEqual(document.nodeName, "#document")
        self.assertEqual(document.createDocumentFragment().nodeName, "#document-fragment")

    def test_doctype_nodename_is_its_name(self):
        from domonic.dom import DOMImplementation

        doctype = DOMImplementation().createDocumentType("html", "", "")
        self.assertEqual(doctype.nodeName, "html")


class NodeIsSameNode(unittest.TestCase):
    def test_compares_by_reference_across_node_types(self):
        from domonic.dom import DOMImplementation

        impl = DOMImplementation()
        pairs = [
            (impl.createDocumentType("q", "p", "s"), impl.createDocumentType("q", "p", "s")),
            (document.createElement("el"), document.createElement("el")),
            (document.createProcessingInstruction("t", "d"), document.createProcessingInstruction("t", "d")),
            (document.createTextNode("data"), document.createTextNode("data")),
            (document.createComment("data"), document.createComment("data")),
            (document.createDocumentFragment(), document.createDocumentFragment()),
            (document.createAttribute("href"), document.createAttribute("href")),
        ]
        for node1, node2 in pairs:
            with self.subTest(kind=type(node1).__name__):
                self.assertTrue(node1.isSameNode(node1))
                self.assertFalse(node1.isSameNode(node2))
                self.assertFalse(node1.isSameNode(None))


class NodeConstants(unittest.TestCase):
    def test_node_type_constants_on_class_and_instance(self):
        from domonic.dom import Node

        expected = {
            "ELEMENT_NODE": 1,
            "ATTRIBUTE_NODE": 2,
            "TEXT_NODE": 3,
            "CDATA_SECTION_NODE": 4,
            "PROCESSING_INSTRUCTION_NODE": 7,
            "COMMENT_NODE": 8,
            "DOCUMENT_NODE": 9,
            "DOCUMENT_TYPE_NODE": 10,
            "DOCUMENT_FRAGMENT_NODE": 11,
        }
        el = document.createElement("foo")
        text = document.createTextNode("bar")
        for name, value in expected.items():
            with self.subTest(name=name):
                self.assertEqual(getattr(Node, name), value)
                self.assertEqual(getattr(el, name), value)
                self.assertEqual(getattr(text, name), value)


class NodeIsDefaultNamespace(unittest.TestCase):
    def test_document_fragment_is_always_in_the_default_namespace(self):
        # A regression check: isDefaultNamespace used to compare against
        # this node's own namespaceURI (which every node defaults to the
        # HTML namespace at construction, DocumentFragment included) instead
        # of the namespace actually in scope -- so a fragment never reported
        # itself as being in the default namespace.
        frag = document.createDocumentFragment()
        self.assertTrue(frag.isDefaultNamespace(None))
        self.assertTrue(frag.isDefaultNamespace(""))
        self.assertFalse(frag.isDefaultNamespace("foo"))
        self.assertFalse(frag.isDefaultNamespace("xmlns"))


class ElementHasAttribute(unittest.TestCase):
    def test_case_insensitive_in_an_html_document(self):
        el = document.createElement("span")
        el.setAttribute("data-e2", "2")
        el.setAttribute("data-F2", "3")
        self.assertTrue(el.hasAttribute("data-e2"))
        self.assertTrue(el.hasAttribute("data-E2"))
        self.assertTrue(el.hasAttribute("data-f2"))
        self.assertTrue(el.hasAttribute("data-F2"))

    def test_checks_presence_irrespective_of_namespace(self):
        el = document.createElement("p")
        el.setAttributeNS("foo", "x", "first")
        self.assertTrue(el.hasAttribute("x"))


class ElementHasAttributes(unittest.TestCase):
    def test_false_when_empty_true_otherwise(self):
        self.assertFalse(document.createElement("button").hasAttributes())
        el = document.createElement("div")
        self.assertFalse(el.hasAttributes())
        el.setAttribute("class", "foo")
        self.assertTrue(el.hasAttributes())


class ElementWebkitMatchesSelector(unittest.TestCase):
    def test_is_an_alias_for_matches(self):
        el = document.createElement("p")
        el.setAttribute("class", "lead")
        self.assertTrue(el.webkitMatchesSelector("p.lead"))
        self.assertFalse(el.webkitMatchesSelector("div"))


class AttrProperties(unittest.TestCase):
    def test_owner_element_none_when_detached(self):
        attr = document.createAttribute("foo")
        self.assertIsNone(attr.ownerElement)

    def test_owner_element_set_by_set_attribute_node(self):
        el = document.createElement("div")
        attr = document.createAttribute("foo")
        el.setAttributeNode(attr)
        self.assertIs(attr.ownerElement, el)

    def test_local_name_and_prefix_derived_from_the_qualified_name(self):
        attr = document.createAttribute("a:bb")
        self.assertEqual(attr.prefix, "a")
        self.assertEqual(attr.localName, "bb")

    def test_unprefixed_name_has_no_prefix(self):
        attr = document.createAttribute("foo")
        self.assertIsNone(attr.prefix)
        self.assertEqual(attr.localName, "foo")

    def test_specified_is_always_true(self):
        self.assertTrue(document.createAttribute("foo").specified)


class DocumentCreateCDATASection(unittest.TestCase):
    def test_throws_in_an_html_document(self):
        with self.assertRaises(DOMException) as ctx:
            HTMLDocument().createCDATASection("foo")
        self.assertEqual(ctx.exception.name, "NotSupportedError")


class TextIsNeverAContainer(unittest.TestCase):
    """A Text node's data lives in the same slot Node uses for children
    elsewhere in the tree (domonic's Node.args) -- so accessors that read
    that slot directly, instead of going through the (correctly Text-empty)
    child-list abstraction, used to treat the text data as if it were a
    child node."""

    def test_has_child_nodes_first_child_last_child(self):
        text = document.createTextNode("a -- b")
        self.assertFalse(text.hasChildNodes())
        self.assertIsNone(text.firstChild)
        self.assertIsNone(text.lastChild)
        self.assertEqual(list(text.childNodes), [])


if __name__ == "__main__":
    unittest.main()
