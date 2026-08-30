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

    @el(html, True)
    @el(body)
    @el(div)
    def test():
        return 'hi!'

    print(test())
    # <html><body><div>hi!</div></body></html>

    # Returns PyML objects, so call str to render.
    assert str(test()) == '<html><body><div>hi!</div></body></html>'


It returns the tag object by default.

Pass ``True`` as the second parameter to return a rendered string instead. The first parameter can also be a string for custom tags.


silence
--------------------------------

Want to silence a noisy function while testing?

.. code-block :: python

    from domonic.decorators import silence

    @silence
    def test_that_wont_pass():
        assert True is False


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
        lambda: º.ajax('https://www.google.com'),
        lambda err: print('error:', err))
    def success(data=None):
        print("Sweet as a Nut!")
        print(data.text)


It is intended for immediate callbacks, not class methods.

It is also aliased as ``iife`` for immediately invoked function expressions.

.. code-block :: python

    @iife()
    def sup():
        print("sup!")
        return True


check
--------------------------------

``check`` logs the entry and exit of a function and is useful for debugging.

.. code-block :: python

    @check
    def somefunc():
        return True

    somefunc()

    # would output this to the console
    # Entering somefunc
    # Exited somefunc



.. autoclass:: domonic.decorators
    :members:
    :noindex:
