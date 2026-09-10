"""Ported from wpt/dom/nodes/Node-properties.html and
Element-siblingElement-null.html.
https://dom.spec.whatwg.org/#dom-node-parentelement

The ``ownerDocument`` of a freshly created node is ``None`` in domonic
(``createElement`` is a ``@staticmethod`` with no owning document -- a tracked
deviation), so those rows are not asserted here.
"""

import unittest

from domonic.dom import Document

document = Document()


class ParentElement(unittest.TestCase):
    def _tree(self):
        root = document.createElement("root")
        document.appendChild(root)
        el = document.createElement("x")
        root.appendChild(el)
        text = document.createTextNode("hi")
        el.appendChild(text)
        comment = document.createComment("c")
        el.appendChild(comment)
        return root, el, text, comment

    def test_element_parent_is_reported(self):
        root, el, _text, _comment = self._tree()
        self.assertIs(el.parentElement, root)

    def test_text_and_comment_parent_element(self):
        _root, el, text, comment = self._tree()
        self.assertIs(text.parentElement, el)
        self.assertIs(comment.parentElement, el)

    def test_a_document_parent_is_not_an_element(self):
        root, _el, _text, _comment = self._tree()
        self.assertIsNone(root.parentElement)

    def test_a_detached_node_has_no_parent_element(self):
        self.assertIsNone(document.createElement("z").parentElement)
        self.assertIsNone(document.createTextNode("t").parentElement)


class SiblingElement(unittest.TestCase):
    def _row(self):
        p = document.createElement("p")
        document.appendChild(p)
        a = document.createElement("a")
        text = document.createTextNode("x")
        b = document.createElement("b")
        p.append(a, text, b)
        return p, a, text, b

    def test_next_and_previous_element_sibling_skip_text(self):
        _p, a, text, b = self._row()
        self.assertIs(text.previousElementSibling, a)
        self.assertIs(text.nextElementSibling, b)
        self.assertIs(a.nextElementSibling, b)
        self.assertIs(b.previousElementSibling, a)

    def test_ends_of_the_row_have_no_sibling_element(self):
        _p, a, _text, b = self._row()
        self.assertIsNone(a.previousElementSibling)
        self.assertIsNone(b.nextElementSibling)


class NodeInvariants(unittest.TestCase):
    def test_nodetype_constants(self):
        el = document.createElement("x")
        self.assertEqual(el.ELEMENT_NODE, 1)
        self.assertEqual(el.TEXT_NODE, 3)
        self.assertEqual(el.COMMENT_NODE, 8)
        self.assertEqual(el.DOCUMENT_NODE, 9)
        self.assertEqual(el.DOCUMENT_FRAGMENT_NODE, 11)

    def test_hasChildNodes(self):
        p = document.createElement("p")
        self.assertFalse(p.hasChildNodes())
        p.appendChild(document.createTextNode("x"))
        self.assertTrue(p.hasChildNodes())

    def test_nodeName_per_type(self):
        self.assertEqual(document.createTextNode("x").nodeName, "#text")
        self.assertEqual(document.createComment("x").nodeName, "#comment")
        self.assertEqual(document.createDocumentFragment().nodeName, "#document-fragment")
        self.assertEqual(document.nodeName, "#document")


if __name__ == "__main__":
    unittest.main()
