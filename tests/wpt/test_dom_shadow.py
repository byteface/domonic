"""Ported from wpt/shadow-dom/Element-interface-attachShadow.html and
wpt/dom/nodes/getRootNode.html (the shadow-including rows).
https://dom.spec.whatwg.org/#dom-element-attachshadow
"""

import unittest

from domonic.dom import Document, DOMException

document = Document()


class AttachShadow(unittest.TestCase):
    def test_returns_a_shadow_root_and_sets_the_host_link(self):
        host = document.createElement("div")
        root = host.attachShadow({"mode": "open"})
        self.assertIs(host.shadowRoot, root)
        self.assertEqual(root.mode, "open")
        self.assertIs(root.host, host)

    def test_a_second_call_throws_not_supported_error(self):
        host = document.createElement("div")
        host.attachShadow({"mode": "open"})
        with self.assertRaises(DOMException) as ctx:
            host.attachShadow({"mode": "open"})
        self.assertEqual(ctx.exception.name, "NotSupportedError")

    def test_an_invalid_mode_is_a_type_error(self):
        host = document.createElement("div")
        with self.assertRaises(TypeError):
            host.attachShadow({"mode": "sideways"})


class GetRootNodeAcrossShadow(unittest.TestCase):
    def test_default_stops_at_the_shadow_root(self):
        host = document.createElement("div")
        root = host.attachShadow({"mode": "open"})
        inner = document.createElement("p")
        root.appendChild(inner)
        self.assertIs(inner.getRootNode(), root)

    def test_composed_crosses_the_shadow_boundary(self):
        outer = document.createElement("section")
        host = document.createElement("div")
        outer.appendChild(host)
        root = host.attachShadow({"mode": "open"})
        inner = document.createElement("p")
        root.appendChild(inner)
        self.assertIs(inner.getRootNode({"composed": True}), outer)


if __name__ == "__main__":
    unittest.main()
