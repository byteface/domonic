Domonic: Javascript
===================

There is a javascript package being started that mirrors the js API:

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

	# from domonic.javascript import Date
	# etc..


setInterval
----------------

You can use setInterval and clearInterval with params

.. code-block :: python

	x=0

	def hi(inc):
	    global x
	    x = x+inc
	    print(x)

	test = window.setInterval(1000, hi, 2)
	import time
	time.sleep(5)
	window.clearInterval(test)
	print(f"Final value of x:{x}")



You can update a-tags the same way as it inherits from URL:

.. code-block :: python

	from domonic.html import *

	atag = a(_href="https://somesite.com:8000/blog/article-one#some-hash")
	print('href:',atag.href)
	print('protocol:',atag.protocol)
	print('port:',atag.port)

	atag.protocol = "http"
	atag.port = 8983
	print(atag)


Styling
----------------

.. code-block :: python

	mytag = div("hi", _id="test")
	mytag.style.backgroundColor = "black"
	mytag.style.fontSize = "12px"
	print(mytag)
	# <div id="test" style="background-color:black;font-size:12px;">hi</div>


several other undocumented features. Take a look at the code.


.. automodule:: domonic.javascript
    :members:
    :noindex:

