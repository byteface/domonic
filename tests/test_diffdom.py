"""
test_diffdom
~~~~~~~~~~~~
- unit tests for domonic.diffdom
"""

import json
import unittest

from domonic.diffdom import DiffDOM, nodeToObj, objToNode
from domonic.dom import Comment, Document, Text
from domonic.html import button, div, h1, p, section, span


class DiffDOMTest(unittest.TestCase):
    def test_diff_and_apply_text_and_added_element(self):
        old = div(h1("Hello"), p("Version one"))
        new = div(h1("Hello"), p("Version two"), button("Save"))

        changes = DiffDOM().diff(old, new)

        self.assertIn(
            {
                "action": "modifyTextElement",
                "route": [1, 0],
                "oldValue": "Version one",
                "newValue": "Version two",
            },
            changes,
        )
        self.assertEqual(changes[-1]["action"], "addElement")
        self.assertEqual(changes[-1]["route"], [2])

        self.assertTrue(DiffDOM().apply(old, changes))
        self.assertEqual(str(old), str(new))

    def test_undo_restores_original_tree(self):
        old = div(p("One", _class="copy"), span("Two"))
        new = div(p("Changed", _id="lead"), button("Save"))
        original = str(old)
        dd = DiffDOM()
        changes = dd.diff(old, new)

        self.assertTrue(dd.apply(old, changes))
        self.assertEqual(str(old), str(new))
        self.assertTrue(dd.undo(old, changes))
        self.assertEqual(str(old), original)

    def test_attribute_actions(self):
        old = div(span("x", _class="old", _title="remove"))
        new = div(span("x", _class="new", _id="added"))

        changes = DiffDOM().diff(old, new)

        self.assertIn(
            {
                "action": "removeAttribute",
                "route": [0],
                "name": "title",
                "oldValue": "remove",
            },
            changes,
        )
        self.assertIn(
            {
                "action": "addAttribute",
                "route": [0],
                "name": "id",
                "value": "added",
            },
            changes,
        )
        self.assertIn(
            {
                "action": "modifyAttribute",
                "route": [0],
                "name": "class",
                "oldValue": "old",
                "newValue": "new",
            },
            changes,
        )

    def test_replace_element(self):
        old = div(p("A"))
        new = div(section("A"))
        changes = DiffDOM().diff(old, new)

        self.assertEqual(changes[0]["action"], "replaceElement")
        self.assertEqual(changes[0]["route"], [0])
        self.assertTrue(DiffDOM().apply(old, changes))
        self.assertEqual(str(old), str(new))

    def test_replace_root_element_mutates_existing_node(self):
        old = div("A", _class="old")
        new = section("B", _id="new")
        changes = DiffDOM().diff(old, new)

        self.assertEqual(changes[0]["action"], "replaceElement")
        self.assertEqual(changes[0]["route"], [])
        self.assertTrue(DiffDOM().apply(old, changes))
        self.assertEqual(str(old), str(new))

    def test_comment_and_text_node_objects(self):
        old = div(Comment("before"), Text("one"))
        new = div(Comment("after"), Text("two"))
        changes = DiffDOM().diff(old, new)

        self.assertEqual(
            changes,
            [
                {
                    "action": "modifyComment",
                    "route": [0],
                    "oldValue": "before",
                    "newValue": "after",
                },
                {
                    "action": "modifyTextElement",
                    "route": [1],
                    "oldValue": "one",
                    "newValue": "two",
                },
            ],
        )
        self.assertTrue(DiffDOM().apply(old, changes))
        self.assertEqual(str(old), str(new))

    def test_json_safe_node_round_trip(self):
        node = div(span("ok", **{"_data-id": "123"}), Comment("kept"))
        payload = nodeToObj(node)
        encoded = json.dumps(payload)

        restored = objToNode(json.loads(encoded))

        self.assertEqual(str(restored), str(node))
        self.assertEqual(restored.childNodes[0].getAttribute("data-id"), "123")

    def test_namespaced_node_round_trip(self):
        math = Document.createElementNS("http://www.w3.org/1998/Math/MathML", "math")
        mi = Document.createElementNS("http://www.w3.org/1998/Math/MathML", "mi")
        mi.appendChild("x")
        math.appendChild(mi)

        restored = objToNode(nodeToObj(math))

        self.assertEqual(str(restored), str(math))
        self.assertEqual(restored.namespaceURI, math.namespaceURI)

    def test_invalid_route_returns_false(self):
        self.assertFalse(
            DiffDOM().apply(
                div(),
                [{"action": "modifyTextElement", "route": [99], "newValue": "x"}],
            )
        )


if __name__ == "__main__":
    unittest.main()
