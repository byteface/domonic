"""
domonic._rendered_text
======================

``innerText`` / ``outerText`` (https://html.spec.whatwg.org/#the-innertext-idl-attribute):
an element's text as it renders.

There is no layout here, so "being rendered" and each box's ``display`` come
from the element's tag (the HTML rendering section's user-agent styles) unless
the page's CSS -- a stylesheet or a ``style`` attribute -- sets ``display``,
``visibility``, ``white-space``, ``text-transform``, ``float`` or
``position``. Hidden and non-rendered elements are skipped, white space
collapses as CSS collapses it, block edges become line breaks (two around a
``<p>``), ``<br>`` is a newline, and table cells and rows are separated by
tabs and newlines. Pseudo-elements (``::before``, ``::first-line``) and
anything that needs line layout are out of reach.
"""

from __future__ import annotations

import re
from typing import Any

# the HTML rendering section's display defaults (https://html.spec.whatwg.org/#rendering)
_NONE = frozenset(
    "area base basefont datalist head link meta noembed noframes noscript param rp script style template title".split()
)
_BLOCK = frozenset(
    "address article aside blockquote body center dd details dialog dir div dl dt fieldset figcaption figure footer "
    "form frameset h1 h2 h3 h4 h5 h6 header hgroup hr html legend listing main menu nav ol optgroup option p "
    "plaintext pre search section summary ul xmp".split()
)
_UA_DISPLAY = {
    "li": "list-item",
    "table": "table",
    "caption": "table-caption",
    "colgroup": "table-column-group",
    "col": "table-column",
    "thead": "table-header-group",
    "tbody": "table-row-group",
    "tfoot": "table-footer-group",
    "tr": "table-row",
    "td": "table-cell",
    "th": "table-cell",
    "ruby": "ruby",
    "rt": "ruby-text",
    "button": "inline-block",
    "select": "inline-block",
    "input": "inline-block",
    "textarea": "inline-block",
    "meter": "inline-block",
    "progress": "inline-block",
    "slot": "contents",
}
#: replaced elements: atomic inlines, and what's inside them isn't rendered as text
_REPLACED = frozenset("audio canvas embed iframe img input meter object progress textarea video".split())
#: SVG elements that are never rendered themselves (only referenced)
_SVG_NONE = frozenset(
    "clippath defs desc filter lineargradient marker mask metadata pattern radialgradient symbol title".split()
)
_PRE = frozenset(("pre", "listing", "plaintext", "xmp"))
#: tags whose user-agent style changes what they pass down
_STATE_TAGS = _PRE | {"nobr", "td", "th", "textarea", "select"}
_BLOCK_LEVEL = frozenset(("block", "list-item", "table", "flex", "grid", "flow-root", "table-caption"))
_ATOMIC_INLINE = frozenset(("inline-block", "inline-table", "inline-flex", "inline-grid", "inline flow-root"))
_ROW_GROUPS = frozenset(("table-header-group", "table-row-group", "table-footer-group"))
#: CSS Display 2.7 blockification: a float, an absolutely positioned box, a flex or grid item
_BLOCKIFIED = {
    "inline": "block",
    "inline-block": "block",
    "inline-table": "table",
    "inline-flex": "flex",
    "inline-grid": "grid",
    "inline flow-root": "flow-root",
    "ruby": "block",
}
_STYLE_PROPERTIES = (
    "display",
    "visibility",
    "white-space",
    "white-space-collapse",
    "text-transform",
    "float",
    "position",
)
_COLLAPSIBLE = re.compile(r"[ \t\n\r\f]+")
_SPACES = re.compile(r"[ \t\f]+")
_LINE_BREAK = re.compile(r"\r\n|[\n\r]")
_WORD_START = re.compile(r"(^|(?<=\s))(\w)")
_SVG_NAMESPACE = "http://www.w3.org/2000/svg"

#: the edges of a box that starts its own lines without breaking the line it
#: sits in (an inline-block, a replaced element, a table cell)
_OPEN = "open"
_CLOSE = "close"


class _State:
    """What an element passes down to its children: the inherited
    properties, and how its own box treats them."""

    __slots__ = ("visible", "white_space", "transform", "svg_text", "table_box", "in_select")

    def __init__(
        self,
        visible: bool = True,
        white_space: str = "normal",
        transform: str = "none",
        svg_text: bool = True,
        table_box: bool = False,
        in_select: bool = False,
    ) -> None:
        self.visible = visible
        self.white_space = white_space
        self.transform = transform
        self.svg_text = svg_text  # False inside an <svg> outside a <text>
        self.table_box = table_box  # a table, row group or row: white space between its cells isn't rendered
        self.in_select = in_select


def _tag(node: Any) -> str:
    return str(getattr(node, "localName", "") or "").lower()


def _is_table_box(display: str) -> bool:
    """A table, row group or row: white space between its parts isn't rendered."""
    return display in ("table", "inline-table", "table-row") or display in _ROW_GROUPS


class _Collector:
    def __init__(self, element: Any) -> None:
        from domonic.dom import Document, Element, Text

        self.Element, self.Document, self.Text = Element, Document, Text
        document = getattr(element, "ownerDocument", None)
        self.author_css = False
        try:
            self.author_css = bool(
                document is not None
                and (len(document.styleSheets or ()) or len(getattr(document, "adoptedStyleSheets", None) or ()))
            )
        except Exception:  # nosec B110 -- no stylesheets to read: tag defaults only
            self.author_css = False
        self.declarations: dict[int, dict[str, str]] = {}
        self.displays: dict[int, str] = {}
        self.last_of: dict[tuple[int, str], Any] = {}

    # -- styles ------------------------------------------------------------------

    def declared(self, element: Any) -> dict[str, str]:
        """The values the page's CSS sets on ``element`` for the properties
        rendered text depends on (empty when it sets none)."""
        key = id(element)
        if key in self.declarations:
            return self.declarations[key]
        values: dict[str, str] = {}
        if self.author_css or element.getAttribute("style"):
            try:
                from domonic.style import ComputedStyleDeclaration

                resolved = ComputedStyleDeclaration(element)._resolved
                for name in _STYLE_PROPERTIES:
                    if name in resolved._declared:
                        raw = str(resolved._declared[name])
                        if "var(" in raw or raw.startswith("\x00"):  # resolved by the cascade
                            raw = str(resolved.get(name) or "")
                        values[name] = raw.strip().lower()
            except Exception:  # nosec B110 -- an unreadable style: tag defaults only
                values = {}
        self.declarations[key] = values
        return values

    def display(self, element: Any, declared: dict[str, str] | None = None, tag: str | None = None) -> str:
        key = id(element)
        if key in self.displays:
            return self.displays[key]
        if declared is None:
            declared = self.declared(element)
        if tag is None:
            tag = _tag(element)
        value = self.ua_display(element, tag)
        if value != "none" or tag not in ("noscript", "template"):  # noscript: display:none !important
            author = " ".join(str(declared.get("display") or "").split())
            if author in ("initial", "unset"):
                value = "inline"
            elif author and author not in ("inherit", "revert", "revert-layer"):
                value = author
        if value not in ("none", "contents", "block"):
            floated = declared and declared.get("float") in ("left", "right", "inline-start", "inline-end")
            positioned = declared and declared.get("position") in ("absolute", "fixed")
            if floated or positioned or self.parent_is_flex(element):
                value = _BLOCKIFIED.get(value, "block" if value.startswith(("table-", "ruby-")) else value)
        self.displays[key] = value
        return value

    def parent_is_flex(self, element: Any) -> bool:
        parent = getattr(element, "parentNode", None)
        if not isinstance(parent, self.Element) or isinstance(parent, self.Document):
            return False
        display = self.display(parent)
        return "flex" in display or "grid" in display

    def ua_display(self, element: Any, tag: str) -> str:
        if tag in _NONE:
            return "none"
        hidden = element.getAttribute("hidden")
        if hidden is not None and hidden is not False:
            return "none"
        namespace = getattr(element, "namespaceURI", None)
        parent = getattr(element, "parentNode", None)
        if namespace == _SVG_NAMESPACE:
            return "none" if tag in _SVG_NONE else "inline"
        if getattr(parent, "namespaceURI", None) == _SVG_NAMESPACE and _tag(parent) != "foreignobject":
            return "none"  # an HTML element in SVG content isn't rendered
        if tag == "dialog" and element.getAttribute("open") in (None, False):
            return "none"
        if tag == "audio" and element.getAttribute("controls") in (None, False):
            return "none"
        if tag == "input" and str(element.getAttribute("type") or "").lower() == "hidden":
            return "none"
        if tag in _BLOCK:
            return "block"
        return _UA_DISPLAY.get(tag, "inline")

    def state(self, element: Any, parent: _State, declared: dict[str, str], display: str, tag: str) -> _State:
        table_box = _is_table_box(display)
        in_select = parent.in_select or tag == "select"
        if not declared and tag not in _STATE_TAGS and table_box == parent.table_box:
            if getattr(element, "namespaceURI", None) != _SVG_NAMESPACE:
                return parent  # nothing it changes
        visibility = declared.get("visibility")
        visible = parent.visible if visibility in (None, "inherit", "unset") else visibility == "visible"
        if visibility in ("initial", "revert", "revert-layer"):
            visible = True

        white_space = parent.white_space
        if tag in _PRE:
            white_space = "pre-wrap" if tag == "pre" and element.getAttribute("wrap") is not None else "pre"
        elif tag == "nobr" or (tag in ("td", "th") and element.getAttribute("nowrap") is not None):
            white_space = "nowrap"
        elif tag == "textarea":
            white_space = "pre-wrap"
        declared_space = declared.get("white-space")
        if declared_space and declared_space not in ("inherit", "unset"):
            white_space = "normal" if declared_space in ("initial", "revert", "revert-layer") else declared_space
        collapse = declared.get("white-space-collapse")
        if collapse in ("preserve", "break-spaces"):
            white_space = "pre-wrap"
        elif collapse == "preserve-breaks":
            white_space = "pre-line"
        elif collapse == "collapse":
            white_space = "normal"

        transform = parent.transform
        declared_transform = declared.get("text-transform")
        if declared_transform and declared_transform not in ("inherit", "unset"):
            transform = "none" if declared_transform in ("initial", "revert", "revert-layer") else declared_transform

        svg_text = parent.svg_text
        if getattr(element, "namespaceURI", None) == _SVG_NAMESPACE:
            svg_text = tag in ("text", "foreignobject") or (svg_text and tag != "svg")
        return _State(visible, white_space, transform, svg_text, table_box, in_select)

    def rendered_children(self, element: Any, display: str, tag: str, in_select: bool) -> list[Any]:
        """The children of ``element`` whose boxes it renders."""
        if tag in _REPLACED or tag == "template" or display in ("table-column", "table-column-group"):
            return []  # (a template's contents live in another document)
        children = list(getattr(element, "args", ()) or ())
        if in_select and tag in ("select", "optgroup"):
            return [child for child in children if isinstance(child, self.Element)]  # no bare text
        if tag == "details" and element.getAttribute("open") in (None, False):
            for child in children:
                if isinstance(child, self.Element) and _tag(child) == "summary":
                    return [child]
            return []
        return children

    # -- the rendered text collection steps -----------------------------------------

    def collect(self, node: Any, parent: _State, items: list, parent_node: Any) -> None:
        # Iterative, so a deep tree can't exhaust the recursion limit: a stack
        # of (children left to visit, their inherited state, their parent,
        # items to append once they are done). Hot path: names bound locally.
        text_type, element_type = self.Text, self.Element
        declared_of, display_of, state_of = self.declared, self.display, self.state
        rendered_children, add_text, is_last = self.rendered_children, self.text, self.is_last
        add, extend = items.append, items.extend
        stack: list[tuple[Any, _State, Any, list | None]] = [(iter((node,)), parent, parent_node, None)]
        while stack:
            children, parent, parent_node, after = stack[-1]
            for node in children:
                if isinstance(node, str) or isinstance(node, text_type):
                    if parent.visible and parent.svg_text:
                        text = node if isinstance(node, str) else str(node.data or "")
                        if not (parent.table_box and not text.strip(" \t\n\r\f")):  # white space between table parts
                            add_text(text, parent, items, parent_node)
                    continue
                if not isinstance(node, element_type):
                    continue  # comments, processing instructions
                tag = _tag(node)
                declared = declared_of(node)
                display = display_of(node, declared, tag)
                if display == "none":
                    continue
                state = state_of(node, parent, declared, display, tag)
                if state.visible and tag == "br":
                    add(("f", "\n"))
                    continue
                closing: list | None = None
                if state.visible and display != "contents":
                    edge = 2 if tag == "p" else 1 if display in _BLOCK_LEVEL or display.startswith("block") else 0
                    # a block's edges are line breaks; an inline-block's, a replaced
                    # element's or a table part's only start and end the lines inside it
                    if edge or display in _ATOMIC_INLINE or display.startswith("table") or tag in _REPLACED:
                        add(edge or _OPEN)
                        closing = [edge or _CLOSE]
                        if display == "table-cell" and not is_last(node, "table-cell"):
                            closing.append(("f", "\t"))
                        elif display == "table-row" and not is_last(node, "table-row"):
                            closing.append(("f", "\n"))
                kids = rendered_children(node, display, tag, state.in_select)
                if kids:
                    stack.append((iter(kids), state, node, closing))
                    break
                if closing:
                    extend(closing)
            else:
                stack.pop()
                if after:
                    extend(after)

    def text(self, text: str, state: _State, items: list, parent_node: Any) -> None:
        if not text:
            return
        if state.transform in ("uppercase", "lowercase") and any(char in text for char in "iIıİ"):
            if _language(parent_node) in ("tr", "az"):  # dotted and dotless i
                text = text.replace("i", "İ").replace("ı", "I") if state.transform == "uppercase" else text
                text = text.replace("I", "ı").replace("İ", "i") if state.transform == "lowercase" else text
        if state.transform == "uppercase":
            text = text.upper()
        elif state.transform == "lowercase":
            text = text.lower()
        elif state.transform == "capitalize":
            text = _WORD_START.sub(lambda match: match.group(2).upper(), text)
        white_space = state.white_space
        if white_space in ("pre", "pre-wrap", "break-spaces"):
            items.append(("p", text))
        elif white_space == "pre-line":
            for index, line in enumerate(_LINE_BREAK.split(text)):
                if index:
                    items.append(("f", "\n"))
                if line:
                    items.append(("c", _SPACES.sub(" ", line)))
        else:
            items.append(("c", _COLLAPSIBLE.sub(" ", text)))

    def is_last(self, node: Any, kind: str) -> bool:
        """Whether ``node`` is the last rendered cell of its row, or the last
        rendered row of its table."""
        container = getattr(node, "parentNode", None)
        if kind == "table-row":
            while isinstance(container, self.Element) and self.display(container) in _ROW_GROUPS:
                container = container.parentNode
        key = (id(container), kind)
        if key not in self.last_of:
            last = None
            for child in getattr(container, "args", ()) or ():
                if not isinstance(child, self.Element):
                    continue
                display = self.display(child)
                if display == kind:
                    last = child
                elif kind == "table-row" and display in _ROW_GROUPS:
                    for row in getattr(child, "args", ()) or ():
                        if isinstance(row, self.Element) and self.display(row) == kind:
                            last = row
            self.last_of[key] = last
        return self.last_of[key] is node

    # -- the element itself --------------------------------------------------------

    def own_state(self, element: Any) -> tuple[_State, str, str] | None:
        """``element``'s state (with its ancestors' inherited values), tag and
        display, or ``None`` when it is not being rendered."""
        chain = []
        node = element
        while isinstance(node, self.Element) and not isinstance(node, self.Document):
            chain.append(node)
            node = getattr(node, "parentNode", None)
        chain.reverse()
        state = _State()
        tag = display = ""
        for index, node in enumerate(chain):
            tag = _tag(node)
            declared = self.declared(node)
            display = self.display(node, declared, tag)
            if display == "none" or (index and not state.svg_text and node.namespaceURI != _SVG_NAMESPACE):
                return None
            if index:
                parent = chain[index - 1]
                parent_tag = _tag(parent)
                siblings = self.rendered_children(parent, self.display(parent), parent_tag, state.in_select)
                if not any(each is node for each in siblings):
                    return None
            state = self.state(node, state, declared, display, tag)
        return state, tag, display


def _language(node: Any) -> str:
    """The primary language subtag in effect at ``node`` (``lang``, inherited)."""
    while node is not None and hasattr(node, "getAttribute"):
        lang = node.getAttribute("lang")
        if isinstance(lang, str):
            return lang.split("-", 1)[0].lower()
        node = getattr(node, "parentNode", None)
    return ""


def _join(items: list) -> str:
    """Steps 4-7 of the innerText getter, plus the CSS white-space
    processing across text runs: a collapsible space after another, or at the
    start or end of a line, is removed; each run of required line break
    counts becomes that many newlines (none at the start or end)."""
    out: list[str] = []
    pending = -1
    line_start = True
    trailing_space = False  # out[-1] ends in a collapsible space
    opened: list[int] = []  # len(out) where each open inline box started

    def drop_trailing_space() -> None:
        out[-1] = out[-1][:-1]
        if not out[-1]:
            out.pop()

    for item in items:
        if type(item) is int:
            if trailing_space:
                drop_trailing_space()
                trailing_space = False
            pending = max(pending, item)
            line_start = True
            continue
        if item is _OPEN:
            opened.append(len(out))
            line_start = True
            continue
        if item is _CLOSE:
            if trailing_space and len(out) > (opened.pop() if opened else 0):
                drop_trailing_space()
            trailing_space = False  # the box sits between the spaces either side of it
            line_start = False
            continue
        kind, text = item
        if kind == "c" and text[:1] == " " and (line_start or trailing_space):
            text = text[1:]
        if not text:
            continue
        if pending > 0 and out:
            out.append("\n" * pending)
        pending = -1
        if kind == "f" and text == "\n" and trailing_space:
            drop_trailing_space()
        out.append(text)
        trailing_space = kind == "c" and text.endswith(" ")
        line_start = kind != "c" and text.endswith("\n")
    if trailing_space:
        drop_trailing_space()
    return "".join(out)


def inner_text(element: Any) -> str:
    """The innerText getter: the rendered text of ``element``, or its
    ``textContent`` when the element itself is not rendered."""
    collector = _Collector(element)
    own = collector.own_state(element)
    if own is None:
        return str(getattr(element, "textContent", "") or "")
    state, tag, display = own
    items: list = []
    for child in collector.rendered_children(element, display, tag, state.in_select):
        collector.collect(child, state, items, element)
    return _join(items)


def text_fragment(element: Any, value: Any) -> list[Any]:
    """The rendered text fragment for ``value``: its lines, with a ``<br>``
    for each line break (https://html.spec.whatwg.org/#rendered-text-fragment)."""
    from domonic.html import br

    text = "" if value is None else str(value)
    parts: list[Any] = []
    for index, line in enumerate(_LINE_BREAK.split(text)):
        if index:
            parts.append(br())
        if line:
            parts.append(line)
    return parts


def set_inner_text(element: Any, value: Any) -> None:
    """The innerText setter: replace the children with ``value``'s lines."""
    parts = text_fragment(element, value)
    if all(isinstance(part, str) for part in parts):
        element.textContent = "".join(parts)  # no line breaks: a plain text child
    else:
        element.replaceChildren(*parts)


def set_outer_text(element: Any, value: Any) -> None:
    """The outerText setter: replace the element itself with ``value``'s lines."""
    from domonic.dom import DOMException

    if getattr(element, "parentNode", None) is None:
        raise DOMException("The element has no parent.", "NoModificationAllowedError")
    element.replaceWith(*(text_fragment(element, value) or [""]))
