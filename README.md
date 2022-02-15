<h1 align="center">
    <br>𖤐 domonic 𖤐<br>
    <sup><sub><sup>Generate html with python 3! (and much more)</sup></sub></sup>
    <br>
</h1>

[![PyPI version](https://badge.fury.io/py/domonic.svg)](https://badge.fury.io/py/domonic.svg) 
[![Downloads](https://pepy.tech/badge/domonic)](https://pepy.tech/project/domonic)
[![Python version](https://img.shields.io/pypi/pyversions/domonic.svg?style=flat)](https://img.shields.io/pypi/pyversions/domonic.svg?style=flat)
[![Build status](https://travis-ci.com/byteface/domonic.svg?branch=master)](https://travis-ci.com/byteface/domonic.svg?branch=master)
[![Python package](https://github.com/byteface/domonic/actions/workflows/python-package.yml/badge.svg?branch=master)](https://github.com/byteface/domonic/actions/workflows/python-package.yml)

#### Contains several evolving packages:

- [html](https://domonic.readthedocs.io/_modules/domonic/html.html) : Generate html with python 3 😎
- [dom](https://domonic.readthedocs.io/_modules/domonic/dom.html) : DOM API in python 3 😲
- [javascript](https://domonic.readthedocs.io/_modules/domonic/javascript.html) : js API in python 3 😳 + ([dQuery](https://domonic.readthedocs.io/packages/dQuery.html), [d3](https://domonic.readthedocs.io/packages/d3.html))
- JSON : utils for loading / decorating / transforming
- SVG || mathml || aframe || x3d tags - generators for popular tags
- terminal || cmd : call terminal commands with python3 😱

See the docs/code for more features...
https://domonic.readthedocs.io/

or examples in the [repo...](https://github.com/byteface/domonic/tree/master/examples)

(small footprint. with only a few common lightweight dependencies)

## HTML Templating with Python 3

```python
from domonic.html import *
print(html(body(h1('Hello, World!'))))
# <html><body><h1>Hello, World!</h1></body></html>
```

or to format it and insert the doctype use an f-string:

```python
mydom = html(body(h1('Hello, World!'), a("somelink", _href="somepage.html")))
print(f"{mydom}")
```

```html
<!DOCTYPE html>
<html>
	<body>
		<h1>Hello, World!</h1>
		<a href="somepage.html">somelink</a>
	</body>
</html>
```

### install

```bash
python3 -m pip install domonic
```

or if you had it before upgrade:

```bash
python3 -m pip install domonic --upgrade
```

### attributes

prepend attributes with an underscore ( avoids clashing with python keywords )

```python
test = label(_class='classname', _for="someinput")
print(test)
```

```html
<label class="classname" for="someinput"></label>
```

### rendering

A domonic tree is composed of objects. i.e

```python
div()
# <domonic.html.div object at 0x106b0e6b0>
```

cast str() on any element to render it without formatting.

```python
el = str(div())
print(el)
# <div></div>
```

There's also a render method that takes 2 parameters, some domonic and an optional output file.

```python
page = div(span('Hello World'))
render(f"{page}", 'index.html')  # notice use of f-string to pretty print the html
```

### DOM

DOM manipulation with python.

#### createElement
to create your own elements use the DOM API

```python
from domonic.dom import *

site = html()
el = document.createElement('myelement')
site.appendChild(el)
print(site)
# <html><myelement></myelement></html>

```

There's an evolving DOM API. To learn more about the webAPI go here.

https://developer.mozilla.org/en-US/docs/Web/API

And check the code/docs to see what's currently been implemented.

```python
mysite.querySelectorAll('button') 

mysite.querySelectorAll("a[rel=nofollow]")
mysite.querySelectorAll("a[href='#services']")
mysite.querySelectorAll("a[href$='technology']")
mysite.querySelectorAll('.fa-twitter')

somelinks = mysite.querySelectorAll("a[href*='twitter']")
for l in somelinks:
    print(l.href)

```

To use the DOM either reference your root 'html' node or import the dom modules global 'document'

```python

# access the document via the html tag
mydom = html()
# mydom.getElementbyID...

# or by importing the document global
from domonic.dom import document
# document.createElement...
print(document)

```

### javascript

There is a javascript package that mimics the js API:

```python
from domonic.javascript import Math
print(Math.random())

from domonic.javascript import Array
myArr=Array(1,2,3)
print(myArr.splice(1))
# [2, 3]

from domonic.javascript import URL
url = URL('https://somesite.com/blog/article-one#some-hash')
print(url.protocol)  # https
print(url.host)  # somesite.com
print(url.pathname)  # /blog/article-one
print(url.hash)  # #some-hash

# Use Global class to import all the js methods from the global namespace i.e
# from domonic.javascript import Global
# Global.decodeURIComponent(...
# Global.encodeComponent(...
# Global.setInterval(...

# from domonic.javascript import Date, String, Number
# etc..
```

Use setInterval and clearInterval with params

```python

from domonic.javascript import setInterval, clearInterval

x=0

def hi(inc):
    global x
    x = x+inc
    print(x)

test = setInterval(hi, 1000, 2)
import time
time.sleep(5)
clearInterval(test)
print(f"Final value of x:{x}")

```

Or for a single delayed function call use setTimeout, clearTimeout

```python

from domonic.javascript import setTimeout, clearTimeout

timeoutID = setTimeout(hi, 1000)

```

call ```()``` on a stringvar to transform it into a Node

```python
from domonic.javascript import String

test = String("Hi there!")
test('div', _style="font-color:red;")
str(test('div', _style="font-color:red;"))
# <div style="font-color:red;">Hi there!</div>
```

passing it the tag and attributes...

a-tags inherit URL:

```python
from domonic.html import *

atag = a(_href="https://somesite.com:8000/blog/article-one#some-hash")
print('href:', atag.href)
# href: https://somesite.com:8000/blog/article-one#some-hash
print('protocol:', atag.protocol)
# protocol: https:
print('port:', atag.port)
# port: 8000

atag.protocol = "http"
atag.port = 8983
print(atag)
# <a href="http://somesite.com:8983/blog/article-one#some-hash">
```

For writing and using regular javascript, load from a src...

```python
script(_src="/docs/5.0/dist/js/bootstrap.bundle.min.js", _integrity="sha384-1234", _crossorigin="anonymous"),
```

or do inline js by opening triple quotes...

```python
script("""
let itbe = ""
"""),
```

### Styling

Styling is supported. Styles get passed to the style tag on render...

```python
mytag = div("hi", _id="test")
mytag.style.backgroundColor = "black"
mytag.style.fontSize = "12px"
print(mytag)
# <div id="test" style="background-color:black;font-size:12px;">hi</div>
```

To use css use a link tag as you usually would...

```python
link(_href="styles.css", _rel="stylesheet"),
```

or use triple quotes to open style tag...

```python
style("""
.placeholder-img {
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
}
"""),
```

### decorators

use decorators to wrap elements around function results

```python
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
```

It returns the tag object by default. You can pass True as a second param to the decorator to return a rendered string instead. Also accepts strings as first param i.e. custom tags.

### data-tags

python doesn't allow hyphens in parameter names. so use variable keyword argument syntax for custom data-tags

```python
div("test", **{"_data-test":"test"} )
```

or for example a colon...

```python
t = div( **{"_:test":"something"} )
str(t)
```

### JSON (utils)

decorate any function that returns python objects to return json instead

```python
from domonic.decorators import as_json
import domonic.JSON as JSON

@as_json
def somefunc():
    myObj = {"hi":[1,2,3]}
    return myObj

print( somefunc() )
# {"hi":[1,2,3]}
print( JSON.is_json(somefunc()) )
# True
```

convert json arrays into html tables...

```python
import domonic.JSON as JSON

# i.e. containting flat json array of dicts... [{"id":"01","name": "some item"},{"id":"02","name": "some other item"}]

json_data = JSON.parse_file('somefile.json')
mytable = JSON.tablify(json_data)
print(mytable)

```

convert json arrays into csv files...

```python
import domonic.JSON as JSON

json_data = JSON.parse_file('somefile.json')
JSON.csvify(json_data, 'data.csv')

```

convert csv files to json...

```python
import domonic.JSON as JSON

json_data =JSON.csv2json("data.csv")
print(json_data)

```

more to come...

### SVG

All tags extend 'Node' and 'tag'. So will have DOM and magic methods available to them. see the docs.

```python
circ = svg(
    circle(_cx="50", _cy="50", _r="40", _stroke="green", **{"_stroke-width": "4"}, _fill="yellow"),
    _width="100", _height="100",
)
mysvg = svg()
mysvg.appendChild(circ / 10)
print(mysvg)
```

### Tweening

Tween values with the tween library:

```python
from domonic.lerpy.easing import *
from domonic.lerpy.tween import *

someObj = {'x':0,'y':0,'z':0}
twn = Tween( someObj, { 'x':10, 'y':5, 'z':3 }, 6, Linear.easeIn )
twn.start()
```

### aframe / x3d

3d tags can be used if you import the js

```python
from domonic.html import *
from domonic.xml.aframe import *
from domonic.CDN import *

_scene = scene(
      box(_position="-1 0.5 -3", _rotation="0 45 0", _color="#4CC3D9"),
      sphere(_position="0 1.25 -5", _radius="1.25", _color="#EF2D5E"),
      cylinder(_position="1 0.75 -3", _radius="0.5", _height="1.5", _color="#FFC65D"),
      plane(_position="0 0 -4", _rotation="-90 0 0", _width="4", _height="4", _color="#7BC8A4"),
      sky(_color="#ECECEC")
    )

_webpage = html(head(),body(
    script(_src=CDN_JS.AFRAME_1_2), # < NOTICE you need to import aframe to use it
    str(_scene)
    )
)

render( _webpage, 'hello.html' )
```

### dQuery (NEW)

dQuery uses the º symbol (alt+0).

```python

    from domonic.html import *
    from domonic.dQuery import º

    d = html(head(body(li(_class='things'), div(_id="test"))))

    print( º('#test') )
    # <div id="test">
    print( º('.things') )
    # <li class="things">
    mydiv = º('<div class="test2"></div>')
    # <domonic.dQuery.o object at 0x107d5c9a0>

    b = º('#test').append(mydiv)
    print(b)
    # <div id="test"><div class="test2"></div></div>

```

Only recently started so check to see what's implemented.

### terminal

There is a command line package that can call bash/unix/posix and other apps on the command line: <br />
This package only works on nix systems as it effectively just passes stuff off to subprocess.

```python
from domonic.terminal import *

print(ls())
print(ls("-al"))
print(ls("../"))
print(pwd())
print(mkdir('somedir'))
print(touch('somefile'))
print(git('status'))

for file in ls( "-al" ):
    print("Line : ", file)

for f in ls():
    try:
        print(f)
        print(cat(f))
    except Exception as e:
        pass

for i, l in enumerate(cat('LICENSE.txt')):
    print(i,l)

print(man("ls"))
print(echo('test'))
print(df())
print(du())

for thing in du():
    print(thing)

print(find('.'))
# print(ping('eventual.technology'))# < TODO - need to strean output
print(cowsay('moo'))
print(wget('eventual.technology'))
print(date())
print(cal())
```

or just run arbitrary commands...

```python
from domonic.terminal import command
command.run("echo hi")
```

Take a look at the code in 'terminal.py' to see all the commands as there's loads. (Disclaimer: not all tested.)

Windows users can use now use cmd.

```python
from domonic.cmd import *
print(dir())
print(dir("..\\")) 
```

## parsing

domonic can work with other Treebuilders

There's a builtin ext to tap into html5lib. And also fork of the c++ htmlparser (see parsing ticket)

If it isn't already. You may need to install it...

```bash
pip install html5lib
```

Then use the domonic treebuilder instead of any of the html5lib treebuilders.

```python
import requests
import html5lib
from domonic.ext.html5lib_ import getTreeBuilder


r = requests.get("https://google.com")
parser = html5lib.HTMLParser(tree=getTreeBuilder())
page = parser.parse(r.content.decode("utf-8"))

# print the page with formatting
# print(f'{page}')

'''
links = page.getElementsByTagName('a')
for l in links:
    try:
        print(l.href)
    except Exception as e:
        # no href on this tag
        pass
'''

# turn the downloaded site into .pyml ;)
print(page.__pyml__())
```

For a quick parse try the window module...

```python
from domonic.window import *
window.location = "http://www.google.com"
print(window.document.title)
```

## DOCS

https://domonic.readthedocs.io/

### notes on templating

while you can create a div with content like :

```python
    div("some content")
```

python doesn't allow named params before unamed ones. So you can't do this:

```python
    div(_class="container", p("Some content") )
```

or it will complain the params are in the wrong order. You have to instead put content before attributes:

```python
    div( p("Some content"), _class="container")
```

which is annoying when a div gets long.

You can get around this by using 'html' which is available on every Element:

```python
    div( _class="container" ).html("Some content")
```

This is NOT like jQuery html func that returns just the inner content. use innerHTML for that.

It is used specifically for rendering.

### Common Errors

If templates are typed incorrectly they will not work.

There's a small learning curve getting .pyml templates correct. Usually (1) a missing comma between tags, (2) an underscore missing on an attribute or (3) params in the wrong order. Use this reference when starting out as a reminder when you get an error.

Here are the 4 solutions to those common errors when creating large templates...
( i.e. see bootstrap5 examples in test_domonic.py )

```python
IndexError: list index out of range
# - You most likely didn't put a underscore on an attribute.
```  

```python
SyntaxError: invalid syntax
# - You are Missing a comma between attributes
```

```python
SyntaxError: positional argument follows keyword argument
# - You have to pass attributes LAST. and strings and objects first. *see notes on templating above*
```

```python
TypeError: unsupported operand type(s) for ** or pow(): 'str' and 'dict'
# - You are Missing a comma between attributes. before the **{}
```

### CLI

Use the command line interface to help you out.

To view the online the docs:

```python
domonic -h
```

To see the version:

```bash
domonic -v
```

To quickly create a domonic project for prototyping:

```bash
domonic -p myproject
```

To evaluate some domonic pyml:

```bash
domonic -e 'html(head(),body(div()))'
```

To use xpath on a website from the command line:

```bash
domonic -x https://google.com '//a'
```

To use css selectors on a website from the command line:

```bash
domonic -q https://google.com 'a'
```

### EXAMPLE PROJECTS

A browser based file browser. Working example of how components can work:
[Blueberry](https://github.com/byteface/Blueberry/)

A cron viewer:
[ezcron](https://github.com/byteface/ezcron/)

A basic game:
[bombdisposer](https://github.com/byteface/bombdisposer/)

A lightweight version of domonic:
[htmlx](https://github.com/byteface/htmlx/tree/master/htmlx)

checkout [the docs](https://domonic.readthedocs.io/) for examples on how to easily make sitemaps with python.
or for example how to use domonic with flask, django, sanic and other server frameworks.

docs:
https://domonic.readthedocs.io/

There's also several useage examples in the repo so pull and have a look.

### Join-In

Feel free to contribute if you find it useful. (I'd be grateful for help on all fronts)

Email me, message me directly if you like or create a discussion on here. Or join the discord.

If there are any methods you want that are missing or not complete yet or you think you can help make it better just update the code and send a pull request.

I'll merge and releaese asap.

In the repo there's a requirements-dev.txt which is mostly the libs used in the examples.

requirements.txt are the libs used for packaging just the lib.

### running examples

```bash
. venv/bin/activate
pip install -r requirements-dev.txt
cd examples
python lifecalendar.py
```

### run tests

There are tests used during dev. They are useful as code examples and to see what still needs doing.

See Makefile to run all tests:

```bash
make test  # default tests ubuntu. so will fail on window when terminal test runs. comment out locally if that's the case
```

or to test a single function:

```bash
python -m unittest tests.test_javascript.TestCase.test_javascript_array
python -m unittest tests.test_dQuery.TestCase.test_addClass
python -m unittest tests.test_geom.TestCase.test_vec2

python3 -m unittest tests.test_cmd.TestCase.test_cmd_dir  # only windows

```

or to test a whole module

```bash
python -m unittest tests.test_html
python -m unittest tests.test_CDN
```

to see coverage

```bash
coverage run -m unittest discover tests/
coverage report
```

### rebuild docs

See Makefile:

```bash
. venv/bin/activate
cd docs
make html
```


### Disclaimer

There's several more widely supported libraries doing HTML generation, DOM reading/manipulation, terminal wrappers etc. Maybe use one of those for production due to strictness and support.

This is more of a fast prototyping library.
