JavaScript
===================

.. meta::
   :description: JavaScript-like APIs in Python including Array, Object, String, Number, Date, Promise, URL, Math, timers, typed arrays, JSON, fetch, and porting helpers.
   :keywords: JavaScript in Python, Python Array, Python Promise, JS port to Python, typed arrays Python, setTimeout Python, Date.now Python

domonic includes a JavaScript-like runtime surface for practical scripting and porting.

It is useful for quickly porting familiar JS code to Python while staying close to web-platform concepts:

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
	mystr.search('a') # False
	mystr.search('o') # True

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
	>>> test.sub()
	>>> test.sup()
	>>> test.div() # ?? hang on?
	>>> test.webpage() # ??? err... wait what!!!


You can actually transform a type String into any tag.

Call ``()`` on a string value to transform it into a node:

.. code-block :: python

	>>> test = String("time to take a mo")
	>>> test('div', _style="font-color:red;")
	>>> str(test('div', _style="font-color:red;"))

Pass the tag name and attributes.


Object methods
----------------

``Object`` is useful for making dictionaries a bit more JS-like:

.. code-block :: python

	o = Object()
	o.prop = 'hi'
	str(o)


It also contains a growing list of methods you may know from JavaScript.


setInterval
----------------

You can use ``setInterval`` and ``clearInterval`` with parameters:

.. code-block :: python

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



fetch
----------------

There is a fetch implementation that uses promises, with threaded and pooled variants.

.. code-block :: python

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
	# <div id="test" style="background-color:black;font-size:12px;">hi</div>


There are many other features. Take a look at the module docs below.


.. automodule:: domonic.javascript
    :members:
    :noindex:
