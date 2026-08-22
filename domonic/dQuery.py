"""
domonic.dQuery
===================================
alt + 0

"""

import copy
import functools
import json
import re

from domonic.dom import *
from domonic.html import *
from domonic.javascript import *


class EventHandler:
    def __init__(self):
        self.events = []

    def bindEvent(self, event: str, callback, targetElement):
        """[binds an event to a callback]

        Args:
            event ([str]): [type of event]
            callback (function): [callback function]
            targetElement ([type]): [target element]
        """
        self.unbindEvent(event, targetElement)
        targetElement.addEventListener(event, callback, False)
        self.events.append({"_type": event, "event": callback, "target": targetElement})

    def findEvent(self, event):
        """[finds an event]

        Args:
            event ([str]): [event]

        Returns:
            [type]: [event]
        """
        for registered in self.events:
            if registered["_type"] == event:
                return registered
        return None

    def unbindEvent(self, event, targetElement):
        """[unbinds an event]

        Args:
            event ([str]): [event]
            targetElement ([type]): [description]
        """
        remaining = []
        for registered in self.events:
            if registered["_type"] == event and registered["target"] == targetElement:
                targetElement.removeEventListener(event, registered["event"])
            else:
                remaining.append(registered)
        self.events = remaining


class dQuery_el:
    """
    alt + 0

    dQuery - methods for querying domonic

    """

    DOM = None

    def __init__(self, dom, *args, **kwargs):
        """Return a collection of matched elements found in the DOM based on passed arguments,
        or created by passing an HTML string."""

        # if first char is < . returs a new html dom node < init() does this
        # if its a selector. execs on the current dom < init() does this
        # if its a dom . set that as default target

        self.q = None
        self.elements = None
        self.prevObject = None
        self.eventHandler = EventHandler()
        if type(dom) == str:
            # print("DO NOT CALL THIS METHOD DIRECTLY! use dQuery or º ")
            return
        else:
            dQuery_el.DOM = dom
            self.dom = dom

    def __str__(self):
        # print(type(self.elements))
        if isinstance(self.elements, (list, tuple)):
            # if isinstance(self.elements, (list, tuple)):
            # print([str(el) for el in self.elements])
            return "".join([str(el) for el in self.elements])
        else:
            # print('asd')
            return str(self.elements)

    def __getitem__(self, index):
        return self.elements[index]

    def _ensure_list(self):
        if self.elements is None:
            self.elements = []
        elif not isinstance(self.elements, (list, tuple)):
            self.elements = [self.elements]
        else:
            self.elements = list(self.elements)
        return self.elements

    @staticmethod
    def _match_selector(element, selector):
        if selector is None:
            return True
        if callable(selector):
            return selector(element)
        if isinstance(selector, str):
            if selector.startswith("#"):
                return element.getAttribute("id") == selector[1:]
            if selector.startswith("."):
                classes = (element.getAttribute("class") or "").split()
                return selector[1:] in classes
            return getattr(element, "tagName", "").lower() == selector.lower()
        return element == selector

    @staticmethod
    def _coerce_nodes(value):
        if isinstance(value, dQuery_el):
            value = value.elements
        if isinstance(value, tuple):
            return list(value)
        if isinstance(value, list):
            return value
        return [value]

    def _set_elements(self, elements, preserve_current=True):
        if preserve_current:
            current = (
                self._coerce_nodes(self.elements) if self.elements is not None else []
            )
            self.prevObject = list(current)
        self.elements = elements
        return self

    @staticmethod
    def _parse_numeric(value):
        if value in (None, "", "auto"):
            return 0
        if isinstance(value, (int, float)):
            return value
        match = re.search(r"-?\d+(?:\.\d+)?", str(value))
        return float(match.group(0)) if match else 0

    @staticmethod
    def _get_style_value(element, name, default=0):
        style = getattr(element, "style", None)
        if style is None:
            return default
        return getattr(style, name, default)

    @staticmethod
    def _event_object(event_name):
        if event_name in {
            "click",
            "dblclick",
            "mousedown",
            "mouseenter",
            "mouseleave",
            "mousemove",
            "mouseout",
            "mouseover",
            "mouseup",
        }:
            return MouseEvent(event_name)
        return Event(event_name)

    @property
    def dom(self):
        # print('getting')
        if dQuery_el.DOM is None:
            from domonic.dom import document

            return document
        # else:
        # print('GOT ONE')
        return dQuery_el.DOM

    @dom.setter
    def dom(self, dom):
        if isinstance(dom, (html, Document)):
            dQuery_el.DOM = dom

    def init(self, q=""):
        self.q = q
        if type(q) is not str:
            return
        # if q == "":
        # return

        if self.q[0] == "<":
            from domonic import domonic

            self.elements = domonic.load(self.q)
            # print(self.elements)
            # print(type(self.elements))
            if isinstance(self.elements, (html, Document)):
                self.dom = self.elements
        else:
            try:
                # element by selector not working on just classes as always needs a tag
                if self.q[0] == ".":

                    # NOTE - if jquery is not present chrome assigns $ to querySelector NOT querySelectorAll
                    # so differing behaviours may be expected.
                    # detect if there's a list in each method if not do it to first item?
                    # so it does bit of both? aka .append

                    self.elements = self.dom.querySelectorAll(self.q)
                    return

                self.elements = self.dom.getElementsBySelector(self.q, self.dom)
            except Exception as e:
                print("Error. No DOM has been set!!", e)
                raise e

    # def _listify(func):
    #     from functools import wraps
    #     @wraps(func)
    #     def as_list_wrapper(self, value=None, *args, **kwargs):
    #         if not isinstance(self.elements, (list, tuple)):
    #             self.elements = (self.elements,)
    #         value = func(value, *args, **kwargs)
    #         return value
    #     return as_list_wrapper

    def add(self, elements):
        """Create a new dQuery object with elements added to the set of matched elements."""
        self._ensure_list()
        if isinstance(elements, str):
            dq = º(0)
            dq.init(elements)
            self.elements.extend(self._coerce_nodes(dq.elements))
        else:
            self.elements.extend(self._coerce_nodes(elements))
        return self

    def addBack(self, selector):
        """Add the previous set of elements on the stack to the current set, optionally filtered by a selector."""
        previous = self.prevObject or []
        current = self._ensure_list()
        merged = current + [el for el in previous if el not in current]
        if selector is not None:
            merged = [el for el in merged if self._match_selector(el, selector)]
        self.elements = merged
        return self

    def addClass(self, name: str):
        """Adds the specified class to each element in the set of matched elements."""
        # print(self.elements, name)
        # print(type(self.elements))
        if not isinstance(self.elements, (list, tuple)):
            self.elements = (self.elements,)
        # print(type(self.elements))

        for el in self.elements:
            if el.getAttribute("class") is not None:
                el.setAttribute("class", el.getAttribute("class") + " " + name)
            else:
                el.setAttribute("class", name)
        return self

    def after(self, newnode):
        """Insert content, specified by the parameter, after each element in the set of matched elements."""
        if not isinstance(self.elements, (list, tuple)):
            self.elements = (self.elements,)

        for el in self.elements:
            p = el.parentNode
            for i, n in enumerate(p.children):
                if n == el:
                    l = list(p.args)
                    l.insert(i + 1, newnode)
                    p.args = tuple(l)
        return self

    def ajaxComplete(self, handler):
        """Register a handler to be called when Ajax requests complete. This is an Ajax Event"""
        raise NotImplementedError

    def ajaxError(self, handler):
        """Register a handler to be called when Ajax requests complete with an error. This is an Ajax Event"""
        raise NotImplementedError

    def ajaxSend(self, handler):
        """Register a handler to be called when Ajax requests complete successfully. This is an Ajax Event"""
        raise NotImplementedError

    def ajaxStart(self, handler):
        """Register a handler to be called when the first Ajax request begins. This is an Ajax Event"""
        raise NotImplementedError

    def ajaxStop(self, handler):
        """Register a handler to be called when all Ajax requests have completed. This is an Ajax Event"""
        raise NotImplementedError

    def ajaxSuccess(self, handler):
        """Attach a function to be executed whenever an Ajax request completes successfully. This is an Ajax Event."""
        raise NotImplementedError

    def andSelf(self):
        """Add the previous set of elements on the stack to the current set."""
        return self.addBack(None)

    def animate(self):
        """Perform a custom animation of a set of CSS properties."""
        raise NotImplementedError

    def append(self, html):
        """Insert content, specified by the parameter, to the end of each element in the set of matched elements."""

        # print('running append', self.elements, html)
        # print(len(self.elements))
        # print(":::::::::::", type(self.elements))

        if type(self.elements) is not tuple and type(self.elements) is not list:
            self.elements.innerHTML = self.elements.innerHTML + str(html)
            return self

        for el in self.elements:
            # print('EL!!')
            el.innerHTML = el.innerHTML + str(html)

        # print('APPEND SAYS:', self.elements)
        return self

    def appendTo(self, target):
        """Insert every element in the set of matched elements to the end of the target."""
        target += self.elements
        return target

    def attr(self, property, value=None):
        """Get the value of an attribute for the first element in the set of matched elements
        or set one or more attributes for every matched element."""

        # if not isinstance(self.elements, (list, tuple)):
        #     self.elements = (self.elements,)

        if value is not None:
            for el in self._ensure_list():
                el.setAttribute(property, value)
            return self
        if type(self.elements) is not tuple and type(self.elements) is not list:
            return self.elements.getAttribute(property)
        else:
            return self.elements[0].getAttribute(property)

    def before(self, content):  # TODO - test
        """Insert content, specified by the parameter, before each element in the set of matched elements."""
        if not isinstance(self.elements, (list, tuple)):
            self.elements = (self.elements,)
        for el in self.elements:
            p = el.parentNode
            for i, n in enumerate(p.children):
                if n == el:
                    l = list(p.args)
                    l.insert(i, content)
                    p.args = tuple(l)
        return self

    def bind(self, event, handler):  # TODO - untested
        """Attach a function to be executed when an event occurs on a set of matched elements."""
        if not isinstance(self.elements, (list, tuple)):
            self.elements = (self.elements,)
        for el in self.elements:
            el.addEventListener(event, handler)
        return self

    def blur(self, handler):  # TODO - untested
        """Bind an event handler to the “blur” JavaScript event, or trigger that event on an element."""
        if not isinstance(self.elements, (list, tuple)):
            self.elements = (self.elements,)
        for el in self.elements:
            el.triggerEvent("blur")
        return self

    def change(
        self, handler
    ):  # TODO - untested... from description sound like would be something like this?
        """Bind an event handler to the “change” JavaScript event, or trigger that event on an element."""
        if not isinstance(self.elements, (list, tuple)):
            self.elements = (self.elements,)
        for el in self.elements:
            if el.hasEvent("change"):
                el.triggerEvent("change")
            else:
                el.addEventListener("change", handler)
            # el.triggerEvent('change')
        return self

    def children(self, selector=None):  # TODO - test
        """Get the children of each element in the set of matched elements, optionally filtered by a selector."""
        children = []
        for el in self._ensure_list():
            for child in list(el.children):
                if self._match_selector(child, selector):
                    children.append(child)
        self.elements = children
        return self

    def clearQueue(self):
        """Remove from the queue all items that have not yet been run."""
        for el in self._ensure_list():
            setattr(el, "_dquery_queue", [])
        return self

    def click(self, handler=None):
        """Bind an event handler to the “click” JavaScript event, or trigger that event on an element."""
        if handler is None:
            for el in self._ensure_list():
                el.dispatchEvent(MouseEvent("click"))
        else:
            for el in self._ensure_list():
                self.eventHandler.bindEvent("click", handler, el)
        return self

    # Create a deep copy of the set of matched elements.
    def clone(self):
        """Create a deep copy of the set of matched elements."""
        import copy

        dq = º(0)
        dq.elements = [copy.deepcopy(el) for el in self._ensure_list()]
        return dq

    def closest(self, selector=None):
        """For each element in the set, get the first element that matches the selector by testing the element itself
        and traversing up through its ancestors in the DOM tree."""
        matches = []
        for el in self._ensure_list():
            current = el
            while current is not None:
                if self._match_selector(current, selector):
                    matches.append(current)
                    break
                current = current.parentNode
        self._set_elements(matches)
        return self

    def contents(self, selector=None):
        """Get the children of each element in the set of matched elements, including text and comment nodes."""
        contents = []
        for el in self._ensure_list():
            for child in list(el.args):
                if selector is None or self._match_selector(child, selector):
                    contents.append(child)
        self._set_elements(contents)
        return self

    @property
    def context(self):
        """The DOM node context originally passed to dQuery if none was passed
        then context will likely be the document."""
        from domonic.dom import document

        return document

    def contextmenu(self):
        """Bind an event handler to the “contextmenu” JavaScript event, or trigger that event on an element."""
        return self._simple_event("contextmenu")

    def css(self, property, value=None):  # TODO - untested
        """Get the value of a computed style property for the first element in the set of matched elements
        or set one or more CSS properties for every matched element."""
        if not isinstance(self.elements, (list, tuple)):
            self.elements = (self.elements,)
        if value is not None:
            if self.elements[0].style.getProperty(property) is not None:
                self.elements[0].style.setProperty(property, value)
                return self
        if type(self.elements) is not tuple and type(self.elements) is not list:
            return self.elements.style.getProperty(property)
        else:
            return self.elements[0].style.getProperty(property)

    def data(self, key, value=None):
        """Store arbitrary data associated with the matched elements or return the value at the named data store
        for the first element in the set of matched elements."""
        elements = self._ensure_list()
        if value is None:
            store = getattr(elements[0], "_dquery_data", {})
            return store.get(key)
        for el in elements:
            store = getattr(el, "_dquery_data", {}).copy()
            store[key] = value
            setattr(el, "_dquery_data", store)
        return self

    def dblclick(self, handler=None):
        """Bind an event handler to the “dblclick” JavaScript event, or trigger that event on an element."""
        return self._simple_event("dblclick", handler)

    def delay(self, time):
        """Set a timer to delay execution of subsequent items in the queue."""
        for el in self._ensure_list():
            queue = getattr(el, "_dquery_queue", [])
            queue.append(("delay", time))
            setattr(el, "_dquery_queue", queue)
        return self

    def delegate(self, selector, event, handler):
        """Attach a handler to one or more events for all elements that match the selector, now or in the future,
        based on a specific set of root elements."""
        for el in self._ensure_list():

            def delegated(evt, _selector=selector, _handler=handler):
                target = getattr(evt, "target", None)
                if target is not None and self._match_selector(target, _selector):
                    _handler(evt)

            self.eventHandler.bindEvent(event, delegated, el)
        return self

    def dequeue(self):
        """Execute the next function on the queue for the matched elements."""
        for el in self._ensure_list():
            queue = getattr(el, "_dquery_queue", [])
            if not queue:
                continue
            item = queue.pop(0)
            setattr(el, "_dquery_queue", queue)
            if callable(item):
                item()
        return self

    def detach(self):  # TODO - test
        """Remove the set of matched elements from the DOM."""
        detached = []
        for el in self._ensure_list():
            p = el.parentNode
            for i, n in enumerate(p.children):
                if n == el:
                    l = list(p.args)
                    l.pop(i)
                    p.args = tuple(l)
                    detached.append(el)
                    break
        self.elements = detached
        return self

    def die(self):
        """Remove event handlers previously attached using .live from the elements."""
        return self.unbind()

    def each(self, func):
        """Iterate over a dQuery object, executing a function for each matched element."""
        # TODO - untested
        for index, value in enumerate(self._ensure_list()):
            try:
                func(index, value)
            except Exception as e:
                func(index)
        return self

    # @_listify
    def empty(self):
        """Remove all child nodes of the set of matched elements from the DOM."""
        # TODO - test
        for el in self._ensure_list():
            el.args = ()
        return self

    def end(self):
        """End the most recent filtering operation in the current chain and return the
        set of matched elements to its previous state."""
        if self.prevObject is not None:
            self.elements = list(self.prevObject)
            self.prevObject = None
        return self

    def eq(self, index):
        """Reduce the set of matched elements to the one at the specified index."""
        return self.elements[index]

    def error(self, handler):
        """Bind an event handler to the “error” JavaScript event."""
        return self._simple_event("error", handler)

    def even(self):  # TODO - untested
        """Reduce the set of matched elements to the even ones in the set, numbered from zero."""
        self.elements = [
            el for index, el in enumerate(self._ensure_list()) if index % 2 == 0
        ]
        return self

    def fadeIn(self):
        """Display the matched elements by fading them to opaque."""
        raise NotImplementedError

    def fadeOut(self):
        """Hide the matched elements by fading them to transparent."""
        raise NotImplementedError

    def fadeTo(self):
        """Adjust the opacity of the matched elements."""
        raise NotImplementedError

    def fadeToggle(self):
        """Display or hide the matched elements by animating their opacity."""
        raise NotImplementedError

    def filter(self, selector):  # TODO - untested
        """Reduce the set of matched elements to those that match the selector or pass the function’s test."""
        self.elements = [
            el for el in self._ensure_list() if self._match_selector(el, selector)
        ]
        return self

    def find(self, selector):
        """Get the descendants of each element in the current set of matched elements, filtered by a selector,
        dQuery object, or element."""
        found = []
        for el in self._ensure_list():
            if isinstance(selector, str):
                matches = el.querySelectorAll(selector)
                found.extend(
                    list(matches) if isinstance(matches, (list, tuple)) else [matches]
                )
            else:
                for child in el.getElementsByTagName("*"):
                    if self._match_selector(child, selector):
                        found.append(child)
        self.elements = found
        return self

    def finish(self):
        """Stop the currently-running animation, remove all queued animations, and complete all animations
        for the matched elements."""
        raise NotImplementedError

    def first(self):
        """Reduce the set of matched elements to the first in the set."""
        if isinstance(self.elements, (list, tuple)):
            self.elements = self.elements[0]
        return self

    def focus(self):
        """Bind an event handler to the “focus” JavaScript event, or trigger that event on an element."""
        for el in self._ensure_list():
            el.dispatchEvent(Event("focus"))
        return self

    def focusin(self):
        """Bind an event handler to the “focusin” event."""
        for el in self._ensure_list():
            el.dispatchEvent(Event("focusin"))
        return self

    def focusout(self):
        """Bind an event handler to the “focusout” JavaScript event."""
        for el in self._ensure_list():
            el.dispatchEvent(Event("focusout"))
        return self

    # def get(self):
    #     """ Retrieve the DOM elements matched by the dQuery object."""
    #     raise NotImplementedError

    def has(self, selector):  # TODO - test
        """Reduce the set of matched elements to those that have a descendant
        that matches the selector or DOM element."""
        matched = []
        for el in self._ensure_list():
            descendants = (
                el.querySelectorAll(selector)
                if isinstance(selector, str)
                else el.getElementsByTagName("*")
            )
            descendants = (
                descendants if isinstance(descendants, (list, tuple)) else [descendants]
            )
            if any(
                self._match_selector(child, selector)
                for child in descendants
                if child is not None
            ):
                matched.append(el)
        self.elements = matched
        return self

    def hasClass(self, classname):
        """Determine whether any of the matched elements are assigned the given class."""
        if not isinstance(self.elements, (list, tuple)):
            self.elements = (self.elements,)

        for el in self.elements:
            if el.getAttribute("class") is not None:
                if classname in el.getAttribute("class"):
                    return True
        return False

    def height(self):
        """Get the current computed height for the first element in the set of matched elements or set the height
        of every matched element."""
        el = self._ensure_list()[0]
        return self._parse_numeric(self._get_style_value(el, "height", 0))

    def hide(self):
        """Hide the matched elements."""
        for el in self._ensure_list():
            el.style.display = "none"
        return self

    def hover(self, handlerIn=None, handlerOut=None):
        """Bind one or two handlers to the matched elements, to be executed when the mouse pointer enters and
        leaves the elements."""
        if handlerIn is not None:
            self.mouseenter(handlerIn)
        if handlerOut is not None:
            self.mouseleave(handlerOut)
        return self

    def html(self, html=None):
        """Get the HTML contents of the first element in the set of matched elements or set the HTML contents
        of every matched element."""
        elements = self._ensure_list()
        if html == None:
            return elements[0].innerHTML
        for el in elements:
            el.innerHTML = html
        return self

    def index(self):  # TODO - test
        """Search for a given element from among the matched elements."""
        elements = self._ensure_list()
        if not elements:
            return -1
        first = elements[0]
        if first.parentNode is None:
            return 0
        siblings = list(first.parentNode.children)
        return siblings.index(first) if first in siblings else -1

    def innerHeight(self):
        """Get the current computed inner height (including padding but not border) for the first element in the set
        of matched elements or set the inner height of every matched element."""
        el = self._ensure_list()[0]
        return (
            self._parse_numeric(self._get_style_value(el, "height", 0))
            + self._parse_numeric(self._get_style_value(el, "paddingTop", 0))
            + self._parse_numeric(self._get_style_value(el, "paddingBottom", 0))
        )

    def innerWidth(self):
        """Get the current computed inner width (including padding but not border) for the first element in the set
        of matched elements or set the inner width of every matched element."""
        el = self._ensure_list()[0]
        return (
            self._parse_numeric(self._get_style_value(el, "width", 0))
            + self._parse_numeric(self._get_style_value(el, "paddingLeft", 0))
            + self._parse_numeric(self._get_style_value(el, "paddingRight", 0))
        )

    def insertAfter(self, target):  # TODO - test
        """Insert the matched elements after the specified target element."""
        if not isinstance(self.elements, (list, tuple)):
            self.elements = (self.elements,)

        if isinstance(target, (list, tuple)):
            for index, value in enumerate(target):
                for el in self.elements:
                    el.insertAfter(value)
        elif isinstance(target, str):
            for el in self.elements:
                el.insertAfter(target)
        elif isinstance(target, Element):
            for el in self.elements:
                el.insertAfter(target)

        return self

    def insertBefore(self, target):  # TODO - test
        """Insert every element in the set of matched elements before the target."""
        if not isinstance(self.elements, (list, tuple)):
            self.elements = (self.elements,)
        if isinstance(target, (list, tuple)):
            for index, value in enumerate(target):
                for el in self.elements:
                    el.insertBefore(value)
        elif isinstance(target, str):
            for el in self.elements:
                el.insertBefore(target)
        elif isinstance(target, Element):
            for el in self.elements:
                el.insertBefore(target)
        return self

        # def is(self):
        """ Check the current matched set of elements against a selector, element,
        or dQuery object and return true if at least one of these elements matches the given arguments."""
        # raise NotImplementedError

    def keydown(self):
        """Bind an event handler to the “keydown” JavaScript event, or trigger that event on an element."""
        raise NotImplementedError

    def keypress(self):
        """Bind an event handler to the “keypress” JavaScript event, or trigger that event on an element."""
        raise NotImplementedError

    def keyup(self):
        """Bind an event handler to the “keyup” JavaScript event, or trigger that event on an element."""
        raise NotImplementedError

    def last(self):
        """Reduce the set of matched elements to the final one in the set."""
        if isinstance(self.elements, (list, tuple)):
            self.elements = self.elements[len(self.elements) - 1]
        return self

    @property
    def length(self):
        """The number of elements in the dQuery object."""
        return len(self.elements)

    def live(self):
        """Attach an event handler for all elements which match the current selector, now and in the future."""
        raise NotImplementedError

    def load(self, url, data=None, complete=None):  # TODO - test
        """Load data from the server and place the returned HTML into the matched elements."""
        if data is None:
            data = {}
        if complete is None:
            complete = lambda x: x
        for el in self.elements:
            el.innerHTML = ""
            el.innerHTML = "<div class='loading'></div>"

            def load(el, url, data, complete):
                def onload(response):
                    el.innerHTML = ""
                    el.innerHTML = response
                    complete(response)

                dQuery.ajax(url, data, onload)

            load(el, url, data, complete)
        return self

    def map(self, func):  # TODO - test
        """Pass each element in the current matched set through a function,
        producing a new dQuery object containing the return values."""
        if not isinstance(self.elements, (list, tuple)):
            self.elements = (self.elements,)
        return dQuery(map(func, self.elements))

    def mousedown(self, handler=None):
        """Bind an event handler to the “mousedown” JavaScript event, or trigger that event on an element."""
        return self._simple_event("mousedown", handler)

    def mouseenter(self, handler=None):
        """Bind an event handler to be fired when the mouse enters an element,
        or trigger that handler on an element."""
        return self._simple_event("mouseenter", handler)

    def mouseleave(self, handler=None):
        """Bind an event handler to be fired when the mouse leaves an element,
        or trigger that handler on an element."""
        return self._simple_event("mouseleave", handler)

    def mousemove(self, handler=None):
        """Bind an event handler to the “mousemove” JavaScript event, or trigger that event on an element."""
        return self._simple_event("mousemove", handler)

    def mouseout(self, handler=None):
        """Bind an event handler to the “mouseout” JavaScript event, or trigger that event on an element."""
        return self._simple_event("mouseout", handler)

    def mouseover(self, handler=None):
        """Bind an event handler to the “mouseover” JavaScript event, or trigger that event on an element."""
        return self._simple_event("mouseover", handler)

    def mouseup(self, handler=None):
        """Bind an event handler to the “mouseup” JavaScript event, or trigger that event on an element."""
        return self._simple_event("mouseup", handler)

    def next(self, selector=None):  # TODO - test
        """Get the immediately following sibling of each element in the set of matched elements.
        If a selector is provided, it retrieves the next sibling only if it matches that selector.
        """
        matches = []
        for el in self._ensure_list():
            if el.parentNode is None:
                continue
            siblings = list(el.parentNode.children)
            try:
                index = siblings.index(el)
            except ValueError:
                continue
            if index + 1 < len(siblings):
                candidate = siblings[index + 1]
                if self._match_selector(candidate, selector):
                    matches.append(candidate)
        self.elements = matches
        return self

    def nextAll(self, selector):
        """Get all following siblings of each element in the set of matched elements,
        optionally filtered by a selector."""
        matches = []
        for el in self._ensure_list():
            if el.parentNode is None:
                continue
            siblings = list(el.parentNode.children)
            try:
                index = siblings.index(el)
            except ValueError:
                continue
            for candidate in siblings[index + 1 :]:
                if self._match_selector(candidate, selector):
                    matches.append(candidate)
        self._set_elements(matches)
        return self

    def nextUntil(self, selector):
        """Get all following siblings of each element up to but not including the element matched by the selector,
        DOM node, or dQuery object passed."""
        matches = []
        for el in self._ensure_list():
            if el.parentNode is None:
                continue
            siblings = list(el.parentNode.children)
            try:
                index = siblings.index(el)
            except ValueError:
                continue
            for candidate in siblings[index + 1 :]:
                if self._match_selector(candidate, selector):
                    break
                matches.append(candidate)
        self._set_elements(matches)
        return self

        # def not(self):
        """ Remove elements from the set of matched elements."""
        # raise NotImplementedError

    def odd(self):  # TODO - untested
        """Reduce the set of matched elements to the odd ones in the set, numbered from zero."""
        self.elements = [
            el for index, el in enumerate(self._ensure_list()) if index % 2 == 1
        ]
        return self

    def off(self, event):
        """Remove an event handler."""
        for el in self.elements:
            self.eventHandler.unbindEvent(event, el)

    def offset(self, coordinates=None):
        """Get the current coordinates of the first element, or set the coordinates of every element,
        in the set of matched elements, relative to the document."""
        elements = self._ensure_list()
        if coordinates is not None:
            for el in elements:
                if "top" in coordinates:
                    el.style.top = coordinates["top"]
                if "left" in coordinates:
                    el.style.left = coordinates["left"]
            return self
        el = elements[0]
        return {
            "top": self._parse_numeric(self._get_style_value(el, "top", 0)),
            "left": self._parse_numeric(self._get_style_value(el, "left", 0)),
        }

    def offsetParent(self):
        """Get the closest ancestor element that is positioned."""
        return self._ensure_list()[0].parentNode

    def on(self, event, callback):
        """Attach an event handler function for one or more events to the selected elements."""
        for el in self.elements:
            self.eventHandler.bindEvent(event, callback, el)
        return self

    def one(self, event, callback):
        """Attach a handler to an event for the elements.
        The handler is executed at most once per element per event type."""
        for el in self._ensure_list():

            @functools.wraps(callback)
            def wrapper(evt, _el=el):
                callback(evt)
                _el.removeEventListener(event, wrapper)

            self.eventHandler.bindEvent(event, wrapper, el)
        return self

    def outerHeight(self):
        """Get the current computed outer height (including padding, border,
        and optionally margin) for the first element in the set of matched elements or set the outer height
        of every matched element."""
        el = self._ensure_list()[0]
        return (
            self.innerHeight()
            + self._parse_numeric(self._get_style_value(el, "borderTopWidth", 0))
            + self._parse_numeric(self._get_style_value(el, "borderBottomWidth", 0))
        )

    def outerWidth(self):
        """Get the current computed outer width (including padding, border, and optionally margin) for the
        first element in the set of matched elements or set the outer width of every matched element.
        """
        el = self._ensure_list()[0]
        return (
            self.innerWidth()
            + self._parse_numeric(self._get_style_value(el, "borderLeftWidth", 0))
            + self._parse_numeric(self._get_style_value(el, "borderRightWidth", 0))
        )

    def parent(self, selector=None):  # TODO - test
        """Get the parent of each element in the current set of matched elements,
        optionally filtered by a selector."""
        parents = []
        for el in self._ensure_list():
            parent = el.parentNode
            if parent is not None and self._match_selector(parent, selector):
                parents.append(parent)
        self.elements = parents
        return self

    def parents(self, selector=None):  # TODO - untested
        """Get the ancestors of each element in the current set of matched elements,
        optionally filtered by a selector."""
        parents = []
        for el in self._ensure_list():
            current = el.parentNode
            while current is not None:
                if self._match_selector(current, selector):
                    parents.append(current)
                current = current.parentNode
        self.elements = parents
        return self

    def parentsUntil(self, selector):
        """Get the ancestors of each element in the current set of matched elements,
        up to but not including the element matched by the selector, DOM node, or dQuery object.
        """
        parents = []
        for el in self._ensure_list():
            current = el.parentNode
            while current is not None and not self._match_selector(current, selector):
                parents.append(current)
                current = current.parentNode
        self._set_elements(parents)
        return self

    def position(self):
        """Get the current coordinates of the first element in the set of matched elements,
        relative to the offset parent."""
        return self.offset()

    def prepend(self, html):
        """Insert content, specified by the parameter, to the beginning of each element
        in the set of matched elements."""
        for el in self._ensure_list():
            el.innerHTML = html + el.innerHTML
        return self

    def prependTo(self, target):  # TODO - test
        """Insert every element in the set of matched elements to the beginning of the target."""
        if not isinstance(self.elements, (list, tuple)):
            self.elements = (self.elements,)
        for el in self.elements:
            target.append(el)
        return self

    def prev(self, selector=None):  # TODO - untested
        """Get the immediately preceding sibling of each element in the set of matched elements.
        If a selector is provided, it retrieves the previous sibling only if it matches that selector.
        """
        matches = []
        for el in self._ensure_list():
            if el.parentNode is None:
                continue
            siblings = list(el.parentNode.children)
            try:
                index = siblings.index(el)
            except ValueError:
                continue
            if index > 0:
                candidate = siblings[index - 1]
                if self._match_selector(candidate, selector):
                    matches.append(candidate)
        self._set_elements(matches)
        return self

    def prevAll(self, selector=None):  # TODO - untested
        """Get all preceding siblings of each element in the set of matched elements,
        optionally filtered by a selector."""
        matches = []
        for el in self._ensure_list():
            if el.parentNode is None:
                continue
            siblings = list(el.parentNode.children)
            try:
                index = siblings.index(el)
            except ValueError:
                continue
            for candidate in siblings[:index]:
                if self._match_selector(candidate, selector):
                    matches.append(candidate)
        self._set_elements(matches)
        return self

    def prevUntil(self, selector):  # TODO - untested
        """Get all preceding siblings of each element up to but not including the element matched by the selector,
        DOM node, or dQuery object."""
        matches = []
        for el in self._ensure_list():
            if el.parentNode is None:
                continue
            siblings = list(el.parentNode.children)
            try:
                index = siblings.index(el)
            except ValueError:
                continue
            for candidate in reversed(siblings[:index]):
                if self._match_selector(candidate, selector):
                    break
                matches.insert(0, candidate)
        self._set_elements(matches)
        return self

    def promise(self):
        """Return a Promise object to observe when all actions of a certain type bound to the collection,
        queued or not, have finished."""
        return {"state": "resolved", "length": len(self._ensure_list())}

    def prop(self, property, value):
        """Get the value of a property for the first element in the set of matched elements or set one or more properties
        for every matched element."""
        return self.attr(property, value)

    def pushStack(self, stack):  # TODO - test
        """Add a collection of DOM elements onto the dQuery."""
        if not isinstance(self.elements, (list, tuple)):
            self.elements = (self.elements,)
        for el in self.elements:
            el.append(stack)
        return self

    def queue(self):
        """Show or manipulate the queue of functions to be executed on the matched elements."""
        queues = [getattr(el, "_dquery_queue", []) for el in self._ensure_list()]
        return queues[0] if len(queues) == 1 else queues

    def ready(self, callback):
        """Specify a function to execute when the DOM is fully loaded."""
        callback()
        return self

    def remove(self, items):  # TODO - test
        """Remove the set of matched elements from the DOM."""
        for el in self._ensure_list():
            if el.parentNode is not None:
                el.parentNode.removeChild(el)
        return self

    def removeAttr(self, attr: str):  # TODO - test
        """Remove an attribute from each element in the set of matched elements."""
        if not isinstance(self.elements, (list, tuple)):
            self.elements = (self.elements,)
        for el in self.elements:
            el.removeAttribute(attr)
        return self

    def removeClass(self, classname: str):
        """Remove a single class, multiple classes, or all classes from each element in the set of matched elements."""

        if not isinstance(self.elements, (list, tuple)):
            self.elements = (self.elements,)

        for el in self.elements:
            if el.getAttribute("class") is not None:
                if classname in el.getAttribute("class"):
                    removed = "".join(el.getAttribute("class").split(classname)).strip()
                    removed = removed.replace("  ", " ")
                    el.setAttribute("class", removed)
        return self

    def removeData(self, name: str):
        """Remove a previously-stored piece of data."""
        for el in self._ensure_list():
            store = getattr(el, "_dquery_data", {}).copy()
            store.pop(name, None)
            setattr(el, "_dquery_data", store)
        return self

    def removeProp(self, prop: str):  # TODO -
        """Remove a property for the set of matched elements."""
        if not isinstance(self.elements, (list, tuple)):
            self.elements = (self.elements,)
        for el in self.elements:
            el.removeAttribute(prop)
        return self

    def replaceAll(self, elements):  # TODO - untested
        """Replace each target element with the set of matched elements."""
        targets = self._coerce_nodes(elements)
        replacements = self._ensure_list()
        for index, target in enumerate(targets):
            if target.parentNode is None or not replacements:
                continue
            replacement = copy.deepcopy(replacements[min(index, len(replacements) - 1)])
            target.parentNode.replaceChild(replacement, target)
        return self

    def replaceWith(self, replacement):  # TODO - test
        """Replace each element in the set of matched elements with the provided new content and return the set
        of elements that was removed."""
        if not isinstance(self.elements, (list, tuple)):
            self.elements = (self.elements,)
        old_elements = []
        for el in self.elements:
            old_elements.append(el)
            el.parentNode.replaceChild(replacement, el)
        return self

    def resize(self, callback=None):
        """Bind an event handler to the “resize” JavaScript event, or trigger that event on an element."""
        return self._simple_event("resize", callback)

    def scroll(self, callback=None):
        """Bind an event handler to the “scroll” JavaScript event, or trigger that event on an element."""
        return self._simple_event("scroll", callback)

    def scrollLeft(self, value=None):
        """Get the current horizontal position of the scroll bar for the first element in the set of matched elements
        or set the horizontal position of the scroll bar for every matched element."""
        elements = self._ensure_list()
        if value is not None:
            for el in elements:
                setattr(el, "_scroll_left", value)
            return self
        return getattr(elements[0], "_scroll_left", 0)

    def scrollTop(self, value=None):
        """Get the current vertical position of the scroll bar for the first element in the set of matched elements
        or set the vertical position of the scroll bar for every matched element."""
        elements = self._ensure_list()
        if value is not None:
            for el in elements:
                setattr(el, "_scroll_top", value)
            return self
        return getattr(elements[0], "_scroll_top", 0)

    def select(self, selector=None):
        """Bind an event handler to the “select” JavaScript event, or trigger that event on an element."""
        return self._simple_event("select", selector)

    def serialize(self):
        """Encode a set of form elements as a string for submission."""
        # raise NotImplementedError
        # from domonic.javascript import Global

        elements = self._ensure_list()
        if not elements:
            return ""
        form = elements[0]

        if form.nodeName.upper() != "FORM":
            return

        q = []
        for el in form.elements:

            name = el.getAttribute("name")
            if name in (None, ""):
                continue

            node_name = el.nodeName.upper()

            if node_name == "INPUT":
                value = getattr(el, "value", None)
                if value is None:
                    value = el.nodeValue if el.nodeValue is not None else ""
                if el.type in [
                    "email",
                    "text",
                    "hidden",
                    "password",
                    "button",
                    "reset",
                    "submit",
                    "email",
                ]:
                    q.append(name + "=" + Global.encodeURIComponent(value))
                elif el.type in ["checkbox", "radio"]:
                    if el.checked:
                        q.append(name + "=" + Global.encodeURIComponent(value))
            elif node_name == "TEXTAREA":
                value = getattr(el, "value", None)
                if value is None:
                    value = el.nodeValue if el.nodeValue is not None else ""
                q.append(name + "=" + Global.encodeURIComponent(value))
            elif node_name == "SELECT":
                if el.getAttribute("multiple") != None:
                    for option in el.getElementsByTagName("option"):
                        if option.getAttribute("selected") != None:
                            q.append(
                                name + "=" + Global.encodeURIComponent(option.nodeValue)
                            )
                else:
                    selected = None
                    for option in el.getElementsByTagName("option"):
                        if option.getAttribute("selected") is not None:
                            selected = option
                            break
                    value = selected.nodeValue if selected is not None else el.nodeValue
                    q.append(name + "=" + Global.encodeURIComponent(value))
            elif node_name == "BUTTON":
                value = getattr(el, "value", None)
                if value is None:
                    value = el.nodeValue if el.nodeValue is not None else ""
                if el.type in ["reset", "submit", "button"]:
                    q.append(name + "=" + Global.encodeURIComponent(value))

        return "&".join(q)

    def serializeArray(self, array=None):
        """Encode an array of form elements as a string for submission."""
        elements = self._ensure_list()
        if not elements:
            return []
        form = elements[0]
        if form.nodeName.upper() != "FORM":
            return []

        serialized = []
        for el in form.elements:
            name = el.getAttribute("name")
            if name in (None, ""):
                continue
            node_name = el.nodeName.upper()

            if node_name == "SELECT" and el.getAttribute("multiple") is not None:
                for option in el.getElementsByTagName("option"):
                    if option.getAttribute("selected") is not None:
                        serialized.append({"name": name, "value": option.nodeValue})
                continue

            value = getattr(el, "value", None)
            if value is None:
                value = el.nodeValue if el.nodeValue is not None else ""
            serialized.append({"name": name, "value": value})
        return serialized

    def show(self):
        """Display the matched elements."""
        for el in self._ensure_list():
            el.style.display = ""
        return self

    def siblings(self, selector=None):  # TODO - untested
        """Return the siblings of the matched elements. filter by selector."""
        siblings = []
        for el in self._ensure_list():
            if el.parentNode is None:
                continue
            for sibling in list(el.parentNode.children):
                if sibling != el and self._match_selector(sibling, selector):
                    siblings.append(sibling)
        self.elements = siblings
        return self

    def size(self):
        """Return the number of elements in the dQuery object."""
        return len(self.elements)

    def slice(self, start, end):  # TODO - test
        """Return a new dQuery object containing the set of matched elements starting at the specified index
        and ending at the specified index."""
        dq = º(0)
        dq.elements = self._ensure_list()[start:end]
        return dq

    def slideDown(self):
        """Display the matched elements with a sliding motion."""
        raise NotImplementedError

    def slideToggle(self):
        """Display or hide the matched elements with a sliding motion."""
        raise NotImplementedError

    def slideUp(self):
        """Hide the matched elements with a sliding motion."""
        raise NotImplementedError

    def stop(self):
        """Stop the currently-running animation on the matched elements."""
        raise NotImplementedError

    def submit(self):
        """Bind an event handler to the “submit” JavaScript event, or trigger that event on an element."""
        for el in self._ensure_list():
            el.dispatchEvent(Event("submit"))
        return self

    def text(self, newVal: str = None):
        """Get the combined text contents of each element in the set of matched elements, including their descendants,
        or set the text contents of the matched elements."""
        elements = self._ensure_list()
        if newVal is not None:
            for el in elements:
                el.textContent = newVal
            return self
        else:
            return [el.textContent for el in elements]

    def toArray(self):
        """Retrieve all the elements contained in the dQuery set, as an array."""
        # raise NotImplementedError
        return self._ensure_list()

    def toggle(self):  # TODO - test
        """Display or hide the matched elements."""
        for el in self._ensure_list():
            el.style.display = "" if el.style.display == "none" else "none"
        return self

    # @_listify
    def toggleClass(self, className):
        """
        Add or remove one or more classes from each element in the set of matched elements
        """
        # TODO - untested / not working

        # if not isinstance(self.elements, (list, tuple)):
        #     self.elements = (self.elements,)

        # for el in self.elements:
        #     if º(el).hasClass(className):
        #         º(el).addClass(className)
        #     else:
        #         º(el).removeClass(className)
        for el in self._ensure_list():
            classes = (el.getAttribute("class") or "").split()
            if className in classes:
                classes = [cls for cls in classes if cls != className]
            else:
                classes.append(className)
            if classes:
                el.setAttribute("class", " ".join(classes))
            else:
                el.removeAttribute("class")
        return self

    def trigger(self, eventName, eventArg=None):  # TODO - test
        """Execute all handlers and behaviors attached to the matched elements for the given event type."""
        if not isinstance(self.elements, (list, tuple)):
            self.elements = (self.elements,)
        for el in self.elements:
            if el.nodeName == "A":
                # el.triggerEvent(eventName, eventArg)
                el.dispatchEvent(eventName, eventArg)
            else:
                # el.trigger(eventName, eventArg)
                el.dispatchEvent(eventName, eventArg)
        return self

    def triggerHandler(self, eventName):
        """Execute all handlers attached to an element for an event."""
        elements = self._ensure_list()
        if not elements:
            return None
        event = Event(eventName)
        elements[0].dispatchEvent(event)
        return event

    def unbind(self, event=None):
        """Remove a previously-attached event handler from the elements."""
        for el in self._ensure_list():
            if event is None:
                for event_type in list(el.listeners.keys()):
                    for callback in list(el.listeners[event_type]):
                        el.removeEventListener(event_type, callback)
                self.eventHandler.events = [
                    registered
                    for registered in self.eventHandler.events
                    if registered["target"] != el
                ]
            else:
                for callback in list(el.listeners.get(event, [])):
                    el.removeEventListener(event, callback)
                self.eventHandler.events = [
                    registered
                    for registered in self.eventHandler.events
                    if not (registered["target"] == el and registered["_type"] == event)
                ]
        return self

    def undelegate(self):
        """Remove a handler from the event for all elements which match the current selector,
        based upon a specific set of root elements."""
        raise NotImplementedError

    def unload(self, handler=None):
        """Bind an event handler to the “unload” JavaScript event."""
        return self._simple_event("unload", handler)

    def unwrap(self):  # TODO - untested
        """Remove the parents of the set of matched elements from the DOM,
        leaving the matched elements in their place."""
        if not isinstance(self.elements, (list, tuple)):
            self.elements = (self.elements,)
        for el in self.elements:
            if el.parentNode.parentNode:
                el.parentNode.parentNode.replaceChild(el, el.parentNode)
        return self

    def val(self, newVal=None):
        """Get the current value of the first element in the set of matched elements
        or set the value of every matched element."""
        elements = self._ensure_list()
        if newVal is not None:
            for el in elements:
                el.value = newVal
            return self
        else:
            return getattr(elements[0], "value", None)

    def width(self):
        """Get the current computed width for the first element in the set of matched elements
        or set the width of every matched element."""
        el = self._ensure_list()[0]
        return self._parse_numeric(self._get_style_value(el, "width", 0))

    def wrap(self, wrappingElement):  # TODO - untested
        """Wrap an HTML structure around each element in the set of matched elements."""
        if isinstance(wrappingElement, str):
            from domonic.html import create_element

            wrappingElement = create_element(wrappingElement)
        for el in self._ensure_list():
            wrapper = wrappingElement.__class__()
            parent = el.parentNode
            wrapper.appendChild(el)
            if parent is not None:
                parent.replaceChild(wrapper, el)
        return self

    def wrapAll(self, wrappingElement):
        """Wrap an HTML structure around all elements in the set of matched elements."""
        elements = self._ensure_list()
        if not elements:
            return self
        if isinstance(wrappingElement, str):
            from domonic.html import create_element

            wrapper = create_element(wrappingElement)
        else:
            wrapper = wrappingElement
        first = elements[0]
        parent = first.parentNode
        if parent is not None:
            parent.replaceChild(wrapper, first)
        wrapper.appendChild(first)
        for el in elements[1:]:
            if el.parentNode is not None:
                el.parentNode.removeChild(el)
            wrapper.appendChild(el)
        return self

    def wrapInner(self):
        """Wrap an HTML struct"""
        raise NotImplementedError

    def _simple_event(self, name, handler=None):
        if handler is None:
            for el in self._ensure_list():
                el.dispatchEvent(self._event_object(name))
        else:
            for el in self._ensure_list():
                self.eventHandler.bindEvent(name, handler, el)
        return self


# class Callbacks():  # TODO - untested. copilot wrote it

#     def __init__(self):
#         self.callbacks = {}

#     def add(self, callback, *args):
#         """[Add a callback or a collection of callbacks to a callback list.]

#         Args:
#             callback (function): [a callback]

#         """
#         if callback in self.callbacks:
#             self.callbacks[callback].append(args)
#         else:
#             self.callbacks[callback] = [args]

#     def disable(self, callback):
#         """[Disable a callback or a collection of callbacks from doing anything.]

#         Args:
#             callback (function): [a callback]

#         """
#         self.callbacks[callback] = []

#     def disabled(self, callback):
#         """ Determine if the callbacks list has been disabled."""
#         return callback not in self.callbacks

#     def empty(self, callback):
#         """ Remove all of the callbacks from a list."""
#         if callback in self.callbacks:
#             del self.callbacks[callback]

#     def fire(self, *args):
#         """ Call all of the callbacks with the given arguments. """
#         for callback in self.callbacks:
#             callback(*args)

#     def fired(self, *args):
#         """ Determine if the callbacks have already been called at least once."""
#         return self.callbacks.fired

#     def fireWith(self, *args):
#         """[Fire the callback(s) with the given arguments.]

#         Args:
#             callback (function): [a callback]

#         """
#         self.fire(*args)

#     def has(self, callback=None):
#         """ Determine whether or not the list has any callbacks attached.
#         If a callback is provided as an argument, determine whether it is in a list. """
#         if callback is None:
#             return bool(self.callbacks)
#         return callback in self.callbacks

#     def lock(self):
#         """ Lock a callback list in its current state. """
#         # TODO - test
#         raise NotImplementedError

#     def locked(self):
#         """ Determine whether or not the callback list is locked."""
#         return self.lock

#     def remove(self, callback):
#         """[Remove a callback or a collection of callbacks from a callback list.]

#         Args:
#             callback (function): [a callback]

#         """
#         if callback in self.callbacks:
#             del self.callbacks[callback]
#         else:
#             raise ValueError


# class Deferred():

#     def __init__(self):
#         pass

#     def always(self, *args):
#         """ Add handlers to be called when the Deferred object is either resolved or rejected."""
#         raise NotImplementedError

#     def catch(self, *args):
#         """ Add handlers to be called when the Deferred object is rejected. """
#         raise NotImplementedError

#     def done(self, *args):
#         """ Add handlers to be called when the Deferred object is resolved. """

#     def fail(self):
#         """ Add handlers to be called when the Deferred object is rejected."""
#         raise NotImplementedError

#     def isRejected(self):
#         """ Determine whether a Deferred object has been rejected."""
#         raise NotImplementedError

#     def isResolved(self):
#         """ Determine whether a Deferred object has been resolved."""
#         raise NotImplementedError

#     def notify(self):
#         """ Call the progressCallbacks on a Deferred object with the given args."""
#         raise NotImplementedError

#     def notifyWith(self):
#         """ Call the progressCallbacks on a Deferred object with the given context and args."""
#         raise NotImplementedError

#     def pipe(self):
#         """ Utility method to filter and/or chain Deferreds."""
#         raise NotImplementedError

#     def progress(self):
#         """ Add handlers to be called when the Deferred object generates progress notifications."""
#         raise NotImplementedError

#     def promise(self):
#         """ Return a Deferred’s Promise object."""
#         raise NotImplementedError

#     def reject(self):
#         """ Reject a Deferred object and call any failCallbacks with the given args."""
#         raise NotImplementedError

#     def rejectWith(self):
#         """ Reject a Deferred object and call any failCallbacks with the given context and args."""
#         raise NotImplementedError

#     def resolve(self):
#         """ Resolve a Deferred object and call any doneCallbacks with the given args."""
#         raise NotImplementedError

#     def resolveWith(self):
#         """ Resolve a Deferred object and call any doneCallbacks with the given context and args."""
#         raise NotImplementedError

#     def state(self):
#         """ Determine the current state of a Deferred object."""
#         raise NotImplementedError

#     def then(self):
#         """ Add handlers to be called when the Deferred object is resolved, rejected, or still in progress."""
#         raise NotImplementedError


# class Event():

#     def __init__(self):
#         self.currentTarget = None
#         self.data = None
#         self.delegateTarget = None
#         self.metaKey = None
#         self.namespace = None
#         self.pageX = None
#         self.pageY = None
#         self.relatedTarget = None
#         self.result = None
#         self.target = None
#         self.timeStamp = None
#         self.type = None
#         self.which = None

#     def isDefaultPrevented(self):
#         """ Returns whether event.preventDefault() was ever called on this event object."""
#         pass

#     def isImmediatePropagationStopped(self):
#         """ Returns whether event.stopImmediatePropagation() was ever called on this event object."""
#         pass

#     def isPropagationStopped(self):
#         """ Returns whether event.stopPropagation() was ever called on this event object."""
#         pass

#     def preventDefault(self):
#         """ If this method is called,
#           the default action of the event will not be triggered."""
#         pass

#     def stopImmediatePropagation(self):
#         """ Keeps the rest of the handlers from being executed and
#           prevents the event from bubbling up the DOM tree."""
#         pass

#     def stopPropagation(self):
#         """ Prevents the event from bubbling up the DOM tree, preventing any parent handlers
#           from being notified of the event."""
#         pass


def dproxy(q):
    el = dQuery_el(q)
    el.init(q)

    # if type(q) is not str:
    return el
    # else:
    #     return el.elements
    # def __str__(self):
    #     return self.elements


class º(dQuery_el):
    def __init__(self, selector=None, *args, **kwargs):
        super().__init__(selector, *args, **kwargs)
        self.init(selector)

    def __call__(self, *args, **kwargs):
        return dproxy(args[0])

    @staticmethod
    def ajax(
        url="/",
        type="GET",
        data=None,
        contentType=False,
        processData=False,
        cache=False,
        success=None,
        error=None,
    ):
        """make an ajax request"""
        try:
            # r = requests.get(url, timeout=3)
            from requests import Request, Session

            method = type

            # if "callback_function" in kwargs:
            #     del kwargs["callback_function"]

            # if "error_handler" in kwargs:
            #     del kwargs["error_handler"]

            # headers = {'Content-type': contentType}
            s = Session()
            req = Request(method, url, data=data)  # , headers=headers)
            prepped = s.prepare_request(req)
            # prepped.body = 'hello'
            # prepped.headers['Keep-Dead'] = 'parrot'
            r = s.send(prepped)  # , **kwargs)
            # resp = s.send(prepped,
            #     stream=stream,
            #     verify=verify,
            #     proxies=proxies,
            #     cert=cert,
            #     timeout=timeout
            # )
            # print(r.status_code)
            if r.status_code == 200:
                # print('sup')
                if success is not None:
                    success(r.text)
            else:
                # print('sup2')
                if error is not None:
                    error(r.text)
            s.close()

            return r

        except Exception as e:
            print(f"Request Failed for URL: {url}", e)
            return None

    @staticmethod
    def ajaxPrefilter():
        """Handle custom Ajax options or modify existing options before each request is sent
        and before they are processed by .ajax"""
        raise NotImplementedError

    @staticmethod
    def ajaxSetup():
        """Set default values for future Ajax requests. Its use is not recommended."""
        raise NotImplementedError

    @staticmethod
    def ajaxTransport():
        """Creates an object that handles the actual transmission of Ajax data."""
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
        """A multi-purpose callbacks list object that provides a powerful way to manage callback lists."""
        callbacks = []

        class _Callbacks:
            def add(self, callback):
                callbacks.append(callback)
                return self

            def fire(self, *args, **kwargs):
                for callback in list(callbacks):
                    callback(*args, **kwargs)
                return self

            def remove(self, callback):
                if callback in callbacks:
                    callbacks.remove(callback)
                return self

            def has(self, callback=None):
                if callback is None:
                    return bool(callbacks)
                return callback in callbacks

        return _Callbacks()

    @staticmethod
    def contains(parent, child):
        """Check to see if a DOM element is a descendant of another DOM element."""
        return parent.contains(child)

        # @staticmethod
        # @ty
        # def cssHooks:
        """ Hook directly into dQuery to override how particular CSS properties are retrieved or set,
        normalize CSS property naming, or create custom properties. """
        # raise NotImplementedError

        # @staticmethod
        # @ty
        # def cssNumber:
        """ An object containing all CSS properties that may be used without a unit.
        The .css method uses this object to see if it may append px to unitless values. """
        # raise NotImplementedError

    @staticmethod
    def data(element=None, key=None, value=None):
        """Store arbitrary data associated with the specified element and/or return the value that was set."""
        if element is None:
            return {}
        store = getattr(element, "_dquery_data", {}).copy()
        if key is None:
            return store
        if value is None:
            return store.get(key)
        store[key] = value
        setattr(element, "_dquery_data", store)
        return value

    @staticmethod
    def Deferred():
        """A factory function that returns a chainable utility object with methods to register multiple callbacks
        into callback queues, invoke callback queues, and relay the success or failure state of
        any synchronous or asynchronous function."""
        state = {"status": "pending", "value": None}
        done_callbacks = []
        fail_callbacks = []

        class _Deferred:
            def done(self, callback):
                done_callbacks.append(callback)
                if state["status"] == "resolved":
                    callback(state["value"])
                return self

            def fail(self, callback):
                fail_callbacks.append(callback)
                if state["status"] == "rejected":
                    callback(state["value"])
                return self

            def resolve(self, value=None):
                state["status"] = "resolved"
                state["value"] = value
                for callback in done_callbacks:
                    callback(value)
                return self

            def reject(self, value=None):
                state["status"] = "rejected"
                state["value"] = value
                for callback in fail_callbacks:
                    callback(value)
                return self

            def state(self):
                return state["status"]

        return _Deferred()

    @staticmethod
    def dequeue(element=None):
        """Execute the next function on the queue for the matched element."""
        if element is None:
            return None
        queue = getattr(element, "_dquery_queue", [])
        if not queue:
            return None
        item = queue.pop(0)
        setattr(element, "_dquery_queue", queue)
        if callable(item):
            return item()
        return item

    @staticmethod
    def each(arr, func):  # TODO - untested
        """A generic iterator function, which can be used to seamlessly iterate over both objects and arrays."""
        for i in arr:
            func(i)

    @staticmethod
    def error(msg):
        """Takes a string and throws an exception containing it."""
        raise Exception(msg)

    @staticmethod
    def escapeSelector(selector):  # TODO - untested
        """Returns a string with all special characters replaced with their respective character codes."""
        if type(selector) is str:
            selector = (
                selector.replace(" ", "\\s")
                .replace(".", "\\.")
                .replace("#", "\\#")
                .replace("[", "\\[")
                .replace("]", "\\]")
            )
            # selector = re.sub(r'([^\w\.-])', '\\\1', selector)
            return selector.replace(" ", "%20")
        else:
            return selector

    @staticmethod
    def extend(*args):
        """Merge the contents of two or more objects together into the first object."""
        result = {}
        for each in args:
            result.update(each)
        return result

    @staticmethod
    def get(url: str, data=None, dataType=False, success=None, error=None):
        """[simplified ajax request]

        Args:
            url (str): [the url to request]
            data ([type]): [the data to send]
            dataType (bool, optional): [the dataType]. Defaults to False.
            success ([type], optional): [a success function]. Defaults to None.
            error ([type], optional): [an error method]. Defaults to None.

        Returns:
            [type]: [the response]
        """
        # print("GO!")
        # r = requests.get(url)
        # return r.content.decode("utf-8")
        r = º.ajax(
            {
                "url": url,
                # 'data': data,
                # 'success': success,
                # 'dataType': dataType
            }
        )
        return r.content.decode("utf-8")

    @staticmethod
    def getJSON():
        """Load JSON-encoded data from the server using a GET HTTP request."""
        raise NotImplementedError

    @staticmethod
    def getScript(filename, *args):
        """execute another python file."""
        from subprocess import Popen

        Popen("python " + filename + ".py")

    @staticmethod  # TODO - test
    def globalEval(code):
        """Execute some python code globally."""
        return eval(code, globals(), locals())

    @staticmethod  # TODO - test
    def grep(arr, func):
        """Returns an array of elements from the original array which satisfy a filter function."""
        return list(filter(func, arr))

    @staticmethod
    def hasData(element):
        """Determine whether an element has any dQuery data associated with it."""
        return bool(getattr(element, "_dquery_data", {}))

    @staticmethod
    def holdReady():
        """Holds or releases the execution of dQuery’s ready event."""
        return True

    @staticmethod
    def htmlPrefilter(html=""):
        """Modify and filter HTML strings passed through dQuery manipulation methods."""
        return html

    @staticmethod
    def inArray(thing, arr):
        """Search for a specified value within an array and return its index or -1 if not found."""
        for count, each in enumerate(arr):
            if thing == each:
                return count
        return -1

    @staticmethod
    def isArray(item):
        """Determine whether the argument is an array."""
        return type(item) == Array

    @staticmethod
    def isEmptyObject(dct):
        """Check to see if an object is empty (contains no enumerable properties)."""
        return not bool(dct)

    @staticmethod
    def isFunction(obj):
        """Determines if its argument is callable as a function."""
        return callable(obj)

    @staticmethod
    def isNumeric(thing):
        """Determine whether the argument is numeric."""
        return type(thing) in (int, float, Number)

    @staticmethod
    def isPlainObject(obj):
        """Check to see if an object is a plain object created using '{}'"""
        return type(obj) is dict

    @staticmethod
    def isWindow(obj):
        """Determine whether the argument is a window object."""
        return type(obj) is Window

    @staticmethod
    def isXMLDoc(obj):
        """Check to see if a DOM node is within an XML document (or is an XML document)."""
        obj = str(obj)
        return obj.startswith("<") and obj.endswith(">")

    @staticmethod
    def makeArray(somelist):
        """Convert an array-like object into a true JavaScript array."""
        return Array(somelist)

    @staticmethod
    def map(arr, func):
        """Translate all items in an array or object to new array of items."""
        return [func(value) for value in arr]

    @staticmethod
    def merge(one, *args):
        """Merge the contents of arrays into the first array."""
        for each in args:
            one.extend(list(each))
        return one

    @staticmethod
    def noConflict():
        """Relinquish dQuery’s control of the º variable."""
        return dQuery

    @staticmethod
    def noop():
        """An empty function."""
        pass

    @staticmethod
    def now():
        """Return a number representing the current time."""
        return Date.now()

    @staticmethod
    def param(obj):
        """Create a serialized representation of an array, a plain object,
        or a dQuery object suitable for use in a URL query string or Ajax request.
        In case a dQuery object is passed, it should contain input elements with name/value properties.
        """
        if isinstance(obj, list):
            return json.dumps(obj)
        elif isinstance(obj, dict):
            return json.dumps(obj)
        elif isinstance(obj, dQuery):
            return json.dumps(obj.inputs)
        else:
            raise TypeError(obj)

    @staticmethod
    def parseHTML(string):
        """Parses a string into an array of DOM nodes."""
        # from bs4 import BeautifulSoup
        # return BeautifulSoup(string, 'html.parser')
        # return BeautifulSoup(string, 'html5lib')
        # return BeautifulSoup(string, 'lxml')
        # return domonic.domonic.parseString(string, 'domonic')
        # return domonic.domonic.parseString(string, 'expat')
        return domonic.domonic.parseString(string)

    @staticmethod
    def parseJSON(string: str):
        """Takes a well-formed JSON string and returns the resulting JavaScript value."""
        return json.loads(string)

    @staticmethod
    def parseXML(string: str):
        """Parses an XMLstring into a pyml"""
        from domonic.domonic import parseString

        return parseString(string)

    @staticmethod
    def post(url, data, success):
        """Send data to the server using a HTTP POST request."""
        r = requests.post(url, data)
        # if r.ok:
        #     succss()
        return r.content.decode("utf-8")

    @staticmethod
    def proxy(func):
        """Takes a function and returns a new one that will always have a particular context."""
        return func

    @staticmethod
    def queue(func):
        """Show or manipulate the queue of functions to be executed on the matched element."""
        raise NotImplementedError

    # @staticmethod
    # @ty
    # def ready:
    # """ A Promise-like object or “thenable” that resolves when the document is ready. """
    # raise NotImplementedError

    @staticmethod
    def readyException():
        """Handles errors thrown synchronously in functions wrapped in dQuery"""
        raise NotImplementedError

    @staticmethod
    def removeData(element=None, key=None):
        """Remove a previously-stored piece of data."""
        if element is None:
            return None
        store = getattr(element, "_dquery_data", {}).copy()
        if key is None:
            store = {}
        else:
            store.pop(key, None)
        setattr(element, "_dquery_data", store)
        return element

    # @staticmethod
    #  @ty
    # def speed:
    # """ Creates an object containing a set of properties ready to be used in the definition
    # of custom animations. """
    # raise NotImplementedError

    @staticmethod
    def sub():
        """Creates a new copy of dQuery whose properties and methods can be modified without affecting
        the original dQuery object."""
        raise NotImplementedError

    # @staticmethod
    # def t:
    #     """ A collection of properties that represent the presence of different browser features or bugs. """
    #     raise NotImplementedError

    @staticmethod
    def trim(content: str) -> str:
        """Remove the whitespace from the beginning and end of a string."""
        content = content.replace("\n", "").replace("\t", "").replace("\r", "").strip()
        return content

    # @staticmethod
    # def type():
    #     """ Determine the internal JavaScript [[Class]] of an object. """
    #     raise NotImplementedError

    @staticmethod
    def unique(arr):  # TODO - test
        """[removes duplicate elements.]

        Args:
            arr ([type]): [list of elements]

        Returns:
            [type]: [a sorted array without duplicates]
        """
        return list(set(arr))

    @staticmethod
    def uniqueSort(arr):  # TODO - test
        """Sorts an array of DOM elements, in place, with the duplicates removed.
        Note that this only works on arrays of DOM elements, not strings or numbers."""
        arr.sort()
        arr = list(set(arr))
        arr.sort()
        return arr

    @staticmethod
    def when():
        """Provides a way to execute callback functions based on zero or more Thenable objects,
        usually Deferred objects that represent asynchronous events."""
        deferred = º.Deferred()
        deferred.resolve(None)
        return deferred

    # Python does not support separate static and instance methods with the same name,
    # so these adapters keep the jQuery-like surface usable in both styles.
    def data(self, key=None, value=None):
        if isinstance(self, dQuery_el):
            return dQuery_el.data(self, key, value)
        element = self
        store = getattr(element, "_dquery_data", {}).copy()
        if key is None:
            return store
        if value is None:
            return store.get(key)
        store[key] = value
        setattr(element, "_dquery_data", store)
        return value

    def dequeue(self):
        if isinstance(self, dQuery_el):
            return dQuery_el.dequeue(self)
        queue = getattr(self, "_dquery_queue", [])
        if not queue:
            return None
        item = queue.pop(0)
        setattr(self, "_dquery_queue", queue)
        if callable(item):
            return item()
        return item

    def queue(self, func=None):
        if isinstance(self, dQuery_el):
            elements = self._ensure_list()
            if func is not None:
                for el in elements:
                    queue = getattr(el, "_dquery_queue", [])
                    queue.append(func)
                    setattr(el, "_dquery_queue", queue)
                return self
            queues = [getattr(el, "_dquery_queue", []) for el in elements]
            return queues[0] if len(queues) == 1 else queues
        queue = getattr(self, "_dquery_queue", [])
        if func is not None:
            queue.append(func)
            setattr(self, "_dquery_queue", queue)
        return queue

    def removeData(self, key=None):
        if isinstance(self, dQuery_el):
            return dQuery_el.removeData(self, key)
        store = getattr(self, "_dquery_data", {}).copy()
        if key is None:
            store = {}
        else:
            store.pop(key, None)
        setattr(self, "_dquery_data", store)
        return self


dQuery = º
