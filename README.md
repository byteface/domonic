<h1 align="center">
<br>
𖤐 domonic 𖤐
<br>
</h1>

<p align="center">
<strong>The browser DOM, in Python.</strong>
</p>

<p align="center">
Generate HTML. Parse real pages. Query with CSS or XPath. Manipulate a browser-style DOM.<br>
Then render it, serve it, scrape it, transform it, or do something strange with it.
</p>

<p align="center">

[![PyPI version](https://badge.fury.io/py/domonic.svg)](https://pypi.org/project/domonic/)
[![Downloads](https://pepy.tech/badge/domonic)](https://pepy.tech/project/domonic)
[![Python version](https://img.shields.io/pypi/pyversions/domonic.svg?style=flat)](https://pypi.org/project/domonic/)
[![Python package](https://github.com/byteface/domonic/actions/workflows/python-package.yml/badge.svg?branch=master)](https://github.com/byteface/domonic/actions/workflows/python-package.yml)
[![Documentation](https://readthedocs.org/projects/domonic/badge/?version=latest)](https://domonic.readthedocs.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/byteface/domonic?style=social)](https://github.com/byteface/domonic)

</p>

---

**domonic** is a pure-Python DOM toolkit inspired by the browser platform.

It gives you one document model for **creating, parsing, querying, traversing, manipulating and rendering markup**.

```python
from domonic.html import *

page = html(
    body(
        h1("Hello, World!"),
        p("HTML as Python objects."),
        a("GitHub", _href="https://github.com")
    )
)

print(page)
```

```html
<html><body><h1>Hello, World!</h1><p>HTML as Python objects.</p><a href="https://github.com">GitHub</a></body></html>
```

But generating HTML is only the beginning.

```python
heading = page.querySelector("h1")
heading.textContent = "Hello, DOM!"

for link in page.querySelectorAll("a"):
    print(link.href)
```

The same kind of DOM can also come from parsed HTML.

```python
from domonic import domonic

document = domonic.parseString("""
<html>
    <body>
        <h1>Hello</h1>
        <a href="/docs">Documentation</a>
    </body>
</html>
""")

print(document.querySelector("h1").textContent)
```

**Create it. Parse it. Query it. Change it. Render it.**

---

## Why domonic?

Python already has HTML generators, parsers and XML libraries.

domonic is interested in something broader:

> **What if Python had a practical, browser-flavoured document platform?**

So the project brings together:

|                             |                                                                                                         |
| --------------------------- | ------------------------------------------------------------------------------------------------------- |
| 🏗️ **Markup generation**   | HTML5, SVG, XML, MathML, RSS, Atom, ODF, A-Frame, X3D and custom elements                               |
| 🌳 **DOM**                  | Document, Element, Node, NodeList, fragments, ranges, events, traversal, observers, shadow DOM and more |
| 🔎 **Querying**             | CSS selectors and XPath                                                                                 |
| 📥 **Parsing**              | Multiple interchangeable parser backends                                                                |
| 🌐 **Web APIs**             | URL, URLPattern, storage, messaging, workers, crypto, performance, permissions and more                 |
| 🟨 **JavaScript-like APIs** | Array, Date, Math, String, Number, Promise, timers, typed arrays and JSON helpers                       |
| ⚡ **CLI**                   | Query URLs, files or piped HTML with CSS and XPath                                                      |
| 🧪 **Experiments**          | dQuery, d3-inspired utilities, diffdom, BeautifulSlop and other browser-inspired ideas                  |

Python `3.10+`.

---

# Install

```bash
python3 -m pip install domonic
```

Upgrade:

```bash
python3 -m pip install --upgrade domonic
```

Then:

```python
from domonic.html import *

print(h1("hello world"))
```

---

# HTML that is actually Python

HTML elements are ordinary Python objects.

```python
from domonic.html import *

card = div(
    h2("domonic"),
    p("The browser DOM, in Python."),
    a("Documentation", _href="https://domonic.readthedocs.io"),
    _class="card"
)

print(card)
```

Attributes are prefixed with `_` to avoid collisions with Python keywords:

```python
label("Email", _for="email", _class="label")
```

```html
<label for="email" class="label">Email</label>
```

For attributes that cannot be expressed as Python identifiers:

```python
div(
    "hello",
    **{"_data-user-id": "42"}
)
```

---

# A real DOM

domonic elements are more than formatted strings.

They're nodes in a document tree.

```python
from domonic.html import *

page = html(
    body(
        main(
            h1("Projects"),
            ul(
                li("domonic"),
                li("Blueberry"),
                li("ezcron")
            )
        )
    )
)

print(page.querySelector("h1"))
print(page.querySelectorAll("li"))
```

Manipulate the tree using familiar DOM concepts:

```python
title = page.querySelector("h1")
title.textContent = "Open source projects"

new_item = document.createElement("li")
new_item.textContent = "something new"

page.querySelector("ul").appendChild(new_item)
```

The project aims to follow the real platform where practical:

* [WHATWG DOM Standard](https://dom.spec.whatwg.org/)
* [HTML Standard](https://html.spec.whatwg.org/)
* [MDN Web APIs](https://developer.mozilla.org/en-US/docs/Web/API)

See the [DOM documentation](https://domonic.readthedocs.io/) for the implemented API.

---

# CSS selectors

Use browser-style selectors directly against the tree.

```python
page.querySelector("button")
page.querySelector("#content")
page.querySelector(".active")

page.querySelectorAll("a")
page.querySelectorAll("a[rel=nofollow]")
page.querySelectorAll("a[href='#services']")
page.querySelectorAll("a[href$='technology']")
page.querySelectorAll("a[href*='github']")
```

```python
for link in page.querySelectorAll("a"):
    print(link.href)
```

---

# XPath

XPath is available too.

From Python:

```python
from domonic import domonic

page = domonic.parseString("<main><h1>Hello</h1></main>")

# use XPath against your document tree
```

Or straight from your terminal:

```bash
domonic -x https://example.com '//a'
```

Against a local file:

```bash
domonic --xpath-file ./page.html '//title'
```

Or pipe HTML directly into it:

```bash
curl -s https://example.com | domonic -x '//a' --count
```

---

# Parse HTML

```python
from domonic import domonic

page = domonic.parseString("""
<!doctype html>
<html>
    <body>
        <article>
            <h1>Hello from HTML</h1>
        </article>
    </body>
</html>
""")

print(page.querySelector("h1"))
```

You can also load a page through the window API:

```python
from domonic.window import window

window.location = "https://example.com"

print(window.document.title)
```

---

# Pick your parser

One parser does not fit every job.

domonic lets you choose between **zero dependencies, pure Python compatibility, malformed-HTML repair and high-performance native parsers**.

```python
from domonic import domonic

page = domonic.parseString("<p>Hello</p>", parser="html.parser")
page = domonic.parseString("<p>Hello</p>", parser="html5lib")
page = domonic.parseString("<p>Hello</p>", parser="lxml_html")
page = domonic.parseString("<p>Hello</p>", parser="markupever")
page = domonic.parseString("<p>Hello</p>", parser="selectolax")
page = domonic.parseString("<p>Hello</p>", parser="html5_parser")
page = domonic.parseString("<p>Hello</p>", parser="justhtml")
page = domonic.parseString("<p>Hello</p>", parser="expat")
```

Set one for your application:

```python
from domonic import domonic

domonic.set_default_parser("html.parser")

page = domonic.parseString("<p>Hello</p>")
```

### Parser choices

| Parser         | Why use it?                                   |
| -------------- | --------------------------------------------- |
| `markupever`   | Fast Rust-powered HTML repair; uses the shared lxml DOM adapter |
| `lxml_html`    | Very fast lxml-backed parsing and direct lxml DOM adaptation |
| `html.parser`  | Python standard library; no extra dependency |
| `selectolax`   | Fast native HTML parsing through the shared lxml DOM adapter |
| `html5_parser` | Fast HTML5 parsing through the shared lxml DOM adapter |
| `justhtml`     | Pure-Python alternative                       |
| `html5lib`     | Pure Python and bundled with domonic          |
| `expat`        | Built into Python; useful for XML-like input  |

Optional parsers require their respective packages.

Install the native parser stack like this:

```bash
python -m pip install markupever lxml
python -m pip install selectolax lxml
python -m pip install html5-parser lxml
```

For parser details and installation notes, see the [documentation](https://domonic.readthedocs.io/).

---

# Render it back to markup

Every element can be rendered with `str()`:

```python
from domonic.html import *

page = div(
    h1("Hello"),
    p("Rendered from a Python DOM.")
)

markup = str(page)

print(markup)
```

Write documents to disk with `render`:

```python
render(f"{page}", "index.html")
```

Rendering behaviour can be configured through `DOMConfig`.

```python
from domonic.dom import DOMConfig

print(DOMConfig.GLOBAL_AUTOESCAPE)
print(DOMConfig.RENDER_OPTIONAL_CLOSING_TAGS)
```

See the docs for all rendering options.

---

# Browser-flavoured Python

domonic includes a large practical slice of JavaScript's familiar APIs.

```python
from domonic.javascript import Math, Array, Date

print(Math.random())

numbers = Array(1, 2, 3)

print(numbers.splice(1))
```

```python
from domonic.javascript import URL

url = URL("https://example.com:8000/blog/article#hello")

print(url.protocol)
print(url.host)
print(url.port)
print(url.pathname)
print(url.hash)
```

Timers are there too:

```python
from domonic.javascript import setTimeout

def hello():
    print("hello")

setTimeout(hello, 1000)
```

Other APIs include things such as:

`String` · `Number` · `Promise` · `JSON` · typed arrays · timers · URL helpers · global functions

This JavaScript-like layer also powers some of domonic's more unusual experiments.

---

# Web APIs

The web platform is much bigger than the DOM.

domonic implements or experiments with Python versions of APIs including:

* `URL`
* `URLSearchParams`
* `URLPattern`
* Fetch / XHR helpers
* Web Storage
* Cookie Store
* History
* File API
* Web Crypto
* Web Workers
* WebSocket
* Server-Sent Events
* Messaging
* Permissions
* Notifications
* Performance APIs
* Scheduler / `postTask`
* Sanitizer
* Compression streams
* Canvas / WebGL
* CSS font loading
* Gamepad
* Media APIs
* Import maps
* Speculation rules
* Custom elements
* Shadow DOM
* Mutation / tree observation
* XPath

…and more.

The README deliberately doesn't try to document all of them.

👉 **[Browse the domonic documentation](https://domonic.readthedocs.io/)**

---

# SVG, XML, MathML and more

The DOM isn't only HTML.

domonic can build other document types using the same object-oriented approach.

### SVG

```python
from domonic.html import *
from domonic.svg import *

icon = svg(
    circle(
        _cx="50",
        _cy="50",
        _r="40",
        _stroke="green",
        _fill="yellow"
    ),
    _width="100",
    _height="100"
)

print(icon)
```

There is also support for:

* XML
* MathML
* RSS
* Atom
* sitemaps
* ODF
* A-Frame
* X3D
* custom elements

See the [documentation](https://domonic.readthedocs.io/) for the individual packages.

---

# Style elements from Python

DOM-style property access works too.

```python
from domonic.html import *

box = div("hello", _id="message")

box.style.backgroundColor = "black"
box.style.fontSize = "12px"

print(box)
```

```html
<div id="message" style="background-color:black;font-size:12px;">hello</div>
```

---

# dQuery

Yes, there is also a jQuery-inspired API.

Because apparently implementing the DOM wasn't enough.

```python
from domonic.html import *
from domonic.dQuery import º

page = html(
    body(
        li(_class="thing"),
        div(_id="test")
    )
)

print(º("#test"))
print(º(".thing"))
```

Append nodes:

```python
new_div = º('<div class="child"></div>')

º("#test").append(new_div)
```

dQuery is useful in its own right, but it also serves as a demanding consumer of the underlying DOM implementation.

---

# d3-inspired utilities

domonic also contains a Python port / interpretation of useful parts of the d3 ecosystem built on top of its JavaScript and DOM layers.

```python
from domonic.d3 import *
```

See the [documentation and examples](https://domonic.readthedocs.io/) for current coverage.

---

# BeautifulSlop

domonic includes **BeautifulSlop**, a BS4-style compatibility experiment built over the domonic parsing system.

It exists for code that wants familiar soup-like ergonomics while still landing in the domonic world.

See the documentation and examples for current compatibility.

---

# JSON utilities

Convert Python data to JSON:

```python
from domonic.decorators import as_json

@as_json
def response():
    return {
        "hello": "world",
        "items": [1, 2, 3]
    }

print(response())
```

JSON arrays can also be turned into HTML tables or CSV:

```python
import domonic.JSON as JSON

data = JSON.parse_file("data.json")

table = JSON.tablify(data)

JSON.csvify(data, "data.csv")
```

And CSV can go the other way:

```python
data = JSON.csv2json("data.csv")
```

---

# Animation / tweening

There is a small tweening library too.

```python
from domonic.lerpy.easing import *
from domonic.lerpy.tween import *

position = {
    "x": 0,
    "y": 0,
    "z": 0
}

tween = Tween(
    position,
    {"x": 10, "y": 5, "z": 3},
    6,
    Linear.easeIn
)

tween.start()
```

---

# Terminal APIs

domonic even contains Python wrappers around common command-line tools on Unix-like systems:

```python
from domonic.terminal import *

print(ls())
print(pwd())
print(git("status"))
print(df())
```

Or run an arbitrary command:

```python
from domonic.terminal import command

command.run("echo hello")
```

Windows users can use `domonic.cmd`.

These utilities are not the core reason to install domonic, but they're part of the project's broader experiment:

**what familiar platform APIs become interesting when exposed naturally to Python?**

---

# Command line

domonic comes with a CLI for working with HTML without writing a script.

### Help

```bash
domonic -h
```

### Version

```bash
domonic -v
```

### Query a URL with CSS

```bash
domonic -q https://example.com 'a'
```

### Query a URL with XPath

```bash
domonic -x https://example.com '//a'
```

### Extract text

```bash
domonic -q https://example.com 'h1' --text
```

### Extract attributes

```bash
domonic -q https://example.com 'a' --attr href
```

### First result

```bash
domonic -q https://example.com 'a' --first
```

### Count results

```bash
domonic -x https://example.com '//a' --count
```

### Local files

```bash
domonic --xpath-file ./page.html '//title'
domonic --query-file ./page.html 'a.cta'
```

### Pipes

```bash
curl -s https://example.com | domonic -x '//a' --count
cat page.html | domonic -q 'a.cta' --attr href
```

### Evaluate pyml

```bash
domonic -e 'html(head(), body(h1("hello")))'
```

### Scaffold a project

```bash
domonic -p myproject
```

Choose a server:

```bash
domonic -p myproject --server fastapi
```

---

# Server-side HTML

Because domonic elements are Python objects that render to markup, they work naturally in Python web applications.

The repository contains examples for frameworks including:

* FastAPI
* Flask
* Django
* Sanic

…and others.

👉 [Browse the examples](https://github.com/byteface/domonic/tree/master/examples)

---

# One library, a lot of surface area

A rough map of the project:

| Area                | Includes                                                                           |
| ------------------- | ---------------------------------------------------------------------------------- |
| **HTML**            | HTML5 tag generation and rendering                                                 |
| **DOM**             | Document, Element, Node, events, ranges, traversal, fragments, observers           |
| **Selectors**       | CSS selectors + XPath                                                              |
| **Parsing**         | html5lib, html.parser, lxml, markupever, selectolax, html5_parser, justhtml, expat |
| **Documents**       | SVG, XML, MathML, RSS, Atom, ODF, sitemaps, A-Frame, X3D                           |
| **Web APIs**        | URL, storage, workers, crypto, messaging, permissions, performance and more        |
| **JavaScript**      | Array, Date, Math, Promise, timers, typed arrays and helpers                       |
| **Experiments**     | dQuery, d3-inspired utilities, BeautifulSlop, diffdom                              |
| **Utilities**       | JSON/CSV tools, decorators, tweening, string/number/byte helpers                   |
| **Developer tools** | CLI, terminal wrappers, project scaffolding                                        |

Not every API is implemented to browser-complete parity.

The goal is to make useful parts of the browser and document ecosystem available naturally from Python, while continuing to move closer to the real standards.

---

# What can you build with it?

domonic is useful anywhere you want **documents as programmable Python object trees**.

For example:

* server-side rendering
* static-site generation
* HTML generation
* scraping utilities
* document transformation
* HTML repair and parsing
* XML / SVG generation
* testing markup
* browser API experiments
* Python-first templating
* command-line extraction
* document diffing
* web framework responses
* programmatic sitemaps and feeds
* tools that need to both **read and write** HTML

The interesting part is that these don't need separate mental models.

A generated document and a parsed document can live in the same DOM world.

---

# Examples

There are working examples throughout the repository:

👉 **[github.com/byteface/domonic/tree/master/examples](https://github.com/byteface/domonic/tree/master/examples)**

Some projects built with domonic:

### [Blueberry](https://github.com/byteface/Blueberry)

A browser-based file OS and an example of building components with domonic.

### [ezcron](https://github.com/byteface/ezcron)

A cron viewer.

### [bombdisposer](https://github.com/byteface/bombdisposer)

A small game.

### [htmlx](https://github.com/byteface/htmlx/tree/master/htmlx)

A lightweight, low-dependency DOM-focused relative of domonic.

---

# Documentation

The README is the tour.

The docs are the manual.

### 📚 [domonic.readthedocs.io](https://domonic.readthedocs.io/)

Use the docs for detailed API coverage, package-specific examples and less common functionality.

Useful links:

* [Documentation](https://domonic.readthedocs.io/)
* [Examples](https://github.com/byteface/domonic/tree/master/examples)
* [Release notes](https://github.com/byteface/domonic/releases)
* [Contributing](CONTRIBUTING.md)
* [Security](SECURITY.md)

---

# Development

Clone the repository and install the development dependencies:

```bash
python3 -m pip install -r requirements-dev.txt
```

Run the test suite:

```bash
make test
```

Or:

```bash
pytest tests
```

Run an individual module:

```bash
python -m unittest tests.test_html
```

Coverage:

```bash
coverage run -m unittest discover tests/
coverage report
```

The tests are also useful as executable examples of the API.

---

# Contributing

Contributions are welcome.

1. Fork the repository
2. Create a branch
3. Make your change
4. Add or update tests where appropriate
5. Open a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for more information.

---

# Philosophy

domonic started with a simple idea:

**HTML should be easy to create from Python.**

That led naturally to elements.

Elements led to a DOM.

A DOM led to selectors, events, traversal and parsing.

Then came JavaScript APIs, Web APIs, SVG, XPath, dQuery, workers, URL APIs, parsers, diffing and everything else that makes documents programmable.

The project is still guided by the same question:

> **What would the browser platform feel like if Python could use it directly?**

If that sounds useful — or just interesting — give domonic a try.

```bash
pip install domonic
```

⭐ If you find it useful, consider starring the project.

[Documentation](https://domonic.readthedocs.io/) ·
[PyPI](https://pypi.org/project/domonic/) ·
[Examples](https://github.com/byteface/domonic/tree/master/examples) ·
[Releases](https://github.com/byteface/domonic/releases)
