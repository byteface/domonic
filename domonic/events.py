"""
    domonic.events
    ====================================

    https://developer.mozilla.org/en-US/docs/Web/Events

"""

from __future__ import annotations

import inspect
import time
from typing import Any, Callable, ClassVar


class EventTarget:
    """
    EventTarget is a class you can extend to give your object event dispatching abilities.

    This class allows you to add, remove, and dispatch custom events, making it useful for creating
    event-driven components in your Python application.

    **Usage:**
    
    To add an event listener:
    - Use the ``addEventListener`` method.

    To remove an event listener:
    - Use the ``removeEventListener`` method.

    To dispatch an event:
    - Create an event object with the desired event type and optional event data.
    - Use the ``dispatchEvent`` method to trigger the event.

    **Example:**
    
    .. code-block:: python

        target = EventTarget()
        
        def my_event_handler(event):
            print("Event received:", event)
        
        target.addEventListener("custom_event", my_event_handler)
        
        event_data = {"message": "Hello, world!"}
        custom_event = {"type": "custom_event", "data": event_data}
        target.dispatchEvent(custom_event)
        
        # Output: Event received: {'type': 'custom_event', 'data': {'message': 'Hello, world!'}}

    **Attributes:**

    - ``listeners`` (dict): A dictionary to store event listeners by event type.
    """

    def __init__(self, *args, **kwargs) -> None:
        # Initialize a dictionary to store event listeners.
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
    ) -> dict[str, bool]:
        normalized = {"capture": False, "once": False, "passive": False}
        if isinstance(options, bool):
            normalized["capture"] = options
        elif isinstance(options, dict):
            normalized["capture"] = bool(options.get("capture", False))
            normalized["once"] = bool(options.get("once", False))
            normalized["passive"] = bool(options.get("passive", False))

        if "use_capture" in kwargs:
            normalized["capture"] = bool(kwargs["use_capture"])
        if "capture" in kwargs:
            normalized["capture"] = bool(kwargs["capture"])
        if "once" in kwargs:
            normalized["once"] = bool(kwargs["once"])
        if "passive" in kwargs:
            normalized["passive"] = bool(kwargs["passive"])
        return normalized

    def _get_event_path(self, target: Any) -> list[Any]:
        path: list[Any] = []
        current = target
        seen: set[int] = set()
        while current is not None and id(current) not in seen:
            path.append(current)
            seen.add(id(current))
            if hasattr(current, "parentNode") and getattr(current, "parentNode", None) is not None:
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

    def _invoke_listeners(self, current_target: Any, event: "Event", capture: bool) -> None:
        event_type = event.type
        listeners = list(getattr(current_target, "_listener_options", {}).get(event_type, []))
        event.currentTarget = current_target
        event.srcElement = event.target
        event.eventPhase = Event.AT_TARGET if current_target is event.target else (
            Event.CAPTURING_PHASE if capture else Event.BUBBLING_PHASE
        )

        for listener in listeners:
            if listener["capture"] != capture:
                continue
            callback = listener["callback"]
            event._in_passive_listener = listener["passive"]
            if hasattr(callback, "handleEvent"):
                result = callback.handleEvent(event)
            else:
                result = callback(event)
            if result is False:
                event.preventDefault()
            event._in_passive_listener = False
            if listener["once"]:
                current_target.removeEventListener(event_type, callback, listener["capture"])
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
        callback: Callable[..., Any],
        options: bool | dict[str, Any] | None = None,
        *args,
        **kwargs,
    ) -> None:
        """
        Add an event listener for the given event type.

        Args:
            eventType (str): The type of the event to listen for.
            callback (Callable): The callback function to be executed when the event occurs.
        """
        if eventType not in self.listeners:
            self.listeners[eventType] = []
            self._listener_options[eventType] = []
        listener_options = self._normalize_listener_options(options, **kwargs)
        for listener in self._listener_options[eventType]:
            if listener["callback"] is callback and listener["capture"] == listener_options["capture"]:
                return
        self.listeners[eventType].append(callback)
        self._listener_options[eventType].append({"callback": callback, **listener_options})

    def removeEventListener(
        self, eventType: str, callback: Callable[..., Any], options: bool | dict[str, Any] | None = None
    ) -> None:
        """
        Remove an event listener for the given event type.

        Args:
            eventType (str): The type of the event.
            callback (Callable): The callback function to be removed.
        """
        if eventType not in self.listeners:
            return
        capture = self._normalize_listener_options(options)["capture"]
        callbacks = self.listeners[eventType]
        listeners = self._listener_options.get(eventType, [])
        for index, listener in enumerate(listeners):
            if listener["callback"] is callback and listener["capture"] == capture:
                listeners.pop(index)
                try:
                    callbacks.remove(callback)
                except ValueError:
                    pass
                break
        if not listeners:
            self._listener_options.pop(eventType, None)
            self.listeners.pop(eventType, None)

    def dispatchEvent(self, event: Any) -> bool:
        """
        Dispatch the specified event to all registered event listeners.

        Args:
            event (Dict): The event object to be dispatched.

        Returns:
            bool: True if the event was successfully dispatched, otherwise False.
        """
        if not isinstance(event, Event):
            event = Event(event.get("type", ""), event)
        event.target = self
        event.currentTarget = self
        event.srcElement = self
        event.cancelBubble = False
        event._propagation_stopped = False
        event._immediate_propagation_stopped = False
        event._in_passive_listener = False

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
            event.eventPhase = Event.NONE
            event.currentTarget = None
            event._in_passive_listener = False

    async def dispatchEventAsync(self, event: Any) -> bool:
        """
        Dispatch the specified event asynchronously to all registered event listeners.

        Args:
            event (Dict): The event object to be dispatched.

        Returns:
            bool: True if the event was successfully dispatched, otherwise False.

        **Usage:**

        To dispatch an event asynchronously, use the ``await`` keyword when calling this method.

        **Example:**

        .. code-block:: python

            event_data = {"message": "Hello, world!"}
            async_event = {"type": "async_event", "data": event_data}
            await target.dispatchEventAsync(async_event)
        """
        if not isinstance(event, Event):
            event = Event(event.get("type", ""), event)
        event.target = self
        event.currentTarget = self
        event.srcElement = self
        event.cancelBubble = False
        event._propagation_stopped = False
        event._immediate_propagation_stopped = False
        event._in_passive_listener = False

        async def call_listener(callback: Callable[..., Any], current_target: Any, capture: bool) -> Any:
            event.currentTarget = current_target
            event.srcElement = event.target
            event.eventPhase = Event.AT_TARGET if current_target is event.target else (
                Event.CAPTURING_PHASE if capture else Event.BUBBLING_PHASE
            )
            if hasattr(callback, "handleEvent"):
                result = callback.handleEvent(event)
            else:
                result = callback(event)
            if inspect.isawaitable(result):
                result = await result
            return result

        async def invoke(current_target: Any, capture: bool) -> None:
            listeners = list(getattr(current_target, "_listener_options", {}).get(event.type, []))
            for listener in listeners:
                if listener["capture"] != capture:
                    continue
                event._in_passive_listener = listener["passive"]
                result = await call_listener(listener["callback"], current_target, capture)
                if result is False:
                    event.preventDefault()
                event._in_passive_listener = False
                if listener["once"]:
                    current_target.removeEventListener(event.type, listener["callback"], listener["capture"])
                if event._immediate_propagation_stopped:
                    return
            if capture is False:
                handler = getattr(current_target, f"on{event.type}", None)
                if callable(handler):
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
            event.eventPhase = Event.NONE
            event.currentTarget = None
            event._in_passive_listener = False


EventDispatcher = EventTarget  #: legacy alias


class Event:
    """Event class represents events and their properties."""

    # Constants for event types
    EMPTIED: str = "emptied"  #:
    ABORT: str = "abort"  #:
    AFTERPRINT: str = "afterprint"  #:
    BEFOREPRINT: str = "beforeprint"  #:
    BEFOREUNLOAD: str = "beforeunload"  #:
    CANPLAY: str = "canplay"  #:
    CANPLAYTHROUGH: str = "canplaythrough"  #:
    CHANGE: str = "change"  #:
    DURATIONCHANGE: str = "durationchange"  #:
    ENDED: str = "ended"  #:
    ERROR: str = "error"  #:
    FULLSCREENCHANGE: str = "fullscreenchange"  #:
    FULLSCREENERROR: str = "fullscreenerror"  #:
    INPUT: str = "input"  #:
    INVALID: str = "invalid"  #:
    LOAD: str = "load"  #:
    LOADEDDATA: str = "loadeddata"  #:
    LOADEDMETADATA: str = "loadedmetadata"  #:
    MESSAGE: str = "message"  #:
    OFFLINE: str = "offline"  #:
    ONLINE: str = "online"  #:
    OPEN: str = "open"  #:
    PAUSE: str = "pause"  #:
    PLAY: str = "play"  #:
    PLAYING: str = "playing"  #:
    PROGRESS: str = "progress"  #:
    RATECHANGE: str = "ratechange"  #:
    READYSTATECHANGE: str = "readystatechange"  #:
    RESIZE: str = "resize"  #:
    RESET: str = "reset"  #:
    SCROLL: str = "scroll"  #:
    SEARCH: str = "search"  #:
    SEEKED: str = "seeked"  #:
    SEEKING: str = "seeking"  #:
    SELECT: str = "select"  #:
    SHOW: str = "show"  #:
    STALLED: str = "stalled"  #:
    SUBMIT: str = "submit"  #:
    SUSPEND: str = "suspend"  #:
    TOGGLE: str = "toggle"  #:
    UNLOAD: str = "unload"  #:
    VOLUMECHANGE: str = "volumechange"  #:
    WAITING: str = "waiting"  #:

    NONE: int = 0
    CAPTURING_PHASE: int = 1
    AT_TARGET: int = 2
    BUBBLING_PHASE: int = 3

    def __str__(self) -> str:
        return self.type + ":" + str(self.timeStamp)

    def __init__(self, _type: str = "", options: dict[str, Any] | None = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.type: str = _type
        self.bubbles: bool = options.get("bubbles", False)
        self.cancelable: bool = options.get("cancelable", False)
        self._cancelBubble: bool = False
        self.composed: bool = options.get("composed", False)
        self.currentTarget: object = options.get("currentTarget", None)
        self.defaultPrevented: bool = options.get("defaultPrevented", False)
        self.eventPhase: int = options.get("eventPhase", Event.NONE)
        self.explicitOriginalTarget: object = options.get("explicitOriginalTarget", None)
        self.isTrusted: bool = options.get("isTrusted", False)
        self.originalTarget: object = options.get("originalTarget", None)
        self._returnValue: bool = True
        self.srcElement: object = options.get("srcElement", None)
        self.target: object = options.get("target", None)
        self.timeStamp: float = time.time_ns() / 1_000_000
        self._propagation_stopped: bool = False
        self._immediate_propagation_stopped: bool = False
        self._in_passive_listener: bool = False
        self._path: list[Any] | None = None
        self.cancelBubble = options.get("cancelBubble", False)
        self.returnValue = options.get("returnValue", True)

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
        """
        Returns a list of the event's path, from the root to the target.
        """
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
        # Include the window as the final item in the path.
        if path:
            last = path[-1]
            default_view = getattr(last, "defaultView", None)
            if default_view is not None and default_view not in path:
                path.append(default_view)
        return path

    def initEvent(
        self, _type: str | None = None, bubbles: bool = True, cancelable: bool = True, *args, **kwargs
    ) -> "Event":
        """Initialize the event."""
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
        """[prevents further propagation of the current event in the capturing and bubbling phases]"""
        self.cancelBubble = True  # Set the cancelBubble flag to stop propagation
        self._propagation_stopped = True

    def msConvertURL(self, url):
        """
        Converts the provided URL to a format recognized by Internet Explorer.

        Args:
            url (str): The URL to be converted.

        Returns:
            str: The converted URL.
        """
        if url.startswith('http'):
            # Example conversion for HTTP/HTTPS URLs in Internet Explorer
            return f'javascript:window.open("{url}");'
        else:
            # Handle other URL formats as needed
            return url

    def preventDefault(self) -> None:
        """
        Prevents the default action associated with the event, if cancelable.

        This method is used to signal that the event should not trigger its default behavior.

        Returns:
            None
        """
        if self.cancelable and not self._in_passive_listener:
            self.defaultPrevented = True
            self.returnValue = False

    def stopImmediatePropagation(self) -> None:
        """
        Prevents further propagation of the current event and immediately stops other event listeners in the same phase from being invoked.

        This method is used to stop the event's propagation immediately and ensure that no other listeners in the same phase are invoked.

        Returns:
            None
        """
        self.cancelBubble = True
        self._propagation_stopped = True
        self._immediate_propagation_stopped = True


class UIEvent(Event):
    """UIEvent is a specialized event class for user interface events."""

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        """
        Initialize a UIEvent.

        Args:
            _type (str): The type of the UIEvent.
            options (dict, optional): Additional options for the event. Defaults to None.

        Returns:
            None
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

    def initUIEvent(self, _type: str, canBubble: bool, cancelable: bool, view, detail) -> "UIEvent":
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
    """mouse events"""

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
        options = options or kwargs
        self.canBubble = options.get("canBubble", None)
        self.cancelable = options.get("cancelable", None)
        self.x = options.get("x", 0)
        self.y = options.get("y", 0)
        self._clientX = options.get("clientX", 0)
        self._clientY = options.get("clientY", 0)
        self._altKey: bool = options.get("altKey", False)
        self._ctrlKey: bool = options.get("ctrlKey", False)
        self._shiftKey: bool = options.get("shiftKey", False)
        self._metaKey: bool = options.get("metaKey", False)
        self._button = None
        self._buttons = []
        super().__init__(_type, options, *args, **kwargs)

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
        from_json={},
        *args,
        **kwargs
    ) -> "MouseEvent":
        # print('initMouseEvent')
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
        self._button = button
        self._buttons = [] if button is None else [button]
        self.relatedTarget = relatedTarget
        # TODO - parse from_json - so can relay
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
        return self._button

    # MOUSE_EVENT
    def getModifierState(self, keyArg: str):
        """Returns an array containing target ranges that will be affected by the insertion/deletion"""
        lookup = {
            "Alt": self.altKey,
            "Control": self.ctrlKey,
            "Meta": self.metaKey,
            "Shift": self.shiftKey,
        }
        return lookup.get(keyArg, False)

    # MovementX Returns the horizontal coordinate of the mouse pointer relative to the position of the last mousemove event MouseEvent
    # MovementY Returns the vertical coordinate of the mouse pointer relative to the position of the last mousemove event   MouseEvent
    # offsetX   Returns the horizontal coordinate of the mouse pointer relative to the position of the edge of the target element   MouseEvent
    # offsetY   Returns the vertical coordinate of the mouse pointer relative to the position of the edge of the target element MouseEvent
    # pageX Returns the horizontal coordinate of the mouse pointer, relative to the document, when the mouse event was triggered    MouseEvent
    # pageY Returns the vertical coordinate of the mouse pointer, relative to the document, when the mouse event was triggered  MouseEvent
    # region        MouseEvent
    # relatedTarget Returns the element related to the element that triggered the mouse event   MouseEvent, FocusEvent


class KeyboardEvent(UIEvent):
    """keyboard events"""

    KEYDOWN: str = "keydown"  #:
    KEYPRESS: str = "keypress"  #:
    KEYUP: str = "keyup"  #:

    DOM_KEY_LOCATION_LEFT: int = 0  #:
    DOM_KEY_LOCATION_STANDARD: int = 1  #:
    DOM_KEY_LOCATION_RIGHT: int = 2  #:
    DOM_KEY_LOCATION_NUMPAD: int = 3  #:
    DOM_KEY_LOCATION_MOBILE: int = 4  #:
    DOM_KEY_LOCATION_JOYSTICK: int = 5  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.canBubble = options.get("canBubble", None)
        self.cancelable = options.get("cancelable", None)
        self._altKey: bool = options.get("altKey", False)
        self._ctrlKey: bool = options.get("ctrlKey", False)
        self._shiftKey: bool = options.get("shiftKey", False)
        self._metaKey: bool = options.get("metaKey", False)

        self.charCode = options.get("charCode", None)
        self.code = options.get("code", None)
        self.key = options.get("key", None)
        self.keyCode = options.get("keyCode", None)

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
        self.initEvent(typeArg, canBubbleArg, cancelableArg)
        self.canBubbleArg = canBubbleArg
        self.cancelableArg = cancelableArg
        self.view = viewArg
        self.viewArg = viewArg
        self.charCode = charArg
        self.key = keyArg
        self.code = keyArg
        self.location = locationArg
        self.locationArg = locationArg
        self.modifiersListArg = modifiersListArg
        modifiers = {modifier.strip().lower() for modifier in str(modifiersListArg).split() if modifier}
        self._altKey = "alt" in modifiers
        self._ctrlKey = "control" in modifiers or "ctrl" in modifiers
        self._metaKey = "meta" in modifiers
        self._shiftKey = "shift" in modifiers
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
        lookup = {
            "Alt": self.altKey,
            "Control": self.ctrlKey,
            "Meta": self.metaKey,
            "Shift": self.shiftKey,
        }
        return lookup.get(keyArg, False)

    # @property
    # def keyCode(self):
    #     return self.keyCode

    # @property
    # def charCode(self):
    #     return self.charCode

    # @property
    # def code(self):
    #     return self.code

    # @property
    # def key(self):
    #     return self.key

    # def isComposing(self, *args, **kwargs):
    #     pass

    # KeyboardEvent
    # isComposing   Returns whether the state of the event is composing or not  InputEvent, KeyboardEvent
    # repeat    Returns whether a key is being hold down repeatedly, or not KeyboardEvent
    # location  Returns the location of a key on the keyboard or device KeyboardEvent


class CompositionEvent(UIEvent):
    """CompositionEvent"""

    START: str = "compositionstart"
    END: str = "compositionend"
    UPDATE: str = "compositionupdate"

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.data = options.get("data", None)
        self.locale = options.get("locale", None)
        super().__init__(_type, options, *args, **kwargs)


class FocusEvent(UIEvent):
    """FocusEvent"""

    BLUR: str = "blur"  #:
    FOCUS: str = "focus"  #:
    FOCUSIN: str = "focusin"  #:
    FOCUSOUT: str = "focusout"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.relatedTarget = options.get("relatedTarget", None)
        super().__init__(_type, options, *args, **kwargs)


class TouchEvent(UIEvent):
    """TouchEvent"""

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


class WheelEvent(UIEvent):
    """WheelEvent"""

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
    """AnimationEvent"""

    ANIMATIONEND: str = "animationend"  #:
    ANIMATIONITERATION: str = "animationiteration"  #:
    ANIMATIONSTART: str = "animationstart"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.animationName = options.get("animationName", None)
        """ Returns the name of the animation """
        self.elapsedTime = options.get("elapsedTime", None)
        """ Returns the number of seconds an animation has been running """
        self.pseudoElement = options.get("pseudoElement", None)
        """ Returns the name of the pseudo-element of the animation """
        super().__init__(_type, options, *args, **kwargs)


class ClipboardEvent(Event):
    """ClipboardEvent"""

    COPY: str = "copy"  #:
    CUT: str = "cut"  #:
    PASTE: str = "paste"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.clipboardData = options.get("clipboardData", None)
        """ Returns an object containing the data affected by the clipboard operation """
        super().__init__(_type, options, *args, **kwargs)


class ErrorEvent(Event):
    """ErrorEvent"""

    ERROR: str = "error"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.message: str = options.get("message", "")
        self.filename = options.get("filename", None)
        self.lineno = options.get("lineno", 0)
        self.colno = options.get("colno", 0)
        self.error = options.get("error", None)
        super().__init__(_type, options, *args, **kwargs)


class SubmitEvent(Event):
    """SubmitEvent"""

    SUBMIT: str = "submit"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.submitter = options.get("submitter", None)
        super().__init__(_type, options, *args, **kwargs)


class PointerEvent(MouseEvent):
    """PointerEvent"""

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
        self.width: float = options.get("width", 0)
        self.height: float = options.get("height", 0)
        self.pressure: float = options.get("pressure", 0)
        self.tangentialPressure: float = options.get("tangentialPressure", 0)
        self.tiltX: float = options.get("tiltX", 0)
        self.tiltY: float = options.get("tiltY", 0)
        self.twist: float = options.get("twist", 0)
        self.pointerType: str = options.get("pointerType", "")
        self.isPrimary: bool = options.get("isPrimary", False)
        self._coalescedEvents = list(options.get("coalescedEvents", []))
        self._predictedEvents = list(options.get("predictedEvents", []))
        super().__init__(_type, options, *args, **kwargs)

    def getCoalescedEvents(self):
        return list(self._coalescedEvents)

    def getPredictedEvents(self):
        return list(self._predictedEvents)

    # def getCurrentPoint(self, element):
    #     """ Returns the current coordinates of the specified element relative to the viewport. """
    #     pass

    # def getIntermediatePoints(self, element):
    #     """ Returns the coordinates of all the intermediate points of the pointer along the path of the pointer. """
    #     pass


class BeforeUnloadEvent(Event):
    BEFOREUNLOAD: ClassVar[str] = Event.BEFOREUNLOAD  #:
    """ BeforeUnloadEvent """

    def __init__(self, _type: str, options: dict[str, Any] | None = None, *args, **kwargs) -> None:
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
    """SVGEvent"""

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

    # def initEvent(self, eventTypeArg, canBubbleArg, cancelableArg):
    #     pass


class TimerEvent(Event):
    TIMER: str = "timer"  #:
    TIMER_COMPLETE: str = "timercomplete"  #:
    """ TimerEvent """

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        super().__init__(_type, options, *args, **kwargs)

    # def initTimerEvent(self, type, bubbles, cancelable, detail):
    #     """ initTimerEvent() """
    #     pass


class DragEvent(Event):
    """DragEvent"""

    DRAG: str = "drag"  #:
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
        """ Returns the data that is dragged/dropped """
        super().__init__(_type, options, *args, **kwargs)


class HashChangeEvent(Event):
    """HashChangeEvent"""

    CHANGE: str = "hashchange"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.newURL = options.get("newURL", "")
        self.oldURL = options.get("oldURL", "")
        super().__init__(_type, options, *args, **kwargs)


class InputEvent(UIEvent):
    """InputEvent"""

    CHANGE: str = "change"  #:
    SELECT: str = "select"  #:
    INPUT: str = "input"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.data = options.get("data", None)
        """ Returns the inserted characters """
        self.dataTransfer = options.get("dataTransfer", None)
        """ Returns an object containing information about the inserted/deleted data """
        self.inputType = options.get("inputType", None)
        """ Returns the type of the change (i.e "inserting" or "deleting") """
        self.isComposing = options.get("isComposing", None)
        """ Returns whether the state of the event is composing or not """
        super().__init__(_type, options, *args, **kwargs)

    def getTargetRanges(self):
        """Returns an array containing target ranges that will be affected by the insertion/deletion"""
        if hasattr(self, "_targetRanges"):
            return list(self._targetRanges)
        if isinstance(getattr(self, "target", None), object):
            target = self.target
            if hasattr(target, "getSelection"):
                selection = target.getSelection()
                if selection is not None:
                    return [selection.getRangeAt(i) for i in range(selection.rangeCount)]
        return []


class PageTransitionEvent(Event):
    """PageTransitionEvent"""

    PAGEHIDE: str = "pagehide"  #:
    PAGESHOW: str = "pageshow"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.persisted = options.get("persisted", None)
        """ Returns whether the webpage was cached by the browser """
        super().__init__(_type, options, *args, **kwargs)


class PopStateEvent(Event):
    """PopStateEvent"""

    POPSTATE: str = "popstate"  #:
    # ONPOPSTATE = "onpopstate"  #:??

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.state = options.get("state", None)
        """ Returns an object containing a copy of the history entries """
        super().__init__(_type, options, *args, **kwargs)


class StorageEvent(Event):
    """StorageEvent"""

    STORAGE: str = "storage"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.key = options.get("key", None)
        """ Returns the key of the changed storage item """
        self.newValue = options.get("newValue", None)
        """ Returns the new value of the changed storage item """
        self.oldValue = options.get("oldValue", None)
        """ Returns the old value of the changed storage item """
        self.storageArea = options.get("storageArea", None)
        """ Returns an object representing the affected storage object """
        self.url = options.get("url", None)
        """ Returns the URL of the changed item's document """
        super().__init__(_type, options, *args, **kwargs)


class TransitionEvent(Event):
    """TransitionEvent"""

    TRANSITIONEND: str = "transitionend"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.propertyName = options.get("propertyName", None)
        """ Returns the name of the transition"""
        self.elapsedTime = options.get("elapsedTime", None)
        """  Returns the number of seconds a transition has been running """
        self.pseudoElement = options.get("pseudoElement", None)
        """ Returns the name of the pseudo-element of the transition """
        super().__init__(_type, options, *args, **kwargs)


class ProgressEvent(Event):
    """ProgressEvent"""

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
    """CustomEvent"""

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.detail = options.get("detail", None)
        super().__init__(_type, options, *args, **kwargs)

    def initCustomEvent(
        self, _type: str, bubbles: bool = True, cancelable: bool = True, detail: Any = None
    ) -> "CustomEvent":
        self.initEvent(_type, bubbles, cancelable)
        self.detail = detail
        return self


class GamePadEvent(Event):
    """GamePadEvent"""

    START: str = "gamepadconnected"  #:
    STOP: str = "gamepaddisconnected"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.gamepad = options.get("gamepad", None)
        super().__init__(_type, options, *args, **kwargs)


# TODO - tests and service worker API
class FetchEvent(Event):
    """FetchEvent"""

    FETCH: str = "fetch"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.clientId = options.get("clientId", None)
        """ Returns the client ID of the fetch request """
        self.request = options.get("request", None)
        """ Returns the request object """
        self._responded_with = options.get("response", None)
        self._pending_promises: list[Any] = []
        super().__init__(_type, options, *args, **kwargs)

    @property
    def isReload(self):
        if self.request is None:
            return False
        return getattr(self.request, "url", None) == getattr(self.request, "referrer", object())

    @property
    def replacesClientId(self):
        if self.request is None:
            return False
        return self.clientId != getattr(self.request, "clientId", None)

    @property
    def resultingClientId(self):
        if self.request is None:
            return self.clientId
        return self.clientId if self.replacesClientId else getattr(self.request, "clientId", None)

    def respondWith(self, response):
        """Returns a promise that resolves to the response object"""
        self._responded_with = response
        return response

    def waitUntil(self, promise):
        """Returns a promise that resolves when the response is available"""
        self._pending_promises.append(promise)
        return promise


class ExtendableEvent(Event):
    """ExtendableEvent"""

    # CAPTURING_PHASE = 1
    # AT_TARGET = 2
    # BUBBLING_PHASE = 3

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.extendable = options.get("extendable", True)
        """ Returns whether the event is extendable or not """
        self._pending_promises: list[Any] = []
        """ Returns the time stamp of the event """
        super().__init__(_type, options, *args, **kwargs)

    def waitUntil(self, promise: Any):
        self._pending_promises.append(promise)
        return promise


class SyncEvent(ExtendableEvent):
    """SyncEvent"""

    SYNC: str = "sync"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.tag = options.get("tag", None)
        """ Returns the tag of the sync event """
        self.lastChance = options.get("lastChance", None)
        """ Returns whether the sync event is the last chance or not """
        super().__init__(_type, options, *args, **kwargs)


class SecurityPolicyViolationEvent(ExtendableEvent):
    """SecurityPolicyViolationEvent"""

    SECURITY_POLICY_VIOLATION: str = "securitypolicyviolation"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.blockedURI = options.get("blockedURI", None)
        """ Returns the blocked URI """
        self.violatedDirective = options.get("violatedDirective", None)
        """ Returns the violated directive """
        self.originalPolicy = options.get("originalPolicy", None)
        """ Returns the original policy """
        self.isFrameAncestor = options.get("isFrameAncestor", None)
        """ Returns whether the frame is an ancestor of the frame that violated the policy """
        self.isMainFrame = options.get("isMainFrame", None)
        """ Returns whether the frame is the main frame """
        self.frame = options.get("frame", None)
        """ Returns the frame that violated the policy """
        super().__init__(_type, options, *args, **kwargs)


class DOMContentLoadedEvent(Event):
    """DOMContentLoadedEvent"""

    DOMCONTENTLOADED: str = "DOMContentLoaded"  #:
    # LOAD: str = "load"  #: already on event
    # BEFOREUNLOAD: str = "beforeunload"  #: already on event
    # UNLOAD: str = "unload"  #: already on event
    # readystatechange = "readystatechange"  #: ?? where does this one belong. Have added it to event

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.document = options.get("document", None)
        """ Returns the document that was loaded """
        super().__init__(_type, options, *args, **kwargs)


# class InstallEvent()

# class DeviceMotionEvent(Event):
#     """ DeviceMotionEvent """
#     def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
#         self.acceleration = None
#         """ Returns the acceleration of the device """
#         self.accelerationIncludingGravity = None
#         """ Returns the acceleration of the device, including gravity """
#         self.rotationRate = None
#         """ Returns the rotation rate of the device """
#         self.interval = None
#         """ Returns the time interval between the previous and the current event """
#         super().__init__(_type, options, *args, **kwargs)


# class DeviceOrientationEvent(Event):
#     """ DeviceOrientationEvent """
#     def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
#         self.absolute = None
#         """ Returns true if the orientation is absolute """
#         self.alpha = None
#         """ Returns the orientation of the device in degrees, relative to the Earth's coordinate system """
#         self.beta = None
#         """ Returns the orientation of the device in degrees, relative to the Earth's coordinate system """
#         self.gamma = None
#         """ Returns the orientation of the device in degrees, relative to the Earth's coordinate system """
#         self.interval = None
#         """ Returns the time interval between the previous and the current event """
#         super().__init__(_type, options, *args, **kwargs)


# class DeviceLightEvent(Event):
#     """ DeviceLightEvent """
#     def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
#         self.value = None
#         """ Returns the value of the ambient light sensor """
#         super().__init__(_type, options, *args, **kwargs)


# class DeviceProximityEvent(Event):
#     """ DeviceProximityEvent """
#     def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
#         self.value = None
#         """ Returns the value of the proximity sensor """
#         self.min = None
#         """ Returns the minimum value of the proximity sensor """
#         self.max = None
#         """ Returns the maximum value of the proximity sensor """
#         super().__init__(_type, options, *args, **kwargs)


class TweenEvent(Event):
    """TweenEvent"""

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
        # super.__init__(self, type, bubbles, cancelable)
        super().__init__(_type)  # TODO -
        self.source = source


class PromiseRejectionEvent(Event):  # TODO - put with the promise?
    """PromiseRejectionEvent"""

    UNHANDLED: str = "unhandledrejection"  #:
    HANDLED: str = "rejectionhandled"  #:

    def __init__(self, _type, options=None, *args, **kwargs):
        options = options or kwargs
        self.promise = options.get("promise", None)
        """ Returns the promise that was rejected """
        self.reason = options.get("reason", None)
        """ Returns the reason of the rejection """
        self.isRejected = options.get("isRejected", None)
        """ Returns whether the promise was rejected or not """
        super().__init__(_type, options, *args, **kwargs)


class MessageEvent(Event):
    """MessageEvent"""

    MESSAGE: str = "message"  #:
    CONNECT: str = "connect"  #:
    DISCONNECT: str = "disconnect"  #:

    def __init__(self, _type, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.data = options.get("data", None)
        """ Returns the data of the message """
        self.origin = options.get("origin", None)
        """ Returns the origin of the message """
        self.lastEventId = options.get("lastEventId", None)
        """ Returns the last event id of the message """
        self.source = options.get("source", None)
        """ Returns the source of the message """
        self.ports = options.get("ports", [])
        """ Returns the ports of the message """
        super().__init__(_type, options, *args, **kwargs)


class GlobalEventHandler:
    _handler_names = (
        "onabort", "onblur", "oncancel", "oncanplay", "oncanplaythrough", "onchange", "onclick",
        "onclose", "oncontextmenu", "oncuechange", "ondblclick", "ondrag", "ondragend",
        "ondragenter", "ondragexit", "ondragleave", "ondragover", "ondragstart", "ondrop",
        "ondurationchange", "onemptied", "onended", "onerror", "onfocus", "ongotpointercapture",
        "oninput", "oninvalid", "onkeydown", "onkeypress", "onkeyup", "onload", "onloadeddata",
        "onloadedmetadata", "onloadend", "onloadstart", "onlostpointercapture", "onmouseenter",
        "onmouseleave", "onmousemove", "onmouseout", "onmouseover", "onmouseup", "onpause",
        "onplay", "onplaying", "onpointercancel", "onpointerdown", "onpointerenter",
        "onpointerleave", "onpointermove", "onpointerout", "onpointerover", "onpointerup",
        "onprogress", "onratechange", "onreset", "onresize", "onscroll", "onseeked",
        "onseeking", "onselect", "onselectionchange", "onselectstart", "onshow", "onstalled",
        "onsubmit", "onsuspend", "ontimeupdate", "onvolumechange", "onwaiting", "onwheel",
        "onanimationcancel", "onanimationend", "onanimationiteration", "onauxclick", "onformdata",
        "onmousedown", "ontouchcancel", "ontouchstart", "ontransitioncancel", "ontransitionend",
    )


class WindowEventHandler:
    _handler_names = (
        "onabort", "onafterprint", "onbeforeprint", "onbeforeunload", "onblur", "oncanplay",
        "oncanplaythrough", "onchange", "onclick", "oncontextmenu", "oncopy", "oncuechange",
        "oncut", "ondblclick", "ondrag", "ondragend", "ondragenter", "ondragleave", "ondragover",
        "ondragstart", "ondrop", "ondurationchange", "onemptied", "onended", "onerror", "onfocus",
        "onhashchange", "oninput", "oninvalid", "onkeydown", "onkeypress", "onkeyup", "onload",
        "onloadeddata", "onloadedmetadata", "onloadstart", "onmessage", "onmousedown",
        "onmouseenter", "onmouseleave", "onmousemove", "onmouseout", "onmouseover", "onmouseup",
        "onmousewheel", "onoffline", "ononline", "onpagehide", "onpageshow", "onpaste",
        "onpopstate", "onresize", "onscroll", "onstorage", "onsubmit", "onunload",
    )

    def __init__(self, window):
        super().__init__()
        self.window = window


def _make_default_event_handler(name: str):
    def handler(self, event):
        self._last_event = event
        callback = getattr(self, f"_{name}_callback", None)
        if callable(callback):
            return callback(event)
        return event

    handler.__name__ = name
    return handler


def _install_default_event_handlers(*classes) -> None:
    for cls in classes:
        for name in getattr(cls, "_handler_names", ()):
            setattr(cls, name, _make_default_event_handler(name))


_install_default_event_handlers(GlobalEventHandler, WindowEventHandler)
