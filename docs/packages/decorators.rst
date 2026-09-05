decorators
======================

.. meta::
   :description: Python decorators for domonic HTML rendering, element wrapping, debugging, immediate callbacks, JSON responses, and utility functions.
   :keywords: Python decorators, HTML decorator, render decorator, domonic decorators, JSON decorator, callback decorator

Everyone loves Python decorators.

domonic includes a few decorators to make rendering and debugging more convenient.


el
--------------------------------

You can use the el decorator to wrap elements around function results.

.. code-block :: python

    from domonic.decorators import el
    from domonic.html import html, body, div

    @el(html)
    @el(body)
    @el(div)
    def test():
        return 'hi!'

    result = test()
    print(type(result))  # <class 'domonic.html.html'> -- a PyML tag object
    print(result)         # <html><body><div>hi!</div></body></html>
    assert str(result) == '<html><body><div>hi!</div></body></html>'


It returns the tag object by default. Pass ``True`` as the second parameter to
the outermost ``el`` to get a rendered string back instead:

.. code-block :: python

    @el(html, True)
    @el(body)
    @el(div)
    def test_string():
        return 'hi!'

    result = test_string()
    print(type(result))  # <class 'str'>
    print(result)         # <html><body><div>hi!</div></body></html>

The first parameter can also be a string for custom tags.


silence
--------------------------------

Want to silence a function's ``print()`` output while testing?
``silence`` redirects ``stdout`` for the duration of the call -- it does not
suppress exceptions, only printed output.

.. code-block :: python

    from domonic.decorators import silence

    @silence
    def noisy():
        print("this will not be printed")
        return 42

    result = noisy()
    print(result)
    # 42


called
--------------------------------

Python's lambda restrictions can force you to define success callbacks above the functions that use them.

domonic has a decorator that calls a setup function first, then passes that result into the decorated callback.

To use it, pass two functions: a setup function and an error handler.

The decorated function receives the setup function's result as its first argument.

For example:

.. code-block :: python

    from domonic.decorators import called

    @called(
        lambda: {"value": 42},
        lambda err: print("error:", err))
    def success(data=None):
        print("Sweet as a Nut!")
        print(data["value"])
    # Sweet as a Nut!
    # 42

The setup function could just as easily be an Ajax call, e.g.
``lambda: º.ajax("https://example.com/api")`` from :doc:`dQuery`.


It is intended for immediate callbacks, not class methods.

It is also aliased as ``iife`` for immediately invoked function expressions.

.. code-block :: python

    from domonic.decorators import iife

    @iife()
    def sup():
        print("sup!")
        return True
    # sup!


check
--------------------------------

``check`` logs the entry and exit of a function through Python's ``logging``
module (not ``print()``), so it's useful for debugging without needing to
strip print statements later. Configure logging to see it on the console:

.. code-block :: python

    import logging
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    from domonic.decorators import check

    @check
    def somefunc():
        return True

    somefunc()

    # outputs this to the console
    # Entering somefunc
    # Exited somefunc



.. autoclass:: domonic.decorators
    :members:
    :noindex:
