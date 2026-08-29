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


class DomonicHTMLParser(HTMLParser):
    """Build a domonic tree from stdlib ``HTMLParser`` callbacks."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.root = Document.createDocumentFragment()
        self.stack: list[Node] = [self.root]

    @property
    def current(self) -> Node:
        return self.stack[-1]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in AUTOCLOSE_SAME_START:
            self._close_open_element(tag)
        element = self._create_element(tag, attrs)
        self.current.appendChild(element)
        if tag not in VOID_ELEMENTS:
            self.stack.append(element)

    def handle_endtag(self, tag: str) -> None:
        self._close_open_element(tag.lower())

    def _close_open_element(self, tag: str) -> None:
        for index in range(len(self.stack) - 1, 0, -1):
            node = self.stack[index]
            if getattr(node, "tagName", "").lower() == tag:
                del self.stack[index:]
                return

    def handle_startendtag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        self.current.appendChild(self._create_element(tag, attrs))

    def handle_data(self, data: str) -> None:
        if data:
            self.current.appendChild(Text(data))

    def handle_comment(self, data: str) -> None:
        self.current.appendChild(Comment(data))

    def handle_entityref(self, name: str) -> None:
        self.handle_data(unescape(f"&{name};"))

    def handle_charref(self, name: str) -> None:
        self.handle_data(unescape(f"&#{name};"))

    def _create_element(self, tag: str, attrs: list[tuple[str, str | None]]) -> Node:
        element = Document.createElement(tag)
        for name, value in attrs:
            element.setAttribute(name, name if value is None else value)
        return element


def parse(source: Any, return_root: bool = True, **kwargs: Any) -> Node:
    """Parse HTML with Python's stdlib parser and return domonic nodes."""
    parser = DomonicHTMLParser()
    parser.feed("" if source is None else str(source))
    parser.close()
    children = list(parser.root.childNodes)
    if return_root and len(children) == 1:
        return children[0]
    return parser.root
