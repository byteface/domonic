"""
domonic.ext.html_parser_
====================================

Adapter for Python's standard-library ``html.parser`` module.
"""

from __future__ import annotations

from html import unescape
from html.parser import HTMLParser
from typing import Any

from domonic.dom import Comment, Document, DocumentFragment, Node, Text


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


class DomonicHTMLParser(HTMLParser):
    """Build a domonic tree from stdlib ``HTMLParser`` callbacks."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.root = Document.createDocumentFragment()
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
            _append_child_raw(self.current, Text(data), self.child_stack[-1])

    def handle_comment(self, data: str) -> None:
        _append_child_raw(self.current, Comment(data), self.child_stack[-1])

    def handle_entityref(self, name: str) -> None:
        self.handle_data(unescape(f"&{name};"))

    def handle_charref(self, name: str) -> None:
        self.handle_data(unescape(f"&#{name};"))

    def _create_element(self, tag: str, attrs: list[tuple[str, str | None]]) -> Node:
        element = Document.createElement(tag)
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
