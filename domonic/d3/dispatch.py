"""
domonic.d3.dispatch
===================================

"""

from domonic.javascript import Array, Object, RegExp, String

noop = {"value": lambda *args: {}}
_MISSING = object()


def dispatch(*args):
    _ = {}
    for arg in args:
        if (not isinstance(arg, str)) or (arg in _) or RegExp(r"[s.]").test(arg):
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
        if t and types.get(t, None) == None:
            raise Exception("unknown type: " + t)
        return {"type": t, "name": name}

    return Array(String(typenames).trim().split()).map(anon)


class Dispatch:
    def __init__(self, _) -> None:
        self._ = _

    def on(self, typename: str, callback=_MISSING, *args):
        _ = self._
        T = parseTypenames(str(typename), _)

        # If no callback was specified, return the callback of the given type and name.
        if callback is _MISSING:
            for typename in T:
                if not typename["type"]:
                    continue
                t = self.get(_[typename["type"]], typename["name"])
                if t is not None:
                    return t
            return None

        # If a type was specified, set the callback for the given type and name.
        # Otherwise, if a None callback was specified, remove callbacks of the given name.
        if callback != None and not callable(callback):
            raise Exception("invalid callback: " + callback)
        for typename in T:
            if typename["type"] is not None:
                _[typename["type"]] = self.set(
                    _[typename["type"]], typename["name"], callback
                )
            elif callback == None:
                for t in _:
                    _[t] = self.set(_[t], typename["name"], None)

        return self

    def copy(self):
        copy = {}
        _ = self._
        for t in _:
            copy[t] = Array(_[t]).slice()
        return Dispatch(copy)

    def call(self, type, that=None, *args):
        if not Object(self._).hasOwnProperty(type):
            raise Exception("unknown type: " + type)

        t = self._[type]
        for i in t:
            i["value"](*args)

    def apply(self, type, that, *args):
        if not Object(self._).hasOwnProperty(type):
            raise Exception("unknown type: " + type)
        t = self._[type]
        for i in t:
            i["value"](*args)

    def get(self, type, name):
        n = len(type)
        for i in range(0, n):
            c = type[i]
            if c["name"] == name:
                return c["value"]

    def set(self, type, name, callback):
        for i, t in enumerate(type):
            if t["name"] == name:
                t = noop
                type = Array(Array(type).slice(0, i)).concat(Array(type).slice(i + 1))
                if type is None:
                    type = []
                break

        if callback != None:
            type.append({"name": name, "value": callback})

        return type
