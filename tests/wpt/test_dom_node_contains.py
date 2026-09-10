"""Ported from wpt/dom/nodes/Node-contains.html
https://dom.spec.whatwg.org/#dom-node-contains

The upstream test walks a fixed ``testNodes`` document; this port builds an
equivalent small tree and checks the same ``contains`` invariants (a node
contains itself, contains its descendants of every node type, and nothing
outside its subtree; ``contains(null)`` is false).
"""

import unittest

from domonic.dom import Document
from tests.wpt._harness import assert_false, assert_true

document = Document()


class NodeContains(unittest.TestCase):
    def setUp(self):
        d = document
        self.root = d.createElement("root")
        self.branch = d.createElement("branch")
        self.leaf = d.createElement("leaf")
        self.sibling = d.createElement("sibling")
        self.text = d.createTextNode("text")
        self.comment = d.createComment("comment")
        self.outside = d.createElement("outside")

        self.root.appendChild(self.branch)
        self.root.appendChild(self.sibling)
        self.branch.appendChild(self.leaf)
        self.branch.appendChild(self.comment)
        self.leaf.appendChild(self.text)

        self.tree = [self.root, self.branch, self.leaf, self.sibling, self.text, self.comment]

    def test_contains_null_is_false(self):
        for node in self.tree:
            assert_false(node.contains(None), f"{node.nodeName}.contains(null)")

    def test_node_contains_itself(self):
        for node in self.tree:
            assert_true(node.contains(node), f"{node.nodeName}.contains(self)")

    def test_contains_matches_ancestor_walk(self):
        for ref in self.tree:
            for other in self.tree:
                ancestor = other
                while ancestor is not None and ancestor is not ref:
                    ancestor = ancestor.parentNode
                expected = ancestor is ref
                got = ref.contains(other)
                if expected:
                    assert_true(got, f"{ref.nodeName}.contains({other.nodeName})")
                else:
                    assert_false(got, f"{ref.nodeName}.contains({other.nodeName})")

    def test_does_not_contain_disconnected_node(self):
        assert_false(self.root.contains(self.outside))
        assert_false(self.outside.contains(self.root))


if __name__ == "__main__":
    unittest.main()
