"""
    test_svg
    ~~~~~~~~~~~~
    - unit tests for svg
"""

import unittest

from domonic import domonic
from domonic.svg import *


class TestCase(unittest.TestCase):

    # @silence
    def test_domonic_svg(self):
        mysvg = svg()
        assert str(mysvg) == "<svg></svg>"
        mysvg.appendChild(
            circle(_cx="50", _cy="50", _r="40", _stroke="green", **{"_stroke-width": "4"}, _fill="yellow")
        )
        assert (
            str(mysvg)
            == '<svg><circle cx="50" cy="50" r="40" stroke="green" stroke-width="4" fill="yellow"></circle></svg>'
        )
        mysvg.appendChild(
            circle(_cx="50", _cy="50", _r="40", _stroke="green", **{"_stroke-width": "4"}, _fill="yellow")
        )
        assert (
            str(mysvg)
            == '<svg><circle cx="50" cy="50" r="40" stroke="green" stroke-width="4" fill="yellow"></circle><circle cx="50" cy="50" r="40" stroke="green" stroke-width="4" fill="yellow"></circle></svg>'
        )
        # assert mysvg.toxml() == '<?xml version="1.0" encoding="utf-8"?>\n<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="100" height="100" viewBox="0 0 100 100">\n</svg>'

    def test_domonic_cirlce(self):
        test = svg(
            circle(_cx="50", _cy="50", _r="40", _stroke="green", **{"_stroke-width": "4"}, _fill="yellow"),
            _width="100",
            _height="100",
        )
        # print(test)
        assert (
            str(test)
            == '<svg width="100" height="100"><circle cx="50" cy="50" r="40" stroke="green" stroke-width="4" fill="yellow"></circle></svg>'
        )

    def test_domonic_node(self):
        circ = svg(
            circle(_cx="50", _cy="50", _r="40", _stroke="green", **{"_stroke-width": "4"}, _fill="yellow"),
            _width="100",
            _height="100",
        )
        mysvg = svg()
        mysvg.appendChild(circ / 10)
        # print(mysvg)

    def test_svg_namespace_and_factory(self):
        drawing = create_element("svg", _viewBox="0 0 10 10")
        grad = create_element("linearGradient")
        custom = create_element("my-custom-svg")

        self.assertEqual(drawing.namespaceURI, "http://www.w3.org/2000/svg")
        self.assertEqual(grad.namespaceURI, "http://www.w3.org/2000/svg")
        self.assertEqual(str(drawing), '<svg viewBox="0 0 10 10"></svg>')
        self.assertEqual(str(custom), "<my-custom-svg></my-custom-svg>")

    def test_svg2_exports_and_namespace_conflicts(self):
        from domonic import a as html_a
        from domonic import style as html_style

        drawing = svg(
            a("home", _href="#home"),
            style("circle { fill: red; }"),
            set(_attributeName="opacity", _to="1"),
        )

        self.assertEqual(a().namespaceURI, "http://www.w3.org/2000/svg")
        self.assertEqual(audio().namespaceURI, "http://www.w3.org/2000/svg")
        self.assertEqual(html_a().namespaceURI, "http://www.w3.org/1999/xhtml")
        self.assertEqual(html_style().namespaceURI, "http://www.w3.org/1999/xhtml")
        self.assertIn("<set attributeName", str(drawing))
        self.assertEqual(str(create_element("font_face")), "<font-face></font-face>")
        self.assertEqual(str(color_profile()), "<color-profile></color-profile>")

    def test_svg_geometry_helpers(self):
        dot = circle(_cx="5", _cy="6", _r="2")
        drawing = svg(g(dot), _width="10", _height="10")

        self.assertIs(dot.ownerSVGElement, drawing)
        self.assertIs(dot.viewportElement, drawing)
        self.assertTrue(drawing.getScreenCTM().isIdentity)

        point = drawing.createSVGPoint(10, 20).matrixTransform(drawing.createSVGMatrix().translate(5, 7))
        self.assertEqual((point.x, point.y), (15.0, 27.0))

        bbox = dot.getBBox()
        self.assertEqual((bbox.x, bbox.y, bbox.width, bbox.height), (3.0, 4.0, 4.0, 4.0))

        points_box = polyline(_points="0,0 10,4 -2,8").getBBox()
        self.assertEqual((points_box.x, points_box.y, points_box.width, points_box.height), (-2.0, 0.0, 12.0, 8.0))

    def test_svg_legacy_and_filter_exports(self):
        icon = svg(
            defs(filter(feGaussianBlur(_in="SourceGraphic", _stdDeviation="2"))),
            metadata("info"),
            missing_glyph(),
        )

        self.assertIn("<filter>", str(icon))
        self.assertIn("<metadata>info</metadata>", str(icon))
        self.assertIn("<missing-glyph></missing-glyph>", str(icon))

    def test_svg_tag_exports_real_constructors(self):
        for tag_name in svg_tags:
            python_name = tag_name.replace("-", "_")
            self.assertIn(python_name, globals())
            self.assertEqual(str(globals()[python_name]()), f"<{tag_name}></{tag_name}>")

    # def test_hyphen_elements(self):
    #     test = svg(
    #         missing_glyph(),
    #     )
    #     print(test)

    # def test_font(self):
    #     test = svg(
    #         font_face(),
    #     )
    #     print(test)


if __name__ == "__main__":
    unittest.main()
