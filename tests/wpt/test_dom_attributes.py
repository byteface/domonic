"""Ported from wpt/dom/nodes/attributes.html (the toggleAttribute and
setAttribute sections) and Element-hasAttribute / Element-removeAttribute.
https://dom.spec.whatwg.org/#dom-element-toggleattribute

The namespaced rows (setAttributeNS / getAttributeNS / attributes[i].namespaceURI)
are skipped -- domonic's setAttributeNS ignores the namespace (a tracked
deviation).  Per the upstream ``productions.js`` the only universally-invalid
attribute name for these APIs is the empty string.
"""

import unittest

from domonic.dom import Document
from tests.wpt._harness import assert_equals, assert_false, assert_throws_dom, assert_true

document = Document()


class ToggleAttribute(unittest.TestCase):
    def test_empty_name_throws_invalid_character_error(self):
        el = document.createElement("foo")
        assert_throws_dom("InvalidCharacterError", lambda: el.toggleAttribute("", True))
        assert_throws_dom("InvalidCharacterError", lambda: el.toggleAttribute(""))
        assert_throws_dom("InvalidCharacterError", lambda: el.toggleAttribute("", False))

    def test_lowercases_its_name_argument(self):
        el = document.createElement("div")
        assert_true(el.toggleAttribute("ALIGN"))
        assert_true(el.hasAttribute("align"))
        assert_true(el.hasAttributeNS("", "align"))
        assert_false(el.toggleAttribute("ALIGN"))
        assert_false(el.hasAttribute("align"))
        assert_false(el.hasAttributeNS("", "align"))

    def test_no_force_toggles(self):
        el = document.createElement("div")
        assert_true(el.toggleAttribute("x"))
        assert_true(el.hasAttribute("x"))
        assert_false(el.toggleAttribute("x"))
        assert_false(el.hasAttribute("x"))

    def test_force_true_is_a_noop_when_already_present_and_keeps_the_value(self):
        el = document.createElement("div")
        el.setAttribute("a", "thing")
        assert_true(el.toggleAttribute("a", True))
        assert_equals(el.getAttribute("a"), "thing")

    def test_force_false_is_a_noop_when_absent(self):
        el = document.createElement("div")
        assert_false(el.toggleAttribute("a", False))
        assert_false(el.hasAttribute("a"))

    def test_does_not_change_the_order_of_previously_set_attributes(self):
        el = document.createElement("foo")
        el.toggleAttribute("a")
        el.toggleAttribute("b")
        el.setAttribute("a", "thing")
        el.toggleAttribute("c")
        assert_equals(el.getAttributeNames(), ["a", "b", "c"])
        assert_equals([el.getAttribute(n) for n in el.getAttributeNames()], ["thing", "", ""])

    def test_toggling_style_off_clears_inline_style(self):
        el = document.createElement("foo")
        el.style = "color: red; background-color: green"
        assert_false(el.toggleAttribute("style"))
        assert_false(el.hasAttribute("style"))


class SetAttribute(unittest.TestCase):
    def test_empty_name_throws(self):
        el = document.createElement("foo")
        assert_throws_dom("InvalidCharacterError", lambda: el.setAttribute("", "test"))

    def test_lowercases_its_name_argument(self):
        el = document.createElement("div")
        el.setAttribute("CHEEseCaKe", "tasty")
        assert_equals(el.getAttribute("cheesecake"), "tasty")

    def test_xmlns_prefixed_names_do_not_throw(self):
        el = document.createElement("foo")
        for name in ("xmlns", "xmlns:a", "xmlnsx", "xmlns0"):
            el.setAttribute(name, "success")
            assert_equals(el.getAttribute(name), "success")

    def test_last_write_wins_and_order_is_stable(self):
        el = document.createElement("foo")
        el.setAttribute("a", "1")
        el.setAttribute("b", "2")
        el.setAttribute("a", "3")
        el.setAttribute("c", "4")
        assert_equals(el.getAttributeNames(), ["a", "b", "c"])
        assert_equals([el.getAttribute(n) for n in el.getAttributeNames()], ["3", "2", "4"])


class HasAndRemoveAttribute(unittest.TestCase):
    def test_missing_attribute_get_is_none_has_is_false(self):
        el = document.createElement("div")
        assert_equals(el.getAttribute("x"), None)
        assert_false(el.hasAttribute("x"))

    def test_remove_is_a_noop_for_a_missing_attribute(self):
        el = document.createElement("div")
        el.removeAttribute("x")  # must not raise
        assert_false(el.hasAttribute("x"))

    def test_has_attributes(self):
        el = document.createElement("div")
        assert_false(el.hasAttributes())
        el.setAttribute("x", "1")
        assert_true(el.hasAttributes())
        el.removeAttribute("x")
        assert_false(el.hasAttributes())


if __name__ == "__main__":
    unittest.main()
