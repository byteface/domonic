"""
    domonic.dom
    ====================================

    The DOM represents a document with a logical tree.
    https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model

"""

from typing import Union, Tuple, List, Dict, Any, Optional, Callable, Iterable

import re
import copy

from domonic.events import Event, EventTarget, MouseEvent  # , KeyboardEvent, TouchEvent, UIEvent, CustomEvent
from domonic.style import CSSStyleDeclaration as Style, StyleSheetList
from domonic.geom import vec3

from domonic.webapi.url import URL
from domonic.webapi.console import Console  # left here for legacy reasons. access via window module instead


class Node(EventTarget):
    """ An abstract base class upon which many other DOM API objects are based """

    ELEMENT_NODE: int = 1
    TEXT_NODE: int = 3
    CDATA_SECTION_NODE: int = 4
    PROCESSING_INSTRUCTION_NODE: int = 7
    COMMENT_NODE: int = 8
    DOCUMENT_NODE: int = 9
    DOCUMENT_TYPE_NODE: int = 10
    DOCUMENT_FRAGMENT_NODE: int = 11

    DOCUMENT_POSITION_DISCONNECTED: int = 1
    DOCUMENT_POSITION_PRECEDING: int = 2
    DOCUMENT_POSITION_FOLLOWING: int = 4
    DOCUMENT_POSITION_CONTAINS: int = 8
    DOCUMENT_POSITION_CONTAINED_BY: int = 16
    DOCUMENT_POSITION_IMPLEMENTATION_SPECIFIC: int = 32

    # The following constants have been deprecated and should not be used anymore.
    ATTRIBUTE_NODE: int = 2
    ENTITY_REFERENCE_NODE: int = 5
    ENTITY_NODE: int = 6
    NOTATION_NODE: int = 12

    __context: list = None  # private. tags will append to last item in context on creation.

    # __slots__ = ['____attributes__',
    #              '__content',
    #              'name',
    #              '__rootNode',
    #              'parentNode',
    #              'baseURI',
    #              'isConnected',
    #              'namespaceURI',
    #              'outerText',
    #              'prefix']

    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs

        if getattr(self, 'name', None) is None:
            self.name = ''

        # if user doesn't put underscore (dont advertise this as still has issues.)
        new_kwargs = {}
        for k, v in kwargs.items():
            if k[0] != "_":
                new_kwargs[f"_{k}"] = v
            else:
                new_kwargs[k] = v
        self.kwargs = new_kwargs

        try:
            self.content = ''.join([each.__str__() for each in args])
            self.__attributes__ = ''.join([''' %s="%s"''' % (key.split('_', 1)[1], value) for key, value in self.kwargs.items()])
        except IndexError as e:
            from domonic.html import TemplateError
            raise TemplateError(e)
        # except Exception as e:
            # print(e)

        self.baseURI: str = 'eventual.technology'  # TODO - if ownerdocument has a basetag, use that
        self.isConnected: bool = True
        self.namespaceURI: str = "http://www.w3.org/1999/xhtml"
        self.outerText: str = None
        self.parentNode = None
        self.prefix = None  # 🗑️
        # self.baseURIObject = None  # ?
        # self.nodePrincipal = None
        self._update_parents()

        # attempt to set init namespaceURI based on the tag name
        try:
            n = self.rootNode
            nm = n.tagName
            # print(n)
            if nm == 'html':
                self.namespaceURI = 'http://www.w3.org/1999/xhtml'
            elif nm == 'svg':
                self.namespaceURI = 'http://www.w3.org/2000/svg'
            elif nm == 'xhtml':
                self.namespaceURI = 'http://www.w3.org/1999/xhtml'
            elif nm == 'xml':
                self.namespaceURI = 'http://www.w3.org/XML/1998/namespace'
            elif nm == 'xlink':
                self.namespaceURI = 'http://www.w3.org/1999/xlink'
            elif nm == 'math':
                self.namespaceURI = 'http://www.w3.org/1998/Math/MathML'
        except Exception as e:
            pass

        # this is for using 'with'
        if Node.__context is not None:
            Node.__context[len(Node.__context) - 1] += self
        super().__init__(*args, **kwargs)

    @property
    def content(self):  # TODO - test
        # return ''.join([each.__str__() for each in self.args])
        # if any child are lists by mistake, loop and call __str__ on each first
        cnt = self.args
        for i, arg in enumerate(cnt):
            if isinstance(arg, list):
                cnt = list(cnt)
                cnt[i] = ''.join([each.__str__() for each in arg])
                cnt = tuple(cnt)
        return ''.join([each.__str__() for each in cnt])

    @content.setter
    def content(self, ignore):
        self.__content = ''.join([each.__str__() for each in self.args])
        return

    @property
    def __attributes__(self):
        def format_attr(key, value):
            if value is True:
                value = 'true'
            if value is False:
                value = 'false'
            key = key.split('_', 1)[1]
            # lets us have boolean attributes  # TODO - should be optional by a global config
            if key in ['async', 'checked', 'autofocus', 'disabled', 'formnovalidate', 'hidden', 'multiple',
                       'novalidate', 'readonly', 'required', 'selected', "open", "contenteditable"]:
                if value == '' or value == key:
                    return ''' %s''' % key
            return ''' %s="%s"''' % (key, value)
        try:
            return ''.join([format_attr(key, value) for key, value in self.kwargs.items()])
        except IndexError as e:
            from domonic.html import TemplateError
            raise TemplateError(e)
        # except Exception as e:
            # print(e)

    @__attributes__.setter
    def __attributes__(self, ignore):
        try:
            self.__attributes = ''.join([''' %s="%s"''' % (key.split('_', 1)[1], value) for key, value in self.kwargs.items()])
        except IndexError as e:
            from domonic.html import TemplateError
            raise TemplateError(e)
        # except Exception as e:
            # print(e)

    def __str__(self):
        return f"<{self.name}{self.__attributes__}>{self.content}</{self.name}>"

    def __mul__(self, other):
        """
        requires you to render yourself i.e.
        cells = cell()*10
        print(''.join([str(c) for c in cells]))
        """
        reproducer = []
        for i in range(other):
            reproducer.append(copy.deepcopy(self))
        return reproducer

    def __rmul__(self, other):
        """
        requires you to render yourself i.e.
        cells = cell()*10
        print(''.join([str(c) for c in cells]))
        """
        reproducer = []
        for i in range(other):
            reproducer.append(copy.deepcopy(self))
        return reproducer

    def __truediv__(self, other):
        """ use to render clones without having to parse commas yourself """
        reproducer = []
        for i in range(other):
            reproducer.append(str(self))
        return ''.join(reproducer)

    def __rtruediv__(self, other):
        """ use to render clones without having to parse commas yourself """
        reproducer = []
        for i in range(other):
            reproducer.append(str(self))
        return ''.join(reproducer)

    def __div__(self, other):
        """
        useful for prototyping as renders. to retain objects use multiply
        """
        reproducer = []
        for i in range(other):
            reproducer.append(str(self))
        return ''.join(reproducer)

    def __rdiv__(self, other):
        """
        useful for prototyping as renders. to retain objects use multiply
        """
        reproducer = []
        for i in range(other):
            reproducer.append(str(self))
        return ''.join(reproducer)

    def __or__(self, other):
        """ return self unless other is something """
        if other is not False:
            return other
        return self

    def __iadd__(self, item):
        """ adds an item to the nodes of children. can also pass a list and it will unpack them """
        if isinstance(item, (list, tuple)):  # TODO - Documentfragment?
            for i in item:
                self.args = self.args + (i,)
            return self

        self.args = self.args + (item,)
        return self

    def __isub__(self, item):
        """ removes an item from the list of children """
        replace_args = list(self.args)
        replace_args.remove(item)
        self.args = tuple(replace_args)
        return self

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.args[index]
        # elif isinstance(index, str):
        #     if index.startswith('_'):
        #         return self.kwargs[index]
        #     else:
        #         return getattr(self, index)
        # super(Node, self).__getitem__(index)

        if isinstance(index, str):
            # call props on self
            # print('erk!')
            try:
                # return Node.__dict__[index]
                return getattr(self, index)
            except Exception as e:
                print(e)
                # return None
        # return super(Node, self).__getitem__(index)

    def __rshift__(self, item):
        try:
            for key in item.keys():
                self.kwargs[key] = item[key]
            return self
        except Exception as e:
            print(e)
            raise ValueError

    # def __add__(self, item):
    #     try:
    #         self.args = self.args + (item,)
    #         return self
    #     except Exception as e:
    #         print(e)
    #         raise ValueError

    # def __sub__(self, item):
    #     try:
    #         self.args = self.args - (item,)
    #         return self
    #     except Exception as e:
    #         print(e)
    #         raise ValueError

    # def render()

    def __getattr__(self, attr):
        """
        allows dot notation for reading attributes
        *credit to the peeps on discord/python for this one*
        """
        kwargs = super().__getattribute__('kwargs')

        if attr in kwargs:
            return kwargs[attr]

        retry = "_" + attr
        if retry in kwargs:
            return kwargs[retry]

        retry = attr[1:len(attr)]
        if retry in kwargs:
            return kwargs[retry]

        try:
            # return getattr(super(), attr)
            # return getattr(self, attr)
            # return getattr(Node, attr)  # means overrideing for style etc in element?
            return getattr(self.__class__, attr)  # means overrideing for style etc in element?
            # return getattr(Element, attr)
        except AttributeError as e:
            # print(e) # TODO - careful. better on for debugging.
            raise e  # ("attribute does not exist:", attr)

        raise AttributeError

    def __pyml__(self):
        """ [returns a representation of the object as a pyml string] """
        # from domonic.dom import Text
        params = ""
        for key, value in self.kwargs.items():
            if '-' in key:
                params += f'**\u007b"{key}":{value}\u007d,'
            else:
                params += f'{key}="{value}", '
        # TODO - will need to loop args and call __pyml__ on each one
        for arg in self.args:
            try:
                if isinstance(arg, Text):
                    params += str(arg) + ", "
                else:
                    params += f"{arg.__pyml__()}, "
            except Exception as e:
                params += str(arg) + ", "
        # TODO - if self is document do dentage
        return f"{self.name}({params[:-2]})"
        # return f"{self.name}({params})"
        # return f"{self.name}({args}, {params})"
        # return f"<{self.name}{self.__attributes__}>{self.content}</{self.name}>"

    # def __repr__(self):
    #     return f"<{self.name}{self.__attributes__}>{self.content}</{self.name}>"

    def __setitem__(self, key, value):
        try:
            self.kwargs[key] = value
            return self
        except Exception as e:
            print(e)
            raise ValueError

    def __enter__(self):
        if Node.__context is None:
            Node.__context = []
        Node.__context.append(self)
        return self

    def __exit__(self, type, value, traceback, *args, **kwargs):
        Node.__context.pop()
        if len(Node.__context) == 0:
            Node.__context = None
        return self

    # def __dir__(self):
    #     return self.__dict__.keys()

    # TODO - these are hard and wil need tests
    # def __setattr__(self, attr, value):
    # def __delattr__(self, attr):
    # def __next__(self):
    # def __iter__(self):

    def __format__(self, format_spec):
        # return super().__format__(format_spec)
        # get node depth by counting parents

        # TODO - this is a hack to get the depth of the node
        n = self
        depth = 0
        while n is not None:
            # print(type(n), type(n.parentNode))
            n = n.parentNode
            depth += 1

        depth -= 1

        # print(f"depth: {depth}")
        # dent = '    ' * depth
        dent = '\t' * depth

        # loop the children and call __format__ on each one
        # content = ""
        # for child in self.childNodes:
        #     content += child.__format__(format_spec)

        self._update_parents()

        content = ''.join([each.__format__(format_spec) for each in self.args])
        # from concurrent.futures import ThreadPoolExecutor
        # content = ''
        # with ThreadPoolExecutor(10) as executor:
        #     for result in executor.map(lambda x: x.__format__(format_spec), self.args):
        #         content += result

        wrap = False
        if len(self.args) == 1:
            if not isinstance(self.args[0], Element):
                wrap = True

        dtype = ""
        if isinstance(self, Document):
            # dtype = "<!DOCTYPE html>"
            dtype = self.doctype

        # if self is a closed_tag, return the content
        from domonic.html import closed_tag
        if isinstance(self, closed_tag):
            return f"\n{dent}<{self.name}{self.__attributes__} />"

        size = len(str(content))
        if size < 150 and wrap:
            return f"\n{dent}<{self.name}{self.__attributes__}>{content}</{self.name}>"
        else:
            return f"{dtype}\n{dent}<{self.name}{self.__attributes__}>{content}\n{dent}</{self.name}>"

    # def __call__(self, *args, **kwargs):
    #     """
    #     allows for calling the object as a function
    #     """
    #     print('calling a tag')
    #     print(args)
    #     print(kwargs)
    #     print(self.name)

    def __setattr__(self, name: str, value: Any) -> None:
        try:
            if name == "args":
                super(Node, self).__setattr__(name, value)
                self._update_parents()
                return
        except Exception as e:
            print(e)
            # pass
        super(Node, self).__setattr__(name, value)

    # def __getattr__(self, name):
    #     # print(name)
    #     try:
    #         if name == "args":
    #             return super(Node, self).__getattr__(name)
    #     except Exception as e:
    #         print(e)
    #     return super(Node, self).__getattr__(name)

    # def __getattribute__(self, name):
        # print('how are you doing today', name)
        # try:
        #     if name == "args":
        #         return super(Node, self).__getattribute__(name)
        # except Exception as e:
        #     print(e)
        # check if its a property on the class
        # if name in self.__dict__:
            # return super(Node, self).__getattribute__(name)
        # return super(Node, self).__getattribute__(name)
        # return self.__dict__[item]

# def __getattr__(self, attrName):
        # if name not in self.__dict__:
        #     value = self.fetchAttr(name)    # computes the value
        #     self.__dict__[name] = value
        # return self.__dict__[name]

    # TODO - html.tag class currently has the required method as its called there.
    # def __getitem__(self, item):
    #     print('GET ITEM CALLED')
    #     if isinstance(item, int):
    #         return self.childNodes[item]
    #     if isinstance(item, str):
    #         # call props on self
    #         print('sup!')
    #         try:
    #             return self.__dict__[item]
    #         except Exception as e:
    #             print(e)
    #             # return None
    #     return super(Node, self).__getitem__(item)

    def _update_parents(self):
        ''' private. - TODO < check these docstrings don't export in docs
        loops all children and sets self as parent.
        cant do as decorator for now as that seems to breaks potential for json serialisation (see Style)
        so will have to call manually whenever self.args are ammended.
        '''
        try:
            # print(self.args)
            for el in self.args:
                # if(type(el) not in [str, list, dict, int, float, tuple, object, set]):
                if isinstance(el, (Element, Node)):
                    el.parentNode = self
                    el._update_parents()
        except Exception as e:
            print('unable to update parent', e)


    def _iterate(self, element, callback) -> None:
        ''' private. - TODO < check these docstrings don't export in docs
        loops all children and sets self as parent.
        cant do as decorator for now as that seems to breaks potential for json serialisation (see Style)
        so will have to call manually whenever self.args are ammended.
        '''
        callback(element)  # TODO - this can block on failed attributes
        elements = []
        if isinstance(element, Node):
            elements = element.args
        elif isinstance(element, list):
            elements = element
        try:
            for el in elements:
                if(type(el) not in [str, list, dict, int, float, tuple, object, set]):
                    # callback(el)
                    el._iterate(el, callback)
                elif isinstance(el, list):  # if someone is incorrectly using a list as a child
                    for e in el:
                        if type(e) not in (str, list, dict, int, float, tuple, object, set):
                            e._iterate(e, callback)
        except Exception as e:
            print('_iterate error', e)

    def __len__(self):
        return len(self.args)

    def appendChild(self, aChild: 'Node') -> 'Node':
        """
        Adds a child to the current element.
        If item is a DocumentFragment, all its children are added.

        Args:
            item (Node): The Node to add.
        """
        if isinstance(aChild, DocumentFragment):
            items = aChild.args
            self.args = self.args + items
            return DocumentFragment()
        else:
            self.args = self.args + (aChild,)
            # return aChild  # causes max recursion when called chained? then don't chain?
            return aChild

    @property
    def childElementCount(self) -> int:
        """ Returns the number of child elements an element has """
        return len(self.args)

    @property
    def childNodes(self) -> 'NodeList':
        """ Returns a live NodeList containing all the children of this node """
        # return list(self.args)
        return NodeList(self.args)

    @property
    def children(self):
        """ Returns a collection of an element's child element (excluding text and comment nodes) """
        newlist: list = []
        for each in self.args:
            if(type(each) != str):
                newlist.append(each)
        return newlist

    def compareDocumentPosition(self, otherElement) -> int:
        """
        An integer value representing otherNode's position relative to node as a bitmask combining the following constant properties of Node:

        https://stackoverflow.com/questions/8334286/cross-browser-compare-document-position

        """
        thisNode = self
        other = otherElement

        # if isinstance(other, str):
        #     other = Text(other)
        # if isinstance(thisNode, str):
        #     thisNode = Text(thisNode)

        def recursivelyWalk(nodes, cb):
            for node in nodes:
                if isinstance(node, str):
                    node = Text(node)
                    # continue
                ret = cb(node)
                if ret:
                    return ret
                if node.childNodes and node.childNodes.length > 0:
                    ret = recursivelyWalk(node.childNodes, cb)
                    if ret:
                        return ret

        def testNodeForComparePosition(node, other):
            if node is other:
                return True

        def identifyWhichIsFirst(node):
            if (node == other):
                return "other"
            elif (node == reference):
                return "reference"

        reference = thisNode
        referenceTop = thisNode
        otherTop = other

        if self == other:
            return 0
        while referenceTop.parentNode is not None:
            referenceTop = referenceTop.parentNode
        while otherTop.parentNode is not None:
            otherTop = otherTop.parentNode

        # print(referenceTop, otherTop)
        if referenceTop != otherTop:
            return Node.DOCUMENT_POSITION_DISCONNECTED

        children = reference.childNodes

        ret = recursivelyWalk(
            children,
            lambda p: testNodeForComparePosition(other, p)
        )
        if ret:
            return Node.DOCUMENT_POSITION_CONTAINED_BY  # + Node.DOCUMENT_POSITION_FOLLOWING

        children = other.childNodes
        ret = recursivelyWalk(
            children,
            lambda p: testNodeForComparePosition(reference, p)
        )
        if ret:
            return Node.DOCUMENT_POSITION_CONTAINS  # + Node.DOCUMENT_POSITION_PRECEDING
        ret = recursivelyWalk(
            [referenceTop],
            identifyWhichIsFirst
        )
        if ret == "other":
            return Node.DOCUMENT_POSITION_PRECEDING
        else:
            return Node.DOCUMENT_POSITION_FOLLOWING

    def contains(self, node):
        """ Check whether a node is a descendant of a given node """
        # this will go crunch on big stuff... need to consider best way
        for each in self.args:
            if each == node:
                return True
            try:
                if each.contains(node):
                    return True
            except Exception:
                pass  # TODO - dont iterate strings

        return False

    @property
    def firstChild(self):
        """ Returns the first child node of an element """
        try:
            return self.args[0]  # TODO - check if this means includes content
        except Exception:
            return None

    def hasChildNodes(self) -> bool:
        """ Returns true if an element has any child nodes, otherwise false """
        return len(self.args) > 0

    @property
    def lastChild(self):
        """ Returns the last child node of an element """
        try:
            return self.args[len(self.args) - 1]
        except Exception:
            return None

    @property
    def localName(self):
        try:
            return self.tagName
        except Exception:
            return None

    @property
    def nodeName(self):
        """ Returns the name of a node """
        # TODO - not sure what's better this or overriding on every element
        # if isinstance(self, Text):
        #     return '#text'
        if isinstance(self, Comment):
            return '#comment'
        # elif isinstance(self, DocumentType):
        #     return '#doctype'
        elif isinstance(self, Document):
            return '#document'
        elif isinstance(self, CDATASection):
            return '#cdata-section'
        elif isinstance(self, DocumentFragment):
            return '#document-fragment'
        elif isinstance(self, Attr):
            return self.name
        elif isinstance(self, ProcessingInstruction):
            return self.target
        elif isinstance(self, DocumentType):
            return self.name

        # print(type(self))
        if isinstance(self, Element):
            return self.tagName  # .upper()
        else:
            try:
                return self.tagName
            except Exception:
                return None

    # @property
    # def nodeType(self):
    #     """ Returns the node type of a node """
    #     return self.ELEMENT_NODE
    nodeType: int = ELEMENT_NODE

    @property
    def nodeValue(self):
        """ Sets or returns the value of a node """
        outp = ""
        for each in self.args:
            if type(each) is str:
                outp = outp + each
            else:
                val = each.nodeValue
                if val is not None:
                    outp = outp + val
                else:
                    return None
        if outp == '':
            outp = None
        return outp

    @nodeValue.setter
    def nodeValue(self, content):
        """ Sets or returns the value of a node """
        self.args = (content,)
        return content

    @property
    def ownerDocument(self):
        """ Returns the root element (document object) for an element """
        return self.rootNode

    @ownerDocument.setter
    def ownerDocument(self, newOwner):  #: Element):
        # self.rootNode = newOwner # NOTE - you can't set rootNode it's property that calcs it
        pass

    @property
    def rootNode(self):
        """[read-only property returns a Node object representing the topmost node in the tree,
        or the current node if it's the topmost node in the tree]

        Returns:
            [Node]: [the topmost Node in the tree]
        """
        if isinstance(self, Document):
            return self

        node = self
        nxt = self.parentNode
        while nxt is not None:
            node = nxt
            nxt = nxt.parentNode
        return node

    def insertBefore(self, new_node, reference_node=None):
        """ inserts a node before a reference node as a child of a specified parent node.
            this will remove the node from its previous parent node, if any.

            # TODO - can throw value error if wrong ordered params. may be helpful to catch to say so.
        """
        if reference_node is None:
            self.appendChild(new_node)
        else:
            # remove new_node from its previous parent node
            if new_node.parentNode is not None:
                new_node.parentNode.removeChild(new_node)
            self.args = self.args[:self.args.index(reference_node)] + (new_node,) + self.args[self.args.index(reference_node):]
        return new_node

    def removeChild(self, node):
        """ removes a child node from the DOM and returns the removed node."""
        for count, each in enumerate(self.args):
            if type(each) == str:
                continue

            if each == node:
                n = node
                n.parentNode = None
                replace_args = list(self.args)
                replace_args.remove(node)
                self.args = tuple(replace_args)

                return n
            r = each.removeChild(node)
            if r:
                return r

        return None

    def replaceChild(self, newChild, oldChild):
        """[Replaces a child node within the given (parent) node.]

        Args:
            newChild ([type]): [a Node object]
            oldChild ([type]): [a Node object]

        Returns:
            [type]: [the old child node]
        """
        for count, each in enumerate(self.args):
            if each == oldChild:
                replace_args = list(self.args)
                replace_args[count] = newChild
                self.args = tuple(replace_args)
                return oldChild
        return oldChild
        # for count, each in enumerate(self.args):
        #     if each == oldChild:
        #         n = oldChild
        #         self.removeChild(newChild)  # doc remove child?
        #         list(self.args).remove(oldChild)
        #         list(self.args).insert(count, newChild)
        #         return n

        #     r = each.replaceChild(newChild, oldChild)
        #     if r:
        #         return r

        # return None

    def cloneNode(self, deep: bool = True):
        """ Returns a copy. """
        import copy
        if deep:
            return copy.deepcopy(self)
        else:
            return copy.copy(self)  # shallow copy

    def isSameNode(self, node):
        """ Checks if two elements are the same node """
        return (self == node)

    def isEqualNode(self, node):
        """ Checks if two elements are equal """
        return (str(self) == str(node))

    def getRootNode(self, options=None):
        # if options is not None:
        # if options['composed'] = True:
        # TODO - need to implement composed
        return self.rootNode

    def isDefaultNamespace(self, ns):
        """ Checks if a namespace is the default namespace """
        if ns == self.namespaceURI:
            return True
        else:
            return False

    def lookupNamespaceURI(self, ns: str):
        """ Returns the namespace URI for a given prefix

        :param ns: prefix - i.e 'xml', 'xlink', 'svg', etc

        """
        from domonic.constants import namespaces
        if ns in namespaces:
            return namespaces[ns]
        else:
            return None

    def lookupPrefix(self, ns):
        """ Returns the prefix for a given namespace URI """
        if ns == self.namespaceURI:
            return self.prefix
        else:
            return None

    @property
    def nextSibling(self):
        """[returns the next sibling of the current node.]
        """
        if self.parentNode is None:
            return None
        else:
            for count, node in enumerate(self.parentNode.args):
                if node == self:
                    if count == len(self.parentNode.args) - 1:
                        return None
                    else:
                        return self.parentNode.args[count + 1]

    def normalize(self):
        """ Normalize a node's value """
        return None

    @property
    def previousSibling(self):
        """[returns the previous sibling of the current node.]
        """
        if self.parentNode is None:
            return None
        else:
            for count, node in enumerate(self.parentNode.args):
                if node == self:
                    if count == 0:
                        return None
                    else:
                        return self.parentNode.args[count - 1]

    @property
    def textContent(self):
        """ Returns the text content of a node and its descendants """
        # TODO - test- also check difference to nodeValue
        # nodevalue is lvl 1 spec. textcontent is lvl 3 spec.
        outp = ""
        for each in self.args:
            if type(each) is str:
                outp = outp + each
            else:
                val = each.textContent
                if val is not None:
                    outp = outp + val
                else:
                    return None
        if outp == '':
            outp = None
        return outp

    @textContent.setter
    def textContent(self, content):
        """ Sets the text content of a node and its descendants """
        self.args = (content,)
        return content

    # def isSupported(self): return False #  🗑
    # getUserData() 🗑️
    # setUserData() 🗑️

    # non standard methods to be etree compatible
    # seems to make it work with https://github.com/sissaschool/elementpath
    # if i hack it to allow domonic root nodes

    def iter(self, tag=None):
        """ Creates a tree iterator with the current element as the root. 
        The iterator iterates over this element and all elements below it, in document (depth first) order.
        If tag is not None or '*', only elements whose tag equals tag are returned from the iterator.
        If the tree structure is modified during iteration, the result is undefined."""
        for each in self.args:
            if type(each) is str:
                continue
            if tag is None or tag == '*':
                yield each
            elif each.tag == tag:
                yield each
            for x in each.iter(tag):
                yield x

    @property
    def tag(self):
        """ Returns the tag name of the current node """
        return self.nodeName

    @property
    def text(self):
        """ Returns the text content of the current node """
        return self.textContent

    @property
    def attrib(self):
        """ Returns the attributes of the current node as a dict not a NamedNodeMap """
        try:
            # print(self.kwargs)
            return self.kwargs
        except Exception as e:
            # print('failed::', e)
            return None

    @property
    def tail(self):
        """ Returns the text content of the current node """
        return self.textContent


class ParentNode(object):
    """ not tested yet """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # @property
    # def childElementCount(self):
    #     return len(self.args)

    # @property
    # def children(self):
    #     return self.args

    # @property
    # def firstElementChild(self):
    #     raise NotImplementedError

    # @property
    # def lastElementChild(self):
    #     raise NotImplementedError

    def append(self, *args):
        self.args += (args)
        return self

    def prepend(self, *args):
        self.args = (args).extend(self.args)
        return self

    def replaceChildren(self, children):
        self.args = children


class ChildNode(Node):
    """ not tested yet """

    def remove(self):
        """Removes this ChildNode from the children list of its parent."""
        if self.parentNode is None:
            self._update_parents()
        if self.parentNode is not None:
            self.parentNode.removeChild(self)
        return self

    def replaceWith(self, newChild):
        """ Replaces this ChildNode with a new one. """
        self.parentNode.replaceChild(newChild, self)
        return self

    def before(self, newChild):
        """ Inserts a newChild node immediately before this ChildNode. """
        self.parentNode.insertBefore(newChild, self)
        return self

    def after(self, newChild):
        """ Inserts a newChild node immediately after this ChildNode. """
        self.parentNode.insertBefore(newChild, self)
        return self


class Attr(Node):
    # https://developer.mozilla.org/en-US/docs/Web/API/Attr

    nodeType: int = Node.ATTRIBUTE_NODE
    __slots__ = ('name', 'value')

    def __init__(self, name: str, value="", *args, **kwargs) -> None:
        self.name: str = name
        self.value = value
        # self.nodeType: int = Node.ATTRIBUTE_NODE

    @property
    def isId(self) -> bool:
        if self.name == "id":
            return True
        else:
            return False

    def getNamedItem(self, name: str):
        """ Returns a specified attribute node from a NamedNodeMap """
        for item in self.parentNode.attributes:
            if item.name == name:
                return item
        return None

    # def __getitem__(self, name):
    #     return self.getNamedItem(name)

    # def __setitem__(self, name, value):
    #     self.setNamedItem(name, value)

    def removeNamedItem(self, name: str) -> bool:
        """ Removes a specified attribute node """
        for item in self.parentNode.attributes:
            if item.name == name:
                self.parentNode.removeAttribute(item)
                return True
        return False

    def setNamedItem(self, name: str, value) -> bool:
        """ Sets the specified attribute node (by name) """
        for item in self.parentNode.attributes:
            if item.name == name:
                item.value = value
                return True
        return False


# from xml.dom.minidom import Attr
from xml.dom.minidom import NamedNodeMap

# class NamedNodeMap(NamedNodeMap):
# def __getitem__(self, name):
#     self.getNamedItem(name)
# def __setitem__(self, name: str, value):
#     self.setNamedItem(name, value)


'''
class NamedNodeMap(object):
    """ TODO - not tested yet.

    a live object that represents a list of nodes.
    """

    def __init__(self, parentNode=None, *args, **kwargs):
        self.parentNode = parentNode
        self.args = args
        self.kwargs = kwargs
        super().__init__(*args, **kwargs)

    def getNamedItem(self, name):
        """ Returns a specified attribute node from a NamedNodeMap """
        for item in self.args:
            if item.name == name:
                return item
        return None

    def __getitem__(self, name):
        print('getting:', name)
        # return self.getNamedItem(name)
        return self.parentNode.kwargs['_' + name]

    def setNamedItem(self, name, value):
        """ Replaces, or adds, the Attr identified in the map by the given name."""
        # if exists replace it otherwise add it
        has_item = False
        for item in self.args:
            if item.name == name:
                item.value = value
                has_item = True
                # return True
        if not has_item:
            self.args.append(Attr(name, value))

        self.parentNode.kwargs['_' + name] = value
        return True

    def __setitem__(self, name: str, value):
        self.setNamedItem(name, value)

    def removeNamedItem(self, name: str):
        """ Removes a specified attribute node """
        for item in self.args:
            if item.name == name:
                self.remove(item)
                return True
        return False

    def item(self, index):
        """ Returns the index'th item in the collection """
        return self.args[index]

    def getNameItemNS(self, namespaceURI: str, localName: str):
        """ Returns a specified attribute node from a NamedNodeMap """
        for item in self.args:
            if item.namespaceURI == namespaceURI and item.localName == localName:
                return item
        return None

    def setNamedItemNS(self, namespaceURI: str, localName: str, value):
        """ Sets the specified attribute node (by name) """
        for item in self.args:
            if item.namespaceURI == namespaceURI and item.localName == localName:
                item.value = value
                return True
        return False

    def removeNamedItemNS(self, namespaceURI: str, localName: str) -> bool:
        """ Removes a specified attribute node """
        for item in self.args:
            if item.namespaceURI == namespaceURI and item.localName == localName:
                self.remove(item)  # TODO - check this? where is remove?
                return True
        return False
'''


class DOMStringMap(object):
    """
    TODO - not tested yet
    TODO - make this like a dict
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, name: str):
        """ Returns the value of the item with the specified name """
        for item in self.args:
            if item.name == name:
                return item.value
        return None

    def set(self, name: str, value):
        """ Sets the value of the item with the specified name """
        for item in self.args:
            if item.name == name:
                item.value = value
                return True
        return False

    def delete(self, name: str) -> bool:
        """ Deletes the item with the specified name """
        for item in self.args:
            if item.name == name:
                self.remove(item)
                return True
        return False

    # def has(self, name):
    #     """ Returns true if the specified name exists """
    #     for item in self.args:
    #         if item.name == name:
    #             return True
    #     return False

    # def clear(self):
    #     """ Removes all items from the map """
    #     self.args = []
    #     return True

    # def keys(self):
    #     """ Returns an array of all the names in the map """
    #     return [item.name for item in self.args]

    # def values(self):
    #     """ Returns an array of all the values in the map """
    #     return [item.value for item in self.args]


class DOMTokenList(object):
    """ TODO - not tested yet """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add(self, *args) -> bool:
        """ Adds the given tokens to the list """
        for item in args:
            if item not in self.args:
                self.args.append(item)
                return True
        return False

    def remove(self, *args) -> bool:
        """ Removes the given tokens from the list """
        for item in args:
            if item in self.args:
                self.args.remove(item)
                return True
        return False

    def toggle(self, token, force):
        """ If force is not given, removes token from list if present,
        otherwise adds token to list. If force is true, adds token to list,
        and if force is false, removes token from list if present. """
        if force is None:
            if token in self.args:
                self.args.remove(token)
            else:
                self.args.append(token)
        elif force is True:
            self.add(token)
        elif force is False:
            self.remove(token)
        else:
            raise TypeError("force must be a boolean")

    def contains(self, token) -> bool:
        """ Returns true if the token is in the list, and false otherwise """
        if token in self.args:
            return True
        return False

    def item(self, index: int):
        """ Returns the token at the specified index """
        return self.args[index]

    def toString(self) -> str:
        """ Returns a string containing all tokens in the list, with spaces separating each token """
        return " ".join(self.args)


class ShadowRoot(Node):  # TODO - this may need to extend tag also to get the args/kwargs
    """ property on element that has hidden DOM """
    def __init__(self, host, mode='open'):
        self.delegatesFocus = False
        self.host = host
        self.mode = mode

    def getSelection(self):
        """
        Returns a Selection object representing the range of text selected by the user,
        or the current position of the caret.
        """
        raise NotImplementedError

    def elementFromPoint(self, x, y):
        """ Returns the topmost element at the specified coordinates. """
        raise NotImplementedError

    def elementsFromPoint(self, x, y):
        """ Returns an array of all elements at the specified coordinates. """
        raise NotImplementedError

    def caretPositionFromPoint(self):
        """
        Returns a CaretPosition object containing the DOM node containing the caret,
        and caret's character offset within that node.
        """
        raise NotImplementedError


class DocumentType(Node):

    nodeType = Node.DOCUMENT_TYPE_NODE
    __slots__ = ('name', 'publicId', 'systemId')

    def __init__(self, name: str = "html", publicId: str = "", systemId: str = "") -> None:
        self.name: str = name  # A DOMString, eg "html" for <!DOCTYPE HTML>.
        self.publicId: str = publicId  # eg "-//W3C//DTD HTML 4.01//EN", empty string for HTML5.
        self.systemId: str = systemId  # eg "http://www.w3.org/TR/html4/strict.dtd", empty string for HTML5.
        super().__init__()

    def internalSubset(self):
        ''' A DOMString of the internal subset, or None. Eg "<!ELEMENT foo (bar)>".'''
        if self.systemId:
            return self.systemId
        else:
            return None

    def notations(self) -> NamedNodeMap:
        """ A NamedNodeMap with notations declared in the DTD. """
        nnm = NamedNodeMap()
        for item in self.ownerDocument.args:
            if item.nodeType == Node.NOTATION_NODE:
                nnm.append(item)
        return nnm

    # @property
    # def nodeType(self):
    #     return Node.DOCUMENT_TYPE_NODE

    def __str__(self) -> str:
        return f"<!DOCTYPE {self.name} {self.publicId} {self.systemId}>"


"""
def AriaMixin():  #???

    @property
    def ariaAtomic(self):
        return self.getAttribute('aria-atomic')

    @ariaAtomic.setter
    def ariaAtomic(self, value: str):
        self.setAttribute('aria-atomic', value)

    @property
    def ariaAtomic(self):
        return self.getAttribute('aria-atomic')

    @property
    def ariaAutoComplete(self):
        return self.getAttribute('aria-autoComplete')

    @ariaAutoComplete.setter
    def ariaAutoComplete(self, value: str):
        return self.getAttribute('aria-autoComplete')

    @property
    def ariaBusy(self):
        return self.getAttribute('aria-busy')

    @ariaBusy.setter
    def ariaBusy(self, value: str):
        return self.getAttribute('aria-busy')

    @property
    def ariaChecked(self):
        return self.getAttribute('aria-checked')

    @ariaChecked.setter
    def ariaChecked(self, value: str):
        return self.getAttribute('aria-checked')

    @property
    def ariaColCount(self):
        return self.getAttribute('aria-colCount')

    @ariaColCount.setter
    def ariaColCount(self, value: str):
        return self.getAttribute('aria-colCount')

    @property
    def ariaColIndex(self):
        return self.getAttribute('aria-colIndex')

    @ariaColIndex.setter
    def ariaColIndex(self, value: str):
        return self.getAttribute('aria-colIndex')

    @property
    def ariaColIndexText(self):
        return self.getAttribute('aria-colIndexText')

    @ariaColIndexText.setter
    def ariaColIndexText(self, value: str):
        return self.getAttribute('aria-colIndexText')

    @property
    def ariaColSpan(self):
        return self.getAttribute('aria-colSpan')

    @ariaColSpan.setter
    def ariaColSpan(self, value: str):
        return self.getAttribute('aria-colSpan')

    @property
    def ariaCurrent(self):
        return self.getAttribute('aria-current')

    @ariaCurrent.setter
    def ariaCurrent(self, value: str):
        return self.getAttribute('aria-current')

    @property
    def ariaDescription(self):
        return self.getAttribute('aria-description')

    @ariaDescription.setter
    def ariaDescription(self, value: str):
        return self.getAttribute('aria-description')

    @property
    def ariaDisabled(self):
        return self.getAttribute('aria-disabled')

    @ariaDisabled.setter
    def ariaDisabled(self, value: str):
        return self.getAttribute('aria-disabled')

    @property
    def ariaExpanded(self):
        return self.getAttribute('aria-expanded')

    @ariaExpanded.setter
    def ariaExpanded(self, value: str):
        return self.getAttribute('aria-expanded')

    @property
    def ariaHasPopup(self):
        return self.getAttribute('aria-hasPopup')

    @ariaHasPopup.setter
    def ariaHasPopup(self, value: str):
        return self.getAttribute('aria-hasPopup')

    @property
    def ariaHidden(self):
        return self.getAttribute('aria-hidden')

    @ariaHidden.setter
    def ariaHidden(self, value: str):
        return self.getAttribute('aria-hidden')

    @property
    def ariaKeyShortcuts(self):
        return self.getAttribute('aria-keyShortcuts')

    @ariaKeyShortcuts.setter
    def ariaKeyShortcuts(self, value: str):
        return self.getAttribute('aria-keyShortcuts')

    @property
    def ariaLabel(self):
        return self.getAttribute('aria-label')

    @ariaLabel.setter
    def ariaLabel(self, value: str):
        return self.getAttribute('aria-label')

    @property
    def ariaLevel(self):
        return self.getAttribute('aria-level')

    @ariaLevel.setter
    def ariaLevel(self, value: str):
        return self.getAttribute('aria-level')

    @property
    def ariaLive(self):
        return self.getAttribute('aria-live')

    @ariaLive.setter
    def ariaLive(self, value: str):
        return self.getAttribute('aria-live')

    @property
    def ariaModal(self):
        return self.getAttribute('aria-modal')

    @ariaModal.setter
    def ariaModal(self, value: str):
        return self.getAttribute('aria-modal')

    @property
    def ariaMultiline(self):
        return self.getAttribute('aria-multiline')

    @ariaMultiline.setter
    def ariaMultiline(self, value: str):
        return self.getAttribute('aria-multiline')

    @property
    def ariaMultiSelectable(self):
        return self.getAttribute('aria-multiSelectable')

    @ariaMultiSelectable.setter
    def ariaMultiSelectable(self, value: str):
        return self.getAttribute('aria-multiSelectable')

    @property
    def ariaOrientation(self):
        return self.getAttribute('aria-orientation')

    @ariaOrientation.setter
    def ariaOrientation(self, value: str):
        return self.getAttribute('aria-orientation')

    @property
    def ariaPlaceholder(self):
        return self.getAttribute('aria-placeholder')

    @ariaPlaceholder.setter
    def ariaPlaceholder(self, value: str):
        return self.getAttribute('aria-placeholder')

    @property
    def ariaPosInSet(self):
        return self.getAttribute('aria-posInSet')

    @ariaPosInSet.setter
    def ariaPosInSet(self, value: str):
        return self.getAttribute('aria-posInSet')

    @property
    def ariaPressed(self):
        return self.getAttribute('aria-pressed')

    @ariaPressed.setter
    def ariaPressed(self, value: str):
        return self.getAttribute('aria-pressed')

    @property
    def ariaReadOnly(self):
        return self.getAttribute('aria-readOnly')

    @ariaReadOnly.setter
    def ariaReadOnly(self, value: str):
        return self.getAttribute('aria-readOnly')

    @property
    def ariaRelevant(self):
        return self.getAttribute('aria-relevant')

    @ariaRelevant.setter
    def ariaRelevant(self, value: str):
        return self.getAttribute('aria-relevant')

    @property
    def ariaRequired(self):
        return self.getAttribute('aria-required')

    @ariaRequired.setter
    def ariaRequired(self, value: str):
        return self.getAttribute('aria-required')

    @property
    def ariaRoleDescription(self):
        return self.getAttribute('aria-roleDescription')

    @ariaRoleDescription.setter
    def ariaRoleDescription(self, value: str):
        return self.getAttribute('aria-roleDescription')

    @property
    def ariaRowCount(self):
        return self.getAttribute('aria-rowCount')

    @ariaRowCount.setter
    def ariaRowCount(self, value: str):
        return self.getAttribute('aria-rowCount')

    @property
    def ariaRowIndex(self):
        return self.getAttribute('aria-rowIndex')

    @ariaRowIndex.setter
    def ariaRowIndex(self, value: str):
        return self.getAttribute('aria-rowIndex')

    @property
    def ariaRowIndexText(self):
        return self.getAttribute('aria-rowIndexText')

    @ariaRowIndexText.setter
    def ariaRowIndexText(self, value: str):
        return self.getAttribute('aria-rowIndexText')

    @property
    def ariaRowSpan(self):
        return self.getAttribute('aria-rowSpan')

    @ariaRowSpan.setter
    def ariaRowSpan(self, value: str):
        return self.getAttribute('aria-rowSpan')

    @property
    def ariaSelected(self):
        return self.getAttribute('aria-selected')

    @ariaSelected.setter
    def ariaSelected(self, value: str):
        return self.getAttribute('aria-selected')

    @property
    def ariaSetSize(self):
        return self.getAttribute('aria-setSize')

    @ariaSetSize.setter
    def ariaSetSize(self, value: str):
        return self.getAttribute('aria-setSize')

    @property
    def ariaSort(self):
        return self.getAttribute('aria-sort')

    @ariaSort.setter
    def ariaSort(self, value: str):
        return self.getAttribute('aria-sort')

    @property
    def ariaValueMax(self):
        return self.getAttribute('aria-valueMax')

    @ariaValueMax.setter
    def ariaValueMax(self, value: str):
        return self.getAttribute('aria-valueMax')

    @property
    def ariaValueMin(self):
        return self.getAttribute('aria-valueMin')

    @ariaValueMin.setter
    def ariaValueMin(self, value: str):
        return self.getAttribute('aria-valueMin')

    @property
    def ariaValueNow(self):
        return self.getAttribute('aria-valueNow')

    @ariaValueNow.setter
    def ariaValueNow(self, value: str):
        return self.getAttribute('aria-valueNow')

    @property
    def ariaValueText(self):
        return self.getAttribute('aria-valueText')

    @ariaValueText.setter
    def ariaValueText(self, value: str):
        return self.getAttribute('aria-valueText')

# class ElementInternals(object, AriaMixin):
#     def __init__(self, element):
#         self.element = element
#         self.shadowRoot = None # Returns the ShadowRoot object associated with this element.
#         self.form  # Returns the HTMLFormElement associated with this element.
#         self.states  # Returns the CustomStateSet associated with this element.
#         self.willValidate # A boolean value which returns true if the element is a submittable element that is a candidate for constraint validation.
#         self.validity  # Returns a ValidityState object which represents the different validity states the element can be in, with respect to constraint validation.
#         self.validationMessage  # A string containing the validation message of this element.
#         self.labels  # Returns a NodeList of all of the label elements associated with this element.


class CustomStateSet(object):

    def __init__(self):
        pass

    def add(self, state):
        pass

    def clear(self):
        pass

    def delete(self, state):
        pass

"""


class NodeList(list):
    """NodeList objects are collections of nodes"""

    @property
    def length(self) -> int:
        return len(self)

    def item(self, index) -> Node:
        """ Returns an item in the list by its index, or null if the index is out-of-bounds."""
        # An alternative to accessing nodeList[i] (which instead returns  undefined when i is out-of-bounds).
        # This is mostly useful for non-JavaScript DOM implementations.
        try:
            return self[index]
        except IndexError:
            return None

    # def items(self):
    #     """ Returns a list of the nodes in the list."""
    #     return self

    def entries(self) -> Iterable[Tuple[int, Node]]:
        """ Returns an iterator, allowing code to go through all key/value pairs contained in the collection.
        (In this case, the keys are numbers starting from 0 and the values are nodes."""
        # i.e.  Array [ 0, <p> ]
        for i in range(len(self)):
            yield i, self[i]

    def forEach(self, func, thisArg=None) -> None:
        """ Calls a function for each item in the NodeList."""
        # thisArg = thisArg or self
        for i in range(len(self)):
            func(self[i], i, self)

    def keys(self) -> Iterable[int]:
        """ Returns an iterator, allowing code to go through all the keys of the key/value pairs contained in the collection.
        (In this case, the keys are numbers starting from 0.)"""
        return iter(range(len(self)))

    def values(self) -> Iterable[Node]:
        """ Returns an iterator allowing code to go through all values (nodes) of the key/value pairs
        contained in the collection."""
        return iter(self)


class RadioNodeList(NodeList):
    # TODO - not tested

    def __init__(self, name: str):  # , owner: Element):
        self.name: str = name

    def __iter__(self):
        return iter(self.getElementsByName(self.name))

    def __getitem__(self, index):
        return self.getElementsByName(self.name)[index]

    def __len__(self) -> int:
        return len(self.getElementsByName(self.name))

    @property
    def value(self):
        """ Returns the value of the first element in the collection,
        or null if there are no elements in the collection. """
        return self[0].value if len(self) > 0 else None


class Element(Node):
    """ Baseclass for all html tags """

    # __slots__ = ('_id')

    def __init__(self, *args, **kwargs):
        # self.content = None
        # self.attributes = None
        if self.hasAttribute('id'):
            self.id = self.id  # ''#None

        self.lang = None
        self.tabIndex = None

        if self.hasAttribute('title'):
            self.title = self.title

        if self.hasAttribute('class'):
            self.className = self.className
            self.classList = self.classList

        # self.tagName
        self.style = None  # Style(self)  # = #'test'#Style()
        self.shadowRoot = None
        self.dir = None
        super().__init__(*args, **kwargs)

    def _getElementById(self, _id: str):
        # TODO - i think i need to build a hash map of IDs to positions on the tree
        # for now I'm going using recursion so this is a bit of a hack to do a few levels
        if self.getAttribute('id') == _id:
            return self
        try:
            for child in self.childNodes:
                if isinstance(child, str):
                    continue
                match = child._getElementById(_id)
                if match is not False and match is not None:
                    return match
        except Exception as e:
            print('fail', e)
            pass  # TODO - dont iterate strings.... ooof nasty. so thats why you never pass silently.
        return False

    def _getElementByAttrVal(self, attr: str, val: str):
        # TODO - i think i need to build a hash map of IDs to positions on the tree
        # for now I'm going using recursion so this is a bit of a hack to do a few levels
        if self.getAttribute(attr) == val:
            return self
        try:
            for child in self.childNodes:
                match = child._getElementByAttrVal(attr, val)
                if match:
                    return match
        except Exception as e:
            pass  # TODO - dont iterate strings
        return False

    def _matchElement(self, element, query):
        """
        tries to match an element based on the query
        at moment very basic. i.e. single level. just checks between id/tag/class
        """
        if not isinstance(element, Element):
            return False

        if query[0] == '#':
            if element.getAttribute('id') == query.split('#')[1]:
                return True

        if element.tagName.lower() == query.lower():
            return True

        if query[0] == '.':
            if query.split('.')[1] in element.classList:
                return True

        return False

    def matches(self, s: str) -> bool:
        """[checks to see if the Element would be selected by the provided selectorString]

        https://developer.mozilla.org/en-US/docs/Web/API/Element/matches

        Args:
            s (str): [css selector]

        Returns:
            [bool]: [True if selector maches Element otherwise False]
        """
        matches = self.ownerDocument.querySelectorAll(s)
        for match in matches:
            if match == self:
                return True
        return False

    # https://developer.mozilla.org/en-US/docs/Web/API/Element/closest
    def closest(self, s: str):
        el = self
        while el != None and el.nodeType == 1:  # TODO - nodeType
            if Element.matches(el, s):
                return el
            el = el.parentElement or el.parentNode
        return None

    # @staticmethod
    def getElementsBySelector(self, all_selectors, document):
        """
            Get DOM elements based on the given CSS Selector
            https://simonwillison.net/2003/Mar/25/getElementsBySelector/ < original author
            http://www.openjs.com/scripts/dom/css_selector/ < ported to support ','
            https://bin-co.com/python/scripts/getelementsbyselector-html-css-query.php < ported to py2 (broken/bugs) *BSD LICENSED*

            note - always needs a tag in the query
            i.e. ('a.classname') will work. but just ('.classname') wont

            fixed and ported to py3 here. quite cool means other peoples code works on my dom
            # TODO - needs to work in conjuctions with _matchElement so querySelector works a bit better and dQuery picks it up
            # TOOD - *= node content

        Args:
            all_selectors ([type]): [description]
            document ([type]): [description]

        Returns:
            [type]: [description]
        """
        selected = []
        # import string
        all_selectors = re.sub(r'\s*([^\w])\s*', r'\1', all_selectors)  # clean up whitespace
        # Grab all of the tagName elements within current context

        def getElements(context, tag):
            if (tag == ""):
                tag = '*'
            # Get elements matching tag, filter them for class selector
            found = []
            for con in context:
                elements = con.getElementsByTagName(tag)
                found.extend(elements)
            return found

        context = [document]
        inheriters = all_selectors.split(" ")

        # Space
        for element in inheriters:
            # This part is to make sure that it is not part of a CSS3 Selector
            left_bracket = str.find(element, "[")
            right_bracket = str.find(element, "]")
            pos = str.find(element, "#")  # ID
            if(pos + 1 and not(pos > left_bracket and pos < right_bracket)):
                parts = str.split(element, "#")
                tag = parts[0]
                id = parts[1]
                ele = document.getElementById(id)
                context = [ele]  # [](ele)
                continue

            pos = str.find(element, ".")  # Class
            if(pos + 1 and not(pos > left_bracket and pos < right_bracket)):
                parts = str.split(element, '.')
                tag = parts[0]
                class_name = parts[1]
                found = getElements(context, tag)
                # found = document.getElementsByClassName(class_name)
                context = []
                for fnd in found:
                    if(fnd.getAttribute("class") and re.search(r'(^|\s)' + class_name + '(\s|$)', fnd.getAttribute("class"))):
                        context.append(fnd)

                continue

            # If the char '[' appears, that means it needs CSS 3 parsing
            if(str.find(element, '[') + 1):
                # Code to deal with attribute selectors
                m = re.match(r'^(\w*)\[(\w+)([=~\|\^\$\*]?)=?[\'"]?([^\]\'"]*)[\'"]?\]$', element)
                if (m):
                    tag = m.group(1)
                    attr = m.group(2)
                    operator = m.group(3)
                    value = m.group(4)
                else:
                    return "NOPE"  # ?

                found = getElements(context, tag)
                context = []
                for fnd in found:
                    if(operator == '=' and fnd.getAttribute(attr) != value):
                        continue  # WORKING
                    if(operator == '~' and not(re.search(r'(^|\\s)' + value + '(\\s|$)', fnd.getAttribute(attr)))):
                        continue  # NOT WORKING?
                    if(operator == '|' and not(re.search(r'^' + value + '-?', fnd.getAttribute(attr)))):
                        continue
                    if(operator == '^' and str.find(fnd.getAttribute(attr), value) != 0):
                        continue  # WORKING
                    if(operator == '$' and str.rfind(fnd.getAttribute(attr), value) != (len(fnd.getAttribute(attr)) - len(value))):
                        continue  # kinda WORKING
                    if(operator == '*' and not(str.find(fnd.getAttribute(attr), value) + 1)):
                        continue  # WORKING
                    elif(not fnd.getAttribute(attr)):
                        continue
                    context.append(fnd)

                continue

            # Tag selectors - no class or id specified.
            found = getElements(context, element)
            context = found

        selected.extend(context)
        return selected

    def append(self, *args):
        """ Inserts a set of Node objects or DOMString objects after the last child of the Element. """
        self.args += (args)
        return self

    # elem.attachShadow({mode: open|closed})
    def attachShadow(self, obj):
        self.shadowRoot = ShadowRoot(self, obj['mode'])
        return self.shadowRoot

    # def accessKey( key: str ): -> None
        # ''' Sets or returns the accesskey attribute of an element'''
        # return
        # example
        # dom.getElementById("myAnchor").accessKey = "w";

    @property
    def attributes(self) -> NamedNodeMap:
        """ Returns a NamedNodeMap of an element's attributes """
        newargs: list = []
        for key, value in self.kwargs.items():
            newargs.append(Attr(key.lstrip('_'), value))
        nnm = NamedNodeMap(newargs, None, self)
        return nnm

    @property
    def innerHTML(self):
        """ Sets or returns the content of an element """
        return self.content

    @innerHTML.setter
    def innerHTML(self, value):
        if value is not None:
            # TODO - will need the parser to work for this to work properly. for now shove all on first content node
            self.args = (value,)
        return self.content

    @property
    def outerHTML(self):
        return self

    @outerHTML.setter
    def outerHTML(self, value):
        if isinstance(value, Element):
            self = value
        if isinstance(value, str):
            # self = value
            # TODO - parse
            # TODO - will need the parser to work for this to work properly
            pass
        return self

    def html(self, *args):
        self.args = args
        return self

    def blur(self):
        """ Removes focus from an element """
        pass

    @property
    def classList(self):
        """ Returns the value of the classList attribute of an element """
        cl = self.getAttribute('class')
        if cl is None:
            return []
        else:
            return cl.split(' ')

    @classList.setter
    def classList(self, newname: str):
        """ Sets or returns the value of the classList attribute of an element """
        self.setAttribute('class', newname)
        # raise NotImplementedError

    @property
    def className(self):
        """ Sets or returns the value of the className attribute of an element """
        return self.getAttribute('class')

    @className.setter
    def className(self, newname: str):
        """ Sets or returns the value of the className attribute of an element """
        self.setAttribute('class', newname)

    def click(self):
        """ Simulates a mouse-click on an element """
        # evt = MouseEvent('click', {'bubbles': True,'cancelable': True,'view': window});
        # TODO - don't if its cancelled
        evt = MouseEvent('click')
        return self.dispatchEvent(evt)

    @property
    def clientHeight(self):
        """ Returns the height of an element, including padding """
        return self.style.height + self.style.paddingTop + self.style.paddingBottom

    @property
    def clientLeft(self):
        """ Returns the width of the left border of an element """
        return self.style.left

    @property
    def clientTop(self):
        """ Returns the width of the top border of an element """
        return self.style.top

    @property
    def clientWidth(self):
        """ Returns the width of an element, including padding """
        return self.style.width + self.style.paddingLeft + self.style.paddingRight

    @property
    def contentEditable(self) -> bool:
        """ Sets or returns whether an element is editable """
        is_editable = self.getAttribute('contenteditable')
        return True if (is_editable == 'true' or is_editable == True) else False

    @contentEditable.setter
    def contentEditable(self, value: bool) -> None:
        self.setAttribute('contenteditable', value)

    @property
    def dataset(self):
        """ Returns the value of the dataset attribute of an element """
        # return self.getAttribute('data-*')  # TODO - copilot suggested a star. is that supposed to work?
        # loop all attributes and return the ones that start with data-
        # return {key: value for key, value in self.kwargs.items() if key.startswith('data-')}
        from domonic.utils import Utils

        dsmap = DOMStringMap()
        for key, value in self.kwargs.items():
            if key.startswith('data-'):
                # remove data from the key and change case to lower
                key = Utils.camel_case(key.replace('data-', ''))
                dsmap[key] = value
        return dsmap

    @property
    def dir(self):
        """ returns the value of the dir attribute of an element """
        return self.getAttribute('dir')

    @dir.setter
    def dir(self, direction: str = 'auto'):
        """ Sets the value of the dir attribute of an element """
        self.setAttribute('dir', direction)

    def exitFullscreen(self):
        """ Cancels an element in fullscreen mode """
        raise NotImplementedError

    def firstElementChild(self):
        """ Returns the first child element of an element """
        try:
            return self.args[0]
        except Exception:
            return None

    def focus(self):
        """ Sets focus on an element """
        raise NotImplementedError

    def setAttributeNodeNS(self, attr):  # TODO - test
        """ Sets the attribute node of an element """
        a = Attr(attr.name.lstrip('_'), attr.value)
        self.setAttributeNode(a)
        return self

    def getAttributeNodeNS(self, attr):  # TODO - test
        """ Sets the attribute node of an element """
        a = self.getAttribute(attr)
        if a is None:
            return None
        return Attr(attr, a)

    def setAttributeNS(self, namespaceURI, localName, value):
        """ Sets an attribute in the given namespace """
        self.setAttribute(localName, value)

    def getAttributeNS(self, namespaceURI, localName):
        """ Returns the value of the specified attribute """
        return self.getAttribute(localName)

    def removeAttributeNS(self, namespaceURI, localName):
        """ Removes an attribute from an element """
        if localName in self.attributes:
            self.removeAttribute(localName)
        # else:
        #     raise AttributeError
        return self

    def getAttribute(self, attribute: str) -> str:
        """ Returns the specified attribute value of an element node """
        try:
            if attribute[0:1] != '_':
                attribute = '_' + attribute
            return self.kwargs[attribute]
        except Exception as e:
            # print('attribute does not exist', e)  # TODO - something about this
            # print(e)
            return None

    def getAttributeNode(self, attribute: str) -> str:
        """ Returns the specified attribute node """
        try:
            return f"{attribute}={self.kwargs[attribute]}"  # TODO - Attr
        except Exception as e:
            # print('failed to get attribute')
            # print(e)
            return ''

    def getBoundingClientRect(self):
        """ Returns the size of an element and its position relative to the viewport """
        raise NotImplementedError

    def getElementsByClassName(self, className: str) -> 'HTMLCollection':
        """[Returns a collection of all child elements with the specified class name]

        Args:
            className (str): [a DOMString representing the class name to match]

        Returns:
            [type]: [a NodeList of all child elements with the specified class name]
        """
        # TODO - this will have to change as this i live and qsa aint.
        # return self.querySelectorAll('.' + className)
        return HTMLCollection(self.querySelectorAll('.' + className))

    def getElementsByTagName(self, tagName: str) -> 'HTMLCollection':
        """[Returns a collection of all child elements with the specified tag name

        Args:
            tagName (str): [a DOMString representing the tag name to match]

        Returns:
            [type]: [method returns a live HTMLCollection of elements with the given tag name.]
        """
        elements = HTMLCollection()

        def anon(el):
            if self._matchElement(el, tagName):
                elements.append(el)
        self._iterate(self, anon)
        return elements

    def hasAttribute(self, attribute: str) -> bool:
        """ Returns true if an element has the specified attribute, otherwise false """
        try:
            if attribute[0:1] != '_':
                attribute = '_' + attribute
            return attribute in self.kwargs.keys()
        except Exception as e:
            # print('failed to get attribute')
            # print(e)
            return False

    def hasAttributes(self) -> bool:
        """ Returns true if an element has any attributes, otherwise false """
        if len(self.kwargs) > 0:
            return True
        else:
            return False

    @property
    def id(self):
        """ Sets or returns the value of the id attribute of an element """
        return self.getAttribute('id')

    @id.setter
    def id(self, newid: str):
        """ Sets or returns the value of the id attribute of an element """
        self.setAttribute('id', newid)

    # Sets or returns the text content of a node and its descendants
    def innerText(self, *args):
        self.args = args
        return ''.join([each.__str__() for each in self.args])

    # Inserts an element adjacent to the current element
    def insertAdjacentElement(self, position: str, element):  # TODO - test. these look wrong.
        """ Inserts an element adjacent to the current element """
        position = position.upper()
        if position == 'BEFOREBEGIN':
            self.insertBefore(element, self.firstElementChild())
        elif position == 'AFTERBEGIN':
            self.insertBefore(element, self.firstElementChild())
        elif position == 'AFTEREND':
            self.insertAfter(element, self.firstElementChild())
        elif position == 'BEFOREEND':
            self.insertBefore(element, self.lastElementChild())

    def insertAdjacentHTML(self, position: str, html: str):
        """ Inserts raw HTML adjacent to the current element """
        # if position == 'beforebegin':
        #     self.insertAdjacentElement('beforebegin', html)
        # elif position == 'afterbegin':
        #     self.insertAdjacentElement('afterbegin', html)
        # elif position == 'beforeend':
        #     self.insertAdjacentElement('beforeend', html)
        # elif position == 'afterend':
        #     self.insertAdjacentElement('afterend', html)
        pass

    def insertAdjacentText(self, position: str, text: str):
        """ Inserts text adjacent to the current element """
        # if position == 'beforebegin':
        #     self.insertAdjacentElement('beforebegin', text)
        # elif position == 'afterbegin':
        #     self.insertAdjacentElement('afterbegin', text)
        # elif position == 'beforeend':
        #     self.insertAdjacentElement('beforeend', text)
        # elif position == 'afterend':
        #     self.insertAdjacentElement('afterend', text)
        pass

    def isContentEditable(self) -> bool:
        """Returns true if the content of an element is editable, otherwise false"""
        if self.getAttribute('contenteditable') == 'true':
            return True
        return False

    # def lang(self) -> str:
    #     """ Sets or returns the value of the lang attribute of an element """ # TODO - prop?
    #     return self.getAttribute('lang')

    def lastElementChild(self):
        """[Returns the last child element of an element]

        Returns:
            [type]: [the last child element of an element]
        """
        try:
            return self.args[len(self.args) - 1]
        except Exception:
            return None

    def namespaceURI(self):
        ''' Returns the namespace URI of an element'''
        pass

    @property
    def nextSibling(self):
        """ Returns the next node at the same node tree level """
        if self.parentNode is not None:
            for count, el in enumerate(self.parentNode.args):
                if el is self and count < len(self.parentNode.args) - 1:
                    return self.parentNode.args[count + 1]
        return None

    @property
    def nextElementSibling(self):
        """ Returns the next element at the same node tree level """
        if self.parentNode is not None:
            for count, el in enumerate(self.parentNode.args):
                if el is self and count < len(self.parentNode.args) - 1:
                    if type(self.parentNode.args[count + 1]) is not str:
                        return self.parentNode.args[count + 1]
        return None

    @property
    def previousElementSibling(self):
        """ returns the Element immediately prior to the specified one in its parent's children list,
        or None if the specified element is the first one in the list. """
        if self.parentNode is not None:
            for count, el in enumerate(self.parentNode.args):
                if el is self and count > 0:
                    if type(self.parentNode.args[count - 1]) is not str:
                        return self.parentNode.args[count - 1]
        return None

    def normalize(self):
        '''Joins adjacent text nodes and removes empty text nodes in an element'''
        content = []
        nodestr = ''
        for s in self.args:
            if type(s) == Text:
                # content.append(s.textContent)
                nodestr += s.textContent
                continue
            elif type(s) == str:
                nodestr += s
                continue
            elif nodestr != '':
                content.append(nodestr)
                nodestr = ''
            elif type(s) != str:
                content.append(s)
        if nodestr != '':
            content.append(nodestr)
        self.args = content
        return self.args

    def offsetHeight(self):
        ''' Returns the height of an element, including padding, border and scrollbar'''
        raise NotImplementedError

    def offsetWidth(self):
        ''' Returns the width of an element, including padding, border and scrollbar'''
        raise NotImplementedError

    def offsetLeft(self):
        ''' Returns the horizontal offset position of an element'''
        raise NotImplementedError

    def offsetParent(self):
        ''' Returns the offset container of an element'''
        raise NotImplementedError

    def offsetTop(self):
        ''' Returns the vertical offset position of an element'''
        raise NotImplementedError

    @property
    def parentElement(self):
        """ Returns the parent element node of an element """
        return self.parentNode

    # @property
    # def previousSibling(self):
    #     """ Returns the previous node at the same node tree level """
    #     if self.parentNode is not None:
    #         for count, el in enumerate(self.parentNode.args):
    #             if el is self and count > 1:
    #                 return self.parentNode.args[count - 1]
    #     return None

    def prepend(self, *args):
        """ Prepends a node to the current element """
        newargs = list(args) + list(self.args)
        self.args = tuple(newargs)

    def querySelector(self, query: str):
        """[Returns the first child element that matches a specified CSS selector(s) of an element]

        Args:
            query (str): [a CSS selector string]

        Returns:
            [type]: [an Element object]
        """
        try:
            return self.querySelectorAll(query)[0]
        except Exception as e:
            return None

    def querySelectorAll(self, query: str):
        """[Returns all child elements that matches a specified CSS selector(s) of an element]

        Args:
            query (str): [a CSS selector string]

        Returns:
            [type]: [a list of Element objects]
        """
        naked_query = query[1:]
        if '.' in naked_query or '[' in naked_query or ' ' in naked_query:
            return self.getElementsBySelector(query, self)
        elements = []
        def anon(el):
            if self._matchElement(el, query):
                elements.append(el)
        self._iterate(self, anon)
        return elements

    def remove(self):
        """ Removes the element from the DOM """
        # try:
        #     self.parentNode.args.remove(self)
        # except Exception:
        #     # print("Element not found")
        #     pass
        # if self.parentNode is None:
            # self._update_parents()
        if self.parentNode is not None:
            self.parentNode.removeChild(self)
        return self

    def removeAttribute(self, attribute: str):
        """ Removes a specified attribute from an element """
        try:
            if attribute[0:1] != '_':
                attribute = '_' + attribute
            del self.kwargs[attribute]
        except Exception as e:
            print('failed to remove!', e)
            pass

    def removeAttributeNode(self, attribute):  # untested
        """ Removes a specified attribute node, and returns the removed node """
        for each in self.kwargs:
            if attribute == each:
                val = self.kwargs[each]
                del self.kwargs[each]
                return Attr(attribute, val)

    def requestFullscreen(self):
        ''' Shows an element in fullscreen mode '''
        raise NotImplementedError

    # def setPointerCapture(self):
    #     ''' Sets the pointer capture to the specified element '''
    #     raise NotImplementedError

    # def releasePointerCapture(self):
    #     ''' Releases the pointer capture from the specified element '''
    #     raise NotImplementedError

    def scrollHeight(self):
        ''' Returns the entire height of an element, including padding '''
        raise NotImplementedError

    def scrollIntoView(self):
        '''Scrolls the specified element into the visible area of the browser window'''
        raise NotImplementedError

    def scrollLeft(self):
        ''' Sets or returns the number of pixels an element's content is scrolled horizontally'''
        raise NotImplementedError

    def scrollTop(self):
        ''' Sets or returns the number of pixels an element's content is scrolled vertically'''
        raise NotImplementedError

    def scrollWidth(self):
        ''' Returns the entire width of an element, including padding'''
        raise NotImplementedError

    def setAttribute(self, attribute, value):
        """ Sets or changes the specified attribute, to the specified value """
        try:
            if attribute[0:1] != '_':
                attribute = '_' + attribute
            self.kwargs[attribute] = value
        except Exception as e:
            # print('failed to set attribute', e)
            return None

    def setAttributeNode(self, attr):
        """[Sets or changes the specified attribute node]

        Args:
            attr ([type]): [an Attr object]
        """
        self.setAttribute(attr.name, attr.value)

    @property
    def style(self):
        """ returns the value of the style attribute of an element """
        if self.__style is None:
            self.style = Style()
        return self.__style

    @style.setter
    def style(self, style):
        self.__style = style
        self.__style.__init__(self)  # to set the parent

    # def tabIndex(self):
        # ''' Sets or returns the value of the tabindex attribute of an element'''
        # pass

    @property
    def tagName(self):
        return self.name

    # @property
    # def textContent(self):
    #     return self.nodeValue

    # @textContent.setter
    # def textContent(self, content):
    #     self.nodeValue = content

    @property
    def title(self):
        """ returns the value of the title attribute of an element """
        return self.getAttribute('title')

    @title.setter
    def title(self, newtitle: str):
        """[Sets the value of the title attribute of an element]

        Args:
            newtitle (str): [the new title value]
        """
        self.setAttribute('title', newtitle)

    def toString(self) -> str:
        """ Converts an element to a string """
        return str(self)


class DOMImplementation(object):

    def __init__(self):
        # self.__domImplementation = None
        pass

    def createDocument(self, namespaceURI: str, qualifiedName: str, doctype: str):
        if namespaceURI is None:
            namespaceURI = ''
        if qualifiedName is None:
            qualifiedName = ''
        if doctype is None:
            doctype = ''
        # d = Document()
        from domonic.html import html
        d = html()
        d.createElementNS(namespaceURI, qualifiedName)
        d.doctype = doctype
        return d

    def createDocumentType(self, qualifiedName: str, publicId: str, systemId: str) -> DocumentType:
        """[creates a DocumentType node]

        Args:
            qualifiedName (str): [the qualified name of the document type]
            publicId (str): [the public identifier of the document type]
            systemId (str): [the system identifier of the document type]

        Returns:
            [type]: [a DocumentType object]
        """
        return DocumentType(qualifiedName, publicId, systemId)

    def createHTMLDocument(self, title=None):
        # d = Document()
        # d.createElement('html')
        # d.createElement('head')
        # d.createElement('body')
        # d.title = title
        # return d
        pass

    def hasFeatures(self, featureList) -> bool:
        # return True
        pass


class ProcessingInstruction(Node):

    nodeType: int = Node.PROCESSING_INSTRUCTION_NODE
    __slots__ = ('target', 'data')

    def __init__(self, target, data) -> None:
        super().__init__()
        self.target = target
        self.data = data

    def toString(self) -> str:
        return f'<?{self.target} {self.data}?>'
    __str__ = toString

    # @property
    # def nodeType(self) -> int:
    #     return Node.PROCESSING_INSTRUCTION_NODE


class Comment(Node):

    nodeType: int = Node.COMMENT_NODE
    __slots__ = ('data')

    def __init__(self, data) -> None:
        self.data = data
        super().__init__()

    def toString(self) -> str:
        return f'<!--{self.data}-->'
    __str__ = toString

    # @property
    # def nodeType(self) -> int:
    #     return Node.COMMENT_NODE


class CDATASection(Node):

    nodeType: int = Node.CDATA_SECTION_NODE
    __slots__ = ('data')

    def __init__(self, data) -> None:
        self.data = data

    def toString(self) -> str:
        return f'<![CDATA[{self.data}]]>'
    __str__ = toString

    # @property
    # def nodeType(self) -> int:
    #     return Node.CDATA_SECTION_NODE


class AbastractRange(object):

    def __init__(self):
        raise NotImplementedError

    def cloneContents(self):
        raise NotImplementedError

    def cloneRange(self):
        raise NotImplementedError

    def compareBoundaryPoints(self, how, sourceRange):
        raise NotImplementedError

    def createContextualFragment(self, data):
        raise NotImplementedError

    def deleteContents(self):
        raise NotImplementedError

    def detach(self):
        raise NotImplementedError

    def expand(self, unit):
        raise NotImplementedError

    def extractContents(self):
        raise NotImplementedError

    def getBoundingClientRect(self):
        raise NotImplementedError

    def getClientRects(self):
        raise NotImplementedError

    def insertNode(self, newNode):
        raise NotImplementedError

    def selectNode(self, refNode):
        raise NotImplementedError

    def selectNodeContents(self, refNode):
        raise NotImplementedError

    def setEnd(self, refNode, offset):
        raise NotImplementedError

    def setEndAfter(self, refNode):
        raise NotImplementedError

    def setEndBefore(self, refNode):
        raise NotImplementedError

    def setStart(self, refNode, offset):
        raise NotImplementedError

    def setStartAfter(self, refNode):
        raise NotImplementedError

    def setStartBefore(self, refNode):
        raise NotImplementedError

    def surroundContents(self, newParent):
        raise NotImplementedError

    def toString(self) -> str:
        raise NotImplementedError

    def comparePoint(self, refNode, offset):
        raise NotImplementedError

    def deleteData(self, offset, count):
        raise NotImplementedError

    def extractData(self, offset, count):
        raise NotImplementedError

    def getData(self, offset, count):
        raise NotImplementedError

    def getEnd(self):
        raise NotImplementedError

    def getStart(self):
        raise NotImplementedError

    def replaceData(self, offset, count, data):
        raise NotImplementedError

    def setData(self, data):
        raise NotImplementedError


class Range(AbastractRange):
    # TODO - untested

    def __init__(self):
        self.startContainer = None
        self.startOffset = None
        self.endContainer = None
        self.endOffset = None
        self.collapsed = None
        self.commonAncestorContainer = None

    def setStart(self, node, offset):
        self.startContainer = node
        self.startOffset = offset
        self.collapsed = False
        self.commonAncestorContainer = node

    def setEnd(self, node, offset):
        self.endContainer = node
        self.endOffset = offset
        self.collapsed = False
        self.commonAncestorContainer = node

    def setStartBefore(self, node):
        self.setStart(node.parentNode, node.index)

    def setStartAfter(self, node):
        self.setStart(node.parentNode, node.index + 1)

    def setEndBefore(self, node):
        self.setEnd(node.parentNode, node.index)

    def setEndAfter(self, node):
        self.setEnd(node.parentNode, node.index + 1)

    def collapse(self, toStart):
        if toStart:
            self.endContainer = self.startContainer
            self.endOffset = self.startOffset
        else:
            self.startContainer = self.endContainer
            self.startOffset = self.endOffset
        self.collapsed = True

    def selectNode(self, node):
        self.setStartBefore(node)
        self.setEndAfter(node)

    def selectNodeContents(self, node):
        self.setStart(node, 0)
        self.setEnd(node, len(node.childNodes))

    def compareBoundaryPoints(self, how, sourceRange):
        if how == 0:
            return self.startContainer == sourceRange.startContainer and self.startOffset == sourceRange.startOffset
        elif how == 2:
            return self.endContainer == sourceRange.endContainer and self.endOffset == sourceRange.endOffset
        else:
            raise NotImplementedError

    def deleteContents(self):
        raise NotImplementedError

    def extractContents(self):
        raise NotImplementedError

    def cloneContents(self):
        raise NotImplementedError

    def insertNode(self, node):
        raise NotImplementedError

    def surroundContents(self, newParent):
        raise NotImplementedError

    def cloneRange(self):
        raise NotImplementedError

    def detach(self):
        raise NotImplementedError

    def createContextualFragment(self, fragment):
        raise NotImplementedError

    def toString(self) -> str:
        raise NotImplementedError


class StaticRange(AbastractRange):

    def __init__(self, startContainer, startOffset, endContainer, endOffset):
        self.startContainer = startContainer
        self.startOffset = startOffset
        self.endContainer = endContainer
        self.endOffset = endOffset
        self.collapsed = False
        self.commonAncestorContainer = None

    # def toRange(self):
    #     return self


class TimeRanges(object):

    def __init__(self):
        self.length = 0

    def start(self, index):
        raise NotImplementedError

    def end(self, index):
        raise NotImplementedError


class XPathExpression(object):

    def __init__(self, expression, nsResolver):
        self.expression = expression
        self.nsResolver = nsResolver

    def evaluate(self, contextNode, type, inResult):
        raise NotImplementedError

# class XPathResult(object):

#     def __init__(self, resultType, snapshotLength):
#         self.resultType = resultType
#         self.snapshotLength = snapshotLength

#     def iter(self):
#         raise NotImplementedError

#     def snapshotItem(self, index):
#         raise NotImplementedError


class XPathEvaluator(object):

    def createExpression(self, expression, nsResolver):
        raise NotImplementedError

    def createNSResolver(self, nodeResolver):
        raise NotImplementedError

    def evaluate(self, expression, contextNode, nsResolver, type, inResult):
        raise NotImplementedError


class Document(Element):
    """The Document interface represents the entire HTML or XML document."""

    URL = None

    def __init__(self, *args, **kwargs):
        """ Constructor for Document objects """
        self.args = args
        self.kwargs = kwargs
        # self.documentURI = uri
        # self.documentElement = self
        self.stylesheets = None
        self.doctype = None
        super().__init__(*args, **kwargs)
        try:
            global document
            document = self
        except Exception as e:
            print('failed to set document', e)

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.__init__(*args, **kwargs)
        instance.documentElement = instance
        instance.URL = URL().href  # ? this might be old code TODO
        instance.baseURI = URL().href  # ? this might be old code TODO
        try:
            global document
            document = instance
        except Exception as e:
            print('failed to set document', e)
        return instance

    # TODO - still not great as it also returns 'links' when searching for 'li'
    # @property
    def _get_tags(self, tag):  # TODO - still old
        ''' returns the tags you want '''
        reg = f"(<{tag}.*?>.+?</{tag}>)"

        closed_tags = ["base", "link", "meta", "hr", "br", "wbr", "img",
                       "embed", "param", "source", "track", "area", "col", "input", "keygen", "command"]
        if tag in closed_tags:
            reg = f"(<{tag}.*?/>)"

        pattern = re.compile(reg)
        tags = re.findall(pattern, str(self))
        return tags

    # def activeElement():
        ''' Returns the currently focused element in the document'''
        # return

    # def adoptNode(self, node):
    #     """ Adopts a node from another document """
    #     if node.ownerDocument is not None:
    #         node.ownerDocument.removeChild(node)
    #     node.ownerDocument = self
    #     return node

    @property
    def stylesheets(self):
        if self.__stylesheets is None:
            self.stylesheets = StyleSheetList()
            self.stylesheets._populate_stylesheets_from_document(self)
        return self.__stylesheets

    @stylesheets.setter
    def stylesheets(self, stylesheets):
        self.__stylesheets = stylesheets
        # self.__stylesheets.__init__(self)  # to set the parent??

    @property
    def anchors(self):
        """[get the anchors in the document]"""
        # only the ones with a name
        tags = self.querySelectorAll('a')
        tags = [tag for tag in tags if tag.hasAttribute('name')]
        return tags

    @property
    def applets(self):
        """Returns a collection of all <applet> elements in the document"""
        return self.querySelectorAll('applet')

    @property
    def body(self):
        """Returns the <body> element in the document"""
        return self.querySelector('body')

    @body.setter
    def body(self, el):
        """Sets the <body> element in the document"""
        if not isinstance(el, HTMLBodyElement):
            raise DOMException(
                DOMException.TYPE_MISMATCH_ERR,
                "The new body element is of type '" + str(type(el)) + "'. It must be a 'HTMLBodyElement'"
            )
        else:
            if self.body is not None:
                self.body.remove()
            self += el

    # def close():
        """ Closes the output stream previously opened with document.open() """
        # return

    # def cookie():
        """ Returns all name/value pairs of cookies in the document """
        # return

    @property
    def charset(self):
        """ Returns the character encoding for the document. Deprecated: Use characterSet instead. """
        return "UTF-8"

    @property
    def characterSet(self):
        """ Returns the character encoding for the document """
        return "UTF-8"

    @staticmethod
    def createAttribute(name):
        """ Creates an attribute node """
        return Attr(name)

    @staticmethod
    def createComment(message):
        """ Creates a Comment node with the specified text """
        return Comment(message)

    @staticmethod
    def createDocumentFragment(*args):
        """ Creates an empty DocumentFragment node if not content passed. I added args as optional to pass content """
        return DocumentFragment(*args)

    @staticmethod
    def createExpression(xpath, nsResolver):
        """ Creates an XPathExpression object for the given XPath string. """
        return XPathExpression(xpath, nsResolver)

    @staticmethod
    def createElement(_type: str, *args, **kwargs):
        """ Creates an Element node """
        from domonic.html import create_element
        return create_element(_type, *args, **kwargs)

    @staticmethod
    def createElementNS(namespaceURI, qualifiedName, options=None):
        """ Creates an element with the specified namespace URI and qualified name."""
        el = type(qualifiedName, (Element,), {'name': qualifiedName})
        el.namespaceURI = namespaceURI
        return el()

    @staticmethod
    def createEvent(event_type=None):
        """[Creates a new event]

        Args:
            event_type ([type], optional): [description]. Defaults to None.

        Returns:
            [type]: [a new event]
        """
        if event_type == "MouseEvent":
            return MouseEvent()
        elif event_type == "KeyboardEvent":
            return MouseEvent()
        elif event_type is None:
            return Event()
        return Event()

    @staticmethod
    def createTextNode(text):
        """[Creates a Text node with the specified text.

        Args:
            text ([str]): [the text to be inserted]

        Returns:
            [type]: [a new Text node]
        """
        return Text(text)

    @staticmethod
    def createTreeWalker(root, whatToShow=None, filter=None, entityReferenceExpansion=None):
        """[creates a TreeWalker object]

        Args:
            root ([type]): [the root node at which to begin traversal]
            whatToShow ([type], optional): [what types of nodes to show]. Defaults to None.
            filter ([type], optional): [a NodeFilter or a function to be called for each node]. Defaults to None.

        Returns:
            [type]: [a new TreeWalker object]
        """
        whatToShow = NodeFilter.SHOW_ALL if whatToShow == None else whatToShow
        return TreeWalker(root, whatToShow, filter, entityReferenceExpansion)

    @staticmethod
    def createProcessingInstruction(target, data):
        """ Creates a ProcessingInstruction node with the specified target and data """
        return ProcessingInstruction(target, data)

    @staticmethod
    def createEntityReference(name):
        """ Creates an EntityReference node with the specified name """
        return EntityReference(name)

    @property
    def xmlversion(self):
        """ Returns the version of XML used for the document """
        return "1.0"

    # @property
    # def currentScript(self):
    #     """ Returns the currently executing script or null if none is executing """
    #     return self.querySelector('script')

    @staticmethod
    def createCDATASection(data):
        """ Creates a CDATASection node with the specified data """
        return CDATASection(data)

    # @staticmethod
    # def createAttributeNS(namespaceURI, qualifiedName):
    #     """ Creates an Attr node with the specified namespace URI and qualified name """
    #     return Attr(qualifiedName)

    @staticmethod
    def createRange():
        """ Creates a Range """
        return Range()

    @staticmethod
    def createNodeIterator(root, whatToShow=None, filter=None):
        """Creates a NodeIterator that can be used to traverse the document tree or subtree under root.
        """
        whatToShow = NodeFilter.SHOW_ALL if whatToShow == None else whatToShow
        return NodeIterator(root, whatToShow, filter)

    # @staticmethod
    # def caretRangeFromPoint(x, y):
        # """ Returns the Range object that is the caret selection at the given coordinates. """
        # return Range()
        # raise NotImplementedError

    # @staticmethod
    # def createNSResolver(nodeResolver):
    #     """ Creates a NodeResolver """
    #     return NodeResolver(nodeResolver)

    # def defaultView(self):
        # """ Returns the window object associated with a document, or null if none is available. """
        # return

    # def designMode(self):
        ''' Controls whether the entire document should be editable or not.'''
        # return

    @property
    def doctype(self):
        ''' Returns the Document Type Declaration associated with the document'''
        return "<!DOCTYPE html>"
        # return self.doctype = value

    @doctype.setter
    def doctype(self, value):
        ''' Sets the Document Type Declaration associated with the document'''
        self._doctype = value
        return

    # def documentElement(self):
        # ''' Returns the Document Element of the document (the <html> element)'''
        # return self

    # def documentMode(self):
        ''' Returns the mode used by the browser to render the document'''
        # return

    def domain(self):
        ''' Returns the domain name of the server that loaded the document'''
        return

    # def domConfig(self):
        '''Obsolete. Returns the DOM configuration of the document'''
        # return

    def elementFromPoint(self, x, y):
        """ Returns the topmost element at the specified coordinates. """
        raise NotImplementedError

    def elementsFromPoint(self, x, y):
        """ Returns an array of all elements at the specified coordinates. """
        raise NotImplementedError

    @property
    def embeds(self):
        """[Returns a collection of all <embed> elements the document]

        Returns:
            [type]: [a collection of all <embed> elements the document]
        """
        return self.querySelectorAll('embed')

    # def execCommand(self):
        '''Invokes the specified clipboard operation on the element currently having focus.'''
        # return

    @property
    def forms(self):
        ''' Returns a collection of all <form> elements in the document'''
        return self.querySelectorAll('form')

    def fullscreenElement(self):
        ''' Returns the current element that is displayed in fullscreen mode'''
        return None

    def fullscreenEnabled(self):
        '''Returns a Boolean value indicating whether the document can be viewed in fullscreen mode'''
        return False

    def getElementById(self, _id):
        """[Returns the element that has the ID attribute with the specified value]

        Args:
            _id ([str]): [the value of the ID attribute]

        Returns:
            [type]: [the element that has the ID attribute with the specified value]
        """
        for each in self.childNodes:
            if each.getAttribute('id') == _id:
                return each
            try:
                for child in each.childNodes:
                    if isinstance(child, str):
                        continue
                    match = child._getElementById(_id)
                    # TODO - i think i need to build a hash map of IDs to positions on the tree
                    # for now I'm going to use recursion and add this same method to Element
                    if match is not False and match is not None:
                        return match
            except Exception as e:
                pass  # TODO - dont iterate strings

        return False

    def getElementsByName(self, name: str):
        """[Returns a NodeList containing all elements with a specified name]

        Args:
            name (str): [the name to search for]

        Returns:
            [type]: [the matching elements]
        """
        for each in self.childNodes:
            if each.getAttribute('name') == name:
                return each
            try:
                for child in each.childNodes:
                    match = child._getElementByAttrVal('name', name)
                    if match:
                        return match
            except Exception as e:
                pass
        return False

    # def hasFocus():
        # '''Returns a Boolean value indicating whether the document has focus'''
        # return

    @property
    def head(self) -> 'HTMLHeadElement':
        """Returns the <head> element of the document"""
        return self.querySelector('head')

    @head.setter
    def head(self, el: 'HTMLHeadElement') -> None:
        """[Sets the <head> element of the document]

        Args:
            el ([HTMLHeadElement]): [the new <head> element]

        Raises:
            DOMException: [if the el is not an HTMLHeadElement]
        """
        if not isinstance(el, HTMLHeadElement):
            raise DOMException('el must be an HTMLHeadElement')
        self.removeChild(self.head)
        if self.firstChild:
            self.insertBefore(el, self.firstChild)
        else:
            self.appendChild(el)

    @property
    def images(self):
        """ Returns a collection of all <img> elements in the document """
        return self.querySelectorAll('img')

    @property
    def implementation(self):
        """ Returns the DOMImplementation object that handles this document """
        return DOMImplementation()

    def importNode(self, node, deep=False):
        """ Imports a node from another document to this document. """
        if isinstance(node, Element):
            node = node.copy()
            node.ownerDocument = self
            return node
        elif isinstance(node, Comment):
            return Comment(node.data)
        elif isinstance(node, Text):
            return Text(node.data)
        elif isinstance(node, ProcessingInstruction):
            return ProcessingInstruction(node.target, node.data)
        elif isinstance(node, DocumentFragment):
            return DocumentFragment()
        elif isinstance(node, Attr):
            return Attr(node.name, node.value)
        else:
            raise Exception("Unsupported node type")

    # def inputEncoding(self):
    #     """ Returns the encoding used to access the document's resources."""
    #     return

    # def lastModified():
        # ''' Returns the date and time the document was last modified'''
        # return

    @property
    def links(self):
        """Returns a collection of all <a> and <area> elements in the document that have a href attribute"""
        return self.querySelectorAll('a')

    # @property
    # def nodeType(self):
    #     return Node.DOCUMENT_NODE
    nodeType: int = Node.DOCUMENT_NODE

    def normalizeDocument(self):  # TODO - test
        """ Removes empty Text nodes, and joins adjacent nodes """
        for each in self.childNodes:
            if each.nodeType == Node.TEXT_NODE:
                if each.nodeValue.strip() == '':
                    each.parentNode.removeChild(each)
                else:
                    each.normalize()
            else:
                each.normalize()
        return

    # def open(self):
        # '''Opens an HTML output stream to collect output from document.write()'''
        # return

    # def readyState(self):
        # ''' Returns the (loading) status of the document'''
        # return

    # def referrer():
        # ''' Returns the URL of the document that loaded the current document'''
        # return

    def renameNode(self, node, namespaceURI :str, nodename: str):
        """[Renames the specified node, and returns the renamed node.]

        Args:
            node ([type]): [the node to rename]
            namespaceURI ([type]): [a namespace URI]
            nodename ([type]): [a node name]

        Returns:
            [type]: [description]
        """
        if node.nodeType == Node.ELEMENT_NODE:
            node.nodeName = nodename
            node.namespaceURI = namespaceURI
            return node
        else:
            return False

    # def requestStorageAccess(self, storage_access_callback):
    #     """ Requests permission to access the user's storage area """
    #     return False

    # def hasStorageAccess(self):
    #     """ Returns whether the user has granted permission to access the user's storage area """
    #     return False

    # @property
    # def pictureInPictureElement(self):
    #     """ Returns the element currently in Picture-in-Picture mode, if any. """
    #     return None

    # def exitPictureInPicture(self):
    #     """ Exits Picture-in-Picture mode, if any. """
    #     return False

    @property
    def pictureInPictureEnabled(self):
        """ Returns whether Picture-in-Picture mode is enabled. """
        return False

    @property
    def scripts(self):
        """[Returns a collection of <script> elements in the document]

        Returns:
            [type]: [a collection of <script> elements in the document]
        """
        return self.querySelectorAll('script')

    def strictErrorChecking(self):
        ''' Returns a Boolean value indicating whether to stop on the first error'''
        return False

    @property
    def title(self) -> str:
        """[gets the title of the document]

        Returns:
            [str]: The title of the document
        """
        if self.querySelector('title'):
            return self.querySelector('title').textContent
        return ''

    @title.setter
    def title(self, value: str):
        """[Sets the title of the document]

        Args:
            value ([str]): [the new title of the document]
        """
        if self.querySelector('title'):
            self.querySelector('title').textContent = value
        else:
            if not self.head:
                self.head = HTMLHeadElement()
            self.head.appendChild(HTMLTitleElement(value))

    @property
    def visibilityState(self):
        """ Returns the visibility state of the document """
        return 'visible'

    def write(self, html: str = ""):  # -> None: # TODO - untested
        """[writes HTML text to a document

        Args:
            html (str, optional): [the content to write to the document]
        """
        content = DocumentFragment(html)
        self.__init__(content)

    def writeln(self, html: str = ""):  # -> None: # TODO - untested
        """[writes HTML text to a document, followed by a line break]

        Args:
            html (str, optional): [the content to write to the document]
        """
        self.write(html + '\n')

    # def __md__(self)
    # def __rst__(self)
    # def __json__(self)


class Location():
    # TODO - move this to the window class and remove all domonic.javascript refs in this file

    def __init__(self, url: str = None, *args, **kwargs) -> None:
        self.href = url

    def __str__(self) -> str:
        return self.href

    # def __repr__(self):
    #     return self.uri

    def origin(self):  # TODO - test
        """ Returns the protocol, hostname and port number of a URL """
        # from domonic.javascript import URL
        from domonic.webapi.url import URL
        return URL(self.href).origin

    def search(self):  # TODO - test
        """ Sets or returns the querystring part of a URL """
        from domonic.webapi.url import URL
        return URL(self.href).search

    def assign(self, url: str = "") -> None:
        """ Loads a new document """
        # TODO - if different download?
        # dom.baseURI = url
        pass

    def reload(self):
        """Reloads the current document """
        raise NotImplementedError

    def replace(self):
        """Replaces the current document with a new one """
        raise NotImplementedError


location = Location


class DocumentFragment(Node):

    def __init__(self, *args) -> None:
        self.args: list = args

    querySelector = Document.querySelector
    querySelectorAll = Document.querySelectorAll
    getElementById = Document.getElementById
    getElementsByTagName = Document.getElementsByTagName
    _matchElement = Document._matchElement
    attributes = Element.attributes

    def replaceChildren(self, newChildren) -> None:
        """ Replaces the childNodes of the DocumentFragment object. """
        self.content.replaceChild(newChildren)

    # @property
    # def nodeType(self) -> int:
    #     return Node.DOCUMENT_FRAGMENT_NODE
    nodeType: int = Node.DOCUMENT_FRAGMENT_NODE

    def __str__(self) -> str:
        return ''.join([str(a) for a in self.args])


class CharacterData(Node):
    """
    The CharacterData abstract interface represents a Node object that contains characters.
    This is an abstract interface, meaning there aren't any objects of type CharacterData:
    it is implemented by other interfaces like Text, Comment, or ProcessingInstruction, which aren't abstract.
    """

    nextElementSibling = Element.nextElementSibling
    previousElementSibling = Element.previousElementSibling

    remove = ChildNode.remove
    replaceWith = ChildNode.replaceWith
    before = ChildNode.before
    after = ChildNode.after

    def appendData(self, data):
        """ Appends the given DOMString to the CharacterData.data string; when this method returns,
        data contains the concatenated DOMString. """
        self.args[0] += data
        return self.args[0]

    def deleteData(self, offset: int, count: int):
        """ Removes the specified amount of characters, starting at the specified offset,
        from the CharacterData.data string; when this method returns, data contains the shortened DOMString. """
        self.args[0] = self.args[0][:offset] + self.args[0][offset + count:]
        return self.args[0]

    def insertData(self, offset: int, data):
        """ Inserts the specified characters, at the specified offset, in the CharacterData.data string;
        when this method returns, data contains the modified DOMString. """
        self.args[0] = self.args[0][:offset] + data + self.args[0][offset:]
        return self.args[0]

    def replaceData(self, offset: int, count: int, data):
        """ Replaces the specified amount of characters, starting at the specified offset, with the specified DOMString;
        when this method returns, data contains the modified DOMString. """
        self.args[0] = self.args[0][:offset] + data + self.args[0][offset + count:]
        return self.args[0]

    # def replaceWith(self, newChildren):
    #     """ Replaces the characters in the children list of its parent with a set of Node or DOMString objects. """
    #     self.replaceChildren(newChildren) # parentNode?

    def substringData(self, offset: int, length: int):
        """ Returns a DOMString containing the part of CharacterData.data of the specified length and
        starting at the specified offset. """
        self.args[0] = self.args[0][offset:offset + length]
        return self.args[0]


class EntityReference(Node):
    """
    The EntityReference interface represents a reference to an entity, either parsed
    or unparsed, in an Entity Node. Note that this is not a CharacterData node,
    and does not have any child nodes.
    """

    def __init__(self, *args) -> None:
        self.args = args

    def __str__(self) -> str:
        return ''.join([str(a) for a in self.args])

    @staticmethod
    def ordinal(entityName: str):
        """ Returns the character corresponding to the given entity name. """
        return ord(entityName)  # TODO - test. would this work?

    @staticmethod
    def fromOrdinal(ordinal: int):
        """ Returns the entity name corresponding to the given character. """
        return chr(ordinal)


class Entity(Node):

    def __init__(self, *args) -> None:
        self.args = args

    def __str__(self) -> str:
        return ''.join([str(a) for a in self.args])

    @staticmethod
    def fromName(entityName: str) -> str:
        """ Returns the entity name corresponding to the given character. """
        return chr(ord(entityName))

    @staticmethod
    def fromChar(char: str) -> str:
        """ Returns the character corresponding to the given entity name. """
        return ord(char)


# class Notation(Node):

#     def __init__(self, *args):
#         self.args = args

#     def __str__(self):
#         return ''.join([str(a) for a in self.args])

#     def getPublicId(self):
#         """ Returns the public identifier of the notation. """
#         return self.args[0]

#     def getSystemId(self):
#         """ Returns the system identifier of the notation. """
#         return self.args[1]


class Text(CharacterData):
    """ Text Node """

    @property
    def wholeText(self):
        """ Returns a DOMString containing all the text content of the node and its descendants. """
        return self.args[0]

    def splitText(self, offset: int):
        """ Splits the Text node into two Text nodes at the specified offset, keeping both in the tree as siblings.
        The first node is returned, while the second node is discarded and exists outside the tree. """
        text = self.args[0][:offset]
        self.args[0] = self.args[0][offset:]
        return text

    @property
    def assignedSlot(self):
        """ Returns the slot whose assignedNodes contains this node. """
        return self.parentNode.assignedSlot

    @property
    def data(self):
        return self.args[0]

    @data.setter
    def data(self, data):
        self.args = (data,)
        return self.args[0]

    nodeType: int = Node.TEXT_NODE

    @property
    def nodeName(self):
        return '#text'

    @property
    def childNodes(self):
        return 0

    @property  # TODO - is this correct?
    def firstChild(self):
        return None  # ?
        # https://www.w3.org/TR/2000/CR-DOM-Level-2-20000510/core.html
        # lvl 2 spec has nochildren on bunch of NodeTypes. might mean overrides required
        #  to null certain behaviours. i.e. treewalker is having issues here.
        # TODO - test what it does in the browser. then fix up all required nochildren nodes i.e. comment, doctype, etc.

    # @property
    # def firstChild(self):
    #     return self.args[0]

    # @property
    # def textContent(self):
    #     return self.nodeValue

    # @textContent.setter
    # def textContent(self, content):
    #     self.nodeValue = content

    def __str__(self) -> str:
        return str(self.textContent)

    # def __repr__(self):
        # return str(self.textContent)

    def __iter__(self):
        yield self


class HTMLCollection(list):

    def __str__(self) -> str:
        return ''.join([str(a) for a in self])

    def item(self, index: int):
        """[gets the indexth item in the collection.
        If index is greater than or equal to the number of nodes in the list, this returns null.]

        Args:
            index ([type]): [the index of the item to return.]

        Returns:
            [type]: [the node at the indexth position, or None]
        """
        if index < len(self):
            return self[index]
        else:
            return None

    def namedItem(self, name: str):
        """Returns the specific node whose ID or, as a fallback, name matches the string specified by name."""
        for item in self:
            if item.id == name:
                return item
            elif item.name == name:
                return item
        return None

    def __getitem__(self, index):
        # can return dot notation i.e
        # index = "named.item.with.periods" # TODO - test
        if isinstance(index, str):
            names = index.split(".")
            if len(names) > 1:
                return self.namedItem(names[0]).namedItem(".".join(names[1:]))
            else:
                return self.namedItem(index)
        else:
            return super().__getitem__(index)


# TODO - is there a webapi module for this now?
# from domonic.javascript import Object
# MutationObserverInit = Object()
# MutationObserverInit.subtree = False
# MutationObserverInit.childList = False
# MutationObserverInit.attributes = False
# MutationObserverInit.attributeFilter = False
# MutationObserverInit.attributeOldValue = False
# MutationObserverInit.characterData = False
# MutationObserverInit.characterDataOldValue = False

# class MutationObserver(): # TODO - test
#     """ The MutationObserver interface provides the ability to watch for changes being made to the DOM tree. """

#     def __init__(self, callback, opts=MutationObserverInit):
#         self.callback = callback
#         self.mutations = []
#         self.observer = None
#         self.is_connected = False

#     def disconnect(self):
#         """ Stops the MutationObserver instance from receiving further notifications until
#         and unless observe() is called again. """
#         self.is_connected = False
#         self.observer = None
#         self.mutations = []
#         self.callback = None
#         return self

#     def observe(self, target, options):
#         """ Configures the MutationObserver to begin receiving notifications through
#         its callback function when DOM changes matching the given options occur. """
#         if self.is_connected:
#             self.disconnect()
#         self.observer = target.ownerDocument.createNodeObserver(self.mutations.append, True)
#         self.is_connected = True

#     def takeRecords(self):
#         """ Removes all pending notifications from the MutationObserver's notification queue
#         and returns them in a new Array of MutationRecord objects. """
#         return []


# ResizeObserver
# IntersectionObserver
# PerformanceObserver


class DOMException(Exception):
    """ The DOMException interface represents an anormal event related to the DOM. """

    INDEX_SIZE_ERR: int = 1
    DOMSTRING_SIZE_ERR: int = 2
    HIERARCHY_REQUEST_ERR: int = 3
    WRONG_DOCUMENT_ERR: int = 4
    INVALID_CHARACTER_ERR: int = 5
    NO_DATA_ALLOWED_ERR: int = 6
    NO_MODIFICATION_ALLOWED_ERR: int = 7
    NOT_FOUND_ERR: int = 8
    NOT_SUPPORTED_ERR: int = 9
    INUSE_ATTRIBUTE_ERR: int = 10
    INVALID_STATE_ERR: int = 11
    SYNTAX_ERR: int = 12
    INVALID_MODIFICATION_ERR: int = 13
    NAMESPACE_ERR: int = 14
    INVALID_ACCESS_ERR: int = 15
    VALIDATION_ERR: int = 16
    TYPE_MISMATCH_ERR: int = 17
    SECURITY_ERR: int = 18
    NETWORK_ERR: int = 19
    ABORT_ERR: int = 20
    URL_MISMATCH_ERR: int = 21
    QUOTA_EXCEEDED_ERR: int = 22
    TIMEOUT_ERR: int = 23
    INVALID_NODE_TYPE_ERR: int = 24
    DATA_CLONE_ERR: int = 25

    def __init__(self, code, message: Optional[str] = None) -> None:
        self.code = code
        self.message: str = message
        self.name = "DOMException"

    def __str__(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return self.message


class DOMTimeStamp(int):
    """ The DOMTimeStamp interface represents a numeric value which represents the
    number of milliseconds since the epoch. """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)


class DOMPoint(vec3):
    """ The DOMPoint interface represents a point specified by x and y coordinates. """

    @staticmethod
    def fromPoint(point) -> 'DOMPoint':
        return DOMPoint(point.x, point.y, point.z, point.w)

    def __init__(self, x: float, y: float, z: float = 0, w: float = 1) -> None:
        self.x: float = x
        self.y: float = y
        self.z: float = z
        self.w: float = w
        super().__init__(x, y, z, w)

    def __str__(self) -> str:
        return '({}, {}, {}, {})'.format(self.x, self.y, self.z, self.w)

    def __repr__(self):
        return '({}, {}, {}, {})'.format(self.x, self.y, self.z, self.w)


class DOMPointReadOnly(DOMPoint):
    """ The DOMPointReadOnly interface represents a point specified by x and y coordinates. """

    @staticmethod
    def fromPoint(point) -> 'DOMPointReadOnly':
        return DOMPointReadOnly(point.x, point.y, point.z, point.w)

    def __init__(self, x: float, y: float, z: float = 0, w: float = 1) -> None:
        self.x: float = x
        self.y: float = y
        self.z: float = z
        self.w: float = w
        super().__init__(x, y, z, w)

    def __str__(self) -> str:
        return '({}, {}, {}, {})'.format(self.x, self.y, self.z, self.w)

    def __repr__(self):
        return '({}, {}, {}, {})'.format(self.x, self.y, self.z, self.w)


'''
class DOMMatrix(mat4):
    """ The DOMMatrix interface represents a transformation matrix

    TODO - https://developer.mozilla.org/en-US/docs/Web/API/DOMMatrix

    """

    @staticmethod
    def fromFloat64Array(array):
        return DOMMatrix(
            array[0],
            array[1],
            array[2],
            array[3],
            array[4],
            array[5],
            array[6],
            array[7],
            array[8],
            array[9],
            array[10],
            array[11],
            array[12],
            array[13],
            array[14],
            array[15]
        )

    @staticmethod
    def fromFloat32Array(array):
        return DOMMatrix(
            array[0],
            array[1],
            array[2],
            array[3],
            array[4],
            array[5],
            array[6],
            array[7],
            array[8],
            array[9],
            array[10],
            array[11],
            array[12],
            array[13],
            array[14],
            array[15]
        )

    @staticmethod
    def fromMatrix(matrix):
        return DOMMatrix(matrix.m00, matrix.m01, matrix.m02, matrix.m03,
                         matrix.m10, matrix.m11, matrix.m12, matrix.m13,
                         matrix.m20, matrix.m21, matrix.m22, matrix.m23,
                         matrix.m30, matrix.m31, matrix.m32, matrix.m33)

    def __init__(self, m00, m01, m02, m03, m10, m11, m12, m13, m20, m21, m22, m23, m30, m31, m32, m33):
        self.m00 = m00
        self.m01 = m01
        self.m02 = m02
        self.m03 = m03
        self.m10 = m10
        self.m11 = m11
        self.m12 = m12
        self.m13 = m13
        self.m20 = m20
        self.m21 = m21
        self.m22 = m22
        self.m23 = m23
        self.m30 = m30
        self.m31 = m31
        self.m32 = m32
        self.m33 = m33
        super().__init__(m00, m01, m02, m03, m10, m11, m12, m13, m20, m21, m22, m23, m30, m31, m32, m33)

    def __str__(self):
        return '({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})'.format(
            self.m00, self.m01, self.m02, self.m03, self.m10, self.m11, self.m12, self.m13,
            self.m20, self.m21, self.m22, self.m23, self.m30, self.m31, self.m32, self.m33
        )

    # def invertSelf(self):
    #     self.invert()
    #     return self

    # def multiplySelf(self, other):
    #     self.multiply(other)
    #     return self

    # def translateSelf(self, tx, ty, tz):
    #     self.translate(tx, ty, tz)
    #     return self
'''


class DOMQuad:
    """ The DOMQuad interface represents a quadrilateral on the plane with its
    four corners represented as Cartesian coordinates. """

    @staticmethod
    def fromRect(rect) -> 'DOMQuad':
        return DOMQuad(rect.x, rect.y, rect.width, rect.height)

    @staticmethod
    def fromQuad(quad) -> 'DOMQuad':
        return DOMQuad(quad.p1.x, quad.p1.y, quad.p2.x, quad.p2.y, quad.p3.x, quad.p3.y, quad.p4.x, quad.p4.y)

    @staticmethod
    def getBounds(quad):
        # return DOMRect(quad.p1.x, quad.p1.y, quad.p2.x - quad.p1.x, quad.p2.y - quad.p1.y)
        raise NotImplementedError

    @staticmethod
    def toJSON(quad):
        return {
            'p1': {'x': quad.p1.x, 'y': quad.p1.y},
            'p2': {'x': quad.p2.x, 'y': quad.p2.y},
            'p3': {'x': quad.p3.x, 'y': quad.p3.y},
            'p4': {'x': quad.p4.x, 'y': quad.p4.y}
        }

    def __init__(self, p1, p2, p3, p4):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4

    def __str__(self):
        return '({}, {}, {}, {})'.format(self.p1, self.p2, self.p3, self.p4)


# NodeFilter
# from xml.dom.NodeFilter import NodeFilter
# https://bspaans.github.io/python-mingus/_modules/xml/dom/xmlbuilder.html
# https://www.w3.org/TR/2003/WD-DOM-Level-3-LS-20030226/load-save.html
# https://bspaans.github.io/python-mingus/_modules/xml/dom/xmlbuilder.html
class NodeFilter():

    SHOW_ALL = 0xFFFFFFFF
    SHOW_ELEMENT = 0x00000001
    SHOW_ATTRIBUTE = 0x00000002
    SHOW_TEXT = 0x00000004
    SHOW_CDATA_SECTION = 0x00000008
    SHOW_ENTITY_REFERENCE = 0x00000010
    SHOW_ENTITY = 0x00000020
    SHOW_PROCESSING_INSTRUCTION = 0x00000040
    SHOW_COMMENT = 0x00000080
    SHOW_DOCUMENT = 0x00000100
    SHOW_DOCUMENT_TYPE = 0x00000200
    SHOW_DOCUMENT_FRAGMENT = 0x00000400
    SHOW_NOTATION = 0x00000800

    FILTER_ACCEPT: int = 1
    FILTER_REJECT: int = 2
    FILTER_SKIP: int = 3

    # def acceptNode(node):
    # return NodeFilter.FILTER_ACCEPT
    # return node

    # def acceptNode(node):
    # result
    # if active:
    #     raise Exception('DOMException: INVALID_STATE_ERR')

    # active = True
    # result = filter(node)
    # active = False

    # return result


class NodeIterator():
    """[NodeIterator is an iterator object that iterates over the descendants of a node, in tree order.]
    """

    def __init__(self, root, whatToShow=NodeFilter.SHOW_ALL, filter=None, entityReferenceExpansion=False):
        self.root = root
        self.whatToShow = whatToShow
        self._filter = filter
        self.entityReferenceExpansion = entityReferenceExpansion
        self.node = root
        self.pointer = 0
        self.stack = []

    @property
    def filter(self):
        return self._filter

    # def expandEntityReferences(self, expand):
        # Is a boolean value indicating if,
        # when discarding an EntityReference its whole sub-tree must be discarded at the same time.

    def referenceNode(self) -> Node:
        """ Returns the Node that is being iterated over. """
        return self.node

    def pointerBeforeReferenceNode(self) -> bool:
        """ Returns a boolean flag that indicates whether the NodeIterator
        is anchored before, the flag being true,
        or after, the flag being false, the anchor node.
        """
        return self.pointer < 0

    def detach(self):
        # This operation is a no-op. It doesn't do anything.
        # Previously it was telling the engine that the NodeIterator was no more used, but this is now useless.
        pass

    def previousNode(self):
        """ Returns the previous Node in the document, or null if there are none. """
        if self.pointer < 0:
            return None
        if self.pointer == 0:
            return self.root
        if self.pointer == 1:
            return self.stack[0]
        return self.stack[self.pointer - 1]

    def nextNode(self):
        """ Returns the next Node in the document, or null if there are none. """
        raise NotImplementedError()


mapChild = {
    "first": 'firstChild',
    "last": 'lastChild',
    "next": 'firstChild',
    "previous": 'lastChild'
}

mapSibling = {
    "next": 'nextSibling',
    "previous": 'previousSibling'
}

# toString = mapChild.toString

# def _is(x, _type):
#     print('!!!!!!!!!!!!!!!!!!! comparing', x, _type)
#     return mapChild[x].toLowerCase() == '[object ' + _type.toLowerCase() + ']'


def nodeFilter(tw, node):
    # Maps nodeType to whatToShow
    # print(node, type(node))
    # if isinstance(node, (str)): #, Text)):
        # node = Text(node)
        # return NodeFilter.FILTER_SKIP
        # return NodeFilter.FILTER_REJECT
    if not (((1 << (node.nodeType - 1)) & tw.whatToShow)):
        return NodeFilter.FILTER_SKIP
    if tw._filter == None:
        return NodeFilter.FILTER_ACCEPT
    return tw._filter.acceptNode(node)


def str_to_TextNode(content_str):
    if isinstance(content_str, str):
        return Text(content_str)
    return content_str


def traverseChildren(tw, _type):
    # var child, node, parent, result, sibling
    # print('mapChild[_type]', mapChild[_type])
    node = getattr(tw.currentNode, mapChild[_type])  # TODO - allow dict access to node props?.... tw.currentNode[mapChild[_type]]
    # print('tw.currentNode', tw.currentNode)
    # node = str_to_TextNode(node)
    while node != None:
        # node = str_to_TextNode(node)
        result = nodeFilter(tw, node)
        if result == NodeFilter.FILTER_ACCEPT:
            tw.currentNode = node
            return node
        if result == NodeFilter.FILTER_SKIP:
            child = getattr(node, mapChild[_type])
            if child != None:
                node = child
                continue
        while node != None:
            sibling = getattr(node, mapChild[_type])
            if sibling != None:
                node = sibling
                break
            parent = node.parentNode
            if parent == None or parent == tw.root or parent == tw.currentNode:
                return None
            else:
                node = parent
    return None


def traverseSiblings(tw, type):
    # node, result, sibling
    node = tw.currentNode
    if (node == tw.root):
        return None
    while True:
        sibling = getattr(node, mapSibling[type])
        while sibling != None:
            node = sibling
            result = nodeFilter(tw, node)
            if (result == NodeFilter.FILTER_ACCEPT):
                tw.currentNode = node
                return node
            sibling = getattr(node, mapChild[type])
            if result == NodeFilter.FILTER_REJECT:
                sibling = getattr(node, mapSibling[type])
        node = node.parentNode
        if node == None or node == tw.root:
            return None
        if nodeFilter(tw, node) == NodeFilter.FILTER_ACCEPT:
            return None


def nextSkippingChildren(node, stayWithin):

    # if isinstance(node, str):
        # node = Text(node)
        # return None
    # TODO - casting is not enough. as the Text node does not know its siblings
    # print( "nsc", node, "??", stayWithin )
    # print( "AND:", node.nextSibling )

    if node == stayWithin:
        # print('a')
        return None
    if node.nextSibling != None:
        # print('b')
        return node.nextSibling

    while node.parentNode != None:
        # print('c')
        node = node.parentNode
        if node == stayWithin:
            # print('d')
            return None
        if node.nextSibling != None:
            # print('e')
            return node.nextSibling
    return None


# https://developer.mozilla.org/en-US/docs/Web/API/TreeWalker
class TreeWalker():
    """ The TreeWalker object represents the nodes of a document subtree and a position within them. """

    def _upgrade_dom(self):
        """[
            Our dom has some strings that are not Text Nodes
            so we have to upgrade them to Node objects. As we can't know siblings otherwise
            # TODO - consider upgrading as they are created.
        ]
        """
        def upgrade(el):
            if isinstance(el, (Text, str)):
                return
            for child in el:
                if isinstance(child, str):
                    # print('doin one')
                    newchild = Text(child)
                    el.replaceChild(newchild, child)
                    newchild.parentNode = el

        self._root._iterate(self._root, upgrade)

    def __init__(self, node, whatToShow=NodeFilter.SHOW_ALL, _filter=None, expandEntityReferences=False):
        self._root = node
        self._upgrade_dom()
        # print("test", type(self._root[0][0]))

        self.currentNode = node
        # TODO - convert whatToShow to a number?
        self.whatToShow = whatToShow
        # self.whatToShow = self.whatToShow & 0xFFFFFFFF
        self.whatToShow = whatToShow or 0

        self._filter = _filter

        def acceptNode(node):
            nonlocal _filter
            # result
            # if active:
            #     raise Exception('DOMException: INVALID_STATE_ERR')

            # active = True
            result = _filter(node)
            # active = False
            return result

        if self._filter is not None:
            NodeFilter.acceptNode = acceptNode

        self.last = None
        self.parent = None
        self.previous = None
        self.children = []
        self.childIndex = 0

        self.tree = None

        """ Is a boolean value indicating,
            when discarding an entity reference its whole sub-tree must be discarded at the same time. """
        self.expandEntityReferences = expandEntityReferences

    @property
    def root(self):
        """ Returns a Node representing the root node as specified when the TreeWalker was created. """
        return self._root

    def whatToShow(self, options):
        """ Returns an unsigned long being a bitmask made of constants describing the types of Node that must be presented.
        Non-matching nodes are skipped, but their children may be included, if relevant. The possible values are: """
        return options

    # def filter(self, options):
    #     """ Returns a NodeFilter object that can be used to filter the nodes that the TreeWalker visits. """
    #     return options

    # @property
    # def currentNode(self):
    #     """ Is the Node on which the TreeWalker is currently pointing at. """
    #     return self.currentNode

    def parentNode(self):
        """ Moves the current Node to the first visible ancestor node in the document order,
        and returns the found node. It also moves the current node to this one. If no such node exists,
        or if it is before that the root node defined at the object construction,
        returns null and the current node is not changed. """
        # return self.currentNode.parentNode
        node = self.currentNode
        while node != None and node != self.root:
            node = node.parentNode
            if node != None and nodeFilter(self, node) == NodeFilter.FILTER_ACCEPT:
                self.currentNode = node
                return node
            return None

    def firstChild(self):
        """ Moves the current Node to the first visible child of the current node, and returns the found child.
        It also moves the current node to this child. If no such child exists,
        returns null and the current node is not changed. """
        # return self.currentNode.firstChild
        return traverseChildren(self, 'first')

    def lastChild(self):
        """ Moves the current Node to the last visible child of the current node, and returns the found child.
        It also moves the current node to this child.
        If no such child exists, null is returned and the current node is not changed. """
        # return self.currentNode.lastChild
        return traverseChildren(self, 'last')

    def previousSibling(self):
        """ Moves the current Node to its previous sibling, if any, and returns the found sibling.
        If there is no such node, return null and the current node is not changed.
        """
        # return self.previous
        return traverseSiblings(self, 'previous')

    def nextSibling(self):
        """ Moves the current Node to its next sibling, if any, and returns the found sibling.
        If there is no such node, null is returned and the current node is not changed. """
        # return self.currentNode.nextSibling
        return traverseSiblings(self, 'next')

    def previousNode(self):
        """ Moves the current Node to the previous visible node in the document order,
        and returns the found node. It also moves the current node to this one.
        If no such node exists, or if it is before that the root node defined at the object construction,
        returns null and the current node is not changed. """
        # return self.previous
        # raise NotImplementedError()
        # var node, result, sibling
        node = self.currentNode
        while (node != self.root):
            sibling = node.previousSibling
            while sibling != None:
                node = sibling
                result = nodeFilter(self, node)
                while result != NodeFilter.FILTER_REJECT and node.lastChild != None:
                    node = node.lastChild
                    result = nodeFilter(self, node)
                if result == NodeFilter.FILTER_ACCEPT:
                    self.currentNode = node
                    return node
            if node == self.root or node.parentNode == None:
                return None
            node = node.parentNode
            if nodeFilter(self, node) == NodeFilter.FILTER_ACCEPT:
                self.currentNode = node
                return node
        return None

    def nextNode(self):
        """ Moves the current Node to the next visible node in the document order, and returns the found node.
        It also moves the current node to this one.
        If no such node exists, returns None and the current node is not changed.
        can be used in a while loop to iterate over all the nodes in the document order.
        """
        # var node, result, following;
        node = self.currentNode

        if isinstance(node, str):
            node = Text(node)
            # return node

        result = NodeFilter.FILTER_ACCEPT
        while True:
            # print('rrr:::', result, node)
            if isinstance(node, str):
                Text(node)
                # continue

            while result != NodeFilter.FILTER_REJECT and node.firstChild != None:
                # print('rrr222:::', result, node)
                node = node.firstChild
                if isinstance(node, str):
                    node = Text(node)
                    # result = NodeFilter.FILTER_REJECT
                    # continue
                    # break
                    # return None

                result = nodeFilter(self, node)
                if result == NodeFilter.FILTER_ACCEPT:
                    self.currentNode = node
                    return node
            following = nextSkippingChildren(node, self.root)
            if following != None:
                node = following
            else:
                # print('NONE')
                return None
            result = nodeFilter(self, node)
            if result == NodeFilter.FILTER_ACCEPT:
                self.currentNode = node
                return node


# TODO - create fetch package and move the js fetch stuff to it?
# fetch api

# AbortController
# AbortSignal
# Cache
# CacheStorage
# ContentIndex
# ContactPicker
# Client - serviceworker api
# CredentialsContainer - new login api
# DOMMatrix #https://developer.mozilla.org/en-US/docs/Web/API/DOMMatrix
# DOMParser
# IndexedDB API
# ImageBitmap
# ImageBitmapRenderingContext
# ImageData
# MutationObserver
# MutationRecord
# OverconstrainedError
# QueueingStrategy
# ReadableStream
# SCTP
# SourceBuffer
# SourceBufferAppendMode
# SourceBufferAppendWindowEnd
# TimeRanges - media
# TrackEvent - media
# ValidityState
# Web Share API
# WebGL
# also
# https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API

# HTMLElementTagNameMap < how many of these types are there?

# XMLSerializer = xml.dom.minidom.XMLSerializer?
# XMLSerializer.serializeToString(rootNode)

class Sanitizer:
    def __init__(self, rules=None, *args, **kwargs):
        """Creates and returns a Sanitizer object."""

        # casting as object gives us . notation
        from domonic.javascript import Object

        self._default_configuration = Object(
            {
                "allowCustomElements": False,
                # "allowElements": [],  # elements that the sanitizer should retain in the input.
                "blockElements": [],  # elements where the sanitizer should remove the elements from the input, but retain their children.
                "dropElements": [],  # elements that the sanitizer should remove from the input, including its children.
                # "allowAttributes": [],  # determines whether an attribute (on a given element) should be allowed.
                "dropAttributes": [],  # determines whether an attribute (on a given element) should be dropped.
                "allowCustomElements": False,  # determines whether custom elements are to be considered. The default is to drop them. If this option is true, custom elements will still be checked against all other built-in or configured configured checks.
                "allowComments": False,  # determines whether HTML comments are allowed.
                "allowElements": [
                    "a",
                    "abbr",
                    "acronym",
                    "address",
                    "area",
                    "article",
                    "aside",
                    "audio",
                    "b",
                    "bdi",
                    "bdo",
                    "bgsound",
                    "big",
                    "blockquote",
                    "body",
                    "br",
                    "button",
                    "canvas",
                    "caption",
                    "center",
                    "cite",
                    "code",
                    "col",
                    "colgroup",
                    "datalist",
                    "dd",
                    "del",
                    "details",
                    "dfn",
                    "dialog",
                    "dir",
                    "div",
                    "dl",
                    "dt",
                    "em",
                    "fieldset",
                    "figcaption",
                    "figure",
                    "font",
                    "footer",
                    "form",
                    "h1",
                    "h2",
                    "h3",
                    "h4",
                    "h5",
                    "h6",
                    "head",
                    "header",
                    "hgroup",
                    "hr",
                    "html",
                    "i",
                    "img",
                    "input",
                    "ins",
                    "kbd",
                    "keygen",
                    "label",
                    "layer",
                    "legend",
                    "li",
                    "link",
                    "listing",
                    "main",
                    "map",
                    "mark",
                    "marquee",
                    "menu",
                    "meta",
                    "meter",
                    "nav",
                    "nobr",
                    "ol",
                    "optgroup",
                    "option",
                    "output",
                    "p",
                    "picture",
                    "popup",
                    "pre",
                    "progress",
                    "q",
                    "rb",
                    "rp",
                    "rt",
                    "rtc",
                    "ruby",
                    "s",
                    "samp",
                    "section",
                    "select",
                    "selectmenu",
                    "small",
                    "source",
                    "span",
                    "strike",
                    "strong",
                    "style",
                    "sub",
                    "summary",
                    "sup",
                    "table",
                    "tbody",
                    "td",
                    "tfoot",
                    "th",
                    "thead",
                    "time",
                    "tr",
                    "track",
                    "tt",
                    "u",
                    "ul",
                    "var",
                    "video",
                    "wbr",
                ],
                "allowAttributes": {
                    "abbr": ["*"],
                    "accept": ["*"],
                    "accept-charset": ["*"],
                    "accesskey": ["*"],
                    "action": ["*"],
                    "align": ["*"],
                    "alink": ["*"],
                    "allow": ["*"],
                    "allowfullscreen": ["*"],
                    "alt": ["*"],
                    "anchor": ["*"],
                    "archive": ["*"],
                    "as": ["*"],
                    "async": ["*"],
                    "autocapitalize": ["*"],
                    "autocomplete": ["*"],
                    "autocorrect": ["*"],
                    "autofocus": ["*"],
                    "autopictureinpicture": ["*"],
                    "autoplay": ["*"],
                    "axis": ["*"],
                    "background": ["*"],
                    "behavior": ["*"],
                    "bgcolor": ["*"],
                    "border": ["*"],
                    "bordercolor": ["*"],
                    "capture": ["*"],
                    "cellpadding": ["*"],
                    "cellspacing": ["*"],
                    "challenge": ["*"],
                    "char": ["*"],
                    "charoff": ["*"],
                    "charset": ["*"],
                    "checked": ["*"],
                    "cite": ["*"],
                    "class": ["*"],
                    "classid": ["*"],
                    "clear": ["*"],
                    "code": ["*"],
                    "codebase": ["*"],
                    "codetype": ["*"],
                    "color": ["*"],
                    "cols": ["*"],
                    "colspan": ["*"],
                    "compact": ["*"],
                    "content": ["*"],
                    "contenteditable": ["*"],
                    "controls": ["*"],
                    "controlslist": ["*"],
                    "conversiondestination": ["*"],
                    "coords": ["*"],
                    "crossorigin": ["*"],
                    "csp": ["*"],
                    "data": ["*"],
                    "datetime": ["*"],
                    "declare": ["*"],
                    "decoding": ["*"],
                    "default": ["*"],
                    "defer": ["*"],
                    "dir": ["*"],
                    "direction": ["*"],
                    "dirname": ["*"],
                    "disabled": ["*"],
                    "disablepictureinpicture": ["*"],
                    "disableremoteplayback": ["*"],
                    "disallowdocumentaccess": ["*"],
                    "download": ["*"],
                    "draggable": ["*"],
                    "elementtiming": ["*"],
                    "enctype": ["*"],
                    "end": ["*"],
                    "enterkeyhint": ["*"],
                    "event": ["*"],
                    "exportparts": ["*"],
                    "face": ["*"],
                    "for": ["*"],
                    "form": ["*"],
                    "formaction": ["*"],
                    "formenctype": ["*"],
                    "formmethod": ["*"],
                    "formnovalidate": ["*"],
                    "formtarget": ["*"],
                    "frame": ["*"],
                    "frameborder": ["*"],
                    "headers": ["*"],
                    "height": ["*"],
                    "hidden": ["*"],
                    "high": ["*"],
                    "href": ["*"],
                    "hreflang": ["*"],
                    "hreftranslate": ["*"],
                    "hspace": ["*"],
                    "http-equiv": ["*"],
                    "id": ["*"],
                    "imagesizes": ["*"],
                    "imagesrcset": ["*"],
                    "importance": ["*"],
                    "impressiondata": ["*"],
                    "impressionexpiry": ["*"],
                    "incremental": ["*"],
                    "inert": ["*"],
                    "inputmode": ["*"],
                    "integrity": ["*"],
                    "invisible": ["*"],
                    "is": ["*"],
                    "ismap": ["*"],
                    "keytype": ["*"],
                    "kind": ["*"],
                    "label": ["*"],
                    "lang": ["*"],
                    "language": ["*"],
                    "latencyhint": ["*"],
                    "leftmargin": ["*"],
                    "link": ["*"],
                    "list": ["*"],
                    "loading": ["*"],
                    "longdesc": ["*"],
                    "loop": ["*"],
                    "low": ["*"],
                    "lowsrc": ["*"],
                    "manifest": ["*"],
                    "marginheight": ["*"],
                    "marginwidth": ["*"],
                    "max": ["*"],
                    "maxlength": ["*"],
                    "mayscript": ["*"],
                    "media": ["*"],
                    "method": ["*"],
                    "min": ["*"],
                    "minlength": ["*"],
                    "multiple": ["*"],
                    "muted": ["*"],
                    "name": ["*"],
                    "nohref": ["*"],
                    "nomodule": ["*"],
                    "nonce": ["*"],
                    "noresize": ["*"],
                    "noshade": ["*"],
                    "novalidate": ["*"],
                    "nowrap": ["*"],
                    "object": ["*"],
                    "open": ["*"],
                    "optimum": ["*"],
                    "part": ["*"],
                    "pattern": ["*"],
                    "ping": ["*"],
                    "placeholder": ["*"],
                    "playsinline": ["*"],
                    "policy": ["*"],
                    "poster": ["*"],
                    "preload": ["*"],
                    "pseudo": ["*"],
                    "readonly": ["*"],
                    "referrerpolicy": ["*"],
                    "rel": ["*"],
                    "reportingorigin": ["*"],
                    "required": ["*"],
                    "resources": ["*"],
                    "rev": ["*"],
                    "reversed": ["*"],
                    "role": ["*"],
                    "rows": ["*"],
                    "rowspan": ["*"],
                    "rules": ["*"],
                    "sandbox": ["*"],
                    "scheme": ["*"],
                    "scope": ["*"],
                    "scopes": ["*"],
                    "scrollamount": ["*"],
                    "scrolldelay": ["*"],
                    "scrolling": ["*"],
                    "select": ["*"],
                    "selected": ["*"],
                    "shadowroot": ["*"],
                    "shadowrootdelegatesfocus": ["*"],
                    "shape": ["*"],
                    "size": ["*"],
                    "sizes": ["*"],
                    "slot": ["*"],
                    "span": ["*"],
                    "spellcheck": ["*"],
                    "src": ["*"],
                    "srcdoc": ["*"],
                    "srclang": ["*"],
                    "srcset": ["*"],
                    "standby": ["*"],
                    "start": ["*"],
                    "step": ["*"],
                    "style": ["*"],
                    "summary": ["*"],
                    "tabindex": ["*"],
                    "target": ["*"],
                    "text": ["*"],
                    "title": ["*"],
                    "topmargin": ["*"],
                    "translate": ["*"],
                    "truespeed": ["*"],
                    "trusttoken": ["*"],
                    "type": ["*"],
                    "usemap": ["*"],
                    "valign": ["*"],
                    "value": ["*"],
                    "valuetype": ["*"],
                    "version": ["*"],
                    "virtualkeyboardpolicy": ["*"],
                    "vlink": ["*"],
                    "vspace": ["*"],
                    "webkitdirectory": ["*"],
                    "width": ["*"],
                    "wrap": ["*"],
                },
            }
        )

        self.config = None
        if isinstance(rules, dict):
            self.rules = rules
            # create a new configuration which is a copy of the default but change it based on the rules object
            import copy
            self.config = copy.deepcopy(self._default_configuration)
            for key, value in self.rules.items():
                # print('ADDING RULES', key, value)
                self.config[key] = value
        else:
            self.rules = None
            self.config = self._default_configuration

    def getDefaultConfiguration(self):
        return self._default_configuration

    def getConfiguration(self):
        """[return the configuration object]

        Returns:
            [Object]: [an Object with the users configuration]
        """
        return self.config

    def sanitize(self, frag):
        """ Returns a sanitized DocumentFragment from an input, removing any offending elements or attributes. """
        if isinstance(frag, str):
            # parse to html then remove all the bad stuff?? - is a really bad idea. as it goes through eval.
            from domonic import domonic
            frag = domonic.load(frag)

        isDomNode = False
        if isinstance(frag, Document):
            isDomNode = True

        if not isDomNode:
            newfrag = Document.createDocumentFragment()
            if isinstance(frag, (tuple, list)):
                for f in frag:
                    newfrag.appendChild(f)
            else:
                newfrag.appendChild(frag)
            frag = newfrag

        # TODO "allowCustomElements": # "allowElements": [], # "blockElements": [], # "dropElements": [],  # "allowAttributes": [],
        # TODO "dropAttributes": # "allowCustomElements": # "allowComments": # "allowElements" # allowAttributes

        for t in self.config["dropElements"]:
            el = frag.getElementsByTagName(t)
            el.parentNode.removeChild(el)

        for t in self.config["dropAttributes"]:
            for e in self.config["allowElements"]:
                els = frag.getElementsByTagName(e)
                if els != False and len(els) > 0:
                    for el in els:
                        for each in el.attributes:
                            if each.name == t:
                                el.removeAttribute(each.name)

        # print("test" frag.querySelectorAll('span'))
        # print("test2", frag.getElementsByTagName('span'))

        for e in self.config["allowElements"]:
            els = frag.getElementsByTagName(e)
            if els != False and len(els) > 0:
                for el in els:
                    # print(el, el.kwargs, el.attributes, el.__attributes__, type(el.attributes))
                    for each in el.attributes:
                        # print(each)
                        key = each.name
                        val = each.value
                        # print(key, val)
                        allowed_on = self.config["allowAttributes"].get(key)
                        # print("ALLOWED ON:", key, allowed_on)
                        if allowed_on == None:
                            el.removeAttribute(key)
                            continue
                        if "*" in allowed_on:
                            continue
                        if e not in allowed_on:
                            el.removeAttribute(key)
                        # else:
                        #     print(key + ' is allowed')

        for t in self.config["blockElements"]:
            el = frag.getElementsByTagName(str(t))
            # keep the children of the element and add them back to the parent
            for c in el.childNodes:
                frag.parentNode.appendChild(c)
            # remove the element
            frag.parentNode.removeChild(el)

        # print(type(frag))
        return frag

    def sanitizeToString(self, frag) -> str:
        """ Returns a sanitized String from an input, removing any offending elements or attributes. """
        return str(self.sanitize(frag))


class HTMLElement(Element):  # TODO - check
    name = ''


class HTMLAnchorElement(HTMLElement):  # TODO - check
    name = 'a'


class HTMLAreaElement(HTMLElement):  # TODO - check
    name = 'area'


class HTMLAudioElement(HTMLElement):
    name = 'audio'


class HTMLBRElement(HTMLElement):
    name = 'br'


class HTMLBaseElement(HTMLElement):
    name = 'base'


class HTMLBaseFontElement(HTMLElement):  # TODO - check
    name = 'basefont'


class HTMLBodyElement(HTMLElement):
    name = 'body'


class HTMLButtonElement(HTMLElement):
    name = 'button'


class HTMLCanvasElement(HTMLElement):
    name = 'canvas'


class HTMLContentElement(HTMLElement):  # TODO - check
    name = 'content'


class HTMLDListElement(HTMLElement):
    name = 'dl'


class HTMLDataElement(HTMLElement):
    name = 'data'


class HTMLDataListElement(HTMLElement):
    name = 'datalist'


class HTMLDialogElement(HTMLElement):
    name = 'dialog'


class HTMLDivElement(HTMLElement):
    name = 'div'


class HTMLDocument(Document):
    name = 'html'


class HTMLEmbedElement(HTMLElement):
    name = 'embed'


class HTMLFieldSetElement(HTMLElement):  # TODO - check
    name = 'fieldset'


class HTMLFormControlsCollection(HTMLElement):  # TODO - check
    name = 'formcontrols'


class HTMLFormElement(HTMLElement):
    name = 'form'


class HTMLFrameSetElement(HTMLElement):  # TODO - check
    name = 'frameset'


class HTMLHRElement(HTMLElement):
    name = 'hr'


class HTMLHeadElement(HTMLElement):
    name = 'head'


class HTMLHeadingElement(HTMLElement):
    name = 'h1'


class HTMLIFrameElement(HTMLElement):
    name = 'iframe'


class HTMLImageElement(HTMLElement):
    name = 'img'


class HTMLInputElement(HTMLElement):
    name = 'input'


class HTMLIsIndexElement(HTMLElement):  # TODO - check
    name = ''


class HTMLKeygenElement(HTMLElement):
    name = 'keygen'


class HTMLLIElement(HTMLElement):
    name = 'li'


class HTMLLabelElement(HTMLElement):
    name = 'label'


class HTMLLegendElement(HTMLElement):
    name = 'legend'


class HTMLLinkElement(HTMLElement):
    name = 'link'


class HTMLMapElement(HTMLElement):  # TODO - check
    name = 'map'


class HTMLMediaElement(HTMLElement):  # TODO - check
    name = 'media'


class HTMLMetaElement(HTMLElement):
    name = 'meta'


class HTMLMeterElement(HTMLElement):
    name = 'meter'


class HTMLModElement(HTMLElement):  # TODO - check
    name = 'mod'


class HTMLOListElement(HTMLElement):
    name = 'ol'


class HTMLObjectElement(HTMLElement):
    name = 'object'


class HTMLOptGroupElement(HTMLElement):
    name = 'optgroup'


class HTMLOptionElement(HTMLElement):
    name = 'option'


# class HTMLOptionsCollection(HTMLElement):   # TODO - check
#     name = 'options'


class HTMLOutputElement(HTMLElement):
    name = 'output'


class HTMLParagraphElement(HTMLElement):
    name = 'p'


class HTMLParamElement(HTMLElement):  # TODO - check
    name = 'param'


class HTMLPictureElement(HTMLElement):
    name = 'picture'


class HTMLPreElement(HTMLElement):
    name = 'pre'


class HTMLProgressElement(HTMLElement):
    name = 'progress'


class HTMLQuoteElement(HTMLElement):  # TODO - check
    name = 'q'


class HTMLScriptElement(HTMLElement):
    name = 'script'


class HTMLSelectElement(HTMLElement):
    name = 'select'


class HTMLShadowElement(HTMLElement):  # TODO - check
    name = 'shadow'


class HTMLSourceElement(HTMLElement):  # TODO - check
    name = 'source'


class HTMLSpanElement(HTMLElement):
    name = 'span'


class HTMLStyleElement(HTMLElement):
    name = 'style'


class HTMLTableCaptionElement(HTMLElement):  # TODO - check
    name = 'caption'


class HTMLTableCellElement(HTMLElement):  # TODO - check
    name = 'td'


class HTMLTableColElement(HTMLElement):
    name = 'col'


class HTMLTableDataCellElement(HTMLElement):  # TODO - check
    name = 'td'


class HTMLTableElement(HTMLElement):
    name = 'table'


class HTMLTableHeaderCellElement(HTMLElement):
    name = 'th'


class HTMLTableRowElement(HTMLElement):
    name = 'tr'


class HTMLTableSectionElement(HTMLElement):
    name = 'tbody'


class HTMLTemplateElement(HTMLElement):  # TODO - check
    name = 'template'


class HTMLTextAreaElement(HTMLElement):
    name = 'textarea'


class HTMLTimeElement(HTMLElement):
    name = 'time'


class HTMLTitleElement(HTMLElement):
    name = 'title'


class HTMLTrackElement(HTMLElement):
    name = 'track'


class HTMLUListElement(HTMLElement):
    name = 'ul'


class HTMLUnknownElement(HTMLElement):
    name = 'unknown'


class HTMLVideoElement(HTMLElement):
    name = 'video'


# document can be set manually but will get set each time a new Document is created.
global document
document = Document
console = Console  # legacy. should access via window


# Considered obsolete dom classes ----
# DOMConfiguration
# DOMErrorHandler
# DOMImplementationList
# DOMImplementationRegistry
# DOMImplementationSource
# DOMLocator
# DOMObject
# DOMSettableTokenList
# DOMUserData
# ElementTraversal
# Entity
# EntityReference
# NameList
# Notation
# TypeInfo
# UserDataHandler


'''
# self.screen = type('screen', (DOM,), {'name':'screen'})
'''
