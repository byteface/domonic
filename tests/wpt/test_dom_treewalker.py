"""Ported from wpt/dom/traversal/TreeWalker-basic.html and
TreeWalker-acceptNode-filter.html.
https://dom.spec.whatwg.org/#interface-treewalker

``createTreeWalker(root, null, null)`` giving ``whatToShow == 0`` is not
ported: domonic cannot tell a missing argument from an explicit ``None`` and
maps ``None`` to ``SHOW_ALL`` (the useful default for a Python caller).
``assert_readonly`` rows are JS property-descriptor checks with no Python
meaning.
"""

import unittest

from domonic.dom import Document, NodeFilter
from tests.wpt._harness import assert_equals, assert_true

document = Document()


def _sample_dom():
    #        #a
    #    +----+----+
    #   "b"        #c
    #          +----+----+
    #         #d        <!--j-->
    #    +----+----+
    #   "e"  #f   "i"
    #     +---+---+
    #    "g"   <!--h-->
    a = document.createElement("div")
    a.id = "a"
    a.appendChild(document.createTextNode("b"))
    c = document.createElement("div")
    c.id = "c"
    a.appendChild(c)
    dd = document.createElement("div")
    dd.id = "d"
    c.appendChild(dd)
    dd.appendChild(document.createTextNode("e"))
    f = document.createElement("span")
    f.id = "f"
    dd.appendChild(f)
    f.appendChild(document.createTextNode("g"))
    f.appendChild(document.createComment("h"))
    dd.appendChild(document.createTextNode("i"))
    c.appendChild(document.createComment("j"))
    return a


def _describe(node):
    if node is None:
        return None
    if getattr(node, "nodeType", None) == 1:
        return ("Element", node.id)
    if getattr(node, "nodeType", None) == 3:
        return ("Text", node.data)
    if getattr(node, "nodeType", None) == 8:
        return ("Comment", node.data)
    return (type(node).__name__, None)


class TreeWalkerConstruction(unittest.TestCase):
    def test_defaults(self):
        root = _sample_dom()
        w = document.createTreeWalker(root)
        assert_equals(w.toString(), "[object TreeWalker]")
        assert_equals(w.root, root)
        assert_equals(w.whatToShow, 0xFFFFFFFF)
        assert_equals(w.filter, None)
        assert_equals(w.currentNode, root)

    def test_whatToShow_is_kept_verbatim(self):
        root = _sample_dom()
        w = document.createTreeWalker(root, 42, None)
        assert_equals(w.whatToShow, 42)
        assert_equals(w.filter, None)

    def test_invalid_root_is_a_type_error(self):
        for bad in (None, object(), 1):
            with self.assertRaises(TypeError):
                document.createTreeWalker(bad)


class TreeWalkerWalk(unittest.TestCase):
    def test_walk_over_nodes(self):
        root = _sample_dom()
        w = document.createTreeWalker(root)
        assert_equals(_describe(w.currentNode), ("Element", "a"))
        assert_equals(w.parentNode(), None)
        assert_equals(_describe(w.firstChild()), ("Text", "b"))
        assert_equals(_describe(w.currentNode), ("Text", "b"))
        assert_equals(_describe(w.nextSibling()), ("Element", "c"))
        assert_equals(_describe(w.lastChild()), ("Comment", "j"))
        assert_equals(_describe(w.previousSibling()), ("Element", "d"))
        assert_equals(_describe(w.nextNode()), ("Text", "e"))
        assert_equals(_describe(w.parentNode()), ("Element", "d"))
        assert_equals(_describe(w.previousNode()), ("Element", "c"))
        assert_equals(w.nextSibling(), None)
        assert_equals(_describe(w.currentNode), ("Element", "c"))

    def test_currentNode_can_be_reassigned(self):
        root = _sample_dom()
        w = document.createTreeWalker(root)
        f = root.lastChild.firstChild.childNodes[1]  # span#f
        w.currentNode = f
        assert_equals(w.currentNode, f)


class TreeWalkerFilter(unittest.TestCase):
    def test_reject_skips_the_whole_subtree(self):
        root = document.createElement("root")
        for name in ("a", "b", "c"):
            el = document.createElement(name)
            el.id = name
            el.appendChild(document.createElement("kid"))
            root.appendChild(el)

        def reject_b(node):
            return NodeFilter.FILTER_REJECT if node.id == "b" else NodeFilter.FILTER_ACCEPT

        w = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT, reject_b)
        seen = []
        node = w.nextNode()
        while node is not None:
            seen.append(node.tagName)
            node = w.nextNode()
        assert_equals(seen, ["a", "kid", "c", "kid"])

    def test_object_filter_with_acceptNode(self):
        root = document.createElement("root")
        for name in ("a", "b"):
            el = document.createElement(name)
            el.appendChild(document.createElement("kid"))
            root.appendChild(el)

        class OnlyKids:
            def acceptNode(self, node):
                return NodeFilter.FILTER_ACCEPT if node.tagName == "kid" else NodeFilter.FILTER_SKIP

        w = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT, OnlyKids())
        seen = []
        node = w.nextNode()
        while node is not None:
            seen.append(node.tagName)
            node = w.nextNode()
        assert_equals(seen, ["kid", "kid"])

    def test_filter_exceptions_propagate(self):
        root = _sample_dom()

        def boom(node):
            raise RuntimeError("from filter")

        w = document.createTreeWalker(root, NodeFilter.SHOW_ALL, boom)
        with self.assertRaises(RuntimeError):
            w.nextNode()


if __name__ == "__main__":
    unittest.main()
