"""
domonic.ext.turbohtml_
====================================

Adapter for using turbohtml as a frontend parser while rebuilding a
domonic document tree directly from turbohtml's native tree.
"""

from __future__ import annotations

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
    _create_cdata_raw,
    _create_comment_raw,
    _create_document_raw,
    _create_doctype_parts_raw as _create_doctype_raw,
    _create_element_raw,
    _create_processing_instruction_raw,
    _create_text_raw,
    _element_class,
    _initialize_element_raw,
    _initialize_node_raw,
    _namespace_for_tag,
    _set_attribute_raw,
)


class _TurboTypes:
    def __init__(self, turbohtml: Any) -> None:
        self.Document = turbohtml.Document
        self.Doctype = turbohtml.Doctype
        self.Text = turbohtml.Text
        self.Comment = turbohtml.Comment
        self.CData = getattr(turbohtml, "CData", None)
        self.ProcessingInstruction = getattr(
            turbohtml, "ProcessingInstruction", None
        )
        self.Element = turbohtml.Element


def _normalize_attribute_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (list, tuple)):
        return " ".join(str(part) for part in value)
    return str(value)


def _set_attributes(element: dom.Element, attrs: Any) -> None:
    if not attrs:
        return
    for name, value in attrs.items():
        _set_attribute_raw(element, name, _normalize_attribute_value(value))



def _adapt_node(
    node: Any,
    types: _TurboTypes,
    parent_namespace: str = HTML_NAMESPACE,
    parent_tag: str = "",
    parent_encoding: str = "",
) -> Any:
    if isinstance(node, types.Document):
        document = _create_document_raw()
        children = []
        for child in getattr(node, "children", ()):
            if isinstance(child, types.Doctype):
                document.doctype = _adapt_node(child, types)
                continue
            adapted = _adapt_node(child, types)
            if adapted is not None:
                children.append(adapted)
        document.args = tuple(children)
        for child in children:
            if isinstance(child, dom.Node):
                child.parentNode = document
        html_root = next(
            (
                child
                for child in children
                if getattr(child, "tagName", "").lower() == "html"
            ),
            None,
        )
        if html_root is not None:
            document.documentElement = html_root
        return document

    if isinstance(node, types.Doctype):
        name = getattr(node, "name", None) or "html"
        return _create_doctype_raw(
            name,
            getattr(node, "public_id", None) or "",
            getattr(node, "system_id", None) or "",
        )

    if isinstance(node, types.Text):
        return _create_text_raw(node.data)

    if isinstance(node, types.Comment):
        return _create_comment_raw(node.data)

    if types.CData is not None and isinstance(node, types.CData):
        return _create_cdata_raw(node.data)

    if types.ProcessingInstruction is not None and isinstance(
        node, types.ProcessingInstruction
    ):
        return _create_processing_instruction_raw(
            getattr(node, "target", ""), node.data
        )

    if isinstance(node, types.Element):
        tag = node.tag
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
        _set_attributes(element, node.attrs)
        child_encoding = ""
        if namespace_uri == MATHML_NAMESPACE and tag == "annotation-xml":
            child_encoding = element.getAttribute("encoding") or ""
        children = []
        for child in getattr(node, "children", ()):
            adapted = _adapt_node(
                child, types, namespace_uri, tag, child_encoding
            )
            if adapted is not None:
                children.append(adapted)
                adapted.__dict__["parentNode"] = element
        element.__dict__["args"] = tuple(children)
        return element

    return None


def parse(source: Any, return_root: bool = True, **kwargs: Any) -> dom.Node:
    import turbohtml

    document = _adapt_node(
        turbohtml.parse("" if source is None else source, **kwargs),
        _TurboTypes(turbohtml),
    )
    if return_root:
        children = list(getattr(document, "childNodes", ()) or ())
        if len(children) == 1:
            return children[0]
    return document
