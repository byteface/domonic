"""
domonic.ext.html_parser_
====================================

Adapter for Python's standard-library ``html.parser`` module.
"""

from __future__ import annotations

import importlib
from html import unescape
from html.parser import HTMLParser
from typing import Any, cast

from domonic import dom
from domonic.dom import Comment, DocumentFragment, Element, Node, Text

HTML_NAMESPACE = "http://www.w3.org/1999/xhtml"
SVG_NAMESPACE = "http://www.w3.org/2000/svg"
MATHML_NAMESPACE = "http://www.w3.org/1998/Math/MathML"

_HTML_ELEMENT_CLASS_CACHE: dict[str, type[Element]] = {}
_UNKNOWN_ELEMENT_CLASS_CACHE: dict[str, type[Element]] = {}


VOID_ELEMENTS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}

AUTOCLOSE_SAME_START = {"dd", "dt", "li", "p"}


def _append_child_raw(parent: Node, child: Node, children: list[Node]) -> None:
    children.append(child)
    child.__dict__["parentNode"] = parent


def _set_attribute_raw(element: Node, name: str, value: str) -> None:
    if name and name[0] != "_":
        name = "_" + name
    element.__dict__["kwargs"][name] = value


def _initialize_node_raw(node: Node, args: tuple[Any, ...] = ()) -> Node:
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
    element: Element, namespace_uri: str = HTML_NAMESPACE
) -> Element:
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


def _element_class(name: str, namespace_uri: str) -> type[Element]:
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
) -> Element:
    element_class = _element_class(name, namespace_uri)
    return cast(
        Element,
        _initialize_element_raw(object.__new__(element_class), namespace_uri),
    )


def _create_text_raw(data: str) -> Text:
    return cast(Text, _initialize_node_raw(object.__new__(Text), (data,)))


def _create_comment_raw(data: str) -> Comment:
    comment = _initialize_node_raw(object.__new__(Comment))
    comment.data = data
    return cast(Comment, comment)


def _create_fragment_raw() -> DocumentFragment:
    return cast(
        DocumentFragment,
        _initialize_node_raw(object.__new__(DocumentFragment)),
    )


class DomonicHTMLParser(HTMLParser):
    """Build a domonic tree from stdlib ``HTMLParser`` callbacks."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.root = _create_fragment_raw()
        self.stack: list[Node] = [self.root]
        self.child_stack: list[list[Node]] = [[]]
        self.namespace_stack: list[str] = [HTML_NAMESPACE]

    @property
    def current(self) -> Node:
        return self.stack[-1]

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        tag = tag.lower()
        if tag in AUTOCLOSE_SAME_START:
            self._close_open_element(tag)
        element = self._create_element(tag, attrs)
        _append_child_raw(self.current, element, self.child_stack[-1])
        if tag not in VOID_ELEMENTS:
            self.stack.append(element)
            self.child_stack.append([])
            self.namespace_stack.append(element.namespaceURI)

    def handle_endtag(self, tag: str) -> None:
        self._close_open_element(tag.lower())

    def _close_open_element(self, tag: str) -> None:
        for index in range(len(self.stack) - 1, 0, -1):
            node = self.stack[index]
            if getattr(node, "tagName", "").lower() == tag:
                for close_index in range(len(self.stack) - 1, index - 1, -1):
                    self.stack[close_index].__dict__["args"] = tuple(
                        self.child_stack[close_index]
                    )
                del self.stack[index:]
                del self.child_stack[index:]
                del self.namespace_stack[index:]
                return

    def handle_startendtag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        _append_child_raw(
            self.current,
            self._create_element(tag, attrs),
            self.child_stack[-1],
        )

    def handle_data(self, data: str) -> None:
        if data:
            _append_child_raw(
                self.current, _create_text_raw(data), self.child_stack[-1]
            )

    def handle_comment(self, data: str) -> None:
        _append_child_raw(
            self.current, _create_comment_raw(data), self.child_stack[-1]
        )

    def handle_entityref(self, name: str) -> None:
        self.handle_data(unescape(f"&{name};"))

    def handle_charref(self, name: str) -> None:
        self.handle_data(unescape(f"&#{name};"))

    def _create_element(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> Node:
        parent_tag = getattr(self.current, "tagName", "")
        namespace_uri = _namespace_for_tag(
            tag, self.namespace_stack[-1], parent_tag
        )
        element = _create_element_raw(tag, namespace_uri)
        for name, value in attrs:
            _set_attribute_raw(element, name, name if value is None else value)
        return element


def parse(source: Any, return_root: bool = True, **kwargs: Any) -> Node:
    """Parse HTML with Python's stdlib parser and return domonic nodes."""
    parser = DomonicHTMLParser()
    parser.feed("" if source is None else str(source))
    parser.close()
    for index, node in enumerate(parser.stack):
        node.__dict__["args"] = tuple(parser.child_stack[index])
    children = list(parser.root.childNodes)
    if return_root and len(children) == 1:
        return children[0]
    return parser.root
