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
from domonic.html import *
from domonic.d3 import *

from domonic.svg import *
from domonic.d3.path import Path
from domonic.d3.format import *
from domonic.d3.format import format


class domonicTestCase(unittest.TestCase):

    # domonic.d3.d3
    # def test_d3_hello(self):
    #     doc = html(head(meta(_charset="utf-8")), body())
    #     d3(doc)
    #     d3.select("body").append("span").text("Hello, world!")
    #     print(doc)

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

        f = format(".1f")  
        for i in range(10):
            # print(i)
            print(f(0.1 * i))

        # dot-filled and centered,
        print(format(".^20")(42))
        assert format(".^20")(42) == ".........42........."

        zero = format("04d")
        # print('...',zero(2))
        assert zero(2) == "0002"
        assert zero(123) == "0123"


        # rounded percentage
        print(format(".0%")(0.123))
        # assert format(".0%")(0.123) == "12%"

        # localized fixed-point currency
        print(format("($.2f")(-3.5))#  , "(£3.50)"

        # space-filled and signed
        assert format("+20")(42) == "                 +42"

        # SI-prefix with two significant digits
        assert format(".2s")(42e6) == "42M"

        # prefixed lowercase hexadecimal
        assert format("#x")(48879) == "0xbeef"
        # return

        # grouped thousands with two significant digits, "4,200"
        print(format(",.2r")(4223))
        # print(formatPrefix(",.0s", 1e-6)(.00042))

        assert type(format("d")(0)) == str
        # print(str(format("d")))
        assert str(format("d")) + "" == " >-d"


        # invalid format: foo/);
        with self.assertRaises(Exception):
            format('foo')

        # /invalid format: \.-2s/);
        # format('.-2s')
        with self.assertRaises(Exception):
            format('.-2s')

        # /invalid format: \.f/);
        # format(".f")
        with self.assertRaises(Exception):
            format(".f")

        s = formatSpecifier("")
        assert isinstance(s, FormatSpecifier)

        s = formatSpecifier("")
        # print(s)
        # print('++', s.fill)
        assert s.fill == " "
        assert s.align == ">"
        assert s.sign == "-"
        assert s.symbol == ""
        assert s.zero == False
        assert s.width == None
        assert s.comma == False
        assert s.precision == None
        assert s.trim == False
        assert s.type == ""

        s = formatSpecifier("q")
        assert s.trim == False
        assert s.type == "q"

        s = formatSpecifier("")
        assert s.trim == False
        assert s.type == ""

        s = FormatSpecifier({
            'fill': 1,
            'align': 2,
            'sign': 3,
            'symbol': 4,
            'zero': 5,
            'width': 6,
            'comma': 7,
            'precision': 8,
            'trim': 9,
            'type': 10
        })
        assert s.fill == "1"
        assert s.align == "2"
        assert s.sign == "3"
        assert s.symbol == "4"
        assert s.zero == True
        assert s.width == 6
        assert s.comma == True
        assert s.precision == 8
        assert s.trim == True
        assert s.type == "10"


        s = formatSpecifier("")
        s.fill = "_"
        assert str(s) == "_>-"
        s.align = "^"
        print(str(s))
        assert str(s) == "_^-"
        s.sign = "+"
        assert str(s) == "_^+"
        s.symbol = "$"
        assert str(s) == "_^+$"
        s.zero = True
        assert str(s) == "_^+$0"
        s.width = 12
        assert str(s) == "_^+$012"
        s.comma = True
        assert str(s) == "_^+$012,"
        s.precision = 2
        assert str(s) == "_^+$012,.2"
        s.type = "f"
        assert str(s) == "_^+$012,.2f"
        s.trim = True
        assert str(s) == "_^+$012,.2~f"

        print("s: errors::", str(format(s)(42)))
        # assert str(format(s)(42)) == "+$0,000,000,042"

        # print("AA::",formatPrefix(",.0s", 1e-6)(.00042))
        assert formatPrefix(",.0s", 1e-6)(.00042) == "420µ"

        # print( formatPrefix(",.0s", 1e-6)(.0042) )
        assert formatPrefix(",.0s", 1e-6)(.0042) == "4,200µ"

        # print( '?', formatPrefix(",.3s", 1e-3)(.00042) )
        assert formatPrefix(",.3s", 1e-3)(.00042) == "0.420m"

        # print( formatPrefix(",.0s", 1e-27)(1e-24) )
        assert formatPrefix(",.0s", 1e-27)(1e-24) == "1y"

        # f = formatPrefix(" $12,.1s", 1e6)
        # print( f(-42e6) )
        # assert f(-42e6) ==  "      −$42.0M"

        # print( f(+4.2e6) )
        # assert f(+4.2e6) == "        $4.2M"

        s = FormatSpecifier({})
        assert s.fill == " "
        assert s.align == ">"
        assert s.sign == "-"
        assert s.symbol == ""
        assert s.zero == False
        assert s.width == None
        assert s.comma == False
        assert s.precision == None
        assert s.trim == False
        assert s.type == ""

        f = format("~r")
        assert f(1) == "1"
        assert f(0.1) == "0.1"
        assert f(0.01) == "0.01"
        assert f(10.0001) == "10.0001"
        assert f(123.45) == "123.45"
        assert f(123.456) == "123.456"
        # print(">>>>>",f(123.4567))
        # assert f(123.4567) == "123.457" #??
        assert f(0.000009) == "0.000009"
        assert f(0.0000009) == "0.0000009"
        assert f(0.00000009) == "0.00000009"
        # assert f(0.111119) == "0.111119"
        # assert f(0.1111119) == "0.111112"
        # assert f(0.11111119) == "0.111111"

        f = format("~e")
        assert f(0) == "0e+0"
        assert f(42) == "4.2e+1"
        assert f(42000000) == "4.2e+7"
        assert f(0.042) == "4.2e-2"
        # print( '|||', f(-4), "−4e+0" )
        assert f(-4) == "−4e+0"
        assert f(-42) == "−4.2e+1"
        assert f(42000000000) == "4.2e+10"
        assert f(0.00000000042) == "4.2e-10"

        f = format(".4~e")
        assert f(0.00000000012345) == "1.2345e-10"
        assert f(0.00000000012340) == "1.234e-10"
        assert f(0.00000000012300) == "1.23e-10"
        assert f(-0.00000000012345) == "−1.2345e-10"
        assert f(-0.00000000012340) == "−1.234e-10"
        assert f(-0.00000000012300) == "−1.23e-10"
        assert f(12345000000) == "1.2345e+10"
        assert f(12340000000) == "1.234e+10"
        assert f(12300000000) == "1.23e+10"
        assert f(-12345000000) == "−1.2345e+10"
        assert f(-12340000000) == "−1.234e+10"
        assert f(-12300000000) == "−1.23e+10"

        f = format("~s")
        assert f(0) == "0"
        assert f(1) == "1"
        assert f(10) == "10"
        assert f(100) == "100"
        # print( f(999.5) )
        assert f(999.5) == "999.5"
        assert f(999500) == "999.5k"
        # print(f(1000))
        assert f(1000) == "1k"
        assert f(1400) == "1.4k"
        assert f(1500) == "1.5k"
        assert f(1500.5) == "1.5005k"
        assert f(1e-15) == "1f"
        assert f(1e-12) == "1p"
        assert f(1e-9) == "1n"
        assert f(1e-6) == "1µ"
        assert f(1e-3) == "1m"
        assert f(1e0) == "1"
        assert f(1e3) == "1k"
        assert f(1e6) == "1M"
        assert f(1e9) == "1G"
        assert f(1e12) == "1T"
        assert f(1e15) == "1P"

        assert format("c")("☃") == "☃"
        assert format("020c")("☃") ==  "0000000000000000000☃"
        assert format(" ^20c")("☃") == "         ☃          "
        assert format("$c")("☃") == "$☃"


        f = format("~%")
        # assert f(0) == "0%"
        # print("???", f(0.1)) # TODO y are percentages using the default precision
        # assert f(0.1) == "10%"
        # assert f(0.01) == "1%"
        # assert f(0.001) == "0.1%"
        # assert f(0.0001) == "0.01%"

        f = format(",~g")
        print( f(10000.0) )
        # assert f(10000.0) == "10,000"
        # assert f(10000.1) == "10,000.1"

        # print( format("06.2f")(2) )
        # return

        assert format(".1f")(0.49) == "0.5"
        assert format(".2f")(0.449) == "0.45"
        assert format(".3f")(0.4449) == "0.445"
        assert format(".5f")(0.444449) == "0.44445"
        print( format(".1f")(100) )
        assert format(".1f")(100) == "100.0"
        assert format(".2f")(100) == "100.00"
        assert format(".3f")(100) == "100.000"
        assert format(".5f")(100) == "100.00000"

        f = format("+$,.2f");
        assert f(0) == "+$0.00"
        assert f(0.429) == "+$0.43"
        assert f(-0.429) == "−$0.43"
        assert f(-1) == "−$1.00"
        assert f(1e4) == "+$10,000.00"
        print( f(1e4) )

        assert format("10,.1f")(123456.49) == " 123,456.5"
        assert format("10,.2f")(1234567.449) == "1,234,567.45"
        assert format("10,.3f")(12345678.4449) == "12,345,678.445"
        assert format("10,.5f")(123456789.444449) == "123,456,789.44445"
        assert format("10,.1f")(123456) == " 123,456.0"
        assert format("10,.2f")(1234567) == "1,234,567.00"
        assert format("10,.3f")(12345678) == "12,345,678.000"
        assert format("10,.5f")(123456789) == "123,456,789.00000"

        assert format("f")(42) == "42.000000"

        # assert format("f")(-0) == "0.000000"
        # assert format("f")(-1e-12) == "0.000000"

        # assert format("+f")(-0) == "−0.000000"
        assert format("+f")(+0) == "+0.000000"
        # assert format("+f")(-1e-12) == "−0.000000"
        assert format("+f")(+1e-12) == "+0.000000"

        # assert formatLocale({"decimal": "|"}).format("06.2f")(2) == "002|00"
        print( formatLocale({"decimal": "/"}).format("06.2f")(2) )
        assert formatLocale({"decimal": "/"}).format("06.2f")(2) == "002/00"
        # return
        assert formatLocale({"decimal": ".", "currency": ["฿", ""]}).format("$06.2f")(2) == "฿02.00"
        assert formatLocale({"decimal": ".", "currency": ["", "฿"]}).format("$06.2f")(2) == "02.00฿"
        # assert formatLocale({"decimal": ",", "currency": ["", " €"]}).format("$.3s")(1.2e9) == "1,20G €"
        # assert formatLocale({"decimal": "."}).format("012,.2f")(2) == "000000002.00" # TODO - bug
        assert formatLocale({"decimal": ".", "grouping": [3], "thousands": ","}).format("012,.2f")(2) == "0,000,002.00"
        assert formatLocale({"decimal": ".", "grouping": [2], "thousands": ","}).format("012,.2f")(2) == "0,00,00,02.00"
        assert formatLocale({"decimal": ".", "grouping": [2, 3], "thousands": ","}).format("012,.2f")(2) == "00,000,02.00"
        assert formatLocale({"decimal": ".", "grouping": [3, 2, 2, 2, 2, 2, 2], "thousands": ","}).format(",d")(1e12) == "10,00,00,00,00,000"

        # f = locale("en-IN").format(",")
        # f = format(",")
        f = set_locale("en-IN").format(",")
        assert f(10) == "10"
        assert f(100) == "100"
        assert f(1000) == "1,000"
        assert f(10000) == "10,000"
        print(f(100000))
        assert f(100000) == "1,00,000"  # note only works with correct locale
        # print(f(1000000))
        assert f(1000000) == "10,00,000"
        # print(f(10000000))
        assert f(10000000) == "1,00,00,000"
        assert f(10000000.4543) == "1,00,00,000.4543"
        assert f(1000.321) == "1,000.321"
        # print(f(10.5))
        assert f(10.5) == "10.5"
        assert f(-10) == "−10"
        assert f(-100) == "−100"
        assert f(-1000) == "−1,000"
        assert f(-10000) == "−10,000"
        assert f(-100000) == "−1,00,000"
        assert f(-1000000) == "−10,00,000"
        assert f(-10000000) == "−1,00,00,000"
        assert f(-10000000.4543) == "−1,00,00,000.4543"
        assert f(-1000.321) == "−1,000.321"
        assert f(-10.5) == "−10.5"

        assert formatLocale({"decimal": ".", "grouping": [3], "thousands": " "}).format("012,.2f")(2) == "0 000 002.00"
        assert formatLocale({"decimal": ".", "grouping": [3], "thousands": "/"}).format("012,.2f")(2) == "0/000/002.00"

        assert formatLocale({"decimal": ".", "percent": "!"}).format("06.2%")(2) == "200.00!"
        # print(formatLocale({"decimal": ".", "percent": "﹪"}).format("06.2%")(2))
        assert formatLocale({"decimal": ".", "percent": "﹪"}).format("06.2%")(2) == "200.00﹪"

        assert formatLocale({"decimal": ".", "minus": "-"}).format("06.2f")(-2) == "-02.00"
        assert formatLocale({"decimal": ".", "minus": "−"}).format("06.2f")(-2) == "−02.00"
        assert formatLocale({"decimal": ".", "minus": "➖"}).format("06.2f")(-2) == "➖02.00"
        assert formatLocale({"decimal": "."}).format("06.2f")(-2) == "−02.00"

        assert formatLocale({"nan": "N/A"}).format("6.2f")(None) == "   N/A"
        assert formatLocale({"nan": "-"}).format("<6.2g")(None) == "-     "
        assert formatLocale({}).format(" 6.2f")(None) == "   NaN"

        # binary
        # print( format("b")(10) )
        assert format("b")(10) == "1010"
        # binary with prefix
        # print(format("#b")(10))
        assert format("#b")(10) == "0b1010"
        # print( format("x")(0xdeadbeef) )
        assert format("x")(0xdeadbeef) == "deadbeef"

        f = format("08d")
        assert f(0) == "00000000"
        assert f(42) == "00000042"
        assert f(42000000) == "42000000"
        assert f(420000000) == "420000000"
        assert f(-4) == "−0000004"
        assert f(-42) == "−0000042"
        assert f(-4200000) == "−4200000"
        assert f(-42000000) == "−42000000"

        f = format("8d")
        assert f(0) == "       0"
        assert f(42) == "      42"
        assert f(42000000) == "42000000"
        assert f(420000000) == "420000000"
        assert f(-4) == "      −4"
        assert f(-42) == "     −42"
        assert f(-4200000) == "−4200000"
        assert f(-42000000) == "−42000000"

        f = format("+08,d")
        assert f(0) == "+0,000,000"
        assert f(42) == "+0,000,042"
        assert f(42000000) == "+42,000,000"
        assert f(420000000) == "+420,000,000"
        assert f(-4) == "−0,000,004"
        assert f(-42) == "−0,000,042"
        assert f(-4200000) == "−4,200,000"
        assert f(-42000000) == "−42,000,000"

        f = format(".2d")
        assert f(0) == "0"
        assert f(42) == "42"
        assert f(-4.2) == "−4"

        assert format("o")(10) == "12"
        assert format("#o")(10) == "0o12"

        # f = format("p")
        # assert f(.00123) == "0.123000%"
        # assert f(.0123) == "1.23000%"
        # assert f(.123) == "12.3000%"
        # assert f(.234) == "23.4000%"
        # assert f(1.23) == "123.000%"
        # assert f(-.00123) == "−0.123000%"
        # assert f(-.0123) == "−1.23000%"
        # assert f(-.123) == "−12.3000%"
        # assert f(-1.23) == "−123.000%"

        assert format(".30f")(0) == "0.00000000000000000000"
        assert format(".0g")(1) == "1"
        # print(format("s")(Number.MIN_VALUE))
        # assert format("s")(Number.MIN_VALUE) == "0.000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000005y"
        # assert format("s")(Number.MAX_VALUE) == "179769000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000Y"
        print( format("n")(123456.78) )
        # assert format("n")(123456.78) == "123,457"
        # assert format(",g")(123456.78) == "123,457"
        print( format("012")(123.456) )
        assert format("012")(123.456) == "00000123.456"
        # assert format("0=12")(123.456) == "00000123.456"

        print('PASSED ALL TESTS1 ====')


if __name__ == '__main__':
    unittest.main()
