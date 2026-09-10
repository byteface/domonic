"""Ported from wpt/domparsing/innerhtml-01.html, innerhtml-05.html,
outerhtml-01.html and the HTML fragment-serialisation checks in
wpt/html/syntax/serializing-html-fragments/.
https://html.spec.whatwg.org/multipage/parsing.html#serialising-html-fragments

domonic's ``innerHTML`` / ``outerHTML`` follow the WHATWG fragment serialiser
and are byte-compatible with a browser (unlike ``str(node)``, which is
XHTML-flavoured). These tests pin that.
"""

import unittest

from domonic.dom import Document

document = Document()


class InnerHTMLGetter(unittest.TestCase):
    def test_void_elements_have_no_slash_and_no_end_tag(self):
        div = document.createElement("div")
        div.innerHTML = "<br><img src=x><hr>"
        self.assertEqual(div.innerHTML, '<br><img src="x"><hr>')

    def test_attributes_are_double_quoted(self):
        div = document.createElement("div")
        div.innerHTML = "<p class=a id=b>t</p>"
        self.assertEqual(div.innerHTML, '<p class="a" id="b">t</p>')

    def test_text_escapes_amp_lt_gt_only(self):
        p = document.createElement("p")
        p.textContent = 'a < b & c > d "e"'
        self.assertEqual(p.innerHTML, 'a &lt; b &amp; c &gt; d "e"')

    def test_attribute_value_escapes_amp_and_quote(self):
        a = document.createElement("a")
        a.setAttribute("title", 'x " & y')
        self.assertEqual(a.outerHTML, '<a title="x &quot; &amp; y"></a>')

    def test_entities_round_trip(self):
        div = document.createElement("div")
        div.innerHTML = '<p title="a &amp; b">x &lt; y</p>'
        self.assertEqual(div.innerHTML, '<p title="a &amp; b">x &lt; y</p>')


class InnerHTMLSetter(unittest.TestCase):
    def test_setting_empty_string_removes_all_children(self):
        div = document.createElement("div")
        div.innerHTML = "<p>a</p><p>b</p>"
        div.innerHTML = ""
        self.assertEqual(list(div.childNodes), [])
        self.assertEqual(div.innerHTML, "")

    def test_setting_replaces_all_existing_children(self):
        div = document.createElement("div")
        div.appendChild(document.createElement("old"))
        div.innerHTML = "<new></new>"
        self.assertEqual([c.tagName for c in div.children], ["NEW"])

    def test_parsed_html_element_tagnames_are_upper_cased(self):
        div = document.createElement("div")
        div.innerHTML = "<section><p>x</p></section>"
        self.assertEqual(div.firstChild.tagName, "SECTION")
        self.assertEqual(div.firstChild.firstChild.tagName, "P")


class OuterHTML(unittest.TestCase):
    def test_getter_includes_the_element_itself(self):
        div = document.createElement("div")
        div.setAttribute("id", "wrap")
        div.innerHTML = "<span>x</span>"
        self.assertEqual(div.outerHTML, '<div id="wrap"><span>x</span></div>')

    def test_setter_replaces_the_element_in_its_parent(self):
        parent = document.createElement("parent")
        document.appendChild(parent)
        child = document.createElement("child")
        parent.appendChild(child)
        child.outerHTML = "<a></a><b></b>"
        self.assertEqual([c.tagName for c in parent.children], ["A", "B"])


if __name__ == "__main__":
    unittest.main()
