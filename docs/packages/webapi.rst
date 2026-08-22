webapi
===================

The ``webapi`` package groups browser-flavoured APIs that sit alongside the DOM surface.


console
----------------

.. code-block :: python

	from domonic.webapi.console import console
	console.log("Hello World")


encoding
----------------

.. code-block :: python

	from domonic.webapi.encoding import TextEncoder, TextDecoder
	encoder = TextEncoder()


fetch
----------------

.. code-block :: python

	from domonic.webapi.fetch import fetch


Web Crypto
----------------

``Crypto`` provides secure random values, UUIDs, and digest hashes through a
browser-like ``crypto`` object.

.. code-block :: python

	from domonic.javascript import Uint8Array
	from domonic.webapi.crypto import crypto

	token = Uint8Array(16)
	crypto.getRandomValues(token)
	print(crypto.randomUUID())
	print(crypto.subtle.digest("SHA-256", b"domonic").data.hex())


File API
----------------

``Blob``, ``File``, ``FileList`` and ``FileReader`` mirror the browser File API and
work with ``fetch``, ``FormData`` and drag-and-drop helpers.

.. code-block :: python

	from domonic.webapi.file import Blob, File, FileReader
	from domonic.webapi.url import URL

	file = File([b"hello"], "hello.txt", {"type": "text/plain"})
	reader = FileReader()
	reader.onload = lambda event: print(reader.result)
	reader.readAsText(file)

	object_url = URL.createObjectURL(file)


Sanitizer API
----------------

``Sanitizer`` cleans HTML fragments into domonic nodes without evaluating the
input. It supports the current ``elements``/``removeElements`` and
``attributes``/``removeAttributes`` configuration names, plus the older domonic
aliases.

.. code-block :: python

	from domonic.html import div
	from domonic.webapi.sanitizer import Sanitizer

	clean = Sanitizer().sanitizeToString(
		'<p onclick="evil()">Hello <script>bad()</script></p>'
	)
	assert clean == "<p>Hello </p>"

	target = div()
	target.setHTML('<a href="javascript:evil()">link</a>')
	assert str(target) == "<div><a>link</a></div>"


URL
----------------

``URL`` is a wrapper around Python's ``urlparse`` and ``urlencode`` helpers.

.. code-block :: python

	from domonic.webapi.url import URL

	myurl = URL("http://www.google.com/search?q=domonic")
	print(myurl.host)
	print(myurl.query)
	print(myurl.query.q)
	print(myurl.query.q.value)

For more information see the MDN URL API docs:
https://developer.mozilla.org/en-US/docs/Web/API/URL


XPATH
----------------

Here's a quick example of using XPath:

.. code-block :: python

	from domonic import domonic
	from domonic.webapi.xpath import XPathEvaluator, XPathResult
	
	somehtml = '''
	<div>XPath example</div>
	<div>Number of &lt;div&gt;s: <output></output></div>
	'''
	page = domonic.parseString(somehtml)
	evaluator = XPathEvaluator()
	expression = evaluator.createExpression("//div")
	result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
	assert result.snapshotLength == 2


For more information, see the MDN Web API docs:
https://developer.mozilla.org/en-US/docs/Web/API




.. automodule:: domonic.webapi.console
    :members:
    :noindex:

.. automodule:: domonic.webapi.encoding
    :members:
    :noindex:

.. automodule:: domonic.webapi.fetch
    :members:
    :noindex:

.. automodule:: domonic.webapi.crypto
    :members:
    :noindex:

.. automodule:: domonic.webapi.file
    :members:
    :noindex:

.. automodule:: domonic.webapi.sanitizer
    :members:
    :noindex:

.. automodule:: domonic.webapi.url
    :members:
    :noindex:

.. automodule:: domonic.webapi.xhr
    :members:
    :noindex:

.. automodule:: domonic.webapi.xpath
    :members:
    :noindex:
