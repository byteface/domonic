"""Ported from wpt/dom/nodes/Node-childNodes.html
https://dom.spec.whatwg.org/#dom-node-childnodes

The JavaScript-only assertions (``list[Symbol.iterator] === Array.prototype
[Symbol.iterator]`` and friends, and ``forEach``'s ``thisArg`` ``this``
binding) are dropped -- they check that a browser's ``NodeList`` borrows
``Array.prototype`` methods, which has no Python meaning.
"""

import unittest

from domonic.dom import Document, NodeList
from tests.wpt._harness import assert_array_equals, assert_equals, assert_false, assert_true

document = Document()


class NodeChildNodes(unittest.TestCase):
    def test_caching_of_node_childnodes(self):
        element = document.createElement("p")
        assert_equals(element.childNodes, element.childNodes)

    def _check_parent_node(self, node):
        assert_array_equals(node.childNodes, [])

        children = node.childNodes
        child = document.createElement("p")
        node.appendChild(child)
        assert_equals(node.childNodes, children)
        assert_array_equals(children, [child])
        assert_equals(children.item(0), child)

        child2 = document.createComment("comment")
        node.appendChild(child2)
        assert_array_equals(children, [child, child2])
        assert_equals(children.item(0), child)
        assert_equals(children.item(1), child2)

        assert_false(2 in children)
        assert_equals(children[2], None)
        assert_equals(children.item(2), None)

    def test_node_childnodes_on_an_element(self):
        self._check_parent_node(document.createElement("p"))

    def test_node_childnodes_on_a_documentfragment(self):
        self._check_parent_node(document.createDocumentFragment())

    def test_node_childnodes_on_a_document(self):
        self._check_parent_node(Document())

    def test_iterator_behaviour_of_node_childnodes(self):
        node = document.createElement("div")
        kid1 = document.createElement("p")
        kid2 = document.createTextNode("hey")
        kid3 = document.createElement("span")
        node.appendChild(kid1)
        node.appendChild(kid2)
        node.appendChild(kid3)

        lst = node.childNodes
        assert_array_equals(list(lst), [kid1, kid2, kid3])

        keys = list(lst.keys())
        assert_array_equals(keys, [0, 1, 2])

        values = list(lst.values())
        assert_array_equals(values, [kid1, kid2, kid3])

        entries = list(lst.entries())
        assert_equals(len(entries), len(keys))
        assert_equals(len(entries), len(values))
        for i, entry in enumerate(entries):
            assert_array_equals(entry, [keys[i], values[i]])

        seen = []
        lst.forEach(lambda value, key, list_obj: seen.append((value, key, list_obj)))
        assert_equals(len(seen), len(entries))
        for cur, (value, key, list_obj) in enumerate(seen):
            assert_equals(list_obj, lst)
            assert_equals(value, values[cur])
            assert_equals(key, keys[cur])

    def test_node_childnodes_should_be_a_live_collection(self):
        node = document.createElement("ul")
        for text in ("1", "2", "3", "4"):
            li = document.createElement("li")
            li.appendChild(document.createTextNode(text))
            node.appendChild(li)
        children = node.childNodes
        assert_true(isinstance(children, NodeList))
        li = document.createElement("li")
        assert_equals(children.length, 4)

        node.appendChild(li)
        assert_equals(children.length, 5)

        node.removeChild(li)
        assert_equals(children.length, 4)


if __name__ == "__main__":
    unittest.main()
