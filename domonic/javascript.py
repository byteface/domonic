"""
    domonic.javascript
    ====================================
    - https://www.w3schools.com/jsref/jsref_reference.asp
    - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference

"""

from typing import Union, Tuple, List, Dict, Any, Optional, Callable

import gc
import re
import json
import os
import array
import struct
import sys
import time
import math
import random
import datetime
import threading
import signal
import urllib.parse
from urllib.parse import unquote, quote

import multiprocessing
from multiprocessing.pool import ThreadPool as Pool

from dateutil.parser import parse
import requests

from domonic.webapi.url import URL, URLSearchParams
from domonic.webapi.webstorage import Storage

def function(python_str: str) -> str:
    """[evals a string i.e.

    sup = function('''print(hi)''')
    sup()

    ]

    Args:
        python_str ([str]): [some valid python code as a string]
    """
    def anon():
        return eval(python_str)
    return anon


# TODO - list all javascript keywords to python keywords
true: bool = True
false: bool = False
null: object = None
undefined: object = None
# globalThis # TODO - do i need to use inpect? or is globals() ok?

# def typeof(v):
#     return type(v).__name__

class Boolean():
    """[Creates a Boolean Object.
        Warning this is NOT a boolean type. for that use Global.Boolean()]
    """
    def __init__(self, value=False) -> None:
        self.value: bool = Global.Boolean(value)


class Object(object):

    def __init__(self, obj=None, *args, **kwargs) -> None:
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

    def __str__(self):
        """ Returns a string representation of the object """
        d = self.__dict__.copy()
        for k, v in list(d.items()):
            if '__' in k:
                del d[k]
            if 'prototype' in k:
                del d[k]
        return str(d)

    # def __repr__(self):
    #     """ Returns a string representation of the object."""
    #     return self.toString()

    @staticmethod
    def fromEntries(entries):
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
    def assign(target, source):
        """ Copies the values of all enumerable own properties from one or more source objects to a target object. """
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
    def create(proto, propertiesObject=None):
        """ Creates a new object with the specified prototype object and properties. """
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
    def defineProperty(obj, prop, descriptor):
        """ Adds the named property described by a given descriptor to an object. """
        obj[prop] = descriptor

    # @staticmethod
    # def defineProperties(obj, props):
    #     """ Adds the named properties described by the given descriptors to an object. """
    #     for prop, desc in props.items():
    #         obj.__define_property__(prop, desc)  # TODO - obviously that wont work

    @staticmethod
    def entries(obj):
        """ Returns an array containing all of the [key, value] pairs in the object. """
        if isinstance(obj, dict):
            return [[k, v] for k, v in obj.items()]
        if isinstance(obj, (float, int)):
            return []

    @staticmethod
    def keys(obj):
        """ Returns an array containing the names of all of the given object's own enumerable string properties."""
        if isinstance(obj, dict):
            return obj.keys()
        if isinstance(obj, (float, int)):
            return []
        return obj.__dict__.keys()   # TODO - this is probably wrong

    @staticmethod
    def values(obj):
        """ Returns an array containing the values that correspond to
        all of a given object's own enumerable string properties. """
        if isinstance(obj, dict):
            return obj.values()
        if isinstance(obj, (float, int)):
            return []
        return obj.__dict__.values()  # TODO - this is probably wrong

    @staticmethod
    def getOwnPropertyDescriptor(obj, prop):
        """ Returns a property descriptor for a named property on an object. """
        if isinstance(obj, dict):
            return obj[prop]
        return obj.__dict__[prop]

    @staticmethod
    def getOwnPropertyNames(obj):
        """ Returns an array containing the names of all of the given object's
        own enumerable and non-enumerable properties. """
        if isinstance(obj, dict):
            return obj.keys()
        elif isinstance(obj, Object):
            return obj.__dict__.keys()
        elif isinstance(obj, object):
            return [prop for prop in dir(obj) if not prop.startswith('__')]
        return obj.__dict__.keys()

    # @staticmethod
    # def _is(value1, value2):
    #     """ Compares if two values are the same value.
    #     Equates all NaN values (which differs from both Abstract Equality Comparison
    #  and Strict Equality Comparison)."""
    #     pass

    @staticmethod
    def getOwnPropertySymbols(obj):
        """ Returns an array of all symbol properties found directly upon a given object. """
        if isinstance(obj, dict):
            return []
        return [prop for prop in dir(obj) if not prop.startswith('__')]

    @staticmethod
    def getPrototypeOf(obj):
        """ Returns the prototype (internal [[Prototype]] property) of the specified object. """
        if isinstance(obj, dict):
            return obj
        elif isinstance(obj, Object):
            return obj.prototype
        elif isinstance(obj, object):
            return obj.__class__
        return obj.__proto__

    # @property #TODO - static or prop?
    # def isExtensible(obj):
    #     """ Determines if extending of an object is allowed """
    #     return obj.__extensible

    # @property #TODO - static or prop?
    # def isSealed(obj):
    #     """ Determines if an object is sealed """
    #     return obj.__sealed

    # @property
    # def preventExtensions(obj):
    #     """ Prevents any extensions of an object. """
    #     if isinstance(obj, dict):
    #         return False
    #     elif isinstance(obj, Object):
    #         obj.extensible = False
    #         return True
    #     elif isinstance(obj, object):
    #         return False
    #     return False

    # @property
    # def seal(obj):
    #     """ Prevents other code from deleting properties of an object. """
    #     if isinstance(obj, dict):
    #         return False
    #     elif isinstance(obj, Object):
    #         obj.sealed = True
    #         return True
    #     elif isinstance(obj, object):
    #         return False
    #     return False

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

    @property  # TODO - static or prop?
    def isFrozen(self, obj):
        """ Determines if an object was frozen. """
        return self.__isFrozen

    @staticmethod  # TODO - static or prop?
    def freeze(obj):
        """ Freezes an object. Other code cannot delete or change its properties. """
        obj.__isFrozen = True

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

    def __defineGetter__(self, prop, func):
        """ Adds a getter function for the specified property. """
        self.__dict__[prop] = property(func)
        return self

    def __defineSetter__(self, prop, func):
        """ Associates a function with a property that, when set, calls the function. """
        self.__dict__[prop] = property(func)
        return self

    def __lookupGetter__(self, prop):
        """
        Returns the getter function for the specified property.
        """
        return self.__dict__[prop]

    def __lookupSetter__(self, prop):
        """ Returns the function associated with the specified property by the __defineSetter__() method. """
        return self.__dict__[prop]

    def hasOwnProperty(self, prop):
        """ Returns a boolean indicating whether an object contains the specified property
        as a direct property of that object and not inherited through the prototype chain. """
        # raise NotImplementedError
        # return hasattr(self, prop)
        return self.__dict__.get(prop, None) != None

    def isPrototypeOf(self, obj):
        """ Returns a boolean indicating whether an object is a copy of this object. """
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

    def toLocaleString(self):
        """ Calls toString()"""
        return self.toString()

    def toString(self):
        """ Returns a string representation of the object."""
        return '[' + self.__class__.__name__ + ': ' + str(self.__dict__) + ']'

    def valueOf(self):
        """ Returns the value of the object. """
        return self

    def __iter__(self):
        """ Iterates over object's properties. """
        for prop in self.__dict__:
            yield prop
        for key in self.__dict__:
            yield key
        # return
        # return self.__dict__.__iter__()

    def __hash__(self):
        """ Returns the hash of the object. """
        return hash(self.toString())

    def __eq__(self, other):
        """ Compares two objects. """
        if isinstance(other, Object):
            return self.toString() == other.toString()
        return False

    def __ne__(self, other):
        """ Compares two objects. """
        if isinstance(other, Object):
            return self.toString() != other.toString()
        return True

    def __nonzero__(self):
        """ Returns whether the object is false. """
        return self.toString() != ''

    def __bool__(self):
        """ Returns whether the object is false. """
        return self.toString() != ''

    # def __dict__(self):
    #     """ Returns the object's attributes as a dictionary. """
    #     return self.__dict__

    def __getitem__(self, key):
        """ Returns the value of the specified property. """
        # return self.__dict__[key]
        # return self.__dict__.get(key, None)
        return self.__dict__.get(key)

    def __deepcopy__(self, memo):
        """ Makes a deep copy of the object. """
        return self.__class__(self.__dict__)

    def __setitem__(self, key, value):
        """ Sets the value of the specified property. """
        # self.__dict__[key] = value
        return self.__dict__.__setitem__(key, value)

    def __delitem__(self, key):
        """ Deletes the specified property. """
        del self.__dict__[key]

    def __len__(self):
        """ Returns the number of properties. """
        return len(self.__dict__)

    def __contains__(self, key):
        """[Returns whether the specified property exists.]

        Args:
            key ([str]): [The name of the property to check for.]

        Returns:
            [bool]: [True if the specified property exists. Otherwise, False.]
        """
        return key in self.__dict__

    def __getattr__(self, name):
        """[gets the value of the specified property]

        Args:
            name ([str]): [the name of the property]

        Returns:
            [str]: [the value of the specified property]
        """
        return self.__getitem__(name)

    def __setattr__(self, name, val):
        """[sets the value of the specified property]

        Args:
            name ([str]): [the name of the property]
            val ([str]): [the value of the property]

        Returns:
            [str]: [the value of the property]
        """
        return self.__setitem__(name, val)

    def __delattr__(self, name):
        """[deletes the specified property]

        Args:
            name ([str]): [the name of the property]

        Returns:
            [type]: [the value of the property]
        """
        return self.__delitem__(name)

    # def __call__(self, *args, **kwargs):
    #     """ Calls the object. """
    #     return self.toString()


class Function(Object):
    """ a Function object """

    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.arguments = args
        self.caller = None
        self.displayName = None
        self.length = None
        self.name = None
        # self.isCallable = True
        # self.constructor = False
        # self.__proto__ = None

    def apply(self, thisArg=None, args=None, **kwargs):
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

    def bind(self, thisArg, *args, **kwargs):
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
    def call(self, thisArg=None, *args, **kwargs):
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

    def toString(self):
        """[Returns a string representing the source code of the function. Overrides the]
        """
        raise NotImplementedError


class Map(object):
    """ Map holds key-value pairs and remembers the original insertion order of the keys.
    """

    def __init__(self, collection):
        """[Pass a list or collection to make a Map object]

        Args:
            collection ([type]): [a list or dict]

        """
        # parses the passed collectionn
        if isinstance(collection, list):
            # create a dict from the list
            self.collection = dict(zip(collection, collection))
        if isinstance(collection, dict):
            # use the passed dict
            self.collection = collection
        else:
            raise TypeError("Map requires a list or dict.")

        self._data: dict = {}
        self._order: list = []

    def __contains__(self, key: str):
        return key in self._dict

    def __getitem__(self, key: str):
        return self._dict[key]

    def __setitem__(self, key: str, value):
        if key not in self._dict:
            self._order.append(key)
            self._dict[key] = value

    def __delitem__(self, key: str):
        self._order.remove(key)
        del self._dict[key]

    def clear(self):
        """ Removes all key-value pairs from the Map object. """
        self._data = {}
        self._order = []

    def delete(self, key: str) -> bool:
        """ Returns true if an element in the Map object existed and has been removed,
        or false if the element does not exist. Map.prototype.has(key) will return false afterwards. """
        try:
            self._order.remove(key)
            del self._dict[key]
            return True
        except Exception:
            return False

    def get(self, key: str, default=None):
        """ Returns the value associated to the key, or undefined if there is none. """
        return self._dict.get(key, default)

    def has(self, key: str) -> bool:
        """ Returns a boolean asserting whether a value has been associated to the key in the Map object or not."""
        return key in self._dict

    def set(self, key: str, value):
        """ Sets the value for the key in the Map object. Returns the Map object. """
        if key not in self._dict:
            self._order.append(key)
            self._dict[key] = value
        return self

    def iterkeys(self):
        return iter(self._order)

    def iteritems(self):
        for key in self._order:
            yield key, self._dict[key]

    def keys(self):
        """ Returns a new Iterator object that contains the keys
        for each element in the Map object in insertion order. """
        return list(self.iterkeys())

    def values(self):
        """ Returns a new Iterator object that contains the values
        for each element in the Map object in insertion order. """
        return list(self.iteritems())

    def entries(self):
        """ Returns a new Iterator object that contains an array of [key, value]
        for each element in the Map object in insertion order. """
        return [(x, self._dict[x]) for x in self._order]

    # def forEach(self, callbackFn[, thisArg]):
    #     raise NotImplementedError
            # TODO - is this supposed to pass count like Node list? i.e.
        # for i in range(len(self.args)):
            # func(self.args[i], i, self.args)

    def update(self, ordered_dict):
        for key, value in ordered_dict.iteritems():
            self[key] = value

    def __str__(self):
        return str([(x, self._dict[x]) for x in self._order])


# TODO - moved to webapi.xhr . might import here for convenience?
# class FormData(object):
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


class Worker(object):
    """[A background task that can be created via script, which can send messages back to its creator.
    Creating a worker is done by calling the Worker("path/to/worker/script") constructor.]
    TODO - JSWorker - Node
    Args:
        object ([str]): [takes a path to a python script]
    """

    def __init__(self, script):
        """ creates a new Worker object. """
        raise NotImplementedError

    def postMessage(self):
        """ Sends a message — consisting of any object — to the worker's inner scope. """
        raise NotImplementedError

    def terminate(self):
        """ Immediately terminates the worker. This does not let worker finish its operations; it is halted at once.
        ServiceWorker instances do not support this method. """
        raise NotImplementedError


class Math(Object):
    """ Math class that mirrors javascript implementation.

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

    def _force_number(func):
        """[private decorator to make Math behave like javascript and turn strings, bools and None into numbers]]
        """
        def validation_decorator(*args, **kwargs):
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
                        if '.' in n:
                            params[i] = float(n)
                        else:
                            params[i] = int(n)
                    except Exception:
                        # raise ValueError("")
                        # js returns None instead
                        pass

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
        """ Returns the hyperbolic arccosine of a number. """
        return math.acosh(x)

    @staticmethod
    @_force_number
    def asin(x: float) -> float:
        """ Returns the arcsine (in radians) of a number. """
        return math.asin(x)

    @staticmethod
    @_force_number
    def asinh(x: float) -> float:
        """ Returns the hyperbolic arcsine of a number. """
        return math.asinh(x)

    @staticmethod
    @_force_number
    def atan(x: float) -> float:
        """ Returns the arctangent (in radians) of a number. """
        return math.atan(x)

    @staticmethod
    @_force_number
    def atan2(x: float, y: float) -> float:
        """ Returns the arctangent of the quotient of its arguments. """
        return math.atan2(x, y)

    @staticmethod
    @_force_number
    def atanh(x: float) -> float:
        """ Returns the hyperbolic arctangent of a number. """
        return math.atanh(x)

    @staticmethod
    @_force_number
    def cbrt(x: float) -> float:
        """ Returns the cube root of a number. """
        return math.cbrt(x)

    @staticmethod
    @_force_number
    def ceil(x: float) -> float:
        """ Returns the smallest integer greater than or equal to a number. """
        return math.ceil(x)

    @staticmethod
    @_force_number
    def cos(x: float) -> float:
        """ Returns the cosine of a number. (x is in radians) """
        return math.cos(x)

    @staticmethod
    @_force_number
    def cosh(x: float) -> float:
        """ Returns the hyperbolic cosine of a number. """
        return math.cosh(x)

    @staticmethod
    @_force_number
    def exp(x: float) -> float:
        """ Returns the value of E^x. """
        return math.exp(x)

    @staticmethod
    @_force_number
    def floor(x: float) -> float:
        """ Returns the largest integer less than or equal to a number. """
        return math.floor(x)

    @staticmethod
    @_force_number
    def log(x: float, base: float = None) -> float:
        """ Returns the natural logarithm (base E) of a number. """
        if base is None:
            return math.log(x)
        else:
            return math.log(x, base)

    @staticmethod
    @_force_number
    def max(x: float, y: float) -> float:
        """ Returns the largest of two numbers. """
        return max(x, y)

    @staticmethod
    @_force_number
    def min(x: float, y: float) -> float:
        """ Returns the smallest of two numbers. """
        return min(x, y)

    @staticmethod
    @_force_number
    def random() -> float:
        """ Returns a random number between 0 and 1. """
        return random.random()

    @staticmethod
    @_force_number
    def round(x: float) -> float:
        """ Returns the value of a number rounded to its nearest integer. """
        return round(x)

    @staticmethod
    @_force_number
    def pow(x: float, y: float) -> float:
        """ Returns the value of a number raised to a power. """
        return math.pow(x, y)

    @staticmethod
    @_force_number
    def sin(x: float) -> float:
        """ Returns the sine of a number. (x is in radians) """
        return math.sin(x)

    @staticmethod
    @_force_number
    def sinh(x: float) -> float:
        """ Returns the hyperbolic sine of a number. """
        return math.sinh(x)

    @staticmethod
    @_force_number
    def sqrt(x: float) -> float:
        """ Returns the square root of a number. """
        return math.sqrt(x)

    @staticmethod
    @_force_number
    def tan(x: float) -> float:
        """ Returns the tangent of a number. (x is in radians) """
        return math.tan(x)

    @staticmethod
    @_force_number
    def tanh(x: float) -> float:
        """ Returns the hyperbolic tangent of a number. """
        return math.tanh(x)

    @staticmethod
    @_force_number
    def trunc(x: float) -> float:
        """ Returns the integer part of a number. """
        return math.trunc(x)

    # TODO - test
    @staticmethod
    # @_force_number
    def hypot(*args):
        """ returns the square root of the sum of squares of its arguments """
        return math.hypot(*args)

    # TODO - test
    @staticmethod
    # @_force_number
    def log2(*args):
        """ returns the square root of the sum of squares of its arguments """
        return math.log2(*args)

    # TODO - test
    @staticmethod
    # @_force_number
    def loglp(*args):
        """ returns the natural logarithm (base e) of 1 + a number, that is """
        return math.loglp(*args)

    # TODO - test
    @staticmethod
    @_force_number
    def log10(x):
        """ function returns the base 10 logarithm of a number, that is """
        return math.log10(x)

    # TODO - test
    @staticmethod
    @_force_number
    def fround(x):
        """ returns the nearest 32-bit single precision float representation of a Number """
        # return math.log10(x)
        raise NotImplementedError

    # TODO - test
    @staticmethod
    @_force_number
    def clz32(x):
        """ returns the number of leading zero bits in the 32-bit binary representation of a number. """
        raise NotImplementedError


# import urllib


class Global(object):
    """ javascript global methods """

    NaN = "NaN"
    Infinity = float("inf")

    __timers = {}

    # TODO - https://stackoverflow.com/questions/747641/what-is-the-difference-between-decodeuricomponent-and-decodeuri

    @staticmethod
    def decodeURI(x):
        """ Decodes a URI """
        return unquote(x)

    @staticmethod
    def decodeURIComponent(x):
        """ Decodes a URI component """
        return unquote(x, encoding="utf-8")

    @staticmethod
    def encodeURI(x):
        """ Encodes a URI """
        return quote(str(x), safe='~@#$&()*!+=:;,.?/\'')

    @staticmethod
    def encodeURIComponent(x):
        """ Encodes a URI component """
        return quote(str(x), safe='~()*!.\'')

    # @staticmethod
    # def escape():
        """ Deprecated in version 1.5. Use encodeURI() or encodeURIComponent() """
        # pass

    @staticmethod
    def eval(pythonstring):
        """ Evaluates a string and executes it as if it was script code """
        eval(pythonstring)

    @staticmethod
    def isFinite(x) -> bool:  # TODO - test
        """ Returns true if x is a finite number """
        return math.isfinite(x)

    @staticmethod
    def isNaN(x):
        """ Determines whether a value is an illegal number """
        try:
            return math.isnan(x)
        except TypeError:
            return True

    def NaN(self):
        """ "Not-a-Number" value """
        # return self.NaN
        return "NaN"

    @staticmethod
    def Number(x):
        """ Converts an object's value to a number """
        try:
            if type(x) == float or type(x) == int:  # or type(x) == long:
                return x

            if type(x) == str:
                if '.' in x:
                    return float(x)
                else:
                    return int(x)
        except Exception:
            return "NaN"
        return "NaN"

    @staticmethod
    def Boolean(x):  # TODO - test
        if isinstance(x, int):
            return bool(x)
        elif isinstance(x, str):
            if x.lower() == 'true':
                return True
            elif x.lower() == 'false':
                return False
            elif x == '':
                return False
            else:
                return True
        elif isinstance(x, bool):
            return x
        elif isinstance(x, (list, tuple, dict, object)):
            return True
        elif x is None:
            return False
        else:
            return True

    @staticmethod
    def parseFloat(x: str):
        """ Parses a string and returns a floating point number """
        # return float(x)
        import ast
        return float(ast.literal_eval(x))

    @staticmethod
    def parseInt(x: str):
        """ Parses a string and returns an integer """
        # return int(x)
        import ast
        return int(ast.literal_eval(x))

    @staticmethod
    def String(x):
        """ Converts an object's value to a string """
        return str(x)

    def undefined(self):
        """ Indicates that a variable has not been assigned a value """
        return None

    # @staticmethod
    # def unescape():
        """ Deprecated in version 1.5. Use decodeURI() or decodeURIComponent() instead """
        # pass

    @staticmethod
    def require(path: str):
        """ Loads a script from a file """
        # '.'.join(path.split('/'))
        # module = __import__(path)  # app.components.{component}
        # my_class = getattr(module, component.title())
        # return my_class()
        raise NotImplementedError

    @staticmethod
    def setTimeout(callback, t, *args, **kwargs):
        """[sets a timer which executes a function or evaluates an expression after a specified delay]

        Args:
            callback (function): [method to be executed after the delay]
            t ([int]): [milliseconds]

        Returns:
            [str]: [an identifier for the timer]
        """
        if isinstance(callback, str):
            callback = eval(callback)

        timer = threading.Timer(t / 1000, callback, args=args, kwargs=kwargs)
        timer_id = id(timer)
        Global.__timers[timer_id] = timer
        timer.start()
        return timer_id

    @staticmethod
    def clearTimeout(timeoutID):
        """ [cancels a timer set with setTimeout()]

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


class Performance():

    _start = time.time()

    def __init__(self):
        pass

    def now(self):
        end = time.time()
        return end - Performance._start

    # def reset(self):
    #     Performance._start = time.time()


performance = Performance()


class Date(Object):
    """ javascript date """

    def __init__(self, date=None, formatter='python'):

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

    def __str__(self):
        return self.toString()

    def toString(self):
        """ Returns a string representation of the date """
        if self.formatter == 'python':
            return self.date.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return self.date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')  # js

    def parse_date(self, date_string):
        self.date = parse(date_string)
        return self.date

    def getDate(self):
        """ Returns the day of the month (from 1-31) """
        return self.date.day
        # TODO - do for a date object passed in. this only does today

    def getDay(self):
        """  Returns the day of the week (from 0-6) """
        day = self.date.isoweekday()
        return day if (day < 7) else 0
        # TODO - do for a date object passed in. this only does today

    def getFullYear(self):
        """ Returns the year """
        return self.date.now().year

    def getHours(self):
        """  Returns the hour (from 0-23) """
        return self.date.now().hour

    def getMilliseconds(self):
        """ Returns the milliseconds (from 0-999) """
        return round(self.date.now().microsecond / 1000)

    def getMinutes(self):
        """  Returns the minutes (from 0-59) """
        return self.date.now().minute

    def getMonth(self):
        """ Returns the month (from 0-11) """
        return self.date.now().month - 1

    def getSeconds(self):
        """  Returns the seconds (from 0-59) """
        return self.date.now().second

    def getTime(self):
        """ Returns the number of milliseconds since midnight Jan 1 1970, and a specified date """
        return int(str(time.time()).split('.')[0])
        # TODO - whats difference between this and 'now()' ?

    def getTimezoneOffset(self):
        """ Returns the time difference between UTC time and local time, in minutes """
        return self.date.now().utcoffset().total_seconds() / 60  # TODO - TEST

    def getUTCDate(self):
        """ Returns the day of the month, according to universal time (from 1-31) """
        return self.date.utcnow().month

    def getUTCDay(self):
        """ Returns the day of the week, according to universal time (from 0-6) """
        return self.date.utcnow().day

    def getUTCFullYear(self):
        """ Returns the year, according to universal time """
        return self.date.utcnow().year

    def getUTCHours(self):
        """ Returns the hour, according to universal time (from 0-23) """
        return self.date.utcnow().hour

    def getUTCMilliseconds(self):
        """ Returns the milliseconds, according to universal time (from 0-999) """
        return round(self.date.utcnow().microsecond / 1000)

    def getUTCMinutes(self):
        """ Returns the minutes, according to universal time (from 0-59) """
        return self.date.utcnow().minute

    def getUTCMonth(self):
        """ Returns the month, according to universal time (from 0-11) """
        return self.date.utcnow().month - 1

    def getUTCSeconds(self):
        """ Returns the seconds, according to universal time (from 0-59) """
        return self.date.utcnow().second

    def getYear(self):
        """ Deprecated. Use the getFullYear() method instead """
        return self.date.now().year

    @staticmethod
    def now():
        """ Returns the number of milliseconds since midnight Jan 1, 1970 """
        return round(time.time() * 1000)

    # @staticmethod
    def parse(self, date_string):
        """ Parses a date string and returns the number of milliseconds since January 1, 1970 """
        self.date = self.parse_date(str(date_string))  #  TODO - huh?
        # return self.date.getTime()

    def setDate(self, day):
        """ Sets the day of the month of a date object """
        self.date.replace(day=int(day))
        # return self.date.getTime()

    def setFullYear(self, year):
        """ Sets the year of a date object """
        self.date.replace(year=int(year))
        # return self.date.getTime()

    def setHours(self, hours):
        """ Sets the hour of a date object """
        self.date.replace(hour=int(hours))
        # return self.date.getTime()

    def setMilliseconds(self, milliseconds):
        """ Sets the milliseconds of a date object """
        # self.date.replace(millisecond=int(milliseconds))
        # return self.now()
        print('TODO: setMilliseconds')
        pass

    # TODO - , seconds = None, milliseconds = None):
    def setMinutes(self, minutes):
        """  Set the minutes of a date object """
        self.date.replace(minute=int(minutes))
        # return self.now()

    def setMonth(self, month):
        """ Sets the month of a date object """
        self.date.replace(month=int(month))
        # return self.now()

    def setSeconds(self, seconds):
        """ Sets the seconds of a date object """
        self.date.replace(second=int(seconds))
        # return self.now()

    # Sets a date to a specified number of milliseconds after/before January 1, 1970
    def setTime(self, milliseconds=None):
        """ Sets the number of milliseconds since January 1, 1970 """
        # test copilot
        # self.date.replace(millisecond=int(milliseconds))
        # return self.now() # TODO - is this right? - is this same as now()?
        # print('TODO: setTime')
        # raise NotImplementedErro
        pass

    def setUTCDate(self, day):
        """  Sets the day of the month of a date object, according to universal time """
        self.setDate(day)
        # return self.getTime()

    def setUTCFullYear(self, year):
        """  Sets the year of a date object, according to universal time """
        self.setFullYear(year)
        # return self.getTime()

    def setUTCHours(self, hour):
        """ Sets the hour of a date object, according to universal time """
        self.setHours(hour)
        # return self.getTime()

    def setUTCMilliseconds(self, milliseconds):
        """  Sets the milliseconds of a date object, according to universal time """
        self.setMilliseconds(milliseconds)
        # return self.getTime()

    def setUTCMinutes(self, minutes):
        """   Set the minutes of a date object, according to universal time """
        self.setMinutes(minutes)
        # return self.getTime()

    def setUTCMonth(self, month):
        """ Sets the month of a date object, according to universal time """
        self.setMonth(month)
        # return self.getTime()

    def setUTCSeconds(self, seconds):
        """   Set the seconds of a date object, according to universal time """
        self.setSeconds(seconds)
        # return self.getTime()

    def setYear(self, year):
        """ Deprecated. Use the setFullYear() method instead """
        self.date.replace(year=int(year))
        # return self.getTime()
        # TODO - there may not be a date object already?

    def toDateString(self):
        """ Converts the date portion of a Date object into a readable string """
        return self.date.strftime('%Y-%m-%d')

    def toUTCString(self):
        """ Converts a Date object to a string, according to universal time """
        return self.date.strftime('%Y-%m-%d %H:%M:%S')

    def toGMTString(self):
        """ Deprecated. Use the toUTCString() method instead """
        return self.toUTCString()

    def toJSON(self):
        """  Returns the date as a string, formatted as a JSON date """
        import json
        return json.dumps(self.date.strftime('%Y-%m-%d'))

    def toISOString(self):
        """ Returns the date as a string, using the ISO standard """
        return self.date.strftime('%Y-%m-%d')

    def toLocaleDateString(self):
        """ Returns the date portion of a Date object as a string, using locale conventions """
        return self.date.strftime('%x')

    def toLocaleString(self):
        """ Converts a Date object to a string, using locale conventions """
        return self.date.strftime('%x')

    def toLocaleTimeString(self):
        """ Returns the time portion of a Date object as a string, using locale conventions """
        return self.date.strftime('%X')

    def toTimeString(self):
        """ Converts the time portion of a Date object to a string """
        return self.date.strftime('%X')

    def UTC(self):
        """ Returns the number of milliseconds in a date since midnight of January 1, 1970, according to UTC time """
        return self.date.utcnow()


class Screen(object):
    """ screen """

    # wrap a lib?
    # https://github.com/rr-/screeninfo?

    def __init__(self):
        # from sys import platform
        # if platform == "linux" or platform == "linux2":
        #     # linux
        # import subprocess
        # resuls = subprocess.Popen(['xrandr'],stdout=subprocess.PIPE).communicate()[0].split("current")[1].split(",")[0]
        # width = resuls.split("x")[0].strip()
        # heigth = resuls.split("x")[1].strip()
        # print width + "x" + heigth
        # elif platform == "darwin":
        #     # OS X
        # results = str(subprocess.Popen(['system_profiler SPDisplaysDataType'],stdout=subprocess.PIPE, shell=True).communicate()[0])
        # res = re.search('Resolution: \d* x \d*', results).group(0).split(' ')
        # width, height = res[1], res[3]
        # return width, height
        # elif platform == "win32":
        # from win32api import GetSystemMetrics
        # print("Width =", GetSystemMetrics(0))
        # print("Height =", GetSystemMetrics(1))
        pass

    def availHeight(self):
        ''' Returns the height of the screen (excluding the Windows Taskbar) '''
        # return self.height
        raise NotImplementedError

    def availWidth(self):
        ''' Returns the width of the screen (excluding the Windows Taskbar) '''
        raise NotImplementedError

    def colorDepth(self):
        ''' Returns the colorDepth '''
        raise NotImplementedError

    def height(self):
        ''' Returns the total height of the screen '''
        raise NotImplementedError

    def pixelDepth(self):
        ''' Returns the pixelDepth '''
        raise NotImplementedError

    def width(self):
        ''' Returns the total width of the screen  '''
        raise NotImplementedError


class ProgramKilled(Exception):
    pass


class Job(threading.Thread):

    def __init__(self, interval, execute, *args, **kwargs):
        threading.Thread.__init__(self)
        self.daemon = False
        self.stopped = threading.Event()
        self.interval = interval
        self.execute = execute
        self.args = args
        self.kwargs = kwargs

    def stop(self):
        self.stopped.set()
        self.join()

    def run(self):
        while not self.stopped.wait(self.interval.total_seconds()):
            self.execute(*self.args, **self.kwargs)

    # def __str__(self):
    #     return "Job every %s" % self.interval


class SetInterval(object):

    def signal_handler(self, signum, frame):
        raise ProgramKilled

    def __init__(self, function, time, *args, **kwargs):
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)
        self.job = Job(datetime.timedelta(microseconds=time * 1000), function, *args, **kwargs)
        self.job.start()

    # def stop(self):
    #     self.job.stop()


class Promise(object):
    # undocumented - warning. use at own risk
    def __init__(self, func=None, *args, **kwargs):
        # print('init')
        self.data = None
        self.state = 'pending'  # fullfilled, rejected
        if func is not None:
            func(self.resolve, self.reject)

    def then(self, func):
        if func is not None:
            # print('--->',self.data)
            self.data = func(self.data)
            # print('-->',self.data)
        return self

    def catch(self, error):
        # func(error)
        print(error)
        return self

    def resolve(self, data):
        # print( 'resolve called::', data )
        self.data = data
        self.state = "fulfilled"
        return self

    def reject(self, data):
        self.data = data
        self.state = "rejected"
        return self
    # def __str__(self):
    #     try:
    #         return self.data.text
    #     except Exception as e:
    #         print(e)
    #     return str(self)


class FetchedSet(object):  # not a promise
    def __init__(self, *args, **kwargs):
        self.results = []

    def __getitem__(self, index):
        return self.results[index]

    def oncomplete(self, func):  # runs once all results are back
        func(self.results)
        return

    # def __call__(self, func):
    #     self.results.append(func)


class Window(object):
    """ window """

    localStorage = Storage()
    location = 'eventual.technology'

    def __init__(self, *args, **kwargs):
        # self.console = dom.console
        # self.document = Document
        # globals()?
        # dir()?
        # locals()?
        pass

    # TODO - tell users to use other window class if methods are called.

    @staticmethod
    def alert(msg):
        """ Displays an alert box with a message and an OK button """
        print(msg)
        return

    @staticmethod
    def prompt(msg, default_text=""):
        """ Displays a dialog box that prompts the visitor for input """
        print(msg)
        data = input()
        return data

    setTimeout = Global.setTimeout
    clearTimeout = Global.clearTimeout

    @staticmethod
    def clearInterval(job):
        job.stop()

    @staticmethod
    def setInterval(function, time, *args, **kwargs):
        interval_ID = SetInterval(function, time, *args, **kwargs)
        return interval_ID.job

    @staticmethod
    def _do_request(url, f=None, **kwargs):
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
            print(f'Request Failed for URL: {url}', e)
            return None

    @staticmethod
    def fetch(url: str, **kwargs):
        # undocumented - warning. use at own risk
        # note - kinda pointless atm. just use requests directly and you wont have to muck about with a Promise
        if type(url) is not str:
            raise ValueError('fetch takes a single url string. use fetch_set, fetch_threaded or fetch_pooled')
        f = Promise()
        r = window._do_request(url, f, *kwargs)
        return f.resolve(r)

    @staticmethod
    def fetch_set(urls: list, callback_function=None, error_handler=None, **kwargs):
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
    def fetch_threaded(urls: list, callback_function=None, error_handler=None, **kwargs):
        # undocumented - warning. use at own risk
        # note - still blocks. just gets all before continuing using threads
        # problems - all urls can only have 1 associated callback, error and set of kwargs
        if type(urls) is str:
            urls = [urls]  # leniency
        f = FetchedSet()
        jobs = []
        for url in urls:
            thread = threading.Thread(target=window._do_request(url, f, **kwargs))
            thread.setDaemon(True)
            jobs.append(thread)
        map(lambda j: j.start(), jobs)
        map(lambda j: j.join(), jobs)
        # f = FetchedSet()
        return f

    @staticmethod
    def fetch_pooled(urls: list, callback_function=None, error_handler=None, **kwargs):
        # undocumented - warning. use at own risk
        # note - still blocks. just gets all before continuing using a pool
        # problems - all urls can only have 1 associated callback, error and set of kwargs
        if type(urls) is str:
            urls = [urls]  # leniency
        f = FetchedSet()

        def _do_request_wrapper(obj):
            url = obj['url']
            f = obj['f']
            kwargs = obj['k']
            kwargs['callback_function'] = obj['c']
            kwargs['error_handler'] = obj['e']
            window._do_request(url, f, **kwargs)

        jobs = []
        p = Pool()
        urls = [{'url': url, 'f': f, 'c': callback_function, 'e': error_handler, 'k': kwargs} for url in urls]
        results = p.map(_do_request_wrapper, urls)
        p.close()
        p.join()
        return f

    # def fetch_aysnc( urls: list, options={}, type="async" ):
        # TODO - a version using async/await

    @staticmethod
    def btoa(dataString):
        """ Encodes a string in base-64 """
        import base64
        dataBytes = dataString.encode("utf-8")
        encoded = base64.b64encode(dataBytes)
        return encoded

    @staticmethod
    def atob(dataString):
        """ Decodes a base-64 encoded string """
        import base64
        return base64.b64decode(dataString).decode()

    @staticmethod
    def requestAnimationFrame(callback):
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


class Array(object):
    """ javascript array """

    @staticmethod
    def from_(obj):  # TODO - test
        """ Creates a new Array instance from an array-like or iterable object. """
        # return Array(object)
        if isinstance(obj, Array):
            return obj
        elif isinstance(obj, list):
            return Array(*obj)
        elif isinstance(obj, tuple):
            items = list(obj)
            return Array(*items)
        elif isinstance(obj, dict):
            items = list(obj.items())
            return Array(*items)
        # if it is iterable unpack it
        elif hasattr(obj, '__iter__'):
            items = list(obj)
            return Array(*items)
        else:
            return Array([obj])

    @staticmethod
    def of(*args):  # TODO - test
        """ Creates a new Array instance with a variable number of arguments,
        regardless of number or type of the arguments. """
        return Array(args)

    def __init__(self, *args):
        """[An Array that behaves like a js array]
        """
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

    def __getitem__(self, index):
        return self.args[index]

    def __getattribute__(self, name):
        try:
            return super().__getattribute__(name)
        except AttributeError:
            # if its a list method get it from args
            if name in dir(list):
                return getattr(self.args, name)

    def __setitem__(self, index, value):
        self.args[index] = value

    def __add__(self, value):
        if isinstance(value, int):
            raise ValueError('int not supported')
        if isinstance(value, Array):
            self.args = self.args + value.args
        if isinstance(value, list):
            self.args = self.args + value
        return self.args

    def __len__(self):
        return len(self.args)

    def __eq__(self, other):
        if isinstance(other, Array):
            return self.args == other.args
        if isinstance(other, list):
            return self.args == other
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return str(self.args)

    def __iter__(self):
        for i in self.args:
            yield i
        # self.args.__iter__()

    def __sub__(self, value):
        if isinstance(value, int):
            raise ValueError('int not supported')
        if isinstance(value, Array):
            self.args = self.args - value.args
        if isinstance(value, list):
            self.args = self.args - value
        return self.args

    def toString(self):
        ''' Converts an array to a string, and returns the result '''
        return str(self.args)  # TODO - check what js does

    def toSource(self):
        """
        Returns the source array.
        """
        return list(self.args)

    @property
    def length(self):
        """ Sets or returns the number of elements in an array """
        return len(self.args)

    def concat(self, *args):
        """[Joins two or more arrays, and returns a copy of the joined arrays]

        Returns:
            [list]: [returns a copy of the joined arrays]
        """
        for a in args:
            self.args += a
        return self.args

    def flat(self, depth=1):  # TODO - test
        """[Flattens an array into a single-dimensional array or a depth of arrays]
        """
        if depth < 1:
            raise ValueError('depth must be greater than 0')
        if depth == 1:
            return self.args
        flat = []
        for i in self.args:
            flat += i.flat(depth - 1)
        return flat

    def flatMap(self, fn):  # TODO - test
        """[Maps a function over an array and flattens the result]
        """
        return Array(fn(i) for i in self.args)

    def fill(self, value=None, start=None, end=None):
        """[Fills elements of an array from a start index to an end index with a static value]
        """
        if start is None:
            start = 0
        if end is None:
            end = len(self.args)
        for i in range(start, end):
            self.args[i] = value
        return self.args

    def groupBy(self, callback) -> dict:  # TODO - test
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

    def findLast(self, callback):
        """[Returns the last element in an array that passes a test]
        """
        for i in range(len(self.args) - 1, -1, -1):
            if callback(self.args[i], i, self.args):
                return self.args[i]
        return None

    def findLastIndex(self, callback):
        """[Returns the last index of an element in an array that passes a test]
        """
        for i in range(len(self.args) - 1, -1, -1):
            if callback(self.args[i], i, self.args):
                return i
        return -1

    def includes(self, value):  # -> bool:
        """[Check if an array contains the specified item

        Args:
            value ([any]): [any value]

        Returns:
            [bool]: [a boolean]
        """
        if value in self.args:
            return True
        else:
            return False

    def indexOf(self, value):
        """ Search the array for an element and returns its position """
        # for count, each in enumerate(self.args):
        #     if each == value:
        #         return count
        try:
            return self.args.index(value)
        except ValueError:
            return -1
        except Exception as e:
            # print(e)
            return -1

    @staticmethod
    def isArray(thing):
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

    def join(self, value):
        """ Joins all elements of an array into a string  """
        # TODO - get passed param names
        return value.join([str(x) for x in self.args])

    def lastIndexOf(self, value):
        """ Search the array for an element, starting at the end, and returns its position """
        try:
            return len(self.args) - self.args[::-1].index(value) - 1
        except Exception as e:
            # print(e)
            return None

    def pop(self):
        """ Removes the last element of an array, and returns that element """
        # item = self.args[len(self.args)-1]
        # del self.args[len(self.args)-1]
        return self.args.pop()

    def push(self, value):
        """ Adds new elements to the end of an array, and returns the new length """
        self.args.append(value)
        return len(self.args)

    def reverse(self):
        """ Reverses the order of the elements in an array """
        self.args = self.args[::-1]
        return self.args

    def slice(self, start=0, stop=None, step=1):
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

    def splice(self, start, delete_count=None, *items):
        """ Selects a part of an array, and returns the new array """
        if delete_count is None:
            delete_count = len(self.args) - start

        total = start + delete_count
        removed = self.args[start:total]
        self.args[start:total] = items
        return removed
        # return self.args

    def unshift(self, *args):
        """[Adds new elements to the beginning of an array, and returns the new length]

        Returns:
            [int]: [the length of the array]
        """
        for i in reversed(args):
            self.args.insert(0, i)
        return len(self.args)

    def shift(self):
        """[removes the first element from an array and returns that removed element]

        Returns:
            [type]: [the removed array element]
        """
        item = self.args[0]
        del self.args[0]
        return item

    def map(self, func):
        """[Creates a new array with the result of calling a function for each array element]

        Args:
            func ([type]): [a function to call on each array element]

        Returns:
            [list]: [a new array]
        """
        # print(func)
        return [func(value) for value in self.args]
        # return map(self.args, func)

    def some(self, func):
        """ Checks if any of the elements in an array pass a test """
        return any(func(value) for value in self.args)

    def sort(self, func=None):  # , *args, **kwargs):
        """ Sorts the elements of an array """

        if func is not None:
            return self.args.sort(key=func(*self.args))

        def comp(o):
            return str(o)

        # manually sort lexicographically
        for i in range(len(self.args)):
            for j in range(i + 1, len(self.args)):
                if comp(self.args[i]) > comp(self.args[j]):
                    self.args[i], self.args[j] = self.args[j], self.args[i]
        return self.args

    def reduce(self, callback, initialValue=None):
        """ Reduces the array to a single value (going left-to-right)
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
                raise Exception("Callback does not have the correct number of parameters")
        return initialValue

    def reduceRight(self, callback, initialValue=None):
        """ Reduces the array to a single value (going right-to-left)
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
                raise Exception("Callback does not have the correct number of parameters")
        return initialValue

    def filter(self, func):
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

    def find(self, func):
        """ Returns the value of the first element in an array that pass a test """
        for each in self.args:
            if func(each):
                return each

    def findIndex(self, value):
        """ Returns the index of the first element in an array that pass a test """
        # written by .ai (https://6b.eleuther.ai/)
        for i, value in enumerate(self.args):
            if value == value:
                return i
        return -1

    def forEach(self, func):
        """ Calls a function for each array element """
        # written by .ai (https://6b.eleuther.ai/)
        for value in self.args:
            func(value)
        # TODO - is this supposed to pass count like Node list? i.e.
        # for i in range(len(self.args)):
            # func(self.args[i], i, self.args)

    def keys(self):
        """ Returns a Array Iteration Object, containing the keys of the original array """
        for i in self.args:
            yield i

    def copyWithin(self, target, start=0, end=None):
        """ Copies array elements within the array, from start to end """
        if end is None:
            end = len(target)
        for i in range(start, end):
            self.args[i] = target[i]

    def entries(self):
        """[Returns a key/value pair Array Iteration Object]

        Yields:
            [type]: [key/value pair]
        """
        for i in self.args:
            yield [i, self.args[i]]

    def every(self, func):
        """[Checks if every element in an array pass a test]

        Args:
            func ([type]): [test function]

        Returns:
            [bool]: [if every array elemnt passed the test]
        """
        return all(func(value) for value in self.args)

    def at(self, index: int):
        """[takes an integer value and returns the item at that index,
        allowing for positive and negative integers.
        Negative integers count back from the last item in the array.]

        Args:
            index ([type]): [position of item]

        Returns:
            [type]: [item at the given position]
        """
        return self.args[index]


Array.prototype = Array


class Set():

    def __init__(self, *args):
        """[The Set object lets you store unique values of any type, whether primitive values or object references.

        TODO - will need to store dictionaries unlike a python set
        https://stackoverflow.com/questions/34097959/add-a-dictionary-to-a-set-with-union

        ]
        """
        self.args = set(args)

    def __iter__(self):
        return iter(self.args)

    def __len__(self):
        return len(self.args)

    def __contains__(self, item):
        return item in self.args

    def __repr__(self):
        return repr(self.args)

    def __str__(self):
        return str(self.args)

    @property
    def species(self):
        """ The constructor function that is used to create derived objects. """
        # return self.args
        raise NotImplementedError

    @property
    def size(self):
        """ Returns the number of values in the Set object. """
        return len(self.args)

    def add(self, value):
        """ Appends value to the Set object. Returns the Set object with added value. """
        # print(type(self.args), value)
        self.args.add(value)
        return self.args

    def clear(self):
        """ Removes all elements from the Set object. """
        self.args.clear()

    def delete(self, value):
        """ Removes the element associated to the value
        returns a boolean asserting whether an element was successfully removed or not. """
        return self.args.remove(value)

    def has(self, value):
        """ Returns a boolean asserting whether an element is present with the given value in the Set object or not. """
        return value in self.args

    def contains(self, value):
        """ Returns a boolean asserting whether an element is present with the given value in the Set object or not. """
        return value in self.args

    # Set.prototype[@@iterator]()
    # Returns a new iterator object that yields the values for each element in the Set object in insertion order.

    def values(self):
        """ Returns a new iterator object that yields the values for each element
        in the Set object in insertion order. """
        return iter(self.args)

    # def keys(self):
    #     """ An alias for values """ #?
    #     return self.values()

    def entries(self):
        """ Returns a new iterator object that contains an array of [value, value] for each element in the Set object,
        in insertion order. """
        return iter([[i, self.args[i]] for i in self.args])
        # This is similar to the Map object, so that each entry's key is the same as its value for a Set.

    def forEach(self, callbackFn, thisArg=None):
        """ Calls callbackFn once for each value present in the Set object, in insertion order.
        If a thisArg parameter is provided, it will be used as the this value for each invocation of callbackFn.
        """
        for i in self.args:
            callbackFn(i, thisArg)


class Number(float):
    """ javascript Number methods """

    # print(sys.float_info)
    MAX_VALUE = list(sys.float_info)[0]
    MIN_VALUE = 5E-324  # CHANGE no longer >  list(sys.float_info)[3]

    NEGATIVE_INFINITY = float("inf")  #: Represents negative infinity (returned on overflow) Number
    POSITIVE_INFINITY = float("-inf")  #: Represents infinity (returned on overflow)  Number

    # prototype Allows you to add properties and methods to an object   Number

    def __init__(self, x="", *args, **kwargs):
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
        return self.x ** other

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
        return self.x ** other

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

    def isInteger(self):
        """ Checks whether a value is an integer """
        return (type(self.x) == int)

    def isSafeInteger(self):
        """ Checks whether a value is a safe integer """
        raise NotImplementedError

    def toExponential(self, num=None):
        """ Converts a number into an exponential notation """
        if num is not None:
            exp = '{:e}'.format(Number(Number(self.x).toFixed(num)))
        else:
            exp = '{:e}'.format(self.x)

        if 'e' in str(self.x):
            exp = str(self.x)  # python already converts.

        n = exp.split('e')[0].rstrip("0")
        e = exp.split('e')[1].replace('00', '0')

        if n == "0.":
            n = "0"

        if int(e) != 0:
            if int(e) < 10 and int(e) > -10:  # TODO - not correct. lazy way to strip left 0s only
                e = e.replace('0', '')

        # print(  "AND:", n, "e" , e )
        if n.endswith('.'):
            n = n.strip('.')

        return n + "e" + e

    def toFixed(self, digits: int):
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

    def toPrecision(self, precision):
        """[returns a string representing the Number object to the specified precision.]

        Args:
            precision ([int]): [An integer specifying the number of significant digits.]

        Returns:
            [str]: [A string representing a Number object in fixed-point
            or exponential notation rounded to precision significant digits]
        """
        precision = int(precision)
        # return str(math.pow(self.x, precision))
        # raise NotImplementedError
        return str(round(self.x, precision))

    def toString(self, base: int):
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
            digits.append('-')

        digits.reverse()

        return ''.join(digits)


class String(object):
    """ javascript String methods """

    @staticmethod
    def fromCodePoint(codePoint: int):
        """ Converts a Unicode code point into a string """
        return chr(codePoint)

    @staticmethod
    def toCodePoint(char: str):
        """ Converts a Unicode string into a code point """
        return ord(char)

    @staticmethod
    def raw(string):
        """ Returns the string as-is """
        import re
        return re.escape(string)

    # @staticmethod
    # def fromCharCode(code: int):
    #     """ Converts a Unicode code point into a string """
    #     return chr(code)

    @staticmethod
    def toCharCode(char: str):
        """ Converts a Unicode string into a code point """
        return ord(char)

    def __init__(self, x="", *args, **kwargs):
        # self.args = args
        # self.kwargs = kwargs
        self.x = str(x)

    def __str__(self):
        return self.x

    def __eq__(self, other):
        if isinstance(other, str):
            return self.x == other
        if isinstance(other, String):
            return self.x == other.x
        return False

    # def __repr__(self):
    #     return self.x

    def __getitem__(self, item):
        # print(item)
        return self.x[item]

    def __add__(self, other):
        return self.x + other

    def __radd__(self, other):
        return self.x + other

    def __iadd__(self, other):
        return self.x + other

    def __sub__(self, other):
        return self.x - other

    def __rsub__(self, other):
        return other - self.x

    def __isub__(self, other):
        return self.x - other

    def __mul__(self, other):
        return self.x * int(other)

    def __rmul__(self, other):
        return self.x * int(other)

    def __imul__(self, other):
        return self.x * int(other)

    def split(self, expr) -> list:
        """[can split a string based on a regex]

        Args:
            expr ([str]): [valid regex or string to split on]

        Returns:
            [list]: [list of str]
        """

        # if isinstance( expr, RegExp)

        import re
        # print( '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.', type(expr) )
        is_regex = False
        try:
            re.compile(expr)
            is_regex = True
        except re.error:
            is_regex = False

        if is_regex:
            return re.split(expr, self.x)
        else:
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
        """ Returns the Unicode of the character at the specified index """
        return ord(self.x[index])

    # @staticmethod
    def fromCharCode(self, *codes) -> str:
        """ returns a string created from the specified sequence of UTF-16 code units """
        return "".join([str(chr(x)) for x in codes])

    @property
    def length(self) -> int:
        return len(self.x)

    def repeat(self, count: int) -> str:
        """ Returns a new string with a specified number of copies of an existing string """
        return self.x * count

    def startsWith(self, x: str, start: int = None, end: int = None) -> bool:
        """ Checks whether a string begins with specified characters """
        if start is None:
            start = 0
        if end is None:
            end = len(x)
        # print(self.x.startswith(x, start, end))
        return self.x.startswith(x, start, end)

    def substring(self, start: int, end: int = None) -> str:
        """ Extracts the characters from a string, between two specified indices """
        if start < 0:
            start = 0
        if end is None:
            end = len(self.x)
        return self.x[start:end]

    def endsWith(self, x: str, start: int = None, end: int = None) -> bool:
        """ Checks whether a string ends with specified string/characters """
        if start is None:
            start = 0
        if end is None:
            end = len(x)
        return self.x.endswith(x, start, end)

    def toLowerCase(self) -> str:
        """ Converts a string to lowercase letters """
        return self.x.lower()

    def toUpperCase(self) -> str:
        """ Converts a string to uppercase letters """
        return self.x.upper()

    def slice(self, start: int = 0, end: int = None) -> str:
        """ Selects a part of an string, and returns the new string """
        if end is None:
            end = len(self.x)
        return self.x[start:end]

    def trim(self):
        """ Removes whitespace from both ends of a string """
        return self.x.strip()

    def charAt(self, index: int) -> str:
        """[Returns the character at the specified index (position)]

        Args:
            index (int): [index position]

        Returns:
            [str]: [the character at the specified index.
            if the index is out of range, an empty string is returned.]
        """
        try:
            return self.x[index]
        except IndexError:
            return ""

    def replace(self, old: str, new) -> str:
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

    def replaceAll(self, old: str, new: str):
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

    def substr(self, start: int = 0, end: int = None):
        """ Extracts the characters from a string, beginning at a specified start position,
        and through the specified number of character """
        if end is None:
            end = len(self.x)
        return self.x[start:start + end]

    def toLocaleLowerCase(self) -> str:
        """ Converts a string to lowercase letters, according to the host's locale """
        # locale.setlocale()
        return self.x.lower()

    def toLocaleUpperCase(self) -> str:
        """ Converts a string to uppercase letters, according to the host's locale """
        # locale.setlocale()
        return self.x.upper()

    def indexOf(self, searchValue: str, fromIndex: int = 0):
        """[returns the index within the calling String object of the first occurrence of the specified value,
        starting the search at fromIndex ]

        Args:
            searchValue (str): [The string value to search for.]
            fromIndex (int): [An integer representing the index at which to start the search]

        Returns:
            [type]: [The index of the first occurrence of searchValue, or -1 if not found.]

        """
        try:
            return self.x.index(searchValue, fromIndex)
        except ValueError:
            return -1

    def codePointAt(self, index: int):
        """[Returns the Unicode code point at the specified index (position)]

        Args:
            index (int): [index position]

        Returns:
            [type]: [the Unicode code point at the specified index (position)]
        """
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
        return str(self.x + padChar * (length - len(self.x)))

    def padStart(self, length: int, padChar: str = " ") -> str:
        """[Pads the start of a string with a specified character]

        Args:
            length (int): [the length of the resulting string]
            padChar (str, optional): [the character to use for padding. Defaults to " "].

        Returns:
            [str]: [the padded string]
        """
        return padChar * (length - len(self.x)) + self.x

    def localeCompare(self, comparisonString: str, locale: str = None, *args) -> int:
        """ method returns a number indicating whether a reference string comes before,
            or after, or is the same as the given string in sort order """
        # if locale is None:
        #     locale = self.locale
        # return locale.strcoll(self.x, comparisonString, *args)
        # pass
        # TODO - implement localeCompare
        raise NotImplementedError

    def trimStart(self, length: int):  # TODO - huh?. length
        """[Removes whitespace from the beginning of a string.]

        Args:
            length (int): [the length of the resulting string]

        Returns:
            [str]: [the trimmed string]
        """
        return self.x.lstrip()

    def trimEnd(self, length: int):  # TODO - huh?. length
        """[Removes whitespace from the end of a string]

        Args:
            length (int): [the length of the resulting string]

        Returns:
            [type]: [the trimmed string]
        """
        return self.x.rstrip()

    def includes(self, searchValue: str, position: int = 0) -> bool:
        """[returns true if the specified string is found within the calling String object,]

        Args:
            searchValue (str): [The string value to search for.]
            position (int, optional): [the position to search from]. Defaults to 0.

        Returns:
            [type]: [a boolean value indicating whether the search value was found.]
        """
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
        return searchValue in self.x[position:]

    def matchAll(self, pattern: str):
        """
        Searches a string for a specified value, or a regular expression,
        and returns a new string where the specified values are replaced.
        only replaces first one.
        """
        return re.sub(pattern, "", self.x)

    def match(self, pattern: str):
        """
        Searches a string for a specified value, or a regular expression,
        and returns a new string where the specified values are replaced.
        only replaces first one.
        """
        return re.match(pattern, self.x)

    def compile(self, pattern: str):
        """
        Searches a string for a specified value, or a regular expression,
        and returns a new string where the specified values are replaced.
        only replaces first one.
        """
        return re.compile(pattern)

    def lastIndexOf(self, searchValue: str, fromIndex: int = 0):
        """
        returns the last index within the calling String object of the first occurrence of the specified value,
        starting the search at fromIndex
        """
        return self.x.rindex(searchValue, fromIndex)

    # def test(self, pattern: str):? was this on string?

    # TODO - test all these
    def anchor(self, name: str):
        # from domonic.html import a
        # return a(str(self), _name=name)  #TODO - no href bug
        return '<a name="{}">{}</a>'.format(name, self.x)

    def big(self):
        """[wraps the string in big tags]

        Returns:
            [str]: [the string in big tags]
        """
        return "<big>" + self.x + "</big>"

    def blink(self):
        """[wraps the string in blink tags]

        Returns:
            [str]: [the string in blink tags]
        """
        return "<blink>" + self.x + "</blink>"

    def bold(self):
        """[wraps the string in bold tags]

        Returns:
            [str]: [the string in bold tags]
        """
        return "<b>" + self.x + "</b>"

    def fixed(self):
        """[wraps the string in fixed tags]

        Returns:
            [str]: [the string in fixed tags]
        """
        return "<tt>" + self.x + "</tt>"

    def fontcolor(self, color: str):
        """[wraps the string in font tags with a specified color]

        Args:
            color (str): [the color to use]

        Returns:
            [str]: [the string in font tags]
        """
        return "<font color=" + color + ">" + self.x + "</font>"

    def fontsize(self, size: str):
        """[wraps the string in font tags with a specified size]

        Args:
            size (str): [the size to use]

        Returns:
            [str]: [the string in font tags]
        """
        return "<font size=" + size + ">" + self.x + "</font>"

    def italics(self):
        """[wraps the string in italics tags]

        Returns:
            [str]: [the string in italics tags]
        """
        return "<i>" + self.x + "</i>"

    def link(self, url: str):
        """[wraps the string in a link tag]

        Args:
            url (str): [the url to use]

        Returns:
            [str]: [the string in a link tag]
        """
        return "<a href=" + url + ">" + self.x + "</a>"

    def small(self):
        """[wraps the string in small tags]

        Returns:
            [str]: [the string in small tags]
        """
        return "<small>" + self.x + "</small>"

    def strike(self):
        """[wraps the string in strike tags]

        Returns:
            [str]: [the string in strike tags]
        """
        return "<strike>" + self.x + "</strike>"

    def sub(self):
        """[wraps the string in sub tags]

        Returns:
            [str]: [the string in sub tags]
        """
        return "<sub>" + self.x + "</sub>"

    def sup(self):
        """[wraps the string in sup tags]

        Returns:
            [str]: [the string in sup tags]
        """
        return "<sup>" + self.x + "</sup>"

    def div(self, *args, **kwargs):
        """[wraps the string in a div tag]

        Returns:
            [str]: [the string in a div tag]
        """
        from domonic.html import div
        return div(self.x, *args, **kwargs)

    def webpage(self):
        """[wraps the string in a webpage]

        Returns:
            [str]: [the string as a webpage]
        """
        from domonic.html import html, body, head, title, script, style, meta, link, h1
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

    def __call__(self, tag: str, **kwargs):
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


class RegExp():

    def __init__(self, expression, flags=""):
        self.expression = expression
        self.flags = flags.lower()  #: A string that contains the flags of the RegExp object.
        # self.multiline  # Whether or not to search in strings across multiple lines.
        # self.source  # The text of the pattern.
        # self.sticky  # Whether or not the search is sticky
        # self.lastIndex  # The index at which to start the next match.

    @property
    def dotAll(self):
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
        if 's' not in self.flags:
            self.flags += "s" if value else ""

    @property
    def multiline(self):
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
        if 'm' not in self.flags:
            self.flags += "m" if value else ""

    @property
    def source(self):
        """[The text of the pattern.]
        Returns:
            [str]: [The text of the pattern.]
        """
        return self.expression

    @property
    def global_(self):
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
        if 'g' not in self.flags:
            self.flags += "g" if value else ""

    @property
    def hasIndices(self):
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
        if 'd' not in self.flags:
            self.flags += "d" if value else ""

    @property
    def ignoreCase(self):
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
        if 'i' not in self.flags:
            self.flags += "i" if value else ""

    @property
    def unicode(self):
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
        if 'u' not in self.flags:
            self.flags += "u" if value else ""

    def compile(self):
        """ (Re-)compiles a regular expression during execution of a script. """
        pass

    # def exec(self, s: str):  # TODO - test
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
    def exec(self, s: str):
        """ Executes a search for a match in its string parameter. """
        # print("exec:", self.expression, s)
        m = re.search(self.expression, s)
        # print(m)
        if (m):
            return [s for s in m.groups()]

    def test(self, s: str):
        """[Tests for a match in its string parameter.]

        Args:
            s (str): [a string to match]

        Returns:
            [bool]: [True if match else False]
        """
        m = re.match(self.expression, s)
        # print(m)
        if (m):
            return True
        else:
            return False

    def toString(self):
        """ Returns a string representation of the RegExp object. """
        return self.__str__()

    def __str__(self):
        """" Returns a string representing the specified object.
        Overrides the Object.prototype.toString() method. """
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


def ToInt32(v):
    return v >> 0


def ToUint32(v):
    return (v >> 0) if v >= 0 else ((v + 0x100000000) >> 0)


class ArrayBuffer:

    def __init__(self, length):
        # self.length = length
        self.buffer = array.array('B', [0] * length)
        # self.byteLength = length
        self.isView = False

    @property
    def byteLength(self):
        return self.buffer.buffer_info()[1]

    def __getitem__(self, index):
        return self.buffer[index]

    def __setitem__(self, index, value):
        self.buffer[index] = value

    def __getattr__(self, name):
        # return getattr(self.buffer, name)
        # TODO - try on self if not get from buffer. (was this a todo)?
        return getattr(self.buffer, name)

    def __len__(self):
        # return self.length
        return len(self.buffer)

    @property
    def length(self):
        # return self.__length
        return len(self.buffer)

    # @length.setter

    def __str__(self):
        return str(self.buffer)

    def __repr__(self):
        return repr(self.buffer)

    def slice(self, start, end):
        return self.buffer[start:end]


class DataView(ArrayBuffer):
    # ?? is this right. don't look lt
    def __init__(self, buffer, byteOffset=0, byteLength=None):
        super().__init__(byteLength)
        self.isView = True
        self.buffer = buffer
        self.byteOffset = byteOffset
        self.byteLength = byteLength

    def getUint8(self, index):
        return self.buffer.getUint8(self.byteOffset + index)

    def getInt8(self, index):
        return self.buffer.getInt8(self.byteOffset + index)

    def getUint16(self, index, littleEndian=False):
        return self.buffer.getUint16(self.byteOffset + index, littleEndian)

    def getInt16(self, index, littleEndian=False):
        return self.buffer.getInt16(self.byteOffset + index, littleEndian)

    def getUint32(self, index, littleEndian=False):
        return self.buffer.getUint32(self.byteOffset + index, littleEndian)

    def getInt32(self, index, littleEndian=False):
        return self.buffer.getInt32(self.byteOffset + index, littleEndian)

    def getFloat32(self, index, littleEndian=False):
        return self.buffer.getFloat32(self.byteOffset + index, littleEndian)

    def getFloat64(self, index, littleEndian=False):
        return self.buffer.getFloat64(self.byteOffset + index, littleEndian)

    def setUint8(self, index, value):
        self.buffer.setUint8(self.byteOffset + index, value)

    def setInt8(self, index, value):
        self.buffer.setInt8(self.byteOffset + index, value)

    def setUint16(self, index, value, littleEndian=False):
        self.buffer.setUint16(self.byteOffset + index, value, littleEndian)

    def setInt16(self, index, value, littleEndian=False):
        self.buffer.setInt16(self.byteOffset + index, value, littleEndian)


class TypedArray:

    BYTES_PER_ELEMENT = 1

    def __init__(self, *args):
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
            self.buffer = array.array('B', [0] * 0)
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
                raise Exception("ArrayBuffer length minus the byteOffset is not a multiple of the element size.")

            if (len(args) < 3):
                self.byteLength = self.buffer.byteLength - self.byteOffset

                if (self.byteLength % self.BYTES_PER_ELEMENT):
                    # raise RangeError("length of buffer minus byteOffset not a multiple of the element size");
                    raise Exception("length of buffer minus byteOffset not a multiple of the element size")

                self.length = self.byteLength / self.BYTES_PER_ELEMENT
            else:
                self.length = ToUint32(args[2])
                self.byteLength = self.length * self.BYTES_PER_ELEMENT
            if ((self.byteOffset + self.byteLength) > self.buffer.byteLength):
                # raise RangeError("byteOffset and length reference an area beyond the end of the buffer");
                raise Exception("byteOffset and length reference an area beyond the end of the buffer")

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
            self.buffer = array.array('B', [0] * 0)
            self.byteLength = 0
            # self.length = 0
            self.isView = False
            self.set(arg)
            return
        elif isinstance(arg, int):
            # self.buffer = array.array('B', [0] * arg)
            print('a!')
            # self.buffer = ArrayBuffer(arg)
            # self.byteLength = arg
            # self.length = arg
            # self.isView = False

            # // Constructor(unsigned long length)
            self.length = ToInt32(args[0])
            if (self.length < 0):
                raise Exception('ArrayBufferView size is not a small enough positive integer')

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

    @property  # TODO - test try this for sneaky way of binding to exsiting array methods?
    def args(self):
        return self.buffer

    @staticmethod
    def of(*args):
        # Creates a new Int8Array with a variable number of arguments
        return Int8Array(args)

    @staticmethod
    def from_(thing):
        # Creates a new Int8Array from an array-like or iterable object
        return Int8Array(thing)

    # def __getitem__(self, index):
    #     return self.buffer[index]

    # def __setitem__(self, index, value):
    #     self.buffer[index] = value

    # // getter type (unsigned long index);
    def __getitem__(self, index):
        if index is None:
            raise SyntaxError("Not enough arguments")

        index = ToUint32(index)
        if (index >= self.length):
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
    def __setitem__(self, index, value):
        # print('set', index, value)
        if (index is None and value is None):
            raise SyntaxError("Not enough arguments")

        index = ToUint32(index)
        if (index >= self.length):
            return undefined

        b = self._pack(value)
        # print(b)
        # print(  self._pack(10) )
        # print(  self._pack(20) )
        # print(  self._pack(30) )
        i = 0
        o = self.byteOffset + index * self.BYTES_PER_ELEMENT
        for i in range(0, self.BYTES_PER_ELEMENT):
            self.buffer[o] = b[i]

    # // void set(TypedArray array, optional unsigned long offset);
    # // void set(sequence<type> array, optional unsigned long offset);
    def set(self, index, value):
        if (index is None):
            raise SyntaxError("Not enough arguments")

        # arr = None
        # sequence = None
        # offset = None
        # nlen = None
        # i = None
        # s = None
        # d = None
        # byteOffset = None
        # byteLength = None
        # tmp = None

        if (type(index, object) and index == self):
            # void set(TypedArray arr, optional unsigned long offset)
            arr = index
            offset = ToUint32(value)

            if (offset + arr.length > self.length):
                # raise RangeError("Offset plus length of array is out of range")
                raise Exception("Offset plus length of array is out of range")

            byteOffset = self.byteOffset + offset * self.BYTES_PER_ELEMENT
            byteLength = arr.length * self.BYTES_PER_ELEMENT

            if (arr.buffer == self.buffer):
                tmp = []
                s = arr.byteOffset
                for i in range(0, byteLength):
                    tmp[i] = arr.buffer[s]
                    s += 1
                d = byteOffset
                for i in range(0, byteLength):
                    self.buffer[d] = tmp[i]
                    d += 1
            else:
                s = arr.byteOffset
                d = byteOffset
                for i in range(0, byteLength):
                    self.buffer[d] = arr.buffer[s]
                    s += 1
                    d += 1
        elif (type(index, object) and index != self):
            # void set(sequence<type> arr, optional unsigned long offset);
            sequence = index
            nlen = ToUint32(sequence.length)
            offset = ToUint32(value)

            if (offset + nlen > self.length):
                # raise RangeError("Offset plus length of arr is out of range")
                raise Exception("Offset plus length of arr is out of range")

            for i in range(0, len):
                s = sequence[i]
                self._setter(offset + i, Number(s))
        else:
            raise TypeError("Unexpected argument type(s)")

    # // TypedArray subarray(long begin, optional long end);

    def subarray(self, start, end):

        def clamp(v, min, max):
            m1 = max if v > max else v
            return min if v < min else m1

        if start is None:
            start = 0
        if end is None:
            end = self.length

        start = ToInt32(start)
        end = ToInt32(end)

        if (start < 0):
            start = self.length + start
        if (end < 0):
            end = self.length + end

        start = clamp(start, 0, self.length)
        end = clamp(end, 0, self.length)

        nlen = end - start
        if (nlen < 0):
            nlen = 0

        return self.__init__(self.buffer, self.byteOffset + start * self.BYTES_PER_ELEMENT, nlen)


def as_signed(value, bits):
    """ Converts an unsigned integer to a signed integer. """
    s = 32 - bits
    mask = (1 << s) - 1
    return (value & mask) - (value & (mask << s))


def as_unsigned(value, bits):
    s = 32 - bits
    mask = (1 << s) - 1
    return value & mask


class __byteutils__():

    def packI8(self, n):
        return [n & 0xff]
        # return struct.pack('B', n)

    def unpackI8(self, b):
        return as_signed(b[0], 8)
        # return struct.unpack('B', b)[0]

    def packU8(self, n):
        return [n & 0xff]
        # return struct.pack('B', n)

    def unpackU8(self, bytes):
        return as_unsigned(bytes[0], 8)
        # return struct.unpack('B', bytes)[0]

    def packU8Clamped(self, n):
        n = Math.round(Number(n))
        # return [n < 0 ? 0 : n > 0xff ? 0xff : n & 0xff]
        if (n < 0):
            return [0]
        elif (n > 0xff):
            return [0xff]
        else:
            return [n & 0xff]
        # return struct.pack('B', n)

    def packI16(self, n):
        return [(n >> 8) & 0xff, n & 0xff]
        # return struct.pack('>H', n)

    def unpackI16(self, bytes):
        return as_signed(bytes[0] << 8 | bytes[1], 16)
        # return struct.unpack('>H', bytes)[0]

    def packU16(self, n):
        return [(n >> 8) & 0xff, n & 0xff]
        # return struct.pack('>H', n)

    def unpackU16(self, bytes):
        return as_unsigned(bytes[0] << 8 | bytes[1], 16)
        # return struct.unpack('>H', bytes)[0]

    def packI32(self, n):
        return [(n >> 24) & 0xff, (n >> 16) & 0xff, (n >> 8) & 0xff, n & 0xff]
        # return struct.pack('>I', n)

    def unpackI32(self, bytes):
        return as_signed(bytes[0] << 24 | bytes[1] << 16 | bytes[2] << 8 | bytes[3], 32)
        # return struct.unpack('>I', bytes)[0]

    def packU32(self, n):
        return [(n >> 24) & 0xff, (n >> 16) & 0xff, (n >> 8) & 0xff, n & 0xff]
        # return struct.pack('>I', n)

    def unpackU32(self, bytes):
        return as_unsigned(bytes[0] << 24 | bytes[1] << 16 | bytes[2] << 8 | bytes[3], 32)
        # return struct.unpack('>I', bytes)[0]

    def packIEEE754(self, v, ebits, fbits):

        bias = (1 << (ebits - 1)) - 1

        def roundToEven(n):
            w = Math.floor(n)
            f = n - w
            if (f < 0.5):
                return w
            if (f > 0.5):
                return w + 1
            # return w % 2 ? w + 1 : w
            return w if (w % 2) else w + 1

        # Compute sign, exponent, fraction
        if (v != v):
            # NaN
            # http://dev.w3.org/2006/webapi/WebIDL/#es-type-mapping
            e = (1 << ebits) - 1
            f = pow(2, fbits - 1)
            s = 0
        elif (v == Global.Infinity or v == -Global.Infinity):
            e = (1 << ebits) - 1
            f = 0
            # s = (v < 0) ? 1 : 0
            s = 1 if (v < 0) else 0
        elif (v == 0):
            e = 0
            f = 0
            s = 1 if (1 / v == -Global.Infinity) else 0
        else:
            s = v < 0
            v = abs(v)

            if (v >= pow(2, 1 - bias)):

                e = min(Math.floor(Math.log(v) / Math.LN2), 1023)
                f = roundToEven(v / pow(2, e) * pow(2, fbits))

                if (f / pow(2, fbits) >= 2):
                    e = e + 1
                    f = 1
                if (e > bias):
                    # Overflow
                    e = (1 << ebits) - 1
                    f = 0
                else:
                    # Normalized
                    e = e + bias
                    f = f - pow(2, fbits)
            else:
                # Denormalized
                e = 0
                f = roundToEven(v / pow(2, 1 - bias - fbits))

        # Pack sign, exponent, fraction
        bits = []
        for i in range(fbits):
            bits.append(f % 2)
            f = Math.floor(f / 2)
        for i in range(ebits):
            bits.append(e % 2)
            e = Math.floor(e / 2)
        bits.append(s)
        bits.reverse()
        mystr = bits.join('')

        # Bits to bytes
        b = []
        while (mystr.length):
            b.push(parseInt(mystr.substring(0, 8), 2))
            mystr = mystr.substring(8)
        return b

    def unpackIEEE754(self, bytes, ebits, fbits):

        # Bytes to bits
        bits = []
        for i in range(len(bytes)):
            b = bytes[i]
            for j in range(8):
                bits.append(1 if b % 2 else 0)
                b = b >> 1

        bits.reverse()
        mystr = bits.join('')

        # Unpack sign, exponent, fraction
        bias = (1 << (ebits - 1)) - 1
        # s = parseInt(str.substring(0, 1), 2) ? -1 : 1
        s = -1 if (mystr[0] == '1') else 1

        e = parseInt(mystr.substring(1, 1 + ebits), 2)
        f = parseInt(mystr.substring(1 + ebits), 2)

        # // Produce number
        if (e == (1 << ebits) - 1):
            # return f !== 0 ? NaN : s * Infinity
            if (f != 0):
                return Global.NaN
            else:
                return s * Global.InfInfinity
        elif (e > 0):
            # Normalized
            return s * pow(2, e - bias) * (1 + f / pow(2, fbits))
        elif (f != 0):
            # Denormalized
            return s * pow(2, -(bias - 1)) * (f / pow(2, fbits))
        else:
            return -0 if s < 0 else 0

    def unpackF64(self, b):
        return self.unpackIEEE754(b, 11, 52)
        # return struct.unpack('>d', b)[0]

    def packF64(self, v):
        return self.packIEEE754(v, 11, 52)
        # return struct.pack('>d', v)

    def unpackF32(self, b):
        return self.unpackIEEE754(b, 8, 23)
        # return struct.unpack('>f', b)[0]

    def packF32(self, v):
        return self.packIEEE754(v, 8, 23)
        # return struct.pack('>f', v)


Int8Array = type('Int8Array',
                 (TypedArray,),
                 {'name': 'Int8Array', '_pack': __byteutils__.packI8, '_unpack': __byteutils__.unpackI8})
Int8Array.BYTES_PER_ELEMENT = 1

Uint8Array = type('Uint8Array',
                  (TypedArray,),
                  {'name': 'Uint8Array', '_pack': __byteutils__.packU8, '_unpack': __byteutils__.unpackU8})
Uint8Array.BYTES_PER_ELEMENT = 1

Uint8ClampedArray = type('Uint8ClampedArray',
                         (TypedArray,),
                         {'name': 'Uint8ClampedArray', '_pack': __byteutils__.packU8Clamped, '_unpack': __byteutils__.unpackU8})
Uint8ClampedArray.BYTES_PER_ELEMENT = 1

Int16Array = type('Int16Array',
                  (TypedArray,),
                  {'name': 'Int16Array', '_pack': __byteutils__.packI16, '_unpack': __byteutils__.unpackI16})
Int16Array.BYTES_PER_ELEMENT = 2

Uint16Array = type('Uint16Array',
                   (TypedArray,),
                   {'name': 'Uint16Array', '_pack': __byteutils__.packU16, '_unpack': __byteutils__.unpackU16})
Uint16Array.BYTES_PER_ELEMENT = 2

Int32Array = type('Int32Array',
                  (TypedArray,),
                  {'name': 'Int32Array', '_pack': __byteutils__.packI32, '_unpack': __byteutils__.unpackI32}
                  )
Int32Array.BYTES_PER_ELEMENT = 4

Uint32Array = type('Uint32Array',
                   (TypedArray,),
                   {'name': 'Uint32Array', '_pack': __byteutils__.packU32, '_unpack': __byteutils__.unpackU32})
Uint32Array.BYTES_PER_ELEMENT = 4

Float32Array = type('Float32Array',
                    (TypedArray,),
                    {'name': 'Float32Array', '_pack': __byteutils__.packF32, '_unpack': __byteutils__.unpackF32})
Float32Array.BYTES_PER_ELEMENT = 4

Float64Array = type('Float64Array',
                    (TypedArray,),
                    {'name': 'Float64Array', '_pack': __byteutils__.packF64, '_unpack': __byteutils__.unpackF64})
Float64Array.BYTES_PER_ELEMENT = 8

# BigInt64Array = type('BigInt64Array',
# (TypedArray,), {'name': 'BigInt64Array', '_pack': __byteutils__.packI64, '_unpack': __byteutils__.unpackI64})
# BigInt64Array.BYTES_PER_ELEMENT = 8

# BigUint64Array = type('BigUint64Array',
# (TypedArray,), {'name': 'BigUint64Array', '_pack': __byteutils__.packU64, '_unpack': __byteutils__.unpackU64})
# BigUint64Array.BYTES_PER_ELEMENT = 8


# TODO - test
class Error(Exception):
    ''' Raise Errors '''
    def __init__(self, message, *args, **kwargs):
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

class Reflect():
    """
    The Reflect object provides the following static functions which have the same names as the proxy handler methods.
    Some of these methods are also the same as corresponding methods on Object,
    although they do have some subtle differences between them.
    """

    @staticmethod
    def ownKeys(target):
        """ Returns an array of the target object's own (not inherited) property keys. """
        return target.keys()
        # return target.__dict__.keys()

    @staticmethod
    def apply(target, thisArgument, argumentsList):
        """ Calls a target function with arguments as specified by the argumentsList parameter.
        See also Function.prototype.apply(). """
        return target(*argumentsList)

    @staticmethod
    def construct(target, argumentsList, newTarget):
        """ The new operator as a function. Equivalent to calling new target(...argumentsList).
        Also provides the option to specify a different prototype. """
        raise NotImplementedError

    @staticmethod
    def defineProperty(target, propertyKey, attributes):
        """ Similar to Object.defineProperty().
        Returns a Boolean that is true if the property was successfully defined. """
        raise NotImplementedError

    @staticmethod
    def deleteProperty(target, propertyKey):
        """ The delete operator as a function. Equivalent to calling delete target[propertyKey]. """
        raise NotImplementedError

    @staticmethod
    def get(target, propertyKey, receiver):
        """ Returns the value of the property.
        Works like getting a property from an object (target[propertyKey]) as a function. """
        raise NotImplementedError

    @staticmethod
    def getOwnPropertyDescriptor(target, propertyKey):
        """ Similar to Object.getOwnPropertyDescriptor().
        Returns a property descriptor of the given property if it exists on the object,  undefined otherwise. """
        raise NotImplementedError

    getPrototypeOf = Object.getPrototypeOf
    # isExtensible = Object.isExtensible

    @staticmethod
    def has(target, propertyKey):
        """ Returns a Boolean indicating whether the target has the property.
        Either as own or inherited. Works like the in operator as a function. """
        raise NotImplementedError

    @staticmethod
    def preventExtensions(target):
        """ Similar to Object.preventExtensions(). Returns a Boolean that is true if the update was successful. """
        raise NotImplementedError

    @staticmethod
    def set(target, propertyKey, value, receiver):
        """ A function that assigns values to properties.
        Returns a Boolean that is true if the update was successful. """
        raise NotImplementedError

    @staticmethod
    def setPrototypeOf(target, prototype):
        """ A function that sets the prototype of an object. Returns a Boolean that is true if the update was successful. """
        raise NotImplementedError


class Symbol():

    # a global registry for symbols
    registry = []

    # Creates a new Symbol object.
    def __init__(self, symbol):
        self.symbol = symbol
        self.description = None
        self.registry.append(self)
        # self.__class__.registry = self.registry

    def hasInstance(self, obj):
        """[A method determining if a constructor object recognizes an object as its instance. Used by instanceof.]

        Args:
            obj ([type]): [a constructor object]

        Returns:
            [type]: [True if obj is an instance of this symbol, False otherwise]
        """
        return self.symbol == obj.symbol

    def isConcatSpreadable(self):
        """ A Boolean value indicating if an object should be flattened to its array elements.
        Used by Array.prototype.concat()."""
        return False

    def iterator(self, obj):
        """ A method returning the default iterator for an object. Used by for...of. """
        return iter(obj)

    def asyncIterator(self, obj):
        """ A method that returns the default AsyncIterator for an object. Used by for await...of. """
        return iter(obj)

    # A method that matches against a string, also used to determine if an object may be used as a regular expression.
    def match(self, item):
        """ A method that matches the symbol against a string,
        also used to determine if an object may be used as a regular expression. """
        raise NotImplementedError

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
    def search(self):
        raise NotImplementedError

    # A method that splits a string at the indices that match a regular expression. Used by String.prototype.split().
    def split(self):
        raise NotImplementedError

    # A constructor function that is used to create derived objects.
    def species(self):
        raise NotImplementedError

    # A method converting an object to a primitive value.
    def toPrimitive(self):
        raise NotImplementedError

    # A string value used for the default description of an object.
    # Used by Object.prototype.toString().
    def toStringTag(self):
        raise NotImplementedError

    # An object value of whose own and inherited property names are excluded from the with environment bindings of the associated object.
    def unscopables(self):
        raise NotImplementedError

    # @staticmethod
    # def for(key):
    #     """ Searches for existing Symbols with the given key and returns it if found.
    #     Otherwise a new Symbol gets created in the global Symbol registry with key. """
    #     raise NotImplementedError

    # @staticmethod
    # def keyFor(sym)
    #     """ Retrieves a shared Symbol key from the global Symbol registry for the given Symbol. """
    #     raise NotImplementedError

    def toSource(self):
        """ Returns a string containing the source of the Symbol. Overrides the Object.prototype.toSource() method. """
        raise NotImplementedError

    def toString(self):
        """ Returns a string containing the description of the Symbol.
        Overrides the Object.prototype.toString() method. """
        raise NotImplementedError

    def valueOf(self):
        """ Returns the Symbol. Overrides the Object.prototype.valueOf() method. """
        raise NotImplementedError


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
