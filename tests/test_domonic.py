"""
test_domonic
~~~~~~~~~~~~
domonic core tests for __init__.py at the root of the domonic package

(previously no tests. was using examples/parsing/page.py to drive dev)

"""

import tempfile
import sys
import unittest
from importlib import import_module
from unittest.mock import patch

from domonic import attributes, domonic
from domonic.CDN import CDN_CSS, CDN_JS


def _debug_print(*args, **kwargs):
    return None


class TestCase(unittest.TestCase):
    """Tests for the domonic"""

    def test_load(self):
        t1 = domonic.load("<html></html>")
        _debug_print("test_load:::", t1, type(t1))

    def test_loads(self):
        with tempfile.NamedTemporaryFile("w+", suffix=".pyml") as template:
            template.write('div("Hello", _id="loaded")')
            template.flush()

            result = domonic.loads(template.name)

        self.assertEqual(str(result), '<div id="loaded">Hello</div>')
        self.assertEqual(result.getAttribute("id"), "loaded")

    def test_dent_formats_single_line_pyml(self):
        self.assertEqual(domonic.dent("div(span())"), "div(\n    span(\n    )\n)")
        self.assertEqual(domonic.dent("div(span())", use_tabs=True), "div(\n\tspan(\n\t)\n)")

    def test_get_can_return_pyml_or_domonic_object(self):
        class Response:
            text = '<div id="downloaded"></div>'

        fake_requests = type(
            "Requests", (), {"get": staticmethod(lambda url, timeout=30: Response())}
        )
        with patch.dict("sys.modules", {"requests": fake_requests}):
            pyml = domonic.get("https://example.test")
            node = domonic.get("https://example.test", evaluate=True)

        self.assertIn('_id="downloaded"', pyml)
        self.assertEqual(str(node), '<div id="downloaded"></div>')

    def parse(self):
        t1 = domonic.parse("<html></html>")
        assert (
            t1 == "html(),"
        )  # hmm wondering if parse is correct term. as returns pyml strings

    def evaluate(self):
        t1 = domonic.evaluate("<html></html>")
        _debug_print(t1)

    def test_pyml_validation_does_not_execute_unsafe_calls(self):
        with patch("os.system") as system:
            is_valid, fixed = domonic._is_valid_pyml(
                "__import__('os').system('echo nope')"
            )

        system.assert_not_called()
        self.assertFalse(is_valid)
        self.assertEqual(fixed, "")

    def test_domonify_does_not_execute_unsafe_calls(self):
        with patch("os.system") as system:
            with self.assertRaises(ValueError):
                domonic.domonify("__import__('os').system('echo nope')")

        system.assert_not_called()

    def test_domonify_accepts_template_context_names(self):
        node = domonic.domonify(
            'div(label, _id=slug, **{"_data-user-id": user_id})',
            label="Hello",
            slug="greeting",
            user_id="7",
        )

        self.assertEqual(str(node), '<div id="greeting" data-user-id="7">Hello</div>')

    def test_safe_pyml_rejects_attribute_calls(self):
        with self.assertRaises(ValueError):
            domonic._safe_eval_pyml("sys.exit()")

    def test_pyml_validation_accepts_safe_markup_fragments(self):
        self.assertEqual(domonic._is_valid_pyml("span("), (True, "span("))
        self.assertEqual(
            domonic._is_valid_pyml('_class="notice"'), (True, '_class="notice"')
        )

    def test_parse_preserves_basic_attribute_output(self):
        page = domonic.parse('<div id="one" class="two"></div>')
        self.assertEqual(
            page,
            """div(
_id="one", _class="two",
),""",
        )

    def test_parse_preserves_hyphenated_attribute_output(self):
        page = domonic.parse('<div data-user-id="7" aria-label="Open"></div>')
        self.assertEqual(
            page,
            """div(
**{"_data-user-id":"7"},  **{"_aria-label":"Open"},
),""",
        )

    def test_parse_preserves_equals_text_and_solo_attrs(self):
        self.assertEqual(domonic.parse("<p>2=2</p>"), 'p(\n"2=2"\n),')
        self.assertEqual(domonic.parse("<div hidden></div>"), "div(\n_hidden=True,\n),")
        self.assertEqual(
            domonic.parse("<div aria-hidden></div>"),
            'div(\n**{"_aria-hidden":True},\n),',
        )

    def test_parse_empty_and_doctype_only_input(self):
        self.assertEqual(domonic.parse(""), "")
        self.assertEqual(domonic.parse("   "), "")
        self.assertEqual(domonic.parse("\n\n"), "")
        self.assertEqual(domonic.parse("<!doctype html>"), "")

    def test_parse_does_not_mutate_global_attributes(self):
        before = list(attributes)

        domonic.parse("<div></div>")
        domonic.parse("<span></span>")

        self.assertEqual(attributes, before)

    def test_hacked_expat_parser(self):
        # test the  hacked version of the xpat parser
        _debug_print("test!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        # t1 = domonic.parseString('<html></html>')
        # print(t1)
        t1 = domonic.parseString(
            f"""<html><head><link rel="stylesheet" href="{CDN_CSS.MARX}" /><script src="{CDN_JS.JQUERY}"></script><script>
	function add(){{
		$('#results').html( Number($('#a').val()) + Number($('#b').val()) )}};
</script></head><body><article><div><label>Add numbers:</label><input id="a" /><span>+</span><input id="b" /><button id="calculate_button" onclick="add();">Calculate</button><div>Result:<div id="results"></div></div></div></article></body></html>"""
        )
        _debug_print("RES:", t1)
        _debug_print("RES:", type(t1))
        _debug_print("RES:", str(t1))
        _debug_print(t1.getElementById("a"))

        # print(t1)
        return
        #         return

        # print( ':FIRE:', type(t1))
        # return
        # print(str(t1))
        # from domonic import render
        # print( render( t1 ) )

        _debug_print("test222!")
        t1 = domonic.parseString("<div></div>")
        _debug_print(t1)
        _debug_print(str(t1))
        # from domonic import render
        # print( render( t1 ) )

    def test_parse_string_with_expat_parser_option(self):
        page = domonic.parseString("<div><span>Hello</span></div>", parser="expat")
        self.assertIsNotNone(page)
        self.assertEqual(page.querySelector("span").text, "Hello")

    def test_parse_string_with_expat_doctype_entities_and_notations(self):
        page = domonic.parseString(
            '<!DOCTYPE root [<!ELEMENT root (#PCDATA)><!ENTITY writer "Ada">'
            '<!NOTATION png SYSTEM "image/png">]><root>&writer;</root>',
            parser="expat",
        )
        root = page.querySelector("root")

        self.assertIs(page.documentElement, root)
        self.assertEqual(root.text, "Ada")
        self.assertEqual(page.doctype.name, "root")
        self.assertIn('<!ENTITY writer "Ada">', page.doctype.internalSubset)
        self.assertEqual(page.doctype.entities.length, 1)
        self.assertEqual(page.doctype.entities.item(0).nodeName, "writer")
        self.assertEqual(str(page.doctype.entities.item(0)), "Ada")
        self.assertEqual(page.doctype.notations.length, 1)
        self.assertEqual(page.doctype.notations.item(0).nodeName, "png")
        self.assertEqual(page.doctype.notations.item(0).systemId, "image/png")

    def test_parse_string_rejects_unknown_parser(self):
        with self.assertRaises(ValueError):
            domonic.parseString("<div></div>", parser="nope")

    def test_parse_string_with_stdlib_html_parser_basic_elements(self):
        page = domonic.parseString("<p>Hello</p>", parser="html.parser")

        self.assertEqual(page.tagName, "p")
        self.assertEqual(page.text, "Hello")

    def test_parse_string_with_stdlib_html_parser_nested_elements(self):
        page = domonic.parseString(
            "<section><p>Hello <strong>there</strong></p></section>",
            parser="html.parser",
        )

        self.assertEqual(page.querySelector("strong").text, "there")
        self.assertEqual(page.text, "Hello there")

    def test_parse_string_with_stdlib_html_parser_attributes(self):
        page = domonic.parseString(
            '<input id="name" class="field" disabled>',
            parser="html.parser",
        )

        self.assertEqual(page.getAttribute("id"), "name")
        self.assertEqual(page.getAttribute("class"), "field")
        self.assertTrue(page.getAttribute("disabled"))
        self.assertEqual(str(page), '<input id="name" class="field" disabled/>')

    def test_parse_string_with_stdlib_html_parser_self_closing_and_void(self):
        page = domonic.parseString(
            '<div><br><img src="x.png"/><input disabled></div>',
            parser="html.parser",
        )

        self.assertEqual(page.querySelector("img").getAttribute("src"), "x.png")
        self.assertEqual(page.querySelector("input").getAttribute("disabled"), "disabled")
        self.assertIn("<br/>", str(page))

    def test_parse_string_with_stdlib_html_parser_fragments(self):
        page = domonic.parseString("<p>One</p><p>Two</p>", parser="html.parser")

        self.assertEqual(len(page.childNodes), 2)
        self.assertEqual([child.text for child in page.childNodes], ["One", "Two"])

    def test_parse_string_with_stdlib_html_parser_full_document(self):
        page = domonic.parseString(
            "<!doctype html><html><head><title>T</title></head><body><p>Hi</p></body></html>",
            parser="html.parser",
        )

        self.assertEqual(page.tagName, "html")
        self.assertEqual(page.querySelector("title").text, "T")
        self.assertEqual(page.querySelector("p").text, "Hi")

    def test_parse_string_with_stdlib_html_parser_malformed_reasonable_html(self):
        page = domonic.parseString("<div><p>One<p>Two</div>", parser="html.parser")

        self.assertEqual(page.tagName, "div")
        self.assertEqual([node.text for node in page.querySelectorAll("p")], ["One", "Two"])

    def test_parse_string_with_stdlib_html_parser_comments_and_entities(self):
        page = domonic.parseString(
            "<div><!--note--><p>A&nbsp;&amp;&#x21;</p></div>",
            parser="html.parser",
        )

        self.assertIn("<!--note-->", str(page))
        self.assertEqual(page.querySelector("p").text, "A\xa0&!")

    def test_parse_string_with_stdlib_html_parser_aliases(self):
        for parser in ("html.parser", "html_parser", "html-parser"):
            with self.subTest(parser=parser):
                page = domonic.parseString("<p>Hello</p>", parser=parser)
                self.assertEqual(page.text, "Hello")

    def test_stdlib_html_parser_adapter_return_root(self):
        from domonic.ext.html_parser_ import parse

        page = parse("<p>Hello</p>")
        fragment = parse("<p>Hello</p><p>World</p>")

        self.assertEqual(page.tagName, "p")
        self.assertEqual(len(fragment.childNodes), 2)

    def test_parse_string_with_html5_parser_option(self):
        try:
            page = domonic.parseString(
                "<html><body><p>Hi</p></body></html>", parser="html5_parser"
            )
        except ImportError:
            self.skipTest("html5_parser is not installed")
        else:
            self.assertIsNotNone(page)
            self.assertEqual(page.querySelector("p").text, "Hi")

    def test_parse_string_with_lxml_html_option(self):
        try:
            page = domonic.parseString(
                "<html><body><p>Hi</p></body></html>", parser="lxml_html"
            )
        except ImportError:
            self.skipTest("lxml is not installed")
        else:
            self.assertIsNotNone(page)
            self.assertEqual(page.querySelector("p").text, "Hi")

    def test_lxml_html_adapter_does_not_require_html5_parser(self):
        module_name = "domonic.ext.lxml_html_"
        cached_adapter = sys.modules.pop(module_name, None)
        try:
            with patch.dict(sys.modules, {"html5_parser": None}):
                adapter = import_module(module_name)
                page = adapter.parse("<html><body><p>Hi</p></body></html>")
        finally:
            if cached_adapter is not None:
                sys.modules[module_name] = cached_adapter

        self.assertEqual(page.querySelector("p").text, "Hi")

    def test_default_parser_setter(self):
        previous = domonic.get_default_parser()
        try:
            domonic.set_default_parser("expat")
            self.assertEqual(domonic.get_default_parser(), "expat")
            page = domonic.parseString("<div><span>Hello</span></div>")
            self.assertEqual(page.querySelector("span").text, "Hello")
            domonic.set_default_parser("html-parser")
            self.assertEqual(domonic.get_default_parser(), "html_parser")
            page = domonic.parseString("<p>Hello</p>")
            self.assertEqual(page.text, "Hello")
        finally:
            domonic.set_default_parser(previous)

    def test_parse_string_with_markupever_option(self):
        try:
            page = domonic.parseString(
                "<html><body><p>Hi</p></body></html>", parser="markupever"
            )
        except ImportError:
            self.skipTest("markupever is not installed")
        else:
            self.assertIsNotNone(page)
            self.assertEqual(page.querySelector("p").text, "Hi")

    def test_parse_string_with_selectolax_option(self):
        try:
            page = domonic.parseString(
                "<html><body><p>Hi</p></body></html>", parser="selectolax"
            )
        except ImportError:
            self.skipTest("selectolax is not installed")
        else:
            self.assertIsNotNone(page)
            self.assertEqual(page.querySelector("p").text, "Hi")

    def test_parse_string_with_justhtml_option(self):
        try:
            page = domonic.parseString(
                "<html><body><p>Hi</p></body></html>", parser="justhtml"
            )
        except ImportError:
            self.skipTest("justhtml is not installed")
        else:
            self.assertIsNotNone(page)
            self.assertEqual(page.querySelector("p").text, "Hi")


if __name__ == "__main__":
    unittest.main()
