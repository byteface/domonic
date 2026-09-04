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

_HTML_ELEMENT_CLASS_CACHE: dict[str, type[dom.Element]] = {}
_UNKNOWN_ELEMENT_CLASS_CACHE: dict[str, type[dom.Element]] = {}
_HTML_CLASS_CACHE: dict[str, type] = {}


def _set_attribute_raw(element: dom.Element, name: str, value: Any) -> None:
    if name and name[0] != "_":
        name = "_" + name
    element.__dict__["kwargs"][name] = value


def _append_child_raw(
    parent: dom.Node, child: dom.Node, children: list[Any]
) -> None:
    children.append(child)
    child.__dict__["parentNode"] = parent


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
    "kwargs": {},
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


def _initialize_node_raw(
    node: _NodeT, args: tuple[Any, ...] = ()
) -> _NodeT:
    state = node.__dict__
    state.update(_NODE_STATE_DEFAULTS)
    state["args"] = args
    state["kwargs"] = {}
    state["name"] = getattr(node.__class__, "name", "") or ""
    state["listeners"] = {}
    state["_listener_options"] = {}
    return node


def _initialize_element_raw(
    element: dom.Element, namespace_uri: str = HTML_NAMESPACE
) -> dom.Element:
    _initialize_node_raw(element)
    state = element.__dict__
    state["namespaceURI"] = namespace_uri
    state["lang"] = None
    state["tabIndex"] = None
    state["_Element__style"] = None
    state["shadowRoot"] = None
    state["dir"] = None
    state["_namespaceURI"] = namespace_uri
    state["_escape_attributes_on_render"] = True
    return element


def _element_class(name: str, namespace_uri: str) -> type[dom.Element]:
    normalized_name = str(name).strip().lower()
    cache_key = f"{namespace_uri}:{normalized_name}"
    cached = _HTML_ELEMENT_CLASS_CACHE.get(cache_key)
    if cached is not None:
        return cached

    if namespace_uri == SVG_NAMESPACE:
        svg_module = importlib.import_module("domonic.svg")
        tag_name = getattr(svg_module, "_PYTHON_NAME_TO_TAG", {}).get(
            normalized_name, name
        )
        if tag_name in svg_module._SVG_TAG_LOOKUP:
            element_class = getattr(
                svg_module, svg_module._svg_class_name(tag_name)
            )
        else:
            element_class = _UNKNOWN_ELEMENT_CLASS_CACHE.get(cache_key)
            if element_class is None:
                element_class = type(
                    "custom_tag", (dom.Element,), {"name": name}
                )
                _UNKNOWN_ELEMENT_CLASS_CACHE[cache_key] = element_class
        _HTML_ELEMENT_CLASS_CACHE[cache_key] = element_class
        return element_class

    if namespace_uri == MATHML_NAMESPACE:
        mathml = importlib.import_module("domonic.xml.mathml")
        lookup_name = "math_" if normalized_name == "math" else normalized_name
        if normalized_name in mathml.mathml_tags and hasattr(
            mathml, lookup_name
        ):
            element_class = getattr(mathml, lookup_name)
        else:
            element_class = _UNKNOWN_ELEMENT_CLASS_CACHE.get(cache_key)
            if element_class is None:
                element_class = type(
                    "custom_tag", (dom.MathMLElement,), {"name": name}
                )
                _UNKNOWN_ELEMENT_CLASS_CACHE[cache_key] = element_class
        _HTML_ELEMENT_CLASS_CACHE[cache_key] = element_class
        return element_class

    html = importlib.import_module("domonic.html")
    if normalized_name in html._HTML_TAG_LOOKUP:
        tag_name = html._TAG_ALIASES.get(normalized_name, normalized_name)
        element_class = getattr(html, tag_name)
    else:
        element_class = _UNKNOWN_ELEMENT_CLASS_CACHE.get(normalized_name)
        if element_class is None:
            element_class = type("custom_tag", (dom.Element,), {"name": name})
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
    if (
        parent_namespace == HTML_NAMESPACE
        and normalized_name in MATHML_TAG_NAMES
    ):
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


def _create_element_raw(
    name: str, namespace_uri: str = HTML_NAMESPACE
) -> dom.Element:
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
    element = _initialize_element_raw(
        object.__new__(element_class), namespace_uri
    )
    if issubclass(element_class, dom.Document):
        # ``domonic.html.html`` subclasses ``HTMLDocument``; the raw element
        # init skips the document-level state those instances still expect.
        _apply_document_state(element)
    return element


def _create_document_raw() -> dom.HTMLDocument:
    document = object.__new__(dom.HTMLDocument)
    _initialize_element_raw(document)
    _apply_document_state(document)
    return document


def _create_text_raw(data: Any) -> dom.Text:
    # Text nodes are ~half of all nodes on a real page and never take event
    # listeners, so skip the listener dicts the general node init allocates.
    text = object.__new__(dom.Text)
    state = text.__dict__
    state.update(_TEXT_STATE_DEFAULTS)
    state["args"] = ("" if data is None else str(data),)
    return text


def _create_comment_raw(data: Any) -> dom.Comment:
    comment = _initialize_node_raw(object.__new__(dom.Comment))
    comment.data = "" if data is None else str(data)
    return comment


def _create_fragment_raw() -> dom.DocumentFragment:
    return _initialize_node_raw(object.__new__(dom.DocumentFragment))


def _create_cdata_raw(data: Any) -> dom.CDATASection:
    cdata = _initialize_node_raw(object.__new__(dom.CDATASection))
    cdata.data = "" if data is None else str(data)
    return cdata


def _create_processing_instruction_raw(
    target: Any, data: Any
) -> dom.ProcessingInstruction:
    instruction = _initialize_node_raw(
        object.__new__(dom.ProcessingInstruction)
    )
    instruction.target = "" if target is None else str(target)
    instruction.data = "" if data is None else str(data)
    return instruction


def _create_doctype_raw(serialized: str) -> dom.DocumentType:
    match = re.match(r"<!doctype\s+([^>\s]+)", serialized or "", re.I)
    doctype = _initialize_node_raw(object.__new__(dom.DocumentType))
    doctype.name = match.group(1) if match else "html"
    doctype.publicId = ""
    doctype.systemId = ""
    doctype._internalSubset = None
    doctype._entities = dom.NamedNodeMap()
    doctype._notations = dom.NamedNodeMap()
    return doctype


def _create_doctype_parts_raw(
    name: Any, public_id: Any = "", system_id: Any = ""
) -> dom.DocumentType:
    doctype = _initialize_node_raw(object.__new__(dom.DocumentType))
    doctype.name = str(name) if name else "html"
    doctype.publicId = str(public_id or "")
    doctype.systemId = str(system_id or "")
    doctype._internalSubset = None
    doctype._entities = dom.NamedNodeMap()
    doctype._notations = dom.NamedNodeMap()
    return doctype
