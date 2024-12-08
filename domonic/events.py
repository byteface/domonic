"""
    domonic.events
    ====================================

    https://developer.mozilla.org/en-US/docs/Web/Events

"""

from typing import Dict, List, Any
import time


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
        self.listeners: Dict[str, List] = {}

    def hasEventListener(self, eventType: str) -> bool:
        """
        Check if an event listener for the given event type exists.

        Args:
            eventType (str): The type of the event.

        Returns:
            bool: True if listeners for the event type exist, otherwise False.
        """
        return eventType in self.listeners

    def addEventListener(self, eventType: str, callback, *args, **kwargs) -> None:
        """
        Add an event listener for the given event type.

        Args:
            eventType (str): The type of the event to listen for.
            callback (Callable): The callback function to be executed when the event occurs.
        """
        if eventType not in self.listeners:
            self.listeners[eventType] = []
        self.listeners[eventType].append(callback)

    def removeEventListener(self, eventType: str, callback) -> None:
        """
        Remove an event listener for the given event type.

        Args:
            eventType (str): The type of the event.
            callback (Callable): The callback function to be removed.
        """
        if eventType in self.listeners:
            stack = self.listeners[eventType]
            if callback in stack:
                stack.remove(callback)

    def dispatchEvent(self, event: Dict[str, Any]) -> bool:
        """
        Dispatch the specified event to all registered event listeners.

        Args:
            event (Dict): The event object to be dispatched.

        Returns:
            bool: True if the event was successfully dispatched, otherwise False.
        """
        eventType = event.type
        if eventType in self.listeners:
            stack = self.listeners[eventType]
            event.target = self
            for callback in stack:
                try:
                    callback(event)
                except Exception as e:
                    print(e)
            return not event.defaultPrevented
        return True

    async def dispatchEventAsync(self, event: Dict[str, Any]) -> bool:
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

        eventType = event.get("type", None)
        if eventType in self.listeners:
            stack = self.listeners[eventType]
            event["target"] = self
            for callback in stack:
                try:
                    if hasattr(callback, '__await__'):
                        await callback(event)
                    else:
                        callback(event)
                except Exception as e:
                    print(e)
            return not event.get("defaultPrevented", False)
        return True


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

    CAPTURING_PHASE: int = 1
    AT_TARGET: int = 2
    BUBBLING_PHASE: int = 3

    def __str__(self) -> str:
        return self.type + ":" + str(self.timeStamp)

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.type: str = _type
        self.bubbles: bool = options.get("bubbles", True)
        self.cancelable: bool = options.get("cancelable", True)
        self.cancelBubble: bool = options.get("cancelBubble", False)
        self.composed: bool = options.get("composed", True)
        self.currentTarget: object = options.get("currentTarget", None)
        self.defaultPrevented: bool = options.get("defaultPrevented", False)
        # self.eventPhase: int = options.get("eventPhase", None)
        self.eventPhase: int = options.get("eventPhase", Event.AT_TARGET)
        self.explicitOriginalTarget: object = options.get("explicitOriginalTarget", None)
        self.isTrusted: bool = options.get("isTrusted", False)
        self.originalTarget: object = options.get("originalTarget", None)
        self.returnValue: bool = options.get("returnValue", True)
        self.srcElement: object = options.get("srcElement", None)
        self.target: object = options.get("target", None)
        # ms = time.time_ns() # 1000000 py3.7 up
        self.timeStamp: float = int(round(time.time() * 1000))

    def composedPath(self):
        """
        Returns a list of the event's path, from the root to the target.
        """
        path = []
        current_target = self.target
        while current_target is not None:
            path.append(current_target)
            if hasattr(current_target, "parentNode"):
                current_target = current_target.parentNode
            else:
                break
        # Include the window as the final item in the path.
        if hasattr(self.target, "defaultView"):
            path.append(self.target.defaultView)
        return path

    def initEvent(self, _type: str = None, *args, **kwargs) -> "Event":
        """Initialize the event."""
        self.__init__(_type, args, kwargs)

    def stopPropagation(self):
        """[prevents further propagation of the current event in the capturing and bubbling phases]"""
        self.cancelBubble = True  # Set the cancelBubble flag to stop propagation

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
        self.defaultPrevented = True

    def stopImmediatePropagation(self) -> None:
        """
        Prevents further propagation of the current event and immediately stops other event listeners in the same phase from being invoked.

        This method is used to stop the event's propagation immediately and ensure that no other listeners in the same phase are invoked.

        Returns:
            None
        """
        self.cancelBubble = True
        self.defaultPrevented = True


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
        self._type = _type
        self.canBubble = canBubble
        self.cancelable = cancelable
        self.view = view
        self.detail = detail


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
        self._clientX = options.get("clientY", 0)
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
        self._type = _type
        self.canBubble = canBubble
        self.cancelable = cancelable
        self.view = view
        self.detail = detail
        self.screenX = screenX
        self.screenY = screenY
        self._clientX = clientX
        self._clientY = clientY
        self._ctrlKey = ctrlKey
        self._altKey = altKey
        self._shiftKey = shiftKey
        self._metaKey = metaKey
        self._button = button
        self.relatedTarget = relatedTarget
        # TODO - parse from_json - so can relay

    @property
    def clientX(self):
        return self.x

    @property
    def clientY(self):
        return self.y

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
    def getModifierState(self):
        """Returns an array containing target ranges that will be affected by the insertion/deletion"""
        pass

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
        self._type = typeArg
        self.canBubbleArg = canBubbleArg
        self.cancelableArg = cancelableArg
        self.viewArg = viewArg
        self.charArg = charArg
        self.keyArg = keyArg
        self.locationArg = locationArg
        self.modifiersListArg = modifiersListArg
        self.repeat = repeat

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
        # self.filename=None
        # self.lineno=0
        # self.colno=0
        # self.error={}
        super().__init__(_type, options, *args, **kwargs)


class SubmitEvent(Event):
    """SubmitEvent"""

    SUBMIT: str = "submit"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        super().__init__(_type, options, *args, **kwargs)


class PointerEvent(Event):
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
        super().__init__(_type, options, *args, **kwargs)

    def getCoalescedEvents(self):
        pass

    def getPredictedEvents(self):
        pass

    # def getCurrentPoint(self, element):
    #     """ Returns the current coordinates of the specified element relative to the viewport. """
    #     pass

    # def getIntermediatePoints(self, element):
    #     """ Returns the coordinates of all the intermediate points of the pointer along the path of the pointer. """
    #     pass


class BeforeUnloadEvent(Event):
    BEFOREUNLOAD = "beforeunload"  #:
    """ BeforeUnloadEvent """

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        super().__init__(_type, options, *args, **kwargs)


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
        pass


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
        self.propertyName = None
        """ Returns the name of the transition"""
        self.elapsedTime = None
        """  Returns the number of seconds a transition has been running """
        self.pseudoElement = None
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
        self.lengthComputable: bool = options.get("lengthComputable", None)
        self.loaded: int = options.get("loaded", None)
        self.total: int = options.get("total", None)
        super().__init__(_type, options, *args, **kwargs)


class CustomEvent(Event):
    """CustomEvent"""

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.detail = None
        super().__init__(_type, options, *args, **kwargs)

    def initCustomEvent(self):
        pass


class GamePadEvent(Event):
    """GamePadEvent"""

    START: str = "gamepadconnected"  #:
    STOP: str = "gamepaddisconnected"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.gamepad = None
        super().__init__(_type, options, *args, **kwargs)


# TODO - tests and service worker API
class FetchEvent(Event):
    """FetchEvent"""

    FETCH: str = "fetch"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.clientId = None
        """ Returns the client ID of the fetch request """
        self.request = None
        """ Returns the request object """
        self.isReload = None
        """ Returns whether the request is a reload or not """
        super().__init__(_type, options, *args, **kwargs)

    @property
    def isReload(self):
        return self.request.url == self.request.referrer

    @property
    def replacesClientId(self):
        return self.clientId != self.request.clientId

    @property
    def resultingClientId(self):
        return self.clientId if self.replacesClientId else self.request.clientId

    def respondWith(self, response):
        """Returns a promise that resolves to the response object"""
        pass

    def waitUntil(self, promise):
        """Returns a promise that resolves when the response is available"""
        pass


class ExtendableEvent(Event):
    """ExtendableEvent"""

    # CAPTURING_PHASE = 1
    # AT_TARGET = 2
    # BUBBLING_PHASE = 3

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.extendable = None
        """ Returns whether the event is extendable or not """
        self.timeStamp = None
        """ Returns the time stamp of the event """
        # self.waitUntil(promise)
        """ Returns a promise that resolves when the event is handled """
        super().__init__(_type, options, *args, **kwargs)


class SyncEvent(ExtendableEvent):
    """SyncEvent"""

    SYNC: str = "sync"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.tag = None
        """ Returns the tag of the sync event """
        self.lastChance = None
        """ Returns whether the sync event is the last chance or not """
        super().__init__(_type, options, *args, **kwargs)


class SecurityPolicyViolationEvent(ExtendableEvent):
    """SecurityPolicyViolationEvent"""

    SECURITY_POLICY_VIOLATION: str = "securitypolicyviolation"  #:

    def __init__(self, _type: str, options: dict = None, *args, **kwargs) -> None:
        options = options or kwargs  # if options is none use kwargs
        self.blockedURI = None
        """ Returns the blocked URI """
        self.violatedDirective = None
        """ Returns the violated directive """
        self.originalPolicy = None
        """ Returns the original policy """
        self.isFrameAncestor = None
        """ Returns whether the frame is an ancestor of the frame that violated the policy """
        self.isMainFrame = None
        """ Returns whether the frame is the main frame """
        self.frame = None
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
        self.promise = None
        """ Returns the promise that was rejected """
        self.reason = None
        """ Returns the reason of the rejection """
        self.isRejected = None
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
        self.ports = options.get("ports", None)
        """ Returns the ports of the message """
        super().__init__(_type, options, *args, **kwargs)


class GlobalEventHandler:  # (EventDispatcher):

    # def __init__(self):
    #     super().__init__(self)
    #     self.addEventListener(KeyboardEvent.KEYDOWN, self.onkeydown)
    #     self.addEventListener(KeyboardEvent.KEYUP, self.onkeyup)

    #     self.addEventListener(MouseEvent.MOUSEMOVE, self.onmousemove)
    #     self.addEventListener(MouseEvent.MOUSEDOWN, self.onmousedown)
    #     self.addEventListener(MouseEvent.MOUSEUP, self.onmouseup)

    #     self.addEventListener(DragEvent.DRAG, self.ondrag)
    #     self.addEventListener(DragEvent.END, self.ondragend)
    #     self.addEventListener(DragEvent.ENTER, self.ondragenter)
    #     self.addEventListener(DragEvent.EXIT, self.ondragexit)
    #     self.addEventListener(DragEvent.LEAVE, self.ondragleave)
    #     self.addEventListener(DragEvent.OVER, self.ondragover)
    #     self.addEventListener(DragEvent.START, self.ondragstart)
    #     self.addEventListener(DragEvent.DROP, self.ondrop)

    #     self.addEventListener(ClipboardEvent.CUT, self.oncut)
    #     self.addEventListener(ClipboardEvent.COPY, self.oncopy)
    #     self.addEventListener(ClipboardEvent.PASTE, self.onpaste)

    def onabort(self, event):
        print(event)
        raise NotImplementedError

    def onblur(self, event):
        print(event)
        raise NotImplementedError

    def oncancel(self, event):
        print(event)
        raise NotImplementedError

    def oncanplay(self, event):
        print(event)
        raise NotImplementedError

    def oncanplaythrough(self, event):
        print(event)
        raise NotImplementedError

    def onchange(self, event):
        print(event)
        raise NotImplementedError

    def onclick(self, event):
        print(event)
        raise NotImplementedError

    def onclose(self, event):
        print(event)
        raise NotImplementedError

    def oncontextmenu(self, event):
        print(event)
        raise NotImplementedError

    def oncuechange(self, event):
        print(event)
        raise NotImplementedError

    def ondblclick(self, event):
        print(event)
        raise NotImplementedError

    def ondrag(self, event):
        print(event)
        raise NotImplementedError

    def ondragend(self, event):
        print(event)
        raise NotImplementedError

    def ondragenter(self, event):
        print(event)
        raise NotImplementedError

    def ondragexit(self, event):
        print(event)
        raise NotImplementedError

    def ondragleave(self, event):
        print(event)
        raise NotImplementedError

    def ondragover(self, event):
        print(event)
        raise NotImplementedError

    def ondragstart(self, event):
        print(event)
        raise NotImplementedError

    def ondrop(self, event):
        print(event)
        raise NotImplementedError

    def ondurationchange(self, event):
        print(event)
        raise NotImplementedError

    def onemptied(self, event):
        print(event)
        raise NotImplementedError

    def onended(self, event):
        print(event)
        raise NotImplementedError

    def onerror(self, event):
        print(event)
        raise NotImplementedError

    def onfocus(self, event):
        print(event)
        raise NotImplementedError

    def ongotpointercapture(self, event):
        print(event)
        raise NotImplementedError

    def oninput(self, event):
        print(event)
        raise NotImplementedError

    def oninvalid(self, event):
        print(event)
        raise NotImplementedError

    def onkeydown(self, event):
        print(event)
        raise NotImplementedError

    def onkeypress(self, event):
        print(event)
        raise NotImplementedError

    def onkeyup(self, event):
        print(event)
        raise NotImplementedError

    def onload(self, event):
        print(event)
        raise NotImplementedError

    def onloadeddata(self, event):
        print(event)
        raise NotImplementedError

    def onloadedmetadata(self, event):
        print(event)
        raise NotImplementedError

    def onloadend(self, event):
        print(event)
        raise NotImplementedError

    def onloadstart(self, event):
        print(event)
        raise NotImplementedError

    def onlostpointercapture(self, event):
        print(event)
        raise NotImplementedError

    def onmouseenter(self, event):
        print(event)
        raise NotImplementedError

    def onmouseleave(self, event):
        print(event)
        raise NotImplementedError

    def onmousemove(self, event):
        print(event)
        raise NotImplementedError

    def onmouseout(self, event):
        print(event)
        raise NotImplementedError

    def onmouseover(self, event):
        print(event)
        raise NotImplementedError

    def onmouseup(self, event):
        print(event)
        raise NotImplementedError

    def onpause(self, event):
        print(event)
        raise NotImplementedError

    def onplay(self, event):
        print(event)
        raise NotImplementedError

    def onplaying(self, event):
        print(event)
        raise NotImplementedError

    def onpointercancel(self, event):
        print(event)
        raise NotImplementedError

    def onpointerdown(self, event):
        print(event)
        raise NotImplementedError

    def onpointerenter(self, event):
        print(event)
        raise NotImplementedError

    def onpointerleave(self, event):
        print(event)
        raise NotImplementedError

    def onpointermove(self, event):
        print(event)
        raise NotImplementedError

    def onpointerout(self, event):
        print(event)
        raise NotImplementedError

    def onpointerover(self, event):
        print(event)
        raise NotImplementedError

    def onpointerup(self, event):
        print(event)
        raise NotImplementedError

    def onprogress(self, event):
        print(event)
        raise NotImplementedError

    def onratechange(self, event):
        print(event)
        raise NotImplementedError

    def onreset(self, event):
        print(event)
        raise NotImplementedError

    def onresize(self, event):
        print(event)
        raise NotImplementedError

    def onscroll(self, event):
        print(event)
        raise NotImplementedError

    def onseeked(self, event):
        print(event)
        raise NotImplementedError

    def onseeking(self, event):
        print(event)
        raise NotImplementedError

    def onselect(self, event):
        print(event)
        raise NotImplementedError

    def onselectionchange(self, event):
        print(event)
        raise NotImplementedError

    def onselectstart(self, event):
        print(event)
        raise NotImplementedError

    def onshow(self, event):
        print(event)
        raise NotImplementedError

    def onstalled(self, event):
        print(event)
        raise NotImplementedError

    def onsubmit(self, event):
        print(event)
        raise NotImplementedError

    def onsuspend(self, event):
        print(event)
        raise NotImplementedError

    def ontimeupdate(self, event):
        print(event)
        raise NotImplementedError

    def onvolumechange(self, event):
        print(event)
        raise NotImplementedError

    def onwaiting(self, event):
        print(event)
        raise NotImplementedError

    def onwheel(self, event):
        print(event)
        raise NotImplementedError

    def onanimationcancel(self, event):
        print(event)
        raise NotImplementedError

    def onanimationend(self, event):
        print(event)
        raise NotImplementedError

    def onanimationiteration(self, event):
        print(event)
        raise NotImplementedError

    def onauxclick(self, event):
        print(event)
        raise NotImplementedError

    def onformdata(self, event):
        print(event)
        raise NotImplementedError

    def onmousedown(self, event):
        print(event)
        raise NotImplementedError

    def ontouchcancel(self, event):
        print(event)
        raise NotImplementedError

    def ontouchstart(self, event):
        print(event)
        raise NotImplementedError

    def ontransitioncancel(self, event):
        print(event)
        raise NotImplementedError

    def ontransitionend(self, event):
        print(event)
        raise NotImplementedError


class WindowEventHandler:  # (EventHandler): # TODO - put in the window module?
    def __init__(self, window):
        super().__init__()
        self.window = window

    def onabort(self, event):
        print(event)
        raise NotImplementedError

    def onafterprint(self, event):
        print(event)
        raise NotImplementedError

    def onbeforeprint(self, event):
        print(event)
        raise NotImplementedError

    def onbeforeunload(self, event):
        print(event)
        raise NotImplementedError

    def onblur(self, event):
        print(event)
        raise NotImplementedError

    def oncanplay(self, event):
        print(event)
        raise NotImplementedError

    def oncanplaythrough(self, event):
        print(event)
        raise NotImplementedError

    def onchange(self, event):
        print(event)
        raise NotImplementedError

    def onclick(self, event):
        print(event)
        raise NotImplementedError

    def oncontextmenu(self, event):
        print(event)
        raise NotImplementedError

    def oncopy(self, event):
        print(event)
        raise NotImplementedError

    def oncuechange(self, event):
        print(event)
        raise NotImplementedError

    def oncut(self, event):
        print(event)
        raise NotImplementedError

    def ondblclick(self, event):
        print(event)
        raise NotImplementedError

    def ondrag(self, event):
        print(event)
        raise NotImplementedError

    def ondragend(self, event):
        print(event)
        raise NotImplementedError

    def ondragenter(self, event):
        print(event)
        raise NotImplementedError

    def ondragleave(self, event):
        print(event)
        raise NotImplementedError

    def ondragover(self, event):
        print(event)
        raise NotImplementedError
