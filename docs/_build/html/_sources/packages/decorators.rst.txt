decorators
======================

Everyone loves python decorators

We have a few in domonic to make life more fun!


el
--------------------------------

You can use the el decorator to wrap elements around function results.

.. code-block :: bash

    from domonic.decorators import el

    @el(html, True)
    @el(body)
    @el(div)
    def test():
        return 'hi!'

    print(test())
    # <html><body><div>hi!</div></body></html>

    # returns pyml objects so call str to render
    assert str(test()) == '<html><body><div>hi!</div></body></html>'


It returns the tag object by default. 

You can pass True as a second param to the decorator to return a rendered string instead. Also accepts strings as first param i.e. custom tags.


silence
--------------------------------

Want that unit test to stfu?

.. code-block :: bash

    from domonic.decorators import silence

    @silence
    def test_that_wont_pass():
        assert True == False


called
--------------------------------

Python's lambda restrictions may force you to create anonymous success methods above calling functions.

domonic uses a unique type of decorator to call anonymouse methods immediately after calling the passed method.

To use it, pass 2 functions, something to call BEFORE hand, and an error method

Then your decorated anonymous function will recieve the data of the first function you passed in as a parameter.

Let me show you...

.. code-block :: bash

    from domonic.decorators import called

    @called(
        lambda: º.ajax('https://www.google.com'),
        lambda err: print('error:', err))
    def success(data=None):
        print("Sweet as a Nut!")
        print(data.text)


It's meant for anonymous functions and calls immediately. So don't go using it on class methods.

It's also called iffe. (so you can know when ur just passing nothing)

.. code-block :: bash

    @iife()
    def sup():
        print("sup!")
        return True


check
--------------------------------

logs the entry and exit of a function and is useful for debugging. i.e.

.. code-block :: bash

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
