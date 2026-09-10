"""Ported from wpt/dom/nodes/ParentNode-append.html, ParentNode-prepend.html,
ParentNode-replaceChildren.html and ParentNode-querySelector-All.html.
https://dom.spec.whatwg.org/#interface-parentnode

The ``null`` / ``undefined`` argument rows are skipped (WebIDL ``DOMString``
coercion).  Text arguments are checked with ``str(child)`` rather than
``child.textContent`` because domonic stores programmatic text as a raw
``str`` (see ``domonic-raw-string-text-model``).
"""

import unittest

from domonic.dom import Document
from tests.wpt._harness import assert_array_equals, assert_equals

document = Document()


def _parents():
    yield "Element", document.createElement("div")
    yield "DocumentFragment", document.createDocumentFragment()
    yield "Document", Document()


class ParentNodeAppend(unittest.TestCase):
    def test_append_nothing_on_empty_parent(self):
        for _name, parent in _parents():
            parent.append()
            assert_array_equals(parent.childNodes, [])

    def test_append_only_text(self):
        for name, parent in _parents():
            parent.append("text")
            assert_equals(str(parent.childNodes[0]), "text", name)

    def test_append_one_element(self):
        for name, parent in _parents():
            x = document.createElement("x")
            parent.append(x)
            assert_array_equals(parent.childNodes, [x], name)

    def test_append_element_and_text_after_an_existing_child(self):
        for name, parent in _parents():
            child = document.createElement("test")
            parent.appendChild(child)
            x = document.createElement("x")
            parent.append(x, "text")
            assert_equals(parent.childNodes[0], child, name)
            assert_equals(parent.childNodes[1], x, name)
            assert_equals(str(parent.childNodes[2]), "text", name)

    def test_append_deduplicates_keeping_the_last_position(self):
        for name, parent in _parents():
            x = document.createElement("x")
            y = document.createElement("y")
            parent.append(x, y, x)
            assert_array_equals(list(parent.childNodes), [y, x], name)


class ParentNodePrepend(unittest.TestCase):
    def test_prepend_before_an_existing_child(self):
        for name, parent in _parents():
            child = document.createElement("test")
            parent.appendChild(child)
            x = document.createElement("x")
            parent.prepend(x, "text")
            assert_equals(parent.childNodes[0], x, name)
            assert_equals(str(parent.childNodes[1]), "text", name)
            assert_equals(parent.childNodes[2], child, name)


class ParentNodeReplaceChildren(unittest.TestCase):
    def test_replace_all_children(self):
        for name, parent in _parents():
            parent.appendChild(document.createElement("old1"))
            parent.appendChild(document.createElement("old2"))
            a = document.createElement("a")
            parent.replaceChildren(a, "tail")
            assert_equals(parent.childNodes[0], a, name)
            assert_equals(str(parent.childNodes[1]), "tail", name)
            assert_equals(len(list(parent.childNodes)), 2, name)

    def test_replace_children_with_nothing_empties_the_parent(self):
        for name, parent in _parents():
            parent.appendChild(document.createElement("old"))
            parent.replaceChildren()
            assert_array_equals(parent.childNodes, [], name)


class ParentNodeElementAccessors(unittest.TestCase):
    def test_first_last_element_child_and_count(self):
        for name, parent in _parents():
            assert_equals(parent.firstElementChild, None, name)
            assert_equals(parent.lastElementChild, None, name)
            parent.append(document.createTextNode("t"))
            a = document.createElement("a")
            b = document.createElement("b")
            parent.append(a, document.createTextNode("u"), b)
            assert_equals(parent.firstElementChild, a, name)
            assert_equals(parent.lastElementChild, b, name)
            assert_equals(parent.childElementCount, 2, name)

    def test_children_excludes_text(self):
        parent = document.createElement("div")
        parent.append("x", document.createElement("a"), "y", document.createElement("b"))
        assert_array_equals(list(parent.children), list(parent.getElementsByTagName("*")))


class ParentNodeQuerySelector(unittest.TestCase):
    def test_querySelector_and_all_on_a_fragment(self):
        frag = document.createDocumentFragment()
        a = document.createElement("a")
        a.setAttribute("class", "pick")
        b = document.createElement("b")
        b.setAttribute("class", "pick")
        frag.append(a, b)
        assert_equals(frag.querySelector(".pick"), a)
        assert_array_equals(list(frag.querySelectorAll(".pick")), [a, b])


if __name__ == "__main__":
    unittest.main()
