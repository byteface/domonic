"""Ported from wpt/html/semantics/scripting-1/the-template-element/*.
https://html.spec.whatwg.org/multipage/scripting.html#the-template-element

domonic keeps a ``<template>``'s parsed markup as the element's own children
and exposes them through ``.content`` as a DocumentFragment view.
"""

import unittest

from domonic.dom import Document, DocumentFragment

document = Document()


class TemplateContent(unittest.TestCase):
    def test_content_is_a_document_fragment(self):
        tpl = document.createElement("template")
        self.assertIsInstance(tpl.content, DocumentFragment)

    def test_setting_innerHTML_fills_the_content(self):
        tpl = document.createElement("template")
        tpl.innerHTML = "<p>x</p><span>y</span>"
        self.assertEqual([c.tagName for c in tpl.content.childNodes], ["P", "SPAN"])
        self.assertEqual(tpl.innerHTML, "<p>x</p><span>y</span>")

    def test_reading_content_repeatedly_does_not_consume_it(self):
        tpl = document.createElement("template")
        tpl.innerHTML = "<p>x</p>"
        first = len(list(tpl.content.childNodes))
        second = len(list(tpl.content.childNodes))
        self.assertEqual((first, second), (1, 1))

    def test_appendChild_content_shows_up(self):
        tpl = document.createElement("template")
        tpl.appendChild(document.createElement("div"))
        self.assertEqual([c.tagName for c in tpl.content.childNodes], ["div"])


if __name__ == "__main__":
    unittest.main()
