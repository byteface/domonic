"""
    domonic.decorators
    ====================================

"""

import functools
from functools import wraps

# wrap whats returned in an element
# def el(element):
#     def wrap(f):
#         return f()
#     return wrap

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


def cash(func, currency="£"):
    @wraps(func)
    def wrapper(*args, **kwargs):
        r = func(*args, **kwargs)
        formatted = currency + '{:.2f}'.format(r)
        return formatted
    return wrapper
# @cash("12.1")


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