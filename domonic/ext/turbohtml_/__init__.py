"""
domonic.ext.turbohtml_
====================================

Adapter for using turbohtml as a frontend parser while rebuilding a
domonic document tree directly from turbohtml's native tree.
"""

from __future__ import annotations

import importlib
from typing import Any, cast

from domonic import dom

HTML_NAMESPACE = "http://www.w3.org/1999/xhtml"
SVG_NAMESPACE = "http://www.w3.org/2000/svg"
MATHML_NAMESPACE = "http://www.w3.org/1998/Math/MathML"

_HTML_ELEMENT_CLASS_CACHE: dict[str, type[dom.Element]] = {}
_UNKNOWN_ELEMENT_CLASS_CACHE: dict[str, type[dom.Element]] = {}


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


def _set_attribute_raw(element: dom.Element, name: str, value: Any) -> None:
    if name and name[0] != "_":
        name = "_" + name
    element.__dict__["kwargs"][name] = value


def _normalize_attribute_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (list, tuple)):
        return " ".join(str(part) for part in value)
    return str(value)


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


def _set_attributes(element: dom.Element, attrs: Any) -> None:
    if not attrs:
        return
    for name, value in attrs.items():
        _set_attribute_raw(element, name, _normalize_attribute_value(value))


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


def _create_cdata_raw(data: Any) -> dom.CDATASection:
    cdata = _initialize_node_raw(object.__new__(dom.CDATASection))
    cdata.data = "" if data is None else str(data)
    return cast(dom.CDATASection, cdata)


def _create_processing_instruction_raw(
    target: Any, data: Any
) -> dom.ProcessingInstruction:
    instruction = _initialize_node_raw(
        object.__new__(dom.ProcessingInstruction)
    )
    instruction.target = "" if target is None else str(target)
    instruction.data = "" if data is None else str(data)
    return cast(dom.ProcessingInstruction, instruction)


def _create_doctype_raw(
    name: Any, public_id: Any, system_id: Any
) -> dom.DocumentType:
    doctype = _initialize_node_raw(object.__new__(dom.DocumentType))
    doctype.name = name or "html"
    doctype.publicId = public_id or ""
    doctype.systemId = system_id or ""
    doctype._internalSubset = None
    doctype._entities = dom.NamedNodeMap()
    doctype._notations = dom.NamedNodeMap()
    return cast(dom.DocumentType, doctype)


def _adapt_node(
    node: Any,
    types: _TurboTypes,
    parent_namespace: str = HTML_NAMESPACE,
    parent_tag: str = "",
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
        namespace_uri = _namespace_for_tag(
            node.tag, parent_namespace, parent_tag
        )
        element = _create_element_raw(node.tag, namespace_uri)
        _set_attributes(element, node.attrs)
        children = []
        for child in getattr(node, "children", ()):
            adapted = _adapt_node(child, types, namespace_uri, node.tag)
            if adapted is not None:
                _append_child_raw(element, adapted, children)
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
