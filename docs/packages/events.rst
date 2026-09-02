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

Propagation
-----------

``dispatchEvent`` runs the full three-phase model over the node's ancestor
chain: capture (root to target), the target itself, then bubble (target back to
root) for events created with ``{"bubbles": True}``. Register a capture-phase
listener by passing ``True`` (or ``{"capture": True}``) as the third argument.
``event.stopPropagation()`` ends the walk after the current node;
``stopImmediatePropagation()`` also skips the remaining listeners on that node.

.. code-block :: python

	from domonic.events import MouseEvent
	from domonic.html import button, div

	root = div(button("x"))
	btn = root.args[0]

	root.addEventListener("click", lambda e: print("root capture"), True)
	root.addEventListener("click", lambda e: print("root bubble"))
	btn.addEventListener("click", lambda e: print("target"))

	btn.dispatchEvent(MouseEvent("click", {"bubbles": True}))
	# root capture / target / root bubble

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
