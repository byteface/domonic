"""
    test_geom
    ~~~~~~~~~~~~
"""

import math
import unittest

import domonic.geom as geom
from domonic.constants.color import Color
from domonic.geom.shape import Circle, Ellipse, Line, Rect, Shape
from domonic.geom.vec2 import vec2
from domonic.geom.vec3 import vec3


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

    def test_color_from_sequences(self):
        c = Color((10, 20, 30))
        self.assertEqual((c.r, c.g, c.b, c.a), (10, 20, 30, 1))

        c = Color([10, 20, 30, 0.25])
        self.assertEqual((c.r, c.g, c.b, c.a), (10, 20, 30, 0.25))

        with self.assertRaises(ValueError):
            Color((10, 20))

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
        self.assertEqual(Color.rgb("#ff0000"), (255, 0, 0))
        self.assertEqual(Color.rgb2hex((255, 0, 255)), "#ff00ff")
        with self.assertRaises(ValueError):
            Color.hex2rgb("#12345")
        with self.assertRaises(ValueError):
            Color.rgb2hex((255, 0))

    # def test_named_colors(self):
    #     named_colors = Color.named_colors()
    #     self.assertIn("red", named_colors)
    #     self.assertEqual(named_colors["red"], (255, 0, 0))
    #     self.assertEqual(named_colors["black"], (0, 0, 0))


class TestCase(unittest.TestCase):

    def test_geom_public_exports(self):
        expected = {
            "Circle",
            "Ellipse",
            "Group",
            "Layer",
            "Line",
            "Oval",
            "Particle",
            "Particle3D",
            "Path",
            "Plane",
            "Plotter",
            "Point",
            "Polygon",
            "Polyline",
            "Quaternion",
            "Rect",
            "Shape",
            "Square",
            "Timeline",
            "matrix",
            "vec2",
            "vec3",
            "vec4",
            "vertex",
        }
        self.assertTrue(expected.issubset(set(geom.__all__)))
        for name in expected:
            self.assertTrue(hasattr(geom, name), name)

        namespace = {}
        exec("from domonic.geom import *", namespace)
        for name in expected:
            self.assertIn(name, namespace)

    def test_shape_instances_do_not_share_default_vertices(self):
        a = Shape()
        b = Shape()

        a.vertices.append(vec2(1, 1))

        self.assertEqual(a.vertices, [vec2(1, 1)])
        self.assertEqual(b.vertices, [])

    def test_shape_constructors_keep_position_and_color(self):
        self.assertEqual(Rect(1, 2, 3, 4, "blue").color, "blue")
        self.assertEqual(Circle(5, 6, 7, "green").center, (5, 6))
        self.assertEqual(Circle(5, 6, 7, "green").color, "green")
        self.assertEqual(Line(vec2(0, 0), vec2(1, 1), "black").color, "black")

        ellipse = Ellipse(1, 2, 3, 4, "orange")
        self.assertEqual(
            (ellipse.x, ellipse.y, ellipse.width, ellipse.height), (1, 2, 3, 4)
        )
        self.assertEqual(ellipse.color, "orange")

    def test_circle_operations_include_radius(self):
        circle = Circle(1, 2, 3, "red")

        self.assertEqual(circle * 2, Circle(2, 4, 6))
        self.assertEqual(circle + Circle(2, 3, 4), Circle(3, 5, 7))
        self.assertEqual(circle - Circle(1, 1, 1), Circle(0, 1, 2))
        self.assertNotEqual(Circle(1, 2, 3), Circle(1, 2, 4))

        circle.center = vec2(8, 9)
        self.assertEqual(circle.center, (8, 9))

    def test_plotter_clear_and_plot(self):
        class Canvas:
            def __init__(self):
                self.cleared = 0
                self.points = []

            def clear(self):
                self.cleared += 1

            def draw_point(self, point):
                self.points.append(point)

        canvas = Canvas()
        plotter = geom.Plotter(canvas)

        self.assertEqual(canvas.cleared, 1)
        self.assertIs(plotter.add_point(vec2(1, 2)), plotter)
        self.assertIs(plotter.plot(), plotter)
        self.assertEqual(canvas.points, [vec2(1, 2)])
        self.assertIs(plotter.clear(), plotter)
        self.assertEqual(plotter.points, [])
        self.assertEqual(canvas.cleared, 2)
        self.assertEqual(geom.Plotter().add_point(vec2(3, 4)).plot(), [vec2(3, 4)])

    def test_layer_shape_helpers(self):
        a = Shape()
        b = Shape()
        c = Shape()
        a.name = "first"

        layer = geom.Layer().add(a).add(b)
        other = geom.Layer().add(b).add(c)

        self.assertTrue(layer.has(a))
        self.assertEqual(layer.get_by_name("first"), a)
        self.assertEqual(layer.get_by_property("color"), [a, b])
        self.assertIs(layer.hide(), layer)
        self.assertFalse(a.visible)
        self.assertFalse(b.visible)
        self.assertIs(layer.show(), layer)
        self.assertTrue(a.visible)
        self.assertTrue(b.visible)
        self.assertIs(layer - other, layer)
        self.assertEqual(list(layer), [a])

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
        self.assertEqual(v // 3, vec3(3, 3, 3))
        self.assertEqual(v - 2, vec3(8, 8, 8))
        self.assertEqual(v + 2, vec3(12, 12, 12))
        self.assertEqual(2 + v, vec3(12, 12, 12))
        self.assertEqual(20 - v, vec3(10, 10, 10))
        self.assertEqual(3 * v, vec3(30, 30, 30))
        self.assertEqual(v // vec3(3, 4, 6), vec3(3, 2, 1))
        self.assertEqual(v + v, vec3(20, 20, 20))
        self.assertEqual(v * v, vec3(100, 100, 100))
        self.assertEqual(v - v, vec3(0, 0, 0))
        self.assertEqual(-vec3(1, -2, 3), vec3(-1, 2, -3))
        self.assertEqual((v[0], v[1], v[2]), (10, 10, 10))
        self.assertEqual((v["x"], v["y"], v["z"]), (10, 10, 10))
        self.assertEqual(tuple(v), (10, 10, 10))
        self.assertEqual(v(), (10, 10, 10))
        self.assertEqual(len(v), 3)

        mutable = vec3(1, 2, 3)
        mutable[0] = 4
        mutable["y"] = 5
        mutable["z"] = 6
        self.assertEqual(mutable, vec3(4, 5, 6))

        mutable += vec3(1, 1, 1)
        self.assertEqual(mutable, vec3(5, 6, 7))
        mutable -= 1
        self.assertEqual(mutable, vec3(4, 5, 6))
        mutable *= 2
        self.assertEqual(mutable, vec3(8, 10, 12))
        mutable /= 2
        self.assertEqual(mutable, vec3(4, 5, 6))

        with self.assertRaises(KeyError):
            v["w"]
        with self.assertRaises(KeyError):
            v["w"] = 1
        with self.assertRaises(ValueError):
            v + object()

    def test_vec3_geometry_helpers(self):
        x_axis = vec3(1, 0, 0)
        y_axis = vec3(0, 1, 0)
        point = vec3(1, 2, 2)

        self.assertEqual(x_axis.dot(y_axis), 0)
        self.assertEqual(x_axis.cross(y_axis), vec3(0, 0, 1))
        self.assertAlmostEqual(x_axis.angleBetween(y_axis), math.pi / 2)
        self.assertEqual(point.squaredLength(), 9)
        self.assertEqual(point.length(), 3)
        self.assertEqual(point.distanceSquared(vec3(1, 2, 5)), 9)
        self.assertEqual(point.squareDistance(vec3(1, 2, 5)), 9)
        self.assertEqual(point.distance(vec3(1, 2, 5)), 3)
        self.assertEqual(point.normalize(), vec3(1 / 3, 2 / 3, 2 / 3))
        self.assertEqual(vec3().normalize(), vec3())
        self.assertTrue(point.intersects(vec3(1, 2, 2)))
        self.assertTrue(point.intersects(vec3(1, 2, 2.001), tolerance=0.01))
        self.assertFalse(point.intersects(vec3(1, 2, 3)))
        self.assertFalse(point.intersects((1, 2, 2)))
        self.assertEqual(point.obj(), {"x": 1, "y": 2, "z": 2})
        self.assertEqual(point.json(), "{'x': 1, 'y': 2, 'z': 2}")
        self.assertEqual(hash(point), hash((1, 2, 2)))

        with self.assertRaises(ValueError):
            vec3().angleBetween(x_axis)

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
