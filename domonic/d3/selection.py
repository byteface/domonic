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
    # print(fullname)
    func = creatorFixed if isinstance(fullname, dict) else creatorInherit
    return func(fullname)


def none():
    return {}


def selector(selector):
    return None if selector == None else lambda: document.querySelector(selector)

# // Given something array like (or null), returns something that is strictly an
# // array. This is used to ensure that array-like objects passed to d3.selectAll
# // or selection.selectAll are converted into proper arrays when creating a
# // selection; we don’t ever want to create a selection backed by a live
# // HTMLCollection or NodeList. However, note that selection.selectAll will use a
# // static NodeList as a group, since it safely derived from querySelectorAll.
def array(x):
    b = x if Array.isArray(x) else Array.from_(x)
    return [] if x == None else b


# export {default as window} from "./window.js";
def window(node):
    return (node.ownerDocument and node.ownerDocument.defaultView) or (node.document and node) or node.defaultView


defaultView = window

# import selection_select from "./select.js";

# import selection_style from "./style.js";
def styleValue(node, name):
    return node.style.getPropertyValue(name) or defaultView(node).getComputedStyle(node, None).getPropertyValue(name)


def sparse(self, update):
    return Array(len(update))


class EnterNode():

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


class ClassList():

    def __init__(self, node):
        # print('class list is in town')
        self._node = node
        self._names = classArray(node.getAttribute("class") or "")

    def add(self, name):
        i = String(self._names).indexOf(name)
        if i < 0:
            self._names.append(name)
            self._node.setAttribute("class", " ".join(self._names))

    def remove(self, name):
        i = self._names.indexOf(name)
        if i >= 0:
            self._names.splice(i, 1)
            self._node.setAttribute("class", " ".join(self._names))

    def contains(self, name):
        return self._names.indexOf(name) >= 0


def classArray(string):
    return String(string).trim().split(r'/^|\s+/')


def classList(node):
    # return node.classList or ClassList(node)
    return ClassList(node)


def classedAdd(node, names):
    mylist = classList(node)
    i = -1
    n = len(names)
    while i < n:
        mylist.add(names[i])
        i += 1


def classedRemove(node, names):
    list = classList(node)
    i = -1
    n = len(names)
    while i < n:
        list.remove(names[i])
        i += 1


# import selection_append from "./append.js";


root = [None]


class Selection():

    def __init__(self, groups, parents, this=None):
        self._groups = groups
        self._parents = parents
        self.this = None
        if this is None:
            # self.this = root[0]
            # self.this = self._groups#[0]
            # self.this = self._groups  #.__iter__()
            pass
        else:
            self.this = this  # context switcher

    # unpack groups into a list of nodes
    def __iter__(self):
        return self._groups.__iter__()

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
                    print('NODE WAS NONE.err?')
                    continue
                try:
                    # print(node.__data__)
                    node.__data__ = None
                    # print('bipm', select)
                    subnode = Function(select).call(node, node.__data__, i, group)
                except Exception as e:
                    # print(e)
                    print('failed. no __data__ on node')
                    subnode = None
                # if subnode is not None:
                #     if "__data__" in subnode:
                #         subnode.__data__ = subnode.__data__
                #     subgroup[i] = subnode
                    # subnode.__data__ = node.__data__
                    # subgroup[i] = subnode
                # print('super::', node, subnode)
                if "__data__" in node:
                    subnode.__data__ = node.__data__
                subgroup[i] = subnode
            j += 1

        # print("this was set to", self.this)
        return Selection(subgroups, self._parents, self.this)

    # import selection_selectAll from "./selectAll.js";
    # import {Selection} from "./index.js";
    # import array from "../array.js";
    # import selectorAll from "../selectorAll.js";

    def arrayAll(self, select, *args):
        return lambda: array(Function(select).apply(self.this, args))

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
                    print('selectaAll : NODE WAS NONE.err?')
                    continue

                try:
                    # print(node.__data__)
                    node.__data__ = None  # TODO - only do this if not there
                    subgroups.append(Function(select).call(node, node.__data__, i, group))
                    parents.append(node)
                except Exception as e:
                    # print(e)
                    print('failed. no __data__ on node')

                # subgroups.append(Function(select).call(node, node.__data__, i, group))
                # parents.append(node)
            j += 1
        return Selection(subgroups, parents, self.this)

    # import selection_selectChild from "./selectChild.js";
    # import {childMatcher} from "../matcher.js";
    find = Array.prototype.find

    def childFind(self, match):
        return lambda: find.call(this.children, match)

    def childFirst(self):
        return this.firstElementChild

    def selectChild(self, match):
        # return this.select(match == null ? childFirst : childFind(typeof match === "function" ? match : childMatcher(match)))
        if callable(match):
            match = childFind(match)
        else:
            match = childMatcher(match)
        return this.select(match)

    # import selection_selectChildren from "./selectChildren.js";
    # def selectChildren: selection_selectChildren,
    # import {childMatcher} from "../matcher.js";

    # filter = Array.prototype.filter

    def children(self):
        return Array.from_(self.this.children)

    def childrenFilter(self, match):
        return lambda: Array.filter.call(self.this.children, match)

    def selectChildren(self, match):
        # TODO - rewrite this as python
        # return this.selectAll(match == None ? children : childrenFilter(typeof match === "function" ? match : childMatcher(match)));
        # return self.selectAll(match == None ? self.children : self.childrenFilter(typeof match == "function" ? match : childMatcher(match)))
        if match is None:
            return self.selectAll(self.this.children)
        else:
            return self.selectAll(self.childrenFilter(match))

    # import selection_filter from "./filter.js";
    # def filter: selection_filter,
    # import {Selection} from "./index.js";
    # import matcher from "../matcher.js"; # TODO - might not be in yet

    def filter(self, match):
        if callable(match):
            match = matcher(match)

        # TODO - rewrite this as python
        # for (var groups = this._groups, m = groups.length, subgroups = new Array(m), j = 0; j < m; ++j) {
        #     for (var group = groups[j], n = group.length, subgroup = subgroups[j] = [], node, i = 0; i < n; ++i) {
        #     if ((node = group[i]) && match.call(node, node.__data__, i, group)) {
        #         subgroup.push(node);
        #     }
        #     }
        # }
        groups = self._groups
        m = len(groups)
        subgroups = []
        j = 0
        for group in groups:
            n = len(group)
            for i in range(n):
                node = group[i]
                if node is None:
                    continue
                if match.call(node, node.__data__, i, group):
                    subgroups.append(node)
            j += 1
        return Selection(subgroups, self._parents, self.this)

    # import selection_data from "./data.js";
    # def data: selection_data, # TODO -------------------------------------- this is a big one

    # import selection_enter from "./enter.js";
    # def enter: selection_enter,
    # import sparse from "./sparse.js";
    # import {Selection} from "./index.js";

    def enter(self):
        return Selection(self._enter or self._groups.map(sparse), self._parents)

    # import selection_exit from "./exit.js";
    # def exit: selection_exit,
    # import sparse from "./sparse.js";
    # import {Selection} from "./index.js";
    def exit(self):
        return Selection(this._exit or self._groups.map(sparse), self._parents)

    # import selection_join from "./join.js";
    # def join: selection_join,
    def join(self, onenter, onupdate, onexit):
        enter = this.enter()
        update = this
        exit = self.exit()
        if callable(onenter):
            enter = onenter(enter)
            if (enter):
                enter = enter.selection()
        else:
            enter = enter.append(onenter + "")

        if onupdate != None:
            update = onupdate(update)
            if (update):
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
        selection = context.selection() if context.selection else context

        # TODO - rewrite this as python
        # for (var groups0 = this._groups, groups1 = selection._groups, m0 = groups0.length, m1 = groups1.length, m = Math.min(m0, m1), merges = new Array(m0), j = 0; j < m; ++j) {
        #     for (var group0 = groups0[j], group1 = groups1[j], n = group0.length, merge = merges[j] = new Array(n), node, i = 0; i < n; ++i) {
        #     if (node = group0[i] || group1[i]) {
        #         merge[i] = node;
        #     }
        #     }
        # }
        groups0 = self._groups
        groups1 = context.selection._groups
        m0 = len(groups0)
        m1 = len(groups1)
        m = min(m0, m1)
        merges = []
        j = 0
        for group0 in groups0:
            group1 = groups1[j]
            n = len(group0)
            merge = []
            for i in range(n):
                node = group0[i]
                if node is None:
                    continue
                if group1[i] is None:
                    continue
                merge.append(node)
            merges.append(merge)
            j += 1

        # TODO - rewrite this as python
        # for (; j < m0; ++j) {
        #     merges[j] = groups0[j];
        # }
        while j < m0:
            merges[j] = groups0[j]
            j += 1

        return Selection(merges, self._parents, self.this)


    # def selection: selection_selection, # ---?? TODO - is this right?

    # import selection_order from "./order.js";
    # def order: selection_order,
    def order(self):
        # TODO - rewrite this as python
        # for (var groups = this._groups, j = -1, m = groups.length; ++j < m;) {
        #     for (var group = groups[j], i = group.length - 1, next = group[i], node; --i >= 0;) {
        #     if (node = group[i]) {
        #         if (next && node.compareDocumentPosition(next) ^ 4) next.parentNode.insertBefore(node, next);
        #         next = node;
        #     }
        #     }
        # }
        groups = self._groups
        j = -1
        m = len(groups)
        while j < m:
            i = len(groups[j]) - 1
            next = groups[j][i]
            while i >= 0:
                node = groups[j][i]
                if node is None:
                    continue
                if next and node.compareDocumentPosition(next) ^ 4:
                    next.parentNode.insertBefore(node, next)
                next = node
                i -= 1
            j += 1
        return self

    # import selection_sort from "./sort.js";
    # def sort: selection_sort,
    # import {Selection} from "./index.js";
    def sort(self, compare):
        if not compare:
            compare = ascending

        def compareNode(a, b):
            # TODO - rewrite this as python
            # return a and b ? compare(a.__data__, b.__data__) : !a - !b
            if a and b:
                return compare(a.__data__, b.__data__)
            return -1 if a else 1

        # TODO - rewrite this as python
        # for (var groups = this._groups, m = groups.length, sortgroups = new Array(m), j = 0; j < m; ++j) {
        #     for (var group = groups[j], n = group.length, sortgroup = sortgroups[j] = new Array(n), node, i = 0; i < n; ++i) {
        #     if (node = group[i]) {
        #         sortgroup[i] = node;
        #     }
        #     }
        #     sortgroup.sort(compareNode);
        # }
        groups = self._groups
        m = len(groups)
        sortgroups = []
        j = 0
        for group in groups:
            n = len(group)
            sortgroup = []
            for i in range(n):
                node = group[i]
                if node is None:
                    continue
                sortgroup.append(node)
            sortgroup.sort(compareNode)
            sortgroups.append(sortgroup)
            j += 1
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
        args[0] = self
        Function(callback).apply(None, args)
        return self

    # import selection_nodes from "./nodes.js";
    def nodes(self):
        return Array.from_(self.this)

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
                if node:
                    return node
                i += 1
        return None

    # import selection_size from "./size.js";
    # def size: selection_size,
    def size(self):
        size = 0
        for node in self.this:
            size += 1  # eslint-disable-line no-unused-vars
        return size

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
                    print('NODE WAS NONE.err?')
                    continue
                # try:
                node.__data__ = None
                Function(callback).call(node, node.__data__, i, group)
                # print('worked on this one')
                # except Exception as e:
                    # print(e)
                    # print('failed. no __data__ on node mate', e)

                i += 1
            j += 1
        return self

    # import selection_attr from "./attr.js";
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
        # self.this.setAttribute(name, value)
        # return self

        def anon(this, *args):
            nonlocal name
            nonlocal value
            # this.textContent = value
            return this.setAttribute(name, value)

        return anon

    def attrConstantNS(self, fullname, value):
        # return lambda this: this.setAttributeNS(fullname['space'], fullname['local'], value)
        self.this.setAttributeNS(fullname['space'], fullname['local'], value)
        return self

    def attrFunction(self, name, value, *args):
        def anon(this):
            nonlocal value
            nonlocal name
            nonlocal args
            v = Function(value).apply(this, args)
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
        # print("NAME!!", name, value, args)
        fullname = namespace(name)

        # if len(args) > 0: #4:
        if value is None:
            node = self.node()
            print(node)
            return node.getAttributeNS(fullname['space'], fullname['local']) if isinstance(fullname, dict) else node.getAttribute(fullname)

        a = self.attrRemoveNS if getattr(fullname, 'local', None) is not None else self.attrRemove
        b = self.attrFunctionNS if getattr(fullname, 'local', None) is not None else self.attrFunction
        c = self.attrConstantNS if getattr(fullname, 'local', None) is not None else self.attrConstant

        if value is None:
            func = a
        elif callable(value):
            func = b
        else:
            func = c

        self.each(func(fullname, value))
        return self

    # def style: selection_style,
    # import defaultView from "../window.js";
    def _styleRemove(self, name, value, priority=None):
        # print('styleing remove')
        def anon(this, *args):
            # print('_styleRemove :anon/name', name)
            this.style.removeProperty(name)
        return anon

    def _styleConstant(self, name, value, priority=None):
        # print('style constant was called')
        def anon(this, *args):
            # print('THE FUNC WAS CALLED')
            nonlocal name
            nonlocal value
            nonlocal priority
            # print('_styleConstantxxx :anon/name', name, type(this), this)
            # print('aaa',this)
            # print('aaaaawtf')
            # print('bbb',this.style)
            # print('ccc')
            this.style.setProperty(name, value, priority)
        return anon

    def _styleFunction(self, name, value, priority=None):
        # print('styling fucntion')
        def anon(this, *args):
            # print('styling fucntion:anon/name', name)
            v = Function(value).apply(this, args)
            # print('dark mavis',v)
            if v == None:
                this.style.removeProperty(name)
            else:
                # print('how you doin')
                this.style.setProperty(name, v, priority)
        return anon

    def style(self, name, value=None, priority=None, *args):
        if value == None:
            return styleValue(self.node(), name)

        # print('hi!!!!!!!!')
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
        # print(create)

        def anon(this, *args):
            # print("THIS", this, args)
            nonlocal create
            # nonlocal self
            # print("self is::", self)
            n = Function(create).apply(self, args)
            # print('n is::', n)
            # print("self this is::", self.this)
            # self.this = this
            return this.appendChild(n)

        self.select(anon)
        return self

    # import selection_property from "./property.js";
    def propertyRemove(self, name):
        def anon(this):
            del this[name]
        return anon

    def propertyConstant(self, name, value):
        def anon(this):
            this[name] = value
        return anon

    def propertyFunction(self, name, value):
        def anon(this, *args):
            v = Function(value).apply(this, args)
            if v == None:
                del this[name]
            else:
                this[name] = v
        return anon

    def property(self, name, value):

    # TODO write this commented out javascript as python instead
    # return arguments.length > 1
    #     ? this.each((value == null
    #         ? propertyRemove : typeof value === "function"
    #         ? propertyFunction
    #         : propertyConstant)(name, value))
    #     : this.node()[name]
        if value == None:
            func = propertyRemove
        elif callable(value):
            func = propertyFunction
        else:
            func = propertyConstant

        return func(name, value)

    # import selection_text from "./text.js";
    # import selection_classed from "./classed.js";

    # def classed: selection_classed,

    def classedTrue(self, names, value):
        # print("classedTrue::::")
        return lambda this, *args: classedAdd(this, names)

    def classedFalse(self, names, value):
        return lambda this, *args: classedRemove(this, names)

    def classedFunction(self, names, value):
        # TODO write this commented out javascript as python instead
        # return function() {
        # (value.apply(this, arguments) ? classedAdd : classedRemove)(this, names)
        # }
        def anon(this, *args):
            nonlocal names
            nonlocal value
            # nonlocal this
            # nonlocal args
            # print('classedFunction', names, value)
            v = Function(value).apply(this, args)
            if v == None:
                classedRemove(this, names)
            else:
                classedAdd(this, names)
        return anon

    def classed(self, name, value, *args):
        names = classArray(str(name))
        # print(names)
        # if (args.length < 2):
        if value == None:
            list = classList(this.node())
            i = -1
            n = len(names)
            while (i < n):
                if not list.contains(names[i]):
                    return False
                i += 1
            return True

        # TODO write this commented out javascript as python instead
        # return this.each((typeof value === "function"
        #     ? classedFunction : value
        #     ? classedTrue
        #     : classedFalse)(names, value));
        # }
        # print( 'hey',value, callable(value) )

        if value == None:
            func = self.classedFalse
        elif callable(value):
            func = self.classedFunction
        else:
            func = self.classedTrue

        self.each(func(names, value))


    # def text: selection_text,
    def _textRemove(self):
        self.this.textContent = ""

    def _textConstant(self, value):
        def anon(this, *args):
            this.textContent = value
        return anon

    def _textFunction(self, value):
        def anon(this, *args):
            v = Function(value).apply(this, args)
            this.textContent = "" if v == None else v
        return anon

    def text(self, value=None):
        if value == None:
            return self.node()._textContent
        # return arguments.length
        #     ? this.each(value == null
        #         ? textRemove : (typeof value === "function"
        #         ? textFunction
        #         : textConstant)(value))
        #     : this.node().textContent
        if value == None:
            func = self._textRemove
        elif callable(value):
            func = self._textFunction
        else:
            func = self._textConstant

        self.each(func(value))

    # import selection_html from "./html.js";
    def htmlRemove(self):
        self.this.innerHTML = ""

    def htmlConstant(self, value):
        def anon(this):
            this.innerHTML = value
        return anon

    def htmlFunction(self, value):
        def anon(this, *args):
            v = Function(value).apply(this, args)
            this.innerHTML = "" if v == None else v
        return anon

    def html(self, value):
        #TODO write this commented out javascript as python instead
        # return arguments.length
        #     ? this.each(value == null
        #         ? htmlRemove : (typeof value === "function"
        #         ? htmlFunction
        #         : htmlConstant)(value))
        #     : this.node().innerHTML;
        if value == None:
            func = htmlRemove
        elif callable(value):
            func = htmlFunction
        else:
            func = htmlConstant
        return func(value)


    # import selection_raise from "./raise.js";
    # def _raise(self):
    #     if (this.nextSibling):
    #         this.parentNode.appendChild(this)

    # def raise(self):
    #     return this.each(raise)

    # import selection_lower from "./lower.js";
    # def lower: selection_lower,
    def _lower(self):
        if self.this.previousSibling:
            self.this.parentNode.insertBefore(self.this, self.this.parentNode.firstChild)

    def lower(self):
        return self.each(lower)

    # import selection_insert from "./insert.js";
    # import creator from "../creator.js"; # already in?
    # import selector from "../selector.js"; # already in?

    def constantNull(self):
        return None

    def insert(self, name, before, *args):
        # TODO write this commented out javascript as python instead
        # var create = typeof name === "function" ? name : creator(name),
        #     select = before == null ? constantNull : typeof before === "function" ? before : selector(before);
        # return this.select(function() {
        #     return this.insertBefore(create.apply(this, arguments), select.apply(this, arguments) || null);
        # })
        create = name if callable(name) else creator(name)
        select = before == None or before == "null" or before == "undefined" or before == "null"
        return self.select(lambda: self.this.insertBefore(Function(create).apply(self, args), select))

    # import selection_remove from "./remove.js";
    # def remove: selection_remove,
    def _remove(self):
        parent = self.this.parentNode
        if parent:
            parent.removeChild(self.this)

    def remove(self):
        return self.each(remove)

    # import selection_clone from "./clone.js";
    def selection_cloneShallow(self):
        clone = this.cloneNode(False)
        parent = self.this.parentNode
        return parent.insertBefore(clone, this.nextSibling) if parent else clone

    def selection_cloneDeep(self):
        clone = this.cloneNode(False)
        parent = self.this.parentNode
        return parent.insertBefore(clone, self.this.nextSibling) if parent else clone

    def clone(self, deep):
        return this.select(selection_cloneDeep if deep else selection_cloneShallow)

    # import selection_datum from "./datum.js";
    def datum(self, value=None, *args):
        # return arguments.length
        #     ? this.property("__data__", value)
        #     : this.node().__data__;
        # }
        return self.this.property("__data__", value) if value is not None else self.node().__data__

    # import selection_on from "./on.js";
    def contextListener(self, listener):
        return lambda event: listener.call(self.this, event, self.this.__data__)

    def parseTypenames(self, typenames):
        # TODO - write this as python
        # return typenames.trim().split(/^|\s+/).map(function(t) {
        #     var name = "", i = t.indexOf(".");
        #     if (i >= 0) name = t.slice(i + 1), t = t.slice(0, i)
        #     return {type: t, name: name}
        # });
        return [{'type': t[0], 'name': t[1]} for t in re.findall(r'\.([^\.]+)', typenames)]

    def onRemove(self, typename):
        # TODO - write this as python
        # return function() {
        #     var on = this.__on;
        #     if (!on) return;
        #     for (var j = 0, i = -1, m = on.length, o; j < m; ++j) {
        #     if (o = on[j], (!typename.type || o.type === typename.type) && o.name === typename.name) {
        #         this.removeEventListener(o.type, o.listener, o.options);
        #     } else {
        #         on[++i] = o;
        #     }
        #     }
        #     if (++i) on.length = i;
        #     else delete this.__on;
        # }
        def anon(this):
            on = this.__on
            if not on:
                return
            for j in range(0, len(on)):
                o = on[j]
                if not typename:
                    on[j] = o
                    return
                if o.type and o.type == typename.type:
                    if o.name == typename.name:
                        this.removeEventListener(o.type, o.listener, o.options)
                    else:
                        on[j] = o
                else:
                    on[j] = o
            on.length = len(on)
            del this.__on
        return anon

    def onAdd(self, typename, value, options):
        # TODO - write this as python
        # return function() {
        #     var on = this.__on, o, listener = contextListener(value);
        #     if (on) for (var j = 0, m = on.length; j < m; ++j) {
        #     if ((o = on[j]).type === typename.type && o.name === typename.name) {
        #         this.removeEventListener(o.type, o.listener, o.options);
        #         this.addEventListener(o.type, o.listener = listener, o.options = options);
        #         o.value = value;
        #         return;
        #     }
        #     }
        #     this.addEventListener(typename.type, listener, options);
        #     o = {type: typename.type, name: typename.name, value: value, listener: listener, options: options};
        #     if (!on) this.__on = [o];
        #     else on.push(o);
        # }
        def anon(this):
            on = this.__on
            if on:
                for j in range(0, len(on)):
                    o = on[j]
                    if o.type == typename.type and o.name == typename.name:
                        this.removeEventListener(o.type, o.listener, o.options)
                        this.addEventListener(o.type, o.listener, o.options)
                        o.value = value
                        return
                this.addEventListener(typename.type, value, options)
                o = {'type': typename.type, 'name': typename.name, 'value': value, 'listener': value, 'options': options}
                if not on:
                    this.__on = [o]
                else:
                    on.push(o)
        return anon


    def on(self, typename, value, options, *args):
        typenames = parseTypenames(str(typename))
        i = None
        n = len(typenames)
        t = None

        # TODO - write this as python
        # if (arguments.length < 2) {
        #     var on = this.node().__on;
        #     if (on) for (var j = 0, m = on.length, o; j < m; ++j) {
        #     for (i = 0, o = on[j]; i < n; ++i) {
        #         if ((t = typenames[i]).type === o.type && t.name === o.name) {
        #         return o.value;
        #         }
        #     }
        #     }
        #     return;
        # }

        # on = value ? onAdd : onRemove;
        # for (i = 0; i < n; ++i) this.each(on(typenames[i], value, options));
        # return this;
        # }

        if arguments.length < 2:
            on = self.node().__on
            if on:
                for j in range(0, len(on)):
                    o = on[j]
                    for i in range(0, n):
                        t = typenames[i]
                        if t is not None and (o.type == t.type) and (o.name == t.name):
                            return o.value
                return
            return
        for i in range(0, n):
            o = self.node().__on[i]
            for j in range(0, n):
                t = typenames[j]
                if (o.type == t.type) and (o.name == t.name):
                    o.value = value
                    return
        self.node().addEventListener(typenames[0].type, value, options)
        o = {'type': typenames[0].type, 'name': typenames[0].name, 'value': value, 'listener': value, 'options': options}
        self.node().__on.push(o)
        return self

    # import selection_dispatch from "./dispatch.js";
    # def dispatch: selection_dispatch,
    # import defaultView from "../window.js";
    def dispatchEvent(self, node, type, params):
        window = defaultView(node)
        event = window.CustomEvent
        # TODO - write this as python
        # if (typeof event === "function") {
        #     event = new event(type, params);
        # } else {
        #     event = window.document.createEvent("Event");
        #     if (params) event.initEvent(type, params.bubbles, params.cancelable), event.detail = params.detail;
        #     else event.initEvent(type, false, false);
        # }
        if callable(event):
            event = event(type, params)
        else:
            event = event.createEvent("Event")
            if params:
                event.initEvent(type, params.bubbles, params.cancelable)
            else:
                event.initEvent(type, False, False)
        node.dispatchEvent(event)
        return node

    def dispatchConstant(self, type, params):
        return lambda this: dispatchEvent(this, type, params)

    def dispatchFunction(self, type, params, *args):
        return lambda this: dispatchEvent(this, type, Object(params).apply(this, args))

    def dispatch(self, type, params):
        # return this.each((typeof params === "function"
        #     ? dispatchFunction
        #     : dispatchConstant)(type, params))
        func = dispatchFunction if callable(params) else dispatchConstant
        return this.each(func(type, params))

    # import selection_iterator from "./iterator.js";
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
nextId = 0


def local():
    return Local


class Local():

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

    if (node.getBoundingClientRect):
        rect = node.getBoundingClientRect()
        return [event.clientX - rect.left - node.clientLeft, event.clientY - rect.top - node.clientTop]

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
    # print(document)
    if isinstance(selector, str):
        return Selection([document.querySelectorAll(selector)], [document.documentElement])
        # return Selection([document.getElementsBySelector(selector, document)], [document.documentElement])
    else:
        return Selection([array(selector)], root)


def selectorAll(selector):
    return empty if selector == None else lambda: document.querySelectorAll(selector)
