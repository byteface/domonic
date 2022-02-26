"""
    domonic.webapi.sse
    ====================================
    https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events

    TODO - consider a blocking verison?
    TODO - port one of the polyfills?
    https://github.com/EventSource/eventsource/blob/master/lib/eventsource.js
    https://github.com/remy/polyfills/blob/master/EventSource.js
    https://github.com/Yaffle/EventSource/blob/master/src/eventsource.js

    # TESTING - useage example... clone this and point at the stream
    # https://github.com/byteface/SSELoggerDemo

"""

from domonic.events import MessageEvent, EventTarget
from domonic.ext.sseclient import SSEClient

class EventSource(EventTarget):
    # https://developer.mozilla.org/en-US/docs/Web/API/EventSource

    CONNECTING = 0
    OPEN = 1
    CLOSED = 2

    def __init__(self, url, eventSourceInitDict=None, **kwargs):
        """
        The EventSource interface provides the ability to asynchronously receive messages from a server using simple push paradigm.
        """
        eventSourceInitDict = eventSourceInitDict or kwargs
        super().__init__()
        self._url = url
        self._readyState = EventSource.CLOSED
        self._withCredentials = eventSourceInitDict.get('withCredentials', False)
        self._lastEventId = eventSourceInitDict.get('lastEventId', None)

        self._onmessage = eventSourceInitDict.get('onmessage', None)
        self._onerror = eventSourceInitDict.get('onerror', None)
        self._onopen = eventSourceInitDict.get('onopen', None)
        self._onreadystatechange = eventSourceInitDict.get('onreadystatechange', None)

        # from sseclient import SSEClient
        # messages = SSEClient(url)
        # self._readyState = EventSource.OPEN
        # for msg in messages:
        #     self.onmessage(MessageEvent(msg))
        #     print(msg)
        # self._readyState = EventSource.CLOSED

        # def _do_stuff():
        # from sseclient import SSEClient
        messages = SSEClient(url)
        self._readyState = EventSource.OPEN
        # self.onopen(MessageEvent(messages))
        for msg in messages:
            # self.onmessage(MessageEvent(msg))
            print(msg)
        self._readyState = EventSource.CLOSED

        # TODO - use a thread or it will block the main thread
        # import threading

        # def _on_message(msg):
        #     self.onmessage(MessageEvent(msg))
        #     print(msg)
        #     self._readyState = EventSource.OPEN

        # def _on_error(err):
        #     self.onerror(err)
        #     self._readyState = EventSource.CLOSED

        # def _on_open(msg):
        #     self.onopen(msg)
        #     self._readyState = EventSource.OPEN

        # def _on_ready_state_change(msg):
        #     self.onreadystatechange(msg)
        #     self._readyState = EventSource.OPEN

        # def _on_close(msg):
        #     self.onclose(msg)
        #     self._readyState = EventSource.CLOSED

        # self._thread = threading.Thread(target=_do_stuff)
        # self._thread.start()

        # print('this is so cool!')

    @property
    def readyState(self):
        """ A number representing the state of the connection.
        Possible values are CONNECTING (0), OPEN (1), or CLOSED (2). """
        return self._readyState

    @property
    def url(self):
        """ A DOMString representing the URL of the source. """
        return self._url

    @property
    def withCredentials(self):
        """ A boolean value indicating whether the EventSource object was
          instantiated with cross-origin (CORS) credentials
        set (true), or not (false, the default). """
        return self._withCredentials

    def close(self):
        """ Closes the connection to the EventSource. """
        self._readyState = EventSource.CLOSED
        # close the thread
        self._thread.join()
        self._thread = None

    def onreadystatechange(self, event):
        """ Called when the state of the connection changes. """
        pass

    def onmessage(self, event):
        """ Called when a message is received. """
        if self._onmessage is not None:
            self._onmessage(event)

    def onerror(self, event):
        """ Called when an error occurs. """
        pass

    def onopen(self, event):
        """ Called when the connection is established. """
        pass

    # '''
    # NOTE - if we write custom one rather than use lib...
    # def _poll(self):

    #     if self._readyState == EventSource.CLOSED:
    #         return

    #     url = 'http://domain.com/events'
    #     headers = {
    #         'Accept': 'text/event-stream',
    #         'Cache-Control': 'no-cache',
    #         'X-requested-with': 'XMLHttpRequest'
    #     }
    #     if self._lastEventId != None:
    #         headers['Last-Event-ID'] = self._lastEventId

    #     import requests
    #     response = requests.get(url, stream=True, headers=headers)
    #    # TODO - parse repsonse
    # '''
