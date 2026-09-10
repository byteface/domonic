"""Ported from wpt/html/dom/documents/dom-tree-accessors/document.forms-*.html,
Document.images.html, Document.links.html, Document.scripts.html.
https://html.spec.whatwg.org/multipage/dom.html#dom-document-forms

These accessors return live HTMLCollections.
"""

import unittest

from domonic.dom import HTMLCollection
from domonic.html import a, area, body, form, head, html, img, script


def _page():
    return html(
        head(script("x")),
        body(
            form(_name="f1"),
            a("link", _href="http://example.org"),
            a("just a name", _name="top"),
            img(_src="a.png"),
            area(_href="http://example.org/area"),
        ),
    )


class DocumentCollections(unittest.TestCase):
    def test_each_accessor_is_an_htmlcollection(self):
        page = _page()
        for name in ("forms", "images", "links", "scripts", "anchors", "embeds"):
            self.assertIsInstance(getattr(page, name), HTMLCollection, name)

    def test_forms_images_scripts_select_by_tag(self):
        page = _page()
        self.assertEqual(len(list(page.forms)), 1)
        self.assertEqual(len(list(page.images)), 1)
        self.assertEqual(len(list(page.scripts)), 1)

    def test_links_are_a_and_area_with_href(self):
        page = _page()
        tags = sorted((el.tagName or "").lower() for el in page.links)
        self.assertEqual(tags, ["a", "area"])

    def test_anchors_are_a_with_name(self):
        page = _page()
        anchors = list(page.anchors)
        self.assertEqual(len(anchors), 1)
        self.assertEqual(anchors[0].getAttribute("name"), "top")

    def test_collections_are_live(self):
        page = _page()
        forms = page.forms
        self.assertEqual(len(list(forms)), 1)
        page.querySelector("body").appendChild(form(_name="f2"))
        self.assertEqual(len(list(forms)), 2)


if __name__ == "__main__":
    unittest.main()
