"""
    test_domonic
    ~~~~~~~~~~~~
    domonic core tests for __init__.py at the root of the domonic package

    (previously no tests. was using examples/parsing/page.py to drive dev)

"""

import unittest
from unittest.mock import patch

from domonic.CDN import CDN_CSS, CDN_JS
from domonic import domonic


class TestCase(unittest.TestCase):
    """Tests for the domonic"""

    def test_load(self):
        t1 = domonic.load("<html></html>")
        print("test_load:::", t1, type(t1))

    def test_loads(self):
        # t1 = domonic.loads('<html></html>')
        # print(t1)
        pass

    def parse(self):
        t1 = domonic.parse("<html></html>")
        assert t1 == "html(),"  # hmm wondering if parse is correct term. as returns pyml strings

    def evaluate(self):
        t1 = domonic.evaluate("<html></html>")
        print(t1)

    def test_pyml_validation_does_not_execute_unsafe_calls(self):
        with patch("os.system") as system:
            is_valid, fixed = domonic._is_valid_pyml("__import__('os').system('echo nope')")

        system.assert_not_called()
        self.assertFalse(is_valid)
        self.assertEqual(fixed, "")

    def test_pyml_validation_accepts_safe_markup_fragments(self):
        self.assertEqual(domonic._is_valid_pyml("span("), (True, "span("))
        self.assertEqual(domonic._is_valid_pyml('_class="notice"'), (True, '_class="notice"'))

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

    def test_hacked_expat_parser(self):
        # test the  hacked version of the xpat parser
        print("test!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        # t1 = domonic.parseString('<html></html>')
        # print(t1)
        t1 = domonic.parseString(
            f"""<html><head><link rel="stylesheet" href="{CDN_CSS.MARX}" /><script src="{CDN_JS.JQUERY}"></script><script>
	function add(){{
		$('#results').html( Number($('#a').val()) + Number($('#b').val()) )}};
</script></head><body><article><div><label>Add numbers:</label><input id="a" /><span>+</span><input id="b" /><button id="calculate_button" onclick="add();">Calculate</button><div>Result:<div id="results"></div></div></div></article></body></html>"""
        )
        print("RES:", t1)
        print("RES:", type(t1))
        print("RES:", str(t1))
        print(t1.getElementById("a"))

        # print(t1)
        return
        #         return

        # print( ':FIRE:', type(t1))
        # return
        # print(str(t1))
        # from domonic import render
        # print( render( t1 ) )

        print("test222!")
        t1 = domonic.parseString("<div></div>")
        print(t1)
        print(str(t1))
        # from domonic import render
        # print( render( t1 ) )

    def test_parse_string_with_expat_parser_option(self):
        page = domonic.parseString("<div><span>Hello</span></div>", parser="expat")
        self.assertIsNotNone(page)
        self.assertEqual(page.querySelector("span").text, "Hello")

    def test_parse_string_rejects_unknown_parser(self):
        with self.assertRaises(ValueError):
            domonic.parseString("<div></div>", parser="nope")

    def test_parse_string_with_html5_parser_option(self):
        try:
            page = domonic.parseString("<html><body><p>Hi</p></body></html>", parser="html5_parser")
        except ImportError:
            self.skipTest("html5_parser is not installed")
        else:
            self.assertIsNotNone(page)
            self.assertEqual(page.querySelector("p").text, "Hi")

    def test_parse_string_with_lxml_html_option(self):
        try:
            page = domonic.parseString("<html><body><p>Hi</p></body></html>", parser="lxml_html")
        except ImportError:
            self.skipTest("lxml is not installed")
        else:
            self.assertIsNotNone(page)
            self.assertEqual(page.querySelector("p").text, "Hi")

    def test_default_parser_setter(self):
        previous = domonic.get_default_parser()
        try:
            domonic.set_default_parser("expat")
            self.assertEqual(domonic.get_default_parser(), "expat")
            page = domonic.parseString("<div><span>Hello</span></div>")
            self.assertEqual(page.querySelector("span").text, "Hello")
        finally:
            domonic.set_default_parser(previous)

    def test_parse_string_with_markupever_option(self):
        try:
            page = domonic.parseString("<html><body><p>Hi</p></body></html>", parser="markupever")
        except ImportError:
            self.skipTest("markupever is not installed")
        else:
            self.assertIsNotNone(page)
            self.assertEqual(page.querySelector("p").text, "Hi")

    def test_parse_string_with_selectolax_option(self):
        try:
            page = domonic.parseString("<html><body><p>Hi</p></body></html>", parser="selectolax")
        except ImportError:
            self.skipTest("selectolax is not installed")
        else:
            self.assertIsNotNone(page)
            self.assertEqual(page.querySelector("p").text, "Hi")

    def test_parse_string_with_justhtml_option(self):
        try:
            page = domonic.parseString("<html><body><p>Hi</p></body></html>", parser="justhtml")
        except ImportError:
            self.skipTest("justhtml is not installed")
        else:
            self.assertIsNotNone(page)
            self.assertEqual(page.querySelector("p").text, "Hi")


if __name__ == "__main__":
    unittest.main()
