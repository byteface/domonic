"""Ported from wpt/html/dom/reflection-misc.html and
wpt/dom/nodes/Element-id.html.
https://html.spec.whatwg.org/multipage/common-dom-interfaces.html#reflecting-content-attributes-in-idl-attributes

IDL string attributes reflect their content attribute as a string and are
never null; boolean attributes reflect presence; ``tabindex`` reflects as a
long with a -1 default.
"""

import unittest

from domonic.dom import Document

document = Document()


class StringReflection(unittest.TestCase):
    def test_id_is_empty_string_when_absent(self):
        el = document.createElement("div")
        self.assertEqual(el.id, "")
        el.id = "x"
        self.assertEqual(el.id, "x")
        self.assertEqual(el.getAttribute("id"), "x")

    def test_className_is_empty_string_when_absent(self):
        el = document.createElement("div")
        self.assertEqual(el.className, "")
        el.className = "a b"
        self.assertEqual(el.className, "a b")
        el.setAttribute("class", "c")
        self.assertEqual(el.className, "c")


class BooleanReflection(unittest.TestCase):
    def test_hidden_reflects_attribute_presence(self):
        el = document.createElement("div")
        self.assertFalse(el.hidden)
        el.hidden = True
        self.assertTrue(el.hidden)
        self.assertTrue(el.hasAttribute("hidden"))
        el.hidden = False
        self.assertFalse(el.hidden)
        self.assertFalse(el.hasAttribute("hidden"))


class TabIndexReflection(unittest.TestCase):
    def test_default_is_minus_one(self):
        self.assertEqual(document.createElement("div").tabIndex, -1)

    def test_reflects_the_integer_value(self):
        el = document.createElement("div")
        el.tabIndex = 3
        self.assertEqual(el.tabIndex, 3)
        self.assertEqual(el.getAttribute("tabindex"), "3")

    def test_invalid_content_attribute_reads_as_minus_one(self):
        el = document.createElement("div")
        el.setAttribute("tabindex", "not-a-number")
        self.assertEqual(el.tabIndex, -1)


if __name__ == "__main__":
    unittest.main()
