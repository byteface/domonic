"""
    domonic.dQuery
    ===================================
    alt + 0

"""

from domonic.dom import *
from domonic.html import *
from domonic.javascript import *


class EventHandler():

    def __init__(self):
        self.events = []

    def bindEvent(event, callback, targetElement):
        self.unbindEvent(event, targetElement)
        targetElement.addEventListener(event, callback, False)
        self.events.append({_type: event, event: callback, target: targetElement})

    def findEvent(event):
        return [e for e in self.events[0] if e == evt['_type']]

    def unbindEvent(event, targetElement):
        foundEvent = self.findEvent(event)
        if foundEvent is not None:
            targetElement.removeEventListener(event, foundEvent['event'], False)
        self.events = [e for e in self.events if e != evt['_type']]


class dQuery_el():
    """ 
    alt + 0

    dQuery - methods for querying domonic
    
    """

    @staticmethod
    def ajax(url='/', type='GET', data=None, 
        contentType=False, processData=False, cache=False, success=None, error=None):
        """ Perform an asynchronous HTTP request. """
        raise NotImplementedError

    @staticmethod
    def ajaxPrefilter():
        """ Handle custom Ajax options or modify existing options before each request is sent and before they are processed by .ajax """
        raise NotImplementedError


    @staticmethod
    def ajaxSetup():
        """ Set default values for future Ajax requests. Its use is not recommended. """
        raise NotImplementedError


    @staticmethod
    def ajaxTransport():
        """ Creates an object that handles the actual transmission of Ajax data. """
        raise NotImplementedError


    # @staticmethod
    # @ty
    # def boxModel:
    #     """ States if the current page, in the user’s browser, is being rendered using the W3C CSS Box Model. """
    #     raise NotImplementedError


    # @staticmethod
    # @ty
    # def browser:
        """ Contains flags for the useragent, read from navigator.userAgent. """
        # raise NotImplementedError


    @staticmethod
    def Callbacks():
        """ A multi-purpose callbacks list object that provides a powerful way to manage callback lists. """
        raise NotImplementedError


    @staticmethod
    def contains(parent, child):
        """ Check to see if a DOM element is a descendant of another DOM element. """
        return parent.contains(child)


    # @staticmethod
    # @ty
    # def cssHooks:
        """ Hook directly into dQuery to override how particular CSS properties are retrieved or set, normalize CSS property naming, or create custom properties. """
        # raise NotImplementedError


    # @staticmethod
    # @ty
    # def cssNumber:
        """ An object containing all CSS properties that may be used without a unit. The .css method uses this object to see if it may append px to unitless values. """
        # raise NotImplementedError


    @staticmethod
    def data():
        """ Store arbitrary data associated with the specified element and/or return the value that was set. """
        raise NotImplementedError


    @staticmethod
    def Deferred():
        """ A factory function that returns a chainable utility object with methods to register multiple callbacks into callback queues, invoke callback queues, and relay the success or failure state of any synchronous or asynchronous function. """
        raise NotImplementedError


    @staticmethod
    def dequeue():
        """ Execute the next function on the queue for the matched element. """
        raise NotImplementedError


    @staticmethod
    def each():
        """ A generic iterator function, which can be used to seamlessly iterate over both objects and arrays. """
        raise NotImplementedError


    @staticmethod
    def error():
        """ Takes a string and throws an exception containing it. """
        raise NotImplementedError

    @staticmethod
    def escapeSelector():
        """ Escapes any character that has a special meaning in a CSS selector. """
        raise NotImplementedError

    @staticmethod
    def extend(*args):
        """ Merge the contents of two or more objects together into the first object. """
        result = {}
        for each in args:
            result.update(each)
        return result

    @staticmethod
    def get(url: str):
        """ Load data from the server using a HTTP GET request. """
        r = requests.get(url)
        return r.content.decode("utf-8")

    @staticmethod
    def getJSON():
        """ Load JSON-encoded data from the server using a GET HTTP request. """
        raise NotImplementedError

    @staticmethod
    def getScript():
        """ Load a JavaScript file from the server using a GET HTTP request, then execute it. """
        raise NotImplementedError


    @staticmethod
    def globalEval():
        """ Execute some JavaScript code globally. """
        raise NotImplementedError


    @staticmethod
    def grep():
        """ Finds the elements of an array which satisfy a filter function. The original array is not affected. """
        raise NotImplementedError


    @staticmethod
    def hasData():
        """ Determine whether an element has any dQuery data associated with it. """
        raise NotImplementedError


    @staticmethod
    def holdReady():
        """ Holds or releases the execution of dQuery’s ready event. """
        raise NotImplementedError


    @staticmethod
    def htmlPrefilter():
        """ Modify and filter HTML strings passed through dQuery manipulation methods. """
        raise NotImplementedError


    @staticmethod
    def inArray(thing, arr):
        """ Search for a specified value within an array and return its index or -1 if not found. """
        for count, each in enumerate(arr):
            if thing == each:
                return count
        return -1


    @staticmethod
    def isArray():
        """ Determine whether the argument is an array. """
        raise NotImplementedError

    @staticmethod
    def isEmptyObject():
        """ Check to see if an object is empty (contains no enumerable properties). """
        raise NotImplementedError

    @staticmethod
    def isFunction(obj):
        """ Determines if its argument is callable as a function. """
        return callable(obj)

    @staticmethod
    def isNumeric():
        """ Determines whether its argument represents a JavaScript number. """
        raise NotImplementedError


    @staticmethod
    def isPlainObject():
        """ Check to see if an object is a plain object created using “{}” or “new Object”. """
        raise NotImplementedError


    @staticmethod
    def isWindow():
        """ Determine whether the argument is a window. """
        raise NotImplementedError


    @staticmethod
    def isXMLDoc():
        """ Check to see if a DOM node is within an XML document (or is an XML document). """
        raise NotImplementedError

    @staticmethod
    def makeArray(somelist):
        """ Convert an array-like object into a true JavaScript array. """
        return Array(somelist)

    @staticmethod
    def map():
        """ Translate all items in an array or object to new array of items. """
        raise NotImplementedError

    @staticmethod
    def merge(one, *args):
        """ Merge the contents of arrays into the first array. """
        import itertools
        one.append(list(itertools.chain(*args)))
        return one

    @staticmethod
    def noConflict():
        """ Relinquish dQuery’s control of the º variable. """
        raise NotImplementedError

    @staticmethod
    def noop():
        """ An empty function. """
        raise NotImplementedError


    @staticmethod
    def now():
        """ Return a number representing the current time. """
        return Date.now()

    @staticmethod
    def param():
        """ Create a serialized representation of an array, a plain object, or a dQuery object suitable for use in a URL query string or Ajax request. In case a dQuery object is passed, it should contain input elements with name/value properties. """
        raise NotImplementedError

    @staticmethod
    def parseHTML():
        """ Parses a string into an array of DOM nodes. """
        raise NotImplementedError

    @staticmethod
    def parseJSON():
        """ Takes a well-formed JSON string and returns the resulting JavaScript value. """
        raise NotImplementedError

    @staticmethod
    def parseXML():
        """ Parses a string into an XML document. """
        raise NotImplementedError


    @staticmethod
    def post():
        """ Send data to the server using a HTTP POST request. """
        raise NotImplementedError


    @staticmethod
    def proxy():
        """ Takes a function and returns a new one that will always have a particular context. """
        raise NotImplementedError


    @staticmethod
    def queue():
        """ Show or manipulate the queue of functions to be executed on the matched element. """
        raise NotImplementedError


    # @staticmethod
    # @ty
    # def ready:
        # """ A Promise-like object or “thenable” that resolves when the document is ready. """
        # raise NotImplementedError


    @staticmethod
    def readyException():
        """ Handles errors thrown synchronously in functions wrapped in dQuery """
        raise NotImplementedError


    @staticmethod
    def removeData():
        """ Remove a previously-stored piece of data. """
        raise NotImplementedError


    # @staticmethod
    #  @ty
    # def speed:
        # """ Creates an object containing a set of properties ready to be used in the definition of custom animations. """
        # raise NotImplementedError


    @staticmethod
    def sub():
        """ Creates a new copy of dQuery whose properties and methods can be modified without affecting the original dQuery object. """
        raise NotImplementedError


    # @staticmethod
    # def t:
    #     """ A collection of properties that represent the presence of different browser features or bugs. """
    #     raise NotImplementedError

    @staticmethod
    def trim(content):
        """ Remove the whitespace from the beginning and end of a string. """
        content = content.replace('\n', '').replace('\t', '').replace('\r', '').strip()
        return content

    # @staticmethod
    # def type():
    #     """ Determine the internal JavaScript [[Class]] of an object. """
    #     raise NotImplementedError


    @staticmethod
    def unique():
        """ Sorts an array of DOM elements, in place, with the duplicates removed. Note that this only works on arrays of DOM elements, not strings or numbers. """
        raise NotImplementedError


    @staticmethod
    def uniqueSort():
        """ Sorts an array of DOM elements, in place, with the duplicates removed. Note that this only works on arrays of DOM elements, not strings or numbers. """
        raise NotImplementedError


    @staticmethod
    def when():
        """ Provides a way to execute callback functions based on zero or more Thenable objects, usually Deferred objects that represent asynchronous events. """
        raise NotImplementedError

    DOM = None

    def __init__(self, dom, *args, **kwargs):
        """ Return a collection of matched elements either found in the DOM based on passed arguments or created by passing an HTML string. """

        # if first char is < . returs a new html dom node < init() does this
        # if its a selector. execs on the current dom < init() does this
        # if its a dom . set that as default target

        self.q = None
        self.elements = None
        if type(dom) == str:
            # print("DO NOT CALL THIS METHOD DIRECTLY! use dQuery or º ")
            return
        else:
            dQuery_el.DOM = dom
            self.dom = dom

    def __str__(self):
        # print(type(self.elements))
        if type(self.elements) is tuple:
        # if isinstance(self.elements, (list, tuple)):
            # print([str(el) for el in self.elements])
            return ''.join([str(el) for el in self.elements])
        else:
            # print('asd')
            return str(self.elements)

    def __getitem__(self, index):
        return self.elements[index]

    @property
    def dom(self):
        # print('getting')
        if dQuery_el.DOM is None:
            return
        # else:
        # print('GOT ONE')
        return dQuery_el.DOM

    @dom.setter
    def dom(self, dom):
        if isinstance(dom, html) or isinstance(dom, Document):
            dQuery_el.DOM = dom

    def init(self, q=''):
        self.q = q
        if type(q) is not str:
            return
        # if q == "":
            # return

        if self.q[0] == '<':
            self.elements = domonic.domonic.load(self.q)
            # print(type(self.elements))
            if isinstance(self.elements, html) or isinstance(self.elements, Document):
                self.dom = self.elements
        else:
            try:
                # element by selector not working on just classes as always needs a tag
                if self.q[0] == '.':

                    # NOTE - if jquery is not present in a webpage chrome assigns $ to querySelector NOT querySelectorAll
                    # so differing behaviours may be expected.
                    # detect if there's a list in each method if not just do it to first item? so it does bit of both? aka .append

                    self.elements = self.dom.querySelectorAll(self.q)
                    return

                self.elements = self.dom.getElementsBySelector(self.q, self.dom)
            except Exception as e:
                print('Error. No DOM has been set!!', e)
                raise e

    def add(self, elements):
        """ Create a new dQuery object with elements added to the set of matched elements."""
        '''
        dq = None
        if type(elements) == str:
            dq = º(elements).elements
        
        if type(dq) not in [list, tuple]:
            dq = [dq]

        if type(self.elements) not in [list, tuple]:
            self.elements = [self.elements]

        # if type(dq) not in [list, tuple]:
            # self.elements = [self.elements]

        self.elements = list(self.elements) + list(dq)
        return self
        '''
        # return self
        raise NotImplementedError

    def addBack(self):
        """ Add the previous set of elements on the stack to the current set, optionally filtered by a selector."""
        raise NotImplementedError

    def addClass(self, name):
        """ Adds the specified class to each element in the set of matched elements."""
        # print(self.elements, name)
        # print(type(self.elements))
        if not isinstance(self.elements, (list, tuple)):
            self.elements = (self.elements,)
        # print(type(self.elements))

        for el in self.elements:
            if el.getAttribute("class") is not None:
                el.setAttribute('class', el.getAttribute("class") + " " + name)
            else:
                el.setAttribute('class', name)
        return self

    def after(self):
        """ Insert content, specified by the parameter, after each element in the set of matched elements."""
        raise NotImplementedError

    def ajaxComplete(self):
        """ Register a handler to be called when Ajax requests complete. This is an AjaxEvent."""
        raise NotImplementedError

    def ajaxError(self):
        """ Register a handler to be called when Ajax requests complete with an error. This is an Ajax Event."""
        raise NotImplementedError

    def ajaxSend(self):
        """ Attach a function to be executed before an Ajax request is sent. This is an Ajax Event."""
        raise NotImplementedError

    def ajaxStart(self):
        """ Register a handler to be called when the first Ajax request begins. This is an Ajax Event."""
        raise NotImplementedError

    def ajaxStop(self):
        """ Register a handler to be called when all Ajax requests have completed. This is an Ajax Event."""
        raise NotImplementedError

    def ajaxSuccess(self):
        """ Attach a function to be executed whenever an Ajax request completes successfully. This is an Ajax Event."""
        raise NotImplementedError

    def andSelf(self):
        """ Add the previous set of elements on the stack to the current set."""
        raise NotImplementedError

    def animate(self):
        """ Perform a custom animation of a set of CSS properties."""
        raise NotImplementedError

    def append(self, html):
        """ Insert content, specified by the parameter, to the end of each element in the set of matched elements."""

        # print('running append')
        # print(len(self.elements))
        # print(":::::::::::", type(self.elements))

        if type(self.elements) is not tuple and type(self.elements) is not list:
            self.elements.innerHTML = self.elements.innerHTML + str(html)
            return self

        for el in self.elements:
            # print('EL!!')
            el.innerHTML = el.innerHTML + str(html)

        # print('APPEND SAYS:', self.elements)
        # return self

    def appendTo(self, target):
        """ Insert every element in the set of matched elements to the end of the target."""
        target += self.elements
        return target

    def attr(self, property, value=None):
        """ Get the value of an attribute for the first element in the set of matched elements or set one or more attributes for every matched element."""

        # if not isinstance(self.elements, (list, tuple)):
            # self.elements = (self.elements,)

        if value is not None:
            if self.elements[0].getAttribute(property) is not None:
                self.elements[0].setAttribute(property, value)
                return self
        if type(self.elements) is not tuple and type(self.elements) is not list:
            return self.elements.getAttribute(property)
        else:
            return self.elements[0].getAttribute(property)

    def before(self):
        """ Insert content, specified by the parameter, before each element in the set of matched elements."""
        raise NotImplementedError

    def bind(self):
        """ Attach a handler to an event for the elements."""
        raise NotImplementedError

    def blur(self):
        """ Bind an event handler to the “blur” JavaScript event, or trigger that event on an element."""
        raise NotImplementedError

    def change(self):
        """ Bind an event handler to the “change” JavaScript event, or trigger that event on an element."""
        raise NotImplementedError

    def children(self):
        """ Get the children of each element in the set of matched elements, optionally filtered by a selector."""
        raise NotImplementedError

    def clearQueue(self):
        """ Remove from the queue all items that have not yet been run."""
        raise NotImplementedError

    def click(self):
        """ Bind an event handler to the “click” JavaScript event, or trigger that event on an element."""
        raise NotImplementedError

    def clone(self):
        """ Create a deep copy of the set of matched elements."""
        raise NotImplementedError

    def closest(self):
        """ For each element in the set, get the first element that matches the selector by testing the element itself and traversing up through its ancestors in the DOM tree."""
        raise NotImplementedError

    def contents(self):
        """ Get the children of each element in the set of matched elements, including text and comment nodes."""
        raise NotImplementedError

    @property
    def context(self):
        """ The DOM node context originally passed to dQuery if none was passed then context will likely be the document. """
        raise NotImplementedError

    def contextmenu(self):
        """ Bind an event handler to the “contextmenu” JavaScript event, or trigger that event on an element."""
        raise NotImplementedError

    def css(self, prop, value):
        """ Get the value of a computed style property for the first element in the set of matched elements or set one or more CSS properties for every matched element."""
        pass

    def data(self):
        """ Store arbitrary data associated with the matched elements or return the value at the named data store for the first element in the set of matched elements."""
        raise NotImplementedError

    def dblclick(self):
        """ Bind an event handler to the “dblclick” JavaScript event, or trigger that event on an element."""
        raise NotImplementedError

    def delay(self):
        """ Set a timer to delay execution of subsequent items in the queue."""
        raise NotImplementedError

    def delegate(self):
        """ Attach a handler to one or more events for all elements that match the selector, now or in the future, based on a specific set of root elements."""
        raise NotImplementedError

    def dequeue(self):
        """ Execute the next function on the queue for the matched elements."""
        raise NotImplementedError

    def detach(self):
        """ Remove the set of matched elements from the DOM."""
        raise NotImplementedError

    def die(self):
        """ Remove event handlers previously attached using .live from the elements."""
        raise NotImplementedError

    def each(self):
        """ Iterate over a dQuery object, executing a function for each matched element."""
        raise NotImplementedError

    def empty(self):
        """ Remove all child nodes of the set of matched elements from the DOM."""
        raise NotImplementedError

    def end(self):
        """ End the most recent filtering operation in the current chain and return the set of matched elements to its previous state."""
        raise NotImplementedError

    def eq(self, index):
        """ Reduce the set of matched elements to the one at the specified index."""
        return self.elements[index]

    def error(self):
        """ Bind an event handler to the “error” JavaScript event."""
        raise NotImplementedError

    def even(self):
        """ Reduce the set of matched elements to the even ones in the set, numbered from zero."""
        raise NotImplementedError

    def fadeIn(self):
        """ Display the matched elements by fading them to opaque."""
        raise NotImplementedError

    def fadeOut(self):
        """ Hide the matched elements by fading them to transparent."""
        raise NotImplementedError

    def fadeTo(self):
        """ Adjust the opacity of the matched elements."""
        raise NotImplementedError

    def fadeToggle(self):
        """ Display or hide the matched elements by animating their opacity."""
        raise NotImplementedError

    def filter(self):
        """ Reduce the set of matched elements to those that match the selector or pass the function’s test."""
        raise NotImplementedError

    def find(self):
        """ Get the descendants of each element in the current set of matched elements, filtered by a selector, dQuery object, or element."""
        raise NotImplementedError

    def finish(self):
        """ Stop the currently-running animation, remove all queued animations, and complete all animations for the matched elements."""
        raise NotImplementedError

    def first(self):
        """ Reduce the set of matched elements to the first in the set."""
        if isinstance(self.elements, (list, tuple)):
            self.elements = self.elements[0]
        return self

    def focus(self):
        """ Bind an event handler to the “focus” JavaScript event, or trigger that event on an element."""
        raise NotImplementedError

    def focusin(self):
        """ Bind an event handler to the “focusin” event."""
        raise NotImplementedError

    def focusout(self):
        """ Bind an event handler to the “focusout” JavaScript event."""
        raise NotImplementedError

    def get(self):
        """ Retrieve the DOM elements matched by the dQuery object."""
        raise NotImplementedError

    def has(self):
        """ Reduce the set of matched elements to those that have a descendant that matches the selector or DOM element."""
        raise NotImplementedError

    def hasClass(self, classname):
        """ Determine whether any of the matched elements are assigned the given class."""
        if not isinstance(self.elements, (list, tuple)):
            self.elements = (self.elements,)

        for el in self.elements:
            if el.getAttribute("class") is not None:
                if classname in el.getAttribute("class"):
                    return True
        return False

    def height(self):
        """ Get the current computed height for the first element in the set of matched elements or set the height of every matched element."""
        raise NotImplementedError

    def hide(self):
        """ Hide the matched elements."""
        for el in self.elements:
              el.style.display = 'none'
        return self

    def hover(self):
        """ Bind one or two handlers to the matched elements, to be executed when the mouse pointer enters and leaves the elements."""
        raise NotImplementedError

    def html(self, html=None):
        """ Get the HTML contents of the first element in the set of matched elements or set the HTML contents of every matched element."""
        if html == None:
            return self.elements[0].innerHTML
        for el in self.elements:
            el.innerHTML = html
        return self

    def index(self):
        """ Search for a given element from among the matched elements."""
        raise NotImplementedError

    def innerHeight(self):
        """ Get the current computed inner height (including padding but not border) for the first element in the set of matched elements or set the inner height of every matched element."""
        raise NotImplementedError

    def innerWidth(self):
        """ Get the current computed inner width (including padding but not border) for the first element in the set of matched elements or set the inner width of every matched element."""
        raise NotImplementedError

    def insertAfter(self):
        """ Insert every element in the set of matched elements after the target."""
        raise NotImplementedError

    def insertBefore(self):
        """ Insert every element in the set of matched elements before the target."""
        raise NotImplementedError

    # def is(self):
        """ Check the current matched set of elements against a selector, element, or dQuery object and return true if at least one of these elements matches the given arguments."""
        # raise NotImplementedError

    def keydown(self):
        """ Bind an event handler to the “keydown” JavaScript event, or trigger that event on an element."""
        raise NotImplementedError

    def keypress(self):
        """ Bind an event handler to the “keypress” JavaScript event, or trigger that event on an element."""
        raise NotImplementedError

    def keyup(self):
        """ Bind an event handler to the “keyup” JavaScript event, or trigger that event on an element."""
        raise NotImplementedError

    def last(self):
        """ Reduce the set of matched elements to the final one in the set."""
        if isinstance(self.elements, list) or isinstance(self.elements, tuple):
            self.elements = self.elements[len(self.elements)-1]
        return self

    @property
    def length(self):
        """ The number of elements in the dQuery object. """
        return len(self.elements)

    def live(self):
        """ Attach an event handler for all elements which match the current selector, now and in the future."""
        raise NotImplementedError

    def load(self):
        """ Load data from the server and place the returned HTML into the matched elements."""
        raise NotImplementedError

    def map(self):
        """ Pass each element in the current matched set through a function, producing a new dQuery object containing the return values."""
        raise NotImplementedError

    def mousedown(self):
        """ Bind an event handler to the “mousedown” JavaScript event, or trigger that event on an element."""
        raise NotImplementedError

    def mouseenter(self):
        """ Bind an event handler to be fired when the mouse enters an element, or trigger that handler on an element."""
        raise NotImplementedError

    def mouseleave(self):
        """ Bind an event handler to be fired when the mouse leaves an element, or trigger that handler on an element."""
        raise NotImplementedError

    def mousemove(self):
        """ Bind an event handler to the “mousemove” JavaScript event, or trigger that event on an element."""
        raise NotImplementedError

    def mouseout(self):
        """ Bind an event handler to the “mouseout” JavaScript event, or trigger that event on an element."""
        raise NotImplementedError

    def mouseover(self):
        """ Bind an event handler to the “mouseover” JavaScript event, or trigger that event on an element."""
        raise NotImplementedError

    def mouseup(self):
        """ Bind an event handler to the “mouseup” JavaScript event, or trigger that event on an element."""
        raise NotImplementedError

    def next(self):
        """ Get the immediately following sibling of each element in the set of matched elements. If a selector is provided, it retrieves the next sibling only if it matches that selector."""
        raise NotImplementedError

    def nextAll(self):
        """ Get all following siblings of each element in the set of matched elements, optionally filtered by a selector."""
        raise NotImplementedError

    def nextUntil(self):
        """ Get all following siblings of each element up to but not including the element matched by the selector, DOM node, or dQuery object passed."""
        raise NotImplementedError

    # def not(self):
        """ Remove elements from the set of matched elements."""
        # raise NotImplementedError

    def odd(self):
        """ Reduce the set of matched elements to the odd ones in the set, numbered from zero."""
        raise NotImplementedError

    def off(self, event):
        """ Remove an event handler."""
        for el in self.elements:
            self.eventHandler.unbindEvent(event, el)

    def offset(self):
        """ Get the current coordinates of the first element, or set the coordinates of every element, in the set of matched elements, relative to the document."""
        raise NotImplementedError

    def offsetParent(self):
        """ Get the closest ancestor element that is positioned."""
        raise NotImplementedError

    def on(self, event, callback):
        """ Attach an event handler function for one or more events to the selected elements."""
        for el in self.elements:
            self.eventHandler.bindEvent(event, callback, el)
        return self

    def one(self):
        """ Attach a handler to an event for the elements. The handler is executed at most once per element per event type."""
        raise NotImplementedError

    def outerHeight(self):
        """ Get the current computed outer height (including padding, border, and optionally margin) for the first element in the set of matched elements or set the outer height of every matched element."""
        raise NotImplementedError

    def outerWidth(self):
        """ Get the current computed outer width (including padding, border, and optionally margin) for the first element in the set of matched elements or set the outer width of every matched element."""
        raise NotImplementedError

    def parent(self):
        """ Get the parent of each element in the current set of matched elements, optionally filtered by a selector."""
        raise NotImplementedError

    def parents(self):
        """ Get the ancestors of each element in the current set of matched elements, optionally filtered by a selector."""
        raise NotImplementedError

    def parentsUntil(self):
        """ Get the ancestors of each element in the current set of matched elements, up to but not including the element matched by the selector, DOM node, or dQuery object."""
        raise NotImplementedError

    def position(self):
        """ Get the current coordinates of the first element in the set of matched elements, relative to the offset parent."""
        raise NotImplementedError

    def prepend(self, html):
        """ Insert content, specified by the parameter, to the beginning of each element in the set of matched elements."""
        for el in self.elements:
            el.innerHTML = html + el.innerHTML
        return self

    def prependTo(self, target):
        """ Insert every element in the set of matched elements to the beginning of the target."""
        raise NotImplementedError

    def prev(self):
        """ Get the immediately preceding sibling of each element in the set of matched elements. If a selector is provided, it retrieves the previous sibling only if it matches that selector."""
        raise NotImplementedError

    def prevAll(self):
        """ Get all preceding siblings of each element in the set of matched elements, optionally filtered by a selector."""
        raise NotImplementedError

    def prevUntil(self):
        """ Get all preceding siblings of each element up to but not including the element matched by the selector, DOM node, or dQuery object."""
        raise NotImplementedError

    def promise(self):
        """ Return a Promise object to observe when all actions of a certain type bound to the collection, queued or not, have finished."""
        raise NotImplementedError

    def prop(self, property, value):
        """ Get the value of a property for the first element in the set of matched elements or set one or more properties for every matched element."""
        if value is not None:
            if self.elements[0].getAttribute(property) is not None:
                self.elements[0].setAttribute(property, value)
                return self
        if type(self.elements) is not tuple and type(self.elements) is not list:
            return self.elements.getAttribute(property)
        else:
            return self.elements[0].getAttribute(property)

    def pushStack(self):
        """ Add a collection of DOM elements onto the dQuery stack."""
        raise NotImplementedError

    def queue(self):
        """ Show or manipulate the queue of functions to be executed on the matched elements."""
        raise NotImplementedError

    def ready(self):
        """ Specify a function to execute when the DOM is fully loaded."""
        raise NotImplementedError

    def remove(self):
        """ Remove the set of matched elements from the DOM."""
        raise NotImplementedError

    def removeAttr(self):
        """ Remove an attribute from each element in the set of matched elements."""
        raise NotImplementedError

    def removeClass(self, classname):
        """ Remove a single class, multiple classes, or all classes from each element in the set of matched elements."""

        if not isinstance(self.elements, (list, tuple)):
            self.elements = (self.elements,)

        for el in self.elements:
            if el.getAttribute("class") is not None:
                if classname in el.getAttribute("class"):
                    removed = ''.join(el.getAttribute("class").split(classname)).strip()
                    removed = removed.replace('  ',' ')
                    el.setAttribute("class", removed)
        return self

    def removeData(self):
        """ Remove a previously-stored piece of data."""
        raise NotImplementedError

    def removeProp(self):
        """ Remove a property for the set of matched elements."""
        raise NotImplementedError

    def replaceAll(self):
        """ Replace each target element with the set of matched elements."""
        raise NotImplementedError

    def replaceWith(self):
        """ Replace each element in the set of matched elements with the provided new content and return the set of elements that was removed."""
        raise NotImplementedError

    def resize(self):
        """ Bind an event handler to the “resize” JavaScript event, or trigger that event on an element."""
        raise NotImplementedError

    def scroll(self):
        """ Bind an event handler to the “scroll” JavaScript event, or trigger that event on an element."""
        raise NotImplementedError

    def scrollLeft(self):
        """ Get the current horizontal position of the scroll bar for the first element in the set of matched elements or set the horizontal position of the scroll bar for every matched element."""
        raise NotImplementedError

    def scrollTop(self):
        """ Get the current vertical position of the scroll bar for the first element in the set of matched elements or set the vertical position of the scroll bar for every matched element."""
        raise NotImplementedError

    def select(self):
        """ Bind an event handler to the “select” JavaScript event, or trigger that event on an element."""
        raise NotImplementedError

    def serialize(self):
        """ Encode a set of form elements as a string for submission."""
        # raise NotImplementedError
        # from domonic.javascript import Global

        if isinstance( self.elements, (tuple, list) ):
            form = self.elements[0]
        else:
            form = self.elements

        if form.nodeName != "FORM":
            return

        q = []
        for el in form.elements:

            if el.getAttribute('name') == "":
                continue
            
            if el.nodeName == 'INPUT':
                if el.type in ['email','text','hidden','password','button','reset','submit','email']:
                    q.append(el.getAttribute('name') + "=" + Global.encodeURIComponent(el.nodeValue))
                elif el.type in ['checkbox','radio']:
                    if el.checked:
                        q.append(el.getAttribute('name') + "=" + Global.encodeURIComponent(el.nodeValue))
            elif el.nodeName == 'TEXTAREA':
                q.append(el.getAttribute('name') + "=" + Global.encodeURIComponent(el.nodeValue))
            elif el.nodeName == 'SELECT':
                if el.getAttribute('multiple') != None:
                    for option in el.getElementsByTagName('option'):
                        if option.getAttribute('selected') != None:
                            q.append(el.getAttribute('name') + "=" + Global.encodeURIComponent(option.nodeValue))
                else:
                    q.append(el.getAttribute('name') + "=" + Global.encodeURIComponent(el.nodeValue))
            elif el.nodeName == 'BUTTON':
                if el.type in ['reset', 'submit', 'button']:
                    q.append(el.getAttribute('name') + "=" + Global.encodeURIComponent(el.nodeValue))

        return "&".join(q)

    def serializeArray(self):
        """ Encode a set of form elements as an array of names and values."""
        raise NotImplementedError

    def show(self):
        """ Display the matched elements."""
        for el in self.elements:
              el.style.display = ''
        return self

    def siblings(self):
        """ Get the siblings of each element in the set of matched elements, optionally filtered by a selector."""
        raise NotImplementedError

    def size(self):
        """ Return the number of elements in the dQuery object."""
        return len(self.elements)

    def slice(self):
        """ Reduce the set of matched elements to a subset specified by a range of indices."""
        raise NotImplementedError

    def slideDown(self):
        """ Display the matched elements with a sliding motion."""
        raise NotImplementedError

    def slideToggle(self):
        """ Display or hide the matched elements with a sliding motion."""
        raise NotImplementedError

    def slideUp(self):
        """ Hide the matched elements with a sliding motion."""
        raise NotImplementedError

    def stop(self):
        """ Stop the currently-running animation on the matched elements."""
        raise NotImplementedError

    def submit(self):
        """ Bind an event handler to the “submit” JavaScript event, or trigger that event on an element."""
        raise NotImplementedError

    def text(self, newVal=None):
        """ Get the combined text contents of each element in the set of matched elements, including their descendants, or set the text contents of the matched elements."""
        if newVal != None:
            for el in self.elements:
                el.textContent = newVal 
        else:
            return [el.textContent for el in self.elements]

    def toArray(self):
        """ Retrieve all the elements contained in the dQuery set, as an array."""
        # raise NotImplementedError
        if isinstance(self.elements, (list, tuple) ):
            return self.elements
        else:
            return [self.elements]

    def toggle(self):
        """ Display or hide the matched elements."""
        raise NotImplementedError

    # def toggle(self):
    #     """ Bind two or more handlers to the matched elements, to be executed on alternate clicks."""
    #     raise NotImplementedError

    def toggleClass(self):
        """ Add or remove one or more classes from each element in the set of matched elements, depending on either the class presence or the value of the state argument."""
        raise NotImplementedError

    def trigger(self):
        """ Execute all handlers and behaviors attached to the matched elements for the given event type."""
        raise NotImplementedError

    def triggerHandler(self):
        """ Execute all handlers attached to an element for an event."""
        raise NotImplementedError

    def unbind(self):
        """ Remove a previously-attached event handler from the elements."""
        raise NotImplementedError

    def undelegate(self):
        """ Remove a handler from the event for all elements which match the current selector, based upon a specific set of root elements."""
        raise NotImplementedError

    def unload(self):
        """ Bind an event handler to the “unload” JavaScript event."""
        raise NotImplementedError

    def unwrap(self):
        """ Remove the parents of the set of matched elements from the DOM, leaving the matched elements in their place."""
        raise NotImplementedError

    def val(self, newVal=None):
        """ Get the current value of the first element in the set of matched elements or set the value of every matched element."""
        if newVal != None:
            for el in elements:
                self.elements.value = newVal 
        else:
            return self.elements.value
        # return self

    def width(self):
        """ Get the current computed width for the first element in the set of matched elements or set the width of every matched element."""
        raise NotImplementedError

    def wrap(self):
        """ Wrap an HTML structure around each element in the set of matched elements."""
        raise NotImplementedError

    def wrapAll(self):
        """ Wrap an HTML structure around all elements in the set of matched elements."""
        raise NotImplementedError

    def wrapInner(self):
        """ Wrap an HTML struct"""
        raise NotImplementedError




# All Selector (“*”)
# Selects all elements.
# :animated Selector
# Select all elements that are in the progress of an animation at the time the selector is run.
# Attribute Contains Prefix Selector [name|=”value”]
# Selects elements that have the specified attribute with a value either equal to a given string or starting with that string followed by a hyphen (-).

# Attribute Contains Selector [name*=”value”]
# Selects elements that have the specified attribute with a value containing a given substring.

# Attribute Contains Word Selector [name~=”value”]
# Selects elements that have the specified attribute with a value containing a given word, delimited by spaces.

# Attribute Ends With Selector [name$=”value”]
# Selects elements that have the specified attribute with a value ending exactly with a given string. The comparison is case sensitive.

# Attribute Equals Selector [name=”value”]
# Selects elements that have the specified attribute with a value exactly equal to a certain value.

# Attribute Not Equal Selector [name!=”value”]
# Select elements that either don’t have the specified attribute, or do have the specified attribute but not with a certain value.

# Attribute Starts With Selector [name^=”value”]
# Selects elements that have the specified attribute with a value beginning exactly with a given string.

# :button Selector
# Selects all button elements and elements of type button.

# Callbacks Object
# callbacks.add()
# Add a callback or a collection of callbacks to a callback list.

# Callbacks Object
# callbacks.disable()
# Disable a callback list from doing anything more.

# Callbacks Object
# callbacks.disabled()
# Determine if the callbacks list has been disabled.

# Callbacks Object
# callbacks.empty()
# Remove all of the callbacks from a list.

# Callbacks Object
# callbacks.fire()
# Call all of the callbacks with the given arguments.

# Callbacks Object
# callbacks.fired()
# Determine if the callbacks have already been called at least once.

# Callbacks Object
# callbacks.fireWith()
# Call all callbacks in a list with the given context and arguments.

# Callbacks Object
# callbacks.has()
# Determine whether or not the list has any callbacks attached. If a callback is provided as an argument, determine whether it is in a list.

# Callbacks Object
# callbacks.lock()
# Lock a callback list in its current state.

# Callbacks Object
# callbacks.locked()
# Determine if the callbacks list has been locked.

# Callbacks Object
# callbacks.remove()
# Remove a callback or a collection of callbacks from a callback list.

# :checkbox Selector
# Selects all elements of type checkbox.

# Selectors > Form
# :checked Selector
# Matches all elements that are checked or selected.

# Selectors > Hierarchy
# Child Selector (“parent > child”)
# Selects all direct child elements specified by “child” of elements specified by “parent”.

# Selectors > Basic
# Class Selector (“.class”)
# Selects all elements with the given class.

# :contains() Selector
# Select all elements that contain the specified text.

# Selectors > Form | Selectors > dQuery Extensions
# :radio Selector
# Selects all elements of type radio.



# Deferred Object
# deferred.always()
# Add handlers to be called when the Deferred object is either resolved or rejected.

# Deferred Object
# deferred.catch()
# Add handlers to be called when the Deferred object is rejected.

# Deferred Object
# deferred.done()
# Add handlers to be called when the Deferred object is resolved.

# Deferred Object
# deferred.fail()
# Add handlers to be called when the Deferred object is rejected.

# Deferred Object | Deprecated > Deprecated 1.7 | Removed
# deferred.isRejected()
# Determine whether a Deferred object has been rejected.

# Deferred Object | Deprecated > Deprecated 1.7 | Removed
# deferred.isResolved()
# Determine whether a Deferred object has been resolved.

# Deferred Object
# deferred.notify()
# Call the progressCallbacks on a Deferred object with the given args.

# Deferred Object
# deferred.notifyWith()
# Call the progressCallbacks on a Deferred object with the given context and args.

# Deferred Object | Deprecated > Deprecated 1.8
# deferred.pipe()
# Utility method to filter and/or chain Deferreds.

# Deferred Object
# deferred.progress()
# Add handlers to be called when the Deferred object generates progress notifications.

# Deferred Object
# deferred.promise()
# Return a Deferred’s Promise object.

# Deferred Object
# deferred.reject()
# Reject a Deferred object and call any failCallbacks with the given args.

# Deferred Object
# deferred.rejectWith()
# Reject a Deferred object and call any failCallbacks with the given context and args.

# Deferred Object
# deferred.resolve()
# Resolve a Deferred object and call any doneCallbacks with the given args.

# Deferred Object
# deferred.resolveWith()
# Resolve a Deferred object and call any doneCallbacks with the given context and args.

# Deferred Object
# deferred.state()
# Determine the current state of a Deferred object.

# Deferred Object
# deferred.then()
# Add handlers to be called when the Deferred object is resolved, rejected, or still in progress.


# Selectors > Hierarchy
# Descendant Selector (“ancestor descendant”)
# Selects all elements that are descendants of a given ancestor.


# Selectors > Form
# :disabled Selector
# Selects all elements that are disabled.

# Selectors > dQuery Extensions | Selectors > Visibility Filter
# :visible Selector
# Selects all elements that are visible.

# .dquery
# A string containing the dQuery version number.

# Selectors > Basic
# Element Selector (“element”)
# Selects all elements with the given tag name.

# Selectors > Content Filter
# :empty Selector
# Select all elements that have no children (including text nodes).

# Selectors > Form
# :enabled Selector
# Selects all elements that are enabled.

# Selectors > Basic Filter | Deprecated > Deprecated 3.4 | Selectors > dQuery Extensions
# :eq() Selector
# Select the element at index n within the matched set.



# Selectors > Basic Filter | Deprecated > Deprecated 3.4 | Selectors > dQuery Extensions
# :even Selector
# Selects even elements, zero-indexed. See also :odd.

# Events > Event Object
# event.currentTarget
# The current DOM element within the event bubbling phase.

# Events > Event Object
# event.data
# An optional object of data passed to an event method when the current executing handler is bound.

# Events > Event Object | Events
# event.delegateTarget
# The element where the currently-called dQuery event handler was attached.

# Events > Event Object
# event.isDefaultPrevented()
# Returns whether event.preventDefault() was ever called on this event object.

# Events > Event Object
# event.isImmediatePropagationStopped()
# Returns whether event.stopImmediatePropagation() was ever called on this event object.

# Events > Event Object
# event.isPropagationStopped()
# Returns whether event.stopPropagation() was ever called on this event object.

# Events > Event Object
# event.metaKey
# Indicates whether the META key was pressed when the event fired.

# Events > Event Object
# event.namespace
# The namespace specified when the event was triggered.

# Events > Event Object
# event.pageX
# The mouse position relative to the left edge of the document.

# Events > Event Object
# event.pageY
# The mouse position relative to the top edge of the document.

# Events > Event Object
# event.preventDefault()
# If this method is called, the default action of the event will not be triggered.

# Events > Event Object
# event.relatedTarget
# The other DOM element involved in the event, if any.

# Events > Event Object
# event.result
# The last value returned by an event handler that was triggered by this event, unless the value was undefined.

# Events > Event Object
# event.stopImmediatePropagation()
# Keeps the rest of the handlers from being executed and prevents the event from bubbling up the DOM tree.

# Events > Event Object
# event.stopPropagation()
# Prevents the event from bubbling up the DOM tree, preventing any parent handlers from being notified of the event.

# Events > Event Object
# event.target
# The DOM element that initiated the event.

# Events > Event Object
# event.timeStamp
# The difference in milliseconds between the time the browser created the event and January 1, 1970.

# Events > Event Object
# event.type
# Describes the nature of the event.

# Events > Event Object
# event.which
# For key or mouse events, this property indicates the specific key or button that was pressed.

# Selectors > Child Filter
# :only-child Selector
# Selects all elements that are the only child of their parent.

# Selectors > Child Filter
# :only-of-type Selector
# Selects all elements that have no siblings with the same element name.


# Selectors > Form | Selectors > dQuery Extensions
# :reset Selector
# Selects all elements of type reset.

# Selectors > Basic Filter
# :root Selector
# Selects the element that is the root of the document.

# Selectors > Form | Selectors > dQuery Extensions
# :file Selector
# Selects all elements of type file.
# Selectors > Child Filter
# :first-child Selector
# Selects all elements that are the first child of their parent.
# Selectors > Child Filter
# :first-of-type Selector
# Selects all elements that are the first among siblings of the same element name.
# Selectors > Basic Filter | Deprecated > Deprecated 3.4 | Selectors > dQuery Extensions
# :first Selector
# Selects the first matched DOM element.

# Selectors > Content Filter | Selectors > dQuery Extensions
# :parent Selector
# Select all elements that have at least one child node (either an element or text).

# Selectors > Form | Selectors > dQuery Extensions
# :password Selector
# Selects all elements of type password.

# Selectors > Basic Filter | Selectors > Form
# :focus Selector
# Selects element if it is currently focused.


# Selectors > Basic Filter | Deprecated > Deprecated 3.4 | Selectors > dQuery Extensions
# :gt() Selector
# Select all elements at an index greater than index within the matched set.

# Selectors > Form | Selectors > dQuery Extensions
# :submit Selector
# Selects all elements of type submit.

# Selectors > Basic Filter
# :target Selector
# Selects the target element indicated by the fragment identifier of the document’s URI.

# Selectors > Form | Selectors > dQuery Extensions
# :text Selector
# Selects all input elements of type text.

# Selectors > Attribute
# Multiple Attribute Selector [name=”value”][name2=”value2″]
# Matches elements that match all of the specified attribute filters.

# Selectors > Basic
# Multiple Selector (“selector1, selector2, selectorN”)
# Selects the combined results of all the specified selectors.

# Selectors > Attribute
# Has Attribute Selector [name]
# Selects elements that have the specified attribute, with any value.

# Selectors > Content Filter | Selectors > dQuery Extensions
# :has() Selector
# Selects elements which contain at least one element that matches the specified selector.

# Selectors > Basic Filter | Selectors > dQuery Extensions
# :header Selector
# Selects all elements that are headers, like h1, h2, h3 and so on.

# Selectors > dQuery Extensions | Selectors > Visibility Filter
# :hidden Selector
# Selects all elements that are hidden.

# Selectors > Child Filter
# :last-child Selector
# Selects all elements that are the last child of their parent.

# Selectors > Child Filter
# :last-of-type Selector
# Selects all elements that are the last among siblings of the same element name.

# Selectors > Basic Filter | Deprecated > Deprecated 3.4 | Selectors > dQuery Extensions
# :last Selector
# Selects the last matched element.

# Selectors > Basic Filter | Deprecated > Deprecated 3.4 | Selectors > dQuery Extensions
# :lt() Selector
# Select all elements at an index less than index within the matched set.

# Selectors > Basic Filter
# :lang() Selector
# Selects all elements of the specified language.

# Selectors > Form | Selectors > dQuery Extensions
# :selected Selector
# Selects all elements that are selected.

# Deprecated > Deprecated 1.7 | Internals | Properties > Properties of dQuery Object Instances | Removed
# .selector
# A selector representing selector passed to dQuery(), if any, when creating the original set.

# Selectors > Basic Filter
# :not() Selector
# Selects all elements that do not match the given selector.

# Selectors > Child Filter
# :nth-child() Selector
# Selects all elements that are the nth-child of their parent.

# Selectors > Child Filter
# :nth-last-child() Selector
# Selects all elements that are the nth-child of their parent, counting from the last element to the first.

# Selectors > Child Filter
# :nth-last-of-type() Selector
# Selects all the elements that are the nth-child of their parent in relation to siblings with the same element name, counting from the last element to the first.

# Selectors > Child Filter
# :nth-of-type() Selector
# Selects all elements that are the nth child of their parent in relation to siblings with the same element name.

# Selectors > Basic Filter | Deprecated > Deprecated 3.4 | Selectors > dQuery Extensions
# :odd Selector
# Selects odd elements, zero-indexed. See also :even.


# Selectors > Basic
# ID Selector (“#id”)
# Selects a single element with the given id attribute.

# Selectors > Form | Selectors > dQuery Extensions
# :image Selector
# Selects all elements of type image.


# Selectors > Hierarchy
# Next Adjacent Selector (“prev + next”)
# Selects all next elements matching “next” that are immediately preceded by a sibling “prev”.

# Selectors > Hierarchy
# Next Siblings Selector (“prev ~ siblings”)
# Selects all sibling elements that follow after the “prev” element, have the same parent, and match the filtering “siblings” selector.

# Effects > Custom | Deprecated > Deprecated 3.0 | Properties > Properties of the Global dQuery Object
# dQuery.fx.interval
# The rate (in milliseconds) at which animations fire.

# Effects > Custom | Properties > Properties of the Global dQuery Object
# dQuery.fx.off
# Globally disable all animations.

# :input Selector
# Selects all input, textarea, select and button elements.


def º(q):
    el = dQuery_el(q)
    el.init(q)

    º.ajax = el.ajax
    # º.boxModel = el.boxModel
    # º.browser = el.browser
    # º.cssHooks = el.cssHooks
    # º.cssNumber = el.cssNumber
    # º.ready = el.ready
    # º.speed = el.speed
    # º.support = el.support

    º.ajaxPrefilter = el.ajaxPrefilter
    º.ajaxSetup = el.ajaxSetup
    º.ajaxTransport = el.ajaxTransport
    º.Callbacks = el.Callbacks
    º.contains = el.contains
    º.data = el.data
    º.Deferred = el.Deferred
    º.dequeue = el.dequeue
    º.each = el.each
    º.error = el.error
    º.escapeSelector = el.escapeSelector
    º.extend = el.extend
    º.get = el.get
    º.getJSON = el.getJSON
    º.getScript = el.getScript
    º.globalEval = el.globalEval
    º.grep = el.grep
    º.hasData = el.hasData
    º.holdReady = el.holdReady
    º.htmlPrefilter = el.htmlPrefilter
    º.inArray = el.inArray
    º.isArray = el.isArray
    º.isEmptyObject = el.isEmptyObject
    º.isFunction = el.isFunction
    º.isNumeric = el.isNumeric
    º.isPlainObject = el.isPlainObject
    º.isWindow = el.isWindow
    º.isXMLDoc = el.isXMLDoc
    º.makeArray = el.makeArray
    º.map = el.map
    º.merge = el.merge
    º.noConflict = el.noConflict
    º.noop = el.noop
    
    º.now = el.now

    º.param = el.param
    º.parseHTML = el.parseHTML
    º.parseJSON = el.parseJSON
    º.parseXML = el.parseXML
    º.post = el.post
    º.proxy = el.proxy
    º.queue = el.queue
    º.readyException = el.readyException
    º.removeData = el.removeData
    º.sub = el.sub
    º.trim = el.trim
    # º.type = el.type
    º.unique = el.unique
    º.uniqueSort = el.uniqueSort
    º.when = el.when

    # º().append = el.append(q)

    # if type(q) is not str:
    return el
    # else:
        # return el.elements
    # def __str__(self):
        # return self.elements

dQuery = º