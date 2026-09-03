from __future__ import annotations

"""
    domonic.javascript
    ====================================
    - https://www.w3schools.com/jsref/jsref_reference.asp
    - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference

"""

import array
import builtins
import calendar

# JS ``Error`` subclasses below shadow the Python built-ins of the same name at
# module scope, so keep a handle on the real ones for ``except`` clauses that
# are catching genuine Python failures.
_PyTypeError = builtins.TypeError

# import chunk
import datetime
import gc
import importlib
import importlib.util
import inspect
import json
import locale as pylocale
import math
import multiprocessing
import os
import random
import re
import signal
import struct
import sys
import threading
import time as _time
import urllib.parse
from collections.abc import Iterable as IterableABC
from collections.abc import Mapping as MappingABC
from datetime import timezone
from email.utils import parsedate_to_datetime
from multiprocessing.pool import ThreadPool as Pool
from typing import Any, Callable, Iterable, Iterator, Mapping, Sequence
from urllib.parse import quote, unquote

# import requests
try:
    from dateutil.parser import parse, parserinfo
except ImportError:  # pragma: no cover - optional dependency

    class parserinfo:  # type: ignore[no-redef]
        def convertyear(self, year: int, *args: Any, **kwargs: Any) -> int:
            return year

    def parse(date_string: Any, parser_info: Any = None) -> datetime.datetime:
        value = str(date_string).strip()
        try:
            parsed = datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            parsed = None
        if parsed is not None:
            return parsed

        try:
            parsed = parsedate_to_datetime(value)
        except (_PyTypeError, ValueError, IndexError):
            parsed = None
        if parsed is not None:
            return parsed

        for fmt in (
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
            "%Y %m %d",
            "%d %B %Y",
            "%d %b %Y",
            "%Y/%m/%d",
            "%m/%d/%Y",
            "%B %d, %Y %H:%M:%S",
            "%B %d, %Y %H:%M",
            "%B %d, %y %H:%M:%S",
            "%B %d, %y %H:%M",
            "%d %b %Y %H:%M:%S GMT",
            "%B %d, %Y %H:%M:%S GMT%z",
            "%B %d, %y %H:%M:%S GMT%z",
        ):
            try:
                return datetime.datetime.strptime(value, fmt)
            except ValueError:
                continue
        raise ValueError(
            f"Unsupported date format without python-dateutil: {date_string}"
        )


from domonic.webapi.url import URL, URLSearchParams
from domonic.webapi.webstorage import Storage
from domonic.webapi.webworkers import Worker as _WebWorker

JSONScalar = str | int | float | bool | None
PropertyDict = dict[str, Any]
ObjectEntries = Iterable[tuple[str, Any] | list[Any]]
ArrayItems = Sequence[Any] | Iterable[Any]


def _own_enumerable_items(obj: Any) -> list[tuple[str, Any]]:
    """Return a JS-ish view of an object's own enumerable string properties."""
    if obj is None:
        return []
    if isinstance(obj, dict):
        return [(str(key), value) for key, value in obj.items()]
    if isinstance(obj, (str, bytes, bytearray)):
        return [(str(index), value) for index, value in enumerate(obj)]
    if isinstance(obj, Sequence) and not isinstance(obj, (str, bytes, bytearray)):
        return [(str(index), value) for index, value in enumerate(obj)]
    if isinstance(obj, (float, int, bool, complex)):
        return []
    if hasattr(obj, "__dict__"):
        return [
            (key, value) for key, value in vars(obj).items() if not key.startswith("_")
        ]
    return []


def function(python_str: str) -> Callable[[], Any]:
    """[evals a string i.e.

    sup = function('''print(hi)''')
    sup()

    ]

    Args:
        python_str ([str]): [some valid python code as a string]
    """

    def anon() -> Any:
        # JavaScript Function compatibility.
        return eval(python_str)  # nosec B307

    return anon


# JavaScript literal aliases for code ported from browser examples.
true: bool = True
false: bool = False
null: object = None
undefined: object = None

# def typeof(v):
#     return type(v).__name__


def _is_nan(value: Any) -> bool:
    return isinstance(value, float) and math.isnan(value)


def _is_js_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _is_js_value_type(value: Any) -> bool:
    return value is None or isinstance(
        value, (str, bool, int, float, bytes, tuple, frozenset)
    )


def _js_same_value_zero(left: Any, right: Any) -> bool:
    if _is_nan(left) and _is_nan(right):
        return True
    try:
        return left == right
    except Exception:
        return False


def _js_set_same_value_zero(left: Any, right: Any) -> bool:
    if _is_nan(left) and _is_nan(right):
        return True
    if _is_js_number(left) and _is_js_number(right):
        return left == right
    if isinstance(left, bool) or isinstance(right, bool):
        return type(left) is type(right) and left == right
    if _is_js_value_type(left) and _is_js_value_type(right):
        if type(left) is not type(right):
            return False
        return left == right
    if _is_js_value_type(left) or _is_js_value_type(right):
        return False
    return left is right


def _invoke_js_callback(callback: Callable[..., Any], *args: Any) -> Any:
    try:
        signature = inspect.signature(callback)
    except (_PyTypeError, ValueError):
        return callback(*args)

    parameters = list(signature.parameters.values())
    if any(param.kind == inspect.Parameter.VAR_POSITIONAL for param in parameters):
        return callback(*args)

    positional = [
        param
        for param in parameters
        if param.kind
        in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
    ]
    return callback(*args[: len(positional)])


def _positional_arity(fn: Any, cap: int) -> "int | None":
    """Number of positional params ``fn`` declares (capped at ``cap``), or
    ``None`` if it takes ``*args`` / its signature can't be read."""
    try:
        params = list(inspect.signature(fn).parameters.values())
    except (_PyTypeError, ValueError):
        return None
    if any(p.kind == inspect.Parameter.VAR_POSITIONAL for p in params):
        return None
    return min(
        cap,
        sum(
            1
            for p in params
            if p.kind
            in (
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
            )
        ),
    )


def _require_callback(fn: Any, label: str = "callback") -> None:
    """Raise a JS-style ``TypeError`` when an array iteration method is handed a
    non-function (``[].map()`` / ``[].filter(5)``)."""
    if not callable(fn):
        raise TypeError(f"{fn!r} is not a function")


def _js_iteratee(fn: Any) -> "Callable[[Any, int, Any], Any]":
    """Wrap a JS array callback so it can always be called ``(value, index,
    array)`` -- resolving the declared arity once, up front, instead of
    inspecting the signature on every element."""
    _require_callback(fn)
    n = _positional_arity(fn, 3)
    if n is None or n >= 3:
        return fn  # already accepts (value, index, array) / *args
    if n == 2:
        return lambda v, i, a: fn(v, i)
    if n == 1:
        return lambda v, i, a: fn(v)
    return lambda v, i, a: fn()


def _js_reducer(fn: Any) -> "Callable[[Any, Any, int, Any], Any]":
    """Like :func:`_js_iteratee` but for reduce callbacks
    ``(accumulator, value, index, array)`` -- arity resolved once."""
    n = _positional_arity(fn, 4)
    if n is None or n >= 4:
        return fn
    if n == 3:
        return lambda acc, v, i, a: fn(acc, v, i)
    if n == 2:
        return lambda acc, v, i, a: fn(acc, v)
    return lambda acc, v, i, a: fn(acc)


def _js_strictish_equal(left: Any, right: Any) -> bool:
    if _is_nan(left) or _is_nan(right):
        return False
    try:
        return left == right
    except Exception:
        return False


def _clamp_js_index(index: int, length: int) -> int:
    if index < 0:
        return max(length + index, 0)
    return min(index, length)


_DECODE_URI_RESERVED_ESCAPES = {
    "%23",
    "%24",
    "%26",
    "%2B",
    "%2C",
    "%2F",
    "%3A",
    "%3B",
    "%3D",
    "%3F",
    "%40",
}


def _decode_uri(value: Any) -> str:
    saved: dict[str, str] = {}

    def preserve_reserved(match: re.Match[str]) -> str:
        token = match.group(0)
        if token.upper() not in _DECODE_URI_RESERVED_ESCAPES:
            return token
        placeholder = f"\x00{len(saved)}\x00"
        saved[placeholder] = token
        return placeholder

    decoded = unquote(re.sub(r"%[0-9A-Fa-f]{2}", preserve_reserved, str(value)))
    for placeholder, token in saved.items():
        decoded = decoded.replace(placeholder, token)
    return decoded


def _looks_like_regex_separator(value: str) -> bool:
    return (
        "\\" in value
        or any(char in value for char in "[](){}|")
        or value.startswith("^")
        or value.endswith("$")
    )


class Boolean:
    """[Creates a Boolean Object.
    Warning this is NOT a boolean type. for that use Global.Boolean()]
    """

    def __init__(self, value: Any = False) -> None:
        self.value: bool = Global.Boolean(value)

    def __bool__(self) -> bool:
        return self.value

    def __eq__(self, other: object) -> bool:
        return self.value == (other.value if isinstance(other, Boolean) else other)

    def __hash__(self) -> int:
        return hash(self.value)

    def __str__(self) -> str:
        return "true" if self.value else "false"

    def valueOf(self) -> bool:
        return self.value

    def toString(self) -> str:
        return "true" if self.value else "false"


class Object:
    def __init__(
        self, obj: Any = None, *args: Mapping[str, Any], **kwargs: Any
    ) -> None:
        """[Creates a Javascript-like Object in python]

        Args:
            obj ([type]): [pass an object, dict or callable to the contructor]
        """
        if obj is None:
            obj = {}

        self.prototype = self.__class__
        self.__extensible = True
        self.__frozen = False
        self.__sealed = False

        for arg in args:
            self.__dict__.update(arg)
        self.__dict__.update(kwargs)

        # self.__dict__ = {}
        if callable(obj):
            self.__dict__.update(obj())
        if isinstance(obj, dict):
            self.__dict__.update(obj)
        else:
            try:
                self.__dict__ = {}
                self.__dict__.update(obj.__dict__)
                self.__dict__.update(kwargs)
                for _a in args:
                    self.__dict__.update(_a)
                # self.__dict__['__class__'] = obj.__class__.__name__
                # self.__dict__['__module__'] = obj.__module__
                # self.__dict__['__doc__'] = obj.__doc__
                # self.__dict__['__proto__'] = obj
                # self.__dict__['__proto__'].__class__ = Object
                # self.__dict__['__proto__'].__dict__ = self.__dict__
            except Exception as e:
                print("Object.__init__() failed to set attribs", e)

    def __str__(self) -> str:
        """Returns a string representation of the object"""
        d = self.__dict__.copy()
        for k, v in list(d.items()):
            if "__" in k:
                del d[k]
            if "prototype" in k:
                del d[k]
        return str(d)

    # def __repr__(self):
    #     """ Returns a string representation of the object."""
    #     return self.toString()

    @staticmethod
    def fromEntries(entries: ObjectEntries) -> PropertyDict:
        """
        transforms a list of lists containing key and value into an object.
        @param entries: a list containing key and value tuples. The key and value are separated by ':'
        @type entries: list of tuple(string, string)
        @returns: a dict object.

        >>> fromEntries(entries)
        {'a': 1, 'b': 2, 'c': 3}
        """
        return {k: v for k, v in entries}

    @staticmethod
    def assign(target: Any, source: Any) -> Any:
        """Copies the values of all enumerable own properties from one or more source objects to a target object."""
        if isinstance(target, dict):
            if isinstance(source, dict):
                for k, v in source.items():
                    target[k] = v
            else:
                for k, v in source.__dict__.items():
                    target[k] = v
        else:
            if isinstance(source, dict):
                for k, v in source.items():
                    setattr(target, k, v)
            else:
                for k, v in source.attribs.items():
                    setattr(target, k, v)

        # return target
        # for prop in source.__dict__:
        #     if source.propertyIsEnumerable(prop):
        #         target.__dict__[prop] = source.__dict__[prop]
        return target

    @staticmethod
    def create(proto: Any, propertiesObject: Any = None) -> Any:
        """Creates a new object with the specified prototype object and properties."""
        obj = Object(proto)
        if propertiesObject is not None:
            Object.defineProperties(obj, propertiesObject)
        return obj

    @staticmethod
    def defineProperty(obj: Any, prop: str, descriptor: Any) -> Any:
        """Adds the named property described by a given descriptor to an object."""
        value = descriptor.get("value") if isinstance(descriptor, dict) else descriptor
        if isinstance(obj, dict):
            obj[prop] = value
        else:
            setattr(obj, prop, value)
        return obj

    @staticmethod
    def defineProperties(obj: Any, props: Mapping[str, Any]) -> Any:
        """Adds named properties described by descriptors to an object."""
        for prop, desc in props.items():
            Object.defineProperty(obj, prop, desc)
        return obj

    @staticmethod
    def entries(obj: Any) -> list[list[Any]]:
        """Returns an array containing all of the [key, value] pairs in the object."""
        return [[key, value] for key, value in _own_enumerable_items(obj)]

    @staticmethod
    def keys(obj: Any) -> list[str]:
        """Returns an array containing the names of all of the given object's own enumerable string properties."""
        return [key for key, _ in _own_enumerable_items(obj)]

    @staticmethod
    def values(obj: Any) -> list[Any]:
        """Returns an array containing the values that correspond to
        all of a given object's own enumerable string properties."""
        return [value for _, value in _own_enumerable_items(obj)]

    @staticmethod
    def getOwnPropertyDescriptor(obj: Any, prop: str) -> Any:
        """Returns a property descriptor for a named property on an object."""
        if isinstance(obj, dict):
            return obj[prop]
        return obj.__dict__[prop]

    @staticmethod
    def getOwnPropertyNames(obj: Any) -> list[str] | Any:
        """Returns an array containing the names of all of the given object's
        own enumerable and non-enumerable properties."""
        if isinstance(obj, dict):
            return obj.keys()
        elif isinstance(obj, Object):
            return obj.__dict__.keys()
        elif isinstance(obj, object):
            return [prop for prop in dir(obj) if not prop.startswith("__")]
        return obj.__dict__.keys()

    # @staticmethod
    # def _is(value1, value2):
    #     """ Compares if two values are the same value.
    #     Equates all NaN values (which differs from both Abstract Equality Comparison
    #  and Strict Equality Comparison)."""
    #     pass

    @staticmethod
    def getOwnPropertySymbols(obj: Any) -> list[str]:
        """Returns an array of all symbol properties found directly upon a given object."""
        if isinstance(obj, dict):
            return []
        return [prop for prop in dir(obj) if not prop.startswith("__")]

    @staticmethod
    def getPrototypeOf(obj: Any) -> Any:
        """Returns the prototype (internal [[Prototype]] property) of the specified object."""
        if isinstance(obj, dict):
            return obj
        elif isinstance(obj, Object):
            return obj.prototype
        elif isinstance(obj, object):
            return obj.__class__
        return obj.__proto__

    @staticmethod
    def isExtensible(obj: Any) -> bool:
        """Determines if extending an object is allowed."""
        if isinstance(obj, Object):
            return bool(getattr(obj, "_Object__extensible", True))
        return True

    @staticmethod
    def isSealed(obj: Any) -> bool:
        """Determines if an object is sealed."""
        if isinstance(obj, Object):
            return bool(getattr(obj, "_Object__sealed", False))
        return False

    @staticmethod
    def preventExtensions(obj: Any) -> Any:
        """Prevent new properties from being added to an object."""
        if isinstance(obj, Object):
            object.__setattr__(obj, "_Object__extensible", False)
        return obj

    @staticmethod
    def seal(obj: Any) -> Any:
        """Prevent extensions and deletion of an object's existing properties."""
        if isinstance(obj, Object):
            object.__setattr__(obj, "_Object__extensible", False)
            object.__setattr__(obj, "_Object__sealed", True)
        return obj

    # @property
    # def setPrototypeOf(obj, prototype):
    #     """ Sets the object's prototype (its internal [[Prototype]] property). """
    #     if isinstance(obj, dict):
    #         return False
    #     elif isinstance(obj, Object):
    #         obj.prototype = prototype
    #         return True
    #     elif isinstance(obj, object):
    #         return False
    #     return False

    @staticmethod
    def isFrozen(obj: Any) -> bool:
        """Determines if an object was frozen."""
        if isinstance(obj, Object):
            return bool(getattr(obj, "_Object__frozen", False))
        return bool(getattr(obj, "__isFrozen", False))

    @staticmethod
    def is_(value1: Any, value2: Any) -> bool:
        """``Object.is`` -- SameValue: like ``===`` but ``NaN`` equals ``NaN``
        and ``+0`` differs from ``-0``. (``is`` is a Python keyword.)"""
        if isinstance(value1, float) and isinstance(value2, float):
            if math.isnan(value1) and math.isnan(value2):
                return True
            if value1 == 0 and value2 == 0:
                return math.copysign(1, value1) == math.copysign(1, value2)
        return type(value1) is type(value2) and value1 == value2

    @staticmethod
    def hasOwn(obj: Any, key: str) -> bool:
        """``Object.hasOwn(obj, key)`` -- a direct (own) property check."""
        if isinstance(obj, dict):
            return key in obj
        if isinstance(obj, Object):
            return key in obj.__dict__
        return key in getattr(obj, "__dict__", {})

    @staticmethod
    def groupBy(items: Iterable[Any], callback: Callable[..., Any]) -> dict:
        """``Object.groupBy`` -- group ``items`` into a dict keyed by
        ``callback(item, index)``."""
        out: dict[Any, list[Any]] = {}
        for index, item in enumerate(items):
            key = callback(item, index)
            out.setdefault(key, []).append(item)
        return out

    @staticmethod
    def freeze(obj: Any) -> Any:
        """Freezes an object. Other code cannot delete or change its properties."""
        if isinstance(obj, Object):
            object.__setattr__(obj, "_Object__extensible", False)
            object.__setattr__(obj, "_Object__sealed", True)
            object.__setattr__(obj, "_Object__frozen", True)
            object.__setattr__(obj, "_Object__isFrozen", True)
        else:
            try:
                setattr(obj, "__isFrozen", True)
            except Exception:
                return obj
        return obj

    # def prototype(self, obj):
    #     """
    #     prototype and allows you to add properties and methods to this object
    #     """
    #     if isinstance(obj, dict):
    #         return False
    #     elif isinstance(obj, Object):
    #         obj.prototype = self
    #         return True
    #     elif isinstance(obj, object):
    #         return False
    #     return False

    def __defineGetter__(self, prop: str, func: Callable[..., Any]) -> Object:
        """Adds a getter function for the specified property."""
        self.__dict__[prop] = property(func)
        return self

    def __defineSetter__(self, prop: str, func: Callable[..., Any]) -> Object:
        """Associates a function with a property that, when set, calls the function."""
        self.__dict__[prop] = property(func)
        return self

    def __lookupGetter__(self, prop: str) -> Any:
        """
        Returns the getter function for the specified property.
        """
        return self.__dict__[prop]

    def __lookupSetter__(self, prop: str) -> Any:
        """Returns the function associated with the specified property by the __defineSetter__() method."""
        return self.__dict__[prop]

    def hasOwnProperty(self, prop: str) -> bool:
        """Returns a boolean indicating whether an object contains the specified property
        as a direct property of that object and not inherited through the prototype chain.
        """
        # raise NotImplementedError
        # return hasattr(self, prop)
        return self.__dict__.get(prop, None) != None

    def isPrototypeOf(self, obj: Any) -> bool:
        """Returns a boolean indicating whether an object is a copy of this object."""
        if isinstance(obj, Object):
            return obj.prototype == self
        elif isinstance(obj, dict):
            return obj == self
        elif isinstance(obj, object):
            return obj.__class__ == self.__class__ and obj.__dict__ == self.__dict__
        return obj.__class__ == self.__class__ and obj.__proto__ == self

    # def propertyIsEnumerable(self, prop):
    #     """ Returns a boolean indicating whether the specified property is enumerable. """
    #     pass

    def toLocaleString(self) -> str:
        """Calls toString()"""
        return self.toString()

    def toString(self) -> str:
        """Returns a string representation of the object."""
        return "[" + self.__class__.__name__ + ": " + str(self.__dict__) + "]"

    def valueOf(self) -> Any:
        """Returns the value of the object."""
        return self

    def __iter__(self) -> Iterator[str]:
        """Iterates over object's properties."""
        for prop in self.__dict__:
            yield prop
        for key in self.__dict__:
            yield key
        # return
        # return self.__dict__.__iter__()

    def __hash__(self) -> int:
        """Returns the hash of the object."""
        return hash(self.toString())

    def __eq__(self, other: object) -> bool:
        """Compares two objects."""
        if isinstance(other, Object):
            return self.toString() == other.toString()
        return False

    def __ne__(self, other: object) -> bool:
        """Compares two objects."""
        if isinstance(other, Object):
            return self.toString() != other.toString()
        return True

    def __nonzero__(self) -> bool:
        """Returns whether the object is false."""
        return self.toString() != ""

    def __bool__(self) -> bool:
        """Returns whether the object is false."""
        return self.toString() != ""

    # def __dict__(self):
    #     """ Returns the object's attributes as a dictionary. """
    #     return self.__dict__

    def __getitem__(self, key: str) -> Any:
        """Returns the value of the specified property."""
        # return self.__dict__[key]
        # return self.__dict__.get(key, None)
        return self.__dict__.get(key)

    def __deepcopy__(self, memo: dict[int, Any]) -> Object:
        """Makes a deep copy of the object."""
        return self.__class__(self.__dict__)

    def __setitem__(self, key: str, value: Any) -> None:
        """Sets the value of the specified property."""
        state = self.__dict__
        is_internal = isinstance(key, str) and (
            key.startswith("_Object__") or key == "prototype"
        )
        if not is_internal:
            if state.get("_Object__frozen", False):
                raise TypeError("Cannot assign to frozen Object")
            if not state.get("_Object__extensible", True) and key not in state:
                raise TypeError("Cannot add property to non-extensible Object")
        return state.__setitem__(key, value)

    def __delitem__(self, key: str) -> None:
        """Deletes the specified property."""
        state = self.__dict__
        is_internal = isinstance(key, str) and (
            key.startswith("_Object__") or key == "prototype"
        )
        if not is_internal:
            if state.get("_Object__frozen", False) or state.get(
                "_Object__sealed", False
            ):
                raise TypeError("Cannot delete property from sealed Object")
        del self.__dict__[key]

    def __len__(self) -> int:
        """Returns the number of properties."""
        return len(self.__dict__)

    def __contains__(self, key: str) -> bool:
        """[Returns whether the specified property exists.]

        Args:
            key ([str]): [The name of the property to check for.]

        Returns:
            [bool]: [True if the specified property exists. Otherwise, False.]
        """
        return key in self.__dict__

    def __getattr__(self, name: str) -> Any:
        """[gets the value of the specified property]

        Args:
            name ([str]): [the name of the property]

        Returns:
            [str]: [the value of the specified property]
        """
        return self.__getitem__(name)

    def __setattr__(self, name: str, val: Any) -> None:
        """[sets the value of the specified property]

        Args:
            name ([str]): [the name of the property]
            val ([str]): [the value of the property]

        Returns:
            [str]: [the value of the property]
        """
        if name == "__dict__":
            object.__setattr__(self, name, val)
            return None
        return self.__setitem__(name, val)

    def __delattr__(self, name: str) -> None:
        """[deletes the specified property]

        Args:
            name ([str]): [the name of the property]

        Returns:
            [type]: [the value of the property]
        """
        if name == "__dict__":
            object.__delattr__(self, name)
            return None
        return self.__delitem__(name)

    # def __call__(self, *args, **kwargs):
    #     """ Calls the object. """
    #     return self.toString()


class Function(Object):
    """a Function object"""

    def __init__(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        self.func = func
        self.arguments = args
        self.caller = None
        self.displayName = None
        self.length = None
        self.name = None
        # self.isCallable = True
        # self.constructor = False
        # self.__proto__ = None

    def apply(
        self, thisArg: Any = None, args: Sequence[Any] | None = None, **kwargs: Any
    ) -> Any:
        """[calls a function with a given this value, and arguments provided as an array]

        Args:
            thisArg ([type]): [The value of this provided for the call to func.]

        Returns:
            [type]: [result of calling the function.]
        """
        if thisArg is not None:
            try:
                return self.func(args)  # kwargs?
            except _PyTypeError:
                return self.func()
        try:
            return self.func(*(args or ()))
        except _PyTypeError:
            return self.func()

    def bind(self, thisArg: Any, *args: Any, **kwargs: Any) -> Callable[..., Any]:
        """[creates a new function that, when called,
        has its this keyword set to the provided value,
        with a given sequence of arguments preceding any provided when the new function is called.]

        Args:
            thisArg ([type]): [The value to be passed as the this parameter to the target
            function func when the bound function is called.]

        Returns:
            [type]: [A copy of the given function with the specified this value, and initial arguments (if provided).]
        """
        from functools import partial

        bound_f = partial(self.func, *args, *kwargs)
        return bound_f
        # raise NotImplementedError

    # @staticmethod
    def call(self, thisArg: Any = None, *args: Any, **kwargs: Any) -> Any:
        """[calls a function with a given this value and arguments provided individually.]

        Args:
            thisArg ([type]): [description]

        Returns:
            [type]: [result of calling the function.]
        """
        if thisArg is not None:
            try:
                return self.func(thisArg)  # kwargs?
            except _PyTypeError as e:
                print(e)
                return self.func()

        try:
            return self.func(*args)
        except _PyTypeError:
            return self.func()

    def toString(self) -> str:
        """[Returns a string representing the source code of the function. Overrides the]"""
        try:
            return inspect.getsource(self.func).strip()
        except (OSError, _PyTypeError):
            name = getattr(self.func, "__name__", "")
            name = "" if name == "<lambda>" else f" {name}"
            return f"function{name}() {{ [native code] }}"


class Map:
    """Map holds key-value pairs and remembers the original insertion order of the keys."""

    def __init__(
        self, collection: "list[Any] | dict[str, Any] | None" = None
    ) -> None:
        """Create a Map. ``collection`` may be omitted (``new Map()``), a dict,
        an iterable of ``[key, value]`` pairs (``new Map([["a", 1]])``), or --
        as a domonic convenience -- a flat list, in which each value is its own
        key."""
        entries: list[tuple[Any, Any]] = []
        if collection is None:
            pass
        elif isinstance(collection, dict):
            entries = list(collection.items())
        elif isinstance(collection, Map):
            entries = list(zip(collection._order, collection.values()))
        elif hasattr(collection, "__iter__"):
            for item in collection:
                if (
                    isinstance(item, (list, tuple))
                    and not isinstance(item, str)
                    and len(item) == 2
                ):
                    entries.append((item[0], item[1]))
                else:
                    entries.append((item, item))
        else:
            raise TypeError("Map requires an iterable of pairs or a dict.")

        self.collection = dict(entries)
        self._data: dict[str, Any] = {}
        self._order: list[str] = []
        self._dict = self._data
        for key, value in entries:
            normalized_key = str(key)
            if normalized_key not in self._dict:
                self._order.append(normalized_key)
            self._dict[normalized_key] = value

    def __contains__(self, key: str) -> bool:
        return str(key) in self._dict

    def __getitem__(self, key: str) -> Any:
        return self._dict[str(key)]

    def __setitem__(self, key: str, value: Any) -> None:
        key = str(key)
        if key not in self._dict:
            self._order.append(key)
        self._dict[key] = value

    def __delitem__(self, key: str) -> None:
        key = str(key)
        self._order.remove(key)
        del self._dict[key]

    def __len__(self) -> int:
        return len(self._order)

    @property
    def size(self) -> int:
        """The number of entries (``map.size`` -- a property, like JS)."""
        return len(self._order)

    def clear(self) -> None:
        """Removes all key-value pairs from the Map object."""
        self._data = {}
        self._dict = self._data
        self._order = []

    def delete(self, key: str) -> bool:
        """Returns true if an element in the Map object existed and has been removed,
        or false if the element does not exist. Map.prototype.has(key) will return false afterwards.
        """
        key = str(key)
        try:
            self._order.remove(key)
            del self._dict[key]
            return True
        except Exception:
            return False

    def get(self, key: str, default: Any = None) -> Any:
        """Returns the value associated to the key, or undefined if there is none."""
        return self._dict.get(str(key), default)

    def has(self, key: str) -> bool:
        """Returns a boolean asserting whether a value has been associated to the key in the Map object or not."""
        return str(key) in self._dict

    def set(self, key: str, value: Any) -> Map:
        """Sets the value for the key in the Map object. Returns the Map object."""
        self[str(key)] = value
        return self

    def iterkeys(self) -> Iterator[str]:
        return iter(self._order)

    def iteritems(self) -> Iterator[tuple[str, Any]]:
        for key in self._order:
            yield key, self._dict[key]

    def keys(self) -> list[str]:
        """Returns a new Iterator object that contains the keys
        for each element in the Map object in insertion order."""
        return list(self.iterkeys())

    def values(self) -> list[Any]:
        """Returns a new Iterator object that contains the values
        for each element in the Map object in insertion order."""
        return [self._dict[key] for key in self._order]

    def entries(self) -> list[tuple[str, Any]]:
        """Returns a new Iterator object that contains an array of [key, value]
        for each element in the Map object in insertion order."""
        return [(x, self._dict[x]) for x in self._order]

    def forEach(
        self, callbackFn: Callable[[Any, Any, "Map"], Any], thisArg: Any = None
    ) -> None:
        """Call callbackFn once for each key/value pair in insertion order."""
        for key in list(self._order):
            _invoke_js_callback(callbackFn, self._dict[key], key, self)

    def update(self, ordered_dict: Any) -> None:
        for key, value in ordered_dict.items():
            self[key] = value

    def __str__(self) -> str:
        return str([(x, self._dict[x]) for x in self._order])


class FormData:
    """Compatibility wrapper for :class:`domonic.webapi.xhr.FormData`."""

    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        from domonic.webapi.xhr import FormData as XHRFormData

        return XHRFormData(*args, **kwargs)


class Worker(_WebWorker):
    """Background worker exposed from the legacy ``domonic.javascript`` namespace."""


class Math(Object):
    """Math class that mirrors javascript implementation.

    i.e. you can pass strings and it will also work, Math.abs('-1')

    """

    PI: float = 3.141592653589793
    E: float = 2.718281828459045
    LN2: float = 0.6931471805599453
    LN10: float = 2.302585092994046
    LOG2E: float = 1.4426950408889634
    LOG10E: float = 0.4342944819032518
    SQRT1_2: float = 0.7071067811865476
    SQRT2: float = 1.4142135623730951

    @staticmethod
    def _force_number(func: Callable[..., Any]) -> Callable[..., Any]:
        """[private decorator to make Math behave like javascript and turn strings, bools and None into numbers]]"""

        def validation_decorator(*args: Any, **kwargs: Any) -> Any:
            params = list(args)
            for i, n in enumerate(params):

                if type(n) == list or type(n) == tuple:
                    if len(n) == 0:
                        params[i] = n = 0
                    elif len(n) == 1:
                        params[i] = n = n[0]

                if type(n) == str:
                    if n == "":
                        params[i] = n = 0
                        continue

                if n is None:
                    params[i] = 0
                    continue

                if type(n) != float and type(n) != int:
                    try:
                        if "." in n:
                            params[i] = float(n)
                        else:
                            params[i] = int(n)
                    except Exception:
                        # raise ValueError("")
                        # Keep historical loose coercion behavior: leave
                        # values that cannot be int/float converted alone.
                        params[i] = n

            args = tuple(params)
            try:
                return func(*args)
            except Exception:
                return None

        return validation_decorator

    @staticmethod
    @_force_number
    def abs(x: float) -> float:
        """[Returns the absolute value of a number.]

        Args:
            x ([float]): [number]

        Returns:
            [float]: [absolute value]
        """
        return abs(x)

    @staticmethod
    @_force_number
    def acos(x: float) -> float:
        """[Returns the arccosine (in radians) of a number.]

        Args:
            x ([float]): [number]

        Returns:
            [float]: [arccosine]
        """
        return math.acos(x)

    @staticmethod
    @_force_number
    def acosh(x: float) -> float:
        """Returns the hyperbolic arccosine of a number."""
        return math.acosh(x)

    @staticmethod
    @_force_number
    def asin(x: float) -> float:
        """Returns the arcsine (in radians) of a number."""
        return math.asin(x)

    @staticmethod
    @_force_number
    def asinh(x: float) -> float:
        """Returns the hyperbolic arcsine of a number."""
        return math.asinh(x)

    @staticmethod
    @_force_number
    def atan(x: float) -> float:
        """Returns the arctangent (in radians) of a number."""
        return math.atan(x)

    @staticmethod
    @_force_number
    def atan2(x: float, y: float) -> float:
        """Returns the arctangent of the quotient of its arguments."""
        return math.atan2(x, y)

    @staticmethod
    @_force_number
    def atanh(x: float) -> float:
        """Returns the hyperbolic arctangent of a number."""
        return math.atanh(x)

    @staticmethod
    @_force_number
    def cbrt(x: float) -> float:
        """Returns the cube root of a number."""
        if hasattr(math, "cbrt"):
            return math.cbrt(x)
        if x == 0:
            return 0.0
        return math.copysign(abs(x) ** (1 / 3), x)

    @staticmethod
    @_force_number
    def ceil(x: float) -> float:
        """Returns the smallest integer greater than or equal to a number."""
        return math.ceil(x)

    @staticmethod
    @_force_number
    def cos(x: float) -> float:
        """Returns the cosine of a number. (x is in radians)"""
        return math.cos(x)

    @staticmethod
    @_force_number
    def cosh(x: float) -> float:
        """Returns the hyperbolic cosine of a number."""
        return math.cosh(x)

    @staticmethod
    @_force_number
    def exp(x: float) -> float:
        """Returns the value of E^x."""
        return math.exp(x)

    @staticmethod
    @_force_number
    def floor(x: float) -> float:
        """Returns the largest integer less than or equal to a number."""
        return math.floor(x)

    @staticmethod
    @_force_number
    def log(x: float, base: float | None = None) -> float:
        """Returns the natural logarithm (base E) of a number."""
        if base is None:
            return math.log(x)
        else:
            return math.log(x, base)

    @staticmethod
    def _extreme(args: tuple[Any, ...], pick: Any, empty: float) -> Any:
        if not args:
            return empty
        nums = [float(Global.Number(a)) for a in args]
        if any(n != n for n in nums):
            return float("nan")
        result = pick(nums)
        return int(result) if result.is_integer() else result

    @staticmethod
    def max(*args: Any) -> Any:
        """The largest of the arguments (``-Infinity`` for none, ``NaN`` if any
        is ``NaN``) -- variadic, like JavaScript."""
        return Math._extreme(args, builtins.max, float("-inf"))

    @staticmethod
    def min(*args: Any) -> Any:
        """The smallest of the arguments (``Infinity`` for none, ``NaN`` if any
        is ``NaN``) -- variadic, like JavaScript."""
        return Math._extreme(args, builtins.min, float("inf"))

    @staticmethod
    @_force_number
    def random() -> float:
        """Returns a random number between 0 and 1."""
        # Math.random is intentionally non-crypto.
        return random.random()  # nosec B311

    @staticmethod
    @_force_number
    def round(x: float) -> float:
        """Nearest integer; ties round toward +Infinity (JavaScript)."""
        if math.isnan(x) or math.isinf(x):
            return x
        return math.floor(x + 0.5)

    @staticmethod
    @_force_number
    def sign(x: float) -> float:
        """-1, 0 or 1 according to the sign of x (NaN stays NaN)."""
        if math.isnan(x):
            return x
        if x > 0:
            return 1
        if x < 0:
            return -1
        return x  # preserves 0 / -0.0

    @staticmethod
    @_force_number
    def expm1(x: float) -> float:
        """exp(x) - 1, accurate for small x."""
        return math.expm1(x)

    @staticmethod
    def imul(a: Any, b: Any) -> int:
        """C-like 32-bit integer multiplication."""
        return ToInt32((ToInt32(int(a)) * ToInt32(int(b))) & 0xFFFFFFFF)

    @staticmethod
    @_force_number
    def pow(x: float, y: float) -> float:
        """Returns the value of a number raised to a power."""
        return math.pow(x, y)

    @staticmethod
    @_force_number
    def sin(x: float) -> float:
        """Returns the sine of a number. (x is in radians)"""
        return math.sin(x)

    @staticmethod
    @_force_number
    def sinh(x: float) -> float:
        """Returns the hyperbolic sine of a number."""
        return math.sinh(x)

    @staticmethod
    @_force_number
    def sqrt(x: float) -> float:
        """Returns the square root of a number."""
        return math.sqrt(x)

    @staticmethod
    @_force_number
    def tan(x: float) -> float:
        """Returns the tangent of a number. (x is in radians)"""
        return math.tan(x)

    @staticmethod
    @_force_number
    def tanh(x: float) -> float:
        """Returns the hyperbolic tangent of a number."""
        return math.tanh(x)

    @staticmethod
    @_force_number
    def trunc(x: float) -> float:
        """Returns the integer part of a number."""
        return math.trunc(x)

    @staticmethod
    def hypot(*args: float) -> float:
        """Return the square root of the sum of squares of its arguments."""
        return math.hypot(*args)

    @staticmethod
    @_force_number
    def log2(x: float) -> float:
        """Return the base 2 logarithm of a number."""
        return math.log2(x)

    @staticmethod
    @_force_number
    def log1p(x: float) -> float:
        """Return the natural logarithm of 1 plus a number."""
        return math.log1p(x)

    @staticmethod
    @_force_number
    def loglp(x: float) -> float:
        """Backward-compatible alias for the historical ``log1p`` typo."""
        return Math.log1p(x)

    @staticmethod
    @_force_number
    def log10(x: float) -> float:
        """function returns the base 10 logarithm of a number, that is"""
        return math.log10(x)

    @staticmethod
    @_force_number
    def fround(x: float) -> float:
        """returns the nearest 32-bit single precision float representation of a Number"""
        return struct.unpack(">f", struct.pack(">f", float(x)))[0]

    @staticmethod
    @_force_number
    def clz32(x: float) -> int:
        """returns the number of leading zero bits in the 32-bit binary representation of a number."""
        value = int(x) & 0xFFFFFFFF
        if value == 0:
            return 32
        return 32 - value.bit_length()


# import urllib


class Global:
    """javascript global methods"""

    NaN = "NaN"
    Infinity = float("inf")

    # populated at module load once Performance / Window exist
    performance: Any
    globalThis: Any
    self: Any
    window: Any
    setInterval: Callable[..., Any]
    clearInterval: Callable[..., Any]

    __timers: dict[int, threading.Timer] = {}

    @staticmethod
    def decodeURI(x: str) -> str:
        """Decodes a URI"""
        return _decode_uri(x)

    @staticmethod
    def decodeURIComponent(x: str) -> str:
        """Decodes a URI component"""
        return unquote(x, encoding="utf-8")

    @staticmethod
    def encodeURI(x: Any) -> str:
        """Encodes a URI"""
        return quote(str(x), safe="~@#$&()*!+=:;,.?/'")

    @staticmethod
    def encodeURIComponent(x: Any) -> str:
        """Encodes a URI component"""
        return quote(str(x), safe="~()*!.'")

        # @staticmethod
        # def escape():
        """ Deprecated in version 1.5. Use encodeURI() or encodeURIComponent() """
        # pass

    @staticmethod
    def eval(pythonstring: str) -> Any:
        """Evaluates a string and executes it as if it was script code"""
        # JavaScript eval compatibility.
        eval(pythonstring)  # nosec B307

    @staticmethod
    def isFinite(x: Any) -> bool:
        """Returns true if x coerces to a finite number."""
        try:
            return math.isfinite(float(Global.Number(x)))
        except (ValueError, _PyTypeError):
            return False

    @staticmethod
    def isNaN(x: Any) -> bool:
        """Determines whether a value coerces to NaN."""
        try:
            return math.isnan(float(Global.Number(x)))
        except (ValueError, _PyTypeError):
            return True

    @staticmethod
    def Number(x: Any) -> int | float:
        """Converts a value to a number, JS-style (non-numeric -> NaN)."""
        if isinstance(x, bool):
            return 1 if x else 0
        if x is None:
            return float("nan")
        if isinstance(x, (int, float)):
            return x
        if isinstance(x, (list, tuple)):
            if len(x) == 0:
                return 0
            if len(x) == 1:
                return Global.Number(x[0])
            return float("nan")

        if isinstance(x, str):
            value = x.strip()
            if value == "":
                return 0
            if "_" in value or value.lower() == "nan":
                return float("nan")

            unsigned = value[1:] if value[:1] in ("+", "-") else value
            try:
                if unsigned.lower().startswith(("0x", "0o", "0b")):
                    return int(value, 0)
                if value.lower() in ("infinity", "+infinity", "-infinity"):
                    return float(value)
                if re.fullmatch(
                    r"[+-]?(?:(?:\d+\.\d*|\.\d+|\d+)(?:[eE][+-]?\d+)?)",
                    value,
                ):
                    if "." in value or "e" in value.lower():
                        return float(value)
                    return int(value, 10)
            except Exception:
                return float("nan")
            return float("nan")

        try:
            return float(x)
        except Exception:
            return float("nan")

    @staticmethod
    def Boolean(x: Any) -> bool:
        if isinstance(x, bool):
            return x
        if x is None:
            return False
        if isinstance(x, (int, float)):
            return x != 0 and not math.isnan(x)
        if isinstance(x, str):
            return x != ""
        return True

    @staticmethod
    def parseFloat(x: str) -> float:
        """Parses a string and returns a floating point number"""
        value = str(x).lstrip()
        match = re.match(
            r"[+-]?(?:Infinity|(?:(?:\d+\.\d*|\.\d+|\d+)(?:[eE][+-]?\d+)?))",
            value,
        )
        if not match:
            return float("nan")
        try:
            return float(match.group(0))
        except Exception:
            return float("nan")

    @staticmethod
    def parseInt(x: str, radix: int = 0) -> int | float:
        """Parses a string and returns an integer"""
        value = str(x).lstrip()
        sign = 1
        if value[:1] in ("+", "-"):
            sign = -1 if value[0] == "-" else 1
            value = value[1:]

        try:
            radix = int(radix or 0)
        except Exception:
            return float("nan")

        if radix and (radix < 2 or radix > 36):
            return float("nan")
        if radix == 0:
            if value.lower().startswith("0x"):
                radix = 16
                value = value[2:]
            else:
                radix = 10
        elif radix == 16 and value.lower().startswith("0x"):
            value = value[2:]

        alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
        allowed = alphabet[:radix]
        digits = []
        for char in value.lower():
            if char in allowed:
                digits.append(char)
            else:
                break

        if not digits:
            return float("nan")
        return sign * int("".join(digits), radix)

    @staticmethod
    def String(x: Any = "") -> str:
        """Converts a value to a string the way JavaScript's ``String(x)`` does."""
        if x is None or x is undefined:
            return "undefined" if x is undefined and undefined is not None else "null"
        if isinstance(x, bool):
            return "true" if x else "false"
        if isinstance(x, float):
            if x != x:
                return "NaN"
            if x == float("inf"):
                return "Infinity"
            if x == float("-inf"):
                return "-Infinity"
            return repr(x) if not x.is_integer() else str(int(x))
        if isinstance(x, (list, tuple)):
            return ",".join(
                "" if item is None else Global.String(item) for item in x
            )
        if isinstance(x, dict):
            return "[object Object]"
        return str(x)

    def undefined(self) -> None:
        """Indicates that a variable has not been assigned a value"""
        return None

        # @staticmethod
        # def unescape():
        """ Deprecated in version 1.5. Use decodeURI() or decodeURIComponent() instead """
        # pass

    @staticmethod
    def require(path: str) -> Any:
        """Loads a script from a file"""
        module_path = str(path).strip()
        if not module_path:
            raise ImportError("require() needs a module name or Python file path")

        if module_path.endswith(".py") or os.path.sep in module_path:
            file_path = os.path.abspath(os.path.expanduser(module_path))
            if os.path.exists(file_path):
                module_name = os.path.splitext(os.path.basename(file_path))[0]
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                if spec is None or spec.loader is None:
                    raise ImportError(f"Cannot load module from {module_path!r}")
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                return module

        module_name = module_path
        if module_name.endswith(".py"):
            module_name = module_name[:-3]
        module_name = module_name.replace("/", ".").replace("\\", ".")
        return importlib.import_module(module_name)

    @staticmethod
    def setTimeout(
        callback: str | Callable[..., Any], t: int | float, *args: Any, **kwargs: Any
    ) -> int:
        """[sets a timer which executes a function or evaluates an expression after a specified delay]

        Args:
            callback (function): [method to be executed after the delay]
            t ([int]): [milliseconds]

        Returns:
            [str]: [an identifier for the timer]
        """
        fn: Callable[..., Any] = (
            eval(callback) if isinstance(callback, str) else callback  # nosec B307
        )

        timer = threading.Timer(t / 1000, fn, args=args, kwargs=kwargs)
        timer_id = id(timer)
        Global.__timers[timer_id] = timer
        timer.start()
        return timer_id

    @staticmethod
    def clearTimeout(timeoutID: int) -> None:
        """[cancels a timer set with setTimeout()]

        Args:
            timeoutID ([str]): [the identifier returned by setTimeout()]
        """
        Global.__timers.pop(timeoutID).cancel()


# NOTE - for globals use the class to make them but then register them here
decodeURI = Global.decodeURI
decodeURIComponent = Global.decodeURIComponent
encodeURI = Global.encodeURI
encodeURIComponent = Global.encodeURIComponent
parseFloat = Global.parseFloat
parseInt = Global.parseInt
setTimeout = Global.setTimeout
clearTimeout = Global.clearTimeout


class Performance:

    _start: float = _time.time()

    def __init__(self) -> None:
        self._entries: list[Any] = []
        self._marks: dict[str, float] = {}

    def now(self) -> float:
        end = _time.time()
        return end - Performance._start

    def mark(self, name: str) -> Any:
        from domonic.dom import PerformanceMark, PerformanceObserver

        start = self.now()
        self._marks[name] = start
        entry = PerformanceMark(name, start)
        self._entries.append(entry)
        PerformanceObserver._notify_entry(entry)
        return entry

    def measure(
        self, name: str, startMark: str | None = None, endMark: str | None = None
    ) -> Any:
        from domonic.dom import PerformanceMeasure, PerformanceObserver

        end = self.now() if endMark is None else self._marks.get(endMark, self.now())
        start = 0.0 if startMark is None else self._marks.get(startMark, 0.0)
        entry = PerformanceMeasure(name, start, end - start)
        self._entries.append(entry)
        PerformanceObserver._notify_entry(entry)
        return entry

    def getEntries(self) -> list[Any]:
        return list(self._entries)

    def getEntriesByType(self, entryType: str) -> list[Any]:
        return [
            entry
            for entry in self._entries
            if getattr(entry, "entryType", None) == entryType
        ]

    def getEntriesByName(self, name: str, entryType: str | None = None) -> list[Any]:
        entries = [
            entry for entry in self._entries if getattr(entry, "name", None) == name
        ]
        if entryType is not None:
            entries = [
                entry
                for entry in entries
                if getattr(entry, "entryType", None) == entryType
            ]
        return entries

    def clearMarks(self, name: str | None = None) -> None:
        if name is None:
            self._marks.clear()
            self._entries = [
                entry
                for entry in self._entries
                if getattr(entry, "entryType", None) != "mark"
            ]
            return
        self._marks.pop(name, None)
        self._entries = [
            entry
            for entry in self._entries
            if not (
                getattr(entry, "entryType", None) == "mark"
                and getattr(entry, "name", None) == name
            )
        ]

    def clearMeasures(self, name: str | None = None) -> None:
        if name is None:
            self._entries = [
                entry
                for entry in self._entries
                if getattr(entry, "entryType", None) != "measure"
            ]
            return
        self._entries = [
            entry
            for entry in self._entries
            if not (
                getattr(entry, "entryType", None) == "measure"
                and getattr(entry, "name", None) == name
            )
        ]

    # def reset(self):
    #     Performance._start = _time.time()


performance = Performance()
Global.performance = performance
globalThis = Global
Global.globalThis = globalThis
Global.self = globalThis


class Intl:
    def __init__(self) -> None:
        """Namespace object for internationalization constructors."""

    _supported_values: dict[str, tuple[str, ...]] = {
        "calendar": (
            "buddhist",
            "chinese",
            "coptic",
            "dangi",
            "ethioaa",
            "ethiopic",
            "gregory",
            "hebrew",
            "indian",
            "islamic",
            "islamic-civil",
            "islamic-rgsa",
            "islamic-tbla",
            "islamic-umalqura",
            "iso8601",
            "japanese",
            "persian",
            "roc",
        ),
        "collation": (
            "big5han",
            "compat",
            "dict",
            "direct",
            "ducet",
            "emoji",
            "eor",
            "gb2312",
            "phonebk",
            "phonetic",
            "pinyin",
            "reformed",
            "searchjl",
            "stroke",
            "trad",
            "unihan",
            "zhuyin",
        ),
        "currency": (
            "AED",
            "AUD",
            "BRL",
            "CAD",
            "CHF",
            "CNY",
            "DKK",
            "EUR",
            "GBP",
            "HKD",
            "INR",
            "JPY",
            "KRW",
            "MXN",
            "NOK",
            "NZD",
            "PLN",
            "SEK",
            "SGD",
            "TRY",
            "USD",
            "ZAR",
        ),
        "numberingsystem": (
            "adlm",
            "arab",
            "arabext",
            "bali",
            "beng",
            "deva",
            "fullwide",
            "gujr",
            "guru",
            "hanidec",
            "khmr",
            "knda",
            "laoo",
            "latn",
            "limb",
            "mlym",
            "mong",
            "mymr",
            "orya",
            "tamldec",
            "telu",
            "thai",
            "tibt",
        ),
        "unit": (
            "acre",
            "bit",
            "byte",
            "celsius",
            "centimeter",
            "day",
            "degree",
            "fahrenheit",
            "fluid-ounce",
            "foot",
            "gallon",
            "gigabit",
            "gigabyte",
            "gram",
            "hectare",
            "hour",
            "inch",
            "kilobit",
            "kilobyte",
            "kilogram",
            "kilometer",
            "liter",
            "megabit",
            "megabyte",
            "meter",
            "mile",
            "mile-scandinavian",
            "milliliter",
            "millimeter",
            "millisecond",
            "minute",
            "month",
            "ounce",
            "percent",
            "petabyte",
            "pound",
            "second",
            "stone",
            "terabit",
            "terabyte",
            "week",
            "yard",
            "year",
        ),
    }

    @staticmethod
    def getCanonicalLocales(locales: str | list[str]) -> list[str]:
        """Returns the canonicalized locales."""
        if isinstance(locales, str):
            locales = [locales]
        canonical = []
        for locale in locales:
            if locale.find("-") != -1:
                locale = (
                    locale.split("-")[0].lower() + "-" + locale.split("-")[1].upper()
                )
            elif locale.find("_") != -1:
                locale = (
                    locale.split("_")[0].lower() + "_" + locale.split("_")[1].upper()
                )
            else:
                locale = locale.lower()
            canonical.append(locale)
        return canonical

    @staticmethod
    def supportedValuesOf(*args: Any) -> list[str]:
        """Returns a sorted array containing the supported unique calendar,
        collation, currency, numbering systems, or unit values supported by the implementation.
        """
        if len(args) == 1:
            key = args[0]
        elif len(args) == 2:
            key = args[1]
        else:
            raise TypeError("supportedValuesOf() expects a key")

        key = str(key)
        normalized = key.replace("-", "").lower()
        if normalized == "timezone":
            return Intl._supported_time_zones()

        try:
            return sorted(Intl._supported_values[normalized])
        except KeyError:
            raise ValueError(f"Unsupported Intl key: {key}") from None

    @staticmethod
    def _supported_time_zones() -> list[str]:
        try:
            from zoneinfo import available_timezones

            zones = set(available_timezones())
        except Exception:
            zones = set()
        zones.update({"UTC", "Etc/UTC"})
        return sorted(zones)

    class _Collator:
        def __init__(
            self,
            locales: str | list[str] | None = None,
            options: Mapping[str, Any] | None = None,
        ) -> None:
            options = dict(options or {})
            canonical = Intl.getCanonicalLocales(locales or "en-US")
            self.locale = canonical[0] if canonical else "en-US"
            self.usage = options.get("usage", "sort")
            self.sensitivity = options.get("sensitivity", "variant")
            self.ignorePunctuation = bool(options.get("ignorePunctuation", False))
            self.numeric = bool(options.get("numeric", False))
            self.caseFirst = options.get("caseFirst", "false")

        @staticmethod
        def supportedLocalesOf(locales: str | list[str]) -> list[str]:
            return Intl.getCanonicalLocales(locales)

        def compare(self, first: Any, second: Any) -> int:
            left = self._prepare(str(first))
            right = self._prepare(str(second))
            if self.numeric:
                left_key = self._numeric_key(left)
                right_key = self._numeric_key(right)
                return (left_key > right_key) - (left_key < right_key)

            previous_locale = None
            try:
                previous_locale = pylocale.setlocale(pylocale.LC_COLLATE)
                pylocale.setlocale(pylocale.LC_COLLATE, self.locale)
                comparison = pylocale.strcoll(left, right)
                return (comparison > 0) - (comparison < 0)
            except Exception:
                return (left > right) - (left < right)
            finally:
                if previous_locale is not None:
                    try:
                        pylocale.setlocale(pylocale.LC_COLLATE, previous_locale)
                    except Exception:
                        previous_locale = None

        def resolvedOptions(self) -> dict[str, Any]:
            return {
                "locale": self.locale,
                "usage": self.usage,
                "sensitivity": self.sensitivity,
                "ignorePunctuation": self.ignorePunctuation,
                "numeric": self.numeric,
                "caseFirst": self.caseFirst,
            }

        def _prepare(self, value: str) -> str:
            if self.ignorePunctuation:
                value = re.sub(r"[^\w\s]", "", value)
            if self.sensitivity == "base":
                value = value.casefold()
            return value

        @staticmethod
        def _numeric_key(value: str) -> list[Any]:
            return [
                int(part) if part.isdigit() else part
                for part in re.split(r"(\d+)", value)
                if part != ""
            ]

    Collator = _Collator

    class _DateTimeFormat:
        def __init__(
            self,
            locales: str | list[str] | None = None,
            options: Mapping[str, Any] | None = None,
        ) -> None:
            options = dict(options or {})
            canonical = Intl.getCanonicalLocales(locales or "en-US")
            self.locale = canonical[0] if canonical else "en-US"
            self.dateStyle = options.get("dateStyle")
            self.timeStyle = options.get("timeStyle")
            self.timeZone = options.get("timeZone")

        @staticmethod
        def supportedLocalesOf(locales: str | list[str]) -> list[str]:
            return Intl.getCanonicalLocales(locales)

        def format(self, value: Any = None) -> str:
            date = self._coerce_datetime(value)
            date_parts = []
            if self.dateStyle is not None or self.timeStyle is None:
                date_parts.append(date.strftime(self._date_format()))
            if self.timeStyle is not None:
                date_parts.append(date.strftime(self._time_format()))
            return ", ".join(part for part in date_parts if part)

        def resolvedOptions(self) -> dict[str, Any]:
            options = {"locale": self.locale}
            if self.dateStyle is not None:
                options["dateStyle"] = self.dateStyle
            if self.timeStyle is not None:
                options["timeStyle"] = self.timeStyle
            if self.timeZone is not None:
                options["timeZone"] = self.timeZone
            return options

        @staticmethod
        def _coerce_datetime(value: Any) -> datetime.datetime:
            if value is None:
                return datetime.datetime.now()
            if isinstance(value, Date):
                return value.date
            if isinstance(value, datetime.datetime):
                return value
            if isinstance(value, (int, float)):
                return datetime.datetime.fromtimestamp(value / 1000)
            return Date(value).date

        def _date_format(self) -> str:
            if self.dateStyle == "full":
                return "%A, %B %d, %Y"
            if self.dateStyle == "long":
                return "%B %d, %Y"
            if self.dateStyle == "medium":
                return "%b %d, %Y"
            return "%m/%d/%y"

        def _time_format(self) -> str:
            if self.timeStyle == "long":
                return "%H:%M:%S %Z"
            if self.timeStyle == "medium":
                return "%H:%M:%S"
            return "%H:%M"

    DateTimeFormat = _DateTimeFormat

    class _NumberFormat:
        _currency_prefixes = {
            "AUD": "$",
            "CAD": "$",
            "CNY": "CNY ",
            "EUR": "EUR ",
            "GBP": "GBP ",
            "JPY": "JPY ",
            "USD": "$",
        }

        def __init__(
            self,
            locales: str | list[str] | None = None,
            options: Mapping[str, Any] | None = None,
        ) -> None:
            options = dict(options or {})
            canonical = Intl.getCanonicalLocales(locales or "en-US")
            self.locale = canonical[0] if canonical else "en-US"
            self.style = options.get("style", "decimal")
            self.currency = options.get("currency")
            self.currencyDisplay = options.get("currencyDisplay", "symbol")
            self.useGrouping = options.get("useGrouping", True)
            default_fraction_digits = 2 if self.style == "currency" else 0
            self.minimumFractionDigits = int(
                options.get("minimumFractionDigits", default_fraction_digits)
            )
            self.maximumFractionDigits = int(
                options.get("maximumFractionDigits", self.minimumFractionDigits)
            )
            if self.maximumFractionDigits < self.minimumFractionDigits:
                self.maximumFractionDigits = self.minimumFractionDigits

        @staticmethod
        def supportedLocalesOf(locales: str | list[str]) -> list[str]:
            return Intl.getCanonicalLocales(locales)

        def format(self, value: int | float | str) -> str:
            number = float(value)
            suffix = ""
            prefix = ""
            if self.style == "percent":
                number *= 100
                suffix = "%"
            elif self.style == "currency":
                prefix = self._currency_prefix()

            formatted = self._format_number(number)
            if number < 0 and prefix:
                return "-" + prefix + formatted.lstrip("-") + suffix
            return prefix + formatted + suffix

        def resolvedOptions(self) -> dict[str, Any]:
            options = {
                "locale": self.locale,
                "style": self.style,
                "useGrouping": self.useGrouping,
                "minimumFractionDigits": self.minimumFractionDigits,
                "maximumFractionDigits": self.maximumFractionDigits,
            }
            if self.currency is not None:
                options["currency"] = self.currency
                options["currencyDisplay"] = self.currencyDisplay
            return options

        def _currency_prefix(self) -> str:
            if self.currency is None:
                return ""
            code = str(self.currency).upper()
            if self.currencyDisplay == "code":
                return f"{code} "
            return self._currency_prefixes.get(code, f"{code} ")

        def _format_number(self, number: float) -> str:
            absolute = abs(number)
            raw = f"{absolute:.{self.maximumFractionDigits}f}"
            integer, _, fraction = raw.partition(".")
            if self.maximumFractionDigits > self.minimumFractionDigits:
                fraction = fraction.rstrip("0")
                if len(fraction) < self.minimumFractionDigits:
                    fraction = fraction.ljust(self.minimumFractionDigits, "0")
            if self.useGrouping:
                integer = f"{int(integer):,}"
            sign = "-" if number < 0 else ""
            if fraction:
                return f"{sign}{integer}.{fraction}"
            return f"{sign}{integer}"

    NumberFormat = _NumberFormat


class Date(Object):
    """javascript date"""

    @staticmethod
    def parse(date_string: Any) -> int:
        """Parses a date string and returns the number of milliseconds since January 1, 1970"""
        d = Date()
        d.parse_date(str(date_string))
        return int(d.date.timestamp() * 1000)

    def __init__(
        self, date: Any = None, *args: Any, formatter: str = "python", **kwargs: Any
    ) -> None:
        """A date object that tries to behave like the Javascript one.

        Python's datetime range is narrower than JavaScript Date, so dates
        outside year 1..9999 are intentionally not represented here.

        Args:
            date (_type_, optional): _description_. Defaults to None.
            formatter (str, optional): _description_. Defaults to 'python'.
        """
        self.formatter = formatter

        # new Date(year, monthIndex, day?, hours?, minutes?, seconds?, ms?)
        # -- monthIndex is 0-based, and each field overflows into the next
        if args and isinstance(date, (int, float)) and all(
            isinstance(a, (int, float)) for a in args
        ):
            parts = [int(date)] + [int(a) for a in args]
            year = parts[0]
            if year < 100:  # JS maps 0..99 to 1900..1999
                year += 1900
            month0 = parts[1] if len(parts) > 1 else 0
            year += month0 // 12
            month0 %= 12
            if month0 < 0:
                year -= 1
                month0 += 12
            day = parts[2] if len(parts) > 2 else 1
            hour = parts[3] if len(parts) > 3 else 0
            minute = parts[4] if len(parts) > 4 else 0
            second = parts[5] if len(parts) > 5 else 0
            millis = parts[6] if len(parts) > 6 else 0
            base = datetime.datetime(year, month0 + 1, 1)
            self.date = base + datetime.timedelta(
                days=day - 1,
                hours=hour,
                minutes=minute,
                seconds=second,
                milliseconds=millis,
            )
            return

        # anything else -- fall back to string parsing
        if args:
            date = " ".join(
                str(p) for p in ([date] if date is not None else []) + list(args)
            ).strip() or None
        if isinstance(date, int):
            self.date = datetime.datetime.fromtimestamp(date)
            return
        # elif isinstance(date, str):
        #     if formatter == 'python':
        #         self.date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        #     elif formatter == 'javascript':
        #         self.date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
        #     else:
        #         raise ValueError('Invalid formatter')
        if date is None:
            self.date = datetime.datetime.now()
        else:
            self.date = self.parse_date(date)

    def __str__(self) -> str:
        return self.toString()

    def toString(self) -> str:
        """Returns a string representation of the date"""
        if self.formatter == "python":
            return self.date.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return self.date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")  # js

    def parse_date(self, date_string: Any) -> datetime.datetime:
        class MyParserInfo(parserinfo):
            def convertyear(self, year: int, *args: Any, **kwargs: Any) -> int:
                # browser ticks over at approx 30 years (1950 when I check in chrome)
                if year < 100 and year > 30:
                    year += 1900
                return year

        self.date = parse(date_string, MyParserInfo())
        return self.date

    def getDate(self) -> int:
        """Returns the day of the month (from 1-31)"""
        return self.date.day

    def getDay(self) -> int:
        """Returns the day of the week (from 0-6 : Sunday-Saturday)

        Returns:
            int: An integer number, between 0 and 6, corresponding to the day of the week for the given date,
            according to local time: 0 for Sunday, 1 for Monday, 2 for Tuesday, and so on
        """
        pyweekday = self.date.isoweekday()
        return pyweekday if pyweekday < 6 else 0

    def getFullYear(self) -> int:
        """Returns the year"""
        return self.date.year

    def getHours(self) -> int:
        """Returns the hour (from 0-23)"""
        return self.date.hour

    def getMilliseconds(self) -> int:
        """Returns the milliseconds (from 0-999)"""
        return round(self.date.microsecond / 1000)

    def getMinutes(self) -> int:
        """Returns the minutes (from 0-59)"""
        return self.date.minute

    def getMonth(self) -> int:
        """Returns the month (from 0-11)"""
        return self.date.month - 1

    def getSeconds(self) -> int:
        """Returns the seconds (from 0-59)"""
        return self.date.second

    def getTime(self) -> int:
        """Returns A number representing the milliseconds elapsed between 1 January 1970 00:00:00 UTC and self.date"""
        epoch = datetime.datetime(1970, 1, 1)
        self.date = self.date.replace(tzinfo=timezone.utc)
        epoch = epoch.replace(tzinfo=timezone.utc)
        return int((self.date - epoch).total_seconds() * 1000)

    def getTimezoneOffset(self) -> int:
        """Returns the difference, in minutes, between a date as evaluated in the UTC time zone,
        and the same date as evaluated in the local time zone"""
        local_date = self.date.astimezone()
        offset = local_date.utcoffset() or datetime.timedelta()
        return int(-(offset.total_seconds() / 60))

    def getUTCDate(self) -> int:
        """Returns the day of the month, according to universal time (from 1-31)"""
        utc_date = self.date.astimezone(timezone.utc) if self.date.tzinfo else self.date
        return utc_date.day

    def getUTCDay(self) -> int:
        """Returns the day of the week, according to universal time (from 0-6)"""
        utc_date = self.date.astimezone(timezone.utc) if self.date.tzinfo else self.date
        pyweekday = utc_date.isoweekday()
        return pyweekday if pyweekday < 6 else 0

    def getUTCFullYear(self) -> int:
        """Returns the year, according to universal time"""
        utc_date = self.date.astimezone(timezone.utc) if self.date.tzinfo else self.date
        return utc_date.year

    def getUTCHours(self) -> int:
        """Returns the hour, according to universal time (from 0-23)"""
        utc_date = self.date.astimezone(timezone.utc) if self.date.tzinfo else self.date
        return utc_date.hour

    def getUTCMilliseconds(self) -> int:
        """Returns the milliseconds, according to universal time (from 0-999)"""
        utc_date = self.date.astimezone(timezone.utc) if self.date.tzinfo else self.date
        return round(utc_date.microsecond / 1000)

    def getUTCMinutes(self) -> int:
        """Returns the minutes, according to universal time (from 0-59)"""
        utc_date = self.date.astimezone(timezone.utc) if self.date.tzinfo else self.date
        return utc_date.minute

    def getUTCMonth(self) -> int:
        """Returns the month, according to universal time (from 0-11)"""
        utc_date = self.date.astimezone(timezone.utc) if self.date.tzinfo else self.date
        return utc_date.month - 1

    def getUTCSeconds(self) -> int:
        """Returns the seconds, according to universal time (from 0-59)"""
        utc_date = self.date.astimezone(timezone.utc) if self.date.tzinfo else self.date
        return utc_date.second

    def getYear(self) -> int:
        """Deprecated. Use the getFullYear() method instead"""
        return self.date.year

    @staticmethod
    def now() -> int:
        """Returns the number of milliseconds since midnight Jan 1, 1970"""
        return round(_time.time() * 1000)

    def setDate(self, day: int) -> int:
        """Sets the day of the month of a date object

        Args:
            day (int): An integer representing the day of the month.

        Returns:
            int: milliseconds between epoch and updated date.
        """
        first_of_month = self.date.replace(day=1)
        self.date = first_of_month + datetime.timedelta(days=int(day) - 1)
        return self.getTime()

    def setFullYear(
        self,
        yearValue: int,
        monthValue: int | None = None,
        dateValue: int | None = None,
    ) -> int:
        """Sets the year of a date object

        Args:
            yearValue (_type_): _description_
            monthValue (int, optional): _description_. Defaults to None.
            dateValue (int, optional): _description_. Defaults to None.

        Returns:
            int: milliseconds between epoch and updated date.
        """
        self.date = self.date.replace(year=int(yearValue))
        if monthValue is not None:
            self.setMonth(monthValue)
        if dateValue is not None:
            self.setDate(dateValue)
        return self.getTime()

    def setHours(
        self,
        hoursValue: int,
        minutesValue: int | None = None,
        secondsValue: int | None = None,
        msValue: int | None = None,
    ) -> int:
        """Sets the hour of a date object

        Args:
            hoursValue (int): an integer between 0 and 23
            minutesValue (int, optional): an integer between 0 and 59
            secondsValue (int, optional): an integer between 0 and 59,
            msValue (int, optional): a number between 0 and 999,

        Returns:
            int: milliseconds between epoch and updated date.
        """
        while hoursValue > 23:
            current_day = self.date.day
            self.setDate(current_day + 1)
            hoursValue -= 24

        while hoursValue < 0:
            current_day = self.date.day
            self.setDate(current_day - 1)
            hoursValue += 24

        self.date = self.date.replace(hour=int(hoursValue))
        if minutesValue is not None:
            self.setMinutes(minutesValue)
        if secondsValue is not None:
            self.setSeconds(secondsValue)
        if msValue is not None:
            self.setMilliseconds(msValue)
        return self.getTime()

    def setMilliseconds(self, milliseconds: int) -> int:
        """Sets the milliseconds of a date object

        Args:
            milliseconds (int): Milliseconds to set i.e 123

        Returns:
            int: milliseconds between epoch and updated date.
        """
        microseconds = int(milliseconds) * 1000
        self.date = self.date.replace(microsecond=microseconds)
        return self.getTime()

    def setMinutes(
        self,
        minutesValue: int,
        secondsValue: int | None = None,
        msValue: int | None = None,
    ) -> int:
        """Set the minutes of a date object

        Args:
            minutesValue (int, optional): an integer between 0 and 59
            secondsValue (int, optional): an integer between 0 and 59,
            msValue (int, optional): a number between 0 and 999,

        Returns:
            int: milliseconds between epoch and updated date.
        """
        while minutesValue > 59:
            current_hour = self.date.hour
            self.setHours(current_hour + 1)
            minutesValue -= 60

        while minutesValue < 0:
            current_hour = self.date.hour
            self.setHours(current_hour - 1)
            minutesValue += 60

        self.date = self.date.replace(minute=int(minutesValue))
        if secondsValue is not None:
            self.setSeconds(secondsValue)
        if msValue is not None:
            self.setMilliseconds(msValue)
        return self.getTime()

    def setMonth(self, monthValue: int, dayValue: int | None = None) -> int:
        """Sets the month of a date object

        Args:
            monthValue (int): a number from 0 to 11 indicating the month.
            dayValue (int, optional): an optional day of the month. Defaults to 0.

        Returns:
            int: milliseconds between epoch and updated date.
        """
        while monthValue < 0:
            current_year = self.date.year
            self.setFullYear(current_year - 1)
            monthValue += 12

        while monthValue > 11:
            current_year = self.date.year
            self.setFullYear(current_year + 1)
            monthValue -= 12

        if monthValue >= 0:
            # if the new month is less days. it will affect the result. i.e
            # js would progress to the next month and add the spare left over days
            # So if the current day is 31st August 2016. and you setMonth(1), it would be 2nd March.
            # as there's 29 days in February that year.
            # in python it will error as the new month has less days.
            # so we need to change it first.
            next_month_total_days = calendar.monthrange(self.date.year, monthValue + 1)[
                1
            ]
            leftovers = next_month_total_days - self.getDate()
            if leftovers < 0:
                leftovers = abs(leftovers)
                self.date = self.date.replace(
                    day=int(leftovers)
                )  # reset the day for now to not error
                self.date = self.date.replace(month=int(monthValue + 1))
                self.date = self.date.replace(day=leftovers)
            else:
                self.date = self.date.replace(month=int(monthValue + 1))

        if dayValue is not None:
            self.setDate(dayValue)
        return self.getTime()

    def setSeconds(self, secondsValue: int, msValue: int | None = None) -> int:
        """Sets the seconds of a date object

        Args:
            secondsValue (int): _description_
            msValue (int, optional): _description_. Defaults to None.

        Returns:
            int: milliseconds between epoch and updated date.
        """
        self.date = self.date.replace(second=int(secondsValue))
        if msValue is not None:
            self.setMilliseconds(msValue)
        return self.getTime()

    def setTime(self, milliseconds: int | None = None, tz: Any = None) -> int | None:
        """Sets the date and time of a date object

        Args:
            milliseconds (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        if milliseconds is None:
            self.date = datetime.datetime.now(tz)
        else:
            self.date = datetime.datetime.fromtimestamp(milliseconds / 1000, tz)
        return self.getTime()

    def setUTCDate(self, day: int) -> int:
        """Sets the day of the month of a date object, according to universal time"""
        self.setDate(day)
        return self.getTime()

    def setUTCFullYear(self, year: int) -> int:
        """Sets the year of a date object, according to universal time"""
        self.setFullYear(year)
        return self.getTime()

    def setUTCHours(self, hour: int) -> int:
        """Sets the hour of a date object, according to universal time"""
        self.setHours(hour)
        return self.getTime()

    def setUTCMilliseconds(self, milliseconds: int) -> int:
        """Sets the milliseconds of a date object, according to universal time"""
        self.setMilliseconds(milliseconds)
        return self.getTime()

    def setUTCMinutes(self, minutes: int) -> int:
        """Set the minutes of a date object, according to universal time"""
        self.setMinutes(minutes)
        return self.getTime()

    def setUTCMonth(self, month: int) -> int:
        """Sets the month of a date object, according to universal time"""
        self.setMonth(month)
        return self.getTime()

    def setUTCSeconds(self, seconds: int) -> int:
        """Set the seconds of a date object, according to universal time"""
        self.setSeconds(seconds)
        return self.getTime()

    def setYear(self, year: int) -> int:
        """Deprecated. Use the setFullYear() method instead"""
        self.date = self.date.replace(year=int(year))
        return self.getTime()

    def toDateString(self) -> str:
        """Converts the date portion of a Date object into a readable string"""
        return self.date.strftime("%Y-%m-%d")

    def toUTCString(self) -> str:
        """Converts a Date object to a string, according to universal time"""
        return self.date.strftime("%Y-%m-%d %H:%M:%S")

    def toGMTString(self) -> str:
        """Deprecated. Use the toUTCString() method instead"""
        return self.toUTCString()

    def toJSON(self) -> str:
        """Returns the date as a string, formatted as a JSON date"""
        return json.dumps(self.date.strftime("%Y-%m-%d"))

    def toISOString(self) -> str:
        """Returns the date as a string, using the ISO standard"""
        return self.date.strftime("%Y-%m-%d")

    def toLocaleDateString(self) -> str:
        """Returns the date portion of a Date object as a string, using locale conventions"""
        return self.date.strftime("%x")

    def toLocaleString(self) -> str:
        """Converts a Date object to a string, using locale conventions"""
        return self.date.strftime("%x")

    def toLocaleTimeString(self) -> str:
        """Returns the time portion of a Date object as a string, using locale conventions"""
        return self.date.strftime("%X")

    def toTimeString(self) -> str:
        """Converts the time portion of a Date object to a string"""
        return self.date.strftime("%X")

    @staticmethod
    def UTC(
        year: int,
        month: int = 0,
        day: int = 1,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0,
        ms: int = 0,
    ) -> int:
        """``Date.UTC(year, monthIndex, ...)`` -- milliseconds since the epoch
        for the given UTC date. ``monthIndex`` is 0-based and fields overflow,
        as in JavaScript."""
        year = int(year)
        if year < 100:
            year += 1900
        month = int(month)
        year += month // 12
        month %= 12
        base = datetime.datetime(year, month + 1, 1, tzinfo=timezone.utc)
        moment = base + datetime.timedelta(
            days=int(day) - 1,
            hours=int(hours),
            minutes=int(minutes),
            seconds=int(seconds),
            milliseconds=int(ms),
        )
        return int(moment.timestamp() * 1000)

    def valueOf(self) -> int:
        """Returns the primitive numeric value of the date."""
        return self.getTime()

    def _comparison_value(self) -> float:
        date = self.date
        if date.tzinfo is None:
            date = date.replace(tzinfo=timezone.utc)
        return date.timestamp()

    @staticmethod
    def _coerce_comparison_value(other: Any) -> float | None:
        if isinstance(other, Date):
            return other._comparison_value()
        if isinstance(other, datetime.datetime):
            if other.tzinfo is None:
                other = other.replace(tzinfo=timezone.utc)
            return other.timestamp()
        return None

    def __eq__(self, other: Any) -> bool:
        other_value = self._coerce_comparison_value(other)
        if other_value is None:
            return False
        return self._comparison_value() == other_value

    def __ne__(self, other: Any) -> bool:
        return not self == other

    def __lt__(self, other: Any) -> bool:
        other_value = self._coerce_comparison_value(other)
        if other_value is None:
            return NotImplemented
        return self._comparison_value() < other_value

    def __le__(self, other: Any) -> bool:
        other_value = self._coerce_comparison_value(other)
        if other_value is None:
            return NotImplemented
        return self._comparison_value() <= other_value

    def __gt__(self, other: Any) -> bool:
        other_value = self._coerce_comparison_value(other)
        if other_value is None:
            return NotImplemented
        return self._comparison_value() > other_value

    def __ge__(self, other: Any) -> bool:
        other_value = self._coerce_comparison_value(other)
        if other_value is None:
            return NotImplemented
        return self._comparison_value() >= other_value


class Screen:
    """Lightweight representation of the browser Screen object."""

    def __init__(
        self,
        width: int = 1024,
        height: int = 768,
        *,
        availWidth: int | None = None,
        availHeight: int | None = None,
        colorDepth: int = 24,
        pixelDepth: int | None = None,
    ) -> None:
        self.availLeft = 0
        self.availTop = 0
        self.availWidth = width if availWidth is None else int(availWidth)
        self.availHeight = height if availHeight is None else int(availHeight)
        self.colorDepth = int(colorDepth)
        self.height = int(height)
        self.left = 0
        self.pixelDepth = self.colorDepth if pixelDepth is None else int(pixelDepth)
        self.top = 0
        self.width = int(width)
        self.orientation = None


class ProgramKilled(Exception):
    """Raised when a scheduled background job is asked to stop."""


class Job(threading.Thread):
    def __init__(
        self,
        interval: datetime.timedelta,
        execute: Callable[..., Any],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        threading.Thread.__init__(self)
        self.daemon = False
        self.stopped = threading.Event()
        self.interval = interval
        self.execute = execute
        self.args = args
        self.kwargs = kwargs

    def stop(self) -> None:
        self.stopped.set()
        self.join()

    def run(self) -> None:
        while not self.stopped.wait(self.interval.total_seconds()):
            self.execute(*self.args, **self.kwargs)

    # def __str__(self):
    #     return "Job every %s" % self.interval


class SetInterval:
    def signal_handler(self, signum: int, frame: Any) -> None:
        raise ProgramKilled

    def __init__(
        self, function: Callable[..., Any], time: int | float, *args: Any, **kwargs: Any
    ) -> None:
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)
        self.job = Job(
            datetime.timedelta(microseconds=time * 1000), function, *args, **kwargs
        )
        self.job.start()

    # def stop(self):
    #     self.job.stop()


class Promise:
    # undocumented - warning. use at own risk
    def __init__(
        self,
        func: (
            Callable[[Callable[[Any], Promise], Callable[[Any], Promise]], Any] | None
        ) = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.data: Any = None
        self.state = "pending"  # fullfilled, rejected
        self._then_callbacks: list[Callable[[Any], Any]] = []
        self._catch_callbacks: list[Callable[[Any], Any]] = []
        if func is not None:
            func(self.resolve, self.reject)

    def then(self, func: Callable[[Any], Any] | None) -> Promise:
        if func is None:
            return self
        if self.state == "fulfilled":
            self._run_then(func)
        elif self.state == "pending":
            self._then_callbacks.append(func)
        return self

    def catch(self, error: Any) -> Promise:
        if not callable(error):
            return self
        if self.state == "rejected":
            self._run_catch(error)
        elif self.state == "pending":
            self._catch_callbacks.append(error)
        return self

    def resolve(self, data: Any) -> Promise:
        if self.state != "pending":
            return self
        self.data = data
        self.state = "fulfilled"
        for callback in list(self._then_callbacks):
            if self.state != "fulfilled":
                break
            self._run_then(callback)
        self._then_callbacks.clear()
        return self

    def reject(self, data: Any) -> Promise:
        if self.state not in ("pending", "fulfilled"):
            return self
        self.data = data
        self.state = "rejected"
        for callback in list(self._catch_callbacks):
            self._run_catch(callback)
        self._catch_callbacks.clear()
        return self

    def _run_then(self, func: Callable[[Any], Any]) -> None:
        try:
            self.data = func(self.data)
        except Exception as exc:
            self.reject(exc)

    def _run_catch(self, func: Callable[[Any], Any]) -> None:
        self.data = func(self.data)

    # def __str__(self):
    #     try:
    #         return self.data.text
    #     except Exception as e:
    #     return str(self)


class FetchedSet:  # not a promise
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.results: list[Any] = []

    def __getitem__(self, index: int) -> Any:
        return self.results[index]

    def oncomplete(
        self, func: Callable[[list[Any]], Any]
    ) -> None:  # runs once all results are back
        func(self.results)
        return

    # def __call__(self, func):
    #     self.results.append(func)


class Window:
    """window"""

    localStorage = Storage()
    location = ""
    screen = Screen()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # self.console = dom.console
        # self.document = Document
        # globals()?
        # dir()?
        # locals()?
        try:
            self.screen = Screen()
        except AttributeError:
            return

    @staticmethod
    def alert(msg: Any) -> None:
        """Displays an alert box with a message and an OK button"""
        print(msg)
        return

    @staticmethod
    def prompt(msg: Any, default_text: str = "") -> str:
        """Displays a dialog box that prompts the visitor for input"""
        print(msg)
        data = input()
        return data

    setTimeout = Global.setTimeout
    clearTimeout = Global.clearTimeout

    @staticmethod
    def clearInterval(job: Job) -> None:
        job.stop()

    @staticmethod
    def setInterval(
        function: Callable[..., Any], time: int | float, *args: Any, **kwargs: Any
    ) -> Job:
        interval_ID = SetInterval(function, time, *args, **kwargs)
        return interval_ID.job

    @staticmethod
    def _do_request(url: str, f: Any = None, **kwargs: Any) -> Any:
        # private - don't use directly. use one of the fetch methods
        try:
            # r = requests.get(url, timeout=3)
            from requests import Request, Session

            method = "GET"
            if "method" in kwargs:
                method = kwargs["method"]

            if "callback_function" in kwargs:
                del kwargs["callback_function"]

            if "error_handler" in kwargs:
                del kwargs["error_handler"]

            s = Session()
            req = Request(method, url)
            prepped = s.prepare_request(req)
            r = s.send(prepped, **kwargs)
            s.close()

            if f is not None and type(f) is FetchedSet:
                f.results.append(r)

            return r
        except Exception as e:
            print(f"Request Failed for URL: {url}", e)
            return None

    @staticmethod
    def fetch(url: str, **kwargs: Any) -> Promise:
        # undocumented - warning. use at own risk
        # note - kinda pointless atm. just use requests directly and you wont have to muck about with a Promise
        if type(url) is not str:
            raise ValueError(
                "fetch takes a single url string. use fetch_set, fetch_threaded or fetch_pooled"
            )
        f = Promise()
        r = window._do_request(url, f, **kwargs)
        return f.resolve(r)

    @staticmethod
    async def fetch_async(url: str, **kwargs: Any) -> Any:
        """Fetch a URL without blocking the current asyncio event loop."""
        import asyncio
        from functools import partial

        if type(url) is not str:
            raise ValueError("fetch_async takes a single url string")
        loop = asyncio.get_running_loop()
        request = partial(window._do_request, url, None, **kwargs)
        return await loop.run_in_executor(None, request)

    @staticmethod
    def fetch_set(
        urls: str | list[str],
        callback_function: Callable[[Any], Any] | None = None,
        error_handler: Callable[[Any], Any] | None = None,
        **kwargs: Any,
    ) -> FetchedSet:
        # undocumented - warning. use at own risk
        # note - still blocks. just gets all before continuing
        # problems - all urls can only have 1 associated callback, error and set of kwargs
        if type(urls) is str:
            urls = [urls]  # leniency
        f = FetchedSet()
        for url in urls:
            r = window.fetch(url, **kwargs).then(callback_function)
            f.results.append(r.data)
        return f

    @staticmethod
    def fetch_threaded(
        urls: str | list[str],
        callback_function: Callable[[Any], Any] | None = None,
        error_handler: Callable[[Any], Any] | None = None,
        **kwargs: Any,
    ) -> FetchedSet:
        # undocumented - warning. use at own risk
        # note - still blocks. just gets all before continuing using threads
        # problems - all urls can only have 1 associated callback, error and set of kwargs
        if type(urls) is str:
            urls = [urls]  # leniency
        f = FetchedSet()
        jobs = []
        for url in urls:
            thread = threading.Thread(
                target=lambda url=url: window._do_request(url, f, **kwargs)
            )
            thread.daemon = True
            jobs.append(thread)
        for job in jobs:
            job.start()
        for job in jobs:
            job.join()
        return f

    @staticmethod
    def fetch_pooled(
        urls: str | list[str],
        callback_function: Callable[[Any], Any] | None = None,
        error_handler: Callable[[Any], Any] | None = None,
        **kwargs: Any,
    ) -> FetchedSet:
        # undocumented - warning. use at own risk
        # note - still blocks. just gets all before continuing using a pool
        # problems - all urls can only have 1 associated callback, error and set of kwargs
        if type(urls) is str:
            urls = [urls]  # leniency
        f = FetchedSet()

        def _do_request_wrapper(obj: dict[str, Any]) -> None:
            url = obj["url"]
            f = obj["f"]
            kwargs = obj["k"]
            kwargs["callback_function"] = obj["c"]
            kwargs["error_handler"] = obj["e"]
            window._do_request(url, f, **kwargs)

        p = Pool()
        jobs = [
            {
                "url": url,
                "f": f,
                "c": callback_function,
                "e": error_handler,
                "k": kwargs,
            }
            for url in urls
        ]
        p.map(_do_request_wrapper, jobs)
        p.close()
        p.join()
        return f

    @staticmethod
    def btoa(dataString: str) -> bytes:
        """Encodes a string in base-64"""
        import base64

        dataBytes = dataString.encode("utf-8")
        encoded = base64.b64encode(dataBytes)
        return encoded

    @staticmethod
    def atob(dataString: str | bytes) -> str:
        """Decodes a base-64 encoded string"""
        import base64

        return base64.b64decode(dataString).decode()

    @staticmethod
    def requestAnimationFrame(callback: Callable[[float], Any]) -> Any:
        """[requests a frame of an animation]

        Args:
            callback (callable): [the callback function]

        Returns:
            [type]: [description]
        """
        perf = Global.performance.now()
        return callback(perf)


# these probably should have been on global. will see about moving them later
setInterval = Window.setInterval
clearInterval = Window.clearInterval

Global.setInterval = Window.setInterval
Global.clearInterval = Window.clearInterval

window = Window
Global.window = window


class Array:
    """javascript array"""

    @staticmethod
    def from_(obj: Any) -> Array:
        """Creates a new Array instance from an array-like or iterable object."""
        if isinstance(obj, Array):
            return Array(*obj.args)
        if isinstance(obj, (list, tuple)):
            return Array._new(obj)
        if isinstance(obj, dict):
            return Array._new(obj.items())
        if isinstance(obj, str):
            return Array._new(obj)
        if hasattr(obj, "__iter__"):
            return Array._new(obj)
        length = getattr(obj, "length", None)
        if isinstance(length, int):
            return Array._new([None] * length)
        return Array._new([])

    @classmethod
    def _new(cls, items: Any) -> "Array":
        """A literal array from ``items`` -- bypasses the ``Array(n)`` /
        ``Array([...])`` casting special cases in ``__init__``."""
        arr = cls.__new__(cls)
        arr.args = list(items)
        arr.prototype = arr
        return arr

    @staticmethod
    def of(*args: Any) -> Array:
        """A new array with exactly the given elements -- unlike ``Array(n)``,
        ``Array.of(7)`` is ``[7]``, not a length-7 array."""
        return Array._new(args)

    def __init__(self, *args: Any) -> None:
        """[An Array that behaves like a js array]"""
        # casting
        if len(args) == 1:
            if isinstance(args[0], list):
                self.args = args[0]
                return
            elif isinstance(args[0], int):
                # self.args = [None] * args[0]
                # self.args = [null()] * args[0]
                self.args = [""] * args[0]
                return
        self.args = list(args)
        self.prototype = self

    def __getitem__(self, index: "int | slice") -> Any:
        if isinstance(index, slice):
            return self.args[index]
        # JS bracket access: the element at a valid position, else ``undefined``
        # (a negative index is not a valid array index in JS -- use ``.at()``).
        return self.args[index] if 0 <= index < len(self.args) else undefined

    def __getattribute__(self, name: str) -> Any:
        try:
            return super().__getattribute__(name)
        except AttributeError:
            # if its a list method get it from args
            if name in dir(list):
                return getattr(self.args, name)

    def __setitem__(self, index: int, value: Any) -> None:
        self.args[index] = value

    def __add__(self, value: Array | list[Any]) -> list[Any]:
        if isinstance(value, int):
            raise ValueError("int not supported")
        if isinstance(value, Array):
            self.args = self.args + value.args
        if isinstance(value, list):
            self.args = self.args + value
        return self.args

    def __len__(self) -> int:
        return len(self.args)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Array):
            return self.args == other.args
        if isinstance(other, list):
            return self.args == other
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __repr__(self) -> str:
        return str(self.args)

    def __iter__(self) -> Iterator[Any]:
        for i in self.args:
            yield i
        # self.args.__iter__()

    def __sub__(self, value: "Array | list[Any]") -> list[Any]:
        if isinstance(value, int):
            raise ValueError("int not supported")
        other = value.args if isinstance(value, Array) else list(value)
        self.args = [item for item in self.args if item not in other]
        return self.args

    @staticmethod
    def _stringify_join_item(value: Any) -> str:
        if value is None:
            return ""
        if isinstance(value, Array):
            return value.join()
        if isinstance(value, (list, tuple)):
            return Array(list(value)).join()
        if isinstance(value, dict):
            return "[object Object]"
        return str(value)

    def toString(self) -> str:
        """Converts an array to a JavaScript-style comma-separated string."""
        return self.join()

    def toSource(self) -> list[Any]:
        """
        Returns the source array.
        """
        return list(self.args)

    @property
    def length(self) -> int:
        """Sets or returns the number of elements in an array"""
        return len(self.args)

    def concat(self, *args: Any) -> "Array":
        """A new array = this array plus each argument, with array arguments
        spread one level deep and everything else appended (JavaScript). The
        original array is not modified."""
        result = list(self.args)
        for arg in args:
            if isinstance(arg, Array):
                result.extend(arg.args)
            elif isinstance(arg, list):
                result.extend(arg)
            else:
                result.append(arg)
        return Array._new(result)

    def flat(self, depth: int = 1) -> list[Any]:
        """[Flattens an array into a single-dimensional array or a depth of arrays]"""
        if depth < 0:
            raise ValueError("depth must be greater than or equal to 0")

        def _flatten(items: list[Any], level: int) -> list[Any]:
            flattened: list[Any] = []
            for item in items:
                if level > 0 and isinstance(item, Array):
                    flattened.extend(_flatten(item.args, level - 1))
                elif level > 0 and isinstance(item, list):
                    flattened.extend(_flatten(item, level - 1))
                else:
                    flattened.append(item)
            return flattened

        return _flatten(self.args, depth)

    def flatMap(self, fn: Callable[..., Any] | None = None) -> Array:
        """[Maps a function over an array and flattens the result]"""
        it = _js_iteratee(fn)
        mapped = [it(v, i, self.args) for i, v in enumerate(self.args)]
        return Array(*Array(mapped).flat(1))

    def fill(
        self, value: Any = None, start: int | None = None, end: int | None = None
    ) -> list[Any]:
        """[Fills elements of an array from a start index to an end index with a static value]"""
        length = len(self.args)
        start = _clamp_js_index(0 if start is None else int(start), length)
        end = length if end is None else _clamp_js_index(int(end), length)
        for i in range(start, end):
            self.args[i] = value
        return self.args

    def groupBy(self, callback) -> dict:
        """[Groups the elements of an array according to the result of calling a callback function on each element]

        Args:
            callback (callable): [the callback recieves the following paramters(value, index, target)]

        Returns:
            [dict]: [a dictionary of arrays]
        """
        groups: dict[Any, Any] = {}
        for i in range(len(self.args)):
            key = callback(self.args[i], i, self.args)
            if key in groups:
                groups[key].append(self.args[i])
            else:
                groups[key] = [self.args[i]]
        return groups

    # def groupByToMap(self, callback):
    #     """[returns a Map object]
    #     """
    #     groups = {}
    #     for i in range(len(self.args)):
    #         key = callback(self.args[i], i, self.args)
    #         if key in groups:
    #             groups[key].append(self.args[i])
    #         else:
    #             groups[key] = [self.args[i]]
    #     return Map(groups)

    def findLast(self, callback: Callable[..., bool] | None = None) -> Any:
        """[Returns the last element in an array that passes a test]"""
        it = _js_iteratee(callback)
        for i in range(len(self.args) - 1, -1, -1):
            if it(self.args[i], i, self.args):
                return self.args[i]
        return None

    def findLastIndex(self, callback: Callable[..., bool] | None = None) -> int:
        """[Returns the last index of an element in an array that passes a test]"""
        it = _js_iteratee(callback)
        for i in range(len(self.args) - 1, -1, -1):
            if it(self.args[i], i, self.args):
                return i
        return -1

    def includes(self, value: Any) -> bool:
        """[Check if an array contains the specified item

        Args:
            value ([any]): [any value]

        Returns:
            [bool]: [a boolean]
        """
        return any(_js_same_value_zero(item, value) for item in self.args)

    def indexOf(self, value: Any, fromIndex: int = 0) -> int:
        """Search the array for an element and returns its position"""
        start = _clamp_js_index(int(fromIndex), len(self.args))
        for index in range(start, len(self.args)):
            if _js_strictish_equal(self.args[index], value):
                return index
        return -1

    @staticmethod
    def isArray(thing: Any) -> bool:
        """[Checks whether an object is an array]

        Args:
            thing ([type]): [thing to check]

        Returns:
            [bool]: [True if the object is list, tuple or Array]
        """
        if isinstance(thing, (list, tuple, Array)):
            return True
        else:
            return False

    def join(self, value: str = ",") -> str:
        """Joins all elements of an array into a string."""
        separator = "," if value is None else str(value)
        return separator.join(self._stringify_join_item(x) for x in self.args)

    def lastIndexOf(self, value: Any, fromIndex: int | None = None) -> int:
        """Search the array for an element, starting at the end, and returns its position"""
        length = len(self.args)
        if length == 0:
            return -1
        if fromIndex is None:
            start = length - 1
        else:
            start = int(fromIndex)
            if start < 0:
                start = length + start
            else:
                start = min(start, length - 1)
        if start < 0:
            return -1
        for index in range(start, -1, -1):
            if _js_strictish_equal(self.args[index], value):
                return index
        return -1

    def pop(self) -> Any:
        """Removes and returns the last element, or ``undefined`` when empty."""
        return self.args.pop() if self.args else undefined

    def push(self, value: Any) -> int:
        """Adds new elements to the end of an array, and returns the new length"""
        self.args.append(value)
        return len(self.args)

    def reverse(self) -> list[Any]:
        """Reverses the order of the elements in an array"""
        self.args = self.args[::-1]
        return self.args

    def slice(
        self, start: int = 0, stop: int | None = None, step: int = 1
    ) -> list[Any]:
        """[Selects a part of an array, and returns the new array]

        Args:
            start ([int]): [index to slice from]
            stop ([int], optional): [index to slice to]. Defaults to end of the array.
            step (int, optional): [description]. Defaults to 1.

        Returns:
            [type]: [new array]
        """
        if stop is None:
            stop = len(self.args)
        return self.args[slice(start, stop, step)]

    def splice(
        self, start: int, delete_count: int | None = None, *items: Any
    ) -> list[Any]:
        """Selects a part of an array, and returns the new array"""
        length = len(self.args)
        start = _clamp_js_index(int(start), length)
        if delete_count is None:
            delete_count = length - start
        else:
            delete_count = min(max(int(delete_count), 0), length - start)

        stop = start + delete_count
        removed = self.args[start:stop]
        self.args[start:stop] = items
        return removed
        # return self.args

    def unshift(self, *args: Any) -> int:
        """[Adds new elements to the beginning of an array, and returns the new length]

        Returns:
            [int]: [the length of the array]
        """
        for i in reversed(args):
            self.args.insert(0, i)
        return len(self.args)

    def shift(self) -> Any:
        """Removes and returns the first element, or ``undefined`` when empty."""
        if not self.args:
            return undefined
        return self.args.pop(0)

    def map(self, func: Callable[..., Any] | None = None) -> list[Any]:
        """[Creates a new array with the result of calling a function for each array element]

        Args:
            func ([type]): [a function to call on each array element]

        Returns:
            [list]: [a new array]
        """
        it = _js_iteratee(func)
        return [it(value, i, self.args) for i, value in enumerate(self.args)]

    def some(self, func: Callable[..., bool] | None = None) -> bool:
        """Checks if any of the elements in an array pass a test"""
        it = _js_iteratee(func)
        return any(it(value, i, self.args) for i, value in enumerate(self.args))

    def sort(self, func: Callable[..., Any] | None = None) -> list[Any]:
        """Sorts the elements of an array"""

        if func is not None:
            from functools import cmp_to_key

            self.args.sort(key=cmp_to_key(func))
            return self.args

        def comp(o: Any) -> str:
            return str(o)

        # manually sort lexicographically
        for i in range(len(self.args)):
            for j in range(i + 1, len(self.args)):
                if comp(self.args[i]) > comp(self.args[j]):
                    self.args[i], self.args[j] = self.args[j], self.args[i]
        return self.args

    def toReversed(self) -> "Array":
        """A reversed copy (the original array is left unchanged) -- ES2023."""
        return Array._new(reversed(self.args))

    def toSorted(self, func: Callable[..., Any] | None = None) -> "Array":
        """A sorted copy (the original array is left unchanged) -- ES2023."""
        if func is not None:
            from functools import cmp_to_key

            return Array._new(sorted(self.args, key=cmp_to_key(func)))
        return Array._new(sorted(self.args, key=str))

    def toSpliced(
        self, start: int, deleteCount: int | None = None, *items: Any
    ) -> "Array":
        """A copy with a splice applied (the original is unchanged) -- ES2023."""
        copy = list(self.args)
        if deleteCount is None:
            deleteCount = len(copy) - start
        copy[start : start + deleteCount] = items
        return Array._new(copy)

    def with_(self, index: int, value: Any) -> "Array":
        """A copy with ``index`` replaced by ``value`` -- ES2023 ``Array#with``
        (``with`` is a Python keyword)."""
        copy = list(self.args)
        copy[index] = value
        return Array._new(copy)

    def reduce(self, cb: Any = None, initialValue: Any = None) -> Any:
        """Reduces the array to a single value (going left-to-right)
        callback recieve theses parameters: previousValue, currentValue, currentIndex, array
        """
        _require_callback(cb)
        callback: Callable[..., Any] = cb
        arguments = self.args
        offset = 0
        if initialValue is None:
            if not arguments:
                raise TypeError("Reduce of empty array with no initial value")
            initialValue = arguments[0]
            offset = 1

        acc = initialValue
        n = _positional_arity(callback, 4)
        if n == 2:  # the common `(acc, value) => ...`
            for i in range(offset, len(arguments)):
                acc = callback(acc, arguments[i])
        elif n is None or n >= 4:
            for i in range(offset, len(arguments)):
                acc = callback(acc, arguments[i], i, self.args)
        elif n == 3:
            for i in range(offset, len(arguments)):
                acc = callback(acc, arguments[i], i)
        else:
            for i in range(offset, len(arguments)):
                acc = callback(acc)
        return acc

    def reduceRight(
        self, callback: Callable[..., Any] | None = None, initialValue: Any = None
    ) -> Any:
        """Reduces the array to a single value (going right-to-left)
        callback recieve theses parameters: previousValue, currentValue, currentIndex, array
        """
        _require_callback(callback)
        arguments = self.args
        last = len(arguments) - 1
        if initialValue is None:
            if not arguments:
                raise TypeError("Reduce of empty array with no initial value")
            initialValue = arguments[last]
            last -= 1

        step = _js_reducer(callback)
        for i in range(last, -1, -1):
            initialValue = step(initialValue, arguments[i], i, self.args)
        return initialValue

    def filter(self, func: Callable[..., bool] | None = None) -> list[Any]:
        """
        Creates a new array with every element in an array that pass a test
        i.e. even_numbers = someArr.filter( lambda x: x % 2 == 0 )
        """
        # written by .ai (https://6b.eleuther.ai/)
        # filtered = []
        # for value in self.args:
        #     if func(value):
        #         filtered.append(value)
        # return filtered
        it = _js_iteratee(func)
        return [v for i, v in enumerate(self.args) if it(v, i, self.args)]

    def find(self, func: Callable[..., bool] | None = None) -> Any:
        """Returns the value of the first element in an array that pass a test"""
        it = _js_iteratee(func)
        for i, each in enumerate(self.args):
            if it(each, i, self.args):
                return each

    def findIndex(self, predicate: Any) -> int:
        """Index of the first element for which ``predicate`` is truthy (a bare
        value is also accepted, as a domonic convenience), or -1."""
        if callable(predicate):
            it = _js_iteratee(predicate)
            for i, current in enumerate(self.args):
                if it(current, i, self.args):
                    return i
        else:
            for i, current in enumerate(self.args):
                if _js_strictish_equal(current, predicate):
                    return i
        return -1

    def forEach(self, func: Callable[..., Any] | None = None) -> None:
        """Calls a function for each array element"""
        it = _js_iteratee(func)
        for index, value in enumerate(list(self.args)):
            it(value, index, self.args)

    def keys(self) -> Iterator[Any]:
        """Returns a Array Iteration Object, containing the keys of the original array"""
        for i in range(len(self.args)):
            yield i

    def copyWithin(
        self, target: int, start: int = 0, end: int | None = None
    ) -> list[Any]:
        """Shallow-copy the ``[start, end)`` slice to ``target`` within the same
        array (indices may be negative), and return the array."""
        length = len(self.args)

        def _clamp(value: int | None, default: int) -> int:
            if value is None:
                return default
            value = int(value)
            return max(length + value, 0) if value < 0 else min(value, length)

        dest = _clamp(target, 0)
        src = _clamp(start, 0)
        stop = _clamp(end, length)
        chunk = self.args[src:stop]
        for offset, item in enumerate(chunk):
            if dest + offset >= length:
                break
            self.args[dest + offset] = item
        return self.args

    def entries(self) -> Iterator[list[Any]]:
        """[Returns a key/value pair Array Iteration Object]

        Yields:
            [type]: [key/value pair]
        """
        for i, value in enumerate(self.args):
            yield [i, value]

    def every(self, func: Callable[..., bool] | None = None) -> bool:
        """[Checks if every element in an array pass a test]"""
        it = _js_iteratee(func)
        return all(it(value, i, self.args) for i, value in enumerate(self.args))

    def at(self, index: int) -> Any:
        """[takes an integer value and returns the item at that index,
        allowing for positive and negative integers.
        Negative integers count back from the last item in the array.]

        Args:
            index ([type]): [position of item]

        Returns:
            [type]: [item at the given position]
        """
        index = int(index)
        if index < 0:
            index = len(self.args) + index
        if index < 0 or index >= len(self.args):
            return undefined
        return self.args[index]


Array.prototype = Array  # type: ignore[assignment]


class Set:
    def __init__(self, *args: Any) -> None:
        """Store unique values of any type in insertion order."""
        self.args: list[Any] = []
        values = args
        if (
            len(args) == 1
            and isinstance(args[0], IterableABC)
            and not isinstance(args[0], (str, bytes, bytearray, MappingABC))
        ):
            values = tuple(args[0])
        for value in values:
            self.add(value)

    def __iter__(self) -> Iterator[Any]:
        return iter(self.args)

    def __len__(self) -> int:
        return len(self.args)

    def __contains__(self, item: Any) -> bool:
        return self.has(item)

    def __repr__(self) -> str:
        return repr(self.args)

    def __str__(self) -> str:
        return str(self.args)

    @property
    def species(self) -> Any:
        """The constructor function that is used to create derived objects."""
        return Set

    @property
    def size(self) -> int:
        """Returns the number of values in the Set object."""
        return len(self.args)

    def add(self, value: Any) -> "Set":
        """Append a value and return this Set."""
        if not self.has(value):
            self.args.append(value)
        return self

    def clear(self) -> None:
        """Removes all elements from the Set object."""
        self.args.clear()

    def delete(self, value: Any) -> bool:
        """Removes the element associated to the value
        returns a boolean asserting whether an element was successfully removed or not.
        """
        for index, item in enumerate(self.args):
            if _js_set_same_value_zero(item, value):
                del self.args[index]
                return True
        return False

    def remove(self, value: Any) -> None:
        """Remove a value using Python set semantics."""
        if not self.delete(value):
            raise KeyError(value)

    def has(self, value: Any) -> bool:
        """Returns a boolean asserting whether an element is present with the given value in the Set object or not."""
        return any(_js_set_same_value_zero(item, value) for item in self.args)

    def contains(self, value: Any) -> bool:
        """Returns a boolean asserting whether an element is present with the given value in the Set object or not."""
        return self.has(value)

    # Set.prototype[@@iterator]()
    # Returns a new iterator object that yields the values for each element in the Set object in insertion order.

    def values(self) -> Iterator[Any]:
        """Returns a new iterator object that yields the values for each element
        in the Set object in insertion order."""
        return iter(self.args)

    def keys(self) -> Iterator[Any]:
        """Alias for values, matching JavaScript Set."""
        return self.values()

    def entries(self) -> Iterator[list[Any]]:
        """Returns a new iterator object that contains an array of [value, value] for each element in the Set object,
        in insertion order."""
        return iter([[value, value] for value in self.args])
        # This is similar to the Map object, so that each entry's key is the same as its value for a Set.

    def forEach(
        self, callbackFn: Callable[[Any, Any], Any], thisArg: Any = None
    ) -> None:
        """Calls callbackFn once for each value present in the Set object, in insertion order.
        If a thisArg parameter is provided, it will be used as the this value for each invocation of callbackFn.
        """
        for value in list(self.args):
            _invoke_js_callback(callbackFn, value, value, self)


class Number(float):
    """javascript Number methods"""

    MAX_VALUE = list(sys.float_info)[0]
    MIN_VALUE = 5e-324  # CHANGE no longer >  list(sys.float_info)[3]

    NEGATIVE_INFINITY = float(
        "-inf"
    )  #: Represents negative infinity (returned on overflow) Number
    POSITIVE_INFINITY = float(
        "inf"
    )  #: Represents infinity (returned on overflow)  Number
    MAX_SAFE_INTEGER: int = 2**53 - 1
    MIN_SAFE_INTEGER: int = -(2**53 - 1)
    EPSILON: float = 2.0**-52
    NaN = float("nan")

    @staticmethod
    def isFinite(value: Any) -> bool:
        """``Number.isFinite`` -- true only for a real finite number (no coercion)."""
        if isinstance(value, Number):
            value = value.x
        return isinstance(value, (int, float)) and math.isfinite(value)

    @staticmethod
    def isNaN(value: Any) -> bool:
        """``Number.isNaN`` -- true only for an actual NaN number (no coercion)."""
        if isinstance(value, Number):
            value = value.x
        return isinstance(value, float) and math.isnan(value)

    @staticmethod
    def parseFloat(value: Any) -> Any:
        """Alias of the global ``parseFloat``."""
        return Global.parseFloat(value)

    @staticmethod
    def parseInt(value: Any, radix: int = 0) -> Any:
        """Alias of the global ``parseInt``."""
        return Global.parseInt(value, radix)

    # prototype Allows you to add properties and methods to an object   Number

    def __new__(cls, x: Any = "", *args: Any, **kwargs: Any) -> "Number":
        # coerce with JS semantics first, so ``Number("abc")`` is NaN rather
        # than a Python ``ValueError`` out of ``float.__new__``
        try:
            numeric = float(Global.Number(x))
        except (ValueError, _PyTypeError):
            numeric = float("nan")
        return super().__new__(cls, numeric)

    def __init__(self, x: Any = "", *args: Any, **kwargs: Any) -> None:
        self.x: Any = Global.Number(x)

    def __str__(self) -> str:
        return Global.String(self.x)

    def __repr__(self) -> str:
        return Global.String(self.x)

    def __add__(self, other):
        return self.x + other

    def __sub__(self, other):
        return self.x - other

    def __mul__(self, other):
        return self.x * other

    def __div__(self, other):
        return self.x / other

    def __mod__(self, other):
        return self.x % other

    def __pow__(self, other):
        return self.x**other

    def __neg__(self):
        return -self.x

    def __pos__(self):
        return +self.x

    def __abs__(self):
        return abs(self.x)

    def __invert__(self):
        return ~self.x

    def __lt__(self, other):
        return self.x < other

    def __le__(self, other):
        return self.x <= other

    def __eq__(self, other):
        return self.x == other

    def __ne__(self, other):
        return self.x != other

    def __gt__(self, other):
        return self.x > other

    def __ge__(self, other):
        return self.x >= other

    def __and__(self, other):
        return self.x & other

    def __or__(self, other):
        return self.x | other

    def __xor__(self, other):
        return self.x ^ other

    def __lshift__(self, other):
        return self.x << other

    def __rshift__(self, other):
        return self.x >> other

    def __iadd__(self, other):
        return self.x + other

    def __isub__(self, other):
        return self.x - other

    def __imul__(self, other):
        return self.x * other

    def __idiv__(self, other):
        return self.x / other

    def __imod__(self, other):
        return self.x % other

    def __ipow__(self, other):
        return self.x**other

    def __ilshift__(self, other):
        return self.x << other

    def __irshift__(self, other):
        return self.x >> other

    def __iand__(self, other):
        return self.x & other

    def __ior__(self, other):
        return self.x | other

    def __ixor__(self, other):
        return self.x ^ other

    def __floordiv__(self, other):
        return self.x // other

    def __rfloordiv__(self, other):
        return other // self.x

    def __ifloordiv__(self, other):
        return other // self.x

    def __truediv__(self, other):
        return self.x / other

    def __rtruediv__(self, other):
        return other / self.x

    def __itruediv__(self, other):
        return other / self.x

    def __rmod__(self, other):
        return other % self.x

    @staticmethod
    def isInteger(value: Any) -> bool:
        """``Number.isInteger`` -- true only for a finite whole-number value."""
        if isinstance(value, bool):
            return False
        if isinstance(value, Number):
            value = value.x
        if not isinstance(value, (int, float)):
            return False
        return math.isfinite(value) and float(value).is_integer()

    @staticmethod
    def isSafeInteger(value: Any) -> bool:
        """``Number.isSafeInteger`` -- an integer value within +/-(2**53 - 1).

        Like JavaScript, a non-number (including a numeric string) is ``False``.
        """
        if isinstance(value, Number):
            value = value.x
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return False
        return (
            math.isfinite(value)
            and float(value).is_integer()
            and -(2**53 - 1) <= value <= 2**53 - 1
        )

    def toExponential(self, num: int | None = None) -> str:
        """Converts a number into an exponential notation"""
        if num is not None:
            exp = f"{self.x:.{int(num)}e}"
        else:
            exp = "{:e}".format(self.x)

        if num is None and "e" in str(self.x):
            exp = str(self.x)  # python already converts.

        n, e = exp.split("e")
        if num is None:
            n = n.rstrip("0")
        e = f"{int(e):+d}"

        if n == "0.":
            n = "0"

        if n.endswith("."):
            n = n.strip(".")

        return n + "e" + e

    def toFixed(self, digits: int) -> str:
        """[formats a number using fixed-point notation.]

        Args:
            digits ([int]): [The number of digits to appear after the decimal point

        Returns:
            [str]: [A string representing the given number using fixed-point notation.]
        """
        digits = max(int(digits), 0)
        value = self.x
        if not isinstance(value, (int, float)) or value != value:
            return "NaN"
        if value in (float("inf"), float("-inf")):
            return str(value)
        from decimal import Decimal, ROUND_FLOOR

        # ECMAScript toFixed: pick the representable value closest to the actual
        # stored double, ties going to the larger value (toward +Infinity) -- so
        # (1.005).toFixed(2) is "1.00" and (-2.5).toFixed(0) is "-2".
        quantum = Decimal(1).scaleb(-digits)
        scaled = Decimal(value) / quantum + Decimal("0.5")
        rounded = scaled.to_integral_value(rounding=ROUND_FLOOR) * quantum
        return f"{rounded:.{digits}f}"

    def toPrecision(self, precision: int) -> str:
        """[returns a string representing the Number object to the specified precision.]

        Args:
            precision ([int]): [An integer specifying the number of significant digits.]

        Returns:
            [str]: [A string representing a Number object in fixed-point
            or exponential notation rounded to precision significant digits]
        """
        precision = int(precision)
        if precision < 1:
            raise ValueError("precision must be at least 1")

        if math.isnan(self.x) or math.isinf(self.x):
            return str(self.x)

        formatted = format(self.x, f".{precision}g")
        if "e" in formatted or "E" in formatted:
            return formatted.replace("E", "e")

        sign = ""
        mantissa = formatted
        if mantissa.startswith(("-", "+")):
            sign = mantissa[0]
            mantissa = mantissa[1:]

        digits_only = mantissa.replace(".", "")
        significant = digits_only.lstrip("0")
        significant_count = len(significant) if significant else 1

        if significant_count < precision:
            if "." not in mantissa:
                mantissa += "."
            mantissa += "0" * (precision - significant_count)

        return sign + mantissa

    def toString(self, base: int | None = None) -> str:
        """A string for the number in the given radix (2-36; default 10)."""
        value = self.x
        if base is None or int(base) == 10:
            return str(value)
        base = int(base)
        if not 2 <= base <= 36:
            raise ValueError("toString() radix must be between 2 and 36")
        if not isinstance(value, (int, float)) or value != value:
            return "NaN"

        import string

        digs = string.digits + string.ascii_lowercase
        sign = "-" if value < 0 else ""
        n = int(abs(value))
        if n == 0:
            return "0"
        out = []
        while n:
            out.append(digs[n % base])
            n //= base
        return sign + "".join(reversed(out))


def _js_replacer(fn: "Callable[..., Any]") -> "Callable[[Any], str]":
    """Adapt a ``String.replace`` callback for :func:`re.sub`.

    A one-argument callback keeps the domonic convention (it receives the
    ``re.Match`` object). A callback that takes more positional arguments (or
    ``*args``) is treated as a JavaScript replacer and receives
    ``(match, p1, ..., pN, offset, string)``.
    """
    try:
        params = list(inspect.signature(fn).parameters.values())
    except (_PyTypeError, ValueError):
        return fn
    positional = [
        p
        for p in params
        if p.kind
        in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
    ]
    has_varargs = any(
        p.kind is inspect.Parameter.VAR_POSITIONAL for p in params
    )
    if not has_varargs and len(positional) <= 1:
        return fn

    def js_style(match: Any) -> str:
        result = fn(
            match.group(0), *match.groups(), match.start(), match.string
        )
        return "" if result is None else str(result)

    return js_style


def _js_replacement_template(replacement: str, group_count: int) -> str:
    """Translate a JavaScript ``String.prototype.replace`` replacement string
    into the substitution syntax :func:`re.sub` expects.

    JavaScript uses ``$1``..``$99`` / ``$<name>`` for captured groups, ``$&``
    for the whole match and ``$$`` for a literal ``$``; Python uses ``\\g<1>``,
    ``\\g<0>`` and a plain ``$``. A group reference past ``group_count`` is left
    literal, matching JavaScript. ``$``` and ``$'`` (text before/after the match)
    have no ``re.sub`` equivalent and are left as written.
    """
    out: list[str] = []
    i = 0
    length = len(replacement)
    while i < length:
        char = replacement[i]
        if char == "\\":
            # Literal in JavaScript; must be escaped for re.sub.
            out.append("\\\\")
            i += 1
            continue
        if char != "$" or i + 1 >= length:
            out.append(char)
            i += 1
            continue
        nxt = replacement[i + 1]
        if nxt == "$":
            out.append("$")
            i += 2
        elif nxt == "&":
            out.append(r"\g<0>")
            i += 2
        elif nxt == "<" and ">" in replacement[i + 2:]:
            end = replacement.index(">", i + 2)
            out.append(r"\g<%s>" % replacement[i + 2:end])
            i = end + 1
        elif nxt.isdigit():
            digits = replacement[i + 1:i + 3]
            if len(digits) == 2 and (
                not digits.isdigit() or int(digits) > group_count
            ):
                digits = digits[0]
            number = int(digits)
            if number == 0 or number > group_count:
                out.append("$")
                i += 1
            else:
                out.append(r"\g<%d>" % number)
                i += 1 + len(digits)
        else:
            out.append("$")
            i += 1
    return "".join(out)


def _expand_js_replacement(replacement: str, m: "re.Match[str]") -> str:
    """Expand a JavaScript ``String.replace`` replacement string against one
    match, including ``$``` (text before) and ``$'`` (text after) which have no
    ``re.sub`` template equivalent."""
    out: list[str] = []
    groups = m.groups()
    i = 0
    n = len(replacement)
    while i < n:
        ch = replacement[i]
        if ch != "$" or i + 1 >= n:
            out.append(ch)
            i += 1
            continue
        nxt = replacement[i + 1]
        if nxt == "$":
            out.append("$")
            i += 2
        elif nxt == "&":
            out.append(m.group(0))
            i += 2
        elif nxt == "`":
            out.append(m.string[: m.start()])
            i += 2
        elif nxt == "'":
            out.append(m.string[m.end():])
            i += 2
        elif nxt == "<" and ">" in replacement[i + 2:]:
            end = replacement.index(">", i + 2)
            try:
                out.append(m.group(replacement[i + 2:end]) or "")
            except (IndexError, re.error):
                pass
            i = end + 1
        elif nxt.isdigit():
            two = replacement[i + 1:i + 3]
            if len(two) == 2 and two.isdigit() and 0 < int(two) <= len(groups):
                out.append(groups[int(two) - 1] or "")
                i += 3
            elif 0 < int(nxt) <= len(groups):
                out.append(groups[int(nxt) - 1] or "")
                i += 2
            else:
                out.append("$")
                i += 1
        else:
            out.append("$")
            i += 1
    return "".join(out)


def _js_sub(
    compiled: "re.Pattern[str]", replacement: str, text: str, count: int
) -> str:
    """``re.sub`` with JavaScript ``$``-pattern semantics."""
    if "$`" in replacement or "$'" in replacement:
        return compiled.sub(
            lambda m: _expand_js_replacement(replacement, m), text, count=count
        )
    template = _js_replacement_template(replacement, compiled.groups)
    return compiled.sub(template, text, count=count)


# --- UTF-16 code units -----------------------------------------------------
# JavaScript strings are sequences of UTF-16 code units; ``.length``, indexing,
# ``charCodeAt``, ``charAt`` and ``slice`` are all code-unit based. A Python str
# is code points, so an astral-plane character (emoji, rare CJK, ...) is one
# Python char but two JS code units. These helpers bridge the two.


def _utf16_units(s: str) -> "list[int]":
    units: list[int] = []
    for ch in s:
        cp = ord(ch)
        if cp > 0xFFFF:
            cp -= 0x10000
            units.append(0xD800 + (cp >> 10))
            units.append(0xDC00 + (cp & 0x3FF))
        else:
            units.append(cp)
    return units


def _units_to_str(units: "list[int]") -> str:
    import struct

    raw = b"".join(struct.pack("<H", u & 0xFFFF) for u in units)
    return raw.decode("utf-16-le", errors="surrogatepass")


def _cp_index_to_unit(s: str, cp_index: int) -> int:
    """A code-point offset into ``s`` -> the equivalent code-unit offset."""
    return cp_index + sum(1 for ch in s[:cp_index] if ord(ch) > 0xFFFF)


def _unit_index_to_cp(s: str, unit_index: int) -> int:
    """A code-unit offset into ``s`` -> the equivalent code-point offset."""
    seen = 0
    for cp, ch in enumerate(s):
        if seen >= unit_index:
            return cp
        seen += 2 if ord(ch) > 0xFFFF else 1
    return len(s)


class String:
    """javascript String methods"""

    @staticmethod
    def fromCodePoint(codePoint: int) -> str:
        """Converts a Unicode code point into a string"""
        return chr(codePoint)

    @staticmethod
    def toCodePoint(char: str) -> int:
        """Converts a Unicode string into a code point"""
        return ord(char)

    @staticmethod
    def raw(template: Any, *substitutions: Any) -> str:
        """``String.raw`` -- the tag function for raw template literals.

        ``template`` is the strings object (``{"raw": [...]}`` or anything with
        a ``raw`` sequence); the raw segments are interleaved with
        ``substitutions``. A plain string is returned unchanged, so
        ``String.raw(r"a\\nb")`` still works.
        """
        if isinstance(template, str):
            return template
        if isinstance(template, dict):
            parts = list(template.get("raw", []))
        else:
            parts = list(getattr(template, "raw", template))
        out: list[str] = []
        for i, part in enumerate(parts):
            out.append(str(part))
            if i < len(substitutions):
                out.append(str(substitutions[i]))
        return "".join(out)

    # @staticmethod
    # def fromCharCode(code: int):
    #     """ Converts a Unicode code point into a string """
    #     return chr(code)

    @staticmethod
    def toCharCode(char: str) -> int:
        """Converts a Unicode string into a code point"""
        return ord(char)

    def __init__(self, x: Any = "", *args: Any, **kwargs: Any) -> None:
        self.x = Global.String(x)
        self._u16_cache: "list[int] | None" = None
        self._astral: "bool | None" = None

    @property
    def _has_astral(self) -> bool:
        """Whether ``self.x`` contains any character outside the BMP -- i.e.
        whether code-unit and code-point positions can differ. Cheap: ASCII
        strings (the common case) short-circuit immediately."""
        if self._astral is None:
            s = self.x
            self._astral = (not s.isascii()) and any(ord(c) > 0xFFFF for c in s)
        return self._astral

    @property
    def _u16(self) -> "list[int]":
        """The UTF-16 code units of ``self.x`` (``x`` is set once at
        construction, so this is computed lazily and never invalidated).
        Only touched by the position methods when the string actually has an
        astral character."""
        cache = self._u16_cache
        if cache is None:
            cache = (
                _utf16_units(self.x)
                if self._has_astral
                else [ord(ch) for ch in self.x]
            )
            self._u16_cache = cache
        return cache

    def __str__(self) -> str:
        return self.x

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.x == other
        if isinstance(other, String):
            return self.x == other.x
        return False

    # def __repr__(self):
    #     return self.x

    def __getitem__(self, item: "int | slice") -> Any:
        if isinstance(item, slice):
            return self.x[item]
        # JS bracket indexing: the char at a valid position, else ``undefined``
        # (a negative index is not a valid array index in JS -- use ``at()``).
        if not self._has_astral:
            return self.x[item] if 0 <= item < len(self.x) else undefined
        units = self._u16
        return _units_to_str([units[item]]) if 0 <= item < len(units) else undefined

    def __add__(self, other: str) -> str:
        return self.x + str(other)

    def __radd__(self, other: str) -> str:
        return str(other) + self.x

    def __iadd__(self, other: str) -> str:
        return self.x + str(other)

    def __sub__(self, other: str) -> Any:
        return self.x - other  # type: ignore[operator]

    def __rsub__(self, other: str) -> Any:
        return other - self.x  # type: ignore[operator]

    def __isub__(self, other: str) -> Any:
        return self.x - other  # type: ignore[operator]

    def __mul__(self, other: int) -> str:
        return self.x * int(other)

    def __rmul__(self, other: int) -> str:
        return self.x * int(other)

    def __imul__(self, other: int) -> str:
        return self.x * int(other)

    def split(
        self, expr: "str | RegExp | None" = None, limit: int | None = None
    ) -> list[str]:
        """``String.prototype.split(separator, limit)``.

        A ``RegExp`` separator with capture groups keeps the captures in the
        result (like JS); ``""`` splits into individual characters; ``limit``
        truncates the result.
        """
        if expr is None:
            parts = [self.x]
        elif isinstance(expr, RegExp):
            parts = expr._compiled().split(self.x)
        else:
            sep = str(expr)
            if sep == "":
                parts = list(self.x)
            elif _looks_like_regex_separator(sep):
                try:
                    parts = re.split(sep, self.x)
                except re.error:
                    parts = self.x.split(sep)
            else:
                parts = self.x.split(sep)
        return parts if limit is None else parts[: int(limit)]

    def concat(self, *args, seperator: str = "") -> str:
        """[concatenates the string arguments to the calling string and returns a new string.]

        Args:
            seperator (str, optional): []. Defaults to "".

        Returns:
            [type]: [A new string containing the combined text of the strings provided.]
        """
        parts = list(args)
        parts.insert(0, self.x)
        return seperator.join(parts)

    # @staticmethod
    def charCodeAt(self, index: int) -> Any:
        """The UTF-16 code unit at ``index``; ``NaN`` (the *number*) when out of
        range, so ``s.charCodeAt(past_end) <= 0xffff`` is simply ``False``."""
        index = int(index)
        if not self._has_astral:
            s = self.x
            return ord(s[index]) if 0 <= index < len(s) else float("nan")
        units = self._u16
        if index < 0 or index >= len(units):
            return float("nan")
        return units[index]

    @staticmethod
    def fromCharCode(*codes: int) -> str:
        """A string built from a sequence of UTF-16 code units.

        Static, like ``String.fromCharCode(...)`` in JavaScript. Adjacent
        surrogate code units are combined (``fromCharCode(0xD83D, 0xDE00)`` ->
        ``"😀"``); a lone surrogate is kept as-is.
        """
        import struct

        raw = b"".join(struct.pack("<H", int(code) & 0xFFFF) for code in codes)
        return raw.decode("utf-16-le", errors="surrogatepass")

    @property
    def length(self) -> int:
        """The number of UTF-16 code units (astral characters count as two)."""
        return len(self._u16) if self._has_astral else len(self.x)

    def repeat(self, count: int) -> str:
        """Returns a new string with a specified number of copies of an existing string"""
        count = int(count)
        if count < 0:
            raise ValueError("repeat count must be non-negative")
        return self.x * count

    def startsWith(self, x: str, position: int | None = None) -> bool:
        """``String.prototype.startsWith(searchString, position=0)``."""
        pos = max(int(position), 0) if position is not None else 0
        return self.x.startswith(x, pos)

    def substring(self, start: int, end: int | None = None) -> str:
        """The code units between two indices (negatives clamp to 0, args swap
        if out of order) -- code-unit based, like JavaScript."""
        seq: Any = self.x if not self._has_astral else self._u16
        length = len(seq)
        start = min(max(int(start), 0), length)
        end = length if end is None else min(max(int(end), 0), length)
        if start > end:
            start, end = end, start
        part = seq[start:end]
        return part if isinstance(part, str) else _units_to_str(part)

    def endsWith(self, x: str, endPosition: int | None = None) -> bool:
        """``String.prototype.endsWith(searchString, endPosition=length)`` --
        treats the string as if it ended at ``endPosition``."""
        end = len(self.x) if endPosition is None else int(endPosition)
        return self.x[:end].endswith(x)

    def toLowerCase(self) -> str:
        """Converts a string to lowercase letters"""
        return self.x.lower()

    def toUpperCase(self) -> str:
        """Converts a string to uppercase letters"""
        return self.x.upper()

    def slice(self, start: int = 0, end: int | None = None) -> str:
        """A slice of the string in code-unit space (negative indices count
        from the end), like JavaScript."""
        seq: Any = self.x if not self._has_astral else self._u16
        length = len(seq)
        s = int(start)
        s = max(length + s, 0) if s < 0 else min(s, length)
        if end is None:
            e = length
        else:
            e = int(end)
            e = max(length + e, 0) if e < 0 else min(e, length)
        if s >= e:
            return ""
        part = seq[s:e]
        return part if isinstance(part, str) else _units_to_str(part)

    def trim(self) -> str:
        """Removes whitespace from both ends of a string"""
        return self.x.strip()

    def at(self, index: int) -> Any:
        """The code unit at ``index`` as a string (negative counts from the
        end), or ``undefined`` when out of range."""
        i = int(index)
        if not self._has_astral:
            s = self.x
            if i < 0:
                i += len(s)
            return s[i] if 0 <= i < len(s) else undefined
        units = self._u16
        if i < 0:
            i += len(units)
        return _units_to_str([units[i]]) if 0 <= i < len(units) else undefined

    def normalize(self, form: str = "NFC") -> str:
        """Unicode normalisation (``NFC`` / ``NFD`` / ``NFKC`` / ``NFKD``)."""
        import unicodedata

        return unicodedata.normalize(form, self.x)  # type: ignore[arg-type]

    def charAt(self, index: int) -> str:
        """The UTF-16 code unit at ``index`` as a one-'character' string (a lone
        surrogate for one half of an astral character); ``""`` when out of
        range."""
        index = int(index)
        if not self._has_astral:
            s = self.x
            return s[index] if 0 <= index < len(s) else ""
        units = self._u16
        if index < 0 or index >= len(units):
            return ""
        return _units_to_str([units[index]])

    def replace(self, old: str | RegExp, new: str | Callable[..., str]) -> str:
        """
        Searches a string for a specified value, or a regular expression,
        and returns a new string where the specified values are replaced.
        only replaces first one.
        """
        if isinstance(old, RegExp):
            count = 0 if old.global_ else 1
            compiled = old._compiled()
            if callable(new):
                return compiled.sub(_js_replacer(new), self.x, count=count)
            return _js_sub(compiled, str(new), self.x, count)
        if callable(new):
            return re.sub(re.escape(str(old)), _js_replacer(new), self.x, count=1)
        return self.x.replace(str(old), str(new), 1)

    def replaceAll(self, old: str | RegExp, new: str | Callable[..., str]) -> str:
        """[returns a new string where the specified values are replaced. ES2021]

        Args:
            old ([str | RegExp]): [word or global pattern to remove]
            new ([str | Callable]): [replacement; ``$1`` etc. work with a RegExp]

        Returns:
            [str]: [new string with all occurrences of old replaced]
        """
        if isinstance(old, RegExp):
            compiled = old._compiled()
            if callable(new):
                return compiled.sub(_js_replacer(new), self.x)
            return _js_sub(compiled, str(new), self.x, 0)
        return self.x.replace(str(old), str(new))

    # def localeCompare():
    # """ Compares two strings in the current locale """
    # pass

    def substr(self, start: int = 0, length: int | None = None) -> str:
        """``length`` code units starting at ``start`` (negative ``start``
        counts from the end) -- code-unit based, like JavaScript."""
        seq = self.x if not self._has_astral else self._u16
        total = len(seq)
        start = int(start)
        if start < 0:
            start = max(total + start, 0)
        count = (total - start) if length is None else int(length)
        if count <= 0:
            return ""
        part = seq[start : start + count]
        return part if isinstance(part, str) else _units_to_str(part)

    def toLocaleLowerCase(self) -> str:
        """Converts a string to lowercase letters, according to the host's locale"""
        # locale.setlocale()
        return self.x.lower()

    def toLocaleUpperCase(self) -> str:
        """Converts a string to uppercase letters, according to the host's locale"""
        # locale.setlocale()
        return self.x.upper()

    def indexOf(self, searchValue: str, fromIndex: int = 0) -> int:
        """[returns the index within the calling String object of the first occurrence of the specified value,
        starting the search at fromIndex ]

        Args:
            searchValue (str): [The string value to search for.]
            fromIndex (int): [An integer representing the index at which to start the search]

        Returns:
            [type]: [The index of the first occurrence of searchValue, or -1 if not found.]

        """
        searchValue = str(searchValue)
        if not self._has_astral:
            frm = max(int(fromIndex), 0)
            if frm > len(self.x):
                return len(self.x) if searchValue == "" else -1
            return self.x.find(searchValue, frm)
        cp_from = _unit_index_to_cp(self.x, max(int(fromIndex), 0))
        if cp_from > len(self.x):
            return self.length if searchValue == "" else -1
        pos = self.x.find(searchValue, cp_from)
        return -1 if pos < 0 else _cp_index_to_unit(self.x, pos)

    def codePointAt(self, index: int) -> Any:
        """[Returns the Unicode code point at the specified index (position)]

        Args:
            index (int): [index position]

        Returns:
            [type]: [the Unicode code point at the specified index (position)]
        """
        index = int(index)
        if not self._has_astral:
            s = self.x
            return ord(s[index]) if 0 <= index < len(s) else None
        units = self._u16
        if index < 0 or index >= len(units):
            return None  # JS: undefined
        unit = units[index]
        if 0xD800 <= unit <= 0xDBFF and index + 1 < len(units):
            nxt = units[index + 1]
            if 0xDC00 <= nxt <= 0xDFFF:
                return 0x10000 + ((unit - 0xD800) << 10) + (nxt - 0xDC00)
        return unit

    def padEnd(self, length: int, padChar: str = " ") -> str:
        """[Pads the end of a string with a specified character
        (repeated, if needed) to create a new string.]

        Args:
            length (int): [the length of the resulting string]
            padChar (str, optional): [the character to use for padding. Defaults to " "].

        Returns:
            [str]: [the padded string]
        """
        length = int(length)
        padChar = str(padChar)
        if length <= len(self.x) or padChar == "":
            return self.x
        needed = length - len(self.x)
        padding = (padChar * ((needed // len(padChar)) + 1))[:needed]
        return self.x + padding

    def padStart(self, length: int, padChar: str = " ") -> str:
        """[Pads the start of a string with a specified character]

        Args:
            length (int): [the length of the resulting string]
            padChar (str, optional): [the character to use for padding. Defaults to " "].

        Returns:
            [str]: [the padded string]
        """
        length = int(length)
        padChar = str(padChar)
        if length <= len(self.x) or padChar == "":
            return self.x
        needed = length - len(self.x)
        padding = (padChar * ((needed // len(padChar)) + 1))[:needed]
        return padding + self.x

    def localeCompare(self, comparisonString: str, locale: str | None = None, *args) -> int:
        """method returns a number indicating whether a reference string comes before,
        or after, or is the same as the given string in sort order"""
        if locale:
            previous_locale = None
            try:
                previous_locale = pylocale.setlocale(pylocale.LC_COLLATE)
                pylocale.setlocale(pylocale.LC_COLLATE, locale)
                comparison = pylocale.strcoll(self.x, comparisonString)
            except Exception:
                comparison = (self.x > comparisonString) - (self.x < comparisonString)
            finally:
                if previous_locale is not None:
                    try:
                        pylocale.setlocale(pylocale.LC_COLLATE, previous_locale)
                    except Exception:
                        previous_locale = None
            return comparison
        return (self.x > comparisonString) - (self.x < comparisonString)

    def trimStart(self) -> str:
        """[Removes whitespace from the beginning of a string.]"""
        return self.x.lstrip()

    def trimEnd(self) -> str:
        """[Removes whitespace from the end of a string]"""
        return self.x.rstrip()

    def includes(self, searchValue: str, position: int = 0) -> bool:
        """[returns true if the specified string is found within the calling String object,]

        Args:
            searchValue (str): [The string value to search for.]
            position (int, optional): [the position to search from]. Defaults to 0.

        Returns:
            [type]: [a boolean value indicating whether the search value was found.]
        """
        position = min(max(int(position), 0), len(self.x))
        return searchValue in self.x[position:]

    def search(self, value: "str | RegExp") -> int:
        """``String.prototype.search`` -- the index of the first match, or -1.

        A non-``RegExp`` ``value`` is converted with ``new RegExp(value)`` (it
        is *not* escaped), matching JavaScript.
        """
        rx = value if isinstance(value, RegExp) else RegExp(str(value))
        m = rx._compiled().search(self.x)
        return m.start() if m is not None else -1

    def matchAll(self, pattern: "str | RegExp") -> Iterator["_RegExpMatch"]:
        """``String.prototype.matchAll`` -- an iterator of match arrays.

        Each item is ``[fullMatch, *groups]`` with ``.index`` / ``.input`` /
        ``.groups`` (named groups), like ``RegExp.exec``.
        """
        rx = pattern if isinstance(pattern, RegExp) else RegExp(str(pattern), "g")
        compiled = rx._compiled()
        for m in compiled.finditer(self.x):
            result = _RegExpMatch([m.group(0), *m.groups()])
            result.index = m.start()
            result.input = self.x
            result.groups = m.groupdict()
            yield result

    def match(self, pattern: "str | RegExp") -> "_RegExpMatch | list[str] | None":
        """``String.prototype.match``.

        Without the ``g`` flag: ``[fullMatch, *groups]`` with ``.index`` /
        ``.input`` / ``.groups``, or ``None``. With the ``g`` flag: a plain
        list of every full match, or ``None`` when there is no match.
        """
        rx = pattern if isinstance(pattern, RegExp) else RegExp(str(pattern))
        compiled = rx._compiled()
        if rx.global_:
            matches = [m.group(0) for m in compiled.finditer(self.x)]
            return matches or None
        m = compiled.search(self.x)
        if m is None:
            return None
        result = _RegExpMatch([m.group(0), *m.groups()])
        result.index = m.start()
        result.input = self.x
        result.groups = m.groupdict()
        return result

    def compile(self, pattern: str) -> re.Pattern[str]:
        """
        Searches a string for a specified value, or a regular expression,
        and returns a new string where the specified values are replaced.
        only replaces first one.
        """
        return re.compile(pattern)

    def lastIndexOf(self, searchValue: str, fromIndex: int | None = None) -> int:
        """
        returns the last index within the calling String object of the first occurrence of the specified value,
        starting the search at fromIndex
        """
        searchValue = str(searchValue)
        if not self._has_astral:
            frm = len(self.x) if fromIndex is None else min(
                max(int(fromIndex), 0), len(self.x)
            )
            if searchValue == "":
                return frm
            return self.x.rfind(searchValue, 0, frm + len(searchValue))
        if fromIndex is None:
            cp_from = len(self.x)
        else:
            cp_from = _unit_index_to_cp(
                self.x, min(max(int(fromIndex), 0), self.length)
            )
        if searchValue == "":
            return _cp_index_to_unit(self.x, cp_from)
        pos = self.x.rfind(searchValue, 0, cp_from + len(searchValue))
        return -1 if pos < 0 else _cp_index_to_unit(self.x, pos)

    # def test(self, pattern: str):? was this on string?

    def anchor(self, name: str) -> str:
        return '<a name="{}">{}</a>'.format(name, self.x)

    def big(self) -> str:
        """[wraps the string in big tags]

        Returns:
            [str]: [the string in big tags]
        """
        return "<big>" + self.x + "</big>"

    def blink(self) -> str:
        """[wraps the string in blink tags]

        Returns:
            [str]: [the string in blink tags]
        """
        return "<blink>" + self.x + "</blink>"

    def bold(self) -> str:
        """[wraps the string in bold tags]

        Returns:
            [str]: [the string in bold tags]
        """
        return "<b>" + self.x + "</b>"

    def fixed(self) -> str:
        """[wraps the string in fixed tags]

        Returns:
            [str]: [the string in fixed tags]
        """
        return "<tt>" + self.x + "</tt>"

    def fontcolor(self, color: str) -> str:
        """[wraps the string in font tags with a specified color]

        Args:
            color (str): [the color to use]

        Returns:
            [str]: [the string in font tags]
        """
        return "<font color=" + color + ">" + self.x + "</font>"

    def fontsize(self, size: str) -> str:
        """[wraps the string in font tags with a specified size]

        Args:
            size (str): [the size to use]

        Returns:
            [str]: [the string in font tags]
        """
        return "<font size=" + size + ">" + self.x + "</font>"

    def italics(self) -> str:
        """[wraps the string in italics tags]

        Returns:
            [str]: [the string in italics tags]
        """
        return "<i>" + self.x + "</i>"

    def link(self, url: str) -> str:
        """[wraps the string in a link tag]

        Args:
            url (str): [the url to use]

        Returns:
            [str]: [the string in a link tag]
        """
        return "<a href=" + url + ">" + self.x + "</a>"

    def small(self) -> str:
        """[wraps the string in small tags]

        Returns:
            [str]: [the string in small tags]
        """
        return "<small>" + self.x + "</small>"

    def strike(self) -> str:
        """[wraps the string in strike tags]

        Returns:
            [str]: [the string in strike tags]
        """
        return "<strike>" + self.x + "</strike>"

    def sub(self) -> str:
        """[wraps the string in sub tags]

        Returns:
            [str]: [the string in sub tags]
        """
        return "<sub>" + self.x + "</sub>"

    def sup(self) -> str:
        """[wraps the string in sup tags]

        Returns:
            [str]: [the string in sup tags]
        """
        return "<sup>" + self.x + "</sup>"

    def div(self, *args: Any, **kwargs: Any) -> Any:
        """[wraps the string in a div tag]

        Returns:
            [str]: [the string in a div tag]
        """
        from domonic.html import div

        return div(self.x, *args, **kwargs)

    def webpage(self) -> str:
        """[wraps the string in a webpage]

        Returns:
            [str]: [the string as a webpage]
        """
        from domonic.html import body, h1, head, html, link, meta, script, style, title

        content = html(
            head(
                title(self.x),
                script(""),
                style(""),
                meta(_charset="utf-8"),
                link(_rel="stylesheet", _href=""),
            ),
            body(
                h1(self.x),
            ),
        )
        return str(content)

    def __call__(self, tag: str, **kwargs: Any) -> Any:
        """
        lets you transform a string into a dom element
        with the string as the content.

        also accepts a list of kwargs to pass as attributes

        i.e
        >>> test = String("time to take a mo")
        >>> test('div', _style="font-color:red;")
        >>> str(test('div', _style="font-color:red;"))

        """
        from domonic.dom import Document

        return Document.createElement(tag, self.x, **kwargs)


import functools as _functools
import sys as _sys
import unicodedata as _unicodedata


# long Unicode-property names -> the general-category code re can be built from
_UNICODE_PROPERTY_ALIASES = {
    "letter": "L", "l": "L",
    "uppercase_letter": "Lu", "lu": "Lu",
    "lowercase_letter": "Ll", "ll": "Ll",
    "titlecase_letter": "Lt", "lt": "Lt",
    "modifier_letter": "Lm", "lm": "Lm",
    "other_letter": "Lo", "lo": "Lo",
    "mark": "M", "m": "M", "combining_mark": "M",
    "nonspacing_mark": "Mn", "mn": "Mn",
    "spacing_combining_mark": "Mc", "mc": "Mc",
    "enclosing_mark": "Me", "me": "Me",
    "number": "N", "n": "N",
    "decimal_number": "Nd", "nd": "Nd", "digit": "Nd",
    "letter_number": "Nl", "nl": "Nl",
    "other_number": "No", "no": "No",
    "punctuation": "P", "p": "P", "punct": "P",
    "dash_punctuation": "Pd", "pd": "Pd",
    "open_punctuation": "Ps", "ps": "Ps",
    "close_punctuation": "Pe", "pe": "Pe",
    "initial_punctuation": "Pi", "pi": "Pi",
    "final_punctuation": "Pf", "pf": "Pf",
    "connector_punctuation": "Pc", "pc": "Pc",
    "other_punctuation": "Po", "po": "Po",
    "symbol": "S", "s": "S",
    "math_symbol": "Sm", "sm": "Sm",
    "currency_symbol": "Sc", "sc_symbol": "Sc",
    "modifier_symbol": "Sk", "sk": "Sk",
    "other_symbol": "So", "so": "So",
    "separator": "Z", "z": "Z",
    "space_separator": "Zs", "zs": "Zs",
    "line_separator": "Zl", "zl": "Zl",
    "paragraph_separator": "Zp", "zp": "Zp",
    "other": "C", "c": "C",
    "control": "Cc", "cc": "Cc", "cntrl": "Cc",
    "format": "Cf", "cf": "Cf",
    "surrogate": "Cs", "cs": "Cs",
    "private_use": "Co", "co": "Co",
    "unassigned": "Cn", "cn": "Cn",
}

# a small set of common scripts, approximated by their principal Unicode blocks
# (unicodedata has no script property). Values are (lo, hi) code-point ranges.
_UNICODE_SCRIPT_RANGES: dict[str, tuple[tuple[int, int], ...]] = {
    "latin": ((0x41, 0x5A), (0x61, 0x7A), (0xC0, 0x24F), (0x1E00, 0x1EFF)),
    "greek": ((0x370, 0x3FF), (0x1F00, 0x1FFF)),
    "cyrillic": ((0x400, 0x4FF), (0x500, 0x52F)),
    "armenian": ((0x530, 0x58F),),
    "hebrew": ((0x590, 0x5FF),),
    "arabic": ((0x600, 0x6FF), (0x750, 0x77F), (0x8A0, 0x8FF)),
    "devanagari": ((0x900, 0x97F),),
    "thai": ((0xE00, 0xE7F),),
    "hiragana": ((0x3040, 0x309F),),
    "katakana": ((0x30A0, 0x30FF), (0x31F0, 0x31FF)),
    "han": ((0x4E00, 0x9FFF), (0x3400, 0x4DBF), (0xF900, 0xFAFF)),
    "hangul": ((0xAC00, 0xD7AF), (0x1100, 0x11FF), (0x3130, 0x318F)),
}


@_functools.lru_cache(maxsize=64)
def _unicode_property_ranges(prop: str, negate: bool = False) -> str:
    """Character-class body (no brackets) for a Unicode ``\\p{...}`` property
    -- ``re`` has no native support. General categories (``P``, ``Lu``, their
    long names such as ``Uppercase_Letter``), ``Script=<name>`` / ``sc=<name>``
    for a common set of scripts, and ``Any`` are understood. When *negate* is
    set, the complement ranges are returned so the fragment stays usable inside
    an existing ``[...]``."""
    key = prop.strip()
    if "=" in key:
        left, _, right = key.partition("=")
        if left.strip().lower() in ("script", "sc", "script_extensions", "scx"):
            key = right.strip()
    low = key.lower()

    script = _UNICODE_SCRIPT_RANGES.get(low)
    if script is not None:
        ranges = sorted(script)
        if negate:
            ranges = _complement_ranges(ranges)
        return "".join(_range_fragment(lo, hi) for lo, hi in ranges)

    if low in ("any", "assigned"):
        return "" if negate else "\\U00000000-\\U0010FFFF"

    prop = _UNICODE_PROPERTY_ALIASES.get(low, prop)
    if not (1 <= len(prop) <= 2 and prop[:1].isupper()):
        raise ValueError(f"Unsupported Unicode property escape: \\p{{{prop}}}")

    exact = len(prop) == 2
    fragments: list[str] = []
    run_start: int | None = None
    prev = -2
    for cp in range(_sys.maxunicode + 1):
        cat = _unicodedata.category(chr(cp))
        hit = (cat == prop) if exact else (cat[:1] == prop)
        if hit != negate:
            if run_start is None:
                run_start = cp
            prev = cp
        elif run_start is not None:
            fragments.append(_range_fragment(run_start, prev))
            run_start = None
    if run_start is not None:
        fragments.append(_range_fragment(run_start, prev))
    return "".join(fragments)


def _range_fragment(lo: int, hi: int) -> str:
    return "\\U%08X" % lo if lo == hi else "\\U%08X-\\U%08X" % (lo, hi)


def _complement_ranges(
    ranges: "list[tuple[int, int]]",
) -> "list[tuple[int, int]]":
    """The code-point ranges *not* covered by ``ranges`` (0..0x10FFFF)."""
    out: list[tuple[int, int]] = []
    cursor = 0
    for lo, hi in ranges:
        if lo > cursor:
            out.append((cursor, lo - 1))
        cursor = max(cursor, hi + 1)
    if cursor <= 0x10FFFF:
        out.append((cursor, 0x10FFFF))
    return out


_JS_PROP_RE = re.compile(r"\\([pP])\{([A-Za-z_]+(?:=[A-Za-z_]+)?)\}")


def _translate_js_regex(pattern: str) -> str:
    """Best-effort JS -> Python regex source translation.

    - ``(?<name>...)`` -> ``(?P<name>...)`` and ``\\k<name>`` -> ``(?P=name)``
    - ``[^]`` (any char) -> ``[\\s\\S]``
    - ``\\u{1F600}`` (braced code-point escape) -> ``\\U0001F600``
    - ``\\p{P}`` / ``\\P{Script=Greek}`` etc. -> classes from ``unicodedata``
    """
    if "(?<" in pattern:
        pattern = re.sub(r"\(\?<([A-Za-z_]\w*)>", r"(?P<\1>", pattern)
        pattern = re.sub(r"\\k<([A-Za-z_]\w*)>", r"(?P=\1)", pattern)

    # JS ``[^]`` (empty negated class = "any char, newlines included") is a
    # syntax error in Python's re -- rewrite it. ``[^]]`` (not "]") is left be.
    # The leading group soaks up any run of *paired* backslashes so ``\\[^]``
    # (an escaped backslash, then the class) is still rewritten.
    if "[^]" in pattern:
        pattern = re.sub(
            r"(?<!\\)((?:\\\\)*)\[\^\](?!\])", r"\1[\\s\\S]", pattern
        )

    # JS ``\u{1F600}`` (braced code-point escape, u/v flags) -> Python ``\Uxxxxxxxx``
    if "\\u{" in pattern:
        pattern = re.sub(
            r"\\u\{([0-9A-Fa-f]{1,6})\}",
            lambda m: "\\U%08X" % int(m.group(1), 16),
            pattern,
        )

    if "\\p{" not in pattern and "\\P{" not in pattern:
        return pattern

    out: list[str] = []
    i = 0
    in_class = False
    n = len(pattern)
    while i < n:
        ch = pattern[i]
        if ch == "\\" and i + 1 < n:
            m = _JS_PROP_RE.match(pattern, i)
            if m:
                negate = m.group(1) == "P"
                body = _unicode_property_ranges(m.group(2), negate and in_class)
                if in_class:
                    out.append(body)
                elif negate:
                    out.append("[^" + _unicode_property_ranges(m.group(2)) + "]")
                else:
                    out.append("[" + body + "]")
                i = m.end()
                continue
            out.append(pattern[i:i + 2])
            i += 2
            continue
        if ch == "[" and not in_class:
            in_class = True
        elif ch == "]" and in_class:
            in_class = False
        out.append(ch)
        i += 1
    return "".join(out)


class _RegExpMatch(list):
    """List of ``[fullMatch, *groups]`` with JS ``exec`` result attributes."""

    index: int = 0  # type: ignore[assignment]  # JS match.index, not list.index()
    input: str = ""
    groups: dict = {}


class RegExp:
    def __init__(self, expression: str, flags: str = "") -> None:
        self.expression = expression
        self._flags = (flags or "").lower()
        self.lastIndex = 0  #: Index at which exec/test resume when the g/y flag is set.

    @property
    def flags(self) -> str:
        """The active flags in canonical order (``d g i m s u v y``)."""
        return "".join(f for f in "dgimsuvy" if f in self._flags)

    @flags.setter
    def flags(self, value: str) -> None:
        self._flags = (value or "").lower()

    @property
    def dotAll(self) -> bool:
        """[Whether . matches newlines or not.]

        Returns:
            [bool]: [True if dot matches newlines, False otherwise]
        """
        return "s" in self._flags

    @dotAll.setter
    def dotAll(self, value: bool):
        """[Whether . matches newlines or not.]
        Args:
            value (bool): [True if dot matches newlines, False otherwise]
        """
        if "s" not in self._flags:
            self._flags += "s" if value else ""

    @property
    def multiline(self) -> bool:
        """[Whether . matches newlines or not.]
        Returns:
            [bool]: [True if dot matches newlines, False otherwise]
        """
        return "m" in self._flags

    @multiline.setter
    def multiline(self, value: bool):
        """[Whether . matches newlines or not.]
        Args:
            value (bool): [True if dot matches newlines, False otherwise]
        """
        if "m" not in self._flags:
            self._flags += "m" if value else ""

    @property
    def source(self) -> str:
        """[The text of the pattern.]
        Returns:
            [str]: [The text of the pattern.]
        """
        return self.expression

    @property
    def sticky(self) -> bool:
        """Whether the match is anchored at ``lastIndex`` (the ``y`` flag)."""
        return "y" in self._flags

    @sticky.setter
    def sticky(self, value: bool) -> None:
        if value and "y" not in self._flags:
            self._flags += "y"

    def _python_pattern(self) -> str:
        """The Python-``re`` source for this regex (``\\p{...}`` translated)."""
        cache = getattr(self, "_pattern_cache", None)
        if cache is None or cache[0] != self.expression:
            cache = (self.expression, _translate_js_regex(self.expression))
            object.__setattr__(self, "_pattern_cache", cache)
        return cache[1]

    def _compiled(self):
        return re.compile(self._python_pattern(), self._re_flags())

    @property
    def global_(self) -> bool:
        """[Whether to test the regular expression against all possible matches in a string,
        or only against the first.]

        Returns:
            [bool]: [True if global, False otherwise]
        """
        return "g" in self._flags

    @global_.setter
    def global_(self, value: bool):
        """[Whether to test the regular expression against all possible matches in a string,
        or only against the first.]
        Args:
            value (bool): [True if global, False otherwise]
        """
        if "g" not in self._flags:
            self._flags += "g" if value else ""

    @property
    def hasIndices(self) -> bool:
        """[Whether the regular expression result exposes the start and end indices of captured substrings.]

        Returns:
            [bool]: [True if hasIndices, False otherwise]
        """
        return "d" in self._flags

    @hasIndices.setter
    def hasIndices(self, value: bool):
        """[Whether the regular expression result exposes the start and end indices of captured substrings.]
        Args:
            value (bool): [True if hasIndices, False otherwise]
        """
        if "d" not in self._flags:
            self._flags += "d" if value else ""

    @property
    def ignoreCase(self) -> bool:
        """[Whether to ignore case while attempting a match in a string.]

        Returns:
            [bool]: [True if ignoreCase, False otherwise]
        """
        return "i" in self._flags

    @ignoreCase.setter
    def ignoreCase(self, value: bool):
        """[Whether to ignore case while attempting a match in a string.]
        Args:
            value (bool): [True if ignoreCase, False otherwise]
        """
        if "i" not in self._flags:
            self._flags += "i" if value else ""

    @property
    def unicode(self) -> bool:
        """[Whether or not Unicode features are enabled.]

        Returns:
            [bool]: [True if unicode, False otherwise]
        """
        return "u" in self._flags

    @unicode.setter
    def unicode(self, value: bool):
        """[Whether or not Unicode features are enabled.]
        Args:
            value (bool): [True if unicode, False otherwise]
        """
        if "u" not in self._flags:
            self._flags += "u" if value else ""

    def _re_flags(self) -> int:
        flags = 0
        if self.ignoreCase:
            flags |= re.IGNORECASE
        if self.multiline:
            flags |= re.MULTILINE
        if self.dotAll:
            flags |= re.DOTALL
        return flags

    def compile(
        self, expression: str | "RegExp" | None = None, flags: str | None = None
    ) -> "RegExp":
        """(Re-)compiles a regular expression during execution of a script."""
        new_expression = self.expression
        new_flags = self._flags
        if isinstance(expression, RegExp):
            new_expression = expression.expression
            new_flags = expression._flags if flags is None else str(flags).lower()
        elif expression is not None:
            new_expression = str(expression)
            if flags is not None:
                new_flags = str(flags).lower()
        elif flags is not None:
            new_flags = str(flags).lower()

        old_expression, old_flags = self.expression, self._flags
        self.expression, self._flags = new_expression, new_flags
        try:
            self._compiled()
        except Exception:
            self.expression, self._flags = old_expression, old_flags
            raise
        self.lastIndex = 0
        return self

    def exec(self, s: str):
        """Search *s* for a match.

        Returns ``None`` on no match. Otherwise a list whose ``[0]`` is the full
        match and ``[1:]`` the capture groups, with ``.index`` / ``.input`` /
        ``.groups`` attributes (JavaScript's ``RegExp.exec``). When the ``g`` or
        ``y`` flag is set, the search resumes from ``lastIndex`` and advances it.
        """
        s = str(s)
        pattern = self._compiled()
        anchored = self.sticky
        stateful = self.global_ or anchored
        start = self.lastIndex if stateful else 0
        if start > len(s):
            if stateful:
                self.lastIndex = 0
            return None
        m = pattern.match(s, start) if anchored else pattern.search(s, start)
        if not m:
            if stateful:
                self.lastIndex = 0
            return None
        if stateful:
            self.lastIndex = m.end() if m.end() > m.start() else m.end() + 1
        result = _RegExpMatch([m.group(0), *m.groups()])
        result.index = m.start()
        result.input = s
        result.groups = m.groupdict()
        return result

    def replace(self, string: str, replacement: "str | Callable[..., str]") -> str:
        """``regexp.replace(str, repl)`` -- JavaScript's ``RegExp[Symbol.replace]``.

        Equivalent to ``String(str).replace(self, repl)``: honours the ``g``
        flag and expands ``$1`` / ``$&`` / ``$<name>`` in a string replacement.
        """
        return String(string).replace(self, replacement)

    def split(self, string: str, limit: int | None = None) -> list[str]:
        parts = self._compiled().split(str(string))
        return parts if limit is None else parts[:limit]

    def test(self, s: str) -> bool:
        """[Tests for a match in its string parameter.]

        Args:
            s (str): [a string to match]

        Returns:
            [bool]: [True if match else False]
        """
        pattern = self._compiled()
        stateful = self.global_ or self.sticky
        start = self.lastIndex if stateful else 0
        m = (
            pattern.match(str(s), start)
            if self.sticky
            else pattern.search(str(s), start)
        )
        if m and stateful:
            self.lastIndex = m.end() if m.end() > m.start() else m.end() + 1
        elif stateful:
            self.lastIndex = 0
        return m is not None

    def toString(self) -> str:
        """``/source/flags`` -- like JavaScript's ``RegExp.prototype.toString``."""
        order = "dgimsuvy"
        flags = "".join(f for f in order if f in self._flags)
        source = self.expression or "(?:)"
        return f"/{source}/{flags}"

    def __str__(self) -> str:
        """The pattern source (not the ``/source/flags`` form; use ``toString``)."""
        return self.expression

    # def [@@match]()
    # Performs match to given string and returns match result.
    # def [@@matchAll]()
    # Returns all matches of the regular expression against a string.
    # def [@@replace]()
    # Replaces matches in given string with new substring.
    # def [@@search]()
    # Searches the match in given string and returns the index the pattern found in the string.
    # def [@@split]()
    # Splits given string into an array by separating the strin


def ToInt32(v: int) -> int:
    return v >> 0


def ToUint32(v: int) -> int:
    return (v >> 0) if v >= 0 else ((v + 0x100000000) >> 0)


class ArrayBuffer:
    # backing store is an ``array.array`` here, but subclasses (DataView,
    # typed arrays) put other buffer-likes here, so keep it untyped
    buffer: Any

    def __init__(self, length: int) -> None:
        # self.length = length
        self.buffer = array.array("B", [0] * length)
        # self.byteLength = length
        self.isView = False

    @property
    def byteLength(self) -> int:
        return self.buffer.buffer_info()[1]

    def __getitem__(self, index: int) -> int:
        return self.buffer[index]

    def __setitem__(self, index: int, value: int) -> None:
        self.buffer[index] = value

    def __getattr__(self, name: str) -> Any:
        return getattr(self.buffer, name)

    def __len__(self) -> int:
        # return self.length
        return len(self.buffer)

    @property
    def length(self) -> int:
        # return self.__length
        return len(self.buffer)

    # @length.setter

    def __str__(self) -> str:
        return str(self.buffer)

    def __repr__(self) -> str:
        return repr(self.buffer)

    def slice(self, start: int, end: int) -> array.array:
        return self.buffer[start:end]

    def _read(self, index: int, size: int, littleEndian: bool = False) -> list[int]:
        chunk = [self.buffer[index + offset] for offset in range(size)]
        return list(reversed(chunk)) if littleEndian and size > 1 else chunk

    def _write(
        self, index: int, values: Sequence[int], littleEndian: bool = False
    ) -> None:
        chunk = (
            list(reversed(list(values)))
            if littleEndian and len(values) > 1
            else list(values)
        )
        for offset, value in enumerate(chunk):
            self.buffer[index + offset] = value

    def getUint8(self, index: int) -> int:
        return __byteutils__().unpackU8(self._read(index, 1))

    def getInt8(self, index: int) -> int:
        return __byteutils__().unpackI8(self._read(index, 1))

    def getUint16(self, index: int, littleEndian: bool = False) -> int:
        return __byteutils__().unpackU16(self._read(index, 2, littleEndian))

    def getInt16(self, index: int, littleEndian: bool = False) -> int:
        return __byteutils__().unpackI16(self._read(index, 2, littleEndian))

    def getUint32(self, index: int, littleEndian: bool = False) -> int:
        return __byteutils__().unpackU32(self._read(index, 4, littleEndian))

    def getInt32(self, index: int, littleEndian: bool = False) -> int:
        return __byteutils__().unpackI32(self._read(index, 4, littleEndian))

    def getFloat32(self, index: int, littleEndian: bool = False) -> Any:
        return __byteutils__().unpackF32(self._read(index, 4, littleEndian))

    def getFloat64(self, index: int, littleEndian: bool = False) -> Any:
        return __byteutils__().unpackF64(self._read(index, 8, littleEndian))

    def setUint8(self, index: int, value: Any) -> None:
        self._write(index, __byteutils__().packU8(int(value)))

    def setInt8(self, index: int, value: Any) -> None:
        self._write(index, __byteutils__().packI8(int(value)))

    def setUint16(self, index: int, value: Any, littleEndian: bool = False) -> None:
        self._write(index, __byteutils__().packU16(int(value)), littleEndian)

    def setInt16(self, index: int, value: Any, littleEndian: bool = False) -> None:
        self._write(index, __byteutils__().packI16(int(value)), littleEndian)

    def setUint32(self, index: int, value: Any, littleEndian: bool = False) -> None:
        self._write(index, __byteutils__().packU32(int(value)), littleEndian)

    def setInt32(self, index: int, value: Any, littleEndian: bool = False) -> None:
        self._write(index, __byteutils__().packI32(int(value)), littleEndian)

    def setFloat32(self, index: int, value: Any, littleEndian: bool = False) -> None:
        self._write(index, __byteutils__().packF32(float(value)), littleEndian)

    def setFloat64(self, index: int, value: Any, littleEndian: bool = False) -> None:
        self._write(index, __byteutils__().packF64(float(value)), littleEndian)


class DataView(ArrayBuffer):
    # ?? is this right. don't look lt
    def __init__(
        self, buffer: Any, byteOffset: int = 0, byteLength: int | None = None
    ) -> None:
        super().__init__(0 if byteLength is None else byteLength)
        self.isView = True
        self.buffer = buffer
        self.byteOffset = byteOffset
        self._viewByteLength = (
            buffer.byteLength - byteOffset if byteLength is None else byteLength
        )

    @property
    def byteLength(self) -> int:
        return self._viewByteLength

    def getUint8(self, index: int) -> Any:
        return self.buffer.getUint8(self.byteOffset + index)

    def getInt8(self, index: int) -> Any:
        return self.buffer.getInt8(self.byteOffset + index)

    def getUint16(self, index: int, littleEndian: bool = False) -> Any:
        return self.buffer.getUint16(self.byteOffset + index, littleEndian)

    def getInt16(self, index: int, littleEndian: bool = False) -> Any:
        return self.buffer.getInt16(self.byteOffset + index, littleEndian)

    def getUint32(self, index: int, littleEndian: bool = False) -> Any:
        return self.buffer.getUint32(self.byteOffset + index, littleEndian)

    def getInt32(self, index: int, littleEndian: bool = False) -> Any:
        return self.buffer.getInt32(self.byteOffset + index, littleEndian)

    def getFloat32(self, index: int, littleEndian: bool = False) -> Any:
        return self.buffer.getFloat32(self.byteOffset + index, littleEndian)

    def getFloat64(self, index: int, littleEndian: bool = False) -> Any:
        return self.buffer.getFloat64(self.byteOffset + index, littleEndian)

    def setUint8(self, index: int, value: Any) -> None:
        self.buffer.setUint8(self.byteOffset + index, value)

    def setInt8(self, index: int, value: Any) -> None:
        self.buffer.setInt8(self.byteOffset + index, value)

    def setUint16(self, index: int, value: Any, littleEndian: bool = False) -> None:
        self.buffer.setUint16(self.byteOffset + index, value, littleEndian)

    def setInt16(self, index: int, value: Any, littleEndian: bool = False) -> None:
        self.buffer.setInt16(self.byteOffset + index, value, littleEndian)

    def setUint32(self, index: int, value: Any, littleEndian: bool = False) -> None:
        self.buffer.setUint32(self.byteOffset + index, value, littleEndian)

    def setInt32(self, index: int, value: Any, littleEndian: bool = False) -> None:
        self.buffer.setInt32(self.byteOffset + index, value, littleEndian)

    def setFloat32(self, index: int, value: Any, littleEndian: bool = False) -> None:
        self.buffer.setFloat32(self.byteOffset + index, value, littleEndian)

    def setFloat64(self, index: int, value: Any, littleEndian: bool = False) -> None:
        self.buffer.setFloat64(self.byteOffset + index, value, littleEndian)


class TypedArray:

    BYTES_PER_ELEMENT: int = 1
    buffer: Any
    length: int
    byteLength: int
    byteOffset: int
    # injected per subclass via the type() call below
    _pack: Callable[..., list[int]]
    _unpack: Callable[..., int]

    def __init__(self, *args: Any) -> None:
        """[ creates a new Int8Array
            can take the following forms:
                Int8Array()
                Int8Array(length)
                Int8Array(typedArray)
                Int8Array(object)
                Int8Array(buffer)
                Int8Array(buffer, byteOffset)
                Int8Array(buffer, byteOffset, length)
        ]
        """
        self.name = "Int8Array"
        self.byteOffset = 0
        # self.BYTES_PER_ELEMENT = Int8Array.BYTES_PER_ELEMENT

        if len(args) == 0:
            self.buffer = array.array("B", [0] * 0)
            self.length = 0
            self.byteLength = self.length * self.BYTES_PER_ELEMENT
            self.isView = False
            return

        arg = args[0]

        if isinstance(arg, (Int8Array, ArrayBuffer)):
            # self.buffer = arg.buffer
            # self.byteLength = arg.byteLength
            # self.length = arg.length
            # self.isView = arg.isView

            self.buffer = arg

            if len(args) > 1:
                self.byteOffset = args[1]
            else:
                self.byteOffset = 0
            self.byteOffset = ToUint32(self.byteOffset)
            # if (this.byteOffset > this.buffer.byteLength) {
            # throw new RangeError("byteOffset out of range");
            # }
            if self.byteOffset > self.buffer.byteLength:
                # raise RangeError("byteOffset out of range")
                raise Exception("byteOffset out of range")

            # if (this.byteOffset % this.BYTES_PER_ELEMENT) {
            # // The given byteOffset must be a multiple of the element size of the specific type,
            # otherwise an exception is raised.
            # throw new RangeError("ArrayBuffer length minus the byteOffset is not a multiple of the element size.");
            # }
            if self.byteOffset % self.BYTES_PER_ELEMENT:
                # raise RangeError("ArrayBuffer length minus the byteOffset is not a multiple of the element size.")
                raise Exception(
                    "ArrayBuffer length minus the byteOffset is not a multiple of the element size."
                )

            if len(args) < 3:
                self.byteLength = self.buffer.byteLength - self.byteOffset

                if self.byteLength % self.BYTES_PER_ELEMENT:
                    # raise RangeError("length of buffer minus byteOffset not a multiple of the element size");
                    raise Exception(
                        "length of buffer minus byteOffset not a multiple of the element size"
                    )

                self.length = self.byteLength // self.BYTES_PER_ELEMENT
            else:
                self.length = ToUint32(args[2])
                self.byteLength = self.length * self.BYTES_PER_ELEMENT
            if (self.byteOffset + self.byteLength) > self.buffer.byteLength:
                # raise RangeError("byteOffset and length reference an area beyond the end of the buffer");
                raise Exception(
                    "byteOffset and length reference an area beyond the end of the buffer"
                )

            return
        # elif isinstance(arg, array.array):
        #     self.buffer = arg
        #     self.byteLength = len(arg)
        #     self.length = len(arg)
        #     self.isView = False
        #     if len(args) == 2:
        #         self.byteOffset = args[1]
        #     if len(args) == 3:
        #         self.byteOffset = args[1]
        #         self.length = args[2]
        #     return
        elif isinstance(arg, dict):
            self.buffer = array.array("B", [0] * 0)
            self.byteLength = 0
            # self.length = 0
            self.isView = False
            self.set(arg)
            return
        elif isinstance(arg, int):
            # self.buffer = array.array('B', [0] * arg)
            # self.buffer = ArrayBuffer(arg)
            # self.byteLength = arg
            # self.length = arg
            # self.isView = False

            # // Constructor(unsigned long length)
            self.length = ToInt32(args[0])
            if self.length < 0:
                raise Exception(
                    "ArrayBufferView size is not a small enough positive integer"
                )

            self.byteLength = self.length * self.BYTES_PER_ELEMENT
            self.buffer = ArrayBuffer(self.byteLength)
            self.byteOffset = 0

            return
        elif isinstance(arg, list):

            # self.buffer = array.array('B', arg)
            # self.byteLength = len(arg)
            # self.length = len(arg)
            # self.isView = False

            # // Constructor(sequence<type> array)
            sequence = arg

            self.length = ToUint32(len(sequence))
            self.byteLength = self.length * self.BYTES_PER_ELEMENT
            self.buffer = ArrayBuffer(self.byteLength)
            self.byteOffset = 0

            for i in range(self.length):
                s = sequence[i]
                self.__setitem__(i, Number(s))

            return
        else:
            raise TypeError("Invalid argument type")

    # @property
    # def length(self):
    #     return self.buffer.buffer_info()[1]

    # @length.setter
    # def length(self, value):
    #     self.buffer.length = value

    @property
    def args(self) -> Any:
        return self.buffer

    @staticmethod
    def of(*args: Any) -> Any:
        # Creates a new Int8Array with a variable number of arguments
        return Int8Array(list(args))

    @staticmethod
    def from_(thing: Any) -> Any:
        # Creates a new Int8Array from an array-like or iterable object
        if isinstance(thing, tuple):
            return Int8Array(list(thing))
        return Int8Array(thing)

    # def __getitem__(self, index):
    #     return self.buffer[index]

    # def __setitem__(self, index, value):
    #     self.buffer[index] = value

    # // getter type (unsigned long index);
    def __getitem__(self, index: int | None) -> Any:
        if index is None:
            raise SyntaxError("Not enough arguments")

        index = ToUint32(index)
        if index >= self.length:
            return undefined

        b = []
        i = 0
        o = self.byteOffset + index * self.BYTES_PER_ELEMENT
        for i in range(0, self.BYTES_PER_ELEMENT):
            b.append(self.buffer[o])
            o += 1
        return self._unpack(b)

    # // NONSTANDARD: convenience alias for getter: type get(unsigned long index);
    get = __getitem__

    # // setter void (unsigned long index, type value);
    def __setitem__(self, index: int | None, value: Any) -> None:
        if index is None and value is None:
            raise SyntaxError("Not enough arguments")

        index = ToUint32(index if index is not None else 0)
        if index >= self.length:
            return

        packed_value = value.x if isinstance(value, Number) else value
        b = self._pack(packed_value)
        i = 0
        o = self.byteOffset + index * self.BYTES_PER_ELEMENT
        for i in range(0, self.BYTES_PER_ELEMENT):
            self.buffer[o] = b[i]
            o += 1

    # // void set(TypedArray array, optional unsigned long offset);
    # // void set(sequence<type> array, optional unsigned long offset);
    def set(self, index: Any, value: Any = None) -> None:
        if index is None:
            raise SyntaxError("Not enough arguments")
        offset = ToUint32(0 if value is None else value)

        if isinstance(index, TypedArray):
            sequence = [index[i] for i in range(index.length)]
        elif isinstance(index, Sequence) and not isinstance(
            index, (str, bytes, bytearray)
        ):
            sequence = list(index)
        else:
            raise TypeError("Unexpected argument type(s)")

        if offset + len(sequence) > self.length:
            raise Exception("Offset plus length of arr is out of range")

        for i, item in enumerate(sequence):
            self.__setitem__(offset + i, item)

    # // TypedArray subarray(long begin, optional long end);

    def subarray(self, start: int | None, end: int | None):
        def clamp(v: int, minimum: int, maximum: int) -> int:
            m1 = maximum if v > maximum else v
            return minimum if v < minimum else m1

        if start is None:
            start = 0
        if end is None:
            end = self.length

        start = ToInt32(start)
        end = ToInt32(end)

        if start < 0:
            start = self.length + start
        if end < 0:
            end = self.length + end

        start = clamp(start, 0, self.length)
        end = clamp(end, 0, self.length)

        nlen = end - start
        if nlen < 0:
            nlen = 0

        return self.__class__(
            self.buffer, self.byteOffset + start * self.BYTES_PER_ELEMENT, nlen
        )


def as_signed(value: int, bits: int) -> int:
    """Converts an unsigned integer to a signed integer."""
    sign_bit = 1 << (bits - 1)
    mask = (1 << bits) - 1
    value &= mask
    return value - (1 << bits) if value & sign_bit else value


def as_unsigned(value: int, bits: int) -> int:
    return value & ((1 << bits) - 1)


class __byteutils__:
    def packI8(self, n: int) -> list[int]:
        return [n & 0xFF]
        # return struct.pack('B', n)

    def unpackI8(self, b: list[int]) -> int:
        return as_signed(b[0], 8)
        # return struct.unpack('B', b)[0]

    def packU8(self, n: int) -> list[int]:
        return [n & 0xFF]
        # return struct.pack('B', n)

    def unpackU8(self, bytes: list[int]) -> int:
        return as_unsigned(bytes[0], 8)
        # return struct.unpack('B', bytes)[0]

    def packU8Clamped(self, n: int) -> list[int]:
        n = Math.round(Number(n))
        # return [n < 0 ? 0 : n > 0xff ? 0xff : n & 0xff]
        if n < 0:
            return [0]
        elif n > 0xFF:
            return [0xFF]
        else:
            return [n & 0xFF]
        # return struct.pack('B', n)

    def packI16(self, n: int) -> list[int]:
        return [(n >> 8) & 0xFF, n & 0xFF]
        # return struct.pack('>H', n)

    def unpackI16(self, bytes: list[int]) -> int:
        return as_signed(bytes[0] << 8 | bytes[1], 16)
        # return struct.unpack('>H', bytes)[0]

    def packU16(self, n: int) -> list[int]:
        return [(n >> 8) & 0xFF, n & 0xFF]
        # return struct.pack('>H', n)

    def unpackU16(self, bytes: list[int]) -> int:
        return as_unsigned(bytes[0] << 8 | bytes[1], 16)
        # return struct.unpack('>H', bytes)[0]

    def packI32(self, n: int) -> list[int]:
        return [(n >> 24) & 0xFF, (n >> 16) & 0xFF, (n >> 8) & 0xFF, n & 0xFF]
        # return struct.pack('>I', n)

    def unpackI32(self, bytes: list[int]) -> int:
        return as_signed(bytes[0] << 24 | bytes[1] << 16 | bytes[2] << 8 | bytes[3], 32)
        # return struct.unpack('>I', bytes)[0]

    def packU32(self, n: int) -> list[int]:
        return [(n >> 24) & 0xFF, (n >> 16) & 0xFF, (n >> 8) & 0xFF, n & 0xFF]
        # return struct.pack('>I', n)

    def unpackU32(self, bytes: list[int]) -> int:
        return as_unsigned(
            bytes[0] << 24 | bytes[1] << 16 | bytes[2] << 8 | bytes[3], 32
        )
        # return struct.unpack('>I', bytes)[0]

    def packIEEE754(self, v: float, ebits: int, fbits: int) -> list[Any]:
        if (ebits, fbits) == (8, 23):
            return list(struct.pack(">f", v))
        if (ebits, fbits) == (11, 52):
            return list(struct.pack(">d", v))
        raise NotImplementedError(
            f"Unsupported IEEE754 layout: ebits={ebits}, fbits={fbits}"
        )

    def unpackIEEE754(self, bytes: list[int], ebits: int, fbits: int) -> Any:
        data = (
            bytes
            if isinstance(bytes, (builtins.bytes, bytearray))
            else builtins.bytes(bytes)
        )
        if (ebits, fbits) == (8, 23):
            return struct.unpack(">f", data)[0]
        if (ebits, fbits) == (11, 52):
            return struct.unpack(">d", data)[0]
        raise NotImplementedError(
            f"Unsupported IEEE754 layout: ebits={ebits}, fbits={fbits}"
        )

    def unpackF64(self, b: list[int]) -> Any:
        return struct.unpack(">d", bytes(b))[0]

    def packF64(self, v: float) -> list[Any]:
        return list(struct.pack(">d", v))

    def unpackF32(self, b: list[int]) -> Any:
        return struct.unpack(">f", bytes(b))[0]

    def packF32(self, v: float) -> list[Any]:
        return list(struct.pack(">f", v))


class Int8Array(TypedArray):
    name = "Int8Array"
    BYTES_PER_ELEMENT = 1
    _pack = __byteutils__.packI8
    _unpack = __byteutils__.unpackI8



class Uint8Array(TypedArray):
    name = "Uint8Array"
    BYTES_PER_ELEMENT = 1
    _pack = __byteutils__.packU8
    _unpack = __byteutils__.unpackU8



class Uint8ClampedArray(TypedArray):
    name = "Uint8ClampedArray"
    BYTES_PER_ELEMENT = 1
    _pack = __byteutils__.packU8Clamped
    _unpack = __byteutils__.unpackU8



class Int16Array(TypedArray):
    name = "Int16Array"
    BYTES_PER_ELEMENT = 2
    _pack = __byteutils__.packI16
    _unpack = __byteutils__.unpackI16



class Uint16Array(TypedArray):
    name = "Uint16Array"
    BYTES_PER_ELEMENT = 2
    _pack = __byteutils__.packU16
    _unpack = __byteutils__.unpackU16



class Int32Array(TypedArray):
    name = "Int32Array"
    BYTES_PER_ELEMENT = 4
    _pack = __byteutils__.packI32
    _unpack = __byteutils__.unpackI32



class Uint32Array(TypedArray):
    name = "Uint32Array"
    BYTES_PER_ELEMENT = 4
    _pack = __byteutils__.packU32
    _unpack = __byteutils__.unpackU32



class Float32Array(TypedArray):
    name = "Float32Array"
    BYTES_PER_ELEMENT = 4
    _pack = __byteutils__.packF32
    _unpack = __byteutils__.unpackF32



class Float64Array(TypedArray):
    name = "Float64Array"
    BYTES_PER_ELEMENT = 8
    _pack = __byteutils__.packF64
    _unpack = __byteutils__.unpackF64



# BigInt64Array = type('BigInt64Array',
# (TypedArray,), {'name': 'BigInt64Array', '_pack': __byteutils__.packI64, '_unpack': __byteutils__.unpackI64})
# BigInt64Array.BYTES_PER_ELEMENT = 8

# BigUint64Array = type('BigUint64Array',
# (TypedArray,), {'name': 'BigUint64Array', '_pack': __byteutils__.packU64, '_unpack': __byteutils__.unpackU64})
# BigUint64Array.BYTES_PER_ELEMENT = 8


class Error(Exception):
    """JavaScript ``Error``. ``name`` defaults to ``"Error"``; ``str(err)`` is
    ``"Error: message"`` (just ``"Error"`` when there is no message)."""

    name: str = "Error"

    def __init__(self, message: Any = "", *args: Any, **kwargs: Any) -> None:
        self.message = "" if message is None else str(message)
        options = args[0] if args and isinstance(args[0], dict) else kwargs
        self.cause = options.get("cause") if isinstance(options, dict) else None
        self.stack = f"{self.name}: {self.message}"
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.name}: {self.message}" if self.message else self.name

    def toString(self) -> str:
        return self.__str__()


# each also subclasses the matching Python built-in, so ``throw new TypeError``
# in ported code is still a Python ``TypeError`` and ``except TypeError`` keeps
# working for callers that imported this module's name.
class TypeError(Error, builtins.TypeError):  # noqa: A001
    name = "TypeError"


class RangeError(Error, builtins.ValueError):
    name = "RangeError"


class SyntaxError(Error, builtins.SyntaxError):  # noqa: A001
    name = "SyntaxError"


class ReferenceError(Error, builtins.NameError):
    name = "ReferenceError"


class EvalError(Error):
    name = "EvalError"


class URIError(Error):
    name = "URIError"


class InternalError(Error):
    name = "InternalError"


class AggregateError(Error):
    """``new AggregateError(errors, message?)`` -- several errors wrapped as one."""

    name = "AggregateError"

    def __init__(
        self, errors: Any = (), message: Any = "", *args: Any, **kwargs: Any
    ) -> None:
        self.errors = list(errors) if errors is not None else []
        super().__init__(message, *args, **kwargs)


# ---- STUBBING OUT SOME NEW ONES TO WORK ON ----


class Reflect:
    """
    The Reflect object provides the following static functions which have the same names as the proxy handler methods.
    Some of these methods are also the same as corresponding methods on Object,
    although they do have some subtle differences between them.
    """

    @staticmethod
    def ownKeys(target: Any) -> list[str]:
        """Returns an array of the target object's own (not inherited) property keys."""
        return Object.getOwnPropertyNames(target)

    @staticmethod
    def apply(
        target: Callable[..., Any], thisArgument: Any, argumentsList: Sequence[Any]
    ) -> Any:
        """Calls a target function with arguments as specified by the argumentsList parameter.
        See also Function.prototype.apply()."""
        return target(*argumentsList)

    @staticmethod
    def construct(
        target: Any, argumentsList: Sequence[Any], newTarget: Any = None
    ) -> Any:
        """The new operator as a function. Equivalent to calling new target(...argumentsList).
        Also provides the option to specify a different prototype."""
        constructor = newTarget or target
        return constructor(*argumentsList)

    @staticmethod
    def defineProperty(target: Any, propertyKey: str, attributes: Any) -> Any:
        """Similar to Object.defineProperty().
        Returns a Boolean that is true if the property was successfully defined."""
        try:
            value = (
                attributes.get("value") if isinstance(attributes, dict) else attributes
            )
            if isinstance(target, dict):
                target[propertyKey] = value
            else:
                setattr(target, propertyKey, value)
            return True
        except Exception:
            return False

    @staticmethod
    def deleteProperty(target: Any, propertyKey: str) -> Any:
        """The delete operator as a function. Equivalent to calling delete target[propertyKey]."""
        try:
            if isinstance(target, dict):
                del target[propertyKey]
            else:
                delattr(target, propertyKey)
            return True
        except Exception:
            return False

    @staticmethod
    def get(target: Any, propertyKey: str, receiver: Any = None) -> Any:
        """Returns the value of the property.
        Works like getting a property from an object (target[propertyKey]) as a function.
        """
        if isinstance(target, dict):
            return target.get(propertyKey)
        return getattr(target, propertyKey, None)

    @staticmethod
    def getOwnPropertyDescriptor(target: Any, propertyKey: str) -> Any:
        """Similar to Object.getOwnPropertyDescriptor().
        Returns a property descriptor of the given property if it exists on the object,  undefined otherwise.
        """
        if isinstance(target, dict):
            if propertyKey not in target:
                return None
            return {
                "value": target[propertyKey],
                "writable": True,
                "enumerable": True,
                "configurable": True,
            }
        if hasattr(target, propertyKey):
            return {
                "value": getattr(target, propertyKey),
                "writable": True,
                "enumerable": True,
                "configurable": True,
            }
        return None

    getPrototypeOf = Object.getPrototypeOf
    # isExtensible = Object.isExtensible

    @staticmethod
    def has(target: Any, propertyKey: str) -> Any:
        """Returns a Boolean indicating whether the target has the property.
        Either as own or inherited. Works like the in operator as a function."""
        if isinstance(target, dict):
            return propertyKey in target
        return hasattr(target, propertyKey)

    @staticmethod
    def preventExtensions(target: Any) -> Any:
        """Similar to Object.preventExtensions(). Returns a Boolean that is true if the update was successful."""
        Object.preventExtensions(target)
        return True

    @staticmethod
    def set(target: Any, propertyKey: str, value: Any, receiver: Any = None) -> Any:
        """A function that assigns values to properties.
        Returns a Boolean that is true if the update was successful."""
        try:
            if isinstance(target, dict):
                target[propertyKey] = value
            else:
                setattr(target, propertyKey, value)
            return True
        except Exception:
            return False

    @staticmethod
    def setPrototypeOf(target: Any, prototype: Any) -> Any:
        """A function that sets the prototype of an object. Returns a Boolean that is true if the update was successful."""
        if isinstance(target, Object):
            target.prototype = prototype
            return True
        return False


class Symbol:

    # a global registry for symbols
    registry: list[Symbol] = []

    # Creates a new Symbol object.
    def __init__(self, symbol: Any) -> None:
        self.symbol = symbol
        self.description = str(symbol)
        self.registry.append(self)
        # self.__class__.registry = self.registry

    def hasInstance(self, obj: Symbol) -> bool:
        """[A method determining if a constructor object recognizes an object as its instance. Used by instanceof.]

        Args:
            obj ([type]): [a constructor object]

        Returns:
            [type]: [True if obj is an instance of this symbol, False otherwise]
        """
        return self.symbol == obj.symbol

    def isConcatSpreadable(self) -> bool:
        """A Boolean value indicating if an object should be flattened to its array elements.
        Used by Array.prototype.concat()."""
        return False

    def iterator(self, obj: Iterable[Any]) -> Iterator[Any]:
        """A method returning the default iterator for an object. Used by for...of."""
        return iter(obj)

    def asyncIterator(self, obj: Iterable[Any]) -> Iterator[Any]:
        """A method that returns the default AsyncIterator for an object. Used by for await...of."""
        return iter(obj)

    # A method that matches against a string, also used to determine if an object may be used as a regular expression.
    def match(self, item: Any) -> Any:
        """A method that matches the symbol against a string,
        also used to determine if an object may be used as a regular expression."""
        if isinstance(item, str):
            return self.description in item
        return self.symbol == item

    # A method that returns an iterator, that yields matches of the regular expression against a string.
    # Used by String.prototype.matchAll().
    # def matchAll(self, obj):
    #     if isinstance(obj, str):
    #         return obj == self.symbol
    #     return False

    # A method that replaces matched substrings of a string. Used by String.prototype.replace().
    # def replace(self,

    # A method that returns the index within a string that matches the regular expression.
    # Used by String.prototype.search().
    def search(self, value: str) -> int:
        if not isinstance(value, str):
            return -1
        return value.find(self.description)

    # A method that splits a string at the indices that match a regular expression. Used by String.prototype.split().
    def split(self, value: str) -> list[str]:
        if not isinstance(value, str):
            return [str(value)]
        return value.split(self.description)

    # A constructor function that is used to create derived objects.
    def species(self) -> type[Symbol]:
        return self.__class__

    # A method converting an object to a primitive value.
    def toPrimitive(self) -> Any:
        return self.symbol

    # A string value used for the default description of an object.
    # Used by Object.prototype.toString().
    def toStringTag(self) -> str:
        return "Symbol"

    # An object value of whose own and inherited property names are excluded from the with environment bindings of the associated object.
    def unscopables(self) -> dict[str, bool]:
        return {}

    # @staticmethod
    # def for(key):
    #     """ Searches for existing Symbols with the given key and returns it if found.
    #     Otherwise a new Symbol gets created in the global Symbol registry with key. """
    #     raise NotImplementedError

    # @staticmethod
    # def keyFor(sym)
    #     """ Retrieves a shared Symbol key from the global Symbol registry for the given Symbol. """
    #     raise NotImplementedError

    def toSource(self) -> Any:
        """Returns a string containing the source of the Symbol. Overrides the Object.prototype.toSource() method."""
        return f"Symbol({self.description})"

    def toString(self) -> Any:
        """Returns a string containing the description of the Symbol.
        Overrides the Object.prototype.toString() method."""
        return f"Symbol({self.description})"

    def valueOf(self) -> Any:
        """Returns the Symbol. Overrides the Object.prototype.valueOf() method."""
        return self.symbol


# class _TNow:

#     def timeZone():
#         pass

#     def instant():
#         pass

#     def plainDateTime(calendar, temporalTimeZoneLike):
#         pass

#     def plainDateTimeISO(temporalTimeZoneLike):
#         pass

#     def zonedDateTime(calendar, temporalTimeZoneLike):
#         pass

#     def zonedDateTimeISO(temporalTimeZoneLike):
#         pass

#     def plainDate(calendar, temporalTimeZoneLike):
#         pass

#     def plainDateISO(temporalTimeZoneLike):
#         pass

#     def plainTimeISO(temporalTimeZoneLike):
#         pass


# class Temporal(Object):

#     @staticmethod
#     def Now(self):
#         return _TNow()

#     @staticmethod
#     def _from(self, temporal):
#         pass


class JSON:
    """``JSON.parse`` / ``JSON.stringify`` -- JavaScript's global JSON object.

    Thin wrapper over :mod:`domonic.JSON` so ports can ``from
    domonic.javascript import JSON`` and call it the browser way.
    """

    @staticmethod
    def parse(text: Any, reviver: Any = None) -> Any:
        import importlib

        return importlib.import_module("domonic.JSON").parse(text)

    @staticmethod
    def stringify(value: Any, replacer: Any = None, space: Any = None) -> str:
        import importlib

        kwargs: dict[str, Any] = {}
        if space is not None:
            kwargs["indent"] = space
        else:
            # JS emits no spaces after ':' / ',' when there is no space arg
            kwargs["separators"] = (",", ":")
        return importlib.import_module("domonic.JSON").stringify(value, **kwargs)


# ``Object.is`` / ``Array#with`` -- the JS names are Python keywords, so expose
# both the underscore form (callable from Python source) and the real name
# (reachable via getattr, and present for feature detection).
setattr(Object, "is", Object.is_)
setattr(Array, "with", Array.with_)


# ``from domonic.javascript import *`` must not quietly shadow Python's own
# ``TypeError`` / ``SyntaxError`` / ``AggregateError`` (they break ``except`` /
# ``assertRaises`` in code that never asked for the JS versions). They stay
# importable by name -- ``from domonic.javascript import TypeError``.
_STAR_HIDDEN = {"TypeError", "SyntaxError", "AggregateError", "_STAR_HIDDEN"}
__all__ = [
    _n
    for _n in dir()
    if not _n.startswith("_") and _n not in _STAR_HIDDEN
]


'''

class Atomics():
    """
    The Atomics object provides atomic operations as static methods
    They are used with SharedArrayBuffer and ArrayBuffer objects.

    When memory is shared, multiple threads can read and write the same data in memory.
    Atomic operations make sure that predictable values are written and read,
    that operations are finished before the next operation starts and that operations are not interrupted.

    Wait and notify
    The wait() and notify() methods are modeled on Linux futexes ("fast user-space mutex") and provide ways for waiting
    until a certain condition becomes true and are typically used as blocking constructs.
    """

    @staticmethod
    def add(array, index, value):
        """ Adds the provided value to the existing value at the specified index of the array.
            Returns the old value at that index."""
        return array.add(index, value)

    def and_(array, index, value):
        """ Computes a bitwise AND on the value at the specified index of the array with the provided value.
        Returns the old value at that index."""
        raise NotImplementedError

    @staticmethod
    """ Stores a value at the specified index of the array, if it equals a value. Returns the old value."""
    def compareExchange(array, index, value):
        raise NotImplementedError

    @staticmethod
    def exchange():
        """ Stores a value at the specified index of the array. Returns the old value."""
        raise NotImplementedError

    @staticmethod
    def isLockFree(size):
        """ An optimization primitive that can be used to determine whether to use locks or atomic operations.
        Returns true if an atomic operation on arrays of the given element size will be implemented
        using a hardware atomic operation (as opposed to a lock). Experts only."""
        raise NotImplementedError

    @staticmethod
    def load():
        """ Returns the value at the specified index of the array."""
        raise NotImplementedError

    # @staticmethod
    # """ Notifies agents that are waiting on the specified index of the array.
    # Returns the number of agents that were notified."""
    # def notify(

    @staticmethod
    def or_():
        """ Computes a bitwise OR on the value at the specified index of the array with the provided value.
        Returns the old value at that index."""
        raise NotImplementedError

    @staticmethod
    def store():
        """ Stores a value at the specified index of the array. Returns the value."""
        raise NotImplementedError
    @staticmethod
    def sub():
        """ Subtracts a value at the specified index of the array. Returns the old value at that index."""
        raise NotImplementedError
    @staticmethod
    def wait():
        """ Verifies that the specified index of the array still contains a value and sleeps awaiting or times out.
        Returns either "ok", "not-equal", or "timed-out". If waiting is not allowed in the calling agent
        then it throws an Error exception. (Most browsers will not allow wait() on the browser's main thread.)"""
        raise NotImplementedError
    @staticmethod
    def xor():
        """ Computes a bitwise XOR on the value at the specified index of the array with the provided value.
        Returns the old value at that index."""
        raise NotImplementedError

'''

# debugger  Stops the execution of JavaScript, and calls (if available) the debugging function  Statements
