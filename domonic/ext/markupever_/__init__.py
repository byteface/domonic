"""
domonic.ext.markupever_
====================================

Adapter for using markupever (html5ever) as a frontend parser while
rebuilding a domonic document tree directly from its native tree.
"""

from __future__ import annotations

from typing import Any

from domonic import dom
from domonic.ext._rawdom import (
    _append_child_raw,
    _create_comment_raw,
    _create_doctype_parts_raw,
    _create_document_raw,
    _create_element_raw,
    _create_text_raw,
)


def _set_attributes(element: dom.Element, attrs: Any) -> None:
    if not attrs:
        return
    kwargs = element.__dict__["kwargs"]
    for name, value in zip(attrs.keys(), attrs.values()):
        prefix = name.prefix
        key = name.local if not prefix else prefix + ":" + name.local
        if key[:1] != "_":
            key = "_" + key
        kwargs[key] = "" if value is None else value


def _adapt_element(node: Any, element_type: type, text_type: type, comment_type: type) -> dom.Element:
    """Iterative walk: html5ever hands back exact namespaces, so no tag-name
    namespace inference is needed."""
    name = node.name
    root = _create_element_raw(name.local, name.ns)
    _set_attributes(root, node.attrs)
    stack = [(node, root)]
    pop = stack.pop
    push = stack.append
    while stack:
        source, dest = pop()
        children: list[Any] = []
        child = source.first_child
        while child is not None:
            kind = type(child)
            if kind is element_type:
                name = child.name
                adapted: Any = _create_element_raw(name.local, name.ns)
                _set_attributes(adapted, child.attrs)
                push((child, adapted))
            elif kind is text_type:
                adapted = _create_text_raw(child.content)
            elif kind is comment_type:
                adapted = _create_comment_raw(child.content)
            else:
                child = child.next_sibling
                continue
            _append_child_raw(dest, adapted, children)
            child = child.next_sibling
        dest.__dict__["args"] = tuple(children)
    return root


def parse(html: Any, return_root: bool = True, **kwargs: Any) -> dom.Node:
    import markupever
    from markupever.dom import Comment, Doctype, Element, Text

    tree = markupever.parse("" if html is None else html, markupever.HtmlOptions())

    document = _create_document_raw()
    children: list[Any] = []
    child = tree.root().first_child
    while child is not None:
        kind = type(child)
        if kind is Element:
            adapted = _adapt_element(child, Element, Text, Comment)
            _append_child_raw(document, adapted, children)
            if child.name.local == "html":
                document.documentElement = adapted
        elif kind is Doctype:
            document.doctype = _create_doctype_parts_raw(child.name, child.public_id, child.system_id)
        elif kind is Comment:
            _append_child_raw(document, _create_comment_raw(child.content), children)
        elif kind is Text:
            _append_child_raw(document, _create_text_raw(child.content), children)
        child = child.next_sibling
    document.__dict__["args"] = tuple(children)

    if return_root and len(children) == 1:
        return children[0]
    return document
