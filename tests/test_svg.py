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
from domonic.decorators import silence


class TestCase(unittest.TestCase):

    @silence
    def test_domonic_svg(self):
        mysvg = svg()
        print(mysvg)

    def test_domonic_cirlce(self):
        test = svg(
            circle(_cx="50", _cy="50", _r="40", _stroke="green", **{"_stroke-width":"4"}, _fill="yellow"),
            _width="100", _height="100",
        )
        print(test)

    def test_domonic_node(self):
        circ = svg(
            circle(_cx="50", _cy="50", _r="40", _stroke="green", **{"_stroke-width": "4"}, _fill="yellow"),
            _width="100", _height="100",
        )
        mysvg = svg()
        mysvg.appendChild(circ / 10)
        print(mysvg)


if __name__ == '__main__':
    unittest.main()
