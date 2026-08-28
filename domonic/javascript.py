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

# import chunk
import datetime
import gc
import inspect
import importlib
import importlib.util
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
import time
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

    class parserinfo:
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
        except (TypeError, ValueError, IndexError):
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
from domonic.webapi.webworkers import Worker as _WebWorker
from domonic.webapi.webstorage import Storage

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


# TODO - list all javascript keywords to python keywords
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
    except (TypeError, ValueError):
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


class Object:
    def __init__(
        self, obj: Any = None, *args: Mapping[str, Any], **kwargs: Any
    ) -> None:
        """[Creates a Javascript-like Object in python]

        Args:
            obj ([type]): [pass an object, dict or callable to the contructor]
        """
        # print('object created!')
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
                self.__dict__.update(args)
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
        if propertiesObject is None:
            return Object(proto)

        if isinstance(propertiesObject, dict):
            return Object(propertiesObject)
        elif isinstance(propertiesObject, Object):
            return propertiesObject
        elif isinstance(propertiesObject, list):
            return Object.fromEntries(propertiesObject)
        else:
            return propertiesObject

        # return Object(propertiesObject)

    #     obj = {}
    #     for key in proto.keys():
    #         obj[key] = propertiesObject[key]
    #     return obj

    @staticmethod
    def defineProperty(obj: dict[str, Any], prop: str, descriptor: Any) -> None:
        """Adds the named property described by a given descriptor to an object."""
        obj[prop] = descriptor

    # @staticmethod
    # def defineProperties(obj, props):
    #     """ Adds the named properties described by the given descriptors to an object. """
    #     for prop, desc in props.items():
    #         obj.__define_property__(prop, desc)  # TODO - obviously that wont work

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

    def valueOf(self) -> Object:
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
            if state.get("_Object__frozen", False) or state.get("_Object__sealed", False):
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
            except TypeError:
                return self.func()
        try:
            return self.func(*args)
        except TypeError:
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
            except TypeError as e:
                print(e)
                return self.func()

        try:
            return self.func(*args)
        except TypeError:
            return self.func()

    def toString(self) -> str:
        """[Returns a string representing the source code of the function. Overrides the]"""
        try:
            return inspect.getsource(self.func).strip()
        except (OSError, TypeError):
            name = getattr(self.func, "__name__", "")
            name = "" if name == "<lambda>" else f" {name}"
            return f"function{name}() {{ [native code] }}"


class Map:
    """Map holds key-value pairs and remembers the original insertion order of the keys."""

    def __init__(self, collection: list[Any] | dict[str, Any]) -> None:
        """[Pass a list or collection to make a Map object]

        Args:
            collection ([type]): [a list or dict]

        """
        # parses the passed collectionn
        if isinstance(collection, list):
            self.collection = dict(zip(collection, collection))
        elif isinstance(collection, dict):
            self.collection = collection
        else:
            raise TypeError("Map requires a list or dict.")

        self._data: dict[str, Any] = {}
        self._order: list[str] = []
        self._dict = self._data
        for key, value in self.collection.items():
            normalized_key = str(key)
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


# TODO - moved to webapi.xhr . might import here for convenience?
# class FormData:
#     """[utils for a form]

#     Args:
#         object ([str]): [takes a string or pyml object and returns a FormData]
#     """

#     def __init__(self, form):
#         """ creates a new FormData object. """
#         # TODO - parse to domonic.
#         # if isinstance(form, str):
#         #   self._data = domonic.loads(form) # TODO - parser wont be done enough yet
#         # if isinstance(form, Node):
#         #   self._data = form
#         raise NotImplementedError

#     def append(self, name, value, filename):
#         """ Appends a new value onto an existing key inside a FormData object,
#         or adds the key if it does not already exist. """
#         raise NotImplementedError

#     def delete(self, name):
#         """ Deletes a key/value pair from a FormData object. """
#         raise NotImplementedError

#     def entries(self):
#         """ Returns an iterator allowing to go through all key/value pairs contained in this object. """
#         raise NotImplementedError

#     def get(self, name):
#         """ Returns the first value associated with a given key from within a FormData object. """
#         raise NotImplementedError

#     def getAll(self, name):
#         """ Returns an array of all the values associated with a given key from within a FormData """
#         raise NotImplementedError

#     def has(self, name):
#         """ Returns a boolean stating whether a FormData object contains a certain key."""
#         raise NotImplementedError

#     def keys(self):
#         """ Returns an iterator allowing to go through all keys of the key/value pairs contained in this object."""
#         raise NotImplementedError

#     def set(self, name, value, filename):
#         """ Sets a new value for an existing key inside a FormData object,
#         or adds the key/value if it does not already exist."""
#         raise NotImplementedError

#     def values(self):
#         """ Returns an iterator allowing to go through all values  contained in this object."""
#         raise NotImplementedError


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
    def log(x: float, base: float = None) -> float:
        """Returns the natural logarithm (base E) of a number."""
        if base is None:
            return math.log(x)
        else:
            return math.log(x, base)

    @staticmethod
    @_force_number
    def max(x: float, y: float) -> float:
        """Returns the largest of two numbers."""
        return max(x, y)

    @staticmethod
    @_force_number
    def min(x: float, y: float) -> float:
        """Returns the smallest of two numbers."""
        return min(x, y)

    @staticmethod
    @_force_number
    def random() -> float:
        """Returns a random number between 0 and 1."""
        # Math.random is intentionally non-crypto.
        return random.random()  # nosec B311

    @staticmethod
    @_force_number
    def round(x: float) -> float:
        """Returns the value of a number rounded to its nearest integer."""
        return round(x)

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
    def isFinite(x) -> bool:
        """Returns true if x is a finite number"""
        value = Global.Number(x)
        if value == "NaN":
            return False
        return math.isfinite(float(value))

    @staticmethod
    def isNaN(x: Any) -> bool:
        """Determines whether a value is an illegal number"""
        value = Global.Number(x)
        if value == "NaN":
            return True
        return math.isnan(float(value))

    def NaN(self) -> str:
        """ "Not-a-Number" value"""
        # return self.NaN
        return "NaN"

    @staticmethod
    def Number(x: Any) -> int | float | str:
        """Converts an object's value to a number"""
        if isinstance(x, bool):
            return 1 if x else 0
        if x is None:
            return "NaN"
        if isinstance(x, (int, float)):
            return x
        if isinstance(x, (list, tuple)):
            if len(x) == 0:
                return 0
            if len(x) == 1:
                return Global.Number(x[0])
            return "NaN"

        if isinstance(x, str):
            value = x.strip()
            if value == "":
                return 0
            if "_" in value or value.lower() == "nan":
                return "NaN"

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
                return "NaN"
            return "NaN"

        try:
            return float(x)
        except Exception:
            return "NaN"

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
    def parseFloat(x: str) -> float | str:
        """Parses a string and returns a floating point number"""
        value = str(x).lstrip()
        match = re.match(
            r"[+-]?(?:Infinity|(?:(?:\d+\.\d*|\.\d+|\d+)(?:[eE][+-]?\d+)?))",
            value,
        )
        if not match:
            return "NaN"
        try:
            return float(match.group(0))
        except Exception:
            return "NaN"

    @staticmethod
    def parseInt(x: str, radix: int = 0) -> int | str:
        """Parses a string and returns an integer"""
        value = str(x).lstrip()
        sign = 1
        if value[:1] in ("+", "-"):
            sign = -1 if value[0] == "-" else 1
            value = value[1:]

        try:
            radix = int(radix or 0)
        except Exception:
            return "NaN"

        if radix and (radix < 2 or radix > 36):
            return "NaN"
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
            return "NaN"
        return sign * int("".join(digits), radix)

    @staticmethod
    def String(x: Any) -> str:
        """Converts an object's value to a string"""
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
        if isinstance(callback, str):
            # setTimeout string callback compatibility.
            callback = eval(callback)  # nosec B307

        timer = threading.Timer(t / 1000, callback, args=args, kwargs=kwargs)
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

    _start: float = time.time()

    def __init__(self) -> None:
        self._entries: list[Any] = []
        self._marks: dict[str, float] = {}

    def now(self) -> float:
        end = time.time()
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
    #     Performance._start = time.time()


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

        TODO - js allowed dates are larger than pythons(mysql) datetime 99999 limit
        TODO - also negative dates i.e. BC don't seem to be allowed with datetime

        Args:
            date (_type_, optional): _description_. Defaults to None.
            formatter (str, optional): _description_. Defaults to 'python'.
        """
        # join all the args on the date string
        if len(args) > 0:
            # parses dates passed in like: Date(1994, 12, 10)
            if date is None:
                date = ""
            else:
                date = str(date)
            for arg in args:
                date += " " + str(arg)
            # print("date is:::::::::::::::::::::::::::::::::::::", date)
            date = date.strip()
            if date == "":
                date = None

        self.formatter = formatter
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
        return round(time.time() * 1000)

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

    def UTC(self) -> datetime.datetime:
        """Returns the number of milliseconds in a date since midnight of January 1, 1970, according to UTC time"""
        return datetime.datetime.now(timezone.utc)

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
        # print('init')
        self.data = None
        self.state = "pending"  # fullfilled, rejected
        self._then_callbacks: list[Callable[[Any], Any]] = []
        self._catch_callbacks: list[Callable[[Any], Any]] = []
        if func is not None:
            func(self.resolve, self.reject)

    def then(self, func: Callable[[Any], Any] | None) -> Promise:
        if func is None:
            return self
        if self.state == "fulfilled":
            # print('--->',self.data)
            self._run_then(func)
            # print('-->',self.data)
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
        # print( 'resolve called::', data )
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
    #         print(e)
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

    # TODO - tell users to use other window class if methods are called.

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
    def _do_request(url: str, f: FetchedSet | None = None, **kwargs: Any) -> Any:
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
            # print(r.status_code)
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
        r = window._do_request(url, f, *kwargs)
        return f.resolve(r)

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
            thread = threading.Thread(target=window._do_request(url, f, **kwargs))
            # thread.setDaemon(True) # deprecated
            thread.daemon = True
            jobs.append(thread)
        map(lambda j: j.start(), jobs)
        map(lambda j: j.join(), jobs)
        # f = FetchedSet()
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

        jobs = []
        p = Pool()
        urls = [
            {
                "url": url,
                "f": f,
                "c": callback_function,
                "e": error_handler,
                "k": kwargs,
            }
            for url in urls
        ]
        results = p.map(_do_request_wrapper, urls)
        p.close()
        p.join()
        return f

    # def fetch_aysnc( urls: list, options={}, type="async" ):
    # TODO - a version using async/await

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
        if isinstance(obj, list):
            return Array(*obj)
        if isinstance(obj, tuple):
            return Array(*obj)
        if isinstance(obj, dict):
            return Array(*obj.items())
        if isinstance(obj, str):
            return Array(*list(obj))
        if hasattr(obj, "__iter__"):
            return Array(*list(obj))
        return Array(obj)

    @staticmethod
    def of(*args: Any) -> Array:
        """Creates a new Array instance with a variable number of arguments,
        regardless of number or type of the arguments."""
        return Array(*args)

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

    def __getitem__(self, index: int) -> Any:
        return self.args[index]

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

    def __sub__(self, value: Array | list[Any]) -> list[Any]:
        if isinstance(value, int):
            raise ValueError("int not supported")
        if isinstance(value, Array):
            self.args = self.args - value.args
        if isinstance(value, list):
            self.args = self.args - value
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

    def concat(self, *args: list[Any]) -> list[Any]:
        """[Joins two or more arrays, and returns a copy of the joined arrays]

        Returns:
            [list]: [returns a copy of the joined arrays]
        """
        for a in args:
            self.args += a
        return self.args

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

    def flatMap(self, fn: Callable[[Any], Any]) -> Array:
        """[Maps a function over an array and flattens the result]"""
        mapped = [fn(i) for i in self.args]
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
        groups = {}
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

    def findLast(self, callback: Callable[[Any, int, list[Any]], bool]) -> Any:
        """[Returns the last element in an array that passes a test]"""
        for i in range(len(self.args) - 1, -1, -1):
            if callback(self.args[i], i, self.args):
                return self.args[i]
        return None

    def findLastIndex(self, callback: Callable[[Any, int, list[Any]], bool]) -> int:
        """[Returns the last index of an element in an array that passes a test]"""
        for i in range(len(self.args) - 1, -1, -1):
            if callback(self.args[i], i, self.args):
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
        """Removes the last element of an array, and returns that element"""
        # item = self.args[len(self.args)-1]
        # del self.args[len(self.args)-1]
        return self.args.pop()

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
        """[removes the first element from an array and returns that removed element]

        Returns:
            [type]: [the removed array element]
        """
        item = self.args[0]
        del self.args[0]
        return item

    def map(self, func: Callable[[Any], Any]) -> list[Any]:
        """[Creates a new array with the result of calling a function for each array element]

        Args:
            func ([type]): [a function to call on each array element]

        Returns:
            [list]: [a new array]
        """
        # print(func)
        return [func(value) for value in self.args]
        # return map(self.args, func)

    def some(self, func: Callable[[Any], bool]) -> bool:
        """Checks if any of the elements in an array pass a test"""
        return any(func(value) for value in self.args)

    def sort(self, func: Callable[..., Any] | None = None) -> list[Any]:
        """Sorts the elements of an array"""

        if func is not None:
            return self.args.sort(key=func(*self.args))

        def comp(o: Any) -> str:
            return str(o)

        # manually sort lexicographically
        for i in range(len(self.args)):
            for j in range(i + 1, len(self.args)):
                if comp(self.args[i]) > comp(self.args[j]):
                    self.args[i], self.args[j] = self.args[j], self.args[i]
        return self.args

    def reduce(self, callback: Callable[..., Any], initialValue: Any = None) -> Any:
        """Reduces the array to a single value (going left-to-right)
        callback recieve theses parameters: previousValue, currentValue, currentIndex, array
        """
        arguments = self.args
        if initialValue is None:
            initialValue = arguments[0]
            arguments = arguments[1:]

        for i, value in enumerate(arguments):
            import inspect

            if len(inspect.signature(callback).parameters) == 4:
                initialValue = callback(initialValue, value, i, arguments)
            elif len(inspect.signature(callback).parameters) == 3:
                initialValue = callback(initialValue, value, i)
            elif len(inspect.signature(callback).parameters) == 2:
                initialValue = callback(initialValue, value)
            elif len(inspect.signature(callback).parameters) == 1:
                initialValue = callback(initialValue)
            else:
                raise Exception(
                    "Callback does not have the correct number of parameters"
                )
        return initialValue

    def reduceRight(
        self, callback: Callable[..., Any], initialValue: Any = None
    ) -> Any:
        """Reduces the array to a single value (going right-to-left)
        callback recieve theses parameters: previousValue, currentValue, currentIndex, array
        """
        arguments = self.args
        if initialValue is None:
            initialValue = arguments[-1]
            arguments = arguments[:-1]

        for i, value in enumerate(reversed(arguments)):
            import inspect

            if len(inspect.signature(callback).parameters) == 4:
                initialValue = callback(initialValue, value, i, arguments)
            elif len(inspect.signature(callback).parameters) == 3:
                initialValue = callback(initialValue, value, i)
            elif len(inspect.signature(callback).parameters) == 2:
                initialValue = callback(initialValue, value)
            elif len(inspect.signature(callback).parameters) == 1:
                initialValue = callback(initialValue)
            else:
                raise Exception(
                    "Callback does not have the correct number of parameters"
                )
        return initialValue

    def filter(self, func: Callable[[Any], bool]) -> list[Any]:
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
        return list(filter(func, self.args))

    def find(self, func: Callable[[Any], bool]) -> Any:
        """Returns the value of the first element in an array that pass a test"""
        for each in self.args:
            if func(each):
                return each

    def findIndex(self, value: Any) -> int:
        """Returns the index of the first element in an array that pass a test"""
        for i, current in enumerate(self.args):
            if callable(value):
                if value(current):
                    return i
            elif _js_strictish_equal(current, value):
                return i
        return -1

    def forEach(self, func: Callable[[Any], Any]) -> None:
        """Calls a function for each array element"""
        for index, value in enumerate(list(self.args)):
            _invoke_js_callback(func, value, index, self.args)

    def keys(self) -> Iterator[Any]:
        """Returns a Array Iteration Object, containing the keys of the original array"""
        for i in range(len(self.args)):
            yield i

    def copyWithin(
        self, target: Sequence[Any], start: int = 0, end: int | None = None
    ) -> None:
        """Copies array elements within the array, from start to end"""
        if end is None:
            end = len(target)
        for i in range(start, end):
            self.args[i] = target[i]

    def entries(self) -> Iterator[list[Any]]:
        """[Returns a key/value pair Array Iteration Object]

        Yields:
            [type]: [key/value pair]
        """
        for i, value in enumerate(self.args):
            yield [i, value]

    def every(self, func: Callable[[Any], bool]) -> bool:
        """[Checks if every element in an array pass a test]

        Args:
            func ([type]): [test function]

        Returns:
            [bool]: [if every array elemnt passed the test]
        """
        return all(func(value) for value in self.args)

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


Array.prototype = Array


class Set:
    def __init__(self, *args: Any) -> None:
        """Store unique values of any type in insertion order."""
        self.args = []
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

    # print(sys.float_info)
    MAX_VALUE = list(sys.float_info)[0]
    MIN_VALUE = 5e-324  # CHANGE no longer >  list(sys.float_info)[3]

    NEGATIVE_INFINITY = float(
        "-inf"
    )  #: Represents negative infinity (returned on overflow) Number
    POSITIVE_INFINITY = float(
        "inf"
    )  #: Represents infinity (returned on overflow)  Number

    # prototype Allows you to add properties and methods to an object   Number

    def __init__(self, x: Any = "", *args: Any, **kwargs: Any) -> None:
        self.x = Global.Number(x)

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

    def isInteger(self) -> bool:
        """Checks whether a value is an integer"""
        return type(self.x) == int

    def isSafeInteger(self) -> bool:
        """Checks whether a value is a safe integer"""
        value = self.x
        if isinstance(value, bool) or value == "NaN":
            return False
        try:
            numeric = float(value)
        except (TypeError, ValueError):
            return False
        return (
            math.isfinite(numeric)
            and numeric.is_integer()
            and -(2**53 - 1) <= numeric <= 2**53 - 1
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

        # print(  "AND:", n, "e" , e )
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
        # print("DIGIT!", digits)
        if digits < 0:
            digits = 0

        fstring = "{:." + str(digits) + "f}"
        return fstring.format(round(self.x, digits))

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

    def toString(self, base: int | None) -> str:
        """[returns a string representing the specified Number object.]

        Args:
            base (int): [An integer in the range 2 through 36
                specifying the base to use for representing numeric values.]

        Returns:
            [str]: [a string representing the specified Number object]
        """
        if base is None:
            return str(self.x)

        import string

        digs = string.digits + string.ascii_letters

        if self.x < 0:
            sign = -1
        elif self.x == 0:
            return digs[0]
        else:
            sign = 1

        self.x *= sign
        digits = []

        while self.x:
            digits.append(digs[int(self.x % base)])
            self.x = int(self.x / base)

        if sign < 0:
            digits.append("-")

        digits.reverse()

        return "".join(digits)


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
    def raw(string: str) -> str:
        """Returns the string as-is"""
        import re

        return re.escape(string)

    # @staticmethod
    # def fromCharCode(code: int):
    #     """ Converts a Unicode code point into a string """
    #     return chr(code)

    @staticmethod
    def toCharCode(char: str) -> int:
        """Converts a Unicode string into a code point"""
        return ord(char)

    def __init__(self, x: Any = "", *args: Any, **kwargs: Any) -> None:
        # self.args = args
        # self.kwargs = kwargs
        self.x = str(x)

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

    def __getitem__(self, item: int | slice) -> str:
        # print(item)
        return self.x[item]

    def __add__(self, other: str) -> str:
        return self.x + str(other)

    def __radd__(self, other: str) -> str:
        return str(other) + self.x

    def __iadd__(self, other: str) -> str:
        return self.x + str(other)

    def __sub__(self, other: str) -> Any:
        return self.x - other

    def __rsub__(self, other: str) -> Any:
        return other - self.x

    def __isub__(self, other: str) -> Any:
        return self.x - other

    def __mul__(self, other: int) -> str:
        return self.x * int(other)

    def __rmul__(self, other: int) -> str:
        return self.x * int(other)

    def __imul__(self, other: int) -> str:
        return self.x * int(other)

    def split(self, expr: str | RegExp) -> list[str]:
        """[can split a string based on a regex]

        Args:
            expr ([str]): [valid regex or string to split on]

        Returns:
            [list]: [list of str]
        """

        if isinstance(expr, RegExp):
            return re.split(expr.expression, self.x)

        expr = str(expr)
        if expr == "":
            return list(self.x)
        if _looks_like_regex_separator(expr):
            try:
                return re.split(expr, self.x)
            except re.error:
                return self.x.split(expr)
        return self.x.split(expr)

    def concat(self, *args, seperator: str = "") -> str:
        """[concatenates the string arguments to the calling string and returns a new string.]

        Args:
            seperator (str, optional): []. Defaults to "".

        Returns:
            [type]: [A new string containing the combined text of the strings provided.]
        """
        args = list(args)
        args.insert(0, self.x)
        return seperator.join(args)

    # @staticmethod
    def charCodeAt(self, index: int) -> int:
        """Returns the Unicode of the character at the specified index"""
        index = int(index)
        if index < 0 or index >= len(self.x):
            return "NaN"
        return ord(self.x[index])

    # @staticmethod
    def fromCharCode(self, *codes: int) -> str:
        """returns a string created from the specified sequence of UTF-16 code units"""
        return "".join([str(chr(x)) for x in codes])

    @property
    def length(self) -> int:
        return len(self.x)

    def repeat(self, count: int) -> str:
        """Returns a new string with a specified number of copies of an existing string"""
        count = int(count)
        if count < 0:
            raise ValueError("repeat count must be non-negative")
        return self.x * count

    def startsWith(self, x: str, start: int = None, end: int = None) -> bool:
        """Checks whether a string begins with specified characters"""
        if start is None:
            start = 0
        start = max(int(start), 0)
        if end is None:
            end = len(self.x)
        # print(self.x.startswith(x, start, end))
        return self.x.startswith(x, start, end)

    def substring(self, start: int, end: int = None) -> str:
        """Extracts the characters from a string, between two specified indices"""
        length = len(self.x)
        start = min(max(int(start), 0), length)
        if end is None:
            end = length
        else:
            end = min(max(int(end), 0), length)
        if start > end:
            start, end = end, start
        return self.x[start:end]

    def endsWith(self, x: str, start: int = None, end: int = None) -> bool:
        """Checks whether a string ends with specified string/characters"""
        if start is None:
            start = 0
        if end is None:
            end = len(self.x)
        return self.x.endswith(x, start, end)

    def toLowerCase(self) -> str:
        """Converts a string to lowercase letters"""
        return self.x.lower()

    def toUpperCase(self) -> str:
        """Converts a string to uppercase letters"""
        return self.x.upper()

    def slice(self, start: int = 0, end: int = None) -> str:
        """Selects a part of an string, and returns the new string"""
        if end is None:
            end = len(self.x)
        return self.x[start:end]

    def trim(self) -> str:
        """Removes whitespace from both ends of a string"""
        return self.x.strip()

    def charAt(self, index: int) -> str:
        """[Returns the character at the specified index (position)]

        Args:
            index (int): [index position]

        Returns:
            [str]: [the character at the specified index.
            if the index is out of range, an empty string is returned.]
        """
        index = int(index)
        if index < 0 or index >= len(self.x):
            return ""
        return self.x[index]

    def replace(self, old: str, new: str | Callable[..., str]) -> str:
        """
        Searches a string for a specified value, or a regular expression,
        and returns a new string where the specified values are replaced.
        only replaces first one.
        """
        if callable(new):
            # return new(self.x, old)
            return re.sub(old, new, self.x)
        else:
            return self.x.replace(old, new, 1)
        # re.sub(r"regepx", "old", "new") # TODO - js one also takes a regex

    def replaceAll(self, old: str, new: str) -> str:
        """[returns a new string where the specified values are replaced. ES2021]

        Args:
            old ([str]): [word to remove]
            new ([str]): [word to replace it with]

        Returns:
            [str]: [new string with all occurences of old word replaced]
        """
        return self.x.replace(old, new)

    # def localeCompare():
    # """ Compares two strings in the current locale """
    # pass

    def substr(self, start: int = 0, end: int | None = None) -> str:
        """Extracts the characters from a string, beginning at a specified start position,
        and through the specified number of character"""
        length = len(self.x)
        start = int(start)
        if start < 0:
            start = max(length + start, 0)
        if end is None:
            end = length - start
        end = int(end)
        if end <= 0:
            return ""
        return self.x[start : start + end]

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
        fromIndex = max(int(fromIndex), 0)
        if fromIndex > len(self.x):
            return len(self.x) if searchValue == "" else -1
        return self.x.find(searchValue, fromIndex)

    def codePointAt(self, index: int) -> int:
        """[Returns the Unicode code point at the specified index (position)]

        Args:
            index (int): [index position]

        Returns:
            [type]: [the Unicode code point at the specified index (position)]
        """
        index = int(index)
        if index < 0 or index >= len(self.x):
            return undefined
        return ord(self.x[index])

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

    def localeCompare(self, comparisonString: str, locale: str = None, *args) -> int:
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

    def search(self, searchValue: str, position: int = 0) -> bool:
        """[returns true if the specified string is found within the calling String object,]
        starting at the specified position.
        Args:
            searchValue (str): [The string value to search for.]
            position (int, optional): [the position to search from]. Defaults to 0.
        Returns:
            [type]: [a boolean value indicating whether the search value was found.]
        """
        position = min(max(int(position), 0), len(self.x))
        return searchValue in self.x[position:]

    def matchAll(self, pattern: str) -> str:
        """
        Searches a string for a specified value, or a regular expression,
        and returns a new string where the specified values are replaced.
        only replaces first one.
        """
        return re.sub(pattern, "", self.x)

    def match(self, pattern: str) -> re.Match[str] | None:
        """
        Searches a string for a specified value, or a regular expression,
        and returns a new string where the specified values are replaced.
        only replaces first one.
        """
        return re.match(pattern, self.x)

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
        if fromIndex is None:
            fromIndex = len(self.x)
        else:
            fromIndex = min(max(int(fromIndex), 0), len(self.x))
        if searchValue == "":
            return fromIndex
        return self.x.rfind(searchValue, 0, fromIndex + len(searchValue))

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


class RegExp:
    def __init__(self, expression: str, flags: str = "") -> None:
        self.expression = expression
        self.flags = (
            flags.lower()
        )  #: A string that contains the flags of the RegExp object.
        # self.multiline  # Whether or not to search in strings across multiple lines.
        # self.source  # The text of the pattern.
        # self.sticky  # Whether or not the search is sticky
        # self.lastIndex  # The index at which to start the next match.

    @property
    def dotAll(self) -> bool:
        """[Whether . matches newlines or not.]

        Returns:
            [bool]: [True if dot matches newlines, False otherwise]
        """
        return "s" in self.flags

    @dotAll.setter
    def dotAll(self, value: bool):
        """[Whether . matches newlines or not.]
        Args:
            value (bool): [True if dot matches newlines, False otherwise]
        """
        if "s" not in self.flags:
            self.flags += "s" if value else ""

    @property
    def multiline(self) -> bool:
        """[Whether . matches newlines or not.]
        Returns:
            [bool]: [True if dot matches newlines, False otherwise]
        """
        return "m" in self.flags

    @multiline.setter
    def multiline(self, value: bool):
        """[Whether . matches newlines or not.]
        Args:
            value (bool): [True if dot matches newlines, False otherwise]
        """
        if "m" not in self.flags:
            self.flags += "m" if value else ""

    @property
    def source(self) -> str:
        """[The text of the pattern.]
        Returns:
            [str]: [The text of the pattern.]
        """
        return self.expression

    @property
    def global_(self) -> bool:
        """[Whether to test the regular expression against all possible matches in a string,
        or only against the first.]

        Returns:
            [bool]: [True if global, False otherwise]
        """
        return "g" in self.flags

    @global_.setter
    def global_(self, value: bool):
        """[Whether to test the regular expression against all possible matches in a string,
        or only against the first.]
        Args:
            value (bool): [True if global, False otherwise]
        """
        if "g" not in self.flags:
            self.flags += "g" if value else ""

    @property
    def hasIndices(self) -> bool:
        """[Whether the regular expression result exposes the start and end indices of captured substrings.]

        Returns:
            [bool]: [True if hasIndices, False otherwise]
        """
        return "d" in self.flags

    @hasIndices.setter
    def hasIndices(self, value: bool):
        """[Whether the regular expression result exposes the start and end indices of captured substrings.]
        Args:
            value (bool): [True if hasIndices, False otherwise]
        """
        if "d" not in self.flags:
            self.flags += "d" if value else ""

    @property
    def ignoreCase(self) -> bool:
        """[Whether to ignore case while attempting a match in a string.]

        Returns:
            [bool]: [True if ignoreCase, False otherwise]
        """
        return "i" in self.flags

    @ignoreCase.setter
    def ignoreCase(self, value: bool):
        """[Whether to ignore case while attempting a match in a string.]
        Args:
            value (bool): [True if ignoreCase, False otherwise]
        """
        if "i" not in self.flags:
            self.flags += "i" if value else ""

    @property
    def unicode(self) -> bool:
        """[Whether or not Unicode features are enabled.]

        Returns:
            [bool]: [True if unicode, False otherwise]
        """
        return "u" in self.flags

    @unicode.setter
    def unicode(self, value: bool):
        """[Whether or not Unicode features are enabled.]
        Args:
            value (bool): [True if unicode, False otherwise]
        """
        if "u" not in self.flags:
            self.flags += "u" if value else ""

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
        new_flags = self.flags
        if isinstance(expression, RegExp):
            new_expression = expression.expression
            new_flags = expression.flags if flags is None else str(flags).lower()
        elif expression is not None:
            new_expression = str(expression)
            if flags is not None:
                new_flags = str(flags).lower()
        elif flags is not None:
            new_flags = str(flags).lower()

        old_expression, old_flags = self.expression, self.flags
        self.expression, self.flags = new_expression, new_flags
        try:
            re.compile(self.expression, self._re_flags())
        except Exception:
            self.expression, self.flags = old_expression, old_flags
            raise
        return self

    # def exec(self, s: str):
    #     """ Executes a search for a match in its string parameter. """
    #     class Match:
    #         def __init__(self, index: int, match: str):
    #             self.index = index
    #             self.match = match
    #         def __str__(self):
    #             return f'{self.match}'
    #         def __repr__(self):
    #             return f'{self.match}'
    #         def __getitem__(self, index):
    #             return self.match[index]
    #     matches = re.finditer(self.expression, s, flags=re.MULTILINE)  # TODO - flags
    #     return [Match(m.start(), m.group(0)) for m in matches]

    # TODO - wanted to change this to be like above. but d3 required me to rollback.
    # need to check if i modifed that implementation to fit my needs at the time.
    def exec(self, s: str) -> list[str] | None:
        """Executes a search for a match in its string parameter."""
        # print("exec:", self.expression, s)
        m = re.search(self.expression, s, self._re_flags())
        # print(m)
        if m:
            groups = m.groups()
            return [group for group in groups] if groups else [m.group(0)]

    def test(self, s: str) -> bool:
        """[Tests for a match in its string parameter.]

        Args:
            s (str): [a string to match]

        Returns:
            [bool]: [True if match else False]
        """
        m = re.search(self.expression, s, self._re_flags())
        # print(m)
        if m:
            return True
        else:
            return False

    def toString(self) -> str:
        """Returns a string representation of the RegExp object."""
        return self.__str__()

    def __str__(self) -> str:
        """ " Returns a string representing the specified object.
        Overrides the Object.prototype.toString() method."""
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
        # return getattr(self.buffer, name)
        # TODO - try on self if not get from buffer. (was this a todo)?
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

    BYTES_PER_ELEMENT = 1

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

        # print(arg)
        # print(type(arg))
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

                self.length = self.byteLength / self.BYTES_PER_ELEMENT
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
        #     print('c!!!!')
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

            # print('bb!', arg)
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
        # print('set', index, value)
        if index is None and value is None:
            raise SyntaxError("Not enough arguments")

        index = ToUint32(index)
        if index >= self.length:
            return undefined

        packed_value = value.x if isinstance(value, Number) else value
        b = self._pack(packed_value)
        # print(b)
        # print(  self._pack(10) )
        # print(  self._pack(20) )
        # print(  self._pack(30) )
        i = 0
        o = self.byteOffset + index * self.BYTES_PER_ELEMENT
        for i in range(0, self.BYTES_PER_ELEMENT):
            self.buffer[o] = b[i]
            o += 1

    # // void set(TypedArray array, optional unsigned long offset);
    # // void set(sequence<type> array, optional unsigned long offset);
    def set(self, index: Any, value: Any) -> None:
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


Int8Array = type(
    "Int8Array",
    (TypedArray,),
    {
        "name": "Int8Array",
        "_pack": __byteutils__.packI8,
        "_unpack": __byteutils__.unpackI8,
    },
)
Int8Array.BYTES_PER_ELEMENT = 1

Uint8Array = type(
    "Uint8Array",
    (TypedArray,),
    {
        "name": "Uint8Array",
        "_pack": __byteutils__.packU8,
        "_unpack": __byteutils__.unpackU8,
    },
)
Uint8Array.BYTES_PER_ELEMENT = 1

Uint8ClampedArray = type(
    "Uint8ClampedArray",
    (TypedArray,),
    {
        "name": "Uint8ClampedArray",
        "_pack": __byteutils__.packU8Clamped,
        "_unpack": __byteutils__.unpackU8,
    },
)
Uint8ClampedArray.BYTES_PER_ELEMENT = 1

Int16Array = type(
    "Int16Array",
    (TypedArray,),
    {
        "name": "Int16Array",
        "_pack": __byteutils__.packI16,
        "_unpack": __byteutils__.unpackI16,
    },
)
Int16Array.BYTES_PER_ELEMENT = 2

Uint16Array = type(
    "Uint16Array",
    (TypedArray,),
    {
        "name": "Uint16Array",
        "_pack": __byteutils__.packU16,
        "_unpack": __byteutils__.unpackU16,
    },
)
Uint16Array.BYTES_PER_ELEMENT = 2

Int32Array = type(
    "Int32Array",
    (TypedArray,),
    {
        "name": "Int32Array",
        "_pack": __byteutils__.packI32,
        "_unpack": __byteutils__.unpackI32,
    },
)
Int32Array.BYTES_PER_ELEMENT = 4

Uint32Array = type(
    "Uint32Array",
    (TypedArray,),
    {
        "name": "Uint32Array",
        "_pack": __byteutils__.packU32,
        "_unpack": __byteutils__.unpackU32,
    },
)
Uint32Array.BYTES_PER_ELEMENT = 4

Float32Array = type(
    "Float32Array",
    (TypedArray,),
    {
        "name": "Float32Array",
        "_pack": __byteutils__.packF32,
        "_unpack": __byteutils__.unpackF32,
    },
)
Float32Array.BYTES_PER_ELEMENT = 4

Float64Array = type(
    "Float64Array",
    (TypedArray,),
    {
        "name": "Float64Array",
        "_pack": __byteutils__.packF64,
        "_unpack": __byteutils__.unpackF64,
    },
)
Float64Array.BYTES_PER_ELEMENT = 8

# BigInt64Array = type('BigInt64Array',
# (TypedArray,), {'name': 'BigInt64Array', '_pack': __byteutils__.packI64, '_unpack': __byteutils__.unpackI64})
# BigInt64Array.BYTES_PER_ELEMENT = 8

# BigUint64Array = type('BigUint64Array',
# (TypedArray,), {'name': 'BigUint64Array', '_pack': __byteutils__.packU64, '_unpack': __byteutils__.unpackU64})
# BigUint64Array.BYTES_PER_ELEMENT = 8


class Error(Exception):
    """Raise Errors"""

    def __init__(self, message: str, *args: Any, **kwargs: Any) -> None:
        self.message = message
        super(Error, self).__init__(message)

    # def __str__(self):
    #     return self.message


# Error
# AggregateError
# EvalError
# InternalError
# RangeError
# ReferenceError
# SyntaxError
# TypeError
# URIError


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
