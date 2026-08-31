"""
domonic.ext.html_parser_
====================================

Adapter for Python's standard-library ``html.parser`` module.
"""

from __future__ import annotations

import importlib
from html import unescape
from html.parser import HTMLParser
from typing import Any

from domonic import dom
from domonic.dom import Comment, DocumentFragment, Element, Node, Text

_HTML_ELEMENT_CLASS_CACHE = {}
_UNKNOWN_ELEMENT_CLASS_CACHE = {}


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
    state["_baseURI"] = ""
    state["isConnected"] = True
    state["namespaceURI"] = "http://www.w3.org/1999/xhtml"
    state["outerText"] = None
    state["_ownerDocument"] = None
    state["parentNode"] = None
    state["prefix"] = None
    return node


def _initialize_element_raw(element: Element) -> Element:
    _initialize_node_raw(element)
    state = element.__dict__
    state["lang"] = None
    state["tabIndex"] = None
    state["_Element__style"] = None
    state["shadowRoot"] = None
    state["dir"] = None
    return element


def _html_element_class(name: str) -> type[Element]:
    normalized_name = str(name).strip().lower()
    cached = _HTML_ELEMENT_CLASS_CACHE.get(normalized_name)
    if cached is not None:
        return cached

    html = importlib.import_module("domonic.html")

    if normalized_name in html._HTML_TAG_LOOKUP:
        tag_name = html._TAG_ALIASES.get(normalized_name, normalized_name)
        element_class = getattr(html, tag_name)
    else:
        element_class = _UNKNOWN_ELEMENT_CLASS_CACHE.get(normalized_name)
        if element_class is None:
            element_class = type("custom_tag", (dom.Element,), {"name": name})
            _UNKNOWN_ELEMENT_CLASS_CACHE[normalized_name] = element_class

    _HTML_ELEMENT_CLASS_CACHE[normalized_name] = element_class
    return element_class


def _create_element_raw(name: str) -> Element:
    element_class = _html_element_class(name)
    return _initialize_element_raw(element_class.__new__(element_class))


def _create_text_raw(data: str) -> Text:
    return _initialize_node_raw(object.__new__(Text), (data,))


def _create_comment_raw(data: str) -> Comment:
    comment = _initialize_node_raw(object.__new__(Comment))
    comment.data = data
    return comment


def _create_fragment_raw() -> DocumentFragment:
    return _initialize_node_raw(object.__new__(DocumentFragment))


class DomonicHTMLParser(HTMLParser):
    """Build a domonic tree from stdlib ``HTMLParser`` callbacks."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.root = _create_fragment_raw()
        self.stack: list[Node] = [self.root]
        self.child_stack: list[list[Node]] = [[]]

    @property
    def current(self) -> Node:
        return self.stack[-1]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in AUTOCLOSE_SAME_START:
            self._close_open_element(tag)
        element = self._create_element(tag, attrs)
        _append_child_raw(self.current, element, self.child_stack[-1])
        if tag not in VOID_ELEMENTS:
            self.stack.append(element)
            self.child_stack.append([])

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
                return

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
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
        _append_child_raw(self.current, _create_comment_raw(data), self.child_stack[-1])

    def handle_entityref(self, name: str) -> None:
        self.handle_data(unescape(f"&{name};"))

    def handle_charref(self, name: str) -> None:
        self.handle_data(unescape(f"&#{name};"))

    def _create_element(self, tag: str, attrs: list[tuple[str, str | None]]) -> Node:
        element = _create_element_raw(tag)
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
