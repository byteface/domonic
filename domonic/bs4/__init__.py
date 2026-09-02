"""
domonic.bs4
===========

Beautiful Soup 4 style convenience methods for domonic nodes.

Importing this module opt-in patches a small, familiar BS4 API onto domonic's
real DOM classes. Returned objects remain normal domonic nodes, not wrappers.
"""

from __future__ import annotations

import re
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
    "turbohtml": "turbohtml",
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
        return getattr(node, "name", getattr(node, "tagName", None))
    if isinstance(node, Document):
        return "[document]"
    return None


def _iter_child_nodes(node: Any) -> Iterator[Any]:
    yield from getattr(node, "args", ()) or ()


def _descendants(node: Any) -> Iterator[Any]:
    stack = list(reversed(tuple(_iter_child_nodes(node))))
    while stack:
        child = stack.pop()
        yield child
        if isinstance(child, Node) and not isinstance(child, (Text, Comment)):
            stack.extend(reversed(getattr(child, "args", ()) or ()))


def _document_order(root: Any) -> list[Any]:
    nodes = [root]
    nodes.extend(_descendants(root))
    return nodes


def _element_descendants(node: Any) -> Iterator[Element]:
    stack = list(reversed(tuple(_iter_child_nodes(node))))
    while stack:
        child = stack.pop()
        if isinstance(child, Element):
            yield child
            stack.extend(reversed(getattr(child, "args", ()) or ()))
        elif isinstance(child, Node) and not isinstance(child, (Text, Comment)):
            stack.extend(reversed(getattr(child, "args", ()) or ()))


def _element_children(node: Any) -> Iterator[Element]:
    for child in _iter_child_nodes(node):
        if isinstance(child, Element):
            yield child


def _sibling_view(
    node: Any, cache: dict[int, tuple[list[Element], dict[int, int]]] | None
) -> tuple[list[Element], int] | None:
    """Return ``(element-siblings list, index of node)`` for ``node``'s parent.

    The list + index map for a parent is built once and cached, so ``+`` / ``~``
    over a wide sibling set stays linear instead of rebuilding the list per node.
    """
    parent = getattr(node, "parentNode", None)
    if parent is None:
        return None
    if cache is None:
        cache = {}
    entry = cache.get(id(parent))
    if entry is None:
        kids = [c for c in _iter_child_nodes(parent) if isinstance(c, Element)]
        entry = (kids, {id(k): i for i, k in enumerate(kids)})
        cache[id(parent)] = entry
    kids, index_map = entry
    idx = index_map.get(id(node))
    return None if idx is None else (kids, idx)


def _following_element_siblings(
    node: Any, cache: dict[int, Any] | None = None
) -> Iterator[Element]:
    view = _sibling_view(node, cache)
    if view is not None:
        kids, idx = view
        yield from kids[idx + 1:]


def _next_element_sibling(
    node: Any, cache: dict[int, Any] | None = None
) -> Element | None:
    view = _sibling_view(node, cache)
    if view is None:
        return None
    kids, idx = view
    return kids[idx + 1] if idx + 1 < len(kids) else None


def _find_element_by_id(
    node: Any,
    element_id: str,
    include_self: bool = False,
) -> Element | None:
    if (
        include_self
        and isinstance(node, Element)
        and _get_attribute(node, "id") == element_id
    ):
        return node
    for child in _element_descendants(node):
        if _get_attribute(child, "id") == element_id:
            return child
    return None


def _root_for_index(node: Any) -> Node | None:
    root = getattr(node, "rootNode", node)
    return root if isinstance(root, Node) else None


def _invalidate_index(node: Any) -> None:
    root = _root_for_index(node)
    if root is not None:
        root.__dict__.pop("_bs4_tag_index", None)


def _tag_index(node: Any) -> dict[str, list[Element]]:
    root = _root_for_index(node)
    if root is None:
        return {}
    cached = root.__dict__.get("_bs4_tag_index")
    if cached is not None:
        return cached

    index: dict[str, list[Element]] = {"*": []}
    for element in _element_descendants(root):
        index["*"].append(element)
        index.setdefault(element.name.lower(), []).append(element)
    root.__dict__["_bs4_tag_index"] = index
    return index


def _indexed_candidates(
    node: Any,
    name: Any = None,
    recursive: bool = True,
    string: Any = None,
) -> Iterator[Any] | None:
    parent = getattr(node, "parentNode", None)
    if (
        string is not None
        or not recursive
        or (parent is not None and not isinstance(parent, Document))
    ):
        return None
    index = _tag_index(node)
    if name is None:
        return iter(index.get("*", ()))
    if isinstance(name, (list, tuple, set)) and all(
        isinstance(item, str) for item in name
    ):
        names = {item.lower() for item in name}
        return (
            element for element in index.get("*", ()) if element.name.lower() in names
        )
    if not isinstance(name, str):
        return None
    return iter(index.get(name.lower(), ()))


def _attribute_name(name: str) -> str:
    if name == "class_":
        return "class"
    if name.endswith("_") and not name.startswith("_"):
        return name[:-1]
    return name


def _get_attribute(node: Any, name: str) -> Any:
    if not isinstance(node, Element):
        return None
    public_name = _attribute_name(name)
    key = public_name if public_name.startswith("_") else f"_{public_name}"
    return getattr(node, "kwargs", {}).get(key)


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


def _merge_attrs(
    attrs: dict[str, Any] | None, kwargs: dict[str, Any]
) -> dict[str, Any]:
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
        candidate = _get_attribute(node, public_name)
        matcher = _class_filter_matches if public_name == "class" else _filter_matches
        if not matcher(expected, candidate, node):
            return False
    return True


def _own_string(node: Any) -> str | None:
    if isinstance(node, (Text, Comment)):
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
    if isinstance(node, (Text, Comment)):
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
        # Beautiful Soup's ``string=`` filter matches any NavigableString,
        # which includes comment text.
        return isinstance(node, (str, Text, Comment)) and _string_matches(
            string, node
        )
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
    if string is None:
        children = _element_descendants(node) if recursive else _element_children(node)
        if callable(name) and not attrs:
            for child in children:
                try:
                    if name(child):
                        yield child
                except TypeError:
                    candidate = _tag_name(child)
                    try:
                        if name(candidate):
                            yield child
                    except TypeError:
                        pass
            return
    else:
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
        if candidate.name.lower() == tag_name
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
    if (
        recursive
        and string is None
        and not merged_attrs
        and isinstance(name, (str, type(None)))
    ):
        candidates = _indexed_candidates(self, name, recursive, string)
        if candidates is None:
            candidates = _candidate_nodes(self, name, recursive, string)
        if candidates is not None:
            return _limit(candidates, limit)
    if recursive and _can_use_css(name, merged_attrs, string):
        selector = _css_from_filters(name, merged_attrs)
        fast = _select_fast(self, selector, limit=limit)
        if fast is not None:
            return _limit(fast, limit)
        try:
            return _limit(self.querySelectorAll(selector), limit)
        except Exception:
            pass
    candidates = _indexed_candidates(self, name, recursive, string)
    if candidates is None:
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
        # ``>`` is always a combinator; ``+`` / ``~`` only when whitespace-
        # separated, so a literal class token such as ``.foo+bar`` is preserved.
        if char == ">" or (char in ("+", "~") and pending_space):
            current = "".join(token).strip()
            if not current:
                return None
            parts.append((combinator, current))
            token = []
            combinator = char
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


def _strip_simple_pseudo(selector: str) -> tuple[str, tuple[str, Any] | None] | None:
    if ":" not in selector:
        return selector, None
    if selector.endswith(":first-child"):
        return selector[: -len(":first-child")], ("first-child", None)
    if selector.endswith(":last-child"):
        return selector[: -len(":last-child")], ("last-child", None)
    match = re.search(r":nth-child\((\d+)\)$", selector)
    if match:
        return selector[: match.start()], ("nth-child", int(match.group(1)))
    # :not(<single compound selector>) - the common form; a selector list or a
    # nested combinator inside :not() bails to the XPath engine.
    match = re.search(r":not\(([^()]+)\)$", selector)
    if match:
        inner = match.group(1).strip()
        if "," in inner or any(c in inner for c in " >+~"):
            return None  # selector list / combinator inside :not() -> XPath
        if inner.startswith(":"):
            nested = _strip_simple_pseudo("x" + inner)
            if nested is None or nested[1] is None:
                return None
            return selector[: match.start()], ("not-pseudo", nested[1])
        inner_parsed = Element._parse_simple_selector(inner)
        if inner_parsed is None:
            return None
        return selector[: match.start()], ("not", inner_parsed)
    return None


def _split_selector_groups(selector: str) -> list[str] | None:
    groups = []
    token = []
    bracket_depth = 0
    quote: str | None = None

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
        if char == "," and not bracket_depth:
            group = "".join(token).strip()
            if not group:
                return None
            groups.append(group)
            token = []
            continue
        token.append(char)

    group = "".join(token).strip()
    if not group or bracket_depth or quote:
        return None
    groups.append(group)
    return groups


def _match_parsed_selector(element: Element, parsed: dict[str, Any]) -> bool:
    tag_name = parsed["tag"]
    if tag_name != "*" and element.name.lower() != tag_name.lower():
        return False
    if parsed["id"] is not None and _get_attribute(element, "id") != parsed["id"]:
        return False
    class_tokens = set(str(_get_attribute(element, "class") or "").split())
    if not set(parsed["classes"]).issubset(class_tokens):
        return False
    for attr, operator, value in parsed["attributes"]:
        if not Element._attribute_selector_matches(
            _get_attribute(element, attr), operator, value
        ):
            return False
    return True


def _element_index(element: Element) -> int | None:
    parent = getattr(element, "parentNode", None)
    if parent is None:
        return None
    index = 0
    for child in _iter_child_nodes(parent):
        if isinstance(child, Element):
            index += 1
            if child is element:
                return index
    return None


def _sibling_positions(parent: Any) -> dict[int, tuple[int, int]]:
    """Map ``id(child element) -> (1-based index, total element count)`` for one
    parent, computed in a single pass. Callers memoise this per ``select`` so
    ``:first-child`` / ``:nth-child`` over a wide list stay linear, not O(n^2).
    """
    elements = [c for c in _iter_child_nodes(parent) if isinstance(c, Element)]
    total = len(elements)
    return {id(el): (i + 1, total) for i, el in enumerate(elements)}


def _match_simple_pseudo(
    element: Element,
    pseudo: tuple[str, Any] | None,
    position_cache: dict[int, dict[int, tuple[int, int]]] | None = None,
) -> bool:
    if pseudo is None:
        return True
    name, value = pseudo
    if name == "not":
        return not _match_parsed_selector(element, value)
    if name == "not-pseudo":
        return not _match_simple_pseudo(element, value, position_cache)
    parent = getattr(element, "parentNode", None)
    if parent is None:
        return False
    if position_cache is None:
        position_cache = {}
    positions = position_cache.get(id(parent))
    if positions is None:
        positions = _sibling_positions(parent)
        position_cache[id(parent)] = positions
    entry = positions.get(id(element))
    if entry is None:
        return False
    index, total = entry
    if name == "first-child":
        return index == 1
    if name == "last-child":
        return index == total
    if name == "nth-child":
        return index == value
    return False


def _prune_nested_contexts(contexts: list[Any]) -> list[Any]:
    """Drop contexts that are descendants of another context in the list: a
    descendant search from the ancestor already covers them. Keeps a chain of
    N nested matches from turning the next descendant step into O(N^2).
    """
    ids = {id(c) for c in contexts}
    kept = []
    for context in contexts:
        node = getattr(context, "parentNode", None)
        covered = False
        while node is not None:
            if id(node) in ids:
                covered = True
                break
            node = getattr(node, "parentNode", None)
        if not covered:
            kept.append(context)
    return kept


def _selector_candidates(
    context: Any,
    parsed: dict[str, Any],
    combinator: str | None,
    sibling_cache: dict[int, Any] | None = None,
) -> Iterator[Element]:
    if combinator == ">":
        yield from _element_children(context)
        return
    if combinator == "+":
        sibling = _next_element_sibling(context, sibling_cache)
        if sibling is not None:
            yield sibling
        return
    if combinator == "~":
        yield from _following_element_siblings(context, sibling_cache)
        return
    if parsed["id"] is not None:
        found = _find_element_by_id(context, parsed["id"])
        if isinstance(found, Element):
            yield found
        return
    if parsed["tag"] != "*":
        tag_name = parsed["tag"].lower()
        for candidate in _element_descendants(context):
            if candidate.name.lower() == tag_name:
                yield candidate
        return
    yield from _element_descendants(context)


def _select_fast(
    self: Node,
    selector: str,
    limit: int | None = None,
) -> list[Element] | None:
    groups = _split_selector_groups(selector)
    if not groups:
        return None
    if len(groups) > 1:
        matched_ids = set()
        for group in groups:
            matches = _select_fast(self, group)
            if matches is None:
                return None
            matched_ids.update(id(match) for match in matches)
        return _limit(
            (
                candidate
                for candidate in _element_descendants(self)
                if id(candidate) in matched_ids
            ),
            limit,
        )
    selector = groups[0]
    parts = _split_simple_selector_chain(selector)
    if not parts:
        return None
    parsed_parts = []
    for combinator, simple in parts:
        pseudo_result = _strip_simple_pseudo(simple)
        if pseudo_result is None:
            return None
        simple, pseudo = pseudo_result
        parsed_parts.append(
            (combinator, Element._parse_simple_selector(simple), pseudo)
        )
    if any(parsed is None for _, parsed, _ in parsed_parts):
        return None

    contexts: list[Any] = [self]
    last_index = len(parsed_parts) - 1
    position_cache: dict[int, dict[int, tuple[int, int]]] = {}
    sibling_cache: dict[int, Any] = {}
    for index, (combinator, parsed, pseudo) in enumerate(parsed_parts):
        if combinator in (None, " ") and len(contexts) > 1:
            contexts = _prune_nested_contexts(contexts)
        elif combinator == "~" and len(contexts) > 1:
            # ``A ~ B``: the earliest A under a parent already yields every
            # following sibling, so later A's under the same parent add nothing.
            seen_parents: set[int] = set()
            pruned = []
            for context in contexts:
                pid = id(getattr(context, "parentNode", None))
                if pid not in seen_parents:
                    seen_parents.add(pid)
                    pruned.append(context)
            contexts = pruned
        next_contexts = []
        seen_candidates: set[int] = set()
        for context in contexts:
            if (
                index == 0
                and index < last_index
                and isinstance(context, Element)
                and _match_parsed_selector(context, parsed)
                and _match_simple_pseudo(context, pseudo, position_cache)
            ):
                next_contexts.append(context)
                seen_candidates.add(id(context))
            for candidate in _selector_candidates(
                context, parsed, combinator, sibling_cache
            ):
                marker = id(candidate)
                if marker in seen_candidates:
                    continue
                if _match_parsed_selector(candidate, parsed) and _match_simple_pseudo(
                    candidate, pseudo, position_cache
                ):
                    seen_candidates.add(marker)
                    next_contexts.append(candidate)
                    if index == last_index and limit == 1:
                        return next_contexts
        contexts = next_contexts
        if not contexts:
            break
    unique_contexts = []
    seen = set()
    for context in contexts:
        context_id = id(context)
        if context_id not in seen:
            unique_contexts.append(context)
            seen.add(context_id)
            if limit is not None and len(unique_contexts) >= limit:
                break
    return unique_contexts


def _select(
    self: Node,
    selector: str,
    limit: int | None = None,
    **kwargs: Any,
) -> list[Element]:
    fast = _select_fast(self, selector, limit=limit)
    if fast is not None:
        return _limit(fast, limit)
    return _limit(self.querySelectorAll(selector), limit)


def _select_one(self: Node, selector: str, **kwargs: Any) -> Element | None:
    fast = _select_fast(self, selector, limit=1)
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
        node for node in _document_order(root) if isinstance(node, (Element, str, Text))
    ]


_NAVIGABLE = (Element, str, Text)


def _subtree_forward(node: Any, skip_self: bool = False) -> Iterator[Any]:
    """Nodes of ``node``'s subtree in document (pre-)order."""
    if not skip_self and isinstance(node, _NAVIGABLE):
        yield node
    stack = list(getattr(node, "args", None) or ())
    stack.reverse()
    while stack:
        cur = stack.pop()
        if isinstance(cur, _NAVIGABLE):
            yield cur
        kids = getattr(cur, "args", None) or ()
        if kids:
            stack.extend(reversed(kids))


def _subtree_backward(node: Any) -> Iterator[Any]:
    """Nodes of ``node``'s subtree in reverse document order (``node`` last)."""
    stack: list[tuple[Any, bool]] = [(node, False)]
    while stack:
        cur, expanded = stack.pop()
        if expanded:
            if isinstance(cur, _NAVIGABLE):
                yield cur
        else:
            stack.append((cur, True))
            for child in getattr(cur, "args", None) or ():
                stack.append((child, False))


def _document_neighbors(self: Node, previous: bool = False) -> Iterator[Any]:
    """Nodes before / after ``self`` in document order, walked lazily.

    Unlike the old "materialise the whole document then slice" approach this is
    O(distance to the results) -- ``find_previous`` on a nearby heading no
    longer costs a full-document scan.
    """
    if not previous:
        yield from _subtree_forward(self, skip_self=True)
    node: Any = self
    while node is not None:
        parent = getattr(node, "parentNode", None)
        if parent is None:
            return
        kids = getattr(parent, "args", None) or ()
        index = None
        for i, child in enumerate(kids):
            if child is node:
                index = i
                break
        if index is None:
            return
        if previous:
            for j in range(index - 1, -1, -1):
                yield from _subtree_backward(kids[j])
            if isinstance(parent, _NAVIGABLE):
                yield parent
        else:
            for j in range(index + 1, len(kids)):
                yield from _subtree_forward(kids[j])
        node = parent


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
    if type(self) is Text:
        args = self.__dict__.get("args", ())
        if args:
            yield args[0]
        return
    stack = list(reversed(self.__dict__.get("args", ()) or ()))
    text_type = Text
    comment_type = Comment
    element_type = Element
    node_type = Node
    isinstance_ = isinstance
    skipped_names = {"script", "style"}
    while stack:
        node = stack.pop()
        node_class = type(node)
        if node_class is text_type:
            args = node.__dict__.get("args", ())
            if args:
                yield args[0]
        elif node_class is str:
            yield node
        elif isinstance_(node, element_type):
            if node.name.lower() in skipped_names:
                continue
            stack.extend(reversed(node.__dict__.get("args", ()) or ()))
        elif isinstance_(node, node_type) and not isinstance_(node, comment_type):
            stack.extend(reversed(node.__dict__.get("args", ()) or ()))


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
    if strip:
        if type(self) is Text:
            text = self.__dict__.get("args", ("",))[0].strip()
            return text if text else ""
        parts = []
        append = parts.append
        stack = list(self.__dict__.get("args", ()) or ())
        stack.reverse()
        text_type = Text
        element_type = Element
        node_type = Node
        comment_type = Comment
        isinstance_ = isinstance
        while stack:
            node = stack.pop()
            node_class = type(node)
            if node_class is text_type:
                stripped = node.__dict__["args"][0].strip()
                if stripped:
                    append(stripped)
            elif node_class is str:
                stripped = node.strip()
                if stripped:
                    append(stripped)
            elif isinstance_(node, element_type):
                name = node.name
                if name == "script" or name == "style":
                    continue
                children = node.__dict__["args"]
                if children:
                    stack.extend(children[::-1])
            elif isinstance_(node, node_type) and not isinstance_(node, comment_type):
                children = node.__dict__.get("args")
                if children:
                    stack.extend(children[::-1])
        return separator.join(parts)
    return separator.join(_strings(self))


def _attrs_get(self: Element) -> dict[str, Any]:
    return _attribute_dict(self)


def _attrs_set(self: Element, value: dict[str, Any]) -> None:
    _invalidate_index(self)
    for attr in list(_attribute_dict(self)):
        self.removeAttribute(attr)
    for attr, attr_value in value.items():
        self.setAttribute(attr, attr_value)


def _get(self: Element, key: str, default: Any = None) -> Any:
    value = _get_attribute(self, key)
    return default if value is None else value


def _has_attr(self: Element, key: str) -> bool:
    return self.hasAttribute(key)


def _has_key(self: Element, key: str) -> bool:
    return self.hasAttribute(key)


def _getitem(self: Element, key: str | int) -> Any:
    if isinstance(key, int):
        return _ORIGINAL_GETITEM(self, key)
    value = _get_attribute(self, key)
    return value


def _setitem(self: Element, key: str | int, value: Any) -> None:
    if isinstance(key, int):
        raise TypeError(
            "Element child assignment by index is not supported by the BS4 layer"
        )
    _invalidate_index(self)
    self.setAttribute(key, value)
    return self


def _delitem(self: Element, key: str | int) -> None:
    if isinstance(key, int):
        raise TypeError(
            "Element child deletion by index is not supported by the BS4 layer"
        )
    if not self.hasAttribute(key):
        raise KeyError(key)
    _invalidate_index(self)
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
    _invalidate_index(self)
    original = _original_append(type(self))
    if original is not None:
        return original(self, *items)
    for item in items:
        self.appendChild(item)
    return self


def _extend(self: Node, items: Iterable[Any]) -> None:
    _invalidate_index(self)
    for item in items:
        self.appendChild(item)


def _insert(self: Node, index: int, item: Any) -> Any:
    _invalidate_index(self)
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
    _invalidate_index(parent)
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
    _invalidate_index(self)
    for child in _iter_child_nodes(self):
        if isinstance(child, Node):
            child.parentNode = None
    self.args = ()


def _extract(self: Node) -> Node:
    parent = getattr(self, "parentNode", None)
    if parent is not None:
        _invalidate_index(parent)
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
    _invalidate_index(parent)
    siblings = list(_iter_child_nodes(parent))
    index = siblings.index(self)
    parent.removeChild(self)
    for offset, node in enumerate(nodes):
        _insert(parent, index + offset, node)
    return self


def _wrap(self: Node, wrapper: Element) -> Element:
    parent = getattr(self, "parentNode", None)
    if parent is not None:
        _invalidate_index(parent)
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
    _invalidate_index(parent)
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


_PRETTIFY_RAW_TAGS = frozenset({"script", "style", "textarea", "pre"})


def _prettify(self: Node, formatter: Any = "minimal", indent: str = " ") -> str:
    """Beautiful Soup's ``prettify()`` -- one node per line, ``indent`` per level.

    Linear in the document size (the old implementation went through
    ``Node.__format__``, which recomputed each node's depth by walking its
    parent chain -- O(n * depth)).
    """
    from domonic.dom import _escape_html
    from domonic.html import closed_tag

    out: list[str] = []
    append = out.append
    escape = _escape_html
    element_type = Element
    text_type = Text
    comment_type = Comment
    document_type = Document

    doctype = getattr(self, "doctype", None)
    if doctype:
        append(str(doctype))
        append("\n")

    # stack entries: (node, depth) to open, or (None, "</name>\n text") sentinel
    stack: list[Any] = [(self, 0)]
    while stack:
        item = stack.pop()
        if type(item) is str:  # a pre-rendered closing line
            append(item)
            continue
        node, depth = item
        node_class = type(node)
        pad = indent * depth

        if node_class is str:
            text = node.strip()
            if text:
                append(pad)
                append(escape(text))
                append("\n")
            continue
        if node_class is text_type:
            text = str(node.textContent).strip()
            if text:
                append(pad)
                append(
                    escape(text)
                    if getattr(node, "_escape_text_on_render", False)
                    else text
                )
                append("\n")
            continue
        if node_class is comment_type:
            append(pad)
            append("<!--")
            append(str(getattr(node, "data", "")))
            append("-->\n")
            continue
        if not isinstance(node, element_type) and not isinstance(node, document_type):
            continue

        name = node.name
        attrs = node.__attributes__
        if isinstance(node, closed_tag):
            append(f"{pad}<{name}{attrs}/>\n")
            continue

        children = getattr(node, "args", ()) or ()
        if not children:
            append(f"{pad}<{name}{attrs}>\n{pad}</{name}>\n" if name else "")
            continue

        if name in _PRETTIFY_RAW_TAGS:
            body = "".join(
                str(c.textContent) if isinstance(c, text_type) else str(c)
                for c in children
            )
            append(f"{pad}<{name}{attrs}>{body}</{name}>\n")
            continue

        if name:
            append(f"{pad}<{name}{attrs}>\n")
            stack.append(f"{pad}</{name}>\n")
        for child in reversed(children):
            stack.append((child, depth + 1 if name else depth))

    return "".join(out)


def _decode(self: Node, *args: Any, **kwargs: Any) -> str:
    """Beautiful Soup's ``.decode()`` - the string form of the tree."""
    return str(self)


def _encode(
    self: Node, encoding: str = "utf-8", *args: Any, **kwargs: Any
) -> bytes:
    """Beautiful Soup's ``.encode()`` - the byte form of the tree."""
    return str(self).encode(encoding, "xmlcharrefreplace")


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
    cls.getText = _get_text
    cls.prettify = _prettify
    cls.decode = _decode
    cls.encode = _encode
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
