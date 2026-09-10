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
Use and learn real HTML, DOM and JavaScript-style APIs using Python code!
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

**domonic** is a pure-Python implementation of the browser platform: a real DOM,
HTML/SVG/XML generation, multiple HTML parsers, CSS selectors, XPath, and a large
slice of the JavaScript and Web API surface — all as ordinary Python objects.

```python
from domonic.html import *

page = html(
    body(
        h1("Hello, World!"),
        p("HTML as Python objects."),
        a("GitHub", _href="https://github.com"),
    )
)

print(page)
# <html><body><h1>Hello, World!</h1><p>HTML as Python objects.</p><a href="https://github.com">GitHub</a></body></html>
```

That tree is a real DOM — query and mutate it like you would in a browser:

```python
page.querySelector("h1").textContent = "Hello, DOM!"     # mutate by selector
print([a.href for a in page.querySelectorAll("a")])       # ['https://github.com']
```

The same kind of tree comes back from parsed HTML:

```python
from domonic import domonic

document = domonic.parseString("<h1>Hello</h1><a href='/docs'>Documentation</a>")
print(document.querySelector("h1").textContent)           # Hello
```

New here? Start with the <a href="https://domonic.readthedocs.io/guides/examples/" target="_blank" rel="noopener">examples gallery</a>.

---

## Recipes

**Scrape a page, keep a real DOM** — Beautiful Soup ergonomics, domonic nodes underneath:

```python
from domonic.bs4 import BeautifulSlop

soup = BeautifulSlop("<main><a href='/docs'>Docs</a></main>", "html.parser")

for link in soup.find_all("a", href=True):
    print(link.text, link["href"])                       # Docs /docs

print(soup.querySelector("a").getAttribute("href"))       # same object, full DOM API
```

**Build a server-side component** — functions that return DOM trees:

```python
from domonic.html import a, article, h2, p

def card(title, body, href):
    return article(h2(title), p(body), a("Open", _href=href), _class="card")

print(card("Python DOM", "Generate HTML with Python objects.", "/docs"))
```

**Stream a large response** — render lazily instead of building one huge string:

```python
from fastapi.responses import StreamingResponse
from domonic.html import body, html, table, td, tr

def rows():
    for i in range(50_000):
        yield tr(td(f"Row {i}"), td(f"Data {i}"))

page = html(body(table(rows())))
return StreamingResponse(page.stream(), media_type="text/html")   # chunks, not one blob
```

More task guides: <a href="https://domonic.readthedocs.io/guides/scrape-html/" target="_blank" rel="noopener">scraping</a> ·
<a href="https://domonic.readthedocs.io/guides/server-side-html/" target="_blank" rel="noopener">server-side HTML</a> ·
<a href="https://domonic.readthedocs.io/guides/live-dom-updates/" target="_blank" rel="noopener">live DOM updates</a> ·
<a href="https://domonic.readthedocs.io/guides/parser-performance/" target="_blank" rel="noopener">parser performance</a> ·
<a href="https://domonic.readthedocs.io/guides/compiled-rendering/" target="_blank" rel="noopener">compiled SSR</a>

---

## Features

|                             |                                                                                                           |
| --------------------------- | --------------------------------------------------------------------------------------------------------- |
| 🏗️ **Markup generation**   | HTML5, SVG, XML, MathML, RSS, Atom, ODF, A-Frame, X3D and custom elements                                 |
| 🌳 **DOM**                  | Document, Element, Node, NodeList, fragments, ranges, events, traversal, observers, shadow DOM and more   |
| 🔎 **Querying**             | CSS selectors and XPath, index-backed for repeated queries                                                |
| 📥 **Parsing**              | Multiple interchangeable parser backends                                                                  |
| 🌐 **Web APIs**             | URL, URLPattern, storage, messaging, workers, crypto, performance, permissions and more                   |
| 🟨 **JavaScript-like APIs** | Array, Date, Math, String, Number, Promise, timers, typed arrays and JSON helpers                         |
| ⚡ **CLI**                   | Query URLs, files or piped HTML with CSS and XPath                                                        |
| 🧪 **Experiments**          | dQuery, d3-inspired utilities, diffdom, BeautifulSlop and other browser-inspired ideas                    |

Not every API is browser-complete — the goal is to keep moving closer to the real
standards. Python `3.10+`.

---

## Install

```bash
python3 -m pip install domonic          # or: pip install --upgrade domonic
```

```python
from domonic.html import *
print(h1("hello world"))
```

Want only the command line tool? Install it isolated with `pipx` — see the
<a href="https://domonic.readthedocs.io/guides/cli/" target="_blank" rel="noopener">CLI guide</a>.

---

## HTML that is actually Python

Tag names are the HTML names. Attributes are the HTML names with a leading
underscore, so examples read like HTML with Python syntax:

```python
from domonic.html import *

card = div(
    h2("domonic"),
    p("The browser DOM, in Python."),
    a("Documentation", _href="https://domonic.readthedocs.io"),
    _class="card",                         # _class -> class (avoids the keyword)
)

print(card)

label("Email", _for="email")              # _for -> for

div("hello", **{"_data-user-id": "42"})   # attributes that aren't valid identifiers
```

---

## A real DOM

domonic elements are nodes in a document tree, not formatted strings.

```python
from domonic.html import *
from domonic.dom import document

page = html(body(main(
    h1("Projects"),
    ul(li("domonic"), li("Blueberry"), li("ezcron")),
)))

page.querySelector("h1").textContent = "Open source projects"   # mutate

new_item = document.createElement("li")                         # create
new_item.textContent = "something new"
page.querySelector("ul").appendChild(new_item)                  # attach
```

domonic follows the <a href="https://dom.spec.whatwg.org/" target="_blank" rel="noopener">WHATWG DOM</a>
and <a href="https://html.spec.whatwg.org/" target="_blank" rel="noopener">HTML</a> standards where
practical. Full API: <a href="https://domonic.readthedocs.io/packages/dom/" target="_blank" rel="noopener">DOM documentation</a>.

---

## Query with CSS or XPath

Browser-style selectors, straight against the tree:

```python
page.querySelector("#content")
page.querySelectorAll("a[rel=nofollow]")
page.querySelectorAll("a[href$='.pdf']")
page.querySelectorAll("article > p:first-child")

for link in page.querySelectorAll("a"):
    print(link.href)
```

XPath works too — from Python (`domonic.webapi.xpath`, see the
<a href="https://domonic.readthedocs.io/guides/scrape-html/" target="_blank" rel="noopener">scraping guide</a>)
or straight from the terminal:

```bash
domonic -x https://example.com '//a/@href'
curl -s https://example.com | domonic -q 'a.cta' --attr href
```

The first lookup builds an index on the tree; the rest are map hits, not walks.
Mutations invalidate it automatically. 🚀
<a href="https://domonic.readthedocs.io/guides/parser-performance/" target="_blank" rel="noopener">Parser performance</a>.

---

## Parse HTML

```python
from domonic import domonic

page = domonic.parseString("<!doctype html><article><h1>Hello from HTML</h1></article>")
print(page.querySelector("h1"))
```

To fetch and parse a live URL in one step, assign `window.location` (see the
<a href="https://domonic.readthedocs.io/packages/html/" target="_blank" rel="noopener">html docs</a>).

Each backend adapts its native tree straight into the domonic DOM — no second
tree, no reparse. Pick one for zero dependencies, malformed-HTML repair, or
speed:

| Backend | Notes |
| --- | --- |
| `html.parser` | Python standard library, no extra dependency |
| `html5lib` | Pure Python, bundled with domonic, spec-accurate tree building |
| `turbohtml` | Pure-Python WHATWG parser, direct DOM adaptation |
| `selectolax` · `lxml_html` · `html5_parser` · `markupever` | Native / compiled parsers via a shared adapter |
| `tl` · `reliq` | Opt-in native parsers, outside `auto` |
| `expat` | Built in, for XML-like input |

```python
domonic.parseString(markup, parser="selectolax")   # pin one
domonic.set_default_parser("html.parser")           # or set a default
domonic.get_active_parser()                         # what "auto" chose
```

The default is `parser="auto"`, which tries the fastest installed backend that
can handle the input. Install notes, the full comparison, whitespace-fidelity
details and benchmarks are in the
<a href="https://domonic.readthedocs.io/guides/parser-performance/" target="_blank" rel="noopener">parser performance guide</a>.

---

## Render back to markup

```python
from domonic.html import div, h1, p, render

page = div(h1("Hello"), p("Rendered from a Python DOM."))

markup = str(page)                        # or: "".join(page.stream()) for chunks
render(f"{page}", "index.html")           # write to disk
```

Rendering is configurable through `DOMConfig` (`GLOBAL_AUTOESCAPE`,
`RENDER_OPTIONAL_CLOSING_TAGS`, `ATTRIBUTE_QUOTES`, an opt-in render cache, …).
See the <a href="https://domonic.readthedocs.io/packages/dom/" target="_blank" rel="noopener">DOM documentation</a>.

---

## More in domonic

Each of these is a package with its own docs — a taste here, the full surface a
click away.

<details>
<summary><strong>JavaScript-style APIs</strong> — <code>Math</code>, <code>Array</code>, <code>Date</code>, <code>URL</code>, <code>Promise</code>, timers…</summary>

```python
from domonic.javascript import Math, Array, URL, setTimeout

Math.random()
Array(1, 2, 3).splice(1)                  # [2, 3]
URL("https://example.com:8000/blog#hello").port   # 8000
setTimeout(lambda: print("later"), 1000)
```
<a href="https://domonic.readthedocs.io/packages/javascript/" target="_blank" rel="noopener">JavaScript documentation</a>
</details>

<details>
<summary><strong>Web APIs</strong> — fetch/XHR, storage, workers, crypto, sanitizer, streams, canvas…</summary>

```python
from domonic.webapi.sanitizer import Sanitizer

Sanitizer().sanitizeToString('<p onclick="bad()">Hi <script>bad()</script></p>')
# <p>Hi </p>
```
Dozens of APIs (`URL`, `URLPattern`, Web Storage, History, File API, Web Crypto,
Web Workers, WebSocket, SSE, Permissions, Performance, Scheduler, Compression
Streams, Canvas/WebGL, custom elements, Shadow DOM, MutationObserver…).
<a href="https://domonic.readthedocs.io/packages/webapi/" target="_blank" rel="noopener">Browse the Web APIs</a>
</details>

<details>
<summary><strong>SVG, XML, MathML and more</strong></summary>

```python
from domonic.svg import svg, circle

print(svg(circle(_cx="50", _cy="50", _r="40"), _width="100", _height="100"))
```
Also <a href="https://domonic.readthedocs.io/packages/xml/" target="_blank" rel="noopener">XML, MathML, RSS, Atom, ODF</a>,
<a href="https://domonic.readthedocs.io/packages/sitemap/" target="_blank" rel="noopener">sitemaps</a> and
<a href="https://domonic.readthedocs.io/packages/x3d/" target="_blank" rel="noopener">A-Frame / X3D</a>.
</details>

<details>
<summary><strong>Style</strong> — DOM-style property access</summary>

```python
box = div("hello", _id="message")
box.style.backgroundColor = "black"
box.style.fontSize = "12px"
# <div id="message" style="background-color: black; font-size: 12px;">hello</div>
```
<a href="https://domonic.readthedocs.io/packages/style/" target="_blank" rel="noopener">Style documentation</a>
</details>

<details>
<summary><strong>BeautifulSlop</strong> — a BS4-style API over domonic parsing</summary>

Familiar `find`, `find_all`, `select`, `get_text` and mutation methods, but the
objects you get back are real domonic nodes — no wrapper `Tag`, no second tree.
<a href="https://domonic.readthedocs.io/packages/bs4/" target="_blank" rel="noopener">BeautifulSlop documentation</a>
</details>

<details>
<summary><strong>diffdom</strong> — minimal DOM patches for live updates</summary>

```python
from domonic.diffdom import DiffDOM
from domonic.html import div, p

DiffDOM().diff(div(p("Version one")), div(p("Version two")))   # patch list
```
<a href="https://domonic.readthedocs.io/packages/diffdom/" target="_blank" rel="noopener">diffdom documentation</a>
</details>

<details>
<summary><strong>dQuery</strong> — a jQuery-inspired API</summary>

```python
from domonic.dQuery import º

º("#test").append(º('<div class="child"></div>'))
```
It also serves as a demanding consumer of the DOM implementation.
<a href="https://domonic.readthedocs.io/packages/dQuery/" target="_blank" rel="noopener">dQuery documentation</a>
</details>

<details>
<summary><strong>d3-inspired utilities</strong></summary>

```python
from domonic.d3 import *
```
A Python interpretation of useful parts of the d3 ecosystem, built on the
JavaScript and DOM layers.
<a href="https://domonic.readthedocs.io/packages/d3/" target="_blank" rel="noopener">d3 documentation</a>
</details>

<details>
<summary><strong>JSON utilities</strong> — data ⇄ HTML tables ⇄ CSV</summary>

```python
import domonic.JSON as JSON

JSON.tablify([{"id": "01", "name": "some item"}])   # -> an HTML table
JSON.csvify(data, "data.csv")
JSON.csv2json("data.csv")
```
<a href="https://domonic.readthedocs.io/packages/JSON/" target="_blank" rel="noopener">JSON documentation</a>
</details>

<details>
<summary><strong>Animation / tweening</strong></summary>

```python
from domonic.lerpy.tween import Tween
from domonic.lerpy.easing import Linear

Tween({"x": 0}, {"x": 10}, 6, Linear.easeIn).start()
```
<a href="https://domonic.readthedocs.io/packages/tween/" target="_blank" rel="noopener">tween documentation</a>
</details>

<details>
<summary><strong>Terminal APIs</strong> — Python wrappers for Unix commands</summary>

```python
from domonic.terminal import ls, git

print(ls())
print(git("status"))
```
Windows users can use `domonic.cmd`.
<a href="https://domonic.readthedocs.io/packages/terminal/" target="_blank" rel="noopener">terminal documentation</a>
</details>

---

## Command line

```bash
domonic -q https://example.com 'a.cta' --attr href --first    # CSS query a URL
domonic --xpath-file ./page.html '//title'                    # XPath a local file
curl -s https://example.com | domonic -q 'h1' --text          # pipe HTML in
domonic -e 'html(body(h1("hello")))'                          # evaluate pyml
domonic -p myproject --server fastapi                         # scaffold a project
```

Full flag reference: <a href="https://domonic.readthedocs.io/guides/cli/" target="_blank" rel="noopener">CLI guide</a>.

---

## Server-side HTML

domonic elements are Python objects that render to markup, so they drop into
FastAPI, Flask, Django, Sanic and others — see the
<a href="https://domonic.readthedocs.io/packages/servers/" target="_blank" rel="noopener">servers documentation</a>.

For views that only return HTML, `@compiled` turns the function into a string
renderer at import time — no DOM is built per request, no warm-up, the first
request as fast as the rest: 🚀

```python
from domonic import compiled
from domonic.html import div, h1, p

@compiled
def home(name="World"):
    return div(h1("Hello"), p(name))

print(home("Alice & Bob"))   # <div><h1>Hello</h1><p>Alice &amp; Bob</p></div>
```

Supported syntax, caching, route integration and how the compiler works are in
the <a href="https://domonic.readthedocs.io/guides/compiled-rendering/" target="_blank" rel="noopener">compiled-rendering guide</a>.

---

## Examples & projects

Working examples throughout the repo:
<a href="https://github.com/byteface/domonic/tree/master/examples" target="_blank" rel="noopener">github.com/byteface/domonic/tree/master/examples</a>

Built with domonic:

- <a href="https://github.com/byteface/domonic-libs/" target="_blank" rel="noopener">domonic-libs</a> — extends domonic further
- <a href="https://pypi.org/project/myjs/" target="_blank" rel="noopener">myjs</a> — a JavaScript interpreter in pure Python
- <a href="https://github.com/byteface/Blueberry" target="_blank" rel="noopener">Blueberry</a> — a browser-based file OS / component example
- <a href="https://github.com/byteface/ezcron" target="_blank" rel="noopener">ezcron</a> — a cron viewer
- <a href="https://github.com/byteface/bombdisposer" target="_blank" rel="noopener">bombdisposer</a> — a small game
- <a href="https://github.com/byteface/htmlx/tree/master/htmlx" target="_blank" rel="noopener">htmlx</a> — a lightweight DOM-focused relative of domonic

---

## Documentation

📚 <a href="https://domonic.readthedocs.io/" target="_blank" rel="noopener">domonic.readthedocs.io</a> —
API coverage, package guides and less common functionality ·
<a href="https://github.com/byteface/domonic/releases" target="_blank" rel="noopener">Release notes</a>

---

## Development & contributing

Contributions are welcome — fork, branch, add or update tests, open a PR.

```bash
python3 -m pip install -r requirements-dev.txt
make test                 # or: pytest tests
```

The tests double as executable examples of the API. See
<a href="CONTRIBUTING.md" target="_blank" rel="noopener">CONTRIBUTING.md</a> for more.

---

⭐ If you find it useful, consider starring the project.

<a href="https://domonic.readthedocs.io/" target="_blank" rel="noopener">Documentation</a> ·
<a href="https://pypi.org/project/domonic/" target="_blank" rel="noopener">PyPI</a> ·
<a href="https://github.com/byteface/domonic/tree/master/examples" target="_blank" rel="noopener">Examples</a> ·
<a href="https://github.com/byteface/domonic/releases" target="_blank" rel="noopener">Releases</a>
</content>
</invoke>
