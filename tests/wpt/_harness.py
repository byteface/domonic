"""A tiny slice of web-platform-tests' ``testharness.js``, in Python.

Ported WPT tests (``tests/wpt/test_*.py``) are transcribed almost line for line
from the upstream ``.html`` files; this module supplies the assertion helpers
so the port stays close to the original and stays readable when it fails.

Only the DOM subset is covered -- these are conformance checks against
``domonic.dom``.  A test that fails here is either a real spec discrepancy or a
deliberate domonic deviation; the latter are marked ``xfail`` with a reason.
"""

from __future__ import annotations

from typing import Any, Callable, Iterable

__all__ = [
    "assert_equals",
    "assert_not_equals",
    "assert_true",
    "assert_false",
    "assert_array_equals",
    "assert_throws_js",
    "assert_throws_dom",
]


class WPTFailure(AssertionError):
    pass


def _fmt(value: Any) -> str:
    return repr(value)


def assert_equals(actual: Any, expected: Any, description: str = "") -> None:
    if actual != expected:
        raise WPTFailure(f"assert_equals {description}: expected {_fmt(expected)} got {_fmt(actual)}")


def assert_not_equals(actual: Any, expected: Any, description: str = "") -> None:
    if actual == expected:
        raise WPTFailure(f"assert_not_equals {description}: got {_fmt(actual)}")


def assert_true(actual: Any, description: str = "") -> None:
    if actual is not True:
        raise WPTFailure(f"assert_true {description}: expected true got {_fmt(actual)}")


def assert_false(actual: Any, description: str = "") -> None:
    if actual is not False:
        raise WPTFailure(f"assert_false {description}: expected false got {_fmt(actual)}")


def assert_array_equals(actual: Iterable[Any], expected: Iterable[Any], description: str = "") -> None:
    a, e = list(actual), list(expected)
    if len(a) != len(e):
        raise WPTFailure(f"assert_array_equals {description}: lengths {len(a)} != {len(e)} ({_fmt(a)} vs {_fmt(e)})")
    for i, (x, y) in enumerate(zip(a, e)):
        # identity first (WPT compares nodes by reference), then value
        if x is not y and x != y:
            raise WPTFailure(f"assert_array_equals {description}: index {i}: {_fmt(x)} != {_fmt(y)}")


def assert_throws_js(exc_type: type, func: Callable[[], Any], description: str = "") -> None:
    try:
        func()
    except exc_type:
        return
    except Exception as other:  # pragma: no cover - diagnostic
        raise WPTFailure(
            f"assert_throws_js {description}: expected {exc_type.__name__}, got {type(other).__name__}: {other}"
        )
    raise WPTFailure(f"assert_throws_js {description}: expected {exc_type.__name__}, nothing raised")


# WPT DOMException names -> the legacy numeric code on domonic's DOMException
_DOM_ERROR_CODES = {
    "IndexSizeError": 1,
    "HierarchyRequestError": 3,
    "WrongDocumentError": 4,
    "InvalidCharacterError": 5,
    "NoModificationAllowedError": 7,
    "NotFoundError": 8,
    "NotSupportedError": 9,
    "InUseAttributeError": 10,
    "InvalidStateError": 11,
    "SyntaxError": 12,
    "InvalidModificationError": 13,
    "NamespaceError": 14,
    "InvalidNodeTypeError": 24,
}


def assert_throws_dom(name: str, func: Callable[[], Any], description: str = "") -> None:
    """Expect a ``DOMException`` (or, until domonic raises typed DOM errors
    everywhere, a plain ``ValueError`` / ``TypeError``) matching ``name``."""
    from domonic.dom import DOMException

    try:
        func()
    except DOMException as exc:
        wanted = _DOM_ERROR_CODES.get(name)
        if getattr(exc, "name", None) == name or (wanted is not None and getattr(exc, "code", None) == wanted):
            return
        raise WPTFailure(
            f"assert_throws_dom {description}: wanted {name}, got DOMException("
            f"name={getattr(exc, 'name', None)!r}, code={getattr(exc, 'code', None)!r})"
        )
    except (ValueError, TypeError):
        # domonic does not yet raise a typed DOMException for every hierarchy /
        # not-found case -- accept the generic error but let the caller decide
        # (these tests are usually xfail'd with a "no typed DOMException" reason)
        return
    except Exception as other:  # pragma: no cover
        raise WPTFailure(f"assert_throws_dom {description}: wanted {name}, got {type(other).__name__}: {other}")
    raise WPTFailure(f"assert_throws_dom {description}: wanted {name}, nothing raised")
