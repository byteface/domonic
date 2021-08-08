"""
    domonic.javascript
    ====================================
    - https://www.w3schools.com/jsref/jsref_reference.asp
    - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference
"""

# from typing import *
import sys
import urllib.parse
from dateutil.parser import parse
import datetime
from datetime import timedelta
import time
from urllib.parse import unquote, quote
import math
import random
import threading
import signal
import typing
import requests
import gc
import multiprocessing
from multiprocessing.pool import ThreadPool as Pool
import re


# true = True
# false = False

class Object(object):
    """ Creates a Mock Javascript Object in python """

    def __init__(self, obj=None, *args, **kwargs):
        """[Creates a Mock Javascript Object in python]

        Args:
            obj ([type]): [pass an object, dict or callable to the contructor]
        """
        # print('object created!')
        if obj is None:
            obj = {}

        self.__attribs__ = {}
        if callable(obj):
            self.__attribs__ = {}
            self.__attribs__['__call__'] = obj
            # self.__attribs__['__call__'].__name__ = '__call__'
            # self.__attribs__['__call__'].__doc__ = 'The function object itself.'
            # self.__attribs__['__call__'].__module__ = '__main__'
        elif isinstance(obj, dict):
            self.__attribs__ = obj  # set the dict as the attribs
            # self.__attribs__['__dict__'] = obj  # set the dict as the attribs
            self.__dict__ = {**self.__dict__, **obj}  # set the dict as the attribs?
            print('YO!')
        else:
            try:
                self.__attribs__ = {}
                self.__attribs__.update(obj.__attribs__)
                self.__attribs__.update(kwargs)
                self.__attribs__.update(args)
                self.__attribs__['__class__'] = obj.__class__.__name__
                self.__attribs__['__module__'] = obj.__module__
                self.__attribs__['__doc__'] = obj.__doc__
                self.__attribs__['__proto__'] = obj
                # self.__attribs__['__proto__'].__class__ = Object
                # self.__attribs__['__proto__'].__attribs__ = self.__attribs__
            except Exception as e:
                print("Object.__init__() failed to set attribs", e)

    def __str__(self):
        """ Returns a string representation of the object."""
        # return self.toString()
        return str(self.__attribs__)

    # def __repr__(self):
    #     """ Returns a string representation of the object."""
    #     return self.toString()

    @staticmethod
    def fromEntries(entries):
        """
        transforms a list of lists containing key and value into an object.

        @param entries: a list containing key and value tuples. The key and value
                        are separated by ':'
        @type entries: list of tuple(string, string)
        @returns: a { dict } object.

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
                for k, v in source.__attribs__.items():
                    target[k] = v
        else:
            if isinstance(source, dict):
                for k, v in source.items():
                    setattr(target, k, v)
            else:
                for k, v in source.attribs.items():
                    setattr(target, k, v)

        # return target
        # for prop in source.__attribs__:
        #     if source.propertyIsEnumerable(prop):
        #         target.__attribs__[prop] = source.__attribs__[prop]
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
        return obj.__attribs__.keys()   # TODO - this is probably wrong

    @staticmethod
    def values(obj):
        """ Returns an array containing the values that correspond to
        all of a given object's own enumerable string properties. """
        if isinstance(obj, dict):
            return obj.values()
        if isinstance(obj, (float, int)):
            return []
        return obj.__attribs__.values()  # TODO - this is probably wrong

    @staticmethod
    def getOwnPropertyDescriptor(obj, prop):
        """ Returns a property descriptor for a named property on an object. """
        if isinstance(obj, dict):
            return obj[prop]
        return obj.__attribs__[prop]

    @staticmethod
    def getOwnPropertyNames(obj):
        """ Returns an array containing the names of all of the given object's
        own enumerable and non-enumerable properties. """
        if isinstance(obj, dict):
            return obj.keys()
        elif isinstance(obj, Object):
            return obj.__attribs__.keys()
        elif isinstance(obj, object):
            return [prop for prop in dir(obj) if not prop.startswith('__')]
        return obj.__attribs__.keys()

    # @staticmethod
    # def _is(value1, value2):
    #     """ Compares if two values are the same value.
    #     Equates all NaN values (which differs from both Abstract Equality Comparison and Strict Equality Comparison)."""
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

    # @staticmethod
    # def isExtensible(obj):
    #     """ Determines if extending of an object is allowed. """
    #     if isinstance(obj, dict):
    #         return True
    #     elif isinstance(obj, Object):
    #         return obj.extensible
    #     elif isinstance(obj, object):
    #         return True
    #     return False

    # @staticmethod
    # def isFrozen(obj):
    #     """ Determines if an object was frozen. """
    #     if isinstance(obj, dict):
    #         return False
    #     elif isinstance(obj, Object):
    #         return obj.frozen
    #     elif isinstance(obj, object):
    #         return False
    #     return False

    # @staticmethod
    # def isSealed(obj):
    #     """ Determines if an object is sealed. """
    #     if isinstance(obj, dict):
    #         return False
    #     elif isinstance(obj, Object):
    #         return obj.sealed
    #     elif isinstance(obj, object):
    #         return False
    #     return False

    # @staticmethod
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

    # @staticmethod
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

    # @staticmethod
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

    # @staticmethod
    # def freeze(obj):
    #     """ Freezes an object. Other code cannot delete or change its properties. """
    #     if isinstance(obj, dict):
    #         return False
    #     elif isinstance(obj, Object):
    #         obj.frozen = True
    #         return True
    #     elif isinstance(obj, object):
    #         return False
    #     return False

    def prototype(self, obj):
        """
        prototype and allows you to add properties and methods to this object
        """
        if isinstance(obj, dict):
            return False
        elif isinstance(obj, Object):
            obj.prototype = self
            return True
        elif isinstance(obj, object):
            return False
        return False

    # def __getattr__(self, name):
    #     """
    #     The __getattr__() method is called when the attribute 'name' is accessed.
    #     """
    #     if name == 'objectId':
    #         return self.getId()
    #     if name == 'proto':
    #         return self.__class__.fromEntries(self.__attribs__)
    #     return getattr(self, name)

    def __defineGetter__(self, prop, func):
        """ Adds a getter function for the specified property. """
        self.__attribs__[prop] = property(func)
        return self

    def __defineSetter__(self, prop, func):
        """ Associates a function with a property that, when set, calls the function. """
        self.__attribs__[prop] = property(func)
        return self

    def __lookupGetter__(self, prop):
        """
        Returns the getter function for the specified property.
        """
        return self.__attribs__[prop]

    def __lookupSetter__(self, prop):
        """ Returns the function associated with the specified property by the __defineSetter__() method. """
        return self.__attribs__[prop]

    def hasOwnProperty(self, prop):
        """ Returns a boolean indicating whether an object contains the specified property
        as a direct property of that object and not inherited through the prototype chain. """
        # raise NotImplementedError
        # return hasattr(self, prop)
        return self.__attribs__.get(prop, None) != None

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
        return '[' + self.__class__.__name__ + ': ' + str(self.__attribs__) + ']'

    def valueOf(self):
        """ Returns the value of the object. """
        return self

    def __str__(self):
        """ Returns a string representation of the object. """
        return self.toString()

    # def __repr__(self):
    #     """ Returns a string representation of the object. """
    #     return self.toString()

    def __iter__(self):
        """ Iterates over object's properties. """
        for prop in self.__attribs__:
            yield prop
        for key in self.__dict__:
            yield key
        return

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
    #     return self.__attribs__

    def __getitem__(self, key):
        """ Returns the value of the specified property. """
        # print('getting', key)
        return self.__attribs__[key]

    def __setitem__(self, key, value):
        """ Sets the value of the specified property. """
        # print('SETTING')
        # print(key, value)
        self.__attribs__[key] = value

    def __delitem__(self, key):
        """ Deletes the specified property. """
        del self.__attribs__[key]

    def __len__(self):
        """ Returns the number of properties. """
        return len(self.__attribs__)

    def __contains__(self, key):
        """ Returns whether the specified property exists. """
        return key in self.__attribs__

    # def __call__(self, *args, **kwargs):
    #     """ Calls the object. """
    #     return self.toString()


class Function(object):
    """ a Function object """

    def __init__(self, func):
        self.func = func
        self.arguments = []
        self.caller = None
        self.displayName = None
        self.length = None
        self.name = None
        # self.isCallable = True
        # self.constructor = False
        # self.__proto__ = None
        # self.prototype = None
        # self.extensible = True
        # self.frozen = False
        # self.sealed = False
        # self.__class__ = Function
        # self.__dict__ = {}
        # self.__attribs__ = {}
        # self.__methods__ = {}

    def apply(self, thisArg=None, *args, **kwargs):
        """[calls a function with a given this value, and arguments provided as an array]

        Args:
            thisArg ([type]): [The value of this provided for the call to func.]

        Returns:
            [type]: [result of calling the function.]
        """
        if thisArg is not None:
            return self.func(args)
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
        # raise NotImplementedError
        print(thisArg)
        print(args)
        if thisArg is not None:
            return self.func(thisArg, args)
            # return self.func(this=thisArg, *args)
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

        self._data = {}
        self._order = []

    def __contains__(self, key):
        return key in self._dict

    def __getitem__(self, key):
        return self._dict[key]

    def __setitem__(self, key, value):
        if key not in self._dict:
            self._order.append(key)
            self._dict[key] = value

    def __delitem__(self, key):
        self._order.remove(key)
        del self._dict[key]

    def clear(self):
        """ Removes all key-value pairs from the Map object. """
        self._data = {}
        self._order = []

    def delete(self, key):
        """ Returns true if an element in the Map object existed and has been removed,
        or false if the element does not exist. Map.prototype.has(key) will return false afterwards. """
        try:
            self._order.remove(key)
            del self._dict[key]
            return True
        except Exception:
            return False

    def get(self, key, default=None):
        """ Returns the value associated to the key, or undefined if there is none. """
        return self._dict.get(key, default)

    def has(self, key):
        """ Returns a boolean asserting whether a value has been associated to the key in the Map object or not."""
        return key in self._dict

    def set(self, key, value):
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

    def update(self, ordered_dict):
        for key, value in ordered_dict.iteritems():
            self[key] = value

    def __str__(self):
        return str([(x, self._dict[x]) for x in self._order])


class FormData(object):
    """[utils for a form]

    Args:
        object ([str]): [takes a string or pyml object and returns a FormData]
    """

    def __init__(self, form):
        """ creates a new FormData object. """
        # TODO - parse to domonic.
        # if isinstance(form, str):
        #   self._data = domonic.loads(form) # TODO - parser wont be done enough yet
        # if isinstance(form, Node):
        #   self._data = form
        raise NotImplementedError

    def append(self, name, value, filename):
        """ Appends a new value onto an existing key inside a FormData object,
        or adds the key if it does not already exist. """
        raise NotImplementedError

    def delete(self, name):
        """ Deletes a key/value pair from a FormData object. """
        raise NotImplementedError

    def entries(self):
        """ Returns an iterator allowing to go through all key/value pairs contained in this object. """
        raise NotImplementedError

    def get(self, name):
        """ Returns the first value associated with a given key from within a FormData object. """
        raise NotImplementedError

    def getAll(self, name):
        """ Returns an array of all the values associated with a given key from within a FormData """
        raise NotImplementedError

    def has(self, name):
        """ Returns a boolean stating whether a FormData object contains a certain key."""
        raise NotImplementedError

    def keys(self):
        """ Returns an iterator allowing to go through all keys of the key/value pairs contained in this object."""
        raise NotImplementedError

    def set(self, name, value, filename):
        """ Sets a new value for an existing key inside a FormData object,
        or adds the key/value if it does not already exist."""
        raise NotImplementedError

    def values(self):
        """ Returns an iterator allowing to go through all values  contained in this object."""
        raise NotImplementedError


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

    i.e. you can pass strings and it will also work
    Math.abs('-1')

    """

    # CONSTANTS
    PI = 3.141592653589793
    E = 2.718281828459045
    LN2 = 0.6931471805599453
    LN10 = 2.302585092994046
    LOG2E = 1.4426950408889634
    LOG10E = 0.4342944819032518
    SQRT1_2 = 0.7071067811865476
    SQRT2 = 1.4142135623730951

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
    def abs(x):
        """ Returns the absolute value of x """
        return abs(x)

    @staticmethod
    @_force_number
    def acos(x):
        """ Returns the arccosine of x, in radians """
        return math.acos(x)

    @staticmethod
    @_force_number
    def acosh(x):
        """ Returns the hyperbolic arccosine of x """
        return math.acosh(x)

    @staticmethod
    @_force_number
    def asin(x):
        """ Returns the arcsine of x, in radians """
        return math.asin(x)

    @staticmethod
    @_force_number
    def asinh(x):
        """ Returns the hyperbolic arcsine of x """
        return math.asinh(x)

    @staticmethod
    @_force_number
    def atan(x):
        """ Returns the arctangent of x as a numeric value between -PI/2 and PI/2 radians """
        return math.atan(x)

    @staticmethod
    @_force_number
    def atan2(x, y):
        """ Returns the arctangent of the quotient of its arguments """
        return math.atan2(x, y)

    @staticmethod
    @_force_number
    def atanh(x):
        """ Returns the hyperbolic arctangent of x """
        return math.atanh(x)

    @staticmethod
    @_force_number
    def cbrt(x):
        """ Returns the cubic root of x """
        # return math.cbrt(x)
        return round(math.pow(x, 1 / 3))

    @staticmethod
    @_force_number
    def ceil(x):
        """ Returns x, rounded upwards to the nearest integer """
        return math.ceil(x)

    @staticmethod
    @_force_number
    def cos(x):
        """ Returns the cosine of x (x is in radians) """
        return math.cos(x)

    @staticmethod
    @_force_number
    def cosh(x):
        """ Returns the hyperbolic cosine of x """
        return math.cosh(x)

    @staticmethod
    @_force_number
    def exp(x):
        """ Returns the value of Ex """
        return math.exp(x)

    @staticmethod
    @_force_number
    def floor(x):
        """ Returns x, rounded downwards to the nearest integer """
        return math.floor(x)

    @staticmethod
    @_force_number
    def log(x, y):
        """ Returns the natural logarithm (base E) of x """
        return math.log(x, y)

    @staticmethod
    @_force_number
    def max(x, y):
        """ Returns the number with the highest value """
        return max(x, y)

    @staticmethod
    @_force_number
    def min(x, y):
        """ Returns the number with the lowest value """
        return min(x, y)

    @staticmethod
    @_force_number
    def random():
        """ Returns a random number between 0 and 1 """
        # return math.random(x)
        return random.random()

    @staticmethod
    @_force_number
    def round(x):
        """ Rounds x to the nearest integer """
        return round(x)

    @staticmethod
    @_force_number
    def pow(x, y):
        """ Returns the value of x to the power of y """
        return math.pow(x, y)

    @staticmethod
    @_force_number
    def sin(x):
        """ Returns the sine of x (x is in radians) """
        return math.sin(x)

    @staticmethod
    @_force_number
    def sinh(x):
        """ Returns the hyperbolic sine of x """
        return math.sinh(x)

    @staticmethod
    @_force_number
    def sqrt(x):
        """ Returns the square root of x """
        return math.sqrt(x)

    @staticmethod
    @_force_number
    def tan(x):
        """ Returns the tangent of an angle """
        return math.tan(x)

    @staticmethod
    @_force_number
    def tanh(x):
        """ Returns the hyperbolic tangent of a number """
        return math.tanh(x)

    @staticmethod
    @_force_number
    def trunc(x):
        """ Returns the integer part of a number (x) """
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
    def isFinite(x):  # TODO - test
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
    def parseFloat(x: str):
        """ Parses a string and returns a floating point number """
        return float(x)

    @staticmethod
    def parseInt(x: str):
        """ Parses a string and returns an integer """
        return int(x)

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
        """ use threads to create a timeout method """
        raise NotImplementedError

    # TODO - clearTimeout.
    @staticmethod
    def clearTimeout(job):
        print(job)
        job.cancel()


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

    def __init__(self, date: str = None, formatter='python'):
        if date is None:
            self.date = datetime.datetime.now()
        else:
            self.date = self.parse_date(date)

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
        self.job = Job(timedelta(microseconds=time * 1000), function, *args, **kwargs)
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

    def __init__(self, *args, **kwargs):
        # self.console = dom.console
        # self.document = dom.document
        # self.location = ''#dom.location
        self.location = None
        # globals()?
        # dir()?
        # locals()?

    @property
    def location(self):
        # print("@@@@@@@@@@@@@@@@@@@@@@")
        return self.__location

    @location.setter
    def location(self, x):
        # print("====================>>>>>>>", x)
        # dom.location = x
        # dom.location = dom.location(x)#Location(x)
        # from .dom import Location
        # print('test::::-------------------------------------------------------',Location)
        # print("xxxxxxxx>>>>>>", dom.location)
        # self.__location = dom.location
        # import requests.
        pass

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

    @staticmethod
    def setTimeout(function, t, *args, **kwargs):
        """ Calls a function or evaluates an expression after a specified number of milliseconds """
        import time
        time.sleep(t / 1000)  # TODO - still blocks
        function()
        return

    # TODO - clearTimeout.
    @staticmethod
    def clearTimeout(job):
        # job.stop()
        pass

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

    # @staticmethod
    # @getter
    # def navigator():
        """ Returns the Navigator object for the window (See Navigator object) """
        # return

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

# WINDOW
# localStorage  Allows to save key/value pairs in a web browser. Stores the data with no expiration date    Window
# blur()    Removes focus from an element   Element, Window
# clearTimeout()    Clears a timer set with setTimeout()    Window
# closed    Returns a Boolean value indicating whether a window has been closed or not  Window
# close()   Closes the output stream previously opened with document.open() Document, Window
# confirm() Displays a dialog box with a message and an OK and a Cancel button  Window
# defaultStatus Sets or returns the default text in the statusbar of a window   Window
# defaultView   Returns the window object associated with a document, or null if none is available. Document
# document  Returns the Document object for the window (See Document object)    Window
# focus()   Gives focus to an element   Element, Window
# frameElement  Returns the <iframe> element in which the current window is inserted    Window
# getComputedStyle()    Gets the current computed CSS styles applied to an element  Window
# getSelection()    Returns a Selection object representing the range of text selected by the user  Window
# history   Returns the History object for the window (See History object)  Window
# innerHeight   Returns the height of the window's content area (viewport) including scrollbars Window
# innerWidth    Returns the width of a window's content area (viewport) including scrollbars    Window
# location  Returns the Location object for the window (See Location object)    Window
# matchMedia()  Returns a MediaQueryList object representing the specified CSS media query string   Window
# moveBy()  Moves a window relative to its current position Window
# moveTo()  Moves a window to the specified position    Window
# name  Sets or returns an error name   Error, Attribute, Window
# navigator Returns the Navigator object for the window (See Navigator object)  Window
# onpopstate    The event occurs when the window's history changes  PopStateEvent
# open()    Opens an HTML output stream to collect output from document.write() Document, Window
# opener    Returns a reference to the window that created the window   Window
# outerHeight   Returns the height of the browser window, including toolbars/scrollbars Window
# outerWidth    Returns the width of the browser window, including toolbars/scrollbars  Window
# pageXOffset   Returns the pixels the current document has been scrolled (horizontally) from the upper left corner of the window   Window
# pageYOffset   Returns the pixels the current document has been scrolled (vertically) from the upper left corner of the window Window
# parent    Returns the parent window of the current window Window
# _print()   Prints the content of the current window    Window
# resizeBy()    Resizes the window by the specified pixels  Window
# resizeTo()    Resizes the window to the specified width and height    Window
# screen    Returns the Screen object for the window (See Screen object)    Window
# screenLeft    Returns the horizontal coordinate of the window relative to the screen  Window
# screenTop Returns the vertical coordinate of the window relative to the screen    Window
# scroll()  Deprecated. This method has been replaced by the scrollTo() method. Window
# scrollBy()    Scrolls the document by the specified number of pixels  Window
# scrollIntoView()  Scrolls the specified element into the visible area of the browser window   Element
# scrollTo()    Scrolls the document to the specified coordinates   Window
# scrollX   An alias of pageXOffset Window
# scrollY   An alias of pageYOffset Window
# sessionStorage    Allows to save key/value pairs in a web browser. Stores the data for one session    Window
# setTimeout()  Calls a function or evaluates an expression after a specified number of milliseconds    Window
# stop()    Stops the window from loading   Window
# status    Sets or returns the text in the statusbar of a window   Window
# top   Returns the topmost browser window  Window
# view  Returns a reference to the Window object where the event occurred   UiEvent


window = Window

# class null():
#     def __str__(self):
#         return ''
#     def __repr__(self):
#         return None


class Array(object):
    """ javascript array """

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

    def __getitem__(self, index):
        return self.args[index]

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
        return isinstance(other, Array) and \
            self.args == other.args

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return str(self.args)

    def __iter__(self):
        for i in self.args:
            yield i

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

    def fill(self):
        """ Fill the elements in an array with a static value """
        raise NotImplementedError

    def includes(self, value):
        """ Check if an array contains the specified element """
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
    def isArray(self, thing):
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
        return sorted(self.args)

    def reduce(self, func, value=None):
        """ Reduce the values of an array to a single value (going left-to-right) """
        try:
            return func(self.args[0], *self.args)
        except IndexError:
            return -1

    def reduceRight(self, func, value=None):
        """ Reduce the values of an array to a single value (going right-to-left) """
        #  written by .ai (https://6b.eleuther.ai/)
        #  Takes an array and reduces it based on a function in reverse order
        try:
            if value is None:
                return func(value, *self.args)
            else:
                return func(self.args[0], value, *self.args[1:])
        except IndexError:
            return -1

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

    # def from(self, obj):
    #     """[Creates an array from an object]

    #     Args:
    #         obj ([type]): [description]
    #     """
        # return [obj]
        # return [obj]

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


class Navigator(object):
    """ navigator """

    # Determines whether cookies are enabled in the browser
    cookieEnabled = False

    # Determines whether the browser is online
    onLine = False

    # Returns the name of the browser Navigator
    appName = "domonic"

    def __init__(self, *args, **kwargs):
        # self.args = args
        # self.kwargs = kwargs
        pass

    # @property
    # def appVersion():
        """ Returns the version information of the browser """
        # from domonic import __version__
        # return __version__

    # @property
    # def language():
        """ Returns the language of the browser Navigator """
        # import locale
        # return locale.getdefaultlocale()

    # platform  Returns for which platform the browser is compiled  Navigator
    # product   Returns the engine name of the browser  Navigator
    # userAgent Returns the user-agent header sent by the browser to the server Navigator
    # geolocation   Returns a Geolocation object that can be used to locate the user's position Navigator
    # appCodeName   Returns the code name of the browser    Navigator


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
            base (int): [An integer in the range 2 through 36 specifying the base to use for representing numeric values.]

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

    def __init__(self, x="", *args, **kwargs):
        # self.args = args
        # self.kwargs = kwargs
        self.x = str(x)

    def __str__(self):
        return self.x

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

    def split(self, expr):
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

    def concat(self, *args, seperator=""):
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
    def charCodeAt(self, index: int):
        """ Returns the Unicode of the character at the specified index """
        return ord(self.x[index])

    # @staticmethod
    def fromCharCode(self, *codes):
        """ returns a string created from the specified sequence of UTF-16 code units """
        return "".join([str(chr(x)) for x in codes])

    @property
    def length(self):
        return len(self.x)

    def repeat(self, count: int):
        """ Returns a new string with a specified number of copies of an existing string """
        return self.x * count

    def startsWith(self, x: str, start: int = None, end: int = None):
        """ Checks whether a string begins with specified characters """
        if start is None:
            start = 0
        if end is None:
            end = len(x)
        # print(self.x.startswith(x, start, end))
        return self.x.startswith(x, start, end)

    def substring(self, start: int, end: int = None):
        """ Extracts the characters from a string, between two specified indices """
        if start < 0:
            start = 0
        if end is None:
            end = len(self.x)
        return self.x[start:end]

    def endsWith(self, x: str, start: int = None, end: int = None):
        """ Checks whether a string ends with specified string/characters """
        if start is None:
            start = 0
        if end is None:
            end = len(x)
        return self.x.endswith(x, start, end)

    def toLowerCase(self):
        """ Converts a string to lowercase letters """
        return self.x.lower()

    def toUpperCase(self):
        """ Converts a string to uppercase letters """
        return self.x.upper()

    def slice(self, start: int = 0, end: int = None):
        """ Selects a part of an string, and returns the new string """
        if end is None:
            end = len(self.x)
        return self.x[start:end]

    def trim(self):
        """ Removes whitespace from both ends of a string """
        return self.x.strip()

    def charAt(self, index: int):
        """[Returns the character at the specified index (position)]

        Args:
            index (int): [index position]

        Returns:
            [str]: [character]
        """
        return self.x[index]

    def replace(self, old: str, new: str):
        """
        Searches a string for a specified value, or a regular expression,
        and returns a new string where the specified values are replaced.
        only replaces first one.
        """
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

    def toLocaleLowerCase(self):
        """ Converts a string to lowercase letters, according to the host's locale """
        # locale.setlocale()
        return self.x.lower()

    def toLocaleUpperCase(self):
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


class RegExp():

    def __init__(self, expression):
        self.expression = expression
        # self.flag  #: A string that contains the flags of the RegExp object.
        # self.dotAll  #: Whether . matches newlines or not.
        # self.global # Whether to test the regular expression against all possible matches in a string, or only against the first.
        # self.hasIndices  # Whether the regular expression result exposes the start and end indices of captured substrings.
        # self.ignoreCase  # Whether to ignore case while attempting a match in a string.
        # self.multiline  # Whether or not to search in strings across multiple lines.
        # self.source  # The text of the pattern.
        # self.sticky  # Whether or not the search is sticky.
        # self.unicode  # Whether or not Unicode features are enabled.
        # self.lastIndex  # The index at which to start the next match.

    def compile(self):
        """ (Re-)compiles a regular expression during execution of a script. """
        pass

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
        """" Returns a string representing the specified object. Overrides the Object.prototype.toString() method. """
        pass

    def __str__(self):
        """" Returns a string representing the specified object. Overrides the Object.prototype.toString() method. """
        pass

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


# https://developer.mozilla.org/en-US/docs/Web/API/URL

class URL(object):
    """ a-tag extends from URL """

    def __update__(self):
        # print( "update URL:", type(self), self  )
        try:
            # make obj with all old props
            new = {}
            new['protocol'] = self.url.scheme
            new['hostname'] = self.url.hostname
            new['href'] = self.url.geturl()
            new['port'] = self.url.port
            new['host'] = ''  # self.url.hostname
            new['pathname'] = self.url.path
            new['hash'] = ''  # self.url.hash
            new['search'] = ''  # self.url.hash

            # update it with all the new ones
            new = {}
            new['protocol'] = self.protocol
            new['hostname'] = self.hostname
            new['href'] = self.href
            new['port'] = self.port
            new['host'] = self.host
            new['pathname'] = self.pathname
            new['hash'] = self.hash  # self.hash
            new['search'] = self.search  # self.url.query
            new['_searchParams'] = self._searchParams  # URLSearchParams(self.url.query)
            # NOTE - rebuild happening here
            self.url = urllib.parse.urlsplit(
                new['protocol'] + "://" + new['host'] + new['pathname'] + new['hash'] + new['search'])

            self.href = self.url.geturl()

        except Exception:  # as e:
            # print('fails on props called by init as they dont exist yet')
            # print(e)
            pass

    def __init__(self, url: str = "", *args, **kwargs):  # TODO - relative to
        """URL

        builds a url

        Args:
            url (str): a url
        """
        self.url = urllib.parse.urlsplit(url)
        self.href = url  # self.url.geturl()
        self.protocol = self.url.scheme
        self.hostname = self.url.hostname
        self.port = self.url.port
        self.host = self.url.hostname
        self.pathname = self.url.path
        self.hash = ''
        self.search = self.url.query
        self._searchParams = URLSearchParams(self.url.query)

    @property
    def searchParams(self):
        return self._searchParams.toString()

    def toString(self):
        return str(self.href)

    # def toJson

    # @property
    # def href(self):
    # TODO - check js vs tag. does js version remove query?. if so detect self.
    #     return self.href

    # @href.setter
    # def href(self, href:str):
    #     self.url = href
    #     self.href = href

    @property
    def protocol(self):
        return self.__protocol

    @protocol.setter
    def protocol(self, p: str):
        self.__protocol = p
        # if self.ready : self.__update__() # TODO - this instead of silent err?
        self.__update__()

    @property
    def hostname(self):
        return self.__hostname

    @hostname.setter
    def hostname(self, h: str):
        if h is None:
            return
        if ":" in h:
            h = h.split(':')[0]
        self.__hostname = h
        self.__update__()

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, p: str):
        self.__port = p
        self.__update__()

    @property
    def host(self):
        if self.port is not None:
            return self.hostname + ":" + str(self.port)
        else:
            return self.hostname

    @host.setter
    def host(self, h: str):
        if h is None:
            return
        p = self.port
        if ":" in h:
            p = int(h.split(':')[1])
            h = h.split(':')[0]
        self.__host = h
        self.hostname = h
        self.port = p
        self.__update__()

    @property
    def pathname(self):
        return self.__pathname

    @pathname.setter
    def pathname(self, p: str):
        self.__pathname = p
        self.__update__()

    @property
    def hash(self):
        """" hash Sets or returns the anchor part (#) of a URL """
        if '#' in self.href:
            return '#' + self.href.split('#')[1]
        # return ''
        return self.__hash

    @hash.setter
    def hash(self, h: str):
        self.__hash = h
        self.__update__()

    # @property
    # def origin(self):
        '''# origin    Returns the protocol, hostname and port number of a URL Location'''

    def __str__(self):
        return str(self.href)

    # NOTE - node -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    # @staticmethod
    # def domainToASCII(domain: str):
    #     """[It returns the Punycode ASCII serialization of the domain.
    #     If domain is an invalid domain, the empty string is returned.]

    #     Args:
    #         domain (str): [description]
    #     """
    #     pass

    # @staticmethod
    # def domainToUnicode(domain: str):
    #     """[returns the Unicode serialization of the domain.
    #     If the domain is invalid, the empty string is returned]

    #     Args:
    #         domain (str): [description]
    #     """
    #     pass

    # @staticmethod
    # def fileURLToPath(url: str):
    #     """[summary]

    #     Args:
    #         url (str): [description]
    #     """
    #     pass

    # @staticmethod
    # def format(URL, options):
    #     """[summary]

    #     Args:
    #         URL ([type]): [description]
    #         options ([type]): [description]
    #     """
    #     pass

    # @staticmethod
    # def pathToFileURL(path: str):
    #     """[summary]

    #     Args:
    #         path (str): [description]
    #     """
    #     pass

    # @staticmethod
    # def urlToHttpOptions(url: str):
    #     """[summary]

    #     Args:
    #         url (str): [description]
    #     """
    #     pass


class URLSearchParams:
    """[utility methods to work with the query string of a URL]

        created with help of https://6b.eleuther.ai/

    """

    def __init__(self, paramString):  # , **paramsObj):
        """[Returns a URLSearchParams object instance.]

        Args:
            paramString ([type]): [ i.e. q=URLUtils.searchParams&topic=api]
        """
        # TODO - escape
        # import ast
        # TODO - dont think i can do this cant urls params have duplicate keys?
        # self.params = ast.literal_eval(paramString)
        if isinstance(paramString, str):
            if paramString.startswith('?'):
                paramString = paramString[1:len(paramString)]

            import urllib
            self.params = urllib.parse.parse_qs(paramString)
        elif hasattr(paramString, '__iter__'):
            self.params = [item for sublist in paramString for item in sublist]
        elif isinstance(paramString, dict):
            self.params = dict([(key, item) for key, item in paramString.iteritems()])
        else:
            raise TypeError("Malformed paramString.  Must be a string or a dict with dict like items. Got: %s" % paramString)

    def __iter__(self):
        for attr in self.params.items():  # dir(self.params.items()):
            # if not attr.startswith("__"):
            yield attr

    def append(self, key, value):
        """ Appends a specified key/value pair as a new search parameter """
        # TODO - ordereddict?
        self.params[key].append(value)  # [key]=value

    def delete(self, key):
        """ Deletes the given search parameter, and its associated value, from the list of all search parameters. """
        del self.params[key]

    def has(self, key):
        """ Returns a Boolean indicating if such a given parameter exists. """
        return key in self.params

    def entries(self):
        """ Returns an iterator allowing iteration through all key/value pairs contained in this object. """
        return self.params.items()

    def forEach(self, func):
        """ Allows iteration through all values contained in this object via a callback function. """
        for key, value in self.params.items():
            func(key, value)

    def keys(self):
        """ Returns an iterator allowing iteration through all keys of the key/value pairs contained in this object. """
        return self.params.keys()

    def get(self, key):
        """ Returns the first value associated with the given search parameter. """
        try:
            return self.params.get(key, None)[0]
        except Exception:
            return None

    def sort(self):
        """ Sorts all key/value pairs, if any, by their keys. """
        self.params.sort()

    def values(self):
        """ Returns an iterator allowing iteration through all values of the key/value pairs contained in this object. """
        return self.params.values()

    def toString(self):
        """ Returns a string containing a query string suitable for use in a URL. """
        # return '&'.join([str(x) for x in self.params])
        return urllib.parse.urlencode(self.params, doseq=True)
        # return str(self.params)

    def set(self, key, value):
        """ Sets the value associated with a given search parameter to the given value.
        If there are several values, the others are deleted. """
        self.params[key] = (value)

    def getAll(self, key):
        """ Returns all the values associated with a given search parameter. """
        return self.params.get(key)

    def __str__(self):
        return urllib.parse.urlencode(self.params, doseq=True)


# TODO - test
class Error(Exception):
    ''' Raise Errors '''
    def __init__(self, message, *args, **kwargs):
        self.message = message
        super(Error, self).__init__(message)
    # def __str__(self):
    #     return self.message


'''

# BELOW is legacy data from a dump of ALL dom/js methods. was looking for useful things to port back when this was the only class.
# -- leave here for now - ill delete stuff later. it reminds me what i haven't covered


# class ClipboardData():
    # clipboardData Returns an object containing the data affected by the clipboard operation
    # def __init__():
        # pass

# class History():
    # def __init__():
        # pass
    # def back():
    #     """ Loads the previous URL in the history list """
    #     raise NotImplementedError
    # def forward():
    #     """ Loads the next URL in the history list """
    #     raise NotImplementedError
    # def go():
    #     """ Loads a specific URL from the history list """
    #     raise NotImplementedError

# class Storage():
    # def __init__():
        # pass
    # def setItem(self):
        # """ Adds that key to the storage, or update that key's value if it already exists """
        # raise NotImplementedError
    # def key():
    #     """ Returns the name of the nth key in the storage """
    #     raise NotImplementedError
    # def removeItem():
    #     """  Removes that key from the storage """
    #     raise NotImplementedError

# class Geolocation():
    # def __init__():
        # pass
    def clearWatch():
    """  Unregister location/error monitoring handlers previously installed using Geolocation.watchPosition()    """
    def coordinates   Returns:
    """ the position and altitude of the device on Earth    """
    def getCurrentPosition():
    """  Returns the current position of the device  """
    def position  Returns:
    """ the position of the concerned device at a given time    """
    def positionError Returns:
    """ the reason of an error occurring when using the geolocating device  """
    def positionOptions   Describes:
    """ an object containing option properties to pass as a parameter of Geolocation.getCurrentPosition() and Geolocation.watchPosition() """
    def watchPosition():
    """   Returns a watch ID value that then can be used to unregister the handler by passing it to the Geolocation.clearWatch() method   """

# clear()   Clears the console  Console, Storage
# debugger  Stops the execution of JavaScript, and calls (if available) the debugging function  Statements
# elapsedTime   Returns the number of seconds a transition has been running
# error()   Outputs an error message to the console Console
# getItem() Returns the value of the specified key name Storage
# getNamedItem()    Returns a specified attribute node from a NamedNodeMap  Attribute
# item()    Returns the attribute node at a specified index in a NamedNodeMap   Attribute, HTMLCollection
# namedItem()   Returns the element with the specified ID, or name, in an HTMLCollection    HTMLCollection
# removeNamedItem() Removes a specified attribute node  Attribute
# setNamedItem()    Sets the specified attribute node (by name) Attribute
# specified Returns true if the attribute has been specified, otherwise it returns false    Attribute

'''
