"""
    test_geom
    ~~~~~~~~~~~~
"""

import unittest
# import requests
# from mock import patch

from domonic import domonic
from domonic.geom import *
from domonic.constants.color import Color


class TestCase(unittest.TestCase):

    # @silence
    def test_vec2(self):
        v = vec2(10, 10)
        assert v == v
        print(v * 2)
        print(v / 2)
        print(v - 2)
        print(v + v)
        print(v * v)
        print(v / v)
        print(v - v)
        print(v[0], v[1])
        print(v['x'], v['y'])
        print(v.x, v.y)

    # @silence
    def test_vec3(self):
        v = vec3(10, 10, 10)
        print(v * 2)
        print(v / 2)
        print(v - 2)
        print(v + v)
        print(v * v)
        # print(v / v)
        print(v - v)

    # @silence
    # def test_vec4(self):
    #     v = vec4(10, 10, 10)
    #     print(v)

    # @silence
    def test_shape(self):
        s = Shape(Color.red)
        print(s.color)

    # @silence
    def test_rect(self):
        r = Rect(0, 0, 10, 10)
        print(r)
        print(r*10)
        print(r/10)

        a = Rect(0, 0, 10, 10)
        b = Rect(0, 0, 20, 20)
        c = Rect(0, 0, 30, 30)
        print( a+b+c )

    # @silence
    def test_line(self):
        l = Line(vec2(0, 0), vec2(10, 10))
        print(l)

    # @silence
    def test_circle(self):
        c = Circle(0, 0, 10)
        print(c)
        print(c*4)

    # @silence
    # def test_plotter(self):
        # p = Plotter()
        # print(p)

    # @silence
    def test_color(self):

        from domonic.constants.color import Color

        c1 = Color('#ff00ff')
        print(c1)
        # c2 = Color('red')
        # print(c2)
        c3 = Color(255, 255, 255)
        print(c3)
        c4 = Color(255, 255, 255, 0)
        print(c4)


if __name__ == '__main__':
    unittest.main()
