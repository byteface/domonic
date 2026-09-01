"""
domonic.ext.selectolax_
====================================

Adapter for using selectolax as a frontend parser while rebuilding a
domonic document tree directly from selectolax's native tree.
"""

from __future__ import annotations

import importlib
import re
from typing import Any, cast

from domonic import dom

HTML_NAMESPACE = "http://www.w3.org/1999/xhtml"
SVG_NAMESPACE = "http://www.w3.org/2000/svg"
MATHML_NAMESPACE = "http://www.w3.org/1998/Math/MathML"

_HTML_ELEMENT_CLASS_CACHE: dict[str, type[dom.Element]] = {}
_UNKNOWN_ELEMENT_CLASS_CACHE: dict[str, type[dom.Element]] = {}


def _set_attribute_raw(element: dom.Element, name: str, value: Any) -> None:
    if name and name[0] != "_":
        name = "_" + name
    element.__dict__["kwargs"][name] = value


def _append_child_raw(
    parent: dom.Node, child: dom.Node, children: list[Any]
) -> None:
    children.append(child)
    child.__dict__["parentNode"] = parent


def _initialize_node_raw(
    node: dom.Node, args: tuple[Any, ...] = ()
) -> dom.Node:
    state = node.__dict__
    state["args"] = args
    state["kwargs"] = {}
    state["listeners"] = {}
    state["_listener_options"] = {}
    state["_baseURI"] = ""
    state["isConnected"] = True
    state["namespaceURI"] = HTML_NAMESPACE
    state["outerText"] = None
    state["_ownerDocument"] = None
    state["parentNode"] = None
    state["prefix"] = None
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
    tag: str, parent_namespace: str = HTML_NAMESPACE, parent_tag: str = ""
) -> str:
    normalized_name = str(tag).strip().lower()
    if normalized_name == "svg":
        return SVG_NAMESPACE
    if normalized_name == "math":
        return MATHML_NAMESPACE
    if parent_namespace == SVG_NAMESPACE:
        if parent_tag.lower() == "foreignobject":
            return HTML_NAMESPACE
        return SVG_NAMESPACE
    if parent_namespace == MATHML_NAMESPACE:
        return MATHML_NAMESPACE
    return HTML_NAMESPACE


def _create_element_raw(
    name: str, namespace_uri: str = HTML_NAMESPACE
) -> dom.Element:
    element_class = _element_class(name, namespace_uri)
    return cast(
        dom.Element,
        _initialize_element_raw(object.__new__(element_class), namespace_uri),
    )


def _create_document_raw() -> dom.HTMLDocument:
    document = object.__new__(dom.HTMLDocument)
    _initialize_element_raw(document)
    document.__dict__.update(
        {
            "_open_filename": None,
            "_activeElement": None,
            "_defaultView": None,
            "_designMode": "off",
            "_currentScript": None,
            "_cookie_store": {},
            "_fonts": None,
            "_lastModified": "",
            "_referrer": "",
            "_timeline": None,
            "_Document__stylesheets": None,
            "_doctype": None,
            "documentElement": document,
            "URL": "",
        }
    )
    return document


def _create_text_raw(data: Any) -> dom.Text:
    return cast(
        dom.Text,
        _initialize_node_raw(
            object.__new__(dom.Text), ("" if data is None else str(data),)
        ),
    )


def _create_comment_raw(data: Any) -> dom.Comment:
    comment = _initialize_node_raw(object.__new__(dom.Comment))
    comment.data = "" if data is None else str(data)
    return cast(dom.Comment, comment)


def _create_doctype_raw(serialized: str) -> dom.DocumentType:
    match = re.match(r"<!doctype\s+([^>\s]+)", serialized or "", re.I)
    doctype = _initialize_node_raw(object.__new__(dom.DocumentType))
    doctype.name = match.group(1) if match else "html"
    doctype.publicId = ""
    doctype.systemId = ""
    doctype._internalSubset = None
    doctype._entities = dom.NamedNodeMap()
    doctype._notations = dom.NamedNodeMap()
    return cast(dom.DocumentType, doctype)


def _node_text(node: Any) -> str:
    text = getattr(node, "text", None)
    if callable(text):
        return text()
    text_content = getattr(node, "text_content", None)
    if callable(text_content):
        return text_content()
    if text_content is not None:
        return text_content
    html = getattr(node, "html", "")
    return "" if html is None else str(html)


def _set_attributes(element: dom.Element, attrs: Any) -> None:
    if not attrs:
        return
    for name, value in attrs.items():
        _set_attribute_raw(element, name, "" if value is None else value)


def _adapt_node(
    node: Any,
    parent_namespace: str = HTML_NAMESPACE,
    parent_tag: str = "",
) -> Any:
    tag = getattr(node, "tag", "")
    if tag in ("-doctype", "!doctype"):
        return _create_doctype_raw(getattr(node, "html", ""))
    if tag == "-text":
        text = getattr(node, "text", None)
        if callable(text):
            return _create_text_raw(text())
        return _create_text_raw(_node_text(node))
    if tag in ("-comment", "_comment"):
        comment = getattr(node, "comment_content", None)
        if comment is None:
            html = getattr(node, "html", "") or ""
            comment = (
                html[4:-3]
                if html.startswith("<!--") and html.endswith("-->")
                else ""
            )
        return _create_comment_raw(comment)
    if not tag:
        return None

    namespace_uri = _namespace_for_tag(tag, parent_namespace, parent_tag)
    element = _create_element_raw(tag, namespace_uri)
    _set_attributes(element, getattr(node, "attributes", None))
    children: list[Any] = []
    child = getattr(node, "child", None)
    while child is not None:
        adapted = _adapt_node(child, namespace_uri, tag)
        if adapted is not None:
            _append_child_raw(element, adapted, children)
        child = getattr(child, "next", None)
    element.__dict__["args"] = tuple(children)
    return element


def _parse_tree(source: Any):
    try:
        parser_module = importlib.import_module("selectolax.lexbor")
        parser_class = parser_module.LexborHTMLParser
    except ImportError:
        parser_module = importlib.import_module("selectolax.parser")
        parser_class = parser_module.HTMLParser

    return parser_class("" if source is None else source)


def parse(html: Any, return_root: bool = True, **kwargs: Any) -> dom.Node:
    parser = _parse_tree(html)
    document = _create_document_raw()
    children: list[Any] = []

    doctype = getattr(parser.root, "prev", None)
    if doctype is not None and getattr(doctype, "tag", "") in (
        "-doctype",
        "!doctype",
    ):
        document.doctype = _adapt_node(doctype)

    root = _adapt_node(parser.root)
    if root is not None:
        _append_child_raw(document, root, children)
        document.documentElement = root

    document.__dict__["args"] = tuple(children)
    if return_root and len(children) == 1:
        return children[0]
    return document
