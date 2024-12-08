"""
    test_geom
    ~~~~~~~~~~~~
"""

import unittest
from domonic.constants.color import Color
from domonic.geom.shape import Circle, Line, Rect, Shape
from domonic.geom.vec2 import vec2
from domonic.geom.vec3 import vec3

import unittest

# TODO - make own class instead of piggy backing here
class TestColor(unittest.TestCase):
    def test_color_from_vec3(self):
        from domonic.geom.vec3 import vec3
        c = Color(vec3(255, 0, 0))
        self.assertEqual((c.r, c.g, c.b, c.a), (255, 0, 0, 1))

    def test_color_from_vec4(self):
        from domonic.geom.vec4 import vec4
        c = Color(vec4(255, 0, 0, 0.5))
        self.assertEqual((c.r, c.g, c.b, c.a), (255, 0, 0, 0.5))

    def test_color_from_hex_full(self):
        c = Color("#ff0000")
        self.assertEqual((c.r, c.g, c.b, c.a), (255, 0, 0, 1))

    # def test_color_from_hex_short(self):
    #     c = Color("#f00")
    #     self.assertEqual((c.r, c.g, c.b, c.a), (255, 0, 0, 1))

    # def test_color_from_named_color(self):
    #     c = Color("blue")
    #     self.assertEqual((c.r, c.g, c.b, c.a), (0, 0, 255, 1))

    def test_color_from_rgb(self):
        c = Color(255, 0, 0)
        self.assertEqual((c.r, c.g, c.b, c.a), (255, 0, 0, 1))

    def test_color_from_rgba(self):
        c = Color(255, 0, 0, 0.5)
        self.assertEqual((c.r, c.g, c.b, c.a), (255, 0, 0, 0.5))

    def test_invalid_hex_color(self):
        with self.assertRaises(ValueError):
            Color("#12345")

    def test_invalid_named_color(self):
        with self.assertRaises(ValueError):
            Color("invalid_color_name")

    def test_invalid_numeric_inputs(self):
        with self.assertRaises(ValueError):
            Color(255, 255)  # Missing blue
        with self.assertRaises(ValueError):
            Color(255)       # Missing green and blue

    def test_color_alpha_default(self):
        c = Color(100, 150, 200)
        self.assertEqual(c.a, 1)  # Alpha defaults to 1

    def test_color_alpha_explicit(self):
        c = Color(100, 150, 200, 0.7)
        self.assertEqual(c.a, 0.7)

    # def test_color_repr(self):
    #     c = Color(255, 255, 255)
    #     self.assertEqual(str(c), "Color(255, 255, 255, 1)")

    def test_color_eq(self):
        c1 = Color(255, 255, 255)
        c2 = Color(255, 255, 255)
        c3 = Color(0, 0, 0)
        self.assertEqual(c1, c2)
        self.assertNotEqual(c1, c3)

    def test_hex_to_rgb(self):
        self.assertEqual(Color.hex2rgb("#ff0000"), (255, 0, 0))
        with self.assertRaises(ValueError):
            Color.hex2rgb("#12345")

    # def test_named_colors(self):
    #     named_colors = Color.named_colors()
    #     self.assertIn("red", named_colors)
    #     self.assertEqual(named_colors["red"], (255, 0, 0))
    #     self.assertEqual(named_colors["black"], (0, 0, 0))


class TestCase(unittest.TestCase):

    def test_vec2_operations(self):
        v = vec2(10, 10)
        self.assertEqual(v, v)  # Identity test
        self.assertEqual(v * 2, vec2(20, 20))
        self.assertEqual(v / 2, vec2(5, 5))
        self.assertEqual(v - 2, vec2(8, 8))
        self.assertEqual(v + v, vec2(20, 20))
        self.assertEqual(v * v, vec2(100, 100))
        self.assertEqual(v / v, vec2(1, 1))
        self.assertEqual(v - v, vec2(0, 0))
        self.assertEqual((v[0], v[1]), (10, 10))
        self.assertEqual((v["x"], v["y"]), (10, 10))
        self.assertEqual((v.x, v.y), (10, 10))

    def test_vec3_operations(self):
        v = vec3(10, 10, 10)
        self.assertEqual(v * 2, vec3(20, 20, 20))
        self.assertEqual(v / 2, vec3(5, 5, 5))
        self.assertEqual(v - 2, vec3(8, 8, 8))
        self.assertEqual(v + v, vec3(20, 20, 20))
        self.assertEqual(v * v, vec3(100, 100, 100))
        self.assertEqual(v - v, vec3(0, 0, 0))

    def test_shape_color(self):
        s = Shape(color=Color.red)
        self.assertEqual(s.color, Color.red)

    def test_rect_operations(self):
        r = Rect(0, 0, 10, 10)
        self.assertEqual(r * 10, Rect(0, 0, 100, 100))
        self.assertEqual(r / 10, Rect(0, 0, 1, 1))

        a = Rect(0, 0, 10, 10)
        b = Rect(0, 0, 20, 20)
        c = Rect(0, 0, 30, 30)
        self.assertEqual(a + b + c, Rect(0, 0, 60, 60))

    def test_line_creation(self):
        l = Line(vec2(0, 0), vec2(10, 10))
        self.assertEqual(l.start, vec2(0, 0))
        self.assertEqual(l.end, vec2(10, 10))

    def test_circle_operations(self):
        c = Circle(0, 0, 10)
        self.assertEqual(c.radius, 10)
        self.assertEqual(c * 4, Circle(0, 0, 40))

    def test_color_creation(self):
        c1 = Color("#ff00ff")
        self.assertEqual(str(c1), "#ff00ff")

        c3 = Color(255, 255, 255)
        self.assertEqual(str(c3), "#ffffff")

        c4 = Color(255, 255, 255, 0)
        self.assertEqual((c4.r, c4.g, c4.b, c4.a), (255, 255, 255, 0))


if __name__ == "__main__":
    unittest.main()
