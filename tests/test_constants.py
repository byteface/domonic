import unittest

from domonic.constants import (
    HTTPStatus,
    doctypes,
    file_extensions,
    http_response_status_codes,
    namespaces,
)
from domonic.constants.color import Color
from domonic.constants.entities import Char, Entity
from domonic.constants.keyboard import KeyCode


class ConstantsTest(unittest.TestCase):
    def test_namespace_constants(self):
        self.assertEqual(namespaces["svg"], "http://www.w3.org/2000/svg")
        self.assertEqual(namespaces["html"], "http://www.w3.org/1999/xhtml")

    def test_doctype_constants(self):
        self.assertEqual(doctypes["HTML5"], "<!DOCTYPE html>")
        self.assertIn("HTML 4.01", doctypes["HTML4_01_Strict"])

    def test_http_status_constants(self):
        self.assertEqual(int(HTTPStatus.OK), 200)
        self.assertEqual(http_response_status_codes[404], "Not Found")
        self.assertEqual(http_response_status_codes[418], "Im A Teapot")

    def test_file_extension_constants(self):
        self.assertEqual(file_extensions["svg"], "image/svg+xml")
        self.assertEqual(file_extensions["json"], "application/json")

    def test_keyboard_modifier_helper(self):
        self.assertTrue(KeyCode.is_modifier(KeyCode.SHIFT))
        self.assertTrue(KeyCode.is_modifier(KeyCode.RIGHT_ALT))
        self.assertFalse(KeyCode.is_modifier(KeyCode.ENTER))

    def test_entity_and_char_rendering(self):
        self.assertEqual(str(Entity("&amp;")), "&")
        self.assertEqual(repr(Entity("&lt;")), "Entity('&lt;')")
        self.assertEqual(str(Char("<tag>")), "&lt;tag&gt;")

    def test_color_helpers(self):
        self.assertEqual(Color.hex2rgb("#ffffff"), (255, 255, 255))
        self.assertEqual(Color.rgb2hex(255, 0, 255), "#ff00ff")
        self.assertEqual(Color(255, 0, 255).toRGBA(), (255, 0, 255, 1))
        self.assertEqual(Color("#00ff00").convert("css"), "#00ff00")


if __name__ == "__main__":
    unittest.main()
