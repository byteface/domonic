JavaScript
===================

.. meta::
   :description: JavaScript-like APIs in Python including Array, Object, String, Number, Date, Promise, URL, Math, timers, typed arrays, JSON, fetch, and porting helpers.
   :keywords: JavaScript in Python, Python Array, Python Promise, JS port to Python, typed arrays Python, setTimeout Python, Date.now Python

domonic includes a JavaScript-like runtime surface for practical scripting and porting.

It is useful for quickly porting familiar JS code to Python while staying close to web-platform concepts:

It is also useful for learning JavaScript from the Python side. Many APIs keep
their browser names and behaviour where practical, so ``Array.map()``,
``String.includes()``, ``Math.random()``, ``Date.now()``, ``Promise`` and
``URL`` feel familiar when you later meet them in JavaScript.

For JavaScript developers using Python, this module gives you familiar tools
while you translate browser or Node habits into Python scripts. It is handy for
ports, teaching material, tests, scraping utilities, and codebases where web
developers need to contribute Python without losing every familiar API at once.

.. code-block :: python

	from domonic.javascript import Math
	print(Math.random())

	from domonic.javascript import Array
	myArr = Array(1, 2, 3)
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

	# from domonic.javascript import Date, String, Number
	# etc..


Alongside the global helpers, there are familiar ``String``, ``Number``, ``Array``, ``Date``, ``URL``, and timing APIs.

Port JavaScript-Like Code
-------------------------

The goal is not to replace JavaScript. The goal is to make JavaScript-shaped
code easier to read, test, port and teach inside Python projects.

.. code-block :: python

	from domonic.javascript import Array, Math, Object, String

	items = Array("HTML", "DOM", "Web APIs")
	items.push("BeautifulSlop")

	meta = Object()
	meta.name = String("domonic")
	meta.score = Math.round(9.6)

	print(items.join(", "))
	print(meta.name.toUpperCase(), meta.score)

Promises and Timers
-------------------

.. code-block :: python

	from domonic.javascript import Promise, setTimeout

	def work(resolve, reject):
	    setTimeout(lambda: resolve("done"), 50)

	Promise(work).then(lambda value: print(value))


Date class
----------------

The ``Date`` class is available:

.. code-block :: python

	from domonic.javascript import Date
	print(Date.now())


Array methods
----------------

Many of the familiar JavaScript array methods are available in Python form:

.. code-block :: python

	myarr = Array("1", "2", 3, {"4": "four"}, 5, [6])
	
	print(myarr.length)
	print(myarr.includes("1"))
	print(myarr.includes(3))
	print(myarr.includes(10))
	print(myarr.indexOf(10))
	print(myarr.indexOf("1"))
	print(myarr.indexOf([6]))
	print(myarr[1])
	print(len(myarr))
	print(myarr.join('---'))
	print(myarr.lastIndexOf("1"))
	print(myarr.lastIndexOf(3))
	print(myarr.reverse())
	print(myarr.slice(0, 1))
	print(myarr.splice(1))
	# print(myarr.splice(2))
	# print(myarr.splice(3))
	# print(myarr.splice(4))
	print(myarr.splice(3, 3, "a", "b", "c"))
	print(myarr)
	print(myarr.pop())
	print(myarr)
	myarr.push(7)
	print(myarr)
	print(myarr.unshift('z'))
	print(myarr)
	print(myarr.shift())
	print(myarr)
	# print(myarr.concat())

	# myarr.sort()
	# myarr.fill()
	# myarr.isArray()?
	# myarr.map()
	# myarr.reduce()
	# myarr.reduceRight()
	# myarr.some()


String methods
----------------

``String`` subclasses ``str`` (like ``Number`` subclasses ``float``), so
``String(x)`` *is* a real string primitive -- ``isinstance(String(5), str)``
is ``True``, it hashes, sorts, and drops into any API that expects a ``str`` --
while still carrying the JavaScript method surface below.

A wide set of familiar string methods is available:

.. code-block :: python


	mystr = String("Some String")

	mystr.toLowerCase() # "some string"
	mystr.toUpperCase() # "SOME STRING"
	# print(mystr.length)
	mystr.repeat(2) # "Some StringSome String"
	print(mystr.startsWith('S'))
	# mystr.endsWith('g'))
	
	# JavaScript substr in Python.
	mystr.substr(1) # 'ome String'

	# JavaScript slice in Python.
	# print(mystr.slice(1, 3))
	mystr.slice(1, 3) # 'om')

	# trim
	mystr = String("   Some String   ")
	mystr.trim() # "Some String")

	# charAt
	mystr = String("Some String")
	mystr.charAt(1) # 'o'
	mystr.charAt(5) # 'S'

	# charCodeAt
	mystr.charCodeAt(1) # 111
	mystr.fromCharCode(111) # 'o'

	# test
	# mystr.test('a') # True
	# mystr.test('b') # False

	# replace
	# print(mystr.replace('S', 'X'))
	mystr.replace('S', 'X') # "Xome String"
	mystr.replace(' ', 'X') # "SomeXString"
	mystr.replace('S', 'X') != "Xome Xtring"

	# search
	mystr = String("Some String")
	mystr.search('a') # -1 (not found)
	mystr.search('o') # 1  (index of the first match)

	# substr
	print(mystr.substr(1, 2))
	mystr.substr(1, 2) # 'om')
	mystr.substr(1, 3) # 'ome')
	mystr.substr(1, 4) # 'ome ')
	mystr.substr(1, 5) # 'ome S')

	# toLocaleLowerCase
	mystr.toLocaleLowerCase() # 'some string'
	mystr.toLocaleLowerCase() # 'some string'

	# toLocaleUpperCase
	# print(mystr.toLocaleUpperCase())
	mystr.toLocaleUpperCase() # 'SOME STRING'

	# lastIndex
	# print(mystr.lastIndexOf('o'))
	mystr.lastIndexOf('o') # 1

	assert mystr.padEnd(13) # "Some String  "
	assert mystr.padStart(13) # "  Some String"
	assert mystr.padStart(13, '-') # "--Some String"
	
	mystr.includes('a') # False
	mystr.includes('Some') # True


Some obsolete JavaScript string helpers are also available:

.. code-block :: python

	>>> test = String("Hello World!")
	>>> test.blink()
	'<blink>Hello World!</blink>'
	>>> test.sub()
	'<sub>Hello World!</sub>'
	>>> test.sup()
	'<sup>Hello World!</sup>'
	>>> test.div() # ?? hang on?
	'<div>Hello World!</div>'
	>>> test.webpage() # ??? err... wait what!!!
	'<html><head><title>Hello World!</title>...</head><body><h1>Hello World!</h1></body></html>'


You can actually transform a type String into any tag.

Call ``()`` on a string value to transform it into a node:

.. code-block :: python

	>>> test = String("time to take a mo")
	>>> test('div', _style="font-color:red;")
	<div style="font-color:red;">time to take a mo</div>
	>>> str(test('div', _style="font-color:red;"))
	'<div style="font-color:red;">time to take a mo</div>'

Pass the tag name and attributes.


Regular expressions
-------------------

``RegExp`` translates JavaScript regex syntax to Python's ``re`` so patterns
copied from JS code keep working:

.. code-block :: python

	from domonic.javascript import RegExp, String

	# \p{...} Unicode property escapes
	String("a, b. c!").replace(RegExp(r"\p{P}+", "gu"), "")   # "a b c"

	# named groups, JS spelling
	RegExp(r"(?<year>\d{4})-(?<month>\d{2})").exec("2026-09").groups
	# {'year': '2026', 'month': '09'}

	# sticky (y) flag honours lastIndex
	r = RegExp(r"\d+", "y"); r.lastIndex = 3
	r.exec("abc123")                                          # ['123']

	# RegExp.replace with $1..$n / $& / $` / $', or a JS-style callback
	RegExp(r"(\w+)@(\w+)").replace("user@host", "$2:$1")      # "host:user"
	String("a1b2").replace(RegExp(r"\d", "g"), lambda m, *a: f"[{m}]")

``\p{...}`` accepts long category names and ``Script=<name>`` for common
scripts, and the JS idiom ``[^]`` (any character, newlines included) is
translated. ``String.search`` returns the match index, ``String.match`` returns
an exec-style array (or a list of matches with ``/g``), and ``matchAll`` yields
match arrays -- all matching the browser.

Strings are UTF-16
------------------

Like JavaScript, ``String`` length and indexing are **UTF-16 code-unit** based,
so an astral-plane character (an emoji, rare CJK, ...) counts as two.

.. code-block :: python

	from domonic.javascript import String

	s = String("a\U0001F600b")
	s.length            # 4  -- the emoji is two code units
	s.charCodeAt(1)     # 55357  (0xD83D, the lead surrogate)
	s.codePointAt(1)    # 128512 (the recombined scalar)
	s.slice(1, 3)       # "😀"

Pure-BMP text behaves exactly as a plain Python ``str`` would.


Object methods
----------------

``Object`` is useful for making dictionaries a bit more JS-like:

.. code-block :: python

	o = Object()
	o.prop = 'hi'
	str(o)


It also contains a growing list of methods you may know from JavaScript.

``Object.assign`` is variadic and returns the target; ``Object.freeze``
returns a version of a ``dict`` that raises on any mutation (use the return
value, the way you would in JS -- a plain Python ``dict`` can't be frozen in
place):

.. code-block :: python

	from domonic.javascript import Object

	config = Object.assign({}, {"a": 1}, {"b": 2}, {"a": 3})
	print(config)               # {'a': 3, 'b': 2}

	config = Object.freeze(config)
	print(Object.isFrozen(config))   # True
	config["a"] = 99             # raises TypeError: cannot modify a frozen object

``Array.from_`` (JS ``Array.from``) applies an optional map callback, and
reads an array-like ``{"length": n}`` by index:

.. code-block :: python

	from domonic.javascript import Array

	print(Array.from_([1, 2, 3], lambda x, *_: x * 2))   # [2, 4, 6]
	print(Array.from_({"length": 3}, lambda _, i: i))    # [0, 1, 2]

``JSON.parse`` / ``JSON.stringify`` honour a reviver / replacer, the way
JavaScript's do:

.. code-block :: python

	from domonic.javascript import JSON

	# replacer function: returning None (JS undefined) omits the key
	print(JSON.stringify({"a": 1, "b": 2}, lambda k, v: None if k == "b" else v))
	# {"a":1}

	# replacer array: a key whitelist
	print(JSON.stringify({"a": 1, "b": 2, "c": 3}, ["a", "c"]))
	# {"a":1,"c":3}

	# reviver: bottom-up transform while parsing
	print(JSON.parse('{"a":1,"b":2}', lambda k, v: v * 10 if isinstance(v, int) else v))
	# {'a': 10, 'b': 20}


setInterval
----------------

You can use ``setInterval`` and ``clearInterval`` with parameters:

.. code-block :: python

	from domonic.javascript import window

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
	# 2
	# 4
	# 6
	# 8
	# Final value of x:8



fetch
----------------

There is a fetch implementation that uses promises, with threaded and pooled variants.

.. code-block :: python

	from domonic.webapi.fetch import fetch

	response = fetch("https://example.com")
	print(response.text())

	from domonic.javascript import *

	urls = ['http://google.com', 'http://linkedin.com', 'http://eventual.technology']  # use your own domains

	print('run 1')
	results = window.fetch(urls[0])
	results.then(lambda r: print(r.text))
	print('run 1 FINISHED')

	def somefunc(response):
		print("I'm a callback", response.ok)
		return response

	mydata = window.fetch(urls[0]).then(somefunc)
	print(mydata)
	print(mydata.data)
	print(mydata.data.text)

	# fetch more than one
	results = window.fetch_set(urls)
	print(results)
	print(list(results))
	for r in results:
		if r is not None:
			print(r.ok)
			# print(r.text)

	# multi-threaded
	results = window.fetch_threaded(urls)
	print(results)
	print(list(results))
	for r in results:
		if r is not None:
			print(r.ok)
			# print(r.text)

	# pooled
	results = window.fetch_pooled(urls, timeout=2)
	print(results)
	for r in results:
		if r is not None:
			print(r.ok)
			# print(r.text)

	print('run 4')
	results = window.fetch(urls[0])
	print(results)
	results.then(lambda r: print(r.text) if r is not None else None)


All fetch methods use ``requests`` and pass keyword arguments through when you need to modify behaviour.

Related Examples and Guides
---------------------------

- :doc:`../guides/scrape-html`
- :doc:`../guides/live-dom-updates`
- `examples/mixed.py <https://github.com/byteface/domonic/blob/master/examples/mixed.py>`_
- `examples/web_crypto.py <https://github.com/byteface/domonic/blob/master/examples/web_crypto.py>`_
- `examples/webworkers.py <https://github.com/byteface/domonic/blob/master/examples/webworkers.py>`_


Keywords
----------------

If you ``import *``, you get the JS-style keywords:

.. code-block :: python

	print(true)  # True
	print(false) # False
	print(undefined) # None
	print(null) # None


You also get a function that evaluates Python strings:

.. code-block :: python

	sup = function('''print("hi")''')
	sup()


Typed arrays
----------------

JS-style typed arrays are also available.



Styling
----------------

Styling gets passed to the style tag on render.

.. code-block :: python

	mytag = div("hi", _id="test")
	mytag.style.backgroundColor = "black"
	mytag.style.fontSize = "12px"
	print(mytag)
	# <div id="test" style="background-color: black; font-size: 12px;">hi</div>


There are many other features. Take a look at the module docs below.


.. automodule:: domonic.javascript
    :members:
    :noindex:
