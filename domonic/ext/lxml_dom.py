#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: Apache 2.0 Copyright: 2017, Kovid Goyal <kovid at kovidgoyal.net>
"""Adapt lxml trees into ordinary domonic DOM nodes."""

# Based on domonic.ext.html5_parser_.dom, originally adapted from
# html5_parser's Apache-2.0 tree adapter by Kovid Goyal.

from __future__ import annotations

from lxml.etree import _Comment

from domonic.dom import DOMImplementation

impl = DOMImplementation()

try:
    dict_items = dict.iteritems
except AttributeError:
    dict_items = dict.items

_ELEM_NAME_CACHE = {}


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
        for prefix, quri in dict_items(elem.nsmap):
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
                for key, value in dict_items(changed)
                if value != parent_namespaces.get(key)
            }
        for prefix, uri in dict_items(changed):
            attr = ("xmlns:" + prefix) if prefix else "xmlns"
            set_attribute_raw(dest, attr, uri)


def append_child_raw(parent, child, children):
    children.append(child)
    child.__dict__["parentNode"] = parent


def adapt(source_tree, return_root=True, **kw):
    """Build a domonic tree from an lxml tree."""
    source_root = source_tree.getroot()
    uri, qname = elem_name_parts(source_root)
    dest_tree = impl.createDocument(uri, qname, None)
    dest_tree.doctype = source_tree.docinfo.doctype
    dest_root = dest_tree.documentElement
    create_text = dest_tree.createTextNode
    create_comment = dest_tree.createComment
    create_element_ns = dest_tree.createElementNS
    stack = [(source_root, dest_root)]

    while stack:
        src, dest = stack.pop()
        children = []
        text = src.text
        if text:
            append_child_raw(dest, create_text(text), children)
        add_namespace_declarations_raw(src, dest)
        for name, val in src.items():
            _, attr_name, attr_value = attr_name_parts(name, src, val)
            set_attribute_raw(dest, attr_name, attr_value)
        for child in src.iterchildren():
            if isinstance(child, _Comment):
                dchild = create_comment((child.text or "").replace("--", "—"))
            else:
                dchild = create_element_ns(*elem_name_parts(child))
                stack.append((child, dchild))
            append_child_raw(dest, dchild, children)
            tail = child.tail
            if tail:
                append_child_raw(dest, create_text(tail), children)
        dest.__dict__["args"] = tuple(children)

    if return_root or (qname and qname.lower() == "html"):
        return dest_root
    return dest_tree
