"""
    domonic.events
    ====================================
    dom events

"""

from typing import *
import time


class Event(object):
    """ events """

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

    def __init__(self, *args, **kwargs):
        # self.args = args
        # self.kwargs = kwargs
        # super().__init__()
        pass

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
    # onclick   The event occurs when the user clicks on an element MouseEvent
    # oncontextmenu The event occurs when the user right-clicks on an element to open a context menu    MouseEvent
    # ondblclick    The event occurs when the user double-clicks on an element  MouseEvent
    # onmousedown   The event occurs when the user presses a mouse button over an element   MouseEvent
    # onmouseenter  The event occurs when the pointer is moved onto an element  MouseEvent
    # onmouseleave  The event occurs when the pointer is moved out of an element    MouseEvent
    # onmousemove   The event occurs when the pointer is moving while it is over an element MouseEvent
    # onmouseover   The event occurs when the pointer is moved onto an element, or onto one of its children MouseEvent
    # onmouseout    The event occurs when a user moves the mouse pointer out of an element, or out of one of its children   MouseEvent
    # onmouseup The event occurs when a user releases a mouse button over an element    MouseEvent
    # pageX Returns the horizontal coordinate of the mouse pointer, relative to the document, when the mouse event was triggered    MouseEvent
    # pageY Returns the vertical coordinate of the mouse pointer, relative to the document, when the mouse event was triggered  MouseEvent
    # region        MouseEvent
    # relatedTarget Returns the element related to the element that triggered the mouse event   MouseEvent, FocusEvent
    # shiftKey  Returns whether the "SHIFT" key was pressed when an event was triggered MouseEvent, KeyboardEvent, TouchEvent
    # which Returns which mouse button was pressed when the mouse event was triggered   MouseEvent, KeyboardEvent


class KeyboardEvent(object):
    """ keyboard events """

    def __init__(self, *args, **kwargs):
        # self.args = args
        # self.kwargs = kwargs
        pass

    # @property
    # def location(self):

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
    # onkeydown The event occurs when the user is pressing a key    KeyboardEvent
    # onkeypress    The event occurs when the user presses a key    KeyboardEvent
    # onkeyup   The event occurs when the user releases a key   KeyboardEvent
    # repeat    Returns whether a key is being hold down repeatedly, or not KeyboardEvent


class UiEvent(object):
    """ UiEvent """
    def __init__(self, *args, **kwargs):
        self.detail = None
        self.view = None


class FocusEvent(object):
    """ FocusEvent """
    def __init__(self, *args, **kwargs):
        self.relatedTarget = None


class TouchEvent(object):
    """ TouchEvent """
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
        """    Returns whether the "SHIFT" key was pressed when the touch event was triggered """
        self.targetTouches = None
        """   Returns a list of all the touch objects that are in contact with the surface and where the touchstart event occured on the same target element as the current target element """
        self.touches = None
        """ Returns a list of all the touch objects that are currently in contact with the surface """


class WheelEvent(object):
    """ WheelEvent """
    def __init__(self, *args, **kwargs):
        self.deltaX = None
        """ Returns the horizontal scroll amount of a mouse wheel (x-axis) """
        self.deltaY = None
        """ Returns the vertical scroll amount of a mouse wheel (y-axis) """
        self.deltaZ = None
        """ Returns the scroll amount of a mouse wheel for the z-axis """
        self.deltaMode = None
        """ Returns a number that represents the unit of measurements for delta values (pixels, lines or pages) """


class AnimationEvent(object):
    """ AnimationEvent """
    def __init__(self, *args, **kwargs):
        self.animationName = None
        """ Returns the name of the animation """
        self.elapsedTime = None
        """ Returns the number of seconds an animation has been running """
        self.pseudoElement = None
        """ Returns the name of the pseudo-element of the animation """


class ClipboardEvent(object):
    """ ClipboardEvent """
    COPY = "oncopy"  # The event occurs when the user copies the content of an element
    CUT = "oncut"  # The event occurs when the user cuts the content of an element
    PASTE = "onpaste"  # The event occurs when the user pastes some content in an element

    def __init__(self, *args, **kwargs):
        self.clipboardData = None
        """ Returns an object containing the data affected by the clipboard operation """


class DragEvent(object):
    """ DragEvent """
    DRAG = "ondrag"  # The event occurs when an element is being dragged
    END = "ondragend"  # The event occurs when the user has finished dragging an element
    ENTER = "ondragenter"  # The event occurs when the dragged element enters the drop target
    LEAVE = "ondragleave"  # The event occurs when the dragged element leaves the drop target
    OVER = "ondragover"  # The event occurs when the dragged element is over the drop target
    START = "ondragstart"  # The event occurs when the user starts to drag an element
    DROP = "ondrop"  # The event occurs when the dragged element is dropped on the drop target

    def __init__(self, *args, **kwargs):
        self.dataTransfer = None
        """ Returns the data that is dragged/dropped """


class HashChangeEvent(object):
    """ HashChangeEvent """
    CHANGE = "onhashchange"  # The event occurs when there has been changes to the anchor part of a URL

    def __init__(self, *args, **kwargs):
        self.newURL = None
        """ Returns the URL of the document, after the hash has been changed """
        self.oldURL
        """ Returns the URL of the document, before the hash was changed """


class InputEvent(object):
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


class PageTransitionEvent(object):
    """ PageTransitionEvent """
    def __init__(self, *args, **kwargs):
        self.persisted = None
        """ Returns whether the webpage was cached by the browser """


class PopStateEvent(object):
    """ PopStateEvent """
    def __init__(self, *args, **kwargs):
        self.state = None
        """ Returns an object containing a copy of the history entries """


class StorageEvent(object):
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


class TransitionEvent(object):
    """ TransitionEvent """
    def __init__(self, *args, **kwargs):
        self.propertyName = None
        """ Returns the name of the transition"""
        self.elapsedTime = None
        """  Returns the number of seconds a transition has been running """
        self.pseudoElement = None
        """ Returns the name of the pseudo-element of the transition """


class CustomEvent(object):
    """ CustomEvent """
    def __init__(self, *args, **kwargs):
        self.detail = None

    def initCustomEvent():
        pass


# bubbles   Returns whether or not a specific event is a bubbling event Event
# cancelable    Returns whether or not an event can have its default action prevented   Event
# composed  Returns whether the event is composed or not    Event
# currentTarget Returns the element whose event listeners triggered the event   Event
# defaultPrevented  Returns whether or not the preventDefault() method was called for the event Event
# eventPhase    Returns which phase of the event flow is currently being evaluated  Event
# isTrusted Returns whether or not an event is trusted  Event
# onabort   The event occurs when the loading of a media is aborted UiEvent, Event
# onafterprint  The event occurs when a page has started printing, or if the print dialogue box has been closed Event
# onanimationend    The event occurs when a CSS animation has completed AnimationEvent
# onanimationiteration  The event occurs when a CSS animation is repeated   AnimationEvent
# onanimationstart  The event occurs when a CSS animation has started   AnimationEvent
# onbeforeprint The event occurs when a page is about to be printed Event
# onbeforeunload    The event occurs before the document is about to be unloaded    UiEvent, Event
# onblur    The event occurs when an element loses focus    FocusEvent
# oncanplay The event occurs when the browser can start playing the media (when it has buffered enough to begin)    Event
# oncanplaythrough  The event occurs when the browser can play through the media without stopping for buffering Event
# onchange  The event occurs when the content of a form element, the selection, or the checked state have changed (for <input>, <select>, and <textarea>)   Event
# ondurationchange  The event occurs when the duration of the media is changed  Event
# onemptied The event occurs when something bad happens and the media file is suddenly unavailable (like unexpectedly disconnects)
# onended   The event occurs when the media has reach the end (useful for messages like "thanks for listening") Event
# onerror   The event occurs when an error occurs while loading an external file    ProgressEvent, UiEvent, Event
# onfocus   The event occurs when an element gets focus FocusEvent
# onfocusin The event occurs when an element is about to get focus  FocusEvent
# onfocusout    The event occurs when an element is about to lose focus FocusEvent
# onfullscreenchange    The event occurs when an element is displayed in fullscreen mode    Event
# onfullscreenerror The event occurs when an element can not be displayed in fullscreen mode    Event
# oninput   The event occurs when an element gets user input    InputEvent, Event
# oninvalid The event occurs when an element is invalid Event
# onload    The event occurs when an object has loaded  UiEvent, Event
# onloadeddata  The event occurs when media data is loaded  Event
# onloadedmetadata  The event occurs when meta data (like dimensions and duration) are loaded   Event
# onloadstart   The event occurs when the browser starts looking for the specified media    ProgressEvent
# onmessage The event occurs when a message is received through the event source    Event
# onmousewheel  Deprecated. Use the wheel event instead WheelEvent
# onoffline The event occurs when the browser starts to work offline    Event
# ononline  The event occurs when the browser starts to work online Event
# onopen    The event occurs when a connection with the event source is opened  Event
# onpagehide    The event occurs when the user navigates away from a webpage    PageTransitionEvent
# onpageshow    The event occurs when the user navigates to a webpage   PageTransitionEvent
# onpause   The event occurs when the media is paused either by the user or programmatically    Event
# onplay    The event occurs when the media has been started or is no longer paused Event
# onplaying The event occurs when the media is playing after having been paused or stopped for buffering    Event
# onprogress    The event occurs when the browser is in the process of getting the media data (downloading the media)   Event
# onratechange  The event occurs when the playing speed of the media is changed Event
# onresize  The event occurs when the document view is resized  UiEvent, Event
# onreset   The event occurs when a form is reset   Event
# onscroll  The event occurs when an element's scrollbar is being scrolled  UiEvent, Event
# onsearch  The event occurs when the user writes something in a search field (for <input="search">)    Event
# onseeked  The event occurs when the user is finished moving/skipping to a new position in the media   Event
# onseeking The event occurs when the user starts moving/skipping to a new position in the media    Event
# onselect  The event occurs after the user selects some text (for <input> and <textarea>)  UiEvent, Event
# onshow    The event occurs when a <menu> element is shown as a context menu   Event
# onstalled The event occurs when the browser is trying to get media data, but data is not available    Event
# onsubmit  The event occurs when a form is submitted   Event
# onsuspend The event occurs when the browser is intentionally not getting media data   Event
# ontoggle  The event occurs when the user opens or closes the <details> element    Event
# ontouchcancel The event occurs when the touch is interrupted  TouchEvent
# ontouchend    The event occurs when a finger is removed from a touch screen   TouchEvent
# ontouchmove   The event occurs when a finger is dragged across the screen TouchEvent
# ontouchstart  The event occurs when a finger is placed on a touch screen  TouchEvent
# ontransitionend   The event occurs when a CSS transition has completed    TransitionEvent
# onunload  The event occurs once a page has unloaded (for <body>)  UiEvent, Event
# onvolumechange    The event occurs when the volume of the media has changed (includes setting the volume to "mute")   Event
# onwaiting The event occurs when the media has paused but is expected to resume (like when the media pauses to buffer more data)   Event
# onwheel   The event occurs when the mouse wheel rolls up or down over an element  WheelEvent
# preventDefault()  Cancels the event if it is cancelable, meaning that the default action that belongs to the event will not occur Event
# targetTouches Returns a list of all the touch objects that are in contact with the surface and where the touchstart event occured on the same target element as the current target element    TouchEvent
# timeStamp Returns the time (in milliseconds relative to the epoch) at which the event was created Event
# transitionend The event occurs when a CSS transition has completed    TransitionEvent