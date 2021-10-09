"""
    test_svg
    ~~~~~~~~~~~~
    - unit tests for svg
"""

import unittest
# import requests
# from mock import patch

from domonic import domonic

from domonic.svg import *
# from domonic.decorators import silence


class TestCase(unittest.TestCase):

    # @silence
    def test_domonic_svg(self):
        mysvg = svg()
        assert str(mysvg) == '<svg></svg>'
        mysvg.appendChild(circle(_cx="50", _cy="50", _r="40", _stroke="green", **{"_stroke-width": "4"}, _fill="yellow"))
        assert str(mysvg) == '<svg><circle cx="50" cy="50" r="40" stroke="green" stroke-width="4" fill="yellow"></circle></svg>'
        mysvg.appendChild(circle(_cx="50", _cy="50", _r="40", _stroke="green", **{"_stroke-width": "4"}, _fill="yellow"))
        assert str(mysvg) == '<svg><circle cx="50" cy="50" r="40" stroke="green" stroke-width="4" fill="yellow"></circle><circle cx="50" cy="50" r="40" stroke="green" stroke-width="4" fill="yellow"></circle></svg>'
        # assert mysvg.toxml() == '<?xml version="1.0" encoding="utf-8"?>\n<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="100" height="100" viewBox="0 0 100 100">\n</svg>'

    def test_domonic_cirlce(self):
        test = svg(
            circle(_cx="50", _cy="50", _r="40", _stroke="green", **{"_stroke-width": "4"}, _fill="yellow"),
            _width="100", _height="100",
        )
        # print(test)
        assert str(test) == '<svg width="100" height="100"><circle cx="50" cy="50" r="40" stroke="green" stroke-width="4" fill="yellow"></circle></svg>'

    def test_domonic_node(self):
        circ = svg(
            circle(_cx="50", _cy="50", _r="40", _stroke="green", **{"_stroke-width": "4"}, _fill="yellow"),
            _width="100", _height="100",
        )
        mysvg = svg()
        mysvg.appendChild(circ / 10)
        # print(mysvg)

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


if __name__ == '__main__':
    unittest.main()
