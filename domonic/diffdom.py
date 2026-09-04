"""
domonic.diffdom
================

DOM tree differ and patcher for domonic nodes.

The API is inspired by diffDOM: compare two DOM trees, get a JSON-safe list of
changes, then apply or undo those changes against another compatible tree.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from domonic.dom import Comment, Document, Element, Node, Text

TEXT_NODE_NAME = "#text"
COMMENT_NODE_NAME = "#comment"


def _is_text_node(node: Any) -> bool:
    return isinstance(node, (str, Text))


def _text_value(node: str | Text) -> str:
    if isinstance(node, Text):
        return node.data
    return node


def _set_text_value(parent: Node | None, route: list[int], value: str) -> None:
    node = _get_from_route(parent, route) if parent is not None else None
    if isinstance(node, Text):
        node.data = value
        return
    if parent is None or not route:
        return
    container = _get_from_route(parent, route[:-1])
    if isinstance(container, Node):
        _replace_child_at(container, route[-1], value)


def _public_attribute_name(name: str) -> str:
    return name[1:] if name.startswith("_") else name


def _dom_attribute_name(name: str) -> str:
    return name if name.startswith("_") else f"_{name}"


def _attributes(node: Element) -> dict[str, Any]:
    return {
        _public_attribute_name(name): deepcopy(value)
        for name, value in getattr(node, "kwargs", {}).items()
    }


def _node_name(node: Any) -> str | None:
    if _is_text_node(node):
        return TEXT_NODE_NAME
    if isinstance(node, Comment):
        return COMMENT_NODE_NAME
    return getattr(node, "nodeName", getattr(node, "tagName", None))


def nodeToObj(node: Any) -> dict[str, Any]:
    """Convert a domonic node or text child into a JSON-safe dictionary."""
    if _is_text_node(node):
        return {"nodeName": TEXT_NODE_NAME, "data": _text_value(node)}
    if isinstance(node, Comment):
        return {"nodeName": COMMENT_NODE_NAME, "data": node.data}
    if not isinstance(node, Node):
        return {"nodeName": TEXT_NODE_NAME, "data": str(node)}

    data: dict[str, Any] = {"nodeName": _node_name(node)}
    namespace = getattr(node, "namespaceURI", None)
    if namespace:
        data["namespaceURI"] = namespace
    if isinstance(node, Element):
        data["attributes"] = _attributes(node)
    children = [nodeToObj(child) for child in getattr(node, "args", ())]
    if children:
        data["childNodes"] = children
    return data


def objToNode(data: dict[str, Any] | str) -> Any:
    """Create a domonic node from a dictionary produced by :func:`nodeToObj`."""
    if isinstance(data, str):
        return data
    node_name = data.get("nodeName")
    if node_name == TEXT_NODE_NAME:
        return data.get("data", "")
    if node_name == COMMENT_NODE_NAME:
        return Comment(data.get("data", ""))

    tag_name = str(node_name or "")
    namespace = data.get("namespaceURI")
    if namespace:
        node = Document.createElementNS(str(namespace), tag_name)
    else:
        node = Document.createElement(tag_name)

    for name, value in data.get("attributes", {}).items():
        node.setAttribute(name, value)
    for child in data.get("childNodes", ()):
        node.appendChild(objToNode(child))
    return node


def _get_from_route(root: Any, route: list[int]) -> Any:
    node = root
    for index in route:
        node = node.args[index]
    return node


def _replace_child_at(parent: Node, index: int, child: Any) -> None:
    children = list(parent.args)
    old_child = children[index]
    if isinstance(old_child, Node):
        old_child.parentNode = None
    children[index] = child
    parent.args = tuple(children)
    if isinstance(child, Node):
        child.parentNode = parent
        child.ownerDocument = getattr(parent, "ownerDocument", None)


def _replace_node_contents(node: Node, replacement: Any) -> None:
    if _is_text_node(node) or _is_text_node(replacement):
        if isinstance(node, Text) and _is_text_node(replacement):
            node.data = _text_value(replacement)
            return
        raise ValueError("Cannot replace root node with a different node kind")
    if isinstance(node, Comment) or isinstance(replacement, Comment):
        if isinstance(node, Comment) and isinstance(replacement, Comment):
            node.data = replacement.data
            return
        raise ValueError("Cannot replace root node with a different node kind")
    if not isinstance(replacement, Node):
        raise ValueError("Replacement root must be a Node")

    if hasattr(replacement, "name"):
        node.name = replacement.name
    if hasattr(replacement, "kwargs"):
        node.kwargs = dict(replacement.kwargs)
    node.namespaceURI = getattr(replacement, "namespaceURI", "") or ""
    node.args = tuple(getattr(replacement, "args", ()))
    for child in node.args:
        if isinstance(child, Node):
            child.parentNode = node
            child.ownerDocument = getattr(node, "ownerDocument", None)


def _insert_child_at(parent: Node, index: int, child: Any) -> None:
    children = list(parent.args)
    index = max(0, min(index, len(children)))
    children.insert(index, child)
    parent.args = tuple(children)
    if isinstance(child, Node):
        child.parentNode = parent
        child.ownerDocument = getattr(parent, "ownerDocument", None)


def _remove_child_at(parent: Node, index: int) -> Any:
    children = list(parent.args)
    child = children.pop(index)
    parent.args = tuple(children)
    if isinstance(child, Node):
        child.parentNode = None
    return child


class DiffDOM:
    """Compare and patch domonic DOM trees with JSON-safe change objects."""

    def diff(self, source: Any, target: Any) -> list[dict[str, Any]]:
        """Return the changes needed to mutate ``source`` into ``target``."""
        changes: list[dict[str, Any]] = []
        self._diff_node(source, target, [], changes)
        return changes

    def apply(self, tree: Node, diffs: list[dict[str, Any]]) -> bool:
        """Apply ``diffs`` to ``tree``.

        Returns ``True`` when every change was applied. Invalid routes or
        unknown actions return ``False`` and leave any previous changes in
        place, matching the pragmatic behaviour of the original JS utility.
        """
        try:
            for change in diffs:
                self._apply_change(tree, change)
            return True
        except (AttributeError, IndexError, KeyError, TypeError, ValueError):
            return False

    def undo(self, tree: Node, diffs: list[dict[str, Any]]) -> bool:
        """Undo ``diffs`` against ``tree`` in reverse order."""
        try:
            for change in reversed(diffs):
                self._apply_change(tree, self._invert_change(change))
            return True
        except (AttributeError, IndexError, KeyError, TypeError, ValueError):
            return False

    def _diff_node(
        self,
        source: Any,
        target: Any,
        route: list[int],
        changes: list[dict[str, Any]],
    ) -> None:
        source_name = _node_name(source)
        target_name = _node_name(target)
        if source_name != target_name:
            changes.append(
                {
                    "action": "replaceElement",
                    "route": route,
                    "oldValue": nodeToObj(source),
                    "newValue": nodeToObj(target),
                }
            )
            return

        if _is_text_node(source) and _is_text_node(target):
            old_value = _text_value(source)
            new_value = _text_value(target)
            if old_value != new_value:
                changes.append(
                    {
                        "action": "modifyTextElement",
                        "route": route,
                        "oldValue": old_value,
                        "newValue": new_value,
                    }
                )
            return

        if isinstance(source, Comment) and isinstance(target, Comment):
            if source.data != target.data:
                changes.append(
                    {
                        "action": "modifyComment",
                        "route": route,
                        "oldValue": source.data,
                        "newValue": target.data,
                    }
                )
            return

        if isinstance(source, Element) and isinstance(target, Element):
            self._diff_attributes(source, target, route, changes)

        source_children = list(getattr(source, "args", ()))
        target_children = list(getattr(target, "args", ()))
        common_length = min(len(source_children), len(target_children))
        for index in range(common_length):
            self._diff_node(
                source_children[index],
                target_children[index],
                route + [index],
                changes,
            )

        for index in range(len(source_children) - 1, len(target_children) - 1, -1):
            child = source_children[index]
            changes.append(
                {
                    "action": (
                        "removeTextElement" if _is_text_node(child) else "removeElement"
                    ),
                    "route": route + [index],
                    "oldValue": nodeToObj(child),
                }
            )

        for index in range(common_length, len(target_children)):
            child = target_children[index]
            changes.append(
                {
                    "action": (
                        "addTextElement" if _is_text_node(child) else "addElement"
                    ),
                    "route": route + [index],
                    "element": nodeToObj(child),
                }
            )

    def _diff_attributes(
        self,
        source: Element,
        target: Element,
        route: list[int],
        changes: list[dict[str, Any]],
    ) -> None:
        source_attrs = _attributes(source)
        target_attrs = _attributes(target)
        for name in sorted(source_attrs.keys() - target_attrs.keys()):
            changes.append(
                {
                    "action": "removeAttribute",
                    "route": route,
                    "name": name,
                    "oldValue": source_attrs[name],
                }
            )
        for name in sorted(target_attrs.keys() - source_attrs.keys()):
            changes.append(
                {
                    "action": "addAttribute",
                    "route": route,
                    "name": name,
                    "value": target_attrs[name],
                }
            )
        for name in sorted(source_attrs.keys() & target_attrs.keys()):
            if source_attrs[name] != target_attrs[name]:
                changes.append(
                    {
                        "action": "modifyAttribute",
                        "route": route,
                        "name": name,
                        "oldValue": source_attrs[name],
                        "newValue": target_attrs[name],
                    }
                )

    def _apply_change(self, tree: Node, change: dict[str, Any]) -> None:
        action = change["action"]
        route = list(change.get("route", ()))

        if action in {"addAttribute", "modifyAttribute"}:
            _get_from_route(tree, route).setAttribute(
                change["name"], change.get("value", change.get("newValue"))
            )
            return
        if action == "removeAttribute":
            _get_from_route(tree, route).removeAttribute(change["name"])
            return

        if action == "modifyTextElement":
            _set_text_value(tree, route, change["newValue"])
            return
        if action == "modifyComment":
            _get_from_route(tree, route).data = change["newValue"]
            return

        if action == "replaceElement":
            replacement = objToNode(change["newValue"])
            if route:
                parent = _get_from_route(tree, route[:-1])
                _replace_child_at(parent, route[-1], replacement)
            else:
                _replace_node_contents(tree, replacement)
            return

        if action in {"addElement", "addTextElement"}:
            if not route:
                raise ValueError("Cannot add a root node")
            parent = _get_from_route(tree, route[:-1])
            _insert_child_at(parent, route[-1], objToNode(change["element"]))
            return

        if action in {"removeElement", "removeTextElement"}:
            if not route:
                raise ValueError("Cannot remove the root node in place")
            parent = _get_from_route(tree, route[:-1])
            _remove_child_at(parent, route[-1])
            return

        raise ValueError(f"Unknown diff action: {action}")

    def _invert_change(self, change: dict[str, Any]) -> dict[str, Any]:
        inverse = dict(change)
        action = inverse["action"]
        if action == "addAttribute":
            inverse["action"] = "removeAttribute"
            inverse["oldValue"] = change.get("value")
        elif action == "removeAttribute":
            inverse["action"] = "addAttribute"
            inverse["value"] = change.get("oldValue")
        elif action == "modifyAttribute":
            inverse["oldValue"], inverse["newValue"] = (
                change.get("newValue"),
                change.get("oldValue"),
            )
        elif action in {"modifyTextElement", "modifyComment"}:
            inverse["oldValue"], inverse["newValue"] = (
                change.get("newValue"),
                change.get("oldValue"),
            )
        elif action in {"addElement", "addTextElement"}:
            inverse["action"] = (
                "removeTextElement" if action == "addTextElement" else "removeElement"
            )
            inverse["oldValue"] = change.get("element")
        elif action in {"removeElement", "removeTextElement"}:
            inverse["action"] = (
                "addTextElement" if action == "removeTextElement" else "addElement"
            )
            inverse["element"] = change.get("oldValue")
        elif action == "replaceElement":
            inverse["oldValue"], inverse["newValue"] = (
                change.get("newValue"),
                change.get("oldValue"),
            )
        else:
            raise ValueError(f"Unknown diff action: {action}")
        return inverse


__all__ = ["DiffDOM", "nodeToObj", "objToNode"]
