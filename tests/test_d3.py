"""
    test_d3
    ~~~~~~~~~~~~~~~
    unit tests for domonic.d3

"""

import time
import unittest
# import requests
# from mock import patch
# from domonic.javascript import Math

# from domonic.dom import *
# from domonic.html import *
from domonic.d3 import *

from domonic.svg import *
from domonic.d3.path import Path
from domonic.d3.format import *
from domonic.d3.format import format


class domonicTestCase(unittest.TestCase):

    # domonic.d3.d3
    def test_d3_hello(self):
        doc = html(head(meta(_charset="utf-8")), body())
        d3(doc)
        d3.select("body").append("span").text("Hello, world!")
        print(doc)

    def test_d3_path(self):
        p = Path()
        p.moveTo(1, 2)
        p.lineTo(3, 4)
        p.closePath()
        print(p)

        # context = d3.path()
        # drawCircle(context, 40);
        # mypath = path(_d="", _fill="red", _stroke="blue", **{"_stroke-width": "3"})
        mypath = path(_fill="red", _stroke="blue", **{"_stroke-width": "3"})
        print(mypath)
        mypath.setAttribute("d", str(p))
        print(mypath)

    def test_d3_format(self):

        for i in range(10):
            print(0.1 * i)


        print(format)

        f = format(".1f")


        for i in range(10):
            print(f(0.1 * i))

        # format(".0%")(0.123)  # rounded percentage, "12%"
        # format("($.2f")(-3.5)  # localized fixed-point currency, "(£3.50)"
        # format("+20")(42)  # space-filled and signed, "                 +42"
        # format(".^20")(42)  # dot-filled and centered, ".........42........."
        # format(".2s")(42e6)  # SI-prefix with two significant digits, "42M"
        # format("#x")(48879)  # prefixed lowercase hexadecimal, "0xbeef"
        # format(",.2r")(4223)  # grouped thousands with two significant digits, "4,200"


if __name__ == '__main__':
    unittest.main()
