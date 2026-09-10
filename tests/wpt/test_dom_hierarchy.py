"""Ported from wpt/dom/nodes/Node-appendChild.html, Node-insertBefore.html and
Node-replaceChild.html -- the "pre-insertion validity" checks.
https://dom.spec.whatwg.org/#concept-node-ensure-pre-insertion-validity

Only the clauses domonic enforces are ported here: a node may not be inserted
into itself or into one of its own descendants (that would build a cycle and
hang traversal), and ``insertBefore`` with a reference node that is not a child
throws ``NotFoundError``.  The WebIDL argument-type clauses and the
document-shape clauses (one element child, doctype placement, ...) are left
permissive by domonic and are not ported.
"""

import unittest

import pytest

from domonic.dom import Document
from tests.wpt._harness import assert_throws_dom

document = Document()


class NodeAppendChildValidity(unittest.TestCase):
    def test_appending_a_node_to_itself_throws_hierarchy_request(self):
        node = document.createElement("div")
        assert_throws_dom("HierarchyRequestError", lambda: node.appendChild(node))

    def test_appending_an_ancestor_throws_hierarchy_request(self):
        grandparent = document.createElement("grandparent")
        parent = document.createElement("parent")
        child = document.createElement("child")
        grandparent.appendChild(parent)
        parent.appendChild(child)
        assert_throws_dom("HierarchyRequestError", lambda: child.appendChild(grandparent))
        assert_throws_dom("HierarchyRequestError", lambda: child.appendChild(parent))


class NodeInsertBeforeValidity(unittest.TestCase):
    def test_reference_node_not_a_child_throws_not_found(self):
        parent = document.createElement("parent")
        parent.appendChild(document.createElement("existing"))
        stranger = document.createElement("stranger")
        incoming = document.createElement("incoming")
        assert_throws_dom("NotFoundError", lambda: parent.insertBefore(incoming, stranger))

    def test_reference_node_not_a_child_does_not_orphan_incoming(self):
        keeper = document.createElement("keeper")
        movable = document.createElement("movable")
        keeper.appendChild(movable)
        target = document.createElement("target")
        target.appendChild(document.createElement("existing"))
        stranger = document.createElement("stranger")
        try:
            target.insertBefore(movable, stranger)
        except Exception:
            pass
        self.assertIs(movable.parentNode, keeper)

    def test_inserting_an_ancestor_throws_hierarchy_request(self):
        parent = document.createElement("parent")
        child = document.createElement("child")
        parent.appendChild(child)
        ref = document.createElement("ref")
        child.appendChild(ref)
        assert_throws_dom("HierarchyRequestError", lambda: child.insertBefore(parent, ref))


class NodeReplaceChildValidity(unittest.TestCase):
    def test_replacing_with_an_ancestor_throws_hierarchy_request(self):
        parent = document.createElement("parent")
        child = document.createElement("child")
        parent.appendChild(child)
        old = document.createElement("old")
        child.appendChild(old)
        assert_throws_dom("HierarchyRequestError", lambda: child.replaceChild(parent, old))

    @pytest.mark.xfail(
        reason="domonic's replaceChild returns oldChild unchanged when it is not "
        "a child, instead of throwing NotFoundError",
        strict=True,
    )
    def test_old_child_not_a_child_throws_not_found(self):
        parent = document.createElement("parent")
        parent.appendChild(document.createElement("existing"))
        stranger = document.createElement("stranger")
        incoming = document.createElement("incoming")
        assert_throws_dom("NotFoundError", lambda: parent.replaceChild(incoming, stranger))


if __name__ == "__main__":
    unittest.main()
