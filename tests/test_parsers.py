"""
test_parsers
~~~~~~~~~~~~
"""

import unittest

from domonic.parsers import (
    add_cdata_tags_to_every_node,
    add_xml_declaration_to_document,
    create_element,
    dent,
    remove_cdata_tags_from_every_node,
    remove_doctype,
    remove_extra_whitespace,
    remove_tags,
)


class TestParsers(unittest.TestCase):
    def test_create_element_passes_args_to_html_tags(self):
        self.assertEqual(
            str(create_element("div", "hello", _id="x")), '<div id="x">hello</div>'
        )

    def test_create_element_passes_args_to_sitemap_tags(self):
        self.assertEqual(
            str(create_element("loc", "https://example.com")),
            "<loc>https://example.com</loc>",
        )

    def test_create_element_falls_back_to_custom_html_tags(self):
        self.assertEqual(
            str(create_element("my-widget", "ok", **{"_data-id": "7"})),
            '<my-widget data-id="7">ok</my-widget>',
        )

    def test_string_cleanup_helpers(self):
        self.assertEqual(remove_extra_whitespace("a \n\t  b"), "a b")
        self.assertEqual(remove_doctype("<!doctype html><p>x</p>"), "<p>x</p>")
        self.assertEqual(
            remove_tags("<p>x</p><script>bad()</script>", "js"), "<p>x</p>"
        )
        self.assertEqual(remove_tags("<style>x</style><p>ok</p>", "css"), "<p>ok</p>")
        self.assertEqual(remove_tags("<p>x</p><!--gone-->", "comments"), "<p>x</p>")

    def test_xml_cdata_helpers(self):
        wrapped = add_cdata_tags_to_every_node("<root>x</root>")
        self.assertEqual(wrapped, "<![CDATA[root]]>x<![CDATA[/root]]>")
        self.assertEqual(remove_cdata_tags_from_every_node(wrapped), "<root>x</root>")
        self.assertEqual(
            add_xml_declaration_to_document("<root/>"),
            '<?xml version="1.0" encoding="UTF-8" ?>\n<root/>',
        )

    def test_dent_handles_single_line_pyml(self):
        self.assertEqual(dent("div(span())"), "div(\n    span(\n    )\n)")

    def test_expat_parses_cdata_in_a_real_xhtml_document(self):
        # a <style>/<script> wrapped in CDATA is the standard way real XHTML
        # protects embedded CSS/JS from XML processing. domonic's <html> tag
        # doubles as its own document (the last html() created becomes the
        # active document), so by the time the expat/XML parser reaches this
        # CDATA section, self.document is an HTMLDocument-derived instance --
        # whose createCDATASection() correctly refuses CDATA per the DOM
        # spec's HTML-document rule. That rule doesn't apply to input parsed
        # as XML, so the expat builder must not route through it.
        from domonic import domonic
        from domonic.dom import CDATASection

        xhtml = (
            '<html xmlns="http://www.w3.org/1999/xhtml"><head>'
            '<style type="text/css"><![CDATA[.a{color:red}]]></style>'
            "</head><body><div class=\"a\">x</div></body></html>"
        )
        page = domonic.parseString(xhtml, parser="expat")
        style = page.getElementsByTagName("style")[0]
        cdata = style.childNodes[0]
        self.assertIsInstance(cdata, CDATASection)
        self.assertEqual(cdata.data, ".a{color:red}")
        self.assertIs(cdata.parentNode, style)


if __name__ == "__main__":
    unittest.main()
