events
=================

There's an Event Dispatcher i.e

.. code-block :: python

	from domonic.events import *

	class SomeEventHandler(EventDispatcher):
	
	    def __init__(self):
	        super().__init__(self)
	        self.addEventListener('some_event', self.on_custom_event)
	
	    def on_custom_event(evt):
	    	print('that just happened')

	my_handler = SomeEventHandler()
	my_handler.dispatchEvent('some_event')


If you create a python virtual DOM with domonic you can listen for events like so...

.. code-block :: python

	def on_page_clicked(evt):
		print('the page was just clicked', evt)
		print('mouseX', evt.x)
		print('mouseY', evt.y)

	page.addEventListener( MouseEvent.CLICK, on_page_clicked )

* above example needs a MouseEvent relaying or dispatching from somewhere. i.e. examples/events


.. automodule:: domonic.events
	:members:
	:noindex:

