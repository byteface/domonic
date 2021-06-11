Domonic: events
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



.. automodule:: domonic.events
	:members:
	:noindex:

