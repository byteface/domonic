"""Ported from wpt/dom/nodes/insert-adjacent.html
https://dom.spec.whatwg.org/#dom-element-insertadjacentelement

``insertAdjacentText`` assertions check the inserted string value directly
rather than ``previousSibling.textContent`` -- domonic stores programmatic text
as a raw ``str`` rather than a ``Text`` node (see
``domonic-raw-string-text-model``).  The ``createHTMLDocument().documentElement``
rows are skipped (domonic's ``documentElement`` is a ``Document`` subclass, a
tracked quirk).
"""

import unittest

from domonic.dom import Document
from tests.wpt._harness import assert_equals, assert_throws_dom

document = Document()

POSITIONS = {
    "beforebegin": "previousSibling",
    "afterbegin": "firstChild",
    "beforeend": "lastChild",
    "afterend": "nextSibling",
}
TEXTS = {
    "beforebegin": "raclette",
    "afterbegin": "tartiflette",
    "beforeend": "lasagne",
    "afterend": "gateau",
}


def _fresh_target():
    parent = document.createElement("parent")
    el = document.createElement("element")
    parent.appendChild(el)
    return parent, el


class InsertAdjacentElement(unittest.TestCase):
    def test_each_position_places_the_element(self):
        for position, accessor in POSITIONS.items():
            parent, el = _fresh_target()
            div = document.createElement("h3")
            div.id = TEXTS[position]
            el.insertAdjacentElement(position, div)
            assert_equals(getattr(el, accessor).id, TEXTS[position], position)

    def test_returns_null_when_there_is_no_parent(self):
        orphan = document.createElement("div")
        other = document.createElement("other")
        assert_equals(orphan.insertAdjacentElement("beforebegin", other), None)
        assert_equals(orphan.insertAdjacentElement("afterend", other), None)

    def test_invalid_position_is_a_syntax_error(self):
        _parent, el = _fresh_target()
        div = document.createElement("h3")
        assert_throws_dom("SyntaxError", lambda: el.insertAdjacentElement("heeeee", div))


class InsertAdjacentText(unittest.TestCase):
    def test_each_position_places_the_text(self):
        for position in POSITIONS:
            parent, el = _fresh_target()
            el.insertAdjacentText(position, TEXTS[position])
            if position == "beforebegin":
                assert_equals(str(el.previousSibling), TEXTS[position], position)
            elif position == "afterend":
                assert_equals(str(el.nextSibling), TEXTS[position], position)
            elif position == "afterbegin":
                assert_equals(str(el.firstChild), TEXTS[position], position)
            else:
                assert_equals(str(el.lastChild), TEXTS[position], position)

    def test_invalid_position_is_a_syntax_error(self):
        _parent, el = _fresh_target()
        assert_throws_dom("SyntaxError", lambda: el.insertAdjacentText("hoooo", "canard"))


if __name__ == "__main__":
    unittest.main()
