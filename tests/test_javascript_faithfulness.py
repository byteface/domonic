"""
test_javascript_faithfulness
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Checks that ``domonic.javascript`` produces the same results a browser / Node
REPL would for the common String / Array / Number / Math / RegExp surface.
Every expected value here is what real JavaScript returns.
"""

import unittest

from domonic.javascript import (
    Array,
    Global,
    Math,
    Number,
    Object,
    RegExp,
    String,
)

S = String
A = Array
N = Number


class StringFaithfulness(unittest.TestCase):
    def test_slice_substring_substr_at(self):
        self.assertEqual(S("hello world").slice(-5), "world")
        self.assertEqual(S("hello").slice(1, 3), "el")
        self.assertEqual(S("hello").substring(3, 1), "el")  # swaps args
        self.assertEqual(S("hello").substr(1, 3), "ell")
        self.assertEqual(S("hello").at(-1), "o")
        self.assertEqual(S("hello").at(0), "h")
        self.assertIsNone(S("hello").at(99))

    def test_char_access(self):
        self.assertEqual(S("abc").charAt(10), "")
        self.assertEqual(S("ABC").charCodeAt(0), 65)
        self.assertEqual(S("abc").charCodeAt(99), "NaN")
        self.assertEqual(S("\U0001F600").codePointAt(0), 128512)

    def test_pad_repeat_trim(self):
        self.assertEqual(S("5").padStart(3, "0"), "005")
        self.assertEqual(S("5").padEnd(3, "0"), "500")
        self.assertEqual(S("ab").repeat(3), "ababab")
        self.assertEqual(S("  hi  ").trim(), "hi")
        self.assertEqual(S("  hi  ").trimStart(), "hi  ")
        self.assertEqual(S("  hi  ").trimEnd(), "  hi")

    def test_search_index_and_positions(self):
        self.assertEqual(S("hello").indexOf("l"), 2)
        self.assertEqual(S("hello").indexOf("z"), -1)
        self.assertEqual(S("hello").lastIndexOf("l"), 3)
        self.assertTrue(S("hello").startsWith("he"))
        self.assertTrue(S("hello").startsWith("llo", 2))
        self.assertTrue(S("hello").endsWith("lo"))
        self.assertTrue(S("hello").endsWith("hell", 4))
        self.assertFalse(S("hello").endsWith("hell"))
        self.assertTrue(S("hello").includes("ell"))

    def test_normalize(self):
        self.assertEqual(len(S("é").normalize("NFD")), 2)
        self.assertEqual(len(S("é").normalize("NFC")), 1)

    def test_split(self):
        self.assertEqual(S("a,b,c,d").split(","), ["a", "b", "c", "d"])
        self.assertEqual(S("abc").split(""), ["a", "b", "c"])
        self.assertEqual(S("a1b2c").split(RegExp(r"\d")), ["a", "b", "c"])
        self.assertEqual(S("a1b2c").split(RegExp(r"(\d)")), ["a", "1", "b", "2", "c"])


class StringRegexFaithfulness(unittest.TestCase):
    def test_replace_specials(self):
        self.assertEqual(S("aaa").replace("a", "b"), "baa")
        self.assertEqual(S("aaa").replaceAll("a", "b"), "bbb")
        self.assertEqual(
            S("a1b2").replace(RegExp(r"\d", "g"), "#"), "a#b#"
        )
        self.assertEqual(
            S("John Smith").replace(RegExp(r"(\w+)\s(\w+)"), "$2, $1"), "Smith, John"
        )
        self.assertEqual(S("abc").replace(RegExp(r"b"), "[$&]"), "a[b]c")
        self.assertEqual(S("abcdef").replace(RegExp("cd"), "[$`]"), "ab[ab]ef")
        self.assertEqual(S("abcdef").replace(RegExp("cd"), "[$']"), "ab[ef]ef")
        self.assertEqual(S("a").replace(RegExp("a"), "$$"), "$")
        self.assertEqual(
            S("2024").replace(RegExp(r"(?<y>\d{4})"), "[$<y>]"), "[2024]"
        )

    def test_replace_callback(self):
        self.assertEqual(
            S("a1b2").replace(RegExp(r"\d", "g"), lambda m, *a: f"<{m}>"), "a<1>b<2>"
        )

    def test_replace_thousands_separator(self):
        self.assertEqual(
            S("1234567").replace(RegExp(r"\B(?=(\d{3})+(?!\d))", "g"), ","),
            "1,234,567",
        )

    def test_match_without_g(self):
        m = S("xx2024-01").match(RegExp(r"(\d+)-(\d+)"))
        self.assertEqual(list(m), ["2024-01", "2024", "01"])
        self.assertEqual(m.index, 2)
        self.assertEqual(m.input, "xx2024-01")
        self.assertIsNone(S("abc").match(RegExp(r"\d")))

    def test_match_with_g(self):
        self.assertEqual(S("a1b2c3").match(RegExp(r"\d", "g")), ["1", "2", "3"])
        self.assertIsNone(S("abc").match(RegExp(r"\d", "g")))

    def test_matchAll(self):
        out = [(m[0], m[1]) for m in S("a1b2").matchAll(RegExp(r"(\w)(\d)", "g"))]
        self.assertEqual(out, [("a1", "a"), ("b2", "b")])

    def test_search(self):
        self.assertEqual(S("hello").search(RegExp(r"l")), 2)
        self.assertEqual(S("hello").search(RegExp(r"z")), -1)
        self.assertEqual(S("a.b").search("."), 0)  # not escaped, like JS

    def test_unicode_property_escapes(self):
        self.assertEqual(S("a,b.c!").replace(RegExp(r"\p{P}", "gu"), ""), "abc")
        self.assertEqual(S("a1b2").replace(RegExp(r"\p{N}", "gu"), ""), "ab")
        self.assertEqual(
            S("aAbB").replace(RegExp(r"\p{Uppercase_Letter}", "gu"), ""), "ab"
        )
        self.assertTrue(RegExp(r"\p{Greek}", "u").test("α"))
        self.assertTrue(RegExp(r"\p{Script=Han}", "u").test("汉"))


class RegExpFaithfulness(unittest.TestCase):
    def test_exec_shape(self):
        m = RegExp(r"(\d)(\d)").exec("ab12")
        self.assertEqual(list(m), ["12", "1", "2"])
        self.assertEqual(m.index, 2)
        self.assertIsNone(RegExp(r"z").exec("abc"))

    def test_global_exec_advances_lastindex(self):
        r = RegExp(r"\d+", "g")
        self.assertEqual(r.exec("a12b345")[0], "12")
        self.assertEqual(r.exec("a12b345")[0], "345")
        self.assertIsNone(r.exec("a12b345"))

    def test_sticky(self):
        r = RegExp(r"a", "y")
        r.lastIndex = 2
        self.assertIsNone(r.exec("aabaa"))
        r.lastIndex = 1
        self.assertIsNotNone(r.exec("aabaa"))

    def test_flags_canonical_order(self):
        self.assertEqual(RegExp("x", "yig").flags, "giy")
        self.assertEqual(RegExp("x", "sm").flags, "ms")

    def test_tostring(self):
        self.assertEqual(RegExp(r"\d+", "g").toString(), "/\\d+/g")
        self.assertEqual(RegExp("", "").toString(), "/(?:)/")

    def test_named_groups(self):
        m = RegExp(r"(?<year>\d{4})-(?<month>\d{2})").exec("2026-09")
        self.assertEqual(m.groups, {"year": "2026", "month": "09"})

    def test_test_shares_lastindex(self):
        r = RegExp(r"\d", "g")
        self.assertTrue(r.test("a1a1"))
        self.assertEqual(r.lastIndex, 2)


class ArrayFaithfulness(unittest.TestCase):
    def test_mutators_return_values(self):
        self.assertEqual(A(1, 2).push(3), 3)
        self.assertEqual(A(1, 2, 3).pop(), 3)
        self.assertEqual(A(1, 2, 3).shift(), 1)
        self.assertEqual(A(2, 3).unshift(1), 3)

    def test_slice_and_splice(self):
        self.assertEqual(A(1, 2, 3, 4).slice(1, 3), [2, 3])
        self.assertEqual(A(1, 2, 3, 4).slice(-2), [3, 4])
        self.assertEqual(A(1, 2, 3, 4).splice(1, 2), [2, 3])

    def test_iteration_helpers(self):
        self.assertEqual(A(1, 2, 3).map(lambda x, *a: x * 2), [2, 4, 6])
        self.assertEqual(A(1, 2, 3, 4).filter(lambda x, *a: x % 2 == 0), [2, 4])
        self.assertEqual(A(1, 2, 3, 4).reduce(lambda acc, x, *a: acc + x, 0), 10)
        self.assertEqual(A(1, 2, 3, 4).reduce(lambda acc, x, *a: acc + x), 10)
        self.assertEqual(
            A("a", "b", "c").reduceRight(lambda acc, x, *a: acc + x, ""), "cba"
        )
        self.assertEqual(A(1, 2, 3, 4).find(lambda x, *a: x > 2), 3)
        self.assertEqual(A(1, 2, 3, 4).findLast(lambda x, *a: x < 4), 3)
        self.assertTrue(A(1, 2, 3).some(lambda x, *a: x > 2))
        self.assertTrue(A(2, 4).every(lambda x, *a: x % 2 == 0))

    def test_flat_and_fill(self):
        self.assertEqual(A(1, [2, [3]]).flat(), [1, 2, [3]])
        self.assertEqual(A(1, [2, [3]]).flat(2), [1, 2, 3])
        self.assertEqual(A(1, 2).flatMap(lambda x, *a: [x, x * 2]), [1, 2, 2, 4])
        self.assertEqual(A(1, 2, 3).fill(0), [0, 0, 0])
        self.assertEqual(A(1, 2, 3, 4).fill(0, 1, 3), [1, 0, 0, 4])

    def test_copyWithin(self):
        self.assertEqual(A(1, 2, 3, 4, 5).copyWithin(0, 3), [4, 5, 3, 4, 5])
        self.assertEqual(A(1, 2, 3, 4, 5).copyWithin(1, 3), [1, 4, 5, 4, 5])
        self.assertEqual(A(1, 2, 3, 4, 5).copyWithin(-2), [1, 2, 3, 1, 2])

    def test_sort(self):
        self.assertEqual(A(10, 1, 2, 20).sort(), [1, 10, 2, 20])  # lexicographic
        self.assertEqual(
            A(10, 1, 2, 20).sort(lambda a, b: a - b), [1, 2, 10, 20]
        )

    def test_immutable_es2023(self):
        original = A(3, 1, 2)
        self.assertEqual(list(original.toSorted(lambda a, b: a - b)), [1, 2, 3])
        self.assertEqual(list(original), [3, 1, 2])  # untouched
        self.assertEqual(list(A(1, 2, 3).toReversed()), [3, 2, 1])
        self.assertEqual(list(A(1, 2, 3).with_(1, 9)), [1, 9, 3])
        self.assertEqual(list(A(1, 2, 3, 4).toSpliced(1, 2, 9)), [1, 9, 4])

    def test_static(self):
        self.assertTrue(A.isArray([1, 2]))
        self.assertFalse(A.isArray("x"))
        self.assertEqual(list(A.from_("abc")), ["a", "b", "c"])
        self.assertEqual(list(A.of(1, 2, 3)), [1, 2, 3])


class NumberMathFaithfulness(unittest.TestCase):
    def test_tofixed(self):
        self.assertEqual(N(3.14159).toFixed(2), "3.14")
        self.assertEqual(N(2.5).toFixed(0), "3")
        self.assertEqual(N(-2.5).toFixed(0), "-2")
        self.assertEqual(N(1.005).toFixed(2), "1.00")
        self.assertEqual(N(1).toFixed(3), "1.000")

    def test_toprecision_toexponential(self):
        self.assertEqual(N(123.456).toPrecision(4), "123.5")
        self.assertEqual(N(12345).toExponential(2), "1.23e+4")

    def test_tostring_radix(self):
        self.assertEqual(N(255).toString(16), "ff")
        self.assertEqual(N(10).toString(2), "1010")
        self.assertEqual(N(-10).toString(2), "-1010")
        n = N(10)
        n.toString(2)
        self.assertEqual(n.x, 10)  # not mutated

    def test_number_statics(self):
        self.assertTrue(Number.isInteger(5))
        self.assertFalse(Number.isInteger(5.5))
        self.assertFalse(Number.isInteger("5"))
        self.assertTrue(Number.isFinite(5))
        self.assertFalse(Number.isFinite("5"))
        self.assertTrue(Number.isNaN(float("nan")))
        self.assertFalse(Number.isNaN("nan"))
        self.assertEqual(Number.MAX_SAFE_INTEGER, 2**53 - 1)
        self.assertEqual(Number.parseInt("42px"), 42)
        self.assertEqual(Number.parseFloat("3.14abc"), 3.14)

    def test_parsers(self):
        self.assertEqual(Global.parseInt("ff", 16), 255)
        self.assertEqual(Global.parseInt("0xFF"), 255)
        self.assertEqual(Global.parseFloat("3.14abc"), 3.14)
        self.assertTrue(Global.isNaN("abc"))
        self.assertFalse(Global.isNaN("123"))

    def test_math_rounding(self):
        self.assertEqual(Math.round(2.5), 3)
        self.assertEqual(Math.round(-2.5), -2)
        self.assertEqual(Math.round(2.4), 2)
        self.assertEqual(Math.floor(2.9), 2)
        self.assertEqual(Math.ceil(2.1), 3)
        self.assertEqual(Math.trunc(-4.7), -4)

    def test_math_additions(self):
        self.assertEqual(Math.sign(-5), -1)
        self.assertEqual(Math.sign(3), 1)
        self.assertEqual(Math.hypot(3, 4), 5.0)
        self.assertEqual(Math.cbrt(27), 3.0)
        self.assertEqual(Math.log2(8), 3.0)
        self.assertEqual(Math.imul(3, 4), 12)
        self.assertAlmostEqual(Math.expm1(0), 0.0)


class ObjectFaithfulness(unittest.TestCase):
    def test_keys_values_entries(self):
        self.assertEqual(Object.keys({"a": 1, "b": 2}), ["a", "b"])
        self.assertEqual(Object.values({"a": 1, "b": 2}), [1, 2])
        self.assertEqual(Object.entries({"a": 1}), [["a", 1]])

    def test_assign_and_fromentries(self):
        self.assertEqual(Object.assign({"a": 1}, {"b": 2}), {"a": 1, "b": 2})
        self.assertEqual(
            Object.fromEntries([["a", 1], ["b", 2]]), {"a": 1, "b": 2}
        )

    def test_is_and_hasown(self):
        self.assertTrue(Object.is_(float("nan"), float("nan")))
        self.assertFalse(Object.is_(0.0, -0.0))
        self.assertTrue(Object.is_("a", "a"))
        self.assertTrue(Object.hasOwn({"a": 1}, "a"))
        self.assertFalse(Object.hasOwn({"a": 1}, "b"))
        # the real JS names are reachable by getattr
        self.assertIs(getattr(Object, "is"), Object.is_)

    def test_groupBy(self):
        grouped = Object.groupBy([1, 2, 3, 4], lambda n, i: "even" if n % 2 == 0 else "odd")
        self.assertEqual(grouped, {"odd": [1, 3], "even": [2, 4]})


class CoercionFaithfulness(unittest.TestCase):
    def test_string_coercion(self):
        self.assertEqual(Global.String(None), "null")
        self.assertEqual(Global.String(True), "true")
        self.assertEqual(Global.String(False), "false")
        self.assertEqual(Global.String([1, 2, 3]), "1,2,3")
        self.assertEqual(Global.String([1, None, 3]), "1,,3")
        self.assertEqual(Global.String({"a": 1}), "[object Object]")
        self.assertEqual(Global.String(3.0), "3")
        self.assertEqual(Global.String(float("nan")), "NaN")
        self.assertEqual(Global.String(float("inf")), "Infinity")

    def test_number_coercion(self):
        self.assertEqual(Global.Number(""), 0)
        self.assertEqual(Global.Number("  12  "), 12)
        self.assertEqual(Global.Number("0x1F"), 31)
        self.assertEqual(Global.Number(True), 1)
        self.assertEqual(Global.Number([5]), 5)
        self.assertEqual(Global.Number([]), 0)
        self.assertEqual(str(Global.Number(None)), "NaN")

    def test_parseint_edges(self):
        self.assertEqual(Global.parseInt("  42  "), 42)
        self.assertEqual(Global.parseInt("3.9"), 3)
        self.assertEqual(Global.parseInt("-0x10"), -16)
        self.assertEqual(Global.parseInt("z", 36), 35)
        self.assertEqual(Global.parseInt("12abc"), 12)
        self.assertEqual(str(Global.parseInt("abc")), "NaN")

    def test_parsefloat_edges(self):
        self.assertEqual(Global.parseFloat("3.14.15"), 3.14)
        self.assertEqual(Global.parseFloat("  .5"), 0.5)
        self.assertEqual(Global.parseFloat("1e3"), 1000.0)
        self.assertEqual(Global.parseFloat("Infinity"), float("inf"))


class DateFaithfulness(unittest.TestCase):
    def test_component_constructor_is_zero_indexed_month(self):
        from domonic.javascript import Date

        d = Date(2026, 0, 15)
        self.assertEqual(d.getFullYear(), 2026)
        self.assertEqual(d.getMonth(), 0)
        self.assertEqual(d.getDate(), 15)

    def test_component_constructor_overflows(self):
        from domonic.javascript import Date

        d = Date(2026, 13, 1)  # month 13 -> Feb 2027
        self.assertEqual(d.getFullYear(), 2027)
        self.assertEqual(d.getMonth(), 1)


class BooleanFaithfulness(unittest.TestCase):
    def test_truthiness(self):
        self.assertFalse(Global.Boolean(""))
        self.assertFalse(Global.Boolean(0))
        self.assertTrue(Global.Boolean("false"))
        self.assertTrue(Global.Boolean("0"))
        self.assertTrue(Global.Boolean([]))  # JS: [] is truthy


class JSONFaithfulness(unittest.TestCase):
    def test_roundtrip(self):
        from domonic.javascript import JSON

        self.assertEqual(JSON.parse('{"a": 1}'), {"a": 1})
        self.assertIn('"a"', JSON.stringify({"a": 1}))


if __name__ == "__main__":
    unittest.main()
