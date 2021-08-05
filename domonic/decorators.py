"""
    domonic.decorators
    ====================================

"""

import warnings
import functools
from functools import wraps


def el(element='div', string=False):
    """[wraps the results of a function in an element]"""

    if isinstance(element, str):
        # tag = __import__('domonic.html.' + element)
        # print(tag)
        # - TODO - get element by name required on html class
        from domonic.html import tag, tag_init
        from domonic.dom import Element
        element = type(element, (tag, Element), {'name': element, '__init__': tag_init})

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


def called(before=None, error=None):
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


def silence(*args, **kwargs):
    """ stop a function from doing anything """
    def dont_do_it(f):
        return None
    return dont_do_it
# @silence


def check(f):
    """ logs entry and exit of a function """
    def new_f():
        print("Entering", f.__name__)
        f()
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
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)  # turn off filter
        warnings.warn("Call to deprecated function {}.".format(func.__name__),
                      category=DeprecationWarning,
                      stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning)  # reset filter
        return func(*args, **kwargs)
    return new_func
# considered this a few times


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
