"""Ported from wpt/html/semantics/forms/the-form-element/* and
form-control-infrastructure/*.
https://html.spec.whatwg.org/multipage/forms.html#the-form-element
"""

import unittest

from domonic.dom import Document
from domonic.html import button, form
from domonic.html import input as input_
from domonic.html import select, textarea

document = Document()


class FormElements(unittest.TestCase):
    def _form(self):
        return form(
            input_(_type="text", _name="username"),
            input_(_type="radio", _name="color", _value="r"),
            input_(_type="radio", _name="color", _value="g", _checked=True),
            button(_type="submit", _name="go"),
            select(_name="size"),
            textarea(_name="bio"),
        )

    def test_elements_and_length(self):
        f = self._form()
        self.assertEqual(f.length, 6)
        self.assertEqual(len(list(f.elements)), 6)

    def test_named_access_returns_the_single_control(self):
        f = self._form()
        self.assertEqual(f.elements["username"].getAttribute("name"), "username")

    def test_named_access_returns_a_radionodelist_for_a_radio_group(self):
        f = self._form()
        group = f.elements["color"]
        self.assertEqual(len(list(group)), 2)

    def test_radionodelist_value_is_the_checked_radios_value(self):
        f = self._form()
        group = f.elements["color"]
        self.assertEqual(group.value, "g")
        list(group)[0].setAttribute("checked", "")
        list(group)[1].removeAttribute("checked")
        self.assertEqual(group.value, "r")


class FormOwner(unittest.TestCase):
    def test_a_control_reports_its_ancestor_form(self):
        i = input_(_type="text", _name="u")
        b = button(_name="go")
        f = form(i, b)
        self.assertIs(i.form, f)
        self.assertIs(b.form, f)

    def test_the_form_attribute_associates_a_detached_control(self):
        doc = Document()
        root = doc.createElement("root")
        doc.appendChild(root)
        f = doc.createElement("form")
        f.id = "the-form"
        root.appendChild(f)
        control = doc.createElement("input")
        control.setAttribute("form", "the-form")
        root.appendChild(control)
        self.assertIs(control.form, f)

    def test_a_non_form_associated_element_has_no_form(self):
        self.assertIsNone(document.createElement("div").form)
        self.assertIsNone(form().form)


if __name__ == "__main__":
    unittest.main()
