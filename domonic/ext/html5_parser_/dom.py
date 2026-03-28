#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: Apache 2.0 Copyright: 2017, Kovid Goyal <kovid at kovidgoyal.net>

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

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


def add_namespace_declarations(src, dest):
    changed = src.nsmap
    if changed:
        p = src.getparent()
        if p is not None:
            # Only add namespace declarations different from the parent's
            p = p.nsmap or {}
            changed = {k: v for k, v in dict_items(changed) if v != p.get(k)}
        for prefix, uri in dict_items(changed):
            attr = ("xmlns:" + prefix) if prefix else "xmlns"
            dest.setAttributeNS("xmlns", attr, uri)


def adapt(source_tree, return_root=True, **kw):
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
        append_child = dest.appendChild
        set_attribute_ns = dest.setAttributeNS

        text = src.text
        if text:
            append_child(create_text(text))
        add_namespace_declarations(src, dest)
        for name, val in src.items():
            set_attribute_ns(*attr_name_parts(name, src, val))
        for child in src.iterchildren():
            if isinstance(child, _Comment):
                dchild = create_comment((child.text or "").replace("--", "—"))
            else:
                dchild = create_element_ns(*elem_name_parts(child))
                stack.append((child, dchild))
            append_child(dchild)
            tail = child.tail
            if tail:
                append_child(create_text(tail))

    if return_root or (qname and qname.lower() == "html"):
        return dest_root
    return dest_tree
