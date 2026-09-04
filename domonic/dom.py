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
import math
import os
import re
import time
import warnings
from collections.abc import Iterable as IterableABC
from email.utils import formatdate
from html import escape as _stdlib_escape_html


def _escape_html(value: str, quote: bool = True) -> str:
    """``html.escape`` with a fast path for text that contains nothing to
    escape (the common case when serialising a parsed document)."""
    if "&" not in value and "<" not in value and ">" not in value:
        if not quote or ('"' not in value and "'" not in value):
            return value
    return _stdlib_escape_html(value, quote)
from typing import Any, Callable, ClassVar, Iterable, Iterator

from domonic import _fontmetrics
from domonic.events import EVENT_HANDLER_NAMES, Event, EventTarget, MouseEvent
from domonic.javascript import undefined
from domonic.geom.vec3 import vec3
from domonic.style import CSSStyleDeclaration as Style
from domonic.style import StyleSheetList
from domonic.webapi.console import Console
from domonic.webapi.url import URL
from domonic.webapi.xpath import (
    XPathEvaluator,
    XPathException,
    XPathExpression,
    XPathResult,
)

# from xml.dom.pulldom import END_ELEMENT


class DOMConfig:
    """Global rendering and behaviour flags for domonic's DOM.

    ``DOMConfig`` controls how trees are rendered and how a few optional
    behaviours are interpreted across the library, such as auto-escaping text
    content and optional closing-tag handling.
    """

    GLOBAL_AUTOESCAPE: bool = False  # Default is False
    RENDER_OPTIONAL_CLOSING_TAGS: bool = True  # Default is True
    RENDER_OPTIONAL_CLOSING_SLASH: bool = (
        True  # on emtpy nodes should the last slash be rendered
    )
    SPACE_BEFORE_OPTIONAL_CLOSING_SLASH: bool = (
        False  # on emtpy nodes should there be a space before the closing slash?
    )
    HTMX_ENABLED: bool = False  # Default is false
    ALPINE_ENABLED: bool = False  # Default is false - opt-in Alpine.js x_* sugar
    # NO_REPR: bool = True  # objects always render?
    ATTRIBUTE_QUOTES: bool | str | None = '"'  # i.e. <tag="">


HTMX_ATTRIBUTES: frozenset[str] = frozenset(
    {
        "boost",
        "confirm",
        "delete",
        "disable",
        "disabled_elt",
        "disinherit",
        "download",
        "encoding",
        "ext",
        "get",
        "headers",
        "history",
        "history_elt",
        "ignore",
        "include",
        "indicator",
        "inherit",
        "live",
        "morph_skip",
        "morph_skip_children",
        "multipart",
        "optimistic",
        "params",
        "patch",
        "pending",
        "post",
        "preload",
        "preserve",
        "prompt",
        "push_url",
        "put",
        "query",
        "replace_url",
        "request",
        "select",
        "select_oob",
        "status",
        "swap",
        "swap_oob",
        "sync",
        "target",
        "targets",
        "trigger",
        "validate",
        "vals",
        "vars",
    }
)
"""Stable HTMX shortcut attributes supported by ``DOMConfig.HTMX_ENABLED``.

These are supplied without the ``hx`` prefix, for example ``_get="/items"`` or
``_swap_oob=True``. They render as ``data-hx-*`` secondary attributes by
default, which HTMX supports via its configurable secondary prefix.
"""

HTMX_LEGACY_ATTRIBUTES: frozenset[str] = frozenset({"sse", "ws"})
"""Legacy HTMX 1 shortcuts retained for backwards-compatible rendering."""

HTMX_EXTENSION_ATTRIBUTES: dict[str, str] = {
    "sse_close": "sse-close",
    "sse_connect": "sse-connect",
    "sse_swap": "sse-swap",
    "ws_connect": "ws-connect",
    "ws_send": "ws-send",
}
"""Legacy HTMX extension attributes that are not prefixed with ``hx-``."""


def _normalize_htmx_attribute(key: str) -> str | None:
    key = key.replace("__inherited", ":inherited")
    base_key = key.split(":", 1)[0]
    if key.startswith("hx_"):
        suffix = key[3:].replace("_", "-")
        if suffix:
            return f"data-hx-{suffix}"
    if key in HTMX_EXTENSION_ATTRIBUTES:
        return HTMX_EXTENSION_ATTRIBUTES[key]
    if key == "on" or key.startswith(("on:", "on-", "on_")):
        return f"data-hx-{key.replace('_', '-')}"
    if base_key in HTMX_ATTRIBUTES or base_key in HTMX_LEGACY_ATTRIBUTES:
        return f"data-hx-{key.replace('_', '-')}"
    return None


ALPINE_DIRECTIVES: frozenset[str] = frozenset(
    {
        "data",
        "bind",
        "on",
        "text",
        "html",
        "model",
        "modelable",
        "show",
        "transition",
        "for",
        "if",
        "id",
        "ref",
        "cloak",
        "effect",
        "ignore",
        "init",
        "teleport",
        "mask",
        "intersect",
        "collapse",
        "trap",
        "resize",
        "sort",
    }
)
"""Alpine.js directives recognised by ``DOMConfig.ALPINE_ENABLED``.

With that flag on, keyword arguments beginning with ``x_`` whose first segment
is one of these directives are rendered as ``x-`` attributes: a double
underscore becomes ``:`` and remaining single underscores become ``-``. So
``x_data`` renders ``x-data`` and ``x_on__click`` renders ``x-on:click``.
Directive modifiers that need a ``.`` (``x-on:keyup.enter``) still require the
``**{"x-on:keyup.enter": ...}`` form, as does the ``@``/``:`` shorthand.
"""


def _normalize_alpine_attribute(key: str) -> str | None:
    if not key.startswith("x_"):
        return None
    body = key[2:]
    if body.split("_", 1)[0] not in ALPINE_DIRECTIVES:
        return None
    return "x-" + body.replace("__", ":").replace("_", "-")


def _attribute_quote_mark() -> str:
    if DOMConfig.ATTRIBUTE_QUOTES is False or DOMConfig.ATTRIBUTE_QUOTES == "":
        return ""
    if DOMConfig.ATTRIBUTE_QUOTES is True or DOMConfig.ATTRIBUTE_QUOTES is None:
        return '"'
    return str(DOMConfig.ATTRIBUTE_QUOTES)


_ATTR_ESCAPE_DQ = {ord("&"): "&amp;", ord("<"): "&lt;", ord(">"): "&gt;", ord('"'): "&quot;"}
_ATTR_ESCAPE_SQ = {ord("&"): "&amp;", ord("<"): "&lt;", ord(">"): "&gt;", ord("'"): "&#x27;"}
_ATTR_ESCAPE_NONE = {
    ord("&"): "&amp;", ord("<"): "&lt;", ord(">"): "&gt;",
    ord('"'): "&quot;", ord("'"): "&#x27;",
}


def _escape_attribute_value(value: str, quote: str) -> str:
    """Escape a value for serialization inside an HTML attribute.

    Follows the HTML serialization algorithm: ``&``, ``<`` and ``>`` are always
    replaced, and whichever quote character delimits the value is replaced too.
    The opposite quote is left untouched so JavaScript handlers such as
    ``onclick="fn('x')"`` stay readable.
    """
    # Most attribute values (ids, classes, plain hrefs) need no escaping - one
    # membership scan is far cheaper than four chained str.replace calls.
    if "&" not in value and "<" not in value and ">" not in value:
        if quote == '"':
            if '"' not in value:
                return value
        elif quote == "'":
            if "'" not in value:
                return value
        elif '"' not in value and "'" not in value:
            return value
    table = (
        _ATTR_ESCAPE_DQ if quote == '"'
        else _ATTR_ESCAPE_SQ if quote == "'"
        else _ATTR_ESCAPE_NONE
    )
    return value.translate(table)


def _render_attribute_value(value: Any, escape: bool | None = None) -> str:
    quote = _attribute_quote_mark()
    should_quote = DOMConfig.ATTRIBUTE_QUOTES is not None or type(value) == str
    if escape is None:
        escape = DOMConfig.GLOBAL_AUTOESCAPE
    rendered_value = (
        _escape_attribute_value(str(value), quote) if escape else value
    )
    quote = quote if should_quote else ""
    return f"{quote}{rendered_value}{quote}"


# --- WHATWG HTML fragment serialization ------------------------------------
# https://html.spec.whatwg.org/multipage/parsing.html#serialising-html-fragments
#
# This is what a browser emits for ``innerHTML`` / ``outerHTML`` / ``getHTML()``
# and it differs from ``str(node)``, which keeps domonic's XHTML-flavoured
# authoring output (``<br/>``, bare boolean attributes, ``<``/``>`` escaped in
# attribute values). Ports whose fixtures diff against real browser output
# (DOMPurify, sanitiser suites) need this byte-compatible form.

_HTML_VOID_ELEMENTS = frozenset({
    "area", "base", "basefont", "bgsound", "br", "col", "embed", "frame", "hr",
    "img", "input", "keygen", "link", "meta", "param", "source", "track", "wbr",
})
_HTML_RAWTEXT_ELEMENTS = frozenset({
    "style", "script", "xmp", "iframe", "noembed", "noframes", "noscript",
    "plaintext",
})

# "escape a string" -- text mode replaces & \xa0 < > ; attribute mode replaces
# & \xa0 and the (double) quote, but never < or >.
_FRAGMENT_TEXT_ESCAPE = {
    ord("&"): "&amp;", ord("\xa0"): "&nbsp;",
    ord("<"): "&lt;", ord(">"): "&gt;",
}
_FRAGMENT_ATTR_ESCAPE = {
    ord("&"): "&amp;", ord("\xa0"): "&nbsp;", ord('"'): "&quot;",
}
_FRAGMENT_ATTR_NAME_ALIASES = {
    "accept_charset": "accept-charset",
    "http_equiv": "http-equiv",
    "is_": "is",
}


def _fragment_text_escape(data: str, raw: bool) -> str:
    if raw or (
        "&" not in data and "<" not in data
        and ">" not in data and "\xa0" not in data
    ):
        return data
    return data.translate(_FRAGMENT_TEXT_ESCAPE)


def _serialize_html_fragment(node: "Node") -> str:
    """Serialize ``node``'s children per the HTML fragment serialization algorithm."""
    out: list[str] = []
    _serialize_fragment_children(node, out)
    return "".join(out)


def _serialize_fragment_element(element: "Node", out: list) -> None:
    tagname = element.name or ""
    out.append("<")
    out.append(tagname)
    kwargs = getattr(element, "kwargs", None)
    if kwargs:
        for key, value in kwargs.items():
            if value is False:
                # a real DOM would not carry this attribute at all
                continue
            if value is True or value is None:
                value = ""
            out.append(" ")
            out.append(
                _FRAGMENT_ATTR_NAME_ALIASES.get(
                    key[1:] if key[:1] == "_" else key,
                    key[1:] if key[:1] == "_" else key,
                )
            )
            out.append('="')
            out.append(str(value).translate(_FRAGMENT_ATTR_ESCAPE))
            out.append('"')
    out.append(">")
    lname = tagname.lower()
    if lname in _HTML_VOID_ELEMENTS:
        return
    _serialize_fragment_children(
        element, out, raw=lname in _HTML_RAWTEXT_ELEMENTS
    )
    out.append("</")
    out.append(tagname)
    out.append(">")


def _serialize_fragment_children(node: "Node", out: list, raw: bool = False) -> None:
    for child in getattr(node, "args", None) or ():
        if type(child) is str:
            out.append(_fragment_text_escape(child, raw))
        elif isinstance(child, Text):
            out.append(
                _fragment_text_escape(child.args[0] if child.args else "", raw)
            )
        elif isinstance(child, Comment):
            out.append("<!--")
            out.append(str(child.data))
            out.append("-->")
        elif isinstance(child, ProcessingInstruction):
            out.append("<?")
            out.append(str(child.target))
            out.append(" ")
            out.append(str(child.data))
            out.append(">")
        elif isinstance(child, DocumentType):
            out.append("<!DOCTYPE ")
            out.append(str(getattr(child, "name", "") or ""))
            out.append(">")
        elif isinstance(child, Element):
            _serialize_fragment_element(child, out)
        elif isinstance(child, Node):
            # DocumentFragment or other container: serialize its children
            _serialize_fragment_children(child, out)
        else:
            out.append(_fragment_text_escape(str(child), raw))


def _find_wrapper_div(parsed: "Node") -> "Node | None":
    """Locate the synthetic ``<div>`` wrapper added by ``_parse_html_fragment``.

    Different parser backends shape a fragment parse differently -- some return
    the wrapper as the root node, some nest it in a full ``<html>`` skeleton --
    so search the root itself and then descendants in document order for the
    first ``div`` element.
    """
    if getattr(parsed, "name", None) == "div":
        return parsed
    stack = list(getattr(parsed, "args", None) or ())
    stack.reverse()
    while stack:
        node = stack.pop()
        if getattr(node, "name", None) == "div":
            return node
        kids = getattr(node, "args", None)
        if kids:
            stack.extend(reversed(kids))
    return None


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
    # iterate ``args`` directly rather than the ``childNodes`` property, which
    # allocates a fresh live NodeList wrapper on every (recursive) call
    for child in node.__dict__.get("args", ()):
        if isinstance(child, Node):
            yield from _iter_dom_nodes(child)


def _node_is_connected(node: "Node") -> bool:
    try:
        return isinstance(node.rootNode, Document)
    except Exception:
        return False


def _notify_attribute_changed(
    element: "Element", attribute: str, old_value: Any, new_value: Any
) -> None:
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


def _run_adopted_callback(
    element: "Element", old_document: "Document | None", new_document: "Document | None"
) -> None:
    callback = getattr(element, "adoptedCallback", None)
    if (
        callable(callback)
        and old_document is not None
        and old_document is not new_document
    ):
        callback(old_document, new_document)


def _adopt_tree(
    node: "Node", old_document: "Document | None", new_document: "Document | None"
) -> None:
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
        elif isinstance(node, (list, tuple)):
            prepared.extend(_coerce_insertion_nodes(*node))
        else:
            prepared.append(node)
    last_node_positions = {
        id(node): index for index, node in enumerate(prepared) if isinstance(node, Node)
    }
    return tuple(
        node
        for index, node in enumerate(prepared)
        if not isinstance(node, Node) or last_node_positions[id(node)] == index
    )


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


def _prepare_detached_clone(
    node: "Node",
    owner_document: "Document | None",
    old_document: "Document | None" = None,
    *,
    run_adopted: bool = False,
    upgrade_custom_elements: bool = False,
) -> "Node":
    node.parentNode = None
    node._update_parents()
    for current in _iter_dom_nodes(node):
        current._ownerDocument = owner_document
        current.isConnected = False
        if isinstance(current, Element):
            if upgrade_custom_elements:
                _upgrade_custom_element_instance(current)
            if run_adopted:
                _run_adopted_callback(current, old_document, owner_document)
    return node


def _upgrade_custom_element_instance(element: "Element") -> "Element":
    registry = _get_custom_element_registry()
    # Nothing is ever registered in the common case -- skip the per-element work.
    if registry is None or not getattr(registry, "store", None):
        return element
    return registry._upgrade_element(element)


def _connect_tree(node: "Node") -> None:
    # ``rootNode`` walks to the top of the tree; it is the same for every node in
    # the subtree being connected, so resolve it once.
    root = node.rootNode
    is_connected = isinstance(root, Document)
    owner = root if is_connected else getattr(node, "_ownerDocument", None)
    registry = _get_custom_element_registry()
    has_custom_elements = registry is not None and bool(
        getattr(registry, "store", None)
    )
    for current in _iter_dom_nodes(node):
        current._ownerDocument = owner
        current.isConnected = is_connected
        if isinstance(current, Element):
            if has_custom_elements:
                _upgrade_custom_element_instance(current)
            if is_connected:
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
        slots = [
            child for child in target.childNodes if isinstance(child, HTMLSlotElement)
        ]
    elif isinstance(target, Element) and isinstance(
        getattr(target, "shadowRoot", None), ShadowRoot
    ):
        slots = [
            child
            for child in target.shadowRoot.childNodes
            if isinstance(child, HTMLSlotElement)
        ]
    for slot in slots:
        slot.dispatchEvent(Event("slotchange"))


def _iter_ancestors_inclusive(node: "Node | None") -> Iterator["Node"]:
    current = node
    while isinstance(current, Node):
        yield current
        current = getattr(current, "parentNode", None)


def _normalize_mutation_observer_options(options: dict[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {
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
        raise TypeError(
            "MutationObserver options must enable childList, attributes, or characterData"
        )
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


def _default_intersection_root_rect(
    target: "Element", target_rect: DOMRectReadOnly
) -> DOMRectReadOnly:
    doc = target.ownerDocument if isinstance(target.ownerDocument, Document) else None
    root = None
    if doc is not None:
        root = getattr(doc, "documentElement", None) or getattr(doc, "body", None)
    if isinstance(root, Element) and root is not target:
        return root.getBoundingClientRect()
    return DOMRectReadOnly.fromRect(target_rect)


def _process_observer_notifications(
    target: "Node | None" = None, target_rect: DOMRectReadOnly | None = None
) -> None:
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
        for io_observer in intersection_observers:
            io_observer._process(target, target_rect)
    finally:
        _observer_processing = False


def _form_owner(control: "Element") -> "HTMLFormElement | None":
    owner_document = (
        control.ownerDocument if isinstance(control.ownerDocument, Document) else None
    )
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


def _dispatch_before_input_event(
    control: "Element",
    new_value: Any,
    *,
    input_type: str = "insertReplacementText",
) -> bool:
    from domonic.events import InputEvent

    event = InputEvent(
        "beforeinput",
        {
            "bubbles": True,
            "cancelable": True,
            "data": "" if new_value is None else str(new_value),
            "inputType": input_type,
            "isComposing": False,
        },
    )
    return control.dispatchEvent(event)


def _append_form_data_value(data: dict[str, Any], name: str | None, value: Any) -> None:
    if not name:
        return
    if name in data:
        existing = data[name]
        if isinstance(existing, list):
            existing.append(value)
        else:
            data[name] = [existing, value]
        return
    data[name] = value


def _construct_form_data(
    form: "HTMLFormElement", submitter: "Element | None" = None
) -> dict[str, Any]:
    data: dict[str, Any] = {}
    for control in form.elements:
        if not isinstance(control, Element) or control.hasAttribute("disabled"):
            continue
        name = control.getAttribute("name")
        if not name:
            continue
        if control is submitter:
            continue
        if isinstance(control, HTMLButtonElement):
            continue
        if isinstance(control, HTMLInputElement):
            input_type = control.type
            if input_type in {"button", "image", "reset", "submit"}:
                continue
            if input_type in {"checkbox", "radio"} and not control.checked:
                continue
            _append_form_data_value(data, name, control.value)
        elif isinstance(control, HTMLSelectElement):
            if control.hasAttribute("multiple"):
                for option in control.selectedOptions:
                    _append_form_data_value(data, name, option.value)
            else:
                _append_form_data_value(data, name, control.value)
        elif isinstance(control, HTMLTextAreaElement):
            _append_form_data_value(data, name, control.value)
        elif hasattr(control, "value"):
            _append_form_data_value(data, name, getattr(control, "value"))

    if (
        isinstance(submitter, Element)
        and not submitter.hasAttribute("disabled")
        and submitter.getAttribute("name")
    ):
        _append_form_data_value(data, submitter.getAttribute("name"), submitter.value)
    return data


def _radio_group_members(
    control: "Element", *, include_disabled: bool = True
) -> list["HTMLInputElement"]:
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


def _control_value(control: "Element") -> str:
    value = getattr(control, "value", "")
    return "" if value is None else str(value)


def _constraint_number(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _constraint_int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


class ValidityState:
    """Represents the constraint-validation state for a form control."""

    def __init__(self, element: "Element") -> None:
        self._element = element

    @property
    def badInput(self) -> bool:
        input_type = (self._element.getAttribute("type") or "").lower()
        value = _control_value(self._element)
        return bool(
            value
            and input_type in {"number", "range"}
            and _constraint_number(value) is None
        )

    @property
    def customError(self) -> bool:
        return bool(getattr(self._element, "_custom_validity_message", ""))

    @property
    def patternMismatch(self) -> bool:
        pattern = self._element.getAttribute("pattern")
        value = _control_value(self._element)
        if not pattern or value == "":
            return False
        try:
            return re.fullmatch(str(pattern), value) is None
        except re.error:
            return False

    @property
    def rangeOverflow(self) -> bool:
        value = _constraint_number(_control_value(self._element))
        maximum = _constraint_number(self._element.getAttribute("max"))
        return value is not None and maximum is not None and value > maximum

    @property
    def rangeUnderflow(self) -> bool:
        value = _constraint_number(_control_value(self._element))
        minimum = _constraint_number(self._element.getAttribute("min"))
        return value is not None and minimum is not None and value < minimum

    @property
    def stepMismatch(self) -> bool:
        step = self._element.getAttribute("step")
        if step in (None, "any"):
            return False
        value = _constraint_number(_control_value(self._element))
        step_value = _constraint_number(step)
        if value is None or step_value in (None, 0):
            return False
        base = _constraint_number(self._element.getAttribute("min")) or 0
        remainder = (value - base) % step_value
        return not (abs(remainder) < 1e-9 or abs(remainder - step_value) < 1e-9)

    @property
    def tooLong(self) -> bool:
        maximum = _constraint_int(self._element.getAttribute("maxlength"))
        return maximum is not None and len(_control_value(self._element)) > maximum

    @property
    def tooShort(self) -> bool:
        minimum = _constraint_int(self._element.getAttribute("minlength"))
        value = _control_value(self._element)
        return bool(value and minimum is not None and len(value) < minimum)

    @property
    def typeMismatch(self) -> bool:
        input_type = (self._element.getAttribute("type") or "").lower()
        value = _control_value(self._element)
        if value == "":
            return False
        if input_type == "email":
            values = [value]
            if self._element.hasAttribute("multiple"):
                values = [item.strip() for item in value.split(",")]
            return any(
                re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", item) is None
                for item in values
            )
        if input_type == "url":
            return re.fullmatch(r"[a-zA-Z][a-zA-Z0-9+.-]*://[^\s]+", value) is None
        return False

    @property
    def valid(self) -> bool:
        return not any(
            (
                self.badInput,
                self.customError,
                self.patternMismatch,
                self.rangeOverflow,
                self.rangeUnderflow,
                self.stepMismatch,
                self.tooLong,
                self.tooShort,
                self.typeMismatch,
                self.valueMissing,
            )
        )

    @property
    def valueMissing(self) -> bool:
        if self._element.hasAttribute("disabled") or not self._element.hasAttribute(
            "required"
        ):
            return False
        tag_name = getattr(
            self._element, "tagName", getattr(self._element, "name", "")
        ).lower()
        if tag_name == "input":
            input_type = (self._element.getAttribute("type") or "text").lower()
            if input_type == "checkbox":
                return not self._element.checked
            if input_type == "radio":
                return not any(
                    radio.checked
                    for radio in _radio_group_members(
                        self._element, include_disabled=False
                    )
                )
        return _control_value(self._element) == ""


def _is_control_valid(control: "Element") -> bool:
    if not isinstance(control, Element) or control.hasAttribute("disabled"):
        return True
    return not getattr(control, "willValidate", True) or control.validity.valid


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

    __isempty: bool = (
        False  # tells us if the node is empty i.e. has no content aka 'self closing'. in html that would be: area, base, br, col, embed, hr, img, input, link, meta, param, source, track, True
    )
    __context: ClassVar[list["Node"] | None] = (
        None  # private. tags will append to last item in context on creation.
    )

    # populated in __init__; declared here so mypy does not infer them as
    # permanently ``None`` from the initial assignment
    parentNode: "Node | None"
    prefix: str | None
    outerText: Any
    _ownerDocument: "Document | None"

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
        # ``args`` -- skip the fragment/dedup coercion for the trivial cases
        # (no children, or a single non-Node child), which is the vast majority
        # of programmatic construction and every text-only element.
        if not args:
            self.__dict__["args"] = ()
        elif len(args) == 1 and not isinstance(args[0], (Node, list, tuple)):
            self.__dict__["args"] = args
        else:
            self.__dict__["args"] = _coerce_insertion_nodes(*args)

        # ``kwargs`` -- attributes get a leading underscore; build the dict once
        if kwargs:
            self.kwargs = {
                (k if k[:1] == "_" else "_" + k): v for k, v in kwargs.items()
            }
        else:
            self.kwargs = {}

        nm = getattr(self, "name", None)
        if nm is None:
            self.name = ""

        self._baseURI: str = ""
        self.isConnected: bool = True
        self.namespaceURI: str = "http://www.w3.org/1999/xhtml"
        self.outerText = None
        self._ownerDocument = None
        self.parentNode = None
        self.prefix = None  # 🗑️
        self._escape_text_on_render = False
        # Attribute values are always escaped on serialization: emitting a raw
        # ``"`` / ``&`` / ``<`` inside a quoted value produces malformed markup
        # that corrupts on the next parse (e.g. Parsoid ``data-mw='{...}'`` JSON
        # spilling into page text). Parser-built elements already force this on;
        # programmatically built ones (constructors, ``createElement``) need the
        # same default. Set to ``False`` on an individual node to opt out.
        self._escape_attributes_on_render = True
        # self.baseURIObject = None  # ?
        # self.nodePrincipal = None
        if self.__dict__["args"]:
            self._update_parents()

        # namespaceURI from the tag name -- ``parentNode`` is always None during
        # __init__, so ``rootNode`` is ``self`` and ``rootNode.tagName`` is just
        # this node's own name.
        if nm == "svg":
            self.namespaceURI = "http://www.w3.org/2000/svg"
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
            #     self.namespaceURI = "http://www.w3.org/2004/02/skos/core#"
            # elif nm == "wot":
            #     self.namespaceURI = "http://xmlns.com/wot/0.1/"
            # elif nm == "wgs84_pos":
            #     self.namespaceURI = "http://www.w3.org/2003/01/geo/wgs84_pos#"
            # elif nm == "xhv":
            #     self.namespaceURI = "http://www.w3.org/1999/xhtml/vocab#"

        # this is for using 'with'
        if Node.__context is not None:
            Node.__context[len(Node.__context) - 1] += self
        super().__init__(*args, **kwargs)

    @property
    def content(self):
        return "".join(self._stream_content())

    @content.setter
    def content(self, ignore):
        self.__content = "".join([each.__str__() for each in self.args])
        return

    @property
    def __attributes__(self):
        def format_attr(key, value):
            escape_attribute = bool(
                self.__dict__.get("_escape_attributes_on_render", False)
            )
            if value is True:
                value = "true"
            if value is False:
                value = "false"
            key = key.split("_", 1)[1]
            key = {
                "accept_charset": "accept-charset",
                "http_equiv": "http-equiv",
                "is_": "is",
            }.get(key, key)

            if DOMConfig.HTMX_ENABLED:
                htmx_attribute = _normalize_htmx_attribute(key)
                if htmx_attribute is not None:
                    return (
                        f""" {htmx_attribute}="""
                        f"""{_render_attribute_value(
                            value,
                            DOMConfig.GLOBAL_AUTOESCAPE or escape_attribute,
                        )}"""
                    )

            if DOMConfig.ALPINE_ENABLED:
                alpine_attribute = _normalize_alpine_attribute(key)
                if alpine_attribute is not None:
                    return (
                        f""" {alpine_attribute}="""
                        f"""{_render_attribute_value(
                            value,
                            DOMConfig.GLOBAL_AUTOESCAPE or escape_attribute,
                        )}"""
                    )

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
                "autoplay",  # Added
                "controls",  # Added
                "loop",  # Added
                "muted",  # Added
                "default",  # Added
                "allowfullscreen",  # Added
                "playsinline",  # Added
                "attributionsrc",  # Attribution Reporting API
                "toolautosubmit",  # WebMCP declarative forms
                "value",  # Added
                "defer",  # Added
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
            return f""" {key}={_render_attribute_value(
                value,
                DOMConfig.GLOBAL_AUTOESCAPE or escape_attribute,
            )}"""

        try:
            return "".join(
                [format_attr(key, value) for key, value in self.kwargs.items()]
            )
        except IndexError as e:
            from domonic.html import TemplateError

            raise TemplateError(e)
        # except Exception as e:

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

    def __str__(self):
        return "".join(self.stream())

    def _stream_value(self, value: Any) -> Iterator[str]:
        if callable(value) and not isinstance(value, Node):
            value = value()

        if isinstance(value, Text):
            escape_text = DOMConfig.GLOBAL_AUTOESCAPE or bool(
                getattr(value, "_escape_text_on_render", False)
            )
            value = str(value.textContent)
            yield _escape_html(value) if escape_text else value
            return

        if isinstance(value, Node):
            yield from value.stream()
            return

        if isinstance(value, IterableABC) and not isinstance(
            value, (str, bytes, bytearray, dict)
        ):
            for child in value:
                yield from self._stream_value(child)
            return

        value = str(value)
        yield _escape_html(value) if DOMConfig.GLOBAL_AUTOESCAPE else value

    def _stream_content(self) -> Iterator[str]:
        for child in self.args:
            yield from self._stream_value(child)

    def stream(self) -> Iterator[str]:
        """Yield rendered HTML chunks without materialising the full subtree."""
        optional_closing_tags = {
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
        }
        stack: list[tuple[str, Any]] = [("value", self)]
        while stack:
            kind, value = stack.pop()
            if kind == "close":
                yield f"</{value.name}>"
                continue
            if kind == "iter":
                try:
                    child = next(value)
                except StopIteration:
                    continue
                stack.append(("iter", value))
                stack.append(("value", child))
                continue

            if callable(value) and not isinstance(value, Node):
                value = value()

            if isinstance(value, Text):
                escape_text = DOMConfig.GLOBAL_AUTOESCAPE or bool(
                    getattr(value, "_escape_text_on_render", False)
                )
                value = str(value.textContent)
                yield _escape_html(value) if escape_text else value
                continue

            if isinstance(value, Node):
                custom_stream = getattr(type(value), "stream", None)
                if custom_stream is not None and custom_stream is not Node.stream:
                    yield from value.stream()
                    continue

                yield f"<{value.name}{value.__attributes__}>"
                if (
                    DOMConfig.RENDER_OPTIONAL_CLOSING_TAGS
                    or value.name not in optional_closing_tags
                ):
                    stack.append(("close", value))
                stack.append(("iter", iter(value.args)))
                continue

            if isinstance(value, IterableABC) and not isinstance(
                value, (str, bytes, bytearray, dict)
            ):
                stack.append(("iter", iter(value)))
                continue

            value = str(value)
            yield _escape_html(value) if DOMConfig.GLOBAL_AUTOESCAPE else value

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
        if isinstance(item, (list, tuple)):
            for i in item:
                self.appendChild(i)
            return self

        self.appendChild(item)
        return self

    def __isub__(self, item):
        """removes an item from the list of children"""
        self.removeChild(item)
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
            return getattr(self, index, None)
        # return super(Node, self).__getitem__(index)

    def __rshift__(self, item):
        try:
            for key in item.keys():
                self.kwargs[key] = item[key]
            return self
        except (AttributeError, TypeError) as exc:
            raise ValueError from exc

    # def __add__(self, item):
    #     try:
    #         self.args = self.args + (item,)
    #         return self
    #     except Exception as e:
    #         raise ValueError

    # def __sub__(self, item):
    #     try:
    #         self.args = self.args - (item,)
    #         return self
    #     except Exception as e:
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

        if self.__class__.__name__ == "a" and attr == "href":
            return ""

        try:
            # return getattr(super(), attr)
            # return getattr(self, attr)
            # return getattr(Node, attr)  # means overrideing for style etc in element?
            return getattr(
                self.__class__, attr
            )  # means overrideing for style etc in element?
            # return getattr(Element, attr)
        except AttributeError as e:
            raise e

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
        for arg in self.args:
            try:
                if isinstance(arg, Text):
                    params += '"' + str(arg) + '"' + ", "
                else:
                    params += f"{arg.__pyml__()}, "
            except Exception as e:
                params += str(arg) + ", "
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
        except (AttributeError, TypeError) as exc:
            raise ValueError from exc

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

    def __iter__(self):
        return iter(self.args)

    def __format__(self, format_spec):
        # return super().__format__(format_spec)
        # get node depth by counting parents

        # Indentation depth is derived from the current parent chain.
        n = self
        depth = 0
        while n is not None:
            n = n.parentNode
            depth += 1

        depth -= 1

        # dent = '    ' * depth
        dent = "\t" * depth

        # loop the children and call __format__ on each one
        # content = ""
        # for child in self.childNodes:
        #     content += child.__format__(format_spec)

        self._update_parents()

        render_args = self.args
        if DOMConfig.GLOBAL_AUTOESCAPE:
            render_args = tuple(
                _escape_html(str(child.textContent))
                if isinstance(child, Text)
                else _escape_html(str(child))
                if isinstance(child, str)
                else child
                for child in self.args
            )
        else:
            render_args = tuple(
                _escape_html(str(child.textContent))
                if isinstance(child, Text)
                and bool(getattr(child, "_escape_text_on_render", False))
                else child
                for child in self.args
            )

        content = "".join([each.__format__(format_spec) for each in render_args])
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
            dtype = str(self.doctype) if self.doctype else ""

        # if self is a closed_tag, return the content
        from domonic.html import closed_tag

        if isinstance(self, closed_tag):
            return f"\n{dent}<{self.name}{self.__attributes__} />"

        # in html5 the following tags are optional closing tags
        # html, head, body, p, dt, dd, li, option, thead, th, tbody, tr, td, tfoot, colgroup
        size = len(str(content))

        if DOMConfig.RENDER_OPTIONAL_CLOSING_TAGS:
            if size < 150 and wrap:
                return (
                    f"\n{dent}<{self.name}{self.__attributes__}>{content}</{self.name}>"
                )
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
                    return (
                        f"{dtype}\n{dent}<{self.name}{self.__attributes__}>{content}\n"
                    )
            else:
                if size < 150 and wrap:
                    return f"\n{dent}<{self.name}{self.__attributes__}>{content}</{self.name}>"
                else:
                    return f"{dtype}\n{dent}<{self.name}{self.__attributes__}>{content}\n{dent}</{self.name}>"

    # def __call__(self, *args, **kwargs):
    #     """
    #     allows for calling the object as a function
    #     """

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "args":
            super().__setattr__(name, value)
            self._update_parents()
            return
        super().__setattr__(name, value)

    # def __getattr__(self, name):
    #     try:
    #         if name == "args":
    #             return super(Node, self).__getattr__(name)
    #     except Exception as e:
    #     return super(Node, self).__getattr__(name)

    # def __getattribute__(self, name):
    # try:
    #     if name == "args":
    #         return super(Node, self).__getattribute__(name)
    # except Exception as e:
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

    def _update_parents(self):
        """Assign this node as parent for child nodes.

        This is called manually when ``args`` are amended because a decorator
        here would interfere with JSON serialisation in a few older helpers.
        """
        try:
            for el in self.args:
                # if(type(el) not in [str, list, dict, int, float, tuple, object, set]):
                if isinstance(el, (Element, Node)):
                    el.parentNode = self
                    el._update_parents()
        except (AttributeError, TypeError) as exc:
            warnings.warn(f"unable to update parent: {exc}", RuntimeWarning)

    def _iterate(self, element, callback) -> None:
        """Walk descendant nodes and call ``callback`` for each node.

        Lists are tolerated for backwards compatibility with older code that
        passed child groups directly.
        """
        callback(element)
        elements = []
        if isinstance(element, Node):
            elements = element.args
        elif isinstance(element, list):
            elements = element
        for el in elements:
            if type(el) not in [str, list, dict, int, float, tuple, object, set]:
                # callback(el)
                el._iterate(el, callback)
            elif isinstance(
                el, list
            ):  # if someone is incorrectly using a list as a child
                for e in el:
                    if type(e) not in (
                        str,
                        list,
                        dict,
                        int,
                        float,
                        tuple,
                        object,
                        set,
                    ):
                        e._iterate(e, callback)

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
        old_documents = [(item, _detach_node_for_insertion(item)) for item in items]
        previous_sibling = self.args[-1] if len(self.args) else None
        self.__dict__["args"] = self.args + items
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
        return len(self.children)

    @property
    def childNodes(self) -> "NodeList":
        """Returns a live NodeList containing all the children of this node"""
        return _LiveNodeList(self)

    @property
    def children(self) -> list[Node]:
        """Returns a live collection of child nodes, excluding string content."""
        return _LiveNodeList(self, lambda child: not isinstance(child, str))

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

        if referenceTop != otherTop:
            return Node.DOCUMENT_POSITION_DISCONNECTED

        children = reference.childNodes

        ret = recursivelyWalk(children, lambda p: testNodeForComparePosition(other, p))
        if ret:
            return (
                Node.DOCUMENT_POSITION_CONTAINED_BY
            )  # + Node.DOCUMENT_POSITION_FOLLOWING

        children = other.childNodes
        ret = recursivelyWalk(
            children, lambda p: testNodeForComparePosition(reference, p)
        )
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
            return self.args[0]
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
        # if isinstance(self, Text):
        #     return '#text'
        # if isinstance(self, Comment):
        # return '#comment'
        # elif isinstance(self, DocumentType):
        #     return '#doctype'
        if isinstance(
            self, Document
        ):  # NOTE - having this one on breaks parser. as it expects 'html'?
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
        return None

    @nodeValue.setter
    def nodeValue(self, content: Any):
        """Sets or returns the value of a node"""
        return content

    @property
    def baseURI(self) -> str:
        """Returns the absolute base URL for this node."""
        explicit_base = getattr(self, "_baseURI", "")
        if explicit_base:
            return explicit_base
        if isinstance(self, Document):
            return self._document_base_uri()
        owner_document = self.ownerDocument
        if isinstance(owner_document, Document):
            return owner_document.baseURI
        return ""

    @baseURI.setter
    def baseURI(self, value: str | None) -> None:
        self._baseURI = "" if value is None else str(value)

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
        self._ownerDocument = (
            newOwner
            if isinstance(newOwner, Document)
            else getattr(newOwner, "ownerDocument", None)
        )

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
        """
        if reference_node is None:
            return self.appendChild(new_node)
        if new_node is reference_node:
            return new_node

        items = _coerce_insertion_nodes(new_node)
        old_documents = [(item, _detach_node_for_insertion(item)) for item in items]
        try:
            index = self.args.index(reference_node)
        except ValueError as exc:
            raise ValueError("reference_node is not a child of this node") from exc
        previous_sibling = (
            self.args[index - 1]
            if index > 0 and isinstance(self.args[index - 1], Node)
            else None
        )
        self.__dict__["args"] = self.args[:index] + items + self.args[index:]
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

    def removeChild(self, node: Any) -> Any:
        """removes a child node from the DOM and returns the removed node."""
        for count, each in enumerate(self.args):
            if type(each) == str:
                if each != node:
                    continue
                replace_args = list(self.args)
                replace_args.pop(count)
                # bypass Node.__setattr__ -> _update_parents(): removing one
                # child never changes the parent link of the siblings that stay.
                self.__dict__["args"] = tuple(replace_args)
                _notify_slot_change(self)
                return each

            if each is node:
                n = node
                previous_sibling = n.previousSibling
                next_sibling = n.nextSibling
                _disconnect_tree(n)
                n.parentNode = None
                replace_args = list(self.args)
                replace_args.pop(count)
                self.__dict__["args"] = tuple(replace_args)
                _queue_mutation_record(
                    "childList",
                    self,
                    removed_nodes=(n,),
                    previous_sibling=previous_sibling,
                    next_sibling=next_sibling,
                )
                _notify_slot_change(self)

                return n

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
        old_documents = [(item, _detach_node_for_insertion(item)) for item in items]
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
        # _connect_inserted_node below re-parents the new items; the siblings
        # that stay keep their parent link, so skip the recursive _update_parents.
        self.__dict__["args"] = tuple(replace_args)
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
            clone = copy.deepcopy(self)
        else:
            clone = copy.copy(self)  # shallow copy
            clone.args = ()
        owner_document = (
            self.ownerDocument if isinstance(self.ownerDocument, Document) else None
        )
        return _prepare_detached_clone(clone, owner_document)

    def isSameNode(self, node):
        """Checks if two elements are the same node"""
        return self == node

    def isEqualNode(self, node):
        """Checks if two elements are equal"""
        return str(self) == str(node)

    def getRootNode(self, options=None):
        composed = False
        if isinstance(options, dict):
            composed = bool(options.get("composed", False))
        elif options is not None:
            composed = bool(getattr(options, "composed", False))

        root = self.rootNode
        if composed and isinstance(root, ShadowRoot):
            return root.host.getRootNode({"composed": True})
        return root

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
        outp = ""
        for each in self.args:
            if type(each) is str:
                outp = outp + each
            else:
                if getattr(each, "nodeType", None) in (
                    Node.COMMENT_NODE,
                    Node.PROCESSING_INSTRUCTION_NODE,
                ):
                    continue
                val = each.textContent
                if val is not None:
                    outp = outp + val
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
            return self.kwargs
        except Exception as e:
            return None

    @property
    def tail(self):
        """ElementTree compatibility: text that follows this element's end tag.

        domonic models trailing text as a sibling text node rather than an
        attribute of the preceding element, so there is nothing to return here.
        (Returning the subtree text made every ``elementpath`` tree build walk
        the whole subtree twice per node.)
        """
        return None

    @property
    def length(self) -> int:
        return len(self)

    def is_matching(self, name, default_namespace=None):
        """
        Determine if this node matches the given name and namespace.
        """
        if name and name != self.tagName:
            return False
        if default_namespace and getattr(self, "namespace", None) != default_namespace:
            return False
        return True


class ParentNode:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # @property
    # def childElementCount(self):
    #     return len(self.args)

    @property
    def children(self) -> "NodeList":
        """Return list of child nodes."""
        return _LiveNodeList(
            self,  # type: ignore[arg-type]
            lambda child: isinstance(child, Element),
        )

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
        for child in reversed(self.childNodes):
            if child.nodeType == Node.ELEMENT_NODE:
                return child
        return None

    def append(self, *args):
        items = _coerce_insertion_nodes(*args)
        old_documents = [(item, _detach_node_for_insertion(item)) for item in items]
        self.__dict__["args"] = self.args + items
        for item, old_document in old_documents:
            _connect_inserted_node(self, item, old_document)
        return self

    def prepend(self, *args):
        items = _coerce_insertion_nodes(*args)
        old_documents = [(item, _detach_node_for_insertion(item)) for item in items]
        self.__dict__["args"] = items + tuple(self.args)
        for item, old_document in old_documents:
            _connect_inserted_node(self, item, old_document)
        return self

    def replaceChildren(self, *children):
        for child in self.args:
            if isinstance(child, Node):
                _disconnect_tree(child)
                child.parentNode = None
        items = _coerce_replacement_nodes(*children)
        old_documents = [(item, _detach_node_for_insertion(item)) for item in items]
        self.__dict__["args"] = items
        for item, old_document in old_documents:
            _connect_inserted_node(self, item, old_document)


class ChildNode(Node):
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

    def __repr__(self) -> str:
        return f'Attr(name={self.name!r}, value={self.value!r})'

    def __str__(self) -> str:
        return "" if self.value is None else str(self.value)

    @property
    def isId(self) -> bool:
        if self.name == "id":
            return True
        else:
            return False

    def getNamedItem(self, name: str):
        """Returns a specified attribute node from a NamedNodeMap"""
        if self.parentNode is None:
            return None
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
        parent = self.parentNode
        if parent is None:
            return False
        for item in parent.attributes:
            if item.name == name:
                parent.removeAttribute(item)
                return True
        return False

    def setNamedItem(self, name: str, value) -> bool:
        """Sets the specified attribute node (by name)"""
        if self.parentNode is None:
            return False
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

    def __init__(
        self, args: Iterable[Attr] | None = None, ownerDocument=None, parentNode=None
    ):
        self.parentNode = parentNode
        self.ownerDocument = ownerDocument
        self._attrs = list(args or [])

    @property
    def _seq(self) -> list[Any]:
        """Compatibility alias used by the Expat/minidom-style parser."""
        return self._attrs

    @_seq.setter
    def _seq(self, value: Iterable[Any] | None) -> None:
        self._attrs = list(value or [])

    def _normalize_name(self, name: str) -> str:
        return name[1:] if isinstance(name, str) and name.startswith("_") else name

    def _storage_key(self, name: str) -> str:
        normalized = self._normalize_name(name)
        return normalized if normalized.startswith("_") else f"_{normalized}"

    def _current_attrs(self) -> list[Attr]:
        if self.parentNode is not None and hasattr(self.parentNode, "kwargs"):
            return [
                Attr(key.lstrip("_"), value)
                for key, value in self.parentNode.kwargs.items()
            ]
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
            self._attrs = [
                existing for existing in self._attrs if existing.name != normalized
            ]
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
            self._attrs = [
                existing for existing in self._attrs if existing.name != normalized
            ]
        return old_attr

    def getNamedItemNS(self, namespaceURI: str, localName: str) -> Attr | None:
        normalized = self._normalize_name(localName)
        for item in self._current_attrs():
            item_local_name = item.name.split(":", 1)[-1]
            if (
                item_local_name == normalized
                and self._attribute_namespace(item) == namespaceURI
            ):
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

    def __getattr__(self, name: str) -> Any:
        # only reached when normal attribute lookup fails; internal names
        # ("_element", "_store") are set via __dict__ so never land here.
        if name.startswith("_"):
            raise AttributeError(name)
        try:
            return self._data()[name]
        except KeyError:
            return undefined

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith("_"):
            object.__setattr__(self, name, value)
            return
        self[name] = value

    def __delattr__(self, name: str) -> None:
        if name.startswith("_"):
            object.__delattr__(self, name)
            return
        del self[name]

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

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        self._x = value

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        self._y = value

    @property
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        self._width = value

    @property
    def height(self) -> float:
        return self._height

    @height.setter
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
        if self.offsetNode is not None and hasattr(
            self.offsetNode, "getBoundingClientRect"
        ):
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
        return self.rangeCount == 0 or all(
            range_obj.collapsed for range_obj in self._ranges
        )

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
        self._ranges = [
            candidate for candidate in self._ranges if candidate is not range_obj
        ]
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
            self._set_anchor_focus(
                active_range.startContainer, active_range.startOffset, node, offset
            )
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

    def containsNode(
        self, node: Node | None, allowPartialContainment: bool = False
    ) -> bool:
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
        if len(token) == 0:
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

    @property
    def value(self) -> str:
        return self.toString()

    @value.setter
    def value(self, new_value: str) -> None:
        tokens: list[str] = []
        for item in str(new_value or "").split():
            token = self._validate_token(item)
            if token not in tokens:
                tokens.append(token)
        list.clear(self)
        list.extend(self, tokens)
        self._sync()

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

    def __iadd__(self, token):  # type: ignore[misc]
        self.add(token)
        return self

    def __isub__(self, token):
        self.remove(token)
        return self

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
        return (
            list.__getitem__(self, index) if 0 <= index < list.__len__(self) else None
        )

    def toString(self) -> str:
        """Returns a string containing all tokens in the list, with spaces separating each token"""
        self._reload()
        return " ".join(list.__iter__(self))

    def entries(self) -> Iterable[tuple[int, str]]:
        """Returns an iterator over index/token pairs."""
        self._reload()
        for i in range(len(self)):
            yield i, list.__getitem__(self, i)

    def forEach(
        self, func: Callable[[str, int, "DOMTokenList"], Any], thisArg: Any = None
    ) -> None:
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


class ShadowRoot(Node):
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

    def caretPositionFromPoint(
        self, x: float = 0, y: float = 0
    ) -> CaretPosition | None:
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
    __slots__ = (
        "name",
        "publicId",
        "systemId",
        "_internalSubset",
        "_entities",
        "_notations",
    )

    def __init__(
        self, name: str = "html", publicId: str = "", systemId: str = ""
    ) -> None:
        self.name: str = name  # A DOMString, eg "html" for <!DOCTYPE HTML>.
        self.publicId: str = (
            publicId  # eg "-//W3C//DTD HTML 4.01//EN", empty string for HTML5.
        )
        self.systemId: str = (
            systemId  # eg "http://www.w3.org/TR/html4/strict.dtd", empty string for HTML5.
        )
        self._internalSubset: str | None = None
        self._entities = NamedNodeMap()
        self._notations = NamedNodeMap()
        super().__init__()

    @property
    def internalSubset(self):
        """A DOMString of the internal subset, or None. Eg "<!ELEMENT foo (bar)>"."""
        return self._internalSubset

    @internalSubset.setter
    def internalSubset(self, value: str | None) -> None:
        self._internalSubset = value

    @property
    def entities(self) -> NamedNodeMap:
        """A NamedNodeMap with entities declared in the DTD."""
        return self._entities

    @property
    def notations(self) -> NamedNodeMap:
        """A NamedNodeMap with notations declared in the DTD."""
        return self._notations

    def __str__(self) -> str:
        # return f"<!DOCTYPE {self.name} {self.publicId} {self.systemId}>"
        full_str = f"<!DOCTYPE {self.name}"
        if self.publicId:
            full_str += f" PUBLIC {self.publicId}"
        if self.systemId:
            full_str += f" SYSTEM {self.systemId}"
        full_str += ">"
        return full_str

    def stream(self) -> Iterator[str]:
        yield str(self)


_ARIA_REFLECTED_ATTRIBUTES: tuple[tuple[str, str], ...] = (
    ("role", "role"),
    ("ariaAtomic", "aria-atomic"),
    ("ariaAutoComplete", "aria-autocomplete"),
    ("ariaBrailleLabel", "aria-braillelabel"),
    ("ariaBrailleRoleDescription", "aria-brailleroledescription"),
    ("ariaBusy", "aria-busy"),
    ("ariaChecked", "aria-checked"),
    ("ariaColCount", "aria-colcount"),
    ("ariaColIndex", "aria-colindex"),
    ("ariaColIndexText", "aria-colindextext"),
    ("ariaColSpan", "aria-colspan"),
    ("ariaCurrent", "aria-current"),
    ("ariaDescription", "aria-description"),
    ("ariaDisabled", "aria-disabled"),
    ("ariaExpanded", "aria-expanded"),
    ("ariaHasPopup", "aria-haspopup"),
    ("ariaHidden", "aria-hidden"),
    ("ariaInvalid", "aria-invalid"),
    ("ariaKeyShortcuts", "aria-keyshortcuts"),
    ("ariaLabel", "aria-label"),
    ("ariaLevel", "aria-level"),
    ("ariaLive", "aria-live"),
    ("ariaModal", "aria-modal"),
    ("ariaMultiLine", "aria-multiline"),
    ("ariaMultiSelectable", "aria-multiselectable"),
    ("ariaOrientation", "aria-orientation"),
    ("ariaPlaceholder", "aria-placeholder"),
    ("ariaPosInSet", "aria-posinset"),
    ("ariaPressed", "aria-pressed"),
    ("ariaReadOnly", "aria-readonly"),
    ("ariaRelevant", "aria-relevant"),
    ("ariaRequired", "aria-required"),
    ("ariaRoleDescription", "aria-roledescription"),
    ("ariaRowCount", "aria-rowcount"),
    ("ariaRowIndex", "aria-rowindex"),
    ("ariaRowIndexText", "aria-rowindextext"),
    ("ariaRowSpan", "aria-rowspan"),
    ("ariaSelected", "aria-selected"),
    ("ariaSetSize", "aria-setsize"),
    ("ariaSort", "aria-sort"),
    ("ariaValueMax", "aria-valuemax"),
    ("ariaValueMin", "aria-valuemin"),
    ("ariaValueNow", "aria-valuenow"),
    ("ariaValueText", "aria-valuetext"),
)

_ARIA_REFLECTED_ELEMENT_ATTRIBUTES: tuple[tuple[str, str, bool], ...] = (
    ("ariaActiveDescendantElement", "aria-activedescendant", False),
    ("ariaControlsElements", "aria-controls", True),
    ("ariaDescribedByElements", "aria-describedby", True),
    ("ariaDetailsElements", "aria-details", True),
    ("ariaErrorMessageElements", "aria-errormessage", True),
    ("ariaFlowToElements", "aria-flowto", True),
    ("ariaLabelledByElements", "aria-labelledby", True),
    ("ariaOwnsElements", "aria-owns", True),
)


class CustomStateSet:
    """Set-like storage for custom element states."""

    def __init__(self, states: Iterable[str] | None = None) -> None:
        self._states: list[str] = []
        for state in states or ():
            self.add(state)

    @property
    def size(self) -> int:
        return len(self._states)

    def add(self, state: str) -> "CustomStateSet":
        state = self._state_name(state)
        if state not in self._states:
            self._states.append(state)
        return self

    def clear(self) -> None:
        self._states.clear()

    def delete(self, state: str) -> bool:
        state = self._state_name(state)
        if state not in self._states:
            return False
        self._states.remove(state)
        return True

    def entries(self) -> Iterator[tuple[str, str]]:
        for state in self._states:
            yield state, state

    def forEach(
        self,
        callback: Callable[[str, str, "CustomStateSet"], Any],
        thisArg: Any = None,
    ) -> None:
        for state in list(self._states):
            callback(state, state, self)

    def has(self, state: str) -> bool:
        return self._state_name(state) in self._states

    def keys(self) -> Iterator[str]:
        return iter(self._states)

    def values(self) -> Iterator[str]:
        return iter(self._states)

    def __contains__(self, state: object) -> bool:
        return isinstance(state, str) and self.has(state)

    def __iter__(self) -> Iterator[str]:
        return self.values()

    def __len__(self) -> int:
        return self.size

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._states!r})"

    @staticmethod
    def _state_name(state: str) -> str:
        state = str(state).strip()
        if not state:
            raise ValueError("custom state names cannot be empty")
        return state


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

    def forEach(
        self, func: Callable[[Node, int, "NodeList"], Any], thisArg: Any = None
    ) -> None:
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


class _LiveNodeList(NodeList):
    """List-like live view over a node's current children."""

    def __init__(
        self, owner: Node, predicate: Callable[[Any], bool] | None = None
    ) -> None:
        self._owner = owner
        self._predicate = predicate
        super().__init__()

    def _nodes(self) -> list[Any]:
        nodes = list(getattr(self._owner, "args", ()))
        if self._predicate is not None:
            nodes = [node for node in nodes if self._predicate(node)]
        return nodes

    @property
    def length(self) -> int:
        return len(self._nodes())

    def __len__(self) -> int:
        return self.length

    def __iter__(self) -> Iterator[Any]:
        return iter(self._nodes())

    def __reversed__(self) -> Iterator[Any]:
        return reversed(self._nodes())

    def __getitem__(self, index):
        return self._nodes()[index]

    def __contains__(self, item: Any) -> bool:
        return item in self._nodes()

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, _LiveNodeList):
            other = other._nodes()
        return self._nodes() == list(other) if isinstance(other, IterableABC) else False

    def __repr__(self) -> str:
        return repr(self._nodes())

    def append(self, item: Any) -> None:
        self._owner.appendChild(item)

    def extend(self, items: Iterable[Any]) -> None:
        for item in items:
            self.append(item)

    def insert(self, index: int, item: Any) -> None:  # type: ignore[override]
        nodes = self._nodes()
        if index < 0:
            index = max(0, len(nodes) + index)
        if index >= len(nodes):
            self.append(item)
            return
        self._owner.insertBefore(item, nodes[index])

    def _remove_direct_child(self, item: Any) -> Any:
        if isinstance(item, Node):
            removed = self._owner.removeChild(item)
            if removed is not None:
                return removed
        siblings = list(getattr(self._owner, "args", ()))
        for index, child in enumerate(siblings):
            if child is item or child == item:
                removed = siblings.pop(index)
                self._owner.args = tuple(siblings)
                _notify_slot_change(self._owner)
                return removed
        raise ValueError("node is not in list")

    def remove(self, item: Any) -> None:
        if item not in self._nodes():
            raise ValueError("node is not in list")
        self._remove_direct_child(item)

    def pop(self, index: int = -1) -> Any:  # type: ignore[override]
        node = self._nodes()[index]
        return self._remove_direct_child(node)

    def clear(self) -> None:
        for node in list(self._nodes()):
            self._remove_direct_child(node)

    def __delitem__(self, index) -> None:
        nodes = self._nodes()[index]
        if isinstance(index, slice):
            for node in list(nodes):
                self._remove_direct_child(node)
            return
        self._remove_direct_child(nodes)

    def __setitem__(self, index, item: Any) -> None:
        if isinstance(index, slice):
            old_nodes = self._nodes()[index]
            new_nodes = list(item)
            if old_nodes:
                reference = old_nodes[0]
                for node in new_nodes:
                    self._owner.insertBefore(node, reference)
                for node in list(old_nodes):
                    self._remove_direct_child(node)
                return
            self.extend(new_nodes)
            return
        self._owner.replaceChild(item, self._nodes()[index])


class RadioNodeList(NodeList):
    """A live collection of form controls sharing an id or name."""

    def __init__(
        self,
        nodes: Iterable[Node] | str | None = None,
        name: str | None = None,
        owner=None,
    ) -> None:
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
                if control.getAttribute("id") == self.name
                or control.getAttribute("name") == self.name
            ]
        return list(list.__iter__(self))

    @property
    def length(self) -> int:
        return len(self._nodes())

    def __iter__(self) -> Iterator[Node]:
        return iter(self._nodes())

    def __getitem__(self, index: int) -> Node:  # type: ignore[override]
        return self._nodes()[index]

    def __len__(self) -> int:
        return self.length

    @property
    def value(self) -> Any:
        """Returns the value of the first element in the collection,
        or null if there are no elements in the collection."""
        for node in self._nodes():
            if (
                isinstance(node, HTMLInputElement)
                and (node.getAttribute("type") or "").lower() == "radio"
                and node.checked
            ):
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
            if (
                isinstance(node, HTMLInputElement)
                and (node.getAttribute("type") or "").lower() == "radio"
            ):
                node.checked = node is matching_radio


class Element(Node):
    """Baseclass for all html tags"""

    # __slots__ = ('_id')

    def __init__(self, *args, **kwargs):
        # Attribute-backed properties (id / title / class) are resolved lazily
        # through __getattr__; ``self.kwargs`` is not populated until
        # ``Node.__init__`` runs below, so there is nothing to reflect here.
        self.lang = None
        self.tabIndex = None
        self.style = None  # Style(self)  # = #'test'#Style()
        self.shadowRoot = None
        self.dir = None
        super().__init__(*args, **kwargs)

    @property
    def childElementCount(self) -> int:
        """Returns the number of child elements an element has."""
        return len(self.children)

    @property
    def children(self) -> list[Node]:
        """Returns child elements, excluding text, comments, and strings."""
        return _LiveNodeList(self, lambda child: isinstance(child, Element))

    def _find_element_by_id(self, _id: str) -> Element | None:
        if self.getAttribute("id") == _id:
            return self
        for child in self.childNodes:
            if not isinstance(child, Element):
                continue
            match = child._find_element_by_id(_id)
            if match is not None:
                return match
        return None

    def _getElementById(self, _id: str) -> Element | None:
        """Compatibility wrapper for older internal callers."""
        return self._find_element_by_id(_id)

    def _getElementByAttrVal(self, attr: str, val: str):
        # Recursion keeps this in sync with live tree mutations.
        if self.getAttribute(attr) == val:
            return self
        for child in self.childNodes:
            get_by_attr = getattr(child, "_getElementByAttrVal", None)
            if not callable(get_by_attr):
                continue
            match = get_by_attr(attr, val)
            if match:
                return match
        return None

    @staticmethod
    def _read_simple_selector_token(selector: str, start: int) -> tuple[str, int]:
        end = start
        while end < len(selector) and selector[end] not in ".#[":
            end += 1
        return selector[start:end], end

    @staticmethod
    def _find_selector_bracket(selector: str, start: int) -> int:
        quote = None
        for index in range(start + 1, len(selector)):
            char = selector[index]
            if quote is not None:
                if char == quote:
                    quote = None
                continue
            if char in ("'", '"'):
                quote = char
                continue
            if char == "]":
                return index
        return -1

    @staticmethod
    def _strip_selector_quotes(value: str) -> str:
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            return value[1:-1]
        return value

    @staticmethod
    def _parse_simple_selector(query: str):
        selector = query.strip()
        if not selector:
            return None

        parsed: dict[str, Any] = {
            "tag": "*", "id": None, "classes": [], "attributes": [], "pseudos": []
        }
        position = 0
        # a type selector stops at the first '.', '#', '[' or ':' -- ':' in that
        # position is always a pseudo-class, never part of the tag name
        tag_match = re.match(r"^(\*|[A-Za-z_][\w-]*)", selector)
        if tag_match:
            parsed["tag"] = tag_match.group(1)
            position = tag_match.end()
        elif selector[0] not in ".#[:":
            return None

        while position < len(selector):
            char = selector[position]
            if char == "#":
                token, position = Element._read_simple_selector_token(
                    selector, position + 1
                )
                if not token:
                    return None
                parsed["id"] = token
                continue
            if char == ".":
                token, position = Element._read_simple_selector_token(
                    selector, position + 1
                )
                if not token:
                    return None
                parsed["classes"].append(token)
                continue
            if char == "[":
                end = Element._find_selector_bracket(selector, position)
                if end == -1:
                    return None
                content = selector[position + 1 : end]
                attribute = re.match(
                    r"^\s*([^\s~|^$*=\]]+)\s*(?:(~=|\|=|\^=|\$=|\*=|=)\s*(.*?)\s*)?$",
                    content,
                )
                if not attribute:
                    return None
                parsed["attributes"].append(
                    (
                        attribute.group(1),
                        attribute.group(2) or "",
                        Element._strip_selector_quotes(attribute.group(3) or ""),
                    )
                )
                position = end + 1
                continue
            if char == ":":
                # Only a small set of self-contained structural pseudo-classes
                # is understood here; anything else (``:hover``, ``:nth-child``,
                # pseudo-elements, ...) fails the parse so the caller falls back
                # to the full selector engine.
                pseudo_match = re.match(
                    r"::?([-\w]+)", selector[position:]
                )
                if not pseudo_match:
                    return None
                pseudo_name = pseudo_match.group(1).lower()
                if pseudo_name not in Element._STRUCTURAL_PSEUDO_CLASSES:
                    return None
                parsed["pseudos"].append(pseudo_name)
                position += pseudo_match.end()
                continue
            return None

        return parsed

    _STRUCTURAL_PSEUDO_CLASSES = frozenset({
        "root", "empty",
        "first-child", "last-child", "only-child",
        "first-of-type", "last-of-type", "only-of-type",
    })

    @staticmethod
    def _matches_structural_pseudo(element, pseudo: str) -> bool:
        parent = getattr(element, "parentNode", None)
        parent_is_element = (
            parent is not None
            and getattr(parent, "nodeType", None) == Node.ELEMENT_NODE
        )

        if pseudo == "root":
            # the root element of the document (``<html>`` in HTML): an element
            # whose parent is the document, or a detached tree's top element
            return not parent_is_element

        if pseudo == "empty":
            for child in element.__dict__.get("args", ()):
                if getattr(child, "nodeType", None) == Node.ELEMENT_NODE:
                    return False
                if isinstance(child, str) and str(child).strip():
                    return False
                if (
                    getattr(child, "nodeType", None) == Node.TEXT_NODE
                    and str(getattr(child, "textContent", "") or "").strip()
                ):
                    return False
            return True

        siblings = (
            [
                c
                for c in parent.__dict__.get("args", ())
                if getattr(c, "nodeType", None) == Node.ELEMENT_NODE
            ]
            if parent_is_element
            else [element]
        )
        if pseudo == "first-child":
            return bool(siblings) and siblings[0] is element
        if pseudo == "last-child":
            return bool(siblings) and siblings[-1] is element
        if pseudo == "only-child":
            return len(siblings) == 1 and siblings[0] is element

        same_type = [
            s for s in siblings if getattr(s, "tagName", None) == element.tagName
        ]
        if pseudo == "first-of-type":
            return bool(same_type) and same_type[0] is element
        if pseudo == "last-of-type":
            return bool(same_type) and same_type[-1] is element
        if pseudo == "only-of-type":
            return len(same_type) == 1 and same_type[0] is element
        return False

    @staticmethod
    def _attribute_selector_matches(attr_value, operator: str, value: str) -> bool:
        if attr_value is None:
            return False
        attr_value = str(attr_value)
        if operator == "":
            return True
        if operator == "=":
            return attr_value == value
        if operator == "~=":
            return value in attr_value.split()
        if operator == "|=":
            return attr_value == value or attr_value.startswith(value + "-")
        if operator == "^=":
            return attr_value.startswith(value)
        if operator == "$=":
            return attr_value.endswith(value)
        if operator == "*=":
            return value in attr_value
        return False

    def _matchElement(self, element, query):
        """
        Matches an element against a simple selector.

        This intentionally handles the single-selector subset used by
        ``matches()``, ``getElementsByTagName()``, and the legacy selector
        fallback: tag, id, classes, and CSS attribute operators.
        """
        if not isinstance(element, Element):
            return False

        parsed = Element._parse_simple_selector(query)
        if parsed is None:
            return False

        tag_name = parsed["tag"]
        if tag_name != "*" and element.tagName.lower() != tag_name.lower():
            return False
        if parsed["id"] is not None and element.getAttribute("id") != parsed["id"]:
            return False

        class_tokens = set(str(element.getAttribute("class") or "").split())
        if not set(parsed["classes"]).issubset(class_tokens):
            return False

        for attr, operator, value in parsed["attributes"]:
            if not Element._attribute_selector_matches(
                element.getAttribute(attr), operator, value
            ):
                return False

        for pseudo in parsed.get("pseudos", ()):
            if not Element._matches_structural_pseudo(element, pseudo):
                return False
        return True

    def matches(self, s: str) -> bool:
        """[checks to see if the Element would be selected by the provided selectorString]

        https://developer.mozilla.org/en-US/docs/Web/API/Element/matches

        Args:
            s (str): [css selector]

        Returns:
            [bool]: [True if selector maches Element otherwise False]
        """
        selectors = [
            selector.strip() for selector in str(s).split(",") if selector.strip()
        ]
        for selector in selectors:
            if self._matchElement(self, selector):
                return True
            # combinator selectors: match right-to-left up the ancestor / sibling
            # chain without running a document-wide query.
            result = self._matches_selector_chain(selector)
            if result is True:
                return True
            if result is None:  # the fast matcher could not parse it
                root = (
                    self.ownerDocument
                    if self.ownerDocument is not None
                    else self.rootNode
                )
                if hasattr(root, "querySelectorAll"):
                    try:
                        if any(m is self for m in root.querySelectorAll(selector)):
                            return True
                    except Exception:
                        return False
        return False

    def _matches_selector_chain(self, selector: str):
        """``True`` / ``False`` if a combinator selector matches this element,
        or ``None`` if the selector is too complex for the fast matcher."""
        try:
            from domonic.bs4 import (
                _split_simple_selector_chain,
                _strip_simple_pseudo,
                _match_parsed_selector,
                _match_simple_pseudo,
                _element_children,
            )
        except Exception:
            return None
        parts = _split_simple_selector_chain(selector)
        if not parts or len(parts) == 1:
            return None
        parsed = []
        for combinator, simple in parts:
            stripped = _strip_simple_pseudo(simple)
            if stripped is None:
                return None
            simple_sel, pseudo = stripped
            compound = Element._parse_simple_selector(simple_sel)
            if compound is None:
                return None
            parsed.append((combinator, compound, pseudo))

        cache: dict = {}

        def matches_compound(el, compound, pseudo):
            return (
                isinstance(el, Element)
                and _match_parsed_selector(el, compound)
                and _match_simple_pseudo(el, pseudo, cache)
            )

        _, compound, pseudo = parsed[-1]
        if not matches_compound(self, compound, pseudo):
            return False
        current = [self]
        # walking left: the combinator joining parsed[i-1] to parsed[i] is
        # stored on parsed[i].
        for i in range(len(parsed) - 1, 0, -1):
            combinator = parsed[i][0]
            _, compound, pseudo = parsed[i - 1]
            next_current = []
            for el in current:
                if combinator == ">":
                    candidates = [getattr(el, "parentNode", None)]
                elif combinator == "+":
                    prev = getattr(el, "previousElementSibling", None)
                    candidates = [prev]
                elif combinator == "~":
                    candidates = []
                    sib = getattr(el, "previousElementSibling", None)
                    while sib is not None:
                        candidates.append(sib)
                        sib = getattr(sib, "previousElementSibling", None)
                else:  # descendant
                    candidates = []
                    ancestor = getattr(el, "parentNode", None)
                    while ancestor is not None and isinstance(ancestor, Element):
                        candidates.append(ancestor)
                        ancestor = getattr(ancestor, "parentNode", None)
                for candidate in candidates:
                    if candidate is not None and matches_compound(
                        candidate, compound, pseudo
                    ):
                        next_current.append(candidate)
            if not next_current:
                return False
            current = next_current
        return True

    # https://developer.mozilla.org/en-US/docs/Web/API/Element/closest
    def closest(self, s: str):
        el: Any = self
        while el is not None and getattr(el, "nodeType", None) == Node.ELEMENT_NODE:
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
        - Preserved as a compatibility helper for older selector-style code.
        - Supports simple descendant selector chains plus tag, id, class, and attribute selectors.

        Args:
            all_selectors (str): The CSS selectors to query.
            document (object): The document object to search within.

        Returns:
            list: A list of elements matching the CSS selectors.
        """

        if not all_selectors:
            return []

        selected = []
        selectors = [
            selector.strip()
            for selector in str(all_selectors).split(",")
            if selector.strip()
        ]
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
                if con is None or not hasattr(con, "getElementsByTagName"):
                    continue
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
            parsed = self._parse_simple_selector(element)
            if parsed is None:
                return []
            found = getElements(context, parsed["tag"])
            # Contexts can overlap (e.g. nested ``<table>`` elements both in
            # scope), so the same descendant can be collected more than once.
            seen_ids: set[int] = set()
            context = []
            for fnd in found:
                marker = id(fnd)
                if marker in seen_ids:
                    continue
                seen_ids.add(marker)
                if self._matchElement(fnd, element):
                    context.append(fnd)

        selected.extend(context)
        return selected

    def append(self, *args):
        """Inserts a set of Node objects or DOMString objects after the last child of the Element."""
        items = _coerce_insertion_nodes(*args)
        old_documents = [(item, _detach_node_for_insertion(item)) for item in items]
        previous_sibling = self.args[-1] if len(self.args) else None
        # Assign via __dict__ to skip the ``args`` __setattr__ hook: it would
        # re-parent the *entire* existing child list on every call (O(n) per
        # append -> O(n^2) for a loop), and this method already links the new
        # nodes below.
        self.__dict__["args"] = self.args + items
        for item, old_document in old_documents:
            _connect_inserted_node(self, item, old_document)
            if isinstance(item, Node):
                item._update_parents()
        added_nodes = [item for item in items if isinstance(item, Node)]
        if added_nodes:
            _queue_mutation_record(
                "childList",
                self,
                added_nodes=added_nodes,
                previous_sibling=previous_sibling,
            )
        _notify_slot_change(self)
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
        """Return this element's content as an HTML-fragment-serialised string.

        Matches a browser's ``innerHTML`` getter (WHATWG fragment serialisation:
        ``<br>`` not ``<br/>``, ``checked=""`` not bare ``checked``, only
        ``& " \\xa0`` escaped in attribute values). ``str(node)`` keeps
        domonic's XHTML-style authoring output.
        """
        return _serialize_html_fragment(self)

    @innerHTML.setter
    def innerHTML(self, value):
        if value is not None:
            self.replaceChildren(*self._parse_html_fragment(value))
        return self.content

    @property
    def outerHTML(self):
        """Return this element serialised per the HTML fragment algorithm.

        Browser-compatible counterpart to ``str(self)`` -- see ``innerHTML``.
        """
        out: list[str] = []
        _serialize_fragment_element(self, out)
        return "".join(out)

    @outerHTML.setter
    def outerHTML(self, value):
        if self.parentNode is None:
            return self
        replacement = DocumentFragment(*self._parse_html_fragment(value))
        self.parentNode.replaceChild(replacement, self)
        return self

    def getHTML(self, options: Any = None) -> str:
        """DOM ``Element.getHTML()`` -- serialised inner HTML.

        ``options`` is accepted for signature compatibility; shadow-root
        serialisation is not implemented.
        """
        return _serialize_html_fragment(self)

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
            if parsed is None:
                return [value]
            wrapper = _find_wrapper_div(parsed)
            if wrapper is None:
                return [value]
            return list(wrapper.args)
        except Exception:
            return [value]

    def setHTML(self, input: Any, options: Any = None):
        """Replace children with sanitized HTML.

        Mirrors the browser ``Element.setHTML()`` method. It always applies
        unsafe-element and unsafe-attribute removal before inserting the
        resulting fragment.
        """
        from domonic.webapi.sanitizer import sanitize_html_fragment

        fragment = sanitize_html_fragment(input, options, safe=True)
        self.replaceChildren(*fragment.args)
        return self

    def setHTMLUnsafe(self, input: Any, options: Any = None):
        """Replace children from HTML, optionally using a Sanitizer config."""
        from domonic.webapi.sanitizer import sanitize_html_fragment

        fragment = sanitize_html_fragment(input, options, safe=False)
        self.replaceChildren(*fragment.args)
        return self

    def blur(self):
        """Removes focus from an element"""
        from domonic.events import FocusEvent

        doc = self.ownerDocument if isinstance(self.ownerDocument, Document) else None
        self._focused = False
        related_target = None
        if doc is not None and getattr(doc, "_activeElement", None) is self:
            doc._activeElement = None
            related_target = getattr(doc, "body", None)
        result = self.dispatchEvent(
            FocusEvent(
                "blur",
                {
                    "bubbles": False,
                    "cancelable": False,
                    "relatedTarget": related_target,
                },
            )
        )
        self.dispatchEvent(
            FocusEvent(
                "focusout",
                {"bubbles": True, "cancelable": False, "relatedTarget": related_target},
            )
        )
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
        view = (
            getattr(self.ownerDocument, "defaultView", None)
            if isinstance(self.ownerDocument, Document)
            else None
        )
        evt = MouseEvent(
            "click", {"bubbles": True, "cancelable": True, "view": view, "detail": 1}
        )
        return self.dispatchEvent(evt)

    def animate(
        self, keyframes: list[dict[str, Any]] | dict[str, Any], options: Any = None
    ):
        from domonic.animation import Animation, KeyframeEffect

        owner_document = (
            self.ownerDocument
            if isinstance(self.ownerDocument, Document)
            else globals().get("document")
        )
        timeline = (
            owner_document.timeline if isinstance(owner_document, Document) else None
        )
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

    @property
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
                current.dispatchEvent(
                    FocusEvent(
                        "blur",
                        {"bubbles": False, "cancelable": False, "relatedTarget": self},
                    )
                )
                current.dispatchEvent(
                    FocusEvent(
                        "focusout",
                        {"bubbles": True, "cancelable": False, "relatedTarget": self},
                    )
                )
            doc._activeElement = self
        self._focused = True
        result = self.dispatchEvent(
            FocusEvent(
                "focus",
                {"bubbles": False, "cancelable": False, "relatedTarget": previous},
            )
        )
        self.dispatchEvent(
            FocusEvent(
                "focusin",
                {"bubbles": True, "cancelable": False, "relatedTarget": previous},
            )
        )
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

    def _attr_key(self, attribute: str) -> str:
        """The internal ``kwargs`` key for ``attribute``.

        Attribute names on elements in an HTML document are ASCII-lower-cased,
        so ``getAttribute`` / ``setAttribute`` are case-insensitive there;
        SVG / MathML keep their case (``viewBox`` etc.).
        """
        name = attribute[1:] if attribute[:1] == "_" else attribute
        if getattr(self, "namespaceURI", "") == "http://www.w3.org/1999/xhtml":
            name = name.lower()
        return "_" + name

    def getAttributeNames(self) -> list[str]:
        """The qualified names of this element's attributes, in order."""
        return [k[1:] if k[:1] == "_" else k for k in self.kwargs]

    def getAttribute(self, attribute: str) -> str:
        """Returns the specified attribute value of an element node"""
        try:
            return self.kwargs[self._attr_key(attribute)]
        except KeyError:
            return None  # type: ignore[return-value]

    def getAttributeNode(self, attribute: str) -> "Attr | None":
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

    # -- SVG geometry (SVGGraphicsElement / SVGTextContentElement) ---------
    def getBBox(self) -> "DOMRect":
        """The tight geometry box of this element in its own user space.

        Works for any SVG-namespaced element or SVG-named tag: leaf shapes use
        their attributes, ``<text>`` / ``<tspan>`` are measured with the bundled
        font metrics (via the computed ``font-size`` / ``font-weight``), and
        containers such as ``<g>`` return the union of their rendered
        descendants with each child's ``transform`` applied.
        """
        if not _svg_is_geometry_element(self):
            return DOMRect()
        return _svg_bbox(self)

    def getComputedTextLength(self) -> float:
        """Advance width of this text element's content, in user units."""
        text = _svg_text_content(self)
        size, bold, _root = _svg_resolve_font(self)
        return _fontmetrics.advance_width(text, size, bold)

    def getSubStringLength(self, charnum: int = 0, nchars: int | None = None) -> float:
        text = _svg_text_content(self)
        end = len(text) if nchars is None else charnum + nchars
        size, bold, _root = _svg_resolve_font(self)
        return _fontmetrics.advance_width(text[charnum:end], size, bold)

    def getNumberOfChars(self) -> int:
        return len(_svg_text_content(self))

    def getCTM(self) -> "DOMMatrix":
        """Transform from this element's user space to its nearest viewport."""
        return _svg_ctm(self, to_screen=False)

    def getScreenCTM(self) -> "DOMMatrix":
        """Transform from this element's user space to the document root."""
        return _svg_ctm(self, to_screen=True)

    def getTransformToElement(self, element: "Element") -> "DOMMatrix":
        return DOMMatrix.fromMatrix(element.getScreenCTM()).inverse().multiply(
            self.getScreenCTM()
        )

    def createSVGPoint(self, x: float = 0.0, y: float = 0.0) -> "DOMPoint":
        return DOMPoint(x, y)

    def createSVGRect(self) -> "DOMRect":
        return DOMRect()

    def createSVGMatrix(self) -> "DOMMatrix":
        return DOMMatrix()

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
            if el is self:
                return
            if not isinstance(el, Element):
                return
            class_tokens = set(str(el.getAttribute("class") or "").split())
            if required.issubset(class_tokens):
                elements.append(el)

        self._iterate(self, anon)
        return elements

    def getElementById(self, _id: str) -> Element | None:
        """Returns the descendant element whose id matches the supplied value."""
        for child in self.childNodes:
            if not isinstance(child, Element):
                continue
            match = child._find_element_by_id(_id)
            if match is not None:
                return match
        return None

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
        tagName = str(tagName)

        if tagName == "*":

            def anon(el):
                if el is not self and isinstance(el, Element):
                    elements.append(el)

            self._iterate(self, anon)
            return elements

        if re.match(r"^[A-Za-z_][\w:-]*$", tagName):
            wanted = tagName.lower()

            def anon(el):
                if (
                    el is not self
                    and isinstance(el, Element)
                    and el.tagName.lower() == wanted
                ):
                    elements.append(el)

            self._iterate(self, anon)
            return elements

        def _collect(el):
            if el is self:
                return
            if self._matchElement(el, tagName):
                elements.append(el)

        self._iterate(self, anon)
        return elements

    def __contains__(self, item: Any) -> bool:
        """``x in element``.

        Keeps the ``Node`` behaviour (child membership) but also answers ``True``
        for the ``on<type>`` event-handler IDL property names, matching a
        browser's ``'onclick' in element`` feature-detection probe, and for
        attributes actually set on the element.
        """
        if isinstance(item, str):
            if item.lower() in EVENT_HANDLER_NAMES:
                return True
            if item in self.kwargs or ("_" + item) in self.kwargs:
                return True
        return super().__contains__(item)

    def hasAttribute(self, attribute: str) -> bool:
        """Returns True if an element has the specified attribute, otherwise False

        Args:
            attribute (str): [the attribute to test for]

        Returns:
            bool: [True if an element has the specified attribute, otherwise False]
        """
        try:
            return self._attr_key(attribute) in self.kwargs
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
        old_documents = [(node, _detach_node_for_insertion(node)) for node in nodes]
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
        old_documents = [(node, _detach_node_for_insertion(node)) for node in nodes]
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

    @property
    def lang(self) -> str | None:
        """Sets or returns the value of the lang attribute of an element."""
        return self.getAttribute("lang")

    @lang.setter
    def lang(self, value: str) -> None:
        self.setAttribute("lang", value)

    @property
    def lastElementChild(self) -> Node | None:
        """[Returns the last child element of an element]

        Returns:
            [type]: [the last child element of an element]
        """
        for child in reversed(self.args):
            if isinstance(child, Element):
                return child
        return None

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

    def normalize(self) -> tuple[Any, ...]:
        """Joins adjacent text nodes and removes empty text nodes in an element"""
        content: list[Any] = []
        nodestr = ""
        removed_nodes: list[Node] = []
        for s in self.args:
            if type(s) == Text:
                nodestr += s.textContent
                removed_nodes.append(s)
                continue
            elif type(s) == str:
                nodestr += s
                continue
            if nodestr != "":
                content.append(nodestr)
                nodestr = ""
            if isinstance(s, Element):
                s.normalize()
            content.append(s)
        if nodestr != "":
            content.append(nodestr)
        for node in removed_nodes:
            _disconnect_tree(node)
            node.parentNode = None
        self.args = tuple(content)
        self._update_parents()
        if removed_nodes:
            _queue_mutation_record("childList", self, removed_nodes=removed_nodes)
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
        old_documents = [(item, _detach_node_for_insertion(item)) for item in items]
        next_sibling = (
            self.args[0] if len(self.args) and isinstance(self.args[0], Node) else None
        )
        self.__dict__["args"] = items + tuple(self.args)
        for item, old_document in old_documents:
            _connect_inserted_node(self, item, old_document)
        added_nodes = [item for item in items if isinstance(item, Node)]
        if added_nodes:
            _queue_mutation_record(
                "childList", self, added_nodes=added_nodes, next_sibling=next_sibling
            )
        _notify_slot_change(self)

    def replaceChildren(self, *nodes: Any) -> None:
        """Replaces the element's children with the supplied nodes."""
        items = _coerce_replacement_nodes(*nodes)
        removed_nodes = [node for node in self.args if isinstance(node, Node)]
        for node in removed_nodes:
            _disconnect_tree(node)
            node.parentNode = None
        old_documents = [(item, _detach_node_for_insertion(item)) for item in items]
        self.__dict__["args"] = items
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

    def querySelector(self, query: str) -> Element | None:
        """[Returns the first child element that matches a specified CSS selector(s) of an element]

        Args:
            query (str): [a CSS selector string]

        Returns:
            [type]: [an Element object]
        """
        if not query:
            return None
        query = query.strip()
        if re.match(r"^#[\w-]+$", query):
            return self.getElementById(query[1:])

        class_match = re.match(r"^\.[\w-]+(?:\.[\w-]+)*$", query)
        tag_match = re.match(r"^(\*|[A-Za-z][\w-]*)$", query)
        # Only a single compound selector (no descendant/child/sibling step) is
        # safe for the in-line stack walk below; with a combinator present
        # ``_parse_simple_selector`` mis-parses (e.g. it folds the space in
        # ``div#x a`` into the id), so route those through querySelectorAll.
        simple_selector = None
        if not re.search(r"[\s>+~]", re.sub(r"\[[^\]]*\]", "", query)):
            simple_selector = Element._parse_simple_selector(query)
        if class_match or tag_match or simple_selector is not None:
            required_classes = None
            wanted_tag = None
            if class_match:
                required_classes = set(query.split(".")[1:])
            elif tag_match:
                wanted_tag = None if query == "*" else query.lower()

            stack = list(reversed(self.__dict__.get("args", ()) or ()))
            while stack:
                node = stack.pop()
                if isinstance(node, Element):
                    if required_classes is not None:
                        class_tokens = set(
                            str(node.getAttribute("class") or "").split()
                        )
                        if required_classes.issubset(class_tokens):
                            return node
                    elif wanted_tag is not None:
                        if node.tagName.lower() == wanted_tag:
                            return node
                    elif wanted_tag is None and tag_match:
                        return node
                    elif self._matchElement(node, query):
                        return node
                    stack.extend(reversed(node.__dict__.get("args", ()) or ()))
                elif isinstance(node, Node):
                    stack.extend(reversed(node.__dict__.get("args", ()) or ()))
            return None

        try:
            return self.querySelectorAll(query)[0]
        except IndexError:
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

        # The native CSS engine shared with BeautifulSlop resolves descendant /
        # child combinators, classes, attribute selectors and simple pseudos
        # several times faster than the cssselect -> XPath -> elementpath path.
        # It returns ``None`` for selectors it does not support (``+``, ``~``,
        # complex pseudo-classes), which then fall through to the XPath engine.
        try:
            from domonic.bs4 import _select_fast

            fast_matches = _select_fast(self, query)
        except Exception:
            fast_matches = None
        if fast_matches is not None:
            return fast_matches

        def _fallback_selector_results():
            if query.startswith("."):
                return list(self.getElementsByClassName(" ".join(query.split(".")[1:])))
            if query.startswith("#"):
                found = self.getElementById(query[1:])
                return [found] if found else []
            results = self.getElementsBySelector(query, self)
            return results if isinstance(results, list) else []

        naked_query = query[1:]
        # ``_select_fast`` already handled the common selectors above; anything
        # with a class, attribute, combinator or pseudo-class that reached here
        # needs the cssselect -> XPath engine, not the plain ``_matchElement``
        # walk (which silently ignores pseudo-classes and returns nothing).
        if (
            "." in naked_query
            or "[" in query
            or " " in naked_query
            or ":" in query
            or ">" in query
            or "+" in query
            or "~" in query
        ):
            try:
                from cssselect import HTMLTranslator, SelectorError

                expression = HTMLTranslator().css_to_xpath(query)
                from domonic.webapi.xpath import XPathEvaluator, XPathResult

                evaluator = XPathEvaluator()
                expression = evaluator.createExpression(expression)
                result = expression.evaluate(
                    self, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE
                )
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
        #     pass
        # if self.parentNode is None:
        # self._update_parents()
        if self.parentNode is not None:
            self.parentNode.removeChild(self)
        return self

    def removeAttribute(self, attribute: str):
        """Removes a specified attribute from an element"""
        attribute = self._attr_key(attribute)
        if attribute not in self.kwargs:
            return None
        old_value = self.kwargs.get(attribute)
        del self.kwargs[attribute]
        _notify_attribute_changed(self, attribute, old_value, None)
        if attribute == "_style":
            self._sync_style_declaration("")
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
        return max(
            self.clientHeight, getattr(self, "_scroll_height", self.clientHeight)
        )

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
        attribute = self._attr_key(attribute)
        try:
            kwargs = object.__getattribute__(self, "kwargs")
        except AttributeError:
            return None
        old_value = kwargs.get(attribute)
        kwargs[attribute] = value
        _notify_attribute_changed(self, attribute, old_value, value)
        if attribute == "_style":
            self._sync_style_declaration("" if value is None else str(value))
        _queue_mutation_record(
            "attributes",
            self,
            attribute_name=(attribute[1:] if attribute.startswith("_") else attribute),
            old_value=str(old_value) if old_value is not None else None,
        )

    def _sync_style_declaration(self, css_text: str) -> None:
        """Push a ``style`` content-attribute change into the live
        ``CSSStyleDeclaration`` (so clearing / replacing the attribute clears
        the declaration, per the DOM)."""
        existing = getattr(self, "_Element__style", None)
        if existing is None or getattr(self, "_syncing_style_attr", False):
            return
        object.__setattr__(self, "_syncing_style_attr", True)
        try:
            existing.cssText = css_text
        finally:
            object.__setattr__(self, "_syncing_style_attr", False)

    def toggleAttribute(self, attribute: str, force: bool | None = None) -> bool:
        """Adds or removes an attribute and returns whether it is present afterwards."""
        should_add = (
            bool(force) if force is not None else not self.hasAttribute(attribute)
        )
        if should_add:
            self.setAttribute(attribute, "")
            return True
        self.removeAttribute(attribute)
        return False

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

    @property
    def attributeStyleMap(self):
        """CSS Typed OM view over the inline ``style`` declaration block."""
        from domonic.style import StylePropertyMap

        return StylePropertyMap(self.style)

    def computedStyleMap(self):
        """CSS Typed OM read-only view over the element's computed style."""
        from domonic.style import ComputedStyleDeclaration, StylePropertyMap

        return StylePropertyMap(
            ComputedStyleDeclaration(self), read_only=True
        )

    @style.setter
    def style(self, style):
        if style is None:
            self.__style = None
            return

        if isinstance(style, Style):
            self.__style = style
            object.__setattr__(self.__style, "_parent_node", self)
            if self.__style.cssText:
                self.setAttribute("style", self.__style.cssText)
            elif self.getAttribute("style"):
                self.__style.cssText = self.getAttribute("style")
            return

        self.__style = Style(self)
        self.__style.cssText = style

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


def _aria_attribute_property(attribute: str) -> property:
    def getter(self):
        return self.getAttribute(attribute)

    def setter(self, value):
        self.setAttribute(attribute, value)

    def deleter(self):
        self.removeAttribute(attribute)

    return property(getter, setter, deleter, f"Reflects the {attribute} attribute.")


def _element_idrefs(element: "Element") -> str:
    if not isinstance(element, Element):
        return str(element)
    element_id = element.id
    if element_id is None:
        raise ValueError("ARIA element references must have an id")
    return element_id


def _resolve_idrefs(context: "Element", attribute: str) -> list["Element"]:
    value = context.getAttribute(attribute)
    if not value:
        return []
    root = context.getRootNode({"composed": True})
    resolver = getattr(root, "getElementById", None)
    if resolver is None:
        return []
    found = []
    for element_id in str(value).split():
        element = resolver(element_id)
        if isinstance(element, Element):
            found.append(element)
    return found


def _aria_element_reference_property(attribute: str, multiple: bool) -> property:
    def getter(self):
        elements = _resolve_idrefs(self, attribute)
        return elements if multiple else elements[0] if elements else None

    def setter(self, value):
        if value is None:
            self.removeAttribute(attribute)
            return
        if multiple:
            values = (
                [value]
                if isinstance(value, (str, Element))
                else list(value) if isinstance(value, IterableABC) else [value]
            )
            idrefs = " ".join(_element_idrefs(item) for item in values)
            self.setAttribute(attribute, idrefs)
            return
        self.setAttribute(attribute, _element_idrefs(value))

    def deleter(self):
        self.removeAttribute(attribute)

    return property(getter, setter, deleter, f"Reflects the {attribute} ID reference.")


for _property_name, _attribute_name in _ARIA_REFLECTED_ATTRIBUTES:
    setattr(Element, _property_name, _aria_attribute_property(_attribute_name))

for _property_name, _attribute_name, _is_multiple in _ARIA_REFLECTED_ELEMENT_ATTRIBUTES:
    setattr(
        Element,
        _property_name,
        _aria_element_reference_property(_attribute_name, _is_multiple),
    )


class DOMImplementation:
    def __init__(self):
        self._features = {}

    def createDocument(self, namespaceURI: str, qualifiedName: str, doctype: str):
        if namespaceURI is None:
            namespaceURI = ""
        if qualifiedName is None:
            qualifiedName = ""
        d = XMLDocument()
        root = d.createElementNS(namespaceURI, qualifiedName) if qualifiedName else None
        if root is not None:
            d.args = (root,)
            root.parentNode = d
            d.documentElement = root
        d.doctype = doctype
        return d

    def createDocumentType(
        self, qualifiedName: str, publicId: str, systemId: str
    ) -> DocumentType:
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

    def hasFeature(self, feature=None, version=None) -> bool:
        """Return whether a DOM feature is supported.

        Modern DOM implementations keep this method for compatibility and
        report support for all feature strings.
        """
        return True


class ProcessingInstruction(Node):

    nodeType: int = Node.PROCESSING_INSTRUCTION_NODE
    __slots__ = ("target", "data")

    def __init__(self, target, data) -> None:
        super().__init__()
        self.target = target
        self.data = data

    @property
    def nodeValue(self) -> str:
        return self.data

    @nodeValue.setter
    def nodeValue(self, value: Any) -> None:
        self.data = "" if value is None else str(value)

    textContent = nodeValue

    def toString(self) -> str:
        return f"<?{self.target} {self.data}?>"

    __str__ = toString

    def stream(self) -> Iterator[str]:
        yield self.toString()


class Comment(Node):

    nodeType: int = Node.COMMENT_NODE
    nodeName: str = "#comment"
    __slots__ = "data"

    def __init__(self, *data) -> None:
        self.data = "".join(str(part) for part in data)
        super().__init__()

    @property
    def nodeValue(self) -> str:
        return self.data

    @nodeValue.setter
    def nodeValue(self, value: Any) -> None:
        self.data = "" if value is None else str(value)

    textContent = nodeValue

    def toString(self) -> str:
        return f"<!--{self.data}-->"

    __str__ = toString

    def stream(self) -> Iterator[str]:
        yield self.toString()

    def __format__(self, format_spec):
        return str(self)

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

    @property
    def nodeValue(self) -> str:
        return self.data

    @nodeValue.setter
    def nodeValue(self, value: Any) -> None:
        self.data = "" if value is None else str(value)

    textContent = nodeValue

    def toString(self) -> str:
        return f"<![CDATA[{self.data}]]>"

    __str__ = toString

    def stream(self) -> Iterator[str]:
        yield self.toString()

    def __len__(self) -> int:
        return len(self.data)

    @property
    def length(self) -> int:
        return len(self.data)

    # def __format__(self, format_spec):
    #     return str(self)


def _range_parent(node: "Node") -> "Node":
    """The parent of a range boundary reference node, or raise if detached."""
    parent = node.parentNode
    if parent is None:
        raise ValueError("the reference node has no parent")
    return parent


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
        if (
            not isinstance(self.startContainer, Text)
            or self.startContainer is not self.endContainer
        ):
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
        parent = _range_parent(refNode)
        self.setEnd(parent, list(parent.childNodes).index(refNode) + 1)

    def setEndBefore(self, refNode: "Node") -> None:
        parent = _range_parent(refNode)
        self.setEnd(parent, list(parent.childNodes).index(refNode))

    def setStart(self, refNode: "Node", offset: int) -> None:
        self.startContainer = refNode
        self.startOffset = offset
        if self.endContainer is None:
            self.endContainer = refNode
            self.endOffset = offset
        self._update_state()

    def setStartAfter(self, refNode: "Node") -> None:
        parent = _range_parent(refNode)
        self.setStart(parent, list(parent.childNodes).index(refNode) + 1)

    def setStartBefore(self, refNode: "Node") -> None:
        parent = _range_parent(refNode)
        self.setStart(parent, list(parent.childNodes).index(refNode))

    def surroundContents(self, newParent: "Node") -> None:
        self.cloneRange().surroundContents(newParent)

    def toString(self) -> str:
        return self.cloneRange().toString()

    def comparePoint(self, refNode: "Node", offset: int) -> int:
        return self.cloneRange().comparePoint(refNode, offset)

    def deleteData(self, offset, count):
        if (
            not isinstance(self.startContainer, Text)
            or self.startContainer is not self.endContainer
        ):
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
        if (
            not isinstance(self.startContainer, Text)
            or self.startContainer is not self.endContainer
        ):
            raise ValueError("Range data helpers require a single Text container")
        return self.startContainer.textContent[offset : offset + count]

    def getEnd(self):
        return (self.endContainer, self.endOffset)

    def getStart(self):
        return (self.startContainer, self.startOffset)

    def replaceData(self, offset, count, data):
        if (
            not isinstance(self.startContainer, Text)
            or self.startContainer is not self.endContainer
        ):
            raise ValueError("Range data helpers require a single Text container")
        self.startContainer.replaceData(offset, count, data)
        self.endOffset = min(
            len(self.startContainer.textContent), max(self.startOffset, self.endOffset)
        )
        self._update_state()
        return self.startContainer.textContent

    def setData(self, data):
        if (
            not isinstance(self.startContainer, Text)
            or self.startContainer is not self.endContainer
        ):
            raise ValueError("Range data helpers require a single Text container")
        self.startContainer.data = data
        self.startOffset = min(self.startOffset, len(data))
        self.endOffset = min(self.endOffset, len(data))
        self._update_state()
        return self.startContainer.textContent

    def _update_state(self) -> None:
        self.collapsed = (
            self.startContainer is self.endContainer
            and self.startOffset == self.endOffset
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
    def _compare_points(
        node_a: Node, offset_a: int, node_b: Node, offset_b: int
    ) -> int:
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
            self.startContainer is self.endContainer
            and self.startOffset == self.endOffset
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

        def resolve_index(
            node: Node | None, offset: int, *, is_end: bool
        ) -> int | None:
            if node is None:
                return None
            if node is ancestor:
                bounded = max(0, min(offset, len(children)))
                return bounded

            current: Any = node
            while (
                current is not None
                and getattr(current, "parentNode", None) is not ancestor
            ):
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
        elif (
            self._compare_points(node, offset, self.startContainer, self.startOffset)
            < 0
        ):
            self.startContainer = node
            self.startOffset = offset
        self._update_state()

    def setStartBefore(self, node: Node) -> None:
        parent = _range_parent(node)
        self.setStart(parent, list(parent.childNodes).index(node))

    def setStartAfter(self, node: Node) -> None:
        parent = _range_parent(node)
        self.setStart(parent, list(parent.childNodes).index(node) + 1)

    def setEndBefore(self, node: Node) -> None:
        parent = _range_parent(node)
        self.setEnd(parent, list(parent.childNodes).index(node))

    def setEndAfter(self, node: Node) -> None:
        parent = _range_parent(node)
        self.setEnd(parent, list(parent.childNodes).index(node) + 1)

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
            self.START_TO_START: (
                self.startContainer,
                self.startOffset,
                sourceRange.startContainer,
                sourceRange.startOffset,
            ),
            self.START_TO_END: (
                self.startContainer,
                self.startOffset,
                sourceRange.endContainer,
                sourceRange.endOffset,
            ),
            self.END_TO_END: (
                self.endContainer,
                self.endOffset,
                sourceRange.endContainer,
                sourceRange.endOffset,
            ),
            self.END_TO_START: (
                self.endContainer,
                self.endOffset,
                sourceRange.startContainer,
                sourceRange.startOffset,
            ),
        }
        if how not in comparisons:
            raise ValueError("Invalid Range comparison type")
        return self._compare_points(*comparisons[how])  # type: ignore[arg-type]

    def deleteContents(self) -> None:
        self.extractContents()

    def extractContents(self) -> "DocumentFragment":
        if self.startContainer is None:
            return DocumentFragment()
        if (
            isinstance(self.startContainer, Text)
            and self.startContainer == self.endContainer
        ):
            text = self.startContainer.textContent
            extracted: Any = text[self.startOffset : self.endOffset]
            self.startContainer.textContent = (
                text[: self.startOffset] + text[self.endOffset :]
            )
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
        if (
            isinstance(self.startContainer, Text)
            and self.startContainer == self.endContainer
        ):
            return DocumentFragment(
                Text(self.startContainer.textContent[self.startOffset : self.endOffset])
            )
        if self.startContainer == self.endContainer:
            container = self.startContainer
            children = list(container.childNodes)
            cloned = [
                copy.deepcopy(child)
                for child in children[self.startOffset : self.endOffset]
            ]
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
        if (
            isinstance(self.startContainer, Text)
            and self.startContainer == self.endContainer
        ):
            parent = getattr(self.startContainer, "parentNode", None)
            return (
                DOMRectList([parent.getBoundingClientRect()])
                if parent is not None and hasattr(parent, "getBoundingClientRect")
                else DOMRectList()
            )
        if self.startContainer == self.endContainer:
            rects = []
            for child in list(self.startContainer.childNodes)[
                self.startOffset : self.endOffset
            ]:
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
            replacement = (
                [
                    part
                    for part in (before, node, after)
                    if part.textContent != ""
                    if isinstance(part, Text)
                ]
                if False
                else None
            )
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
            ref = (
                children[self.startOffset] if self.startOffset < len(children) else None
            )
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
            return DocumentFragment(fragment)
        return DocumentFragment(fragment)

    def toString(self) -> str:
        if self.startContainer is None:
            return ""
        if (
            isinstance(self.startContainer, Text)
            and self.startContainer == self.endContainer
        ):
            return self.startContainer.textContent[self.startOffset : self.endOffset]
        if self.startContainer == self.endContainer:
            container = self.startContainer
            children = list(container.childNodes)
            return "".join(
                str(child) for child in children[self.startOffset : self.endOffset]
            )
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
        if (
            self._compare_points(refNode, offset, self.startContainer, self.startOffset)
            < 0
        ):
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
            self._compare_points(
                end_node, end_offset, self.startContainer, self.startOffset
            )
            <= 0
            or self._compare_points(
                start_node, start_offset, self.endContainer, self.endOffset
            )
            >= 0
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
        self._fonts = None
        self._lastModified = formatdate(time.time(), usegmt=True)
        self._referrer = ""
        self._timeline = None
        self.stylesheets = None
        self.adoptedStyleSheets: list = []
        self.doctype = None
        super().__init__(*args, **kwargs)
        try:
            global document
            document = self
        except Exception as exc:
            warnings.warn(f"failed to set document: {exc}", RuntimeWarning)

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.__init__(*args, **kwargs)
        instance.documentElement = instance
        instance.URL = ""
        instance.baseURI = ""
        try:
            global document
            document = instance
        except Exception as exc:
            warnings.warn(f"failed to set document: {exc}", RuntimeWarning)
        return instance

    def _document_base_uri(self) -> str:
        for base_element in self.getElementsByTagName("base"):
            href = base_element.getAttribute("href")
            if href is not None:
                return href
        return getattr(self, "URL", "") or ""

    # @property
    def _get_tags(self, tag):
        """returns the tags you want"""
        return [str(element) for element in self.getElementsByTagName(tag)]

        # def activeElement():
        """ Returns the currently focused element in the document"""
        # return

    @property
    def fonts(self):
        """The document's CSS Font Loading API ``FontFaceSet``."""
        if self._fonts is None:
            from domonic.webapi.cssfontloading import FontFaceSet

            self._fonts = FontFaceSet()
        return self._fonts

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
    def styleSheets(self):
        """DOM-spec spelling of :attr:`stylesheets`."""
        return self.stylesheets

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
                "The new body element is of type '"
                + str(type(el))
                + "'. It must be a 'HTMLBodyElement'",
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
        pairs = []
        for name, value in self._cookie_store.items():
            if isinstance(value, dict):
                value = value.get("value", "")
            pairs.append(f"{name}={value}")
        return "; ".join(pairs)

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
    def parseHTML(input: Any, options: Any = None) -> "Document":
        """Parse HTML into an ``HTMLDocument`` using safe Sanitizer defaults."""
        from domonic.webapi.sanitizer import parse_html_document

        return parse_html_document(input, options, safe=True)

    @staticmethod
    def parseHTMLUnsafe(input: Any, options: Any = None) -> "Document":
        """Parse HTML into an ``HTMLDocument``, optionally using a Sanitizer."""
        from domonic.webapi.sanitizer import parse_html_document

        return parse_html_document(input, options, safe=False)

    @staticmethod
    def createExpression(xpath: str, nsResolver: Any) -> XPathExpression:
        """Creates an XPathExpression object for the given XPath string."""
        return XPathExpression(xpath, nsResolver)

    @staticmethod
    def createElement(_type: str, *args: Any, **kwargs: Any) -> "Element":
        """Creates an Element node.

        The DOM ``createElement(tagName, options)`` form is supported for
        customized built-ins: pass ``{"is": "my-button"}`` as a trailing
        positional dict, or ``is_=`` / ``**{"is": ...}`` as a keyword.
        """
        from domonic.html import create_element

        if args and isinstance(args[-1], dict) and "is" in args[-1]:
            *_args, options = args
            args = tuple(_args)
            kwargs.setdefault("is", options["is"])
        is_value = kwargs.pop("is", None) or kwargs.pop("is_", None)
        if is_value is not None:
            kwargs["_is"] = is_value

        el = create_element(_type, *args, **kwargs)
        if isinstance(el, Element):
            _upgrade_custom_element_instance(el)
        return el

    @staticmethod
    def createElementNS(
        namespaceURI: str, qualifiedName: str, options: Any = None
    ) -> "Element":
        """Creates an element with the specified namespace URI and qualified name."""
        # el = type(qualifiedName, (Element,), {'name': qualifiedName})
        from domonic.html import create_element

        local_name = str(qualifiedName).split(":", 1)[-1]
        if namespaceURI == MATHML_NAMESPACE:
            element_type = type(local_name, (MathMLElement,), {"name": local_name})
            el = element_type()
        elif namespaceURI == SVG_NAMESPACE:
            from domonic.svg import create_element as create_svg_element

            el = create_svg_element(local_name)
        else:
            el = create_element(qualifiedName)  # , *args, **kwargs)
            el.namespaceURI = namespaceURI
        _upgrade_custom_element_instance(el)
        # el["name"] = qualifiedName
        return el

    @staticmethod
    def createEvent(event_type: str | None = None) -> Event:
        """Creates a DOM-style event instance for the requested interface.

        Args:
            event_type: Event interface name, such as ``MouseEvent`` or
                ``SubmitEvent``. Defaults to a plain ``Event``.

        Returns:
            Event: A new event object.
        """
        from domonic.events import (
            AnimationEvent,
            BeforeUnloadEvent,
            BlobEvent,
            ClipboardEvent,
            CloseEvent,
            CommandEvent,
            CompositionEvent,
            CustomEvent,
            DeviceLightEvent,
            DeviceMotionEvent,
            DeviceOrientationEvent,
            DeviceProximityEvent,
            DOMContentLoadedEvent,
            DragEvent,
            ErrorEvent,
            ExtendableEvent,
            FetchEvent,
            FocusEvent,
            FormDataEvent,
            GamePadEvent,
            HashChangeEvent,
            InputEvent,
            KeyboardEvent,
            MessageEvent,
            PageTransitionEvent,
            PointerEvent,
            PopStateEvent,
            ProgressEvent,
            SecurityPolicyViolationEvent,
            StorageEvent,
            SubmitEvent,
            SVGEvent,
            SyncEvent,
            TimerEvent,
            ToggleEvent,
            TrackEvent,
            TransitionEvent,
            UIEvent,
            WebGLContextEvent,
            WheelEvent,
        )

        if event_type is None:
            return Event()
        factories: dict[str, Callable[[], Event]] = {
            "AnimationEvent": lambda: AnimationEvent("animationstart"),
            "BeforeUnloadEvent": lambda: BeforeUnloadEvent("beforeunload"),
            "BlobEvent": lambda: BlobEvent("dataavailable"),
            "ClipboardEvent": lambda: ClipboardEvent("copy"),
            "CloseEvent": lambda: CloseEvent("close"),
            "CommandEvent": lambda: CommandEvent("command"),
            "CompositionEvent": lambda: CompositionEvent("compositionstart"),
            "CustomEvent": lambda: CustomEvent("custom"),
            "DeviceLightEvent": lambda: DeviceLightEvent("devicelight"),
            "DeviceMotionEvent": lambda: DeviceMotionEvent("devicemotion"),
            "DeviceOrientationEvent": lambda: DeviceOrientationEvent(
                "deviceorientation"
            ),
            "DeviceProximityEvent": lambda: DeviceProximityEvent("deviceproximity"),
            "DOMContentLoadedEvent": lambda: DOMContentLoadedEvent("DOMContentLoaded"),
            "DragEvent": lambda: DragEvent("drag"),
            "ErrorEvent": lambda: ErrorEvent("error"),
            "Event": lambda: Event(),
            "ExtendableEvent": lambda: ExtendableEvent("extendable"),
            "FetchEvent": lambda: FetchEvent("fetch"),
            "FocusEvent": lambda: FocusEvent("focus"),
            "FormDataEvent": lambda: FormDataEvent("formdata"),
            "GamePadEvent": lambda: GamePadEvent("gamepadconnected"),
            "HashChangeEvent": lambda: HashChangeEvent("hashchange"),
            "InputEvent": lambda: InputEvent("input"),
            "KeyboardEvent": lambda: KeyboardEvent("keydown"),
            "MessageEvent": lambda: MessageEvent("message"),
            "MouseEvent": lambda: MouseEvent("click"),
            "PageTransitionEvent": lambda: PageTransitionEvent("pageshow"),
            "PointerEvent": lambda: PointerEvent("pointerdown"),
            "PopStateEvent": lambda: PopStateEvent("popstate"),
            "ProgressEvent": lambda: ProgressEvent("progress"),
            "SecurityPolicyViolationEvent": lambda: SecurityPolicyViolationEvent(
                "securitypolicyviolation"
            ),
            "StorageEvent": lambda: StorageEvent("storage"),
            "SubmitEvent": lambda: SubmitEvent("submit"),
            "SVGEvent": lambda: SVGEvent("load"),
            "SyncEvent": lambda: SyncEvent("sync"),
            "TimerEvent": lambda: TimerEvent("timer"),
            "ToggleEvent": lambda: ToggleEvent("toggle"),
            "TrackEvent": lambda: TrackEvent("addtrack"),
            "TransitionEvent": lambda: TransitionEvent("transitionend"),
            "UIEvent": lambda: UIEvent("load"),
            "WebGLContextEvent": lambda: WebGLContextEvent("webglcontextlost"),
            "WheelEvent": lambda: WheelEvent("wheel"),
        }
        factory = factories.get(event_type)
        if factory is not None:
            return factory()
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
        root: Node,
        whatToShow: int | None = None,
        filter: Any = None,
        entityReferenceExpansion: Any = None,
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

    def _create_entity(
        self,
        name: str,
        publicId: str | None = None,
        systemId: str | None = None,
        notationName: str | None = None,
    ) -> "Entity":
        """Create an Entity node for the Expat DTD parser."""
        node = Entity(name, publicId, systemId, notationName)
        node.ownerDocument = self
        return node

    def _create_notation(
        self, name: str, publicId: str | None = None, systemId: str | None = None
    ) -> "Notation":
        """Create a Notation node for the Expat DTD parser."""
        node = Notation(name, publicId, systemId)
        node.ownerDocument = self
        return node

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
    def createNodeIterator(
        root: Node, whatToShow: int | None = None, filter: Any = None
    ) -> NodeIterator:
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
        doctype = getattr(self, "_doctype", None)
        if doctype is not None:
            return doctype
        if getattr(self, "contentType", None) == "text/html":
            return DocumentType("html", "", "")
        return None

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
        contextNode: "Node | None" = None,
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
        result = expression.evaluate(
            contextNode, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE
        )
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
            match = each._find_element_by_id(_id)
            if match is not None:
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
    def head(self) -> "HTMLHeadElement | None":
        """Returns the <head> element of the document"""
        return self.querySelector("head")  # type: ignore[return-value]

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
        if isinstance(node, (Element, DocumentFragment)):
            cloned = copy.deepcopy(node)
            if not deep:
                cloned.args = ()
            return _prepare_detached_clone(
                cloned,
                self,
                old_document,
                run_adopted=True,
                upgrade_custom_elements=True,
            )
        elif isinstance(node, Comment):
            cloned = Comment(node.data)
        elif isinstance(node, Text):
            cloned = Text(node.data)
        elif isinstance(node, ProcessingInstruction):
            cloned = ProcessingInstruction(node.target, node.data)
        elif isinstance(node, Attr):
            return Attr(node.name, node.value)
        else:
            raise Exception("Unsupported node type")
        cloned._ownerDocument = self
        cloned.isConnected = False
        return cloned

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
        anchors = [
            node
            for node in self.getElementsByTagName("a")
            if node.getAttribute("href") is not None
        ]
        areas = [
            node
            for node in self.getElementsByTagName("area")
            if node.getAttribute("href") is not None
        ]
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
        title_el = self.querySelector("title")
        if title_el is not None:
            return title_el.textContent
        return ""

    @title.setter
    def title(self, value: str):
        """[Sets the title of the document]

        Args:
            value ([str]): [the new title of the document]
        """
        title_el = self.querySelector("title")
        if title_el is not None:
            title_el.textContent = value
        else:
            head_el = self.head
            if head_el is None:
                head_el = HTMLHeadElement()
                self.head = head_el
            head_el.appendChild(HTMLTitleElement(value))

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
        self.__init__(content)  # type: ignore[misc]
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
    def __init__(self, url: str | None = None, *args, **kwargs) -> None:
        self.href = url

    def __str__(self) -> str:
        return self.href or ""

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

    @property
    def children(self) -> NodeList:
        return _LiveNodeList(self, lambda child: isinstance(child, Element))

    @property
    def childElementCount(self) -> int:
        return self.children.length

    querySelector = Document.querySelector
    querySelectorAll = Document.querySelectorAll
    getElementById = Document.getElementById
    getElementsByTagName = Document.getElementsByTagName
    _matchElement = Document._matchElement
    attributes = Element.attributes

    def append(self, *nodes: Any) -> None:
        """Appends nodes or strings to the DocumentFragment."""
        items = _coerce_insertion_nodes(*nodes)
        old_documents = [(item, _detach_node_for_insertion(item)) for item in items]
        self.__dict__["args"] = self.args + items
        for item, old_document in old_documents:
            _connect_inserted_node(self, item, old_document)

    def prepend(self, *nodes: Any) -> None:
        """Prepends nodes or strings to the DocumentFragment."""
        items = _coerce_insertion_nodes(*nodes)
        old_documents = [(item, _detach_node_for_insertion(item)) for item in items]
        self.__dict__["args"] = items + self.args
        for item, old_document in old_documents:
            _connect_inserted_node(self, item, old_document)

    def replaceChildren(self, *newChildren: Any) -> None:
        """Replaces the childNodes of the DocumentFragment object."""
        for child in self.args:
            if isinstance(child, Node):
                _disconnect_tree(child)
                child.parentNode = None

        items = _coerce_replacement_nodes(*newChildren)
        old_documents = [(item, _detach_node_for_insertion(item)) for item in items]
        self.__dict__["args"] = items
        for item, old_document in old_documents:
            _connect_inserted_node(self, item, old_document)

    def __format__(self, format_spec):
        return self.__str__()

    def __str__(self) -> str:
        return "".join(self.stream())

    def stream(self) -> Iterator[str]:
        for child in self.args:
            yield from self._stream_value(child)


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

    @property
    def nodeValue(self) -> str:
        return self.data

    @nodeValue.setter
    def nodeValue(self, content: Any) -> None:
        self.data = "" if content is None else str(content)

    @property
    def textContent(self) -> str:
        return self.data

    @textContent.setter
    def textContent(self, content: Any) -> None:
        self.data = "" if content is None else str(content)

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
        from the CharacterData.data string; when this method returns, data contains the shortened DOMString.
        """
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
        return "".join(self.stream())

    def stream(self) -> Iterator[str]:
        for child in self.args:
            yield from self._stream_value(child)

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
    """A DTD entity declaration."""

    nodeType = Node.ENTITY_NODE
    nodeValue = None
    actualEncoding = None
    encoding = None
    version = None

    def __init__(
        self,
        name: str = "",
        publicId: str | None = None,
        systemId: str | None = None,
        notationName: str | None = None,
    ) -> None:
        self.name = name
        self.publicId = publicId or ""
        self.systemId = systemId or ""
        self.notationName = notationName
        super().__init__()

    @property
    def nodeName(self) -> str:
        """The entity name."""
        return self.name

    def __str__(self) -> str:
        return "".join(self.stream())

    def stream(self) -> Iterator[str]:
        for child in self.args:
            yield from self._stream_value(child)

    @staticmethod
    def fromName(entityName: str) -> str:
        """Returns the entity name corresponding to the given character."""
        return chr(ord(entityName))

    @staticmethod
    def fromChar(char: str) -> str:
        """Returns the character corresponding to the given entity name."""
        return chr(ord(char))


class Notation(Node):
    """A DTD notation declaration."""

    nodeType = Node.NOTATION_NODE
    nodeValue = None

    def __init__(
        self,
        name: str = "",
        publicId: str | None = None,
        systemId: str | None = None,
    ) -> None:
        self.name = name
        self.publicId = publicId or ""
        self.systemId = systemId or ""
        super().__init__()

    @property
    def nodeName(self) -> str:
        """The notation name."""
        return self.name

    def __str__(self) -> str:
        return self.name

    def stream(self) -> Iterator[str]:
        yield self.name


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
        The first node is returned, while the second node is discarded and exists outside the tree.
        """
        self._validate_data_range(offset)
        current = self.args[0]
        head = current[:offset]
        tail = current[offset:]
        self.args = (head,)
        sibling = Text(tail)
        if self.parentNode is not None and hasattr(self.parentNode, "args"):
            siblings = list(self.parentNode.args)
            try:
                index = siblings.index(self)
                sibling.parentNode = self.parentNode
                siblings.insert(index + 1, sibling)
                self.parentNode.args = tuple(siblings)
                self.parentNode._update_parents()
            except ValueError:
                sibling.parentNode = None
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
        value = str(self.textContent)
        escape_text = DOMConfig.GLOBAL_AUTOESCAPE or bool(
            getattr(self, "_escape_text_on_render", False)
        )
        return _escape_html(value) if escape_text else value

    def __format__(self, format_spec):
        return str(self)

    def stream(self) -> Iterator[str]:
        value = str(self.textContent)
        escape_text = DOMConfig.GLOBAL_AUTOESCAPE or bool(
            getattr(self, "_escape_text_on_render", False)
        )
        yield _escape_html(value) if escape_text else value

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
            item_id = (
                item.getAttribute("id")
                if hasattr(item, "getAttribute")
                else getattr(item, "id", None)
            )
            item_name = (
                item.getAttribute("name")
                if hasattr(item, "getAttribute")
                else getattr(item, "name", None)
            )
            if item_id == name:
                return item
            elif item_name == name:
                return item
        return None

    def __getitem__(self, index: int | str):  # type: ignore[override]
        if isinstance(index, str):
            direct = self.namedItem(index)
            if direct is not None:
                return direct
            names = index.split(".")
            current = self.namedItem(names[0])
            for name in names[1:]:
                if current is None:
                    return None
                if hasattr(current, "namedItem"):
                    current = current.namedItem(name)
                elif hasattr(current, name):
                    current = getattr(current, name)
                else:
                    return None
            return current
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
                if (
                    attribute_filter is not None
                    and record.attributeName not in attribute_filter
                ):
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
                old_value = (
                    record.oldValue if options["characterDataOldValue"] else None
                )
                filtered_record = MutationRecord(
                    "characterData", record.target, oldValue=old_value
                )
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

    def _process(
        self,
        changed_target: Node | None = None,
        target_rect: DOMRectReadOnly | None = None,
    ) -> None:
        for target, previous in list(self._observations.items()):
            rect = (
                DOMRect.fromRect(target_rect)
                if target is changed_target and target_rect is not None
                else DOMRect.fromRect(target.getBoundingClientRect())
            )
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
        self.isIntersecting = (
            self.intersectionRect.width > 0 and self.intersectionRect.height > 0
        )
        target_area = self.boundingClientRect.width * self.boundingClientRect.height
        intersection_area = self.intersectionRect.width * self.intersectionRect.height
        self.intersectionRatio = (
            0.0 if target_area == 0 else intersection_area / target_area
        )


IntersectionObserverCallback = Callable[
    [list["IntersectionObserverEntry"], "IntersectionObserver"], Any
]


class IntersectionObserver:
    """Observe whether elements intersect a root rectangle or viewport-like area.

    Domonic models intersections using element bounding boxes and a root
    rectangle, which is enough for practical DOM-side visibility checks and
    tests.
    """

    _all_observers: ClassVar[list["IntersectionObserver"]] = []

    def __init__(
        self,
        callback: IntersectionObserverCallback,
        options: dict[str, Any] | None = None,
    ) -> None:
        if not callable(callback):
            raise TypeError("IntersectionObserver callback must be callable")
        self.callback = callback
        self.root = (options or {}).get("root")
        threshold = (options or {}).get("threshold", 0.0)
        self.thresholds = sorted(
            threshold if isinstance(threshold, list) else [threshold]
        )
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

    def _process(
        self,
        changed_target: Node | None = None,
        target_rect: DOMRectReadOnly | None = None,
    ) -> None:
        now_ms = time.perf_counter() * 1000.0
        for target, previous in list(self._observations.items()):
            bounding_rect = (
                DOMRect.fromRect(target_rect)
                if target is changed_target and target_rect is not None
                else DOMRect.fromRect(target.getBoundingClientRect())
            )
            if isinstance(self.root, Element):
                root_rect = DOMRect.fromRect(self.root.getBoundingClientRect())
            else:
                root_rect = DOMRect.fromRect(
                    _default_intersection_root_rect(target, bounding_rect)
                )
            intersection_rect = _intersect_rects(root_rect, bounding_rect)
            entry = IntersectionObserverEntry(
                target, root_rect, bounding_rect, intersection_rect, now_ms
            )
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
    def __init__(
        self, name: str, entryType: str, startTime: float, duration: float
    ) -> None:
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


PerformanceObserverCallback = Callable[
    [list["PerformanceEntry"], "PerformanceObserver"], Any
]


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
                self._flush()
                return
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
        self.message: str = message or ""
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


def _format_matrix_number(value: float) -> str:
    """Serialise a matrix component the way a browser does -- an integer with no
    decimal point, otherwise a trimmed decimal."""
    rounded = round(value, 6)
    if rounded == int(rounded):
        return str(int(rounded))
    return f"{rounded:.6f}".rstrip("0").rstrip(".")


class DOMMatrixReadOnly:
    """Read-only 4x4 transformation matrix for DOM geometry APIs.

    Supports the common 2D aliases as well as the full 4x4 member set used by
    transforms, points, and animation/geometry helpers.
    """

    # m11..m44 are installed as ``property`` objects by the loop after this
    # class body (and given setters on ``DOMMatrix``); declare them so callers
    # and the 2D aliases below type-check.
    m11: float; m12: float; m13: float; m14: float
    m21: float; m22: float; m23: float; m24: float
    m31: float; m32: float; m33: float; m34: float
    m41: float; m42: float; m43: float; m44: float

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
                values.append(
                    getattr(matrix, f"m{row}{col}", 1.0 if row == col else 0.0)
                )
        return DOMMatrixReadOnly(*values)

    def __init__(self, *values: float) -> None:
        if not values:
            values = (
                1.0,
                0.0,
                0.0,
                0.0,
                0.0,
                1.0,
                0.0,
                0.0,
                0.0,
                0.0,
                1.0,
                0.0,
                0.0,
                0.0,
                0.0,
                1.0,
            )
        if len(values) == 6:
            a, b, c, d, e, f = values
            values = (
                a,
                b,
                0.0,
                0.0,
                c,
                d,
                0.0,
                0.0,
                0.0,
                0.0,
                1.0,
                0.0,
                e,
                f,
                0.0,
                1.0,
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
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
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
        data = {
            f"m{row}{col}": self._get(row, col)
            for row in range(1, 5)
            for col in range(1, 5)
        }
        data.update({"is2D": self.is2D, "isIdentity": self.isIdentity})
        return data

    def multiply(self, other: Any) -> "DOMMatrix":
        return DOMMatrix.fromMatrix(self).multiplySelf(other)

    def translate(self, tx: float = 0, ty: float = 0, tz: float = 0) -> "DOMMatrix":
        return DOMMatrix.fromMatrix(self).translateSelf(tx, ty, tz)

    def scale(
        self, scaleX: float = 1, scaleY: float | None = None, scaleZ: float = 1
    ) -> "DOMMatrix":
        return DOMMatrix.fromMatrix(self).scaleSelf(scaleX, scaleY, scaleZ)

    def inverse(self) -> "DOMMatrix":
        return DOMMatrix.fromMatrix(self).invertSelf()

    def rotate(
        self, rotX: float = 0, rotY: float | None = None, rotZ: float | None = None
    ) -> "DOMMatrix":
        return DOMMatrix.fromMatrix(self).rotateSelf(rotX, rotY, rotZ)

    def skewX(self, sx: float = 0) -> "DOMMatrix":
        return DOMMatrix.fromMatrix(self).skewXSelf(sx)

    def skewY(self, sy: float = 0) -> "DOMMatrix":
        return DOMMatrix.fromMatrix(self).skewYSelf(sy)

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
            property(lambda self, r=_row, c=_col: self._get(r, c)),  # type: ignore[misc]
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

    @property
    def a(self) -> float:
        return self.m11

    @a.setter
    def a(self, value: float) -> None:
        self.m11 = value

    @property
    def b(self) -> float:
        return self.m12

    @b.setter
    def b(self, value: float) -> None:
        self.m12 = value

    @property
    def c(self) -> float:
        return self.m21

    @c.setter
    def c(self, value: float) -> None:
        self.m21 = value

    @property
    def d(self) -> float:
        return self.m22

    @d.setter
    def d(self, value: float) -> None:
        self.m22 = value

    @property
    def e(self) -> float:
        return self.m41

    @e.setter
    def e(self, value: float) -> None:
        self.m41 = value

    @property
    def f(self) -> float:
        return self.m42

    @f.setter
    def f(self, value: float) -> None:
        self.m42 = value

    def multiplySelf(self, other: Any) -> "DOMMatrix":
        other_matrix = DOMMatrixReadOnly.fromMatrix(other)
        left = self._values
        right = other_matrix._values
        result = [0.0] * 16
        for row in range(4):
            for col in range(4):
                result[row * 4 + col] = sum(
                    left[row * 4 + k] * right[k * 4 + col] for k in range(4)
                )
        self._values = result
        return self

    def translateSelf(self, tx: float = 0, ty: float = 0, tz: float = 0) -> "DOMMatrix":
        translation = DOMMatrix(
            1,
            0,
            0,
            0,
            0,
            1,
            0,
            0,
            0,
            0,
            1,
            0,
            tx,
            ty,
            tz,
            1,
        )
        return self.multiplySelf(translation)

    def scaleSelf(
        self, scaleX: float = 1, scaleY: float | None = None, scaleZ: float = 1
    ) -> "DOMMatrix":
        if scaleY is None:
            scaleY = scaleX
        scale = DOMMatrix(
            scaleX,
            0,
            0,
            0,
            0,
            scaleY,
            0,
            0,
            0,
            0,
            scaleZ,
            0,
            0,
            0,
            0,
            1,
        )
        return self.multiplySelf(scale)

    def rotateSelf(
        self, rotX: float = 0, rotY: float | None = None, rotZ: float | None = None
    ) -> "DOMMatrix":
        # 1-arg form is a rotation about the Z axis (the common CSS ``rotate()``)
        if rotY is None and rotZ is None:
            rotZ, rotX = rotX, 0.0
        rotY = rotY or 0.0
        rotZ = rotZ or 0.0
        for angle, build in (
            (rotX, lambda c, s: DOMMatrix(1, 0, 0, 0, 0, c, s, 0, 0, -s, c, 0, 0, 0, 0, 1)),
            (rotY, lambda c, s: DOMMatrix(c, 0, -s, 0, 0, 1, 0, 0, s, 0, c, 0, 0, 0, 0, 1)),
            (rotZ, lambda c, s: DOMMatrix(c, s, 0, 0, -s, c, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1)),
        ):
            if angle:
                rad = math.radians(angle)
                self.multiplySelf(build(math.cos(rad), math.sin(rad)))
        return self

    def rotateFromVectorSelf(self, x: float = 0, y: float = 0) -> "DOMMatrix":
        angle = math.degrees(math.atan2(y, x)) if (x or y) else 0.0
        return self.rotateSelf(angle)

    def skewXSelf(self, sx: float = 0) -> "DOMMatrix":
        return self.multiplySelf(
            DOMMatrix(1, 0, math.tan(math.radians(sx)), 1, 0, 0)
        )

    def skewYSelf(self, sy: float = 0) -> "DOMMatrix":
        return self.multiplySelf(
            DOMMatrix(1, math.tan(math.radians(sy)), 0, 1, 0, 0)
        )

    def toString(self) -> str:
        if self.is2D:
            parts = [self.a, self.b, self.c, self.d, self.e, self.f]
            return "matrix(" + ", ".join(_format_matrix_number(v) for v in parts) + ")"
        return (
            "matrix3d("
            + ", ".join(_format_matrix_number(v) for v in self._values)
            + ")"
        )

    def __str__(self) -> str:
        return self.toString()

    def invertSelf(self) -> "DOMMatrix":
        matrix = [[self._values[row * 4 + col] for col in range(4)] for row in range(4)]
        identity = [
            [1.0 if row == col else 0.0 for col in range(4)] for row in range(4)
        ]
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
                matrix[row] = [
                    current - factor * pivot_value
                    for current, pivot_value in zip(matrix[row], matrix[col])
                ]
                identity[row] = [
                    current - factor * pivot_value
                    for current, pivot_value in zip(identity[row], identity[col])
                ]
        self._values = [identity[row][col] for row in range(4) for col in range(4)]
        return self


for _row in range(1, 5):
    for _col in range(1, 5):
        readonly_prop = getattr(DOMMatrixReadOnly, f"m{_row}{_col}")
        setattr(
            DOMMatrix,
            f"m{_row}{_col}",
            readonly_prop.setter(
                lambda self, value, r=_row, c=_col: self._set(r, c, value)
            ),
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
        return DOMQuad(
            DOMPointReadOnly(quad.p1.x, quad.p1.y),
            DOMPointReadOnly(quad.p2.x, quad.p2.y),
            DOMPointReadOnly(quad.p3.x, quad.p3.y),
            DOMPointReadOnly(quad.p4.x, quad.p4.y),
        )

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


def _coerce_what_to_show(whatToShow: int | str | None) -> int:
    try:
        return int(0 if whatToShow is None else whatToShow) & 0xFFFFFFFF
    except (TypeError, ValueError) as exc:
        raise TypeError("whatToShow must be an integer bitmask") from exc


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
        self.whatToShow = _coerce_what_to_show(whatToShow)
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
        return None

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


mapChild = {
    "first": "firstChild",
    "last": "lastChild",
    "next": "firstChild",
    "previous": "lastChild",
}

mapSibling = {"next": "nextSibling", "previous": "previousSibling"}

# toString = mapChild.toString

# def _is(x, _type):
#     return mapChild[x].toLowerCase() == '[object ' + _type.toLowerCase() + ']'


def nodeFilter(tw: NodeIterator | TreeWalker, node: Node) -> int:
    # Maps nodeType to whatToShow
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
    node = getattr(tw.currentNode, mapChild[_type])
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
            sibling = getattr(
                node, mapSibling["next" if _type == "first" else "previous"]
            )
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
        node = node.parentNode  # type: ignore[assignment]
        if node == None or node == tw.root:
            return None
        if nodeFilter(tw, node) == NodeFilter.FILTER_ACCEPT:
            return None


def nextSkippingChildren(node: Node, stayWithin: Node) -> Node | None:
    if node == stayWithin:
        return None
    if node.nextSibling != None:
        return node.nextSibling

    while node.parentNode != None:
        node = node.parentNode
        if node == stayWithin:
            return None
        if node.nextSibling != None:
            return node.nextSibling
    return None


# https://developer.mozilla.org/en-US/docs/Web/API/TreeWalker
class TreeWalker:
    """The TreeWalker object represents the nodes of a document subtree and a position within them."""

    def _upgrade_dom(self) -> None:
        """[
            Our dom has some strings that are not Text Nodes
            so we have to upgrade them to Node objects. As we can't know siblings otherwise
        ]
        """

        def upgrade(el: Node) -> None:
            if isinstance(el, (Text, str)):
                return
            for child in el:
                if isinstance(child, str):
                    newchild = Text(child)
                    el.replaceChild(newchild, child)  # type: ignore[arg-type]
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

        self.currentNode = node
        self.whatToShow = _coerce_what_to_show(whatToShow)

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
            NodeFilter.acceptNode = acceptNode  # type: ignore[attr-defined]

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
            node = node.parentNode  # type: ignore[assignment]
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
        If no such child exists, null is returned and the current node is not changed.
        """
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
        If there is no such node, null is returned and the current node is not changed.
        """
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
            if isinstance(node, str):
                Text(node)
                # continue

            while result != NodeFilter.FILTER_REJECT and node.firstChild != None:
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
                return None
            result = nodeFilter(self, node)
            if result == NodeFilter.FILTER_ACCEPT:
                self.currentNode = node
                return node


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


class DOMParser:
    """``new DOMParser().parseFromString(markup, mimeType)`` -- parse a string
    into a document, mirroring the browser API."""

    def parseFromString(self, string: str, mimeType: str = "text/html") -> "Node":
        from domonic import domonic

        mime = (mimeType or "text/html").lower()
        if "xml" in mime or "svg" in mime:
            return domonic.parseString(str(string), parser="expat")
        return domonic.parseString(str(string))


class XMLSerializer:
    """``new XMLSerializer().serializeToString(node)`` -- serialise a node back
    to markup."""

    def serializeToString(self, node: Any) -> str:
        outer = getattr(node, "outerHTML", None)
        return outer if isinstance(outer, str) else str(node)


class Sanitizer:
    """Backward-compatible proxy for ``domonic.webapi.sanitizer.Sanitizer``."""

    def __new__(cls, *args, **kwargs):
        from domonic.webapi.sanitizer import Sanitizer as WebSanitizer

        return WebSanitizer(*args, **kwargs)

    @staticmethod
    def getDefaultConfiguration():
        from domonic.webapi.sanitizer import Sanitizer as WebSanitizer

        return WebSanitizer.getDefaultConfiguration()


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


SVG_NAMESPACE = "http://www.w3.org/2000/svg"

# SVG elements whose geometry is intrinsic (a leaf shape or text run) rather
# than the union of their children.
_SVG_SHAPE_TAGS = frozenset(
    {"rect", "circle", "ellipse", "line", "polygon", "polyline", "path",
     "image", "use", "foreignObject"}
)
_SVG_TEXT_TAGS = frozenset({"text", "tspan", "textPath", "textpath"})
# containers whose getBBox() is the union of rendered descendants
_SVG_CONTAINER_TAGS = frozenset(
    {"svg", "g", "a", "switch", "marker", "symbol", "clipPath", "clippath",
     "pattern", "mask"}
)
_SVG_ALL_GEOMETRY_TAGS = (
    _SVG_SHAPE_TAGS | _SVG_TEXT_TAGS | _SVG_CONTAINER_TAGS
)

_SVG_TRANSFORM_RE = re.compile(
    r"(matrix|translate|scale|rotate|skewX|skewY)\s*\(([^)]*)\)"
)


def _svg_numbers(value: Any) -> list[float]:
    return [
        float(token)
        for token in re.split(r"[\s,]+", str(value or "").strip())
        if token and _SVG_NUMBER_RE.match(token)
    ]


_SVG_NUMBER_RE = re.compile(r"^[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?$")


def _svg_length(value: Any, default: float = 0.0) -> float:
    if value is None:
        return default
    match = re.search(r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?", str(value))
    return float(match.group(0)) if match else default


def _parse_svg_transform(value: Any) -> "DOMMatrix":
    """Parse an SVG ``transform`` attribute into a ``DOMMatrix`` such that a
    local point ``p`` maps to the parent space as ``p.matrixTransform(M)``."""
    matrix = DOMMatrix()
    if not value:
        return matrix
    for name, raw in _SVG_TRANSFORM_RE.findall(str(value)):
        args = _svg_numbers(raw)
        if name == "matrix" and len(args) == 6:
            token = DOMMatrix(*args)
        elif name == "translate":
            tx = args[0] if args else 0.0
            ty = args[1] if len(args) > 1 else 0.0
            token = DOMMatrix(1, 0, 0, 1, tx, ty)
        elif name == "scale":
            sx = args[0] if args else 1.0
            sy = args[1] if len(args) > 1 else sx
            token = DOMMatrix(sx, 0, 0, sy, 0, 0)
        elif name == "rotate":
            angle = math.radians(args[0]) if args else 0.0
            cos_a, sin_a = math.cos(angle), math.sin(angle)
            rot = DOMMatrix(cos_a, sin_a, -sin_a, cos_a, 0, 0)
            if len(args) >= 3:
                cx, cy = args[1], args[2]
                token = (
                    DOMMatrix(1, 0, 0, 1, -cx, -cy)
                    .multiply(rot)
                    .multiply(DOMMatrix(1, 0, 0, 1, cx, cy))
                )
            else:
                token = rot
        elif name == "skewX":
            token = DOMMatrix(1, 0, math.tan(math.radians(args[0] if args else 0)), 1, 0, 0)
        elif name == "skewY":
            token = DOMMatrix(1, math.tan(math.radians(args[0] if args else 0)), 0, 1, 0, 0)
        else:
            continue
        matrix = token.multiply(matrix)
    return matrix


def _svg_is_geometry_element(element: "Element") -> bool:
    if getattr(element, "namespaceURI", None) == SVG_NAMESPACE:
        return True
    name = str(getattr(element, "nodeName", "") or getattr(element, "name", "")).lower()
    return name in _SVG_ALL_GEOMETRY_TAGS


def _svg_resolve_font(element: "Element") -> tuple[float, bool, float]:
    """Return ``(font_size_px, bold, root_font_size)`` for a text element."""

    def prop(name: str):
        value = element.getAttribute(name)
        if value:
            return value
        style = getattr(element, "style", None)
        if style is not None:
            got = style.getPropertyValue(name)
            if got:
                return got
        try:
            from domonic.window import window as _window

            computed = _window.getComputedStyle(element)
            got = computed.getPropertyValue(name)
            if got and got not in ("normal", "medium"):
                return got
        except Exception:
            pass
        return None

    size = _fontmetrics.parse_length(prop("font-size"), default=16.0)
    weight = prop("font-weight")
    return size, _fontmetrics.is_bold(weight), 16.0


def _svg_text_content(element: "Element") -> str:
    try:
        return element.textContent or ""
    except Exception:
        return ""


def _svg_own_bbox(element: "Element") -> "DOMRect | None":
    name = str(
        getattr(element, "nodeName", "") or getattr(element, "name", "")
    ).lower()
    g = lambda a: element.getAttribute(a)  # noqa: E731

    if name in ("rect", "image", "use", "foreignobject"):
        return DOMRect(_svg_length(g("x")), _svg_length(g("y")),
                       _svg_length(g("width")), _svg_length(g("height")))
    if name == "circle":
        cx, cy, r = _svg_length(g("cx")), _svg_length(g("cy")), _svg_length(g("r"))
        return DOMRect(cx - r, cy - r, r * 2, r * 2)
    if name == "ellipse":
        cx, cy = _svg_length(g("cx")), _svg_length(g("cy"))
        rx, ry = _svg_length(g("rx")), _svg_length(g("ry"))
        return DOMRect(cx - rx, cy - ry, rx * 2, ry * 2)
    if name == "line":
        x1, y1 = _svg_length(g("x1")), _svg_length(g("y1"))
        x2, y2 = _svg_length(g("x2")), _svg_length(g("y2"))
        return DOMRect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
    if name in ("polygon", "polyline"):
        nums = _svg_numbers(g("points"))
        xs, ys = nums[0::2], nums[1::2]
        if not xs:
            return DOMRect()
        return DOMRect(min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys))
    if name == "path":
        return _svg_path_bbox(g("d"))
    if name in _SVG_TEXT_TAGS:
        text = _svg_text_content(element)
        size, bold, _root = _svg_resolve_font(element)
        width, height, ascent, descent = _fontmetrics.text_extent(text, size, bold)
        x = _svg_length(g("x")) + _svg_length(g("dx"))
        y = _svg_length(g("y")) + _svg_length(g("dy"))
        anchor = (g("text-anchor") or "").strip().lower()
        if anchor == "middle":
            x -= width / 2
        elif anchor == "end":
            x -= width
        return DOMRect(x, y - ascent, width, ascent + descent)
    return None


_SVG_PATH_TOKEN_RE = re.compile(r"([MmLlHhVvCcSsQqTtAaZz])|(-?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?)")


def _svg_path_bbox(d: Any) -> "DOMRect":
    if not d:
        return DOMRect()
    tokens = _SVG_PATH_TOKEN_RE.findall(str(d))
    xs: list[float] = []
    ys: list[float] = []
    cx = cy = 0.0
    start_x = start_y = 0.0
    i = 0
    cmd = ""
    numbers: list[float] = []
    for op, num in tokens:
        if op:
            cmd = op
            numbers = []
            if cmd in ("Z", "z"):
                cx, cy = start_x, start_y
            continue
        numbers.append(float(num))
        needed = {"H": 1, "h": 1, "V": 1, "v": 1, "M": 2, "m": 2, "L": 2, "l": 2,
                  "T": 2, "t": 2, "Q": 4, "q": 4, "S": 4, "s": 4, "C": 6, "c": 6,
                  "A": 7, "a": 7}.get(cmd, 2)
        if len(numbers) < needed:
            continue
        rel = cmd.islower()
        if cmd in ("H", "h"):
            cx = (cx + numbers[0]) if rel else numbers[0]
        elif cmd in ("V", "v"):
            cy = (cy + numbers[0]) if rel else numbers[0]
        elif cmd in ("A", "a"):
            nx, ny = numbers[5], numbers[6]
            cx, cy = (cx + nx, cy + ny) if rel else (nx, ny)
        else:
            nx, ny = numbers[-2], numbers[-1]
            cx, cy = (cx + nx, cy + ny) if rel else (nx, ny)
        if cmd in ("M", "m"):
            start_x, start_y = cx, cy
        xs.append(cx)
        ys.append(cy)
        numbers = []
    if not xs:
        return DOMRect()
    return DOMRect(min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys))


def _rect_union(a: "DOMRect | None", b: "DOMRect | None") -> "DOMRect | None":
    if a is None:
        return b
    if b is None:
        return a
    x0 = min(a.x, b.x)
    y0 = min(a.y, b.y)
    x1 = max(a.x + a.width, b.x + b.width)
    y1 = max(a.y + a.height, b.y + b.height)
    return DOMRect(x0, y0, x1 - x0, y1 - y0)


def _rect_transform(rect: "DOMRect", matrix: "DOMMatrix") -> "DOMRect":
    corners = [
        (rect.x, rect.y),
        (rect.x + rect.width, rect.y),
        (rect.x, rect.y + rect.height),
        (rect.x + rect.width, rect.y + rect.height),
    ]
    pts = [matrix.transformPoint(DOMPoint(px, py)) for px, py in corners]
    xs = [p.x for p in pts]
    ys = [p.y for p in pts]
    return DOMRect(min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys))


def _svg_bbox(element: "Element", _include_own_transform: bool = False) -> "DOMRect":
    own = _svg_own_bbox(element)
    if own is not None:
        result: "DOMRect | None" = own
    else:
        result = None
        for child in getattr(element, "childNodes", []):
            if not isinstance(child, Element) or not _svg_is_geometry_element(child):
                continue
            name = str(getattr(child, "nodeName", "")).lower()
            if name in ("defs", "metadata", "title", "desc"):
                continue
            child_box = _svg_bbox(child)
            if child_box is None:
                continue
            transform = _parse_svg_transform(child.getAttribute("transform"))
            if not transform.isIdentity:
                child_box = _rect_transform(child_box, transform)
            result = _rect_union(result, child_box)
    if result is None:
        return DOMRect()
    if _include_own_transform:
        transform = _parse_svg_transform(element.getAttribute("transform"))
        if not transform.isIdentity:
            result = _rect_transform(result, transform)
    return result


def _svg_ctm(element: "Element", to_screen: bool) -> "DOMMatrix":
    matrix = DOMMatrix()
    node: "Any" = element
    while isinstance(node, Element):
        local = _parse_svg_transform(node.getAttribute("transform"))
        matrix = matrix.multiply(local)
        name = str(getattr(node, "nodeName", "")).lower()
        if name == "svg":
            x = _svg_length(node.getAttribute("x"))
            y = _svg_length(node.getAttribute("y"))
            if x or y:
                matrix = matrix.multiply(DOMMatrix(1, 0, 0, 1, x, y))
            if not to_screen:
                break
        node = getattr(node, "parentNode", None)
    return matrix


MATHML_NAMESPACE = "http://www.w3.org/1998/Math/MathML"


class MathMLElement(Element):
    """DOM interface for MathML elements."""

    name = ""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.namespaceURI = MATHML_NAMESPACE

    @property
    def nonce(self) -> str | None:
        return self.getAttribute("nonce")

    @nonce.setter
    def nonce(self, value: Any) -> None:
        if value is None:
            self.removeAttribute("nonce")
            return
        self.setAttribute("nonce", value)


class HTMLElement(Element):
    name = ""

    @property
    def validity(self) -> ValidityState:
        return ValidityState(self)

    @property
    def validationMessage(self) -> str:
        custom_message = getattr(self, "_custom_validity_message", "")
        if custom_message:
            return custom_message
        validity = self.validity
        messages = (
            (validity.valueMissing, "Please fill out this field."),
            (validity.typeMismatch, "Please enter a valid value."),
            (validity.patternMismatch, "Please match the requested format."),
            (validity.rangeOverflow, "Value must be less than or equal to max."),
            (validity.rangeUnderflow, "Value must be greater than or equal to min."),
            (validity.stepMismatch, "Please enter a valid step value."),
            (validity.tooLong, "Please shorten this text."),
            (validity.tooShort, "Please lengthen this text."),
            (validity.badInput, "Please enter a valid value."),
        )
        for failed, message in messages:
            if failed:
                return message
        return ""

    @property
    def willValidate(self) -> bool:
        tag_name = getattr(self, "tagName", getattr(self, "name", "")).lower()
        if self.hasAttribute("disabled") or tag_name in {"fieldset", "output"}:
            return False
        if tag_name == "input" and self.type in {"hidden", "button", "reset"}:
            return False
        if tag_name == "button" and (self.getAttribute("type") or "submit").lower() in {
            "button",
            "reset",
        }:
            return False
        return tag_name in {"button", "input", "select", "textarea"}

    def checkValidity(self) -> bool:
        valid = not self.willValidate or self.validity.valid
        if not valid:
            self.dispatchEvent(Event("invalid", {"bubbles": False, "cancelable": True}))
        return valid

    def reportValidity(self) -> bool:
        return self.checkValidity()

    def setCustomValidity(self, message: Any) -> None:
        self._custom_validity_message = "" if message is None else str(message)

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
            {
                "bubbles": False,
                "cancelable": True,
                "oldState": old_state,
                "newState": new_state,
            },
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
                {
                    "bubbles": False,
                    "cancelable": False,
                    "oldState": old_state,
                    "newState": new_state,
                },
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
        autoplay: bool | None = None,
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
        return "".join(self.stream())

    def stream(self) -> Iterator[str]:
        if DOMConfig.RENDER_OPTIONAL_CLOSING_SLASH:
            if DOMConfig.SPACE_BEFORE_OPTIONAL_CLOSING_SLASH:
                yield f"<{self.name}{self.__attributes__} />"
            else:
                yield f"<{self.name}{self.__attributes__}/>"
            return
        yield f"<{self.name}{self.__attributes__} >"


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
        disabled: bool | None = None,
        form=None,
        formaction: str | None = None,
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
        if not result or self.hasAttribute("disabled"):
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

    def __init__(self, *args, width: int | None = None, height: int | None = None, **kwargs):
        """HTMLCanvasElement

        Args:
            width (int, optional): The height of the coordinate space in CSS pixels. Defaults to 150.
            height (int, optional): The width of the coordinate space in CSS pixels. Defaults to 300.
        """
        super().__init__(*args, **kwargs)
        self._context_type = None
        self._context = None
        if width is not None:
            self.setAttribute("width", width)
        if height is not None:
            self.setAttribute("height", height)

    def getContext(self, contextId: str, options: dict[str, Any] | None = None) -> Any:
        """Return a 2D, WebGL, or WebGL2 context for the canvas."""
        from domonic.webapi.canvas import get_canvas_context

        return get_canvas_context(self, contextId, options)

    def toDataURL(self, type: str = "image/png", quality: Any | None = None) -> str:
        """Return a data URL describing the current canvas command state."""
        from domonic.webapi.canvas import canvas_to_data_url

        return canvas_to_data_url(self, type, quality)

    def toBlob(
        self,
        callback: Callable[[Any], Any] | None = None,
        type: str = "image/png",
        quality: Any | None = None,
    ):
        """Create a ``Blob`` for the canvas data and optionally pass it to a callback."""
        from domonic.webapi.canvas import canvas_to_blob

        blob = canvas_to_blob(self, type)
        if callback is not None:
            callback(blob)
            return None
        return blob

    def captureStream(self, frameRate: float | None = None):
        """Return a simple video ``MediaStream`` for canvas capture examples."""
        from domonic.webapi.mediadevices import MediaStream, MediaStreamTrack

        constraints = {}
        if frameRate is not None:
            constraints["frameRate"] = frameRate
        return MediaStream(
            [MediaStreamTrack("video", "Canvas capture", constraints=constraints)]
        )

    def transferControlToOffscreen(self):
        """Return an ``OffscreenCanvas`` with the same dimensions."""
        from domonic.webapi.canvas import OffscreenCanvas

        return OffscreenCanvas(
            int(self.getAttribute("width") or 300),
            int(self.getAttribute("height") or 150),
        )


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
        from domonic.events import ToggleEvent

        previous = self.open
        old_state = "open" if previous else "closed"
        if is_open:
            self.setAttribute("open", True)
        else:
            self.removeAttribute("open")
        if previous != self.open:
            self.dispatchEvent(
                ToggleEvent(
                    ToggleEvent.TOGGLE,
                    {
                        "bubbles": False,
                        "cancelable": False,
                        "oldState": old_state,
                        "newState": "open" if self.open else "closed",
                    },
                )
            )

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
        self.dispatchEvent(
            CloseEvent(
                "close",
                {
                    "bubbles": False,
                    "cancelable": False,
                    "code": 0,
                    "reason": str(returnValue),
                    "wasClean": True,
                },
            )
        )
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

    def __getitem__(self, index: int | str):  # type: ignore[override]
        controls = self._controls()
        if isinstance(index, str):
            return self.namedItem(index)
        return controls[index]

    def item(self, index: int) -> HTMLElement | None:
        controls = self._controls()
        return controls[index] if 0 <= index < len(controls) else None

    def namedItem(  # type: ignore[override]
        self, name: str
    ) -> HTMLElement | RadioNodeList | None:
        matches = [
            control
            for control in self._controls()
            if control.getAttribute("id") == name
            or control.getAttribute("name") == name
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
        action: str | None = None,
        accept_charset: str | None = None,
        autocomplete=None,
        enctype: str | None = None,
        method: str | None = None,
        name: str | None = None,
        novalidate: bool | None = None,
        rel: str | None = None,
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
                control.dispatchEvent(
                    Event("invalid", {"bubbles": False, "cancelable": True})
                )
        return valid

    def requestSubmit(self, submitter=None):
        from domonic.events import FormDataEvent, SubmitEvent

        should_validate = not self.hasAttribute("novalidate")
        if submitter is not None and submitter.hasAttribute("formnovalidate"):
            should_validate = False
        if should_validate and not self.checkValidity():
            return False
        submit_event_result = self.dispatchEvent(
            SubmitEvent(
                "submit", {"bubbles": True, "cancelable": True, "submitter": submitter}
            )
        )
        if not submit_event_result:
            return False
        form_data = _construct_form_data(self, submitter)
        self.dispatchEvent(
            FormDataEvent(
                "formdata",
                {"bubbles": False, "cancelable": False, "formData": form_data},
            )
        )
        return True

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

    @property
    def files(self):
        from domonic.webapi.file import FileList

        if self.type != "file":
            return None
        selected_files = getattr(self, "_files", None)
        if selected_files is None:
            selected_files = FileList()
            self._files = selected_files
        return selected_files

    @files.setter
    def files(self, new_files: Any) -> None:
        from domonic.webapi.file import FileList

        self._files = (
            new_files if isinstance(new_files, FileList) else FileList(new_files)
        )

    def setValue(self, new_value: Any, *, dispatch_events: bool = True) -> str:
        if dispatch_events and not _dispatch_before_input_event(self, new_value):
            return self.value
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
        if not result or self.hasAttribute("disabled"):
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
        return super().checkValidity()

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
        self.textTracks: list[dict[str, Any]] = []
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
        self.dispatchEvent(
            Event("loadedmetadata", {"bubbles": False, "cancelable": False})
        )
        self.dispatchEvent(Event("loadeddata", {"bubbles": False, "cancelable": False}))
        return self

    def play(self):
        self.dispatchEvent(Event("play", {"bubbles": False, "cancelable": False}))
        self.dispatchEvent(Event("playing", {"bubbles": False, "cancelable": False}))
        return True

    def pause(self):
        self.dispatchEvent(Event("pause", {"bubbles": False, "cancelable": False}))
        return None

    def addTextTrack(
        self, kind: str, label: str = "", language: str = ""
    ) -> dict[str, Any]:
        from domonic.events import TrackEvent

        track = {
            "kind": kind,
            "label": label,
            "language": language,
            "mode": "disabled",
            "cues": [],
        }
        self.textTracks.append(track)
        self.dispatchEvent(
            TrackEvent(
                TrackEvent.ADDTRACK,
                {"bubbles": False, "cancelable": False, "track": track},
            )
        )
        return track

    def removeTextTrack(self, track: dict[str, Any]) -> None:
        from domonic.events import TrackEvent

        if track not in self.textTracks:
            return
        self.textTracks.remove(track)
        self.dispatchEvent(
            TrackEvent(
                TrackEvent.REMOVETRACK,
                {"bubbles": False, "cancelable": False, "track": track},
            )
        )


class HTMLMetaElement(HTMLElement):
    name = "meta"
    __isempty = True

    def __init__(
        self, *args, charset=None, content=None, http_equiv=None, name=None, **kwargs
    ):
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

    def __init__(
        self,
        *args,
        value=None,
        _min=None,
        _max=None,
        low=None,
        high=None,
        optimum=None,
        **kwargs,
    ):
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

    def __init__(
        self, *args, disabled=None, label=None, selected=None, value=None, **kwargs
    ):
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
            while select_owner is not None and not isinstance(
                select_owner, HTMLSelectElement
            ):
                select_owner = getattr(select_owner, "parentNode", None)
            if isinstance(
                select_owner, HTMLSelectElement
            ) and not select_owner.hasAttribute("multiple"):
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

    def __getitem__(self, index: int | str):  # type: ignore[override]
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
        autofocus: bool | None = None,
        disabled: bool | None = None,
        multiple: bool | None = None,
        name: str | None = None,
        required: bool | None = None,
        size: int | None = None,
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
        return super().checkValidity()

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

    def __init__(
        self,
        *args,
        height=None,
        media=None,
        sizes=None,
        src=None,
        srcset=None,
        type=None,
        width=None,
        **kwargs,
    ):
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

    def __init__(
        self, *args, blocking=None, media=None, scoped=None, type=None, **kwargs
    ):
        """HTMLStyleElement

        Args:
            type (str, optional): Specifies the type of style sheet.
            media (str, optional): Specifies the media for which the styles are intended.
            scoped (str, optional): Indicates whether the style is scoped to the element.
        """
        super().__init__(*args, **kwargs)
        _set_attributes(
            self, {"blocking": blocking, "media": media, "scoped": scoped, "type": type}
        )


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
        align: str | None = None,
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

    def __init__(self, *args, open: bool | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        if open is not None:
            self.open = open

    @property
    def open(self) -> bool:
        return self.hasAttribute("open")

    @open.setter
    def open(self, is_open: bool) -> None:
        from domonic.events import ToggleEvent

        previous = self.open
        old_state = "open" if previous else "closed"
        if is_open:
            self.setAttribute("open", True)
        else:
            self.removeAttribute("open")
        if previous != self.open:
            self.dispatchEvent(
                ToggleEvent(
                    ToggleEvent.TOGGLE,
                    {
                        "bubbles": False,
                        "cancelable": False,
                        "oldState": old_state,
                        "newState": "open" if self.open else "closed",
                    },
                )
            )

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
        return [
            node for node in self.assignedNodes(options) if isinstance(node, Element)
        ]


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
        if dispatch_events and not _dispatch_before_input_event(self, new_value):
            return self.value
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
        return super().checkValidity()

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

    def __init__(
        self,
        *args,
        kind=None,
        label=None,
        src=None,
        srclang=None,
        default=None,
        **kwargs,
    ):
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
