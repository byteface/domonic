"""
    domonic.events
    ====================================
    dom events

"""

# from typing import *
import time


class EventDispatcher(object):
    """ EventDispatcher is a class you can extend to give your obj event dispatching abilities """

    def __init__(self, *args, **kwargs):
        self.listeners = {}

    def hasEventListener(self, _type):
        return _type in self.listeners

    # TODO - event: str, function, useCapture: bool
    # def addEventListener(self, event: str, function, useCapture: bool) -> None:
    def addEventListener(self, _type, callback, *args, **kwargs):
        if _type not in self.listeners:
            self.listeners[_type] = []
        self.listeners[_type].append(callback)

    def removeEventListener(self, _type, callback):
        if _type not in self.listeners:
            return

        stack = self.listeners[_type]

        for thing in stack:
            if thing == callback:
                stack.remove(thing)
                return

    def dispatchEvent(self, event):
        if event.type not in self.listeners:
            return True  # huh?. surely false?

        stack = self.listeners[event.type]
        # .slice()
        event.target = self  # TODO/NOTE - is this correct? - cant think where else would set it

        for thing in stack:
            try:
                thing(event)
                # type(thing, (Event,), self)
            except Exception as e:
                print(e)
                thing()  # try calling without params, user may not create param

        return not event.defaultPrevented


class Event(object):
    """ event """
    EMPTIED = "emptied"
    ABORT = "abort"
    AFTERPRINT = "afterprint"
    BEFOREPRINT = "beforeprint"
    BEFOREUNLOAD = "beforeunload"
    CANPLAY = "canplay"
    CANPLAYTHROUGH = "canplaythrough"
    CHANGE = "change"
    DURATIONCHANGE = "durationchange"
    ENDED = "ended"
    ERROR = "error"
    FULLSCREENCHANGE = "fullscreenchange"
    FULLSCREENERROR = "fullscreenerror"
    INPUT = "input"
    INVALID = "invalid"
    LOAD = "load"
    LOADEDDATA = "loadeddata"
    LOADEDMETADATA = "loadedmetadata"
    MESSAGE = "message"
    OFFLINE = "offline"
    ONLINE = "online"
    OPEN = "open"
    PAUSE = "pause"
    PLAY = "play"
    PLAYING = "playing"
    PROGRESS = "progress"
    RATECHANGE = "ratechange"
    RESIZE = "resize"
    RESET = "reset"
    SCROLL = "scroll"
    SEARCH = "search"
    SEEKED = "seeked"
    SEEKING = "seeking"
    SELECT = "select"
    SHOW = "show"
    STALLED = "stalled"
    SUBMIT = "submit"
    SUSPEND = "suspend"
    TOGGLE = "toggle"
    UNLOAD = "unload"
    VOLUMECHANGE = "volumechange"
    WAITING = "waiting"

    # Event("look", {"bubbles":true, "cancelable":false});
    def __init__(self, _type=None, *args, **kwargs):
        # print('type', _type)
        self.type = _type
        self.bubbles = None
        self.cancelable = None
        self.cancelBubble = None
        self.composed = None
        self.currentTarget = None
        self.defaultPrevented = False
        self.eventPhase = None
        self.explicitOriginalTarget = None
        self.isTrusted = None
        self.originalTarget = None
        self.returnValue = None
        self.srcElement = None
        self.target = None
        # ms = time.time_ns() // 1000000 3.7 up
        self.timeStamp = int(round(time.time() * 1000))

    def composedPath(self):
        pass

    def createEvent(self):
        pass

    def initEvent(self, _type=None, *args, **kwargs):
        self.__init__(_type, args, kwargs)

    def msConvertURL(self):
        pass

    def preventDefault(self):
        pass

    def stopImmediatePropagation(self):
        pass

    def stopPropagation(self):
        pass


class MouseEvent(Event):
    """ mouse events """
    CLICK = "click"
    CONTEXTMENU = "contextmenu"
    DBLCLICK = "dblclick"
    MOUSEDOWN = "mousedown"
    MOUSEENTER = "mouseenter"
    MOUSELEAVE = "mouseleave"
    MOUSEMOVE = "mousemove"
    MOUSEOVER = "mouseover"
    MOUSEOUT = "mouseout"
    MOUSEUP = "mouseup"

    def __init__(self, _type, *args, **kwargs):
        # self.args = args
        # self.kwargs = kwargs
        self.x = 0
        self.y = 0
        self._altKey = False
        self._ctrlKey = False
        self._shiftKey = False
        self._metaKey = False
        self._button = None
        self._buttons = []

        super().__init__(_type, *args, **kwargs)

    def initMouseEvent(self, _type=None, canBubble=True, cancelable=True, view=None,
                        detail=None, screenX=0, screenY=0, clientX=0, clientY=0,
                        ctrlKey=False, altKey=False, shiftKey=False, metaKey=False,
                        button=None, relatedTarget=None, from_json={}, *args, **kwargs):
        print('initMouseEvent')
        self._type = _type
        self.canBubble = canBubble
        self.cancelable = cancelable
        self.view = view
        self.detail = detail
        self.screenX = screenX
        self.screenY = screenY
        self.clientX = clientX
        self.clientY = clientY
        self.ctrlKey = ctrlKey
        self.altKey = altKey
        self.shiftKey = shiftKey
        self.metaKey = metaKey
        self.button = button
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
    # getModifierState()    Returns an array containing target ranges that will be affected by the insertion/deletion   MouseEvent
    # MovementX Returns the horizontal coordinate of the mouse pointer relative to the position of the last mousemove event MouseEvent
    # MovementY Returns the vertical coordinate of the mouse pointer relative to the position of the last mousemove event   MouseEvent
    # offsetX   Returns the horizontal coordinate of the mouse pointer relative to the position of the edge of the target element   MouseEvent
    # offsetY   Returns the vertical coordinate of the mouse pointer relative to the position of the edge of the target element MouseEvent
    # pageX Returns the horizontal coordinate of the mouse pointer, relative to the document, when the mouse event was triggered    MouseEvent
    # pageY Returns the vertical coordinate of the mouse pointer, relative to the document, when the mouse event was triggered  MouseEvent
    # region        MouseEvent
    # relatedTarget Returns the element related to the element that triggered the mouse event   MouseEvent, FocusEvent


class KeyboardEvent(Event):
    """ keyboard events """
    KEYDOWN = "keydown"
    KEYPRESS = "keypress"
    KEYUP = "keyup"

    def __init__(self, _type, *args, **kwargs):
        # self.args = args
        # self.kwargs = kwargs
        self._altKey = False
        self._ctrlKey = False
        self._shiftKey = False
        self._metaKey = False

        self.charCode = None
        self.code = None
        self.key = None
        self.keyCode = None

        super().__init__(_type, *args, **kwargs)

    def initKeyboardEvent(self, typeArg, canBubbleArg, cancelableArg,
                        viewArg, charArg, keyArg,
                        locationArg, modifiersListArg, repeat):
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

    # KeyboardEvent
    # isComposing   Returns whether the state of the event is composing or not  InputEvent, KeyboardEvent
    # repeat    Returns whether a key is being hold down repeatedly, or not KeyboardEvent
    # location  Returns the location of a key on the keyboard or device KeyboardEvent


class UiEvent(Event):
    """ UiEvent """
    def __init__(self, _type, *args, **kwargs):
        self.detail = None
        self.view = None
        super().__init__(_type, *args, **kwargs)


class FocusEvent(Event):
    """ FocusEvent """
    BLUR = "blur"
    FOCUS = "focus"
    FOCUSIN = "focusin"
    FOCUSOUT = "focusout"

    def __init__(self, _type, *args, **kwargs):
        self.relatedTarget = None
        super().__init__(_type, *args, **kwargs)


class TouchEvent(Event):
    """ TouchEvent """
    TOUCHCANCEL = "touchcancel"
    TOUCHEND = "touchend"
    TOUCHMOVE = "touchmove"
    TOUCHSTART = "touchstart"

    def __init__(self, _type, *args, **kwargs):
        self.shiftKey = None
        self.altKey = None
        """  Returns whether the "ALT" key was pressed when the touch event was triggered """
        self.changedTouches = None
        """  Returns a list of all the touch objects whose state changed between the previous touch and this touch """
        self.ctrlKey = None
        """ Returns whether the "CTRL" key was pressed when the touch event was triggered """
        self.metaKey = None
        """ Returns whether the "meta" key was pressed when the touch event was triggered """
        self.shiftKey = None
        """  Returns whether the "SHIFT" key was pressed when the touch event was triggered """
        self.targetTouches = None
        """   Returns a list of all the touch objects that are in contact with the surface and where the touchstart event occured on the same target element as the current target element """
        self.touches = None
        """ Returns a list of all the touch objects that are currently in contact with the surface """
        super().__init__(_type, *args, **kwargs)


class WheelEvent(Event):
    """ WheelEvent """
    MOUSEWHEEL = "mousewheel"  # DEPRECATED - USE WHEEL
    WHEEL = "wheel"

    def __init__(self, _type, *args, **kwargs):
        self.deltaX = None
        """ Returns the horizontal scroll amount of a mouse wheel (x-axis) """
        self.deltaY = None
        """ Returns the vertical scroll amount of a mouse wheel (y-axis) """
        self.deltaZ = None
        """ Returns the scroll amount of a mouse wheel for the z-axis """
        self.deltaMode = None
        """ Returns a number that represents the unit of measurements for delta values (pixels, lines or pages) """
        super().__init__(_type, *args, **kwargs)


class AnimationEvent(Event):
    """ AnimationEvent """
    ANIMATIONEND = "animationend"
    ANIMATIONITERATION = "animationiteration"
    ANIMATIONSTART = "animationstart"

    def __init__(self, _type, *args, **kwargs):
        self.animationName = None
        """ Returns the name of the animation """
        self.elapsedTime = None
        """ Returns the number of seconds an animation has been running """
        self.pseudoElement = None
        """ Returns the name of the pseudo-element of the animation """
        super().__init__(_type, *args, **kwargs)


class ClipboardEvent(Event):
    """ ClipboardEvent """
    COPY = "copy"
    CUT = "cut"
    PASTE = "paste"

    def __init__(self, _type, *args, **kwargs):
        self.clipboardData = None
        """ Returns an object containing the data affected by the clipboard operation """
        super().__init__(_type, *args, **kwargs)


class ErrorEvent(Event):
    """ ErrorEvent """
    ERROR = "error"

    def __init__(self, _type, *args, **kwargs):
        self.message = None
        # self.filename=None
        # self.lineno=0
        # self.colno=0
        # self.error={}
        super().__init__(_type, *args, **kwargs)


class SubmitEvent(Event):
    """ SubmitEvent """
    SUBMIT = "submit"

    def __init__(self, _type, *args, **kwargs):
        super().__init__(_type, *args, **kwargs)


class PointerEvent(Event):
    """ PointerEvent """
    POINTER = "pointer"

    def __init__(self, _type, *args, **kwargs):
        self.pointerId = None
        self.width = None
        self.height = None
        self.pressure = None
        self.tangentialPressure = None
        self.tiltX = None
        self.tiltY = None
        self.twist = None
        self.pointerType = None
        self.isPrimary = None
        super().__init__(_type, *args, **kwargs)


class BeforeUnloadEvent(Event):
    BEFOREUNLOAD = "beforeunload"
    """ BeforeUnloadEvent """
    def __init__(self, _type, *args, **kwargs):
        super().__init__(_type, *args, **kwargs)


class SVGEvent(Event):
    TIMER = "svg"
    """ SVGEvent """
    def __init__(self, _type, *args, **kwargs):
        super().__init__(_type, *args, **kwargs)


class TimerEvent(Event):
    TIMER = "timer"
    """ TimerEvent """
    def __init__(self, _type, *args, **kwargs):
        super().__init__(_type, *args, **kwargs)


class DragEvent(Event):
    """ DragEvent """
    DRAG = "drag"
    END = "dragend"
    ENTER = "dragenter"
    LEAVE = "dragleave"
    OVER = "dragover"
    START = "dragstart"
    DROP = "drop"

    def __init__(self, _type, *args, **kwargs):
        self.dataTransfer = None
        """ Returns the data that is dragged/dropped """
        super().__init__(_type, *args, **kwargs)


class HashChangeEvent(Event):
    """ HashChangeEvent """
    CHANGE = "hashchange"

    def __init__(self, _type, *args, **kwargs):
        self.newURL = None
        """ Returns the URL of the document, after the hash has been changed """
        self.oldURL
        """ Returns the URL of the document, before the hash was changed """
        super().__init__(_type, *args, **kwargs)


class InputEvent(Event):
    """ InputEvent """
    def __init__(self, _type, *args, **kwargs):
        self.data = None
        """ Returns the inserted characters """
        self.dataTransfer
        """ Returns an object containing information about the inserted/deleted data """
        self.getTargetRanges
        """ Returns an array containing target ranges that will be affected by the insertion/deletion """
        self.inputType
        """ Returns the type of the change (i.e "inserting" or "deleting") """
        self.isComposing
        """ Returns whether the state of the event is composing or not """
        super().__init__(_type, *args, **kwargs)


class PageTransitionEvent(Event):
    PAGEHIDE = "pagehide"
    PAGESHOW = "pageshow"
    """ PageTransitionEvent """
    def __init__(self, _type, *args, **kwargs):
        self.persisted = None
        """ Returns whether the webpage was cached by the browser """
        super().__init__(_type, *args, **kwargs)


class PopStateEvent(Event):
    """ PopStateEvent """
    def __init__(self, _type, *args, **kwargs):
        self.state = None
        """ Returns an object containing a copy of the history entries """
        super().__init__(_type, *args, **kwargs)


class StorageEvent(Event):
    """ StorageEvent """
    def __init__(self, _type, *args, **kwargs):
        self.key = None
        """ Returns the key of the changed storage item """
        self.newValue = None
        """ Returns the new value of the changed storage item """
        self.oldValue = None
        """ Returns the old value of the changed storage item """
        self.storageArea = None
        """ Returns an object representing the affected storage object """
        self.url = None
        """ Returns the URL of the changed item's document """
        super().__init__(_type, *args, **kwargs)


class TransitionEvent(Event):
    TRANSITIONEND = "transitionend"
    """ TransitionEvent """
    def __init__(self, _type, *args, **kwargs):
        self.propertyName = None
        """ Returns the name of the transition"""
        self.elapsedTime = None
        """  Returns the number of seconds a transition has been running """
        self.pseudoElement = None
        """ Returns the name of the pseudo-element of the transition """
        super().__init__(_type, *args, **kwargs)


class ProgressEvent(Event):
    """ ProgressEvent """
    LOADSTART = "loadstart"

    def __init__(self, _type, *args, **kwargs):
        super().__init__(_type, *args, **kwargs)


class CustomEvent(Event):
    """ CustomEvent """
    def __init__(self, _type, *args, **kwargs):
        self.detail = None
        super().__init__(_type, *args, **kwargs)

    def initCustomEvent(self):
        pass


class TweenEvent(Event):
    """ TweenEvent """
    START = "onStart"
    STOP = "onStop"
    RESET = "onReset"
    PAUSE = "onPause"
    UNPAUSE = "onUnPause"
    UPDATE_START = "onUpdateStart"
    UPDATE_END = "onUpdateEnd"
    COMPLETE = "onComplete"

    TIMER = "onTimer"
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


class GlobalEventHandler:

    def onabort(self):
        raise NotImplementedError

    def onblur(self):
        raise NotImplementedError

    def oncancel(self):
        raise NotImplementedError

    def oncanplay(self):
        raise NotImplementedError

    def oncanplaythrough(self):
        raise NotImplementedError

    def onchange(self):
        raise NotImplementedError

    def onclick(self):
        raise NotImplementedError

    def onclose(self):
        raise NotImplementedError

    def oncontextmenu(self):
        raise NotImplementedError

    def oncuechange(self):
        raise NotImplementedError

    def ondblclick(self):
        raise NotImplementedError

    def ondrag(self):
        raise NotImplementedError

    def ondragend(self):
        raise NotImplementedError

    def ondragenter(self):
        raise NotImplementedError

    def ondragexit(self):
        raise NotImplementedError

    def ondragleave(self):
        raise NotImplementedError

    def ondragover(self):
        raise NotImplementedError

    def ondragstart(self):
        raise NotImplementedError

    def ondrop(self):
        raise NotImplementedError

    def ondurationchange(self):
        raise NotImplementedError

    def onemptied(self):
        raise NotImplementedError

    def onended(self):
        raise NotImplementedError

    def onerror(self):
        raise NotImplementedError

    def onfocus(self):
        raise NotImplementedError

    def ongotpointercapture(self):
        raise NotImplementedError

    def oninput(self):
        raise NotImplementedError

    def oninvalid(self):
        raise NotImplementedError

    def onkeydown(self):
        raise NotImplementedError

    def onkeypress(self):
        raise NotImplementedError

    def onkeyup(self):
        raise NotImplementedError

    def onload(self):
        raise NotImplementedError

    def onloadeddata(self):
        raise NotImplementedError

    def onloadedmetadata(self):
        raise NotImplementedError

    def onloadend(self):
        raise NotImplementedError

    def onloadstart(self):
        raise NotImplementedError

    def onlostpointercapture(self):
        raise NotImplementedError

    def onmouseenter(self):
        raise NotImplementedError

    def onmouseleave(self):
        raise NotImplementedError

    def onmousemove(self):
        raise NotImplementedError

    def onmouseout(self):
        raise NotImplementedError

    def onmouseover(self):
        raise NotImplementedError

    def onmouseup(self):
        raise NotImplementedError

    def onpause(self):
        raise NotImplementedError

    def onplay(self):
        raise NotImplementedError

    def onplaying(self):
        raise NotImplementedError

    def onpointercancel(self):
        raise NotImplementedError

    def onpointerdown(self):
        raise NotImplementedError

    def onpointerenter(self):
        raise NotImplementedError

    def onpointerleave(self):
        raise NotImplementedError

    def onpointermove(self):
        raise NotImplementedError

    def onpointerout(self):
        raise NotImplementedError

    def onpointerover(self):
        raise NotImplementedError

    def onpointerup(self):
        raise NotImplementedError

    def onprogress(self):
        raise NotImplementedError

    def onratechange(self):
        raise NotImplementedError

    def onreset(self):
        raise NotImplementedError

    def onresize(self):
        raise NotImplementedError

    def onscroll(self):
        raise NotImplementedError

    def onseeked(self):
        raise NotImplementedError

    def onseeking(self):
        raise NotImplementedError

    def onselect(self):
        raise NotImplementedError

    def onselectionchange(self):
        raise NotImplementedError

    def onselectstart(self):
        raise NotImplementedError

    def onshow(self):
        raise NotImplementedError

    def onstalled(self):
        raise NotImplementedError

    def onsubmit(self):
        raise NotImplementedError

    def onsuspend(self):
        raise NotImplementedError

    def ontimeupdate(self):
        raise NotImplementedError

    def onvolumechange(self):
        raise NotImplementedError

    def onwaiting(self):
        raise NotImplementedError

    def onwheel(self):
        raise NotImplementedError

    def onanimationcancel(self):
        raise NotImplementedError

    def onanimationend(self):
        raise NotImplementedError

    def onanimationiteration(self):
        raise NotImplementedError

    def onauxclick(self):
        raise NotImplementedError

    def onformdata(self):
        raise NotImplementedError

    def onmousedown(self):
        raise NotImplementedError

    def ontouchcancel(self):
        raise NotImplementedError

    def ontouchstart(self):
        raise NotImplementedError

    def ontransitioncancel(self):
        raise NotImplementedError

    def ontransitionend(self):
        raise NotImplementedError
