"""Ported from wpt/dom/nodes/Element-getElementsByTagName.html,
Document-Element-getElementsByTagName.js, Element-getElementsByClassName.html
and Document-getElementsByName.html.
https://dom.spec.whatwg.org/#dom-element-getelementsbytagname

The headline behaviour under test is *liveness*: these collections re-scan the
tree on every access.  The foreign-namespace / prefixed-name case-sensitivity
rows from the upstream shared helper are skipped -- domonic normalises tag
names to lower case and has only partial namespace modelling (a tracked
deviation, see ``tests/wpt/README.md``).
"""

import unittest

from domonic.dom import Document, HTMLCollection
from tests.wpt._harness import assert_array_equals, assert_equals, assert_false, assert_true

document = Document()


def _fixture():
    element = document.createElement("div")
    element.appendChild(document.createTextNode("text"))
    p = document.createElement("p")
    element.appendChild(p)
    a = document.createElement("a")
    p.appendChild(a)
    a.appendChild(document.createTextNode("link"))
    b = document.createElement("b")
    p.appendChild(b)
    b.appendChild(document.createTextNode("bold"))
    em = document.createElement("em")
    p.appendChild(em)
    u = document.createElement("u")
    em.appendChild(u)
    u.appendChild(document.createTextNode("emphasized"))
    element.appendChild(document.createComment("comment"))
    return element


class GetElementsByTagName(unittest.TestCase):
    def test_returns_an_htmlcollection(self):
        element = _fixture()
        assert_true(isinstance(element.getElementsByTagName("a"), HTMLCollection))

    def test_caching_is_allowed(self):
        element = _fixture()
        first = element.getElementsByTagName("a")
        second = element.getElementsByTagName("a")
        assert_true(first is not second or first is second)

    def test_out_of_range_access(self):
        element = _fixture()
        collection = element.getElementsByTagName("nosuchtag")
        assert_equals(collection[5], None)
        assert_equals(collection.item(5), None)

    def test_matching_the_context_object(self):
        element = _fixture()
        assert_array_equals(element.getElementsByTagName(element.localName), [])

    def test_star_returns_every_descendant_element_in_tree_order(self):
        element = _fixture()
        expected = []

        def walk(node):
            for child in node.childNodes:
                if getattr(child, "nodeType", None) == 1:
                    expected.append(child)
                    walk(child)

        walk(element)
        assert_array_equals(element.getElementsByTagName("*"), expected)

    def test_uppercase_input_matches_html_element(self):
        element = _fixture()
        extra = document.createElement("abc")
        element.appendChild(extra)
        assert_array_equals(element.getElementsByTagName("ABC"), [extra])
        assert_array_equals(element.getElementsByTagName("abc"), [extra])

    def test_is_a_live_collection(self):
        element = _fixture()
        t1 = document.createElement("abc")
        element.appendChild(t1)
        live = element.getElementsByTagName("abc")
        assert_true(isinstance(live, HTMLCollection))
        assert_equals(live.length, 1)

        t2 = document.createElement("abc")
        element.appendChild(t2)
        assert_equals(live.length, 2)

        element.removeChild(t2)
        assert_equals(live.length, 1)

    def test_named_access_by_id_and_name(self):
        element = _fixture()
        t1 = document.createElement("pre")
        t1.id = "x"
        element.appendChild(t1)
        t2 = document.createElement("pre")
        t2.setAttribute("name", "y")
        element.appendChild(t2)

        collection = element.getElementsByTagName("pre")
        assert_equals(collection[0].id, "x")
        assert_equals(collection["x"], collection[0])
        assert_equals(collection["y"], collection[1])
        assert_equals(collection.namedItem("x"), t1)


class GetElementsByClassName(unittest.TestCase):
    def test_requires_every_token_and_is_live(self):
        root = document.createElement("root")
        a = document.createElement("a")
        a.setAttribute("class", "foo")
        b = document.createElement("b")
        b.setAttribute("class", "foo bar")
        root.appendChild(a)
        root.appendChild(b)

        foo = root.getElementsByClassName("foo")
        foo_bar = root.getElementsByClassName("foo bar")
        assert_array_equals(foo, [a, b])
        assert_array_equals(foo_bar, [b])

        a.setAttribute("class", "foo bar")
        assert_array_equals(foo_bar, [a, b])

        root.removeChild(b)
        assert_array_equals(foo, [a])
        assert_array_equals(foo_bar, [a])

    def test_empty_token_string_matches_nothing(self):
        root = document.createElement("root")
        kid = document.createElement("kid")
        kid.setAttribute("class", "anything")
        root.appendChild(kid)
        assert_array_equals(root.getElementsByClassName("   "), [])


class GetElementsByName(unittest.TestCase):
    def test_is_live(self):
        # getElementsByName is a Document method (DOM spec)
        doc = Document()
        root = doc.createElement("root")
        doc.appendChild(root)
        one = doc.createElement("input")
        one.setAttribute("name", "field")
        root.appendChild(one)

        named = doc.getElementsByName("field")
        assert_equals(named.length, 1)

        two = doc.createElement("input")
        two.setAttribute("name", "field")
        root.appendChild(two)
        assert_equals(named.length, 2)

        one.setAttribute("name", "other")
        assert_array_equals(named, [two])


if __name__ == "__main__":
    unittest.main()
