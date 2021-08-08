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

from domonic.dom import *
from domonic.html import *
from domonic.d3 import *

from domonic.svg import *
from domonic.d3.path import Path
from domonic.d3.format import *
from domonic.d3.format import format

from domonic.d3.dispatch import dispatch, Dispatch

# from domonic.d3.polygon import *
# from domonic.d3.timer import *

from domonic.d3.selection import *


class TestCase(unittest.TestCase):

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


    def test_d3_dispatch(self):

        d = dispatch("foo", "bar")
        assert isinstance(d, Dispatch)

        d = dispatch("on")
        assert isinstance(d, Dispatch)

        # throws an error if a specified type name is illegal

        # with self.assertRaises(Exception):
        #     dispatch("__proto__")

        # with self.assertRaises(Exception):
        #     dispatch("hasOwnProperty")

        # with self.assertRaises(Exception):
        #     dispatch("")

        # with self.assertRaises(Exception):
        #     dispatch("foo.bar")

        # with self.assertRaises(Exception):
        #     dispatch("foo bar")

        # with self.assertRaises(Exception):
        #     dispatch("foo\tbar")


        # throws an error if a specified type name is a duplicate"
        with self.assertRaises(Exception):
            dispatch("foo", "foo")

        foo = 0
        bar = 0

        def _foo(*args, **kwargs):
            nonlocal foo
            foo += 1

        def _bar(*args, **kwargs):
            nonlocal bar
            bar += 1

        # d = dispatch("foo", "bar").on("foo", lambda x: eval('foo=foo+1') ).on( "bar", lambda x: eval('bar=bar+1') )
        d = dispatch("foo", "bar").on("foo", _foo).on("bar", _bar)
        d.call("foo")
        assert foo == 1
        assert bar == 0
        d.call("foo")
        d.call("bar")
        assert foo == 2
        assert bar == 1

        d = dispatch("foo")
        assert d.call("foo") == None

        '''
        # scope?
        results = []
        foo = {}
        bar = {}

        def some_func(*args, **kwargs):
            # nonlocal results
            from domonic.javascript import Function
            # results.append({'this': 'this', 'arguments': Function(Array([]).slice).call(args)})
            results.append({'this': foo, 'arguments': args})

        d = dispatch("foo").on("foo", some_func)

        d.call("foo", foo, bar)
        print(results)
        print([{'this':foo, 'arguments':[bar]}])
        assert results == [{'this':foo, 'arguments':[bar]}]
        return

        # d.call("foo", bar, foo, 42, "baz")
        # assert results == [{this: foo, arguments: [bar]}, {this: bar, arguments: [foo, 42, "baz"]}])
        '''
        results = []
        d = dispatch("foo")
        d.on("foo.a", lambda: results.append("A"))
        d.on("foo.b", lambda: results.append("B"))
        d.call("foo")
        d.on("foo.c", lambda: results.append("C"))
        d.on("foo.a", lambda: results.append("A"))  # // move to end
        d.call("foo")
        assert results == ["A", "B", "B", "C", "A"]

        d = dispatch("foo")
        assert d.on("foo", lambda: {}) == d

        # replaces an existing callback, if present
        foo = 0
        bar = 0
        d = dispatch("foo", "bar")

        def _foo():
            nonlocal foo
            foo += 1

        def _bar():
            nonlocal bar
            bar += 1

        d.on("foo", lambda: _foo())
        d.call("foo")
        assert foo == 1
        assert bar == 0
        d.on("foo", lambda: _bar())
        d.call("foo")
        assert foo == 1
        assert bar == 1

        # replacing an existing callback with itself has no effect
        foo = 0

        def FOO():
            nonlocal foo
            foo += 1

        d = dispatch("foo").on("foo", FOO)
        d.call("foo")
        assert foo == 1
        d.on("foo", FOO).on("foo", FOO).on("foo", FOO)
        d.call("foo")
        assert foo == 2


        # is equivalent to dispatch(type).on(type, …)
        d = dispatch("foo")
        foos = 0
        bars = 0
        def _foo():
            nonlocal foos
            foos += 1

        def _bar():
            nonlocal bars
            bars += 1

        assert d.on("foo.", _foo) == d
        assert d.on("foo.") == _foo
        assert d.on("foo") == _foo
        assert d.on("foo.", _bar) == d
        assert d.on("foo.") == _bar
        assert d.on("foo") == _bar
        assert d.call("foo") == None
        assert foos == 0
        assert bars == 1

        # assert d.on(".", None) == d
        # assert d.on("foo") == None
        # assert d.call("foo") == None
        # assert foos == 0
        # assert bars == 1

        #  removes an existing callback, if present
        # foo = 0
        # d = dispatch("foo", "bar")

        # def _foo():
        #     nonlocal foo
        #     foo += 1

        # d.on("foo", _foo)
        # d.call("foo")
        # assert foo == 1
        # d.on("foo", None)
        # d.call("foo")
        # print(foo)
        # assert foo == 1 # TODO - fails


    def test_select(self):

        # document is a global so has to be implicitely imported
        from domonic.dom import document
        print(document)

        # page = html(body())

        # somebody = document.createElement('sometag')
        # print(str(somebody))

        # d3.select("body") 
        page = html(body())
        # print( select("body") )
        # select("body").append("svg")
        # select("body").append("svg").attr("width", 960)
        # select("body").append("svg").attr("width", 960).attr("height", 500).attr("byte", "face")

        select("body").append("svg").attr("width", 960).attr("height", 500)  #.append("g")
        select("svg").append("g")
        # select("body").append("svg")

        # select("body").append("svg")
        # print(select("body").append("svg"))

        print(str(page))

        # d3.select("body")
        #   .append("svg")
        #     .attr("width", 960)
        #     .attr("height", 500)
        #   .append("g")
        #     .attr("transform", "translate(20,20)")
        #   .append("rect")
        #     .attr("width", 920)
        #     .attr("height", 460);


        # 
        # #.append("svg").attr("width", 960).attr("height", 500).append("g").attr("transform", "translate(20,20)").append("rect").attr("width", 920).attr("height", 460)


        page = html(
            head(
                meta(_charset="utf-8"),
                meta(**{"_http-equiv": "X-UA-Compatible"}, _content="IE=edge"),
                title('website.com'),
                meta(_name="description", _content=""),
                meta(_name="viewport", _content="width=device-width, initial-scale=1"),
                meta(_name="robots", _content="all,follow"),
                link(_rel="stylesheet", _href="static/css/bootstrap.min.css"),
                link(_rel="shortcut icon", _href="favicon.png")
            ),
            body(
                div(_class="overlay").html(
                    div(_class="content h-100 d-flex align-items-center").html(
                        div(_class="container text-center text-black").html(
                            p("Welcome to the information age", _class="headings-font-family text-uppercase lead"),
                            h1("We are", span("COMPANY", _class="font-weight-bold d-block"), _class="text-uppercase hero-text text-black"),
                            p("And this is our company website", _class="headings-font-family text-uppercase lead")
                        )
                    )
                ),
                header(_class="header sticky-top").html(
                    nav(_class="navbar navbar-expand-lg bg-white border-bottom py-0").html(
                        div(_class="container").html(
                            h6("website.com"),
                            div(_id="navbarSupportedContent", _class="collapse navbar-collapse").html(
                                ul(_class="navbar-nav ml-auto px-3").html(
                                    li(a("Home", _href="", _class="nav-link text-uppercase link-scroll"), _class="nav-item active"),
                                    li(a("About", _href="#about", _class="nav-link text-uppercase link-scroll"), _class="nav-item"),
                                    li(a("Services", _href="#services", _class="nav-link text-uppercase link-scroll"), _class="nav-item"),
                                    li(a("Team", _href="#team", _class="nav-link text-uppercase link-scroll"), _class="nav-item"),
                                    li(a("Contact", _href="#contact", _class="nav-link text-uppercase link-scroll"), _class="nav-item"),
                                )
                            )
                        )
                    )
                ),
                section(_id="about", _class="about").html(
                    div(_class="container").html(
                        div(_class="row mb-5").html(
                            div(_class="col-lg-12").html(
                                header(_style="padding-top:20px;").html(
                                    h6("About us", _class="lined text-uppercase"),
                                ),
                                p("Specialists in xxxxx.", _class="lead"),
                                p("COMPANY can provide xxxxxx solutions. We have expertise in the following areas."),
                                div(_class="row").html(
                                    div(_class="col-lg-6").html(
                                        ul(_class="mb-0").html(
                                            li("A"),
                                            li("B"),
                                            li("C"),
                                        )
                                    ),
                                    div(_class="col-lg-6").html(
                                        ul(_class="mb-0").html(
                                            li("1"),
                                            li("2"),
                                            li("3"),
                                        )
                                    )
                                )
                            )
                        )
                    )
                ),
                div(_class="row text-white text-center", _style="background: url(static/img/header.jpg); padding:20px;").html(
                    div(_class="col-lg-12").html(
                        h5(_class="text-uppercase font-weight-bold").html(
                            i(_class="far fa-image mr-2", ), "Headline."),
                        p("Lorem ipsum."),
                    ),
                    div(_class="col-lg-12").html(
                        h5(_class="text-uppercase font-weight-bold").html(
                            i(_class="far fa-image mr-2", ), "Headline."),
                        p("Lorem ipsum."),
                    ),

                ),
                section(_id="services", _class="bg-gray").html(
                    div(_class="container").html(
                        header(_class="text-center mb-5").html(
                            #  h2("Services", _class="lined text-uppercase"),
                        ),
                        div(_class="row text-center").html(
                            div(_class="col-lg-4").html(
                                div(_class="bg-white mb-4 p-4").html(
                                    h3(i(_class="fas fa-desktop"), _class="icon mb-3"),
                                    h4("Headline", _class="text-uppercase font-weight-bold"),
                                    p("Lorem ipsum.", _class="small text-gray"),
                                )
                            ),
                            div(_class="col-lg-4").html(
                                div(_class="bg-white mb-4 p-4").html(
                                    h3(i(_class="fas fa-desktop"), _class="icon mb-3"),
                                    h4("Headline", _class="text-uppercase font-weight-bold"),
                                    p("Lorem ipsum.", _class="small text-gray"),
                                )
                            ),
                            div(_class="col-lg-4").html(
                                div(_class="bg-white mb-4 p-4").html(
                                    h3(i(_class="fas fa-desktop"), _class="icon mb-3"),
                                    h4("Headline", _class="text-uppercase font-weight-bold"),
                                    p("Lorem ipsum.", _class="small text-gray"),
                                )
                            ),
                        )
                    ),
                    section(_id="team").html(
                        div(_class="container").html(
                            header(_class="text-center mb-5").html(
                                # h2("Our team", _class="text-uppercase lined"),
                            ),
                            div(_class="row text-center").html(
                                # div(_class="col-lg-3 col-md-6 mb-4").html(
                                div(_class="col-lg-12").html(
                                    img(_src="static/img/gol.gif", _alt="Username", _class="img-fluid mb-4", _width="300px;", _height="300px;"),
                                    h4(_class="font-weight-bold text-uppercase").html(
                                        a("Username", _href="#", _class="no-anchor-style")
                                    ),
                                    p("Director", _class="small text-gray text-uppercase"),
                                ),
                            )
                        )
                    ),
                    section(_id="contact").html(
                        div(_class="container").html(
                            header(_class="text-center mb-5").html(
                                #  h2("Contact", _class="text-uppercase lined"),
                            ),
                            div(_class="row").html(
                                div(_class="col-lg-12 text-center").html(
                                    p(
                                        "Email : ",
                                        a("user@website.com", _href="mailto:user@website.com"),
                                        br(),
                                        "or Call us on : ",
                                        a("123456789", _href="tel:123456789")
                                    ),
                                    ul(_class="mb-0 list-inline text-center").html(
                                        li(a(i(_class="fab fa-twitter"), _href="https://twitter.com/user", _class="social-link social-link-twitter"), _class="list-inline-item"),
                                        li(a(i(_class="fab fa-linkedin"), _rel="nofollow", _href="https://www.linkedin.com/in/user/", _class="social-link social-link-instagram"), _class="list-inline-item"),
                                        li(a(i(_class="fas fa-envelope"), _href="mailto:user@website.com", _class="social-link social-link-email"), _class="list-inline-item")
                                    )
                                )
                            )
                        )
                    ),
                    footer(_style="padding:20px;").html(
                        div(_class="row text-center").html(
                            div(_class="col-lg-12 text-center").html(
                                p("Copyright &copy; 2021 COMPANY. All rights Reserved.", _class="mb-0 text-gray"),
                            )
                        )
                    ),
                    script(_src="static/js/jquery.min.js"),
                    link(_rel="stylesheet", _href="https://use.fontawesome.com/releases/v5.7.1/css/all.css", _integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr", _crossorigin="anonymous")
                )
            )
        )

        # selectAll("p").attr("class", "graf").style("color", "red")
        # selectAll("p").attr("class", "test")
        selectAll("p").append("div")
        print(page)

        # select("body").append("svg").attr("width", 960).attr("height", 500).append("g").attr("transform", "translate(20,20)").append("rect").attr("width", 920).attr("height", 460)



if __name__ == '__main__':
    unittest.main()
