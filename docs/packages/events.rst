events
=================

.. meta::
   :description: DOM events in Python with EventTarget, Event, MouseEvent, KeyboardEvent, CustomEvent, bubbling, listeners, and dispatchEvent.
   :keywords: Python DOM events, EventTarget, dispatchEvent, addEventListener, CustomEvent, MouseEvent, KeyboardEvent, browser events

Domonic includes a DOM-style event system with ``EventTarget`` at the core.
Use it for Python browser-event ports, server-side DOM events, component tests,
worker messages, custom events, and event-driven examples.

EventTarget
-----------

.. code-block :: python

	from domonic.events import Event, EventTarget

	class SomeEventHandler(EventTarget):
	    def __init__(self):
	        super().__init__()
	        self.addEventListener("some_event", self.on_custom_event)

	    def on_custom_event(self, event):
	        print("that just happened", event.type)

	my_handler = SomeEventHandler()
	my_handler.dispatchEvent(Event("some_event"))

CustomEvent Data
----------------

Use ``CustomEvent`` when you want to pass structured data with the event.

.. code-block :: python

	from domonic.events import CustomEvent, EventTarget

	target = EventTarget()
	target.addEventListener("cart:add", lambda event: print(event.detail["sku"]))
	target.dispatchEvent(CustomEvent("cart:add", {"detail": {"sku": "DOM-001"}}))

DOM Node Events
---------------

DOM nodes also inherit from the event model, so you can listen for events on
virtual documents and elements.

.. code-block :: python

	from domonic.events import MouseEvent
	from domonic.html import button

	page = button("Save")

	def on_page_clicked(event):
	    print("clicked", event.x, event.y)

	page.addEventListener(MouseEvent.CLICK, on_page_clicked)
	page.dispatchEvent(MouseEvent(MouseEvent.CLICK, {"x": 12, "y": 20}))

Common Event Classes
--------------------

.. code-block :: python

	from domonic.events import Event, KeyboardEvent, MouseEvent, UIEvent

	Event("ready")
	MouseEvent(MouseEvent.CLICK, {"x": 10, "y": 20})
	KeyboardEvent(KeyboardEvent.KEYDOWN, {"key": "Enter"})
	UIEvent("resize")

.. automodule:: domonic.events
	:members:
	:noindex:
