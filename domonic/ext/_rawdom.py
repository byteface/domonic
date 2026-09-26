"""
domonic.ext._rawdom
====================================

Shared low-level helpers for the native-tree parser adapters
(``selectolax_``, ``turbohtml_``, ``justhtml_``, ``html5lib_`` and friends).

These build domonic ``Node`` instances by writing ``__dict__`` directly and
skipping ``Element.__init__`` / the DOM mutation machinery, which is safe during
a bulk parse where the whole tree is assembled before anything observes it. The
adapters were each carrying their own copy of this code; keeping one copy means
an optimisation lands everywhere at once.
"""

from __future__ import annotations

import importlib
import re
from typing import Any, TypeVar

from domonic import dom

HTML_NAMESPACE = "http://www.w3.org/1999/xhtml"
SVG_NAMESPACE = "http://www.w3.org/2000/svg"
MATHML_NAMESPACE = "http://www.w3.org/1998/Math/MathML"
HTML_INTEGRATION_ENCODINGS = {"application/xhtml+xml", "text/html"}

HTML_TAGS = frozenset(importlib.import_module("domonic.html").html_tags)
SVG_TAGS = frozenset(importlib.import_module("domonic.svg").svg_tags) - HTML_TAGS
MATHML_TAGS = frozenset(importlib.import_module("domonic.xml.mathml").mathml_tags)
SVG_TAG_NAMES = frozenset(tag.lower() for tag in SVG_TAGS)
MATHML_TAG_NAMES = frozenset(tag.lower() for tag in MATHML_TAGS)

_NodeT = TypeVar("_NodeT", bound=dom.Node)

# Bind the base allocator/setter once; these paths deliberately bypass DOM hooks.
_new_node = object.__new__
_set_state = object.__setattr__

_HTML_ELEMENT_CLASS_CACHE: dict[str, type[dom.Element]] = {}
_UNKNOWN_ELEMENT_CLASS_CACHE: dict[str, type[dom.Element]] = {}
_HTML_CLASS_CACHE: dict[str, type] = {}


def _set_attribute_raw(element: dom.Element, name: str, value: Any) -> None:
    if name and name[0] != "_":
        name = "_" + name
    element.__dict__["kwargs"][name] = value


def _append_child_raw(parent: dom.Node, child: dom.Node, children: list[Any]) -> None:
    children.append(child)
    child.__dict__["parentNode"] = parent


_Text = dom.Text
_Comment = dom.Comment


def _live_args(node: dom.Node) -> list[Any]:
    """Return ``node``'s children as a mutable ``list``, converting the ``args``
    tuple in place on first touch. A tree builder appends into these lists
    (O(1) each; growing a tuple per child was O(n^2) for wide parents) and
    freezes them back to the tuple the rest of domonic expects with
    ``_freeze_args`` as each element closes, or ``_freeze`` for a whole tree.
    """
    state = node.__dict__
    args = state.get("args")
    if type(args) is list:
        return args
    args = list(args) if args else []
    state["args"] = args
    return args


def _live_append(parent: dom.Node, child: dom.Node) -> None:
    _live_args(parent).append(child)
    child.__dict__["parentNode"] = parent


def _freeze_args(node: dom.Node) -> None:
    """Turn ``node``'s builder-time child list back into a tuple (one node)."""
    state = node.__dict__
    args = state.get("args")
    if type(args) is list:
        state["args"] = tuple(args)


def _freeze(root: dom.Node) -> None:
    """``_freeze_args`` for every element under ``root``. One pass; text and
    comment nodes are leaves and are skipped without a lookup."""
    stack = [root]
    pop = stack.pop
    push = stack.append
    while stack:
        state = pop().__dict__
        args = state.get("args")
        if type(args) is list:
            # Convert before the emptiness check: html5lib's adoption agency
            # leaves the original formatting element with an empty list.
            args = tuple(args)
            state["args"] = args
        if not args:
            continue
        for node in args:
            kind = type(node)
            if kind is not _Text and kind is not _Comment and kind is not str:
                push(node)


def _invalidate_indexes() -> None:
    """Drop every cached id / tag / class index and computed style.

    Raw insertion bypasses the epoch bookkeeping in ``dom.py``, so a lookup
    made against a tree that is still being built would otherwise keep
    answering from that snapshot. Anything that lets user code observe a
    raw-built tree before it is complete (a streaming checkpoint) must call
    this at each observation boundary. Cached ``str(node)`` output is the
    caller's to mark dirty (``dom._invalidate_render_cache``) for the nodes
    that can still gain children.
    """
    dom._bump_dom_epoch()
    dom._bump_structure_epoch()
    dom._cssom.bump_dom_style_epoch()


_NODE_STATE_DEFAULTS = {
    "_baseURI": "",
    "isConnected": True,
    "namespaceURI": HTML_NAMESPACE,
    "outerText": None,
    "_ownerDocument": None,
    "parentNode": None,
    "prefix": None,
    "_escape_text_on_render": False,
    "_escape_attributes_on_render": False,
    # every element/text node this module's HTML-parser adapters build belongs
    # to an HTML document -- gates Element.tagName / nodeName upper-casing
    "_html_doc": True,
}

_DOCUMENT_STATE_DEFAULTS = {
    "_open_filename": None,
    "_activeElement": None,
    "_defaultView": None,
    "_designMode": "off",
    "_currentScript": None,
    "_fonts": None,
    "_lastModified": "",
    "_referrer": "",
    "_timeline": None,
    "_Document__stylesheets": None,
    "_doctype": None,
    "URL": "",
}

_TEXT_STATE_DEFAULTS = {
    "name": "",
    "_baseURI": "",
    "isConnected": True,
    "namespaceURI": HTML_NAMESPACE,
    "outerText": None,
    "_ownerDocument": None,
    "parentNode": None,
    "prefix": None,
    "_escape_text_on_render": True,
    "_escape_attributes_on_render": False,
    "_html_doc": True,
}


_ELEMENT_STATE_DEFAULTS = {
    **_NODE_STATE_DEFAULTS,
    "args": (),
    "_Element__style": None,
    "shadowRoot": None,
    "_namespaceURI": HTML_NAMESPACE,
    "_escape_attributes_on_render": True,
}
# ``dir`` / ``lang`` / ``tabIndex`` are reflection *properties* on Element that
# read from getAttribute(); a same-named __dict__ entry is shadowed by the
# descriptor and never read, so the parser adapters don't seed them.


def _initialize_node_raw(node: _NodeT, args: tuple[Any, ...] = ()) -> _NodeT:
    state = node.__dict__
    state.update(_NODE_STATE_DEFAULTS)
    state["args"] = args
    state["kwargs"] = {}
    state["name"] = getattr(node.__class__, "name", "") or ""
    state["listeners"] = {}
    state["_listener_options"] = {}
    return node


def _initialize_element_raw(element: dom.Element, namespace_uri: str = HTML_NAMESPACE) -> dom.Element:
    state = element.__dict__
    state.update(_ELEMENT_STATE_DEFAULTS)
    state["kwargs"] = {}
    state["name"] = getattr(element.__class__, "name", "") or ""
    state["listeners"] = {}
    state["_listener_options"] = {}
    # _ELEMENT_STATE_DEFAULTS already carries the HTML namespace on both keys;
    # only the (rare) foreign-namespace element needs the override.
    if namespace_uri != HTML_NAMESPACE:
        state["namespaceURI"] = namespace_uri
        state["_namespaceURI"] = namespace_uri
    return element


def _element_class(name: str, namespace_uri: str) -> type[dom.Element]:
    normalized_name = str(name).strip().lower()
    cache_key = f"{namespace_uri}:{normalized_name}"
    cached = _HTML_ELEMENT_CLASS_CACHE.get(cache_key)
    if cached is not None:
        return cached

    if namespace_uri == SVG_NAMESPACE:
        svg_module = importlib.import_module("domonic.svg")
        tag_name = getattr(svg_module, "_PYTHON_NAME_TO_TAG", {}).get(normalized_name, name)
        if tag_name in svg_module._SVG_TAG_LOOKUP:
            element_class = getattr(svg_module, svg_module._svg_class_name(tag_name))
        else:
            element_class = _UNKNOWN_ELEMENT_CLASS_CACHE.get(cache_key)
            if element_class is None:
                element_class = type("custom_tag", (dom.Element,), {"name": name})
                _UNKNOWN_ELEMENT_CLASS_CACHE[cache_key] = element_class
        _HTML_ELEMENT_CLASS_CACHE[cache_key] = element_class
        return element_class

    if namespace_uri == MATHML_NAMESPACE:
        mathml = importlib.import_module("domonic.xml.mathml")
        lookup_name = "math_" if normalized_name == "math" else normalized_name
        if normalized_name in mathml.mathml_tags and hasattr(mathml, lookup_name):
            element_class = getattr(mathml, lookup_name)
        else:
            element_class = _UNKNOWN_ELEMENT_CLASS_CACHE.get(cache_key)
            if element_class is None:
                element_class = type("custom_tag", (dom.MathMLElement,), {"name": name})
                _UNKNOWN_ELEMENT_CLASS_CACHE[cache_key] = element_class
        _HTML_ELEMENT_CLASS_CACHE[cache_key] = element_class
        return element_class

    html = importlib.import_module("domonic.html")
    if normalized_name in html._HTML_TAG_LOOKUP:
        tag_name = html._TAG_ALIASES.get(normalized_name, normalized_name)
        element_class = getattr(html, tag_name)
    else:
        element_class = _UNKNOWN_ELEMENT_CLASS_CACHE.get(cache_key)
        if element_class is None:
            # https://html.spec.whatwg.org/#elements-in-the-dom: a valid custom
            # element name (it has a hyphen) is an HTMLElement awaiting upgrade;
            # anything else unknown is an HTMLUnknownElement.
            base = dom.HTMLElement if "-" in normalized_name else dom.HTMLUnknownElement
            element_class = type("custom_tag", (base,), {"name": name})
            _UNKNOWN_ELEMENT_CLASS_CACHE[cache_key] = element_class

    _HTML_ELEMENT_CLASS_CACHE[cache_key] = element_class
    return element_class


def _namespace_for_tag(
    tag: str,
    parent_namespace: str = HTML_NAMESPACE,
    parent_tag: str = "",
    parent_encoding: str = "",
) -> str:
    normalized_name = str(tag).strip().lower()
    if normalized_name == "svg":
        return SVG_NAMESPACE
    if normalized_name == "math":
        return MATHML_NAMESPACE
    if parent_namespace == HTML_NAMESPACE and normalized_name in SVG_TAG_NAMES:
        return SVG_NAMESPACE
    if parent_namespace == HTML_NAMESPACE and normalized_name in MATHML_TAG_NAMES:
        return MATHML_NAMESPACE
    if (
        parent_namespace == MATHML_NAMESPACE
        and parent_tag.lower() == "annotation-xml"
        and parent_encoding.strip().lower() in HTML_INTEGRATION_ENCODINGS
    ):
        return HTML_NAMESPACE
    if parent_namespace == SVG_NAMESPACE:
        if parent_tag.lower() == "foreignobject":
            return HTML_NAMESPACE
        return SVG_NAMESPACE
    if parent_namespace == MATHML_NAMESPACE:
        return MATHML_NAMESPACE
    return HTML_NAMESPACE


def _apply_document_state(element: dom.Element) -> None:
    state = element.__dict__
    state.update(_DOCUMENT_STATE_DEFAULTS)
    state["_cookie_store"] = {}
    state.setdefault("documentElement", element)


def _create_element_raw(name: str, namespace_uri: str = HTML_NAMESPACE) -> dom.Element:
    if namespace_uri == HTML_NAMESPACE:
        # Hot path: skip the ``str().strip().lower()`` + f-string cache key that
        # ``_element_class`` builds. Frontend parsers already emit clean
        # lower-case tag names for the HTML namespace.
        element_class = _HTML_CLASS_CACHE.get(name)
        if element_class is None:
            element_class = _element_class(name, HTML_NAMESPACE)
            _HTML_CLASS_CACHE[name] = element_class
    else:
        element_class = _element_class(name, namespace_uri)
    element = _initialize_element_raw(_new_node(element_class), namespace_uri)
    if issubclass(element_class, dom.Document):
        # ``domonic.html.html`` subclasses ``HTMLDocument``; the raw element
        # init skips the document-level state those instances still expect.
        _apply_document_state(element)
    return element


def _create_document_raw() -> dom.HTMLDocument:
    document = _new_node(dom.HTMLDocument)
    _initialize_element_raw(document)
    _apply_document_state(document)
    return document


def _create_text_raw(data: Any) -> dom.Text:
    # Text nodes are ~half of all nodes on a real page and never take event
    # listeners, so skip the listener dicts the general node init allocates.
    text = _new_node(dom.Text)
    state = _TEXT_STATE_DEFAULTS.copy()
    state["kwargs"] = {}
    state["args"] = ("" if data is None else str(data),)
    _set_state(text, "__dict__", state)
    return text


def _create_comment_raw(data: Any) -> dom.Comment:
    comment = _initialize_node_raw(_new_node(dom.Comment))
    comment.data = "" if data is None else str(data)
    return comment


def _create_fragment_raw() -> dom.DocumentFragment:
    return _initialize_node_raw(_new_node(dom.DocumentFragment))


def _create_cdata_raw(data: Any) -> dom.CDATASection:
    cdata = _initialize_node_raw(_new_node(dom.CDATASection))
    cdata.data = "" if data is None else str(data)
    return cdata


def _create_processing_instruction_raw(target: Any, data: Any) -> dom.ProcessingInstruction:
    instruction = _initialize_node_raw(_new_node(dom.ProcessingInstruction))
    instruction.target = "" if target is None else str(target)
    instruction.data = "" if data is None else str(data)
    return instruction


def _create_doctype_raw(serialized: str) -> dom.DocumentType:
    match = re.match(r"<!doctype\s+([^>\s]+)", serialized or "", re.I)
    doctype = _initialize_node_raw(_new_node(dom.DocumentType))
    doctype.name = match.group(1) if match else "html"
    doctype.publicId = ""
    doctype.systemId = ""
    doctype._internalSubset = None
    doctype._entities = dom.NamedNodeMap()
    doctype._notations = dom.NamedNodeMap()
    return doctype


def _create_doctype_parts_raw(name: Any, public_id: Any = "", system_id: Any = "") -> dom.DocumentType:
    doctype = _initialize_node_raw(_new_node(dom.DocumentType))
    doctype.name = str(name) if name else "html"
    doctype.publicId = str(public_id or "")
    doctype.systemId = str(system_id or "")
    doctype._internalSubset = None
    doctype._entities = dom.NamedNodeMap()
    doctype._notations = dom.NamedNodeMap()
    return doctype
