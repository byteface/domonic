"""
domonic.ext.selectolax_
====================================

Adapter for using selectolax as a frontend parser while rebuilding a
domonic document tree directly from selectolax's native tree.
"""

from __future__ import annotations

import importlib
from typing import Any

from domonic import dom
from domonic.ext._rawdom import (
    HTML_INTEGRATION_ENCODINGS,
    HTML_NAMESPACE,
    MATHML_NAMESPACE,
    MATHML_TAG_NAMES,
    SVG_NAMESPACE,
    SVG_TAG_NAMES,
    _append_child_raw,
    _create_comment_raw,
    _create_document_raw,
    _create_doctype_raw,
    _create_element_raw,
    _create_text_raw,
    _element_class,
    _initialize_element_raw,
    _initialize_node_raw,
    _namespace_for_tag,
    _set_attribute_raw,
)


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
    parent_encoding: str = "",
) -> Any:
    tag = node.tag
    if not tag:
        return None
    if tag[0] == "-" or tag == "!doctype" or tag == "_comment":
        # Non-element node: text, comment or doctype (selectolax uses a ``-``
        # prefix / these literals for pseudo-nodes).
        if tag == "-text":
            text = node.text
            return _create_text_raw(text() if callable(text) else _node_text(node))
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
        if tag in ("-doctype", "!doctype"):
            return _create_doctype_raw(getattr(node, "html", ""))
        return None

    # Fast path: an HTML-namespaced parent with an ordinary HTML tag stays in
    # the HTML namespace, which is the overwhelming common case.
    if (
        parent_namespace == HTML_NAMESPACE
        and tag not in SVG_TAG_NAMES
        and tag not in MATHML_TAG_NAMES
        and tag != "svg"
        and tag != "math"
    ):
        namespace_uri = HTML_NAMESPACE
    else:
        namespace_uri = _namespace_for_tag(
            tag, parent_namespace, parent_tag, parent_encoding
        )
    element = _create_element_raw(tag, namespace_uri)
    attrs = node.attributes
    if attrs:
        kwargs = element.__dict__["kwargs"]
        for attr_name, value in attrs.items():
            key = attr_name if attr_name[:1] == "_" else "_" + attr_name
            kwargs[key] = "" if value is None else value

    # ``encoding`` only influences child namespaces at a MathML
    # ``annotation-xml`` integration point, so read it back only there rather
    # than once per child.
    child_encoding = ""
    if namespace_uri == MATHML_NAMESPACE and tag == "annotation-xml":
        child_encoding = element.getAttribute("encoding") or ""

    children: list[Any] = []
    child = node.child
    while child is not None:
        adapted = _adapt_node(child, namespace_uri, tag, child_encoding)
        if adapted is not None:
            children.append(adapted)
            adapted.__dict__["parentNode"] = element
        child = child.next
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
