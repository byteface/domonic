"""
test_inner_text
~~~~~~~~~~~~~~~

innerText / outerText (https://html.spec.whatwg.org/#the-innertext-idl-attribute).
The getter's spec cases are the WPT port in tests/wpt/test_html_inner_text.py;
these cover domonic's own surface.
"""

import copy
import pickle
import unittest

from domonic.dom import DOMException, DOMParser
from domonic.html import b, body, div, html, p, pre, span, style


def parse(markup):
    return DOMParser().parseFromString(markup, "text/html")


class TestInnerText(unittest.TestCase):
    def test_a_page(self):
        page = parse(
            "<body><h1>Title</h1><p>One   two</p><script>x()</script>"
            "<ul><li>a</li> <li>b</li></ul><table><tr><td>1</td><td>2</td></tr></table></body>"
        )
        self.assertEqual(page.body.innerText, "Title\n\nOne two\n\na\nb\n1\t2")

    def test_author_css(self):
        page = parse(
            "<style>.ad{display:none} .loud{text-transform:uppercase}</style><p>hi<span class=ad>BUY</span> <b class=loud>you</b>"
        )
        self.assertEqual(page.body.innerText, "hi YOU")

    def test_trees_built_in_python(self):
        page = html(body(div("one", span(" two "), p("three"), style("p{}"))))
        self.assertEqual(page.querySelector("div").innerText, "one two\n\nthree")

    def test_a_hidden_element_gives_its_text_content(self):
        self.assertEqual(div("a  b", _hidden="").innerText, "a  b")

    def test_inherits_white_space_from_its_ancestors(self):
        page = html(body(pre("  x  ", b("  y  "))))
        self.assertEqual(page.querySelector("b").innerText, "  y  ")

    def test_still_callable(self):
        box = div("hi")
        self.assertEqual(box.innerText(), "hi")  # the old method form
        box.innerText("new")
        self.assertEqual(str(box), "<div>new</div>")

    def test_copies_are_plain_text(self):
        text = div("hi").innerText
        self.assertIs(type(copy.deepcopy(text)), str)
        self.assertIs(type(pickle.loads(pickle.dumps(text))), str)

    def test_setter(self):
        box = div(span("old"))
        box.innerText = "a\nb"
        self.assertEqual(str(box), "<div>a<br/>b</div>")
        box.innerText = None
        self.assertEqual(str(box), "<div></div>")

    def test_outer_text(self):
        box = div(p("one"), span("two"))
        self.assertEqual(box.firstChild.outerText, "one")
        box.firstChild.outerText = "x\ny"
        self.assertEqual(str(box), "<div>x<br/>y<span>two</span></div>")
        with self.assertRaises(DOMException) as caught:
            div().outerText = "z"
        self.assertEqual(caught.exception.name, "NoModificationAllowedError")


if __name__ == "__main__":
    unittest.main()
