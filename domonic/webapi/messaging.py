"""
domonic.webapi.messaging
====================================
https://developer.mozilla.org/en-US/docs/Web/API/Channel_Messaging_API
"""

from __future__ import annotations

import copy
import itertools
import weakref
from collections import defaultdict, deque
from typing import Any, ClassVar

from domonic.events import EventTarget, MessageEvent


def _clone_message(message: Any) -> Any:
    """Best-effort structured-clone stand-in for local Python messaging."""
    return copy.deepcopy(message)


class MessagePort(EventTarget):
    """One endpoint of a ``MessageChannel``.

    Ports are entangled in pairs. ``postMessage()`` on one port dispatches a
    ``message`` event at the other port. Messages are queued until the receiving
    port is started, matching the browser pattern where assigning ``onmessage``
    starts the port and ``addEventListener`` users can call ``start()``.
    """

    _ids = itertools.count(1)

    def __init__(self) -> None:
        super().__init__()
        self._id = next(self._ids)
        self._entangled: "MessagePort | None" = None
        self._closed = False
        self._started = False
        self._message_queue: deque[MessageEvent] = deque()
        self._onmessage = None
        self._onmessageerror = None

    @property
    def onmessage(self):
        return self._onmessage

    @onmessage.setter
    def onmessage(self, handler) -> None:
        self._onmessage = handler
        if handler is not None:
            self.start()

    @property
    def onmessageerror(self):
        return self._onmessageerror

    @onmessageerror.setter
    def onmessageerror(self, handler) -> None:
        self._onmessageerror = handler
        if handler is not None:
            self.start()

    @property
    def closed(self) -> bool:
        return self._closed

    def _entangle(self, other: "MessagePort") -> None:
        self._entangled = other

    def _dispatch_or_queue(self, event: MessageEvent) -> None:
        if self._closed:
            return
        if self._started:
            self.dispatchEvent(event)
            return
        self._message_queue.append(event)

    def _dispatch_messageerror(
        self, message: Any, error: Exception, source: Any, ports: list[Any]
    ) -> None:
        event = MessageEvent(
            "messageerror",
            {
                "data": message,
                "origin": "",
                "source": source,
                "ports": ports,
                "error": error,
                "bubbles": False,
                "cancelable": False,
            },
        )
        event.error = error
        self._dispatch_or_queue(event)

    def postMessage(self, message: Any, transfer: list[Any] | None = None) -> None:
        """Send a message to the entangled port."""
        if self._closed or self._entangled is None or self._entangled._closed:
            return None

        ports = list(transfer or [])
        try:
            data = _clone_message(message)
        except Exception as exc:
            self._entangled._dispatch_messageerror(message, exc, self, ports)
            return None

        event = MessageEvent(
            "message",
            {
                "data": data,
                "origin": "",
                "source": self,
                "ports": ports,
                "bubbles": False,
                "cancelable": False,
            },
        )
        self._entangled._dispatch_or_queue(event)
        return None

    def start(self) -> None:
        """Start dispatching queued messages."""
        if self._closed:
            return None
        self._started = True
        while self._message_queue and not self._closed:
            self.dispatchEvent(self._message_queue.popleft())
        return None

    def close(self) -> None:
        """Close this port and clear pending messages."""
        self._closed = True
        self._started = False
        self._message_queue.clear()
        self._entangled = None
        return None

    def __repr__(self) -> str:
        state = "closed" if self.closed else "open"
        return f"<MessagePort id={self._id} {state}>"


class MessageChannel:
    """Two-way channel containing two entangled ``MessagePort`` objects."""

    def __init__(self) -> None:
        self.port1 = MessagePort()
        self.port2 = MessagePort()
        self.port1._entangle(self.port2)
        self.port2._entangle(self.port1)


class BroadcastChannel(EventTarget):
    """Named in-process broadcast channel.

    Channels with the same name receive messages from each other. The posting
    channel does not receive its own message, matching browser behaviour.
    """

    _channels: ClassVar[dict[str, weakref.WeakSet["BroadcastChannel"]]] = defaultdict(
        weakref.WeakSet
    )

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = str(name)
        self._closed = False
        self._onmessage = None
        self._onmessageerror = None
        self._channels[self.name].add(self)

    @property
    def onmessage(self):
        return self._onmessage

    @onmessage.setter
    def onmessage(self, handler) -> None:
        self._onmessage = handler

    @property
    def onmessageerror(self):
        return self._onmessageerror

    @onmessageerror.setter
    def onmessageerror(self, handler) -> None:
        self._onmessageerror = handler

    @property
    def closed(self) -> bool:
        return self._closed

    def postMessage(self, message: Any) -> None:
        """Broadcast a message to other open channels with the same name."""
        if self._closed:
            return None
        for channel in list(self._channels.get(self.name, ())):
            if channel is self or channel._closed:
                continue
            try:
                data = _clone_message(message)
            except Exception as exc:
                channel._dispatch_messageerror(message, exc)
                continue
            channel.dispatchEvent(
                MessageEvent(
                    "message",
                    {
                        "data": data,
                        "origin": "",
                        "source": self,
                        "ports": [],
                        "bubbles": False,
                        "cancelable": False,
                    },
                )
            )
        return None

    def _dispatch_messageerror(self, message: Any, error: Exception) -> None:
        event = MessageEvent(
            "messageerror",
            {
                "data": message,
                "origin": "",
                "source": None,
                "ports": [],
                "error": error,
                "bubbles": False,
                "cancelable": False,
            },
        )
        event.error = error
        self.dispatchEvent(event)

    def close(self) -> None:
        """Leave the named channel and stop receiving broadcasts."""
        if self._closed:
            return None
        self._closed = True
        channels = self._channels.get(self.name)
        if channels is not None:
            channels.discard(self)
            if not channels:
                self._channels.pop(self.name, None)
        return None

    def __repr__(self) -> str:
        state = "closed" if self.closed else "open"
        return f"<BroadcastChannel name={self.name!r} {state}>"


__all__ = ["BroadcastChannel", "MessageChannel", "MessageEvent", "MessagePort"]
