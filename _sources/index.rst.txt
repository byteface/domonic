Domonic:
========

.. image:: _static/domonic.jpg
  :width: 696
  :alt: domonic

Generate HTML with Python 3
===========================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

-------------------

.. image:: https://pepy.tech/badge/domonic
    :target: https://pepy.tech/project/domonic
    
.. image:: https://img.shields.io/pypi/pyversions/domonic.svg
    :target: https://pypi.org/project/domonic/

.. image:: https://travis-ci.com/byteface/domonic.svg?branch=master
    :target: https://travis-ci.com/byteface/domonic.svg?branch=master
    
.. image:: https://img.shields.io/pypi/l/domonic.svg
    :target: https://pypi.org/project/domonic/
    :alt: License Badge

.. image:: https://img.shields.io/pypi/wheel/domonic.svg
    :target: https://pypi.org/project/domonic/
    :alt: Wheel Support Badge


**Domonic** Not only a Python library for generating HTML

-------------------

**Domonic contains several evolving packages:**

- html : Generate html with python 3 😎
- dom : DOM API in python 3 😲
- javascript : js API in python 3 😳
- terminal || cmd : call terminal commands with python3 😱 (*see at the end*)
- JSON : utils for loading / decorating / transformin
- SVG : Generate svg using python
- aframe || x3d tags : auto generate 3d worlds with aframe. (see examples folder
- dQuery - Utils for querying domonic. (alt + 0 for the º symbol)
- geom - vec2, vec3 with _dunders_ as well as shape classes

Take a look at the source code and contribute!


HTML TEMPLATING
---------------

.. code-block :: python

  from domonic.html import *

  mydom = html(body(h1('Hello, World!')))
  print(f"{mydom}")

.. code-block :: html

  <!DOCTYPE html>
  <html>
      <body>
          <h1>Hello, World!</h1>
      </body>
  </html>


To pretty print use an f-string. Which also adds the doctype.


install
----------------
.. code-block :: python

  python3 -m pip install domonic


or if you had it before upgrade:

.. code-block :: python

  python3 -m pip install domonic --upgrade


The User Guide
----------------

Here you can find some instructions for getting the most out of Domonic.


.. toctree::
   :maxdepth: 2

   packages/html
   packages/dom
   packages/javascript
   packages/events
   packages/sitemap
   packages/dQuery
   packages/d3
   packages/JSON
   packages/constants
   packages/terminal
   packages/cmd
   packages/tween
   packages/geom
   packages/x3d
   packages/CDN
   packages/decorators
   packages/components
   packages/utils
   packages/webapi
   packages/style
   packages/servers
   packages/autodocs
   contribute

CLI
----------------

There's a few args you can pass to domonic on the command line to help you out.

To launch the docs for a quick reference to the APIs use:

.. code-block :: python

  python3 -m domonic -h


This command will attempt to generate a template from a webpage. (only simple pages for now)

.. code-block :: python

  python3 -m domonic -d http://eventual.technology


Then you can edit/tweak it to get what you need and build new components quicker.


INSTALLING - (linux/mac only)

If you like you can install domonic to your .bashprofile

.. code-block :: python

  python3 -m domonic --install

Now in your terminal whenever you want to start a new project you can type...

.. code-block :: python

  project mycoolproject

and it will smash out a basic project for you.

you can also now access the docs quickly simply by typing...

.. code-block :: python

  domonic -h

Finally, you can open and edit .bashprofile to tweak it to your own preferences.


Join-In
----------------
Feel free to join in if you find it useful.

If there's any methods you want that are missing or not complete yet. Just update the code and send a pull request.

I'll merge and releaese asap.


EXAMPLE PROJECT
----------------
A browser based file browser. Working example of how components can work:
https://github.com/byteface/Blueberry/

A cron viewer:
https://github.com/byteface/ezcron/


Disclaimer
----------------
There's several more widely supported libraries doing HTML generation, DOM reading/manipulation, terminal wrappers etc. Maybe use one of those for production due to strictness and support.

This is becoming more of a fast prototyping library.


----------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
