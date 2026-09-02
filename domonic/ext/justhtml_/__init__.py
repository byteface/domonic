"""
domonic.ext.justhtml_
====================================

Adapter for using justhtml as a frontend parser, rebuilding a domonic
document tree directly from justhtml's native node tree.
"""

from __future__ import annotations

from typing import Any

from domonic import dom
from domonic.ext._rawdom import (
    HTML_NAMESPACE,
    MATHML_NAMESPACE,
    SVG_NAMESPACE,
    _create_comment_raw,
    _create_document_raw,
    _create_doctype_raw,
    _create_element_raw,
    _create_text_raw,
    _set_attribute_raw,
)

_NAMESPACE_URI = {
    "html": HTML_NAMESPACE,
    "svg": SVG_NAMESPACE,
    "math": MATHML_NAMESPACE,
    "mathml": MATHML_NAMESPACE,
}


def _adapt_node(node: Any) -> Any:
    kind = type(node).__name__
    if kind == "Text":
        return _create_text_raw(node.data)
    if kind == "Comment":
        return _create_comment_raw(node.data)

    name = getattr(node, "name", None)
    if not isinstance(name, str) or name in ("!doctype", "#doctype"):
        return None  # doctype handled separately from the document children

    namespace_uri = _NAMESPACE_URI.get(
        getattr(node, "namespace", None) or "html", HTML_NAMESPACE
    )
    element = _create_element_raw(name, namespace_uri)

    attrs = getattr(node, "attrs", None)
    if attrs:
        kwargs = element.__dict__["kwargs"]
        for attr_name, value in attrs.items():
            key = attr_name if attr_name[:1] == "_" else "_" + attr_name
            kwargs[key] = "" if value is None else value

    children: list[Any] = []
    for child in node.children or ():
        adapted = _adapt_node(child)
        if adapted is not None:
            adapted.__dict__["parentNode"] = element
            children.append(adapted)
    element.__dict__["args"] = tuple(children)
    return element


def _adapt_doctype(document_node: Any) -> Any:
    for child in getattr(document_node, "children", None) or ():
        name = getattr(child, "name", None)
        if type(child).__name__ == "Doctype" or (
            isinstance(name, str) and name in ("!doctype", "#doctype")
        ):
            serialized = getattr(child, "to_html", lambda: "")() or "<!doctype html>"
            return _create_doctype_raw(serialized)
        if isinstance(name, str):
            serialized = getattr(child, "_source_html", "") or ""
            if serialized[:9].lower() == "<!doctype":
                return _create_doctype_raw(serialized)
    return None


def parse(html: Any, return_root: bool = True, **kwargs: Any) -> dom.Node:
    from justhtml import JustHTML

    parsed = JustHTML("" if html is None else html, fragment=False, sanitize=False)
    root_node = parsed.root

    document = _create_document_raw()
    document.doctype = _adapt_doctype(root_node)

    children: list[Any] = []
    for child in getattr(root_node, "children", None) or ():
        adapted = _adapt_node(child)
        if adapted is not None:
            adapted.__dict__["parentNode"] = document
            children.append(adapted)
            if getattr(adapted, "name", "") == "html":
                document.documentElement = adapted
    document.__dict__["args"] = tuple(children)

    if return_root and len(children) == 1:
        return children[0]
    return document
