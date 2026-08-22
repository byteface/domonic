"""
domonic.decorators
====================================

"""

import functools
import inspect
import io
import logging
import warnings
from typing import Callable


def _invoke_before(before, function):
    result = before()
    params = list(inspect.signature(function).parameters.values())
    can_receive_value = any(
        param.kind
        in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
        for param in params
    ) or any(param.kind == inspect.Parameter.VAR_POSITIONAL for param in params)
    return result, can_receive_value


def el(element="div", string: bool = False):
    """[wraps the results of a function in an element]"""

    return_string = string or isinstance(element, str)

    if isinstance(element, str):
        from domonic.dom import Document

        element = Document.createElement(element).__class__

    def decorator(function):
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            if result is None:
                result = ""
            if return_string is False:
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
    """Call a hook before a function runs, with light support for legacy callback sugar."""

    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            if before:
                _, _ = _invoke_before(before, f)
            try:
                return f(*args, **kwargs)
            except Exception as e:
                if error:
                    error(e)
                raise

        if before is None:
            wrapper()
            return wrapper

        params = inspect.signature(f).parameters
        if params:
            try:
                result, can_receive_value = _invoke_before(before, f)
                if can_receive_value:
                    f(result)
                else:
                    f()
            except Exception as e:
                if error:
                    error(e)
                else:
                    raise

        return wrapper

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
        if len(types) != f.__code__.co_argcount:
            raise AssertionError(
                "accepts decorator argument count must match function argument count"
            )

        def new_f(*args, **kwds):
            for a, t in zip(args, types):
                if not isinstance(a, t):
                    raise AssertionError("arg %r does not match %s" % (a, t))
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
    """Suppress stdout for the wrapped function.

    Supports both ``@silence`` and ``@silence()``.
    """

    def decorator(f):
        @functools.wraps(f)
        def wrapper(*f_args, **f_kwargs):
            import contextlib

            with contextlib.redirect_stdout(io.StringIO()):
                return f(*f_args, **f_kwargs)

        return wrapper

    if args and callable(args[0]) and len(args) == 1 and not kwargs:
        return decorator(args[0])
    return decorator


def check(f):
    """Log entry and exit around a function call."""

    logger = logging.getLogger(__name__)

    @functools.wraps(f)
    def new_f(*args, **kwargs):
        logger.info("Entering %s", f.__name__)
        result = f(*args, **kwargs)
        logger.info("Exited %s", f.__name__)
        return result

    return new_f


def log(logger, level="info"):
    """@log(logging.getLogger('main'), level='warning')"""

    def log_decorator(fn):
        @functools.wraps(fn)
        def wrapper(*a, **kwa):
            getattr(logger, level)(fn.__name__)
            return fn(*a, **kwa)

        return wrapper

    return log_decorator


def instead(somethingelse):
    """Return a fallback value when the wrapped function raises."""

    def decorator(f):
        @functools.wraps(f)
        def new_f(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception:
                return somethingelse

        return new_f

    return decorator


def deprecated(func):
    """
    marks a function as deprecated.
    """

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        raise Warning("Call to deprecated function {}.".format(func.__name__))
        return func(*args, **kwargs)

    return new_func


def as_json(func):
    """decorate any function to return json instead of a python obj
    note - used by JSON.py
    """

    def JSON_decorator(*args, **kwargs):
        import json

        return json.dumps(func(*args, **kwargs))

    return JSON_decorator


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


"""
import functools

# def DIV(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         result = func(*args, **kwargs)
#         return div(result)
#     return wrapper

# Create dynamic decorators for each tag
def create_html_decorator(tag):
    def decorator(func=None, **kwargs):
        # If no function is provided, we have been called with keyword arguments
        if func is None:
            return functools.partial(decorator, **kwargs)

        # Convert underscores in attributes to valid HTML (e.g., _class to class)
        updated_kwargs = {key.lstrip('_'): value for key, value in kwargs.items()}

        # Define the wrapper function that is called when the decorated function is called
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Call the original function to get the content
            content = func(*args, **kwargs)

            # Generate attributes for the HTML tag
            attrs = ''
            for key, value in updated_kwargs.items():
                attrs += f' {key}="{value}"'

            # Return the HTML wrapped content
            return f"<{tag}{attrs}>{content}</{tag}>"

        return wrapper

    return decorator


# from domonic.html import html_tags -- circular reference

# Dynamically create decorators for all HTML tags
for tag in html_tags:
    globals()[tag.upper()] = create_html_decorator(tag)


# @DIV(_id="cool", _class"awesome")
# @SPAN
# def somecontent():
#     return 'content only'
"""
