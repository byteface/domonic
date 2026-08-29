"""
domonic.webapi.sse
====================================
https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events

https://github.com/EventSource/eventsource/blob/master/lib/eventsource.js
https://github.com/remy/polyfills/blob/master/EventSource.js
https://github.com/Yaffle/EventSource/blob/master/src/eventsource.js

# TESTING - useage example... clone this and point at the stream
# https://github.com/byteface/SSELoggerDemo

"""

from __future__ import annotations

import threading
from typing import Any

from domonic.events import Event, EventTarget, MessageEvent
from domonic.ext.sseclient import SSEClient


class EventSource(EventTarget):
    # https://developer.mozilla.org/en-US/docs/Web/API/EventSource

    CONNECTING = 0
    OPEN = 1
    CLOSED = 2

    def __init__(
        self,
        url: str,
        eventSourceInitDict: dict[str, Any] | None = None,
        **kwargs,
    ):
        """
        The EventSource interface provides the ability to asynchronously receive messages from a server using simple push paradigm.
        """
        eventSourceInitDict = dict(eventSourceInitDict or {})
        eventSourceInitDict.update(kwargs)
        super().__init__()
        self._url = url
        self._readyState = EventSource.CONNECTING
        self._withCredentials = eventSourceInitDict.get("withCredentials", False)
        self._lastEventId = eventSourceInitDict.get("lastEventId", None)
        self._retry = eventSourceInitDict.get("retry", 3000)
        self._session = eventSourceInitDict.get("session", None)
        self._chunk_size = eventSourceInitDict.get("chunk_size", 1024)
        self._client = None
        self._thread: threading.Thread | None = None
        self._closed = False
        self._last_error: Exception | None = None

        reserved_options = {
            "autoStart",
            "auto_start",
            "blocking",
            "chunk_size",
            "lastEventId",
            "onerror",
            "onmessage",
            "onopen",
            "onreadystatechange",
            "retry",
            "session",
            "withCredentials",
        }
        self._requests_kwargs = {
            key: value
            for key, value in eventSourceInitDict.items()
            if key not in reserved_options
        }

        self._onmessage = eventSourceInitDict.get("onmessage", None)
        self._onerror = eventSourceInitDict.get("onerror", None)
        self._onopen = eventSourceInitDict.get("onopen", None)
        self._onreadystatechange = eventSourceInitDict.get("onreadystatechange", None)

        auto_start = eventSourceInitDict.get(
            "autoStart", eventSourceInitDict.get("auto_start", True)
        )
        if auto_start:
            self.start(blocking=eventSourceInitDict.get("blocking", False))

    def _set_ready_state(self, ready_state: int) -> None:
        if self._readyState == ready_state:
            return
        self._readyState = ready_state
        self.dispatchEvent(Event(Event.READYSTATECHANGE))

    def _event_from_message(self, message: Any) -> MessageEvent:
        event_type = getattr(message, "event", None) or MessageEvent.MESSAGE
        message_id = getattr(message, "id", None)
        last_event_id = self._lastEventId if message_id is None else message_id
        return MessageEvent(
            event_type,
            {
                "data": getattr(message, "data", None),
                "lastEventId": last_event_id or "",
                "origin": self._url,
                "source": self,
            },
        )

    def _dispatch_error(self, error: Exception) -> None:
        self._last_error = error
        event = Event(Event.ERROR)
        event.error = error
        self.dispatchEvent(event)

    def _run(self) -> None:
        try:
            self._client = SSEClient(
                self._url,
                last_id=self._lastEventId,
                retry=self._retry,
                session=self._session,
                chunk_size=self._chunk_size,
                **self._requests_kwargs,
            )
            if self._closed:
                return
            self._set_ready_state(EventSource.OPEN)
            self.dispatchEvent(Event(Event.OPEN))
            for message in self._client:
                if self._closed:
                    break
                if getattr(message, "retry", None) is not None:
                    self._retry = message.retry
                if getattr(message, "id", None) is not None:
                    self._lastEventId = message.id
                self.dispatchEvent(self._event_from_message(message))
        except Exception as exc:
            self._dispatch_error(exc)
        finally:
            self._set_ready_state(EventSource.CLOSED)

    def start(self, blocking: bool = False) -> "EventSource":
        """Open the stream, optionally blocking until it closes."""
        if self._thread is not None and self._thread.is_alive():
            return self
        if self._readyState == EventSource.OPEN:
            return self
        self._closed = False
        self._set_ready_state(EventSource.CONNECTING)
        if blocking:
            self._run()
            return self
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        return self

    @property
    def readyState(self):
        """A number representing the state of the connection.
        Possible values are CONNECTING (0), OPEN (1), or CLOSED (2)."""
        return self._readyState

    @property
    def url(self):
        """A DOMString representing the URL of the source."""
        return self._url

    @property
    def withCredentials(self):
        """Whether the EventSource was opened with CORS credentials."""
        return self._withCredentials

    def close(self):
        """Closes the connection to the EventSource."""
        self._closed = True
        client = getattr(self, "_client", None)
        response = getattr(client, "resp", None)
        close = getattr(response, "close", None)
        if callable(close):
            close()
        self._set_ready_state(EventSource.CLOSED)
        if (
            getattr(self, "_thread", None) is not None
            and self._thread is not threading.current_thread()
        ):
            self._thread.join(timeout=1)
            self._thread = None

    def onreadystatechange(self, event):
        """Called when the state of the connection changes."""
        if self._onreadystatechange is not None:
            self._onreadystatechange(event)

    def onmessage(self, event):
        """Called when a message is received."""
        if self._onmessage is not None:
            self._onmessage(event)

    def onerror(self, event):
        """Called when an error occurs."""
        if self._onerror is not None:
            self._onerror(event)

    def onopen(self, event):
        """Called when the connection is established."""
        if self._onopen is not None:
            self._onopen(event)
