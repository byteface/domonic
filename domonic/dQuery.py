"""
domonic.dQuery
===================================
alt + 0

"""

import copy
import functools
import json
import re
import sys
import time

from domonic.dom import *
from domonic.events import (
    CustomEvent,
    Event,
    FocusEvent,
    InputEvent,
    KeyboardEvent,
    MouseEvent,
    SubmitEvent,
)
from domonic.html import *
from domonic.javascript import *


_UNSET = object()

_MOUSE_EVENTS = {
    "click",
    "contextmenu",
    "dblclick",
    "mousedown",
    "mouseenter",
    "mouseleave",
    "mousemove",
    "mouseout",
    "mouseover",
    "mouseup",
}
_KEYBOARD_EVENTS = {"keydown", "keypress", "keyup"}
_FOCUS_EVENTS = {"blur", "focus", "focusin", "focusout"}
_INPUT_EVENTS = {"beforeinput", "input"}
_AJAX_EVENTS = (
    "ajaxStart",
    "ajaxSend",
    "ajaxSuccess",
    "ajaxError",
    "ajaxComplete",
    "ajaxStop",
)


def _split_event_name(event_name):
    event_name = str(event_name or "").strip()
    if "." not in event_name:
        return event_name, None
    event_type, namespace = event_name.split(".", 1)
    return event_type, namespace or None


def _event_names(events):
    if events is None:
        return []
    if isinstance(events, str):
        return [event for event in events.split() if event]
    return [str(event) for event in events]


class EventHandler:
    def __init__(self):
        self.events = []

    def bindEvent(
        self,
        event: str,
        callback,
        targetElement,
        original=None,
        selector=None,
        data=None,
        options=None,
    ):
        """[binds an event to a callback]

        Args:
            event ([str]): [type of event]
            callback (function): [callback function]
            targetElement ([type]): [target element]
        """
        event_type, namespace = _split_event_name(event)
        if not event_type:
            return
        targetElement.addEventListener(event_type, callback, options or False)
        registered = {
            "_type": event_type,
            "namespace": namespace,
            "event": callback,
            "original": original or callback,
            "selector": selector,
            "data": data,
            "target": targetElement,
        }
        self.events.append(registered)
        element_events = getattr(targetElement, "_dquery_events", [])
        element_events.append(registered)
        setattr(targetElement, "_dquery_events", element_events)

    def findEvent(self, event):
        """[finds an event]

        Args:
            event ([str]): [event]

        Returns:
            [type]: [event]
        """
        event_type, namespace = _split_event_name(event)
        for registered in self.events:
            if registered["_type"] == event_type and (
                namespace is None or registered["namespace"] == namespace
            ):
                return registered
        return None

    def unbindEvent(self, event=None, targetElement=None, callback=None):
        """[unbinds an event]

        Args:
            event ([str]): [event]
            targetElement ([type]): [description]
        """
        event_type, namespace = _split_event_name(event) if event else (None, None)
        source = (
            list(getattr(targetElement, "_dquery_events", []))
            if targetElement is not None
            else list(self.events)
        )
        remaining_for_target = []

        for registered in source:
            type_matches = event_type in (None, "") or registered["_type"] == event_type
            namespace_matches = (
                namespace is None or registered["namespace"] == namespace
            )
            callback_matches = callback is None or callback in (
                registered["event"],
                registered["original"],
            )
            target_matches = (
                targetElement is None or registered["target"] == targetElement
            )

            if type_matches and namespace_matches and callback_matches and target_matches:
                registered["target"].removeEventListener(
                    registered["_type"], registered["event"]
                )
            else:
                remaining_for_target.append(registered)

        if targetElement is not None:
            setattr(targetElement, "_dquery_events", remaining_for_target)

        self.events = [
            registered
            for registered in self.events
            if registered in remaining_for_target
            or (
                targetElement is not None
                and registered.get("target") is not targetElement
            )
        ]


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
        if dom in (None, 0):
            return
        if isinstance(dom, (html, Document)):
            dQuery_el.DOM = dom
            self.dom = dom
        else:
            self.elements = dom

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
    def _call_with_fallback(func, *attempts):
        last_error = None
        for args in attempts:
            try:
                return func(*args)
            except TypeError as error:
                last_error = error
        if last_error is not None:
            raise last_error

    @staticmethod
    def _match_selector(element, selector, index=None):
        if selector is None:
            return True
        if callable(selector):
            return bool(
                dQuery_el._call_with_fallback(
                    selector, (index, element), (element,), (index,)
                )
            )
        if isinstance(selector, dQuery_el):
            return element in selector.toArray()
        if isinstance(selector, (list, tuple, set)):
            return element in selector
        if isinstance(selector, str):
            selector = selector.strip()
            if not selector:
                return False
            if hasattr(element, "matches"):
                try:
                    return bool(element.matches(selector))
                except Exception:
                    pass
            if selector.startswith("#"):
                return element.getAttribute("id") == selector[1:]
            if selector.startswith("."):
                classes = (element.getAttribute("class") or "").split()
                return all(token in classes for token in selector.split(".") if token)
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

    @staticmethod
    def _class_tokens(value, element=None, index=0):
        if value is None:
            return []
        if callable(value):
            current = element.getAttribute("class") if element is not None else ""
            value = dQuery_el._call_with_fallback(
                value, (index, current or ""), (index,), (element,)
            )
        if isinstance(value, (list, tuple, set)):
            tokens = []
            for item in value:
                tokens.extend(dQuery_el._class_tokens(item, element, index))
            return tokens
        return [token for token in str(value).split() if token]

    @staticmethod
    def _data_attribute_name(key):
        key = re.sub(r"([A-Z])", lambda match: "-" + match.group(1).lower(), str(key))
        return "data-" + key.replace("_", "-")

    @staticmethod
    def _coerce_data_value(value):
        if value in ("true", "false"):
            return value == "true"
        if value == "null":
            return None
        if isinstance(value, str):
            try:
                return json.loads(value)
            except Exception:
                return value
        return value

    @staticmethod
    def _content_nodes(value):
        if isinstance(value, dQuery_el):
            return value.toArray()
        if isinstance(value, (list, tuple)):
            nodes = []
            for item in value:
                nodes.extend(dQuery_el._content_nodes(item))
            return nodes
        if isinstance(value, str) and value.lstrip().startswith("<"):
            from domonic import domonic

            loaded = domonic.load(value)
            return dQuery_el._coerce_nodes(loaded)
        return [value]

    @staticmethod
    def _copy_for_target(node, target_index):
        if target_index == 0:
            return node
        if isinstance(node, Node):
            return copy.deepcopy(node)
        return node

    @staticmethod
    def _new(elements=None, prev=None):
        dq = object.__new__(º)
        dQuery_el.__init__(dq, "")
        dq.elements = [] if elements is None else elements
        dq.prevObject = list(prev or [])
        return dq

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
    def _event_object(event_name, event_arg=None, *, bubbles=True):
        if isinstance(event_name, Event):
            return event_name

        event_type, _namespace = _split_event_name(event_name)
        options = {"bubbles": bubbles, "cancelable": True}
        if isinstance(event_arg, dict):
            options.update(event_arg)
        elif event_arg is not None:
            options["detail"] = event_arg

        if event_type in _MOUSE_EVENTS:
            return MouseEvent(event_type, options)
        if event_type in _KEYBOARD_EVENTS:
            return KeyboardEvent(event_type, options)
        if event_type in _FOCUS_EVENTS:
            return FocusEvent(event_type, options)
        if event_type in _INPUT_EVENTS:
            return InputEvent(event_type, options)
        if event_type == "submit":
            return SubmitEvent(event_type, options)
        if "detail" in options:
            return CustomEvent(event_type, options)
        return Event(event_type, options)

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
        for index, el in enumerate(self._ensure_list()):
            tokens = self._class_tokens(name, el, index)
            if tokens and hasattr(el, "classList"):
                el.classList.add(*tokens)
        return self

    def after(self, newnode):
        """Insert content, specified by the parameter, after each element in the set of matched elements."""
        for target_index, el in enumerate(self._ensure_list()):
            p = el.parentNode
            if p is None:
                continue
            siblings = list(p.args)
            try:
                insertion_index = siblings.index(el) + 1
            except ValueError:
                continue
            items = [
                self._copy_for_target(item, target_index)
                for item in self._content_nodes(newnode)
            ]
            p.args = tuple(siblings[:insertion_index] + items + siblings[insertion_index:])
            p._update_parents()
        return self

    def ajaxComplete(self, handler):
        """Register a handler to be called when Ajax requests complete. This is an Ajax Event"""
        return º._add_ajax_handler("ajaxComplete", handler, self)

    def ajaxError(self, handler):
        """Register a handler to be called when Ajax requests complete with an error. This is an Ajax Event"""
        return º._add_ajax_handler("ajaxError", handler, self)

    def ajaxSend(self, handler):
        """Register a handler to be called when Ajax requests complete successfully. This is an Ajax Event"""
        return º._add_ajax_handler("ajaxSend", handler, self)

    def ajaxStart(self, handler):
        """Register a handler to be called when the first Ajax request begins. This is an Ajax Event"""
        return º._add_ajax_handler("ajaxStart", handler, self)

    def ajaxStop(self, handler):
        """Register a handler to be called when all Ajax requests have completed. This is an Ajax Event"""
        return º._add_ajax_handler("ajaxStop", handler, self)

    def ajaxSuccess(self, handler):
        """Attach a function to be executed whenever an Ajax request completes successfully. This is an Ajax Event."""
        return º._add_ajax_handler("ajaxSuccess", handler, self)

    def andSelf(self):
        """Add the previous set of elements on the stack to the current set."""
        return self.addBack(None)

    def animate(self):
        """Perform a custom animation of a set of CSS properties."""
        raise NotImplementedError

    def append(self, html):
        """Insert content, specified by the parameter, to the end of each element in the set of matched elements."""
        for target_index, el in enumerate(self._ensure_list()):
            for item in self._content_nodes(html):
                if isinstance(item, str) and item.lstrip().startswith("<"):
                    el.innerHTML = el.innerHTML + item
                elif isinstance(item, Node):
                    el.append(self._copy_for_target(item, target_index))
                else:
                    el.innerHTML = el.innerHTML + str(item)
        return self

    def appendTo(self, target):
        """Insert every element in the set of matched elements to the end of the target."""
        target = º(target) if isinstance(target, str) else target
        targets = target.toArray() if isinstance(target, dQuery_el) else self._coerce_nodes(target)
        for target_index, el in enumerate(targets):
            for item in self._ensure_list():
                el.append(self._copy_for_target(item, target_index))
        return self

    def attr(self, property, value=_UNSET):
        """Get the value of an attribute for the first element in the set of matched elements
        or set one or more attributes for every matched element."""

        if isinstance(property, dict):
            for key, attr_value in property.items():
                self.attr(key, attr_value)
            return self
        if value is not _UNSET:
            for el in self._ensure_list():
                if value is None:
                    el.removeAttribute(property)
                else:
                    el.setAttribute(property, value)
            return self
        elements = self._ensure_list()
        return elements[0].getAttribute(property) if elements else None

    def before(self, content):  # TODO - test
        """Insert content, specified by the parameter, before each element in the set of matched elements."""
        for target_index, el in enumerate(self._ensure_list()):
            p = el.parentNode
            if p is None:
                continue
            siblings = list(p.args)
            try:
                insertion_index = siblings.index(el)
            except ValueError:
                continue
            items = [
                self._copy_for_target(item, target_index)
                for item in self._content_nodes(content)
            ]
            p.args = tuple(siblings[:insertion_index] + items + siblings[insertion_index:])
            p._update_parents()
        return self

    def bind(self, event, handler):  # TODO - untested
        """Attach a function to be executed when an event occurs on a set of matched elements."""
        return self.on(event, handler)

    def blur(self, handler=None):  # TODO - untested
        """Bind an event handler to the “blur” JavaScript event, or trigger that event on an element."""
        return self._simple_event("blur", handler)

    def change(self, handler=None):
        """Bind an event handler to the “change” JavaScript event, or trigger that event on an element."""
        return self._simple_event("change", handler)

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
        return self._simple_event("click", handler)

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

    def css(self, property, value=_UNSET):  # TODO - untested
        """Get the value of a computed style property for the first element in the set of matched elements
        or set one or more CSS properties for every matched element."""
        if isinstance(property, dict):
            for key, css_value in property.items():
                self.css(key, css_value)
            return self
        elements = self._ensure_list()
        if value is not _UNSET:
            for el in elements:
                el.style.setProperty(property, value)
            return self
        return elements[0].style.getProperty(property) if elements else None

    def data(self, key=_UNSET, value=_UNSET):
        """Store arbitrary data associated with the matched elements or return the value at the named data store
        for the first element in the set of matched elements."""
        elements = self._ensure_list()
        if not elements:
            return None if key is not _UNSET else {}
        if key is _UNSET:
            store = getattr(elements[0], "_dquery_data", {}).copy()
            for attr in elements[0].attributes:
                if attr.name.startswith("data-"):
                    data_key = re.sub(
                        r"-([a-z])",
                        lambda match: match.group(1).upper(),
                        attr.name[5:],
                    )
                    store.setdefault(data_key, self._coerce_data_value(attr.value))
            return store
        if isinstance(key, dict):
            for data_key, data_value in key.items():
                self.data(data_key, data_value)
            return self
        if value is _UNSET:
            store = getattr(elements[0], "_dquery_data", {})
            if key in store:
                return store.get(key)
            attr_value = elements[0].getAttribute(self._data_attribute_name(key))
            return self._coerce_data_value(attr_value) if attr_value is not None else None
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
        return self.on(event, selector, handler)

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
            if p is not None:
                p.removeChild(el)
                detached.append(el)
        self.elements = detached
        return self

    def die(self):
        """Remove event handlers previously attached using .live from the elements."""
        return self.unbind()

    def each(self, func):
        """Iterate over a dQuery object, executing a function for each matched element."""
        for index, value in enumerate(self._ensure_list()):
            self._call_with_fallback(func, (index, value), (value,), (index,))
        return self

    # @_listify
    def empty(self):
        """Remove all child nodes of the set of matched elements from the DOM."""
        for el in self._ensure_list():
            if hasattr(el, "replaceChildren"):
                el.replaceChildren()
            else:
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
        elements = self._ensure_list()
        try:
            selected = [elements[index]]
        except IndexError:
            selected = []
        return self._new(selected, prev=elements)

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
            el
            for index, el in enumerate(self._ensure_list())
            if self._match_selector(el, selector, index)
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
        return self.eq(0)

    def focus(self, handler=None):
        """Bind an event handler to the “focus” JavaScript event, or trigger that event on an element."""
        return self._simple_event("focus", handler)

    def focusin(self, handler=None):
        """Bind an event handler to the “focusin” event."""
        return self._simple_event("focusin", handler)

    def focusout(self, handler=None):
        """Bind an event handler to the “focusout” JavaScript event."""
        return self._simple_event("focusout", handler)

    # def get(self):
    #     """ Retrieve the DOM elements matched by the dQuery object."""
    #     raise NotImplementedError

    def has(self, selector):  # TODO - test
        """Reduce the set of matched elements to those that have a descendant
        that matches the selector or DOM element."""
        matched = []
        for index, el in enumerate(self._ensure_list()):
            descendants = (
                el.querySelectorAll(selector)
                if isinstance(selector, str)
                else el.getElementsByTagName("*")
            )
            descendants = (
                descendants if isinstance(descendants, (list, tuple)) else [descendants]
            )
            if any(
                self._match_selector(child, selector, index)
                for child in descendants
                if child is not None
            ):
                matched.append(el)
        self.elements = matched
        return self

    def hasClass(self, classname):
        """Determine whether any of the matched elements are assigned the given class."""
        tokens = self._class_tokens(classname)
        if not tokens:
            return False
        return any(all(token in el.classList for token in tokens) for el in self._ensure_list())

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
            return elements[0].innerHTML if elements else None
        for el in elements:
            el.innerHTML = str(html)
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

    def get(self, index=None):
        """Retrieve the DOM elements matched by the dQuery object."""
        elements = self._ensure_list()
        if index is None:
            return elements
        try:
            return elements[index]
        except IndexError:
            return None

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

    def is_(self, selector):
        """ Check the current matched set of elements against a selector, element,
        or dQuery object and return true if at least one of these elements matches the given arguments."""
        return any(
            self._match_selector(el, selector, index)
            for index, el in enumerate(self._ensure_list())
        )

    def beforeinput(self, handler=None):
        """Bind an event handler to the “beforeinput” event, or trigger that event on an element."""
        return self._simple_event("beforeinput", handler)

    def input(self, handler=None):
        """Bind an event handler to the “input” event, or trigger that event on an element."""
        return self._simple_event("input", handler)

    def keydown(self, handler=None):
        """Bind an event handler to the “keydown” JavaScript event, or trigger that event on an element."""
        return self._simple_event("keydown", handler)

    def keypress(self, handler=None):
        """Bind an event handler to the “keypress” JavaScript event, or trigger that event on an element."""
        return self._simple_event("keypress", handler)

    def keyup(self, handler=None):
        """Bind an event handler to the “keyup” JavaScript event, or trigger that event on an element."""
        return self._simple_event("keyup", handler)

    def last(self):
        """Reduce the set of matched elements to the final one in the set."""
        return self.eq(-1)

    @property
    def length(self):
        """The number of elements in the dQuery object."""
        return len(self._coerce_nodes(self.elements)) if self.elements is not None else 0

    def live(self):
        """Attach an event handler for all elements which match the current selector, now and in the future."""
        raise NotImplementedError

    def load(self, url, data=None, complete=None):  # TODO - test
        """Load data from the server and place the returned HTML into the matched elements."""
        if callable(data) and complete is None:
            complete = data
            data = None

        for el in self._ensure_list():
            el.innerHTML = ""
            el.innerHTML = "<div class='loading'></div>"

            def load(el, url, data, complete):
                def onload(response, text_status="success", jqxhr=None):
                    el.innerHTML = ""
                    el.innerHTML = response
                    if complete is not None:
                        dQuery_el._call_with_fallback(
                            complete,
                            (response, text_status, jqxhr),
                            (response, text_status),
                            (response,),
                            (),
                        )

                dQuery.ajax(
                    {
                        "url": url,
                        "type": "POST" if data is not None else "GET",
                        "data": data,
                        "dataType": "html",
                        "success": onload,
                    }
                )

            load(el, url, data, complete)
        return self

    def map(self, func):  # TODO - test
        """Pass each element in the current matched set through a function,
        producing a new dQuery object containing the return values."""
        results = [
            self._call_with_fallback(func, (index, value), (value,), (index,))
            for index, value in enumerate(self._ensure_list())
        ]
        return self._new(results, prev=self._ensure_list())

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

    def not_(self, selector):
        """ Remove elements from the set of matched elements."""
        self.elements = [
            el
            for index, el in enumerate(self._ensure_list())
            if not self._match_selector(el, selector, index)
        ]
        return self

    def odd(self):  # TODO - untested
        """Reduce the set of matched elements to the odd ones in the set, numbered from zero."""
        self.elements = [
            el for index, el in enumerate(self._ensure_list()) if index % 2 == 1
        ]
        return self

    def off(self, event=None, callback=None):
        """Remove an event handler."""
        for el in self._ensure_list():
            for event_name in _event_names(event) or [None]:
                self.eventHandler.unbindEvent(event_name, el, callback)
        return self

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

    def on(self, event, selector=None, data=None, callback=None):
        """Attach an event handler function for one or more events to the selected elements."""
        if isinstance(event, dict):
            for event_name, handler in event.items():
                self.on(event_name, selector, data, handler)
            return self

        if callback is None and callable(data):
            callback = data
            data = None
        if callback is None and callable(selector):
            callback = selector
            selector = None
            data = None
        if callback is None:
            return self

        for el in self._ensure_list():
            for event_name in _event_names(event):
                if selector is None:

                    def listener(evt, _handler=callback, _data=data):
                        if _data is not None:
                            evt.data = _data
                        return _handler(evt)

                    self.eventHandler.bindEvent(
                        event_name, listener, el, original=callback, data=data
                    )
                    continue

                def delegated(
                    evt,
                    _root=el,
                    _selector=selector,
                    _handler=callback,
                    _data=data,
                ):
                    target = getattr(evt, "target", None)
                    current = target
                    while current is not None:
                        if self._match_selector(current, _selector):
                            evt.delegateTarget = _root
                            evt.currentTarget = current
                            if _data is not None:
                                evt.data = _data
                            return _handler(evt)
                        if current is _root:
                            break
                        current = getattr(current, "parentNode", None)
                    return None

                self.eventHandler.bindEvent(
                    event_name,
                    delegated,
                    el,
                    original=callback,
                    selector=selector,
                    data=data,
                )
        return self

    def one(self, event, callback):
        """Attach a handler to an event for the elements.
        The handler is executed at most once per element per event type."""
        for el in self._ensure_list():
            for event_name in _event_names(event):

                @functools.wraps(callback)
                def wrapper(evt, _callback=callback):
                    return _callback(evt)

                self.eventHandler.bindEvent(
                    event_name,
                    wrapper,
                    el,
                    original=callback,
                    options={"once": True},
                )
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
        for target_index, el in enumerate(self._ensure_list()):
            items = [
                self._copy_for_target(item, target_index)
                for item in self._content_nodes(html)
            ]
            if all(isinstance(item, Node) for item in items):
                el.prepend(*items)
            else:
                el.innerHTML = "".join(str(item) for item in items) + el.innerHTML
        return self

    def prependTo(self, target):  # TODO - test
        """Insert every element in the set of matched elements to the beginning of the target."""
        target = º(target) if isinstance(target, str) else target
        targets = target.toArray() if isinstance(target, dQuery_el) else self._coerce_nodes(target)
        for target_index, el in enumerate(targets):
            items = [
                self._copy_for_target(item, target_index)
                for item in self._ensure_list()
            ]
            el.prepend(*items)
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

    def prop(self, property, value=_UNSET):
        """Get the value of a property for the first element in the set of matched elements or set one or more properties
        for every matched element."""
        if isinstance(property, dict):
            for key, prop_value in property.items():
                self.prop(key, prop_value)
            return self
        elements = self._ensure_list()
        if value is not _UNSET:
            for el in elements:
                setattr(el, property, value)
            return self
        if not elements:
            return None
        return getattr(elements[0], property, elements[0].getAttribute(property))

    def pushStack(self, stack):  # TODO - test
        """Add a collection of DOM elements onto the dQuery."""
        return self._new(self._coerce_nodes(stack), prev=self._ensure_list())

    def queue(self):
        """Show or manipulate the queue of functions to be executed on the matched elements."""
        queues = [getattr(el, "_dquery_queue", []) for el in self._ensure_list()]
        return queues[0] if len(queues) == 1 else queues

    def ready(self, callback):
        """Specify a function to execute when the DOM is fully loaded."""
        callback()
        return self

    def remove(self, selector=None):  # TODO - test
        """Remove the set of matched elements from the DOM."""
        for index, el in enumerate(list(self._ensure_list())):
            if not self._match_selector(el, selector, index):
                continue
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

    def removeClass(self, classname=None):
        """Remove a single class, multiple classes, or all classes from each element in the set of matched elements."""

        for index, el in enumerate(self._ensure_list()):
            if classname is None:
                el.removeAttribute("class")
                continue
            tokens = self._class_tokens(classname, el, index)
            if tokens and hasattr(el, "classList"):
                el.classList.remove(*tokens)
            if not str(el.getAttribute("class") or "").strip():
                el.removeAttribute("class")
        return self

    def removeData(self, name=_UNSET):
        """Remove a previously-stored piece of data."""
        for el in self._ensure_list():
            store = getattr(el, "_dquery_data", {}).copy()
            if name is _UNSET:
                store = {}
            else:
                for key in str(name).split():
                    store.pop(key, None)
            setattr(el, "_dquery_data", store)
        return self

    def removeProp(self, prop: str):  # TODO -
        """Remove a property for the set of matched elements."""
        for el in self._ensure_list():
            if hasattr(el, prop):
                try:
                    delattr(el, prop)
                    continue
                except Exception:
                    pass
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
        old_elements = []
        for target_index, el in enumerate(self._ensure_list()):
            old_elements.append(el)
            if el.parentNode is None:
                continue
            items = self._content_nodes(replacement)
            if not items:
                continue
            el.parentNode.replaceChild(self._copy_for_target(items[0], target_index), el)
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

    def _serializable_controls(self):
        controls = []
        for el in self._ensure_list():
            if getattr(el, "nodeName", "").upper() == "FORM":
                controls.extend(list(getattr(el, "elements", [])))
            else:
                controls.append(el)
        return controls

    @staticmethod
    def _control_values(el):
        name = el.getAttribute("name") if hasattr(el, "getAttribute") else None
        if name in (None, ""):
            return []
        if getattr(el, "disabled", False) or (
            hasattr(el, "hasAttribute") and el.hasAttribute("disabled")
        ):
            return []

        node_name = getattr(el, "nodeName", "").upper()
        input_type = str(getattr(el, "type", "") or "").lower()
        if node_name == "INPUT" and input_type in {"submit", "button", "image", "reset", "file"}:
            return []
        if node_name == "BUTTON":
            return []
        if input_type in {"checkbox", "radio"} and not getattr(el, "checked", False):
            return []

        if node_name == "SELECT":
            values = []
            options = list(el.getElementsByTagName("option"))
            selected_options = [
                option for option in options if option.getAttribute("selected") is not None
            ]
            if el.getAttribute("multiple") is None and not selected_options and options:
                selected_options = [options[0]]
            for option in selected_options:
                value = option.getAttribute("value")
                values.append(option.textContent if value is None else value)
            return [(name, value) for value in values]

        value = getattr(el, "value", None)
        if value is None:
            value = el.nodeValue if getattr(el, "nodeValue", None) is not None else ""
        return [(name, value)]

    def serialize(self):
        """Encode a set of form elements as a string for submission."""
        q = []
        for el in self._serializable_controls():
            for name, value in self._control_values(el):
                q.append(
                    Global.encodeURIComponent(name)
                    + "="
                    + Global.encodeURIComponent(value)
                )

        return "&".join(q)

    def serializeArray(self, array=None):
        """Encode an array of form elements as a string for submission."""
        serialized = []
        for el in self._serializable_controls():
            for name, value in self._control_values(el):
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
        return self.length

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

    def submit(self, handler=None):
        """Bind an event handler to the “submit” JavaScript event, or trigger that event on an element."""
        return self._simple_event("submit", handler)

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
    def toggleClass(self, className, state=None):
        """
        Add or remove one or more classes from each element in the set of matched elements
        """
        for index, el in enumerate(self._ensure_list()):
            for token in self._class_tokens(className, el, index):
                el.classList.toggle(token, state)
            if not str(el.getAttribute("class") or "").strip():
                el.removeAttribute("class")
        return self

    def trigger(self, eventName, eventArg=None):  # TODO - test
        """Execute all handlers and behaviors attached to the matched elements for the given event type."""
        for el in self._ensure_list():
            el.dispatchEvent(self._event_object(eventName, eventArg))
        return self

    def triggerHandler(self, eventName, eventArg=None):
        """Execute all handlers attached to an element for an event."""
        elements = self._ensure_list()
        if not elements:
            return None
        event = self._event_object(eventName, eventArg, bubbles=False)
        elements[0].dispatchEvent(event)
        return event

    def unbind(self, event=None):
        """Remove a previously-attached event handler from the elements."""
        for el in self._ensure_list():
            if event is None:
                self.eventHandler.unbindEvent(None, el)
            else:
                for event_name in _event_names(event):
                    self.eventHandler.unbindEvent(event_name, el)
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
                if hasattr(el, "setValue"):
                    el.setValue(newVal, dispatch_events=False)
                else:
                    el.value = newVal
            return self
        else:
            return getattr(elements[0], "value", None) if elements else None

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
            return self.trigger(name)
        else:
            return self.on(name, handler)


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
    ajaxSettings = {
        "timeout": 30,
        "headers": {},
        "processData": True,
        "cache": True,
        "global": True,
    }
    _ajax_event_handlers = {event: [] for event in _AJAX_EVENTS}
    _ajax_prefilters = []
    _ajax_active = 0

    def __init__(self, selector=None, *args, **kwargs):
        super().__init__(selector, *args, **kwargs)
        self.init(selector)

    def __call__(self, *args, **kwargs):
        return dproxy(args[0])

    @staticmethod
    def _add_ajax_handler(event_name, handler, collection=None):
        if handler is not None:
            º._ajax_event_handlers.setdefault(event_name, []).append(handler)
        return collection if collection is not None else handler

    @staticmethod
    def _ajax_event_adapter(self_or_handler, handler, event_name):
        if isinstance(self_or_handler, dQuery_el):
            return º._add_ajax_handler(event_name, handler, self_or_handler)
        return º._add_ajax_handler(event_name, self_or_handler)

    @staticmethod
    def _callback(callback, *args):
        if callback is None:
            return None
        attempts = [args]
        for length in range(len(args) - 1, -1, -1):
            attempts.append(args[:length])
        return dQuery_el._call_with_fallback(callback, *attempts)

    @staticmethod
    def _ajax_error_callback(callback, response, text_status, thrown):
        if callback is None:
            return None
        return dQuery_el._call_with_fallback(
            callback,
            (response, text_status, thrown),
            (thrown,),
            (response,),
            (),
        )

    @staticmethod
    def _trigger_ajax_event(event_name, *args):
        event = Event(event_name)
        for handler in list(º._ajax_event_handlers.get(event_name, [])):
            º._callback(handler, event, *args)

    @staticmethod
    def _ajax_success_status(response):
        return 200 <= response.status_code < 300 or response.status_code == 304

    @staticmethod
    def _parse_ajax_response(response, dataType=None):
        data_type = str(dataType or "").lower()
        if data_type == "json":
            return response.json()
        if data_type in ("", "text", "html", "script"):
            return response.text
        if data_type == "xml":
            return º.parseXML(response.text)
        return response.text

    @staticmethod
    def _normalize_ajax_options(
        url="/",
        type="GET",
        data=None,
        contentType=False,
        processData=None,
        cache=None,
        success=None,
        error=None,
        **kwargs,
    ):
        if isinstance(url, dict):
            options = dict(url)
            explicit = dict(kwargs)
            if contentType is not False:
                explicit["contentType"] = contentType
            if success is not None:
                explicit["success"] = success
            if error is not None:
                explicit["error"] = error
            if type != "GET":
                explicit["type"] = type
            if data is not None:
                explicit["data"] = data
            if processData is not None:
                explicit["processData"] = processData
            if cache is not None:
                explicit["cache"] = cache
            options.update(
                {key: value for key, value in explicit.items() if value is not None}
            )
        else:
            options = dict(kwargs)
            options.update(
                {
                    "url": url,
                    "type": type,
                    "data": data,
                    "contentType": contentType,
                    "success": success,
                    "error": error,
                }
            )
            if processData is not None:
                options["processData"] = processData
            if cache is not None:
                options["cache"] = cache

        settings = copy.deepcopy(º.ajaxSettings)
        headers = dict(settings.get("headers", {}))
        headers.update(options.get("headers") or {})
        settings.update(options)
        settings["headers"] = headers
        settings["url"] = settings.get("url", "/")
        settings["type"] = str(
            settings.get("method", settings.get("type", "GET")) or "GET"
        ).upper()
        if "data" not in settings:
            settings["data"] = None
        if "processData" not in settings or settings["processData"] is None:
            settings["processData"] = True
        if "cache" not in settings or settings["cache"] is None:
            settings["cache"] = True
        if "global" not in settings:
            settings["global"] = True
        if settings.get("contentType"):
            settings["headers"]["Content-Type"] = settings["contentType"]
        return settings

    def ajaxComplete(self, handler=None):
        return º._ajax_event_adapter(self, handler, "ajaxComplete")

    def ajaxError(self, handler=None):
        return º._ajax_event_adapter(self, handler, "ajaxError")

    def ajaxSend(self, handler=None):
        return º._ajax_event_adapter(self, handler, "ajaxSend")

    def ajaxStart(self, handler=None):
        return º._ajax_event_adapter(self, handler, "ajaxStart")

    def ajaxStop(self, handler=None):
        return º._ajax_event_adapter(self, handler, "ajaxStop")

    def ajaxSuccess(self, handler=None):
        return º._ajax_event_adapter(self, handler, "ajaxSuccess")

    @staticmethod
    def ajax(
        url="/",
        type="GET",
        data=None,
        contentType=False,
        processData=None,
        cache=None,
        success=None,
        error=None,
        complete=None,
        dataType=None,
        headers=None,
        timeout=None,
        **kwargs,
    ):
        """make an ajax request"""
        extra_options = dict(kwargs)
        if complete is not None:
            extra_options["complete"] = complete
        if dataType is not None:
            extra_options["dataType"] = dataType
        if headers is not None:
            extra_options["headers"] = headers
        if timeout is not None:
            extra_options["timeout"] = timeout
        options = º._normalize_ajax_options(
            url=url,
            type=type,
            data=data,
            contentType=contentType,
            processData=processData,
            cache=cache,
            success=success,
            error=error,
            **extra_options,
        )
        for prefilter in list(º._ajax_prefilters):
            º._callback(prefilter, options)

        method = options["type"]
        request_data = options.get("data")
        request_params = dict(options.get("params") or {})
        request_headers = dict(options.get("headers") or {})
        request_kwargs = {
            "headers": request_headers or None,
            "timeout": options.get("timeout") or 30,
        }

        if options.get("json") is not None:
            request_kwargs["json"] = options.get("json")
        elif method in ("GET", "HEAD") and request_data is not None:
            if options.get("processData") and isinstance(request_data, dict):
                request_params.update(request_data)
            else:
                request_kwargs["data"] = request_data
        elif request_data is not None:
            if options.get("processData") and isinstance(request_data, (dict, list)):
                request_kwargs["data"] = º.param(request_data)
                request_headers.setdefault(
                    "Content-Type", "application/x-www-form-urlencoded; charset=UTF-8"
                )
            else:
                request_kwargs["data"] = request_data

        if options.get("cache") is False and method in ("GET", "HEAD"):
            request_params.setdefault("_", int(time.time() * 1000))
        if request_params:
            request_kwargs["params"] = request_params

        use_global_events = bool(options.get("global", True))
        if use_global_events:
            if º._ajax_active == 0:
                º._trigger_ajax_event("ajaxStart")
            º._ajax_active += 1

        response = None
        text_status = "error"
        try:
            from requests import Session

            before_send = options.get("beforeSend")
            if before_send is not None:
                should_send = º._callback(before_send, None, options)
                if should_send is False:
                    text_status = "abort"
                    return None

            if use_global_events:
                º._trigger_ajax_event("ajaxSend", None, options)

            with Session() as session:
                response = session.request(method, options["url"], **request_kwargs)

            response.data = º._parse_ajax_response(response, options.get("dataType"))
            response.parsedData = response.data
            text_status = "success" if º._ajax_success_status(response) else "error"

            status_handlers = options.get("statusCode") or {}
            status_handler = status_handlers.get(response.status_code)
            if status_handler is not None:
                º._callback(status_handler, response, text_status)

            if text_status == "success":
                º._callback(options.get("success"), response.data, text_status, response)
                if use_global_events:
                    º._trigger_ajax_event(
                        "ajaxSuccess", response, options, response.data
                    )
            else:
                thrown = response.reason or response.text
                º._ajax_error_callback(
                    options.get("error"), response, text_status, thrown
                )
                if use_global_events:
                    º._trigger_ajax_event("ajaxError", response, options, thrown)
            return response

        except Exception as exc:
            text_status = "parsererror" if response is not None else "error"
            º._ajax_error_callback(options.get("error"), response, text_status, exc)
            if use_global_events:
                º._trigger_ajax_event("ajaxError", response, options, exc)
            return None
        finally:
            º._callback(options.get("complete"), response, text_status)
            if use_global_events:
                º._trigger_ajax_event("ajaxComplete", response, options)
                º._ajax_active = max(0, º._ajax_active - 1)
                if º._ajax_active == 0:
                    º._trigger_ajax_event("ajaxStop")

    @staticmethod
    def ajaxPrefilter(callback=None):
        """Handle custom Ajax options or modify existing options before each request is sent
        and before they are processed by .ajax"""
        if callback is None:
            return list(º._ajax_prefilters)
        º._ajax_prefilters.append(callback)
        return callback

    @staticmethod
    def ajaxSetup(options=None, **kwargs):
        """Set default values for future Ajax requests. Its use is not recommended."""
        updates = {}
        if options:
            updates.update(options)
        updates.update(kwargs)
        if "headers" in updates:
            headers = dict(º.ajaxSettings.get("headers", {}))
            headers.update(updates.pop("headers") or {})
            º.ajaxSettings["headers"] = headers
        º.ajaxSettings.update(updates)
        return º.ajaxSettings.copy()

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
    def getJSON(url, data=None, success=None, error=None):
        """Load JSON-encoded data from the server using a GET HTTP request."""
        if callable(data) and success is None:
            success = data
            data = None
        return º.get(url, data=data, dataType="json", success=success, error=error)

    @staticmethod
    def getScript(filename, *args):
        """execute another python file."""
        from subprocess import Popen  # nosec B404

        Popen([sys.executable, filename + ".py"])  # nosec B603

    @staticmethod  # TODO - test
    def globalEval(code):
        """Execute some python code globally."""
        return eval(code, globals(), locals())  # nosec B307

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
        pairs = []

        def add_pair(key, value):
            pairs.append(
                Global.encodeURIComponent(key)
                + "="
                + Global.encodeURIComponent("" if value is None else value)
            )

        if isinstance(obj, dQuery_el):
            return obj.serialize()
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, (list, tuple)):
                    for item in value:
                        add_pair(key, item)
                else:
                    add_pair(key, value)
            return "&".join(pairs)
        if isinstance(obj, list):
            for item in obj:
                if isinstance(item, dict) and "name" in item:
                    add_pair(item["name"], item.get("value", ""))
                elif isinstance(item, (list, tuple)) and len(item) == 2:
                    add_pair(item[0], item[1])
                else:
                    raise TypeError(item)
            return "&".join(pairs)
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
    def post(url, data=None, success=None, dataType=False, error=None):
        """Send data to the server using a HTTP POST request."""
        if callable(data) and success is None:
            success = data
            data = None
        response = º.ajax(
            {
                "url": url,
                "type": "POST",
                "data": data,
                "dataType": dataType,
                "success": success,
                "error": error,
            }
        )
        if response is None:
            return None
        return response.data

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
    def each(self, func=None):
        if isinstance(self, dQuery_el):
            return dQuery_el.each(self, func)
        for index, value in enumerate(self):
            dQuery_el._call_with_fallback(func, (index, value), (value,), (index,))
        return self

    def get(self, data=None, dataType=False, success=None, error=None):
        if isinstance(self, dQuery_el):
            return dQuery_el.get(self, data)
        if callable(data) and success is None:
            success = data
            data = None
            dataType = False
        elif callable(dataType):
            callback = dataType
            if isinstance(success, str):
                dataType = success
            else:
                dataType = False if success is None else success
            success = callback
        url = self
        response = º.ajax(
            {
                "url": url,
                "type": "GET",
                "data": data,
                "dataType": dataType,
                "success": success,
                "error": error,
            }
        )
        if response is None:
            return None
        return response.data

    def map(self, func=None):
        if isinstance(self, dQuery_el):
            return dQuery_el.map(self, func)
        return [
            dQuery_el._call_with_fallback(func, (index, value), (value,), (index,))
            for index, value in enumerate(self)
        ]

    def data(self, key=_UNSET, value=_UNSET):
        if isinstance(self, dQuery_el):
            return dQuery_el.data(self, key, value)
        element = self
        store = getattr(element, "_dquery_data", {}).copy()
        if key is _UNSET:
            return store
        if isinstance(key, dict):
            store.update(key)
            setattr(element, "_dquery_data", store)
            return element
        if value is _UNSET:
            if key in store:
                return store.get(key)
            if hasattr(element, "getAttribute"):
                attr_value = element.getAttribute(dQuery_el._data_attribute_name(key))
                if attr_value is not None:
                    return dQuery_el._coerce_data_value(attr_value)
            return None
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

    def removeData(self, key=_UNSET):
        if isinstance(self, dQuery_el):
            return dQuery_el.removeData(self, key)
        store = getattr(self, "_dquery_data", {}).copy()
        if key is _UNSET:
            store = {}
        else:
            for name in str(key).split():
                store.pop(name, None)
        setattr(self, "_dquery_data", store)
        return self


dQuery = º
