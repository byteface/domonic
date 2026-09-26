"""
domonic.ext.html5lib_
====================================

stolen from here and modded to work with domonic instead of mindidom
https://github.com/html5lib/html5lib-python/blob/master/html5lib/treebuilders/__init__.py

"""

'''
from __future__ import absolute_import, division, unicode_literals
# from .._utils import default_etree

treeBuilderCache = {}

def getTreeBuilder(treeType, implementation='domonic', **kwargs):
    treeType = treeType.lower()
    if treeType not in treeBuilderCache:
        if treeType == "domonic":
            from . import dom
            if implementation is None:
                from xml.dom import minidom
                implementation = minidom
            return dom.getDomModule(implementation, **kwargs).TreeBuilder
        else:
            raise ValueError("""domonic treebuilder required "%s" """ % treeType)
    return treeBuilderCache.get(treeType)
'''

# from __future__ import absolute_import, division, unicode_literals

# from xml.dom import minidom, Node
import threading
import weakref
from collections.abc import MutableMapping
from importlib import import_module

from html5lib import constants
from html5lib._utils import moduleFactoryFactory
from html5lib.constants import namespaces
from html5lib.treebuilders import base

from domonic.dom import DOMImplementation, Node
from domonic.ext._rawdom import HTML_NAMESPACE as _HTML_NS
from domonic.ext._rawdom import (
    _create_comment_raw,
    _create_element_raw,
    _create_text_raw,
    _freeze,
    _live_args,
)

# ``_recording.hook`` is set by a streaming session on the thread that runs
# html5lib, so insertions can be reported to MutationObserver after each
# write. Thread-local, so concurrent sessions never see each other's nodes.
_recording = threading.local()


def _record_insert(parent, child):
    hook = getattr(_recording, "hook", None)
    if hook is not None:
        hook(parent, child)


def _raw_detach(child):
    """Remove ``child`` from its current parent's ``args`` without firing any
    of the DOM mutation machinery (observers, connected callbacks, adoption).
    """
    old_parent = child.__dict__.get("parentNode")
    if old_parent is None:
        return
    args = _live_args(old_parent)
    # Identity, not ``==``: a detach nearly always targets a recent child, so
    # scan from the end.
    for index in range(len(args) - 1, -1, -1):
        if args[index] is child:
            del args[index]
            break


def _raw_append(parent, child):
    _raw_detach(child)
    _live_args(parent).append(child)
    child.__dict__["parentNode"] = parent


def _raw_insert_before(parent, child, ref):
    _raw_detach(child)
    args = _live_args(parent)
    index = next((i for i, node in enumerate(args) if node is ref), len(args))
    args.insert(index, child)
    child.__dict__["parentNode"] = parent


def _raw_remove(parent, child):
    args = _live_args(parent)
    for index in range(len(args) - 1, -1, -1):
        if args[index] is child:
            del args[index]
            break
    child.__dict__["parentNode"] = None


HTML_TAGS = frozenset(import_module("domonic.html").html_tags)
SVG_TAGS = frozenset(import_module("domonic.svg").svg_tags) - HTML_TAGS
MATHML_TAGS = frozenset(import_module("domonic.xml.mathml").mathml_tags)
SVG_TAG_NAMES = frozenset(tag.lower() for tag in SVG_TAGS)
MATHML_TAG_NAMES = frozenset(tag.lower() for tag in MATHML_TAGS)


# def getDomBuilder(DomImplementation):
#     Dom = DomImplementation


def getDomBuilder(ignore: object):
    # Dom = DomImplementation

    class AttrList(MutableMapping):
        def __init__(self, element):
            self.element = element

        def __iter__(self):
            return iter(self.element.attributes.keys())

        def __setitem__(self, name, value):
            if isinstance(name, tuple):
                raise NotImplementedError
            else:
                attr = self.element.ownerDocument.createAttribute(name)
                attr.value = value
                self.element.attributes[name] = attr

        def __len__(self):
            return len(self.element.attributes)

        def items(self):
            # return list(self.element.attributes.items())
            return list(self.element.attributes.items())
            # return self.element.attributes

        def values(self):
            return list(self.element.attributes.values())

        def __getitem__(self, name):
            if isinstance(name, tuple):
                raise NotImplementedError
            else:
                # MutableMapping's default __contains__ (and so `in`/`not in`)
                # works by calling __getitem__ and catching KeyError -- it must
                # propagate, not be swallowed, or every "x not in element.attributes"
                # check (used by html5lib's insertHtmlElement -> startTagHtml to
                # merge a later <html ...> tag's attributes onto the already-
                # inserted root) sees every name as already present and never
                # copies the attribute across.
                return self.element.attributes[name].value

        def __delitem__(self, name):
            if isinstance(name, tuple):
                raise NotImplementedError
            else:
                del self.element.attributes[name]

    class NodeBuilder(base.Node):
        def __init__(self, element):
            # NOTE requires tagname to be correct as it checks that against keys in namespaces.
            # i.e '#document' needs to be converted to 'html'.
            # base.Node.__init__(self, element.nodeName)
            base.Node.__init__(self, element.name)
            self.element = element
            # ``namespace`` / ``nameTuple`` are read hundreds of thousands of
            # times per parse by html5lib's scope checks; resolve them once.
            self.namespace = element.__dict__.get("namespaceURI") or None
            self.nameTuple = (
                self.namespace or namespaces["html"],
                self.name,
            )

        def appendChild(self, node):
            node.parent = self
            _raw_append(self.element, node.element)
            _record_insert(self.element, node.element)

        def insertText(self, data, insertBefore=None):
            # Whitespace-only text nodes are kept: whitespace between inline
            # elements (``<b>x</b> <i>y</i>``) is significant, and dropping it
            # here loses information the HTML5 tree builder is meant to preserve.
            text = _create_text_raw(data)
            if insertBefore is not None:
                _raw_insert_before(self.element, text, insertBefore.element)
            else:
                _raw_append(self.element, text)
            _record_insert(self.element, text)

        def insertBefore(self, node, refNode):
            _raw_insert_before(self.element, node.element, refNode.element)
            node.parent = self
            _record_insert(self.element, node.element)

        def removeChild(self, node):
            if node.element.__dict__.get("parentNode") is self.element:
                _raw_remove(self.element, node.element)
            node.parent = None

        def reparentChildren(self, newParent):
            target = newParent.element
            moved = _live_args(self.element)
            self.element.__dict__["args"] = []
            _live_args(target).extend(moved)
            for child in moved:
                child.__dict__["parentNode"] = target
            self.childNodes = []

        def getAttributes(self):
            return AttrList(self.element)

        def setAttributes(self, attributes):
            if not attributes:
                return
            kwargs = self.element.__dict__["kwargs"]
            for name, value in attributes.items():
                if isinstance(name, tuple):
                    qualified = name[1] if name[0] is None else name[0] + ":" + name[1]
                    self.element.setAttributeNS(name[2], qualified, value)
                else:
                    key = name if name[:1] == "_" else "_" + name
                    kwargs[key] = "" if value is None else value

        attributes = property(getAttributes, setAttributes)

        def cloneNode(self):
            return NodeBuilder(self.element.cloneNode(False))

        def hasContent(self):
            return bool(self.element.__dict__.get("args"))

    class TreeBuilder(base.TreeBuilder):  # pylint:disable=unused-variable
        def documentClass(self):
            # self.dom = Dom.getDOMImplementation().createDocument(None, None, None)
            self.dom = DOMImplementation().createDocument(None, None, None)
            return weakref.proxy(self)

        def insertDoctype(self, token):
            name = token["name"]
            publicId = token["publicId"]
            systemId = token["systemId"]

            # domimpl = Dom.getDOMImplementation()
            domimpl = DOMImplementation()
            doctype = domimpl.createDocumentType(name, publicId, systemId)
            self.document.appendChild(NodeBuilder(doctype))
            # if Dom == minidom:
            doctype.ownerDocument = self.dom

        def elementClass(self, name, namespace=None):
            normalized_name = str(name).lower()
            if namespace == namespaces["html"] and normalized_name in SVG_TAG_NAMES:
                namespace = namespaces["svg"]
            if namespace == namespaces["html"] and normalized_name in MATHML_TAG_NAMES:
                namespace = namespaces["mathml"]
            node = _create_element_raw(name, namespace or _HTML_NS)
            return NodeBuilder(node)

        def commentClass(self, data):
            return NodeBuilder(_create_comment_raw(data))

        def fragmentClass(self):
            return NodeBuilder(self.dom.createDocumentFragment())

        def appendChild(self, node):
            from domonic.dom import HTMLDocument

            if isinstance(self.dom, HTMLDocument) and isinstance(node.element, HTMLDocument):
                # TODO - this can't be the final solution as a nested html would replace the outer
                self.dom = node.element
                # transfer all props from node.element to self.dom
                # self.dom.__dict__.update(node.element.__dict__)
                # self.dom.appendChild(node.element)
            else:
                self.dom.appendChild(node.element)

        def testSerializer(self, element):
            return testSerializer(element)

        def getDocument(self):
            _freeze(self.dom)
            return self.dom

        def getFragment(self):
            fragment = base.TreeBuilder.getFragment(self).element
            _freeze(fragment)
            return fragment

        def insertText(self, data, parent=None):
            data = data
            if parent != self:
                base.TreeBuilder.insertText(self, data, parent)
            else:
                # HACK: allow text nodes as children of the document node
                if hasattr(self.dom, "_child_node_types"):
                    # pylint:disable=protected-access
                    if Node.TEXT_NODE not in self.dom._child_node_types:
                        self.dom._child_node_types = list(self.dom._child_node_types)
                        self.dom._child_node_types.append(Node.TEXT_NODE)
                text = self.dom.createTextNode(data)
                text._escape_text_on_render = True
                self.dom.appendChild(text)

        # DOM implementation adapter, not XML parsing.
        from xml.dom import minidom  # nosec B408

        implementation = minidom  # DomImplementation
        name = None

    def testSerializer(element):
        element.normalize()
        rv = []

        def serializeElement(element, indent=0):
            if element.nodeType == Node.DOCUMENT_TYPE_NODE:
                if element.name:
                    if element.publicId or element.systemId:
                        publicId = element.publicId or ""
                        systemId = element.systemId or ""
                        rv.append("""|%s<!DOCTYPE %s "%s" "%s">""" % (" " * indent, element.name, publicId, systemId))
                    else:
                        rv.append("|%s<!DOCTYPE %s>" % (" " * indent, element.name))
                else:
                    rv.append("|%s<!DOCTYPE >" % (" " * indent,))
            elif element.nodeType == Node.DOCUMENT_NODE:
                rv.append("#document")
            elif element.nodeType == Node.DOCUMENT_FRAGMENT_NODE:
                rv.append("#document-fragment")
            elif element.nodeType == Node.COMMENT_NODE:
                rv.append("|%s<!-- %s -->" % (" " * indent, element.nodeValue))
            elif element.nodeType == Node.TEXT_NODE:
                rv.append('|%s"%s"' % (" " * indent, element.nodeValue))
            else:
                if hasattr(element, "namespaceURI") and element.namespaceURI is not None:
                    name = "%s %s" % (
                        constants.prefixes[element.namespaceURI],
                        element.nodeName,
                    )
                else:
                    name = element.nodeName
                rv.append("|%s<%s>" % (" " * indent, name))
                if element.hasAttributes():
                    attributes = []
                    for i in range(len(element.attributes)):
                        attr = element.attributes.item(i)
                        name = attr.nodeName
                        value = attr.value
                        ns = attr.namespaceURI
                        if ns:
                            name = "%s %s" % (constants.prefixes[ns], attr.localName)
                        else:
                            name = attr.nodeName
                        attributes.append((name, value))

                    for name, value in sorted(attributes):
                        rv.append('|%s%s="%s"' % (" " * (indent + 2), name, value))
            indent += 2
            for child in element.childNodes:
                serializeElement(child, indent)

        serializeElement(element, 0)

        return "\n".join(rv)

    return locals()


# The actual means to get a module!
getDomModule = moduleFactoryFactory(getDomBuilder)

# if implementation is None:
# DOM implementation adapter, not XML parsing.
from xml.dom import minidom  # nosec B408

implementation = minidom


def getTreeBuilder(target=None):
    """The html5lib tree builder that builds domonic nodes.

    With ``target`` (a document), the tree is built into that document
    instead of a fresh one: ``document.write()`` streams a page this way.
    domonic's ``HTMLDocument`` is the ``<html>`` element, so when the target
    is one the parser's html element *is* the target; a plain ``Document``
    gets the html element as a child.
    """
    base = getDomModule(implementation).TreeBuilder
    if target is None:
        return base

    target_is_html = getattr(target, "name", "") == "html"

    class TargetTreeBuilder(base):
        def documentClass(self):
            self.dom = target
            return weakref.proxy(self)

        def elementClass(self, name, namespace=None):
            node = base.elementClass(self, name, namespace)
            if target_is_html and str(name).lower() == "html" and namespace in (None, namespaces["html"]):
                node.element = target  # the document is its own <html> element
            return node

        def insertDoctype(self, token):
            target.doctype = DOMImplementation().createDocumentType(token["name"], token["publicId"], token["systemId"])

    return TargetTreeBuilder
