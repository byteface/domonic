"""
domonic.dom
===========

The core DOM implementation for domonic.

This module provides the document tree, node and element types, collections,
range and selection helpers, geometry interfaces, mutation and layout
observers, and the document-facing APIs that the rest of the package builds on.
It is intended to feel like a practical Python surface for the DOM and related
web-platform concepts rather than a small HTML helper tree.
"""
from __future__ import annotations

import copy
from html import escape as _escape_html
import os
import re
import time
from collections.abc import Iterable as IterableABC
from email.utils import formatdate
from typing import Any, Callable, ClassVar, Iterable, Iterator

from domonic.events import Event, EventTarget, MouseEvent
from domonic.geom.vec3 import vec3
from domonic.style import CSSStyleDeclaration as Style
from domonic.style import StyleSheetList
from domonic.webapi.console import Console
from domonic.webapi.url import URL
from domonic.webapi.xpath import (XPathEvaluator, XPathException,
                                  XPathExpression, XPathResult)

# from xml.dom.pulldom import END_ELEMENT


class DOMConfig:
    """Global rendering and behaviour flags for domonic's DOM.

    ``DOMConfig`` controls how trees are rendered and how a few optional
    behaviours are interpreted across the library, such as auto-escaping text
    content and optional closing-tag handling.
    """

    GLOBAL_AUTOESCAPE: bool = False  # Default is False
    RENDER_OPTIONAL_CLOSING_TAGS: bool = True  # Default is True
    RENDER_OPTIONAL_CLOSING_SLASH: bool = True  # on emtpy nodes should the last slash be rendered
    SPACE_BEFORE_OPTIONAL_CLOSING_SLASH: bool = (
        False  # on emtpy nodes should there be a space before the closing slash?
    )
    HTMX_ENABLED: bool = False  # Default is false
    # NO_REPR: bool = True  # objects always render?
    ATTRIBUTE_QUOTES: bool | str | None = '"'  # i.e. <tag="">


def _attribute_quote_mark() -> str:
    if DOMConfig.ATTRIBUTE_QUOTES is False or DOMConfig.ATTRIBUTE_QUOTES == "":
        return ""
    if DOMConfig.ATTRIBUTE_QUOTES is True or DOMConfig.ATTRIBUTE_QUOTES is None:
        return '"'
    return str(DOMConfig.ATTRIBUTE_QUOTES)


def _render_attribute_value(value: Any) -> str:
    quote = _attribute_quote_mark()
    should_quote = DOMConfig.ATTRIBUTE_QUOTES is not None or type(value) == str
    rendered_value = _escape_html(str(value), quote=True) if DOMConfig.GLOBAL_AUTOESCAPE else value
    quote = quote if should_quote else ""
    return f"{quote}{rendered_value}{quote}"


def _get_custom_element_registry():
    try:
        from domonic.window import window as domonic_window
    except Exception:
        return None
    return getattr(domonic_window, "customElements", None)


def _iter_dom_nodes(node):
    if not isinstance(node, Node):
        return
    yield node
    for child in getattr(node, "childNodes", []):
        if isinstance(child, Node):
            yield from _iter_dom_nodes(child)


def _node_is_connected(node: "Node") -> bool:
    try:
        return isinstance(node.rootNode, Document)
    except Exception:
        return False


def _notify_attribute_changed(element: "Element", attribute: str, old_value: Any, new_value: Any) -> None:
    callback = getattr(element, "attributeChangedCallback", None)
    if not callable(callback) or old_value == new_value:
        return
    observed = getattr(element.__class__, "observedAttributes", ())
    if observed is None:
        observed = ()
    normalized = attribute[1:] if attribute.startswith("_") else attribute
    if normalized in tuple(observed):
        callback(normalized, old_value, new_value)


def _run_connected_callback(element: "Element") -> None:
    callback = getattr(element, "connectedCallback", None)
    if callable(callback) and not getattr(element, "_custom_element_connected", False):
        element._custom_element_connected = True
        callback()


def _run_disconnected_callback(element: "Element") -> None:
    callback = getattr(element, "disconnectedCallback", None)
    if callable(callback) and getattr(element, "_custom_element_connected", False):
        element._custom_element_connected = False
        callback()


def _run_adopted_callback(element: "Element", old_document: "Document | None", new_document: "Document | None") -> None:
    callback = getattr(element, "adoptedCallback", None)
    if callable(callback) and old_document is not None and old_document is not new_document:
        callback(old_document, new_document)


def _adopt_tree(node: "Node", old_document: "Document | None", new_document: "Document | None") -> None:
    for current in _iter_dom_nodes(node):
        current._ownerDocument = new_document
        if isinstance(current, Element):
            _run_adopted_callback(current, old_document, new_document)


def _owner_document_for(node: "Node") -> "Document | None":
    owner_document = node.ownerDocument
    return owner_document if isinstance(owner_document, Document) else None


def _drain_document_fragment(fragment: "DocumentFragment") -> tuple[Any, ...]:
    children = tuple(fragment.args)
    fragment.args = ()
    for child in children:
        if isinstance(child, Node):
            child.parentNode = None
    return children


def _coerce_insertion_nodes(*nodes: Any) -> tuple[Any, ...]:
    prepared: list[Any] = []
    for node in nodes:
        if isinstance(node, DocumentFragment):
            prepared.extend(_drain_document_fragment(node))
        else:
            prepared.append(node)
    return tuple(prepared)


def _coerce_replacement_nodes(*nodes: Any) -> tuple[Any, ...]:
    if (
        len(nodes) == 1
        and isinstance(nodes[0], IterableABC)
        and not isinstance(nodes[0], (str, bytes, bytearray, Node))
    ):
        nodes = tuple(nodes[0])
    return _coerce_insertion_nodes(*nodes)


def _detach_node_for_insertion(node: Any) -> "Document | None":
    if not isinstance(node, Node):
        return None
    old_document = _owner_document_for(node)
    old_parent = getattr(node, "parentNode", None)
    if isinstance(old_parent, Node):
        removed = old_parent.removeChild(node)
        if removed is None:
            node.parentNode = None
    return old_document


def _connect_inserted_node(
    parent: "Node",
    node: Any,
    old_document: "Document | None",
) -> None:
    if not isinstance(node, Node):
        return
    node.parentNode = parent
    parent_document = parent.ownerDocument
    new_document = parent_document if isinstance(parent_document, Document) else None
    _adopt_tree(node, old_document, new_document)
    _connect_tree(node)


def _upgrade_custom_element_instance(element: "Element") -> "Element":
    registry = _get_custom_element_registry()
    if registry is None:
        return element
    return registry._upgrade_element(element)


def _connect_tree(node: "Node") -> None:
    for current in _iter_dom_nodes(node):
        current._ownerDocument = current.rootNode if isinstance(current.rootNode, Document) else getattr(current, "_ownerDocument", None)
        current.isConnected = _node_is_connected(current)
        if isinstance(current, Element):
            _upgrade_custom_element_instance(current)
            if current.isConnected:
                _run_connected_callback(current)


def _disconnect_tree(node: "Node") -> None:
    for current in _iter_dom_nodes(node):
        current.isConnected = False
        if isinstance(current, Element):
            _run_disconnected_callback(current)


def _assigned_slot_for_node(node: "Node") -> "HTMLSlotElement | None":
    parent = getattr(node, "parentNode", None)
    if not isinstance(parent, Element):
        return None
    shadow_root = getattr(parent, "shadowRoot", None)
    if not isinstance(shadow_root, ShadowRoot):
        return None
    slot_name = ""
    if isinstance(node, Element):
        slot_name = node.getAttribute("slot") or ""
    for child in shadow_root.childNodes:
        if isinstance(child, HTMLSlotElement):
            if (child.getAttribute("name") or "") == slot_name:
                return child
    if slot_name == "":
        for child in shadow_root.childNodes:
            if isinstance(child, HTMLSlotElement) and not child.getAttribute("name"):
                return child
    return None


def _notify_slot_change(target: "Node") -> None:
    slots: list[HTMLSlotElement] = []
    if isinstance(target, ShadowRoot):
        slots = [child for child in target.childNodes if isinstance(child, HTMLSlotElement)]
    elif isinstance(target, Element) and isinstance(getattr(target, "shadowRoot", None), ShadowRoot):
        slots = [child for child in target.shadowRoot.childNodes if isinstance(child, HTMLSlotElement)]
    for slot in slots:
        slot.dispatchEvent(Event("slotchange"))


def _iter_ancestors_inclusive(node: "Node | None") -> Iterator["Node"]:
    current = node
    while isinstance(current, Node):
        yield current
        current = getattr(current, "parentNode", None)


def _normalize_mutation_observer_options(options: dict[str, Any]) -> dict[str, Any]:
    normalized = {
        "subtree": bool(options.get("subtree", False)),
        "childList": bool(options.get("childList", False)),
        "attributes": bool(options.get("attributes", False)),
        "attributeFilter": options.get("attributeFilter"),
        "attributeOldValue": bool(options.get("attributeOldValue", False)),
        "characterData": bool(options.get("characterData", False)),
        "characterDataOldValue": bool(options.get("characterDataOldValue", False)),
    }
    if normalized["attributeFilter"] is not None or normalized["attributeOldValue"]:
        normalized["attributes"] = True
    if normalized["characterDataOldValue"]:
        normalized["characterData"] = True
    if normalized["attributeFilter"] is not None:
        normalized["attributeFilter"] = tuple(
            attr[1:] if isinstance(attr, str) and attr.startswith("_") else attr
            for attr in normalized["attributeFilter"]
        )
    if not any(
        (
            normalized["childList"],
            normalized["attributes"],
            normalized["characterData"],
        )
    ):
        raise TypeError("MutationObserver options must enable childList, attributes, or characterData")
    return normalized


def _queue_mutation_record(
    record_type: str,
    target: "Node",
    *,
    added_nodes: Iterable["Node"] | None = None,
    removed_nodes: Iterable["Node"] | None = None,
    previous_sibling: "Node | None" = None,
    next_sibling: "Node | None" = None,
    attribute_name: str | None = None,
    attribute_namespace: str | None = None,
    old_value: str | None = None,
) -> None:
    try:
        observers = list(MutationObserver._all_observers)
    except NameError:
        return
    if not observers:
        return
    record = MutationRecord(
        record_type,
        target,
        addedNodes=added_nodes or (),
        removedNodes=removed_nodes or (),
        previousSibling=previous_sibling,
        nextSibling=next_sibling,
        attributeName=attribute_name,
        attributeNamespace=attribute_namespace,
        oldValue=old_value,
    )
    pending: list[MutationObserver] = []
    for observer in observers:
        if observer._enqueue_if_observing(record):
            pending.append(observer)
    for observer in pending:
        observer._flush()
    _process_observer_notifications(target)


_observer_processing: bool = False


def _intersect_rects(first: DOMRectReadOnly, second: DOMRectReadOnly) -> DOMRect:
    left = max(first.left, second.left)
    top = max(first.top, second.top)
    right = min(first.right, second.right)
    bottom = min(first.bottom, second.bottom)
    if right <= left or bottom <= top:
        return DOMRect(left, top, 0, 0)
    return DOMRect(left, top, right - left, bottom - top)


def _default_intersection_root_rect(target: "Element", target_rect: DOMRectReadOnly) -> DOMRectReadOnly:
    doc = target.ownerDocument if isinstance(target.ownerDocument, Document) else None
    root = None
    if doc is not None:
        root = getattr(doc, "documentElement", None) or getattr(doc, "body", None)
    if isinstance(root, Element) and root is not target:
        return root.getBoundingClientRect()
    return DOMRectReadOnly.fromRect(target_rect)


def _process_observer_notifications(target: "Node | None" = None, target_rect: DOMRectReadOnly | None = None) -> None:
    global _observer_processing
    if _observer_processing:
        return
    _observer_processing = True
    try:
        try:
            resize_observers = list(ResizeObserver._all_observers)
        except NameError:
            resize_observers = []
        for observer in resize_observers:
            observer._process(target, target_rect)

        try:
            intersection_observers = list(IntersectionObserver._all_observers)
        except NameError:
            intersection_observers = []
        for observer in intersection_observers:
            observer._process(target, target_rect)
    finally:
        _observer_processing = False


def _form_owner(control: "Element") -> "HTMLFormElement | None":
    owner_document = control.ownerDocument if isinstance(control.ownerDocument, Document) else None
    form_id = control.getAttribute("form") if isinstance(control, Element) else None
    if form_id and owner_document is not None:
        form = owner_document.getElementById(form_id)
        if isinstance(form, HTMLFormElement):
            return form
    for ancestor in _iter_ancestors_inclusive(getattr(control, "parentNode", None)):
        if isinstance(ancestor, HTMLFormElement):
            return ancestor
    return None


def _dispatch_value_change_events(control: "Element") -> None:
    from domonic.events import Event, InputEvent

    control.dispatchEvent(InputEvent("input", {"bubbles": True, "cancelable": False}))
    control.dispatchEvent(Event("change", {"bubbles": True, "cancelable": False}))


def _radio_group_members(control: "Element", *, include_disabled: bool = True) -> list["HTMLInputElement"]:
    if not isinstance(control, Element):
        return []
    name = control.getAttribute("name")
    if not name:
        return [control] if isinstance(control, HTMLInputElement) else []
    form = _form_owner(control)
    root = form if form is not None else getattr(control, "parentNode", None)
    if root is None or not hasattr(root, "querySelectorAll"):
        return [control] if isinstance(control, HTMLInputElement) else []
    radios = []
    for candidate in root.querySelectorAll("input"):
        if (
            isinstance(candidate, HTMLInputElement)
            and (include_disabled or not candidate.hasAttribute("disabled"))
            and (candidate.getAttribute("type") or "").lower() == "radio"
            and candidate.getAttribute("name") == name
        ):
            radios.append(candidate)
    return radios or ([control] if isinstance(control, HTMLInputElement) else [])


def _is_control_valid(control: "Element") -> bool:
    if not isinstance(control, Element) or control.hasAttribute("disabled"):
        return True
    if control.hasAttribute("required"):
        tag_name = getattr(control, "tagName", getattr(control, "name", "")).lower()
        if tag_name == "input":
            input_type = (control.getAttribute("type") or "text").lower()
            if input_type == "checkbox":
                return control.checked
            if input_type == "radio":
                return any(radio.checked for radio in _radio_group_members(control, include_disabled=False))
            return control.value != ""
        if tag_name == "textarea":
            return control.value != ""
        if tag_name == "select":
            return control.value != ""
    return True


class Node(EventTarget):
    """An abstract base class upon which many other DOM API objects are based"""

    ELEMENT_NODE: int = 1
    TEXT_NODE: int = 3
    CDATA_SECTION_NODE: int = 4
    PROCESSING_INSTRUCTION_NODE: int = 7
    COMMENT_NODE: int = 8
    DOCUMENT_NODE: int = 9
    DOCUMENT_TYPE_NODE: int = 10
    DOCUMENT_FRAGMENT_NODE: int = 11

    DOCUMENT_POSITION_DISCONNECTED: int = 1
    DOCUMENT_POSITION_PRECEDING: int = 2
    DOCUMENT_POSITION_FOLLOWING: int = 4
    DOCUMENT_POSITION_CONTAINS: int = 8
    DOCUMENT_POSITION_CONTAINED_BY: int = 16
    DOCUMENT_POSITION_IMPLEMENTATION_SPECIFIC: int = 32

    # The following constants have been deprecated and should not be used anymore.
    ATTRIBUTE_NODE: int = 2
    ENTITY_REFERENCE_NODE: int = 5
    ENTITY_NODE: int = 6
    NOTATION_NODE: int = 12

    __isempty: bool = False  # tells us if the node is empty i.e. has no content aka 'self closing'. in html that would be: area, base, br, col, embed, hr, img, input, link, meta, param, source, track, True
    __context: ClassVar[list["Node"] | None] = None  # private. tags will append to last item in context on creation.

    # __slots__ = ['____attributes__',
    #              '__content',
    #              'name',
    #              '__rootNode',
    #              'parentNode',
    #              'baseURI',
    #              'isConnected',
    #              'namespaceURI',
    #              'outerText',
    #              'prefix']

    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs

        if getattr(self, "name", None) is None:
            self.name = ""

        # if user doesn't put underscore (dont advertise this as still has issues.)
        new_kwargs = {}
        for k, v in kwargs.items():
            if k[0] != "_":
                new_kwargs[f"_{k}"] = v
            else:
                new_kwargs[k] = v
        self.kwargs = new_kwargs

        self.baseURI: str = ""  # TODO - if ownerdocument has a basetag, use that
        self.isConnected: bool = True
        self.namespaceURI: str = "http://www.w3.org/1999/xhtml"
        self.outerText: str = None
        self._ownerDocument = None
        self.parentNode = None
        self.prefix = None  # 🗑️
        # self.baseURIObject = None  # ?
        # self.nodePrincipal = None
        self._update_parents()

        # attempt to set init namespaceURI based on the tag name
        try:
            n = self.rootNode
            nm = n.tagName
            # print(n)
            if nm == "html":
                self.namespaceURI = "http://www.w3.org/1999/xhtml"
            elif nm == "svg":
                self.namespaceURI = "http://www.w3.org/2000/svg"
            elif nm == "xhtml":
                self.namespaceURI = "http://www.w3.org/1999/xhtml"
            elif nm == "xml":
                self.namespaceURI = "http://www.w3.org/XML/1998/namespace"
            elif nm == "xlink":
                self.namespaceURI = "http://www.w3.org/1999/xlink"
            elif nm == "math":
                self.namespaceURI = "http://www.w3.org/1998/Math/MathML"
            # elif nm == "rdf":
            #     self.namespaceURI = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
            # elif nm == "rdfs":
            #     self.namespaceURI = "http://www.w3.org/2000/01/rdf-schema#"
            # elif nm == "owl":
            #     self.namespaceURI = "http://www.w3.org/2002/07/owl#"
            # elif nm == "dc":
            #     self.namespaceURI = "http://purl.org/dc/elements/1.1/"
            # elif nm == "dcterms":
            #     self.namespaceURI = "http://purl.org/dc/terms/"
            # elif nm == "foaf":
            #     self.namespaceURI = "http://xmlns.com/foaf/0.1/"
            # elif nm == "cc":
            #     self.namespaceURI = "http://web.resource.org/cc/"
            # elif nm == "gr":
            #     self.namespaceURI = "http://purl.org/goodrelations/v1#"
            # elif nm == "sioc":
            #     self.namespaceURI = "http://rdfs.org/sioc/ns#"
            # elif nm == "doap":
            #     self.namespaceURI = "http://usefulinc.com/ns/doap#"
            # elif nm == "vcard":
            #     self.namespaceURI = "http://www.w3.org/2006/vcard/ns#"
            # elif nm == "schema":
            #     self.namespaceURI = "http://schema.org/"
            # elif nm == "og":
            #     self.namespaceURI = "http://ogp.me/ns#"
            # elif nm == "geo":
            #     self.namespaceURI = "http://www.w3.org/2003/01/geo/wgs84_pos#"
            # elif nm == "rev":
            #     self.namespaceURI = "http://purl.org/stuff/rev#"
            # elif nm == "sioc":
            #     self.namespaceURI = "http://rdfs.org/sioc/ns#"
            # elif nm == "skos":
            #     self.namespaceURI = "http://www.w3.org/2004/02/skos/core#"  # TODO - test
            # elif nm == "wot":
            #     self.namespaceURI = "http://xmlns.com/wot/0.1/"
            # elif nm == "wgs84_pos":
            #     self.namespaceURI = "http://www.w3.org/2003/01/geo/wgs84_pos#"
            # elif nm == "xhv":
            #     self.namespaceURI = "http://www.w3.org/1999/xhtml/vocab#"
        except Exception as e:
            pass

        # this is for using 'with'
        if Node.__context is not None:
            Node.__context[len(Node.__context) - 1] += self
        super().__init__(*args, **kwargs)

    @property
    def content(self):
        # return ''.join([each.__str__() for each in self.args])

        # if any child are lists by mistake, loop and call __str__ on each first
        cnt = self.args
        for i, arg in enumerate(cnt):
            if isinstance(arg, list):
                cnt = list(cnt)
                cnt[i] = "".join([each.__str__() for each in arg])
                cnt = tuple(cnt)

        if DOMConfig.GLOBAL_AUTOESCAPE:
            import html as fix

            cnt = list(cnt)
            for each, child in enumerate(cnt):
                if isinstance(child, str) or isinstance(child, Text):
                    child = fix.escape(str(child))
                    cnt[each] = child
            cnt = tuple(cnt)
            return "".join([each.__str__() for each in cnt])
        # else:
        return "".join([each.__str__() for each in cnt])

    @content.setter
    def content(self, ignore):
        self.__content = "".join([each.__str__() for each in self.args])
        return

    @property
    def __attributes__(self):
        def format_attr(key, value):
            if value is True:
                value = "true"
            if value is False:
                value = "false"
            key = key.split("_", 1)[1]
            key = {
                "accept_charset": "accept-charset",
                "http_equiv": "http-equiv",
            }.get(key, key)

            # note - consider making this an attributes handler for any custom attributes
            # so on config user can add a handler function for the attribute
            if DOMConfig.HTMX_ENABLED:
                # if htmx is enabld
                htmx_attributes = [
                    "boost",
                    "confirm",
                    "delete",
                    "disable",
                    "disinherit",
                    "encoding",
                    "ext",
                    "get",
                    "headers",
                    "history_elt",
                    "include",
                    "indicator",
                    "params",
                    "patch",
                    "post",
                    "preserve",
                    "prompt",
                    "push_url",
                    "put",
                    "request",
                    "select",
                    "sse",
                    "swap",
                    "swap_oob",
                    "sync",
                    "target",
                    "trigger",
                    "vals",
                    "vars",
                    "ws",
                ]

                if key in htmx_attributes:
                    return f""" data-hx-{key}={_render_attribute_value(value)}"""

            # lets us have boolean attributes
            if key in [
                "async",
                "checked",
                "autofocus",
                "disabled",
                "formnovalidate",
                "hidden",
                "multiple",
                "novalidate",
                "readonly",
                "required",
                "selected",
                "open",
                "contenteditable",
                "reversed",
                "download",
                "draggable",
                "spellcheck",
                "translate",
                "autoplay",       # Added
                "controls",       # Added
                "loop",           # Added
                "muted",          # Added
                "default",        # Added
                "allowfullscreen",# Added
                "playsinline",    # Added
                "value",          # Added
                "defer",          # Added
                # "compact",        # Added
                # "ismap",          # Added
                # "sandbox",        # Added
                # "seamless",       # Added
                # "selected",       # Added
                # "sortable",       # Added
                # "truespeed",      # Added
                # "typemustmatch",  # Added
                # "visible",        # Added
                # "wrap",           # Added
                # "novalidate",     # Added
                # "open",           # Added
                # "readonly",       # Added
                # "required",       # Added
                

            ]:
                if value == "" or value == key:
                    return f""" {key}"""
            return f""" {key}={_render_attribute_value(value)}"""

        try:
            return "".join([format_attr(key, value) for key, value in self.kwargs.items()])
        except IndexError as e:
            from domonic.html import TemplateError

            raise TemplateError(e)
        # except Exception as e:
        # print(e)

    @__attributes__.setter
    def __attributes__(self, ignore):
        try:
            self.__attributes = "".join(
                [
                    f""" {key.split('_', 1)[1]}={_render_attribute_value(value)}"""
                    for key, value in self.kwargs.items()
                ]
            )
        except IndexError as e:
            from domonic.html import TemplateError

            raise TemplateError(e)
        # except Exception as e:
        # print(e)

    def __str__(self):
        if not DOMConfig.RENDER_OPTIONAL_CLOSING_TAGS:
            if self.name in [
                "html",
                "head",
                "body",
                "p",
                "dt",
                "dd",
                "li",
                "option",
                "thead",
                "th",
                "tbody",
                "tr",
                "td",
                "tfoot",
                "colgroup",
            ]:
                return f"<{self.name}{self.__attributes__}>{self.content}"
        return f"<{self.name}{self.__attributes__}>{self.content}</{self.name}>"

    def __mul__(self, other):
        """
        requires you to render yourself i.e.
        cells = cell()*10
        print(''.join([str(c) for c in cells]))
        """
        reproducer = []
        for i in range(other):
            reproducer.append(copy.deepcopy(self))
        return reproducer

    def __rmul__(self, other):
        """
        requires you to render yourself i.e.
        cells = cell()*10
        print(''.join([str(c) for c in cells]))
        """
        reproducer = []
        for i in range(other):
            reproducer.append(copy.deepcopy(self))
        return reproducer

    def __truediv__(self, other):
        """use to render clones without having to parse commas yourself"""
        reproducer = []
        for i in range(other):
            reproducer.append(str(self))
        return "".join(reproducer)

    def __rtruediv__(self, other):
        """use to render clones without having to parse commas yourself"""
        reproducer = []
        for i in range(other):
            reproducer.append(str(self))
        return "".join(reproducer)

    def __div__(self, other):
        """
        useful for prototyping as renders. to retain objects use multiply
        """
        reproducer = []
        for i in range(other):
            reproducer.append(str(self))
        return "".join(reproducer)

    def __rdiv__(self, other):
        """
        useful for prototyping as renders. to retain objects use multiply
        """
        reproducer = []
        for i in range(other):
            reproducer.append(str(self))
        return "".join(reproducer)

    def __or__(self, other):
        """return self unless other is something"""
        if other is not False:
            return other
        return self

    def __iadd__(self, item):
        """adds an item to the nodes of children. can also pass a list and it will unpack them"""
        if isinstance(item, (list, tuple)):  # TODO - Documentfragment?
            for i in item:
                self.args = self.args + (i,)
            return self

        self.args = self.args + (item,)
        return self

    def __isub__(self, item):
        """removes an item from the list of children"""
        replace_args = list(self.args)
        replace_args.remove(item)
        self.args = tuple(replace_args)
        return self

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.args[index]
        # elif isinstance(index, str):
        #     if index.startswith('_'):
        #         return self.kwargs[index]
        #     else:
        #         return getattr(self, index)
        # super(Node, self).__getitem__(index)

        if isinstance(index, str):
            # call props on self
            # print('erk!')
            try:
                # return Node.__dict__[index]
                return getattr(self, index)
            except Exception as e:
                print(e)
                # return None
        # return super(Node, self).__getitem__(index)

    def __rshift__(self, item):
        try:
            for key in item.keys():
                self.kwargs[key] = item[key]
            return self
        except Exception as e:
            print(e)
            raise ValueError

    # def __add__(self, item):
    #     try:
    #         self.args = self.args + (item,)
    #         return self
    #     except Exception as e:
    #         print(e)
    #         raise ValueError

    # def __sub__(self, item):
    #     try:
    #         self.args = self.args - (item,)
    #         return self
    #     except Exception as e:
    #         print(e)
    #         raise ValueError

    # def render()

    def __getattr__(self, attr):
        """
        allows dot notation for reading attributes
        *credit to the peeps on discord/python for this one*
        """
        try:
            kwargs = super().__getattribute__("kwargs")
        except AttributeError:
            kwargs = {}

        if attr in kwargs:
            return kwargs[attr]

        retry = "_" + attr
        if retry in kwargs:
            return kwargs[retry]

        retry = attr[1 : len(attr)]
        if retry in kwargs:
            return kwargs[retry]

        # TODO - think of solution for other MIA attributes as when it would fail silently
        # it was a nightmare. But having to catch the raised errors may also be sluggish
        # maybe specific tags can override this method and provide default values when not present?
        if self.__class__.__name__ == "a" and attr == "href":
            print("    Warning: No 'href' attribute was defined for this 'a' tag.")
            return ""

        try:
            # return getattr(super(), attr)
            # return getattr(self, attr)
            # return getattr(Node, attr)  # means overrideing for style etc in element?
            return getattr(self.__class__, attr)  # means overrideing for style etc in element?
            # return getattr(Element, attr)
        except AttributeError as e:
            # print(e) # TODO - careful. better on for debugging.
            raise e  # ("attribute does not exist:", attr)

        raise AttributeError

    def __pyml__(self):
        """[returns a representation of the object as a pyml string]"""
        # from domonic.dom import Text
        params = ""
        for key, value in self.kwargs.items():
            if "-" in key:
                params += f'**\u007b"{key}":{value}\u007d,'
            else:
                params += f'{key}="{value}", '
        # TODO - will need to loop args and call __pyml__ on each one
        for arg in self.args:
            try:
                if isinstance(arg, Text):
                    params += '"' + str(arg) + '"' + ", "
                else:
                    params += f"{arg.__pyml__()}, "
            except Exception as e:
                params += str(arg) + ", "
        # TODO - if self is document do dentage
        return f"{self.name}({params[:-2]})"
        # return f"{self.name}({params})"
        # return f"{self.name}({args}, {params})"
        # return f"<{self.name}{self.__attributes__}>{self.content}</{self.name}>"

    def __repr__(self) -> str:
        name = self.name or self.__class__.__name__
        return f"<{name}{self.__attributes__}>"

    def _repr_html_(self) -> str:
        return str(self)

    def __setitem__(self, key, value):
        try:
            self.kwargs[key] = value
            return self
        except Exception as e:
            print(e)
            raise ValueError

    def __enter__(self):
        if Node.__context is None:
            Node.__context = []
        Node.__context.append(self)
        return self

    def __exit__(self, type, value, traceback, *args, **kwargs):
        Node.__context.pop()
        if len(Node.__context) == 0:
            Node.__context = None
        return self

    # def __dir__(self):
    #     return self.__dict__.keys()

    # TODO - these are hard and wil need tests
    # def __setattr__(self, attr, value):
    # def __delattr__(self, attr):
    # def __next__(self):
    # def __iter__(self):

    def __iter__(self):
        return iter(self.args)

    def __format__(self, format_spec):
        # return super().__format__(format_spec)
        # get node depth by counting parents

        # TODO - this is a hack to get the depth of the node
        n = self
        depth = 0
        while n is not None:
            # print(type(n), type(n.parentNode))
            n = n.parentNode
            depth += 1

        depth -= 1

        # print(f"depth: {depth}")
        # dent = '    ' * depth
        dent = "\t" * depth

        # loop the children and call __format__ on each one
        # content = ""
        # for child in self.childNodes:
        #     content += child.__format__(format_spec)

        self._update_parents()

        if DOMConfig.GLOBAL_AUTOESCAPE:  # TODO - unit tests
            import html as fix

            self.args = list(self.args)
            for each, child in enumerate(self.args):
                if isinstance(child, str) or isinstance(child, Text):
                    child = fix.escape(str(child))
                    self.args[each] = child
            self.args = tuple(self.args)

        content = "".join([each.__format__(format_spec) for each in self.args])
        # from concurrent.futures import ThreadPoolExecutor
        # content = ''
        # with ThreadPoolExecutor(10) as executor:
        #     for result in executor.map(lambda x: x.__format__(format_spec), self.args):
        #         content += result

        wrap = False
        if len(self.args) == 1:
            if not isinstance(self.args[0], Element):
                wrap = True

        dtype = ""
        if isinstance(self, Document):
            # dtype = "<!DOCTYPE html>"
            dtype = self.doctype

        # if self is a closed_tag, return the content
        from domonic.html import closed_tag

        if isinstance(self, closed_tag):
            return f"\n{dent}<{self.name}{self.__attributes__} />"

        # in html5 the following tags are optional closing tags
        # html, head, body, p, dt, dd, li, option, thead, th, tbody, tr, td, tfoot, colgroup
        size = len(str(content))

        if DOMConfig.RENDER_OPTIONAL_CLOSING_TAGS:
            if size < 150 and wrap:
                return f"\n{dent}<{self.name}{self.__attributes__}>{content}</{self.name}>"
            else:
                return f"{dtype}\n{dent}<{self.name}{self.__attributes__}>{content}\n{dent}</{self.name}>"
        else:
            if self.name in [
                "html",
                "head",
                "body",
                "p",
                "dt",
                "dd",
                "li",
                "option",
                "thead",
                "th",
                "tbody",
                "tr",
                "td",
                "tfoot",
                "colgroup",
            ]:
                if size < 150 and wrap:
                    return f"\n{dent}<{self.name}{self.__attributes__}>{content}"
                else:
                    return f"{dtype}\n{dent}<{self.name}{self.__attributes__}>{content}\n"
            else:
                if size < 150 and wrap:
                    return f"\n{dent}<{self.name}{self.__attributes__}>{content}</{self.name}>"
                else:
                    return f"{dtype}\n{dent}<{self.name}{self.__attributes__}>{content}\n{dent}</{self.name}>"

    # def __call__(self, *args, **kwargs):
    #     """
    #     allows for calling the object as a function
    #     """
    #     print('calling a tag')
    #     print(args)
    #     print(kwargs)
    #     print(self.name)

    def __setattr__(self, name: str, value: Any) -> None:
        try:
            if name == "args":
                super().__setattr__(name, value)
                self._update_parents()
                return
        except Exception as e:
            print(e)
            # pass
        super().__setattr__(name, value)

    # def __getattr__(self, name):
    #     # print(name)
    #     try:
    #         if name == "args":
    #             return super(Node, self).__getattr__(name)
    #     except Exception as e:
    #         print(e)
    #     return super(Node, self).__getattr__(name)

    # def __getattribute__(self, name):
    # print('how are you doing today', name)
    # try:
    #     if name == "args":
    #         return super(Node, self).__getattribute__(name)
    # except Exception as e:
    #     print(e)
    # check if its a property on the class
    # if name in self.__dict__:
    # return super(Node, self).__getattribute__(name)
    # return super(Node, self).__getattribute__(name)
    # return self.__dict__[item]

    # def __getattr__(self, attrName):
    # if name not in self.__dict__:
    #     value = self.fetchAttr(name)    # computes the value
    #     self.__dict__[name] = value
    # return self.__dict__[name]

    # TODO - html.tag class currently has the required method as its called there.
    # def __getitem__(self, item):
    #     print('GET ITEM CALLED')
    #     if isinstance(item, int):
    #         return self.childNodes[item]
    #     if isinstance(item, str):
    #         # call props on self
    #         print('sup!')
    #         try:
    #             return self.__dict__[item]
    #         except Exception as e:
    #             print(e)
    #             # return None
    #     return super(Node, self).__getitem__(item)

    def _update_parents(self):
        """private. - TODO < check these docstrings don't export in docs
        loops all children and sets self as parent.
        cant do as decorator for now as that seems to breaks potential for json serialisation (see Style)
        so will have to call manually whenever self.args are ammended.
        """
        try:
            # print(self.args)
            for el in self.args:
                # if(type(el) not in [str, list, dict, int, float, tuple, object, set]):
                if isinstance(el, (Element, Node)):
                    el.parentNode = self
                    el._update_parents()
        except Exception as e:
            print("unable to update parent", e)

    def _iterate(self, element, callback) -> None:
        """private. - TODO < check these docstrings don't export in docs
        loops all children and sets self as parent.
        cant do as decorator for now as that seems to breaks potential for json serialisation (see Style)
        so will have to call manually whenever self.args are ammended.
        """
        callback(element)  # TODO - this can block on failed attributes
        elements = []
        if isinstance(element, Node):
            elements = element.args
        elif isinstance(element, list):
            elements = element
        try:
            for el in elements:
                if type(el) not in [str, list, dict, int, float, tuple, object, set]:
                    # callback(el)
                    el._iterate(el, callback)
                elif isinstance(el, list):  # if someone is incorrectly using a list as a child
                    for e in el:
                        if type(e) not in (str, list, dict, int, float, tuple, object, set):
                            e._iterate(e, callback)
        except Exception:
            return

    def __bool__(self) -> bool:
        # Nodes should be truthy by existence, not by child count.
        return True

    def __len__(self) -> int:
        return len(self.args)

    def __contains__(self, item: Any) -> bool:
        if item in self.args:
            return True
        return self.contains(item) if isinstance(item, Node) else False

    @property
    def assignedSlot(self):
        return _assigned_slot_for_node(self)

    def appendChild(self, aChild: "Node") -> "Node":
        """
        Adds a child to the current element.
        If item is a DocumentFragment, all its children are added.

        Args:
            item (Node): The Node to add.
        """
        items = _coerce_insertion_nodes(aChild)
        old_documents = [
            (item, _detach_node_for_insertion(item)) for item in items
        ]
        previous_sibling = self.args[-1] if len(self.args) else None
        self.args = self.args + items
        for item, old_document in old_documents:
            _connect_inserted_node(self, item, old_document)
        added_nodes = [item for item in items if isinstance(item, Node)]
        if added_nodes:
            _queue_mutation_record(
                "childList",
                self,
                added_nodes=added_nodes,
                previous_sibling=previous_sibling,
            )
        _notify_slot_change(self)
        return aChild

    @property
    def childElementCount(self) -> int:
        """Returns the number of child elements an element has"""
        return len([child for child in self.args if not isinstance(child, str)])

    @property
    def childNodes(self) -> "NodeList":
        """Returns a live NodeList containing all the children of this node"""
        # return list(self.args)
        return NodeList(self.args)

    @property
    def children(self) -> list[Node]:
        """Returns a collection of child nodes, excluding string content."""
        return [child for child in self.args if not isinstance(child, str)]

    def compareDocumentPosition(self, otherElement: "Node") -> int:
        """
        An integer value representing otherNode's position relative to node as a bitmask combining the following constant properties of Node:

        https://stackoverflow.com/questions/8334286/cross-browser-compare-document-position

        """
        thisNode = self
        other = otherElement

        # if isinstance(other, str):
        #     other = Text(other)
        # if isinstance(thisNode, str):
        #     thisNode = Text(thisNode)

        def recursivelyWalk(nodes, cb):
            for node in nodes:
                if isinstance(node, str):
                    node = Text(node)
                    # continue
                ret = cb(node)
                if ret:
                    return ret
                if node.childNodes and node.childNodes.length > 0:
                    ret = recursivelyWalk(node.childNodes, cb)
                    if ret:
                        return ret

        def testNodeForComparePosition(node, other):
            if node is other:
                return True

        def identifyWhichIsFirst(node):
            if node == other:
                return "other"
            elif node == reference:
                return "reference"

        reference = thisNode
        referenceTop = thisNode
        otherTop = other

        if self == other:
            return 0
        while referenceTop.parentNode is not None:
            referenceTop = referenceTop.parentNode
        while otherTop.parentNode is not None:
            otherTop = otherTop.parentNode

        # print(referenceTop, otherTop)
        if referenceTop != otherTop:
            return Node.DOCUMENT_POSITION_DISCONNECTED

        children = reference.childNodes

        ret = recursivelyWalk(children, lambda p: testNodeForComparePosition(other, p))
        if ret:
            return Node.DOCUMENT_POSITION_CONTAINED_BY  # + Node.DOCUMENT_POSITION_FOLLOWING

        children = other.childNodes
        ret = recursivelyWalk(children, lambda p: testNodeForComparePosition(reference, p))
        if ret:
            return Node.DOCUMENT_POSITION_CONTAINS  # + Node.DOCUMENT_POSITION_PRECEDING
        ret = recursivelyWalk([referenceTop], identifyWhichIsFirst)
        if ret == "other":
            return Node.DOCUMENT_POSITION_PRECEDING
        else:
            return Node.DOCUMENT_POSITION_FOLLOWING

    def contains(self, node: "Node") -> bool:
        """Check whether a node is a descendant of a given node"""
        if node is self:
            return True
        parent = getattr(node, "parentNode", None)
        while parent is not None:
            if parent is self:
                return True
            parent = getattr(parent, "parentNode", None)
        return False

    @property
    def firstChild(self) -> Node | None:
        """Returns the first child node of an element"""
        try:
            return self.args[0]  # TODO - check if this means includes content
        except Exception:
            return None

    def hasChildNodes(self) -> bool:
        """Returns true if an element has any child nodes, otherwise false"""
        return len(self.args) > 0

    @property
    def lastChild(self) -> Node | None:
        """Returns the last child node of an element"""
        try:
            return self.args[len(self.args) - 1]
        except Exception:
            return None

    @property
    def localName(self) -> str | None:
        try:
            return self.tagName
        except Exception:
            return None

    @property
    def nodeName(self) -> str | None:
        """Returns the name of a node"""
        # TODO - not sure what's better this or overriding on every element
        # if isinstance(self, Text):
        #     return '#text'
        # if isinstance(self, Comment):
        # return '#comment'
        # elif isinstance(self, DocumentType):
        #     return '#doctype'
        if isinstance(self, Document):  # NOTE - having this one on breaks parser. as it expects 'html'?
            return "#document"
        if isinstance(self, CDATASection):
            return "#cdata-section"
        elif isinstance(self, DocumentFragment):
            return "#document-fragment"
        elif isinstance(self, Attr):
            return self.name
        elif isinstance(self, ProcessingInstruction):
            return self.target
        elif isinstance(self, DocumentType):
            return self.name

        # print(type(self))
        if isinstance(self, Element):
            return self.tagName  # .upper()
        else:
            try:
                return self.tagName
            except Exception:
                return None

    nodeType: int = ELEMENT_NODE

    @property
    def nodeValue(self) -> str | None:
        """Sets or returns the value of a node"""
        outp = ""
        for each in self.args:
            if type(each) is str:
                outp = outp + each
            else:
                val = each.nodeValue
                if val is not None:
                    outp = outp + val
                else:
                    return None
        if outp == "":
            outp = None
        return outp

    @nodeValue.setter
    def nodeValue(self, content: Any):
        """Sets or returns the value of a node"""
        old_value = self.nodeValue
        self.args = (content,)
        if isinstance(self, CharacterData):
            _queue_mutation_record("characterData", self, old_value=old_value)
        return content

    @property
    def ownerDocument(self) -> "Node | None":
        """Returns the root element (document object) for an element"""
        root = self.rootNode
        if isinstance(root, Document):
            return root
        return getattr(self, "_ownerDocument", None)

    @ownerDocument.setter
    def ownerDocument(self, newOwner: Node | None):  #: Element):
        """Sets the root element (document object) for an element"""
        if newOwner is None:
            return
        self._ownerDocument = newOwner if isinstance(newOwner, Document) else getattr(newOwner, "ownerDocument", None)

    @property
    def rootNode(self) -> "Node":
        """[read-only property returns a Node object representing the topmost node in the tree,
        or the current node if it's the topmost node in the tree]

        Returns:
            [Node]: [the topmost Node in the tree]
        """
        if isinstance(self, Document):
            return self

        node = self
        nxt = self.parentNode
        while nxt is not None:
            node = nxt
            nxt = nxt.parentNode
        return node

    def insertBefore(self, new_node: Node, reference_node: Node | None = None) -> Node:
        """inserts a node before a reference node as a child of a specified parent node.
        this will remove the node from its previous parent node, if any.

        # TODO - can throw value error if wrong ordered params. may be helpful to catch to say so.
        """
        if reference_node is None:
            return self.appendChild(new_node)
        if new_node is reference_node:
            return new_node

        items = _coerce_insertion_nodes(new_node)
        old_documents = [
            (item, _detach_node_for_insertion(item)) for item in items
        ]
        index = self.args.index(reference_node)
        previous_sibling = (
            self.args[index - 1]
            if index > 0 and isinstance(self.args[index - 1], Node)
            else None
        )
        self.args = self.args[:index] + items + self.args[index:]
        for item, old_document in old_documents:
            _connect_inserted_node(self, item, old_document)
        added_nodes = [item for item in items if isinstance(item, Node)]
        if added_nodes:
            _queue_mutation_record(
                "childList",
                self,
                added_nodes=added_nodes,
                previous_sibling=previous_sibling,
                next_sibling=reference_node,
            )
        else:
            return new_node
        _notify_slot_change(self)
        return new_node

    def removeChild(self, node: Node) -> Node | None:
        """removes a child node from the DOM and returns the removed node."""
        for count, each in enumerate(self.args):
            if type(each) == str:
                continue

            if each == node:
                n = node
                previous_sibling = n.previousSibling
                next_sibling = n.nextSibling
                _disconnect_tree(n)
                n.parentNode = None
                replace_args = list(self.args)
                replace_args.remove(node)
                self.args = tuple(replace_args)
                _queue_mutation_record(
                    "childList",
                    self,
                    removed_nodes=(n,),
                    previous_sibling=previous_sibling,
                    next_sibling=next_sibling,
                )
                _notify_slot_change(self)

                return n
            r = each.removeChild(node)
            if r:
                return r

        return None

    def replaceChild(self, newChild: "Node", oldChild: "Node") -> "Node":
        """[Replaces a child node within the given (parent) node.]

        Args:
            newChild ([type]): [a Node object]
            oldChild ([type]): [a Node object]

        Returns:
            [type]: [the old child node]
        """
        if newChild is oldChild:
            return oldChild

        items = _coerce_insertion_nodes(newChild)
        old_documents = [
            (item, _detach_node_for_insertion(item)) for item in items
        ]
        try:
            count = list(self.args).index(oldChild)
        except ValueError:
            return oldChild

        replace_args = list(self.args)
        previous_sibling = (
            replace_args[count - 1]
            if count > 0 and isinstance(replace_args[count - 1], Node)
            else None
        )
        next_sibling = (
            replace_args[count + 1]
            if count + 1 < len(replace_args)
            and isinstance(replace_args[count + 1], Node)
            else None
        )
        if isinstance(oldChild, Node):
            _disconnect_tree(oldChild)
        replace_args[count : count + 1] = list(items)
        self.args = tuple(replace_args)
        for item, old_document in old_documents:
            _connect_inserted_node(self, item, old_document)
        if isinstance(oldChild, Node):
            oldChild.parentNode = None
        _queue_mutation_record(
            "childList",
            self,
            added_nodes=[item for item in items if isinstance(item, Node)],
            removed_nodes=(oldChild,) if isinstance(oldChild, Node) else (),
            previous_sibling=previous_sibling,
            next_sibling=next_sibling,
        )
        _notify_slot_change(self)
        return oldChild
        # for count, each in enumerate(self.args):
        #     if each == oldChild:
        #         n = oldChild
        #         self.removeChild(newChild)  # doc remove child?
        #         list(self.args).remove(oldChild)
        #         list(self.args).insert(count, newChild)
        #         return n

        #     r = each.replaceChild(newChild, oldChild)
        #     if r:
        #         return r

        # return None

    def cloneNode(self, deep: bool = True):
        """Returns a copy."""
        import copy

        if deep:
            return copy.deepcopy(self)
        else:
            clone = copy.copy(self)  # shallow copy
            clone.args = ()
            clone.parentNode = None
            return clone

    def isSameNode(self, node):
        """Checks if two elements are the same node"""
        return self == node

    def isEqualNode(self, node):
        """Checks if two elements are equal"""
        return str(self) == str(node)

    def getRootNode(self, options=None):
        # if options is not None:
        # if options['composed'] = True:
        # TODO - need to implement composed
        return self.rootNode

    def isDefaultNamespace(self, ns):
        """Checks if a namespace is the default namespace"""
        if ns == self.namespaceURI:
            return True
        else:
            return False

    def lookupNamespaceURI(self, ns: str):
        """Returns the namespace URI for a given prefix

        :param ns: prefix - i.e 'xml', 'xlink', 'svg', etc

        """
        from domonic.constants import namespaces

        if ns in namespaces:
            return namespaces[ns]
        else:
            return None

    def lookupPrefix(self, ns):
        """Returns the prefix for a given namespace URI"""
        if ns == self.namespaceURI:
            return self.prefix
        else:
            return None

    @property
    def nextSibling(self):
        """[returns the next sibling of the current node.]"""
        if self.parentNode is None:
            return None
        else:
            for count, node in enumerate(self.parentNode.args):
                if node == self:
                    if count == len(self.parentNode.args) - 1:
                        return None
                    else:
                        return self.parentNode.args[count + 1]

    def normalize(self):
        """Normalize a node's value"""
        return None

    @property
    def previousSibling(self):
        """[returns the previous sibling of the current node.]"""
        if self.parentNode is None:
            return None
        else:
            for count, node in enumerate(self.parentNode.args):
                if node == self:
                    if count == 0:
                        return None
                    else:
                        return self.parentNode.args[count - 1]

    @property
    def textContent(self):
        """Returns the text content of a node and its descendants"""
        # TODO - test- also check difference to nodeValue
        # nodevalue is lvl 1 spec. textcontent is lvl 3 spec.
        outp = ""
        for each in self.args:
            if type(each) is str:
                outp = outp + each
            else:
                val = each.textContent
                if val is not None:
                    outp = outp + val
                else:
                    return None
        if outp == "":
            outp = None
        return outp

    @textContent.setter
    def textContent(self, content):
        """Sets the text content of a node and its descendants"""
        old_value = self.textContent
        removed_nodes = [node for node in self.args if isinstance(node, Node)]
        for node in removed_nodes:
            _disconnect_tree(node)
            node.parentNode = None
        if content in (None, ""):
            self.args = ()
        else:
            self.args = (content,)
        if isinstance(self, CharacterData):
            _queue_mutation_record("characterData", self, old_value=old_value)
        elif removed_nodes:
            _queue_mutation_record("childList", self, removed_nodes=removed_nodes)
        return content

    # def isSupported(self): return False #  🗑
    # getUserData() 🗑️
    # setUserData() 🗑️

    # Non-standard helpers kept for etree-style compatibility.
    # seems to make it work with https://github.com/sissaschool/elementpath
    # if i hack it to allow domonic root nodes

    def iter(self, tag=None):
        """Creates a tree iterator with the current element as the root.
        The iterator iterates over this element and all elements below it, in document (depth first) order.
        If tag is not None or '*', only elements whose tag equals tag are returned from the iterator.
        If the tree structure is modified during iteration, the result is undefined."""
        for each in self.args:
            if type(each) is str:
                continue
            if tag is None or tag == "*":
                yield each
            elif each.tag == tag:
                yield each
            for x in each.iter(tag):
                yield x

    @property
    def tag(self):
        """Returns the tag name of the current node"""
        return self.nodeName
        # return self.tagName  # not sure current is correct as would return #nodeName

    @property
    def text(self):
        """Returns the text content of the current node"""
        return self.textContent

    @property
    def attrib(self):
        """Returns the attributes of the current node as a dict not a NamedNodeMap"""
        try:
            # print(self.kwargs)
            return self.kwargs
        except Exception as e:
            # print('failed::', e)
            return None

    @property
    def tail(self):
        """Returns the text content of the current node"""
        return self.textContent

    @property
    def length(self) -> int:
        return len(self)

    def is_matching(self, name, default_namespace=None):
        """
        Determine if this node matches the given name and namespace.
        """
        if name and name != self.tagName:
            return False
        if default_namespace and getattr(self, 'namespace', None) != default_namespace:
            return False
        return True



class ParentNode:
    """not tested yet"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # @property
    # def childElementCount(self):
    #     return len(self.args)

    @property
    def children(self) -> "NodeList":
        """Return list of child nodes."""
        return NodeList([e for e in self.childNodes if e.nodeType == Node.ELEMENT_NODE])

    @property
    def firstElementChild(self):
        """First Element child node."""
        for child in self.childNodes:
            if child.nodeType == Node.ELEMENT_NODE:
                return child
        return None

    @property
    def lastElementChild(self):
        """Last Element child node."""
        for child in reversed(self.childNodes):  # type: ignore
            if child.nodeType == Node.ELEMENT_NODE:
                return child
        return None

    def append(self, *args):
        self.args += _coerce_insertion_nodes(*args)
        self._update_parents()
        return self

    def prepend(self, *args):
        self.args = _coerce_insertion_nodes(*args) + tuple(self.args)
        self._update_parents()
        return self

    def replaceChildren(self, *children):
        self.args = _coerce_replacement_nodes(*children)
        self._update_parents()


class ChildNode(Node):
    """not tested yet"""

    def remove(self):
        """Removes this ChildNode from the children list of its parent."""
        if self.parentNode is None:
            self._update_parents()
        if self.parentNode is not None:
            self.parentNode.removeChild(self)
        return self

    def replaceWith(self, *nodes):
        """Replaces this ChildNode with one or more nodes or strings."""
        if self.parentNode is None:
            return self
        replacement = DocumentFragment(*_coerce_replacement_nodes(*nodes))
        self.parentNode.replaceChild(replacement, self)
        return self

    def before(self, *nodes):
        """Inserts one or more nodes or strings immediately before this ChildNode."""
        if self.parentNode is None:
            return self
        insertion = DocumentFragment(*_coerce_insertion_nodes(*nodes))
        self.parentNode.insertBefore(insertion, self)
        return self

    def after(self, *nodes):
        """Inserts one or more nodes or strings immediately after this ChildNode."""
        if self.parentNode is None:
            return self
        siblings = list(self.parentNode.childNodes)
        index = siblings.index(self)
        reference = siblings[index + 1] if index + 1 < len(siblings) else None
        insertion = DocumentFragment(*_coerce_insertion_nodes(*nodes))
        self.parentNode.insertBefore(insertion, reference)
        return self


class Attr(Node):
    # https://developer.mozilla.org/en-US/docs/Web/API/Attr

    nodeType: int = Node.ATTRIBUTE_NODE
    __slots__ = ("name", "value")

    def __init__(self, name: str, value="", *args, **kwargs) -> None:
        self.name: str = name
        self.value = value
        # self.nodeType: int = Node.ATTRIBUTE_NODE

    @property
    def isId(self) -> bool:
        if self.name == "id":
            return True
        else:
            return False

    def getNamedItem(self, name: str):
        """Returns a specified attribute node from a NamedNodeMap"""
        for item in self.parentNode.attributes:
            if item.name == name:
                return item
        return None

    # def __getitem__(self, name):
    #     return self.getNamedItem(name)

    # def __setitem__(self, name, value):
    #     self.setNamedItem(name, value)

    def removeNamedItem(self, name: str) -> bool:
        """Removes a specified attribute node"""
        for item in self.parentNode.attributes:
            if item.name == name:
                self.parentNode.removeAttribute(item)
                return True
        return False

    def setNamedItem(self, name: str, value) -> bool:
        """Sets the specified attribute node (by name)"""
        for item in self.parentNode.attributes:
            if item.name == name:
                item.value = value
                return True
        return False

class NamedNodeMap:
    """Live attribute collection exposed by ``Element.attributes``.

    ``NamedNodeMap`` behaves like the DOM interface rather than a plain Python
    dict: it is ordered, can be accessed by index or attribute name, and stays
    in sync with the owning element's current attributes.
    """

    def __init__(self, args: Iterable[Attr] | None = None, ownerDocument=None, parentNode=None):
        self.parentNode = parentNode
        self.ownerDocument = ownerDocument
        self._attrs = list(args or [])

    def _normalize_name(self, name: str) -> str:
        return name[1:] if isinstance(name, str) and name.startswith("_") else name

    def _storage_key(self, name: str) -> str:
        normalized = self._normalize_name(name)
        return normalized if normalized.startswith("_") else f"_{normalized}"

    def _current_attrs(self) -> list[Attr]:
        if self.parentNode is not None and hasattr(self.parentNode, "kwargs"):
            return [Attr(key.lstrip("_"), value) for key, value in self.parentNode.kwargs.items()]
        return list(self._attrs)

    def _attribute_namespace(self, attr: Attr) -> str | None:
        if ":" not in attr.name or self.parentNode is None:
            return None
        prefix = attr.name.split(":", 1)[0]
        return self.parentNode.lookupNamespaceURI(prefix)

    @property
    def length(self) -> int:
        return len(self._current_attrs())

    def __len__(self) -> int:
        return self.length

    def __iter__(self) -> Iterator[Attr]:
        return iter(self._current_attrs())

    def __contains__(self, item: Any) -> bool:
        if isinstance(item, Attr):
            return self.getNamedItem(item.name) is not None
        if isinstance(item, str):
            return self.getNamedItem(item) is not None
        return False

    def __getitem__(self, key: int | str) -> Attr:
        if isinstance(key, int):
            item = self.item(key)
            if item is None:
                raise IndexError(key)
            return item
        item = self.getNamedItem(key)
        if item is None:
            raise KeyError(key)
        return item

    def __setitem__(self, key: str, value: Attr | Any) -> None:
        if isinstance(value, Attr):
            value.name = self._normalize_name(key)
            self.setNamedItem(value)
            return
        self.setNamedItem(Attr(self._normalize_name(key), value))

    def __delitem__(self, key: str) -> None:
        removed = self.removeNamedItem(key)
        if removed is None:
            raise KeyError(key)

    def item(self, index: int) -> Attr | None:
        if not isinstance(index, int):
            raise TypeError("index must be an integer")
        attrs = self._current_attrs()
        return attrs[index] if 0 <= index < len(attrs) else None

    def getNamedItem(self, name: str) -> Attr | None:
        normalized = self._normalize_name(name)
        for item in self._current_attrs():
            if item.name == normalized:
                return item
        return None

    def setNamedItem(self, attr: Attr) -> Attr | None:
        normalized = self._normalize_name(attr.name)
        old_attr = self.getNamedItem(normalized)
        attr.name = normalized
        if self.parentNode is not None and hasattr(self.parentNode, "kwargs"):
            self.parentNode.setAttribute(normalized, attr.value)
        else:
            self._attrs = [existing for existing in self._attrs if existing.name != normalized]
            self._attrs.append(Attr(normalized, attr.value))
        return old_attr

    def removeNamedItem(self, name: str) -> Attr | None:
        normalized = self._normalize_name(name)
        old_attr = self.getNamedItem(normalized)
        if old_attr is None:
            return None
        if self.parentNode is not None and hasattr(self.parentNode, "kwargs"):
            self.parentNode.removeAttribute(normalized)
        else:
            self._attrs = [existing for existing in self._attrs if existing.name != normalized]
        return old_attr

    def getNamedItemNS(self, namespaceURI: str, localName: str) -> Attr | None:
        normalized = self._normalize_name(localName)
        for item in self._current_attrs():
            item_local_name = item.name.split(":", 1)[-1]
            if item_local_name == normalized and self._attribute_namespace(item) == namespaceURI:
                return item
        return None

    def setNamedItemNS(self, attr: Attr) -> Attr | None:
        return self.setNamedItem(attr)

    def removeNamedItemNS(self, namespaceURI: str, localName: str) -> Attr | None:
        attr = self.getNamedItemNS(namespaceURI, localName)
        if attr is None:
            return None
        return self.removeNamedItem(attr.name)

    def keys(self) -> list[str]:
        return [attr.name for attr in self._current_attrs()]

    def values(self) -> list[Attr]:
        return self._current_attrs()

    def items(self) -> list[tuple[str, Attr]]:
        return [(attr.name, attr) for attr in self._current_attrs()]


class DOMStringMap:
    """Dictionary-like helper for element dataset values."""

    def __init__(self, *args, element: "Element | None" = None, **kwargs):
        self._element = element
        self._store: dict[str, Any] = dict(*args, **kwargs)
        super().__init__()

    @staticmethod
    def _attribute_name(name: str) -> str:
        from domonic.utils import Utils

        return f"data-{Utils.case_kebab(str(name))}"

    @staticmethod
    def _property_name(attribute: str) -> str:
        from domonic.utils import Utils

        return Utils.case_camel(attribute[5:])

    def _data(self) -> dict[str, Any]:
        if self._element is None:
            return self._store

        data: dict[str, Any] = {}
        for key, value in self._element.kwargs.items():
            attr_name = key[1:] if key.startswith("_") else key
            if attr_name.startswith("data-") and len(attr_name) > 5:
                data[self._property_name(attr_name)] = value
        return data

    def __getitem__(self, name: str) -> Any:
        return self._data()[name]

    def __setitem__(self, name: str, value: Any) -> None:
        if self._element is not None:
            self._element.setAttribute(self._attribute_name(name), value)
            return
        self._store[name] = value

    def __delitem__(self, name: str) -> None:
        if self._element is not None:
            self._element.removeAttribute(self._attribute_name(name))
            return
        del self._store[name]

    def __contains__(self, name: str) -> bool:
        return name in self._data()

    def __iter__(self):
        return iter(self._data())

    def __len__(self) -> int:
        return len(self._data())

    def keys(self):
        return self._data().keys()

    def values(self):
        return self._data().values()

    def items(self):
        return self._data().items()

    def __repr__(self) -> str:
        return repr(self._data())

    def get(self, name: str):
        """Returns the value of the item with the specified name"""
        return self._data().get(name)

    def set(self, name: str, value):
        """Sets the value of the item with the specified name"""
        self[name] = value
        return True

    def delete(self, name: str) -> bool:
        """Deletes the item with the specified name"""
        if name in self:
            del self[name]
            return True
        return False

    # def has(self, name):
    #     """ Returns true if the specified name exists """
    #     for item in self.args:
    #         if item.name == name:
    #             return True
    #     return False

    # def clear(self):
    #     """ Removes all items from the map """
    #     self.args = []
    #     return True

    # def keys(self):
    #     """ Returns an array of all the names in the map """
    #     return [item.name for item in self.args]

    # def values(self):
    #     """ Returns an array of all the values in the map """
    #     return [item.value for item in self.args]


class DOMRectReadOnly:
    """Read-only rectangle object for DOM geometry APIs."""

    @staticmethod
    def fromRect(other: Any | None = None) -> "DOMRectReadOnly":
        if other is None:
            return DOMRectReadOnly()
        return DOMRectReadOnly(
            getattr(other, "x", 0),
            getattr(other, "y", 0),
            getattr(other, "width", 0),
            getattr(other, "height", 0),
        )

    def __init__(self, x: float = 0, y: float = 0, width: float = 0, height: float = 0):
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def width(self) -> float:
        return self._width

    @property
    def height(self) -> float:
        return self._height

    @property
    def top(self) -> float:
        return min(self._y, self._y + self._height)

    @property
    def right(self) -> float:
        return max(self._x, self._x + self._width)

    @property
    def bottom(self) -> float:
        return max(self._y, self._y + self._height)

    @property
    def left(self) -> float:
        return min(self._x, self._x + self._width)

    def toJSON(self):
        return {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "top": self.top,
            "right": self.right,
            "bottom": self.bottom,
            "left": self.left,
        }


class DOMRect(DOMRectReadOnly):
    """Mutable rectangle object for DOM geometry APIs."""

    @staticmethod
    def fromRect(other: Any | None = None) -> "DOMRect":
        rect = DOMRectReadOnly.fromRect(other)
        return DOMRect(rect.x, rect.y, rect.width, rect.height)

    @DOMRectReadOnly.x.setter
    def x(self, value: float) -> None:
        self._x = value

    @DOMRectReadOnly.y.setter
    def y(self, value: float) -> None:
        self._y = value

    @DOMRectReadOnly.width.setter
    def width(self, value: float) -> None:
        self._width = value

    @DOMRectReadOnly.height.setter
    def height(self, value: float) -> None:
        self._height = value


class DOMRectList(list):
    """An ordered collection of DOMRect objects."""

    @property
    def length(self) -> int:
        return len(self)

    def item(self, index: int) -> DOMRect | None:
        if not isinstance(index, int):
            raise TypeError("index must be an integer")
        return self[index] if 0 <= index < len(self) else None


class DocumentTimeline:
    """Document-associated timeline used by animation surfaces.

    This is the timing source behind ``document.timeline`` and
    ``Element.animate(...)``.
    """

    def __init__(self, document: "Document | None" = None, originTime: float = 0.0):
        self.document = document
        self.originTime = float(originTime)
        self._started_at = time.perf_counter()

    @property
    def currentTime(self) -> float:
        return self.originTime + ((time.perf_counter() - self._started_at) * 1000.0)


class CaretPosition:
    """Represents a caret location as a node plus offset pair."""

    def __init__(self, offsetNode: Node | None = None, offset: int = 0) -> None:
        self.offsetNode = offsetNode
        self.offset = offset

    def getClientRect(self) -> DOMRect:
        if hasattr(self.offsetNode, "getBoundingClientRect"):
            return self.offsetNode.getBoundingClientRect()
        return DOMRect(0, 0, 0, 0)


class Selection:
    """Represents the user's current selection within a document or shadow tree.

    Domonic keeps both ordered ``Range`` data and anchor/focus information so
    selection direction can still be represented.
    """

    def __init__(self) -> None:
        self._ranges: list[Range] = []
        self._anchorNode: Node | None = None
        self._anchorOffset: int = 0
        self._focusNode: Node | None = None
        self._focusOffset: int = 0

    def _set_anchor_focus(
        self,
        anchorNode: Node | None,
        anchorOffset: int = 0,
        focusNode: Node | None = None,
        focusOffset: int = 0,
    ) -> None:
        self._anchorNode = anchorNode
        self._anchorOffset = anchorOffset
        self._focusNode = anchorNode if focusNode is None else focusNode
        self._focusOffset = anchorOffset if focusNode is None else focusOffset

    def _sync_anchor_focus_from_range(self, range_obj: "Range | None") -> None:
        if range_obj is None:
            self._set_anchor_focus(None, 0, None, 0)
            return
        self._set_anchor_focus(
            range_obj.startContainer,
            range_obj.startOffset,
            range_obj.endContainer,
            range_obj.endOffset,
        )

    @property
    def rangeCount(self) -> int:
        return len(self._ranges)

    @property
    def isCollapsed(self) -> bool:
        return self.rangeCount == 0 or all(range_obj.collapsed for range_obj in self._ranges)

    @property
    def anchorNode(self) -> Node | None:
        return self._anchorNode if self._ranges else None

    @property
    def anchorOffset(self) -> int:
        return self._anchorOffset if self._ranges else 0

    @property
    def focusNode(self) -> Node | None:
        return self._focusNode if self._ranges else None

    @property
    def focusOffset(self) -> int:
        return self._focusOffset if self._ranges else 0

    @property
    def type(self) -> str:
        if self.rangeCount == 0:
            return "None"
        return "Caret" if self.isCollapsed else "Range"

    def addRange(self, range_obj: "Range") -> None:
        if range_obj not in self._ranges:
            self._ranges.append(range_obj)
            if len(self._ranges) == 1:
                self._sync_anchor_focus_from_range(range_obj)

    def removeRange(self, range_obj: "Range") -> None:
        self._ranges = [candidate for candidate in self._ranges if candidate is not range_obj]
        self._sync_anchor_focus_from_range(self._ranges[0] if self._ranges else None)

    def removeAllRanges(self) -> None:
        self._ranges = []
        self._sync_anchor_focus_from_range(None)

    def getRangeAt(self, index: int) -> "Range":
        if index < 0 or index >= len(self._ranges):
            raise IndexError("Selection range index out of range")
        return self._ranges[index]

    def collapse(self, node: Node | None, offset: int = 0) -> None:
        if node is None:
            self.removeAllRanges()
            return
        range_obj = Range()
        range_obj.setStart(node, offset)
        range_obj.setEnd(node, offset)
        self._ranges = [range_obj]
        self._set_anchor_focus(node, offset, node, offset)

    def collapseToStart(self) -> None:
        if not self._ranges:
            return
        first = self._ranges[0]
        self.collapse(first.startContainer, first.startOffset)

    def collapseToEnd(self) -> None:
        if not self._ranges:
            return
        last = self._ranges[-1]
        self.collapse(last.endContainer, last.endOffset)

    def extend(self, node: Node, offset: int = 0) -> None:
        if not self._ranges:
            self.collapse(node, offset)
            return
        anchor_node = self.anchorNode
        anchor_offset = self.anchorOffset
        active_range = self._ranges[-1]
        if anchor_node is None:
            active_range.setEnd(node, offset)
            self._set_anchor_focus(active_range.startContainer, active_range.startOffset, node, offset)
            return
        if Range._compare_points(anchor_node, anchor_offset, node, offset) <= 0:
            active_range.setStart(anchor_node, anchor_offset)
            active_range.setEnd(node, offset)
        else:
            active_range.setStart(node, offset)
            active_range.setEnd(anchor_node, anchor_offset)
        self._set_anchor_focus(anchor_node, anchor_offset, node, offset)

    def setBaseAndExtent(
        self,
        anchorNode: Node,
        anchorOffset: int,
        focusNode: Node,
        focusOffset: int,
    ) -> None:
        range_obj = Range()
        if Range._compare_points(anchorNode, anchorOffset, focusNode, focusOffset) <= 0:
            range_obj.setStart(anchorNode, anchorOffset)
            range_obj.setEnd(focusNode, focusOffset)
        else:
            range_obj.setStart(focusNode, focusOffset)
            range_obj.setEnd(anchorNode, anchorOffset)
        self._ranges = [range_obj]
        self._set_anchor_focus(anchorNode, anchorOffset, focusNode, focusOffset)

    def empty(self) -> None:
        self.removeAllRanges()

    def selectAllChildren(self, node: "Node") -> None:
        range_obj = Range()
        range_obj.selectNodeContents(node)
        self._ranges = [range_obj]
        self._set_anchor_focus(node, 0, node, Range._container_length(node))

    def deleteFromDocument(self) -> None:
        for range_obj in list(self._ranges):
            range_obj.deleteContents()
        self.removeAllRanges()

    def containsNode(self, node: Node | None, allowPartialContainment: bool = False) -> bool:
        if node is None:
            return False

        if isinstance(node, Text):
            node_end_offset = len(node.textContent)
        else:
            node_end_offset = len(list(getattr(node, "childNodes", [])))

        for range_obj in self._ranges:
            start_relation = range_obj.comparePoint(node, 0)
            end_relation = range_obj.comparePoint(node, node_end_offset)
            if allowPartialContainment:
                if start_relation != 1 and end_relation != -1:
                    return True
            else:
                if start_relation == 0 and end_relation == 0:
                    return True
        return False

    def toString(self) -> str:
        return "".join(range_obj.toString() for range_obj in self._ranges)

    __str__ = toString


class DOMTokenList(list):
    """DOMTokenList represents a set of space-separated tokens."""

    def __init__(self, element: "Node"):
        self.el = element
        tokens = self._tokens_from_element()
        self.classes = tokens
        super().__init__(tokens)

    def _tokens_from_element(self) -> list[str]:
        tokens = []
        for token in str(self.el.className or "").split():
            if token not in tokens:
                tokens.append(token)
        return tokens

    def _reload(self) -> None:
        tokens = self._tokens_from_element()
        if tokens != list(list.__iter__(self)):
            list.clear(self)
            list.extend(self, tokens)
        self.classes = tokens

    @staticmethod
    def _validate_token(token) -> str:
        token = str(token)
        if token == "":
            raise ValueError("DOMTokenList token must not be empty")
        if any(char.isspace() for char in token):
            raise ValueError("DOMTokenList token must not contain whitespace")
        return token

    def _sync(self) -> None:
        self.classes = list(list.__iter__(self))
        self.el.className = " ".join(self.classes)

    @property
    def length(self) -> int:
        self._reload()
        return list.__len__(self)

    def __len__(self) -> int:
        return self.length

    def __iter__(self):
        self._reload()
        return list.__iter__(self)

    def __contains__(self, token) -> bool:
        self._reload()
        return list.__contains__(self, token)

    def __getitem__(self, index):
        self._reload()
        return list.__getitem__(self, index)

    def __eq__(self, other):
        self._reload()
        return list(list.__iter__(self)) == other

    def add(self, *args):
        """Adds the given tokens to the list"""
        self._reload()
        for item in args:
            token = self._validate_token(item)
            if not list.__contains__(self, token):
                list.append(self, token)
        self._sync()

    def remove(self, *args):
        """Removes the given tokens from the list"""
        self._reload()
        for item in args:
            token = self._validate_token(item)
            while list.__contains__(self, token):
                list.remove(self, token)
        self._sync()

    def toggle(self, token, force=None):
        """If force is not given, removes token from list if present,
        otherwise adds token to list. If force is true, adds token to list,
        and if force is false, removes token from list if present."""
        token = self._validate_token(token)
        self._reload()
        if force is None:
            if list.__contains__(self, token):
                self.remove(token)
                return False
            else:
                self.add(token)
                return True
        elif force is True:
            self.add(token)
            return True
        elif force is False:
            self.remove(token)
            return False
        else:
            raise TypeError("force must be a boolean")

    def replace(self, token, newToken) -> bool:
        """Replaces an existing token with a new token."""
        token = self._validate_token(token)
        newToken = self._validate_token(newToken)
        self._reload()
        if not list.__contains__(self, token):
            return False
        if token == newToken:
            self._sync()
            return True

        index = list.index(self, token)
        if list.__contains__(self, newToken):
            list.remove(self, token)
        else:
            list.__setitem__(self, index, newToken)
        self._sync()
        return True

    def contains(self, token) -> bool:
        """Returns true if the token is in the list, and false otherwise"""
        # return token in self.el.className
        token = self._validate_token(token)
        return token in self

    def item(self, index: int):
        """Returns the token at the specified index"""
        self._reload()
        return list.__getitem__(self, index) if 0 <= index < list.__len__(self) else None

    def toString(self) -> str:
        """Returns a string containing all tokens in the list, with spaces separating each token"""
        self._reload()
        return " ".join(list.__iter__(self))

    def entries(self) -> Iterable[tuple[int, str]]:
        """Returns an iterator over index/token pairs."""
        self._reload()
        for i in range(len(self)):
            yield i, list.__getitem__(self, i)

    def forEach(self, func: Callable[[str, int, "DOMTokenList"], Any], thisArg: Any = None) -> None:
        """Calls a function for each token in the list."""
        self._reload()
        for i in range(len(self)):
            func(list.__getitem__(self, i), i, self)

    def keys(self) -> Iterable[int]:
        """Returns an iterator over token indexes."""
        self._reload()
        return iter(range(len(self)))

    def values(self) -> Iterable[str]:
        """Returns an iterator over tokens."""
        self._reload()
        return list.__iter__(self)

    def __str__(self):
        return self.toString()


class ShadowRoot(Node):  # TODO - this may need to extend tag also to get the args/kwargs
    """property on element that has hidden DOM"""

    def __init__(self, host, mode="open"):
        self.adoptedStyleSheets = []
        self.delegatesFocus = False
        self.host = host
        self.mode = mode
        self.parentNode = host
        self._selection = Selection()
        super().__init__()

    def elementFromPoint(self, x: float, y: float) -> Element | None:
        """Returns the topmost element at the specified coordinates."""
        hits = self.elementsFromPoint(x, y)
        return hits[0] if hits else None

    def getSelection(self) -> Selection:
        """Returns a Selection object for the document."""
        if not hasattr(self, "_selection"):
            self._selection = Selection()
        return self._selection

    def elementsFromPoint(self, x: float, y: float) -> list[Element]:
        """Returns an array of all elements at the specified coordinates."""
        matches = []

        def walk(node):
            if not isinstance(node, Element):
                return
            rect = node.getBoundingClientRect()
            if rect.left <= x <= rect.right and rect.top <= y <= rect.bottom:
                matches.append(node)
            for child in getattr(node, "childNodes", []):
                walk(child)

        for child in self.childNodes:
            walk(child)
        return matches

    def caretPositionFromPoint(self, x: float = 0, y: float = 0) -> CaretPosition | None:
        """
        Returns a CaretPosition object containing the DOM node containing the caret,
        and caret's character offset within that node.
        """
        target = self.elementFromPoint(x, y)
        if target is None:
            return None
        first_child = target.firstChild
        if isinstance(first_child, Text):
            rect = target.getBoundingClientRect()
            width = max(rect.width, 1)
            text_length = len(first_child.textContent)
            relative = max(0, min(x - rect.left, width))
            offset = min(text_length, int((relative / width) * text_length))
            return CaretPosition(first_child, offset)
        return CaretPosition(target, 0)


class DocumentType(Node):

    nodeType = Node.DOCUMENT_TYPE_NODE
    __slots__ = ("name", "publicId", "systemId")

    def __init__(self, name: str = "html", publicId: str = "", systemId: str = "") -> None:
        self.name: str = name  # A DOMString, eg "html" for <!DOCTYPE HTML>.
        self.publicId: str = publicId  # eg "-//W3C//DTD HTML 4.01//EN", empty string for HTML5.
        self.systemId: str = systemId  # eg "http://www.w3.org/TR/html4/strict.dtd", empty string for HTML5.
        super().__init__()

    def internalSubset(self):
        """A DOMString of the internal subset, or None. Eg "<!ELEMENT foo (bar)>"."""
        if self.systemId:
            return self.systemId
        else:
            return None

    def notations(self) -> NamedNodeMap:
        """A NamedNodeMap with notations declared in the DTD."""
        nnm = NamedNodeMap()
        for item in self.ownerDocument.args:
            if item.nodeType == Node.NOTATION_NODE:
                nnm.append(item)
        return nnm

    def __str__(self) -> str:
        # return f"<!DOCTYPE {self.name} {self.publicId} {self.systemId}>"
        # TODO fix broken spacing when no publicId or systemId
        full_str = f"<!DOCTYPE {self.name}"
        if self.publicId:
            full_str += f" PUBLIC {self.publicId}"
        if self.systemId:
            full_str += f" SYSTEM {self.systemId}"
        full_str += ">"
        return full_str


"""
def AriaMixin():  # ???

    @property
    def ariaAtomic(self):
        return self.getAttribute('aria-atomic')

    @ariaAtomic.setter
    def ariaAtomic(self, value: str):
        self.setAttribute('aria-atomic', value)

    @property
    def ariaAtomic(self):
        return self.getAttribute('aria-atomic')

    @property
    def ariaAutoComplete(self):
        return self.getAttribute('aria-autoComplete')

    @ariaAutoComplete.setter
    def ariaAutoComplete(self, value: str):
        return self.getAttribute('aria-autoComplete')

    @property
    def ariaBusy(self):
        return self.getAttribute('aria-busy')

    @ariaBusy.setter
    def ariaBusy(self, value: str):
        return self.getAttribute('aria-busy')

    @property
    def ariaChecked(self):
        return self.getAttribute('aria-checked')

    @ariaChecked.setter
    def ariaChecked(self, value: str):
        return self.getAttribute('aria-checked')

    @property
    def ariaColCount(self):
        return self.getAttribute('aria-colCount')

    @ariaColCount.setter
    def ariaColCount(self, value: str):
        return self.getAttribute('aria-colCount')

    @property
    def ariaColIndex(self):
        return self.getAttribute('aria-colIndex')

    @ariaColIndex.setter
    def ariaColIndex(self, value: str):
        return self.getAttribute('aria-colIndex')

    @property
    def ariaColIndexText(self):
        return self.getAttribute('aria-colIndexText')

    @ariaColIndexText.setter
    def ariaColIndexText(self, value: str):
        return self.getAttribute('aria-colIndexText')

    @property
    def ariaColSpan(self):
        return self.getAttribute('aria-colSpan')

    @ariaColSpan.setter
    def ariaColSpan(self, value: str):
        return self.getAttribute('aria-colSpan')

    @property
    def ariaCurrent(self):
        return self.getAttribute('aria-current')

    @ariaCurrent.setter
    def ariaCurrent(self, value: str):
        return self.getAttribute('aria-current')

    @property
    def ariaDescription(self):
        return self.getAttribute('aria-description')

    @ariaDescription.setter
    def ariaDescription(self, value: str):
        return self.getAttribute('aria-description')

    @property
    def ariaDisabled(self):
        return self.getAttribute('aria-disabled')

    @ariaDisabled.setter
    def ariaDisabled(self, value: str):
        return self.getAttribute('aria-disabled')

    @property
    def ariaExpanded(self):
        return self.getAttribute('aria-expanded')

    @ariaExpanded.setter
    def ariaExpanded(self, value: str):
        return self.getAttribute('aria-expanded')

    @property
    def ariaHasPopup(self):
        return self.getAttribute('aria-hasPopup')

    @ariaHasPopup.setter
    def ariaHasPopup(self, value: str):
        return self.getAttribute('aria-hasPopup')

    @property
    def ariaHidden(self):
        return self.getAttribute('aria-hidden')

    @ariaHidden.setter
    def ariaHidden(self, value: str):
        return self.getAttribute('aria-hidden')

    @property
    def ariaKeyShortcuts(self):
        return self.getAttribute('aria-keyShortcuts')

    @ariaKeyShortcuts.setter
    def ariaKeyShortcuts(self, value: str):
        return self.getAttribute('aria-keyShortcuts')

    @property
    def ariaLabel(self):
        return self.getAttribute('aria-label')

    @ariaLabel.setter
    def ariaLabel(self, value: str):
        return self.getAttribute('aria-label')

    @property
    def ariaLevel(self):
        return self.getAttribute('aria-level')

    @ariaLevel.setter
    def ariaLevel(self, value: str):
        return self.getAttribute('aria-level')

    @property
    def ariaLive(self):
        return self.getAttribute('aria-live')

    @ariaLive.setter
    def ariaLive(self, value: str):
        return self.getAttribute('aria-live')

    @property
    def ariaModal(self):
        return self.getAttribute('aria-modal')

    @ariaModal.setter
    def ariaModal(self, value: str):
        return self.getAttribute('aria-modal')

    @property
    def ariaMultiline(self):
        return self.getAttribute('aria-multiline')

    @ariaMultiline.setter
    def ariaMultiline(self, value: str):
        return self.getAttribute('aria-multiline')

    @property
    def ariaMultiSelectable(self):
        return self.getAttribute('aria-multiSelectable')

    @ariaMultiSelectable.setter
    def ariaMultiSelectable(self, value: str):
        return self.getAttribute('aria-multiSelectable')

    @property
    def ariaOrientation(self):
        return self.getAttribute('aria-orientation')

    @ariaOrientation.setter
    def ariaOrientation(self, value: str):
        return self.getAttribute('aria-orientation')

    @property
    def ariaPlaceholder(self):
        return self.getAttribute('aria-placeholder')

    @ariaPlaceholder.setter
    def ariaPlaceholder(self, value: str):
        return self.getAttribute('aria-placeholder')

    @property
    def ariaPosInSet(self):
        return self.getAttribute('aria-posInSet')

    @ariaPosInSet.setter
    def ariaPosInSet(self, value: str):
        return self.getAttribute('aria-posInSet')

    @property
    def ariaPressed(self):
        return self.getAttribute('aria-pressed')

    @ariaPressed.setter
    def ariaPressed(self, value: str):
        return self.getAttribute('aria-pressed')

    @property
    def ariaReadOnly(self):
        return self.getAttribute('aria-readOnly')

    @ariaReadOnly.setter
    def ariaReadOnly(self, value: str):
        return self.getAttribute('aria-readOnly')

    @property
    def ariaRelevant(self):
        return self.getAttribute('aria-relevant')

    @ariaRelevant.setter
    def ariaRelevant(self, value: str):
        return self.getAttribute('aria-relevant')

    @property
    def ariaRequired(self):
        return self.getAttribute('aria-required')

    @ariaRequired.setter
    def ariaRequired(self, value: str):
        return self.getAttribute('aria-required')

    @property
    def ariaRoleDescription(self):
        return self.getAttribute('aria-roleDescription')

    @ariaRoleDescription.setter
    def ariaRoleDescription(self, value: str):
        return self.getAttribute('aria-roleDescription')

    @property
    def ariaRowCount(self):
        return self.getAttribute('aria-rowCount')

    @ariaRowCount.setter
    def ariaRowCount(self, value: str):
        return self.getAttribute('aria-rowCount')

    @property
    def ariaRowIndex(self):
        return self.getAttribute('aria-rowIndex')

    @ariaRowIndex.setter
    def ariaRowIndex(self, value: str):
        return self.getAttribute('aria-rowIndex')

    @property
    def ariaRowIndexText(self):
        return self.getAttribute('aria-rowIndexText')

    @ariaRowIndexText.setter
    def ariaRowIndexText(self, value: str):
        return self.getAttribute('aria-rowIndexText')

    @property
    def ariaRowSpan(self):
        return self.getAttribute('aria-rowSpan')

    @ariaRowSpan.setter
    def ariaRowSpan(self, value: str):
        return self.getAttribute('aria-rowSpan')

    @property
    def ariaSelected(self):
        return self.getAttribute('aria-selected')

    @ariaSelected.setter
    def ariaSelected(self, value: str):
        return self.getAttribute('aria-selected')

    @property
    def ariaSetSize(self):
        return self.getAttribute('aria-setSize')

    @ariaSetSize.setter
    def ariaSetSize(self, value: str):
        return self.getAttribute('aria-setSize')

    @property
    def ariaSort(self):
        return self.getAttribute('aria-sort')

    @ariaSort.setter
    def ariaSort(self, value: str):
        return self.getAttribute('aria-sort')

    @property
    def ariaValueMax(self):
        return self.getAttribute('aria-valueMax')

    @ariaValueMax.setter
    def ariaValueMax(self, value: str):
        return self.getAttribute('aria-valueMax')

    @property
    def ariaValueMin(self):
        return self.getAttribute('aria-valueMin')

    @ariaValueMin.setter
    def ariaValueMin(self, value: str):
        return self.getAttribute('aria-valueMin')

    @property
    def ariaValueNow(self):
        return self.getAttribute('aria-valueNow')

    @ariaValueNow.setter
    def ariaValueNow(self, value: str):
        return self.getAttribute('aria-valueNow')

    @property
    def ariaValueText(self):
        return self.getAttribute('aria-valueText')

    @ariaValueText.setter
    def ariaValueText(self, value: str):
        return self.getAttribute('aria-valueText')

# class ElementInternals(object, AriaMixin):
#     def __init__(self, element):
#         self.element = element
#         self.shadowRoot = None # Returns the ShadowRoot object associated with this element.
#         self.form  # Returns the HTMLFormElement associated with this element.
#         self.states  # Returns the CustomStateSet associated with this element.
#         self.willValidate # A boolean value which returns true if the element is a submittable element that is a candidate for constraint validation.
#         self.validity  # Returns a ValidityState object which represents the different validity states the element can be in, with respect to constraint validation.
#         self.validationMessage  # A string containing the validation message of this element.
#         self.labels  # Returns a NodeList of all of the label elements associated with this element.


class CustomStateSet:

    def __init__(self):
        pass

    def add(self, state):
        pass

    def clear(self):
        pass

    def delete(self, state):
        pass

"""


class NodeList(list):
    """NodeList objects are collections of nodes"""

    @property
    def length(self) -> int:
        return len(self)

    def item(self, index: int) -> Node | None:
        """Returns an item in the list by its index, or null if the index is out-of-bounds."""
        # An alternative to accessing nodeList[i] (which instead returns  undefined when i is out-of-bounds).
        # This is mostly useful for non-JavaScript DOM implementations.
        try:
            return self[index] if 0 <= index < self.length else None
        except IndexError:
            return None

    # def items(self):
    #     """ Returns a list of the nodes in the list."""
    #     return self

    def entries(self) -> Iterable[tuple[int, Node]]:
        """Returns an iterator, allowing code to go through all key/value pairs contained in the collection.
        (In this case, the keys are numbers starting from 0 and the values are nodes."""
        # i.e.  Array [ 0, <p> ]
        for i in range(len(self)):
            yield i, self[i]

    def forEach(self, func: Callable[[Node, int, "NodeList"], Any], thisArg: Any = None) -> None:
        """Calls a function for each item in the NodeList."""
        # thisArg = thisArg or self
        for i in range(len(self)):
            func(self[i], i, self)

    def keys(self) -> Iterable[int]:
        """Returns an iterator, allowing code to go through all the keys of the key/value pairs contained in the collection.
        (In this case, the keys are numbers starting from 0.)"""
        return iter(range(len(self)))

    def values(self) -> Iterable[Node]:
        """Returns an iterator allowing code to go through all values (nodes) of the key/value pairs
        contained in the collection."""
        return iter(self)


class RadioNodeList(NodeList):
    """A live collection of form controls sharing an id or name."""

    def __init__(self, nodes: Iterable[Node] | str | None = None, name: str | None = None, owner=None) -> None:
        if isinstance(nodes, str) and name is None:
            name = nodes
            nodes = None
        self.name: str = name or ""
        self._owner = owner
        super().__init__(list(nodes or []))

    def _nodes(self) -> list[Node]:
        if self._owner is not None and hasattr(self._owner, "_controls"):
            return [
                control
                for control in self._owner._controls()
                if control.getAttribute("id") == self.name or control.getAttribute("name") == self.name
            ]
        return list(list.__iter__(self))

    @property
    def length(self) -> int:
        return len(self._nodes())

    def __iter__(self) -> Iterator[Node]:
        return iter(self._nodes())

    def __getitem__(self, index: int) -> Node:
        return self._nodes()[index]

    def __len__(self) -> int:
        return self.length

    @property
    def value(self) -> Any:
        """Returns the value of the first element in the collection,
        or null if there are no elements in the collection."""
        for node in self._nodes():
            if isinstance(node, HTMLInputElement) and (node.getAttribute("type") or "").lower() == "radio" and node.checked:
                return node.value
        return ""

    @value.setter
    def value(self, new_value: Any) -> None:
        matching_radio = None
        for node in self._nodes():
            if (
                isinstance(node, HTMLInputElement)
                and (node.getAttribute("type") or "").lower() == "radio"
                and node.value == str(new_value)
            ):
                matching_radio = node
                break
        if matching_radio is None:
            return
        for node in self._nodes():
            if isinstance(node, HTMLInputElement) and (node.getAttribute("type") or "").lower() == "radio":
                node.checked = node is matching_radio


class Element(Node):
    """Baseclass for all html tags"""

    # __slots__ = ('_id')

    def __init__(self, *args, **kwargs):
        # self.content = None
        # self.attributes = None
        if self.hasAttribute("id"):
            self.id = self.id  # ''#None

        self.lang = None
        self.tabIndex = None

        if self.hasAttribute("title"):
            self.title = self.title

        if self.hasAttribute("class"):
            self.className = self.className
            self.classList = self.classList

        # self.tagName
        self.style = None  # Style(self)  # = #'test'#Style()
        self.shadowRoot = None
        self.dir = None
        super().__init__(*args, **kwargs)

    @property
    def childElementCount(self) -> int:
        """Returns the number of child elements an element has."""
        return len([child for child in self.args if isinstance(child, Element)])

    @property
    def children(self) -> list[Node]:
        """Returns child elements, excluding text, comments, and strings."""
        return [child for child in self.args if isinstance(child, Element)]

    def _getElementById(self, _id: str):
        for element in self.getElementsByTagName("*"):
            if element.getAttribute("id") == _id:
                return element
        return False

    def _getElementByAttrVal(self, attr: str, val: str):
        # TODO - i think i need to build a hash map of IDs to positions on the tree
        # for now I'm going using recursion so this is a bit of a hack to do a few levels
        if self.getAttribute(attr) == val:
            return self
        try:
            for child in self.childNodes:
                match = child._getElementByAttrVal(attr, val)
                if match:
                    return match
        except Exception as e:
            pass  # TODO - dont iterate strings
        return False

    def _matchElement(self, element, query):
        """
        tries to match an element based on the query
        at moment very basic. i.e. single level. just checks between id/tag/class
        """
        if not isinstance(element, Element):
            return False

        query = query.strip()
        if not query:
            return False

        if "." in query and not query.startswith(".") and "[" not in query:
            tag_name, class_name = query.split(".", 1)
            return element.tagName.lower() == tag_name.lower() and class_name in element.classList

        if "#" in query and not query.startswith("#") and "[" not in query:
            tag_name, element_id = query.split("#", 1)
            return element.tagName.lower() == tag_name.lower() and element.getAttribute("id") == element_id

        if query[0] == "#":
            if element.getAttribute("id") == query.split("#")[1]:
                return True

        if query == "*":
            return True

        if element.tagName.lower() == query.lower():
            return True

        if query[0] == ".":
            if query.split(".")[1] in element.classList:
                return True

        return False

    def matches(self, s: str) -> bool:
        """[checks to see if the Element would be selected by the provided selectorString]

        https://developer.mozilla.org/en-US/docs/Web/API/Element/matches

        Args:
            s (str): [css selector]

        Returns:
            [bool]: [True if selector maches Element otherwise False]
        """
        selectors = [selector.strip() for selector in str(s).split(",") if selector.strip()]
        for selector in selectors:
            if self._matchElement(self, selector):
                return True

        root = self.ownerDocument if self.ownerDocument is not None else self.rootNode
        if hasattr(root, "querySelectorAll"):
            for match in root.querySelectorAll(s):
                if match is self:
                    return True
        return False

    # https://developer.mozilla.org/en-US/docs/Web/API/Element/closest
    def closest(self, s: str):
        el = self
        while el != None and el.nodeType == 1:  # TODO - nodeType
            if Element.matches(el, s):
                return el
            el = el.parentElement or el.parentNode
        return None

    # @staticmethod
    def getElementsBySelector(self, all_selectors, document):
        """
        Get DOM elements based on the given CSS Selector.

        Original sources:
        - https://simonwillison.net/2003/Mar/25/getElementsBySelector/
        - http://www.openjs.com/scripts/dom/css_selector/
        - https://bin-co.com/python/scripts/getelementsbyselector-html-css-query.php (ported to Python 2, broken/bugs, BSD licensed)

        Note:
        - Always include a tag in the query. For example, `'a.classname'` will work, but just `'.classname'` will not.
        - Preserved as a compatibility helper for older selector-style code.
        - TODO: Needs to work in conjunction with `_matchElement` for better querySelector support, and to ensure dQuery compatibility.
        - TODO: Implement support for `*=` (node content).

        Args:
            all_selectors (str): The CSS selectors to query.
            document (object): The document object to search within.

        Returns:
            list: A list of elements matching the CSS selectors.
        """

        if not all_selectors:
            return []

        selected = []
        selectors = [selector.strip() for selector in str(all_selectors).split(",") if selector.strip()]
        if len(selectors) > 1:
            seen = []
            for selector in selectors:
                for item in self.getElementsBySelector(selector, document):
                    if item not in seen:
                        seen.append(item)
            return seen

        current = []
        quote = None
        for char in all_selectors:
            if quote is not None:
                current.append(char)
                if char == quote:
                    quote = None
                continue
            if char in ("'", '"'):
                quote = char
                current.append(char)
                continue
            if char.isspace():
                if current and current[-1] != " ":
                    current.append(" ")
                continue
            current.append(char)
        all_selectors = "".join(current).strip()
        # Grab all of the tagName elements within current context

        def getElements(context, tag):
            if tag == "":
                tag = "*"
            # Get elements matching tag, filter them for class selector
            found = []
            for con in context:
                elements = con.getElementsByTagName(tag)
                found.extend(elements)
            return found

        context = [document]
        inheriters = []
        current = []
        bracket_depth = 0
        quote = None
        for char in all_selectors:
            if quote is not None:
                current.append(char)
                if char == quote:
                    quote = None
                continue
            if char in ("'", '"'):
                quote = char
                current.append(char)
                continue
            if char == "[":
                bracket_depth += 1
                current.append(char)
                continue
            if char == "]":
                bracket_depth = max(0, bracket_depth - 1)
                current.append(char)
                continue
            if char == " " and bracket_depth == 0:
                if current:
                    inheriters.append("".join(current))
                    current = []
                continue
            current.append(char)
        if current:
            inheriters.append("".join(current))

        # Space
        for element in inheriters:
            # This part is to make sure that it is not part of a CSS3 Selector
            left_bracket = str.find(element, "[")
            right_bracket = str.find(element, "]")
            pos = str.find(element, "#")  # ID
            if pos + 1 and not (pos > left_bracket and pos < right_bracket):
                parts = str.split(element, "#")
                tag = parts[0]
                id = parts[1]
                ele = document.getElementById(id)
                context = [ele]  # [](ele)
                continue

            pos = str.find(element, ".")  # Class
            if pos + 1 and not (pos > left_bracket and pos < right_bracket):
                parts = str.split(element, ".")
                tag = parts[0]
                class_names = [part for part in parts[1:] if part]
                found = getElements(context, tag)
                # found = document.getElementsByClassName(class_name)
                context = []
                if not class_names:
                    continue
                for fnd in found:
                    class_attribute = fnd.getAttribute("class")
                    if class_attribute and all(class_name in class_attribute.split() for class_name in class_names):
                        context.append(fnd)

                continue

            # If the char '[' appears, that means it needs CSS 3 parsing
            if str.find(element, "[") + 1:
                # Code to deal with attribute selectors
                m = re.match(r"^([\w\*-]*)\[([\w-]+)([=~\|\^\$\*]?)=?['\"]?([^\]'\"]*)['\"]?\]$", element)
                if m:
                    tag = m.group(1)
                    attr = m.group(2)
                    operator = m.group(3)
                    value = m.group(4)
                else:
                    return []

                found = getElements(context, tag)
                context = []
                for fnd in found:
                    attr_value = fnd.getAttribute(attr)
                    if attr_value is None:
                        continue
                    if operator == "=" and fnd.getAttribute(attr) != value:
                        continue  # WORKING
                    if operator == "~" and value not in str(attr_value).split():
                        continue  # NOT WORKING?
                    if operator == "|" and attr_value != value and not str(attr_value).startswith(value + "-"):
                        continue
                    if operator == "^" and str.find(attr_value, value) != 0:
                        continue  # WORKING
                    if operator == "$" and str.rfind(attr_value, value) != (len(attr_value) - len(value)):
                        continue  # kinda WORKING
                    if operator == "*" and not (str.find(attr_value, value) + 1):
                        continue  # WORKING
                    elif not attr_value:
                        continue
                    context.append(fnd)

                continue

            # Tag selectors - no class or id specified.
            found = getElements(context, element)
            context = found

        selected.extend(context)
        return selected

    def append(self, *args):
        """Inserts a set of Node objects or DOMString objects after the last child of the Element."""
        items = _coerce_insertion_nodes(*args)
        old_documents = [
            (item, _detach_node_for_insertion(item)) for item in items
        ]
        previous_sibling = self.args[-1] if len(self.args) else None
        self.args += items
        for item, old_document in old_documents:
            _connect_inserted_node(self, item, old_document)
        added_nodes = [item for item in items if isinstance(item, Node)]
        if added_nodes:
            _queue_mutation_record(
                "childList",
                self,
                added_nodes=added_nodes,
                previous_sibling=previous_sibling,
            )
        _notify_slot_change(self)
        self._update_parents()
        return self

    # elem.attachShadow({mode: open|closed})
    def attachShadow(self, obj):
        mode = (obj or {}).get("mode", "open")
        self.shadowRoot = ShadowRoot(self, mode)
        return self.shadowRoot

    # def accessKey( key: str ): -> None
    # ''' Sets or returns the accesskey attribute of an element'''
    # return
    # example
    # dom.getElementById("myAnchor").accessKey = "w";

    @property
    def attributes(self) -> NamedNodeMap:
        """Returns a NamedNodeMap of an element's attributes"""
        newargs: list = []
        for key, value in self.kwargs.items():
            newargs.append(Attr(key.lstrip("_"), value))
        nnm = NamedNodeMap(newargs, None, self)
        return nnm

    @property
    def innerHTML(self):
        """Sets or returns the content of an element"""
        return self.content

    @innerHTML.setter
    def innerHTML(self, value):
        if value is not None:
            self.replaceChildren(*self._parse_html_fragment(value))
        return self.content

    @property
    def outerHTML(self):
        return str(self)

    @outerHTML.setter
    def outerHTML(self, value):
        if self.parentNode is None:
            return self
        replacement = DocumentFragment(*self._parse_html_fragment(value))
        self.parentNode.replaceChild(replacement, self)
        return self

    def html(self, *args):
        self.replaceChildren(*args)
        return self

    def _parse_html_fragment(self, value: Any) -> list[Any]:
        if isinstance(value, Element):
            return [value]
        if isinstance(value, (list, tuple)):
            nodes: list[Any] = []
            for item in value:
                nodes.extend(self._parse_html_fragment(item))
            return nodes
        if not isinstance(value, str):
            return [value]
        if "<" not in value or ">" not in value:
            return [value]

        try:
            from domonic import domonic as domonic_module

            parsed = domonic_module.parseString(f"<div>{value}</div>")
            wrapper = parsed.querySelector("div") if parsed is not None else None
            if wrapper is None:
                return [value]
            return list(wrapper.args)
        except Exception:
            return [value]

    def blur(self):
        """Removes focus from an element"""
        from domonic.events import FocusEvent

        doc = self.ownerDocument if isinstance(self.ownerDocument, Document) else None
        self._focused = False
        related_target = None
        if doc is not None and getattr(doc, "_activeElement", None) is self:
            doc._activeElement = None
            related_target = getattr(doc, "body", None)
        result = self.dispatchEvent(FocusEvent("blur", {"bubbles": False, "cancelable": False, "relatedTarget": related_target}))
        self.dispatchEvent(FocusEvent("focusout", {"bubbles": True, "cancelable": False, "relatedTarget": related_target}))
        return result

    @property
    def classList(self):
        """Returns the value of the classList attribute of an element"""
        return DOMTokenList(self)

    @classList.setter
    def classList(self, newlist):
        """Sets or returns the value of the classList attribute of an element"""
        if isinstance(newlist, DOMTokenList):
            newlist = newlist.toString()
        elif isinstance(newlist, (list, tuple, set)):
            newlist = " ".join(str(item) for item in newlist)
        self.setAttribute("class", newlist)
        # raise NotImplementedError

    @property
    def className(self):
        """Sets or returns the value of the className attribute of an element"""
        return self.getAttribute("class")

    @className.setter
    def className(self, newname: str):
        """Sets or returns the value of the className attribute of an element"""
        self.setAttribute("class", newname)

    def click(self):
        """Simulates a mouse-click on an element"""
        view = getattr(self.ownerDocument, "defaultView", None) if isinstance(self.ownerDocument, Document) else None
        evt = MouseEvent("click", {"bubbles": True, "cancelable": True, "view": view, "detail": 1})
        return self.dispatchEvent(evt)

    def animate(self, keyframes: list[dict[str, Any]] | dict[str, Any], options: Any = None):
        from domonic.animation import Animation, KeyframeEffect

        owner_document = self.ownerDocument if isinstance(self.ownerDocument, Document) else globals().get("document")
        timeline = owner_document.timeline if isinstance(owner_document, Document) else None
        effect = KeyframeEffect(self, keyframes, options)
        animation = Animation(effect, timeline)
        animation.play()
        return animation

    @staticmethod
    def _style_number(value):
        if value in (None, "", "auto", "none"):
            return 0
        if isinstance(value, (int, float)):
            return value
        match = re.search(r"-?\d+(?:\.\d+)?", str(value))
        return float(match.group(0)) if match else 0

    @property
    def clientHeight(self):
        """Returns the height of an element, including padding"""
        return (
            Element._style_number(self.style.height)
            + Element._style_number(self.style.paddingTop)
            + Element._style_number(self.style.paddingBottom)
        )

    @property
    def clientLeft(self):
        """Returns the width of the left border of an element"""
        return Element._style_number(self.style.left)

    @property
    def clientTop(self):
        """Returns the width of the top border of an element"""
        return Element._style_number(self.style.top)

    @property
    def clientWidth(self):
        """Returns the width of an element, including padding"""
        return (
            Element._style_number(self.style.width)
            + Element._style_number(self.style.paddingLeft)
            + Element._style_number(self.style.paddingRight)
        )

    @property
    def contentEditable(self) -> bool:
        """Sets or returns whether an element is editable"""
        is_editable = self.getAttribute("contenteditable")
        return True if (is_editable == "true" or is_editable is True) else False

    @contentEditable.setter
    def contentEditable(self, value: bool) -> None:
        self.setAttribute("contenteditable", value)

    @property
    def dataset(self):
        """Returns the value of the dataset attribute of an element"""
        return DOMStringMap(element=self)

    @property
    def dir(self):
        """returns the value of the dir attribute of an element"""
        return self.getAttribute("dir")

    @dir.setter
    def dir(self, direction: str = "auto"):
        """Sets the value of the dir attribute of an element"""
        self.setAttribute("dir", direction)

    def exitFullscreen(self):
        """Cancels an element in fullscreen mode"""
        doc = self.ownerDocument
        if doc is not None:
            doc._fullscreenElement = None
        return None

    def firstElementChild(self):
        """Returns the first child element of an element"""
        for child in self.args:
            if isinstance(child, Element):
                return child
        return None

    def focus(self):
        """Sets focus on an element"""
        from domonic.events import FocusEvent

        doc = self.ownerDocument if isinstance(self.ownerDocument, Document) else None
        previous = None
        if doc is not None:
            current = getattr(doc, "_activeElement", None)
            if current is not None and current is not self:
                previous = current
                current._focused = False
                current.dispatchEvent(FocusEvent("blur", {"bubbles": False, "cancelable": False, "relatedTarget": self}))
                current.dispatchEvent(FocusEvent("focusout", {"bubbles": True, "cancelable": False, "relatedTarget": self}))
            doc._activeElement = self
        self._focused = True
        result = self.dispatchEvent(FocusEvent("focus", {"bubbles": False, "cancelable": False, "relatedTarget": previous}))
        self.dispatchEvent(FocusEvent("focusin", {"bubbles": True, "cancelable": False, "relatedTarget": previous}))
        return result

    def setAttributeNodeNS(self, attr):
        """Sets the attribute node of an element"""
        a = Attr(attr.name.lstrip("_"), attr.value)
        self.setAttributeNode(a)
        return self

    def getAttributeNodeNS(self, attr):
        """Sets the attribute node of an element"""
        a = self.getAttribute(attr)
        if a is None:
            return None
        return Attr(attr, a)

    def setAttributeNS(self, namespaceURI, localName, value):
        """Sets an attribute in the given namespace"""
        self.setAttribute(localName, value)

    def getAttributeNS(self, namespaceURI, localName):
        """Returns the value of the specified attribute"""
        return self.getAttribute(localName)

    def removeAttributeNS(self, namespaceURI, localName):
        """Removes an attribute from an element"""
        if localName in self.attributes:
            self.removeAttribute(localName)
        # else:
        #     raise AttributeError
        return self

    def getAttribute(self, attribute: str) -> str:
        """Returns the specified attribute value of an element node"""
        try:
            if attribute[0:1] != "_":
                attribute = "_" + attribute
            return self.kwargs[attribute]
        except KeyError:
            return None

    def getAttributeNode(self, attribute: str) -> str:
        """Returns the specified attribute node"""
        value = self.getAttribute(attribute)
        if value is None:
            return None
        return Attr(attribute.lstrip("_"), value)

    def getBoundingClientRect(self):
        """Returns the size of an element and its position relative to the viewport"""
        rect = DOMRect(
            Element._style_number(self.style.left),
            Element._style_number(self.style.top),
            self.offsetWidth(),
            self.offsetHeight(),
        )
        _process_observer_notifications(self, rect)
        return rect

    def getSelection(self):
        """Returns a Selection object for this element's root tree."""
        root = self.rootNode
        if hasattr(root, "_selection"):
            return root._selection
        selection = Selection()
        setattr(root, "_selection", selection)
        return selection

    def getElementsByClassName(self, className: str) -> "HTMLCollection":
        """[Returns a collection of all child elements with the specified class name]

        Args:
            className (str): [a DOMString representing the class name to match]

        Returns:
            [type]: [a NodeList of all child elements with the specified class name]
        """
        required = {token for token in str(className).split() if token}
        if not required:
            return HTMLCollection()

        elements = HTMLCollection()

        def anon(el):
            if not isinstance(el, Element):
                return
            class_tokens = set(str(el.getAttribute("class") or "").split())
            if required.issubset(class_tokens):
                elements.append(el)

        self._iterate(self, anon)
        return elements

    def getElementById(self, _id: str) -> Element | None:
        """Returns the descendant element whose id matches the supplied value."""
        return self._getElementById(_id) or None

    def elementFromPoint(self, x: float, y: float) -> Element | None:
        """Returns the topmost element in this subtree at the specified coordinates."""
        hits = self.elementsFromPoint(x, y)
        return hits[0] if hits else None

    def elementsFromPoint(self, x: float, y: float) -> list[Element]:
        """Returns all elements in this subtree at the specified coordinates."""
        matches = []

        def walk(node):
            if not isinstance(node, Element):
                return
            rect = node.getBoundingClientRect()
            if rect.left <= x <= rect.right and rect.top <= y <= rect.bottom:
                matches.append(node)
            for child in getattr(node, "childNodes", []):
                walk(child)

        walk(self)
        return matches

    def caretPositionFromPoint(self, x: float, y: float) -> CaretPosition | None:
        """Returns a CaretPosition for the closest element within this subtree."""
        target = self.elementFromPoint(x, y)
        if target is None:
            return None
        first_child = target.firstChild
        if isinstance(first_child, Text):
            return CaretPosition(first_child, 0)
        return CaretPosition(target, 0)

    def getElementsByTagName(self, tagName: str) -> "HTMLCollection":
        """[Returns a collection of all child elements with the specified tag name

        Args:
            tagName (str): [a DOMString representing the tag name to match]

        Returns:
            [type]: [method returns a live HTMLCollection of elements with the given tag name.]
        """
        elements = HTMLCollection()

        def anon(el):
            if self._matchElement(el, tagName):
                elements.append(el)

        self._iterate(self, anon)
        return elements

    def hasAttribute(self, attribute: str) -> bool:
        """Returns True if an element has the specified attribute, otherwise False

        Args:
            attribute (str): [the attribute to test for]

        Returns:
            bool: [True if an element has the specified attribute, otherwise False]
        """
        try:
            if attribute[0:1] != "_":
                attribute = "_" + attribute
            return attribute in self.kwargs.keys()
        except AttributeError:
            return False

    def hasAttributes(self) -> bool:
        """Returns true if an element has any attributes, otherwise false"""
        if len(self.kwargs) > 0:
            return True
        else:
            return False

    @property
    def id(self) -> str | None:
        """Sets or returns the value of the id attribute of an element"""
        return self.getAttribute("id")

    @id.setter
    def id(self, newid: str):
        """Sets or returns the value of the id attribute of an element"""
        self.setAttribute("id", newid)

    # Sets or returns the text content of a node and its descendants
    def innerText(self, *args: Any) -> str:
        if args:
            self.textContent = "".join(str(each) for each in args)
            return self.textContent
        return self.textContent

    # Inserts an element adjacent to the current element
    def _normalize_adjacent_position(self, position: str) -> str:
        pos = str(position).lower()
        if pos not in ("beforebegin", "afterbegin", "beforeend", "afterend"):
            raise ValueError(
                f"The value provided ({position}) is not one of"
                '"beforeBegin", "afterBegin", "beforeEnd", or "afterEnd".'
            )
        return pos

    def _coerce_adjacent_nodes(self, content: Any) -> list[Any]:
        if isinstance(content, tuple):
            return list(content)
        if isinstance(content, list):
            return content
        return [content]

    def before(self, *nodes: Any) -> None:
        if self.parentNode is None:
            return
        nodes = tuple(
            node for node in _coerce_insertion_nodes(*nodes) if node is not self
        )
        if not nodes:
            return
        parent = self.parentNode
        old_documents = [
            (node, _detach_node_for_insertion(node)) for node in nodes
        ]
        index = parent.args.index(self)
        previous_sibling = (
            parent.args[index - 1]
            if index > 0 and isinstance(parent.args[index - 1], Node)
            else None
        )
        parent.args = parent.args[:index] + nodes + parent.args[index:]
        for node, old_document in old_documents:
            _connect_inserted_node(parent, node, old_document)
        added_nodes = [node for node in nodes if isinstance(node, Node)]
        if added_nodes:
            _queue_mutation_record(
                "childList",
                parent,
                added_nodes=added_nodes,
                previous_sibling=previous_sibling,
                next_sibling=self,
            )
        _notify_slot_change(parent)
        parent._update_parents()

    def after(self, *nodes: Any) -> None:
        if self.parentNode is None:
            return
        nodes = tuple(
            node for node in _coerce_insertion_nodes(*nodes) if node is not self
        )
        if not nodes:
            return
        parent = self.parentNode
        old_documents = [
            (node, _detach_node_for_insertion(node)) for node in nodes
        ]
        index = parent.args.index(self) + 1
        next_sibling = (
            parent.args[index]
            if index < len(parent.args) and isinstance(parent.args[index], Node)
            else None
        )
        parent.args = parent.args[:index] + nodes + parent.args[index:]
        for node, old_document in old_documents:
            _connect_inserted_node(parent, node, old_document)
        added_nodes = [node for node in nodes if isinstance(node, Node)]
        if added_nodes:
            _queue_mutation_record(
                "childList",
                parent,
                added_nodes=added_nodes,
                previous_sibling=self,
                next_sibling=next_sibling,
            )
        _notify_slot_change(parent)
        parent._update_parents()

    def insertAdjacentElement(self, position: str, element: Element) -> Element | None:
        """Inserts an element adjacent to the current element."""
        pos = self._normalize_adjacent_position(position)
        if pos == "beforebegin":
            if self.parentNode is None:
                return None
            self.before(element)
        elif pos == "afterbegin":
            self.prepend(element)
        elif pos == "beforeend":
            self.append(element)
        elif pos == "afterend":
            if self.parentNode is None:
                return None
            self.after(element)
        return element

    def insertAdjacentHTML(self, position: str, html: str) -> None:
        """Inserts raw HTML adjacent to the current element"""
        from domonic import domonic

        try:
            content = domonic.load(html)
        except Exception:
            content = html

        nodes = self._coerce_adjacent_nodes(content)
        pos = self._normalize_adjacent_position(position)
        if pos == "beforebegin":
            self.before(*nodes)
        elif pos == "afterbegin":
            self.prepend(*nodes)
        elif pos == "beforeend":
            self.append(*nodes)
        elif pos == "afterend":
            self.after(*nodes)

    def insertAdjacentText(self, position: str, text: str) -> None:
        """Inserts text adjacent to the current element"""
        pos = self._normalize_adjacent_position(position)
        if pos == "beforebegin":
            self.before(text)
        elif pos == "afterbegin":
            self.prepend(text)
        elif pos == "beforeend":
            self.append(text)
        elif pos == "afterend":
            self.after(text)

    def isContentEditable(self) -> bool:
        """Returns true if the content of an element is editable, otherwise false"""
        if self.getAttribute("contenteditable") == "true":
            return True
        return False

    # def lang(self) -> str:
    #     """ Sets or returns the value of the lang attribute of an element """ # TODO - prop?
    #     return self.getAttribute('lang')

    def lastElementChild(self) -> Node | None:
        """[Returns the last child element of an element]

        Returns:
            [type]: [the last child element of an element]
        """
        for child in reversed(self.args):
            if isinstance(child, Element):
                return child
        return None

    def namespaceURI(self) -> str:
        """Returns the namespace URI of an element"""
        return getattr(self, "_namespaceURI", "http://www.w3.org/1999/xhtml")

    @property
    def nextSibling(self) -> Node | None:
        """Returns the next node at the same node tree level"""
        if self.parentNode is not None:
            for count, el in enumerate(self.parentNode.args):
                if el is self and count < len(self.parentNode.args) - 1:
                    return self.parentNode.args[count + 1]
        return None

    @property
    def nextElementSibling(self) -> Node | None:
        """Returns the next element at the same node tree level"""
        if self.parentNode is not None:
            found_self = False
            for el in self.parentNode.args:
                if el is self:
                    found_self = True
                    continue
                if found_self and isinstance(el, Element):
                    return el
        return None

    @property
    def previousElementSibling(self) -> Node | None:
        """returns the Element immediately prior to the specified one in its parent's children list,
        or None if the specified element is the first one in the list."""
        if self.parentNode is not None:
            previous = None
            for el in self.parentNode.args:
                if el is self:
                    return previous
                if isinstance(el, Element):
                    previous = el
        return None

    def normalize(self) -> list[Any]:
        """Joins adjacent text nodes and removes empty text nodes in an element"""
        content = []
        nodestr = ""
        for s in self.args:
            if type(s) == Text:
                # content.append(s.textContent)
                nodestr += s.textContent
                continue
            elif type(s) == str:
                nodestr += s
                continue
            elif nodestr != "":
                content.append(nodestr)
                nodestr = ""
            elif type(s) != str:
                content.append(s)
        if nodestr != "":
            content.append(nodestr)
        self.args = content
        return self.args

    def offsetHeight(self) -> float:
        """Returns the height of an element, including padding, border and scrollbar"""
        return (
            self.clientHeight
            + Element._style_number(self.style.borderTopWidth)
            + Element._style_number(self.style.borderBottomWidth)
        )

    def offsetWidth(self) -> float:
        """Returns the width of an element, including padding, border and scrollbar"""
        return (
            self.clientWidth
            + Element._style_number(self.style.borderLeftWidth)
            + Element._style_number(self.style.borderRightWidth)
        )

    def offsetLeft(self) -> float:
        """Returns the horizontal offset position of an element"""
        return Element._style_number(self.style.left)

    def offsetParent(self) -> Node | None:
        """Returns the offset container of an element"""
        return self.parentNode

    def offsetTop(self) -> float:
        """Returns the vertical offset position of an element"""
        return Element._style_number(self.style.top)

    @property
    def parentElement(self) -> Node | None:
        """Returns the parent element node of an element"""
        return self.parentNode

    # @property
    # def previousSibling(self):
    #     """ Returns the previous node at the same node tree level """
    #     if self.parentNode is not None:
    #         for count, el in enumerate(self.parentNode.args):
    #             if el is self and count > 1:
    #                 return self.parentNode.args[count - 1]
    #     return None

    def prepend(self, *args: Any) -> None:
        """Prepends a node to the current element"""
        items = _coerce_insertion_nodes(*args)
        old_documents = [
            (item, _detach_node_for_insertion(item)) for item in items
        ]
        next_sibling = (
            self.args[0]
            if len(self.args) and isinstance(self.args[0], Node)
            else None
        )
        self.args = items + tuple(self.args)
        for item, old_document in old_documents:
            _connect_inserted_node(self, item, old_document)
        added_nodes = [item for item in items if isinstance(item, Node)]
        if added_nodes:
            _queue_mutation_record("childList", self, added_nodes=added_nodes, next_sibling=next_sibling)
        _notify_slot_change(self)
        self._update_parents()

    def replaceChildren(self, *nodes: Any) -> None:
        """Replaces the element's children with the supplied nodes."""
        items = _coerce_replacement_nodes(*nodes)
        removed_nodes = [node for node in self.args if isinstance(node, Node)]
        for node in removed_nodes:
            _disconnect_tree(node)
            node.parentNode = None
        old_documents = [
            (item, _detach_node_for_insertion(item)) for item in items
        ]
        self.args = items
        for item, old_document in old_documents:
            _connect_inserted_node(self, item, old_document)
        added_nodes = [item for item in items if isinstance(item, Node)]
        if added_nodes or removed_nodes:
            _queue_mutation_record(
                "childList",
                self,
                added_nodes=added_nodes,
                removed_nodes=removed_nodes,
            )
        _notify_slot_change(self)
        self._update_parents()

    def querySelector(self, query: str) -> Element | None:
        """[Returns the first child element that matches a specified CSS selector(s) of an element]

        Args:
            query (str): [a CSS selector string]

        Returns:
            [type]: [an Element object]
        """
        try:
            return self.querySelectorAll(query)[0]
        except Exception as e:
            return None

    def querySelectorAll(self, query: str) -> list[Element]:
        """[Returns all child elements that matches a specified CSS selector(s) of an element]

        Args:
            query (str): [a CSS selector string]

        Returns:
            [type]: [a list of Element objects]
        """
        if not query:
            return []

        query = query.strip()
        if re.match(r"^#[\w-]+$", query):
            found = self.getElementById(query[1:])
            return [found] if found is not None else []
        if re.match(r"^\.[\w-]+(?:\.[\w-]+)*$", query):
            return list(self.getElementsByClassName(" ".join(query.split(".")[1:])))
        if re.match(r"^(\*|[A-Za-z][\w-]*)$", query):
            return list(self.getElementsByTagName(query))

        def _fallback_selector_results():
            if query.startswith("."):
                return list(self.getElementsByClassName(" ".join(query.split(".")[1:])))
            if query.startswith("#"):
                found = self.getElementById(query[1:])
                return [found] if found else []
            results = self.getElementsBySelector(query, self)
            return results if isinstance(results, list) else []

        naked_query = query[1:]
        if "." in naked_query or "[" in query or " " in naked_query:
            try:
                from cssselect import HTMLTranslator, SelectorError

                expression = HTMLTranslator().css_to_xpath(query)
                from domonic.webapi.xpath import XPathEvaluator, XPathResult

                evaluator = XPathEvaluator()
                expression = evaluator.createExpression(expression)
                result = expression.evaluate(self, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
                if result.nodes:
                    return result.nodes
                return _fallback_selector_results()
            except ImportError:
                return _fallback_selector_results()
            except SelectorError:
                return _fallback_selector_results()

        elements = []

        def anon(el):
            if self._matchElement(el, query):
                elements.append(el)

        self._iterate(self, anon)
        return elements

    def remove(self):
        """Removes the element from the DOM"""
        # try:
        #     self.parentNode.args.remove(self)
        # except Exception:
        #     # print("Element not found")
        #     pass
        # if self.parentNode is None:
        # self._update_parents()
        if self.parentNode is not None:
            self.parentNode.removeChild(self)
        return self

    def removeAttribute(self, attribute: str):
        """Removes a specified attribute from an element"""
        if attribute[0:1] != "_":
            attribute = "_" + attribute
        if attribute not in self.kwargs:
            return None
        old_value = self.kwargs.get(attribute)
        del self.kwargs[attribute]
        _notify_attribute_changed(self, attribute, old_value, None)
        _queue_mutation_record(
            "attributes",
            self,
            attribute_name=attribute[1:] if attribute.startswith("_") else attribute,
            old_value=str(old_value) if old_value is not None else None,
        )
        return None

    def removeAttributeNode(self, attribute):
        """Removes a specified attribute node, and returns the removed node"""
        attr_name = attribute.name if isinstance(attribute, Attr) else str(attribute)
        key = attr_name if attr_name.startswith("_") else f"_{attr_name}"
        if key not in self.kwargs:
            return None

        val = self.kwargs.pop(key)
        public_name = key[1:] if key.startswith("_") else key
        _notify_attribute_changed(self, key, val, None)
        _queue_mutation_record(
            "attributes",
            self,
            attribute_name=public_name,
            old_value=str(val) if val is not None else None,
        )
        return Attr(public_name, val)

    def requestFullscreen(self):
        """Shows an element in fullscreen mode"""
        doc = self.ownerDocument
        if doc is not None:
            doc._fullscreenElement = self
        return self

    # def setPointerCapture(self):
    #     ''' Sets the pointer capture to the specified element '''
    #     raise NotImplementedError

    # def releasePointerCapture(self):
    #     ''' Releases the pointer capture from the specified element '''
    #     raise NotImplementedError

    def scrollHeight(self):
        """Returns the entire height of an element, including padding"""
        return max(self.clientHeight, getattr(self, "_scroll_height", self.clientHeight))

    def scrollIntoView(self):
        """Scrolls the specified element into the visible area of the browser window"""
        self._scrolled_into_view = True
        return self

    def scrollLeft(self):
        """Sets or returns the number of pixels an element's content is scrolled horizontally"""
        return getattr(self, "_scroll_left", 0)

    def scrollTop(self):
        """Sets or returns the number of pixels an element's content is scrolled vertically"""
        return getattr(self, "_scroll_top", 0)

    def scrollWidth(self):
        """Returns the entire width of an element, including padding"""
        return max(self.clientWidth, getattr(self, "_scroll_width", self.clientWidth))

    def setAttribute(self, attribute, value):
        """Sets or changes the specified attribute, to the specified value"""
        try:
            if attribute[0:1] != "_":
                attribute = "_" + attribute
            old_value = self.kwargs.get(attribute)
            self.kwargs[attribute] = value
            _notify_attribute_changed(self, attribute, old_value, value)
            _queue_mutation_record(
                "attributes",
                self,
                attribute_name=attribute[1:] if attribute.startswith("_") else attribute,
                old_value=str(old_value) if old_value is not None else None,
            )
        except Exception as e:
            # print('failed to set attribute', e)
            return None

    def setAttributeNode(self, attr):
        """[Sets or changes the specified attribute node]

        Args:
            attr ([type]): [an Attr object]
        """
        self.setAttribute(attr.name, attr.value)

    @property
    def style(self):
        """returns the value of the style attribute of an element"""
        if self.__style is None:
            self.style = Style()
        return self.__style

    @style.setter
    def style(self, style):
        self.__style = style
        self.__style.__init__(self)  # to set the parent

    # def tabIndex(self):
    # ''' Sets or returns the value of the tabindex attribute of an element'''
    # pass

    @property
    def tagName(self):
        return self.name

    # @property
    # def textContent(self):
    #     return self.nodeValue

    # @textContent.setter
    # def textContent(self, content):
    #     self.nodeValue = content

    @property
    def title(self):
        """returns the value of the title attribute of an element"""
        return self.getAttribute("title")

    @title.setter
    def title(self, newtitle: str):
        """[Sets the value of the title attribute of an element]

        Args:
            newtitle (str): [the new title value]
        """
        self.setAttribute("title", newtitle)

    def toString(self) -> str:
        """Converts an element to a string"""
        return str(self)


class DOMImplementation:
    def __init__(self):
        # self.__domImplementation = None
        pass

    def createDocument(self, namespaceURI: str, qualifiedName: str, doctype: str):
        if namespaceURI is None:
            namespaceURI = ""
        if qualifiedName is None:
            qualifiedName = ""
        if doctype is None:
            doctype = ""
        d = XMLDocument()
        root = d.createElementNS(namespaceURI, qualifiedName) if qualifiedName else None
        if root is not None:
            d.args = (root,)
            root.parentNode = d
            d.documentElement = root
        d.doctype = doctype
        return d

    def createDocumentType(self, qualifiedName: str, publicId: str, systemId: str) -> DocumentType:
        """[creates a DocumentType node]

        Args:
            qualifiedName (str): [the qualified name of the document type]
            publicId (str): [the public identifier of the document type]
            systemId (str): [the system identifier of the document type]

        Returns:
            [type]: [a DocumentType object]
        """
        return DocumentType(qualifiedName, publicId, systemId)

    def createHTMLDocument(self, title=None):
        doc = HTMLDocument()
        html_el = Document.createElement("html")
        head_el = Document.createElement("head")
        body_el = Document.createElement("body")
        if title is not None:
            head_el.appendChild(Document.createElement("title", title))
        html_el.appendChild(head_el)
        html_el.appendChild(body_el)
        doc.args = (html_el,)
        html_el.parentNode = doc
        doc.documentElement = html_el
        return doc

    def hasFeatures(self, featureList) -> bool:
        return True


class ProcessingInstruction(Node):

    nodeType: int = Node.PROCESSING_INSTRUCTION_NODE
    __slots__ = ("target", "data")

    def __init__(self, target, data) -> None:
        super().__init__()
        self.target = target
        self.data = data

    def toString(self) -> str:
        return f"<?{self.target} {self.data}?>"

    __str__ = toString


class Comment(Node):

    nodeType: int = Node.COMMENT_NODE
    nodeName: str = "#comment"
    __slots__ = "data"

    def __init__(self, data) -> None:
        self.data = data
        super().__init__()

    def toString(self) -> str:
        return f"<!--{self.data}-->"

    __str__ = toString

    def __format__(self, format_spec):
        return str(self)

    @property
    def __len__(self) -> int:
        return len(self.data)

    @property
    def length(self) -> int:
        return len(self.data)


class CDATASection(Node):
    """The CDATASection interface represents a CDATA section that can be used within XML 
    to include extended portions of unescaped text, such that the symbols < and & do not 
    need escaping as they normally do within XML when used as text."""

    nodeType: int = Node.CDATA_SECTION_NODE
    __slots__ = "data"

    def __init__(self, data) -> None:
        self.data = data

    def toString(self) -> str:
        return f"<![CDATA[{self.data}]]>"

    __str__ = toString

    @property
    def __len__(self) -> int:
        return len(self.data)

    @property
    def length(self) -> int:
        return len(self.data)

    # def __format__(self, format_spec):
    #     return str(self)


class AbastractRange:
    def __init__(self) -> None:
        """Constructor for Range objects"""
        self.startContainer: Node | None = None
        self.startOffset: int = 0
        self.endContainer: Node | None = None
        self.endOffset: int = 0
        self.collapsed: bool = True
        self.commonAncestorContainer: Node | None = None

    def cloneContents(self) -> "DocumentFragment":
        return self.cloneRange().cloneContents()

    def cloneRange(self) -> "Range":
        new_range = Range()
        if self.startContainer is not None:
            new_range.setStart(self.startContainer, self.startOffset)
        if self.endContainer is not None:
            new_range.setEnd(self.endContainer, self.endOffset)
        return new_range

    def compareBoundaryPoints(self, how: int, sourceRange: "Range") -> int:
        return self.cloneRange().compareBoundaryPoints(how, sourceRange)

    def createContextualFragment(self, data: Any) -> "DocumentFragment":
        return self.cloneRange().createContextualFragment(data)

    def deleteContents(self) -> None:
        self.cloneRange().deleteContents()

    def detach(self) -> None:
        self.startContainer = None
        self.endContainer = None
        self.startOffset = 0
        self.endOffset = 0
        self.collapsed = True
        self.commonAncestorContainer = None

    def expand(self, unit: Any) -> None:
        if self.startContainer is None:
            return
        unit = str(unit or "").lower()
        if unit in ("all", "document", "container"):
            self.selectNodeContents(self.commonAncestorContainer or self.startContainer)
            return
        if not isinstance(self.startContainer, Text) or self.startContainer is not self.endContainer:
            self.selectNodeContents(self.commonAncestorContainer or self.startContainer)
            return

        text = self.startContainer.textContent
        if unit == "character":
            start = max(0, min(self.startOffset, len(text)))
            end = max(start, min(len(text), start + 1))
            self.setStart(self.startContainer, start)
            self.setEnd(self.startContainer, end)
            return

        if unit == "word":
            start = max(0, min(self.startOffset, len(text)))
            end = max(start, min(self.endOffset, len(text)))
            while start > 0 and not text[start - 1].isspace():
                start -= 1
            while end < len(text) and not text[end].isspace():
                end += 1
            self.setStart(self.startContainer, start)
            self.setEnd(self.startContainer, end)
            return

        self.selectNodeContents(self.startContainer)

    def extractContents(self) -> "DocumentFragment":
        return self.cloneRange().extractContents()

    def getBoundingClientRect(self) -> DOMRect:
        return self.cloneRange().getBoundingClientRect()

    def getClientRects(self) -> DOMRectList:
        return self.cloneRange().getClientRects()

    def insertNode(self, newNode: "Node") -> None:
        self.cloneRange().insertNode(newNode)

    def selectNode(self, refNode: "Node") -> None:
        if refNode.parentNode is None:
            raise ValueError("Cannot select a detached node")
        self.setStartBefore(refNode)
        self.setEndAfter(refNode)

    def selectNodeContents(self, refNode: "Node") -> None:
        self.setStart(refNode, 0)
        self.setEnd(refNode, Range._container_length(refNode))

    def setEnd(self, refNode: "Node", offset: int) -> None:
        self.endContainer = refNode
        self.endOffset = offset
        if self.startContainer is None:
            self.startContainer = refNode
            self.startOffset = offset
        self._update_state()

    def setEndAfter(self, refNode: "Node") -> None:
        self.setEnd(refNode.parentNode, list(refNode.parentNode.childNodes).index(refNode) + 1)

    def setEndBefore(self, refNode: "Node") -> None:
        self.setEnd(refNode.parentNode, list(refNode.parentNode.childNodes).index(refNode))

    def setStart(self, refNode: "Node", offset: int) -> None:
        self.startContainer = refNode
        self.startOffset = offset
        if self.endContainer is None:
            self.endContainer = refNode
            self.endOffset = offset
        self._update_state()

    def setStartAfter(self, refNode: "Node") -> None:
        self.setStart(refNode.parentNode, list(refNode.parentNode.childNodes).index(refNode) + 1)

    def setStartBefore(self, refNode: "Node") -> None:
        self.setStart(refNode.parentNode, list(refNode.parentNode.childNodes).index(refNode))

    def surroundContents(self, newParent: "Node") -> None:
        self.cloneRange().surroundContents(newParent)

    def toString(self) -> str:
        return self.cloneRange().toString()

    def comparePoint(self, refNode: "Node", offset: int) -> int:
        return self.cloneRange().comparePoint(refNode, offset)

    def deleteData(self, offset, count):
        if not isinstance(self.startContainer, Text) or self.startContainer is not self.endContainer:
            raise ValueError("Range data helpers require a single Text container")
        self.startContainer.deleteData(offset, count)
        self.endOffset = min(self.endOffset, len(self.startContainer.textContent))
        self.startOffset = min(self.startOffset, self.endOffset)
        self._update_state()
        return self.startContainer.textContent

    def extractData(self, offset, count):
        data = self.getData(offset, count)
        self.deleteData(offset, count)
        return data

    def getData(self, offset, count):
        if not isinstance(self.startContainer, Text) or self.startContainer is not self.endContainer:
            raise ValueError("Range data helpers require a single Text container")
        return self.startContainer.textContent[offset : offset + count]

    def getEnd(self):
        return (self.endContainer, self.endOffset)

    def getStart(self):
        return (self.startContainer, self.startOffset)

    def replaceData(self, offset, count, data):
        if not isinstance(self.startContainer, Text) or self.startContainer is not self.endContainer:
            raise ValueError("Range data helpers require a single Text container")
        self.startContainer.replaceData(offset, count, data)
        self.endOffset = min(len(self.startContainer.textContent), max(self.startOffset, self.endOffset))
        self._update_state()
        return self.startContainer.textContent

    def setData(self, data):
        if not isinstance(self.startContainer, Text) or self.startContainer is not self.endContainer:
            raise ValueError("Range data helpers require a single Text container")
        self.startContainer.data = data
        self.startOffset = min(self.startOffset, len(data))
        self.endOffset = min(self.endOffset, len(data))
        self._update_state()
        return self.startContainer.textContent

    def _update_state(self) -> None:
        self.collapsed = (
            self.startContainer is self.endContainer and self.startOffset == self.endOffset
        )
        if self.startContainer is None or self.endContainer is None:
            self.commonAncestorContainer = None
            return
        start_path = Range._path_to_root(self.startContainer)
        end_path = Range._path_to_root(self.endContainer)
        ancestor = None
        while start_path and end_path and start_path[-1] is end_path[-1]:
            ancestor = start_path.pop()
            end_path.pop()
        self.commonAncestorContainer = ancestor


AbstractRange = AbastractRange


class Range(AbastractRange):
    # TODO - untested

    START_TO_START: ClassVar[int] = 0
    START_TO_END: ClassVar[int] = 1
    END_TO_END: ClassVar[int] = 2
    END_TO_START: ClassVar[int] = 3

    def __init__(self) -> None:
        self.startContainer: Node | None = None
        self.startOffset = 0
        self.endContainer: Node | None = None
        self.endOffset = 0
        self.collapsed = True
        self.commonAncestorContainer: Node | None = None

    @staticmethod
    def _container_length(node: Node | None) -> int:
        if node is None:
            return 0
        if isinstance(node, Text):
            return len(node.textContent)
        return len(getattr(node, "childNodes", []))

    @staticmethod
    def _path_to_root(node: Node | None) -> list[Node]:
        path: list[Node] = []
        current = node
        while current is not None:
            path.append(current)
            current = getattr(current, "parentNode", None)
        return path

    @staticmethod
    def _compare_points(node_a: Node, offset_a: int, node_b: Node, offset_b: int) -> int:
        if node_a is node_b:
            if offset_a < offset_b:
                return -1
            if offset_a > offset_b:
                return 1
            return 0

        path_a = Range._path_to_root(node_a)
        path_b = Range._path_to_root(node_b)
        common = None
        while path_a and path_b and path_a[-1] is path_b[-1]:
            common = path_a.pop()
            path_b.pop()
        if common is None:
            return 0
        child_a = path_a[-1] if path_a else common
        child_b = path_b[-1] if path_b else common
        siblings = list(getattr(common, "childNodes", []))
        try:
            index_a = siblings.index(child_a)
            index_b = siblings.index(child_b)
        except ValueError:
            return 0
        if index_a < index_b:
            return -1
        if index_a > index_b:
            return 1
        return 0

    def _update_state(self) -> None:
        self.collapsed = (
            self.startContainer is self.endContainer and self.startOffset == self.endOffset
        )
        if self.startContainer is None or self.endContainer is None:
            self.commonAncestorContainer = None
            return
        start_path = self._path_to_root(self.startContainer)
        end_path = self._path_to_root(self.endContainer)
        ancestor = None
        while start_path and end_path and start_path[-1] is end_path[-1]:
            ancestor = start_path.pop()
            end_path.pop()
        self.commonAncestorContainer = ancestor

    def _common_ancestor_child_slice(self) -> tuple[Node, int, int] | None:
        ancestor = self.commonAncestorContainer
        if ancestor is None or isinstance(ancestor, Text):
            return None

        children = list(getattr(ancestor, "childNodes", []))

        def resolve_index(node: Node | None, offset: int, *, is_end: bool) -> int | None:
            if node is None:
                return None
            if node is ancestor:
                bounded = max(0, min(offset, len(children)))
                return bounded

            current = node
            while current is not None and getattr(current, "parentNode", None) is not ancestor:
                current = getattr(current, "parentNode", None)

            if current is None:
                return None

            try:
                index = children.index(current)
            except ValueError:
                return None

            if is_end:
                if isinstance(node, Text) and offset == 0:
                    return index
                return index + 1
            return index

        start_index = resolve_index(self.startContainer, self.startOffset, is_end=False)
        end_index = resolve_index(self.endContainer, self.endOffset, is_end=True)
        if start_index is None or end_index is None:
            return None
        return ancestor, start_index, end_index

    @classmethod
    def _validate_boundary_point(cls, node: Node, offset: int) -> int:
        if node is None:
            raise ValueError("Boundary node cannot be None")
        if not isinstance(offset, int):
            raise TypeError("Range offset must be an integer")
        max_offset = cls._container_length(node)
        if offset < 0 or offset > max_offset:
            raise ValueError("Range offset is out of bounds")
        return offset

    def setStart(self, node: Node, offset: int) -> None:
        offset = self._validate_boundary_point(node, offset)
        self.startContainer = node
        self.startOffset = offset
        if self.endContainer is None:
            self.endContainer = node
            self.endOffset = offset
        elif self._compare_points(node, offset, self.endContainer, self.endOffset) > 0:
            self.endContainer = node
            self.endOffset = offset
        self._update_state()

    def setEnd(self, node: Node, offset: int) -> None:
        offset = self._validate_boundary_point(node, offset)
        self.endContainer = node
        self.endOffset = offset
        if self.startContainer is None:
            self.startContainer = node
            self.startOffset = offset
        elif self._compare_points(node, offset, self.startContainer, self.startOffset) < 0:
            self.startContainer = node
            self.startOffset = offset
        self._update_state()

    def setStartBefore(self, node: Node) -> None:
        self.setStart(node.parentNode, list(node.parentNode.childNodes).index(node))

    def setStartAfter(self, node: Node) -> None:
        self.setStart(node.parentNode, list(node.parentNode.childNodes).index(node) + 1)

    def setEndBefore(self, node: Node) -> None:
        self.setEnd(node.parentNode, list(node.parentNode.childNodes).index(node))

    def setEndAfter(self, node: Node) -> None:
        self.setEnd(node.parentNode, list(node.parentNode.childNodes).index(node) + 1)

    def collapse(self, toStart: bool = False) -> None:
        if toStart:
            self.endContainer = self.startContainer
            self.endOffset = self.startOffset
        else:
            self.startContainer = self.endContainer
            self.startOffset = self.endOffset
        self._update_state()

    def selectNode(self, node: Node) -> None:
        self.setStartBefore(node)
        self.setEndAfter(node)

    def selectNodeContents(self, node: Node) -> None:
        self.setStart(node, 0)
        self.setEnd(node, self._container_length(node))

    def compareBoundaryPoints(self, how: int, sourceRange: "Range") -> int:
        comparisons = {
            self.START_TO_START: (self.startContainer, self.startOffset, sourceRange.startContainer, sourceRange.startOffset),
            self.START_TO_END: (self.startContainer, self.startOffset, sourceRange.endContainer, sourceRange.endOffset),
            self.END_TO_END: (self.endContainer, self.endOffset, sourceRange.endContainer, sourceRange.endOffset),
            self.END_TO_START: (self.endContainer, self.endOffset, sourceRange.startContainer, sourceRange.startOffset),
        }
        if how not in comparisons:
            raise ValueError("Invalid Range comparison type")
        return self._compare_points(*comparisons[how])

    def deleteContents(self) -> None:
        self.extractContents()

    def extractContents(self) -> "DocumentFragment":
        if self.startContainer is None:
            return DocumentFragment()
        if isinstance(self.startContainer, Text) and self.startContainer == self.endContainer:
            text = self.startContainer.textContent
            extracted = text[self.startOffset : self.endOffset]
            self.startContainer.textContent = text[: self.startOffset] + text[self.endOffset :]
            self.endContainer = self.startContainer
            self.endOffset = self.startOffset
            self._update_state()
            return DocumentFragment(Text(extracted))
        if self.startContainer == self.endContainer:
            container = self.startContainer
            children = list(container.childNodes)
            extracted = children[self.startOffset : self.endOffset]
            if hasattr(container, "args"):
                kept = children[: self.startOffset] + children[self.endOffset :]
                container.args = tuple(kept)
                for child in kept:
                    if isinstance(child, Node):
                        child.parentNode = container
            self.endContainer = container
            self.endOffset = self.startOffset
            self._update_state()
            return DocumentFragment(*extracted)
        child_slice = self._common_ancestor_child_slice()
        if child_slice is not None:
            container, start_index, end_index = child_slice
            children = list(container.childNodes)
            extracted = children[start_index:end_index]
            if hasattr(container, "args"):
                kept = children[:start_index] + children[end_index:]
                container.args = tuple(kept)
                for child in kept:
                    if isinstance(child, Node):
                        child.parentNode = container
            self.startContainer = container
            self.endContainer = container
            self.startOffset = start_index
            self.endOffset = start_index
            self._update_state()
            return DocumentFragment(*extracted)
        return DocumentFragment()

    def cloneContents(self) -> "DocumentFragment":
        import copy

        if self.startContainer is None:
            return DocumentFragment()
        if isinstance(self.startContainer, Text) and self.startContainer == self.endContainer:
            return DocumentFragment(Text(self.startContainer.textContent[self.startOffset : self.endOffset]))
        if self.startContainer == self.endContainer:
            container = self.startContainer
            children = list(container.childNodes)
            cloned = [copy.deepcopy(child) for child in children[self.startOffset : self.endOffset]]
            return DocumentFragment(*cloned)
        child_slice = self._common_ancestor_child_slice()
        if child_slice is not None:
            container, start_index, end_index = child_slice
            children = list(container.childNodes)
            cloned = [copy.deepcopy(child) for child in children[start_index:end_index]]
            return DocumentFragment(*cloned)
        return DocumentFragment()

    def getBoundingClientRect(self) -> DOMRect:
        rects = self.getClientRects()
        if not rects:
            return DOMRect(0, 0, 0, 0)
        left = min(rect.left for rect in rects)
        top = min(rect.top for rect in rects)
        right = max(rect.right for rect in rects)
        bottom = max(rect.bottom for rect in rects)
        return DOMRect(left, top, right - left, bottom - top)

    def getClientRects(self) -> DOMRectList:
        if self.startContainer is None:
            return DOMRectList()
        if isinstance(self.startContainer, Text) and self.startContainer == self.endContainer:
            parent = getattr(self.startContainer, "parentNode", None)
            return DOMRectList([parent.getBoundingClientRect()]) if hasattr(parent, "getBoundingClientRect") else DOMRectList()
        if self.startContainer == self.endContainer:
            rects = []
            for child in list(self.startContainer.childNodes)[self.startOffset : self.endOffset]:
                if hasattr(child, "getBoundingClientRect"):
                    rects.append(child.getBoundingClientRect())
            return DOMRectList(rects)
        child_slice = self._common_ancestor_child_slice()
        if child_slice is not None:
            container, start_index, end_index = child_slice
            rects = []
            for child in list(container.childNodes)[start_index:end_index]:
                if hasattr(child, "getBoundingClientRect"):
                    rects.append(child.getBoundingClientRect())
            return DOMRectList(rects)
        return DOMRectList()

    def insertNode(self, node: Node) -> None:
        if self.startContainer is None:
            return
        container = self.startContainer
        if isinstance(container, Text):
            text = container.textContent
            before = Text(text[: self.startOffset])
            after = Text(text[self.startOffset :])
            parent = container.parentNode
            if parent is None:
                return
            children = list(parent.childNodes)
            index = children.index(container)
            replacement = [part for part in (before, node, after) if part.textContent != "" if isinstance(part, Text)] if False else None
            new_children = children[:index]
            if before.textContent != "":
                new_children.append(before)
                before.parentNode = parent
            new_children.append(node)
            node.parentNode = parent
            if after.textContent != "":
                new_children.append(after)
                after.parentNode = parent
            new_children.extend(children[index + 1 :])
            parent.args = tuple(new_children)
            self.startContainer = parent
            self.endContainer = parent
            self.startOffset = index + 1
            self.endOffset = index + 1
            self._update_state()
            return
        if hasattr(container, "insertBefore"):
            children = list(container.childNodes)
            ref = children[self.startOffset] if self.startOffset < len(children) else None
            container.insertBefore(node, ref)
            self.startOffset += 1
            self.endOffset = max(self.endOffset, self.startOffset)
            self._update_state()

    def surroundContents(self, newParent: Node) -> None:
        fragment = self.extractContents()
        for child in fragment.args:
            newParent.appendChild(child)
        self.insertNode(newParent)
        self.selectNode(newParent)

    def cloneRange(self) -> "Range":
        new_range = Range()
        new_range.startContainer = self.startContainer
        new_range.startOffset = self.startOffset
        new_range.endContainer = self.endContainer
        new_range.endOffset = self.endOffset
        new_range.collapsed = self.collapsed
        new_range.commonAncestorContainer = self.commonAncestorContainer
        return new_range

    def detach(self) -> None:
        self.startContainer = None
        self.endContainer = None
        self.startOffset = 0
        self.endOffset = 0
        self._update_state()

    def createContextualFragment(self, fragment: Any) -> "DocumentFragment":
        if isinstance(fragment, DocumentFragment):
            return fragment
        if isinstance(fragment, Node):
            return DocumentFragment(fragment)
        if not isinstance(fragment, str):
            return DocumentFragment(fragment)

        try:
            from domonic import domonic

            page = domonic.parseString(f"<body>{fragment}</body>")
            if page is not None:
                body = page.querySelector("body")
                if body is not None:
                    return DocumentFragment(*list(body.childNodes))
        except Exception:
            pass
        return DocumentFragment(fragment)

    def toString(self) -> str:
        if self.startContainer is None:
            return ""
        if isinstance(self.startContainer, Text) and self.startContainer == self.endContainer:
            return self.startContainer.textContent[self.startOffset : self.endOffset]
        if self.startContainer == self.endContainer:
            container = self.startContainer
            children = list(container.childNodes)
            return "".join(str(child) for child in children[self.startOffset : self.endOffset])
        child_slice = self._common_ancestor_child_slice()
        if child_slice is not None:
            container, start_index, end_index = child_slice
            children = list(container.childNodes)
            return "".join(str(child) for child in children[start_index:end_index])
        return ""

    def comparePoint(self, refNode: Node, offset: int) -> int:
        if self.startContainer is None or self.endContainer is None:
            raise Exception("Range has no boundaries")
        offset = self._validate_boundary_point(refNode, offset)
        if self._compare_points(refNode, offset, self.startContainer, self.startOffset) < 0:
            return -1
        if self._compare_points(refNode, offset, self.endContainer, self.endOffset) > 0:
            return 1
        return 0

    def isPointInRange(self, refNode: Node, offset: int) -> bool:
        return self.comparePoint(refNode, offset) == 0

    def intersectsNode(self, refNode: Node) -> bool:
        if self.startContainer is None or self.endContainer is None:
            return False
        if isinstance(refNode, Text):
            start_node, start_offset = refNode, 0
            end_node, end_offset = refNode, len(refNode.textContent)
        else:
            parent = getattr(refNode, "parentNode", None)
            if parent is None:
                return refNode is self.commonAncestorContainer
            siblings = list(getattr(parent, "childNodes", []))
            if refNode not in siblings:
                return False
            index = siblings.index(refNode)
            start_node, start_offset = parent, index
            end_node, end_offset = parent, index + 1

        return not (
            self._compare_points(end_node, end_offset, self.startContainer, self.startOffset) <= 0
            or self._compare_points(start_node, start_offset, self.endContainer, self.endOffset) >= 0
        )


class StaticRange(Range):
    """Immutable snapshot of a range boundary pair.

    ``StaticRange`` mirrors the platform idea of a range-like object that can
    be inspected and cloned back into a mutable ``Range`` but cannot be edited
    in place.
    """

    def __init__(self, startContainer, startOffset, endContainer, endOffset):
        super().__init__()
        self.startContainer = startContainer
        self.startOffset = startOffset
        self.endContainer = endContainer
        self.endOffset = endOffset
        self._update_state()

    def _immutable(self, *args, **kwargs):
        raise TypeError("StaticRange is immutable")

    collapse = _immutable
    createContextualFragment = Range.createContextualFragment
    deleteContents = _immutable
    deleteData = _immutable
    detach = _immutable
    expand = _immutable
    extractContents = _immutable
    insertNode = _immutable
    replaceData = _immutable
    selectNode = _immutable
    selectNodeContents = _immutable
    setData = _immutable
    setEnd = _immutable
    setEndAfter = _immutable
    setEndBefore = _immutable
    setStart = _immutable
    setStartAfter = _immutable
    setStartBefore = _immutable
    surroundContents = _immutable

    def toRange(self) -> Range:
        return self.cloneRange()


class TimeRanges:
    def __init__(self, *ranges):
        self._ranges = []
        for item in ranges:
            if isinstance(item, (list, tuple)) and len(item) == 2:
                self._ranges.append((item[0], item[1]))
        self.length = len(self._ranges)

    def _range_at(self, index):
        if not isinstance(index, int):
            raise TypeError("index must be an integer")
        if index < 0 or index >= self.length:
            raise IndexError("TimeRanges index is out of bounds")
        return self._ranges[index]

    def start(self, index):
        return self._range_at(index)[0]

    def end(self, index):
        return self._range_at(index)[1]

    def __len__(self):
        return self.length


class Document(Element):
    """The Document interface represents the entire HTML or XML document."""

    URL: ClassVar[URL | None] = None

    def __init__(self, *args, **kwargs):
        """Constructor for Document objects"""
        self.args = args
        self.kwargs = kwargs
        # self.documentURI = uri
        # self.documentElement = self
        self._open_filename = None
        self._activeElement = None
        self._defaultView = None
        self._designMode = "off"
        self._currentScript = None
        self._cookie_store: dict[str, str] = {}
        self._lastModified = formatdate(time.time(), usegmt=True)
        self._referrer = ""
        self._timeline = None
        self.stylesheets = None
        self.doctype = None
        super().__init__(*args, **kwargs)
        try:
            global document
            document = self
        except Exception as e:
            print("failed to set document", e)

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.__init__(*args, **kwargs)
        instance.documentElement = instance
        instance.URL = ""
        instance.baseURI = ""
        try:
            global document
            document = instance
        except Exception as e:
            print("failed to set document", e)
        return instance

    # TODO - still not great as it also returns 'links' when searching for 'li'
    # @property
    def _get_tags(self, tag):  # TODO - still old
        """returns the tags you want"""
        reg = f"(<{tag}.*?>.+?</{tag}>)"

        closed_tags = [
            "base",
            "link",
            "meta",
            "hr",
            "br",
            "wbr",
            "img",
            "embed",
            "param",
            "source",
            "track",
            "area",
            "col",
            "input",
            "keygen",
            "command",
        ]
        if tag in closed_tags:
            reg = f"(<{tag}.*?/>)"

        pattern = re.compile(reg)
        tags = re.findall(pattern, str(self))
        return tags

        # def activeElement():
        """ Returns the currently focused element in the document"""
        # return

    # def adoptNode(self, node):
    #     """ Adopts a node from another document """
    #     if node.ownerDocument is not None:
    #         node.ownerDocument.removeChild(node)
    #     node.ownerDocument = self
    #     return node

    @property
    def stylesheets(self):
        if self.__stylesheets is None:
            self.stylesheets = StyleSheetList()
            self.stylesheets._populate_stylesheets_from_document(self)
        return self.__stylesheets

    @stylesheets.setter
    def stylesheets(self, stylesheets):
        self.__stylesheets = stylesheets
        # self.__stylesheets.__init__(self)  # to set the parent??

    @property
    def activeElement(self) -> Element | None:
        """Returns the currently focused element, or the body/document element fallback."""
        if self._activeElement is not None:
            return self._activeElement
        return self.body or self.documentElement

    @property
    def timeline(self) -> DocumentTimeline:
        if self._timeline is None:
            self._timeline = DocumentTimeline(self)
        return self._timeline

    @property
    def currentScript(self) -> Element | None:
        if self._currentScript is not None:
            return self._currentScript
        scripts = self.scripts
        return scripts[-1] if scripts else None

    @currentScript.setter
    def currentScript(self, script: Element | None) -> None:
        self._currentScript = script

    @property
    def defaultView(self):
        return self._defaultView

    @defaultView.setter
    def defaultView(self, value) -> None:
        self._defaultView = value

    @property
    def designMode(self) -> str:
        return self._designMode

    @designMode.setter
    def designMode(self, value: str) -> None:
        normalized = str(value).strip().lower()
        if normalized not in {"on", "off"}:
            raise ValueError("designMode must be 'on' or 'off'")
        self._designMode = normalized

    def hasFocus(self) -> bool:
        """Returns True when the document currently tracks a focused element."""
        return self._activeElement is not None

    @property
    def anchors(self):
        """[get the anchors in the document]"""
        # only the ones with a name
        tags = self.querySelectorAll("a")
        tags = [tag for tag in tags if tag.hasAttribute("name")]
        return tags

    @property
    def applets(self):
        """Returns a collection of all <applet> elements in the document"""
        return self.querySelectorAll("applet")

    @property
    def body(self):
        """Returns the <body> element in the document"""
        return self.querySelector("body")

    @body.setter
    def body(self, el):
        """Sets the <body> element in the document"""
        if not isinstance(el, HTMLBodyElement):
            raise DOMException(
                DOMException.TYPE_MISMATCH_ERR,
                "The new body element is of type '" + str(type(el)) + "'. It must be a 'HTMLBodyElement'",
            )
        else:
            if self.body is not None:
                self.body.remove()
            self += el

    def close(self):
        """Closes the output stream previously opened with document.open()"""
        self._open_filename = None

    @property
    def cookie(self) -> str:
        return "; ".join(f"{name}={value}" for name, value in self._cookie_store.items())

    @cookie.setter
    def cookie(self, value: str) -> None:
        if value is None:
            return
        text = str(value).strip()
        if not text or "=" not in text:
            return
        first_pair = text.split(";", 1)[0]
        name, cookie_value = first_pair.split("=", 1)
        self._cookie_store[name.strip()] = cookie_value.strip()

    @property
    def charset(self):
        """Returns the character encoding for the document. Deprecated: Use characterSet instead."""
        return "UTF-8"

    @property
    def characterSet(self):
        """Returns the character encoding for the document"""
        return "UTF-8"

    @staticmethod
    def createAttribute(name: str) -> Attr:
        """Creates an attribute node"""
        return Attr(name)

    @staticmethod
    def createComment(message: str) -> "Comment":
        """Creates a Comment node with the specified text"""
        return Comment(message)

    @staticmethod
    def createDocumentFragment(*args: Any) -> "DocumentFragment":
        """Creates an empty DocumentFragment node if not content passed. I added args as optional to pass content"""
        return DocumentFragment(*args)

    @staticmethod
    def createExpression(xpath: str, nsResolver: Any) -> XPathExpression:
        """Creates an XPathExpression object for the given XPath string."""
        return XPathExpression(xpath, nsResolver)

    @staticmethod
    def createElement(_type: str, *args: Any, **kwargs: Any) -> "Element":
        """Creates an Element node"""
        from domonic.html import create_element

        el = create_element(_type, *args, **kwargs)
        if isinstance(el, Element):
            _upgrade_custom_element_instance(el)
        return el

    @staticmethod
    def createElementNS(namespaceURI: str, qualifiedName: str, options: Any = None) -> "Element":
        """Creates an element with the specified namespace URI and qualified name."""
        # el = type(qualifiedName, (Element,), {'name': qualifiedName})
        from domonic.html import create_element

        el = create_element(qualifiedName)  # , *args, **kwargs)
        el.namespaceURI = namespaceURI
        _upgrade_custom_element_instance(el)
        # el["name"] = qualifiedName
        return el

    @staticmethod
    def createEvent(event_type: str | None = None) -> Event:
        """[Creates a new event]

        Args:
            event_type ([type], optional): [description]. Defaults to None.

        Returns:
            [type]: [a new event]
        """
        if event_type == "MouseEvent":
            return MouseEvent("click")
        if event_type == "PointerEvent":
            from domonic.events import PointerEvent

            return PointerEvent("pointerdown")
        if event_type == "FocusEvent":
            from domonic.events import FocusEvent

            return FocusEvent("focus")
        if event_type == "KeyboardEvent":
            from domonic.events import KeyboardEvent

            return KeyboardEvent("keydown")
        if event_type == "UIEvent":
            from domonic.events import UIEvent

            return UIEvent("load")
        if event_type == "CustomEvent":
            from domonic.events import CustomEvent

            return CustomEvent("custom")
        if event_type == "CompositionEvent":
            from domonic.events import CompositionEvent

            return CompositionEvent("compositionstart")
        if event_type == "SubmitEvent":
            from domonic.events import SubmitEvent

            return SubmitEvent("submit")
        if event_type == "InputEvent":
            from domonic.events import InputEvent

            return InputEvent("input")
        if event_type == "ClipboardEvent":
            from domonic.events import ClipboardEvent

            return ClipboardEvent("copy")
        if event_type == "WheelEvent":
            from domonic.events import WheelEvent

            return WheelEvent("wheel")
        if event_type == "BeforeUnloadEvent":
            from domonic.events import BeforeUnloadEvent

            return BeforeUnloadEvent("beforeunload")
        if event_type == "MessageEvent":
            from domonic.events import MessageEvent

            return MessageEvent("message")
        if event_type == "TransitionEvent":
            from domonic.events import TransitionEvent

            return TransitionEvent("transitionend")
        if event_type == "ProgressEvent":
            from domonic.events import ProgressEvent

            return ProgressEvent("progress")
        if event_type == "ErrorEvent":
            from domonic.events import ErrorEvent

            return ErrorEvent("error")
        if event_type == "PopStateEvent":
            from domonic.events import PopStateEvent

            return PopStateEvent("popstate")
        if event_type == "CloseEvent":
            from domonic.events import CloseEvent

            return CloseEvent("close")
        if event_type is None:
            return Event()
        return Event(event_type)

    @staticmethod
    def createTextNode(text: str) -> "Text":
        """[Creates a Text node with the specified text.

        Args:
            text ([str]): [the text to be inserted]

        Returns:
            [type]: [a new Text node]
        """
        return Text(text)

    @staticmethod
    def createTreeWalker(
        root: Node, whatToShow: int | None = None, filter: Any = None, entityReferenceExpansion: Any = None
    ) -> "TreeWalker":
        """[creates a TreeWalker object]

        Args:
            root ([type]): [the root node at which to begin traversal]
            whatToShow ([type], optional): [what types of nodes to show]. Defaults to None.
            filter ([type], optional): [a NodeFilter or a function to be called for each node]. Defaults to None.

        Returns:
            [type]: [a new TreeWalker object]
        """
        whatToShow = NodeFilter.SHOW_ALL if whatToShow == None else whatToShow
        return TreeWalker(root, whatToShow, filter, entityReferenceExpansion)

    @staticmethod
    def createProcessingInstruction(target: str, data: str) -> ProcessingInstruction:
        """Creates a ProcessingInstruction node with the specified target and data"""
        return ProcessingInstruction(target, data)

    @staticmethod
    def createEntityReference(name: str) -> "EntityReference":
        """Creates an EntityReference node with the specified name"""
        return EntityReference(name)

    @property
    def xmlversion(self):
        """Returns the version of XML used for the document"""
        return "1.0"

    @staticmethod
    def createCDATASection(data: str) -> CDATASection:
        """Creates a CDATASection node with the specified data"""
        return CDATASection(data)

    # @staticmethod
    # def createAttributeNS(namespaceURI, qualifiedName):
    #     """ Creates an Attr node with the specified namespace URI and qualified name """
    #     return Attr(qualifiedName)

    @staticmethod
    def createRange() -> Range:
        """Creates a Range"""
        return Range()

    @staticmethod
    def createNodeIterator(root: Node, whatToShow: int | None = None, filter: Any = None) -> NodeIterator:
        """Creates a NodeIterator that can be used to traverse the document tree or subtree under root."""
        whatToShow = NodeFilter.SHOW_ALL if whatToShow == None else whatToShow
        return NodeIterator(root, whatToShow, filter)

        # @staticmethod
        # def caretRangeFromPoint(x, y):
        # """ Returns the Range object that is the caret selection at the given coordinates. """
        # return Range()
        # raise NotImplementedError

        # @staticmethod
        # def createNSResolver(nodeResolver):
        #     """ Creates a NodeResolver """
        #     return NodeResolver(nodeResolver)

    @property
    def doctype(self):
        """Returns the Document Type Declaration associated with the document"""
        return "<!DOCTYPE html>"
        # return self.doctype = value

    @doctype.setter
    def doctype(self, value):
        """Sets the Document Type Declaration associated with the document"""
        self._doctype = value
        return

        # def documentElement(self):
        # ''' Returns the Document Element of the document (the <html> element)'''
        # return self

        # def documentMode(self):
        """ Returns the mode used by the browser to render the document"""
        # return

    def domain(self):
        """Returns the domain name of the server that loaded the document"""
        try:
            from domonic.webapi.url import URL

            return URL(getattr(self, "URL", "")).hostname or ""
        except Exception:
            return ""

    def domConfig(self):
        """Returns the DOMConfig which has settings for how html content is rendered"""
        return DOMConfig

    def elementFromPoint(self, x: float, y: float) -> Element | None:
        """Returns the topmost element at the specified coordinates."""
        hits = self.elementsFromPoint(x, y)
        return hits[0] if hits else None

    def evaluate(
        self,
        xpathExpression: str,
        contextNode: "Node" = None,
        namespaceResolver=None,
        resultType=XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,
        result=None,
    ):
        """Evaluates an XPath expression and returns the result."""
        if not isinstance(xpathExpression, str):
            raise TypeError("xpathExpression must be a string")
        if contextNode is None:
            contextNode = self
        evaluator = XPathEvaluator()
        expression = evaluator.createExpression(xpathExpression)
        result = expression.evaluate(contextNode, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        return result.nodes

    def elementsFromPoint(self, x: float, y: float) -> list[Element]:
        """Returns an array of all elements at the specified coordinates."""
        matches = []

        def walk(node):
            if isinstance(node, Element):
                rect = node.getBoundingClientRect()
                if rect.left <= x <= rect.right and rect.top <= y <= rect.bottom:
                    matches.append(node)
            for child in getattr(node, "childNodes", []):
                if isinstance(child, str):
                    continue
                walk(child)

        walk(self)
        return matches

    def caretPositionFromPoint(self, x: float, y: float) -> CaretPosition | None:
        """Returns a CaretPosition for the closest element at the given coordinates."""
        target = self.elementFromPoint(x, y)
        if target is None:
            return None
        first_child = target.firstChild
        if isinstance(first_child, Text):
            rect = target.getBoundingClientRect()
            width = max(rect.width, 1)
            text_length = len(first_child.textContent)
            relative = max(0, min(x - rect.left, width))
            offset = min(text_length, int((relative / width) * text_length))
            return CaretPosition(first_child, offset)
        return CaretPosition(target, 0)

    @property
    def embeds(self):
        """[Returns a collection of all <embed> elements the document]

        Returns:
            [type]: [a collection of all <embed> elements the document]
        """
        return self.querySelectorAll("embed")

        # def execCommand(self):
        """Invokes the specified clipboard operation on the element currently having focus."""
        # return

    @property
    def forms(self):
        """Returns a collection of all <form> elements in the document"""
        return self.querySelectorAll("form")

    def fullscreenElement(self):
        """Returns the current element that is displayed in fullscreen mode"""
        return getattr(self, "_fullscreenElement", None)

    def fullscreenEnabled(self):
        """Returns a Boolean value indicating whether the document can be viewed in fullscreen mode"""
        return False

    def getElementById(self, _id: str) -> Element | None:
        """[Returns the element that has the ID attribute with the specified value]

        Args:
            _id ([str]): [the value of the ID attribute]

        Returns:
            [type]: [the element that has the ID attribute with the specified value]
        """
        for each in self.childNodes:
            if not isinstance(each, Element):
                continue
            match = each._getElementById(_id)
            if match is not False and match is not None:
                return match

        return None

    def getElementsByName(self, name: str):
        """[Returns a NodeList containing all elements with a specified name]

        Args:
            name (str): [the name to search for]

        Returns:
            [type]: [the matching elements]
        """
        matches = HTMLCollection()

        def walk(node):
            if not isinstance(node, Element):
                return
            if node.getAttribute("name") == name:
                matches.append(node)
            for child in getattr(node, "childNodes", []):
                walk(child)

        for each in self.childNodes:
            walk(each)
        return matches

    # def hasFocus():
    # '''Returns a Boolean value indicating whether the document has focus'''
    # return

    @property
    def head(self) -> "HTMLHeadElement":
        """Returns the <head> element of the document"""
        return self.querySelector("head")

    @head.setter
    def head(self, el: "HTMLHeadElement") -> None:
        """[Sets the <head> element of the document]

        Args:
            el ([HTMLHeadElement]): [the new <head> element]

        Raises:
            DOMException: [if the el is not an HTMLHeadElement]
        """
        if not isinstance(el, HTMLHeadElement):
            raise DOMException("el must be an HTMLHeadElement")
        self.removeChild(self.head)
        if self.firstChild:
            self.insertBefore(el, self.firstChild)
        else:
            self.appendChild(el)

    @property
    def images(self):
        """Returns a collection of all <img> elements in the document"""
        return self.querySelectorAll("img")

    @property
    def implementation(self):
        """Returns the DOMImplementation object that handles this document"""
        return DOMImplementation()

    def importNode(self, node, deep=False):
        """Imports a node from another document to this document."""
        old_document = node.ownerDocument if isinstance(node, Node) else None
        if isinstance(node, Element):
            cloned = copy.deepcopy(node)
            if not deep:
                cloned.args = ()
            cloned.ownerDocument = self
            cloned._update_parents()
            cloned._iterate(cloned, lambda current: setattr(current, "ownerDocument", self))
            for current in _iter_dom_nodes(cloned):
                if isinstance(current, Element):
                    _upgrade_custom_element_instance(current)
                    _run_adopted_callback(current, old_document, self)
            return cloned
        elif isinstance(node, Comment):
            return Comment(node.data)
        elif isinstance(node, Text):
            return Text(node.data)
        elif isinstance(node, ProcessingInstruction):
            return ProcessingInstruction(node.target, node.data)
        elif isinstance(node, DocumentFragment):
            return DocumentFragment()
        elif isinstance(node, Attr):
            return Attr(node.name, node.value)
        else:
            raise Exception("Unsupported node type")

    # def inputEncoding(self):
    #     """ Returns the encoding used to access the document's resources."""
    #     return

    @property
    def lastModified(self) -> str:
        return self._lastModified

    @lastModified.setter
    def lastModified(self, value: str) -> None:
        self._lastModified = str(value)

    @property
    def links(self):
        """Returns a collection of all <a> and <area> elements in the document that have a href attribute"""
        anchors = [node for node in self.getElementsByTagName("a") if node.getAttribute("href") is not None]
        areas = [node for node in self.getElementsByTagName("area") if node.getAttribute("href") is not None]
        return anchors + areas

    # @property
    # def nodeType(self):
    #     return Node.DOCUMENT_NODE
    nodeType: int = Node.DOCUMENT_NODE

    def normalizeDocument(self):
        """Removes empty Text nodes, and joins adjacent nodes"""
        content = []
        pending_text = ""
        for each in list(self.childNodes):
            if each.nodeType == Node.TEXT_NODE:
                value = each.nodeValue or ""
                if value.strip() == "":
                    continue
                pending_text += value
                continue
            if pending_text != "":
                content.append(Text(pending_text))
                pending_text = ""
            each.normalize()
            content.append(each)
        if pending_text != "":
            content.append(Text(pending_text))
        self.args = tuple(content)
        self._update_parents()
        return

    def open(self, index="index.html"):
        """Opens an HTML output stream to collect output from document.write()"""
        self._open_filename = index
        if not os.path.exists(index):
            open(index, "w").close()
        else:
            print("File already exists")

    # def readyState(self):
    # ''' Returns the (loading) status of the document'''
    # return

    @property
    def referrer(self) -> str:
        return self._referrer

    @referrer.setter
    def referrer(self, value: str) -> None:
        self._referrer = "" if value is None else str(value)

    def renameNode(self, node, namespaceURI: str, nodename: str):
        """[Renames the specified node, and returns the renamed node.]

        Args:
            node ([type]): [the node to rename]
            namespaceURI ([type]): [a namespace URI]
            nodename ([type]): [a node name]

        Returns:
            [type]: [description]
        """
        if node.nodeType == Node.ELEMENT_NODE:
            node.nodeName = nodename
            node.namespaceURI = namespaceURI
            return node
        else:
            return False

    # def requestStorageAccess(self, storage_access_callback):
    #     """ Requests permission to access the user's storage area """
    #     return False

    # def hasStorageAccess(self):
    #     """ Returns whether the user has granted permission to access the user's storage area """
    #     return False

    # @property
    # def pictureInPictureElement(self):
    #     """ Returns the element currently in Picture-in-Picture mode, if any. """
    #     return None

    # def exitPictureInPicture(self):
    #     """ Exits Picture-in-Picture mode, if any. """
    #     return False

    @property
    def pictureInPictureEnabled(self):
        """Returns whether Picture-in-Picture mode is enabled."""
        return False

    @property
    def scripts(self):
        """[Returns a collection of <script> elements in the document]

        Returns:
            [type]: [a collection of <script> elements in the document]
        """
        return self.querySelectorAll("script")

    def strictErrorChecking(self):
        """Returns a Boolean value indicating whether to stop on the first error"""
        return False

    @property
    def title(self) -> str:
        """[gets the title of the document]

        Returns:
            [str]: The title of the document
        """
        if self.querySelector("title"):
            return self.querySelector("title").textContent
        return ""

    @title.setter
    def title(self, value: str):
        """[Sets the title of the document]

        Args:
            value ([str]): [the new title of the document]
        """
        if self.querySelector("title"):
            self.querySelector("title").textContent = value
        else:
            if not self.head:
                self.head = HTMLHeadElement()
            self.head.appendChild(HTMLTitleElement(value))

    @property
    def visibilityState(self):
        """Returns the visibility state of the document"""
        return "visible"

    def write(self, html: str = ""):
        """[writes HTML text to a document

        Args:
            html (str, optional): [the content to write to the document]
        """
        html = str(html)
        current_open_filename = self._open_filename
        if current_open_filename is not None:
            # open the file and APPEND the html to the file without losing the previous content
            with open(current_open_filename, "a") as f:
                f.write(html)
        content = DocumentFragment(html)
        self.__init__(content)
        self._open_filename = current_open_filename

    def writeln(self, html: str = ""):
        """[writes HTML text to a document, followed by a line break]

        Args:
            html (str, optional): [the content to write to the document]
        """
        self.write(html + "\n")

    # def __md__(self)
    # def __rst__(self)
    # def __json__(self)


class Location:
    # TODO - move this to the window class and remove all domonic.javascript refs in this file

    def __init__(self, url: str = None, *args, **kwargs) -> None:
        self.href = url

    def __str__(self) -> str:
        return self.href

    # def __repr__(self):
    #     return self.uri

    def origin(self):
        """Returns the protocol, hostname and port number of a URL"""
        from domonic.webapi.url import URL

        return URL(self.href or "").origin

    def search(self):
        """Sets or returns the querystring part of a URL"""
        from domonic.webapi.url import URL

        return URL(self.href or "").search

    def assign(self, url: str = "") -> None:
        """Loads a new document"""
        self.href = url
        return None

    def reload(self):
        """Reloads the current document"""
        return self.href

    def replace(self, url: str = ""):
        """Replaces the current document with a new one"""
        self.href = url
        return None


location = Location


class DocumentFragment(Node):

    nodeType: int = Node.DOCUMENT_FRAGMENT_NODE

    def __init__(self, *args: Any) -> None:
        super().__init__(*args)

    querySelector = Document.querySelector
    querySelectorAll = Document.querySelectorAll
    getElementById = Document.getElementById
    getElementsByTagName = Document.getElementsByTagName
    _matchElement = Document._matchElement
    attributes = Element.attributes

    def append(self, *nodes: Any) -> None:
        """Appends nodes or strings to the DocumentFragment."""
        items = _coerce_insertion_nodes(*nodes)
        old_documents = [
            (item, _detach_node_for_insertion(item)) for item in items
        ]
        self.args = self.args + items
        for item, old_document in old_documents:
            _connect_inserted_node(self, item, old_document)

    def prepend(self, *nodes: Any) -> None:
        """Prepends nodes or strings to the DocumentFragment."""
        items = _coerce_insertion_nodes(*nodes)
        old_documents = [
            (item, _detach_node_for_insertion(item)) for item in items
        ]
        self.args = items + self.args
        for item, old_document in old_documents:
            _connect_inserted_node(self, item, old_document)

    def replaceChildren(self, *newChildren: Any) -> None:
        """Replaces the childNodes of the DocumentFragment object."""
        for child in self.args:
            if isinstance(child, Node):
                _disconnect_tree(child)
                child.parentNode = None

        items = _coerce_replacement_nodes(*newChildren)
        old_documents = [
            (item, _detach_node_for_insertion(item)) for item in items
        ]
        self.args = items
        for item, old_document in old_documents:
            _connect_inserted_node(self, item, old_document)

    def __format__(self, format_spec):
        return self.__str__()

    def __str__(self) -> str:
        return "".join([str(a) for a in self.args])


class CharacterData(Node):
    """
    The CharacterData abstract interface represents a Node object that contains characters.
    This is an abstract interface, meaning there aren't any objects of type CharacterData:
    it is implemented by other interfaces like Text, Comment, or ProcessingInstruction, which aren't abstract.
    """

    nextElementSibling = Element.nextElementSibling
    previousElementSibling = Element.previousElementSibling

    remove = ChildNode.remove
    replaceWith = ChildNode.replaceWith
    before = ChildNode.before
    after = ChildNode.after

    def _validate_data_range(self, offset: int, count: int | None = None) -> str:
        if not isinstance(offset, int):
            raise TypeError("offset must be an integer")
        data = self.args[0] if self.args else ""
        if offset < 0 or offset > len(data):
            raise IndexError("CharacterData offset is out of bounds")
        if count is not None:
            if not isinstance(count, int):
                raise TypeError("count must be an integer")
            if count < 0:
                raise IndexError("CharacterData count is out of bounds")
        return data

    def appendData(self, data):
        """Appends the given DOMString to the CharacterData.data string; when this method returns,
        data contains the concatenated DOMString."""
        old_value = self.args[0]
        updated = self.args[0] + data
        self.args = (updated,)
        _queue_mutation_record("characterData", self, old_value=old_value)
        return updated

    def deleteData(self, offset: int, count: int):
        """Removes the specified amount of characters, starting at the specified offset,
        from the CharacterData.data string; when this method returns, data contains the shortened DOMString."""
        old_value = self._validate_data_range(offset, count)
        updated = old_value[:offset] + old_value[offset + count :]
        self.args = (updated,)
        _queue_mutation_record("characterData", self, old_value=old_value)
        return updated

    def insertData(self, offset: int, data):
        """Inserts the specified characters, at the specified offset, in the CharacterData.data string;
        when this method returns, data contains the modified DOMString."""
        old_value = self._validate_data_range(offset)
        updated = old_value[:offset] + data + old_value[offset:]
        self.args = (updated,)
        _queue_mutation_record("characterData", self, old_value=old_value)
        return updated

    def replaceData(self, offset: int, count: int, data):
        """Replaces the specified amount of characters, starting at the specified offset, with the specified DOMString;
        when this method returns, data contains the modified DOMString."""
        old_value = self._validate_data_range(offset, count)
        updated = old_value[:offset] + data + old_value[offset + count :]
        self.args = (updated,)
        _queue_mutation_record("characterData", self, old_value=old_value)
        return updated

    # def replaceWith(self, newChildren):
    #     """ Replaces the characters in the children list of its parent with a set of Node or DOMString objects. """
    #     self.replaceChildren(newChildren) # parentNode?

    def substringData(self, offset: int, length: int):
        """Returns a DOMString containing the part of CharacterData.data of the specified length and
        starting at the specified offset."""
        data = self._validate_data_range(offset, length)
        return data[offset : offset + length]


class EntityReference(Node):
    """
    The EntityReference interface represents a reference to an entity, either parsed
    or unparsed, in an Entity Node. Note that this is not a CharacterData node,
    and does not have any child nodes.
    """

    def __init__(self, *args) -> None:
        self.args = args

    def __str__(self) -> str:
        return "".join([str(a) for a in self.args])

    @staticmethod
    def ordinal(entityName: str):
        """Returns the character corresponding to the given entity name."""
        if len(entityName) != 1:
            raise ValueError("entityName must be a single character")
        return ord(entityName)

    @staticmethod
    def fromOrdinal(ordinal: int):
        """Returns the entity name corresponding to the given character."""
        return chr(ordinal)


class Entity(Node):
    def __init__(self, *args) -> None:
        self.args = args

    def __str__(self) -> str:
        return "".join([str(a) for a in self.args])

    @staticmethod
    def fromName(entityName: str) -> str:
        """Returns the entity name corresponding to the given character."""
        return chr(ord(entityName))

    @staticmethod
    def fromChar(char: str) -> str:
        """Returns the character corresponding to the given entity name."""
        return ord(char)


# class Notation(Node):

#     def __init__(self, *args):
#         self.args = args

#     def __str__(self):
#         return ''.join([str(a) for a in self.args])

#     def getPublicId(self):
#         """ Returns the public identifier of the notation. """
#         return self.args[0]

#     def getSystemId(self):
#         """ Returns the system identifier of the notation. """
#         return self.args[1]



class Text(CharacterData):
    """Text Node"""

    @property
    def wholeText(self):
        """Returns a DOMString containing all the text content of the node and its descendants."""
        if self.args and isinstance(self.args[0], str):
            return self.args[0]
        return ""

    def splitText(self, offset: int):
        """Splits the Text node into two Text nodes at the specified offset, keeping both in the tree as siblings.
        The first node is returned, while the second node is discarded and exists outside the tree."""
        self._validate_data_range(offset)
        current = self.args[0]
        head = current[:offset]
        tail = current[offset:]
        self.args = (head,)
        sibling = Text(tail)
        sibling.parentNode = self.parentNode
        if self.parentNode is not None and hasattr(self.parentNode, "args"):
            siblings = list(self.parentNode.args)
            try:
                index = siblings.index(self)
                siblings.insert(index + 1, sibling)
                self.parentNode.args = tuple(siblings)
                self.parentNode._update_parents()
            except ValueError:
                pass
        return sibling

    @property
    def assignedSlot(self):
        """Returns the slot whose assignedNodes contains this node."""
        return _assigned_slot_for_node(self)

    @property
    def data(self):
        return self.args[0]

    @data.setter
    def data(self, data):
        if not isinstance(data, str):
            raise ValueError("Data must be a string.")
        old_value = self.args[0] if self.args else ""
        self.args = (data,)
        _queue_mutation_record("characterData", self, old_value=old_value)

    nodeType: int = Node.TEXT_NODE

    @property
    def nodeName(self):
        return "#text"

    @property
    def childNodes(self):
        return ()  # Text nodes have no children


    @property
    def firstChild(self):
        return None

    # @property
    # def firstChild(self):
    #     return self.args[0]

    # @property
    # def textContent(self):
    #     return self.nodeValue

    # @textContent.setter
    # def textContent(self, content):
    #     self.nodeValue = content

    def __str__(self) -> str:
        return str(self.textContent)

    def __format__(self, format_spec):
        return str(self.textContent)

    # def __repr__(self):
    # return str(self.textContent)

    def __iter__(self):
        return iter(())  # No children for text nodes




class HTMLCollection(list):
    @property
    def length(self) -> int:
        return len(self)

    def __str__(self) -> str:
        return "".join([str(a) for a in self])

    def item(self, index: int) -> Node | None:
        """[gets the indexth item in the collection.
        If index is greater than or equal to the number of nodes in the list, this returns null.]

        Args:
            index ([type]): [the index of the item to return.]

        Returns:
            [type]: [the node at the indexth position, or None]
        """
        if 0 <= index < len(self):
            return self[index]
        else:
            return None

    def namedItem(self, name: str) -> Node | None:
        """Returns the specific node whose ID or, as a fallback, name matches the string specified by name."""
        for item in self:
            item_id = item.getAttribute("id") if hasattr(item, "getAttribute") else getattr(item, "id", None)
            item_name = item.getAttribute("name") if hasattr(item, "getAttribute") else getattr(item, "name", None)
            if item_id == name:
                return item
            elif item_name == name:
                return item
        return None

    def __getitem__(self, index: int | str):
        # can return dot notation i.e
        # index = "named.item.with.periods" # TODO - test
        if isinstance(index, str):
            names = index.split(".")
            if len(names) > 1:
                return self.namedItem(names[0]).namedItem(".".join(names[1:]))
            else:
                return self.namedItem(index)
        else:
            return super().__getitem__(index)


MutationCallback = Callable[[list["MutationRecord"], "MutationObserver"], Any]


class MutationRecord:
    """Single mutation payload delivered to a ``MutationObserver``.

    Records describe one child-list, attribute, or character-data change and
    carry the pieces of context the observer asked to receive.
    """

    __slots__ = (
        "type",
        "target",
        "addedNodes",
        "removedNodes",
        "previousSibling",
        "nextSibling",
        "attributeName",
        "attributeNamespace",
        "oldValue",
    )

    def __init__(
        self,
        type: str,
        target: Node,
        *,
        addedNodes: Iterable[Node] = (),
        removedNodes: Iterable[Node] = (),
        previousSibling: Node | None = None,
        nextSibling: Node | None = None,
        attributeName: str | None = None,
        attributeNamespace: str | None = None,
        oldValue: str | None = None,
    ) -> None:
        self.type = type
        self.target = target
        self.addedNodes = NodeList(addedNodes)
        self.removedNodes = NodeList(removedNodes)
        self.previousSibling = previousSibling
        self.nextSibling = nextSibling
        self.attributeName = attributeName
        self.attributeNamespace = attributeNamespace
        self.oldValue = oldValue


class MutationObserver:
    """Observe DOM tree mutations and receive ``MutationRecord`` batches.

    This implementation follows the familiar platform model: call ``observe()``
    with a target and options, allow DOM operations to queue records, then
    receive them through the callback or ``takeRecords()``.
    """

    _all_observers: ClassVar[list["MutationObserver"]] = []

    def __init__(self, callback: MutationCallback) -> None:
        if not callable(callback):
            raise TypeError("MutationObserver callback must be callable")
        self.callback = callback
        self._records: list[MutationRecord] = []
        self._observations: dict[Node, dict[str, Any]] = {}
        MutationObserver._all_observers.append(self)

    def disconnect(self) -> None:
        self._observations.clear()
        self._records.clear()

    def observe(self, target: Node, options: dict[str, Any]) -> None:
        if not isinstance(target, Node):
            raise TypeError("MutationObserver target must be a Node")
        self._observations[target] = _normalize_mutation_observer_options(options)

    def takeRecords(self) -> list[MutationRecord]:
        records = list(self._records)
        self._records.clear()
        return records

    def _enqueue_if_observing(self, record: MutationRecord) -> bool:
        for current in _iter_ancestors_inclusive(record.target):
            options = self._observations.get(current)
            if options is None:
                continue
            if current is not record.target and not options["subtree"]:
                continue
            if record.type == "childList" and not options["childList"]:
                continue
            if record.type == "attributes":
                if not options["attributes"]:
                    continue
                attribute_filter = options.get("attributeFilter")
                if attribute_filter is not None and record.attributeName not in attribute_filter:
                    continue
                old_value = record.oldValue if options["attributeOldValue"] else None
                filtered_record = MutationRecord(
                    "attributes",
                    record.target,
                    attributeName=record.attributeName,
                    attributeNamespace=record.attributeNamespace,
                    oldValue=old_value,
                )
                self._records.append(filtered_record)
                return True
            if record.type == "characterData":
                if not options["characterData"]:
                    continue
                old_value = record.oldValue if options["characterDataOldValue"] else None
                filtered_record = MutationRecord("characterData", record.target, oldValue=old_value)
                self._records.append(filtered_record)
                return True
            if record.type == "childList":
                self._records.append(record)
                return True
        return False

    def _flush(self) -> None:
        if not self._records:
            return
        records = self.takeRecords()
        self.callback(records, self)


class ResizeObserverSize:
    """Inline and block dimensions reported by ``ResizeObserver`` entries."""

    def __init__(self, inlineSize: float, blockSize: float) -> None:
        self.inlineSize = inlineSize
        self.blockSize = blockSize


class ResizeObserverEntry:
    """Geometry snapshot for a single observed element resize."""

    def __init__(self, target: Element, contentRect: DOMRectReadOnly) -> None:
        self.target = target
        self.contentRect = DOMRect.fromRect(contentRect)
        size = ResizeObserverSize(self.contentRect.width, self.contentRect.height)
        self.borderBoxSize = [size]
        self.contentBoxSize = [size]
        self.devicePixelContentBoxSize = [size]


ResizeObserverCallback = Callable[[list["ResizeObserverEntry"], "ResizeObserver"], Any]


class ResizeObserver:
    """Observe element box changes through DOM geometry reads.

    Domonic treats layout changes pragmatically: when relevant geometry changes
    are computed, resize entries are queued and delivered to the callback.
    """

    _all_observers: ClassVar[list["ResizeObserver"]] = []

    def __init__(self, callback: ResizeObserverCallback) -> None:
        if not callable(callback):
            raise TypeError("ResizeObserver callback must be callable")
        self.callback = callback
        self._observations: dict[Element, tuple[float, float, float, float] | None] = {}
        self._records: list[ResizeObserverEntry] = []
        ResizeObserver._all_observers.append(self)

    def observe(self, target: Element, options: dict[str, Any] | None = None) -> None:
        if not isinstance(target, Element):
            raise TypeError("ResizeObserver target must be an Element")
        self._observations[target] = None
        target.getBoundingClientRect()

    def unobserve(self, target: Element) -> None:
        self._observations.pop(target, None)

    def disconnect(self) -> None:
        self._observations.clear()
        self._records.clear()

    def takeRecords(self) -> list[ResizeObserverEntry]:
        records = list(self._records)
        self._records.clear()
        return records

    def _process(self, changed_target: Node | None = None, target_rect: DOMRectReadOnly | None = None) -> None:
        for target, previous in list(self._observations.items()):
            rect = DOMRect.fromRect(target_rect) if target is changed_target and target_rect is not None else DOMRect.fromRect(target.getBoundingClientRect())
            current = (rect.x, rect.y, rect.width, rect.height)
            if previous is None or previous != current:
                self._observations[target] = current
                self._records.append(ResizeObserverEntry(target, rect))
        self._flush()

    def _flush(self) -> None:
        if not self._records:
            return
        records = self.takeRecords()
        self.callback(records, self)


class IntersectionObserverEntry:
    """Visibility snapshot for one target observed by ``IntersectionObserver``."""

    def __init__(
        self,
        target: Element,
        rootBounds: DOMRectReadOnly,
        boundingClientRect: DOMRectReadOnly,
        intersectionRect: DOMRectReadOnly,
        time_value: float,
    ) -> None:
        self.target = target
        self.rootBounds = DOMRect.fromRect(rootBounds)
        self.boundingClientRect = DOMRect.fromRect(boundingClientRect)
        self.intersectionRect = DOMRect.fromRect(intersectionRect)
        self.time = time_value
        self.isIntersecting = self.intersectionRect.width > 0 and self.intersectionRect.height > 0
        target_area = self.boundingClientRect.width * self.boundingClientRect.height
        intersection_area = self.intersectionRect.width * self.intersectionRect.height
        self.intersectionRatio = 0.0 if target_area == 0 else intersection_area / target_area


IntersectionObserverCallback = Callable[[list["IntersectionObserverEntry"], "IntersectionObserver"], Any]


class IntersectionObserver:
    """Observe whether elements intersect a root rectangle or viewport-like area.

    Domonic models intersections using element bounding boxes and a root
    rectangle, which is enough for practical DOM-side visibility checks and
    tests.
    """

    _all_observers: ClassVar[list["IntersectionObserver"]] = []

    def __init__(self, callback: IntersectionObserverCallback, options: dict[str, Any] | None = None) -> None:
        if not callable(callback):
            raise TypeError("IntersectionObserver callback must be callable")
        self.callback = callback
        self.root = (options or {}).get("root")
        threshold = (options or {}).get("threshold", 0.0)
        self.thresholds = sorted(threshold if isinstance(threshold, list) else [threshold])
        self._observations: dict[Element, tuple[bool, float] | None] = {}
        self._records: list[IntersectionObserverEntry] = []
        IntersectionObserver._all_observers.append(self)

    def observe(self, target: Element) -> None:
        if not isinstance(target, Element):
            raise TypeError("IntersectionObserver target must be an Element")
        self._observations[target] = None
        target.getBoundingClientRect()

    def unobserve(self, target: Element) -> None:
        self._observations.pop(target, None)

    def disconnect(self) -> None:
        self._observations.clear()
        self._records.clear()

    def takeRecords(self) -> list[IntersectionObserverEntry]:
        records = list(self._records)
        self._records.clear()
        return records

    def _process(self, changed_target: Node | None = None, target_rect: DOMRectReadOnly | None = None) -> None:
        now_ms = time.perf_counter() * 1000.0
        for target, previous in list(self._observations.items()):
            bounding_rect = DOMRect.fromRect(target_rect) if target is changed_target and target_rect is not None else DOMRect.fromRect(target.getBoundingClientRect())
            if isinstance(self.root, Element):
                root_rect = DOMRect.fromRect(self.root.getBoundingClientRect())
            else:
                root_rect = DOMRect.fromRect(_default_intersection_root_rect(target, bounding_rect))
            intersection_rect = _intersect_rects(root_rect, bounding_rect)
            entry = IntersectionObserverEntry(target, root_rect, bounding_rect, intersection_rect, now_ms)
            state = (entry.isIntersecting, entry.intersectionRatio)
            if previous is None or previous != state:
                self._observations[target] = state
                self._records.append(entry)
        self._flush()

    def _flush(self) -> None:
        if not self._records:
            return
        records = self.takeRecords()
        self.callback(records, self)


class PerformanceEntry:
    def __init__(self, name: str, entryType: str, startTime: float, duration: float) -> None:
        self.name = name
        self.entryType = entryType
        self.startTime = startTime
        self.duration = duration

    def toJSON(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "entryType": self.entryType,
            "startTime": self.startTime,
            "duration": self.duration,
        }


class PerformanceMark(PerformanceEntry):
    def __init__(self, name: str, startTime: float) -> None:
        super().__init__(name, "mark", startTime, 0.0)


class PerformanceMeasure(PerformanceEntry):
    def __init__(self, name: str, startTime: float, duration: float) -> None:
        super().__init__(name, "measure", startTime, duration)


PerformanceObserverCallback = Callable[[list["PerformanceEntry"], "PerformanceObserver"], Any]


class PerformanceObserver:
    supportedEntryTypes: ClassVar[list[str]] = ["mark", "measure"]
    _all_observers: ClassVar[list["PerformanceObserver"]] = []

    def __init__(self, callback: PerformanceObserverCallback) -> None:
        if not callable(callback):
            raise TypeError("PerformanceObserver callback must be callable")
        self.callback = callback
        self._entry_types: set[str] = set()
        self._records: list[PerformanceEntry] = []
        PerformanceObserver._all_observers.append(self)

    def observe(self, options: dict[str, Any]) -> None:
        entry_types = options.get("entryTypes")
        if not entry_types:
            raise TypeError("PerformanceObserver.observe requires entryTypes")
        self._entry_types = set(entry_types)
        if options.get("buffered"):
            try:
                from domonic.javascript import performance as js_performance

                for entry in js_performance.getEntries():
                    self._enqueue(entry)
            except Exception:
                pass
        self._flush()

    def disconnect(self) -> None:
        self._entry_types.clear()
        self._records.clear()

    def takeRecords(self) -> list[PerformanceEntry]:
        records = list(self._records)
        self._records.clear()
        return records

    def _enqueue(self, entry: PerformanceEntry) -> None:
        if entry.entryType in self._entry_types:
            self._records.append(entry)

    def _flush(self) -> None:
        if not self._records:
            return
        records = self.takeRecords()
        self.callback(records, self)

    @classmethod
    def _notify_entry(cls, entry: PerformanceEntry) -> None:
        for observer in list(cls._all_observers):
            observer._enqueue(entry)
            observer._flush()


class DOMException(Exception):
    """The DOMException interface represents an anormal event related to the DOM."""

    INDEX_SIZE_ERR: int = 1
    DOMSTRING_SIZE_ERR: int = 2
    HIERARCHY_REQUEST_ERR: int = 3
    WRONG_DOCUMENT_ERR: int = 4
    INVALID_CHARACTER_ERR: int = 5
    NO_DATA_ALLOWED_ERR: int = 6
    NO_MODIFICATION_ALLOWED_ERR: int = 7
    NOT_FOUND_ERR: int = 8
    NOT_SUPPORTED_ERR: int = 9
    INUSE_ATTRIBUTE_ERR: int = 10
    INVALID_STATE_ERR: int = 11
    SYNTAX_ERR: int = 12
    INVALID_MODIFICATION_ERR: int = 13
    NAMESPACE_ERR: int = 14
    INVALID_ACCESS_ERR: int = 15
    VALIDATION_ERR: int = 16
    TYPE_MISMATCH_ERR: int = 17
    SECURITY_ERR: int = 18
    NETWORK_ERR: int = 19
    ABORT_ERR: int = 20
    URL_MISMATCH_ERR: int = 21
    QUOTA_EXCEEDED_ERR: int = 22
    TIMEOUT_ERR: int = 23
    INVALID_NODE_TYPE_ERR: int = 24
    DATA_CLONE_ERR: int = 25

    def __init__(self, code, message: str | None = None) -> None:
        self.code = code
        self.message: str = message
        self.name = "DOMException"

    def __str__(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return self.message


class DOMTimeStamp(int):
    """The DOMTimeStamp interface represents a numeric value which represents the
    number of milliseconds since the epoch."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)


class DOMPoint(vec3):
    """The DOMPoint interface represents a point specified by x and y coordinates."""

    @staticmethod
    def fromPoint(point: Any) -> "DOMPoint":
        return DOMPoint(point.x, point.y, point.z, point.w)

    def __init__(self, x: float, y: float, z: float = 0, w: float = 1) -> None:
        self.x: float = x
        self.y: float = y
        self.z: float = z
        self.w: float = w
        super().__init__(x, y, z)

    def __str__(self) -> str:
        return "({}, {}, {}, {})".format(self.x, self.y, self.z, self.w)

    def __repr__(self) -> str:
        return "({}, {}, {}, {})".format(self.x, self.y, self.z, self.w)


class DOMPointReadOnly(DOMPoint):
    """The DOMPointReadOnly interface represents a point specified by x and y coordinates."""

    @staticmethod
    def fromPoint(point: Any) -> "DOMPointReadOnly":
        return DOMPointReadOnly(point.x, point.y, point.z, point.w)

    def __init__(self, x: float, y: float, z: float = 0, w: float = 1) -> None:
        self.x: float = x
        self.y: float = y
        self.z: float = z
        self.w: float = w
        super().__init__(x, y, z, w)

    def __str__(self) -> str:
        return "({}, {}, {}, {})".format(self.x, self.y, self.z, self.w)

    def __repr__(self) -> str:
        return "({}, {}, {}, {})".format(self.x, self.y, self.z, self.w)


class DOMMatrixReadOnly:
    """Read-only 4x4 transformation matrix for DOM geometry APIs.

    Supports the common 2D aliases as well as the full 4x4 member set used by
    transforms, points, and animation/geometry helpers.
    """

    @staticmethod
    def fromFloat64Array(array: Iterable[float]) -> "DOMMatrixReadOnly":
        return DOMMatrixReadOnly(*list(array))

    @staticmethod
    def fromFloat32Array(array: Iterable[float]) -> "DOMMatrixReadOnly":
        return DOMMatrixReadOnly.fromFloat64Array(array)

    @staticmethod
    def fromMatrix(matrix: Any | None = None) -> "DOMMatrixReadOnly":
        if matrix is None:
            return DOMMatrixReadOnly()
        values = []
        for row in range(1, 5):
            for col in range(1, 5):
                values.append(getattr(matrix, f"m{row}{col}", 1.0 if row == col else 0.0))
        return DOMMatrixReadOnly(*values)

    def __init__(self, *values: float) -> None:
        if not values:
            values = (
                1.0, 0.0, 0.0, 0.0,
                0.0, 1.0, 0.0, 0.0,
                0.0, 0.0, 1.0, 0.0,
                0.0, 0.0, 0.0, 1.0,
            )
        if len(values) == 6:
            a, b, c, d, e, f = values
            values = (
                a, b, 0.0, 0.0,
                c, d, 0.0, 0.0,
                0.0, 0.0, 1.0, 0.0,
                e, f, 0.0, 1.0,
            )
        if len(values) != 16:
            raise TypeError("DOMMatrix requires 6 or 16 values")
        self._values = [float(value) for value in values]

    def _get(self, row: int, col: int) -> float:
        return self._values[(row - 1) * 4 + (col - 1)]

    def _set(self, row: int, col: int, value: float) -> None:
        self._values[(row - 1) * 4 + (col - 1)] = float(value)

    @property
    def is2D(self) -> bool:
        return (
            self.m13 == 0.0
            and self.m14 == 0.0
            and self.m23 == 0.0
            and self.m24 == 0.0
            and self.m31 == 0.0
            and self.m32 == 0.0
            and self.m34 == 0.0
            and self.m43 == 0.0
            and self.m33 == 1.0
            and self.m44 == 1.0
        )

    @property
    def isIdentity(self) -> bool:
        return self._values == [
            1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0,
        ]

    @property
    def a(self) -> float:
        return self.m11

    @property
    def b(self) -> float:
        return self.m12

    @property
    def c(self) -> float:
        return self.m21

    @property
    def d(self) -> float:
        return self.m22

    @property
    def e(self) -> float:
        return self.m41

    @property
    def f(self) -> float:
        return self.m42

    def __str__(self) -> str:
        return f"DOMMatrix({', '.join(str(v) for v in self._values)})"

    def toFloat64Array(self) -> list[float]:
        return list(self._values)

    def toFloat32Array(self) -> list[float]:
        return list(self._values)

    def toJSON(self) -> dict[str, float | bool]:
        data = {f"m{row}{col}": self._get(row, col) for row in range(1, 5) for col in range(1, 5)}
        data.update({"is2D": self.is2D, "isIdentity": self.isIdentity})
        return data

    def multiply(self, other: Any) -> "DOMMatrix":
        return DOMMatrix.fromMatrix(self).multiplySelf(other)

    def translate(self, tx: float = 0, ty: float = 0, tz: float = 0) -> "DOMMatrix":
        return DOMMatrix.fromMatrix(self).translateSelf(tx, ty, tz)

    def scale(self, scaleX: float = 1, scaleY: float | None = None, scaleZ: float = 1) -> "DOMMatrix":
        return DOMMatrix.fromMatrix(self).scaleSelf(scaleX, scaleY, scaleZ)

    def inverse(self) -> "DOMMatrix":
        return DOMMatrix.fromMatrix(self).invertSelf()

    def transformPoint(self, point: Any | None = None) -> DOMPoint:
        if point is None:
            point = DOMPoint(0, 0, 0, 1)
        x = getattr(point, "x", 0.0)
        y = getattr(point, "y", 0.0)
        z = getattr(point, "z", 0.0)
        w = getattr(point, "w", 1.0)
        values = self._values
        return DOMPoint(
            x * values[0] + y * values[4] + z * values[8] + w * values[12],
            x * values[1] + y * values[5] + z * values[9] + w * values[13],
            x * values[2] + y * values[6] + z * values[10] + w * values[14],
            x * values[3] + y * values[7] + z * values[11] + w * values[15],
        )


for _row in range(1, 5):
    for _col in range(1, 5):
        setattr(
            DOMMatrixReadOnly,
            f"m{_row}{_col}",
            property(lambda self, r=_row, c=_col: self._get(r, c)),
        )


class DOMMatrix(DOMMatrixReadOnly):
    """Mutable ``DOMMatrix`` implementation.

    Use this when you want to construct, compose, invert, or transform points
    with a matrix that can be updated in place.
    """

    @staticmethod
    def fromFloat64Array(array: Iterable[float]) -> "DOMMatrix":
        return DOMMatrix(*list(array))

    @staticmethod
    def fromFloat32Array(array: Iterable[float]) -> "DOMMatrix":
        return DOMMatrix.fromFloat64Array(array)

    @staticmethod
    def fromMatrix(matrix: Any | None = None) -> "DOMMatrix":
        readonly = DOMMatrixReadOnly.fromMatrix(matrix)
        return DOMMatrix(*readonly.toFloat64Array())

    @DOMMatrixReadOnly.a.setter
    def a(self, value: float) -> None:
        self.m11 = value

    @DOMMatrixReadOnly.b.setter
    def b(self, value: float) -> None:
        self.m12 = value

    @DOMMatrixReadOnly.c.setter
    def c(self, value: float) -> None:
        self.m21 = value

    @DOMMatrixReadOnly.d.setter
    def d(self, value: float) -> None:
        self.m22 = value

    @DOMMatrixReadOnly.e.setter
    def e(self, value: float) -> None:
        self.m41 = value

    @DOMMatrixReadOnly.f.setter
    def f(self, value: float) -> None:
        self.m42 = value

    def multiplySelf(self, other: Any) -> "DOMMatrix":
        other_matrix = DOMMatrixReadOnly.fromMatrix(other)
        left = self._values
        right = other_matrix._values
        result = [0.0] * 16
        for row in range(4):
            for col in range(4):
                result[row * 4 + col] = sum(left[row * 4 + k] * right[k * 4 + col] for k in range(4))
        self._values = result
        return self

    def translateSelf(self, tx: float = 0, ty: float = 0, tz: float = 0) -> "DOMMatrix":
        translation = DOMMatrix(
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            tx, ty, tz, 1,
        )
        return self.multiplySelf(translation)

    def scaleSelf(self, scaleX: float = 1, scaleY: float | None = None, scaleZ: float = 1) -> "DOMMatrix":
        if scaleY is None:
            scaleY = scaleX
        scale = DOMMatrix(
            scaleX, 0, 0, 0,
            0, scaleY, 0, 0,
            0, 0, scaleZ, 0,
            0, 0, 0, 1,
        )
        return self.multiplySelf(scale)

    def invertSelf(self) -> "DOMMatrix":
        matrix = [[self._values[row * 4 + col] for col in range(4)] for row in range(4)]
        identity = [[1.0 if row == col else 0.0 for col in range(4)] for row in range(4)]
        for col in range(4):
            pivot = max(range(col, 4), key=lambda row: abs(matrix[row][col]))
            if matrix[pivot][col] == 0:
                raise ValueError("Matrix is not invertible")
            matrix[col], matrix[pivot] = matrix[pivot], matrix[col]
            identity[col], identity[pivot] = identity[pivot], identity[col]
            factor = matrix[col][col]
            matrix[col] = [value / factor for value in matrix[col]]
            identity[col] = [value / factor for value in identity[col]]
            for row in range(4):
                if row == col:
                    continue
                factor = matrix[row][col]
                matrix[row] = [current - factor * pivot_value for current, pivot_value in zip(matrix[row], matrix[col])]
                identity[row] = [current - factor * pivot_value for current, pivot_value in zip(identity[row], identity[col])]
        self._values = [identity[row][col] for row in range(4) for col in range(4)]
        return self


for _row in range(1, 5):
    for _col in range(1, 5):
        readonly_prop = getattr(DOMMatrixReadOnly, f"m{_row}{_col}")
        setattr(
            DOMMatrix,
            f"m{_row}{_col}",
            readonly_prop.setter(lambda self, value, r=_row, c=_col: self._set(r, c, value)),
        )


class DOMQuad:
    """The DOMQuad interface represents a quadrilateral on the plane with its
    four corners represented as Cartesian coordinates."""

    @staticmethod
    def fromRect(rect: DOMRect) -> "DOMQuad":
        return DOMQuad(
            DOMPointReadOnly(rect.left, rect.top),
            DOMPointReadOnly(rect.right, rect.top),
            DOMPointReadOnly(rect.right, rect.bottom),
            DOMPointReadOnly(rect.left, rect.bottom),
        )

    @staticmethod
    def fromQuad(quad: Any) -> "DOMQuad":
        return DOMQuad(quad.p1.x, quad.p1.y, quad.p2.x, quad.p2.y, quad.p3.x, quad.p3.y, quad.p4.x, quad.p4.y)

    @staticmethod
    def getBounds(quad: "DOMQuad") -> DOMRect:
        xs = [quad.p1.x, quad.p2.x, quad.p3.x, quad.p4.x]
        ys = [quad.p1.y, quad.p2.y, quad.p3.y, quad.p4.y]
        left = min(xs)
        top = min(ys)
        right = max(xs)
        bottom = max(ys)
        return DOMRect(left, top, right - left, bottom - top)

    @staticmethod
    def toJSON(quad: DOMQuad) -> dict[str, dict[str, float]]:
        return {
            "p1": {"x": quad.p1.x, "y": quad.p1.y},
            "p2": {"x": quad.p2.x, "y": quad.p2.y},
            "p3": {"x": quad.p3.x, "y": quad.p3.y},
            "p4": {"x": quad.p4.x, "y": quad.p4.y},
        }

    def __init__(self, p1: Any, p2: Any, p3: Any, p4: Any) -> None:
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4

    def __str__(self):
        return "({}, {}, {}, {})".format(self.p1, self.p2, self.p3, self.p4)


# NodeFilter
# from xml.dom.NodeFilter import NodeFilter
# https://bspaans.github.io/python-mingus/_modules/xml/dom/xmlbuilder.html
# https://www.w3.org/TR/2003/WD-DOM-Level-3-LS-20030226/load-save.html
# https://bspaans.github.io/python-mingus/_modules/xml/dom/xmlbuilder.html
class NodeFilter:

    SHOW_ALL: int = 0xFFFFFFFF
    SHOW_ELEMENT: int = 0x00000001
    SHOW_ATTRIBUTE: int = 0x00000002
    SHOW_TEXT: int = 0x00000004
    SHOW_CDATA_SECTION: int = 0x00000008
    SHOW_ENTITY_REFERENCE: int = 0x00000010
    SHOW_ENTITY: int = 0x00000020
    SHOW_PROCESSING_INSTRUCTION: int = 0x00000040
    SHOW_COMMENT: int = 0x00000080
    SHOW_DOCUMENT: int = 0x00000100
    SHOW_DOCUMENT_TYPE: int = 0x00000200
    SHOW_DOCUMENT_FRAGMENT: int = 0x00000400
    SHOW_NOTATION: int = 0x00000800

    FILTER_ACCEPT: int = 1
    FILTER_REJECT: int = 2
    FILTER_SKIP: int = 3

    # def acceptNode(node):
    # return NodeFilter.FILTER_ACCEPT
    # return node

    # def acceptNode(node):
    # result
    # if active:
    #     raise Exception('DOMException: INVALID_STATE_ERR')

    # active = True
    # result = filter(node)
    # active = False

    # return result


class NodeIterator:
    """[NodeIterator is an iterator object that iterates over the descendants of a node, in tree order.]"""

    def __init__(
        self,
        root: Node,
        whatToShow: int = NodeFilter.SHOW_ALL,
        filter: Any = None,
        entityReferenceExpansion: bool = False,
    ) -> None:
        self.root = root
        self.whatToShow = whatToShow
        self._filter = filter
        self.entityReferenceExpansion = entityReferenceExpansion
        self.node = root
        self.pointer = -1
        self.stack: list[Node] = []

        def collect(node: Node) -> None:
            self.stack.append(node)
            for child in getattr(node, "childNodes", []):
                if isinstance(child, str):
                    continue
                collect(child)

        collect(root)

    @property
    def filter(self) -> Any:
        return self._filter

    # def expandEntityReferences(self, expand):
    # Is a boolean value indicating if,
    # when discarding an EntityReference its whole sub-tree must be discarded at the same time.

    def referenceNode(self) -> Node:
        """Returns the Node that is being iterated over."""
        return self.node

    def pointerBeforeReferenceNode(self) -> bool:
        """Returns a boolean flag that indicates whether the NodeIterator
        is anchored before, the flag being true,
        or after, the flag being false, the anchor node.
        """
        return self.pointer < 0

    def detach(self) -> None:
        # This operation is a no-op. It doesn't do anything.
        # Previously it was telling the engine that the NodeIterator was no more used, but this is now useless.
        pass

    def previousNode(self) -> Node | None:
        """Returns the previous Node in the document, or null if there are none."""
        if self.pointer <= 0:
            return None
        self.pointer -= 1
        self.node = self.stack[self.pointer]
        return self.node

    def nextNode(self) -> Node | None:
        """Returns the next Node in the document, or null if there are none."""
        self.pointer += 1
        while self.pointer < len(self.stack):
            candidate = self.stack[self.pointer]
            if nodeFilter(self, candidate) == NodeFilter.FILTER_ACCEPT:
                self.node = candidate
                return candidate
            self.pointer += 1
        return None


mapChild = {"first": "firstChild", "last": "lastChild", "next": "firstChild", "previous": "lastChild"}

mapSibling = {"next": "nextSibling", "previous": "previousSibling"}

# toString = mapChild.toString

# def _is(x, _type):
#     print('!!!!!!!!!!!!!!!!!!! comparing', x, _type)
#     return mapChild[x].toLowerCase() == '[object ' + _type.toLowerCase() + ']'


def nodeFilter(tw: NodeIterator | TreeWalker, node: Node) -> int:
    # Maps nodeType to whatToShow
    # print(node, type(node))
    # if isinstance(node, (str)): #, Text)):
    # node = Text(node)
    # return NodeFilter.FILTER_SKIP
    # return NodeFilter.FILTER_REJECT
    if not (((1 << (node.nodeType - 1)) & tw.whatToShow)):
        return NodeFilter.FILTER_SKIP
    if tw._filter == None:
        return NodeFilter.FILTER_ACCEPT
    if callable(tw._filter):
        return tw._filter(node)
    return tw._filter.acceptNode(node)


def str_to_TextNode(content_str: Any) -> Any:
    if isinstance(content_str, str):
        return Text(content_str)
    return content_str


def traverseChildren(tw: TreeWalker, _type: str) -> Node | None:
    # var child, node, parent, result, sibling
    # print('mapChild[_type]', mapChild[_type])
    node = getattr(
        tw.currentNode, mapChild[_type]
    )  # TODO - allow dict access to node props?.... tw.currentNode[mapChild[_type]]
    # print('tw.currentNode', tw.currentNode)
    # node = str_to_TextNode(node)
    while node != None:
        # node = str_to_TextNode(node)
        result = nodeFilter(tw, node)
        if result == NodeFilter.FILTER_ACCEPT:
            tw.currentNode = node
            return node
        if result == NodeFilter.FILTER_SKIP:
            child = getattr(node, mapChild[_type])
            if child != None:
                node = child
                continue
        while node != None:
            sibling = getattr(node, mapSibling["next" if _type == "first" else "previous"])
            if sibling != None:
                node = sibling
                break
            parent = node.parentNode
            if parent == None or parent == tw.root or parent == tw.currentNode:
                return None
            else:
                node = parent
    return None


def traverseSiblings(tw: TreeWalker, type: str) -> Node | None:
    # node, result, sibling
    node = tw.currentNode
    if node == tw.root:
        return None
    while True:
        sibling = getattr(node, mapSibling[type])
        while sibling != None:
            node = sibling
            result = nodeFilter(tw, node)
            if result == NodeFilter.FILTER_ACCEPT:
                tw.currentNode = node
                return node
            sibling = getattr(node, mapChild[type])
            if result == NodeFilter.FILTER_REJECT:
                sibling = getattr(node, mapSibling[type])
        node = node.parentNode
        if node == None or node == tw.root:
            return None
        if nodeFilter(tw, node) == NodeFilter.FILTER_ACCEPT:
            return None


def nextSkippingChildren(node: Node, stayWithin: Node) -> Node | None:

    # if isinstance(node, str):
    # node = Text(node)
    # return None
    # TODO - casting is not enough. as the Text node does not know its siblings
    # print( "nsc", node, "??", stayWithin )
    # print( "AND:", node.nextSibling )

    if node == stayWithin:
        # print('a')
        return None
    if node.nextSibling != None:
        # print('b')
        return node.nextSibling

    while node.parentNode != None:
        # print('c')
        node = node.parentNode
        if node == stayWithin:
            # print('d')
            return None
        if node.nextSibling != None:
            # print('e')
            return node.nextSibling
    return None


# https://developer.mozilla.org/en-US/docs/Web/API/TreeWalker
class TreeWalker:
    """The TreeWalker object represents the nodes of a document subtree and a position within them."""

    def _upgrade_dom(self) -> None:
        """[
            Our dom has some strings that are not Text Nodes
            so we have to upgrade them to Node objects. As we can't know siblings otherwise
            # TODO - consider upgrading as they are created.
        ]
        """

        def upgrade(el: Node) -> None:
            if isinstance(el, (Text, str)):
                return
            for child in el:
                if isinstance(child, str):
                    # print('doin one')
                    newchild = Text(child)
                    el.replaceChild(newchild, child)
                    newchild.parentNode = el

        self._root._iterate(self._root, upgrade)

    def __init__(
        self,
        node: Node,
        whatToShow: int = NodeFilter.SHOW_ALL,
        _filter: Any = None,
        expandEntityReferences: bool = False,
    ) -> None:
        self._root = node
        self._upgrade_dom()
        # print("test", type(self._root[0][0]))

        self.currentNode = node
        # TODO - convert whatToShow to a number?
        self.whatToShow = whatToShow
        # self.whatToShow = self.whatToShow & 0xFFFFFFFF
        self.whatToShow = whatToShow or 0

        self._filter = _filter

        def acceptNode(node: Node) -> int:
            nonlocal _filter
            # result
            # if active:
            #     raise Exception('DOMException: INVALID_STATE_ERR')

            # active = True
            result = _filter(node)
            # active = False
            return result

        if self._filter is not None:
            NodeFilter.acceptNode = acceptNode

        self.last = None
        self.parent = None
        self.previous = None
        self.children: list[Node] = []
        self.childIndex = 0

        self.tree = None

        """ Is a boolean value indicating,
            when discarding an entity reference its whole sub-tree must be discarded at the same time. """
        self.expandEntityReferences = expandEntityReferences

    @property
    def root(self) -> Node:
        """Returns a Node representing the root node as specified when the TreeWalker was created."""
        return self._root

    def whatToShow(self, options: int) -> int:
        """Returns an unsigned long being a bitmask made of constants describing the types of Node that must be presented.
        Non-matching nodes are skipped, but their children may be included, if relevant. The possible values are:"""
        return options

    # def filter(self, options):
    #     """ Returns a NodeFilter object that can be used to filter the nodes that the TreeWalker visits. """
    #     return options

    # @property
    # def currentNode(self):
    #     """ Is the Node on which the TreeWalker is currently pointing at. """
    #     return self.currentNode

    def parentNode(self) -> Node | None:
        """Moves the current Node to the first visible ancestor node in the document order,
        and returns the found node. It also moves the current node to this one. If no such node exists,
        or if it is before that the root node defined at the object construction,
        returns null and the current node is not changed."""
        # return self.currentNode.parentNode
        node = self.currentNode
        while node != None and node != self.root:
            node = node.parentNode
            if node != None and nodeFilter(self, node) == NodeFilter.FILTER_ACCEPT:
                self.currentNode = node
                return node
        return None

    def firstChild(self) -> Node | None:
        """Moves the current Node to the first visible child of the current node, and returns the found child.
        It also moves the current node to this child. If no such child exists,
        returns null and the current node is not changed."""
        # return self.currentNode.firstChild
        return traverseChildren(self, "first")

    def lastChild(self) -> Node | None:
        """Moves the current Node to the last visible child of the current node, and returns the found child.
        It also moves the current node to this child.
        If no such child exists, null is returned and the current node is not changed."""
        # return self.currentNode.lastChild
        return traverseChildren(self, "last")

    def previousSibling(self) -> Node | None:
        """Moves the current Node to its previous sibling, if any, and returns the found sibling.
        If there is no such node, return null and the current node is not changed.
        """
        # return self.previous
        return traverseSiblings(self, "previous")

    def nextSibling(self) -> Node | None:
        """Moves the current Node to its next sibling, if any, and returns the found sibling.
        If there is no such node, null is returned and the current node is not changed."""
        # return self.currentNode.nextSibling
        return traverseSiblings(self, "next")

    def previousNode(self):
        """Moves the current Node to the previous visible node in the document order,
        and returns the found node. It also moves the current node to this one.
        If no such node exists, or if it is before that the root node defined at the object construction,
        returns null and the current node is not changed."""
        # return self.previous
        # raise NotImplementedError()
        # var node, result, sibling
        node = self.currentNode
        while node != self.root:
            sibling = node.previousSibling
            while sibling != None:
                node = sibling
                result = nodeFilter(self, node)
                while result != NodeFilter.FILTER_REJECT and node.lastChild != None:
                    node = node.lastChild
                    result = nodeFilter(self, node)
                if result == NodeFilter.FILTER_ACCEPT:
                    self.currentNode = node
                    return node
            if node == self.root or node.parentNode == None:
                return None
            node = node.parentNode
            if nodeFilter(self, node) == NodeFilter.FILTER_ACCEPT:
                self.currentNode = node
                return node
        return None

    def nextNode(self):
        """Moves the current Node to the next visible node in the document order, and returns the found node.
        It also moves the current node to this one.
        If no such node exists, returns None and the current node is not changed.
        can be used in a while loop to iterate over all the nodes in the document order.
        """
        # var node, result, following;
        node = self.currentNode

        if isinstance(node, str):
            node = Text(node)
            # return node

        result = NodeFilter.FILTER_ACCEPT
        while True:
            # print('rrr:::', result, node)
            if isinstance(node, str):
                Text(node)
                # continue

            while result != NodeFilter.FILTER_REJECT and node.firstChild != None:
                # print('rrr222:::', result, node)
                node = node.firstChild
                if isinstance(node, str):
                    node = Text(node)
                    # result = NodeFilter.FILTER_REJECT
                    # continue
                    # break
                    # return None

                result = nodeFilter(self, node)
                if result == NodeFilter.FILTER_ACCEPT:
                    self.currentNode = node
                    return node
            following = nextSkippingChildren(node, self.root)
            if following != None:
                node = following
            else:
                # print('NONE')
                return None
            result = nodeFilter(self, node)
            if result == NodeFilter.FILTER_ACCEPT:
                self.currentNode = node
                return node


# TODO - create fetch package and move the js fetch stuff to it?
# fetch api

# AbortController
# AbortSignal
# Cache
# CacheStorage
# ContentIndex
# ContactPicker
# Client - serviceworker api
# CredentialsContainer - new login api
# DOMMatrix #https://developer.mozilla.org/en-US/docs/Web/API/DOMMatrix
# DOMParser
# IndexedDB API
# ImageBitmap
# ImageBitmapRenderingContext
# ImageData
# MutationObserver
# MutationRecord
# OverconstrainedError
# QueueingStrategy
# ReadableStream
# SCTP
# SourceBuffer
# SourceBufferAppendMode
# SourceBufferAppendWindowEnd
# TimeRanges - media
# TrackEvent - media
# ValidityState
# Web Share API
# WebGL
# also
# https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API

# HTMLElementTagNameMap < how many of these types are there?

# XMLSerializer = xml.dom.minidom.XMLSerializer?
# XMLSerializer.serializeToString(rootNode)


class Sanitizer:
    def __init__(self, rules=None, *args, **kwargs):
        """Creates and returns a Sanitizer object."""

        # casting as object gives us . notation
        from domonic.javascript import Object

        self._default_configuration = Object(
            {
                "allowCustomElements": False,
                # "allowElements": [],  # elements that the sanitizer should retain in the input.
                "blockElements": [],  # elements where the sanitizer should remove the elements from the input, but retain their children.
                "dropElements": [],  # elements that the sanitizer should remove from the input, including its children.
                # "allowAttributes": [],  # determines whether an attribute (on a given element) should be allowed.
                "dropAttributes": [],  # determines whether an attribute (on a given element) should be dropped.
                "allowCustomElements": False,  # determines whether custom elements are to be considered. The default is to drop them. If this option is true, custom elements will still be checked against all other built-in or configured configured checks.
                "allowComments": False,  # determines whether HTML comments are allowed.
                "allowElements": [
                    "a",
                    "abbr",
                    "acronym",
                    "address",
                    "area",
                    "article",
                    "aside",
                    "audio",
                    "b",
                    "bdi",
                    "bdo",
                    "bgsound",
                    "big",
                    "blockquote",
                    "body",
                    "br",
                    "button",
                    "canvas",
                    "caption",
                    "center",
                    "cite",
                    "code",
                    "col",
                    "colgroup",
                    "datalist",
                    "dd",
                    "del",
                    "details",
                    "dfn",
                    "dialog",
                    "dir",
                    "div",
                    "dl",
                    "dt",
                    "em",
                    "fieldset",
                    "figcaption",
                    "figure",
                    "font",
                    "footer",
                    "form",
                    "h1",
                    "h2",
                    "h3",
                    "h4",
                    "h5",
                    "h6",
                    "head",
                    "header",
                    "hgroup",
                    "hr",
                    "html",
                    "i",
                    "img",
                    "input",
                    "ins",
                    "kbd",
                    "keygen",
                    "label",
                    "layer",
                    "legend",
                    "li",
                    "link",
                    "listing",
                    "main",
                    "map",
                    "mark",
                    "marquee",
                    "menu",
                    "meta",
                    "meter",
                    "nav",
                    "nobr",
                    "ol",
                    "optgroup",
                    "option",
                    "output",
                    "p",
                    "picture",
                    "popup",
                    "pre",
                    "progress",
                    "q",
                    "rb",
                    "rp",
                    "rt",
                    "rtc",
                    "ruby",
                    "s",
                    "samp",
                    "section",
                    "select",
                    "selectedcontent",
                    "selectmenu",
                    "small",
                    "source",
                    "span",
                    "strike",
                    "strong",
                    "style",
                    "sub",
                    "summary",
                    "sup",
                    "table",
                    "tbody",
                    "td",
                    "tfoot",
                    "th",
                    "thead",
                    "time",
                    "tr",
                    "track",
                    "tt",
                    "u",
                    "ul",
                    "var",
                    "video",
                    "wbr",
                ],
                "allowAttributes": {
                    "abbr": ["*"],
                    "accept": ["*"],
                    "accept-charset": ["*"],
                    "accesskey": ["*"],
                    "action": ["*"],
                    "align": ["*"],
                    "alink": ["*"],
                    "alpha": ["*"],
                    "allow": ["*"],
                    "allowfullscreen": ["*"],
                    "alt": ["*"],
                    "anchor": ["*"],
                    "archive": ["*"],
                    "as": ["*"],
                    "async": ["*"],
                    "autocapitalize": ["*"],
                    "autocomplete": ["*"],
                    "autocorrect": ["*"],
                    "autofocus": ["*"],
                    "autopictureinpicture": ["*"],
                    "autoplay": ["*"],
                    "axis": ["*"],
                    "background": ["*"],
                    "behavior": ["*"],
                    "bgcolor": ["*"],
                    "border": ["*"],
                    "bordercolor": ["*"],
                    "blocking": ["*"],
                    "browsingtopics": ["*"],
                    "capture": ["*"],
                    "cellpadding": ["*"],
                    "cellspacing": ["*"],
                    "challenge": ["*"],
                    "char": ["*"],
                    "charoff": ["*"],
                    "charset": ["*"],
                    "checked": ["*"],
                    "cite": ["*"],
                    "class": ["*"],
                    "classid": ["*"],
                    "clear": ["*"],
                    "code": ["*"],
                    "codebase": ["*"],
                    "codetype": ["*"],
                    "color": ["*"],
                    "cols": ["*"],
                    "colspan": ["*"],
                    "colorspace": ["*"],
                    "compact": ["*"],
                    "closedby": ["*"],
                    "command": ["*"],
                    "commandfor": ["*"],
                    "content": ["*"],
                    "contenteditable": ["*"],
                    "controls": ["*"],
                    "controlslist": ["*"],
                    "conversiondestination": ["*"],
                    "coords": ["*"],
                    "credentialless": ["*"],
                    "crossorigin": ["*"],
                    "csp": ["*"],
                    "data": ["*"],
                    "datetime": ["*"],
                    "declare": ["*"],
                    "decoding": ["*"],
                    "default": ["*"],
                    "defer": ["*"],
                    "dir": ["*"],
                    "direction": ["*"],
                    "dirname": ["*"],
                    "disabled": ["*"],
                    "disablepictureinpicture": ["*"],
                    "disableremoteplayback": ["*"],
                    "disallowdocumentaccess": ["*"],
                    "download": ["*"],
                    "draggable": ["*"],
                    "elementtiming": ["*"],
                    "enctype": ["*"],
                    "end": ["*"],
                    "enterkeyhint": ["*"],
                    "event": ["*"],
                    "exportparts": ["*"],
                    "face": ["*"],
                    "fetchpriority": ["*"],
                    "for": ["*"],
                    "form": ["*"],
                    "formaction": ["*"],
                    "formenctype": ["*"],
                    "formmethod": ["*"],
                    "formnovalidate": ["*"],
                    "formtarget": ["*"],
                    "frame": ["*"],
                    "frameborder": ["*"],
                    "headers": ["*"],
                    "headingoffset": ["*"],
                    "headingreset": ["*"],
                    "height": ["*"],
                    "hidden": ["*"],
                    "high": ["*"],
                    "href": ["*"],
                    "hreflang": ["*"],
                    "hreftranslate": ["*"],
                    "hspace": ["*"],
                    "http-equiv": ["*"],
                    "id": ["*"],
                    "imagesizes": ["*"],
                    "imagesrcset": ["*"],
                    "importance": ["*"],
                    "impressiondata": ["*"],
                    "impressionexpiry": ["*"],
                    "incremental": ["*"],
                    "inert": ["*"],
                    "interestfor": ["*"],
                    "inputmode": ["*"],
                    "integrity": ["*"],
                    "invisible": ["*"],
                    "is": ["*"],
                    "ismap": ["*"],
                    "keytype": ["*"],
                    "kind": ["*"],
                    "label": ["*"],
                    "lang": ["*"],
                    "language": ["*"],
                    "latencyhint": ["*"],
                    "leftmargin": ["*"],
                    "link": ["*"],
                    "list": ["*"],
                    "loading": ["*"],
                    "longdesc": ["*"],
                    "loop": ["*"],
                    "low": ["*"],
                    "lowsrc": ["*"],
                    "manifest": ["*"],
                    "marginheight": ["*"],
                    "marginwidth": ["*"],
                    "max": ["*"],
                    "maxlength": ["*"],
                    "mayscript": ["*"],
                    "media": ["*"],
                    "method": ["*"],
                    "min": ["*"],
                    "minlength": ["*"],
                    "multiple": ["*"],
                    "muted": ["*"],
                    "name": ["*"],
                    "nohref": ["*"],
                    "nomodule": ["*"],
                    "nonce": ["*"],
                    "noresize": ["*"],
                    "noshade": ["*"],
                    "novalidate": ["*"],
                    "nowrap": ["*"],
                    "object": ["*"],
                    "open": ["*"],
                    "optimum": ["*"],
                    "part": ["*"],
                    "pattern": ["*"],
                    "ping": ["*"],
                    "placeholder": ["*"],
                    "playsinline": ["*"],
                    "policy": ["*"],
                    "popover": ["*"],
                    "popovertarget": ["*"],
                    "popovertargetaction": ["*"],
                    "poster": ["*"],
                    "preload": ["*"],
                    "pseudo": ["*"],
                    "readonly": ["*"],
                    "referrerpolicy": ["*"],
                    "rel": ["*"],
                    "reportingorigin": ["*"],
                    "required": ["*"],
                    "resources": ["*"],
                    "rev": ["*"],
                    "reversed": ["*"],
                    "role": ["*"],
                    "rows": ["*"],
                    "rowspan": ["*"],
                    "rules": ["*"],
                    "sandbox": ["*"],
                    "scheme": ["*"],
                    "scope": ["*"],
                    "scopes": ["*"],
                    "scrollamount": ["*"],
                    "scrolldelay": ["*"],
                    "scrolling": ["*"],
                    "select": ["*"],
                    "selected": ["*"],
                    "shadowroot": ["*"],
                    "shadowrootclonable": ["*"],
                    "shadowrootcustomelementregistry": ["*"],
                    "shadowrootdelegatesfocus": ["*"],
                    "shadowrootmode": ["*"],
                    "shadowrootserializable": ["*"],
                    "shadowrootslotassignment": ["*"],
                    "shape": ["*"],
                    "size": ["*"],
                    "sizes": ["*"],
                    "slot": ["*"],
                    "span": ["*"],
                    "spellcheck": ["*"],
                    "src": ["*"],
                    "srcdoc": ["*"],
                    "srclang": ["*"],
                    "srcset": ["*"],
                    "standby": ["*"],
                    "start": ["*"],
                    "step": ["*"],
                    "style": ["*"],
                    "summary": ["*"],
                    "tabindex": ["*"],
                    "target": ["*"],
                    "text": ["*"],
                    "title": ["*"],
                    "topmargin": ["*"],
                    "translate": ["*"],
                    "truespeed": ["*"],
                    "trusttoken": ["*"],
                    "type": ["*"],
                    "usemap": ["*"],
                    "valign": ["*"],
                    "value": ["*"],
                    "valuetype": ["*"],
                    "version": ["*"],
                    "virtualkeyboardpolicy": ["*"],
                    "vlink": ["*"],
                    "vspace": ["*"],
                    "webkitdirectory": ["*"],
                    "width": ["*"],
                    "writingsuggestions": ["*"],
                    "wrap": ["*"],
                },
            }
        )

        self.config = None
        if isinstance(rules, dict):
            self.rules = rules
            # create a new configuration which is a copy of the default but change it based on the rules object
            import copy

            self.config = copy.deepcopy(self._default_configuration)
            for key, value in self.rules.items():
                # print('ADDING RULES', key, value)
                self.config[key] = value
        else:
            self.rules = None
            self.config = self._default_configuration

    def getDefaultConfiguration(self):
        return self._default_configuration

    def getConfiguration(self):
        """[return the configuration object]

        Returns:
            [Object]: [an Object with the users configuration]
        """
        return self.config

    def sanitize(self, frag):
        """Returns a sanitized DocumentFragment from an input, removing any offending elements or attributes."""
        if isinstance(frag, str):
            # parse to html then remove all the bad stuff?? - is a really bad idea. as it goes through eval.
            from domonic import domonic

            frag = domonic.load(frag)

        isDomNode = False
        if isinstance(frag, Document):
            isDomNode = True

        if not isDomNode:
            newfrag = Document.createDocumentFragment()
            if isinstance(frag, (tuple, list)):
                for f in frag:
                    newfrag.appendChild(f)
            else:
                newfrag.appendChild(frag)
            frag = newfrag

        # TODO "allowCustomElements": # "allowElements": [], # "blockElements": [], # "dropElements": [],  # "allowAttributes": [],
        # TODO "dropAttributes": # "allowCustomElements": # "allowComments": # "allowElements" # allowAttributes

        for t in self.config["dropElements"]:
            el = frag.getElementsByTagName(t)
            el.parentNode.removeChild(el)

        for t in self.config["dropAttributes"]:
            for e in self.config["allowElements"]:
                els = frag.getElementsByTagName(e)
                if els != False and len(els) > 0:
                    for el in els:
                        for each in el.attributes:
                            if each.name == t:
                                el.removeAttribute(each.name)

        # print("test" frag.querySelectorAll('span'))
        # print("test2", frag.getElementsByTagName('span'))

        for e in self.config["allowElements"]:
            els = frag.getElementsByTagName(e)
            if els != False and len(els) > 0:
                for el in els:
                    # print(el, el.kwargs, el.attributes, el.__attributes__, type(el.attributes))
                    for each in el.attributes:
                        # print(each)
                        key = each.name
                        val = each.value
                        # print(key, val)
                        allowed_on = self.config["allowAttributes"].get(key)
                        # print("ALLOWED ON:", key, allowed_on)
                        if allowed_on == None:
                            el.removeAttribute(key)
                            continue
                        if "*" in allowed_on:
                            continue
                        if e not in allowed_on:
                            el.removeAttribute(key)
                        # else:
                        #     print(key + ' is allowed')

        for t in self.config["blockElements"]:
            el = frag.getElementsByTagName(str(t))
            # keep the children of the element and add them back to the parent
            for c in el.childNodes:
                frag.parentNode.appendChild(c)
            # remove the element
            frag.parentNode.removeChild(el)

        # print(type(frag))
        return frag

    def sanitizeToString(self, frag) -> str:
        """Returns a sanitized String from an input, removing any offending elements or attributes."""
        return str(self.sanitize(frag))


def _resolve_id_reference(element: "Element", attribute: str) -> "Element | None":
    target_id = element.getAttribute(attribute)
    if not target_id:
        return None
    doc = element.ownerDocument
    return doc.getElementById(target_id) if doc is not None else None


def _set_id_reference(element: "Element", attribute: str, target: Any) -> None:
    if target is None:
        element.removeAttribute(attribute)
        return
    if isinstance(target, Element):
        target_id = target.getAttribute("id")
        if target_id is None:
            raise ValueError(f"{attribute} target element must have an id")
        element.setAttribute(attribute, target_id)
        return
    element.setAttribute(attribute, target)


def _set_attributes(element: "Element", attributes: dict[str, Any]) -> None:
    for name, value in attributes.items():
        if value is not None:
            element.setAttribute(name, value)


class HTMLElement(Element):
    name = ""

    @property
    def popover(self) -> str | None:
        return self.getAttribute("popover")

    @popover.setter
    def popover(self, value: Any) -> None:
        if value is None or value is False:
            self.removeAttribute("popover")
            return
        if value is True:
            value = "auto"
        self.setAttribute("popover", value)

    def _set_popover_open(self, is_open: bool):
        from domonic.events import ToggleEvent

        old_state = "open" if self.hasAttribute("open") else "closed"
        new_state = "open" if is_open else "closed"
        if old_state == new_state:
            return self
        before_toggle = ToggleEvent(
            ToggleEvent.BEFORETOGGLE,
            {"bubbles": False, "cancelable": True, "oldState": old_state, "newState": new_state},
        )
        if not self.dispatchEvent(before_toggle):
            return self
        if is_open:
            self.setAttribute("open", True)
        else:
            self.removeAttribute("open")
        self.dispatchEvent(
            ToggleEvent(
                ToggleEvent.TOGGLE,
                {"bubbles": False, "cancelable": False, "oldState": old_state, "newState": new_state},
            )
        )
        return self

    def showPopover(self):
        return self._set_popover_open(True)

    def hidePopover(self):
        return self._set_popover_open(False)

    def togglePopover(self, force: bool | None = None):
        if force is None:
            force = not self.hasAttribute("open")
        return self._set_popover_open(bool(force))


class HTMLAnchorElement(HTMLElement):
    name = "a"

    def __init__(
        self,
        *args,
        href=None,
        target=None,
        rel=None,
        download=None,
        hreflang=None,
        ping=None,
        referrerpolicy=None,
        type=None,
        **kwargs,
    ):
        """HTMLAnchorElement

        Args:
            href (str, optional): Specifies the URL of the page the link goes to.
            target (str, optional): Specifies where to open the linked document (e.g., "_self", "_blank").
            rel (str, optional): Specifies the relationship between the current document and the linked document (e.g., "noopener", "noreferrer").
            download (str, optional): Specifies that the target will be downloaded when clicked, instead of navigating to it.
            type (str, optional): Specifies the MIME type of the linked resource.
        """
        super().__init__(*args, **kwargs)
        _set_attributes(
            self,
            {
                "href": href,
                "target": target,
                "rel": rel,
                "download": download,
                "hreflang": hreflang,
                "ping": ping,
                "referrerpolicy": referrerpolicy,
                "type": type,
            },
        )

    @property
    def interestForElement(self) -> Element | None:
        return _resolve_id_reference(self, "interestfor")

    @interestForElement.setter
    def interestForElement(self, target: Any) -> None:
        _set_id_reference(self, "interestfor", target)


class HTMLAreaElement(HTMLElement):
    name = "area"

    def __init__(
        self,
        *args,
        href=None,
        target=None,
        alt=None,
        coords=None,
        download=None,
        ping=None,
        rel=None,
        referrerpolicy=None,
        shape=None,
        **kwargs,
    ):
        """HTMLAreaElement

        Args:
            href (str, optional): Specifies the URL of the page the area links to.
            target (str, optional): Specifies where to open the linked document (e.g., "_self", "_blank").
            alt (str, optional): Specifies alternative text for the area.
            coords (str, optional): Specifies the coordinates of the area in the image map (e.g., "x1,y1,x2,y2").
            shape (str, optional): Specifies the shape of the clickable area (e.g., "rect", "circle", "poly").
        """
        super().__init__(*args, **kwargs)
        _set_attributes(
            self,
            {
                "href": href,
                "target": target,
                "alt": alt,
                "coords": coords,
                "download": download,
                "ping": ping,
                "rel": rel,
                "referrerpolicy": referrerpolicy,
                "shape": shape,
            },
        )

    @property
    def interestForElement(self) -> Element | None:
        return _resolve_id_reference(self, "interestfor")

    @interestForElement.setter
    def interestForElement(self, target: Any) -> None:
        _set_id_reference(self, "interestfor", target)


class HTMLAudioElement(HTMLElement):
    name = "audio"

    def __init__(
        self,
        *args,
        autoplay: bool = None,
        controls=None,
        crossorigin=None,
        loading=None,
        loop=None,
        muted=None,
        preload=None,
        src=None,
        **kwargs,
    ):
        """HTMLAudioElement

        Args:
            autoplay (bool, optional): if specified, the audio will automatically begin playback as soon as it can do so, without waiting for the entire audio file to finish downloading
            controls (_type_, optional): _description_. Defaults to None.
            loop (_type_, optional): _description_. Defaults to None.
            muted (_type_, optional): _description_. Defaults to None.
            preload (_type_, optional): _description_. Defaults to None.
            src (_type_, optional): _description_. Defaults to None.
        """
        super().__init__(*args, **kwargs)
        _set_attributes(
            self,
            {
                "autoplay": autoplay,
                "controls": controls,
                "crossorigin": crossorigin,
                "loading": loading,
                "loop": loop,
                "muted": muted,
                "preload": preload,
                "src": src,
            },
        )


class HTMLBRElement(HTMLElement):
    name = "br"
    __isempty = True

    def __str__(self):
        if DOMConfig.RENDER_OPTIONAL_CLOSING_SLASH:
            if DOMConfig.SPACE_BEFORE_OPTIONAL_CLOSING_SLASH:
                return f"<{self.name}{self.__attributes__} />"
            else:
                return f"<{self.name}{self.__attributes__}/>"
        return f"<{self.name}{self.__attributes__} >"


class HTMLBaseElement(HTMLElement):
    name = "base"

    def __init__(self, *args, href=None, target=None, **kwargs):
        """HTMLBaseElement

        Args:
            href (str, optional): The base URL to be used throughout the document for relative URLs. Absolute and relative URLs are allowed.
            target (str, optional): A keyword or author-defined name of the default browsing context...
        """
        super().__init__(*args, **kwargs)
        if href is not None:
            self.setAttribute("href", href)
        if target is not None:
            self.setAttribute("target", target)


class HTMLBaseFontElement(HTMLElement):
    name = "basefont"

    def __init__(self, *args, color=None, face=None, size=None, **kwargs):
        super().__init__(*args, **kwargs)
        if color is not None:
            self.setAttribute("color", color)
        if face is not None:
            self.setAttribute("face", face)
        if size is not None:
            self.setAttribute("size", size)


class HTMLBodyElement(HTMLElement):
    name = "body"

    def __init__(
        self,
        *args,
        aLink=None,
        background=None,
        bgColor=None,
        link=None,
        onload=None,
        onunload=None,
        text=None,
        vLink=None,
        **kwargs,
    ):
        """HTMLBodyElement

        Appears docs are telling you not to use many of the props you can pass and to use css instead.

        Args:
            aLink (str, optional): Color of text for hyperlinks when selected. Do not use this attribute! Use the CSS color property in conjunction with the :active pseudo-class instead.
            background (str, optional): URI of a image to use as a background. Do not use this attribute! Use the CSS background property on the element instead.
            bgColor (str, optional): Background color for the document. Do not use this attribute! Use the CSS background-color property on the element instead.
            bgProperties (str, optional): The size of the text.
            link (str, optional): Color of text for unvisited hypertext links. Do not use this attribute! Use the CSS color property in conjunction with the :link pseudo-class instead.
            onload (str, optional): Function to call when the document is going away.
            onunload (str, optional): Function to call when the document has finished loading.
            text (str, optional): Foreground color of text. Do not use this attribute! Use CSS color property on the element instead.
            vLink (str, optional): Color of text for visited hypertext links. Do not use this attribute! Use the CSS color property in conjunction with the :visited pseudo-class instead.
        """
        super().__init__(*args, **kwargs)
        if aLink is not None:
            self.setAttribute("aLink", aLink)
        if background is not None:
            self.setAttribute("background", background)
        if bgColor is not None:
            self.setAttribute("bgColor", bgColor)
        if link is not None:
            self.setAttribute("link", link)
        if onload is not None:
            self.setAttribute("onload", onload)
        if onunload is not None:
            self.setAttribute("onunload", onunload)
        if text is not None:
            self.setAttribute("text", text)
        if vLink is not None:
            self.setAttribute("vLink", vLink)


class HTMLButtonElement(HTMLElement):
    name = "button"

    # autofocus?
    def __init__(
        self,
        *args,
        command=None,
        commandfor=None,
        disabled: bool = None,
        form=None,
        formaction: str = None,
        formenctype=None,
        formmethod=None,
        formnovalidate=None,
        formtarget=None,
        name=None,
        popovertarget=None,
        popovertargetaction=None,
        type=None,
        value=None,
        **kwargs,
    ):
        """HTMLButtonElement

        Args:
            disabled (bool, optional): prevents the user from interacting with the button: it cannot be pressed or focused.
            form (_type_, optional): The <form> element to associate the button with (its form owner). The value of this attribute must be the id of a <form> in the same document.
            formaction (str, optional): The URL that processes the information submitted by the button. Overrides the action attribute of the button's form owner. Does nothing if there is no form owner.
            formenctype (_type_, optional): _description_. Defaults to None.
            formmethod (_type_, optional): _description_. Defaults to None.
            formnovalidate (_type_, optional): _description_. Defaults to None.
            formtarget (_type_, optional): _description_. Defaults to None.
            name (_type_, optional): _description_. Defaults to None.
            type (_type_, optional): _description_. Defaults to None.
            value (_type_, optional): _description_. Defaults to None.
        """
        super().__init__(*args, **kwargs)
        if command is not None:
            self.setAttribute("command", command)
        if commandfor is not None:
            self.setAttribute("commandfor", commandfor)
        if disabled is not None:
            self.setAttribute("disabled", disabled)
        if form is not None:
            self.setAttribute("form", form)
        if formaction is not None:
            self.setAttribute("formaction", formaction)
        if formenctype is not None:
            self.setAttribute("formenctype", formenctype)
        if formmethod is not None:
            self.setAttribute("formmethod", formmethod)
        if formnovalidate is not None:
            self.setAttribute("formnovalidate", formnovalidate)
        if formtarget is not None:
            self.setAttribute("formtarget", formtarget)
        if name is not None:
            self.setAttribute("name", name)
        if popovertarget is not None:
            self.setAttribute("popovertarget", popovertarget)
        if popovertargetaction is not None:
            self.setAttribute("popovertargetaction", popovertargetaction)
        if type is not None:
            self.setAttribute("type", type)
        if value is not None:
            self.setAttribute("value", value)

    @property
    def popoverTargetElement(self) -> Element | None:
        return _resolve_id_reference(self, "popovertarget")

    @popoverTargetElement.setter
    def popoverTargetElement(self, target: Any) -> None:
        _set_id_reference(self, "popovertarget", target)

    @property
    def popoverTargetAction(self) -> str | None:
        return self.getAttribute("popovertargetaction")

    @popoverTargetAction.setter
    def popoverTargetAction(self, action: Any) -> None:
        if action is None:
            self.removeAttribute("popovertargetaction")
        else:
            self.setAttribute("popovertargetaction", action)

    @property
    def interestForElement(self) -> Element | None:
        return _resolve_id_reference(self, "interestfor")

    @interestForElement.setter
    def interestForElement(self, target: Any) -> None:
        _set_id_reference(self, "interestfor", target)

    @property
    def value(self) -> str:
        attr_value = self.getAttribute("value")
        return "" if attr_value is None else str(attr_value)

    @value.setter
    def value(self, new_value: Any) -> None:
        self.setAttribute("value", new_value)

    def click(self):
        result = super().click()
        if self.hasAttribute("disabled"):
            return result
        button_type = (self.getAttribute("type") or "submit").lower()
        form = _form_owner(self)
        if form is None:
            return result
        if button_type == "submit":
            form.requestSubmit(self)
        elif button_type == "reset":
            form.reset()
        return result


class HTMLCanvasElement(HTMLElement):
    name = "canvas"

    def __init__(self, *args, width: int = None, height: int = None, **kwargs):
        """HTMLCanvasElement

        Args:
            width (int, optional): The height of the coordinate space in CSS pixels. Defaults to 150.
            height (int, optional): The width of the coordinate space in CSS pixels. Defaults to 300.
        """
        super().__init__(*args, **kwargs)
        if width is not None:
            self.setAttribute("width", width)
        if height is not None:
            self.setAttribute("height", height)


class HTMLContentElement(HTMLElement):
    name = "content"

    def __init__(self, *args, select=None, **kwargs):
        super().__init__(*args, **kwargs)
        if select is not None:
            self.setAttribute("select", select)


class HTMLDListElement(HTMLElement):
    name = "dl"


class HTMLDataElement(HTMLElement):
    name = "data"
    
    def __init__(self, *args, value=None, **kwargs):
        """HTMLDataElement

        Args:
            value (str, optional): Contains the machine-readable value associated with the content.
        """
        super().__init__(*args, **kwargs)
        if value is not None:
            self.setAttribute("value", value)


class HTMLDataListElement(HTMLElement):
    name = "datalist"


class HTMLDialogElement(HTMLElement):
    name = "dialog"

    def __init__(self, *args, open=None, closedby=None, **kwargs):
        """HTMLDialogElement

        Args:
            open (bool, optional): Whether the dialog is open or closed.
        """
        super().__init__(*args, **kwargs)
        if open is not None:
            self.setAttribute("open", open)
        if closedby is not None:
            self.setAttribute("closedby", closedby)

    @property
    def open(self) -> bool:
        return self.hasAttribute("open")

    @open.setter
    def open(self, is_open: bool) -> None:
        previous = self.open
        if is_open:
            self.setAttribute("open", True)
        else:
            self.removeAttribute("open")
        if previous != self.open:
            self.dispatchEvent(Event("toggle", {"bubbles": False, "cancelable": False}))

    def show(self):
        self.open = True
        return self

    def showModal(self):
        self.open = True
        return self

    def close(self, returnValue: Any = ""):
        from domonic.events import CloseEvent

        self.returnValue = returnValue
        self.open = False
        self.dispatchEvent(CloseEvent("close", {"bubbles": False, "cancelable": False, "code": 0, "reason": str(returnValue), "wasClean": True}))
        return self


class HTMLDivElement(HTMLElement):
    name = "div"


class XMLDocument(Document):
    name = "xml"
    contentType: str = "application/xml"


class HTMLDocument(Document):
    name = "html"
    contentType: str = "text/html"


class HTMLEmbedElement(HTMLElement):
    name = "embed"


class HTMLFieldSetElement(HTMLElement):
    name = "fieldset"

    def __init__(self, *args, disabled=None, form=None, name=None, **kwargs):
        super().__init__(*args, **kwargs)
        if disabled is not None:
            self.setAttribute("disabled", disabled)
        if form is not None:
            self.setAttribute("form", form)
        if name is not None:
            self.setAttribute("name", name)


class HTMLFormControlsCollection(HTMLCollection):
    """Live collection of a form's listed controls."""

    CONTROL_TYPES: ClassVar[tuple[type[HTMLElement], ...]] = ()

    def __init__(self, form: "HTMLFormElement"):
        super().__init__()
        self._form = form

    def _controls(self) -> list[HTMLElement]:
        controls: list[HTMLElement] = []

        def walk(node):
            if not isinstance(node, Element):
                return
            if node is not self._form and isinstance(node, self.CONTROL_TYPES):
                controls.append(node)
            for child in getattr(node, "childNodes", []):
                walk(child)

        walk(self._form)
        return controls

    @property
    def length(self) -> int:
        return len(self._controls())

    def __len__(self) -> int:
        return self.length

    def __iter__(self):
        return iter(self._controls())

    def __getitem__(self, index: int | str):
        controls = self._controls()
        if isinstance(index, str):
            return self.namedItem(index)
        return controls[index]

    def item(self, index: int) -> HTMLElement | None:
        controls = self._controls()
        return controls[index] if 0 <= index < len(controls) else None

    def namedItem(self, name: str) -> HTMLElement | RadioNodeList | None:
        matches = [
            control
            for control in self._controls()
            if control.getAttribute("id") == name or control.getAttribute("name") == name
        ]
        if not matches:
            return None
        if len(matches) > 1:
            return RadioNodeList(matches, name=name, owner=self)
        return matches[0]


class HTMLFormElement(HTMLElement):
    name = "form"

    # accept-charset??
    def __init__(
        self,
        *args,
        action: str = None,
        accept_charset: str = None,
        autocomplete=None,
        enctype: str = None,
        method: str = None,
        name: str = None,
        novalidate: bool = None,
        rel: str = None,
        target=None,
        **kwargs,
    ):
        """HTMLFormElement

        Args:
            action (str, optional): The URL that processes the form submission.
            accept_charset (str, optional): Character encoding to use for form submission.
            autocomplete (str, optional): off/on.
            enctype (str, optional): If the value of the method attribute is post, enctype is the MIME type of the form submission
            method (str, optional): The HTTP method to submit the form with. GET and POST
            name (str, optional): _description_. Defaults to None.
            novalidate (bool, optional): _description_. Defaults to None.
            rel (str, optional): Relationship between the target resource and the current document.
            target (str, optional): _description_. Defaults to None.
        """
        super().__init__(*args, **kwargs)
        if action is not None:
            self.setAttribute("action", action)
        if accept_charset is not None:
            self.setAttribute("accept-charset", accept_charset)
        if autocomplete is not None:
            self.setAttribute("autocomplete", autocomplete)
        if enctype is not None:
            self.setAttribute("enctype", enctype)
        if method is not None:
            self.setAttribute("method", method)
        if name is not None:
            self.setAttribute("name", name)
        if novalidate is not None:
            self.setAttribute("novalidate", novalidate)
        if rel is not None:
            self.setAttribute("rel", rel)
        if target is not None:
            self.setAttribute("target", target)

    def submit(self):
        return self.requestSubmit(None)

    def checkValidity(self) -> bool:
        from domonic.events import Event

        valid = True
        for control in self.elements:
            if not _is_control_valid(control):
                valid = False
                control.dispatchEvent(Event("invalid", {"bubbles": False, "cancelable": True}))
        return valid

    def requestSubmit(self, submitter=None):
        from domonic.events import SubmitEvent

        should_validate = not self.hasAttribute("novalidate")
        if submitter is not None and submitter.hasAttribute("formnovalidate"):
            should_validate = False
        if should_validate and not self.checkValidity():
            return False
        return self.dispatchEvent(SubmitEvent("submit", {"bubbles": True, "cancelable": True, "submitter": submitter}))

    def reset(self):
        from domonic.events import Event

        for control in self.elements:
            if isinstance(control, HTMLInputElement):
                control.value = control.defaultValue
                control.checked = control.defaultChecked
            elif isinstance(control, HTMLTextAreaElement):
                control.value = control.defaultValue
            elif isinstance(control, HTMLSelectElement):
                for option in control.options:
                    option.selected = option.defaultSelected
        return self.dispatchEvent(Event("reset", {"bubbles": True, "cancelable": True}))

    def reportValidity(self) -> bool:
        return self.checkValidity()

    @property
    def elements(self) -> HTMLFormControlsCollection:
        return HTMLFormControlsCollection(self)


class HTMLFrameSetElement(HTMLElement):
    name = "frameset"

    def __init__(self, *args, cols=None, rows=None, **kwargs):
        super().__init__(*args, **kwargs)
        if cols is not None:
            self.setAttribute("cols", cols)
        if rows is not None:
            self.setAttribute("rows", rows)


class HTMLHRElement(HTMLElement):
    name = "hr"


class HTMLHeadElement(HTMLElement):
    name = "head"


class HTMLHeadingElement(HTMLElement):
    name = "h1"


class HTMLIFrameElement(HTMLElement):
    name = "iframe"

    def __init__(
        self,
        *args,
        allow=None,
        allowfullscreen=None,
        credentialless=None,
        height=None,
        loading=None,
        name=None,
        referrerpolicy=None,
        sandbox=None,
        src=None,
        srcdoc=None,
        width=None,
        **kwargs,
    ):
        """HTMLIFrameElement

        Args:
            src (str, optional): _description_. Defaults to None.
            name (str, optional): _description_. Defaults to None.
            sandbox (str, optional): _description_. Defaults to None.
            allowfullscreen (str, optional): _description_. Defaults to None.
        """
        super().__init__(*args, **kwargs)
        _set_attributes(
            self,
            {
                "allow": allow,
                "allowfullscreen": allowfullscreen,
                "credentialless": credentialless,
                "height": height,
                "loading": loading,
                "name": name,
                "referrerpolicy": referrerpolicy,
                "sandbox": sandbox,
                "src": src,
                "srcdoc": srcdoc,
                "width": width,
            },
        )


class HTMLImageElement(HTMLElement):
    name = "img"
    __isempty = True

    def __init__(
        self,
        *args,
        alt=None,
        controls=None,
        crossorigin=None,
        decoding=None,
        fetchpriority=None,
        height=None,
        ismap=None,
        loading=None,
        longdesc=None,
        referrerpolicy=None,
        sizes=None,
        src=None,
        srcset=None,
        usemap=None,
        width=None,
        **kwargs,
    ):
        """HTMLImageElement

        Args:
            alt (str, optional): _description_. Defaults to None.
            src (str, optional): _description_. Defaults to None.
            crossorigin (str, optional): _description_. Defaults to None.
            height (str, optional): _description_. Defaults to None.
            ismap (str, optional): _description_. Defaults to None.
            longdesc (str, optional): _description_. Defaults to None.
            sizes (str, optional): _description_. Defaults to None.
            srcset (str, optional): _description_. Defaults to None.
            usemap (str, optional): _description_. Defaults to None.
            width (str, optional): _description_. Defaults to None.
        """
        super().__init__(*args, **kwargs)
        _set_attributes(
            self,
            {
                "alt": alt,
                "controls": controls,
                "crossorigin": crossorigin,
                "decoding": decoding,
                "fetchpriority": fetchpriority,
                "height": height,
                "ismap": ismap,
                "loading": loading,
                "longdesc": longdesc,
                "referrerpolicy": referrerpolicy,
                "sizes": sizes,
                "src": src,
                "srcset": srcset,
                "usemap": usemap,
                "width": width,
            },
        )

    def load(self):
        self.dispatchEvent(Event("loadstart", {"bubbles": False, "cancelable": False}))
        self.dispatchEvent(Event("load", {"bubbles": False, "cancelable": False}))
        return self

    def decode(self) -> bool:
        self.dispatchEvent(Event("load", {"bubbles": False, "cancelable": False}))
        return True

    def error(self):
        self.dispatchEvent(Event("error", {"bubbles": False, "cancelable": False}))
        return None

    def abort(self):
        self.dispatchEvent(Event("abort", {"bubbles": False, "cancelable": False}))
        return None


class HTMLInputElement(HTMLElement):
    name = "input"
    __isempty = True

    def __init__(
        self,
        *args,
        accept=None,
        alpha=None,
        alt=None,
        autocomplete=None,
        autofocus=None,
        capture=None,
        checked=None,
        colorspace=None,
        dirname=None,
        disabled=None,
        form=None,
        formaction=None,
        formenctype=None,
        formmethod=None,
        formnovalidate=None,
        formtarget=None,
        height=None,
        _list=None,
        _max=None,
        maxlength=None,
        minlength=None,
        _min=None,
        multiple=None,
        name=None,
        pattern=None,
        placeholder=None,
        popovertarget=None,
        popovertargetaction=None,
        readonly=None,
        required=None,
        size=None,
        src=None,
        step=None,
        type=None,
        value=None,
        width=None,
        **kwargs,
    ):
        """HTMLInputElement

        Args:
            accept (_type_, optional): _description_. Defaults to None.
            alt (_type_, optional): _description_. Defaults to None.
            autocomplete (_type_, optional): _description_. Defaults to None.
            autofocus (_type_, optional): _description_. Defaults to None.
            checked (_type_, optional): _description_. Defaults to None.
            dirname (_type_, optional): _description_. Defaults to None.
            disabled (_type_, optional): _description_. Defaults to None.
            form (_type_, optional): _description_. Defaults to None.
            formaction (_type_, optional): _description_. Defaults to None.
            formenctype (_type_, optional): _description_. Defaults to None.
            formmethod (_type_, optional): _description_. Defaults to None.
            formnovalidate (_type_, optional): _description_. Defaults to None.
            formtarget (_type_, optional): _description_. Defaults to None.
            height (_type_, optional): _description_. Defaults to None.
            _list (_type_, optional): _description_. Defaults to None.
            _max (_type_, optional): _description_. Defaults to None.
            maxlength (_type_, optional): _description_. Defaults to None.
            _min (_type_, optional): _description_. Defaults to None.
            multiple (_type_, optional): _description_. Defaults to None.
            name (_type_, optional): _description_. Defaults to None.
            pattern (_type_, optional): _description_. Defaults to None.
            placeholder (_type_, optional): _description_. Defaults to None.
            readonly (_type_, optional): _description_. Defaults to None.
            required (_type_, optional): _description_. Defaults to None.
            size (_type_, optional): _description_. Defaults to None.
            src (_type_, optional): _description_. Defaults to None.
            step (_type_, optional): _description_. Defaults to None.
            type (_type_, optional): _description_. Defaults to None.
            value (_type_, optional): _description_. Defaults to None.
            width (_type_, optional): _description_. Defaults to None.
        """
        super().__init__(*args, **kwargs)
        if accept is not None:
            self.setAttribute("accept", accept)
        if alpha is not None:
            self.setAttribute("alpha", alpha)
        if alt is not None:
            self.setAttribute("alt", alt)
        if autocomplete is not None:
            self.setAttribute("autocomplete", autocomplete)
        if autofocus is not None:
            self.setAttribute("autofocus", autofocus)
        if capture is not None:
            self.setAttribute("capture", capture)
        if checked is not None:
            self.setAttribute("checked", checked)
        if colorspace is not None:
            self.setAttribute("colorspace", colorspace)
        if dirname is not None:
            self.setAttribute("dirname", dirname)
        if disabled is not None:
            self.setAttribute("disabled", disabled)
        if form is not None:
            self.setAttribute("form", form)
        if formaction is not None:
            self.setAttribute("formaction", formaction)
        if formenctype is not None:
            self.setAttribute("formenctype", formenctype)
        if formmethod is not None:
            self.setAttribute("formmethod", formmethod)
        if formnovalidate is not None:
            self.setAttribute("formnovalidate", formnovalidate)
        if formtarget is not None:
            self.setAttribute("formtarget", formtarget)
        if height is not None:
            self.setAttribute("height", height)
        if _list is not None:
            self.setAttribute("list", _list)
        if _max is not None:
            self.setAttribute("max", _max)
        if maxlength is not None:
            self.setAttribute("maxlength", maxlength)
        if minlength is not None:
            self.setAttribute("minlength", minlength)
        if _min is not None:
            self.setAttribute("min", _min)
        if multiple is not None:
            self.setAttribute("multiple", multiple)
        if name is not None:
            self.setAttribute("name", name)
        if pattern is not None:
            self.setAttribute("pattern", pattern)
        if placeholder is not None:
            self.setAttribute("placeholder", placeholder)
        if popovertarget is not None:
            self.setAttribute("popovertarget", popovertarget)
        if popovertargetaction is not None:
            self.setAttribute("popovertargetaction", popovertargetaction)
        if readonly is not None:
            self.setAttribute("readonly", readonly)
        if required is not None:
            self.setAttribute("required", required)
        if size is not None:
            self.setAttribute("size", size)
        if src is not None:
            self.setAttribute("src", src)
        if step is not None:
            self.setAttribute("step", step)
        if type is not None:
            self.setAttribute("type", type)
        if value is not None:
            self.setAttribute("value", value)
        if width is not None:
            self.setAttribute("width", width)
        self._default_value = self.value
        self._default_checked = self.checked

    @property
    def popoverTargetElement(self) -> Element | None:
        return _resolve_id_reference(self, "popovertarget")

    @popoverTargetElement.setter
    def popoverTargetElement(self, target: Any) -> None:
        _set_id_reference(self, "popovertarget", target)

    @property
    def popoverTargetAction(self) -> str | None:
        return self.getAttribute("popovertargetaction")

    @popoverTargetAction.setter
    def popoverTargetAction(self, action: Any) -> None:
        if action is None:
            self.removeAttribute("popovertargetaction")
        else:
            self.setAttribute("popovertargetaction", action)

    @property
    def type(self) -> str:
        return str(self.getAttribute("type") or "text").lower()

    @type.setter
    def type(self, new_type: Any) -> None:
        self.setAttribute("type", new_type)

    @property
    def value(self) -> str:
        attr_value = self.getAttribute("value")
        if attr_value is None:
            return "on" if self.type in {"checkbox", "radio"} else ""
        return str(attr_value)

    @value.setter
    def value(self, new_value: Any) -> None:
        self.setAttribute("value", new_value)

    def setValue(self, new_value: Any, *, dispatch_events: bool = True) -> str:
        self.value = new_value
        if dispatch_events:
            _dispatch_value_change_events(self)
        return self.value

    @property
    def defaultValue(self) -> str:
        return getattr(self, "_default_value", self.value)

    @defaultValue.setter
    def defaultValue(self, new_value: Any) -> None:
        self._default_value = "" if new_value is None else str(new_value)

    @property
    def defaultChecked(self) -> bool:
        return bool(getattr(self, "_default_checked", self.checked))

    @defaultChecked.setter
    def defaultChecked(self, is_checked: bool) -> None:
        self._default_checked = bool(is_checked)

    @property
    def checked(self) -> bool:
        return self.hasAttribute("checked")

    @checked.setter
    def checked(self, is_checked: bool) -> None:
        if is_checked:
            if self.type == "radio":
                for candidate in _radio_group_members(self):
                    if candidate is not self:
                        candidate.checked = False
            self.setAttribute("checked", True)
        else:
            self.removeAttribute("checked")

    def click(self):
        result = super().click()
        if self.hasAttribute("disabled"):
            return result
        input_type = self.type
        if input_type in {"checkbox", "radio"}:
            was_checked = self.checked
            if input_type == "radio":
                if not was_checked:
                    self.checked = True
            else:
                self.checked = not was_checked
            if self.checked != was_checked:
                _dispatch_value_change_events(self)
        elif input_type == "submit":
            form = _form_owner(self)
            if form is not None:
                form.requestSubmit(self)
        elif input_type == "reset":
            form = _form_owner(self)
            if form is not None:
                form.reset()
        return result

    def checkValidity(self) -> bool:
        return _is_control_valid(self)

    def reportValidity(self) -> bool:
        return self.checkValidity()


class HTMLIsIndexElement(HTMLElement):
    name = "isindex"

    def __init__(self, *args, prompt=None, **kwargs):
        super().__init__(*args, **kwargs)
        if prompt is not None:
            self.setAttribute("prompt", prompt)


class HTMLKeygenElement(HTMLElement):
    name = "keygen"
    __isempty = True


class HTMLLIElement(HTMLElement):
    name = "li"


class HTMLLabelElement(HTMLElement):
    name = "label"

    # def __init__(self, *args, _for=None, **kwargs):
    #     """_summary_

    #     Args:
    #         _for (_type_, optional): the id of the element that this label is for. Defaults to None.
    #     """
    # super().__init__(*args, **kwargs)
    # if _for is not None:
    #     self.setAttribute('for', _for)


class HTMLLegendElement(HTMLElement):
    name = "legend"


class HTMLLinkElement(HTMLElement):
    name = "link"

    def __init__(
        self,
        *args,
        as_=None,
        blocking=None,
        color=None,
        crossorigin=None,
        disabled=None,
        fetchpriority=None,
        href=None,
        hreflang=None,
        imagesizes=None,
        imagesrcset=None,
        integrity=None,
        media=None,
        referrerpolicy=None,
        rel=None,
        sizes=None,
        type=None,
        **kwargs,
    ):
        """HTMLLinkElement

        Args:
            rel (str, optional): Specifies the relationship between the current document and the linked resource.
            href (str, optional): The URL of the linked resource.
            type (str, optional): Specifies the type of the linked resource (like 'text/css').
            sizes (str, optional): Defines the sizes of the icons linked.
        """
        super().__init__(*args, **kwargs)
        _set_attributes(
            self,
            {
                "as": as_,
                "blocking": blocking,
                "color": color,
                "crossorigin": crossorigin,
                "disabled": disabled,
                "fetchpriority": fetchpriority,
                "href": href,
                "hreflang": hreflang,
                "imagesizes": imagesizes,
                "imagesrcset": imagesrcset,
                "integrity": integrity,
                "media": media,
                "referrerpolicy": referrerpolicy,
                "rel": rel,
                "sizes": sizes,
                "type": type,
            },
        )


class HTMLMapElement(HTMLElement):
    name = "map"

    def __init__(self, *args, name=None, **kwargs):
        super().__init__(*args, **kwargs)
        if name is not None:
            self.setAttribute("name", name)

class HTMLMediaElement(HTMLElement):
    name = ""

    def __init__(
        self,
        *args,
        src=None,
        crossorigin=None,
        preload=None,
        autoplay=None,
        loop=None,
        muted=None,
        controls=None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        _set_attributes(
            self,
            {
                "src": src,
                "crossorigin": crossorigin,
                "preload": preload,
                "autoplay": autoplay,
                "loop": loop,
                "muted": muted,
                "controls": controls,
            },
        )

    def load(self):
        self.dispatchEvent(Event("loadstart", {"bubbles": False, "cancelable": False}))
        self.dispatchEvent(Event("loadedmetadata", {"bubbles": False, "cancelable": False}))
        self.dispatchEvent(Event("loadeddata", {"bubbles": False, "cancelable": False}))
        return self

    def play(self):
        self.dispatchEvent(Event("play", {"bubbles": False, "cancelable": False}))
        self.dispatchEvent(Event("playing", {"bubbles": False, "cancelable": False}))
        return True

    def pause(self):
        self.dispatchEvent(Event("pause", {"bubbles": False, "cancelable": False}))
        return None


class HTMLMetaElement(HTMLElement):
    name = "meta"
    __isempty = True

    def __init__(self, *args, charset=None, content=None, http_equiv=None, name=None, **kwargs):
        """HTMLMetaElement

        Args:
            charset (_type_, optional): _description_. Defaults to None.
            content (_type_, optional): _description_. Defaults to None.
            http_equiv (_type_, optional): _description_. Defaults to None.
            name (_type_, optional): _description_. Defaults to None.
        """
        super().__init__(*args, **kwargs)
        if charset is not None:
            self.setAttribute("charset", charset)
        if content is not None:
            self.setAttribute("content", content)
        if http_equiv is not None:
            self.setAttribute("http-equiv", http_equiv)
        if name is not None:
            self.setAttribute("name", name)


class HTMLMeterElement(HTMLElement):
    name = "meter"

    def __init__(self, *args, value=None, _min=None, _max=None, low=None, high=None, optimum=None, **kwargs):
        """HTMLMeterElement

        The <meter> HTML element represents either a scalar value within a known range or a fractional value.

        Args:
            value (_type_, optional): The current numeric value. This must be between the minimum and maximum values (min attribute and max attribute) if they are specified.
            min (_type_, optional): The lower numeric bound of the measured range. This must be less than the maximum value (max attribute), if specified. If unspecified, the minimum value is 0.
            max (_type_, optional): The upper numeric bound of the measured range. This must be greater than the minimum value (min attribute), if specified. If unspecified, the maximum value is 1.
            low (_type_, optional): _description_. Defaults to None.
            high (_type_, optional): _description_. Defaults to None.
            optimum (_type_, optional): _description_. Defaults to None.
        """
        super().__init__(*args, **kwargs)
        if value is not None:
            self.setAttribute("value", value)
        if _min is not None:
            self.setAttribute("_min", _min)
        if _max is not None:
            self.setAttribute("_max", _max)
        if low is not None:
            self.setAttribute("low", low)
        if high is not None:
            self.setAttribute("high", high)
        if optimum is not None:
            self.setAttribute("optimum", optimum)


class HTMLModElement(HTMLElement):
    name = "mod"

    def __init__(self, *args, datetime=None, **kwargs):
        """HTMLModElement

        Args:
            datetime (str, optional): The date and time when the modification occurred.
        """
        super().__init__(*args, **kwargs)
        if datetime is not None:
            self.setAttribute("datetime", datetime)


class HTMLOListElement(HTMLElement):
    name = "ol"


class HTMLObjectElement(HTMLElement):
    name = "object"


class HTMLOptGroupElement(HTMLElement):
    name = "optgroup"


class HTMLOptionElement(HTMLElement):
    name = "option"

    def __init__(self, *args, disabled=None, label=None, selected=None, value=None, **kwargs):
        """HTMLOptionElement

        Args:
            disabled (_type_, optional): _description_. Defaults to None.
            label (_type_, optional): _description_. Defaults to None.
            selected (_type_, optional): _description_. Defaults to None.
            value (_type_, optional): _description_. Defaults to None.
        """
        super().__init__(*args, **kwargs)
        if disabled is not None:
            self.setAttribute("disabled", disabled)
        if label is not None:
            self.setAttribute("label", label)
        if selected is not None:
            self.setAttribute("selected", selected)
        if value is not None:
            self.setAttribute("value", value)
        self._default_selected = self.selected

    @property
    def value(self) -> str:
        attr_value = self.getAttribute("value")
        return self.textContent if attr_value is None else str(attr_value)

    @value.setter
    def value(self, new_value: Any) -> None:
        self.setAttribute("value", new_value)

    @property
    def selected(self) -> bool:
        return self.hasAttribute("selected")

    @selected.setter
    def selected(self, is_selected: bool) -> None:
        if is_selected:
            select_owner = self.parentNode
            while select_owner is not None and not isinstance(select_owner, HTMLSelectElement):
                select_owner = getattr(select_owner, "parentNode", None)
            if isinstance(select_owner, HTMLSelectElement) and not select_owner.hasAttribute("multiple"):
                for option in select_owner.options:
                    if option is not self:
                        option.removeAttribute("selected")
            self.setAttribute("selected", True)
        else:
            self.removeAttribute("selected")

    @property
    def defaultSelected(self) -> bool:
        return bool(getattr(self, "_default_selected", self.selected))

    @defaultSelected.setter
    def defaultSelected(self, is_selected: bool) -> None:
        self._default_selected = bool(is_selected)


class HTMLOptionsCollection(HTMLCollection):
    """Live collection of a select element's option descendants."""

    def __init__(self, select: "HTMLSelectElement"):
        super().__init__()
        self._select = select

    def _options(self) -> list[HTMLOptionElement]:
        options: list[HTMLOptionElement] = []

        def walk(node):
            if not isinstance(node, Element):
                return
            if node is not self._select and isinstance(node, HTMLOptionElement):
                options.append(node)
            for child in getattr(node, "childNodes", []):
                walk(child)

        walk(self._select)
        return options

    @property
    def length(self) -> int:
        return len(self._options())

    def __len__(self) -> int:
        return self.length

    def __iter__(self):
        return iter(self._options())

    def __getitem__(self, index: int | str):
        options = self._options()
        if isinstance(index, str):
            return self.namedItem(index)
        return options[index]

    def item(self, index: int) -> HTMLOptionElement | None:
        options = self._options()
        return options[index] if 0 <= index < len(options) else None

    def namedItem(self, name: str) -> HTMLOptionElement | None:
        for option in self._options():
            if option.getAttribute("id") == name or option.getAttribute("name") == name:
                return option
        return None

    def add(self, element: HTMLOptionElement, before: int | Node | None = None) -> None:
        if isinstance(before, int):
            reference = self.item(before)
            if reference is None:
                self._select.appendChild(element)
            else:
                self._select.insertBefore(element, reference)
            return
        if isinstance(before, Node):
            self._select.insertBefore(element, before)
            return
        self._select.appendChild(element)

    def remove(self, index: int) -> None:
        option = self.item(index)
        if option is not None:
            self._select.removeChild(option)


class HTMLOutputElement(HTMLElement):
    name = "output"


class HTMLParagraphElement(HTMLElement):
    name = "p"


class HTMLParamElement(HTMLElement):
    name = "param"
    __isempty = True

    def __init__(self, *args, name=None, value=None, **kwargs):
        """HTMLParamElement

        Args:
            name (str, optional): The name of the parameter.
            value (str, optional): The value of the parameter.
        """
        super().__init__(*args, **kwargs)
        if name is not None:
            self.setAttribute("name", name)
        if value is not None:
            self.setAttribute("value", value)


class HTMLPictureElement(HTMLElement):
    name = "picture"

    def __init__(self, *args, **kwargs):
        """HTMLPictureElement

        A container for `<source>` elements, allowing the browser to choose from multiple images based on media queries.
        """
        super().__init__(*args, **kwargs)


class HTMLPreElement(HTMLElement):
    name = "pre"


class HTMLProgressElement(HTMLElement):
    name = "progress"

    def __init__(self, *args, value=None, max=None, **kwargs):
        """HTMLProgressElement

        Args:
            value (str, optional): The current progress value.
            max (str, optional): The maximum value of the progress.
        """
        super().__init__(*args, **kwargs)
        if value is not None:
            self.setAttribute("value", value)
        if max is not None:
            self.setAttribute("max", max)


class HTMLQuoteElement(HTMLElement):
    name = "q"

    def __init__(self, *args, cite=None, **kwargs):
        """HTMLQuoteElement

        Args:
            cite (str, optional): The source URL for the quotation.
        """
        super().__init__(*args, **kwargs)
        if cite is not None:
            self.setAttribute("cite", cite)


class HTMLScriptElement(HTMLElement):
    name = "script"

    def __init__(
        self,
        *args,
        async_=None,
        blocking=None,
        crossorigin=None,
        defer=None,
        fetchpriority=None,
        integrity=None,
        nomodule=None,
        referrerpolicy=None,
        src=None,
        type=None,
        **kwargs,
    ):
        """HTMLScriptElement"""
        super().__init__(*args, **kwargs)
        _set_attributes(
            self,
            {
                "async": async_,
                "blocking": blocking,
                "crossorigin": crossorigin,
                "defer": defer,
                "fetchpriority": fetchpriority,
                "integrity": integrity,
                "nomodule": nomodule,
                "referrerpolicy": referrerpolicy,
                "src": src,
                "type": type,
            },
        )


class HTMLSelectElement(HTMLElement):
    name = "select"

    def __init__(
        self,
        *args,
        autofocus: bool = None,
        disabled: bool = None,
        multiple: bool = None,
        name: str = None,
        required: bool = None,
        size: int = None,
        **kwargs,
    ):
        """HTMLSelectElement

        Args:
            autofocus (bool, optional): lets you specify that a form control should have input focus when the page loads.
            disabled (bool, optional): toggles if user can interact
            multiple (bool, optional): If multiple options can be selected in the list.
            name (str, optional): This attribute is used to specify the name of the control.
            required (bool, optional): indicating that an option with a non-empty string value must be selected.
            size (int, optional): the number of rows in the list that should be visible at one time.
        """
        super().__init__(*args, **kwargs)
        if autofocus is not None:
            self.setAttribute("autofocus", autofocus)
        if disabled is not None:
            self.setAttribute("disabled", disabled)
        if multiple is not None:
            self.setAttribute("multiple", multiple)
        if name is not None:
            self.setAttribute("name", name)
        if required is not None:
            self.setAttribute("required", required)
        if size is not None:
            self.setAttribute("size", size)

    @property
    def options(self) -> HTMLOptionsCollection:
        return HTMLOptionsCollection(self)

    @property
    def selectedIndex(self) -> int:
        for index, option in enumerate(self.options):
            if option.selected:
                return index
        return -1

    @selectedIndex.setter
    def selectedIndex(self, index: int) -> None:
        for option_index, option in enumerate(self.options):
            option.selected = option_index == index

    @property
    def value(self) -> str:
        index = self.selectedIndex
        option = self.options.item(index)
        return option.value if option is not None else ""

    @value.setter
    def value(self, new_value: Any) -> None:
        string_value = "" if new_value is None else str(new_value)
        matched = False
        for option in self.options:
            is_match = option.value == string_value
            option.selected = is_match
            matched = matched or is_match
        if not matched and not self.hasAttribute("multiple"):
            self.selectedIndex = -1

    @property
    def selectedOptions(self) -> list[HTMLOptionElement]:
        return [option for option in self.options if option.selected]

    def setValue(self, new_value: Any, *, dispatch_events: bool = True) -> str:
        self.value = new_value
        if dispatch_events:
            _dispatch_value_change_events(self)
        return self.value

    def selectIndex(self, index: int, *, dispatch_events: bool = True) -> int:
        self.selectedIndex = index
        if dispatch_events:
            _dispatch_value_change_events(self)
        return self.selectedIndex

    def checkValidity(self) -> bool:
        return _is_control_valid(self)

    def reportValidity(self) -> bool:
        return self.checkValidity()


class HTMLSelectedContentElement(HTMLElement):
    name = "selectedcontent"


class HTMLShadowElement(HTMLElement):
    name = "shadow"
    # Currently, the shadow element is obsolete and not typically used in HTML5. Its use was associated with the deprecated Shadow DOM v0 API.

    def __init__(self, *args, **kwargs):
        """HTMLShadowElement

        The <shadow> element was used in the Shadow DOM v0 specification. It's not commonly used in modern web development.
        """
        super().__init__(*args, **kwargs)


class HTMLSourceElement(HTMLElement):
    name = "source"
    __isempty = True

    def __init__(self, *args, height=None, media=None, sizes=None, src=None, srcset=None, type=None, width=None, **kwargs):
        """HTMLSourceElement

        Args:
            src (str, optional): Specifies the URL of the resource.
            type (str, optional): Specifies the MIME type of the resource.
            media (str, optional): Specifies the media query for when to apply the source.
            sizes (str, optional): Specifies the sizes of the source.
        """
        super().__init__(*args, **kwargs)
        _set_attributes(
            self,
            {
                "height": height,
                "media": media,
                "sizes": sizes,
                "src": src,
                "srcset": srcset,
                "type": type,
                "width": width,
            },
        )


class HTMLSpanElement(HTMLElement):
    name = "span"



class HTMLStyleElement(HTMLElement):
    name = "style"

    def __init__(self, *args, blocking=None, media=None, scoped=None, type=None, **kwargs):
        """HTMLStyleElement

        Args:
            type (str, optional): Specifies the type of style sheet.
            media (str, optional): Specifies the media for which the styles are intended.
            scoped (str, optional): Indicates whether the style is scoped to the element.
        """
        super().__init__(*args, **kwargs)
        _set_attributes(self, {"blocking": blocking, "media": media, "scoped": scoped, "type": type})


class HTMLTableCaptionElement(HTMLElement):
    name = "caption"


class HTMLTableCellElement(HTMLElement):
    name = "td"


class HTMLTableColElement(HTMLElement):
    name = "col"
    __isempty = True


class HTMLTableDataCellElement(HTMLElement):
    name = "td"


class HTMLTableElement(HTMLElement):
    name = "table"

    def __init__(
        self,
        *args,
        align: str = None,
        bgcolor=None,
        border=None,
        cellpadding=None,
        cellspacing=None,
        frame=None,
        rules=None,
        summary=None,
        width=None,
        **kwargs,
    ):
        """HTMLTableElement

        - in most cases it seems docs are advising to use css instead

        Args:
            align (str, optional): This enumerated attribute indicates how the table must be aligned inside the containing document.
            bgcolor (str, optional): The background color of the table. It is a 6-digit hexadecimal RGB code, prefixed by a '#'. One of the predefined color keywords can also be used.
            border (int, optional): The size of the frame surrounding the table. If set to 0, the frame attribute is set to void.
            cellpadding (int, optional): This attribute defines the space between the content of a cell and its border, displayed or not. If the cellpadding's length is defined in pixels, this pixel-sized space will be applied to all four sides of the cell's content. If the length is defined using a percentage value, the content will be centered and the total vertical space (top and bottom) will represent this value.
            cellspacing (int, optional): This attribute defines the size of the space between two cells in a percentage value or pixels. The attribute is applied both horizontally and vertically, to the space between the top of the table and the cells of the first row, the left of the table and the first column, the right of the table and the last column and the bottom of the table and the last row.
            frame (str, optional): This enumerated attribute defines which side of the frame surrounding the table must be displayed.
            rules (str, optional): This enumerated attribute defines where rules, i.e. lines, should appear in a table. It can have the following values
            summary (str, optional): This attribute defines an alternative text that summarizes the content of the table. Use the <caption> element instead.
            width (str, optional): This attribute defines the width of the table. Use the CSS width property instead.
        """
        super().__init__(*args, **kwargs)
        if align is not None:
            self.setAttribute("align", align)
        if bgcolor is not None:
            self.setAttribute("bgcolor", bgcolor)
        if border is not None:
            self.setAttribute("border", border)
        if cellpadding is not None:
            self.setAttribute("cellpadding", cellpadding)
        if cellspacing is not None:
            self.setAttribute("cellspacing", cellspacing)
        if frame is not None:
            self.setAttribute("frame", frame)
        if rules is not None:
            self.setAttribute("rules", rules)
        if summary is not None:
            self.setAttribute("summary", summary)
        if width is not None:
            self.setAttribute("width", width)


class HTMLTableHeaderCellElement(HTMLElement):
    name = "th"


class HTMLTableRowElement(HTMLElement):
    name = "tr"


class HTMLTableSectionElement(HTMLElement):
    name = "tbody"


class HTMLDetailsElement(HTMLElement):
    name = "details"

    def __init__(self, *args, open: bool = None, **kwargs):
        super().__init__(*args, **kwargs)
        if open is not None:
            self.open = open

    @property
    def open(self) -> bool:
        return self.hasAttribute("open")

    @open.setter
    def open(self, is_open: bool) -> None:
        previous = self.open
        if is_open:
            self.setAttribute("open", True)
        else:
            self.removeAttribute("open")
        if previous != self.open:
            self.dispatchEvent(Event("toggle", {"bubbles": False, "cancelable": False}))

    def toggle(self) -> bool:
        self.open = not self.open
        return self.open


class HTMLSummaryElement(HTMLElement):
    name = "summary"


class HTMLSlotElement(HTMLElement):
    name = "slot"

    def assignedNodes(self, options: dict[str, Any] | None = None) -> list[Node]:
        flatten = bool((options or {}).get("flatten"))
        root = getattr(self, "parentNode", None)
        if not isinstance(root, ShadowRoot):
            return []

        slot_name = self.getAttribute("name") or ""
        assigned: list[Node] = []
        for child in getattr(root.host, "childNodes", []):
            if isinstance(child, Element):
                child_slot = child.getAttribute("slot") or ""
                if child_slot == slot_name:
                    assigned.append(child)
            elif slot_name == "":
                assigned.append(child)

        if assigned:
            return assigned

        fallback = [child for child in self.childNodes if isinstance(child, Node)]
        if flatten:
            flattened: list[Node] = []
            for child in fallback:
                if isinstance(child, HTMLSlotElement):
                    flattened.extend(child.assignedNodes(options))
                else:
                    flattened.append(child)
            return flattened
        return fallback

    def assignedElements(self, options: dict[str, Any] | None = None) -> list[Element]:
        return [node for node in self.assignedNodes(options) if isinstance(node, Element)]


class HTMLTemplateElement(HTMLElement):
    name = "template"

    def __init__(
        self,
        *args,
        shadowrootclonable=None,
        shadowrootcustomelementregistry=None,
        shadowrootdelegatesfocus=None,
        shadowrootmode=None,
        shadowrootserializable=None,
        shadowrootslotassignment=None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        _set_attributes(
            self,
            {
                "shadowrootclonable": shadowrootclonable,
                "shadowrootcustomelementregistry": shadowrootcustomelementregistry,
                "shadowrootdelegatesfocus": shadowrootdelegatesfocus,
                "shadowrootmode": shadowrootmode,
                "shadowrootserializable": shadowrootserializable,
                "shadowrootslotassignment": shadowrootslotassignment,
            },
        )

    @property
    def content(self):
        return DocumentFragment(*self.args)

    @content.setter
    def content(self, ignore):
        self.__content = "".join([each.__str__() for each in self.args])


class HTMLTextAreaElement(HTMLElement):
    name = "textarea"

    def __init__(
        self,
        *args,
        autocomplete=None,
        autofocus=None,
        cols=None,
        dirname=None,
        disabled=None,
        form=None,
        maxlength=None,
        minlength=None,
        name=None,
        placeholder=None,
        readonly=None,
        required=None,
        rows=None,
        wrap=None,
        **kwargs,
    ):
        """HTMLTextAreaElement

        Args:
            autofocus (_type_, optional): _description_. Defaults to None.
            cols (_type_, optional): _description_. Defaults to None.
            disabled (_type_, optional): _description_. Defaults to None.
            form (_type_, optional): _description_. Defaults to None.
            maxlength (_type_, optional): _description_. Defaults to None.
            name (_type_, optional): _description_. Defaults to None.
            placeholder (_type_, optional): _description_. Defaults to None.
            readonly (_type_, optional): _description_. Defaults to None.
            required (_type_, optional): _description_. Defaults to None.
            rows (_type_, optional): _description_. Defaults to None.
            wrap (_type_, optional): _description_. Defaults to None.
        """
        super().__init__(*args, **kwargs)
        if autocomplete is not None:
            self.setAttribute("autocomplete", autocomplete)
        if autofocus is not None:
            self.setAttribute("autofocus", autofocus)
        if cols is not None:
            self.setAttribute("cols", cols)
        if dirname is not None:
            self.setAttribute("dirname", dirname)
        if disabled is not None:
            self.setAttribute("disabled", disabled)
        if form is not None:
            self.setAttribute("form", form)
        if maxlength is not None:
            self.setAttribute("maxlength", maxlength)
        if minlength is not None:
            self.setAttribute("minlength", minlength)
        if name is not None:
            self.setAttribute("name", name)
        if placeholder is not None:
            self.setAttribute("placeholder", placeholder)
        if readonly is not None:
            self.setAttribute("readonly", readonly)
        if required is not None:
            self.setAttribute("required", required)
        if rows is not None:
            self.setAttribute("rows", rows)
        if wrap is not None:
            self.setAttribute("wrap", wrap)
        self._default_value = self.value

    @property
    def value(self) -> str:
        return "" if self.textContent is None else self.textContent

    @value.setter
    def value(self, new_value: Any) -> None:
        self.textContent = "" if new_value is None else str(new_value)

    def setValue(self, new_value: Any, *, dispatch_events: bool = True) -> str:
        self.value = new_value
        if dispatch_events:
            _dispatch_value_change_events(self)
        return self.value

    @property
    def defaultValue(self) -> str:
        return getattr(self, "_default_value", self.value)

    @defaultValue.setter
    def defaultValue(self, new_value: Any) -> None:
        self._default_value = "" if new_value is None else str(new_value)

    def checkValidity(self) -> bool:
        return _is_control_valid(self)

    def reportValidity(self) -> bool:
        return self.checkValidity()


HTMLFormControlsCollection.CONTROL_TYPES = (
    HTMLButtonElement,
    HTMLFieldSetElement,
    HTMLInputElement,
    HTMLObjectElement,
    HTMLOutputElement,
    HTMLSelectElement,
    HTMLTextAreaElement,
)


class HTMLTimeElement(HTMLElement):
    name = "time"

    def __init__(self, *args, datetime=None, **kwargs):
        """HTMLTimeElement

        Args:
            datetime (str, optional): Represents the time value in a machine-readable format.
        """
        super().__init__(*args, **kwargs)
        if datetime is not None:
            self.setAttribute("datetime", datetime)


class HTMLTitleElement(HTMLElement):
    name = "title"


class HTMLTrackElement(HTMLElement):
    name = "track"
    
    def __init__(self, *args, kind=None, label=None, src=None, srclang=None, default=None, **kwargs):
        """HTMLTrackElement

        Args:
            kind (str, optional): Specifies the kind of text track. Can be "subtitles", "captions", "descriptions", or "chapters".
            label (str, optional): A user-readable title for the track.
            src (str, optional): The URL of the track file.
            srclang (str, optional): The language of the track text.
            default (bool, optional): Indicates if the track should be shown by default.
        """
        super().__init__(*args, **kwargs)
        if kind is not None:
            self.setAttribute("kind", kind)
        if label is not None:
            self.setAttribute("label", label)
        if src is not None:
            self.setAttribute("src", src)
        if srclang is not None:
            self.setAttribute("srclang", srclang)
        if default is not None:
            self.setAttribute("default", default)


class HTMLUListElement(HTMLElement):
    name = "ul"


class HTMLUnknownElement(HTMLElement):
    name = "unknown"


class HTMLVideoElement(HTMLElement):
    name = "video"

    def __init__(
        self,
        *args,
        autoplay=None,
        controls=None,
        controlslist=None,
        crossorigin=None,
        disablepictureinpicture=None,
        height=None,
        loop=None,
        muted=None,
        playsinline=None,
        poster=None,
        preload=None,
        src=None,
        width=None,
        **kwargs,
    ):
        """HTMLVideoElement

        Args:
            autoplay (_type_, optional): _description_. Defaults to None.
            controls (_type_, optional): _description_. Defaults to None.
            height (_type_, optional): _description_. Defaults to None.
            loop (_type_, optional): _description_. Defaults to None.
            muted (_type_, optional): _description_. Defaults to None.
            poster (_type_, optional): _description_. Defaults to None.
            preload (_type_, optional): _description_. Defaults to None.
            src (_type_, optional): _description_. Defaults to None.
            width (_type_, optional): _description_. Defaults to None.
        """
        super().__init__(*args, **kwargs)
        _set_attributes(
            self,
            {
                "autoplay": autoplay,
                "controls": controls,
                "controlslist": controlslist,
                "crossorigin": crossorigin,
                "disablepictureinpicture": disablepictureinpicture,
                "height": height,
                "loop": loop,
                "muted": muted,
                "playsinline": playsinline,
                "poster": poster,
                "preload": preload,
                "src": src,
                "width": width,
            },
        )


class HTMLPortalElement(HTMLElement):
    name = "portal"


# document can be set manually but will get set each time a new Document is created.
global document
document = Document()
console = Console  # legacy. should access via window

# Considered obsolete dom classes ----
# DOMConfiguration - we now use a variation of this name DOMConfig for render settings
# DOMErrorHandler
# DOMImplementationList
# DOMImplementationRegistry
# DOMImplementationSource
# DOMLocator
# DOMObject
# DOMSettableTokenList
# DOMUserData
# ElementTraversal
# Entity
# EntityReference
# NameList
# Notation
# TypeInfo
# UserDataHandler


"""
# self.screen = type('screen', (DOM,), {'name':'screen'})
"""


# https://developer.mozilla.org/en-US/docs/Glossary/Empty_element
# def is_empty(node):
# if its a class,
# if its an instance
# if its a string

# meta = HTMLMetaElement
# br = HTMLBRElement
# img = HTMLImageElement
# input = HTMLInputElement
# param = HTMLParamElement
# source = HTMLSourceElement
# track = HTMLTrackElement
# col = HTMLTableColElement
# keygen = HTMLKeygenElement

# hr = type("hr", (closed_tag, Element), {"name": "hr"})
# wbr = type("wbr", (closed_tag, Element), {"name": "wbr"})
# command = type("command", (closed_tag, Element), {"name": "command"})
