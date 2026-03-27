events
=================

Domonic includes a DOM-style event system with ``EventTarget`` at the core.

You can use it directly on your own Python objects:

.. code-block :: python

	from domonic.events import *

	class SomeEventHandler(EventTarget):
	
	    def __init__(self):
	        super().__init__()
	        self.addEventListener('some_event', self.on_custom_event)
	
	    def on_custom_event(self, evt):
	    	print('that just happened')

	my_handler = SomeEventHandler()
	my_handler.dispatchEvent(Event('some_event'))


And because DOM nodes also inherit from that event model, you can listen for
events on virtual documents and elements too:

.. code-block :: python

	def on_page_clicked(evt):
		print('the page was just clicked', evt)
		print('mouseX', evt.x)
		print('mouseY', evt.y)

	page.addEventListener( MouseEvent.CLICK, on_page_clicked )

.. automodule:: domonic.events
	:members:
	:noindex:
