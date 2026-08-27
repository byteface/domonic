"""
domonic.webapi.xpath
====================================
https://developer.mozilla.org/en-US/docs/Glossary/XPath

uses elementpath lib.

String children are upgraded to ``Text`` nodes before evaluation so text
selectors work against normal domonic trees.

"""

from __future__ import annotations

import re
from typing import Any, Mapping

try:
    import elementpath
except ImportError:  # pragma: no cover - optional dependency
    elementpath = None


class XPathEvaluator:
    def __init__(self, namespaces: Mapping[str, str] | None = None) -> None:
        """Creates an evaluator with optional namespace prefix mappings."""
        self.namespaces = dict(namespaces or {})

    def createExpression(
        self, expression: str, resolver: Any = None
    ) -> XPathExpression:
        """Compiles an XPath expression for later evaluation."""
        return XPathExpression(
            expression, self.namespaces if resolver is None else resolver
        )

    def createNSResolver(self, nodeResolver: Any) -> "XPathNSResolver":
        """Creates a namespace resolver from a node, mapping, or callable."""
        return XPathNSResolver(nodeResolver, self.namespaces)

    def evaluate(
        self,
        expression: str,
        contextNode: Any,
        resolver: Any = None,
        type: int = 0,
        result: Any = None,
    ) -> "XPathResult":
        """Evaluates an XPath expression against a context node."""
        return self.createExpression(expression, resolver).evaluate(
            contextNode, type, result
        )


class XPathException(Exception):
    INVALID_EXPRESSION_ERR = 51
    TYPE_ERR = 52

    def __init__(self, message: str = "", code: int | None = None) -> None:
        """Creates an XPath exception with an optional DOM-style error code."""
        super().__init__(message)
        self.code = code


class XPathExpression:
    def __init__(self, expr: str, resolver: Any = None):
        # domonic stores rendered attributes with leading underscores internally.
        # Accept browser-style XPath attribute names and normalize them here.
        if not isinstance(expr, str):
            raise TypeError("expr must be a string")
        expr = expr.replace("[@", "[@_")
        expr = expr.replace("[@__", "[@_")
        expr = expr.replace("(@", "(@_")
        expr = expr.replace("(@__", "(@_")
        expr = expr.replace("/@", "/@_")
        expr = expr.replace("/@__", "/@_")

        if len(expr) <= 0:
            raise XPathException(
                "no expression", XPathException.INVALID_EXPRESSION_ERR
            )
        self.expr = expr
        self.resolver = resolver
        self.namespaces = self._resolver_namespaces(resolver, expr)
        try:
            self.selector = (
                elementpath.Selector(expr, namespaces=self.namespaces or None)
                if elementpath is not None
                else None
            )
        except Exception as exc:
            raise XPathException(
                str(exc), XPathException.INVALID_EXPRESSION_ERR
            ) from exc

    @staticmethod
    def _expression_prefixes(expr: str) -> set[str]:
        expr = re.sub(r"'[^']*'|\"[^\"]*\"", "", expr)
        prefixes = set(re.findall(r"\b([A-Za-z_][\w.-]*)\:[A-Za-z_][\w.-]*", expr))
        return {prefix for prefix in prefixes if prefix not in {"http", "https"}}

    @staticmethod
    def _resolver_namespaces(resolver: Any, expr: str) -> dict[str, str]:
        if resolver is None:
            return {}
        if isinstance(resolver, XPathNSResolver):
            namespaces = dict(resolver.namespaces)
            for prefix in XPathExpression._expression_prefixes(expr):
                uri = resolver.lookupNamespaceURI(prefix)
                if uri:
                    namespaces[prefix] = uri
            return namespaces
        if isinstance(resolver, Mapping):
            return {str(prefix): str(uri) for prefix, uri in resolver.items()}
        if callable(resolver):
            namespaces = {}
            for prefix in XPathExpression._expression_prefixes(expr):
                uri = resolver(prefix)
                if uri:
                    namespaces[prefix] = uri
            return namespaces
        lookup = getattr(resolver, "lookupNamespaceURI", None)
        if callable(lookup):
            namespaces = {}
            for prefix in XPathExpression._expression_prefixes(expr):
                uri = lookup(prefix)
                if uri:
                    namespaces[prefix] = uri
            return namespaces
        return {}

    @staticmethod
    def _upgrade_dom(node: Any) -> Any:
        def upgrade(el):
            from domonic.dom import Text

            if isinstance(el, (Text, str)):
                return
            for child in el:
                if isinstance(child, str):
                    newchild = Text(child)
                    el.replaceChild(newchild, child)
                    newchild.parentNode = el

        node._iterate(node, upgrade)
        return node

    @staticmethod
    def _iter_descendants(node: Any) -> list[Any]:
        from domonic.dom import Element, Text

        descendants = []

        def walk(current):
            if isinstance(current, (Element, Text)):
                descendants.append(current)
            for child in getattr(current, "args", []):
                if isinstance(child, str):
                    continue
                walk(child)

        for child in getattr(node, "args", []):
            if isinstance(child, str):
                continue
            walk(child)
        return descendants

    @staticmethod
    def _iter_children(node: Any) -> list[Any]:
        from domonic.dom import Element, Text

        children = []
        for child in getattr(node, "args", []):
            if isinstance(child, (Element, Text)):
                children.append(child)
        return children

    @staticmethod
    def _parse_steps(expr: str) -> list[tuple[str, str]]:
        steps = []
        i = 0
        axis = "child"
        if expr.startswith("//"):
            axis = "descendant"
            i = 2
        elif expr.startswith("/"):
            axis = "child"
            i = 1
        current = []
        bracket_depth = 0
        paren_depth = 0
        quote = None
        while i < len(expr):
            char = expr[i]
            if quote is not None:
                current.append(char)
                if char == quote:
                    quote = None
                i += 1
                continue
            if char in ("'", '"'):
                quote = char
                current.append(char)
                i += 1
                continue
            if char == "[":
                bracket_depth += 1
            elif char == "]":
                bracket_depth -= 1
            elif char == "(":
                paren_depth += 1
            elif char == ")":
                paren_depth -= 1
            if bracket_depth == 0 and paren_depth == 0:
                if expr.startswith("//", i):
                    if current:
                        steps.append((axis, "".join(current)))
                        current = []
                    axis = "descendant"
                    i += 2
                    continue
                if char == "/":
                    if current:
                        steps.append((axis, "".join(current)))
                        current = []
                    axis = "child"
                    i += 1
                    continue
            current.append(char)
            i += 1
        if current:
            steps.append((axis, "".join(current)))
        return steps

    @staticmethod
    def _parse_step(step: str) -> tuple[str, list[str]]:
        predicates = []
        name_chars = []
        i = 0
        while i < len(step) and step[i] != "[":
            name_chars.append(step[i])
            i += 1
        name = "".join(name_chars).strip() or "*"
        while i < len(step):
            if step[i] != "[":
                i += 1
                continue
            depth = 1
            i += 1
            start = i
            quote = None
            while i < len(step) and depth > 0:
                char = step[i]
                if quote is not None:
                    if char == quote:
                        quote = None
                    i += 1
                    continue
                if char in ("'", '"'):
                    quote = char
                elif char == "[":
                    depth += 1
                elif char == "]":
                    depth -= 1
                    if depth == 0:
                        predicates.append(step[start:i].strip())
                        i += 1
                        break
                i += 1
        return name, predicates

    @staticmethod
    def _node_name(node: Any) -> str:
        return getattr(node, "tagName", getattr(node, "name", ""))

    @staticmethod
    def _predicate_matches(
        node: Any, predicate: str, index: int, nodes: list[Any]
    ) -> bool:
        from domonic.dom import Text

        if predicate.isdigit():
            return index == int(predicate) - 1
        if predicate in {"position()=last()", "position() = last()"}:
            return index == len(nodes) - 1
        if predicate.startswith("position()"):
            _, _, value = predicate.partition("=")
            try:
                return index == int(value.strip()) - 1
            except ValueError:
                return False
        if predicate == "last()":
            return index == len(nodes) - 1
        if predicate.startswith("name()="):
            expected = predicate.split("=", 1)[1].strip().strip("'\"")
            return XPathExpression._node_name(node) == expected
        if predicate.startswith("@"):
            attr, _, value = predicate.partition("=")
            attr = attr[1:]
            if value:
                value = value.strip().strip("'\"")
                return node.getAttribute(attr) == value
            return node.getAttribute(attr) is not None
        if predicate.startswith("contains(") and predicate.endswith(")"):
            inner = predicate[len("contains(") : -1]
            attr_expr, _, needle = inner.partition(",")
            attr_expr = attr_expr.strip()
            needle = needle.strip().strip("'\"")
            if attr_expr.startswith("@"):
                attr_value = node.getAttribute(attr_expr[1:]) or ""
                return needle in attr_value
        if predicate.startswith("starts-with(") and predicate.endswith(")"):
            inner = predicate[len("starts-with(") : -1]
            attr_expr, _, needle = inner.partition(",")
            attr_expr = attr_expr.strip()
            needle = needle.strip().strip("'\"")
            if attr_expr.startswith("@"):
                attr_value = node.getAttribute(attr_expr[1:]) or ""
                return attr_value.startswith(needle)
        if predicate.startswith("ends-with(") and predicate.endswith(")"):
            inner = predicate[len("ends-with(") : -1]
            attr_expr, _, needle = inner.partition(",")
            attr_expr = attr_expr.strip()
            needle = needle.strip().strip("'\"")
            if attr_expr.startswith("@"):
                attr_value = node.getAttribute(attr_expr[1:]) or ""
                return attr_value.endswith(needle)
        return False

    @staticmethod
    def _step_matches(node: Any, name: str) -> bool:
        from domonic.dom import Element, Text

        if name == "text()":
            return isinstance(node, Text)
        if not isinstance(node, Element):
            return False
        if name == "*":
            return True
        return XPathExpression._node_name(node) == name

    def _fallback_select(self, node: Any) -> list[Any]:
        from domonic.dom import Text

        if self.expr == "/":
            return [node]

        nodes = [node]
        for axis, raw_step in self._parse_steps(self.expr):
            name, predicates = self._parse_step(raw_step)
            candidates = []
            for current in nodes:
                if axis == "descendant":
                    scope = self._iter_descendants(current)
                else:
                    scope = self._iter_children(current)
                for candidate in scope:
                    if self._step_matches(candidate, name):
                        candidates.append(candidate)
            if predicates:
                filtered = []
                for idx, candidate in enumerate(candidates):
                    if all(
                        self._predicate_matches(candidate, predicate, idx, candidates)
                        for predicate in predicates
                    ):
                        filtered.append(candidate)
                candidates = filtered
            nodes = candidates
        return nodes

    def evaluate(
        self, node: Any, type: int = 6, result: Any = None
    ):  # XPathResult.ANY_TYPE):
        # note: otherwise would fail on regular text?
        node = XPathExpression._upgrade_dom(node)
        try:
            value = (
                self.selector.select(node)
                if self.selector is not None
                else self._fallback_select(node)
            )
        except Exception as exc:
            raise XPathException(
                str(exc), XPathException.INVALID_EXPRESSION_ERR
            ) from exc
        xpath_result = XPathResult(value, type)
        if isinstance(result, XPathResult):
            result.__dict__.clear()
            result.__dict__.update(xpath_result.__dict__)
            return result
        return xpath_result


class XPathNSResolver:
    def __init__(
        self, nodeResolver: Any = None, namespaces: Mapping[str, str] | None = None
    ) -> None:
        """Creates a namespace resolver from a node, mapping, or callable."""
        from domonic.constants import namespaces as default_namespaces

        self.nodeResolver = nodeResolver
        self.namespaces = dict(default_namespaces)
        self.namespaces.update(namespaces or {})
        if isinstance(nodeResolver, Mapping):
            self.namespaces.update(
                {str(prefix): str(uri) for prefix, uri in nodeResolver.items()}
            )

    def lookupNamespaceURI(self, prefix: str | None) -> str | None:
        """Returns the namespace URI for a prefix."""
        attr_name = "xmlns" if prefix in (None, "") else f"xmlns:{prefix}"
        current = self.nodeResolver
        while current is not None and not isinstance(current, Mapping):
            get_attribute = getattr(current, "getAttribute", None)
            if callable(get_attribute):
                uri = get_attribute(attr_name)
                if uri is not None:
                    return uri
            current = getattr(current, "parentNode", None)

        if callable(self.nodeResolver):
            uri = self.nodeResolver(prefix)
            if uri:
                return uri

        lookup = getattr(self.nodeResolver, "lookupNamespaceURI", None)
        if callable(lookup):
            uri = lookup(prefix)
            if uri:
                return uri

        if prefix in (None, ""):
            return None
        return self.namespaces.get(prefix)


class XPathResult:

    ANY_TYPE = 0
    NUMBER_TYPE = 1
    STRING_TYPE = 2
    BOOLEAN_TYPE = 3
    UNORDERED_NODE_ITERATOR_TYPE = 4
    ORDERED_NODE_ITERATOR_TYPE = 5
    UNORDERED_NODE_SNAPSHOT_TYPE = 6
    ORDERED_NODE_SNAPSHOT_TYPE = 7
    ANY_UNORDERED_NODE_TYPE = 8
    FIRST_ORDERED_NODE_TYPE = 9

    def __init__(self, value: Any, _type: int):
        if _type == XPathResult.ANY_TYPE:
            if isinstance(value, bool):
                _type = self.BOOLEAN_TYPE
            elif isinstance(value, (int, float)):
                _type = self.NUMBER_TYPE
            elif isinstance(value, str):
                _type = self.STRING_TYPE
            else:
                _type = self.UNORDERED_NODE_ITERATOR_TYPE

        if _type < self.NUMBER_TYPE or self.FIRST_ORDERED_NODE_TYPE < _type:
            raise XPathException(f"unknown type: {_type}", XPathException.TYPE_ERR)

        self.resultType = _type
        self.booleanValue = None
        self.invalidIteratorState = False
        self.nodes = []
        self.numberValue = None
        self.singleNodeValue = None
        self.snapshotLength = 0
        self.stringValue = None
        self.index = 0

        if _type == self.NUMBER_TYPE:
            # self.numberValue=value.number() if getattr(value,'isNodeSet',None) else toNumber(value)
            if getattr(value, "isNodeSet", None):
                self.numberValue = value  # .number()
            else:
                self.numberValue = float(value)
        elif _type == self.STRING_TYPE:
            # self.stringValue=value.string() if getattr(value,'isNodeSet',None) else toString(value)
            if getattr(value, "isNodeSet", None):
                self.stringValue = value  # .string()
            else:
                first = self._first(value)
                self.stringValue = "" if first is None else str(first)
        elif _type == self.BOOLEAN_TYPE:
            # self.booleanValue=value.bool() if getattr(value,'isNodeSet',None) else toBoolean(value)
            if getattr(value, "isNodeSet", None):
                self.booleanValue = value  # .bool()
            elif isinstance(value, (list, tuple)):
                self.booleanValue = bool(value)
            else:
                self.booleanValue = bool(value)
        elif (
            _type == self.ANY_UNORDERED_NODE_TYPE
            or _type == self.FIRST_ORDERED_NODE_TYPE
        ):
            self.singleNodeValue = self._first(value)  # .first()
        else:
            self.nodes = self._nodes(value)  # .list()
            self.snapshotLength = len(self.nodes)

    @staticmethod
    def _nodes(value: Any) -> list[Any]:
        if value is None:
            return []
        if isinstance(value, list):
            return value
        if isinstance(value, tuple):
            return list(value)
        if isinstance(value, (str, bytes)):
            return [value]
        if hasattr(value, "__iter__"):
            return list(value)
        return [value]

    @classmethod
    def _first(cls, value: Any) -> Any:
        nodes = cls._nodes(value)
        return nodes[0] if nodes else None

    def iterateNext(self):
        """Returns the next node from an iterator result, or ``None``."""
        if self.index >= len(self.nodes):
            return None
        node = self.nodes[self.index]
        self.index += 1
        return node

    def snapshotItem(self, i):
        """Returns a node from a snapshot result by index, or ``None``."""
        if i < 0 or i >= len(self.nodes):
            return None
        return self.nodes[i]
