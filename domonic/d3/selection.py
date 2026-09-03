"""
domonic.d3.selection
====================================

https://github.com/d3/d3-selection/tree/main/src/selection

"""

# from domonic.html import *

import inspect
import re
from functools import cmp_to_key

from domonic.dom import Node, document  # bring in the global
from domonic.javascript import *

xhtml = "http://www.w3.org/1999/xhtml"

namespaces = {
    "svg": "http://www.w3.org/2000/svg",
    "xhtml": xhtml,
    "xlink": "http://www.w3.org/1999/xlink",
    "xml": "http://www.w3.org/XML/1998/namespace",
    "xmlns": "http://www.w3.org/2000/xmlns/",
}


# export {default as namespace} from "./namespace.js";
# export {default as namespaces} from "./namespaces.js";
def namespace(name):
    name = str(name)
    prefix = name
    i = String(prefix).indexOf(":")
    if i > 0:
        prefix = String(name).slice(0, i)
    if i >= 0 and prefix != "xmlns":
        name = String(name).slice(i + 1)
    return (
        {"space": namespaces[prefix], "local": name}
        if Object(namespaces).hasOwnProperty(prefix)
        else name
    )  # eslint-disable-line no-prototype-builtins


def creatorInherit(name):
    def anon(this, *args):
        from domonic.dom import document

        owner_document = this.ownerDocument or document
        uri = getattr(this, "namespaceURI", xhtml)
        return (
            owner_document.createElement(name)
            if uri == xhtml and owner_document.documentElement.namespaceURI == xhtml
            else owner_document.createElementNS(uri, name)
        )

    return anon


def creatorFixed(fullname):
    # return lambda this: this.ownerDocument.createElementNS(fullname['space'], fullname['local'])
    from domonic.dom import document  # bring in the global document

    return lambda *args: document.ownerDocument.createElementNS(
        fullname["space"], fullname["local"]
    )


def creator(name):
    fullname = namespace(name)
    func = creatorFixed if isinstance(fullname, dict) else creatorInherit
    return func(fullname)


def none():
    return {}


def selector(selector):
    return (
        None if selector == None else lambda this, *args: this.querySelector(selector)
    )


# // Given something array like (or null), returns something that is strictly an
# // array. This is used to ensure that array-like objects passed to d3.selectAll
# // or selection.selectAll are converted into proper arrays when creating a
# // selection; we don’t ever want to create a selection backed by a live
# // HTMLCollection or NodeList. However, note that selection.selectAll will use a
# // static NodeList as a group, since it safely derived from querySelectorAll.
def array(x):  # type: ignore[no-redef]
    b = x if Array.isArray(x) else Array.from_(x)
    return [] if x == None else b


# export {default as window} from "./window.js";
def window(node):  # type: ignore[no-redef]
    return (
        (node.ownerDocument and node.ownerDocument.defaultView)
        or (node.document and node)
        or node.defaultView
    )


defaultView = window

# import selection_select from "./select.js";


# import selection_style from "./style.js";
def styleValue(node, name):
    return node.style.getPropertyValue(name) or defaultView(node).getComputedStyle(
        node, None
    ).getPropertyValue(name)


def sparse(self, update):
    return Array(len(update))


class EnterNode:
    def __init__(self, parent, datum):
        self.ownerDocument = parent.ownerDocument
        self.namespaceURI = parent.namespaceURI
        self._next = None
        self._parent = parent
        self.__data__ = datum

    def appendChild(self, child):
        return self._parent.insertBefore(child, self._next)

    def insertBefore(self, child, next):
        return self._parent.insertBefore(child, next)

    def querySelector(self, selector):
        return self._parent.querySelector(selector)

    def querySelectorAll(self, selector):
        return self._parent.querySelectorAll(selector)


class ClassList:
    def __init__(self, node):
        self._node = node
        self._names = classArray(node.getAttribute("class") or "")

    def add(self, name):
        if name not in self._names:
            self._names.append(name)
            self._node.setAttribute("class", " ".join(self._names))

    def remove(self, name):
        if name in self._names:
            self._names.remove(name)
            self._node.setAttribute("class", " ".join(self._names))

    def contains(self, name):
        return name in self._names


def classArray(string):
    string = String(string).trim()
    if string == "":
        return []
    return re.split(r"\s+", string)


def classList(node):
    # return node.classList or ClassList(node)
    return ClassList(node)


def classedAdd(node, names):
    mylist = classList(node)
    for name in names:
        mylist.add(name)


def classedRemove(node, names):
    mylist = classList(node)
    for name in names:
        mylist.remove(name)


# import selection_append from "./append.js";


root = [None]
_MISSING = object()


def _invoke_callback(callback, *args):
    try:
        signature = inspect.signature(callback)
    except (TypeError, ValueError):
        return callback(*args)

    parameters = list(signature.parameters.values())
    if any(param.kind == inspect.Parameter.VAR_POSITIONAL for param in parameters):
        return callback(*args)

    positional = [
        param
        for param in parameters
        if param.kind
        in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
    ]
    return callback(*args[: len(positional)])


def _children_of(node):
    children = getattr(node, "children", [])
    if callable(children):
        children = children()
    return list(children or [])


def _first_element_child(node):
    child = getattr(node, "firstElementChild", None)
    return child() if callable(child) else child


def _set_property(node, name, value):
    setattr(node, name, value)


def _get_property(node, name):
    if node is None:
        return None
    if name in getattr(node, "__dict__", {}):
        return node.__dict__[name]
    if hasattr(type(node), name):
        return getattr(node, name)
    kwargs = getattr(node, "kwargs", {})
    if name in kwargs:
        return kwargs[name]
    storage_name = name if str(name).startswith("_") else f"_{name}"
    if storage_name in kwargs:
        return kwargs[storage_name]
    return None


def _remove_property(node, name):
    if name in getattr(node, "__dict__", {}):
        delattr(node, name)
        return
    kwargs = getattr(node, "kwargs", None)
    if kwargs is None:
        return
    candidates = [name]
    if str(name).startswith("_"):
        candidates.append(str(name)[1:])
    else:
        candidates.append(f"_{name}")
    for candidate in candidates:
        if candidate in kwargs:
            del kwargs[candidate]
            return


class Selection:
    def __init__(self, groups, parents, this=None):
        self._groups = groups
        self._parents = parents
        if this is None:
            self.this = root[0]
        else:
            self.this = this  # context switcher

    # unpack groups into a list of nodes
    def __iter__(self):
        for group in self._groups:
            for node in group:
                if node is not None:
                    yield node

    def select(self, select):
        if not callable(select):
            select = selector(select)

        groups = self._groups
        m = len(groups)
        subgroups = Array(m)
        j = 0
        for group in groups:
            n = len(group)
            subgroup = subgroups[j] = Array(n)
            for i in range(n):
                node = group[i]
                if node is None:
                    subgroup[i] = None
                    continue
                try:
                    data = getattr(node, "__data__", None)
                    subnode = select(node, data, i, group)
                except Exception as e:
                    subnode = None
                if subnode is not None and hasattr(node, "__data__"):
                    subnode.__data__ = node.__data__
                subgroup[i] = subnode
            j += 1

        return Selection(subgroups, self._parents, self.this)

    # import selection_selectAll from "./selectAll.js";
    # import {Selection} from "./index.js";
    # import array from "../array.js";
    # import selectorAll from "../selectorAll.js";

    def arrayAll(self, select, *args):
        return lambda this, *call_args: array(select(this, *call_args))

    def selectAll(self, select):
        if callable(select):
            select = self.arrayAll(select)
        else:
            select = selectorAll(select)

        groups = self._groups
        m = len(groups)
        subgroups = []
        parents = []
        j = 0
        for group in groups:
            n = len(group)
            for i in range(n):
                node = group[i]
                if node is None:
                    continue

                try:
                    data = getattr(node, "__data__", None)
                    subgroups.append(select(node, data, i, group))
                    parents.append(node)
                except Exception as e:
                    subgroups.append([])
                    parents.append(node)

                # subgroups.append(Function(select).call(node, node.__data__, i, group))
                # parents.append(node)
            j += 1
        return Selection(subgroups, parents, self.this)

    # import selection_selectChild from "./selectChild.js";
    # import {childMatcher} from "../matcher.js";

    def childFind(self, match):
        def find_child(node, *args):
            children = _children_of(node)
            for i, child in enumerate(children):
                if _invoke_callback(
                    match, child, getattr(child, "__data__", None), i, children
                ):
                    return child
            return None

        return find_child

    def childFirst(self, node, *args):
        return _first_element_child(node)

    def selectChild(self, match=None):
        if match is None:
            select = self.childFirst
        else:
            select = self.childFind(match if callable(match) else childMatcher(match))
        return self.select(select)

    # import selection_selectChildren from "./selectChildren.js";
    # def selectChildren: selection_selectChildren,
    # import {childMatcher} from "../matcher.js";

    # filter = Array.prototype.filter

    def children(self, node, *args):
        return _children_of(node)

    def childrenFilter(self, match):
        def filter_children(node, *args):
            children = _children_of(node)
            return [
                child
                for i, child in enumerate(children)
                if _invoke_callback(
                    match, child, getattr(child, "__data__", None), i, children
                )
            ]

        return filter_children

    def selectChildren(self, match=None):
        if match is None:
            return self.selectAll(self.children)
        return self.selectAll(
            self.childrenFilter(match if callable(match) else childMatcher(match))
        )

    # import selection_filter from "./filter.js";
    # def filter: selection_filter,
    def filter(self, match):
        if not callable(match):
            match = matcher(match)

        groups = self._groups
        subgroups = []
        for group in groups:
            subgroup = []
            for i in range(len(group)):
                node = group[i]
                if node is None:
                    continue
                data = getattr(node, "__data__", None)
                if _invoke_callback(match, node, data, i, group):
                    subgroup.append(node)
            subgroups.append(subgroup)
        return Selection(subgroups, self._parents, self.this)

    def data(self, value=_MISSING, key=None):
        if value is _MISSING:
            return [getattr(node, "__data__", None) for node in self]

        bind = self._bind_key if callable(key) else self._bind_index
        update_groups = []
        enter_groups = []
        exit_groups = []

        for j, group in enumerate(self._groups):
            parent = self._parents[j] if j < len(self._parents) else None
            parent_data = getattr(parent, "__data__", None)
            values = (
                _invoke_callback(value, parent_data, j, self._parents)
                if callable(value)
                else value
            )
            data_values = array(values)
            update, enter, exit_ = bind(parent, group, data_values, key)
            update_groups.append(update)
            enter_groups.append(enter)
            exit_groups.append(exit_)

        selection = Selection(update_groups, self._parents, self.this)
        selection._enter = enter_groups
        selection._exit = exit_groups
        return selection

    def _bind_index(self, parent, group, data_values, key=None):
        update = Array(len(data_values))
        enter = Array(len(data_values))
        exit_ = []
        group_length = len(group)

        for i, datum in enumerate(data_values):
            node = group[i] if i < group_length else None
            if node is None:
                enter[i] = EnterNode(parent, datum) if parent is not None else None
                update[i] = None
            else:
                node.__data__ = datum
                update[i] = node
                enter[i] = None

        for i in range(len(data_values), group_length):
            node = group[i]
            if node is not None:
                exit_.append(node)

        self._link_enter_nodes(enter, update)
        return update, enter, exit_

    def _bind_key(self, parent, group, data_values, key):
        update = Array(len(data_values))
        enter = Array(len(data_values))
        exit_ = []
        node_by_key = {}

        for i, node in enumerate(group):
            if node is None:
                continue
            node_key = str(
                _invoke_callback(key, getattr(node, "__data__", None), i, group)
            )
            if node_key in node_by_key:
                exit_.append(node)
            else:
                node_by_key[node_key] = node

        for i, datum in enumerate(data_values):
            data_key = str(_invoke_callback(key, datum, i, data_values))
            node = node_by_key.pop(data_key, None)
            if node is None:
                enter[i] = EnterNode(parent, datum) if parent is not None else None
                update[i] = None
            else:
                node.__data__ = datum
                update[i] = node
                enter[i] = None

        exit_.extend(node_by_key.values())
        self._link_enter_nodes(enter, update)
        return update, enter, exit_

    def _link_enter_nodes(self, enter, update):
        next_node = None
        for i in range(len(enter) - 1, -1, -1):
            node = update[i]
            if node is not None:
                next_node = node
                continue
            enter_node = enter[i]
            if enter_node is not None:
                enter_node._next = next_node

    # import selection_enter from "./enter.js";
    # def enter: selection_enter,
    # import sparse from "./sparse.js";
    # import {Selection} from "./index.js";

    def enter(self):
        groups = getattr(self, "_enter", None)
        if groups is None:
            groups = [sparse(self, group) for group in self._groups]
        return Selection(groups, self._parents, self.this)

    # import selection_exit from "./exit.js";
    # def exit: selection_exit,
    # import sparse from "./sparse.js";
    # import {Selection} from "./index.js";
    def exit(self):
        groups = getattr(self, "_exit", None)
        if groups is None:
            groups = [sparse(self, group) for group in self._groups]
        return Selection(groups, self._parents, self.this)

    # import selection_join from "./join.js";
    # def join: selection_join,
    def join(self, onenter, onupdate=None, onexit=None):
        enter = self.enter()
        update = self
        exit = self.exit()
        if callable(onenter):
            enter = onenter(enter)
            if enter and hasattr(enter, "selection"):
                enter = enter.selection()
        else:
            enter = enter.append(str(onenter))

        if onupdate != None:
            update = onupdate(update)
            if update and hasattr(update, "selection"):
                update = update.selection()
        if onexit == None:
            exit.remove()
        else:
            onexit(exit)
        return enter.merge(update).order() if enter and update else update

    # import selection_merge from "./merge.js";
    # def merge: selection_merge,
    # import {Selection} from "./index.js";
    def merge(self, context):
        selection_method = getattr(context, "selection", None)
        selection = selection_method() if callable(selection_method) else context
        groups0 = self._groups
        groups1 = selection._groups
        merges = []

        for j, group0 in enumerate(groups0):
            if j >= len(groups1):
                merges.append(group0)
                continue

            group1 = groups1[j]
            merge = Array(len(group0))
            for i, node0 in enumerate(group0):
                node1 = group1[i] if i < len(group1) else None
                merge[i] = node0 or node1
            merges.append(merge)

        return Selection(merges, self._parents, self.this)

    def selection(self):
        return self

    # import selection_order from "./order.js";
    # def order: selection_order,
    def order(self):
        for group in self._groups:
            next_node = None
            i = len(group) - 1
            while i >= 0:
                node = group[i]
                if node is None:
                    i -= 1
                    continue
                if next_node is not None:
                    position = node.compareDocumentPosition(next_node)
                    if (
                        position != Node.DOCUMENT_POSITION_FOLLOWING
                        and next_node.parentNode is not None
                    ):
                        next_node.parentNode.insertBefore(node, next_node)
                next_node = node
                i -= 1
        return self

    # import selection_sort from "./sort.js";
    # def sort: selection_sort,
    # import {Selection} from "./index.js";
    def sort(self, compare=None):
        if compare is None:
            compare = self.ascending

        def compareNode(a, b):
            if a and b:
                result = _invoke_callback(
                    compare, getattr(a, "__data__", None), getattr(b, "__data__", None)
                )
                return 0 if result is None else result
            if not a and not b:
                return 0
            return -1 if a else 1

        sortgroups = []
        for group in self._groups:
            n = len(group)
            sortgroup = []
            for i in range(n):
                node = group[i]
                if node is None:
                    continue
                sortgroup.append(node)
            sortgroup.sort(key=cmp_to_key(compareNode))
            sortgroups.append(sortgroup)
        return Selection(sortgroups, self._parents, self.this).order()

    def ascending(self, a, b):
        # return a < b ? -1 : a > b ? 1 : a >= b ? 0 : NaN
        if a < b:
            return -1
        if a > b:
            return 1
        if a >= b:
            return 0
        return None

    # import selection_call from "./call.js"
    def call(self, *args):
        args = list(args)
        callback = args[0]
        _invoke_callback(callback, self, *args[1:])
        return self

    # import selection_nodes from "./nodes.js";
    def nodes(self):
        return [node for node in self]

    # import selection_node from "./node.js";
    def node(self):
        groups = self._groups
        j = 0
        m = len(groups)
        for group in groups:
            i = 0
            n = len(group)
            while i < n:
                node = group[i]
                if node is not None:
                    return node
                i += 1
        return None

    # import selection_size from "./size.js";
    # def size: selection_size,
    def size(self):
        return len(self.nodes())

    # import selection_empty from "./empty.js";
    # def empty: selection_empty,
    def empty(self):
        # return not self.this.node()
        if isinstance(self.this, list):
            return not self.this

        if self.node() is None:
            return True
        return False
        # return not self.this.node()

    # import selection_each from "./each.js";
    def each(self, callback):
        groups = self._groups
        j = 0
        m = len(groups)
        for group in groups:
            i = 0
            n = len(group)
            while i < n:
                node = group[i]
                if node is None:
                    i += 1
                    continue
                data = getattr(node, "__data__", None)
                _invoke_callback(callback, node, data, i, group)

                i += 1
            j += 1
        return self

    # import selection_attr from "./attr.js";
    def attrRemove(self, name):
        def anon(this, *args):
            this.removeAttribute(name)

        return anon

    def attrRemoveNS(self, fullname):
        def anon(this, *args):
            this.removeAttributeNS(fullname["space"], fullname["local"])

        return anon

    def attrConstant(self, name, value):
        # return lambda: self.setAttribute(name, value)
        # self.this.setAttribute(name, value)
        # return self

        def anon(this, *args):
            nonlocal name
            nonlocal value
            # this.textContent = value
            return this.setAttribute(name, value)

        return anon

    def attrConstantNS(self, fullname, value):
        def anon(this, *args):
            this.setAttributeNS(fullname["space"], fullname["local"], value)

        return anon

    def attrFunction(self, name, value, *args):
        def anon(this, *call_args):
            nonlocal value
            nonlocal name
            v = _invoke_callback(value, *call_args)
            if v == None:
                this.removeAttribute(name)
            else:
                this.setAttribute(name, v)

        return anon

    def attrFunctionNS(self, fullname, value, *args):
        def anon(this, *call_args):
            nonlocal value
            nonlocal fullname
            v = _invoke_callback(value, *call_args)
            if v == None:
                this.removeAttributeNS(fullname["space"], fullname["local"])
            else:
                this.setAttributeNS(fullname["space"], fullname["local"], v)

        return anon

    def attr(self, name, value=_MISSING, *args):
        fullname = namespace(name)

        if value is _MISSING:
            node = self.node()
            if node is None:
                return None
            return (
                node.getAttributeNS(fullname["space"], fullname["local"])
                if isinstance(fullname, dict)
                else node.getAttribute(fullname)
            )

        is_namespaced = isinstance(fullname, dict)
        a = self.attrRemoveNS if is_namespaced else self.attrRemove
        b = self.attrFunctionNS if is_namespaced else self.attrFunction
        c = self.attrConstantNS if is_namespaced else self.attrConstant

        if value is None:
            func = a(fullname) if is_namespaced else a(fullname)
        elif callable(value):
            func = b(fullname, value)
        else:
            func = c(fullname, value)

        self.each(func)
        return self

    # def style: selection_style,
    # import defaultView from "../window.js";
    def _styleRemove(self, name, value, priority=None):
        def anon(this, *args):
            this.style.removeProperty(name)

        return anon

    def _styleConstant(self, name, value, priority=None):
        def anon(this, *args):
            nonlocal name
            nonlocal value
            nonlocal priority
            this.style.setProperty(name, value, priority)

        return anon

    def _styleFunction(self, name, value, priority=None):
        def anon(this, *args):
            v = _invoke_callback(value, *args)
            if v == None:
                this.style.removeProperty(name)
            else:
                this.style.setProperty(name, v, priority)

        return anon

    def style(self, name, value=None, priority=None, *args):
        if value == None:
            return styleValue(self.node(), name)

        if value == None:  # ?? need to understand what below is doing
            func = self._styleRemove  # (name, value, priority)
        elif callable(value):
            func = self._styleFunction  # (name, value, priority)
        else:
            func = self._styleConstant  # (name, value, priority)

        p = "" if priority == None else priority
        return self.each(func(name, value, p))

    def append(self, name, *args):
        create = name if callable(name) else creator(name)

        def anon(this, *args):
            n = create(this, *args)
            return this.appendChild(n)

        return self.select(anon)

    # import selection_property from "./property.js";
    def propertyRemove(self, name):
        def anon(this, *args):
            _remove_property(this, name)

        return anon

    def propertyConstant(self, name, value):
        def anon(this, *args):
            _set_property(this, name, value)

        return anon

    def propertyFunction(self, name, value):
        def anon(this, *args):
            v = _invoke_callback(value, *args)
            if v == None:
                _remove_property(this, name)
            else:
                _set_property(this, name, v)

        return anon

    def property(self, name, value=_MISSING):
        if value is _MISSING:
            return _get_property(self.node(), name)

        if value == None:
            func = self.propertyRemove
        elif callable(value):
            func = self.propertyFunction
        else:
            func = self.propertyConstant

        callback = func(name) if value == None else func(name, value)
        self.each(callback)
        return self

    # import selection_text from "./text.js";
    # import selection_classed from "./classed.js";

    # def classed: selection_classed,

    def classedTrue(self, names, value):
        return lambda this, *args: classedAdd(this, names)

    def classedFalse(self, names, value):
        return lambda this, *args: classedRemove(this, names)

    def classedFunction(self, names, value):
        def anon(this, *args):
            v = _invoke_callback(value, *args)
            if v:
                classedAdd(this, names)
            else:
                classedRemove(this, names)

        return anon

    def classed(self, name, value=_MISSING, *args):
        names = classArray(str(name))
        if value is _MISSING:
            node = self.node()
            if node is None:
                return False
            mylist = classList(node)
            for class_name in names:
                if not mylist.contains(class_name):
                    return False
            return True

        if callable(value):
            func = self.classedFunction
        elif value:
            func = self.classedTrue
        else:
            func = self.classedFalse

        self.each(func(names, value))
        return self

    # def text: selection_text,
    def _textRemove(self):
        def anon(this, *args):
            this.textContent = ""

        return anon

    def _textConstant(self, value):
        def anon(this, *args):
            this.textContent = value

        return anon

    def _textFunction(self, value):
        def anon(this, *args):
            v = _invoke_callback(value, *args)
            this.textContent = "" if v == None else v

        return anon

    def text(self, value=_MISSING):
        if value is _MISSING:
            node = self.node()
            return None if node is None else node.textContent

        if value == None:
            func = self._textRemove
        elif callable(value):
            func = self._textFunction
        else:
            func = self._textConstant

        callback = func() if value == None else func(value)
        self.each(callback)
        return self

    # import selection_html from "./html.js";
    def htmlRemove(self):
        def anon(this, *args):
            this.innerHTML = ""

        return anon

    def htmlConstant(self, value):
        def anon(this, *args):
            this.innerHTML = value

        return anon

    def htmlFunction(self, value):
        def anon(this, *args):
            v = _invoke_callback(value, *args)
            this.innerHTML = "" if v == None else v

        return anon

    def html(self, value=_MISSING):
        if value is _MISSING:
            node = self.node()
            return None if node is None else node.innerHTML

        if value == None:
            func = self.htmlRemove
        elif callable(value):
            func = self.htmlFunction
        else:
            func = self.htmlConstant
        callback = func() if value == None else func(value)
        self.each(callback)
        return self

    # import selection_raise from "./raise.js";
    # def _raise(self):
    #     if (this.nextSibling):
    #         this.parentNode.appendChild(this)

    # def raise(self):
    #     return this.each(raise)

    # import selection_lower from "./lower.js";
    # def lower: selection_lower,
    def _lower(self, node, *args):
        if node.previousSibling and node.parentNode:
            node.parentNode.insertBefore(node, node.parentNode.firstChild)

    def lower(self):
        return self.each(self._lower)

    # import selection_insert from "./insert.js";
    # import creator from "../creator.js"; # already in?
    # import selector from "../selector.js"; # already in?

    def constantNull(self):
        return None

    def insert(self, name, before=None, *args):
        create = name if callable(name) else creator(name)
        select = self.constantNull if before is None else before
        if not callable(select):
            select = selector(select)

        def insert_node(node, data, i, group):
            new_node = _invoke_callback(create, node, data, i, group)
            reference_node = _invoke_callback(select, node, data, i, group)
            return node.insertBefore(new_node, reference_node)

        return self.select(insert_node)

    # import selection_remove from "./remove.js";
    # def remove: selection_remove,
    def _remove(self, node, *args):
        parent = node.parentNode
        if parent:
            parent.removeChild(node)

    def remove(self):
        return self.each(self._remove)

    # import selection_clone from "./clone.js";
    def selection_cloneShallow(self, node, *args):
        clone = node.cloneNode(False)
        parent = node.parentNode
        return parent.insertBefore(clone, node.nextSibling) if parent else clone

    def selection_cloneDeep(self, node, *args):
        clone = node.cloneNode(True)
        parent = node.parentNode
        return parent.insertBefore(clone, node.nextSibling) if parent else clone

    def clone(self, deep=True):
        return self.select(
            self.selection_cloneDeep if deep else self.selection_cloneShallow
        )

    # import selection_datum from "./datum.js";
    def datum(self, value=_MISSING, *args):
        if value is _MISSING:
            return _get_property(self.node(), "__data__")
        return self.property("__data__", value)

    # import selection_on from "./on.js";
    def contextListener(self, listener):
        def wrapped(event):
            data = getattr(getattr(event, "currentTarget", None), "__data__", None)
            return _invoke_callback(listener, event, data)

        return wrapped

    def parseTypenames(self, typenames):
        parsed = []
        for typename in str(typenames).strip().split():
            event_type = typename
            name = ""
            if "." in typename:
                event_type, name = typename.split(".", 1)
            parsed.append({"type": event_type, "name": name})
        return parsed

    def onRemove(self, typename):
        def anon(this, *args):
            listeners = list(getattr(this, "__on", []))
            if not listeners:
                return

            kept = []
            for listener in listeners:
                matches_type = (
                    not typename["type"] or listener["type"] == typename["type"]
                )
                matches_name = listener["name"] == typename["name"]
                if matches_type and matches_name:
                    this.removeEventListener(
                        listener["type"], listener["listener"], listener["options"]
                    )
                else:
                    kept.append(listener)

            if kept:
                setattr(this, "__on", kept)
            elif hasattr(this, "__on"):
                delattr(this, "__on")

        return anon

    def onAdd(self, typename, value, options):
        def anon(this, *args):
            if not typename["type"]:
                return

            listener = self.contextListener(value)
            listeners = list(getattr(this, "__on", []))

            for existing in listeners:
                if (
                    existing["type"] == typename["type"]
                    and existing["name"] == typename["name"]
                ):
                    this.removeEventListener(
                        existing["type"],
                        existing["listener"],
                        existing["options"],
                    )
                    this.addEventListener(typename["type"], listener, options)
                    existing.update(
                        {
                            "value": value,
                            "listener": listener,
                            "options": options,
                        }
                    )
                    setattr(this, "__on", listeners)
                    return

            this.addEventListener(typename["type"], listener, options)
            listeners.append(
                {
                    "type": typename["type"],
                    "name": typename["name"],
                    "value": value,
                    "listener": listener,
                    "options": options,
                }
            )
            setattr(this, "__on", listeners)

        return anon

    def on(self, typename, value=_MISSING, options=None, *args):
        typenames = self.parseTypenames(str(typename))

        if value is _MISSING:
            node = self.node()
            if node is None:
                return None
            listeners = getattr(node, "__on", [])
            for listener in listeners:
                for parsed in typenames:
                    if (
                        listener["type"] == parsed["type"]
                        and listener["name"] == parsed["name"]
                    ):
                        return listener["value"]
            return None

        for parsed in typenames:
            callback = (
                self.onRemove(parsed)
                if value is None
                else self.onAdd(parsed, value, options)
            )
            self.each(callback)
        return self

    # import selection_dispatch from "./dispatch.js";
    # def dispatch: selection_dispatch,
    # import defaultView from "../window.js";
    def dispatchEvent(self, node, type, params):
        from domonic.events import CustomEvent

        if params is None:
            params = {}
        elif not isinstance(params, dict):
            params = dict(getattr(params, "__dict__", {}))

        event = CustomEvent(type, params)
        node.dispatchEvent(event)
        return node

    def dispatchConstant(self, type, params):
        return lambda this, *args: self.dispatchEvent(this, type, params)

    def dispatchFunction(self, type, params, *args):
        def anon(this, *call_args):
            event_params = _invoke_callback(params, *call_args)
            return self.dispatchEvent(this, type, event_params)

        return anon

    def dispatch(self, type, params=None):
        func = self.dispatchFunction if callable(params) else self.dispatchConstant
        return self.each(func(type, params))

    # import selection_iterator from "./iterator.js";
    # #   [Symbol.iterator]: selection_iterator


def selection():
    return Selection([[document.documentElement]], root)


def selection_selection():
    return this


def select(selector):
    from domonic.dom import document  # bring in the global document

    if isinstance(selector, str):
        return Selection(
            [[document.querySelector(selector)]], [document.documentElement]
        )
    else:
        return Selection([[selector]], root)


def create(name):
    return select(creator(name).call(document.documentElement))


# export {default as create} from "./create.js";
# export {default as creator} from "./creator.js";
# export {default as local} from "./local.js";
nextId = 0


def local():
    return Local


class Local:
    def __init__(self):
        self.nextId = 0  # += 1
        self._ = "@" + String(self.nextId).toString(36)

    def get(self, node):
        id = self._
        while not (id in node):
            node = node.parentNode
            if node is None:
                return
        return node[id]

    def set(self, node, value):
        node[this._] = value
        return node[self._]

    def remove(self, node):
        for i in range(0, len(node)):
            if node[i] == self._:
                a = node.remove(i)
                # del node[i]
                return a
        # return this._ in node and delete node[this._]

    def toString(self):
        return self._


# export {default as matcher} from "./matcher.js";
def matcher(selector):
    return lambda this: this.matches(selector)


def childMatcher(selector):
    return lambda node: node.matches(selector)


# export {default as pointer} from "./pointer.js";
# import sourceEvent from "./sourceEvent.js";
def sourceEvent(event):
    sourceEvent = event.sourceEvent
    while sourceEvent is not None:
        event = sourceEvent
        sourceEvent = event.sourceEvent
    return event


def pointer(event, node):
    event = sourceEvent(event)
    if node == None:
        node = event.currentTarget
    if node:
        svg = node.ownerSVGElement or node
    if svg.createSVGPoint:
        point = svg.createSVGPoint()
        point.x = event.clientX
        point.y = event.clientY
        point = point.matrixTransform(node.getScreenCTM().inverse())
        return [point.x, point.y]

    if node.getBoundingClientRect:
        rect = node.getBoundingClientRect()
        return [
            event.clientX - rect.left - node.clientLeft,
            event.clientY - rect.top - node.clientTop,
        ]

    return [event.pageX, event.pageY]


def pointers(events, node):
    if events.target is not None:  # i.e., instanceof Event, not TouchList or iterable
        events = sourceEvent(events)
    if node == None:
        node = events.currentTarget
    events = events.touches or [events]
    return Array.from_(events, lambda event: pointer(event, node))


def empty():
    return []


def selectAll(selector):
    from domonic.dom import document  # bring in the global document

    if isinstance(selector, str):
        return Selection(
            [document.querySelectorAll(selector)], [document.documentElement]
        )
        # return Selection([document.getElementsBySelector(selector, document)], [document.documentElement])
    else:
        return Selection([array(selector)], root)


def selectorAll(selector):
    return (
        empty
        if selector == None
        else lambda this, *args: this.querySelectorAll(selector)
    )
