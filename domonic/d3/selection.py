"""
    domonic.d3.selection
    ====================================

    https://github.com/d3/d3-selection/tree/main/src/selection

"""

# from domonic.html import *

from domonic.javascript import *
from domonic.dom import document  # bring in the global

xhtml = "http://www.w3.org/1999/xhtml"

namespaces = {"svg": "http://www.w3.org/2000/svg", "xhtml": xhtml, "xlink": "http://www.w3.org/1999/xlink", "xml": "http://www.w3.org/XML/1998/namespace", "xmlns": "http://www.w3.org/2000/xmlns/"}


def namespace(name):
    name = str(name)
    prefix = name
    i = String(prefix).indexOf(":")
    if i > 0:
        prefix = String(name).slice(0, i)
    if (i >= 0 and (prefix) != "xmlns"):
        name = name.slice(i + 1)
    return {"space": namespaces[prefix], "local": name} if Object(namespaces).hasOwnProperty(prefix) else name  # eslint-disable-line no-prototype-builtins


def creatorInherit(name):
    def anon(this):
        # document = this.ownerDocument
        from domonic.dom import document 
        # uri = this.namespaceURI
        uri = document.namespaceURI
        return document.createElement(name) if uri == xhtml and document.documentElement.namespaceURI == xhtml else document.createElementNS(uri, name)
    return anon


def creatorFixed(fullname):
    # print('this one')
    # return lambda this: print(this[0] , "TESTESTESTE")
    # return lambda this: this.ownerDocument.createElementNS(fullname['space'], fullname['local'])
    from domonic.dom import document  # bring in the global document
    return lambda *args: document.ownerDocument.createElementNS(fullname['space'], fullname['local'])


def creator(name):
    fullname = namespace(name)
    print(fullname)
    func = creatorFixed if isinstance(fullname, dict) else creatorInherit
    return func(fullname)


def none():
    return {}


def selector(selector):
    return None if selector == None else lambda: this.querySelector(selector)



# // Given something array like (or null), returns something that is strictly an
# // array. This is used to ensure that array-like objects passed to d3.selectAll
# // or selection.selectAll are converted into proper arrays when creating a
# // selection; we don’t ever want to create a selection backed by a live
# // HTMLCollection or NodeList. However, note that selection.selectAll will use a
# // static NodeList as a group, since it safely derived from querySelectorAll.
def array(x):
    b =  x if Array.isArray(x) else Array.from_(x)
    return [] if x == None else b


# import selection_select from "./select.js";

# import selection_selectAll from "./selectAll.js";
# import selection_selectChild from "./selectChild.js";
# import selection_selectChildren from "./selectChildren.js";
# import selection_filter from "./filter.js";
# import selection_data from "./data.js";
# import selection_enter from "./enter.js";
# import selection_exit from "./exit.js";
# import selection_join from "./join.js";
# import selection_merge from "./merge.js";
# import selection_order from "./order.js";
# import selection_sort from "./sort.js";
# import selection_call from "./call.js";

# import selection_nodes from "./nodes.js";
# import selection_node from "./node.js";

# import selection_size from "./size.js";
# import selection_empty from "./empty.js";
# import selection_each from "./each.js";
# import selection_attr from "./attr.js";
# import selection_style from "./style.js";
# import selection_property from "./property.js";
# import selection_classed from "./classed.js";
# import selection_text from "./text.js";
# import selection_html from "./html.js";
# import selection_raise from "./raise.js";
# import selection_lower from "./lower.js";

# import selection_append from "./append.js";

# import selection_insert from "./insert.js";
# import selection_remove from "./remove.js";
# import selection_clone from "./clone.js";
# import selection_datum from "./datum.js";
# import selection_on from "./on.js";
# import selection_dispatch from "./dispatch.js";
# import selection_iterator from "./iterator.js";

root = [None]


class Selection():

    def __init__(self, groups, parents, this=None):
        self._groups = groups
        self._parents = parents
        self.this = this  # context switcher

    def select(self, select):
        if not callable(select):
            select = selector(select)

        # TODO write this commented out javascript as python instead

        # for (var groups = self._groups, m = groups.length, subgroups = new Array(m), j = 0; j < m; ++j) {
        #     for (var group = groups[j], n = group.length, subgroup = subgroups[j] = new Array(n), node, subnode, i = 0; i < n; ++i) {
        #     if ((node = group[i]) && (subnode = select.call(node, node.__data__, i, group))) {
        #         if ("__data__" in node) subnode.__data__ = node.__data__;
        #         subgroup[i] = subnode;

        #     }
        # }


        groups = self._groups
        m = len(groups)
        subgroups = Array(m)
        j = 0
        for group in groups:
            n = len(group)
            subgroup = subgroups[j] = Array(n)
            for i in range(n):
                node = group[i]
                print("node", node)
                if node is None:
                    print('NODE WAS NONE.err?')
                    continue
                try:
                    node.__data__ = None
                    print('bipm', select)
                    subnode = Function(select).call(node, node.__data__, i, group)
                except Exception as e:
                    print(e)
                    print('failed. no __data__ on node')
                    subnode = None
                if "__data__" in node:
                    subnode.__data__ = node.__data__
                subgroup[i] = subnode
            j += 1
        return Selection(subgroups, self._parents, self.this)


    # def selectAll: selection_selectAll,


    # import {Selection} from "./index.js";
    # import array from "../array.js";


    # import selectorAll from "../selectorAll.js";

    def arrayAll(select):
        return lambda: array(select.apply(this, arguments))

    def selectAll(select):
        if callable(select):
            select = arrayAll(select)
        else:
            select = selectorAll(select)

        # TODO - wrewrite this as python
        # for (var groups = this._groups, m = groups.length, subgroups = [], parents = [], j = 0; j < m; ++j) {
        #     for (var group = groups[j], n = group.length, node, i = 0; i < n; ++i) {
        #     if (node = group[i]) {
        #         subgroups.push(select.call(node, node.__data__, i, group));
        #         parents.push(node);
        #     }
        #     }
        # }

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
                subgroups.append(select.call(node, node.__data__, i, group))
                parents.append(node)
            j += 1
        return Selection(subgroups, parents)


    # def selectChild: selection_selectChild,
    # def selectChildren: selection_selectChildren,
    # def filter: selection_filter,
    # def data: selection_data,
    # def enter: selection_enter,
    # def exit: selection_exit,

    def sparse(update):
        return Array(len(update))

    def exit(self):
        return Selection(this._exit or self._groups.map(sparse), self._parents)


    # def join: selection_join,
    # def merge: selection_merge,
    # def selection: selection_selection,
    # def order: selection_order,
    # def sort: selection_sort,
    # def call: selection_call,
    # def nodes: selection_nodes,
    
    # def node: selection_node,
    def node(self):

        # TODO write this commented out javascript as python instead
        # for (var groups = this._groups, j = 0, m = groups.length; j < m; ++j) {
        #     for (var group = groups[j], i = 0, n = group.length; i < n; ++i) {
        #     var node = group[i];
        #     if (node) return node;
        #     }
        # }
        # return null;

        groups = self._groups
        j = 0
        m = len(groups)
        for group in groups:
            i = 0
            n = len(group)
            while i < n:
                node = group[i]
                if node:
                    return node
                i += 1
        return None


    # def size: selection_size,
    # def empty: selection_empty,
    # def each: selection_each,
    # def attr: selection_attr,


    def attrRemove(self, name):
        # return lambda this: this.removeAttribute(name)
        self.this.removeAttribute(name)
        return self

    def attrRemoveNS(self, fullname):
        # return lambda this: this.removeAttributeNS(fullname['space'], fullname['local'])
        self.this.removeAttributeNS(fullname['space'], fullname['local'])
        return self

    def attrConstant(self, name, value):
        # print('setting:::', name, value)
        # print('setting:::', self.this)
        # return lambda: self.setAttribute(name, value)
        self.this.setAttribute(name, value)
        return self

    def attrConstantNS(self, fullname, value):
        # return lambda this: this.setAttributeNS(fullname['space'], fullname['local'], value)
        self.this.setAttributeNS(fullname['space'], fullname['local'], value)
        return self

    def attrFunction(self, name, value, *args):
        def anon(this):
            nonlocal value
            nonlocal name
            nonlocal args
            v = value.apply(this, args)
            if v == None:
                this.removeAttribute(name)
            else:
                this.setAttribute(name, v)

        return self

    def attrFunctionNS(self, fullname, value, *args):
        def anon(this):
            nonlocal value
            nonlocal fullname
            nonlocal args
            v = Object(value).apply(this, args)
            if v == None:
                this.removeAttributeNS(fullname['space'], fullname['local'])
            else:
                this.setAttributeNS(fullname['space'], fullname['local'], v)
        return anon

    def attr(self, name, value, *args):

        print("NAME!!", name, value, args)

        fullname = namespace(name)

        # if len(args) < 2: #4:
        #     node = self.node()
        #     print(node)
        #     return node.getAttributeNS(fullname['space'], fullname['local']) if isinstance(fullname, dict) else node.getAttribute(fullname)

        a = self.attrRemoveNS if isinstance(fullname, dict) else self.attrRemove
        b = self.attrFunctionNS if isinstance(fullname, dict) else self.attrFunction
        c = self.attrConstantNS if isinstance(fullname, dict) else self.attrConstant

        if value == None:
            func = a
        elif callable(value):
            func = b
        else:
            func = c

        return func(fullname, value)



    # def style: selection_style,
    # def property: selection_property,
    # def classed: selection_classed,
    # def text: selection_text,
    # def html: selection_html,
    # def raise: selection_raise,

    # def _raise(self):
    #     if (this.nextSibling):
    #         this.parentNode.appendChild(this)


    # def raise(self):
    #     return this.each(raise)

    # def lower: selection_lower,

    def _lower(self):
        if self.this.previousSibling:
            self.this.parentNode.insertBefore(self.this, self.this.parentNode.firstChild)

    def lower(self):
        return self.each(lower)


    def append(self, name, *args):
        create = name if callable(name) else creator(name)
        print(create)

        def anon(this, *args):
            # print("THIS", this, args)
            nonlocal create
            # nonlocal self

            # print("self is::", self)
            self.this = Function(create).apply(self, args)
            # print("self this is::", self.this)
            return this.appendChild(self.this)

        return self.select(anon)

    # def insert: selection_insert,
    # def remove: selection_remove,
    def _remove(self):
        parent = self.this.parentNode
        if parent:
            parent.removeChild(self.this)

    def remove(self):
        return self.each(remove)

    # def clone: selection_clone,
    # def datum: selection_datum,

    # def datum(value):
        # todo write this as python
        # return arguments.length ? this.property("__data__", value) : this.node().__data__

    # def on: selection_on,
    # def dispatch: selection_dispatch,

    # #   [Symbol.iterator]: selection_iterator


def selection():
    return Selection([[document.documentElement]], root)


def selection_selection():
    return this


def select(selector):
    # print(selector)
    # print(document)
    from domonic.dom import document  # bring in the global document
    if isinstance(selector, str):
        return Selection([[document.querySelector(selector)]], [document.documentElement])
    else:
        return Selection([[selector]], root)


def create(name):
    return select(creator(name).call(document.documentElement))


# export {default as create} from "./create.js";
# export {default as creator} from "./creator.js";
# export {default as local} from "./local.js";
# export {default as matcher} from "./matcher.js";
# export {default as namespace} from "./namespace.js";
# export {default as namespaces} from "./namespaces.js";
# export {default as pointer} from "./pointer.js";
# export {default as pointers} from "./pointers.js";
# export {default as select} from "./select.js";
# export {default as selectAll} from "./selectAll.js";
def empty():
    return []


def selectAll(selector):
    # print(selector)
    from domonic.dom import document  # bring in the global document
    # print(document)
    if isinstance(selector, str):
        return Selection([document.querySelectorAll(selector)], [document.documentElement], document)
        # return Selection([document.getElementsBySelector(selector, document)], [document.documentElement])
    else:
        return Selection([array(selector)], root, document)


# export {default as selection} from "./selection/index.js";
# export {default as selector} from "./selector.js";
# export {default as selectorAll} from "./selectorAll.js";
# export {styleValue as style} from "./selection/style.js";
# export {default as window} from "./window.js";
