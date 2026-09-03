"""
test_javascript
~~~~~~~~~~~~~~~
unit tests for domonic.javascript
"""

import math
import re
import time
import unittest
import asyncio
from types import SimpleNamespace
from unittest.mock import Mock, patch

from domonic.javascript import *
from domonic.javascript import (
    URL,
    Array,
    Date,
    Global,
    Math,
    Object,
    String,
    Window,
    globalThis,
    performance,
)

# import requests
# from mock import patch


class TestCase(unittest.TestCase):

    @staticmethod
    def _py_cbrt(value):
        if hasattr(math, "cbrt"):
            return math.cbrt(value)
        if value == 0:
            return 0.0
        return math.copysign(abs(value) ** (1 / 3), value)

    # domonic.javascript.Math

    def test_object(self):

        o = Object()

        myObj = Object()
        string = "myString"
        rand = Math.random()
        obj1 = Object()
        myObj.type = "Dot syntax"
        myObj["date created"] = "String with space"
        myObj[string] = "String value"
        myObj[rand] = "Random Number"
        myObj[obj1] = "Object"
        myObj[""] = "Even an empty string"

        assert myObj.type == "Dot syntax"
        assert myObj["date created"] == "String with space"
        assert myObj[string] == "String value"
        assert myObj[rand] == "Random Number"
        assert myObj[obj1] == "Object"
        assert myObj[""] == "Even an empty string"

        assert o is not myObj

        myCar = Object()
        propertyName = "make"
        myCar[propertyName] = "Ford"
        assert myCar[propertyName] == "Ford"
        propertyName = "model"
        myCar[propertyName] = "Mustang"
        assert myCar[propertyName] == "Mustang"

        def showProps(obj, objName):
            result = ""
            for i in obj:
                if obj.hasOwnProperty(i):
                    result += objName + "." + str(i) + "= " + str(obj[i]) + "\n"
            return result

        showProps(myCar, "myCar")
        # print(showProps(myCar, "myCar"))

        obj = {"a": 1}
        copy = Object.assign({}, obj)
        assert copy == {"a": 1}

        # print(Object().fromEntries())
        arr = [["0", "a"], ["1", "b"], ["2", "c"]]
        obj = Object.fromEntries(arr)
        assert obj == {"0": "a", "1": "b", "2": "c"}

        obj = {"foo": "bar", "baz": 42}
        assert Object.entries(obj) == [["foo", "bar"], ["baz", 42]]

        # array like object
        obj = {"0": "a", "1": "b", "2": "c"}
        assert Object.entries(obj) == [["0", "a"], ["1", "b"], ["2", "c"]]

        # def listAllProperties(o):
        #     result = []
        #     objectToInspect = o
        #     while objectToInspect != None:
        #         print(objectToInspect)
        #         objectToInspect = Object.getPrototypeOf(objectToInspect)
        #         result = Array(result).concat(Object.getOwnPropertyNames(objectToInspect))

        #     return result
        # print(listAllProperties(myCar))

        # array like object with random key ordering
        # anObj = {'100': 'a', '2': 'b', '7': 'c'}
        # print(anObj)
        # print(Object.entries(anObj))
        # assert Object.entries(anObj) == [['2', 'b'], ['7', 'c'], ['100', 'a']]

        # returns an empty array for any primitive type
        assert Object.entries(100) == []
        assert Object.keys(100) == []
        assert Object.values(100) == []

        class ExampleObject:
            def __init__(self):
                self.alpha = 1
                self.beta = 2
                self._private = 3

        example = ExampleObject()
        self.assertEqual(Object.entries(example), [["alpha", 1], ["beta", 2]])
        self.assertEqual(Object.keys(example), ["alpha", "beta"])
        self.assertEqual(Object.values(example), [1, 2])

        # iterate through key-value gracefully
        obj = {"a": 5, "b": 7, "c": 9}
        for key, value in Object.entries(obj):
            self.assertEqual(obj[key], value)

        configured = Object({"name": "Jane"})
        Object.defineProperty(configured.__dict__, "role", "admin")
        Object.defineProperties(
            configured,
            {
                "level": {"value": 7},
                "active": True,
            },
        )
        self.assertEqual(configured.level, 7)
        self.assertTrue(configured.active)
        self.assertEqual(Object.getOwnPropertyDescriptor(configured, "name"), "Jane")
        self.assertIn("name", list(Object.getOwnPropertyNames(configured)))
        self.assertTrue("name" in Object.getOwnPropertySymbols(configured))
        self.assertTrue(configured.hasOwnProperty("name"))
        self.assertFalse(configured.hasOwnProperty("missing"))
        created = Object.create(configured, {"created": {"value": "yes"}})
        self.assertEqual(created.name, "Jane")
        self.assertEqual(created.created, "yes")
        self.assertEqual(Object.getPrototypeOf(created), Object)
        getter_holder = Object()
        getter_holder.__defineGetter__("greet", lambda: "hi")
        getter_holder.__defineSetter__("target", lambda value: value)
        self.assertIsNotNone(getter_holder.__lookupGetter__("greet"))
        self.assertIsNotNone(getter_holder.__lookupSetter__("target"))
        self.assertEqual(getter_holder.toLocaleString(), getter_holder.toString())

        def sample_function(value):
            return value + 1

        source = Function(sample_function).toString()
        self.assertIn("sample_function", source)
        self.assertIn("return value + 1", source)
        self.assertEqual(Function(len).toString(), "function len() { [native code] }")
        self.assertEqual(Global.require("math").sqrt(9), 3)
        self.assertIs(getter_holder.valueOf(), getter_holder)
        self.assertIs(Object.freeze(getter_holder), getter_holder)
        self.assertTrue(getattr(getter_holder, "_Object__isFrozen"))
        self.assertTrue(Object.isFrozen(getter_holder))
        self.assertTrue(Object.isSealed(getter_holder))
        self.assertFalse(Object.isExtensible(getter_holder))
        with self.assertRaises(TypeError):
            getter_holder.new_prop = 1
        with self.assertRaises(TypeError):
            getter_holder.greet = "hello"
        with self.assertRaises(TypeError):
            del getter_holder.greet

        extensible = Object({"name": "Jane"})
        self.assertTrue(Object.isExtensible(extensible))
        self.assertIs(Object.preventExtensions(extensible), extensible)
        self.assertFalse(Object.isExtensible(extensible))
        self.assertFalse(Object.isFrozen(extensible))
        extensible.name = "Janet"
        self.assertEqual(extensible.name, "Janet")
        with self.assertRaises(TypeError):
            extensible.age = 30

        sealed = Object({"name": "Ada"})
        self.assertIs(Object.seal(sealed), sealed)
        self.assertTrue(Object.isSealed(sealed))
        self.assertFalse(Object.isFrozen(sealed))
        sealed.name = "Grace"
        self.assertEqual(sealed.name, "Grace")
        with self.assertRaises(TypeError):
            sealed.extra = True
        with self.assertRaises(TypeError):
            del sealed.name

        # class Car(Object):
        #     def __init__(self, make, model, year):
        #         super().__init__()
        #         self.make = make
        #         self.model = model
        #         self.year = year
        #         # super().__init__()

        # mycar = Car('Eagle', 'Talon TSi', 1993)
        # print(mycar)
        # print(mycar.make)
        # print(mycar.__attribs__)

    # Animal properties and method encapsulation

    Animal = {
        "type": "Invertebrates",  # Default value of properties
        "displayType": lambda self: self.type,
    }
    animal1 = Object.create(Animal)
    animal1.displayType(animal1)

    fish = Object.create(Animal)
    fish.type = "Fishes"
    fish.displayType(animal1)

    def test_domonic_abs(self):
        # python -m unittest tests.test_javascript.TestCase.test_domonic_abs

        self.assertEqual(Math.abs("-1"), 1)
        self.assertEqual(Math.abs(-2), 2)
        self.assertEqual(Math.abs(None), 0)
        self.assertEqual(Math.abs(""), 0)
        self.assertEqual(Math.abs([]), 0)
        self.assertEqual(Math.abs([2]), 2)
        self.assertEqual(Math.abs([1, 2]), None)
        self.assertEqual(Math.abs({}), None)
        self.assertEqual(Math.abs("string"), None)
        self.assertEqual(Math.abs(), None)

        self.assertEqual(100, Math.abs(-100.0))

    def test_domonic_LN2(self):
        self.assertEqual(Math.LN2, math.log(2))

    def test_domonic_LOG2E(self):
        self.assertEqual(Math.LOG2E, math.log2(math.e))

    def test_domonic_LOG10E(self):
        self.assertEqual(Math.LOG10E, math.log10(math.e))

    def test_domonic_PI(self):
        self.assertEqual(Math.PI, math.pi)

    def test_domonic_SQRT1_2(self):
        self.assertEqual(Math.SQRT1_2, math.sqrt(0.5))

    def test_domonic_SQRT2(self):
        self.assertEqual(Math.SQRT2, math.sqrt(2))

    def test_domonic_math_matches_python_for_core_operations(self):
        cases = [
            ("ceil", -100.2, math.ceil(-100.2)),
            ("floor", -100.8, math.floor(-100.8)),
            ("round", -100.2, round(-100.2)),
            ("trunc", -100.8, math.trunc(-100.8)),
            ("sin", -1.2, math.sin(-1.2)),
            ("cos", -1.2, math.cos(-1.2)),
            ("tan", -1.2, math.tan(-1.2)),
            ("sqrt", 100, math.sqrt(100)),
            ("log2", 8, math.log2(8)),
            ("log10", 1000, math.log10(1000)),
            ("log1p", 4, math.log1p(4)),
            ("loglp", 4, math.log1p(4)),
        ]
        for name, value, expected in cases:
            with self.subTest(name=name, value=value):
                self.assertEqual(getattr(Math, name)(value), expected)
        self.assertEqual(Math.hypot(3, 4), 5)

    def test_domonic_acos(self):
        self.assertEqual(Math.acos(0.5), math.acos(0.5))

    def test_domonic_acosh(self):
        self.assertEqual(Math.acosh(100), math.acosh(100))

    def test_domonic_asin(self):
        self.assertEqual(Math.asin(0.5), math.asin(0.5))

    def test_domonic_asinh(self):
        self.assertEqual(Math.asinh(-100), math.asinh(-100))

    def test_domonic_atan(self):
        self.assertEqual(Math.atan(-100), math.atan(-100))

    def test_domonic_atan2(self):
        self.assertEqual(Math.atan2(-100, 100), math.atan2(-100, 100))

    def test_domonic_atanh(self):
        self.assertEqual(Math.atanh(0.5), math.atanh(0.5))

    def test_domonic_cbrt(self):
        self.assertEqual(Math.cbrt(100), self._py_cbrt(100))

    def test_domonic_ceil(self):
        self.assertEqual(Math.ceil(-100), math.ceil(-100))

    def test_domonic_cos(self):
        self.assertEqual(Math.cos(-100), math.cos(-100))

    def test_domonic_cosh(self):
        self.assertEqual(Math.cosh(-100), math.cosh(-100))

    def test_domonic_E(self):
        self.assertEqual(2.718281828459045, Math.E)

    def test_domonic_exp(self):
        self.assertEqual(Math.exp(-100), math.exp(-100))

    def test_domonic_floor(self):
        self.assertEqual(Math.floor(-100), math.floor(-100))

    def test_domonic_LN10(self):
        self.assertEqual(2.302585092994046, Math.LN10)

    def test_domonic_log(self):
        self.assertEqual(Math.log(100, 10), math.log(100, 10))

    def test_domonic_max(self):
        self.assertEqual(Math.max(-100, 100), 100)

    def test_domonic_min(self):
        self.assertEqual(Math.min(-100, 100), -100)

    def test_domonic_random(self):
        value = Math.random()
        self.assertGreaterEqual(value, 0)
        self.assertLess(value, 1)

    def test_domonic_round(self):
        self.assertEqual(Math.round(-100), round(-100))

    def test_domonic_pow(self):
        self.assertEqual(Math.pow(100, 10), math.pow(100, 10))

    def test_domonic_sin(self):
        self.assertEqual(Math.sin(-100), math.sin(-100))

    def test_domonic_sinh(self):
        self.assertEqual(Math.sinh(-100), math.sinh(-100))

    def test_domonic_sqrt(self):
        self.assertEqual(Math.sqrt(100), math.sqrt(100))

    def test_domonic_tan(self):
        self.assertEqual(Math.tan(-100), math.tan(-100))

    def test_domonic_tanh(self):
        # print("test_domonic_tanh:::")
        # print(Math.tanh(-100))
        assert Math.tanh(0) == 0
        assert Math.tanh(1) == 0.7615941559557649
        assert Math.tanh(2) == 0.9640275800758169
        assert Math.tanh(3) == 0.9950547536867305

    def test_domonic_trunc(self):
        self.assertEqual(Math.trunc(-100), math.trunc(-100))

    # def test_domonic_math_test(self):
    #   print("test_domonic_math_test:::")
    #   print( Math.abs(-100)*Math.random()*10 )

    # domonic.javascript.Global

    def test_domonic_isNaN(self):
        self.assertEqual(True, Global.isNaN("yo"))
        self.assertEqual(False, Global.isNaN(1))

    def test_domonic_Number(self):
        self.assertEqual(1, Global.Number(1))
        self.assertEqual("NaN", Global.Number("test"))
        self.assertEqual(2, Global.Number("1") + Global.Number("1.0"))

    def test_domonic_global_boolean_and_isfinite(self):
        self.assertTrue(Global.isFinite("12.5"))
        self.assertTrue(Global.isFinite(3))
        self.assertFalse(Global.isFinite("abc"))
        self.assertFalse(Global.isFinite(float("inf")))

        self.assertFalse(Global.Boolean(""))
        self.assertFalse(Global.Boolean(0))
        self.assertFalse(Global.Boolean(None))
        self.assertTrue(Global.Boolean("false"))
        self.assertTrue(Global.Boolean([]))

    def test_domonic_global_number_and_parser_edge_cases(self):
        self.assertEqual(Global.Number(""), 0)
        self.assertEqual(Global.Number("   "), 0)
        self.assertEqual(Global.Number(True), 1)
        self.assertEqual(Global.Number(False), 0)
        self.assertEqual(Global.Number(None), "NaN")
        self.assertEqual(Global.Number("0x10"), 16)
        self.assertEqual(Global.Number("-1.5e2"), -150.0)
        self.assertEqual(Global.Number("1_000"), "NaN")

        self.assertTrue(Global.isFinite(""))
        self.assertFalse(Global.isFinite(None))
        self.assertFalse(Global.isNaN("12.5"))
        self.assertFalse(Global.isNaN(""))
        self.assertTrue(Global.isNaN(None))
        self.assertTrue(Global.isNaN("nope"))

        self.assertEqual(Global.parseFloat("  -12.5px"), -12.5)
        self.assertEqual(Global.parseFloat(".5rem"), 0.5)
        self.assertEqual(Global.parseFloat("1e3ms"), 1000.0)
        self.assertEqual(Global.parseFloat("0x10"), 0.0)
        self.assertEqual(Global.parseFloat("nope"), "NaN")
        self.assertEqual(Global.parseInt("  -12px"), -12)
        self.assertEqual(Global.parseInt("0x10"), 16)
        self.assertEqual(Global.parseInt("10", 2), 2)
        self.assertEqual(Global.parseInt("0x10", 10), 0)
        self.assertEqual(Global.parseInt("ff", 16), 255)
        self.assertEqual(Global.parseInt("nope"), "NaN")

    def test_domonic_global_this_alias(self):
        self.assertIs(globalThis, Global)
        self.assertIs(Global.globalThis, Global)
        self.assertIs(Global.self, Global)
        self.assertIs(Global.window, Window)
        self.assertIs(globalThis.performance, performance)

    def test_domonic_window_console_log(self):
        # window = Window()
        # Window().console.log("test this")
        # window.console.log("test this")

        # c = Console()
        # c.log()
        # Console.log('test')
        self.assertTrue(True)

    def test_domonic_window_alert(self):
        with patch("builtins.print") as print_mock:
            Window().alert("test this 2")
        print_mock.assert_called_once_with("test this 2")

    def test_domonic_window_prompt(self):
        with patch("builtins.print") as print_mock, patch(
            "builtins.input", return_value="typed"
        ):
            self.assertEqual(Window.prompt("say something"), "typed")
        print_mock.assert_called_once_with("say something")

    def test_window_base64_animation_and_performance(self):
        encoded = Window.btoa("hello")
        self.assertEqual(Window.atob(encoded), "hello")

        observed = []
        Window.requestAnimationFrame(lambda ts: observed.append(ts))
        self.assertEqual(len(observed), 1)
        self.assertIsInstance(observed[0], float)

        performance = Performance()
        mark = performance.mark("start")
        measure = performance.measure("total", "start")
        self.assertEqual(mark.name, "start")
        self.assertEqual(measure.name, "total")
        self.assertTrue(performance.getEntries())
        self.assertEqual(performance.getEntriesByType("mark")[0].name, "start")
        self.assertEqual(performance.getEntriesByName("total")[0].name, "total")
        performance.clearMarks("start")
        self.assertEqual(performance.getEntriesByType("mark"), [])
        performance.mark("again")
        performance.clearMarks()
        self.assertEqual(performance.getEntriesByType("mark"), [])
        performance.measure("named")
        self.assertEqual(
            performance.getEntriesByName("named", "measure")[0].name, "named"
        )
        performance.clearMeasures("named")
        self.assertEqual(performance.getEntriesByName("named"), [])
        performance.clearMeasures()
        self.assertEqual(performance.getEntriesByType("measure"), [])

    def test_domonic_window_document_baseURI(self):
        # Window().alert("test this 2")
        # window = Window()
        # window.alert("test this 2")
        # print(window.document.baseURI)
        # window.document.baseURI = "eventual.technology"
        # print("=",window.document.baseURI)

        self.assertTrue(True)

    """
    def test_domonic_window_location(self):
        # Window().alert("test this 2")
        window = Window()
        # window.alert("test this 2")
        print("window.location")
        print(window.location)
        window.location = "eventual.technology"
        print("window.location.uri")
        print(window.location)
        print(str(window.location))
        print(window.location.href)
    """

    def test_domonic_global_encodeURIComponent(self):

        msg = "Test encoding this string! 123 aweseome"
        enc_msg = Global.encodeURIComponent(msg)
        self.assertEqual(Global.decodeURIComponent(enc_msg), msg)
        self.assertIn("%20", enc_msg)

        # Window().alert("test this 2")
        # window = Window()
        # window.alert("test this 2")
        # print(window.document.baseURI)
        # window.document.baseURI = "eventual.technology"
        # print("=",window.document.baseURI)
        self.assertNotEqual(enc_msg, msg)

    def test_domonic_global_uri_helpers(self):
        uri = "https://example.com/a path/?q=one&two=three#frag"
        encoded_uri = Global.encodeURI(uri)
        self.assertIn("%20", encoded_uri)
        self.assertIn("?", encoded_uri)
        self.assertEqual(Global.decodeURI(encoded_uri), uri)
        self.assertEqual(
            Global.decodeURI(
                "https://example.com/a%20path%3Fq%3Done%26two%3Dthree%23frag%2Ftail"
            ),
            "https://example.com/a path%3Fq%3Done%26two%3Dthree%23frag%2Ftail",
        )
        self.assertEqual(Global.decodeURI("%E2%9C%93%3F"), "✓%3F")

        component = "a path/with?symbols&more"
        encoded_component = Global.encodeURIComponent(component)
        self.assertIn("%2F", encoded_component)
        self.assertIn("%3F", encoded_component)
        self.assertEqual(Global.decodeURIComponent(encoded_component), component)
        self.assertEqual(
            Global.decodeURIComponent("a%2Fb%3Fq%3D1%26x%3D2"),
            "a/b?q=1&x=2",
        )

        self.assertEqual(Global.parseFloat("12.5"), 12.5)
        self.assertEqual(Global.parseInt("12"), 12)

    def test_javascript_url(self):
        url = URL("https://somesite.com/blog/article-one#some-hash")
        # print('TESTS:')
        # print(url)
        assert url.href == "https://somesite.com/blog/article-one#some-hash"
        assert url.protocol == "https"
        assert url.host == "somesite.com"
        assert url.hostname == "somesite.com"
        assert url.port is None
        assert url.pathname == "/blog/article-one"
        assert url.hash == "#some-hash"
        assert url.toString() == "https://somesite.com/blog/article-one#some-hash"
        # print(url.protocol)
        url.protocol = "http"
        # print(url.protocol)
        assert url.protocol == "http"
        assert url.href == "http://somesite.com/blog/article-one#some-hash"

        url.host = "test.com"
        assert url.href == "http://test.com/blog/article-one#some-hash"
        assert url.host == "test.com"
        assert url.hostname == "test.com"
        url.port = 8983
        assert url.href == "http://test.com:8983/blog/article-one#some-hash"
        assert url.port == 8983
        # print(url.toString())

    def test_javascript_url_setter_edge_cases(self):
        url = URL("https://somesite.com/blog/article-one?x=1#some-hash")

        url.protocol = "http:"
        self.assertEqual(url.href, "http://somesite.com/blog/article-one?x=1#some-hash")

        url.pathname = "next"
        self.assertEqual(url.href, "http://somesite.com/next?x=1#some-hash")

        url.hash = "updated"
        self.assertEqual(url.href, "http://somesite.com/next?x=1#updated")
        self.assertEqual(url.hash, "#updated")

        url.hash = ""
        self.assertEqual(url.href, "http://somesite.com/next?x=1")

    # def test_javascript_window(self):
    # print('asdf')
    # print(window)
    # print(window.location)

    # window.location = "https://google.com"
    # print(window.location.href)
    # pass

    def test_javascript_array(self):
        myarr = Array("1", "2", 3, {"4": "four"}, 5, [6])
        assert isinstance(myarr, Array)
        assert myarr.length == 6
        assert myarr.includes("1")
        assert myarr.includes(3)
        assert not myarr.includes(10)
        assert myarr.indexOf(10) == -1
        assert myarr.indexOf("1") == 0
        assert myarr.indexOf([6]) == 5
        assert myarr[1] == "2"
        assert len(myarr) == 6
        assert myarr == Array("1", "2", 3, {"4": "four"}, 5, [6])
        assert myarr.join("---") == "1---2---3---[object Object]---5---6"
        assert Array(1, None, 3).join() == "1,,3"
        # print(myarr.lastIndexOf("1"))
        assert myarr.lastIndexOf("1") == 0
        assert myarr.lastIndexOf(3) == 2
        assert myarr.reverse() == [[6], 5, {"4": "four"}, 3, "2", "1"]
        myarr = Array([[6], 5, {"4": "four"}, 3, "2", "1"])
        assert myarr.slice(0, 1) == [[6]]
        assert myarr == Array([[6], 5, {"4": "four"}, 3, "2", "1"])
        assert myarr.splice(1) == [5, {"4": "four"}, 3, "2", "1"]
        assert myarr[0][0] == 6
        # tests equality. Array == list
        assert myarr == [[6]]
        # casting back to list
        myarr = list(myarr)
        assert myarr == [[6]]
        # test casting
        myarr = ["1", "a", "b", "c"]
        assert Array(myarr).splice(1, 1) == ["a"]
        assert myarr == ["1", "b", "c"]
        myarr = Array(["1", "a", "b", "c"])
        assert myarr.pop() == "c"
        assert myarr == ["1", "a", "b"]
        myarr.push(7)
        assert myarr == ["1", "a", "b", 7]
        assert myarr.unshift("z") == 5
        assert myarr == ["z", "1", "a", "b", 7]
        assert myarr.shift() == "z"
        assert myarr == ["1", "a", "b", 7]
        assert myarr.concat() == ["1", "a", "b", 7]
        # assert myarr.concat(['a', 'b', 'c']) == ["1", "a", "b", 7, "a", "b", "c"]
        assert myarr.concat(["a", "b", "c"], ["d", "e", "f"]) == [
            "1",
            "a",
            "b",
            7,
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
        ]
        # make array do both python and javascript methods.
        myarr = Array("1", "2", 3, {"4": "four"}, 5, [6])
        myarr.append("test")
        myarr = Array([2, 3, 1, "a", "b", 5, "2"])
        assert myarr.sort() == [1, 2, "2", 3, 5, "a", "b"]
        assert myarr.reverse() == ["b", "a", 5, 3, "2", 2, 1]
        # print(myarr.fill()) # note - js returns list of undefined
        assert myarr.fill() == [None, None, None, None, None, None, None]
        # print(myarr.fill(1))
        assert myarr.fill(1) == [1, 1, 1, 1, 1, 1, 1]
        # print(myarr.fill(1, 1))
        assert myarr.fill(1, 1) == [1, 1, 1, 1, 1, 1, 1]
        assert myarr.fill(7, 1, 3) == [1, 7, 7, 1, 1, 1, 1]
        # print(myarr.isArray()) # fails as it should as its a static method.
        assert Array.isArray(myarr) == True

        myarr = Array([3, 4, 2, "b", "c", 6, 3])
        # print(myarr.map(lambda x: x + 1 if type(x) == int else chr(ord(x) + 1)))
        assert myarr.map(lambda x: x + 1 if type(x) == int else chr(ord(x) + 1)) == [
            4,
            5,
            3,
            "c",
            "d",
            7,
            4,
        ]
        # print(myarr.filter()) # passing nothing fails like javascript
        with self.assertRaises(TypeError):
            myarr.filter()
        # print(myarr.filter(lambda x: x == "a"))
        assert myarr.filter(lambda x: x == "a") == []
        # print(myarr.filter(lambda x: x == 3))
        assert myarr.filter(lambda x: x == 3) == [3, 3]
        # print(myarr.reduce()) # passing nothing fails like javascript
        with self.assertRaises(TypeError):
            myarr.reduce()
        # print(myarr.reduce(lambda x, y: x + y))
        # print(myarr)
        myarr = Array([3, 4, 2, 6, 3])
        # print(myarr.reduce(lambda x, y: x + y))
        assert myarr.reduce(lambda x, y: x + y) == 18
        # print(myarr)
        assert myarr.reduce(lambda x, y: x + y, 10) == 28
        # print(myarr.reduceRight())
        with self.assertRaises(TypeError):
            myarr.reduceRight()
        # print(myarr.reduceRight(lambda x, y: x + y))
        assert myarr.reduceRight(lambda x, y: x + y) == 18
        # print(myarr)
        assert myarr.reduceRight(lambda x, y: x + y, 10) == 28

        with self.assertRaises(TypeError):
            myarr.every()
        # print(myarr.every(lambda x: x == "a"))
        assert myarr.every(lambda x: x == "a") == False

        # do a test for true
        myarr = Array([3, 3, 3, 3, 3])
        # print(myarr.every(lambda x: x == 3))
        assert myarr.every(lambda x: x == 3) == True

        myarr = Array([3, 4, 2, "b", "c", 6, 3])
        with self.assertRaises(TypeError):
            myarr.some()
        # print(myarr.some(lambda x: x == "a"))
        assert myarr.some(lambda x: x == "b") == True

        # print(myarr.find())
        with self.assertRaises(TypeError):
            myarr.find()

        # print(myarr.find(lambda x: x == "a"))
        assert myarr.find(lambda x: x == "a") == None
        # print(myarr.find(lambda x: x == "b"))
        assert myarr.find(lambda x: x == "b") == "b"
        assert myarr.findIndex("b") == 3
        assert myarr.findIndex("missing") == -1
        assert list(myarr.keys()) == list(range(len(myarr)))
        assert list(myarr.entries()) == [
            [0, 3],
            [1, 4],
            [2, 2],
            [3, "b"],
            [4, "c"],
            [5, 6],
            [6, 3],
        ]

        assert Array.from_("abc") == ["a", "b", "c"]
        assert Array.from_({"a": 1}) == [("a", 1)]
        assert Array.of(1, 2, 3) == [1, 2, 3]
        assert Array([1, [2, [3]], 4]).flat() == [1, 2, [3], 4]
        assert Array([1, [2, [3]], 4]).flat(2) == [1, 2, 3, 4]
        assert Array([1, 2, 3]).flatMap(lambda value: [value, value * 10]) == [
            1,
            10,
            2,
            20,
            3,
            30,
        ]
        assert Array([1, 2, 3, 4]).groupBy(
            lambda value, index, arr: "even" if value % 2 == 0 else "odd"
        ) == {
            "odd": [1, 3],
            "even": [2, 4],
        }

    def test_javascript_array_extended_surface(self):
        self.assertEqual(Array.from_((1, 2)), [1, 2])
        self.assertEqual(Array.from_(x for x in [3, 4]), [3, 4])
        self.assertEqual(Array.from_(10), [""] * 10)

        arr = Array(3)
        self.assertEqual(arr, ["", "", ""])
        arr[1] = "x"
        self.assertEqual(arr[1], "x")
        self.assertEqual(arr.toString(), ",x,")
        self.assertEqual(arr.toSource(), ["", "x", ""])
        self.assertEqual(repr(arr), "['', 'x', '']")
        self.assertNotEqual(arr, "not-an-array")

        self.assertEqual(Array([1, 2]) + [3, 4], [1, 2, 3, 4])
        self.assertEqual(Array([1, 2]) + Array([3]), [1, 2, 3])
        with self.assertRaises(ValueError):
            Array([1, 2]) + 3
        with self.assertRaises(ValueError):
            Array([1, 2]) - 3
        self.assertEqual(Array([1, 2]).flat(0), [1, 2])
        with self.assertRaises(ValueError):
            Array([1]).flat(-1)

    def test_javascript_array_edge_cases(self):
        myarr = Array([1, float("nan"), 3])
        self.assertTrue(myarr.includes(float("nan")))
        self.assertEqual(myarr.indexOf(float("nan")), -1)
        self.assertEqual(myarr.lastIndexOf("missing"), -1)
        self.assertIs(Array([1, 2]).at(5), undefined)
        self.assertIs(Array([1, 2]).at(-3), undefined)

        self.assertEqual(Array([1, 2, 3, 4]).fill(0, -2), [1, 2, 0, 0])
        self.assertEqual(Array([1, 2, 3]).fill(9, 1, 99), [1, 9, 9])
        self.assertEqual(Array([1, 2, 3]).fill(9, 2, 1), [1, 2, 3])

        spliced = Array(["a", "b", "c"])
        self.assertEqual(spliced.splice(1, -1, "x"), [])
        self.assertEqual(spliced, ["a", "x", "b", "c"])

        spliced = Array(["a", "b", "c"])
        self.assertEqual(spliced.splice(-2, 1, "x"), ["b"])
        self.assertEqual(spliced, ["a", "x", "c"])
        self.assertEqual(
            Array(["a", "b", "c"]).findIndex(lambda value: value == "b"), 1
        )
        visited = []
        myarr = Array(["a", "b"])
        myarr.forEach(
            lambda value, index, values: visited.append((value, index, values))
        )
        self.assertEqual(visited, [("a", 0, myarr.args), ("b", 1, myarr.args)])

        values = []
        myarr.forEach(lambda value: values.append(value))
        self.assertEqual(values, ["a", "b"])

    def test_javascript_map(self):
        mapping = Map({"a": 1})
        self.assertTrue(mapping.has("a"))
        self.assertEqual(mapping.get("a"), 1)
        self.assertEqual(mapping.keys(), ["a"])
        self.assertEqual(mapping.entries(), [("a", 1)])
        self.assertEqual(mapping.values(), [1])
        mapping.set("b", 2)
        self.assertEqual(mapping.get("b"), 2)
        self.assertEqual(mapping.keys(), ["a", "b"])
        self.assertEqual(mapping.values(), [1, 2])
        visited = []
        mapping.forEach(lambda value, key, owner: visited.append((value, key, owner)))
        self.assertEqual(visited, [(1, "a", mapping), (2, "b", mapping)])
        self.assertTrue(mapping.delete("a"))
        self.assertFalse(mapping.delete("a"))
        self.assertFalse(mapping.has("a"))
        mapping.clear()
        self.assertFalse(mapping.has("b"))
        self.assertEqual(mapping.keys(), [])
        self.assertEqual(mapping.entries(), [])

        list_map = Map(["x", "y"])
        self.assertEqual(list_map.get("x"), "x")
        self.assertEqual(list_map.get("y"), "y")
        numeric = Map({1: "one"})
        self.assertTrue(numeric.delete(1))
        self.assertFalse(numeric.has(1))

    def test_javascript_interval(self):
        callback = Mock()
        test = window.setInterval(callback, 10)
        time.sleep(0.05)
        window.clearInterval(test)
        self.assertGreaterEqual(callback.call_count, 1)

    def test_javascript_Number(self):
        # print(Number.MAX_VALUE)
        assert Number.MAX_VALUE == 1.7976931348623157e308

    def test_javascript_fetch(self):
        urls = ["http://google.com", "http://linkedin.com"]

        def fake_request(url, f=None, **kwargs):
            response = Mock()
            response.url = url
            response.ok = True
            response.text = f"response:{url}"
            if f is not None and hasattr(f, "results"):
                f.results.append(response)
            return response

        with patch.object(Window, "_do_request", side_effect=fake_request):
            promise = window.fetch(urls[0], timeout=1)
            self.assertEqual(promise.state, "fulfilled")
            self.assertEqual(promise.data.url, urls[0])
            self.assertEqual(Window._do_request.call_args_list[0].kwargs["timeout"], 1)
            self.assertEqual(
                promise.then(lambda response: response.text).data, f"response:{urls[0]}"
            )

            fetched = window.fetch_set(urls)
            self.assertEqual(len(fetched.results), 2)
            self.assertTrue(all(result.ok for result in fetched.results))
            self.assertEqual([result.url for result in fetched.results], urls)

            threaded = window.fetch_threaded(urls)
            self.assertEqual(len(threaded.results), 2)
            self.assertEqual([result.url for result in threaded.results], urls)

            pooled = window.fetch_pooled(urls)
            self.assertEqual(len(pooled.results), 2)
            self.assertEqual(
                sorted(result.url for result in pooled.results), sorted(urls)
            )

            async_response = asyncio.run(window.fetch_async(urls[0], timeout=2))
            self.assertEqual(async_response.url, urls[0])
            self.assertEqual(Window._do_request.call_args_list[-1].kwargs["timeout"], 2)

    def test_javascript_do_request_success_and_failure(self):
        class FakeRequest:
            def __init__(self, method, url):
                self.method = method
                self.url = url

        class FakeSession:
            def prepare_request(self, req):
                return req

            def send(self, prepped, **kwargs):
                response = Mock()
                response.method = prepped.method
                response.url = prepped.url
                return response

            def close(self):
                return None

        fetched = FetchedSet()
        fake_requests = SimpleNamespace(
            Request=FakeRequest, Session=lambda: FakeSession()
        )
        with patch.dict("sys.modules", {"requests": fake_requests}):
            response = Window._do_request(
                "https://example.com",
                fetched,
                method="POST",
                callback_function=lambda _: _,
                error_handler=None,
            )
        self.assertEqual(response.url, "https://example.com")
        self.assertEqual(response.method, "POST")
        self.assertEqual(len(fetched.results), 1)

        broken_requests = SimpleNamespace(
            Request=FakeRequest,
            Session=lambda: (_ for _ in ()).throw(RuntimeError("boom")),
        )
        with patch.dict("sys.modules", {"requests": broken_requests}), patch(
            "builtins.print"
        ) as print_mock:
            self.assertIsNone(Window._do_request("https://example.com"))
        print_mock.assert_called()

    def test_javascript_promise(self):
        myPromise = Promise(lambda resolve, reject: resolve("once!"))
        returned = myPromise.then(lambda successMessage: str(successMessage).upper())
        self.assertIs(returned, myPromise)
        self.assertEqual(myPromise.state, "fulfilled")
        self.assertEqual(myPromise.data, "ONCE!")

        rejected = Promise(lambda resolve, reject: reject("bad"))
        self.assertEqual(
            rejected.catch(lambda error: f"caught:{error}").data, "caught:bad"
        )
        self.assertEqual(rejected.state, "rejected")

        pending = Promise()
        seen = []
        pending.then(lambda value: seen.append(value) or f"{value}!")
        self.assertEqual(seen, [])
        pending.resolve("later")
        self.assertEqual(seen, ["later"])
        self.assertEqual(pending.data, "later!")
        self.assertEqual(pending.state, "fulfilled")

        caught_later = Promise()
        caught_later.catch(lambda error: f"queued:{error}")
        caught_later.reject("bad")
        self.assertEqual(caught_later.data, "queued:bad")
        self.assertEqual(caught_later.state, "rejected")

        thrown = Promise()
        thrown.then(lambda value: (_ for _ in ()).throw(RuntimeError("boom")))
        thrown.catch(lambda error: f"handled:{error}")
        thrown.resolve("start")
        self.assertEqual(thrown.data, "handled:boom")
        self.assertEqual(thrown.state, "rejected")

    def test_javascript_string(self):
        mystr = String("Some String")

        assert mystr.toLowerCase() == "some string"
        assert mystr.toUpperCase() == "SOME STRING"

        # print(type(mystr))
        # print(mystr.length)
        assert mystr.length == 11

        assert mystr.repeat(2) == "Some StringSome String"
        # print(mystr)
        # print(mystr)
        # print(mystr)
        assert mystr.startsWith("S")
        assert mystr.startsWith("String", 5)
        assert mystr.endsWith("String")
        assert mystr.endsWith("Some", 0, 4)

        # print(">>", mystr.substr(1))
        assert mystr.substr(1) == "ome String"

        # substring
        # print(mystr)
        # print(mystr.substring(1, 3))
        assert mystr.substring(1, 3) == "om"

        # slice
        # print(mystr.slice(1, 3))
        assert mystr.slice(1, 3) == "om"

        # test trim
        mystr = String("   Some String   ")
        assert mystr.trim() == "Some String"

        # charAt
        mystr = String("Some String")
        assert mystr.charAt(1) == "o"
        assert mystr.charAt(5) == "S"

        # charCodeAt
        assert mystr.charCodeAt(1) == 111
        assert mystr.fromCharCode(111) == "o"

        # test
        # assert(mystr.test('a') == True)
        # assert(mystr.test('b') == False)

        # replace
        # print(mystr.replace('S', 'X'))
        assert mystr.replace("S", "X") == "Xome String"
        assert mystr.replace(" ", "X") == "SomeXString"
        assert mystr.replace("S", "X") != "Xome Xtring"
        assert mystr.replace(RegExp("s", "i"), "X") == "Xome String"
        assert mystr.replace(RegExp("s", "ig"), "X") == "Xome Xtring"
        # JavaScript replacement patterns: $1/$2 for groups, $& for the match,
        # $$ for a literal dollar.
        assert mystr.replace(RegExp(r"(\w+)\s+(\w+)"), "$2 $1") == "String Some"
        assert mystr.replace(RegExp(r"\w+"), "[$&]") == "[Some] String"
        assert mystr.replace(RegExp(r"Some"), "$$") == "$ String"
        assert mystr.replace(RegExp(r"(o)"), "$3") == "S$3me String"

        # localeCompare
        self.assertLess(String("apple").localeCompare("banana"), 0)
        self.assertEqual(String("apple").localeCompare("apple"), 0)
        self.assertGreater(String("banana").localeCompare("apple"), 0)
        self.assertLess(String("a").localeCompare("aa"), 0)

        # search
        mystr = String("Some String")
        assert mystr.search("a") == -1
        assert mystr.search("o") == 1

        # substr
        assert mystr.substr(1, 2) == "om"
        assert mystr.substr(1, 3) == "ome"
        assert mystr.substr(1, 4) == "ome "
        assert mystr.substr(1, 5) == "ome S"

        # toLocaleLowerCase
        # print(mystr.toLocaleLowerCase())
        assert mystr.toLocaleLowerCase() == "some string"
        # print(mystr.toLocaleLowerCase())
        assert mystr.toLocaleLowerCase() == "some string"

        # toLocaleUpperCase
        # print(mystr.toLocaleUpperCase())
        assert mystr.toLocaleUpperCase() == "SOME STRING"

        # compile
        # print(mystr.compile())
        # assert(mystr.compile() == '"Some String"')

        # lastIndex
        # print(mystr.lastIndexOf('o'))
        assert mystr.lastIndexOf("o") == 1
        assert mystr.lastIndexOf("z") == -1

        # replace
        assert mystr.codePointAt(1) == 111
        # print(mystr.padEnd(2))
        # print(f"-{mystr}-")
        assert mystr.padEnd(13) == "Some String  "
        assert mystr.padStart(13) == "  Some String"
        assert mystr.padStart(13, "-") == "--Some String"
        # assert mystr.localeCompare('a', 'a') == 0

        assert mystr.includes("a") == False
        assert mystr.includes("Some") == True
        self.assertEqual(String("aba").search("b"), 1)
        assert String("  Some").trimStart() == "Some"
        assert String("String  ").trimEnd() == "String"

    def test_javascript_URLSearchParams(self):
        paramsString = "q=test&topic=api"
        searchParams = URLSearchParams(paramsString)

        # Iterate the search parameters.
        self.assertEqual(list(searchParams), [("q", ["test"]), ("topic", ["api"])])

        assert searchParams.has("topic") == True  # True
        # print( searchParams.get("topic") )
        assert searchParams.get("topic") == "api"  # True
        # searchParams.getAll("topic"); # ["api"]
        assert searchParams.get("foo") is None  # true
        searchParams.append("topic", "webdev")
        assert searchParams.toString() == "q=test&topic=api&topic=webdev"
        searchParams.set("topic", "More webdev")
        assert searchParams.toString() == "q=test&topic=More+webdev"
        searchParams.delete("topic")
        assert searchParams.toString() == "q=test"
        searchParams.delete("missing")
        assert searchParams.toString() == "q=test"
        assert searchParams.getAll("missing") == []

        emptyParams = URLSearchParams("empty=&flag")
        assert emptyParams.get("empty") == ""
        assert emptyParams.get("flag") == ""
        assert emptyParams.toString() == "empty=&flag="

        # GOTCHAS

        paramsString1 = "http://example.com/search?query=%40"
        searchParams1 = URLSearchParams(paramsString1)

        assert searchParams1.has("query") == False
        assert searchParams1.has("http://example.com/search?query") == True

        assert searchParams1.get("query") == None
        searchParams1.get(
            "http://example.com/search?query"
        )  # "@" (equivalent to decodeURIComponent('%40'))

        paramsString2 = "?query=value"
        searchParams2 = URLSearchParams(paramsString2)
        assert searchParams2.has("query") == True

        url = URL("http://example.com/search?query=%40")

        searchParams3 = URLSearchParams(url.search)

        self.assertEqual(searchParams3.toString(), "query=%40")

        base64 = window.btoa(
            String.fromCharCode(19, 224, 23, 64, 31, 128)
        )  # base64 is "E+AXQB+A"
        searchParams = URLSearchParams("q=foo&bin=" + str(base64))  # q=foo&bin=E+AXQB+A
        self.assertTrue(searchParams.has("bin"))
        # getBin = searchParams.get("bin")  # "E AXQB A" + char is replaced by spaces
        # print(getBin)
        # window.btoa(window.atob(getBin))  # "EAXQBA==" no error thrown
        # window.btoa(String.fromCharCode(16, 5, 208, 4))  # "EAXQBA==" decodes to wrong binary value
        # getBin.replace(r'/ /g', "+")  # "E+AXQB+A" is one solution

        # or use set to add the parameter, but this increases the query string length
        # searchParams.set("bin2", base64)  # "q=foo&bin=E+AXQB+A&bin2=E%2BAXQB%2BA" encodes + as %2B
        # searchParams.get("bin2")  # "E+AXQB+A"

    def test_javascript_FormData(self):
        from domonic.webapi.xhr import FormData as XHRFormData

        data = FormData()
        data.append("name", "domonic")

        self.assertIsInstance(data, XHRFormData)
        self.assertEqual(data.get("name"), "domonic")

    def test_javascript_Worker(self):
        with self.assertRaises(FileNotFoundError):
            Worker("/worker.py")

    def test_javascript_Intl_supportedValuesOf(self):
        self.assertIn("gregory", Intl.supportedValuesOf("calendar"))
        self.assertIn("GBP", Intl.supportedValuesOf("en-GB", "currency"))
        self.assertIn("latn", Intl.supportedValuesOf("numberingSystem"))
        self.assertIn("meter", Intl.supportedValuesOf("unit"))
        self.assertIn("UTC", Intl.supportedValuesOf("timeZone"))

        with self.assertRaises(ValueError):
            Intl.supportedValuesOf("not-a-real-key")

    def test_javascript_Intl_NumberFormat(self):
        formatter = Intl.NumberFormat(
            "en-US", {"minimumFractionDigits": 0, "maximumFractionDigits": 2}
        )
        self.assertEqual(formatter.format(1234.567), "1,234.57")
        self.assertEqual(formatter.format("1234.5"), "1,234.5")

        no_grouping = Intl.NumberFormat("en-US", {"useGrouping": False})
        self.assertEqual(no_grouping.format(1234), "1234")

        currency = Intl.NumberFormat("en-GB", {"style": "currency", "currency": "GBP"})
        self.assertEqual(currency.format(1234.5), "GBP 1,234.50")
        self.assertEqual(
            Intl.NumberFormat("en-US", {"style": "currency", "currency": "USD"}).format(
                -12.5
            ),
            "-$12.50",
        )

        percent = Intl.NumberFormat(
            "en-US", {"style": "percent", "maximumFractionDigits": 1}
        )
        self.assertEqual(percent.format(0.123), "12.3%")
        self.assertEqual(
            currency.resolvedOptions()["currencyDisplay"],
            "symbol",
        )
        self.assertEqual(
            Intl.NumberFormat.supportedLocalesOf(["en-us", "fr-fr"]),
            ["en-US", "fr-FR"],
        )

    def test_javascript_Intl_Collator(self):
        collator = Intl.Collator(
            "en-US", {"sensitivity": "base", "ignorePunctuation": True}
        )
        self.assertEqual(collator.compare("resume!", "Resume"), 0)
        self.assertLess(collator.compare("apple", "banana"), 0)
        self.assertGreater(collator.compare("banana", "apple"), 0)

        numeric = Intl.Collator("en-US", {"numeric": True})
        self.assertLess(numeric.compare("item2", "item10"), 0)
        self.assertEqual(
            numeric.resolvedOptions()["locale"],
            "en-US",
        )
        self.assertEqual(
            Intl.Collator.supportedLocalesOf(["en-us", "cy-gb"]),
            ["en-US", "cy-GB"],
        )

    def test_javascript_screen(self):
        screen = Screen(1280, 720, availWidth=1200, availHeight=700, colorDepth=30)
        self.assertEqual(screen.width, 1280)
        self.assertEqual(screen.height, 720)
        self.assertEqual(screen.availWidth, 1200)
        self.assertEqual(screen.availHeight, 700)
        self.assertEqual(screen.colorDepth, 30)
        self.assertEqual(screen.pixelDepth, 30)
        self.assertEqual(window.screen.width, 1024)
        self.assertEqual(Window().screen.height, 768)

    def test_javascript_at(self):
        myarr = Array(["a", "b", "c", "d"])
        assert myarr.at(-1) == "d"
        myarr = ["a", "b", "c", "d"]
        myarr = Array(myarr)
        assert myarr.at(-1) == "d"
        myarr = Array("a", "b", "c", "d")
        assert myarr.at(-1) == "d"

    # def test_javascript_Node(self):
    # url = require('url');
    # console.log(url.domainToASCII('español.com'))
    # console.log(url.domainToASCII('??.com'))
    # console.log(url.domainToASCII('xn--iñvalid.com'))
    # console.log(url.domainToUnicode('español.com'))
    # console.log(url.domainToUnicode('??.com'))
    # console.log(url.domainToUnicode('xn--iñvalid.com'))

    # def test_javascript_call(self):

    #     class Product():
    #         def __init__(self, name, price):
    #             self.name = name
    #             self.price = price

    #     class Food():
    #         def __init__(self, name, price):
    #             Function(Product).call(self, name, price)
    #             self.category = 'food'

    #     class Toy():
    #         def __init__(self, name, price):
    #             Function(Product).call(self, name, price)
    #             self.category = 'toy'

    #     cheese = Food('feta', 5)
    #     fun = Toy('robot', 40)

    #     print(cheese)
    #     print(fun)

    def test_javascript_called(self):

        from domonic.decorators import called
        from domonic.dQuery import º

        response = Mock()
        response.text = "sweet!"
        seen = []
        errors = []

        with patch.object(º, "ajax", return_value=response):

            @called(
                lambda: º.ajax("https://www.google.com"), lambda err: errors.append(err)
            )
            def success(data=None):
                seen.append(data.text if data is not None else None)

        from domonic.decorators import iife

        iife_seen = []

        @iife()
        def sup():
            iife_seen.append("sup")
            return True

        self.assertEqual(seen, ["sweet!"])
        self.assertEqual(errors, [])
        self.assertEqual(iife_seen, ["sup"])
        self.assertTrue(callable(sup))

    def test_javascript_numbersandstrings(self):
        n = Number(1)
        n2 = Number(2)
        self.assertEqual(n + n2, 3)

        s = String("a")
        s2 = String("b")
        self.assertEqual(s + s2, "ab")
        self.assertEqual(s * n2, "aa")

        test = String("test")
        self.assertEqual(test[0:1], "t")
        self.assertEqual(test.toUpperCase(), "TEST")
        self.assertEqual(test.toLowerCase(), "test")
        self.assertEqual(test.toLocaleLowerCase(), "test")
        self.assertEqual(test.toLocaleUpperCase(), "TEST")

    def test_javascript_number_methods(self):
        value = Number(255)
        self.assertEqual(value.toString(None), "255")
        self.assertEqual(value.toString(16), "ff")
        self.assertEqual(Number(-10).toString(2), "-1010")
        self.assertEqual(Number.NEGATIVE_INFINITY, float("-inf"))
        self.assertEqual(Number.POSITIVE_INFINITY, float("inf"))
        self.assertEqual(Number(12.3456).toFixed(2), "12.35")
        self.assertEqual(Number(12.3456).toExponential(2), "1.23e+1")
        self.assertEqual(Number(1).toExponential(2), "1.00e+0")
        self.assertEqual(Number(0.001).toExponential(), "1e-3")
        self.assertEqual(Number(100000000).toExponential(), "1e+8")
        self.assertEqual(Number(12.3456).toPrecision(4), "12.35")
        self.assertTrue(Number.isInteger(5))
        self.assertFalse(Number.isInteger(5.5))
        self.assertEqual(abs(Number(-5)), 5)
        self.assertEqual(Number(5) // 2, 2)
        self.assertEqual(20 // Number(5), 4)
        self.assertEqual(Number(5) % 2, 1)
        self.assertEqual(11 % Number(5), 1)
        self.assertEqual(Number(5) & 3, 1)
        self.assertEqual(Number(5) | 2, 7)
        self.assertEqual(Number(5) ^ 1, 4)
        self.assertEqual(Number(5) << 1, 10)
        self.assertEqual(Number(5) >> 1, 2)
        self.assertEqual(+Number(5), 5)
        self.assertEqual(-Number(5), -5)
        self.assertTrue(Number(5) < 6)
        self.assertTrue(Number(5) <= 5)
        self.assertTrue(Number(5) > 4)
        self.assertTrue(Number(5) >= 5)
        self.assertEqual(Number(5).__iadd__(2), 7)
        self.assertEqual(Number(5).__isub__(2), 3)
        self.assertEqual(Number(5).__imul__(2), 10)
        self.assertEqual(Number(5).__idiv__(2), 2.5)
        self.assertEqual(Number(5).__imod__(2), 1)
        self.assertEqual(Number(5).__ipow__(2), 25)
        self.assertEqual(Number(5).__ilshift__(1), 10)
        self.assertEqual(Number(5).__irshift__(1), 2)
        self.assertEqual(Number(5).__iand__(3), 1)
        self.assertEqual(Number(5).__ior__(2), 7)
        self.assertEqual(Number(5).__ixor__(1), 4)
        self.assertEqual(Number(5).__truediv__(2), 2.5)
        self.assertEqual(Number(10).__rtruediv__(20), 2)
        self.assertEqual(Number(5).__itruediv__(20), 4)
        self.assertEqual(Number(3).__rmod__(10), 1)
        self.assertEqual(Number(1.2e3).toExponential(), "1.2e+3")
        self.assertEqual(Number(10).toFixed(-2), "10")
        self.assertEqual(Number(0).toString(16), "0")
        self.assertEqual(Number(float("inf")).toPrecision(2), "inf")
        self.assertTrue(Number.isSafeInteger(5))
        self.assertTrue(Number.isSafeInteger(5.0))
        self.assertTrue(Number.isSafeInteger(2**53 - 1))
        self.assertFalse(Number.isSafeInteger(5.5))
        self.assertFalse(Number.isSafeInteger(2**53))
        self.assertFalse(Number.isSafeInteger(float("inf")))
        self.assertFalse(Number.isSafeInteger("NaN"))
        with self.assertRaises(ValueError):
            Number(1).toPrecision(0)

    def test_javascript_string_extended_surface(self):
        text = String("Hello.World")
        self.assertTrue(text == "Hello.World")
        self.assertTrue(text == String("Hello.World"))
        self.assertFalse(text == "Other")
        self.assertEqual("Say " + text, "Say Hello.World")
        self.assertEqual(text + "!", "Hello.World!")
        self.assertEqual(text.__iadd__("!"), "Hello.World!")
        self.assertEqual(text * 2, "Hello.WorldHello.World")
        self.assertEqual(2 * text, "Hello.WorldHello.World")
        self.assertEqual(text.__imul__(2), "Hello.WorldHello.World")
        self.assertEqual(text.split(r"\."), ["Hello", "World"])
        self.assertEqual(String("a,b,c").split(","), ["a", "b", "c"])
        self.assertEqual(text.concat("!", seperator=""), "Hello.World!")
        self.assertEqual(
            text.replace(r"Hello", lambda match: match.group(0).upper()), "HELLO.World"
        )
        self.assertEqual(text.replaceAll(".", "-"), "Hello-World")
        self.assertEqual(
            text.replaceAll(RegExp(r"(\w)o"), "$1O"), "HellO.WOrld"
        )
        self.assertEqual(text.indexOf("World"), 6)
        self.assertEqual(text.indexOf("missing"), -1)
        self.assertEqual(
            [m[0] for m in text.matchAll(r"[A-Z]")], ["H", "W"]
        )
        self.assertEqual(text.match(r"l+")[0], "ll")
        self.assertIsNone(text.match(r"z"))
        self.assertEqual(text.match(RegExp(r"[A-Z]", "g")), ["H", "W"])
        self.assertEqual(text.search(r"\."), 5)
        self.assertEqual(text.compile(r"World").pattern, "World")
        self.assertEqual(text.anchor("greeting"), '<a name="greeting">Hello.World</a>')
        self.assertEqual(text.big(), "<big>Hello.World</big>")
        self.assertEqual(text.blink(), "<blink>Hello.World</blink>")
        self.assertEqual(text.bold(), "<b>Hello.World</b>")
        self.assertEqual(text.fixed(), "<tt>Hello.World</tt>")
        self.assertEqual(text.fontcolor("red"), "<font color=red>Hello.World</font>")
        self.assertEqual(text.fontsize("3"), "<font size=3>Hello.World</font>")
        self.assertEqual(text.italics(), "<i>Hello.World</i>")
        self.assertEqual(text.link("/home"), "<a href=/home>Hello.World</a>")
        self.assertEqual(text.small(), "<small>Hello.World</small>")
        self.assertEqual(text.strike(), "<strike>Hello.World</strike>")
        self.assertEqual(text.sub(), "<sub>Hello.World</sub>")
        self.assertEqual(text.sup(), "<sup>Hello.World</sup>")
        self.assertEqual(String.fromCodePoint(65), "A")
        self.assertEqual(String.toCodePoint("A"), 65)
        self.assertEqual(String.toCharCode("A"), 65)
        self.assertEqual(String.raw(r"a\b"), r"a\\b")
        rendered = text("div", _id="greeting")
        self.assertEqual(rendered.tagName, "div")
        self.assertEqual(rendered.getAttribute("id"), "greeting")
        self.assertIn("Hello.World", str(rendered))
        self.assertEqual(text.div(_class="hero").tagName, "div")
        self.assertIn("<html>", text.webpage())

    def test_javascript_string_edge_cases(self):
        self.assertEqual(String("a.b.c").split("."), ["a", "b", "c"])
        self.assertEqual(String("abc").split(""), ["a", "b", "c"])
        self.assertEqual(String("abcabc").indexOf("a", -1), 0)
        self.assertEqual(String("abc").indexOf("", 99), 3)
        self.assertEqual(String("ababa").lastIndexOf("ba", 2), 1)
        self.assertEqual(String("ababa").lastIndexOf("a", 0), 0)
        self.assertEqual(String("abc").lastIndexOf("", 99), 3)
        self.assertTrue(String("abc").includes("a", -1))
        self.assertTrue(String("abc").includes("", 99))
        self.assertEqual(String("abc").charAt(-1), "")
        self.assertEqual(String("abc").charCodeAt(99), "NaN")
        self.assertIs(String("abc").codePointAt(99), undefined)
        self.assertEqual(String("abc").substring(2, 1), "b")
        self.assertEqual(String("abc").substr(1, -1), "")
        self.assertEqual(String("abc").padStart(6, "01"), "010abc")
        self.assertEqual(String("abc").padEnd(6, "01"), "abc010")
        self.assertEqual(String("abc").padStart(6, ""), "abc")
        with self.assertRaises(ValueError):
            String("x").repeat(-1)

    def test_javascript_regexp_surface(self):
        regex = RegExp(r"(foo)(bar)", "im")
        self.assertTrue(regex.ignoreCase)
        self.assertTrue(regex.multiline)
        self.assertFalse(regex.dotAll)
        regex.dotAll = True
        regex.global_ = True
        regex.hasIndices = True
        regex.unicode = True
        self.assertTrue(regex.dotAll)
        self.assertTrue(regex.global_)
        self.assertTrue(regex.hasIndices)
        self.assertTrue(regex.unicode)
        self.assertEqual(regex.source, r"(foo)(bar)")
        # exec returns [fullMatch, *groups] with .index / .input (JS semantics)
        match = regex.exec("xxfoobarxx")
        self.assertEqual(match, ["foobar", "foo", "bar"])
        self.assertEqual(match.index, 2)
        self.assertEqual(match.input, "xxfoobarxx")
        self.assertEqual(RegExp(r"foo").exec("xxfooxx"), ["foo"])
        self.assertIsNone(RegExp(r"foo").exec("nope"))
        # a global regex shares lastIndex between exec/test, like JS
        regex.lastIndex = 0
        self.assertTrue(regex.test("foobar"))
        regex.lastIndex = 0
        self.assertTrue(regex.test("xxFooBarxx"))
        regex.lastIndex = 0
        self.assertFalse(regex.test("barfoo"))
        self.assertEqual(regex.toString(), "/(foo)(bar)/dgimsu")
        self.assertEqual(str(regex), r"(foo)(bar)")
        self.assertIs(regex.compile(r"hello", "i"), regex)
        self.assertEqual(regex.source, "hello")
        self.assertTrue(regex.ignoreCase)
        self.assertTrue(regex.test("well HELLO there"))
        self.assertIs(regex.compile(RegExp(r"^bye$", "m")), regex)
        self.assertEqual(regex.source, r"^bye$")
        self.assertTrue(regex.multiline)
        self.assertTrue(regex.test("hi\nbye"))
        with self.assertRaises(re.error):
            regex.compile("[")
        self.assertEqual(regex.source, r"^bye$")

    def test_regexp_unicode_property_classes(self):
        self.assertTrue(RegExp(r"^[\p{L}]+$", "u").test("café"))
        self.assertFalse(RegExp(r"^[\p{L}]+$", "u").test("ab12"))
        self.assertTrue(RegExp(r"[\p{P}\p{S}]").test("a + b"))
        self.assertTrue(RegExp(r"[\p{P}\p{S}]").test("hi!"))
        self.assertFalse(RegExp(r"[\p{P}\p{S}]").test("plain"))
        # negated, standalone
        self.assertEqual(RegExp(r"\P{L}", "").exec("ab-cd")[0], "-")

    def test_regexp_named_groups_and_replace(self):
        m = RegExp(r"(?<y>\d{4})-(?<m>\d{2})").exec("2024-06")
        self.assertEqual(m[0], "2024-06")
        self.assertEqual(m.groups, {"y": "2024", "m": "06"})
        self.assertEqual(
            String("2024-06").replace(
                RegExp(r"(?<y>\d{4})-(?<m>\d{2})"), "$<m>/$<y>"
            ),
            "06/2024",
        )
        # RegExp.replace convenience (JS RegExp[Symbol.replace])
        self.assertEqual(RegExp(r"o", "g").replace("foo boo", "0"), "f00 b00")
        self.assertEqual(
            RegExp(r"(\w+)\s(\w+)").replace("Some String", "$2 $1"), "String Some"
        )

    def test_regexp_sticky_flag_and_last_index(self):
        r = RegExp(r"\d+", "y")
        r.lastIndex = 0
        self.assertEqual(r.exec("12,34")[0], "12")
        self.assertEqual(r.lastIndex, 2)
        self.assertIsNone(r.exec("12,34"))  # "," is not a digit at lastIndex 2
        r.lastIndex = 3
        self.assertEqual(r.exec("12,34")[0], "34")

        g = RegExp(r"\w+", "g")
        tokens = []
        while (match := g.exec("foo bar baz")) is not None:
            tokens.append(match[0])
        self.assertEqual(tokens, ["foo", "bar", "baz"])

    def test_string_replace_js_style_callback(self):
        # JS replacer signature: (match, p1, ..., offset, string)
        self.assertEqual(
            String("a1b2").replace(
                RegExp(r"([a-z])(\d)", "g"),
                lambda whole, letter, digit, offset, source: f"{digit}{letter}",
            ),
            "1a2b",
        )
        # one-argument callbacks still receive the match object
        self.assertEqual(
            String("hello").replace(RegExp("l", "g"), lambda m: m.group(0).upper()),
            "heLLo",
        )

    def test_javascript_error_message(self):
        err = Error("boom")

        self.assertEqual(err.message, "boom")
        self.assertEqual(str(err), "boom")

    def test_set(self):

        mySet1 = Set()
        self.assertIs(mySet1.species, Set)

        mySet1.add(1)  # Set [ 1 ]
        assert mySet1.size == 1
        assert mySet1.contains(1) == True
        assert mySet1.contains(2) == False

        mySet1.add(5)  # Set [ 1, 5 ]
        assert mySet1.size == 2
        assert mySet1.contains(1) == True
        assert mySet1.contains(2) == False
        assert mySet1.contains(5) == True

        mySet1.add(5)  # Set [ 1, 5 ]
        assert mySet1.size == 2
        assert mySet1.contains(1) == True

        mySet1.add("some text")  # Set [ 1, 5, 'some text' ]
        assert mySet1.size == 3
        assert mySet1.contains(1) == True
        assert mySet1.contains(2) == False
        assert mySet1.contains(5) == True
        assert mySet1.contains("some text") == True
        assert mySet1.contains("text") == False
        self.assertTrue(mySet1.delete(5))
        self.assertFalse(mySet1.delete(5))
        self.assertFalse(mySet1.contains(5))
        self.assertTrue(all(left == right for left, right in mySet1.entries()))

        self.assertIs(mySet1.add(5), mySet1)
        o = {"a": 1, "b": 2}
        mySet1.add(o)
        assert mySet1.size == 4
        assert mySet1.contains(o) == True

        mySet1.add({"a": 1, "b": 2})
        assert mySet1.size == 5

        assert mySet1.has(1) == True
        assert mySet1.has(3) == False
        assert mySet1.has(5) == True
        assert mySet1.has(Math.sqrt(25)) == True
        assert mySet1.has(String("Some Text").toLowerCase()) == True
        assert mySet1.has(o) == True

        mySet1.delete(5)
        assert mySet1.has(5) == False
        assert mySet1.size == 4

        nan = float("nan")
        mySet1.add(nan).add(float("nan"))
        assert mySet1.size == 5
        assert mySet1.has(nan) == True
        mySet1.add(True)
        assert mySet1.has(True) == True
        assert mySet1.size == 6

        visited = []
        mySet1.forEach(lambda value, key, owner: visited.append((value, key, owner)))
        self.assertEqual([item[0] for item in visited], list(mySet1.values()))
        self.assertTrue(all(value is key for value, key, owner in visited))
        self.assertTrue(all(owner is mySet1 for value, key, owner in visited))

        constructed = Set(["first", "second", "first"])
        self.assertEqual(list(constructed.keys()), ["first", "second"])
        self.assertEqual(
            list(constructed.entries()), [["first", "first"], ["second", "second"]]
        )
        constructed.remove("first")
        self.assertEqual(list(constructed.values()), ["second"])
        with self.assertRaises(KeyError):
            constructed.remove("missing")

    def test_setTimeout(self):
        """Test the Global.setTimeout function calls the callback."""

        callback = Mock()

        args = ("hello", "world")
        kwargs = {"foo": "bar"}

        timer_id = Global.setTimeout(callback, 1000, *args, **kwargs)
        callback.assert_not_called()

        assert timer_id in Global._Global__timers

        time.sleep(1.5)

        callback.assert_called_once()
        callback.assert_called_with(*args, **kwargs)

    def test_clearTimeout(self):
        """Test that Global.clearTimeout function can cancel a timeout."""

        callback = Mock()

        args = ("hello", "world")
        kwargs = {"foo": "bar"}

        timer_id = Global.setTimeout(callback, 1000, *args, **kwargs)
        callback.assert_not_called()

        assert timer_id in Global._Global__timers
        Global.clearTimeout(timer_id)
        assert timer_id not in Global._Global__timers

        time.sleep(1.5)
        callback.assert_not_called()

    def test_timeouts(self):
        callback = Mock()
        someID = Global.setTimeout(callback, 50)
        Global.clearTimeout(someID)
        time.sleep(0.1)
        callback.assert_not_called()

        # from domonic.javascript import setTimeout, clearTimeout
        # setTimeout(somefunc, 2000)
        # time.sleep(2.5)

        # from domonic.javascript import setInterval, clearInterval
        # def somefunc2():
        # print("testing interval")
        # interval_id = setInterval(somefunc2, 2000)
        # time.sleep(10)
        # clearInterval(interval_id)
        # time.sleep(4)
        # print('end')

        # from domonic.javascript import window
        # intID = window.setInterval(somefunc2, 2000)
        # time.sleep(10)
        # clearInterval(intID)  # not clearing brings it back to life!

    def test_TypedArrays(self):
        # typed arrays
        # https://developer.mozilla.org/en-US/docs/Web/JavaScript/Typed_arrays
        # https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray
        # https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/ArrayBuffer
        # https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/DataView
        # https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Int8Array

        b = ArrayBuffer(8)
        # print(b.byteLength)
        assert b.byteLength == 8

        # var buffer = new ArrayBuffer(8);
        view = Int8Array(b)
        self.assertEqual(view.byteLength, 8)

        # From a length
        int8 = Int8Array(2)
        # print(int8[0])
        # print(Int8Array(2)[0])
        # print(Int8Array(25)[0])
        # print(Int8Array(12)[0])
        int8[0] = 42
        assert int8[0] == 42
        # print(int8.length)  # 2
        assert int8.length == 2
        # print(int8.BYTES_PER_ELEMENT)  # 1
        assert int8.BYTES_PER_ELEMENT == 1

        # From an array
        arr = Int8Array([21, 31])
        # print(arr[1])  # 31
        assert arr[1] == 31

        # From another TypedArray
        x = Int8Array([21, 31])
        y = Int8Array(x)
        # print(y[0])  # 21
        assert y[0] == 21

        # From an ArrayBuffer
        b = ArrayBuffer(8)
        z = Int8Array(b, 1, 4)
        # print(z[0])  # 0
        assert z[0] == 0
        assert z[1] == 0
        assert z[2] == 0
        assert z[3] == 0
        assert z.length == 4
        with self.assertRaises(Exception):
            Int8Array(ArrayBuffer(2), 3)

        # test Int8Array in various ways

        # From a length
        int8 = Int8Array(2)
        # print(int8[0])
        # print(Int8Array(2)[0])
        # print(Int8Array(25)[0])

        # From an array
        arr = Int8Array([21, 31])
        # print(arr[1])  # 31
        assert arr[1] == 31

        # From another TypedArray
        x = Int8Array([21, 31])
        y = Int8Array(x)
        # print(y[0])  # 21
        assert y[0] == 21

    def test_javascript_date_utc_accessors(self):
        date = Date("2020-01-02 03:04:05.006")
        self.assertEqual(date.getUTCDate(), 2)
        self.assertEqual(date.getUTCDay(), 4)
        self.assertEqual(date.getUTCFullYear(), 2020)
        self.assertEqual(date.getUTCHours(), 3)
        self.assertEqual(date.getUTCMinutes(), 4)
        self.assertEqual(date.getUTCSeconds(), 5)
        self.assertEqual(date.getUTCMonth(), 0)

        # From an ArrayBuffer
        # b = ArrayBuffer(8)
        # z = Int8Array(b, 1, 4)

        # print(z[0])  # 31
        # assert z[0] == 31

        # From a DataView
        # d = DataView(b, 1, 4)
        # print(d.getInt8(0))  # 31
        # assert d.getInt8(0) == 31

        # var size = 1000000;
        # var buffer = new ArrayBuffer(4 * size);
        # var intArray = new Int32Array(buffer);
        # var array = new Array(size);
        # // Ensure all values are 0 in the array.
        # for (var i = 0; i < size; i++) {
        #     array[i] = 0;
        # }

        size = 1000000
        # size = 10
        buf = ArrayBuffer(4 * size)
        intArray = Int32Array(buf)
        array = [0] * size
        for i in range(size):
            array[i] = 0

        # assert various features of the array
        # print(intArray.length)  # 1000000
        # assert intArray.length == 1000000
        # print(intArray.BYTES_PER_ELEMENT)  # 4
        assert intArray.BYTES_PER_ELEMENT == 4
        # print(intArray.byteLength)  # 4000000
        assert intArray.byteLength == 4000000
        # print(intArray.byteOffset)  # 0
        assert intArray.byteOffset == 0

        size = 100
        intArray = Int8Array(4 * size)
        array = [0] * size

        # var x1 = performance.now();
        x1 = time.time()

        # // Version 1: modify values in Int32Array.
        # for (var i = 0; i < 1000; i++) {
        #     for (var z = 0; z < size; z++) {
        #         intArray[z] = intArray[z] + 2;
        #     }
        # }
        for i in range(100):
            for z in range(size):
                intArray[z] = intArray[z] + 2

        # var x2 = performance.now();
        x2 = time.time()

        # // Version 2: modify values in Array.
        # for (var i = 0; i < 1000; i++) {
        #     for (var z = 0; z < size; z++) {
        #         array[z] = array[z] + 2;
        #     }
        # }
        for i in range(100):
            for z in range(size):
                array[z] = array[z] + 2

        # var x3 = performance.now();
        x3 = time.time()
        self.assertGreaterEqual(x2 - x1, 0)
        self.assertGreaterEqual(x3 - x2, 0)

        # test uint8array in various ways
        arr = Uint8Array()
        assert arr.length == 0

        arr = Uint8Array(2)
        assert arr.length == 2

        # test uint8array in various ways
        arr = Uint8ClampedArray()
        assert arr.length == 0

        arr = Uint8ClampedArray(2)
        assert arr.length == 2

        # test uint8array in various ways
        arr = Int16Array()
        assert arr.length == 0

        arr = Int16Array(2)
        assert arr.length == 2

        # test uint8array in various ways
        arr = Uint16Array()
        assert arr.length == 0

        arr = Uint16Array(2)
        assert arr.length == 2

        # test uint8array in various ways
        arr = Int32Array()
        assert arr.length == 0

        arr = Int32Array(2)
        assert arr.length == 2

        # test uint8array in various ways
        arr = Uint32Array()
        assert arr.length == 0

        arr = Uint32Array(2)
        assert arr.length == 2

        # test uint8array in various ways
        arr = Float32Array()
        assert arr.length == 0

        arr = Float32Array(2)
        assert arr.length == 2

        # test uint8array in various ways
        arr = Float64Array()
        assert arr.length == 0

        arr = Float64Array(2)
        assert arr.length == 2

    def test_javascript_math_bit_helpers(self):
        self.assertAlmostEqual(Math.fround(1.337), 1.3370000123977661)
        self.assertEqual(Math.clz32(1), 31)
        self.assertEqual(Math.clz32(1000), 22)
        self.assertEqual(Math.clz32(0), 32)

    def test_arraybuffer_and_dataview(self):
        buffer = ArrayBuffer(16)
        self.assertEqual(buffer.byteLength, 16)
        self.assertEqual(list(buffer.slice(0, 4)), [0, 0, 0, 0])

        buffer.setUint8(0, 255)
        buffer.setInt8(1, -1)
        buffer.setUint16(2, 0x1234)
        buffer.setUint16(4, 0x1234, True)
        buffer.setInt16(6, -2)
        buffer.setUint32(8, 0x12345678)
        self.assertEqual(buffer.getUint8(0), 255)
        self.assertEqual(buffer.getInt8(1), -1)
        self.assertEqual(buffer.getUint16(2), 0x1234)
        self.assertEqual(buffer.getUint16(4, True), 0x1234)
        self.assertEqual(buffer.getInt16(6), -2)
        self.assertEqual(buffer.getUint32(8), 0x12345678)

        view = DataView(buffer, 2, 8)
        self.assertEqual(view.byteLength, 8)
        self.assertEqual(view.getUint16(0), 0x1234)
        self.assertEqual(view.getUint16(2, True), 0x1234)
        view.setInt16(4, -7)
        self.assertEqual(buffer.getInt16(6), -7)
        view.setUint32(0, 0x01020304, True)
        self.assertEqual(buffer.getUint32(2, True), 0x01020304)
        view.setFloat32(0, 1.5)
        self.assertAlmostEqual(view.getFloat32(0), 1.5, places=6)

    def test_typedarray_set_and_subarray(self):
        target = Int8Array(4)
        target.set([1, 2, 3], 1)
        self.assertEqual([target[i] for i in range(target.length)], [0, 1, 2, 3])

        source = Int8Array([5, 6])
        target.set(source, 0)
        self.assertEqual([target[i] for i in range(target.length)], [5, 6, 2, 3])

        sub = target.subarray(1, 3)
        self.assertIsInstance(sub, Int8Array)
        self.assertEqual(sub.length, 2)
        self.assertEqual([sub[i] for i in range(sub.length)], [6, 2])

        clamped = Uint8ClampedArray([300, -5, 128])
        self.assertEqual([clamped[i] for i in range(clamped.length)], [255, 0, 128])

        float32 = Float32Array([1.5, 2.25])
        self.assertAlmostEqual(float32[0], 1.5, places=6)
        self.assertAlmostEqual(float32[1], 2.25, places=6)

        float64 = Float64Array([3.5])
        self.assertEqual(float64[0], 3.5)

    def test_typedarray_error_paths_and_helpers(self):
        self.assertEqual(Int8Array.of(1, 2)[0], 1)
        self.assertEqual(Int8Array.from_([3, 4])[1], 4)
        self.assertEqual(Int8Array(2).args.byteLength, 2)
        self.assertIs(Int8Array(2).get(5), undefined)

        with self.assertRaises(Exception):
            Int16Array(ArrayBuffer(3), 1)
        with self.assertRaises(Exception):
            Int16Array(ArrayBuffer(3))
        with self.assertRaises(Exception):
            Int16Array(ArrayBuffer(2), 2, 1)
        with self.assertRaises(Exception):
            Int8Array(-1)
        with self.assertRaises(TypeError):
            Int8Array("bad")
        with self.assertRaises(SyntaxError):
            Int8Array(2).__getitem__(None)
        with self.assertRaises(SyntaxError):
            Int8Array(2).__setitem__(None, None)
        with self.assertRaises(TypeError):
            Int8Array(2).set("bad", 0)
        with self.assertRaises(Exception):
            Int8Array(2).set([1, 2, 3], 0)

        base = Int8Array([1, 2, 3, 4])
        self.assertEqual([base.subarray(-3, -1)[i] for i in range(2)], [2, 3])

    def test_reflect(self):
        target = {"name": "John"}
        self.assertEqual(list(Reflect.ownKeys(target)), ["name"])
        self.assertEqual(
            Reflect.apply(lambda left, right: left + right, None, [2, 3]), 5
        )
        self.assertEqual(
            Reflect.construct(dict, [[("name", "John")]]), {"name": "John"}
        )
        self.assertTrue(Reflect.defineProperty(target, "age", {"value": 30}))
        self.assertEqual(Reflect.get(target, "age", None), 30)
        self.assertTrue(Reflect.has(target, "age"))
        self.assertEqual(
            Reflect.getOwnPropertyDescriptor(target, "age"),
            {"value": 30, "writable": True, "enumerable": True, "configurable": True},
        )
        self.assertTrue(Reflect.set(target, "age", 31, None))
        self.assertEqual(target["age"], 31)
        self.assertTrue(Reflect.deleteProperty(target, "age"))
        self.assertFalse(Reflect.has(target, "age"))

        obj = Object({"name": "Jane"})
        self.assertTrue(Reflect.setPrototypeOf(obj, Object))
        self.assertEqual(Reflect.getPrototypeOf(obj), Object)
        self.assertTrue(Reflect.preventExtensions(obj))
        self.assertFalse(Object.isExtensible(obj))
        self.assertFalse(Object.isFrozen(obj))

    def test_symbol(self):
        symbol = Symbol("token")
        same_symbol = Symbol("token")
        other_symbol = Symbol("other")
        self.assertTrue(symbol.hasInstance(same_symbol))
        self.assertFalse(symbol.hasInstance(other_symbol))
        self.assertFalse(symbol.isConcatSpreadable())
        self.assertEqual(list(symbol.iterator([1, 2])), [1, 2])
        self.assertEqual(list(symbol.asyncIterator([3, 4])), [3, 4])
        self.assertTrue(symbol.match("auth token present"))
        self.assertEqual(symbol.search("auth token present"), 5)
        self.assertEqual(symbol.split("pretokenpost"), ["pre", "post"])
        self.assertIs(symbol.species(), Symbol)
        self.assertEqual(symbol.toPrimitive(), "token")
        self.assertEqual(symbol.toStringTag(), "Symbol")
        self.assertEqual(symbol.unscopables(), {})
        self.assertEqual(symbol.toString(), "Symbol(token)")
        self.assertEqual(symbol.toSource(), "Symbol(token)")
        self.assertEqual(symbol.valueOf(), "token")

    # def test_storage(self):
    #     print("test_storage")

    #     myObj = Storage()
    #     myObj.name = 'John'
    #     myObj.age = 30
    #     myObj.address = '123 Main St'

    #     assert myObj.name == 'John'
    #     assert myObj.age == 30
    #     assert myObj.address == '123 Main St'

    #     window.localStorage.setItem('myObj', myObj)
    #     window.localStorage.getItem('myObj')
    #     myObj2 = window.localStorage.getItem('myObj')
    #     assert myObj2.name == 'John'
    #     assert myObj2.age == 30

    # def test_reflect(self):
    #     print("test_reflect")
    #     myObj = {'name': 'John', 'age': 30, 'address': '123 Main St'}

    #     myObj2 = Reflect(myObj)
    #     assert myObj2.name == 'John'
    #     assert myObj2.age == 30
    #     assert myObj2.address == '123 Main St'
    #     assert myObj2.toString() == '{"name": "John", "age": 30, "address": "123 Main St"}'

    # def test_symbol(self):
    #     print("test_symbol")
    #     symbol = Symbol('x')

    #     assert symbol.name == 'x'
    #     assert symbol.value == 0
    #     assert symbol.toString() == 'x'
    #     assert symbol.toNumber() == 0
    #     assert symbol.toString(True) == '0'


_intID = None
_results = []


if __name__ == "__main__":
    unittest.main()
