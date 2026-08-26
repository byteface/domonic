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
