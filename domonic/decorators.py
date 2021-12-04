"""
    domonic.decorators
    ====================================

"""

from typing import Callable
import warnings
import functools
from functools import wraps


def el(element='div', string: bool = False):
    """[wraps the results of a function in an element]"""

    if isinstance(element, str):
        from domonic.dom import Document
        element = Document.createElement(element).__class__

    def decorator(function):
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            if string == False:
                return element(result)
            else:
                return str(element(result))
        return wrapper
    return decorator
# @el(div)
# @el(span)

# def doctype(doctype):
#     """
#     @doctype('html')
#     @doctype('xhtml')
#     @doctype('xml')
#     """
#     def decorator(f):
#         @wraps(f)
#         def wrapper(*args, **kwargs):
#             return f(*args, **kwargs)
#         return wrapper
#     return decorator


def called(before=None, error: Callable[[Exception], None] = None):
    """
    Decorator to call a function before and after a function call.
    """
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            if before:
                before()
            try:
                return f(*args, **kwargs)
            except Exception as e:
                if error:
                    error(e)
                else:
                    raise
            finally:
                if before:
                    before()
        return wrapper
    return decorator
    """[calls before() passing the response as args to the decorated function.
        optional error handler. run the decorated function immediately.

        WARNING: this is not for the regular decorating of a function
        its syntactical sugar for a callback i.e.

        @called(
            lambda: º.ajax('https://www.google.com'),
            lambda err: print('error:', err))
        def success(data=None):
            print("sweet!")
            print(data)

        """
    def decorator(function):
        nonlocal before
        nonlocal error
        try:
            if before is None:
                return function()
            r = before()
            return function(r)
        except Exception as e:
            if error is not None:
                error(e)
            else:
                raise e

    return decorator


iife = called  # pass None for an iife

# def static(endpoint, update="11101"):
#     '''
#     render the endpoint to a cron timestamp. when user vists that function.
#     it will load the rendered version instead of executing the function.
#     '''
#     def dont_do_it(f):
#         return None
#     return dont_do_it


# https://www.python.org/dev/peps/pep-0318/
# https://stackoverflow.com/questions/15299878/how-to-use-python-decorators-to-check-function-arguments
def accepts(*types):
    def check_accepts(f):
        assert len(types) == f.__code__.co_argcount

        def new_f(*args, **kwds):
            for (a, t) in zip(args, types):
                assert isinstance(a, t), \
                       "arg %r does not match %s" % (a, t)
            return f(*args, **kwds)
        new_f.__name__ = f.__name__
        return new_f
    return check_accepts
# @accepts(int)


# CACHED = {}
# def memoize(f):
#     """
#     @memoize
#     def fib(n):
#         if n in (0, 1):
#             return n
#         return fib(n - 1) + fib(n - 2)
#     """
#     @functools.wraps(f)
#     def new_f(*args):
#         if args in CACHED:
#             return CACHED[args]
#         else:
#             result = f(*args)
#             CACHED[args] = result
#             return result
#     return new_f


# def requires_websocket(f): # decorate all functions that require websockets to warn user


def silence(*args, **kwargs):
    """ stop a function from doing anything """
    def dont_do_it(f):
        return None
    return dont_do_it
# @silence


def check(f):
    """ Prints entry and exit of a function to the console """
    def new_f(*args, **kwargs):
        print("Entering", f.__name__)
        f(*args, **kwargs)
        print("Exited", f.__name__)
    return new_f
# @check()


def log(logger, level='info'):
    """ @log(logging.getLogger('main'), level='warning') """
    def log_decorator(fn):
        @functools.wraps(fn)
        def wrapper(*a, **kwa):
            getattr(logger, level)(fn.__name__)
            return fn(*a, **kwa)
        return wrapper
    return log_decorator


def instead(f, somethingelse):
    """ what to return if it fails """
    def new_f():
        try:
            return f()
        except Exception as e:
            print('failed', e)
        return somethingelse
    return new_f
# @instead("something else instead of what was supposed to happen")


def deprecated(func):
    """
    marks a function as deprecated.
    """
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)
        warnings.warn("Call to deprecated function {}.".format(func.__name__), category=DeprecationWarning, stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning)
        return func(*args, **kwargs)
    return new_func


def as_json(func):
    """ decorate any function to return json instead of a python obj
        note - used by JSON.py
    """
    def JSON_decorator(*args, **kwargs):
        import json
        return json.dumps(func(*args, **kwargs))
    return JSON_decorator

# def evt(event, *args, **kwargs):  #TODO
#     """
#     a decorator that will call a function when an event is triggered.
#     """
#     def decorator(f):
#         def wrapper(*args, **kwargs):
#             return f(*args, **kwargs)
#         return wrapper
    # return decorator
# @evt('event', 'args', 'kwargs')


# def catch(f):
#     """ catch exceptions and return None """
#     def new_f():
#         try:
#             return f()
#         except Exception as e:
#             print('failed', e)
#             return None
#     return new_f


# def lenient(*args, **kwargs):
# """ can try to remap args if passed incorrectly.
    # i.e. if expecting array but gets string, puts string in arr
    # should never switch order probably. just re-type
    # prints warning and runs
# """

'''
def aka(names):
    """ @aka(*mylist) """
    def aka_decorator(fn):
        @functools.wraps(fn)
        def wrapper(*a, **kwa):
            return fn(*a, **kwa)
        return wrapper
    return log_decorator
'''
