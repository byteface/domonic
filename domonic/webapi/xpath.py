"""
    domonic.webapi.xpath
    ====================================
    https://developer.mozilla.org/en-US/docs/Glossary/XPath

    uses elementpath lib.

    TODO - content strings must be TextNodes for it to work.
        so will have to iterate and update them. i.e. Treewalker

"""

from typing import Any, Callable, Dict, List, Optional, Union

try:
    import elementpath
except ImportError:  # pragma: no cover - optional dependency
    elementpath = None


class XPathEvaluator:
    def __init__(self) -> None:
        pass

    def createExpression(self, expression: str):  # , namespaces: Dict[str, str]) -> None:
        return XPathExpression(expression)


class XPathException:
    def __init__(self) -> None:
        pass


class XPathExpression:
    def __init__(self, expr: str):  # , resolver):
        # TODO - hack.
        # need to allow non underscore accessors to get underscored.
        # when that's fixed can remove this.
        expr = expr.replace("[@", "[@_")
        expr = expr.replace("[@__", "[@_")
        expr = expr.replace("(@", "(@_")
        expr = expr.replace("(@__", "(@_")
        expr = expr.replace("/@", "/@_")
        expr = expr.replace("/@__", "/@_")

        if len(expr) <= 0:
            raise Exception("no expression")
        self.expr = expr
        self.selector = elementpath.Selector(expr) if elementpath is not None else None

    # TODO - DRY - make some utils . just stole this from Treewalker.
    @staticmethod
    def _upgrade_dom(node):
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
    def _iter_descendants(node):
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
    def _iter_children(node):
        from domonic.dom import Element, Text

        children = []
        for child in getattr(node, "args", []):
            if isinstance(child, (Element, Text)):
                children.append(child)
        return children

    @staticmethod
    def _parse_steps(expr):
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
    def _parse_step(step):
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
    def _node_name(node):
        return getattr(node, "tagName", getattr(node, "name", ""))

    @staticmethod
    def _predicate_matches(node, predicate, index, nodes):
        from domonic.dom import Text

        if predicate == "last()":
            return index == len(nodes) - 1
        if predicate.startswith('name()='):
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
        return False

    @staticmethod
    def _step_matches(node, name):
        from domonic.dom import Element, Text

        if name == "text()":
            return isinstance(node, Text)
        if not isinstance(node, Element):
            return False
        if name == "*":
            return True
        return XPathExpression._node_name(node) == name

    def _fallback_select(self, node):
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
                    if all(self._predicate_matches(candidate, predicate, idx, candidates) for predicate in predicates):
                        filtered.append(candidate)
                candidates = filtered
            nodes = candidates
        return nodes

    def evaluate(self, node, type=6):  # XPathResult.ANY_TYPE):
        # note: otherwise would fail on regular text?
        node = XPathExpression._upgrade_dom(node)
        if self.selector is not None:
            return XPathResult(self.selector.select(node), type)
        return XPathResult(self._fallback_select(node), type)


class XPathNSResolver:
    def __init__(self) -> None:
        pass


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

    def __init__(self, value, _type):
        if _type == XPathResult.ANY_TYPE:
            tov = type(value)
            if tov == "object":
                _type = self.UNORDERED_NODE_ITERATOR_TYPE
            if tov == "boolean":
                _type = self.BOOLEAN_TYPE
            if tov == "string":
                _type = self.STRING_TYPE
            if tov == "number":
                _type = self.NUMBER_TYPE

        if _type < self.NUMBER_TYPE or self.FIRST_ORDERED_NODE_TYPE < _type:
            raise Exception(f"unknown type: {_type}")

        self.resultType = _type

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
                self.stringValue = str(value)
        elif _type == self.BOOLEAN_TYPE:
            # self.booleanValue=value.bool() if getattr(value,'isNodeSet',None) else toBoolean(value)
            if getattr(value, "isNodeSet", None):
                self.booleanValue = value  # .bool()
            else:
                self.booleanValue = bool(value)
        elif _type == self.ANY_UNORDERED_NODE_TYPE or _type == self.FIRST_ORDERED_NODE_TYPE:
            self.singleNodeValue = value  # .first()
        else:
            self.nodes = value  # .list()
            self.snapshotLength = len(value)
            self.index = 0
            self.invalidIteratorState = False

    # def iterateNext(self):
    #     node = self.nodes[self.index]
    #     self.index += 1
    #     return node

    # def snapshotItem(self, i):
    #     return self.nodes[i]
