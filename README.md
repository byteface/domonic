<h1 align="center">
    <br>𖤐 domonic 𖤐<br>
</h1>

[![PyPI version](https://badge.fury.io/py/domonic.svg)](https://badge.fury.io/py/domonic.svg)
[![Downloads](https://pepy.tech/badge/domonic)](https://pepy.tech/project/domonic)
[![Python version](https://img.shields.io/pypi/pyversions/domonic.svg?style=flat)](https://img.shields.io/pypi/pyversions/domonic.svg?style=flat)
[![Python package](https://github.com/byteface/domonic/actions/workflows/python-package.yml/badge.svg?branch=master)](https://github.com/byteface/domonic/actions/workflows/python-package.yml)
[![readthedocs](https://readthedocs.org/projects/domonic/badge/?version=latest)](https://domonic.readthedocs.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![byteface github](https://img.shields.io/badge/GitHub-byteface-181717.svg?style=flat&logo=github)](https://github.com/byteface)

#### A pure Python [DOM](https://dom.spec.whatwg.org/) that goes way beyond minidom

- Python `3.10+`
- HTML, SVG, DOM, events, web APIs, animation, and a JavaScript-like runtime
- Built for generating, parsing, traversing, and manipulating real document trees

### Install

```bash
python3 -m pip install domonic
python3 -m pip install --upgrade domonic
```

For development:

```bash
python3 -m pip install -r requirements-dev.txt
```

## Creating HTML with Python 3

```python
from domonic.html import *
print(html(body(h1('Hello, World!'))))
# <html><body><h1>Hello, World!</h1></body></html>
```

to pretty format and insert the doctype, use an f-string:

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

### Parsing html

```python
from domonic import domonic
mydom = domonic.parseString('<somehtml...')
```

or parse an entire webpage with the window module...

```python
from domonic.window import window
window.location = "https://example.com"
print(window.document.title)
```

html5lib is bundled as the default parser as it's pure python. However see the `Parsers` section below as other parser backends are supported and are much faster.


### xpath or css

Use xpath or css selectors on command line...

```bash
domonic -x https://google.com '//a' | uniq | sort
```

### More

- [html](https://domonic.readthedocs.io/_modules/domonic/html.html) : Generate html with Python 3 😎
- [dom](https://domonic.readthedocs.io/_modules/domonic/dom.html) : DOM API in Python 3 😲
- [javascript](https://domonic.readthedocs.io/_modules/domonic/javascript.html) : js API in Python 3 😳 + ([dQuery](https://domonic.readthedocs.io/packages/dQuery.html), [d3](https://domonic.readthedocs.io/packages/d3.html))
- JSON : utils for loading / decorating / transforming
- SVG || mathml || aframe || x3d tags - generators for popular tags
- terminal || cmd : call terminal commands with Python3 😱

See the [docs/code](https://domonic.readthedocs.io/) for more features or examples in the [repo](https://github.com/byteface/domonic/tree/master/examples)


### Namespace

Simply import what you need...

```python
from domonic import div, span, input as myinput, html as root
```

or use the tags package if you want a namespace. i.e.

```python
import domonic.tags
print(domonic.tags.h1)
# or
import domonic.tags as tags
str(tags.div)
# or 
import domonic.tags as html
print(html.span)
```


### HTML attributes

Prepend attributes with an underscore ( avoids clashing with Python keywords )

```python
test = label(_class='classname', _for="someinput")
print(test)
```

```html
<label class="classname" for="someinput"></label>
```

### Rendering DOM objects

domonic is a pure Python DOM whose tree is composed of objects. i.e

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

For rendering options see DOMConfig.

```python
from domonic.dom import DOMConfig
print(DOMConfig.GLOBAL_AUTOESCAPE)  # Default False
print(DOMConfig.RENDER_OPTIONAL_CLOSING_TAGS)  # Default True
print(DOMConfig.RENDER_OPTIONAL_CLOSING_SLASH)  # Defaults True
print(DOMConfig.SPACE_BEFORE_OPTIONAL_CLOSING_SLASH)  # Default False
```

## DOM

DOM manipulation with Python, built with the actual platform in mind.

### createElement

Create your own elements with the DOM API

```python
from domonic.dom import *

site = html()
el = document.createElement('myelement')
site.appendChild(el)
print(site)
# <html><myelement></myelement></html>

```

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

The aim is to track the real platform as closely as possible :
- [WHATWG DOM Standard](https://dom.spec.whatwg.org/)
- [HTML Standard](https://html.spec.whatwg.org/)
- [MDN Web APIs](https://developer.mozilla.org/en-US/docs/Web/API)

Check the [code/docs](https://domonic.readthedocs.io/) to see what's currently implemented.


### Javascript

There is a Javascript package that mirrors a large, practical slice of the JS API:

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

You can call ```()``` on a stringvar to transform it into a Node

```python
from domonic.javascript import String

test = String("Hi there!")
test('div', _style="font-color:red;")
str(test('div', _style="font-color:red;"))
# <div style="font-color:red;">Hi there!</div>
```

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

For writing and using regular Javascript, load from a src...

```python
script(_src="/docs/5.0/dist/js/bootstrap.bundle.min.js", _integrity="sha384-1234", _crossorigin="anonymous"),
# <script src="/docs/5.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-1234" crossorigin="anonymous"></script>
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

### Decorators

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

Python doesn't allow hyphens in parameter names. so use variable keyword argument syntax for custom data-tags

```python
div("test", **{"_data-test":"test"} )
# <div data-test="test">test</div>
```

or for example a colon...

```python
t = div( **{"_:test":"something"} )
str(t)
# <div :test="something"></div>
```

### JSON (utils)

Decorate any function that returns Python objects to return json instead

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

### SVG

All tags extend 'Element'. So will have DOM and magic methods available to them. See the [docs](https://domonic.readthedocs.io/).

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

Tween values with the built-in tween library:

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
    script(_src=CDN_JS.AFRAME), # < NOTICE you need to import aframe to use it
    str(_scene)
    )
)

render( _webpage, 'hello.html' )
```

### dQuery

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

dQuery is included here because it is useful for proving out the DOM against a demanding consumer API, not just as a convenience wrapper.

### Terminal

There is a command line package that can call bash/unix/posix and other apps on the command line:

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
# print(wget('eventual.technology'))
print(date())
print(cal())
```

or just run arbitrary commands...

```python
from domonic.terminal import command
command.run("echo hi")
```

Take a look at the code in `terminal.py` to see all the commands as there's loads. (Disclaimer: not all tested.)

Windows users can use now use cmd.

```python
from domonic.cmd import *
print(dir())
print(dir("..\\")) 
```

### Docs

[https://domonic.readthedocs.io/](https://domonic.readthedocs.io/)

### CLI

Use the command line interface to help you out.

To view the online docs:

```python
domonic -h
```

See the version:

```bash
domonic -v
```

Quickly create a domonic project for prototyping:

```bash
domonic -p myproject
```

Evaluate some domonic pyml:

```bash
domonic -e 'html(head(),body(div()))'
```

Use xpath on a website from the command line:

```bash
domonic -x https://google.com '//a'
```

Use css selectors on a website from the command line:

```bash
domonic -q https://google.com 'a'
```

Use XPath or CSS selectors against a local file:

```bash
domonic --xpath-file ./page.html '//title'
domonic --query-file ./page.html 'a.cta'
```

Pipe HTML in directly:

```bash
curl -s https://example.com | domonic -x '//a' --count
cat page.html | domonic -q 'a.cta' --attr href
```

Output controls:

```bash
domonic -q https://example.com 'a' --text
domonic -q https://example.com 'a' --attr href --first
domonic -x https://example.com '//a' --count
```

Create a project non-interactively with a chosen server:

```bash
domonic -p myproject --server fastapi
```

### Example Projects

[Blueberry](https://github.com/byteface/Blueberry/) : A browser based file OS. Working example of how components can work.

[ezcron](https://github.com/byteface/ezcron/) : A cron viewer

[bombdisposer](https://github.com/byteface/bombdisposer/) : A basic game

[htmlx](https://github.com/byteface/htmlx/tree/master/htmlx) : A low dependency lightweight (DOM only) version of domonic

Checkout [the docs](https://domonic.readthedocs.io/) for more examples i.e. generating sitemaps or using domonic with server frameworks like Flask, Django, Sanic, FastAPI and others.

There are also several usage examples in the repo, so pull it and have a look.

### Running the examples

```bash
. venv/bin/activate
pip install -r requirements-dev.txt
cd examples
python lifecalendar.py
```

### Run the tests

The tests are useful both as regression coverage and as working code examples.

See Makefile to run all tests:

```bash
make test  # or testpc on Windows to avoid terminal tests
```

Testing a single function:

```bash
python -m unittest tests.test_javascript.TestCase.test_javascript_array
python -m unittest tests.test_dQuery.TestCase.test_addClass
python -m unittest tests.test_geom.TestCase.test_vec2
python3 -m unittest tests.test_cmd.TestCase.test_cmd_dir  # only windows
```

Test a whole module

```bash
python -m unittest tests.test_html
python -m unittest tests.test_CDN
```

to see coverage

```bash
coverage run -m unittest discover tests/
coverage report
```

or...

```bash
pip install pytest
pytest tests
```


### Parsers

You can choose a parser per call (see below on parser install notes):

```python
from domonic import domonic

page = domonic.parseString("<p>Hello</p>", parser="html5_parser")
page = domonic.parseString("<p>Hello</p>", parser="html5lib") # bundled with domonic
page = domonic.parseString("<p>Hello</p>", parser="justhtml")
page = domonic.parseString("<p>Hello</p>", parser="markupever") # stupidly fast
page = domonic.parseString("<p>Hello</p>", parser="selectolax")
page = domonic.parseString("<p>Hello</p>", parser="expat")
```

Or set the default parser for your app:

```python
from domonic import domonic

domonic.set_default_parser("html5_parser")
page = domonic.parseString("<p>Hello</p>")
```

Parser install notes (listed in order of speed when used with domonic):

- `markupever`: `pip install markupever` 🚀 Rust
- `html5_parser`: `pip install html5-parser lxml` 🚀 c++
- `selectolax`: `pip install selectolax lxml` 🚀 c++
- `justhtml`: `pip install justhtml` 🐢 python
- `html5lib`: `pip install html5lib` 🐢 python
- `expat`: 🐌 built into Python. (chokes on html5 or malformed content)

`html5lib` has a direct treebuilder integration.
`markupever` also uses an lxml adapter but we can get content w/o pretty formatting
`html5_parser` and `selectolax` have to use an lxml adapter as there's no hooks
`justhtml` uses html5lib adapter-backed parser (parse + conversion == slower).

*html5parser was a hidden feature on older version of domonic

## Contributing
Contributions are welcome! If you'd like to contribute, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Write your code and add tests if applicable.
4. Submit a pull request with a clear description of your changes.

For more details, see the [CONTRIBUTING.md](CONTRIBUTING.md) file.
