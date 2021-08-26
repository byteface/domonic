"""
    domonic.d3.queue
    ====================================

    # TODO - completely untested

"""

# import {slice} from "./array";
from domonic.javascript import *


noabort = {}


class Queue():

    def __init__(self, size):
        self._size = size
        self._call = None
        self._error = None
        self._tasks = []
        self._data = []
        self._waiting = None
        self._active = None
        self._ended = None
        self._start = 0  # inside a synchronous task callback?

    def defer(self, callback, *args):
        if not type(callback, callable):
            raise Error("invalid callback")
        if (self._call):
            raise Error("defer after await")
        if (self._error != None):
            return self

        t = slice.call(args, 1)
        t.append(callback)
        self._waiting += 1
        self._tasks.append(t)
        poke(self)
        return self

    def abort(self):
        if self._error == None:
            abort(self, Error("abort"))
        return self

    def await(self, callback):
        if not type(callback, callable):
            raise Error("invalid callback")
        if (self._call):
            raise Error("multiple await")

        def _call(error, results):
            callback.apply(None, [error].concat(results))

        self._call = _call

        maybeNotify(self)
        return self

    def awaitAll(self, callback):
        if not type(callback, callable):
            raise Error("invalid callback")
        if (self._call):
            raise Error("multiple await")
        self._call = callback
        maybeNotify(self)
        return self


def poke(q):
    if not q._start:
        try:
            start(q)  # let the current task complete
        except Exception as e:
            if (q._tasks[q._ended + q._active - 1]):
                abort(q, e)  # task errored synchronously
            elif not q._data:
                raise e  # await callback errored synchronously


def start(q):
    q._start = q._waiting
    while (q._start and q._active < q._size):
        i = q._ended + q._active
        t = q._tasks[i]
        j = len(t) - 1
        c = t[j]
        t[j] = end(q, i)
        q._waiting -= 1
        q._active += 1
        t = c.apply(None, t)
        if not q._tasks[i]:
            continue  # task finished synchronously
        q._tasks[i] = t or noabort


def end(q, i):

    def _end(e, r):
        nonlocal q
        nonlocal i
        if not q._tasks[i]:
            return  # ignore multiple callbacks
        q._active -= 1
        q._ended += 1
        q._tasks[i] = None
        if q._error != None:
            return  # ignore secondary errors
        if e != None:
            abort(q, e)
        else:
            q._data[i] = r
            if q._waiting:
                poke(q)
            else:
                maybeNotify(q)

    return _end


def abort(q, e):
    i = len(q._tasks)
    q._error = e  # ignore active callbacks
    q._data = None  # allow gc
    q._waiting = None  # prevent starting

    while i >= 0:
        t = q._tasks[i]
        if t:
            q._tasks[i] = None
        if t.abort:
            try:
                t.abort()
            except Exception as e:
                pass
        i -= 1
    q._active = None  # allow notification
    maybeNotify(q)


def maybeNotify(q):
    if not q._active and q._call:
        d = q._data
        q._data = None  # allow gc
        q._call(q._error, d)


def queue(concurrency):
    if concurrency is None:
        concurrency = Infinity
    elif not (concurrency >= 1):
        raise Error("invalid concurrency")
    return Queue(concurrency)