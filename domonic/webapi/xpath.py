"""
    domonic.webapi.xpath
    ====================================
    https://developer.mozilla.org/en-US/docs/Glossary/XPath

    uses elementpath lib.

    TODO - content strings must be TextNodes for it to work. 
        so will have to iterate and update them. i.e. Treewalker

"""

import json
import os
import sys
from typing import Any, Callable, Dict, List, Optional, Union

import elementpath


class XPathEvaluator:

    def __init__(self) -> None:
        pass

    def createExpression(self, expression: str):  # , namespaces: Dict[str, str]) -> None:
        return XPathExpression(expression)


class XPathException:
    def __init__(self) -> None:
        pass


class XPathExpression(object):

    def __init__(self, expr: str):  #, resolver):

        # TODO - hack.
        # need to allow non underscore accessors to get underscored.
        # when that's fixed can remove this.
        expr = expr.replace('[@', '[@_')
        expr = expr.replace('[@__', '[@_')
        expr = expr.replace('(@', '(@_')
        expr = expr.replace('(@__', '(@_')
        expr = expr.replace('/@', '/@_')
        expr = expr.replace('/@__', '/@_')

        if len(expr) <= 0:
            raise Exception('no expression')
        self.selector = elementpath.Selector(expr)

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

    def evaluate(self, node, type=6):  # XPathResult.ANY_TYPE):
        # note: otherwise would fail on regular text?
        node = XPathExpression._upgrade_dom(node)
        return XPathResult(self.selector.select(node), type)


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
            if tov == 'object':
                _type = self.UNORDERED_NODE_ITERATOR_TYPE
            if tov == 'boolean':
                _type = self.BOOLEAN_TYPE
            if tov == 'string':
                _type = self.STRING_TYPE
            if tov == 'number':
                _type = self.NUMBER_TYPE

        if _type < self.NUMBER_TYPE or self.FIRST_ORDERED_NODE_TYPE < _type:
            raise Exception(f'unknown type: {_type}')

        self.resultType = _type

        if _type == self.NUMBER_TYPE:
            #self.numberValue=value.number() if getattr(value,'isNodeSet',None) else toNumber(value)
            if getattr(value, 'isNodeSet', None):
                self.numberValue = value#.number()
            else:
                self.numberValue = float(value)
        elif _type == self.STRING_TYPE:
            #self.stringValue=value.string() if getattr(value,'isNodeSet',None) else toString(value)
            if getattr(value, 'isNodeSet', None):
                self.stringValue = value#.string()
            else:
                self.stringValue = str(value)
        elif _type == self.BOOLEAN_TYPE:
            #self.booleanValue=value.bool() if getattr(value,'isNodeSet',None) else toBoolean(value)
            if getattr(value, 'isNodeSet', None):
                self.booleanValue = value#.bool()
            else:
                self.booleanValue = bool(value)
        elif _type == self.ANY_UNORDERED_NODE_TYPE or _type == self.FIRST_ORDERED_NODE_TYPE:
            self.singleNodeValue = value#.first()
        else:
            self.nodes = value#.list()
            self.snapshotLength = len(value)
            self.index = 0
            self.invalidIteratorState = False

    # def iterateNext(self):
    #     node = self.nodes[self.index]
    #     self.index += 1
    #     return node

    # def snapshotItem(self, i):
    #     return self.nodes[i]
