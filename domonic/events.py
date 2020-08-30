"""
    domonic.events
    ~~~~~~~~~~~~~~
    dom events

"""

from typing import *


class Event(object):

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
        self.timeStamp = None
        

    def composedPath(self):
        pass

    def createEvent(self):
        pass

    def initEvent(self):
        pass

    def msConvertURL(self):
        pass

    def preventDefault(self):
        pass

    def stopImmediatePropagation(self):
        pass

    def stopPropagation(self):
        pass


class MouseEvent(Event):
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
# oncopy    The event occurs when the user copies the content of an element ClipboardEvent
# oncut The event occurs when the user cuts the content of an element   ClipboardEvent
# ondrag    The event occurs when an element is being dragged   DragEvent
# ondragend The event occurs when the user has finished dragging an element DragEvent
# ondragenter   The event occurs when the dragged element enters the drop target    DragEvent
# ondragleave   The event occurs when the dragged element leaves the drop target    DragEvent
# ondragover    The event occurs when the dragged element is over the drop target   DragEvent
# ondragstart   The event occurs when the user starts to drag an element    DragEvent
# ondrop    The event occurs when the dragged element is dropped on the drop target DragEvent
# ondurationchange  The event occurs when the duration of the media is changed  Event
# onemptied The event occurs when something bad happens and the media file is suddenly unavailable (like unexpectedly disconnects)
# onended   The event occurs when the media has reach the end (useful for messages like "thanks for listening") Event
# onerror   The event occurs when an error occurs while loading an external file    ProgressEvent, UiEvent, Event
# onfocus   The event occurs when an element gets focus FocusEvent
# onfocusin The event occurs when an element is about to get focus  FocusEvent
# onfocusout    The event occurs when an element is about to lose focus FocusEvent
# onfullscreenchange    The event occurs when an element is displayed in fullscreen mode    Event
# onfullscreenerror The event occurs when an element can not be displayed in fullscreen mode    Event
# onhashchange  The event occurs when there has been changes to the anchor part of a URL    HashChangeEvent
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
# onpaste   The event occurs when the user pastes some content in an element    ClipboardEvent
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