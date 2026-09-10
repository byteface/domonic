"""Ported from wpt/dom/nodes/Document-getElementById.html.
https://dom.spec.whatwg.org/#dom-nonelementparentnode-getelementbyid

domonic backs getElementById with a lazily-built id -> element index that is
kept in sync across mutations; these tests pin the observable behaviour.
"""

import unittest

from domonic.dom import Document

document = Document()


def _tree():
    root = document.createElement("root")
    document.appendChild(root)
    return root


class GetElementById(unittest.TestCase):
    def test_finds_an_element_by_its_id(self):
        root = _tree()
        el = document.createElement("a")
        el.id = "target"
        root.appendChild(el)
        self.assertIs(document.getElementById("target"), el)

    def test_returns_none_for_a_missing_id(self):
        _tree()
        self.assertIsNone(document.getElementById("nope"))

    def test_first_element_in_tree_order_wins_for_a_duplicated_id(self):
        root = _tree()
        first = document.createElement("a")
        first.id = "dup"
        second = document.createElement("b")
        second.id = "dup"
        root.appendChild(first)
        root.appendChild(second)
        self.assertIs(document.getElementById("dup"), first)

    def test_reflects_an_element_added_after_the_first_lookup(self):
        root = _tree()
        self.assertIsNone(document.getElementById("late"))
        el = document.createElement("a")
        el.id = "late"
        root.appendChild(el)
        self.assertIs(document.getElementById("late"), el)

    def test_reflects_an_element_removed_after_a_lookup(self):
        root = _tree()
        el = document.createElement("a")
        el.id = "gone"
        root.appendChild(el)
        self.assertIs(document.getElementById("gone"), el)
        root.removeChild(el)
        self.assertIsNone(document.getElementById("gone"))

    def test_reflects_an_id_renamed_via_the_property(self):
        root = _tree()
        el = document.createElement("a")
        el.id = "before"
        root.appendChild(el)
        self.assertIs(document.getElementById("before"), el)
        el.id = "after"
        self.assertIsNone(document.getElementById("before"))
        self.assertIs(document.getElementById("after"), el)

    def test_reflects_an_id_set_and_removed_via_setattribute(self):
        root = _tree()
        el = document.createElement("a")
        root.appendChild(el)
        el.setAttribute("id", "sa")
        self.assertIs(document.getElementById("sa"), el)
        el.removeAttribute("id")
        self.assertIsNone(document.getElementById("sa"))

    def test_removing_the_first_of_a_duplicate_pair_exposes_the_second(self):
        root = _tree()
        first = document.createElement("a")
        first.id = "dup2"
        second = document.createElement("b")
        second.id = "dup2"
        root.appendChild(first)
        root.appendChild(second)
        self.assertIs(document.getElementById("dup2"), first)
        root.removeChild(first)
        self.assertIs(document.getElementById("dup2"), second)

    def test_reflects_a_wholesale_innerHTML_replacement(self):
        root = _tree()
        old = document.createElement("a")
        old.id = "old"
        root.appendChild(old)
        self.assertIsNotNone(document.getElementById("old"))
        root.innerHTML = '<span id="new">hi</span>'
        self.assertIsNone(document.getElementById("old"))
        self.assertIsNotNone(document.getElementById("new"))

    def test_works_on_a_document_fragment_and_a_detached_element(self):
        frag = document.createDocumentFragment()
        kid = document.createElement("kid")
        kid.id = "fk"
        frag.appendChild(kid)
        self.assertIs(frag.getElementById("fk"), kid)

        subtree = document.createElement("sub")
        inner = document.createElement("inner")
        inner.id = "sk"
        subtree.appendChild(inner)
        self.assertIs(subtree.getElementById("sk"), inner)


if __name__ == "__main__":
    unittest.main()
