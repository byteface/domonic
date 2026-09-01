#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: Apache 2.0 Copyright: 2017, Kovid Goyal <kovid at kovidgoyal.net>
"""Adapt lxml trees into ordinary domonic DOM nodes."""

# Based on domonic.ext.html5_parser_.dom, originally adapted from
# html5_parser's Apache-2.0 tree adapter by Kovid Goyal.

from __future__ import annotations

import importlib
from typing import Any

from lxml.etree import _Comment

from domonic.dom import (
    MATHML_NAMESPACE,
    Comment,
    Element,
    MathMLElement,
    Text,
    XMLDocument,
)

HTML_NAMESPACE = "http://www.w3.org/1999/xhtml"
SVG_NAMESPACE = "http://www.w3.org/2000/svg"

_ELEM_NAME_CACHE: dict[tuple[Any, Any], tuple[str | None, str]] = {}
_MATHML_ELEMENT_CACHE: dict[str, type[MathMLElement]] = {}
_HTML_ELEMENT_CLASS_CACHE: dict[str, type[Element]] = {}
_UNKNOWN_ELEMENT_CLASS_CACHE: dict[str, type[Element]] = {}


def elem_name_parts(elem):
    key = (elem.tag, elem.prefix)
    cached = _ELEM_NAME_CACHE.get(key)
    if cached is not None:
        return cached

    tag, prefix = key
    if tag.startswith("{"):
        uri, _, name = tag.rpartition("}")
        if prefix:
            name = prefix + ":" + name
        cached = (uri[1:], name)
    else:
        cached = (None, tag)

    _ELEM_NAME_CACHE[key] = cached
    return cached


def attr_name_parts(name, elem, val):
    if name.startswith("{"):
        uri, _, name = name.rpartition("}")
        uri = uri[1:]
        for prefix, quri in elem.nsmap.items():
            if quri == uri:
                break
        else:
            prefix = None
        if prefix:
            name = prefix + ":" + name
        return uri, name, val
    return None, name, val


def set_attribute_raw(dest, name, val):
    if name and name[0] != "_":
        name = "_" + name
    dest.__dict__["kwargs"][name] = val


def add_namespace_declarations_raw(src, dest):
    changed = src.nsmap
    if changed:
        parent = src.getparent()
        if parent is not None:
            parent_namespaces = parent.nsmap or {}
            changed = {
                key: value
                for key, value in changed.items()
                if value != parent_namespaces.get(key)
            }
        for prefix, uri in changed.items():
            attr = ("xmlns:" + prefix) if prefix else "xmlns"
            set_attribute_raw(dest, attr, uri)


def append_child_raw(parent, child, children):
    children.append(child)
    child.__dict__["parentNode"] = parent


def initialize_node_raw(node, args=(), namespace_uri=None):
    state = node.__dict__
    state["args"] = args
    state["kwargs"] = {}
    state["listeners"] = {}
    state["_listener_options"] = {}
    state["_baseURI"] = ""
    state["isConnected"] = True
    state["namespaceURI"] = namespace_uri or HTML_NAMESPACE
    state["outerText"] = None
    state["_ownerDocument"] = None
    state["parentNode"] = None
    state["prefix"] = None
    return node


def initialize_element_raw(element, namespace_uri):
    initialize_node_raw(element, namespace_uri=namespace_uri)
    state = element.__dict__
    state["lang"] = None
    state["tabIndex"] = None
    state["_Element__style"] = None
    state["shadowRoot"] = None
    state["dir"] = None
    return element


def create_text_raw(data):
    return initialize_node_raw(
        object.__new__(Text), ("" if data is None else str(data),)
    )


def create_comment_raw(data):
    comment = initialize_node_raw(object.__new__(Comment))
    comment.data = "" if data is None else str(data)
    return comment


def create_document_raw(namespace_uri, qualified_name, doctype):
    document = object.__new__(XMLDocument)
    initialize_element_raw(document, namespace_uri)
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
            "_doctype": doctype,
            "documentElement": document,
            "URL": "",
        }
    )
    if qualified_name:
        root = create_element_ns_raw(namespace_uri, qualified_name)
        document.__dict__["args"] = (root,)
        root.__dict__["parentNode"] = document
        document.__dict__["documentElement"] = root
    return document


def html_element_class(qualified_name):
    normalized_name = str(qualified_name).strip().lower()
    cached = _HTML_ELEMENT_CLASS_CACHE.get(normalized_name)
    if cached is not None:
        return cached

    html = importlib.import_module("domonic.html")

    if normalized_name in html._HTML_TAG_LOOKUP:
        tag_name = html._TAG_ALIASES.get(normalized_name, normalized_name)
        element_class = getattr(html, tag_name)
    else:
        element_class = _UNKNOWN_ELEMENT_CLASS_CACHE.get(normalized_name)
        if element_class is None:
            element_class = type(
                "custom_tag", (Element,), {"name": qualified_name}
            )
            _UNKNOWN_ELEMENT_CLASS_CACHE[normalized_name] = element_class

    _HTML_ELEMENT_CLASS_CACHE[normalized_name] = element_class
    return element_class


def svg_element_class(qualified_name):
    normalized_name = str(qualified_name).strip()
    cache_key = f"{SVG_NAMESPACE}:{normalized_name}"
    cached = _HTML_ELEMENT_CLASS_CACHE.get(cache_key)
    if cached is not None:
        return cached

    svg_module = importlib.import_module("domonic.svg")
    tag_name = getattr(svg_module, "_PYTHON_NAME_TO_TAG", {}).get(
        normalized_name, normalized_name
    )
    if tag_name in svg_module._SVG_TAG_LOOKUP:
        element_class = getattr(
            svg_module, svg_module._svg_class_name(tag_name)
        )
    else:
        element_class = _UNKNOWN_ELEMENT_CLASS_CACHE.get(cache_key)
        if element_class is None:
            element_class = type(
                "custom_tag", (Element,), {"name": normalized_name}
            )
            _UNKNOWN_ELEMENT_CLASS_CACHE[cache_key] = element_class

    _HTML_ELEMENT_CLASS_CACHE[cache_key] = element_class
    return element_class


def _namespace_for_tag(qualified_name, parent_namespace=None, parent_tag=""):
    normalized_name = str(qualified_name).split(":", 1)[-1].lower()
    if normalized_name == "svg":
        return SVG_NAMESPACE
    if normalized_name == "math":
        return MATHML_NAMESPACE
    if parent_namespace == SVG_NAMESPACE:
        if str(parent_tag).lower() == "foreignobject":
            return HTML_NAMESPACE
        return SVG_NAMESPACE
    if parent_namespace == MATHML_NAMESPACE:
        return MATHML_NAMESPACE
    return HTML_NAMESPACE


def create_element_ns_raw(namespace_uri, qualified_name):
    local_name = str(qualified_name).split(":", 1)[-1]
    namespace_uri = namespace_uri or _namespace_for_tag(qualified_name)
    if namespace_uri == SVG_NAMESPACE:
        element_class = svg_element_class(qualified_name)
        return initialize_element_raw(
            element_class.__new__(element_class), namespace_uri
        )
    if namespace_uri == MATHML_NAMESPACE:
        element_type = _MATHML_ELEMENT_CACHE.get(local_name)
        if element_type is None:
            element_type = type(
                local_name, (MathMLElement,), {"name": local_name}
            )
            _MATHML_ELEMENT_CACHE[local_name] = element_type
        return initialize_element_raw(
            element_type.__new__(element_type), namespace_uri
        )

    element_class = html_element_class(qualified_name)
    return initialize_element_raw(
        element_class.__new__(element_class), namespace_uri
    )


def adapt(source_tree, return_root=True, **kw):
    """Build a domonic tree from an lxml tree."""
    source_root = source_tree.getroot()
    uri, qname = elem_name_parts(source_root)
    uri = uri or _namespace_for_tag(qname)
    dest_tree = create_document_raw(uri, qname, source_tree.docinfo.doctype)
    dest_root = dest_tree.documentElement
    stack = [(source_root, dest_root, uri, qname)]

    while stack:
        src, dest, parent_namespace, parent_tag = stack.pop()
        children = []
        text = src.text
        if text:
            append_child_raw(dest, create_text_raw(text), children)
        add_namespace_declarations_raw(src, dest)
        for name, val in src.items():
            _, attr_name, attr_value = attr_name_parts(name, src, val)
            set_attribute_raw(dest, attr_name, attr_value)
        for child in src.iterchildren():
            if isinstance(child, _Comment):
                dchild = create_comment_raw(
                    (child.text or "").replace("--", "—")
                )
            else:
                child_uri, child_name = elem_name_parts(child)
                child_uri = child_uri or _namespace_for_tag(
                    child_name, parent_namespace, parent_tag
                )
                dchild = create_element_ns_raw(child_uri, child_name)
                stack.append((child, dchild, child_uri, child_name))
            append_child_raw(dest, dchild, children)
            tail = child.tail
            if tail:
                append_child_raw(dest, create_text_raw(tail), children)
        dest.__dict__["args"] = tuple(children)

    if return_root or (qname and qname.lower() == "html"):
        return dest_root
    return dest_tree
