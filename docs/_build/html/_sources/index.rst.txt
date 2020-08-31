.. domonic documentation master file, created by
   sphinx-quickstart on Mon Aug 31 15:08:04 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Domonic: Generate HTML with Python 3
====================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

-------------------

.. image:: https://pepy.tech/badge/domonic
    :target: https://pepy.tech/project/domonic
    
.. image:: https://img.shields.io/pypi/pyversions/domonic.svg
    :target: https://pypi.org/project/domonic/

.. image:: https://travis-ci.com/byteface/domonic.svg?branch=master
    :target: https://travis-ci.com/byteface/domonic.svg?branch=master

**Domonic** is a HTML library for Python 3.

-------------------

**Domonic contains several main packages:**
(but by no means are any of them complete)

- html : Generate html with python3 😎
- dom : DOM API in python3 😲
- javascript : js API in python3 😳
- terminal : call terminal commands with python3 😱 - NEW (*see at the end*)
- JSON : utils for loading / decorating / transforming


HTML TEMPLATING
----------------

.. code-block :: python

  from domonic import *

    output = render( 
        html(
            head(
                style(),
                script(),
            ),
            body(
                div("hello world"),
                a("this is a link", _href="http://www.somesite.com", _style="font-size:10px;"),
                ol(''.join([f'{li()}' for thing in range(5)])),
                h1("test", _class="test"),
            )
        )
    )

.. code-block :: html

  <html><head><style></style><script></script></head><body><div>hello world</div><a href="http://www.somesite.com" style="font-size:10px;">this is a link</a><ol><li></li><li></li><li></li><li></li><li></li></ol><h1 class="test">test</h1></body></html>



install
----------------
.. code-block :: python

  python3 -m pip install domonic


or if you had it before upgrade:

.. code-block :: python

  python3 -m pip install domonic --upgrade


usage
----------------

::

  print(html(body(h1('Hello, World!'))))

  <html><body><h1>Hello, World!</h1></body></html>



The User Guide
----------------

Here you can find instructions for getting the most out of Domonic.

.. toctree::
   :maxdepth: 2

   packages/html
   packages/dom
   packages/javascript
   packages/JSON
   packages/terminal


Join-in
----------------
Feel free to join in if you find it useful.

If there's any methods you want that are missing or not complete yet. Just update the code and send a pull request.

I'll merge and releaese asap.


EXAMPLE PROJECT
----------------
A browser based file browser. Working example of how components can work:
https://github.com/byteface/Blueberry/

A cron viewer
https://github.com/byteface/ezcron/


disclaimer
----------------
There's several more widely supported libraries doing HTML generation, DOM reading/manipulation, terminal wrappers etc. Maybe use one of those for production due to strictness and support.

This is becoming more of a fast prototyping library.
