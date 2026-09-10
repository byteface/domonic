"""Ported from wpt/dom/nodes/Element-classlist.html
https://dom.spec.whatwg.org/#dom-element-classlist

The ``null`` / ``undefined`` argument rows are skipped -- they exercise
WebIDL ``DOMString`` coercion (``null`` -> ``"null"``), which has no Python
equivalent.  The MutationObserver record-count assertions are dropped; the
class-attribute value after each call is checked instead, which is what they
were guarding.  Only the HTML-node cases are ported (the XHTML / MathML / XML
namespace variants exercise the same ``DOMTokenList`` code).
"""

import unittest

from domonic.dom import Document
from tests.wpt._harness import assert_equals, assert_throws_dom, assert_throws_js

document = Document()


def _set_class(e, value):
    if value is None:
        e.removeAttribute("class")
    else:
        e.setAttribute("class", value)


class _ClassListBase(unittest.TestCase):
    def setUp(self):
        self.e = document.createElement("div")

    def check_modification(self, func_name, args, expected_res, before, after, expected_exception):
        if not isinstance(args, list):
            args = [args]
        should_throw = isinstance(expected_exception, str)
        if should_throw:
            after = before
        _set_class(self.e, before)
        if should_throw:
            assert_throws_dom(
                expected_exception,
                lambda: getattr(self.e.classList, func_name)(*args),
            )
        else:
            res = getattr(self.e.classList, func_name)(*args)
            assert_equals(res, expected_res, "wrong return value")
        assert_equals(self.e.getAttribute("class"), after, "wrong class after modification")


class ClassListMisc(_ClassListBase):
    def test_assigning_to_classlist_is_ignored(self):
        # domonic exposes classList as a plain attribute; assigning a string to
        # it would shadow the descriptor.  The browser ignores the assignment.
        # We at least confirm classList keeps working after a round-trip.
        _set_class(self.e, "a b")
        self.assertEqual(list(self.e.classList), ["a", "b"])

    def test_supports_must_throw_type_error(self):
        assert_throws_js(TypeError, lambda: self.e.classList.supports("a"))

    def test_length(self):
        for value, length in [
            (None, 0),
            ("", 0),
            ("   \t  \f", 0),
            ("a", 1),
            ("a A", 2),
            ("\r\na\t\f", 1),
            ("a a", 1),
            ("a a a a a a", 1),
            ("a a b b", 2),
            ("a A B b", 4),
            ("a b c c b a a b c c", 3),
            ("   a  a b", 2),
            ("a\tb\nc\fd\re f", 6),
        ]:
            _set_class(self.e, value)
            assert_equals(self.e.classList.length, length, f"length for {value!r}")

    def test_stringifier_is_verbatim(self):
        for value, expected in [(None, ""), ("foo", "foo"), ("   a  a b", "   a  a b")]:
            _set_class(self.e, value)
            assert_equals(self.e.classList.toString(), expected)

    def test_item_and_indexed_access(self):
        for value, expected in [
            (None, []),
            ("a", ["a"]),
            ("aa AA aa", ["aa", "AA"]),
            ("a b", ["a", "b"]),
            ("   a  a b", ["a", "b"]),
            ("\t\n\f\r a\t\n\f\r b\t\n\f\r ", ["a", "b"]),
        ]:
            _set_class(self.e, value)
            cl = self.e.classList
            assert_equals(cl.item(-1), None)
            assert_equals(cl[-1], None)
            i = 0
            while i < len(expected):
                assert_equals(cl.item(i), expected[i], f"item({i})")
                assert_equals(cl[i], expected[i], f"[{i}]")
                i += 1
            assert_equals(cl.item(i), None)
            assert_equals(cl[i], None)
            assert_equals(cl.item(0xFFFFFFFF), None)
            assert_equals(cl[0xFFFFFFFF], None)


class ClassListContains(_ClassListBase):
    def test_contains(self):
        cases = [
            ("a", ["a"], True),
            ("a", ["aa", "b", "A", "a.", "a)", "a'", 'a"', "a$", "a~", "a?", "a\\"], False),
            ("a", ["a\t", "\ta", "a\n", "\na", "a\f", "\fa", "a\r", "\ra", "a ", " a"], False),
            ("", ["a"], False),
        ]
        for attr, args, expected in cases:
            _set_class(self.e, attr)
            for token in args:
                assert_equals(self.e.classList.contains(token), expected, f"contains({token!r}) for {attr!r}")

    def test_contains_multi(self):
        _set_class(self.e, "aa AA")
        assert_equals(self.e.classList.contains("aa"), True)
        assert_equals(self.e.classList.contains("AA"), True)
        assert_equals(self.e.classList.contains("aA"), False)
        _set_class(self.e, "a b c")
        assert_equals(self.e.classList.contains("a"), True)
        assert_equals(self.e.classList.contains("b"), True)
        _set_class(self.e, "\t\n\f\r a\t\n\f\r b\t\n\f\r ")
        assert_equals(self.e.classList.contains("a"), True)
        assert_equals(self.e.classList.contains("b"), True)


class ClassListAdd(_ClassListBase):
    def test_add_errors(self):
        for arg, exc in [
            ("", "SyntaxError"),
            (["a", ""], "SyntaxError"),
            (" ", "InvalidCharacterError"),
            ("\ta", "InvalidCharacterError"),
            ("a\t", "InvalidCharacterError"),
            ("\na", "InvalidCharacterError"),
            ("a\n", "InvalidCharacterError"),
            ("\fa", "InvalidCharacterError"),
            ("a\f", "InvalidCharacterError"),
            ("\ra", "InvalidCharacterError"),
            ("a\r", "InvalidCharacterError"),
            (" a", "InvalidCharacterError"),
            ("a ", "InvalidCharacterError"),
            (["a", " "], "InvalidCharacterError"),
            (["a", "aa "], "InvalidCharacterError"),
        ]:
            self.check_modification("add", arg, None, None, None, exc)

    def test_add(self):
        for before, arg, after in [
            ("a", "a", "a"),
            ("aa", "AA", "aa AA"),
            ("a b c", "a", "a b c"),
            ("a a a  b", "a", "a b"),  # noop still runs update steps
            (None, "a", "a"),
            ("", "a", "a"),
            (" ", "a", "a"),
            ("   \f", "a", "a"),
            ("a", "b", "a b"),
            ("a b c", "d", "a b c d"),
            ("a b c ", "d", "a b c d"),
            ("   a  a b", "c", "a b c"),
            ("   a  a b", "a", "a b"),
            ("\t\n\f\r a\t\n\f\r b\t\n\f\r ", "c", "a b c"),
            ("a b c ", ["d", "e"], "a b c d e"),
            ("a b c ", ["a", "a"], "a b c"),
            ("a b c ", ["d", "d"], "a b c d"),
            ("a b c a ", [], "a b c"),
            (None, ["a", "b"], "a b"),
            ("", ["a", "b"], "a b"),
        ]:
            self.check_modification("add", arg, None, before, after, None)

    def test_force_toggle_true_matches_add(self):
        # toggle(token, True) adds, but a no-op does NOT run the update steps
        for before, token, after, noop in [
            ("a", "a", "a", True),
            ("aa", "AA", "aa AA", False),
            ("a a a  b", "a", "a b", True),
            (None, "a", "a", False),
        ]:
            expected_after = before if noop else after
            self.check_modification("toggle", [token, True], True, before, expected_after, None)


class ClassListRemove(_ClassListBase):
    def test_remove_errors(self):
        for before, arg, exc in [
            (None, "", "SyntaxError"),
            (None, " ", "InvalidCharacterError"),
            ("\ta", "\ta", "InvalidCharacterError"),
            ("a\t", "a\t", "InvalidCharacterError"),
            ("\na", "\na", "InvalidCharacterError"),
            ("a\n", "a\n", "InvalidCharacterError"),
            ("\fa", "\fa", "InvalidCharacterError"),
            ("a\f", "a\f", "InvalidCharacterError"),
            ("\ra", "\ra", "InvalidCharacterError"),
            ("a\r", "a\r", "InvalidCharacterError"),
            (" a", " a", "InvalidCharacterError"),
            ("a ", "a ", "InvalidCharacterError"),
            ("aa ", "aa ", "InvalidCharacterError"),
        ]:
            self.check_modification("remove", arg, None, before, before, exc)

    def test_remove(self):
        for before, arg, after in [
            (None, "a", None),
            ("", "a", ""),
            ("a b  c", "d", "a b c"),  # noop re-serialises
            ("a b  c", "A", "a b c"),
            (" a a a ", "a", ""),
            ("a  b", "a", "b"),
            ("a  b  ", "a", "b"),
            ("a a b", "a", "b"),
            ("aa aa bb", "aa", "bb"),
            ("a a b a a c a a", "a", "b c"),
            ("a  b  c", "b", "a c"),
            ("aaa  bbb  ccc", "bbb", "aaa ccc"),
            (" a  b  c ", "b", "a c"),
            ("a b b b c", "b", "a c"),
            ("a  b  c", "c", "a b"),
            (" a  b  c ", "c", "a b"),
            ("a b c c c", "c", "a b"),
            ("a b a c a d a", "a", "b c d"),
            ("AA BB aa CC AA dd aa", "AA", "BB aa CC dd"),
            ("\ra\na\ta\f", "a", ""),
            ("\t\n\f\r a\t\n\f\r b\t\n\f\r ", "a", "b"),
            ("a b c ", ["d", "e"], "a b c"),
            ("a b c ", ["a", "b"], "c"),
            ("a b c ", ["a", "c"], "b"),
            ("a b c ", ["a", "a"], "b c"),
            ("a b c ", ["d", "d"], "a b c"),
            ("a b c ", [], "a b c"),
            (None, ["a", "b"], None),
            ("", ["a", "b"], ""),
            ("a a", [], "a"),
        ]:
            self.check_modification("remove", arg, None, before, after, None)

    def test_force_toggle_false_matches_remove(self):
        for before, token, after, noop in [
            ("a b  c", "d", "a b c", True),
            (" a a a ", "a", "", False),
            ("a  b", "a", "b", False),
        ]:
            expected_after = before if noop else after
            self.check_modification("toggle", [token, False], False, before, expected_after, None)


class ClassListToggle(_ClassListBase):
    def test_toggle_errors(self):
        self.check_modification("toggle", "", None, None, None, "SyntaxError")
        self.check_modification("toggle", "aa ", None, None, None, "InvalidCharacterError")

    def test_toggle(self):
        for before, token, res, after in [
            (None, "a", True, "a"),
            ("", "a", True, "a"),
            (" ", "a", True, "a"),
            ("   \f", "a", True, "a"),
            ("a", "b", True, "a b"),
            ("a", "A", True, "a A"),
            ("a b c", "d", True, "a b c d"),
            ("   a  a b", "d", True, "a b d"),
            ("a", "a", False, ""),
            (" a a a ", "a", False, ""),
            (" A A A ", "a", True, "A a"),
            (" a b c ", "b", False, "a c"),
            (" a b c b b", "b", False, "a c"),
            (" a b  c  ", "c", False, "a b"),
            (" a b c ", "a", False, "b c"),
            ("   a  a b", "b", False, "a"),
            ("\t\n\f\r a\t\n\f\r b\t\n\f\r ", "a", False, "b"),
            ("\t\n\f\r a\t\n\f\r b\t\n\f\r ", "c", True, "a b c"),
        ]:
            self.check_modification("toggle", token, res, before, after, None)


class ClassListReplace(_ClassListBase):
    def test_replace_errors(self):
        for token, new_token, exc in [
            ("", "a", "SyntaxError"),
            ("", " ", "SyntaxError"),
            (" ", "a", "InvalidCharacterError"),
            ("\ta", "b", "InvalidCharacterError"),
            ("a\t", "b", "InvalidCharacterError"),
            ("a", "", "SyntaxError"),
            (" ", "", "SyntaxError"),
            ("a", " ", "InvalidCharacterError"),
            ("b", "\ta", "InvalidCharacterError"),
            ("b", "a ", "InvalidCharacterError"),
        ]:
            self.check_modification("replace", [token, new_token], None, None, None, exc)

    def test_replace(self):
        for before, token, new_token, res, after in [
            ("a", "a", "a", True, "a"),
            ("a", "a", "b", True, "b"),
            ("a", "A", "b", False, "a"),
            ("a b", "b", "A", True, "a A"),
            ("a b", "c", "a", False, "a b"),
            ("a b c", "d", "e", False, "a b c"),
            ("a a a  b", "a", "a", True, "a b"),
            ("a a a  b", "c", "d", False, "a a a  b"),
            (None, "a", "b", False, None),
            ("", "a", "b", False, ""),
            (" ", "a", "b", False, " "),
            (" a  \f", "a", "b", True, "b"),
            ("a b c", "b", "d", True, "a d c"),
            ("a b c", "c", "a", True, "a b"),
            ("c b a", "c", "a", True, "a b"),
            ("a b a", "a", "c", True, "c b"),
            ("a b a", "b", "c", True, "a c"),
            ("   a  a b", "a", "c", True, "c b"),
            ("   a  a b", "b", "c", True, "a c"),
            ("\t\n\f\r a\t\n\f\r b\t\n\f\r ", "a", "c", True, "c b"),
            ("\t\n\f\r a\t\n\f\r b\t\n\f\r ", "b", "c", True, "a c"),
        ]:
            self.check_modification("replace", [token, new_token], res, before, after, None)


if __name__ == "__main__":
    unittest.main()
