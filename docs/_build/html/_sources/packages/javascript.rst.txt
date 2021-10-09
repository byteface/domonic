javascript
===================

There's a javascript package that mimics the js API.

It's useful for things like quickly porting javascript code to python but also if you already know javascript:

.. code-block :: python

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

	# from domonic.javascript import Date, String, Number
	# etc..


As as all of the usual String and Numbers methods you may be familiar with.


Array methods
----------------

All the javascript array methods you may be familiar with available python

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
	print(myarr.join('---'))  #  TODO - test some js ones
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

A whole bunch of familiar string methods for you to enjoy...

.. code-block :: python


	mystr = String("Some String")

	mystr.toLowerCase() # "some string"
	mystr.toUpperCase() # "SOME STRING"
	# print(mystr.length)
	mystr.repeat(2) # "Some StringSome String"
	print(mystr.startsWith('S'))
	# mystr.endsWith('g'))
	
	# javascript substr in python
	mystr.substr(1) # 'ome String'

	# javascript slice in python
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


Object methods
----------------

Object is useful for making dicts a bit more js-like...

.. code-block :: python

	o = Object()
	o.prop = 'hi'
	str(o)


But also contains a growing list of methods you may know from javascript.



setInterval
----------------

You can use setInterval and clearInterval with params

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

There's a fetch implementation that uses promises. With additional mulithreaded and pooled versions.

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


All fetch methods use requests and will pass all the kwargs along should you need to modify


Styling
----------------

Styling gets passed to the style tag on render.

.. code-block :: python

	mytag = div("hi", _id="test")
	mytag.style.backgroundColor = "black"
	mytag.style.fontSize = "12px"
	print(mytag)
	# <div id="test" style="background-color:black;font-size:12px;">hi</div>



Many other undocumented features. Take a look at the code.


.. automodule:: domonic.javascript
    :members:
    :noindex:

