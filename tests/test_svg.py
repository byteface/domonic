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
            circle(
                _cx="50",
                _cy="50",
                _r="40",
                _stroke="green",
                **{"_stroke-width": "4"},
                _fill="yellow",
            )
        )
        assert (
            str(mysvg)
            == '<svg><circle cx="50" cy="50" r="40" stroke="green" stroke-width="4" fill="yellow"></circle></svg>'
        )
        mysvg.appendChild(
            circle(
                _cx="50",
                _cy="50",
                _r="40",
                _stroke="green",
                **{"_stroke-width": "4"},
                _fill="yellow",
            )
        )
        assert (
            str(mysvg)
            == '<svg><circle cx="50" cy="50" r="40" stroke="green" stroke-width="4" fill="yellow"></circle><circle cx="50" cy="50" r="40" stroke="green" stroke-width="4" fill="yellow"></circle></svg>'
        )
        # assert mysvg.toxml() == '<?xml version="1.0" encoding="utf-8"?>\n<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="100" height="100" viewBox="0 0 100 100">\n</svg>'

    def test_domonic_cirlce(self):
        test = svg(
            circle(
                _cx="50",
                _cy="50",
                _r="40",
                _stroke="green",
                **{"_stroke-width": "4"},
                _fill="yellow",
            ),
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
            circle(
                _cx="50",
                _cy="50",
                _r="40",
                _stroke="green",
                **{"_stroke-width": "4"},
                _fill="yellow",
            ),
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

        point = drawing.createSVGPoint(10, 20).matrixTransform(
            drawing.createSVGMatrix().translate(5, 7)
        )
        self.assertEqual((point.x, point.y), (15.0, 27.0))

        bbox = dot.getBBox()
        self.assertEqual(
            (bbox.x, bbox.y, bbox.width, bbox.height), (3.0, 4.0, 4.0, 4.0)
        )

        points_box = polyline(_points="0,0 10,4 -2,8").getBBox()
        self.assertEqual(
            (points_box.x, points_box.y, points_box.width, points_box.height),
            (-2.0, 0.0, 12.0, 8.0),
        )

    def test_svg_text_measurement(self):
        label = text("Alice", x=0, y=0)
        box = label.getBBox()
        # ~34px advance for "Alice" at the 16px default, positive height
        self.assertAlmostEqual(box.width, 34.7, delta=1.5)
        self.assertTrue(0 < box.height < 25)
        self.assertLess(box.y, 0)  # baseline at y=0, box starts above it
        self.assertAlmostEqual(label.getComputedTextLength(), box.width, delta=0.1)
        self.assertAlmostEqual(
            label.getSubStringLength(0, 3),
            text("Ali").getComputedTextLength(),
        )
        # bold is wider
        self.assertGreater(
            text("Alice", **{"_font-weight": "bold"}).getComputedTextLength(),
            label.getComputedTextLength(),
        )
        # font-size scales linearly
        self.assertAlmostEqual(
            text("Alice", **{"_font-size": "32"}).getComputedTextLength(),
            2 * label.getComputedTextLength(),
            delta=0.1,
        )

    def test_group_bbox_unions_transformed_children(self):
        grp = g(
            rect(x=10, y=10, width=20, height=20),
            rect(x=100, y=5, width=10, height=10),
        )
        box = grp.getBBox()
        self.assertEqual(
            (box.x, box.y, box.width, box.height), (10.0, 5.0, 100.0, 25.0)
        )

        moved = g(rect(x=0, y=0, width=10, height=10))
        moved.setAttribute("transform", "translate(50, 50)")
        outer = g(moved)
        obox = outer.getBBox()
        self.assertEqual((obox.x, obox.y), (50.0, 50.0))

    def test_ctm_composes_ancestor_transforms(self):
        from domonic.dom import DOMPoint

        leaf = g(text("X", x=0, y=0))
        leaf.setAttribute("transform", "translate(100, 50)")
        scaled = g(leaf)
        scaled.setAttribute("transform", "scale(2)")
        root = svg(scaled)

        ctm = leaf.getScreenCTM()
        self.assertEqual((ctm.a, ctm.d, ctm.e, ctm.f), (2.0, 2.0, 200.0, 100.0))
        p = ctm.transformPoint(DOMPoint(10, 10))
        self.assertEqual((p.x, p.y), (220.0, 120.0))

    def test_createElementNS_and_d3_append_get_svg_api(self):
        from domonic.dom import document
        from domonic.d3.selection import select

        SVG_NS = "http://www.w3.org/2000/svg"
        made = document.createElementNS(SVG_NS, "text")
        self.assertEqual(made.namespaceURI, SVG_NS)
        made.setAttribute("x", "0")
        self.assertTrue(hasattr(made, "getBBox"))
        made.appendChild(document.createTextNode("hi"))
        self.assertGreater(made.getBBox().width, 0)

        appended = select(document.createElement("svg")).append("text").node()
        self.assertTrue(hasattr(appended, "getComputedTextLength"))

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
            self.assertEqual(
                str(globals()[python_name]()), f"<{tag_name}></{tag_name}>"
            )

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
