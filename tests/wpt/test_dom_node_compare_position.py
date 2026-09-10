"""Ported from wpt/dom/nodes/Node-compareDocumentPosition.html
https://dom.spec.whatwg.org/#dom-node-comparedocumentposition

The upstream test builds a fixed node set (``dom/common.js``) and, for every
ordered pair, recomputes the expected bitmask straight from the tree using the
spec's own wording.  This port does the same over a self-contained tree of
elements, text and comment nodes plus a detached subtree, so the assertions
follow the spec text rather than hard-coded numbers.
"""

import unittest

from domonic.dom import Document, Node

document = Document()

# constants, spelled out so the test reads like the spec
DISCONNECTED = Node.DOCUMENT_POSITION_DISCONNECTED
PRECEDING = Node.DOCUMENT_POSITION_PRECEDING
FOLLOWING = Node.DOCUMENT_POSITION_FOLLOWING
CONTAINS = Node.DOCUMENT_POSITION_CONTAINS
CONTAINED_BY = Node.DOCUMENT_POSITION_CONTAINED_BY
IMPLEMENTATION_SPECIFIC = Node.DOCUMENT_POSITION_IMPLEMENTATION_SPECIFIC


def _furthest_ancestor(node):
    while getattr(node, "parentNode", None) is not None:
        node = node.parentNode
    return node


def _ancestors(node):
    chain = []
    node = getattr(node, "parentNode", None)
    while node is not None:
        chain.append(node)
        node = getattr(node, "parentNode", None)
    return chain


def _preorder(root):
    out = [root]
    for kid in list(getattr(root, "args", ())):
        if isinstance(kid, Node):
            out.extend(_preorder(kid))
    return out


class NodeCompareDocumentPosition(unittest.TestCase):
    def setUp(self):
        self.root = document.createElement("root")
        self.a = document.createElement("a")
        self.b = document.createElement("b")
        self.a_text = document.createTextNode("a-text")
        self.a_comment = document.createComment("a-comment")
        self.b1 = document.createElement("b1")
        self.b2 = document.createElement("b2")
        self.root.appendChild(self.a)
        self.a.appendChild(self.a_text)
        self.a.appendChild(self.a_comment)
        self.root.appendChild(self.b)
        self.b.appendChild(self.b1)
        self.b.appendChild(self.b2)

        # a separate, disconnected tree
        self.lonely = document.createElement("lonely")
        self.lonely_kid = document.createElement("lonely-kid")
        self.lonely.appendChild(self.lonely_kid)

        self.nodes = [
            self.root,
            self.a,
            self.a_text,
            self.a_comment,
            self.b,
            self.b1,
            self.b2,
            self.lonely,
            self.lonely_kid,
        ]

    def test_every_ordered_pair_matches_the_spec(self):
        order = _preorder(self.root)
        for reference in self.nodes:
            for other in self.nodes:
                result = reference.compareDocumentPosition(other)
                label = f"{reference.nodeName}.compareDocumentPosition({other.nodeName})"

                if other is reference:
                    self.assertEqual(result, 0, label)
                    continue

                if _furthest_ancestor(reference) is not _furthest_ancestor(other):
                    self.assertTrue(result & DISCONNECTED, label)
                    self.assertTrue(result & IMPLEMENTATION_SPECIFIC, label)
                    self.assertIn(result & (PRECEDING | FOLLOWING), (PRECEDING, FOLLOWING), label)
                    back = other.compareDocumentPosition(reference)
                    self.assertNotEqual(bool(result & PRECEDING), bool(back & PRECEDING), label)
                    self.assertNotEqual(bool(result & FOLLOWING), bool(back & FOLLOWING), label)
                    continue

                if any(anc is other for anc in _ancestors(reference)):
                    self.assertEqual(result, CONTAINS | PRECEDING, label)
                elif any(anc is reference for anc in _ancestors(other)):
                    self.assertEqual(result, CONTAINED_BY | FOLLOWING, label)
                elif order.index(other) < order.index(reference):
                    self.assertEqual(result, PRECEDING, label)
                else:
                    self.assertEqual(result, FOLLOWING, label)

    def test_identical_node_is_zero(self):
        self.assertEqual(self.a.compareDocumentPosition(self.a), 0)

    def test_contained_and_container_are_symmetric_pairs(self):
        self.assertEqual(
            self.root.compareDocumentPosition(self.b1),
            CONTAINED_BY | FOLLOWING,
        )
        self.assertEqual(
            self.b1.compareDocumentPosition(self.root),
            CONTAINS | PRECEDING,
        )

    def test_siblings_use_tree_order(self):
        self.assertEqual(self.a.compareDocumentPosition(self.b), FOLLOWING)
        self.assertEqual(self.b.compareDocumentPosition(self.a), PRECEDING)
        self.assertEqual(self.a_text.compareDocumentPosition(self.b2), FOLLOWING)
        self.assertEqual(self.b2.compareDocumentPosition(self.a_text), PRECEDING)


class NodeGetRootNode(unittest.TestCase):
    def test_connected_node_root_is_the_top_of_the_tree(self):
        root = document.createElement("top")
        mid = document.createElement("mid")
        leaf = document.createElement("leaf")
        root.appendChild(mid)
        mid.appendChild(leaf)
        self.assertIs(leaf.getRootNode(), root)
        self.assertIs(mid.getRootNode(), root)
        self.assertIs(root.getRootNode(), root)

    def test_detached_node_is_its_own_root(self):
        orphan = document.createElement("orphan")
        self.assertIs(orphan.getRootNode(), orphan)

    def test_root_follows_the_node_as_it_is_moved(self):
        tree_a = document.createElement("a")
        tree_b = document.createElement("b")
        child = document.createElement("child")
        tree_a.appendChild(child)
        self.assertIs(child.getRootNode(), tree_a)
        tree_b.appendChild(child)
        self.assertIs(child.getRootNode(), tree_b)


if __name__ == "__main__":
    unittest.main()
