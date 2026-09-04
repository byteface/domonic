"""
domonic.ext.html_parser_
====================================

Adapter for Python's standard-library ``html.parser`` module.
"""

from __future__ import annotations

from html import unescape
from html.parser import HTMLParser
from typing import Any

from domonic.dom import Element, Node
from domonic.ext._rawdom import (
    HTML_NAMESPACE,
    _append_child_raw,
    _create_comment_raw,
    _create_element_raw,
    _create_fragment_raw,
    _create_text_raw,
    _element_class,
    _initialize_element_raw,
    _initialize_node_raw,
    _namespace_for_tag,
    _set_attribute_raw,
)


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

# stdlib ``HTMLParser`` does no implied-tag handling, so a start tag that should
# close an open sibling is handled here. Each entry maps a start tag to the set
# of open tags it closes, and ``AUTOCLOSE_BOUNDARY`` names the containers that
# stop the search: ``<li>`` inside a ``<ul>`` inside a ``<li>`` starts a fresh
# item in the inner list, it does not reopen the outer one; ``<dd>`` closes an
# open ``<dt>`` or ``<dd>`` but not across a nested ``<dl>``.
AUTOCLOSE_ON_START = {
    "li": {"li"},
    "dd": {"dd", "dt"},
    "dt": {"dd", "dt"},
    "p": {"p"},
}
AUTOCLOSE_SAME_START = set(AUTOCLOSE_ON_START)
AUTOCLOSE_BOUNDARY = {
    "li": {"ul", "ol", "menu"},
    "dd": {"dl"},
    "dt": {"dl"},
}

# A ``<p>`` cannot contain flow-content block elements; starting one of these
# while a ``<p>`` is open closes the ``<p>`` first (HTML5 "close a p element").
CLOSES_OPEN_P = {
    "address", "article", "aside", "blockquote", "details", "div", "dl",
    "fieldset", "figcaption", "figure", "footer", "form", "h1", "h2", "h3",
    "h4", "h5", "h6", "header", "hgroup", "hr", "main", "menu", "nav", "ol",
    "p", "pre", "section", "table", "ul",
}


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

    _TABLE_SECTIONS = {"thead", "tbody", "tfoot"}

    def _open_implicit(self, tag: str) -> None:
        element = self._create_element(tag, [])
        _append_child_raw(self.current, element, self.child_stack[-1])
        self.stack.append(element)
        self.child_stack.append([])
        self.namespace_stack.append(element.namespaceURI)

    def _insert_implied_table_containers(self, tag: str) -> None:
        """The HTML tree builder inserts ``<tbody>`` / ``<tr>`` that the markup
        omits; stdlib ``HTMLParser`` does not, so do it here."""
        current = getattr(self.current, "tagName", "").lower()
        if tag in self._TABLE_SECTIONS or tag in ("caption", "colgroup"):
            if current in self._TABLE_SECTIONS:
                self._close_open_element(self._TABLE_SECTIONS)
            return
        if tag == "tr" and current == "table":
            self._open_implicit("tbody")
            return
        if tag in ("td", "th"):
            if current == "table":
                self._open_implicit("tbody")
                current = "tbody"
            if current in self._TABLE_SECTIONS:
                self._open_implicit("tr")

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        tag = tag.lower()
        self._insert_implied_table_containers(tag)
        if tag in AUTOCLOSE_ON_START:
            self._close_open_element(
                AUTOCLOSE_ON_START[tag], boundary=AUTOCLOSE_BOUNDARY.get(tag)
            )
        elif tag in CLOSES_OPEN_P and any(
            getattr(node, "tagName", "").lower() == "p" for node in self.stack[1:]
        ):
            self._close_open_element("p")
        element = self._create_element(tag, attrs)
        _append_child_raw(self.current, element, self.child_stack[-1])
        if tag not in VOID_ELEMENTS:
            self.stack.append(element)
            self.child_stack.append([])
            self.namespace_stack.append(element.namespaceURI)

    def handle_endtag(self, tag: str) -> None:
        self._close_open_element(tag.lower())

    def _close_open_element(
        self, tag: "str | set[str]", boundary: "set[str] | None" = None
    ) -> None:
        targets = {tag} if isinstance(tag, str) else tag
        for index in range(len(self.stack) - 1, 0, -1):
            name = getattr(self.stack[index], "tagName", "").lower()
            if name in targets:
                for close_index in range(len(self.stack) - 1, index - 1, -1):
                    self.stack[close_index].__dict__["args"] = tuple(
                        self.child_stack[close_index]
                    )
                del self.stack[index:]
                del self.child_stack[index:]
                del self.namespace_stack[index:]
                return
            if boundary and name in boundary:
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
        parent_encoding = ""
        if isinstance(self.current, Element):
            parent_encoding = self.current.getAttribute("encoding") or ""
        namespace_uri = _namespace_for_tag(
            tag, self.namespace_stack[-1], parent_tag, parent_encoding
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
