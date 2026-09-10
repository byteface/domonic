"""Ported from wpt/dom/traversal/NodeIterator.html
https://dom.spec.whatwg.org/#interface-nodeiterator

domonic's ``NodeIterator`` is not live (it snapshots the tree at construction)
and does not implement the "active flag" that makes a recursive filter throw
``InvalidStateError`` -- those rows are skipped.  ``createNodeIterator(root,
null, null)`` giving ``whatToShow == 0`` is skipped for the same reason as the
``TreeWalker`` port.
"""

import unittest

from domonic.dom import Document, NodeFilter
from tests.wpt._harness import assert_equals, assert_true

document = Document()


def _tree():
    root = document.createElement("root")
    a = document.createElement("a")
    root.appendChild(a)
    a.appendChild(document.createTextNode("t1"))
    b = document.createElement("b")
    root.appendChild(b)
    b.appendChild(document.createComment("c1"))
    return root, a, b


class NodeIteratorBasics(unittest.TestCase):
    def test_defaults(self):
        root, _a, _b = _tree()
        it = document.createNodeIterator(root)
        assert_equals(it.toString(), "[object NodeIterator]")
        assert_equals(it.root, root)
        assert_equals(it.whatToShow, 0xFFFFFFFF)
        assert_equals(it.filter, None)
        assert_equals(it.referenceNode, root)
        assert_equals(it.pointerBeforeReferenceNode, True)

    def test_detach_is_a_noop(self):
        it = document.createNodeIterator(document.createElement("x"))
        assert_equals(it.detach(), None)
        assert_equals(it.detach(), None)

    def test_invalid_root_is_a_type_error(self):
        for bad in (None, object(), 1):
            with self.assertRaises(TypeError):
                document.createNodeIterator(bad)

    def test_forward_traversal_visits_the_root_then_every_node_in_tree_order(self):
        root, a, b = _tree()
        it = document.createNodeIterator(root, NodeFilter.SHOW_ALL)
        seen = []
        node = it.nextNode()
        while node is not None:
            seen.append(node)
            node = it.nextNode()
        assert_equals(seen[0], root)
        assert_equals(seen[1], a)
        assert_equals([type(n).__name__ for n in seen[2:4]], ["Text", type(b).__name__])

    def test_show_element_only(self):
        root, a, b = _tree()
        it = document.createNodeIterator(root, NodeFilter.SHOW_ELEMENT)
        seen = []
        node = it.nextNode()
        while node is not None:
            seen.append(node)
            node = it.nextNode()
        assert_equals(seen, [root, a, b])

    def test_show_comment_only(self):
        root, _a, _b = _tree()
        it = document.createNodeIterator(root, NodeFilter.SHOW_COMMENT)
        first = it.nextNode()
        assert_equals(getattr(first, "data", None), "c1")
        assert_equals(it.nextNode(), None)

    def test_filter_function_can_reject(self):
        root, _a, b = _tree()
        it = document.createNodeIterator(
            root,
            NodeFilter.SHOW_ELEMENT,
            lambda n: NodeFilter.FILTER_REJECT if n.tagName == "a" else NodeFilter.FILTER_ACCEPT,
        )
        seen = []
        node = it.nextNode()
        while node is not None:
            seen.append(node.tagName)
            node = it.nextNode()
        # NOTE: NodeIterator FILTER_REJECT behaves like FILTER_SKIP (only the
        # node is skipped, not its subtree) -- but this tree has no elements
        # under <a> anyway, so the observable result is [root, b].
        assert_equals(seen, ["root", "b"])

    def test_filter_exceptions_propagate(self):
        root, _a, _b = _tree()

        def boom(node):
            raise RuntimeError("from filter")

        it = document.createNodeIterator(root, NodeFilter.SHOW_ALL, boom)
        with self.assertRaises(RuntimeError):
            it.nextNode()

    def test_backward_traversal(self):
        root, a, _b = _tree()
        it = document.createNodeIterator(root, NodeFilter.SHOW_ELEMENT)
        while it.nextNode() is not None:
            pass
        seen = []
        node = it.previousNode()
        while node is not None:
            seen.append(node)
            node = it.previousNode()
        assert_true(root in seen and a in seen)


if __name__ == "__main__":
    unittest.main()
