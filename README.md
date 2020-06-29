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

#### Now contains 4 main packages: (but by no means are any of them complete)

• html : Generate html with python3 😎 <br />
• dom : DOM API in python3 😲 <br />
• javascript : js API in python3 😳 <br />
• terminal : call terminal commands with python3 😱 -NEW (*see at the end*)<br />


## HTML TEMPLATING

```python
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
```
```html
<html><head><style></style><script></script></head><body><div>hello world</div><a href="http://www.somesite.com" style="font-size:10px;">this is a link</a><ol><li></li><li></li><li></li><li></li><li></li></ol><h1 class="test">test</h1></body></html>
```


### install
```bash
    python3 -m pip install domonic
```

or if you had it before upgrade:

```bash
    python3 -m pip install domonic --upgrade
```

### usage
```python
    print(html(body(h1('Hello, World!'))))
```
```html
<html><body><h1>Hello, World!</h1></body></html>
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

### lists
just do list comprehension and join it to strip the square brackets
```python
ul(''.join([f'{li()}' for thing in range(5)])),
```
```html
<ul><li></li><li></li><li></li><li></li></ul>
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

### fugly
use your own methods to prettify. the example uses a library that leverages beautifulsoup. i.e.
```python
output = render(html(body(h1('Hello, World!'))))
from html5print import HTMLBeautifier
print(HTMLBeautifier.beautify(output, 4))
```

### run tests
```bash
python3 test_domonic.py
python3 test_javascript.py
python3 test_terminal.py
```


### MORE

### javascript

There is a javascript package being started that mirrors the js API:

```python
from domonic.javascript import Math

print(Math.random())
```

```python
from domonic.javascript import URL

url = URL('https://somesite.com/blog/article-one#some-hash')
print(url.protocol)
print(url.host)
print(url.pathname)
print(url.hash)
```

You can update a-tags the same way as it inherits from URL:

```python
from domonic import *

atag = a(_href="https://somesite.com:8000/blog/article-one#some-hash")
print('href:',atag.href)
print('protocol:',atag.protocol)
print('port:',atag.port)

atag.protocol = "http"
atag.port = 8983
print(atag)
```

several other undocumented features. take a look at the code.


### terminal (NEW)

There is a command line package being started that can call bash/unix/posix and other apps on the command line: <br />
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

Take a look at the code in 'terminal.py' to see all the commands as there's loads. (Disclaimer: not all tested.)


## DOCS

### notes on templating

while you can create a div with content like :

    div("some content")

python doesn't allow named params before unamed ones. So you can't do this:

    div(_class="container", p("Some content") )

or it will complain the params are in the wrong order. You have to instead put content before attributes:

    div( p("Some content"), _class="container")

which is annoying when a div gets long. You can get around this several ways.

With 'innerHTML' which is available on every Node:

    div( _class="container" ).innerHTML("Some content")

With 'html' which is available on every Node:

    div( _class="container" ).html("Some content")


### Common Errors
If code is incorrectly typed it will obviously not work. Here are some common errors I've noticed when creating large templates...
( i.e. bootstrap5 examples in test_domonic.py )

IndexError: list index out of range
    - You most likely didn't put a underscore on an attribute.

SyntaxError: invalid syntax
    - You are Missing a comma between attributes

SyntaxError: positional argument follows keyword argument
    - You have to pass attributes LAST. and strings and objects first. *see docs*

TypeError: unsupported operand type(s) for ** or pow(): 'str' and 'dict'
    - You are Missing a comma between attributes. before the **{}


##### TODO - catch these errors and raise a friendly custom ParseError that tells you what to fix


### help
Feel free to send pull requests. I'll merge and releaese asap.


### disclaimer
exerimental/learning project

There's a complete more supported library I found already doing similar called 'dominate' . So if you want to do something like this, use that.


### Notes
https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56