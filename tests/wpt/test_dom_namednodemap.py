"""Ported from wpt/dom/nodes/attributes-namednodemap.html and attributes.html
(the NamedNodeMap rows).
https://dom.spec.whatwg.org/#interface-namednodemap

domonic stores attributes as plain strings, not live ``Attr`` nodes, so the
rows that assert ``removeNamedItem`` returns the *same* object passed to
``setNamedItem`` and the WebIDL named-property field access (``map.attr1``)
are not ported.
"""

import unittest

from domonic.dom import Attr, Document, DOMException

document = Document()


class NamedNodeMap(unittest.TestCase):
    def _element(self):
        el = document.createElement("div")
        el.setAttribute("a", "1")
        el.setAttribute("b", "2")
        el.setAttribute("c", "3")
        return el

    def test_length_and_item(self):
        attrs = self._element().attributes
        self.assertEqual(attrs.length, 3)
        self.assertEqual(len(attrs), 3)
        self.assertEqual((attrs.item(0).name, attrs.item(0).value), ("a", "1"))
        self.assertIsNone(attrs.item(3))
        self.assertIsNone(attrs.item(99))

    def test_getNamedItem(self):
        attrs = self._element().attributes
        self.assertEqual(attrs.getNamedItem("b").value, "2")
        self.assertIsNone(attrs.getNamedItem("missing"))

    def test_iteration_is_in_insertion_order(self):
        attrs = self._element().attributes
        self.assertEqual([(a.name, a.value) for a in attrs], [("a", "1"), ("b", "2"), ("c", "3")])

    def test_setNamedItem_adds_the_attribute_to_the_element(self):
        el = self._element()
        el.attributes.setNamedItem(Attr("d", "4"))
        self.assertEqual(el.getAttribute("d"), "4")
        self.assertEqual(el.attributes.length, 4)

    def test_removeNamedItem_removes_and_returns_the_attribute(self):
        el = self._element()
        removed = el.attributes.removeNamedItem("a")
        self.assertEqual(removed.name, "a")
        self.assertEqual(el.getAttributeNames(), ["b", "c"])

    def test_removeNamedItem_on_a_missing_attribute_throws_not_found(self):
        attrs = self._element().attributes
        with self.assertRaises(DOMException) as ctx:
            attrs.removeNamedItem("nope")
        self.assertEqual(ctx.exception.name, "NotFoundError")


if __name__ == "__main__":
    unittest.main()
