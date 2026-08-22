"""
domonic.events
==============

DOM-style event classes and dispatch machinery for domonic.

This module provides ``EventTarget`` plus a broad set of web-platform-flavoured
event classes so DOM nodes, windows, animations, and helper objects can share a
common event model.
"""

from __future__ import annotations

import inspect
import time
from typing import Any, Callable, ClassVar

from domonic.constants.keyboard import (
    Code,
    Key,
    KeyCode,
    KeyLocation,
    normalize_code,
    normalize_key,
)


class EventListener:
    """Interface-style base for listener objects with ``handleEvent()``."""

    def handleEvent(self, event: "Event") -> Any:
        """Handle an event passed by ``EventTarget`` dispatch."""
        raise NotImplementedError


class EventListenerOptions(dict):
    """Dictionary-like helper for DOM listener options.

    Supports the common ``capture``, ``once``, ``passive``, and ``signal``
    fields accepted by ``addEventListener()``.
    """

    def __init__(
        self,
        capture: bool = False,
        once: bool = False,
        passive: bool = False,
        signal: Any = None,
    ) -> None:
        super().__init__(capture=capture, once=once, passive=passive, signal=signal)


class EventTarget:
    """DOM-style event target base class.

    Extend ``EventTarget`` to give an object support for
    ``addEventListener()``, ``removeEventListener()``, and ``dispatchEvent()``
    with DOM-like capture, target, and bubble semantics where appropriate.
    """

    def __init__(self, *args, **kwargs) -> None:
        self.listeners: dict[str, list[Callable[..., Any]]] = {}
        self._listener_options: dict[str, list[dict[str, Any]]] = {}

    def hasEventListener(self, eventType: str) -> bool:
        """
        Check if an event listener for the given event type exists.

        Args:
            eventType (str): The type of the event.

        Returns:
            bool: True if listeners for the event type exist, otherwise False.
        """
        return bool(self.listeners.get(eventType))

    @staticmethod
    def _normalize_listener_options(
        options: bool | dict[str, Any] | None = None, **kwargs: Any
    ) -> dict[str, Any]:
        normalized: dict[str, Any] = {
            "capture": False,
            "once": False,
            "passive": False,
            "signal": None,
        }
        if isinstance(options, bool):
            normalized["capture"] = options
        elif isinstance(options, dict):
            normalized["capture"] = bool(options.get("capture", False))
            normalized["once"] = bool(options.get("once", False))
            normalized["passive"] = bool(options.get("passive", False))
            normalized["signal"] = options.get("signal")

        if "use_capture" in kwargs:
            normalized["capture"] = bool(kwargs["use_capture"])
        if "capture" in kwargs:
            normalized["capture"] = bool(kwargs["capture"])
        if "once" in kwargs:
            normalized["once"] = bool(kwargs["once"])
        if "passive" in kwargs:
            normalized["passive"] = bool(kwargs["passive"])
        if "signal" in kwargs:
            normalized["signal"] = kwargs["signal"]
        return normalized

    def _get_event_path(self, target: Any) -> list[Any]:
        path: list[Any] = []
        current = target
        seen: set[int] = set()
        while current is not None and id(current) not in seen:
            path.append(current)
            seen.add(id(current))
            if (
                hasattr(current, "parentNode")
                and getattr(current, "parentNode", None) is not None
            ):
                current = current.parentNode
                continue
            owner_document = getattr(current, "ownerDocument", None)
            if owner_document is not None and owner_document is not current:
                current = owner_document
                continue
            default_view = getattr(current, "defaultView", None)
            if default_view is not None and default_view is not current:
                current = default_view
                continue
            break
        return path

    def _invoke_listeners(
        self, current_target: Any, event: "Event", capture: bool
    ) -> None:
        event_type = event.type
        listeners = list(
            getattr(current_target, "_listener_options", {}).get(event_type, [])
        )
        event.currentTarget = current_target
        event.srcElement = event.target
        event.eventPhase = (
            Event.AT_TARGET
            if current_target is event.target
            else (Event.CAPTURING_PHASE if capture else Event.BUBBLING_PHASE)
        )

        for listener in listeners:
            if listener["capture"] != capture:
                continue
            callback = listener["callback"]
            event._in_passive_listener = listener["passive"]
            try:
                if hasattr(callback, "handleEvent"):
                    result = callback.handleEvent(event)
                else:
                    result = callback(event)
                if result is False:
                    event.preventDefault()
            finally:
                event._in_passive_listener = False
                if listener["once"]:
                    current_target.removeEventListener(
                        event_type, callback, listener["capture"]
                    )
            if event._immediate_propagation_stopped:
                return

        if capture is False:
            handler = getattr(current_target, f"on{event_type}", None)
            if callable(handler):
                result = handler(event)
                if result is False:
                    event.preventDefault()

    def addEventListener(
        self,
        eventType: str,
        callback: Callable[..., Any] | None,
        options: bool | dict[str, Any] | None = None,
        *args,
        **kwargs,
    ) -> None:
        """Add an event listener for the given event type.

        Args:
            eventType (str): The type of the event to listen for.
            callback (Callable): The callback function to be executed when the event occurs.
            options: A DOM-style options dictionary or legacy capture boolean.

        ``options`` may contain ``capture``, ``once``, ``passive``, and
        ``signal``. Duplicate listeners with the same callback and capture
        value are ignored, matching DOM listener registration behavior.
        """
        if callback is None:
            return
        if eventType not in self.listeners:
            self.listeners[eventType] = []
            self._listener_options[eventType] = []
        listener_options = self._normalize_listener_options(options, **kwargs)
        signal = listener_options.get("signal")
        if signal is not None:
            if getattr(signal, "aborted", False):
                return
        for listener in self._listener_options[eventType]:
            if (
                listener["callback"] is callback
                and listener["capture"] == listener_options["capture"]
            ):
                return
        self.listeners[eventType].append(callback)
        self._listener_options[eventType].append(
            {"callback": callback, **listener_options}
        )
        if signal is not None and hasattr(signal, "addEventListener"):

            def _remove_on_abort(
                event: Any,
                target=self,
                ev_type=eventType,
                cb=callback,
                capture=listener_options["capture"],
            ):
                target.removeEventListener(ev_type, cb, {"capture": capture})

            signal.addEventListener("abort", _remove_on_abort, {"once": True})

    def removeEventListener(
        self,
        eventType: str,
        callback: Callable[..., Any] | None,
        options: bool | dict[str, Any] | None = None,
    ) -> None:
        """Remove an event listener for the given event type.

        Args:
            eventType (str): The type of the event.
            callback (Callable): The callback function to be removed.
            options: A DOM-style options dictionary or legacy capture boolean.
        """
        if callback is None or eventType not in self.listeners:
            return
        capture = self._normalize_listener_options(options)["capture"]
        callbacks = self.listeners[eventType]
        listeners = self._listener_options.get(eventType, [])
        for index, listener in enumerate(listeners):
            if listener["callback"] is callback and listener["capture"] == capture:
                listeners.pop(index)
                if index < len(callbacks):
                    callbacks.pop(index)
                break
        if not listeners:
            self._listener_options.pop(eventType, None)
            self.listeners.pop(eventType, None)

    @staticmethod
    def _coerce_event(event: Any) -> "Event":
        if isinstance(event, Event):
            return event
        if isinstance(event, str):
            return Event(event)
        if isinstance(event, dict):
            return Event(event.get("type", ""), event)
        raise TypeError("dispatchEvent() expects an Event, event type, or mapping")

    def dispatchEvent(self, event: Any) -> bool:
        """Dispatch the specified event to registered listeners.

        Args:
            event: An ``Event`` instance, event type string, or event mapping.

        Returns:
            bool: ``False`` when a cancelable event had its default prevented,
            otherwise ``True``.
        """
        event = self._coerce_event(event)
        event.target = self
        event.currentTarget = self
        event.srcElement = self
        event.cancelBubble = False
        event._propagation_stopped = False
        event._immediate_propagation_stopped = False
        event._in_passive_listener = False
        event._dispatching = True

        path = self._get_event_path(self)
        event._path = path
        capture_targets = list(reversed(path[1:]))
        bubble_targets = path[1:] if event.bubbles else []

        try:
            for target in capture_targets:
                self._invoke_listeners(target, event, capture=True)
                if event._propagation_stopped:
                    return not event.defaultPrevented

            self._invoke_listeners(self, event, capture=True)
            if not event._immediate_propagation_stopped:
                self._invoke_listeners(self, event, capture=False)

            if event._propagation_stopped:
                return not event.defaultPrevented

            for target in bubble_targets:
                self._invoke_listeners(target, event, capture=False)
                if event._propagation_stopped:
                    break
            return not event.defaultPrevented
        finally:
            event._dispatching = False
            event.eventPhase = Event.NONE
            event.currentTarget = None
            event._in_passive_listener = False

    async def dispatchEventAsync(self, event: Any) -> bool:
        """Dispatch the specified event to sync and async listeners.

        Args:
            event: An ``Event`` instance, event type string, or event mapping.

        Returns:
            bool: ``False`` when a cancelable event had its default prevented,
            otherwise ``True``.

        **Usage:**

        To dispatch an event asynchronously, use the ``await`` keyword when calling this method.

        **Example:**

        .. code-block:: python

            event_data = {"message": "Hello, world!"}
            async_event = {"type": "async_event", "data": event_data}
            await target.dispatchEventAsync(async_event)
        """
        event = self._coerce_event(event)
        event.target = self
        event.currentTarget = self
        event.srcElement = self
        event.cancelBubble = False
        event._propagation_stopped = False
        event._immediate_propagation_stopped = False
        event._in_passive_listener = False
        event._dispatching = True

        async def call_listener(
            callback: Callable[..., Any], current_target: Any, capture: bool
        ) -> Any:
            event.currentTarget = current_target
            event.srcElement = event.target
            event.eventPhase = (
                Event.AT_TARGET
                if current_target is event.target
                else (Event.CAPTURING_PHASE if capture else Event.BUBBLING_PHASE)
            )
            if hasattr(callback, "handleEvent"):
                result = callback.handleEvent(event)
            else:
                result = callback(event)
            if inspect.isawaitable(result):
                result = await result
            return result

        async def invoke(current_target: Any, capture: bool) -> None:
            listeners = list(
                getattr(current_target, "_listener_options", {}).get(event.type, [])
            )
            for listener in listeners:
                if listener["capture"] != capture:
                    continue
                event._in_passive_listener = listener["passive"]
                try:
                    result = await call_listener(
                        listener["callback"], current_target, capture
                    )
                    if result is False:
                        event.preventDefault()
                finally:
                    event._in_passive_listener = False
                    if listener["once"]:
                        current_target.removeEventListener(
                            event.type, listener["callback"], listener["capture"]
                        )
                if event._immediate_propagation_stopped:
                    return
            if capture is False:
                handler = getattr(current_target, f"on{event.type}", None)
                if callable(handler):
                    event.currentTarget = current_target
                    event.srcElement = event.target
                    event.eventPhase = (
                        Event.AT_TARGET
                        if current_target is event.target
                        else Event.BUBBLING_PHASE
                    )
                    result = handler(event)
                    if inspect.isawaitable(result):
                        result = await result
                    if result is False:
                        event.preventDefault()

        path = self._get_event_path(self)
        event._path = path
        try:
            for target in reversed(path[1:]):
                await invoke(target, True)
                if event._propagation_stopped:
                    return not event.defaultPrevented

            await invoke(self, True)
            if not event._immediate_propagation_stopped:
                await invoke(self, False)

            if event._propagation_stopped or not event.bubbles:
                return not event.defaultPrevented

            for target in path[1:]:
                await invoke(target, False)
                if event._propagation_stopped:
                    break
            return not event.defaultPrevented
        finally:
            event._dispatching = False
            event.eventPhase = Event.NONE
            event.currentTarget = None
            event._in_passive_listener = False


EventDispatcher = EventTarget  #: legacy alias


class Event:
    """Base DOM event with propagation, cancelation, and path state."""

    # Constants for event types
    EMPTIED: str = "emptied"  #:
    ABORT: str = "abort"  #:
    ADDTRACK: str = "addtrack"  #:
    AFTERPRINT: str = "afterprint"  #:
    ANIMATIONCANCEL: str = "animationcancel"  #:
    ANIMATIONEND: str = "animationend"  #:
    ANIMATIONITERATION: str = "animationiteration"  #:
    ANIMATIONSTART: str = "animationstart"  #:
    AUXCLICK: str = "auxclick"  #:
    BEFOREINPUT: str = "beforeinput"  #:
    BEFOREMATCH: str = "beforematch"  #:
    BEFOREPRINT: str = "beforeprint"  #:
    BEFORETOGGLE: str = "beforetoggle"  #:
    BEFOREUNLOAD: str = "beforeunload"  #:
    BLUR: str = "blur"  #:
    CANCEL: str = "cancel"  #:
    CANPLAY: str = "canplay"  #:
    CANPLAYTHROUGH: str = "canplaythrough"  #:
    CHANGE: str = "change"  #:
    CLICK: str = "click"  #:
    CLOSE: str = "close"  #:
    COMMAND: str = "command"  #:
    CONNECT: str = "connect"  #:
    CONTEXTLOST: str = "contextlost"  #:
    CONTEXTRESTORED: str = "contextrestored"  #:
    CURRENTENTRYCHANGE: str = "currententrychange"  #:
    DATAAVAILABLE: str = "dataavailable"  #:
    DEVICELIGHT: str = "devicelight"  #:
    DEVICEMOTION: str = "devicemotion"  #:
    DEVICEORIENTATION: str = "deviceorientation"  #:
    DEVICEORIENTATIONABSOLUTE: str = "deviceorientationabsolute"  #:
    DEVICEPROXIMITY: str = "deviceproximity"  #:
    DISPOSE: str = "dispose"  #:
    DOMCONTENTLOADED: str = "DOMContentLoaded"  #:
    DURATIONCHANGE: str = "durationchange"  #:
    ENDED: str = "ended"  #:
    ERROR: str = "error"  #:
    FOCUS: str = "focus"  #:
    FORMDATA: str = "formdata"  #:
    FULLSCREENCHANGE: str = "fullscreenchange"  #:
    FULLSCREENERROR: str = "fullscreenerror"  #:
    HASHCHANGE: str = "hashchange"  #:
    INPUT: str = "input"  #:
    INVALID: str = "invalid"  #:
    LANGUAGECHANGE: str = "languagechange"  #:
    LOAD: str = "load"  #:
    LOADEDDATA: str = "loadeddata"  #:
    LOADEDMETADATA: str = "loadedmetadata"  #:
    MESSAGE: str = "message"  #:
    MESSAGEERROR: str = "messageerror"  #:
    MOUSEENTER: str = "mouseenter"  #:
    MOUSELEAVE: str = "mouseleave"  #:
    NAVIGATE: str = "navigate"  #:
    NAVIGATEERROR: str = "navigateerror"  #:
    NAVIGATESUCCESS: str = "navigatesuccess"  #:
    OFFLINE: str = "offline"  #:
    ONLINE: str = "online"  #:
    OPEN: str = "open"  #:
    PAGEHIDE: str = "pagehide"  #:
    PAGEREVEAL: str = "pagereveal"  #:
    PAGESHOW: str = "pageshow"  #:
    PAGESWAP: str = "pageswap"  #:
    PAUSE: str = "pause"  #:
    PLAY: str = "play"  #:
    PLAYING: str = "playing"  #:
    POINTERCANCEL: str = "pointercancel"  #:
    POPSTATE: str = "popstate"  #:
    PROGRESS: str = "progress"  #:
    RATECHANGE: str = "ratechange"  #:
    READYSTATECHANGE: str = "readystatechange"  #:
    REMOVETRACK: str = "removetrack"  #:
    RESIZE: str = "resize"  #:
    REJECTIONHANDLED: str = "rejectionhandled"  #:
    RESET: str = "reset"  #:
    SCROLL: str = "scroll"  #:
    SCROLLEND: str = "scrollend"  #:
    SEARCH: str = "search"  #:
    SECURITYPOLICYVIOLATION: str = "securitypolicyviolation"  #:
    SEEKED: str = "seeked"  #:
    SEEKING: str = "seeking"  #:
    SELECT: str = "select"  #:
    SHOW: str = "show"  #:
    SLOTCHANGE: str = "slotchange"  #:
    STALLED: str = "stalled"  #:
    STORAGE: str = "storage"  #:
    SUBMIT: str = "submit"  #:
    SUSPEND: str = "suspend"  #:
    TOGGLE: str = "toggle"  #:
    TRANSITIONCANCEL: str = "transitioncancel"  #:
    TRANSITIONEND: str = "transitionend"  #:
    UNHANDLEDREJECTION: str = "unhandledrejection"  #:
    UNLOAD: str = "unload"  #:
    VISIBILITYCHANGE: str = "visibilitychange"  #:
    VOLUMECHANGE: str = "volumechange"  #:
    WAITING: str = "waiting"  #:
    WEBGLCONTEXTCREATIONERROR: str = "webglcontextcreationerror"  #:
    WEBGLCONTEXTLOST: str = "webglcontextlost"  #:
    WEBGLCONTEXTRESTORED: str = "webglcontextrestored"  #:

    NONE: int = 0
    CAPTURING_PHASE: int = 1
    AT_TARGET: int = 2
    BUBBLING_PHASE: int = 3

    def __str__(self) -> str:
        return self.type + ":" + str(self.timeStamp)

    def __init__(
        self, _type: str = "", options: dict[str, Any] | None = None, *args, **kwargs
    ) -> None:
        """Create an event from an event type and optional initializer values.

        ``options`` accepts the common DOM ``EventInit`` fields such as
        ``bubbles``, ``cancelable``, and ``composed``. Keyword arguments are
        also accepted for backwards-compatible domonic call sites.
        """
        options = options or kwargs  # if options is none use kwargs
        self.type: str = _type
        self.bubbles: bool = options.get("bubbles", False)
        self.cancelable: bool = options.get("cancelable", False)
        self._cancelBubble: bool = False
        self.composed: bool = options.get("composed", False)
        self.currentTarget: object = options.get("currentTarget", None)
        self.defaultPrevented: bool = bool(options.get("defaultPrevented", False))
        self.eventPhase: int = options.get("eventPhase", Event.NONE)
        self.explicitOriginalTarget: object = options.get(
            "explicitOriginalTarget", None
        )
        self.isTrusted: bool = options.get("isTrusted", False)
        self.originalTarget: object = options.get("originalTarget", None)
        self._returnValue: bool = not self.defaultPrevented
        self.srcElement: object = options.get("srcElement", None)
        self.target: object = options.get("target", None)
        self.timeStamp: float = time.time_ns() / 1_000_000
        self._propagation_stopped: bool = False
        self._immediate_propagation_stopped: bool = False
        self._in_passive_listener: bool = False
        self._dispatching: bool = False
        self._path: list[Any] | None = None
        self.cancelBubble = options.get("cancelBubble", False)
        if "returnValue" in options:
            self.returnValue = options["returnValue"]

    @property
    def cancelBubble(self) -> bool:
        return self._cancelBubble

    @cancelBubble.setter
    def cancelBubble(self, value: bool) -> None:
        self._cancelBubble = bool(value)
        if self._cancelBubble:
            self._propagation_stopped = True

    @property
    def returnValue(self) -> bool:
        return self._returnValue

    @returnValue.setter
    def returnValue(self, value: bool) -> None:
        self._returnValue = bool(value)
        self.defaultPrevented = not self._returnValue

    def composedPath(self):
        """Return the event path captured during dispatch."""
        if self._path is not None:
            return list(self._path)
        path = []
        current_target = self.target
        while current_target is not None:
            path.append(current_target)
            if hasattr(current_target, "parentNode"):
                current_target = current_target.parentNode
            else:
                break
        # Include a document/window default view when the target chain exposes one.
        if path:
            last = path[-1]
            default_view = getattr(last, "defaultView", None)
            if default_view is not None and default_view not in path:
                path.append(default_view)
        return path

    def initEvent(
        self,
        _type: str | None = None,
        bubbles: bool = False,
        cancelable: bool = False,
        *args,
        **kwargs,
    ) -> "Event":
        """Reinitialize the event when it is not currently dispatching."""
        if self._dispatching:
            return self
        self.type = _type or self.type
        self.bubbles = bubbles
        self.cancelable = cancelable
        self.cancelBubble = False
        self.defaultPrevented = False
        self.currentTarget = None
        self.eventPhase = Event.NONE
        self._propagation_stopped = False
        self._immediate_propagation_stopped = False
        self._path = None
        return self

    def stopPropagation(self):
        """Prevent further propagation in the capture and bubble phases."""
        self.cancelBubble = True
        self._propagation_stopped = True

    def msConvertURL(self, url):
        """Convert a URL using domonic's legacy Microsoft-style helper.

        Args:
            url (str): The URL to be converted.

        Returns:
            str: A ``javascript:window.open(...)`` wrapper for HTTP(S) URLs,
            otherwise the original URL.
        """
        if url.startswith("http"):
            return f'javascript:window.open("{url}");'
        return url

    def preventDefault(self) -> None:
        """Mark the default action as prevented when the event is cancelable."""
        if self.cancelable and not self._in_passive_listener:
            self.defaultPrevented = True
            self.returnValue = False

    def stopImmediatePropagation(self) -> None:
        """Stop propagation and skip remaining listeners on the current target."""
        self.cancelBubble = True
        self._propagation_stopped = True
        self._immediate_propagation_stopped = True


class AbortSignal(EventTarget):
    """Signal object used to communicate cancellation."""

    def __init__(self) -> None:
        super().__init__()
        self.aborted: bool = False
        self.reason: Any = None
        self.onabort = None

    def _signal_abort(self, reason: Any = None) -> None:
        if self.aborted:
            return
        self.aborted = True
        self.reason = reason
        self.dispatchEvent(Event(Event.ABORT))

    def throwIfAborted(self) -> None:
        if self.aborted:
            raise RuntimeError(
                self.reason if self.reason is not None else "Signal already aborted"
            )


class AbortController:
    """Controller used to abort work associated with an AbortSignal."""

    def __init__(self) -> None:
        self.signal = AbortSignal()

    def abort(self, reason: Any = None) -> None:
        self.signal._signal_abort(reason)


class UIEvent(Event):
    """Event carrying view, detail, and UI coordinate context."""

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        """Create a UI event from an event type and UI initializer values.

        Args:
            _type (str): The type of the UIEvent.
            options: UI event initializer values such as ``view`` and ``detail``.
        """
        options = options or kwargs  # If options is None, use kwargs
        self.canBubble = options.get("canBubble", None)
        self.cancelable = options.get("cancelable", None)
        self.detail = options.get("detail", None)
        self.view = options.get("view", None)
        self.layerX = options.get("layerX", None)
        self.layerY = options.get("layerY", None)
        self.sourceCapabilities = options.get("sourceCapabilities", None)
        super().__init__(_type, options, *args, **kwargs)

    def initUIEvent(
        self, _type: str, canBubble: bool, cancelable: bool, view, detail
    ) -> "UIEvent":
        """
        Initialize a UIEvent with specific parameters.

        Args:
            _type (str): The type of the UIEvent.
            canBubble (bool): Specifies whether the event should bubble.
            cancelable (bool): Specifies whether the event is cancelable.
            view: The associated view or window.
            detail: Additional event-specific detail.

        Returns:
            UIEvent: The initialized UIEvent object.
        """
        self.initEvent(_type, canBubble, cancelable)
        self.canBubble = canBubble
        self.view = view
        self.detail = detail
        return self


class MouseEvent(UIEvent):
    """Mouse input event with button, coordinate, and modifier state."""

    CLICK: str = "click"  #:
    CONTEXTMENU: str = "contextmenu"  #:
    DBLCLICK: str = "dblclick"  #:
    MOUSEDOWN: str = "mousedown"  #:
    MOUSEENTER: str = "mouseenter"  #:
    MOUSELEAVE: str = "mouseleave"  #:
    MOUSEMOVE: str = "mousemove"  #:
    MOUSEOVER: str = "mouseover"  #:
    MOUSEOUT: str = "mouseout"  #:
    MOUSEUP: str = "mouseup"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        """Create a mouse event from standard mouse initializer values."""
        options = options or kwargs
        self.canBubble = options.get("canBubble", None)
        self.cancelable = options.get("cancelable", None)
        self.screenX = options.get("screenX", 0)
        self.screenY = options.get("screenY", 0)
        self._clientX = options.get("clientX", 0)
        self._clientY = options.get("clientY", 0)
        self.x = options.get("x", self._clientX)
        self.y = options.get("y", self._clientY)
        self.pageX = options.get("pageX", self._clientX)
        self.pageY = options.get("pageY", self._clientY)
        self.offsetX = options.get("offsetX", self._clientX)
        self.offsetY = options.get("offsetY", self._clientY)
        self.movementX = options.get("movementX", 0)
        self.movementY = options.get("movementY", 0)
        self.layerX = options.get("layerX", self._clientX)
        self.layerY = options.get("layerY", self._clientY)
        self.relatedTarget = options.get("relatedTarget", None)
        self.region = options.get("region", None)
        self._altKey: bool = options.get("altKey", False)
        self._ctrlKey: bool = options.get("ctrlKey", False)
        self._shiftKey: bool = options.get("shiftKey", False)
        self._metaKey: bool = options.get("metaKey", False)
        self._button = options.get("button", 0)
        self._buttons = options.get("buttons", 0)
        super().__init__(_type, options, *args, **kwargs)
        self.layerX = options.get("layerX", self._clientX)
        self.layerY = options.get("layerY", self._clientY)

    def initMouseEvent(
        self,
        _type: str = None,
        canBubble: bool = True,
        cancelable: bool = True,
        view=None,
        detail=None,
        screenX: float = 0,
        screenY: float = 0,
        clientX: float = 0,
        clientY: float = 0,
        ctrlKey: bool = False,
        altKey: bool = False,
        shiftKey: bool = False,
        metaKey: bool = False,
        button=None,
        relatedTarget=None,
        from_json=None,
        *args,
        **kwargs,
    ) -> "MouseEvent":
        """Legacy initializer for updating an existing mouse event."""
        from_json = from_json or {}
        self.initEvent(_type or self.type, canBubble, cancelable)
        self.canBubble = canBubble
        self.view = view
        self.detail = detail
        self.screenX = screenX
        self.screenY = screenY
        self.x = clientX
        self.y = clientY
        self._clientX = clientX
        self._clientY = clientY
        self._ctrlKey = ctrlKey
        self._altKey = altKey
        self._shiftKey = shiftKey
        self._metaKey = metaKey
        self._button = 0 if button is None else button
        self._buttons = 0 if button is None else 1 << int(button)
        self.relatedTarget = relatedTarget
        for name in (
            "screenX",
            "screenY",
            "clientX",
            "clientY",
            "ctrlKey",
            "altKey",
            "shiftKey",
            "metaKey",
            "button",
            "buttons",
            "relatedTarget",
        ):
            if name in from_json:
                if name == "clientX":
                    self._clientX = from_json[name]
                    self.x = from_json[name]
                elif name == "clientY":
                    self._clientY = from_json[name]
                    self.y = from_json[name]
                elif name == "ctrlKey":
                    self._ctrlKey = from_json[name]
                elif name == "altKey":
                    self._altKey = from_json[name]
                elif name == "shiftKey":
                    self._shiftKey = from_json[name]
                elif name == "metaKey":
                    self._metaKey = from_json[name]
                elif name == "button":
                    self._button = from_json[name]
                elif name == "buttons":
                    self._buttons = from_json[name]
                else:
                    setattr(self, name, from_json[name])
        return self

    @property
    def clientX(self):
        return self._clientX

    @property
    def clientY(self):
        return self._clientY

    @property
    def altKey(self):
        return self._altKey

    @property
    def ctrlKey(self):
        return self._ctrlKey

    @property
    def shiftKey(self):
        return self._shiftKey

    @property
    def metaKey(self):
        return self._metaKey

    @property
    def button(self):
        return self._button

    @property
    def buttons(self):
        return self._buttons

    @property
    def which(self):
        return 0 if self._button is None else int(self._button) + 1

    def getModifierState(self, keyArg: str):
        """Return whether the named modifier key was active for the event."""
        lookup = {
            "Alt": self.altKey,
            "Control": self.ctrlKey,
            "Meta": self.metaKey,
            "Shift": self.shiftKey,
        }
        return lookup.get(keyArg, False)


def _infer_char_code(key: str) -> int:
    if len(key) == 1:
        return ord(key)
    return 0


def _infer_legacy_keycode(key: str) -> int:
    inferred = KeyCode.from_key(key)
    return inferred if inferred is not None else 0


def _infer_code_from_key_and_location(key: str, location: int) -> str:
    key_to_code = {
        Key.ENTER: Code.NUMPAD_ENTER if location == KeyLocation.NUMPAD else Code.ENTER,
        Key.TAB: Code.TAB,
        Key.SPACE: Code.SPACE,
        Key.ESCAPE: Code.ESCAPE,
        Key.BACKSPACE: Code.BACKSPACE,
        Key.DELETE: Code.DELETE,
        Key.INSERT: Code.INSERT,
        Key.HOME: Code.HOME,
        Key.END: Code.END,
        Key.PAGE_UP: Code.PAGE_UP,
        Key.PAGE_DOWN: Code.PAGE_DOWN,
        Key.ARROW_LEFT: Code.ARROW_LEFT,
        Key.ARROW_RIGHT: Code.ARROW_RIGHT,
        Key.ARROW_UP: Code.ARROW_UP,
        Key.ARROW_DOWN: Code.ARROW_DOWN,
        Key.SHIFT: (
            Code.SHIFT_RIGHT if location == KeyLocation.RIGHT else Code.SHIFT_LEFT
        ),
        Key.CONTROL: (
            Code.CONTROL_RIGHT if location == KeyLocation.RIGHT else Code.CONTROL_LEFT
        ),
        Key.ALT: Code.ALT_RIGHT if location == KeyLocation.RIGHT else Code.ALT_LEFT,
        Key.META: Code.META_RIGHT if location == KeyLocation.RIGHT else Code.META_LEFT,
        Key.CAPS_LOCK: Code.CAPS_LOCK,
        Key.NUM_LOCK: Code.NUM_LOCK,
        Key.SCROLL_LOCK: Code.SCROLL_LOCK,
        Key.CONTEXT_MENU: Code.CONTEXT_MENU,
    }
    if key in key_to_code:
        return key_to_code[key]
    normalized_code = normalize_code(key)
    if normalized_code:
        return normalized_code
    return ""


class KeyboardEvent(UIEvent):
    """Keyboard input event with normalized key, code, and modifier state."""

    KEYDOWN: str = "keydown"  #:
    KEYPRESS: str = "keypress"  #:
    KEYUP: str = "keyup"  #:

    DOM_KEY_LOCATION_STANDARD: int = KeyLocation.STANDARD  #:
    DOM_KEY_LOCATION_LEFT: int = KeyLocation.LEFT  #:
    DOM_KEY_LOCATION_RIGHT: int = KeyLocation.RIGHT  #:
    DOM_KEY_LOCATION_NUMPAD: int = KeyLocation.NUMPAD  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        """Create a keyboard event from standard keyboard initializer values."""
        options = options or kwargs  # if options is none use kwargs
        self.canBubble = options.get("canBubble", None)
        self.cancelable = options.get("cancelable", None)
        self._altKey: bool = options.get("altKey", False)
        self._ctrlKey: bool = options.get("ctrlKey", False)
        self._shiftKey: bool = options.get("shiftKey", False)
        self._metaKey: bool = options.get("metaKey", False)

        self.location = options.get("location", self.DOM_KEY_LOCATION_STANDARD)
        self.repeat = bool(options.get("repeat", False))
        self.isComposing = bool(options.get("isComposing", False))
        self._modifier_states = {
            "Alt": self._altKey,
            "Control": self._ctrlKey,
            "Meta": self._metaKey,
            "Shift": self._shiftKey,
            "CapsLock": bool(options.get("capsLock", False)),
            "NumLock": bool(options.get("numLock", False)),
            "ScrollLock": bool(options.get("scrollLock", False)),
            "AltGraph": bool(options.get("altGraph", False)),
        }

        raw_key = options.get("key", "")
        raw_code = options.get("code", "")
        raw_key_code = options.get("keyCode", None)
        self.key = normalize_key(raw_key)
        self.code = (
            normalize_code(raw_code)
            or KeyCode.to_code(raw_key_code)
            or _infer_code_from_key_and_location(self.key, self.location)
        )
        self.keyCode = (
            int(raw_key_code)
            if raw_key_code not in (None, "")
            else _infer_legacy_keycode(self.key)
        )
        self.charCode = int(options.get("charCode", _infer_char_code(self.key)))

        super().__init__(_type, options, *args, **kwargs)

    def initKeyboardEvent(
        self,
        typeArg: str,
        canBubbleArg: bool,
        cancelableArg: bool,
        viewArg,
        charArg,
        keyArg,
        locationArg,
        modifiersListArg,
        repeat,
    ) -> "KeyboardEvent":
        """Legacy initializer for updating an existing keyboard event."""
        self.initEvent(typeArg, canBubbleArg, cancelableArg)
        self.canBubbleArg = canBubbleArg
        self.cancelableArg = cancelableArg
        self.view = viewArg
        self.viewArg = viewArg
        self.charCode = charArg
        self.key = normalize_key(keyArg)
        self.location = locationArg
        self.locationArg = locationArg
        self.modifiersListArg = modifiersListArg
        modifiers = {
            modifier.strip().lower()
            for modifier in str(modifiersListArg).split()
            if modifier
        }
        self._altKey = "alt" in modifiers
        self._ctrlKey = "control" in modifiers or "ctrl" in modifiers
        self._metaKey = "meta" in modifiers
        self._shiftKey = "shift" in modifiers
        self._modifier_states.update(
            {
                "Alt": self._altKey,
                "Control": self._ctrlKey,
                "Meta": self._metaKey,
                "Shift": self._shiftKey,
            }
        )
        self.code = _infer_code_from_key_and_location(self.key, self.location)
        self.keyCode = _infer_legacy_keycode(self.key)
        self.repeat = repeat
        return self

    @property
    def altKey(self):
        return self._altKey

    @property
    def ctrlKey(self):
        return self._ctrlKey

    @property
    def shiftKey(self):
        return self._shiftKey

    @property
    def metaKey(self):
        return self._metaKey

    @property
    def unicode(self):
        return self.key

    def getModifierState(self, keyArg: str) -> bool:
        """Return whether the named modifier key was active for the event."""
        return self._modifier_states.get(keyArg, False)


class CompositionEvent(UIEvent):
    """Input method editor composition event."""

    START: str = "compositionstart"
    END: str = "compositionend"
    UPDATE: str = "compositionupdate"

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.data = options.get("data", None)
        self.locale = options.get("locale", None)
        super().__init__(_type, options, *args, **kwargs)


class FocusEvent(UIEvent):
    """Focus transition event with an optional related target."""

    BLUR: str = "blur"  #:
    FOCUS: str = "focus"  #:
    FOCUSIN: str = "focusin"  #:
    FOCUSOUT: str = "focusout"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.relatedTarget = options.get("relatedTarget", None)
        super().__init__(_type, options, *args, **kwargs)


class TouchEvent(UIEvent):
    """Touch input event with active, target, and changed touch lists."""

    TOUCHCANCEL: str = "touchcancel"  #:
    TOUCHEND: str = "touchend"  #:
    TOUCHMOVE: str = "touchmove"  #:
    TOUCHSTART: str = "touchstart"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.shiftKey = options.get("shiftKey", False)
        self.altKey = options.get("altKey", False)
        self.changedTouches = options.get("changedTouches", [])
        self.ctrlKey = options.get("ctrlKey", False)
        self.metaKey = options.get("metaKey", False)
        self.shiftKey = options.get("shiftKey", False)
        self.targetTouches = options.get("targetTouches", [])
        self.touches = options.get("touches", [])
        super().__init__(_type, options, *args, **kwargs)

    def getModifierState(self, keyArg: str):
        """Return whether the named modifier key was active for the event."""
        lookup = {
            "Alt": self.altKey,
            "Control": self.ctrlKey,
            "Meta": self.metaKey,
            "Shift": self.shiftKey,
        }
        return lookup.get(keyArg, False)


class WheelEvent(UIEvent):
    """Wheel input event with delta values and delta mode constants."""

    DOM_DELTA_PIXEL: int = 0
    DOM_DELTA_LINE: int = 1
    DOM_DELTA_PAGE: int = 2

    MOUSEWHEEL: str = "mousewheel"  # DEPRECATED - USE WHEEL  #:
    WHEEL: str = "wheel"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.deltaX = options.get("deltaX", 0)
        self.deltaY = options.get("deltaY", 0)
        self.deltaZ = options.get("deltaZ", 0)
        self.deltaMode = options.get("deltaMode", 0)
        super().__init__(_type, options, *args, **kwargs)


class AnimationEvent(Event):
    """CSS animation lifecycle event."""

    ANIMATIONEND: str = "animationend"  #:
    ANIMATIONITERATION: str = "animationiteration"  #:
    ANIMATIONSTART: str = "animationstart"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.animationName = options.get("animationName", None)
        # Name of the animation that fired the event.
        self.elapsedTime = options.get("elapsedTime", None)
        # Seconds the animation has been running, excluding paused time.
        self.pseudoElement = options.get("pseudoElement", None)
        # Name of the pseudo-element that fired the event, when present.
        super().__init__(_type, options, *args, **kwargs)


class ClipboardEvent(Event):
    """Clipboard operation event exposing clipboard data."""

    COPY: str = "copy"  #:
    CUT: str = "cut"  #:
    PASTE: str = "paste"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.clipboardData = options.get("clipboardData", None)
        # Data affected by the clipboard operation.
        super().__init__(_type, options, *args, **kwargs)


class ErrorEvent(Event):
    """Script or resource error event."""

    ERROR: str = "error"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.message: str = options.get("message", "")
        self.filename = options.get("filename", None)
        self.lineno = options.get("lineno", 0)
        self.colno = options.get("colno", 0)
        self.error = options.get("error", None)
        super().__init__(_type, options, *args, **kwargs)


class CloseEvent(Event):
    """Close event used by streams, sockets, and similar resources."""

    CLOSE: str = "close"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.code = options.get("code", 0)
        self.reason = options.get("reason", "")
        self.wasClean = bool(options.get("wasClean", False))
        super().__init__(_type, options, *args, **kwargs)


class SubmitEvent(Event):
    """Form submission event with the submitting control."""

    SUBMIT: str = "submit"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.submitter = options.get("submitter", None)
        super().__init__(_type, options, *args, **kwargs)


class PointerEvent(MouseEvent):
    """Pointer input event extending mouse events for pen, touch, and mouse."""

    POINTER: str = "pointer"  #:
    POINTERCANCEL: str = "pointercancel"  #:
    POINTERDOWN: str = "pointerdown"  #:
    POINTERENTER: str = "pointerenter"  #:
    POINTERLEAVE: str = "pointerleave"  #:
    POINTERMOVE: str = "pointermove"  #:
    POINTEROUT: str = "pointerout"  #:
    POINTEROVER: str = "pointerover"  #:
    POINTERUP: str = "pointerup"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.pointerId: float = options.get("pointerId", 0)
        self.width: float = options.get("width", 1)
        self.height: float = options.get("height", 1)
        self.pressure: float = options.get("pressure", 0)
        self.tangentialPressure: float = options.get("tangentialPressure", 0)
        self.tiltX: float = options.get("tiltX", 0)
        self.tiltY: float = options.get("tiltY", 0)
        self.twist: float = options.get("twist", 0)
        self.altitudeAngle: float = options.get("altitudeAngle", 0)
        self.azimuthAngle: float = options.get("azimuthAngle", 0)
        self.pointerType: str = options.get("pointerType", "")
        self.isPrimary: bool = options.get("isPrimary", False)
        self.persistentDeviceId: int = options.get("persistentDeviceId", 0)
        self._coalescedEvents = list(options.get("coalescedEvents", []))
        self._predictedEvents = list(options.get("predictedEvents", []))
        super().__init__(_type, options, *args, **kwargs)

    def getCoalescedEvents(self):
        """Return the coalesced pointer events supplied at construction."""
        return list(self._coalescedEvents)

    def getPredictedEvents(self):
        """Return the predicted pointer events supplied at construction."""
        return list(self._predictedEvents)


class BeforeUnloadEvent(Event):
    """Before-unload event with browser-compatible return value handling."""

    BEFOREUNLOAD: ClassVar[str] = Event.BEFOREUNLOAD  #:

    def __init__(
        self, _type: str, options: dict[str, Any] | None = None, *args, **kwargs
    ) -> None:
        options = options or kwargs  # if options is none use kwargs
        self._beforeunload_return_value = options.get("returnValue", "")
        super().__init__(_type, options, *args, **kwargs)

    @property
    def returnValue(self) -> Any:
        return self._beforeunload_return_value

    @returnValue.setter
    def returnValue(self, value: Any) -> None:
        self._beforeunload_return_value = "" if value is None else value
        self.defaultPrevented = value not in ("", True, False, None)


class SVGEvent(Event):
    """SVG event type constants and base behavior."""

    ABORT: str = "abort"  #:
    LOAD: str = "load"  #:
    LOADEDDATA: str = "loadeddata"  #:
    LOADEDMETADATA: str = "loadedmetadata"  #:
    LOADSTART: str = "loadstart"  #:
    PROGRESS: str = "progress"  #:
    SCROLL: str = "scroll"  #:
    UNLOAD: str = "unload"  #:
    ERROR: str = "error"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        super().__init__(_type, options, *args, **kwargs)


class TimerEvent(Event):
    """Timer lifecycle event used by domonic animation helpers."""

    TIMER: str = "timer"  #:
    TIMER_COMPLETE: str = "timercomplete"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        super().__init__(_type, options, *args, **kwargs)


class DragEvent(MouseEvent):
    """Drag-and-drop event carrying optional data transfer state."""

    DRAG: str = "drag"  #:
    DRAGEND: str = "dragend"  #:
    DRAGENTER: str = "dragenter"  #:
    DRAGEXIT: str = "dragexit"  #:
    DRAGLEAVE: str = "dragleave"  #:
    DRAGOVER: str = "dragover"  #:
    DRAGSTART: str = "dragstart"  #:
    END: str = "dragend"  #:
    ENTER: str = "dragenter"  #:
    EXIT: str = "dragexit"  #:
    LEAVE: str = "dragleave"  #:
    OVER: str = "dragover"  #:
    START: str = "dragstart"  #:
    DROP: str = "drop"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.dataTransfer = options.get("dataTransfer", None)
        # Data transfer object associated with the drag operation.
        super().__init__(_type, options, *args, **kwargs)


class HashChangeEvent(Event):
    """URL fragment transition event."""

    CHANGE: str = "hashchange"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.newURL = options.get("newURL", "")
        self.oldURL = options.get("oldURL", "")
        super().__init__(_type, options, *args, **kwargs)


class InputEvent(UIEvent):
    """Editable-content input event with inserted data and target ranges."""

    CHANGE: str = "change"  #:
    SELECT: str = "select"  #:
    INPUT: str = "input"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.data = options.get("data", None)
        # Inserted characters, if any.
        self.dataTransfer = options.get("dataTransfer", None)
        # DataTransfer details for rich insertions, if any.
        self.inputType = options.get("inputType", None)
        # Type of edit operation, for example ``insertText`` or ``deleteContentBackward``.
        self.isComposing = options.get("isComposing", None)
        # Whether the input occurs during an active composition session.
        self._targetRanges = list(options.get("targetRanges", []))
        super().__init__(_type, options, *args, **kwargs)

    def getTargetRanges(self):
        """Return target ranges affected by the insertion or deletion."""
        if hasattr(self, "_targetRanges"):
            return list(self._targetRanges)
        if isinstance(getattr(self, "target", None), object):
            target = self.target
            if hasattr(target, "getSelection"):
                selection = target.getSelection()
                if selection is not None:
                    return [
                        selection.getRangeAt(i) for i in range(selection.rangeCount)
                    ]
        return []


class PageTransitionEvent(Event):
    """Page show/hide transition event."""

    PAGEHIDE: str = "pagehide"  #:
    PAGESHOW: str = "pageshow"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.persisted = options.get("persisted", None)
        # Whether the page was restored from a page cache.
        super().__init__(_type, options, *args, **kwargs)


class PopStateEvent(Event):
    """History navigation event carrying restored state."""

    POPSTATE: str = "popstate"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.state = options.get("state", None)
        # State object associated with the history entry.
        super().__init__(_type, options, *args, **kwargs)


class StorageEvent(Event):
    """Storage mutation event."""

    STORAGE: str = "storage"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.key = options.get("key", None)
        # Key of the changed storage item.
        self.newValue = options.get("newValue", None)
        # New value of the changed storage item.
        self.oldValue = options.get("oldValue", None)
        # Previous value of the changed storage item.
        self.storageArea = options.get("storageArea", None)
        # Storage object that was affected.
        self.url = options.get("url", None)
        # URL of the document where the change happened.
        super().__init__(_type, options, *args, **kwargs)


class TransitionEvent(Event):
    """CSS transition lifecycle event."""

    TRANSITIONEND: str = "transitionend"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.propertyName = options.get("propertyName", None)
        # Name of the CSS property that transitioned.
        self.elapsedTime = options.get("elapsedTime", None)
        # Seconds the transition has been running, excluding delay.
        self.pseudoElement = options.get("pseudoElement", None)
        # Name of the pseudo-element that fired the event, when present.
        super().__init__(_type, options, *args, **kwargs)


class ProgressEvent(Event):
    """Progress event with byte counts and computability state."""

    LOADSTART: str = "loadstart"  #:
    PROGRESS: str = "progress"  #:
    ABORT: str = "abort"  #:
    ERROR: str = "error"  #:
    LOAD: str = "load"  #:
    LOADED: str = "loaded"  #:
    LOADEND: str = "loadend"  #:
    TIMEOUT: str = "timeout"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.lengthComputable: bool = options.get("lengthComputable", False)
        self.loaded: int = options.get("loaded", 0)
        self.total: int = options.get("total", 0)
        super().__init__(_type, options, *args, **kwargs)


class CustomEvent(Event):
    """Custom application event carrying arbitrary detail data."""

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.detail = options.get("detail", None)
        super().__init__(_type, options, *args, **kwargs)

    def initCustomEvent(
        self,
        _type: str,
        bubbles: bool = True,
        cancelable: bool = True,
        detail: Any = None,
    ) -> "CustomEvent":
        self.initEvent(_type, bubbles, cancelable)
        self.detail = detail
        return self


class ToggleEvent(Event):
    """Popover or details toggle event with old and new state."""

    BEFORETOGGLE: str = "beforetoggle"  #:
    TOGGLE: str = "toggle"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs
        self.oldState = options.get("oldState", "")
        self.newState = options.get("newState", "")
        self.source = options.get("source", None)
        super().__init__(_type, options, *args, **kwargs)


class CommandEvent(Event):
    """Command activation event carrying a command string and source."""

    COMMAND: str = "command"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs
        self.command = options.get("command", "")
        self.source = options.get("source", None)
        super().__init__(_type, options, *args, **kwargs)


class GamePadEvent(Event):
    """Gamepad connection event."""

    START: str = "gamepadconnected"  #:
    STOP: str = "gamepaddisconnected"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.gamepad = options.get("gamepad", None)
        super().__init__(_type, options, *args, **kwargs)


class FormDataEvent(Event):
    """FormData construction event carrying a form data object."""

    FORMDATA: str = "formdata"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs
        self.formData = options.get("formData", None)
        super().__init__(_type, options, *args, **kwargs)


class TrackEvent(Event):
    """Media track add/remove event."""

    ADDTRACK: str = "addtrack"  #:
    REMOVETRACK: str = "removetrack"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs
        self.track = options.get("track", None)
        super().__init__(_type, options, *args, **kwargs)


class BlobEvent(Event):
    """Media recorder data event carrying a blob-like object."""

    DATAAVAILABLE: str = "dataavailable"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs
        self.data = options.get("data", None)
        self.timecode = options.get("timecode", 0)
        super().__init__(_type, options, *args, **kwargs)


class DeviceMotionEvent(Event):
    """Device motion event with acceleration and rotation readings."""

    DEVICEMOTION: str = "devicemotion"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs
        self.acceleration = options.get("acceleration", None)
        self.accelerationIncludingGravity = options.get(
            "accelerationIncludingGravity", None
        )
        self.rotationRate = options.get("rotationRate", None)
        self.interval = options.get("interval", 0)
        super().__init__(_type, options, *args, **kwargs)


class DeviceOrientationEvent(Event):
    """Device orientation event with alpha, beta, and gamma angles."""

    DEVICEORIENTATION: str = "deviceorientation"  #:
    DEVICEORIENTATIONABSOLUTE: str = "deviceorientationabsolute"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs
        self.absolute = bool(options.get("absolute", False))
        self.alpha = options.get("alpha", None)
        self.beta = options.get("beta", None)
        self.gamma = options.get("gamma", None)
        super().__init__(_type, options, *args, **kwargs)


class DeviceLightEvent(Event):
    """Ambient light event carrying a light level value."""

    DEVICELIGHT: str = "devicelight"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs
        self.value = options.get("value", None)
        super().__init__(_type, options, *args, **kwargs)


class DeviceProximityEvent(Event):
    """Device proximity event carrying distance bounds."""

    DEVICEPROXIMITY: str = "deviceproximity"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs
        self.value = options.get("value", None)
        self.min = options.get("min", None)
        self.max = options.get("max", None)
        super().__init__(_type, options, *args, **kwargs)


class WebGLContextEvent(Event):
    """WebGL context lifecycle event with an optional status message."""

    WEBGLCONTEXTLOST: str = "webglcontextlost"  #:
    WEBGLCONTEXTRESTORED: str = "webglcontextrestored"  #:
    WEBGLCONTEXTCREATIONERROR: str = "webglcontextcreationerror"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs
        self.statusMessage = options.get("statusMessage", "")
        super().__init__(_type, options, *args, **kwargs)


class FetchEvent(Event):
    """Service-worker-style fetch event."""

    FETCH: str = "fetch"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.clientId = options.get("clientId", None)
        # Client ID associated with the fetch request.
        self.request = options.get("request", None)
        # Request-like object being handled.
        self._responded_with = options.get("response", None)
        self._pending_promises: list[Any] = []
        super().__init__(_type, options, *args, **kwargs)

    @property
    def isReload(self):
        if self.request is None:
            return False
        return getattr(self.request, "url", None) == getattr(
            self.request, "referrer", object()
        )

    @property
    def replacesClientId(self):
        if self.request is None:
            return False
        return self.clientId != getattr(self.request, "clientId", None)

    @property
    def resultingClientId(self):
        if self.request is None:
            return self.clientId
        return (
            self.clientId
            if self.replacesClientId
            else getattr(self.request, "clientId", None)
        )

    def respondWith(self, response):
        """Store and return the response object supplied for this fetch."""
        self._responded_with = response
        return response

    def waitUntil(self, promise):
        """Track and return a pending wait object supplied by the caller."""
        self._pending_promises.append(promise)
        return promise


class ExtendableEvent(Event):
    """Event that can track caller-supplied work before completion."""

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.extendable = options.get("extendable", True)
        # Whether the event accepts work through waitUntil().
        self._pending_promises: list[Any] = []
        super().__init__(_type, options, *args, **kwargs)

    def waitUntil(self, promise: Any):
        """Track and return a pending wait object supplied by the caller."""
        self._pending_promises.append(promise)
        return promise


class SyncEvent(ExtendableEvent):
    """Background sync event with tag and final-attempt state."""

    SYNC: str = "sync"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.tag = options.get("tag", None)
        # Sync registration tag.
        self.lastChance = options.get("lastChance", None)
        # Whether this is the final retry opportunity.
        super().__init__(_type, options, *args, **kwargs)


class SecurityPolicyViolationEvent(Event):
    """Content Security Policy violation event."""

    SECURITY_POLICY_VIOLATION: str = "securitypolicyviolation"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.documentURI = options.get("documentURI", None)
        # URI of the protected document.
        self.referrer = options.get("referrer", None)
        # Referrer of the protected document or blocked resource.
        self.blockedURI = options.get("blockedURI", None)
        # URI blocked by the policy.
        self.violatedDirective = options.get("violatedDirective", None)
        # Directive text that was violated.
        self.effectiveDirective = options.get("effectiveDirective", None)
        # Effective directive name.
        self.originalPolicy = options.get("originalPolicy", None)
        # Full policy text.
        self.disposition = options.get("disposition", None)
        # Policy disposition, typically ``enforce`` or ``report``.
        self.sourceFile = options.get("sourceFile", None)
        # Source file related to the violation.
        self.statusCode = options.get("statusCode", 0)
        # HTTP status code of the document or resource.
        self.lineNumber = options.get("lineNumber", 0)
        # Line number where the violation occurred.
        self.columnNumber = options.get("columnNumber", 0)
        # Column number where the violation occurred.
        self.sample = options.get("sample", "")
        # Source sample associated with the violation.
        self.isFrameAncestor = options.get("isFrameAncestor", None)
        # Whether the violating frame is an ancestor frame.
        self.isMainFrame = options.get("isMainFrame", None)
        # Whether the violation occurred in the main frame.
        self.frame = options.get("frame", None)
        # Frame object associated with the violation.
        super().__init__(_type, options, *args, **kwargs)


class DOMContentLoadedEvent(Event):
    """Document-ready event carrying the loaded document."""

    DOMCONTENTLOADED: str = "DOMContentLoaded"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.document = options.get("document", None)
        # Document that finished parsing.
        super().__init__(_type, options, *args, **kwargs)


class TweenEvent(Event):
    """Animation tween lifecycle event with a source object."""

    START: str = "onStart"  #:
    STOP: str = "onStop"  #:
    RESET: str = "onReset"  #:
    PAUSE: str = "onPause"  #:
    UNPAUSE: str = "onUnPause"  #:
    UPDATE_START: str = "onUpdateStart"  #:
    UPDATE_END: str = "onUpdateEnd"  #:
    COMPLETE: str = "onComplete"  #:

    TIMER: str = "onTimer"  #:
    _source = None

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, source):
        self._source = source

    def __init__(self, _type, source=None, bubbles=False, cancelable=False):
        super().__init__(_type, {"bubbles": bubbles, "cancelable": cancelable})
        self.source = source


class PromiseRejectionEvent(Event):
    """Unhandled or handled promise rejection event."""

    UNHANDLED: str = "unhandledrejection"  #:
    HANDLED: str = "rejectionhandled"  #:

    def __init__(self, _type, options=None, *args, **kwargs):
        options = options or kwargs
        self.promise = options.get("promise", None)
        # Promise-like object that was rejected.
        self.reason = options.get("reason", None)
        # Rejection reason.
        self.isRejected = options.get("isRejected", None)
        # Whether the promise is currently rejected.
        super().__init__(_type, options, *args, **kwargs)


class MessageEvent(Event):
    """Cross-context message event."""

    MESSAGE: str = "message"  #:
    CONNECT: str = "connect"  #:
    DISCONNECT: str = "disconnect"  #:

    def __init__(self, _type, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.data = options.get("data", None)
        # Message payload.
        self.origin = options.get("origin", None)
        # Origin that produced the message.
        self.lastEventId = options.get("lastEventId", None)
        # Last event ID for streaming/event-source messages.
        self.source = options.get("source", None)
        # Source object that sent the message.
        self.ports = options.get("ports", [])
        # Message ports transferred with the event.
        super().__init__(_type, options, *args, **kwargs)


class GlobalEventHandler:
    """Mixin that installs default ``on*`` event handler methods."""

    _handler_names = (
        "onabort",
        "onanimationcancel",
        "onanimationend",
        "onanimationiteration",
        "onauxclick",
        "onbeforeinput",
        "onbeforematch",
        "onbeforetoggle",
        "onblur",
        "oncancel",
        "oncanplay",
        "oncanplaythrough",
        "onchange",
        "onclick",
        "onclose",
        "oncommand",
        "onconnect",
        "oncontextlost",
        "oncontextmenu",
        "oncontextrestored",
        "oncuechange",
        "oncurrententrychange",
        "ondblclick",
        "ondispose",
        "ondrag",
        "ondragend",
        "ondragenter",
        "ondragexit",
        "ondragleave",
        "ondragover",
        "ondragstart",
        "ondrop",
        "ondurationchange",
        "onemptied",
        "onended",
        "onerror",
        "onfocus",
        "onformdata",
        "ongotpointercapture",
        "oninput",
        "oninvalid",
        "onkeydown",
        "onkeypress",
        "onkeyup",
        "onlanguagechange",
        "onload",
        "onloadeddata",
        "onloadedmetadata",
        "onloadend",
        "onloadstart",
        "onlostpointercapture",
        "onmessage",
        "onmessageerror",
        "onmouseenter",
        "onmouseleave",
        "onmousedown",
        "onmousemove",
        "onmouseout",
        "onmouseover",
        "onmouseup",
        "onnavigate",
        "onnavigateerror",
        "onnavigatesuccess",
        "onopen",
        "onpause",
        "onplay",
        "onplaying",
        "onpointercancel",
        "onpointerdown",
        "onpointerenter",
        "onpointerleave",
        "onpointermove",
        "onpointerout",
        "onpointerover",
        "onpointerup",
        "onprogress",
        "onratechange",
        "onreadystatechange",
        "onrejectionhandled",
        "onreset",
        "onresize",
        "onscroll",
        "onscrollend",
        "onsearch",
        "onsecuritypolicyviolation",
        "onseeked",
        "onseeking",
        "onselect",
        "onselectionchange",
        "onselectstart",
        "onshow",
        "onslotchange",
        "onstalled",
        "onsubmit",
        "onsuspend",
        "ontimeupdate",
        "ontoggle",
        "ontouchcancel",
        "ontouchstart",
        "ontransitioncancel",
        "ontransitionend",
        "onunhandledrejection",
        "onvisibilitychange",
        "onvolumechange",
        "onwaiting",
        "onwheel",
    )


class WindowEventHandler:
    """Window-specific ``on*`` event handler methods."""

    _handler_names = (
        "onabort",
        "onafterprint",
        "onbeforeinput",
        "onbeforematch",
        "onbeforeprint",
        "onbeforetoggle",
        "onbeforeunload",
        "onblur",
        "oncanplay",
        "oncanplaythrough",
        "onchange",
        "onclick",
        "oncommand",
        "onconnect",
        "oncontextlost",
        "oncontextmenu",
        "oncontextrestored",
        "oncopy",
        "oncuechange",
        "oncurrententrychange",
        "oncut",
        "ondblclick",
        "ondispose",
        "ondrag",
        "ondragend",
        "ondragenter",
        "ondragleave",
        "ondragover",
        "ondragstart",
        "ondrop",
        "ondurationchange",
        "onemptied",
        "onended",
        "onerror",
        "onfocus",
        "onformdata",
        "onhashchange",
        "oninput",
        "oninvalid",
        "onkeydown",
        "onkeypress",
        "onkeyup",
        "onlanguagechange",
        "onload",
        "onloadeddata",
        "onloadedmetadata",
        "onloadstart",
        "onmessage",
        "onmessageerror",
        "onmousedown",
        "onmouseenter",
        "onmouseleave",
        "onmousemove",
        "onmouseout",
        "onmouseover",
        "onmouseup",
        "onmousewheel",
        "onnavigate",
        "onnavigateerror",
        "onnavigatesuccess",
        "onoffline",
        "ononline",
        "onopen",
        "onpagehide",
        "onpagereveal",
        "onpageshow",
        "onpageswap",
        "onpaste",
        "onpopstate",
        "onreadystatechange",
        "onrejectionhandled",
        "onresize",
        "onscroll",
        "onscrollend",
        "onsearch",
        "onsecuritypolicyviolation",
        "onslotchange",
        "onstorage",
        "onsubmit",
        "ontoggle",
        "onunhandledrejection",
        "onunload",
        "onvisibilitychange",
    )

    def __init__(self, window):
        """Bind the handler collection to a window-like object."""
        super().__init__()
        self.window = window


def _make_default_event_handler(name: str):
    """Create a default handler that records and forwards the event."""

    def handler(self, event):
        self._last_event = event
        callback = getattr(self, f"_{name}_callback", None)
        if callable(callback):
            return callback(event)
        return event

    handler.__name__ = name
    return handler


def _install_default_event_handlers(*classes) -> None:
    """Install generated default handlers on each supplied handler class."""
    for cls in classes:
        for name in getattr(cls, "_handler_names", ()):
            setattr(cls, name, _make_default_event_handler(name))


_install_default_event_handlers(GlobalEventHandler, WindowEventHandler)
