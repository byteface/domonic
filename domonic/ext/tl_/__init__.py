"""Adapt the optional Rust ``tl-parser`` tree directly to raw domonic nodes."""

from __future__ import annotations

import re
from html import unescape
from typing import Any

from domonic import dom
from domonic.ext._rawdom import (
    HTML_NAMESPACE,
    MATHML_TAG_NAMES,
    SVG_TAG_NAMES,
    _create_comment_raw,
    _create_document_raw,
    _create_doctype_raw,
    _create_element_raw,
    _create_text_raw,
    _namespace_for_tag,
    _new_node,
    _set_state,
)

_RAW_TEXT = {"script", "style", "xmp", "iframe", "noembed", "noframes", "plaintext"}
# The comment body is a tempered ``[\s\S]`` rather than ``.*?``: a lazy ``.*?``
# under DOTALL can match across ``-->`` boundaries, so a run of leading comments
# ``<!-- --><!-- -->...`` has exponentially many parses and a trailing near-miss
# doctype triggers catastrophic backtracking (ReDoS). ``(?:(?!-->)[\s\S])*``
# cannot cross a ``-->`` and keeps the match linear.
_DOCTYPE = re.compile(
    r"""\A\s*(?:<!--(?:(?!-->)[\s\S])*-->\s*)*"""
    r"""(<!doctype\s+(?:[^>"']|"[^"]*"|'[^']*')*>)""",
    re.IGNORECASE | re.DOTALL,
)


def parse(html: Any, return_root: bool = True, **kwargs: Any) -> dom.Node:
    """Build a DOM without reparsing; retain tl's native recovery semantics.

    ``tl-parser`` 0.7.12 requires Python 3.12+. It is imported only when this
    optional adapter is selected. The conversion uses only its public API.
    """
    import tl

    source = "" if html is None else html
    if isinstance(source, bytes):
        source = source.decode("utf-8")
    document = _create_document_raw()
    # tl does not expose doctype nodes, and its version detector only consumes
    # part of PUBLIC/SYSTEM declarations. Preserve the complete declaration
    # and exclude it from the input to avoid introducing spurious text nodes.
    match = _DOCTYPE.match(source)
    if match:
        declaration = match.group(1)
        doctype = _create_doctype_raw(declaration)
        tokens = re.findall(r""""[^"]*"|'[^']*'|[^\s<>]+""", declaration)
        if len(tokens) >= 4:
            kind = tokens[2].upper()
            if kind == "PUBLIC":
                doctype.publicId = tokens[3][1:-1]
                if len(tokens) >= 5:
                    doctype.systemId = tokens[4][1:-1]
            elif kind == "SYSTEM":
                doctype.systemId = tokens[3][1:-1]
        document.doctype = doctype
        source = source[: match.start(1)] + source[match.end(1) :]
    parsed = tl.parse(source)

    # Iterator frames finalize args once per element, without Python recursion.
    stack = [(iter(parsed.children()), document, [], HTML_NAMESPACE, "", "")]
    html_attribute_names = {}
    foreign_attribute_names = {}
    # Derive templates from the shared raw constructor, once per tag/namespace.
    # Only immutable defaults are reused; mutable node dictionaries stay private.
    # Documents keep their specialized initialization and are never cloned.
    element_templates = {}
    tag_info = {}
    while stack:
        iterator, parent, children, namespace, parent_tag, encoding = stack[-1]
        node = next(iterator, None)
        if node is None:
            parent.__dict__["args"] = tuple(children)
            stack.pop()
            continue
        kind = node.node_type()
        if kind == "element":
            tag = node.name()
            info = tag_info.get(tag)
            if info is None:
                normalized = tag.lower()
                ordinary_html = (
                    normalized not in SVG_TAG_NAMES
                    and normalized not in MATHML_TAG_NAMES
                    and normalized not in ("svg", "math")
                )
                # Keep the HTML template beside the tag metadata so the hot
                # path needs no second lookup or (tag, namespace) tuple.
                info = tag_info[tag] = [normalized, ordinary_html, None]
            normalized, ordinary_html, html_template = info
            if namespace == HTML_NAMESPACE and ordinary_html:
                child_namespace = HTML_NAMESPACE
            else:
                child_namespace = _namespace_for_tag(
                    normalized, namespace, parent_tag, encoding
                )
            if child_namespace == HTML_NAMESPACE:
                tag = normalized
            if child_namespace == HTML_NAMESPACE:
                cached = html_template
            else:
                cached = element_templates.get((tag, child_namespace))
            if cached is None:
                converted = _create_element_raw(tag, child_namespace)
                if not isinstance(converted, dom.Document):
                    template = converted.__dict__.copy()
                    for mutable in ("kwargs", "listeners", "_listener_options"):
                        del template[mutable]
                    cached = (type(converted), template)
                    if child_namespace == HTML_NAMESPACE:
                        info[2] = cached
                    else:
                        element_templates[(tag, child_namespace)] = cached
            else:
                element_class, template = cached
                converted = _new_node(element_class)
                state = template.copy()
                state["kwargs"] = {}
                state["listeners"] = {}
                state["_listener_options"] = {}
                _set_state(converted, "__dict__", state)
            attrs = converted.__dict__["kwargs"]
            attribute_names = (
                html_attribute_names
                if child_namespace == HTML_NAMESPACE
                else foreign_attribute_names
            )
            for name, value in node.attributes().items():
                key = attribute_names.get(name)
                if key is None:
                    key = name.lower() if child_namespace == HTML_NAMESPACE else name
                    key = key if key.startswith("_") else "_" + key
                    attribute_names[name] = key
                attrs[key] = (
                    unescape(value) if value and "&" in value else (value or "")
                )
            child_encoding = (
                attrs.get("_encoding", "") if normalized == "annotation-xml" else ""
            )
            native_children = node.children()
            if len(native_children) == 1 and native_children[0].node_type() == "text":
                text = native_children[0].inner_text()
                if "&" in text and not (
                    child_namespace == HTML_NAMESPACE and normalized in _RAW_TEXT
                ):
                    text = unescape(text)
                child = _create_text_raw(text)
                child.__dict__["parentNode"] = converted
                converted.__dict__["args"] = (child,)
            elif native_children:
                stack.append(
                    (
                        iter(native_children),
                        converted,
                        [],
                        child_namespace,
                        normalized,
                        child_encoding,
                    )
                )
            if parent is document and normalized == "html":
                document.documentElement = converted
        elif kind == "comment":
            text = node.outer_html()
            converted = _create_comment_raw(
                text[4:-3] if text.startswith("<!--") and text.endswith("-->") else text
            )
        else:
            # Only read a text leaf, never aggregated inner_text on an element.
            text = node.inner_text()
            if "&" in text and not (
                namespace == HTML_NAMESPACE and parent_tag in _RAW_TEXT
            ):
                text = unescape(text)
            converted = _create_text_raw(text)
        converted.__dict__["parentNode"] = parent
        children.append(converted)

    children = document.__dict__["args"]
    if return_root and len(children) == 1 and document.__dict__["_doctype"] is None:
        return children[0]
    return document
