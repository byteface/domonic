"""Ported from wpt/dom/nodes/Element-matches.html and Element-closest.html
(the rows domonic's selector engine supports, plus the :scope behaviour).
https://dom.spec.whatwg.org/#dom-element-matches
"""

import unittest

from domonic.dom import Document

document = Document()


def _tree():
    root = document.createElement("div")
    root.setAttribute("class", "root")
    document.appendChild(root)
    section = document.createElement("section")
    section.setAttribute("id", "s")
    root.appendChild(section)
    p = document.createElement("p")
    p.setAttribute("class", "lead highlight")
    section.appendChild(p)
    span = document.createElement("span")
    p.appendChild(span)
    return root, section, p, span


class Matches(unittest.TestCase):
    def test_type_class_and_id(self):
        _root, section, p, _span = _tree()
        self.assertTrue(p.matches("p"))
        self.assertTrue(p.matches(".lead"))
        self.assertTrue(p.matches(".lead.highlight"))
        self.assertFalse(p.matches(".lead.missing"))
        self.assertTrue(section.matches("#s"))
        self.assertTrue(section.matches("section#s"))

    def test_selector_list(self):
        _root, _section, p, _span = _tree()
        self.assertTrue(p.matches("a, p, span"))
        self.assertFalse(p.matches("a, b, i"))

    def test_descendant_combinator(self):
        root, _section, p, span = _tree()
        self.assertTrue(span.matches("div span"))
        self.assertTrue(span.matches("section p span"))
        self.assertFalse(span.matches("p div span"))

    def test_scope_matches_the_element_itself(self):
        _root, _section, p, span = _tree()
        self.assertTrue(span.matches(":scope"))
        self.assertTrue(p.matches(":scope"))
        self.assertTrue(p.matches("p:scope"))
        self.assertFalse(p.matches("span:scope"))
        self.assertTrue(p.matches(".lead:scope"))


class Closest(unittest.TestCase):
    def test_walks_up_the_ancestor_chain(self):
        root, section, p, span = _tree()
        self.assertIs(span.closest("p"), p)
        self.assertIs(span.closest("section"), section)
        self.assertIs(span.closest("div"), root)
        self.assertIs(span.closest(".root"), root)

    def test_matches_the_element_itself_first(self):
        _root, _section, p, _span = _tree()
        self.assertIs(p.closest("p"), p)
        self.assertIs(p.closest(":scope"), p)

    def test_returns_none_when_nothing_matches(self):
        _root, _section, _p, span = _tree()
        self.assertIsNone(span.closest("table"))


if __name__ == "__main__":
    unittest.main()
