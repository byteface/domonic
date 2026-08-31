"""
test_domonic
~~~~~~~~~~~~
- unit tests for domonic
"""

import unittest

from domonic.CDN import CDN_JS
from domonic.dom import Document, MATHML_NAMESPACE, MathMLElement
from domonic.xml.mathml import *


def _debug_print(*args, **kwargs):
    return None


class TestCase(unittest.TestCase):
    def test_mathml(self):
        somemath = math_(
            maction("x"),
            menclose("x"),
            merror("x"),
            mfenced("x"),
            mfrac("x"),
            mi("x"),
            mmultiscripts("x"),
            mn("x"),
            mo("x"),
            mover("x"),
            mpadded("x"),
            mphantom("x"),
            mroot("x"),
            mrow("x"),
            ms("x"),
            mspace("x"),
            msqrt("x"),
            mstyle("x"),
            msub("x"),
            msubsup("x"),
            msup("x"),
            mtable("x"),
            mtd("x"),
            mtext("x"),
            mtr("x"),
            munder("x"),
            munderover("x"),
            semantics("x"),
            maligngroup("x"),
            malignmark("x"),
            msline("x"),
            msgroup("x"),
            mlongdiv("x"),
            mstyle("x"),
            mprescripts("x"),
            mscarries("x"),
            mscarry("x"),
            munder("x"),
            munderover("x"),
            none("x"),
        )

        rendered = str(somemath)
        self.assertIn("<math>", rendered)
        self.assertIn("<mfrac>x</mfrac>", rendered)
        self.assertIn("<msup>x</msup>", rendered)

    def test_mathml_elements_use_mathml_dom_interface(self):
        root = math_(mrow(mi("x"), mo("="), mn("1")), **{"_data-equation": "linear"})
        row = root.firstChild

        self.assertIsInstance(root, MathMLElement)
        self.assertIsInstance(row, MathMLElement)
        self.assertEqual(root.namespaceURI, MATHML_NAMESPACE)
        self.assertEqual(row.namespaceURI, MATHML_NAMESPACE)
        self.assertEqual(root.dataset["equation"], "linear")

        root.style = "color: red;"
        self.assertIs(root.attributeStyleMap, root.style)

        root.nonce = "abc123"
        self.assertEqual(root.getAttribute("nonce"), "abc123")
        self.assertEqual(root.nonce, "abc123")
        root.nonce = None
        self.assertIsNone(root.nonce)

        self.assertTrue(root.focus())
        self.assertTrue(root.blur())

    def test_create_element_ns_returns_mathml_interface(self):
        node = Document.createElementNS(MATHML_NAMESPACE, "math:msqrt")

        self.assertIsInstance(node, MathMLElement)
        self.assertEqual(node.tagName, "msqrt")
        self.assertEqual(node.namespaceURI, MATHML_NAMESPACE)

    def test_mathml_example_with_shim(self):
        from examples.mathml import build_page

        rendered = str(build_page())

        self.assertIn(CDN_JS.MATHML, rendered)
        self.assertIn('<script id="MathJax-script" defer', rendered)
        self.assertIn('xmlns="http://www.w3.org/1998/Math/MathML"', rendered)
        self.assertIn("<mfrac>", rendered)
        self.assertIn("<msqrt>", rendered)


if __name__ == "__main__":
    unittest.main()
