"""Ported from wpt/dom/nodes/ChildNode-replaceWith.html and ChildNode-before/after.
https://dom.spec.whatwg.org/#interface-childnode

The ``null`` / ``undefined`` argument cases are skipped -- they exercise
WebIDL's ``DOMString`` coercion (``null`` -> ``"null"``), which has no Python
equivalent.  Assertions on ``parent.innerHTML`` use the WHATWG fragment
serialiser (``Element.innerHTML``), which is browser-compatible in domonic.
"""

import unittest

from domonic.dom import Document
from tests.wpt._harness import assert_equals

document = Document()


def _parent_and_child(kind):
    parent = document.createElement("div")
    if kind == "Element":
        child, inner = document.createElement("test"), "<test></test>"
    elif kind == "Comment":
        child, inner = document.createComment("test"), "<!--test-->"
    else:
        child, inner = document.createTextNode("test"), "test"
    parent.appendChild(child)
    return parent, child, inner


class ChildNodeReplaceWith(unittest.TestCase):
    def _run(self, kind):
        parent, child, inner = _parent_and_child(kind)
        child.replaceWith()
        assert_equals(parent.innerHTML, "", "no argument")

        parent, child, inner = _parent_and_child(kind)
        child.replaceWith("")
        assert_equals(parent.innerHTML, "", "empty string")

        parent, child, inner = _parent_and_child(kind)
        child.replaceWith("text")
        assert_equals(parent.innerHTML, "text", "only text")

        parent, child, inner = _parent_and_child(kind)
        x = document.createElement("x")
        child.replaceWith(x)
        assert_equals(parent.innerHTML, "<x></x>", "one element")

        parent, child, inner = _parent_and_child(kind)
        x, y, z = (document.createElement(n) for n in "xyz")
        parent.appendChild(y)
        parent.insertBefore(y, child)
        parent.appendChild(x)
        child.replaceWith(x, y, z)
        assert_equals(parent.innerHTML, "<x></x><y></y><z></z>", "siblings as args")

        parent, child, inner = _parent_and_child(kind)
        x = document.createElement("x")
        parent.appendChild(x)
        parent.appendChild(document.createTextNode("1"))
        child.replaceWith(x, "2")
        assert_equals(parent.innerHTML, "<x></x>21", "sibling + text")

        parent, child, inner = _parent_and_child(kind)
        x = document.createElement("x")
        parent.appendChild(x)
        parent.appendChild(document.createTextNode("text"))
        child.replaceWith(x, child)
        assert_equals(parent.innerHTML, "<x></x>" + inner + "text", "sibling + child itself")

        parent, child, inner = _parent_and_child(kind)
        x = document.createElement("x")
        child.replaceWith(x, "text")
        assert_equals(parent.innerHTML, "<x></x>text", "one element + text")

    def test_replace_with_element_child(self):
        self._run("Element")

    def test_replace_with_comment_child(self):
        self._run("Comment")

    def test_replace_with_text_child(self):
        self._run("Text")


class ChildNodeBeforeAfter(unittest.TestCase):
    def test_before_inserts_text_and_elements_in_order(self):
        parent = document.createElement("div")
        child = document.createElement("c")
        parent.appendChild(child)
        x = document.createElement("x")
        child.before(x, "text")
        assert_equals(parent.innerHTML, "<x></x>text<c></c>")

    def test_before_with_context_object_itself_is_a_noop_move(self):
        parent = document.createElement("div")
        child = document.createElement("c")
        parent.appendChild(child)
        child.before("text", child)
        assert_equals(parent.innerHTML, "text<c></c>")

    def test_after_inserts_text_and_elements_in_order(self):
        parent = document.createElement("div")
        child = document.createElement("c")
        parent.appendChild(child)
        x = document.createElement("x")
        child.after(x, "text")
        assert_equals(parent.innerHTML, "<c></c><x></x>text")

    def test_before_with_all_siblings_as_args_reorders(self):
        parent = document.createElement("div")
        child = document.createElement("c")
        x, y, z = (document.createElement(n) for n in "xyz")
        parent.appendChild(y)
        parent.appendChild(child)
        parent.appendChild(x)
        child.before(x, y, z)
        assert_equals(parent.innerHTML, "<x></x><y></y><z></z><c></c>")


if __name__ == "__main__":
    unittest.main()
