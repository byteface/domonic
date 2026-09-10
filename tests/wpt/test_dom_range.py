"""Ported from wpt/dom/ranges/Range-attributes.html, Range-collapse.html,
Range-comparePoint.html, Range-isPointInRange.html and Range-selectNode.html.
https://dom.spec.whatwg.org/#interface-range

Only the boundary-point and attribute behaviour is ported; the content
mutation methods (extractContents / deleteContents / surroundContents) and the
Text-container offset arithmetic have their own domonic tests.
"""

import unittest

from domonic.dom import Document, DOMException, Range

document = Document()


def _tree():
    root = document.createElement("root")
    document.appendChild(root)
    kids = [document.createElement(name) for name in ("a", "b", "c")]
    for kid in kids:
        root.appendChild(kid)
    return root, kids


class RangeAttributes(unittest.TestCase):
    def test_fresh_range_is_anchored_at_the_document(self):
        r = document.createRange()
        self.assertIs(r.startContainer, document)
        self.assertIs(r.endContainer, document)
        self.assertEqual(r.startOffset, 0)
        self.assertEqual(r.endOffset, 0)
        self.assertTrue(r.collapsed)

    def test_detach_is_a_noop(self):
        r = document.createRange()
        r.detach()
        self.assertIs(r.startContainer, document)
        self.assertIs(r.endContainer, document)
        self.assertEqual((r.startOffset, r.endOffset), (0, 0))
        self.assertTrue(r.collapsed)


class RangeCollapse(unittest.TestCase):
    def test_collapsed_reflects_equal_boundary_points(self):
        root, _kids = _tree()
        r = document.createRange()
        r.setStart(root, 1)
        r.setEnd(root, 2)
        self.assertFalse(r.collapsed)

        r.collapse(True)
        self.assertTrue(r.collapsed)
        self.assertIs(r.endContainer, root)
        self.assertEqual(r.endOffset, 1)

    def test_collapse_to_end(self):
        root, _kids = _tree()
        r = document.createRange()
        r.setStart(root, 0)
        r.setEnd(root, 3)
        r.collapse(False)
        self.assertTrue(r.collapsed)
        self.assertEqual(r.startOffset, 3)


class RangeComparePoint(unittest.TestCase):
    def test_relative_to_boundary_points(self):
        root, _kids = _tree()
        r = document.createRange()
        r.setStart(root, 1)
        r.setEnd(root, 2)
        self.assertEqual(r.comparePoint(root, 0), -1)
        self.assertEqual(r.comparePoint(root, 1), 0)
        self.assertEqual(r.comparePoint(root, 2), 0)
        self.assertEqual(r.comparePoint(root, 3), 1)

    def test_point_in_a_different_tree_throws_wrong_document_error(self):
        root, _kids = _tree()
        r = document.createRange()
        r.setStart(root, 0)
        r.setEnd(root, 1)
        stranger = document.createElement("stranger")
        with self.assertRaises(DOMException) as ctx:
            r.comparePoint(stranger, 0)
        self.assertEqual(ctx.exception.name, "WrongDocumentError")

    def test_offset_past_the_end_throws(self):
        root, _kids = _tree()
        r = document.createRange()
        r.setStart(root, 0)
        r.setEnd(root, 1)
        with self.assertRaises(Exception):
            r.comparePoint(root, 99)


class RangeIsPointInRange(unittest.TestCase):
    def test_true_only_between_the_boundary_points(self):
        root, _kids = _tree()
        r = document.createRange()
        r.setStart(root, 1)
        r.setEnd(root, 2)
        self.assertFalse(r.isPointInRange(root, 0))
        self.assertTrue(r.isPointInRange(root, 1))
        self.assertFalse(r.isPointInRange(root, 3))

    def test_point_in_a_different_tree_is_false_not_an_error(self):
        root, _kids = _tree()
        r = document.createRange()
        r.setStart(root, 0)
        r.setEnd(root, 1)
        stranger = document.createElement("stranger")
        self.assertFalse(r.isPointInRange(stranger, 0))


class RangeSelectNode(unittest.TestCase):
    def test_select_node_wraps_the_node(self):
        root, kids = _tree()
        r = document.createRange()
        r.selectNode(kids[1])
        self.assertIs(r.startContainer, root)
        self.assertEqual(r.startOffset, 1)
        self.assertEqual(r.endOffset, 2)
        self.assertIs(r.commonAncestorContainer, root)

    def test_select_node_contents_spans_the_children(self):
        root, kids = _tree()
        kids[0].appendChild(document.createElement("grandchild"))
        r = document.createRange()
        r.selectNodeContents(kids[0])
        self.assertIs(r.startContainer, kids[0])
        self.assertEqual(r.startOffset, 0)
        self.assertEqual(r.endOffset, 1)


if __name__ == "__main__":
    unittest.main()
