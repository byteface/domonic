"""Convert Reliq's native tree directly into domonic nodes without reparsing HTML."""

from __future__ import annotations

import sys
from functools import lru_cache
from html import unescape
from importlib import import_module
from importlib.metadata import PackageNotFoundError, version
from struct import Struct
from typing import Any

from domonic import dom
from domonic.ext._rawdom import (
    HTML_NAMESPACE,
    MATHML_TAG_NAMES,
    SVG_TAG_NAMES,
    _create_comment_raw,
    _create_doctype_raw,
    _create_document_raw,
    _create_element_raw,
    _create_text_raw,
    _namespace_for_tag,
    _set_attribute_raw,
)

_RAW_TEXT = {"script", "style", "xmp", "iframe", "noembed", "noframes", "plaintext"}


def parse(html: Any, return_root: bool = True, **kwargs: Any) -> dom.Node:
    """Parse with optional ``reliq``; preserve its tree and recovery semantics."""
    from reliq import reliq

    parsed = reliq("" if html is None else html)
    document = (
        _parse_native(parsed)
        if _native_api() is not None and parsed.single is None and parsed.compressed is None
        else _parse_public(parsed)
    )
    children = document.__dict__["args"]
    if return_root and len(children) == 1 and document.__dict__["_doctype"] is None:
        return children[0]
    return document


def _parse_public(parsed):
    from reliq import reliq

    document = _create_document_raw()

    def adapt(node, namespace=HTML_NAMESPACE, parent_tag="", encoding=""):
        if node.type == reliq.Type.tag:
            tag = node.name
            child_namespace = _namespace_for_tag(tag, namespace, parent_tag, encoding)
            element = _create_element_raw(tag, child_namespace)
            for name, value in node.attrib.items():
                _set_attribute_raw(element, name, unescape(value or ""))
            child_encoding = element.getAttribute("encoding") or "" if tag == "annotation-xml" else ""
            children = []
            for child in node.children(gen=True, type=None):
                converted = adapt(child, child_namespace, tag, child_encoding)
                if converted is not None:
                    converted.__dict__["parentNode"] = element
                    children.append(converted)
            element.__dict__["args"] = tuple(children)
            return element
        if node.type == reliq.Type.comment:
            source = str(node)
            if source[:9].lower() == "<!doctype":
                document.doctype = _create_doctype_raw(source)
                return None
            return _create_comment_raw(node.insides or "")
        text = str(node)
        return _create_text_raw(text if namespace == HTML_NAMESPACE and parent_tag in _RAW_TEXT else unescape(text))

    children = []
    for node in parsed.self(gen=True, type=None):
        converted = adapt(node)
        if converted is not None:
            converted.__dict__["parentNode"] = document
            children.append(converted)
            if getattr(converted, "name", "") == "html":
                document.documentElement = converted
    document.__dict__["args"] = tuple(children)
    return document


@lru_cache(maxsize=1)
def _native_api():
    # These are private bindings. Only use the version whose conversion API
    # has been checked; unknown releases retain the public traversal path.
    try:
        if version("reliq") != "0.0.48":
            return None
    except PackageNotFoundError:
        return None
    return import_module("reliq.reliq")


def _parse_native(parsed):
    """Walk the native preorder array once, without per-node Reliq wrappers.

    Bulk-read a checked packed layout; otherwise use Reliq's own ctypes
    conversion functions. ``parsed`` owns the source and native arrays until
    every string has been copied into the resulting DOM.
    """
    from ctypes import byref, string_at

    api = _native_api()
    document = _create_document_raw()
    if parsed.struct is None:
        return document
    source = parsed.struct.struct
    data = bytes(parsed.data)
    data_start = source.data
    source_ref = byref(source)
    node = api._reliq_hnode_struct()
    node_ref = byref(node)
    attribute = api._reliq_attrib_struct()
    attribute_ref = byref(attribute)
    convert_node = api.libreliq.reliq_chnode_conv
    convert_attribute = api.libreliq.reliq_cattrib_conv
    node_size = api.chnode_sz
    attribute_size = api.cattrib_sz

    packed = _packed_layout()
    if packed:
        records = _PACKED_NODE.iter_unpack(string_at(source.nodes, source.nodesl * node_size))
        sentinel = (0, 0, 0, source.attribsl, 0, 0, 0)
        following = next(records, sentinel)
        attributes = string_at(source.attribs, source.attribsl * attribute_size)
        unpack_attribute = _PACKED_ATTRIBUTE.unpack_from

    # (depth, element, children, namespace, tag, child encoding)
    stack = [(-1, document, [], HTML_NAMESPACE, "", "")]
    names = {}
    attribute_names = {}
    for index in range(source.nodesl):
        if packed:
            start, length, end, attr_start, depth, tag_length, tag_offset = following
            following = next(records, sentinel)
            attr_end = following[3]
            kind = 0 if tag_offset else (1 if end else 2)
        else:
            convert_node(source_ref, source.nodes + index * node_size, node_ref)
            depth = node.lvl
            kind = node.type
            start = node.all.b - data_start
            length = node.all.s
        while stack[-1][0] >= depth:
            _, element, children, _, _, _ = stack.pop()
            element.__dict__["args"] = tuple(children)
        _, parent, siblings, namespace, parent_tag, encoding = stack[-1]
        if kind == 0:
            if packed:
                tag_start = start + tag_offset
            else:
                tag_start = node.tag.b - data_start
                tag_length = node.tag.s
                attr_start = 0
                attr_end = node.attribsl
            raw_name = data[tag_start : tag_start + tag_length]
            tag = names.get(raw_name)
            if tag is None:
                tag = raw_name.decode()
                names[raw_name] = tag
            if (
                namespace == HTML_NAMESPACE
                and tag not in SVG_TAG_NAMES
                and tag not in MATHML_TAG_NAMES
                and tag not in ("svg", "math")
            ):
                child_namespace = HTML_NAMESPACE
            else:
                child_namespace = _namespace_for_tag(tag, namespace, parent_tag, encoding)
            converted = _create_element_raw(tag, child_namespace)
            attrs = converted.__dict__["kwargs"]
            for attr_index in range(attr_start, attr_end):
                if packed:
                    key_start, value_bits, key_length = unpack_attribute(attributes, attr_index * attribute_size)
                    value_length = value_bits & 0xFFFFFF
                    value_start = key_start + key_length + (value_bits >> 24)
                else:
                    convert_attribute(
                        source_ref,
                        node.attribs + attr_index * attribute_size,
                        attribute_ref,
                    )
                    key_start = attribute.key.b - data_start
                    key_length = attribute.key.s
                    value_length = attribute.value.s
                    value_start = attribute.value.b - data_start if value_length else 0
                raw_key = data[key_start : key_start + key_length]
                key = attribute_names.get(raw_key)
                if key is None:
                    key = raw_key.decode().lower()
                    attribute_names[raw_key] = key
                if value_length:
                    value = data[value_start : value_start + value_length].decode()
                else:
                    value = ""
                previous = attrs.get(key)
                attrs[key] = previous + " " + value if previous else value
            # Match Reliq's duplicate-attribute concatenation before decoding
            # entities or applying domonic's underscore attribute convention.
            converted.__dict__["kwargs"] = attrs = {
                key if key.startswith("_") else "_" + key: (unescape(value) if "&" in value else value)
                for key, value in attrs.items()
            }
            child_encoding = attrs.get("_encoding", "") if tag == "annotation-xml" else ""
            stack.append((depth, converted, [], child_namespace, tag, child_encoding))
            if parent is document and tag == "html":
                document.documentElement = converted
        elif kind == 1:
            text = data[start : start + length].decode()
            if text[:9].lower() == "<!doctype":
                document.doctype = _create_doctype_raw(text)
                continue
            if packed:
                comment_start = start + tag_length
                comment_length = end - tag_length
            else:
                comment_length = node.insides.s
                comment_start = node.insides.b - data_start if comment_length else 0
            converted = _create_comment_raw(data[comment_start : comment_start + comment_length].decode())
        else:
            text = data[start : start + length].decode()
            if "&" in text and not (namespace == HTML_NAMESPACE and parent_tag in _RAW_TEXT):
                text = unescape(text)
            converted = _create_text_raw(text)
        converted.__dict__["parentNode"] = parent
        siblings.append(converted)
    for _, element, children, _, _, _ in reversed(stack):
        element.__dict__["args"] = tuple(children)
    return document


# Reliq 0.0.48, RELIQ_HTML_SIZE=1: packed node header and packed attribute.
# Layout checked against that distribution's src/lib/reliq.h and hnode.c.
# The 11 trailing node bytes contain descendant counters, which this walk
# does not need. Never apply this layout to unrecognized builds.
_PACKED_NODE = Struct("<IIIIHHB11x")
_PACKED_ATTRIBUTE = Struct("<IIB")


@lru_cache(maxsize=1)
def _packed_layout():
    from ctypes import string_at

    api = _native_api()
    if api is None or sys.byteorder != "little" or (api.chnode_sz, api.cattrib_sz) != (32, 9):
        return False
    # Check field offsets as well as sizes before reading actual input. The
    # fallback uses Reliq's own conversion functions, including on other ABIs.
    probe = api.reliq('<p x="one">text</p>')
    source = probe.struct.struct
    nodes = list(_PACKED_NODE.iter_unpack(string_at(source.nodes, source.nodesl * api.chnode_sz)))
    attrs = list(_PACKED_ATTRIBUTE.iter_unpack(string_at(source.attribs, source.attribsl * api.cattrib_sz)))
    return nodes == [(0, 19, 13, 0, 0, 1, 1), (11, 4, 0, 1, 1, 0, 0)] and attrs == [(3, (2 << 24) | 3, 1)]
