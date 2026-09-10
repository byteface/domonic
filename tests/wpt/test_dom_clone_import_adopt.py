"""Ported from wpt/dom/nodes/Node-cloneNode.html, Document-importNode.html and
Document-adoptNode.html.
https://dom.spec.whatwg.org/#dom-node-clonenode
"""

import unittest

from domonic.dom import Document, DOMException

document = Document()


class CloneNode(unittest.TestCase):
    def test_deep_clone_of_an_element_copies_attributes_and_the_subtree(self):
        p = document.createElement("p")
        p.setAttribute("id", "x")
        p.setAttribute("class", "c")
        span = document.createElement("span")
        p.appendChild(span)
        span.appendChild(document.createTextNode("hi"))

        clone = p.cloneNode(True)
        self.assertIsNot(clone, p)
        self.assertIsNone(clone.parentNode)
        self.assertEqual(clone.getAttribute("id"), "x")
        self.assertEqual(clone.getAttribute("class"), "c")
        self.assertEqual(len(list(clone.childNodes)), 1)
        self.assertEqual(clone.firstChild.firstChild.data, "hi")
        self.assertTrue(p.isEqualNode(clone))

    def test_shallow_clone_drops_children_keeps_attributes(self):
        p = document.createElement("p")
        p.setAttribute("id", "x")
        p.appendChild(document.createElement("span"))
        clone = p.cloneNode(False)
        self.assertEqual(len(list(clone.childNodes)), 0)
        self.assertEqual(clone.getAttribute("id"), "x")

    def test_clone_text_comment_and_doctype(self):
        t = document.createTextNode("abc")
        self.assertEqual(t.cloneNode().data, "abc")
        self.assertIsNot(t.cloneNode(), t)

        c = document.createComment("cc")
        self.assertEqual(c.cloneNode().data, "cc")

        dt = document.implementation.createDocumentType("html", "p", "s")
        dtc = dt.cloneNode()
        self.assertEqual((dtc.name, dtc.publicId, dtc.systemId), ("html", "p", "s"))

    def test_clone_document_fragment(self):
        frag = document.createDocumentFragment()
        frag.appendChild(document.createElement("a"))
        clone = frag.cloneNode(True)
        self.assertEqual(clone.nodeType, 11)
        self.assertEqual(len(list(clone.childNodes)), 1)

    def test_clone_does_not_carry_event_listeners(self):
        el = document.createElement("button")
        hits = []
        el.addEventListener("click", lambda e: hits.append(1))
        clone = el.cloneNode(True)
        from domonic.events import Event

        clone.dispatchEvent(Event("click"))
        self.assertEqual(hits, [])


class ImportNode(unittest.TestCase):
    def test_import_copies_the_node_into_the_target_document(self):
        source = Document()
        root = source.createElement("r")
        source.appendChild(root)
        el = source.createElement("x")
        el.setAttribute("id", "y")
        root.appendChild(el)
        el.appendChild(source.createElement("kid"))

        imported = document.importNode(el, True)
        self.assertIsNot(imported, el)
        self.assertIs(imported.ownerDocument, document)
        self.assertEqual(len(list(imported.childNodes)), 1)
        # the original is untouched
        self.assertIs(el.parentNode, root)

    def test_shallow_import(self):
        source = Document()
        el = source.createElement("x")
        el.appendChild(source.createElement("kid"))
        imported = document.importNode(el, False)
        self.assertEqual(len(list(imported.childNodes)), 0)


class AdoptNode(unittest.TestCase):
    def test_adopt_moves_the_node_and_its_subtree(self):
        source = Document()
        target = Document()
        root = source.createElement("r")
        source.appendChild(root)
        el = source.createElement("x")
        root.appendChild(el)
        el.appendChild(source.createElement("kid"))

        adopted = target.adoptNode(el)
        self.assertIs(adopted, el)
        self.assertIsNone(el.parentNode)
        self.assertIs(el.ownerDocument, target)
        self.assertIs(el.firstChild.ownerDocument, target)
        self.assertNotIn(el, list(root.childNodes))

    def test_adopting_a_document_is_not_supported(self):
        target = Document()
        with self.assertRaises(DOMException) as ctx:
            target.adoptNode(Document())
        self.assertEqual(ctx.exception.name, "NotSupportedError")


if __name__ == "__main__":
    unittest.main()
