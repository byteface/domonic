"""Ported from the DocumentFragment rows of wpt/dom/nodes/Node-appendChild.html,
Node-insertBefore.html and Node-replaceChild.html.
https://dom.spec.whatwg.org/#concept-node-insert

Inserting a DocumentFragment moves its children into the parent and leaves the
fragment empty; an empty fragment is a no-op.

``tagName`` is compared lower-case here: these elements are built with
``createElement`` without an owning HTML document, so domonic does not
upper-case them (a tracked deviation -- see ``tests/wpt/README.md``).
"""

import unittest

from domonic.dom import Document

document = Document()


def _fragment(*names):
    frag = document.createDocumentFragment()
    for name in names:
        frag.appendChild(document.createElement(name))
    return frag


class AppendChildFragment(unittest.TestCase):
    def test_children_are_moved_and_the_fragment_is_emptied(self):
        root = document.createElement("root")
        frag = _fragment("a", "b")
        a, b = list(frag.childNodes)
        root.appendChild(frag)
        self.assertEqual([c.tagName for c in root.children], ["a", "b"])
        self.assertEqual(len(list(frag.childNodes)), 0)
        self.assertIs(a.parentNode, root)
        self.assertIs(b.parentNode, root)

    def test_appendChild_returns_the_fragment(self):
        root = document.createElement("root")
        frag = _fragment("a")
        self.assertIs(root.appendChild(frag), frag)

    def test_empty_fragment_is_a_noop(self):
        root = document.createElement("root")
        root.appendChild(document.createElement("keep"))
        root.appendChild(document.createDocumentFragment())
        self.assertEqual([c.tagName for c in root.children], ["keep"])


class InsertBeforeFragment(unittest.TestCase):
    def test_fragment_children_are_inserted_before_the_reference(self):
        root = document.createElement("root")
        ref = document.createElement("ref")
        root.appendChild(ref)
        root.insertBefore(_fragment("x", "y"), ref)
        self.assertEqual([c.tagName for c in root.children], ["x", "y", "ref"])


class ReplaceChildFragment(unittest.TestCase):
    def test_fragment_children_replace_the_old_child(self):
        root = document.createElement("root")
        old = document.createElement("old")
        keep = document.createElement("keep")
        root.appendChild(old)
        root.appendChild(keep)
        root.replaceChild(_fragment("x", "y"), old)
        self.assertEqual([c.tagName for c in root.children], ["x", "y", "keep"])


if __name__ == "__main__":
    unittest.main()
