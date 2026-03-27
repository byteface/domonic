import unittest

from domonic.constants import (
    HTTPStatus,
    doctypes,
    file_extensions,
    get_doctype,
    get_mime_type,
    get_namespace,
    get_status_text,
    http_response_status_codes,
    mime_types,
    namespaces,
)
from domonic.constants.color import Color
from domonic.constants.entities import Char, Entity
from domonic.constants.keyboard import Code, Key, KeyCode, KeyLocation, normalize_code, normalize_key


class ConstantsTest(unittest.TestCase):
    def test_namespace_constants(self):
        self.assertEqual(namespaces["svg"], "http://www.w3.org/2000/svg")
        self.assertEqual(namespaces["html"], "http://www.w3.org/1999/xhtml")
        self.assertEqual(get_namespace("svg"), "http://www.w3.org/2000/svg")
        self.assertEqual(get_namespace("missing", "fallback"), "fallback")

    def test_doctype_constants(self):
        self.assertEqual(doctypes["HTML5"], "<!DOCTYPE html>")
        self.assertIn("HTML 4.01", doctypes["HTML4_01_Strict"])
        self.assertEqual(get_doctype("HTML5"), "<!DOCTYPE html>")
        self.assertEqual(get_doctype("missing", "fallback"), "fallback")

    def test_http_status_constants(self):
        self.assertEqual(int(HTTPStatus.OK), 200)
        self.assertEqual(http_response_status_codes[404], "Not Found")
        self.assertEqual(http_response_status_codes[418], "I'm a Teapot")
        self.assertEqual(http_response_status_codes[200], "OK")
        self.assertEqual(get_status_text(200), "OK")
        self.assertEqual(get_status_text(499), "Client Closed Request")
        self.assertEqual(get_status_text(999, "fallback"), "fallback")

    def test_file_extension_constants(self):
        self.assertEqual(file_extensions["svg"], "image/svg+xml")
        self.assertEqual(file_extensions["json"], "application/json")
        self.assertIs(mime_types, file_extensions)
        self.assertEqual(get_mime_type(".svg"), "image/svg+xml")
        self.assertEqual(get_mime_type("JSON"), "application/json")
        self.assertEqual(get_mime_type("missing", "fallback"), "fallback")

    def test_keyboard_modifier_helper(self):
        self.assertTrue(KeyCode.is_modifier(KeyCode.SHIFT))
        self.assertTrue(KeyCode.is_modifier(KeyCode.LEFT_COMMAND))
        self.assertFalse(KeyCode.is_modifier(KeyCode.ENTER))

    def test_modern_keyboard_constants(self):
        self.assertEqual(Key.ENTER, "Enter")
        self.assertEqual(Key.SPACE, " ")
        self.assertEqual(Code.KEY_A, "KeyA")
        self.assertEqual(Code.DIGIT_7, "Digit7")
        self.assertEqual(KeyLocation.STANDARD, 0)
        self.assertEqual(KeyLocation.LEFT, 1)
        self.assertEqual(KeyLocation.RIGHT, 2)
        self.assertEqual(KeyLocation.NUMPAD, 3)
        self.assertEqual(normalize_key("Esc"), "Escape")
        self.assertEqual(normalize_key("A"), "a")
        self.assertEqual(normalize_code("a"), "KeyA")
        self.assertEqual(normalize_code("7"), "Digit7")
        self.assertEqual(KeyCode.to_key("13"), "Enter")
        self.assertEqual(KeyCode.to_code("65"), "KeyA")
        self.assertEqual(KeyCode.from_key("Enter"), 13)

    def test_entity_and_char_rendering(self):
        self.assertEqual(str(Entity("&amp;")), "&")
        self.assertEqual(repr(Entity("&lt;")), "Entity('&lt;')")
        self.assertEqual(str(Char("<tag>")), "&lt;tag&gt;")

    def test_entity_disambiguated_aliases(self):
        self.assertEqual(Char.AGRAVE, "&agrave;")
        self.assertEqual(Char.LATIN_CAPITAL_A_GRAVE, "&Agrave;")
        self.assertEqual(Char.ALPHA, "&alpha;")
        self.assertEqual(Char.GREEK_CAPITAL_ALPHA, "&Alpha;")
        self.assertEqual(Char.DAGGER, "&Dagger;")
        self.assertEqual(Char.SINGLE_DAGGER, "&dagger;")
        self.assertEqual(Char.DOUBLE_DAGGER, "&Dagger;")
        self.assertEqual(Char.PRIME, "&Prime;")
        self.assertEqual(Char.SINGLE_PRIME, "&prime;")
        self.assertEqual(Char.DOUBLE_PRIME, "&Prime;")
        self.assertEqual(Char.TILDE, "&tilde;")
        self.assertEqual(Char.ASCII_TILDE, "&#126;")
        self.assertEqual(Char.YUML, "&Yuml;")
        self.assertEqual(Char.LATIN_SMALL_Y_UMLAUT, "&yuml;")

    def test_color_helpers(self):
        self.assertEqual(Color.hex2rgb("#ffffff"), (255, 255, 255))
        self.assertEqual(Color.rgb2hex(255, 0, 255), "#ff00ff")
        self.assertEqual(Color(255, 0, 255).toRGBA(), (255, 0, 255, 1))
        self.assertEqual(Color("#00ff00").convert("css"), "#00ff00")


if __name__ == "__main__":
    unittest.main()
