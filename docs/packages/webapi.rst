webapi
===================

.. meta::
   :description: Browser Web APIs in Python: fetch, XMLHttpRequest, URL, URLPattern, XPath, FileReader, Blob, Sanitizer, Web Crypto, Streams, Workers, History, Geolocation, Canvas and console.
   :keywords: Python Web API, fetch Python, XMLHttpRequest Python, FileReader Python, Web Crypto Python, URLPattern Python, Web Workers Python, DOM API Python, XPath Python

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

	encoded = TextEncoder().encode("hello")
	decoded = TextDecoder("utf-8").decode(encoded)
	print(decoded)


fetch
----------------

.. code-block :: python

	from domonic.webapi.fetch import fetch

	response = fetch("https://example.com")
	print(response.text())


XHR
----------------

``XMLHttpRequest`` and ``FormData`` provide browser-shaped request helpers for
code that was originally written against web APIs.

.. code-block :: python

	from domonic.webapi.xhr import FormData, XMLHttpRequest

	data = FormData()
	data.append("name", "domonic")

	request = XMLHttpRequest()
	request.open("POST", "https://example.com/api")
	request.send(data)


URLPattern
----------------

``URLPattern`` matches URLs against path, hostname, protocol, and search
patterns.

.. code-block :: python

	from domonic.webapi.urlpattern import URLPattern

	pattern = URLPattern({"pathname": "/users/:id"})
	print(pattern.test("https://example.com/users/42"))


History
----------------

``History`` models ``pushState()``, ``replaceState()``, ``back()``,
``forward()``, ``go()``, ``length``, ``state`` and ``scrollRestoration``.

.. code-block :: python

	from domonic.window import Window

	win = Window("https://example.com/")
	win.history.pushState({"page": 2}, "", "/page/2")
	win.history.replaceState({"page": 2, "filter": "new"}, "", "/page/2?filter=new")

	print(win.location.href)
	print(win.history.state)


Geolocation
----------------

The geolocation helper is deterministic and test-friendly: set coordinates,
read the current position, or watch for position changes.

.. code-block :: python

	from domonic.webapi.geo import Geolocation

	geo = Geolocation()
	geo.setPosition({"latitude": 51.5072, "longitude": -0.1276, "accuracy": 10})
	geo.getCurrentPosition(lambda position: print(position.coords.latitude))


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


Messaging
----------------

``MessageChannel`` and ``BroadcastChannel`` provide browser-style in-process
message wiring for worker-like code and tests.

.. code-block :: python

	from domonic.webapi.messaging import BroadcastChannel, MessageChannel

	channel = MessageChannel()
	channel.port1.onmessage = lambda event: print(event.data)
	channel.port2.postMessage("hello")

	updates = BroadcastChannel("updates")
	updates.onmessage = lambda event: print(event.data)
	BroadcastChannel("updates").postMessage({"ok": True})


Web Workers
----------------

``Worker`` runs a local Python script or callable in a daemon thread with a
browser-style ``DedicatedWorkerGlobalScope``. Messages are cloned between the
parent and worker, and both sides support ``onmessage``, ``messageerror`` and
``error`` events.

.. code-block :: python

	from threading import Event

	from domonic.webapi.webworkers import Worker

	done = Event()

	def worker_main(scope):
		scope.onmessage = lambda event: scope.postMessage(event.data.upper())

	worker = Worker(worker_main)
	worker.onmessage = lambda event: (print(event.data), done.set())
	worker.postMessage("hello")
	done.wait(2)
	worker.terminate()


Scheduler
----------------

``Scheduler`` and ``TaskController`` provide a small Prioritized Task Scheduling
surface for ordered server-side work.

.. code-block :: python

	from domonic.webapi.scheduler import scheduler

	scheduler.postTask(lambda: "done", {"priority": "user-visible"})


Streams
----------------

Readable, writable, transform, compression, and decompression streams are
available for Web Streams-style examples and tests.

.. code-block :: python

	from domonic.webapi.streams import ReadableStream

	stream = ReadableStream(["hello", "world"])
	print(stream.getReader().read().value)


Canvas and WebGL
----------------

``HTMLCanvasElement.getContext()`` supports inspectable ``2d``, ``webgl`` and
``webgl2`` contexts. These contexts record drawing/setup commands so generated
examples and tests can verify canvas output without a browser renderer.

.. code-block :: python

	from domonic.html import canvas

	surface = canvas(width=320, height=180)
	ctx = surface.getContext("2d")
	ctx.fillRect(0, 0, 20, 20)
	print(ctx.commands)


CSS Font Loading
----------------

``FontFace`` and ``FontFaceSet`` model the browser font-loading surface and are
available through ``document.fonts``.

.. code-block :: python

	from domonic.dom import Document
	from domonic.webapi.cssfontloading import FontFace

	doc = Document()
	doc.fonts.add(FontFace("Demo", "url(/demo.woff2)")).load("16px Demo")


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


Notifications and Gamepad
-------------------------

``Notification`` provides browser-style notification objects without OS side
effects, while ``GamepadManager`` backs ``navigator.getGamepads()`` for tests and
interactive examples.

.. code-block :: python

	from domonic.webapi.gamepad import Gamepad
	from domonic.webapi.notifications import Notification
	from domonic.window import Window

	Notification.requestPermission()
	notice = Notification("Done", {"body": "Build finished"})
	notice.show()

	win = Window()
	win.navigator.connectGamepad(Gamepad("Pad"))
	print(win.navigator.getGamepads())


Service Workers
----------------

``ServiceWorkerContainer`` and registrations model the lifecycle enough for DOM
tests and worker-style examples without requiring a browser runtime.

.. code-block :: python

	from domonic.webapi.serviceworker import ServiceWorkerContainer

	container = ServiceWorkerContainer("https://example.com/app/")
	registration = container.register("/sw.js")


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

Object URLs work with the File API:

.. code-block :: python

	from domonic.webapi.file import Blob
	from domonic.webapi.url import URL

	blob = Blob(["hello"], {"type": "text/plain"})
	url = URL.createObjectURL(blob)
	print(url)
	URL.revokeObjectURL(url)

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

Related Examples and Guides
---------------------------

- :doc:`../guides/server-side-html`
- :doc:`../guides/live-dom-updates`
- `examples/file_api.py <https://github.com/byteface/domonic/blob/master/examples/file_api.py>`_
- `examples/web_crypto.py <https://github.com/byteface/domonic/blob/master/examples/web_crypto.py>`_
- `examples/messaging.py <https://github.com/byteface/domonic/blob/master/examples/messaging.py>`_
- `examples/webworkers.py <https://github.com/byteface/domonic/blob/master/examples/webworkers.py>`_
- `examples/scheduler_api.py <https://github.com/byteface/domonic/blob/master/examples/scheduler_api.py>`_




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

.. automodule:: domonic.webapi.messaging
    :members:
    :noindex:

.. automodule:: domonic.webapi.webworkers
    :members:
    :noindex:

.. automodule:: domonic.webapi.file
    :members:
    :noindex:

.. automodule:: domonic.webapi.sanitizer
    :members:
    :noindex:

.. automodule:: domonic.webapi.scheduler
    :members:
    :noindex:

.. automodule:: domonic.webapi.streams
    :members:
    :noindex:

.. automodule:: domonic.webapi.urlpattern
    :members:
    :noindex:

.. automodule:: domonic.webapi.history
    :members:
    :noindex:

.. automodule:: domonic.webapi.clipboard
    :members:
    :noindex:

.. automodule:: domonic.webapi.dragndrop
    :members:
    :noindex:

.. automodule:: domonic.webapi.credentials
    :members:
    :noindex:

.. automodule:: domonic.webapi.geo
    :members:
    :noindex:

.. automodule:: domonic.webapi.webstorage
    :members:
    :noindex:

.. automodule:: domonic.webapi.cookiestore
    :members:
    :noindex:

.. automodule:: domonic.webapi.mediadevices
    :members:
    :noindex:

.. automodule:: domonic.webapi.mediacapabilities
    :members:
    :noindex:

.. automodule:: domonic.webapi.mediasession
    :members:
    :noindex:

.. automodule:: domonic.webapi.netinfo
    :members:
    :noindex:

.. automodule:: domonic.webapi.push
    :members:
    :noindex:

.. automodule:: domonic.webapi.webrtc
    :members:
    :noindex:

.. automodule:: domonic.webapi.permissions
    :members:
    :noindex:

.. automodule:: domonic.webapi.serviceworker
    :members:
    :noindex:

.. automodule:: domonic.webapi.sse
    :members:
    :noindex:

.. automodule:: domonic.webapi.websocket
    :members:
    :noindex:

.. automodule:: domonic.webapi.canvas
    :members:
    :noindex:

.. automodule:: domonic.webapi.cssfontloading
    :members:
    :noindex:

.. automodule:: domonic.webapi.gamepad
    :members:
    :noindex:

.. automodule:: domonic.webapi.notifications
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
