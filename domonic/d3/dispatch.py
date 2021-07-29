"""
    domonic.d3
    ===================================

"""

from domonic.javascript import Array, String, RegExp, Object, Function

noop = {"value": lambda *args: {}}


def dispatch(*args):
    _ = {}
    for arg in args:
        if ((not isinstance(arg, str)) or (arg in _) or RegExp(r'[s.]').test(arg)):
            raise Exception("illegal type: " + arg)
        _[arg] = []
    return Dispatch(_)


def parseTypenames(typenames, types):

    def anon(t):
        name = ""
        i = String(t).indexOf(".")
        if i >= 0:
            name = String(t).slice(i + 1)
            t = String(t).slice(0, i)
        if types.get(t, None) == None:
            raise Exception("unknown type: " + t)
        return {"type": t, "name": name}

    import re
    return Array(re.split(r'/^|\s+/', String(typenames).trim())).map(anon)


class Dispatch():

    def __init__(self, _):
        self._ = _

    def on(self, typename, callback=None, *args):
        _ = self._
        T = parseTypenames(str(typename), _)
        t = None
        i = -1
        n = len(T)

        # If no callback was specified, return the callback of the given type and name.
        if callback is None:
            while i < n:
                typename = T[i]
                t = self.get(_[typename['type']], typename['name'])
                if t is not None:
                    return t
                i += 1
            return self

        # If a type was specified, set the callback for the given type and name.
        # Otherwise, if a None callback was specified, remove callbacks of the given name.
        if callback != None and not callable(callback):
            raise Exception("invalid callback: " + callback)
        while i < n:
            typename = T[i]
            if typename['type'] is not None:
                _[typename['type']] = self.set(_[typename['type']], typename['name'], callback)
            elif callback == None:
                for t in _:
                    _[typename['type']] = self.set(_[typename['type']], typename['name'], None)
            i += 1

        return self

    def copy(self):
        copy = {}
        _ = self._
        for t in _:
            copy[t] = Array(_[t]).slice()
        return Dispatch(copy)

    def call(self, type, that=None, *args):
        arguments = Array()
        n = len(args)
        if (n - 2) > 0:
            arguments = Array(n)
            for i in range(n):
                arguments[i] = arguments[i + 2]

        if not Object(self._).hasOwnProperty(type):
            raise Exception("unknown type: " + type)

        t = self._[type]
        for i in t:
            Function(i['value']).apply(that, arguments)

    def apply(self, type, that, *args):
        if not self._.hasOwnProperty(type):
            raise Exception("unknown type: " + type)
        t = self._[type]
        for i in t:
            Function(i['value']).apply(that, args)

    def get(self, type, name):
        n = len(type)
        for i in range(0, n):
            c = type[i]
            if c['name'] == name:
                return c['value']

    def set(self, type, name, callback):

        for i, t in enumerate(type):
            if t['name'] == name:
                t = noop
                type = Array(Array(type).slice(0, i)).concat(Array(type).slice(i + 1))
                if type is None:
                    type = []
                break

        if callback != None:
            type.append({"name": name, "value": callback})

        return type
