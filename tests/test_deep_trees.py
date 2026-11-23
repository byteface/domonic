"""
test_deep_trees
~~~~~~~~~~~~~~~
Broken pages (unclosed <div> or <font> soups) nest thousands of levels deep.
Tree walks must not hit Python's recursion limit on them.
"""

import sys
import unittest

from domonic.dom import DOMParser, NodeFilter

DEPTH = 3000


class TestDeepTrees(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        assert DEPTH * 2 > sys.getrecursionlimit()
        cls.doc = DOMParser().parseFromString("<div>" * DEPTH + "x<br>y" + "</div>" * DEPTH, "text/html")
        cls.deepest = cls.doc.querySelectorAll("div")[-1]

    def test_clone(self):
        clone = self.doc.body.cloneNode(True)
        divs = clone.querySelectorAll("div")
        self.assertEqual(len(divs), DEPTH)
        self.assertIs(divs[-1].parentNode, divs[-2])
        self.assertTrue(clone.isEqualNode(self.doc.body))

    def test_serialization(self):
        self.assertTrue(self.doc.body.outerHTML.startswith("<body><div><div>"))
        self.assertIn("<div>x<br>y</div>", self.doc.body.innerHTML)

    def test_text(self):
        body = self.doc.body.cloneNode(True)  # a changed tree: walked, not read from the parser's text index
        self.assertEqual(body.textContent, "xy")
        self.assertEqual(self.doc.body.innerText, "x\ny")

    def test_tree_walker(self):
        walker = self.doc.createTreeWalker(self.doc.body, NodeFilter.SHOW_ELEMENT)
        count = 0
        while walker.nextNode():
            count += 1
        self.assertEqual(count, DEPTH + 1)  # the divs and the <br>

    def test_closest_and_contains(self):
        self.assertIs(self.deepest.closest("body"), self.doc.body)
        self.assertTrue(self.doc.body.contains(self.deepest))


if __name__ == "__main__":
    unittest.main()
