"""
domonic.bs4
===========

Beautiful Soup 4 style convenience methods for domonic nodes.

Importing this module opt-in patches a small, familiar BS4 API onto domonic's
real DOM classes. Returned objects remain normal domonic nodes, not wrappers.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from typing import Any

from domonic import domonic
from domonic.dom import Comment, Document, DocumentFragment, Element, Node, Text


_PARSER_ALIASES = {
    None: "auto",
    "": "auto",
    "auto": "auto",
    "html.parser": "html.parser",
    "html5lib": "html5lib",
    "lxml": "lxml_html",
    "lxml-html": "lxml_html",
    "lxml_html": "lxml_html",
    "html5_parser": "html5_parser",
    "html5-parser": "html5_parser",
    "markupever": "markupever",
    "selectolax": "selectolax",
    "justhtml": "justhtml",
    "expat": "expat",
}


_SIMPLE_FILTER_TYPES = (str, type(None))


class BeautifulSlop:
    """Parse markup and return a domonic tree with BS4-style helpers."""

    def __new__(
        cls,
        markup: str = "",
        features: str | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> Node:
        install()
        parser = _normalize_parser(features or kwargs.pop("parser", None))
        return domonic.parseString(markup, parser=parser)


def _normalize_parser(parser: str | None) -> str:
    try:
        return _PARSER_ALIASES[parser.lower() if isinstance(parser, str) else parser]
    except KeyError as exc:
        raise ValueError(f"Unknown BeautifulSlop parser: {parser}") from exc


def _tag_name(node: Any) -> str | None:
    if isinstance(node, Element):
        return getattr(node, "tagName", getattr(node, "name", None))
    if isinstance(node, Document):
        return "[document]"
    return None


def _iter_child_nodes(node: Any) -> Iterator[Any]:
    yield from getattr(node, "args", ()) or ()


def _descendants(node: Any) -> Iterator[Any]:
    for child in _iter_child_nodes(node):
        yield child
        if isinstance(child, Node) and not isinstance(child, (Text, Comment)):
            yield from _descendants(child)


def _document_order(root: Any) -> list[Any]:
    nodes = [root]
    nodes.extend(_descendants(root))
    return nodes


def _element_descendants(node: Any) -> Iterator[Element]:
    for child in _iter_child_nodes(node):
        if isinstance(child, Element):
            yield child
            yield from _element_descendants(child)
        elif isinstance(child, Node) and not isinstance(child, (Text, Comment)):
            yield from _element_descendants(child)


def _element_children(node: Any) -> Iterator[Element]:
    for child in _iter_child_nodes(node):
        if isinstance(child, Element):
            yield child


def _find_element_by_id(
    node: Any,
    element_id: str,
    include_self: bool = False,
) -> Element | None:
    if (
        include_self
        and isinstance(node, Element)
        and node.getAttribute("id") == element_id
    ):
        return node
    for child in _element_descendants(node):
        if child.getAttribute("id") == element_id:
            return child
    return None


def _attribute_name(name: str) -> str:
    if name == "class_":
        return "class"
    if name.endswith("_") and not name.startswith("_"):
        return name[:-1]
    return name


def _attribute_dict(node: Any) -> dict[str, Any]:
    if not isinstance(node, Element):
        return {}
    return {
        key[1:] if key.startswith("_") else key: value
        for key, value in getattr(node, "kwargs", {}).items()
    }


def _filter_matches(value: Any, candidate: Any, node: Any | None = None) -> bool:
    if value is True:
        return candidate is not None
    if value is None:
        return candidate is None
    if isinstance(value, (list, tuple, set)):
        return any(_filter_matches(item, candidate, node) for item in value)
    if hasattr(value, "search"):
        return candidate is not None and value.search(str(candidate)) is not None
    if callable(value):
        for arg in (candidate, node):
            try:
                return bool(value(arg))
            except TypeError:
                continue
        return False
    return str(candidate) == str(value)


def _class_filter_matches(value: Any, candidate: Any, node: Any | None = None) -> bool:
    if value is None:
        return candidate is None
    if candidate is None:
        return value is False
    class_value = str(candidate)
    tokens = class_value.split()
    if value is True:
        return bool(tokens)
    if isinstance(value, (list, tuple, set)):
        return any(_class_filter_matches(item, candidate, node) for item in value)
    if hasattr(value, "search"):
        return value.search(class_value) is not None or any(
            value.search(token) is not None for token in tokens
        )
    if callable(value):
        for arg in (class_value, *tokens, node):
            try:
                if value(arg):
                    return True
            except TypeError:
                continue
        return False
    expected_tokens = str(value).split()
    if not expected_tokens:
        return False
    return all(token in tokens for token in expected_tokens)


def _name_matches(name: Any, node: Any) -> bool:
    if not isinstance(node, Element):
        return False
    candidate = _tag_name(node)
    if name is None or name is True:
        return True
    if isinstance(name, (list, tuple, set)):
        return any(_name_matches(item, node) for item in name)
    if hasattr(name, "search"):
        return candidate is not None and name.search(candidate) is not None
    if callable(name):
        for arg in (node, candidate):
            try:
                return bool(name(arg))
            except TypeError:
                continue
        return False
    return candidate == str(name)


def _merge_attrs(attrs: dict[str, Any] | None, kwargs: dict[str, Any]) -> dict[str, Any]:
    merged = dict(attrs or {})
    for key, value in kwargs.items():
        merged[_attribute_name(key)] = value
    return merged


def _attributes_match(node: Any, attrs: dict[str, Any] | None) -> bool:
    if not isinstance(node, Element):
        return False
    if not attrs:
        return True
    for name, expected in attrs.items():
        public_name = _attribute_name(name)
        candidate = node.getAttribute(public_name)
        matcher = _class_filter_matches if public_name == "class" else _filter_matches
        if not matcher(expected, candidate, node):
            return False
    return True


def _own_string(node: Any) -> str | None:
    if isinstance(node, Text):
        return node.data
    if isinstance(node, str):
        return node
    children = list(_iter_child_nodes(node))
    if len(children) != 1:
        return None
    child = children[0]
    if isinstance(child, (str, Text)):
        return _string_value(child)
    return None


def _string_value(node: Any) -> str | None:
    if isinstance(node, Text):
        return node.data
    if isinstance(node, str):
        return node
    own = _own_string(node)
    if own is not None:
        return _string_value(own)
    return None


def _string_matches(string: Any, node: Any) -> bool:
    if string is None:
        return True
    value = _string_value(node)
    return _filter_matches(string, value, node)


def _matches(
    node: Any,
    name: Any = None,
    attrs: dict[str, Any] | None = None,
    string: Any = None,
) -> bool:
    if name is None and not attrs and string is not None:
        return isinstance(node, (str, Text)) and _string_matches(string, node)
    return (
        _name_matches(name, node)
        and _attributes_match(node, attrs)
        and _string_matches(string, node)
    )


def _can_use_css(name: Any, attrs: dict[str, Any] | None, string: Any) -> bool:
    if string is not None:
        return False
    if not isinstance(name, _SIMPLE_FILTER_TYPES):
        return False
    if not attrs:
        return True
    return all(
        value is not None and isinstance(value, _SIMPLE_FILTER_TYPES)
        for value in attrs.values()
    )


def _css_escape_value(value: Any) -> str:
    return str(value).replace("\\", "\\\\").replace('"', '\\"')


def _css_from_filters(name: str | None, attrs: dict[str, Any] | None) -> str:
    selector = name or "*"
    for attr, value in (attrs or {}).items():
        public_name = _attribute_name(attr)
        if value is None:
            continue
        if value is True:
            selector += f"[{public_name}]"
        elif public_name == "id":
            selector += f"#{value}"
        elif public_name == "class":
            selector += "".join(f".{part}" for part in str(value).split())
        else:
            selector += f'[{public_name}="{_css_escape_value(value)}"]'
    return selector


def _search_nodes(
    node: Any,
    name: Any = None,
    attrs: dict[str, Any] | None = None,
    recursive: bool = True,
    string: Any = None,
) -> Iterator[Any]:
    children = _descendants(node) if recursive else _iter_child_nodes(node)
    for child in children:
        if _matches(child, name, attrs, string):
            yield child


def _candidate_nodes(
    node: Any,
    name: Any = None,
    recursive: bool = True,
    string: Any = None,
) -> Iterator[Any] | None:
    if string is not None or not isinstance(name, (str, type(None))):
        return None
    if not recursive:
        return _iter_child_nodes(node)
    if name is None:
        return _element_descendants(node)
    tag_name = name.lower()
    return (
        candidate
        for candidate in _element_descendants(node)
        if candidate.tagName.lower() == tag_name
    )


def _limit(items: Iterable[Any], limit: int | None = None) -> list[Any]:
    if limit is None:
        return list(items)
    out = []
    for item in items:
        out.append(item)
        if len(out) >= limit:
            break
    return out


def _string_alias(string: Any, kwargs: dict[str, Any]) -> Any:
    if string is None and "text" in kwargs:
        return kwargs.pop("text")
    return string


def _find(
    self: Node,
    name: Any = None,
    attrs: dict[str, Any] | None = None,
    recursive: bool = True,
    string: Any = None,
    **kwargs: Any,
) -> Any | None:
    string = _string_alias(string, kwargs)
    found = _find_all(self, name, attrs, recursive, string, limit=1, **kwargs)
    return found[0] if found else None


def _find_all(
    self: Node,
    name: Any = None,
    attrs: dict[str, Any] | None = None,
    recursive: bool = True,
    string: Any = None,
    limit: int | None = None,
    **kwargs: Any,
) -> list[Any]:
    string = _string_alias(string, kwargs)
    merged_attrs = _merge_attrs(attrs, kwargs)
    if recursive and _can_use_css(name, merged_attrs, string):
        selector = _css_from_filters(name, merged_attrs)
        try:
            return _limit(self.querySelectorAll(selector), limit)
        except Exception:
            pass
    candidates = _candidate_nodes(self, name, recursive, string)
    if candidates is not None:
        return _limit(
            (node for node in candidates if _matches(node, name, merged_attrs, string)),
            limit,
        )
    return _limit(_search_nodes(self, name, merged_attrs, recursive, string), limit)


def _find_child(
    self: Node,
    name: Any = None,
    attrs: dict[str, Any] | None = None,
    string: Any = None,
    **kwargs: Any,
) -> Any | None:
    return _find(self, name, attrs, recursive=False, string=string, **kwargs)


def _find_children(
    self: Node,
    name: Any = None,
    attrs: dict[str, Any] | None = None,
    limit: int | None = None,
    string: Any = None,
    **kwargs: Any,
) -> list[Any]:
    return _find_all(
        self,
        name,
        attrs,
        recursive=False,
        string=string,
        limit=limit,
        **kwargs,
    )


def _split_simple_selector_chain(selector: str) -> list[tuple[str | None, str]] | None:
    parts: list[tuple[str | None, str]] = []
    token = []
    combinator: str | None = None
    bracket_depth = 0
    quote: str | None = None
    pending_space = False

    for char in selector.strip():
        if quote:
            token.append(char)
            if char == quote:
                quote = None
            continue
        if char in ("'", '"'):
            token.append(char)
            quote = char
            continue
        if char == "[":
            bracket_depth += 1
            token.append(char)
            continue
        if char == "]":
            bracket_depth -= 1
            if bracket_depth < 0:
                return None
            token.append(char)
            continue
        if bracket_depth:
            token.append(char)
            continue
        if char == ">":
            current = "".join(token).strip()
            if not current:
                return None
            parts.append((combinator, current))
            token = []
            combinator = ">"
            pending_space = False
            continue
        if char.isspace():
            if token:
                pending_space = True
            continue
        if pending_space:
            current = "".join(token).strip()
            if not current:
                return None
            parts.append((combinator, current))
            token = []
            combinator = " "
            pending_space = False
        token.append(char)

    current = "".join(token).strip()
    if not current or bracket_depth or quote:
        return None
    parts.append((combinator, current))
    return parts


def _match_parsed_selector(element: Element, parsed: dict[str, Any]) -> bool:
    tag_name = parsed["tag"]
    if tag_name != "*" and element.tagName.lower() != tag_name.lower():
        return False
    if parsed["id"] is not None and element.getAttribute("id") != parsed["id"]:
        return False
    class_tokens = set(str(element.getAttribute("class") or "").split())
    if not set(parsed["classes"]).issubset(class_tokens):
        return False
    for attr, operator, value in parsed["attributes"]:
        if not Element._attribute_selector_matches(
            element.getAttribute(attr), operator, value
        ):
            return False
    return True


def _selector_candidates(
    context: Any,
    parsed: dict[str, Any],
    combinator: str | None,
) -> Iterator[Element]:
    if combinator == ">":
        yield from _element_children(context)
        return
    if parsed["id"] is not None:
        found = _find_element_by_id(context, parsed["id"])
        if isinstance(found, Element):
            yield found
        return
    if parsed["tag"] != "*":
        tag_name = parsed["tag"].lower()
        for candidate in _element_descendants(context):
            if candidate.tagName.lower() == tag_name:
                yield candidate
        return
    yield from _element_descendants(context)


def _select_fast(self: Node, selector: str) -> list[Element] | None:
    if "," in selector or any(char in selector for char in ("+", "~", ":")):
        return None
    parts = _split_simple_selector_chain(selector)
    if not parts:
        return None
    parsed_parts = [
        (combinator, Element._parse_simple_selector(simple))
        for combinator, simple in parts
    ]
    if any(parsed is None for _, parsed in parsed_parts):
        return None

    contexts: list[Any] = [self]
    for combinator, parsed in parsed_parts:
        next_contexts = []
        for context in contexts:
            for candidate in _selector_candidates(context, parsed, combinator):
                if _match_parsed_selector(candidate, parsed):
                    next_contexts.append(candidate)
        contexts = next_contexts
        if not contexts:
            break
    return contexts


def _select(
    self: Node,
    selector: str,
    limit: int | None = None,
    **kwargs: Any,
) -> list[Element]:
    fast = _select_fast(self, selector)
    if fast is not None:
        return _limit(fast, limit)
    return _limit(self.querySelectorAll(selector), limit)


def _select_one(self: Node, selector: str, **kwargs: Any) -> Element | None:
    fast = _select_fast(self, selector)
    if fast is not None:
        return fast[0] if fast else None
    return self.querySelector(selector)


def _parents(self: Node) -> Iterator[Node]:
    parent = getattr(self, "parentNode", None)
    while parent is not None:
        yield parent
        parent = getattr(parent, "parentNode", None)


def _parent(self: Node) -> Node | None:
    return getattr(self, "parentNode", None)


def _find_parent(
    self: Node,
    name: Any = None,
    attrs: dict[str, Any] | None = None,
    **kwargs: Any,
) -> Any | None:
    found = _find_parents(self, name, attrs, limit=1, **kwargs)
    return found[0] if found else None


def _find_parents(
    self: Node,
    name: Any = None,
    attrs: dict[str, Any] | None = None,
    limit: int | None = None,
    **kwargs: Any,
) -> list[Any]:
    merged_attrs = _merge_attrs(attrs, kwargs)
    return _limit(
        (node for node in _parents(self) if _matches(node, name, merged_attrs)),
        limit,
    )


def _siblings_from(self: Node, previous: bool = False) -> Iterator[Any]:
    parent = getattr(self, "parentNode", None)
    if parent is None:
        return
    siblings = list(_iter_child_nodes(parent))
    try:
        index = siblings.index(self)
    except ValueError:
        return
    items = reversed(siblings[:index]) if previous else iter(siblings[index + 1 :])
    yield from items


def _find_siblings(
    self: Node,
    previous: bool,
    name: Any = None,
    attrs: dict[str, Any] | None = None,
    string: Any = None,
    limit: int | None = None,
    **kwargs: Any,
) -> list[Any]:
    merged_attrs = _merge_attrs(attrs, kwargs)
    return _limit(
        (
            node
            for node in _siblings_from(self, previous)
            if _matches(node, name, merged_attrs, string)
        ),
        limit,
    )


def _find_next_sibling(
    self: Node,
    name: Any = None,
    attrs: dict[str, Any] | None = None,
    string: Any = None,
    **kwargs: Any,
) -> Any | None:
    string = _string_alias(string, kwargs)
    found = _find_siblings(self, False, name, attrs, string, limit=1, **kwargs)
    return found[0] if found else None


def _find_next_siblings(
    self: Node,
    name: Any = None,
    attrs: dict[str, Any] | None = None,
    string: Any = None,
    limit: int | None = None,
    **kwargs: Any,
) -> list[Any]:
    string = _string_alias(string, kwargs)
    return _find_siblings(self, False, name, attrs, string, limit, **kwargs)


def _find_previous_sibling(
    self: Node,
    name: Any = None,
    attrs: dict[str, Any] | None = None,
    string: Any = None,
    **kwargs: Any,
) -> Any | None:
    string = _string_alias(string, kwargs)
    found = _find_siblings(self, True, name, attrs, string, limit=1, **kwargs)
    return found[0] if found else None


def _find_previous_siblings(
    self: Node,
    name: Any = None,
    attrs: dict[str, Any] | None = None,
    string: Any = None,
    limit: int | None = None,
    **kwargs: Any,
) -> list[Any]:
    string = _string_alias(string, kwargs)
    return _find_siblings(self, True, name, attrs, string, limit, **kwargs)


def _all_elements(root: Any) -> list[Any]:
    return [
        node
        for node in _document_order(root)
        if isinstance(node, (Element, str, Text))
    ]


def _document_neighbors(self: Node, previous: bool = False) -> Iterator[Any]:
    root = getattr(self, "rootNode", self)
    nodes = _all_elements(root)
    try:
        index = nodes.index(self)
    except ValueError:
        return
    items = reversed(nodes[:index]) if previous else iter(nodes[index + 1 :])
    yield from items


def _find_document_order(
    self: Node,
    previous: bool,
    name: Any = None,
    attrs: dict[str, Any] | None = None,
    string: Any = None,
    limit: int | None = None,
    **kwargs: Any,
) -> list[Any]:
    merged_attrs = _merge_attrs(attrs, kwargs)
    return _limit(
        (
            node
            for node in _document_neighbors(self, previous)
            if _matches(node, name, merged_attrs, string)
        ),
        limit,
    )


def _find_next(
    self: Node,
    name: Any = None,
    attrs: dict[str, Any] | None = None,
    string: Any = None,
    **kwargs: Any,
) -> Any | None:
    string = _string_alias(string, kwargs)
    found = _find_document_order(self, False, name, attrs, string, limit=1, **kwargs)
    return found[0] if found else None


def _find_all_next(
    self: Node,
    name: Any = None,
    attrs: dict[str, Any] | None = None,
    string: Any = None,
    limit: int | None = None,
    **kwargs: Any,
) -> list[Any]:
    string = _string_alias(string, kwargs)
    return _find_document_order(self, False, name, attrs, string, limit, **kwargs)


def _find_previous(
    self: Node,
    name: Any = None,
    attrs: dict[str, Any] | None = None,
    string: Any = None,
    **kwargs: Any,
) -> Any | None:
    string = _string_alias(string, kwargs)
    found = _find_document_order(self, True, name, attrs, string, limit=1, **kwargs)
    return found[0] if found else None


def _find_all_previous(
    self: Node,
    name: Any = None,
    attrs: dict[str, Any] | None = None,
    string: Any = None,
    limit: int | None = None,
    **kwargs: Any,
) -> list[Any]:
    string = _string_alias(string, kwargs)
    return _find_document_order(self, True, name, attrs, string, limit, **kwargs)


def _strings(self: Node) -> Iterator[str]:
    if isinstance(self, Text):
        yield self.data
        return
    for node in _descendants(self):
        if isinstance(node, Text):
            yield node.data
        elif isinstance(node, str):
            yield node


def _stripped_strings(self: Node) -> Iterator[str]:
    for item in _strings(self):
        stripped = item.strip()
        if stripped:
            yield stripped


def _get_text(
    self: Node,
    separator: str = "",
    strip: bool = False,
    types: Any = None,
) -> str:
    values = _stripped_strings(self) if strip else _strings(self)
    return separator.join(values)


def _attrs_get(self: Element) -> dict[str, Any]:
    return _attribute_dict(self)


def _attrs_set(self: Element, value: dict[str, Any]) -> None:
    for attr in list(_attribute_dict(self)):
        self.removeAttribute(attr)
    for attr, attr_value in value.items():
        self.setAttribute(attr, attr_value)


def _get(self: Element, key: str, default: Any = None) -> Any:
    value = self.getAttribute(key)
    return default if value is None else value


def _has_attr(self: Element, key: str) -> bool:
    return self.hasAttribute(key)


def _has_key(self: Element, key: str) -> bool:
    return self.hasAttribute(key)


def _getitem(self: Element, key: str | int) -> Any:
    if isinstance(key, int):
        return _ORIGINAL_GETITEM(self, key)
    value = self.getAttribute(key)
    return value


def _setitem(self: Element, key: str | int, value: Any) -> None:
    if isinstance(key, int):
        raise TypeError(
            "Element child assignment by index is not supported by the BS4 layer"
        )
    self.setAttribute(key, value)
    return self


def _delitem(self: Element, key: str | int) -> None:
    if isinstance(key, int):
        raise TypeError(
            "Element child deletion by index is not supported by the BS4 layer"
        )
    if not self.hasAttribute(key):
        raise KeyError(key)
    self.removeAttribute(key)


def _contents(self: Node) -> list[Any]:
    return list(_iter_child_nodes(self))


def _children(self: Node) -> Iterator[Any]:
    return iter(_contents(self))


def _next_sibling(self: Node) -> Any | None:
    return getattr(self, "nextSibling", None)


def _previous_sibling(self: Node) -> Any | None:
    return getattr(self, "previousSibling", None)


def _next_siblings(self: Node) -> Iterator[Any]:
    yield from _siblings_from(self, previous=False)


def _previous_siblings(self: Node) -> Iterator[Any]:
    yield from _siblings_from(self, previous=True)


def _next_element(self: Node) -> Any | None:
    return next(_document_neighbors(self, previous=False), None)


def _next_elements(self: Node) -> Iterator[Any]:
    yield from _document_neighbors(self, previous=False)


def _previous_element(self: Node) -> Any | None:
    return next(_document_neighbors(self, previous=True), None)


def _previous_elements(self: Node) -> Iterator[Any]:
    yield from _document_neighbors(self, previous=True)


def _string(self: Node) -> str | Text | None:
    return _own_string(self)


def _set_string(self: Node, value: Any) -> None:
    self.textContent = "" if value is None else str(value)


def _append(self: Node, *items: Any) -> Any:
    original = _original_append(type(self))
    if original is not None:
        return original(self, *items)
    for item in items:
        self.appendChild(item)
    return self


def _extend(self: Node, items: Iterable[Any]) -> None:
    for item in items:
        self.appendChild(item)


def _insert(self: Node, index: int, item: Any) -> Any:
    children = list(_iter_child_nodes(self))
    if index >= len(children):
        self.appendChild(item)
    else:
        self.insertBefore(item, children[index])
    return item


def _insert_relative(self: Node, item: Any, after: bool = False) -> Any:
    parent = getattr(self, "parentNode", None)
    if parent is None:
        return item
    siblings = list(_iter_child_nodes(parent))
    index = siblings.index(self) + (1 if after else 0)
    if index >= len(siblings):
        parent.appendChild(item)
    else:
        parent.insertBefore(item, siblings[index])
    return item


def _insert_before(self: Node, item: Any) -> Any:
    return _insert_relative(self, item, after=False)


def _insert_after(self: Node, item: Any) -> Any:
    return _insert_relative(self, item, after=True)


def _clear(self: Node) -> None:
    for child in _iter_child_nodes(self):
        if isinstance(child, Node):
            child.parentNode = None
    self.args = ()


def _extract(self: Node) -> Node:
    parent = getattr(self, "parentNode", None)
    if parent is not None:
        parent.removeChild(self)
    return self


def _decompose(self: Node) -> None:
    _extract(self)
    _clear(self)
    return None


def _replace_with(self: Node, *nodes: Any) -> Node:
    parent = getattr(self, "parentNode", None)
    if parent is None:
        return self
    siblings = list(_iter_child_nodes(parent))
    index = siblings.index(self)
    parent.removeChild(self)
    for offset, node in enumerate(nodes):
        _insert(parent, index + offset, node)
    return self


def _wrap(self: Node, wrapper: Element) -> Element:
    parent = getattr(self, "parentNode", None)
    if parent is not None:
        siblings = list(_iter_child_nodes(parent))
        index = siblings.index(self)
        parent.removeChild(self)
        _insert(parent, index, wrapper)
    wrapper.appendChild(self)
    return wrapper


def _unwrap(self: Node) -> Node:
    parent = getattr(self, "parentNode", None)
    if parent is None:
        return self
    children = list(_iter_child_nodes(self))
    siblings = list(_iter_child_nodes(parent))
    index = siblings.index(self)
    parent.removeChild(self)
    for offset, child in enumerate(children):
        _insert(parent, index + offset, child)
    self.args = ()
    return self


def _smooth(self: Node) -> None:
    normalize = getattr(self, "normalize", None)
    if callable(normalize):
        normalize()


def _new_tag(
    self: Node,
    name: str,
    namespace: str | None = None,
    nsprefix: str | None = None,
    attrs: dict[str, Any] | None = None,
    **kwargs: Any,
) -> Element:
    tag = (
        Document.createElementNS(namespace, name)
        if namespace
        else Document.createElement(name)
    )
    for attr, value in _merge_attrs(attrs, kwargs).items():
        tag.setAttribute(attr, value)
    return tag


def _new_string(self: Node, value: Any = "") -> Text:
    return Text(str(value))


def _prettify(self: Node, formatter: Any = "minimal") -> str:
    return format(self)


def _install_node_api(cls: type) -> None:
    cls.find = _find
    cls.find_all = _find_all
    cls.findAll = _find_all
    cls.find_child = _find_child
    cls.findChild = _find_child
    cls.find_children = _find_children
    cls.findChildren = _find_children
    cls.select = _select
    cls.select_one = _select_one
    cls.find_parent = _find_parent
    cls.findParent = _find_parent
    cls.find_parents = _find_parents
    cls.findParents = _find_parents
    cls.find_next = _find_next
    cls.findNext = _find_next
    cls.find_all_next = _find_all_next
    cls.findAllNext = _find_all_next
    cls.find_previous = _find_previous
    cls.findPrevious = _find_previous
    cls.find_all_previous = _find_all_previous
    cls.findAllPrevious = _find_all_previous
    cls.find_next_sibling = _find_next_sibling
    cls.findNextSibling = _find_next_sibling
    cls.find_next_siblings = _find_next_siblings
    cls.findNextSiblings = _find_next_siblings
    cls.find_previous_sibling = _find_previous_sibling
    cls.findPreviousSibling = _find_previous_sibling
    cls.find_previous_siblings = _find_previous_siblings
    cls.findPreviousSiblings = _find_previous_siblings
    cls.get_text = _get_text
    cls.prettify = _prettify
    cls.append = _append
    cls.extend = _extend
    cls.insert = _insert
    cls.insert_before = _insert_before
    cls.insert_after = _insert_after
    cls.clear = _clear
    cls.extract = _extract
    cls.decompose = _decompose
    cls.replace_with = _replace_with
    cls.wrap = _wrap
    cls.unwrap = _unwrap
    cls.smooth = _smooth
    cls.new_tag = _new_tag
    cls.new_string = _new_string
    cls.parent = property(_parent)
    cls.parents = property(_parents)
    cls.contents = property(_contents)
    cls.descendants = property(_descendants)
    cls.next_sibling = property(_next_sibling)
    cls.next_siblings = property(_next_siblings)
    cls.previous_sibling = property(_previous_sibling)
    cls.previous_siblings = property(_previous_siblings)
    cls.next_element = property(_next_element)
    cls.next_elements = property(_next_elements)
    cls.previous_element = property(_previous_element)
    cls.previous_elements = property(_previous_elements)
    cls.string = property(_string, _set_string)
    cls.strings = property(_strings)
    cls.stripped_strings = property(_stripped_strings)


def _install_element_api() -> None:
    Element.attrs = property(_attrs_get, _attrs_set)
    Element.get = _get
    Element.has_attr = _has_attr
    Element.has_key = _has_key
    Element.__getitem__ = _getitem
    Element.__setitem__ = _setitem
    Element.__delitem__ = _delitem


_ORIGINAL_GETITEM = Element.__getitem__
_ORIGINAL_APPEND = {
    cls: getattr(cls, "append")
    for cls in (Node, Element, Document, DocumentFragment)
    if hasattr(cls, "append")
}
_INSTALLED = False


def _original_append(cls: type) -> Callable[..., Any] | None:
    for base in cls.__mro__:
        if base in _ORIGINAL_APPEND:
            return _ORIGINAL_APPEND[base]
    return None


def install() -> None:
    """Install the BS4 compatibility API onto domonic node classes."""
    global _INSTALLED
    if _INSTALLED:
        return
    for cls in (Node, Element, Document, DocumentFragment, Text, Comment):
        _install_node_api(cls)
    _install_element_api()
    _INSTALLED = True


install()


__all__ = ["BeautifulSlop", "install"]
