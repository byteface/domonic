"""Ported from wpt/dom/traversal/{NodeFilter-constants,TreeWalker-currentNode,
TreeWalker-previousNodeLastChildReject,TreeWalker-walking-outside-a-tree}.html.
https://dom.spec.whatwg.org/#interface-treewalker

NodeIterator-removal(-during-filtering).html is not ported: it exercises the
"pre-removing steps" (https://dom.spec.whatwg.org/#nodeiterator-pre-removing-steps)
that make a NodeIterator's referenceNode/pointerBeforeReferenceNode adjust
automatically when a node is removed from the tree elsewhere -- domonic has
no such hook (the same class of gap as Range's live boundary points, see
test_dom_range.py), and it is a large, generative, common.js-driven suite
like dom/ranges/ besides.
"""

import unittest

from domonic.dom import Document, NodeFilter

document = Document()


class NodeFilterConstants(unittest.TestCase):
    def test_accept_node_results(self):
        self.assertEqual(NodeFilter.FILTER_ACCEPT, 1)
        self.assertEqual(NodeFilter.FILTER_REJECT, 2)
        self.assertEqual(NodeFilter.FILTER_SKIP, 3)

    def test_what_to_show_bitmask(self):
        self.assertEqual(NodeFilter.SHOW_ALL, 0xFFFFFFFF)
        self.assertEqual(NodeFilter.SHOW_ELEMENT, 0x1)
        self.assertEqual(NodeFilter.SHOW_ATTRIBUTE, 0x2)
        self.assertEqual(NodeFilter.SHOW_TEXT, 0x4)
        self.assertEqual(NodeFilter.SHOW_COMMENT, 0x80)


class TreeWalkerCurrentNode(unittest.TestCase):
    def test_setting_to_a_non_node_value_throws(self):
        root = document.createElement("div")
        w = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT, lambda n: True)
        for bad in (None, {}, object(), "not a node"):
            with self.subTest(bad=bad):
                with self.assertRaises(TypeError):
                    w.currentNode = bad

    def test_parent_of_root_does_not_move_current_node(self):
        root = document.createElement("div")
        document.appendChild(root)
        w = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT, lambda n: True)
        self.assertIsNone(w.parentNode())
        self.assertIs(w.currentNode, root)


class TreeWalkerPreviousNodeRespectsTheFilter(unittest.TestCase):
    def test_previous_node_skips_a_rejected_subtree(self):
        # Regression check: previousNode() used to loop forever whenever the
        # first backward sibling candidate wasn't immediately FILTER_ACCEPTed
        # (a rejected node, or one whose descendants don't accept either) --
        # the spec's "set sibling to node's previous sibling" retry step was
        # missing, so the search never advanced past that first candidate.
        root = document.createElement("div")
        root.id = "root"
        a1 = document.createElement("div")
        a1.id = "A1"
        b1 = document.createElement("div")
        b1.id = "B1"
        b2 = document.createElement("div")
        b2.id = "B2"
        c1 = document.createElement("div")
        c1.id = "C1"
        c2 = document.createElement("div")
        c2.id = "C2"
        d1 = document.createElement("div")
        d1.id = "D1"
        d2 = document.createElement("div")
        d2.id = "D2"
        root.appendChild(a1)
        a1.appendChild(b1)
        a1.appendChild(b2)
        b1.appendChild(c1)
        b1.appendChild(c2)
        c2.appendChild(d1)
        c2.appendChild(d2)

        def reject_c2(node):
            return NodeFilter.FILTER_REJECT if node.id == "C2" else NodeFilter.FILTER_ACCEPT

        w = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT, reject_c2)
        self.assertEqual(w.firstChild().id, "A1")
        self.assertEqual(w.nextNode().id, "B1")
        self.assertEqual(w.nextNode().id, "C1")
        self.assertEqual(w.nextNode().id, "B2")
        previous = w.previousNode()
        self.assertIsNotNone(previous)
        self.assertEqual(previous.id, "C1")  # not C2 (rejected) or D1/D2 (its children)


class TreeWalkerWalkingOutsideATree(unittest.TestCase):
    def test_survives_detachment_and_regrafting(self):
        root_doc = document.createElement("div")
        head = document.createElement("head")
        title = document.createElement("title")
        body = document.createElement("body")
        p = document.createElement("p")
        root_doc.appendChild(head)
        head.appendChild(title)
        root_doc.appendChild(body)
        body.appendChild(p)

        w = document.createTreeWalker(body, 0xFFFFFFFF, None)
        root_doc.removeChild(body)
        self.assertIs(w.lastChild(), p, "TreeWalker failed after removing the current node from the tree")

        root_doc.appendChild(p)
        self.assertIs(w.previousNode(), title, "failed to handle regrafting correctly")

        p.appendChild(body)
        self.assertIs(w.nextNode(), p, "couldn't retrace steps")
        self.assertIs(w.nextNode(), body, "couldn't step back into root")
        self.assertIsNone(w.previousNode(), "root didn't retake its rootish position")


if __name__ == "__main__":
    unittest.main()
