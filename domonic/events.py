"""
    domonic.events
    ====================================
    dom events

"""

from typing import *
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
    EMPTIED = "onemptied"
    ABORT = "onabort"
    AFTERPRINT = "onafterprint"
    BEFOREPRINT = "onbeforeprint"
    BEFOREUNLOAD = "onbeforeunload"
    CANPLAY = "oncanplay"
    CANPLAYTHROUGH = "oncanplaythrough"
    CHANGE = "onchange"
    DURATIONCHANGE = "ondurationchange"
    ENDED = "onended"
    ERROR = "onerror"
    FULLSCREENCHANGE = "onfullscreenchange"
    FULLSCREENERROR = "onfullscreenerror"
    INPUT = "oninput"
    INVALID = "oninvalid"
    LOAD = "onload"
    LOADEDDATA = "onloadeddata"
    LOADEDMETADATA = "onloadedmetadata"
    MESSAGE = "onmessage"
    OFFLINE = "onoffline"
    ONLINE = "ononline"
    OPEN = "onopen"
    PAUSE = "onpause"
    PLAY = "onplay"
    PLAYING = "onplaying"
    PROGRESS = "onprogress"
    RATECHANGE = "onratechange"
    RESIZE = "onresize"
    RESET = "onreset"
    SCROLL = "onscroll"
    SEARCH = "onsearch"
    SEEKED = "onseeked"
    SEEKING = "onseeking"
    SELECT = "onselect"
    SHOW = "onshow"
    STALLED = "onstalled"
    SUBMIT = "onsubmit"
    SUSPEND = "onsuspend"
    TOGGLE = "ontoggle"
    UNLOAD = "onunload"
    VOLUMECHANGE = "onvolumechange"
    WAITING = "onwaiting"

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
    CLICK = "onclick"
    CONTEXTMENU = "oncontextmenu"
    DBLCLICK = "ondblclick"
    MOUSEDOWN = "onmousedown"
    MOUSEENTER = "onmouseenter"
    MOUSELEAVE = "onmouseleave"
    MOUSEMOVE = "onmousemove"
    MOUSEOVER = "onmouseover"
    MOUSEOUT = "onmouseout"
    MOUSEUP = "onmouseup"

    def __init__(self, evt, *args, **kwargs):
        # self.args = args
        # self.kwargs = kwargs
        self.x = 0
        self.y = 0
        super().__init__(evt, *args, **kwargs)

    # MOUSE_EVENT
    # altKey    Returns whether the "ALT" key was pressed when the mouse event was triggered    MouseEvent, KeyboardEvent, TouchEvent
    # button    Returns which mouse button was pressed when the mouse event was triggered   MouseEvent
    # buttons   Returns which mouse buttons were pressed when the mouse event was triggered MouseEvent
    # ctrlKey   Returns whether the "CTRL" key was pressed when the mouse event was triggered   MouseEvent, KeyboardEvent, TouchEvent
    # getModifierState()    Returns an array containing target ranges that will be affected by the insertion/deletion   MouseEvent
    # metaKey   Returns whether the "META" key was pressed when an event was triggered  MouseEvent, KeyboardEvent, TouchEvent
    # MovementX Returns the horizontal coordinate of the mouse pointer relative to the position of the last mousemove event MouseEvent
    # MovementY Returns the vertical coordinate of the mouse pointer relative to the position of the last mousemove event   MouseEvent
    # offsetX   Returns the horizontal coordinate of the mouse pointer relative to the position of the edge of the target element   MouseEvent
    # offsetY   Returns the vertical coordinate of the mouse pointer relative to the position of the edge of the target element MouseEvent
    # pageX Returns the horizontal coordinate of the mouse pointer, relative to the document, when the mouse event was triggered    MouseEvent
    # pageY Returns the vertical coordinate of the mouse pointer, relative to the document, when the mouse event was triggered  MouseEvent
    # region        MouseEvent
    # relatedTarget Returns the element related to the element that triggered the mouse event   MouseEvent, FocusEvent
    # shiftKey  Returns whether the "SHIFT" key was pressed when an event was triggered MouseEvent, KeyboardEvent, TouchEvent
    # which Returns which mouse button was pressed when the mouse event was triggered   MouseEvent, KeyboardEvent


class KeyboardEvent(Event):
    """ keyboard events """
    KEYDOWN = "onkeydown"
    KEYPRESS = "onkeypress"
    KEYUP = "onkeyup"

    def __init__(self, *args, **kwargs):
        # self.args = args
        # self.kwargs = kwargs
        super().__init__(evt, *args, **kwargs)

    # KeyboardEvent
    # altKey    Returns whether the "ALT" key was pressed when the mouse event was triggered    MouseEvent, KeyboardEvent, TouchEvent
    # ctrlKey   Returns whether the "CTRL" key was pressed when the mouse event was triggered   MouseEvent, KeyboardEvent, TouchEvent
    # metaKey   Returns whether the "META" key was pressed when an event was triggered  MouseEvent, KeyboardEvent, TouchEvent
    # shiftKey  Returns whether the "SHIFT" key was pressed when an event was triggered MouseEvent, KeyboardEvent, TouchEvent
    # which Returns which mouse button was pressed when the mouse event was triggered   MouseEvent, KeyboardEvent
    # charCode  Returns the Unicode character code of the key that triggered the onkeypress event   KeyboardEvent
    # code  Returns the code of the key that triggered the event    KeyboardEvent
    # isComposing   Returns whether the state of the event is composing or not  InputEvent, KeyboardEvent
    # key   Returns the key value of the key represented by the event   KeyboardEvent, StorageEvent
    # keyCode   Returns the Unicode character code of the key that triggered the onkeypress event, or the Unicode key code of the key that triggered the onkeydown or onkeyup event KeyboardEvent
    # location  Returns the location of a key on the keyboard or device KeyboardEvent
    # repeat    Returns whether a key is being hold down repeatedly, or not KeyboardEvent


class UiEvent(Event):
    """ UiEvent """
    def __init__(self, *args, **kwargs):
        self.detail = None
        self.view = None
        super().__init__(evt, *args, **kwargs)


class FocusEvent(Event):
    """ FocusEvent """
    BLUR = "onblur"
    FOCUS = "onfocus"
    FOCUSIN = "onfocusin"
    FOCUSOUT = "onfocusout"

    def __init__(self, *args, **kwargs):
        self.relatedTarget = None
        super().__init__(evt, *args, **kwargs)


class TouchEvent(Event):
    """ TouchEvent """
    TOUCHCANCEL = "ontouchcancel"
    TOUCHEND = "ontouchend"
    TOUCHMOVE = "ontouchmove"
    TOUCHSTART = "ontouchstart"

    def __init__(self, *args, **kwargs):
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
        super().__init__(evt, *args, **kwargs)


class WheelEvent(Event):
    """ WheelEvent """
    MOUSEWHEEL = "onmousewheel"  # DEPRECATED - USE ONWHEEL
    WHEEL = "onwheel"

    def __init__(self, *args, **kwargs):
        self.deltaX = None
        """ Returns the horizontal scroll amount of a mouse wheel (x-axis) """
        self.deltaY = None
        """ Returns the vertical scroll amount of a mouse wheel (y-axis) """
        self.deltaZ = None
        """ Returns the scroll amount of a mouse wheel for the z-axis """
        self.deltaMode = None
        """ Returns a number that represents the unit of measurements for delta values (pixels, lines or pages) """
        super().__init__(evt, *args, **kwargs)


class AnimationEvent(Event):
    """ AnimationEvent """
    ANIMATIONEND = "onanimationend"
    ANIMATIONITERATION = "onanimationiteration"
    ANIMATIONSTART = "onanimationstart"

    def __init__(self, *args, **kwargs):
        self.animationName = None
        """ Returns the name of the animation """
        self.elapsedTime = None
        """ Returns the number of seconds an animation has been running """
        self.pseudoElement = None
        """ Returns the name of the pseudo-element of the animation """
        super().__init__(evt, *args, **kwargs)


class ClipboardEvent(Event):
    """ ClipboardEvent """
    COPY = "oncopy"
    CUT = "oncut"
    PASTE = "onpaste"

    def __init__(self, *args, **kwargs):
        self.clipboardData = None
        """ Returns an object containing the data affected by the clipboard operation """
        super().__init__(evt, *args, **kwargs)


class DragEvent(Event):
    """ DragEvent """
    DRAG = "ondrag"
    END = "ondragend"
    ENTER = "ondragenter"
    LEAVE = "ondragleave"
    OVER = "ondragover"
    START = "ondragstart"
    DROP = "ondrop"

    def __init__(self, *args, **kwargs):
        self.dataTransfer = None
        """ Returns the data that is dragged/dropped """
        super().__init__(evt, *args, **kwargs)


class HashChangeEvent(Event):
    """ HashChangeEvent """
    CHANGE = "onhashchange"

    def __init__(self, *args, **kwargs):
        self.newURL = None
        """ Returns the URL of the document, after the hash has been changed """
        self.oldURL
        """ Returns the URL of the document, before the hash was changed """
        super().__init__(evt, *args, **kwargs)


class InputEvent(Event):
    """ InputEvent """
    def __init__(self, *args, **kwargs):
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
        super().__init__(evt, *args, **kwargs)


class PageTransitionEvent(Event):
    PAGEHIDE = "onpagehide"
    PAGESHOW = "onpageshow"
    """ PageTransitionEvent """
    def __init__(self, *args, **kwargs):
        self.persisted = None
        """ Returns whether the webpage was cached by the browser """
        super().__init__(evt, *args, **kwargs)


class PopStateEvent(Event):
    """ PopStateEvent """
    def __init__(self, *args, **kwargs):
        self.state = None
        """ Returns an object containing a copy of the history entries """
        super().__init__(evt, *args, **kwargs)


class StorageEvent(Event):
    """ StorageEvent """
    def __init__(self, *args, **kwargs):
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
        super().__init__(evt, *args, **kwargs)


class TransitionEvent(Event):
    TRANSITIONEND = "ontransitionend"
    """ TransitionEvent """
    def __init__(self, *args, **kwargs):
        self.propertyName = None
        """ Returns the name of the transition"""
        self.elapsedTime = None
        """  Returns the number of seconds a transition has been running """
        self.pseudoElement = None
        """ Returns the name of the pseudo-element of the transition """
        super().__init__(evt, *args, **kwargs)


class ProgressEvent(Event):
    """ CustomEvent """
    LOADSTART = "onloadstart"

    def __init__(self, *args, **kwargs):
        super().__init__(evt, *args, **kwargs)


class CustomEvent(Event):
    """ CustomEvent """
    def __init__(self, *args, **kwargs):
        self.detail = None
        super().__init__(evt, *args, **kwargs)

    def initCustomEvent(self):
        pass


class TweenEvent(Event):
    
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
    
    def __init__(self, _type, source = None, bubbles = False, cancelable = False):
        # super.__init__(self, type, bubbles, cancelable)
        super().__init__(_type) # TODO -
        self.source = source
