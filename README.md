<h1 align="center">
    <img src="https://image.freepik.com/free-vector/demonic-goat_71119-56.jpg"
    style="background-color:rgba(0,0,0,0);" height=230 alt="domonic: generate html with python 3!">
    <br>
    domonic
    <br>
    <sup><sub><sup>Generate html with python 3! (and much more)</sup></sub></sup>
    <br>
</h1>

[![PyPI version](https://badge.fury.io/py/domonic.svg)](https://badge.fury.io/py/domonic.svg) 
[![Downloads](https://pepy.tech/badge/domonic)](https://pepy.tech/project/domonic)
[![Python version](https://img.shields.io/pypi/pyversions/domonic.svg?style=flat)](https://img.shields.io/pypi/pyversions/domonic.svg?style=flat)
[![Build status](https://travis-ci.com/byteface/domonic.svg?branch=master)](https://travis-ci.com/byteface/domonic.svg?branch=master)

#### Contains several evolving packages: (but by no means are any of them complete)

• html : Generate html with python 3 😎 <br />
• dom : DOM API in python 3 😲 <br />
• javascript : js API in python 3 😳 <br />
• terminal : call terminal commands with python3 😱 - NEW (*see at the end*)<br />
• JSON : utils for loading / decorating / transforming<br />
• SVG : Generate svg using python (untested)<br />

See the docs/code for more hidden features...
https://domonic.readthedocs.io/

## HTML Templating with Python 3

```python
    print(html(body(h1('Hello, World!'))))
```
```html
<html><body><h1>Hello, World!</h1></body></html>
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
render takes 2 parameters, some domonic and an optional output file.
```python
page = div(span('Hello World'))
render(page, 'index.html')
```

### data-tags
python doesn't allow hyphens in parameter names. so use variable keyword argument syntax for custom data-tags
```python
div("test", **{"_data-test":"test"} )
```

### DOM

#### createElement
to create your own elements use the DOM API
```python
from domonic.dom import *

site = html()
el = document.createElement('myelement')
site.appendChild(el)
print(site)

```

addEventlisteners recently been started. There's several more DOM methods. Check code to see what's currently implemented.


### javascript

There is a javascript package being started that mirrors the js API:

```python
from domonic.javascript import Math
print(Math.random())

from domonic.javascript import Array
myArr=Array(1,2,3)
print(myArr.splice(1))

from domonic.javascript import URL
url = URL('https://somesite.com/blog/article-one#some-hash')
print(url.protocol)
print(url.host)
print(url.pathname)
print(url.hash)

# from domonic.javascript import Global
# Global.decodeURIComponent(...
# Global.encodeComponent(...

# from domonic.javascript import Date
# etc..
```


You can use setInterval and clearInterval with params

```python

x=0

def hi(inc):
    global x
    x = x+inc
    print(x)

test = window.setInterval(hi, 1000, 2)
import time
time.sleep(5)
window.clearInterval(test)
print(f"Final value of x:{x}")


```

You can update a-tags the same way as it inherits from URL:

```python
from domonic.html import *

atag = a(_href="https://somesite.com:8000/blog/article-one#some-hash")
print('href:',atag.href)
print('protocol:',atag.protocol)
print('port:',atag.port)

atag.protocol = "http"
atag.port = 8983
print(atag)
```

Styling is now supported...

```python
mytag = div("hi", _id="test")
mytag.style.backgroundColor = "black"
mytag.style.fontSize = "12px"
print(mytag)
# <div id="test" style="background-color:black;font-size:12px;">hi</div>
```

several other undocumented features. Take a look at the code.


### JSON (utils)

decorate any function that returns python objects to return json instead

```python
from domonic.JSON import *

@return_json
def somefunc():
    myObj = {"hi":[1,2,3]}
    return myObj

print( somefunc() )
print( is_json(somefunc()) )
```

convert json arrays into html tables...

```python
from domonic.JSON import *

# i.e. containting flat json array of dicts... [{"id":"01","name": "some item"},{"id":"02","name": "some other item"}]

json_data = JSON.parse_file('somefile.json')
mytable = JSON.tablify(json_data)
print(mytable)

```

convert json arrays into csv files...

```python
from domonic.JSON import *

json_data = JSON.parse_file('somefile.json')
JSON.csvify(json_data, 'data.csv')

```

convert csv files to json...

```python
from domonic.JSON import *

json_data =JSON.csv2json("data.csv")
print(json_data)

```

more to come...


### SVG (untested)

Well I tested circle and that works...  But should be fine :)

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

You can tween values with the tween library:

```python
from domonic.lerpy.easing import *
from domonic.lerpy.tween import *

someObj = {'x':0,'y':0,'z':0}
twn = Tween( someObj, { 'x':10, 'y':5, 'z':3 }, 6, Linear.easeIn )
twn.start()
```

### terminal (NEW)

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


## DOCS

https://domonic.readthedocs.io/

### notes on templating

while you can create a div with content like :

    div("some content")

python doesn't allow named params before unamed ones. So you can't do this:

    div(_class="container", p("Some content") )

or it will complain the params are in the wrong order. You have to instead put content before attributes:

    div( p("Some content"), _class="container")

which is annoying when a div gets long.

You can get around this by using 'html' which is available on every Element:

div( _class="container" ).html("Some content")

This is NOT like jQuery html func that returns just the inner content. use innerHTML for that.

It is used specifically for rendering.


### Common Errors
If templates are typed incorrectly they will not work. Here are some solutions to common errors when creating large templates...
( i.e. see bootstrap5 examples in test_domonic.py )

IndexError: list index out of range
    - You most likely didn't put a underscore on an attribute.

SyntaxError: invalid syntax
    - You are Missing a comma between attributes

SyntaxError: positional argument follows keyword argument
    - You have to pass attributes LAST. and strings and objects first. *see docs*

TypeError: unsupported operand type(s) for ** or pow(): 'str' and 'dict'
    - You are Missing a comma between attributes. before the **{}


##### TODO - catch these errors and raise a friendly custom ParseError that tells you what to fix



### CLI
There's a few args you can pass to domonic on the command line to help you out.

To launch the docs for a quick reference to the APIs use:

```python

python3 -m domonic -h

```

This command will attempt to generate a template from a webpage. (only simple pages for now)

```python

python3 -m domonic -d http://eventual.technology

```

Then you can edit/tweak it to get what you need and build new components quicker.


### EXAMPLE PROJECTS

A browser based file browser. Working example of how components can work:
https://github.com/byteface/Blueberry/

A cron viewer:
https://github.com/byteface/ezcron/

A basic game:
https://github.com/byteface/bombdisposer/

docs:
https://domonic.readthedocs.io/


### Join-In
Feel free to contribute if you find it useful.

If there are any methods you want that are missing or not complete yet. Just update the code and send a pull request.

I'll merge and releaese asap.


### run tests
See Makefile:
```bash
make test
```
or to test a single function:
```bash
python3.7 -m unittest tests.test_javascript.domonicTestCase.test_javascript_array
```
see coverage
```bash
coverage run -m unittest discover tests/
coverage report
```

### Disclaimer

There's several more widely supported libraries doing HTML generation, DOM reading/manipulation, terminal wrappers etc. Maybe use one of those for production due to strictness and support.

This is more of a fast prototyping library.
