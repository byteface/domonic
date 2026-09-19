window
===================

.. meta::
   :description: Python browser Window object: location, history, screen, matchMedia, resize/move, open/close, requestAnimationFrame, scrolling, postMessage and native host attachment.
   :keywords: Python Window API, browser window Python, window.location Python, matchMedia Python, requestAnimationFrame Python, window.open Python, postMessage Python

``Window`` is domonic's browsing context: the object a script gets as the
global ``window`` in a browser. It owns the current ``document``,
``location``, ``history``, ``navigator`` and ``screen``, and it is the class
that a renderer (headless or native) drives.

.. code-block :: python

	from domonic.window import Window

	win = Window(url="https://example.com/")
	print(win.location.href)
	# https://example.com/
	print(win.document)

A default instance is also importable directly, matching a browser's global
``window``:

.. code-block :: python

	from domonic.window import window, alert, confirm

	print(window.location.href)
	alert("hello")


Location and history
---------------------

Setting ``location`` navigates the window, updating ``document.URL`` and
pushing an entry onto ``history``.

.. code-block :: python

	from domonic.window import Window

	win = Window(url="https://example.com/")
	win.history.pushState({"page": 2}, "", "/page/2")
	win.history.replaceState({"page": 2, "filter": "new"}, "", "/page/2?filter=new")

	print(win.location.href)
	# https://example.com/page/2?filter=new
	print(win.history.state)
	# {'page': 2, 'filter': 'new'}


Screen, resize and move
------------------------

``resizeTo()``/``resizeBy()`` and ``moveTo()``/``moveBy()`` update the
window's screen state and dispatch a ``resize`` event when the size actually
changes.

.. code-block :: python

	from domonic.window import Window

	win = Window()
	win.addEventListener("resize", lambda e: print("resized to", win.innerWidth, win.innerHeight))

	win.resizeTo(800, 600)
	# resized to 800 600
	print(win.outerWidth, win.outerHeight)
	# 800 600

	win.moveTo(100, 50)
	print(win.screenX, win.screenY)
	# 100 50


matchMedia
----------------

``matchMedia()`` returns a live ``MediaQueryList`` evaluated against
``window.mediaFeatures``, which can be overridden for testing.

.. code-block :: python

	from domonic.window import Window

	win = Window()
	win.mediaFeatures["prefers-color-scheme"] = "dark"

	query = win.matchMedia("(prefers-color-scheme: dark)")
	print(query.matches)
	# True

	query.addEventListener("change", lambda e: print("now matches:", e.matches))
	win.resizeTo(400, 800)


Opening and closing windows
----------------------------

``open()`` returns a new child ``Window`` with ``opener``/``parent`` wired up;
``close()`` and ``focus()``/``blur()`` dispatch the matching lifecycle events.

.. code-block :: python

	from domonic.window import Window

	win = Window()
	child = win.open("https://example.com/popup")
	print(child.opener is win)
	# True

	child.addEventListener("close", lambda e: print("popup closed"))
	child.close()
	print(child.closed)
	# True


Animation frames and scheduling
--------------------------------

``requestAnimationFrame()``, ``requestIdleCallback()`` and
``queueMicrotask()`` schedule work the same way they do in a browser.

.. code-block :: python

	from domonic.window import Window

	win = Window()

	def on_frame(timestamp):
		print("frame at", timestamp)

	frame_id = win.requestAnimationFrame(on_frame)
	win.cancelAnimationFrame(frame_id)

	win.queueMicrotask(lambda: print("microtask ran"))


Scrolling
----------------

``scrollTo()``, ``scrollBy()`` and ``scroll()`` all accept either positional
``x, y`` or an options dict, matching the browser API.

.. code-block :: python

	from domonic.window import Window

	win = Window()
	win.addEventListener("scroll", lambda e: print("scrolled to", win.scrollX, win.scrollY))

	win.scrollTo({"left": 0, "top": 200})
	win.scrollBy(0, 50)
	print(win.scrollY)
	# 250


postMessage
----------------

.. code-block :: python

	from domonic.window import Window

	win = Window()
	win.addEventListener("message", lambda e: print("received:", e.data))
	win.postMessage({"hello": "world"})


Native hosts
----------------

A ``Window`` can attach to a native/backend host -- a renderer such as
Chromonic providing a real OS window. Host-specific extensions live behind
``window.native``, so domonic itself stays renderer-agnostic: calls like
``close()``, ``focus()``, ``resizeTo()`` and ``requestAnimationFrame()``
notify the host when it implements the matching method, but no host is ever
required.

.. code-block :: python

	from domonic.window import Window

	win = Window()
	win.attach_host(my_renderer)   # calls my_renderer.attach(win)
	win.native                     # my_renderer
	win.detach_host()              # calls my_renderer.detach(win)
