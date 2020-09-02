"""
    domonic.dom
    ====================================
    methods on the dom
"""

from typing import *
import re

from domonic.style import Style
import domonic.javascript
from domonic.events import *


class EventTarget:
    """ Baseclass for Node """

    def __init__(self):
        self.listeners = {}

    # TODO - event: str, function, useCapture: bool
    # def addEventListener(self, event: str, function, useCapture: bool) -> None:
    def addEventListener(self, _type, callback, *args, **kwargs):
        if _type not in self.listeners:
            self.listeners[_type] = []
        self.listeners[_type].append(callback)

    def removeEventListener(self, _type, callback):
        if _type not in self.listeners:
            return

        stack = self.listeners[_type]

        for thing in stack:
            if thing == callback:
                stack.remove(thing)
                return

    def dispatchEvent(self, event):
        if event.type not in self.listeners:
            return True  # huh?. surely false?

        stack = self.listeners[event.type]
        # .slice()
        event.target = self  # TODO/NOTE - is this correct? - cant think where else would set it

        for thing in stack:
            try:
                thing(event)
                # type(thing, (Event,), self)
            except Exception as e:
                print(e)
                thing()  # try calling without params, user may not create param

        return not event.defaultPrevented


class Node(EventTarget):
    """ Element extends from Node """

    def __init__(self, *args, **kwargs):
        # self.args = args
        # self.kwargs = kwargs
        self.baseURI = 'eventual.technology'
        # self.baseURIObject = None
        self.isConnected = True
        # self.localName = None
        self.namespaceURI = "http://www.w3.org/1999/xhtml"
        self.nextSibling = None
        # self.nodePrincipal = None
        self.outerText = None
        self.ownerDocument = None
        self.parentElement = None
        self.parentNode = None
        self.prefix = None  # 🗑️
        self.previousSibling = None
        self.rootNode = None
        self.textContent = None
        super().__init__()

    def appendChild(self, item):
        """ Adds a new child node, to an element, as the last child node """
        self.args = self.args + (item,)

    def hasChildNodes(self):
        """ Returns true if an element has any child nodes, otherwise false """
        return len(self.args) > 1

    def lastChild(self):
        """ Returns the last child node of an element """
        try:
            return self.args[len(self.args) - 1]
        except Exception:
            return None

    def firstChild(self):
        """ Returns the first child node of an element """
        try:
            return self.args[0]  # TODO - check if this means includes content
        except Exception:
            return None

    def childElementCount(self):
        """ Returns the number of child elements an element has """
        return len(self.args)

    def childNodes(self):
        """ Returns a collection of an element's child nodes (including text and comment nodes) """
        return self.args

    def children(self):
        """ Returns a collection of an element's child element (excluding text and comment nodes) """
        newlist = []
        for each in self.args:
            if(type(each) != str):
                newlist.append(each)
        return newlist

    def nodeType(self):
        """ Returns the node type of a node """
        # pass
        return 1

    @property
    def localName(self):
        return self.tagName

    @property
    def nodeName(self):
        """ Returns the name of a node """
        return self.tagName.upper()

    def nodeValue(self):
        """ Sets or returns the value of a node """
        pass

    # - TODO - tests all below

    def contains(self, node):
        """ Check whether a node is a descendant of a given node """
        # this will go crunch on big stuff... need to consider best way
        for each in self.args:
            if each == node:
                return True
            try:
                if each.contains(node):
                    return True
            except Exception as e:
                pass  # TODO - dont iterate strings

        return False

    def insertBefore(self, node):
        """ inserts a node before a reference node as a child of a specified parent node. """
        for count, each in enumerate(self.args):
            if each == node:
                self.args.insert(node, count)
                return node
        return node

    def removeChild(self, node):
        ''' removes a child node from the DOM and returns the removed node.'''
        for count, each in enumerate(self.args):
            if each == node:
                n = node
                self.args.remove(node)
                return n

            r = each.removeChild(node)
            if r:
                return r

        return None

    def replaceChild(self, newChild, oldChild):
        ''' Replaces a child node within the given (parent) node. '''
        for count, each in enumerate(self.args):
            if each == oldChild:
                n = oldChild
                self.removeChild(newChild)
                self.args.remove(oldChild)
                self.args.insert(count, newChild)
                return n

            r = each.replaceChild(newChild, oldChild)
            if r:
                return r

        return None

    def cloneNode(self, deep=True):
        ''' Returns a copy. '''
        import copy
        if deep:
            return copy.deepcopy(self)
        else:
            return copy.copy(self)  # shallow copy

    def isSameNode(self, node):
        ''' Checks if two elements are the same node '''
        return (self == node)

    def isEqualNode(self, node):
        ''' Checks if two elements are equal '''
        return (str(self) == str(node))

        # compareDocumentPosition()
        # getRootNode()
        # isDefaultNamespace()
        # lookupNamespaceURI()
        # lookupPrefix()
        # normalize()

    # def isSupported(self): return False #  🗑
    # getUserData() 🗑️
    # setUserData() 🗑️


class Console(object):

    @staticmethod
    def log(msg: str, substitute=None):
        """log

        prints a message to the console

        Args:
            msg (str): msg to log
            substitute (str): replace %s with this
        """
        if substitute is not None:
            msg = substitute.join(msg.split('%s'))
        print(msg)

    def __init__(self, *args, **kwargs):
        # self.args = args
        # self.kwargs = kwargs
        # self.log = lambda msg : print(msg)
        # assert()
        # clear()
        # count()
        # error()
        # group()
        # groupCollapsed()
        # groupEnd()
        # info()
        # table()
        # time()
        # timeEnd()
        # trace()
        # warn()
        pass


console = Console


class Attr(object):

    def __init__(self, name, *args, **kwargs):
        # self.isId
        self.name = name
        self.value = ""
        # self.value = value
        # self.specified


class Element(Node):
    """ Baseclass for all html tags """

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

        self.tagName
        self.style = None  # Style(self)  # = #'test'#Style()
        super().__init__()

    # def accessKey( key: str ): -> None
        # ''' Sets or returns the accesskey attribute of an element'''
        # return
        # example
        # dom.getElementById("myAnchor").accessKey = "w";

    def attributes(self) -> List:
        """ Returns a List of an element's attributes """
        return self.attributes

    @property
    def innerHTML(self) -> str:
        """ Sets or returns the content of an element """
        # self.args = args
        return self.content

    @innerHTML.setter
    def innerHTML(self, value):
        if value is not None:
            self.args = (value,)  # TODO - will need the parser to work for this to work properly. for now shove all on first content node
        return self.content

    def html(self, *args) -> str:
        self.args = args
        return self

    def blur(self):
        """ Removes focus from an element """
        pass

    @property
    def classList(self):
        """ Sets or returns the value of the classList attribute of an element """
        return self.getAttribute('class').split(' ')

    @classList.setter
    def classList(self, newname: str):
        """ Sets or returns the value of the classList attribute of an element """
        # self.setAttribute('class', newid)
        return

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
        evt = Event('click')
        return self.dispatchEvent(evt)

    def clientHeight(self):
        """ Returns the height of an element, including padding """
        return self.style.height + self.style.paddingTop + self.style.paddingBottom

    def clientLeft(self):
        """ Returns the width of the left border of an element """
        return self.style.left

    def clientTop(self):
        """ Returns the width of the top border of an element """
        return self.style.top

    def clientWidth(self):
        """ Returns the width of an element, including padding """
        return self.style.width + self.style.paddingLeft + self.style.paddingRight

    def compareDocumentPosition(self):
        """ Compares the document position of two elements """
        pass

    def contentEditable(self):
        """ Sets or returns whether the content of an element is editable or not """
        pass

    def dir(self):
        """ Sets or returns the value of the dir attribute of an element """
        pass

    def exitFullscreen(self):
        """ Cancels an element in fullscreen mode """
        pass

    def firstElementChild(self):
        """ Returns the first child element of an element """
        pass

    def focus(self):
        """ Gives focus to an element """
        pass

    def getAttribute(self, attribute: str) -> str:
        '''Returns the specified attribute value of an element node'''
        try:

            if attribute[0:1] != '_':
                attribute = '_' + attribute

            return self.kwargs[attribute]
        except Exception as e:
            print('failed to get attribute')
            print(e)
            return None

    def getAttributeNode(self, attribute: str) -> str:
        '''Returns the specified attribute node'''
        try:
            return f"{attribute}={self.kwargs[attribute]}"
        except Exception as e:
            print('failed to get attribute')
            print(e)
            return ''

    def getBoundingClientRect(self):
        '''Returns the size of an element and its position relative to the viewport'''
        pass

    def getElementsByClassName(self):
        '''Returns a collection of all child elements with the specified class name'''
        pass

    def getElementsByTagName(self, tag: str) -> List:
        ''' Returns a collection of all child elements with the specified tag name '''
        reg = f"(<{tag}.*?>.+?</{tag}>)"

        closed_tags = ["base", "link", "meta", "hr", "br", "wbr", "img", "embed", "param", "source", "track", "area", "col", "input", "keygen", "command"]
        if tag in closed_tags:
            reg = f"(<{tag}.*?/>)"

        pattern = re.compile(reg)
        tags = re.findall(pattern, str(self))
        return tags

    def hasAttribute(self, attribute: str) -> str:
        '''Returns true if an element has the specified attribute, otherwise false'''
        try:

            if attribute[0:1] != '_':
                attribute = '_' + attribute

            return attribute in self.kwargs.keys()
        except Exception as e:
            print('failed to get attribute')
            print(e)
            return False

    def hasAttributes(self) -> bool:
        '''Returns true if an element has any attributes, otherwise false'''
        if len(self.kwargs) > 0:
            return True
        else:
            return False

    @property
    def id(self):
        ''' Sets or returns the value of the id attribute of an element'''
        return self.getAttribute('id')

    @id.setter
    def id(self, newid: str):
        ''' Sets or returns the value of the id attribute of an element'''
        self.setAttribute('id', newid)

    def innerText(self):
        ''' Sets or returns the text content of a node and its descendants'''
        return ''.join([each.__str__() for each in self.args])

    def insertAdjacentElement(self):
        '''Inserts a HTML element at the specified position relative to the current element'''
        pass

    def insertAdjacentHTML(self):
        '''Inserts a HTML formatted text at the specified position relative to the current element'''
        pass

    def insertAdjacentText(self):
        '''Inserts text into the specified position relative to the current element'''
        pass

    def isContentEditable(self):
        ''' Returns true if the content of an element is editable, otherwise false'''
        pass

    def isDefaultNamespace(self):
        '''Returns true if a specified namespaceURI is the default, otherwise false'''
        pass

    # def lang(self):
        ''' Sets or returns the value of the lang attribute of an element'''
        # pass

    def lastElementChild(self):
        ''' Returns the last child element of an element'''
        pass

    def namespaceURI(self):
        ''' Returns the namespace URI of an element'''
        pass

    def nextSibling(self):
        ''' Returns the next node at the same node tree level'''
        pass

    def nextElementSibling(self):
        ''' Returns the next element at the same node tree level'''
        pass

    def normalize(self):
        '''Joins adjacent text nodes and removes empty text nodes in an element'''
        pass

    def offsetHeight(self):
        ''' Returns the height of an element, including padding, border and scrollbar'''
        pass

    def offsetWidth(self):
        ''' Returns the width of an element, including padding, border and scrollbar'''
        pass

    def offsetLeft(self):
        ''' Returns the horizontal offset position of an element'''
        pass

    def offsetParent(self):
        ''' Returns the offset container of an element'''
        pass

    def offsetTop(self):
        ''' Returns the vertical offset position of an element'''
        pass

    def ownerDocument(self):
        ''' Returns the root element (document object) for an element'''
        pass

    def parentNode(self):
        ''' Returns the parent node of an element'''
        pass

    def parentElement(self):
        ''' Returns the parent element node of an element'''
        pass

    def previousSibling(self):
        ''' Returns the previous node at the same node tree level'''
        pass

    def previousElementSibling(self):
        ''' Returns the previous element at the same node tree level'''
        pass

    def querySelector(self):
        '''Returns the first child element that matches a specified CSS selector(s) of an element'''
        pass

    def querySelectorAll(self):
        '''Returns all child elements that matches a specified CSS selector(s) of an element'''
        pass

    def remove(self):
        '''Removes the element from the DOM'''
        pass

    def removeAttribute(self, attribute: str):
        '''Removes a specified attribute from an element'''
        try:

            if attribute[0:1] != '_':
                attribute = '_' + attribute

            del self.kwargs[attribute]
        except Exception as e:
            print('failed to remove!', e)
            pass

    def removeAttributeNode(self):
        '''Removes a specified attribute node, and returns the removed node'''
        pass

    def requestFullscreen(self):
        '''Shows an element in fullscreen mode'''
        pass

    def scrollHeight(self):
        ''' Returns the entire height of an element, including padding'''
        pass

    def scrollIntoView(self):
        '''Scrolls the specified element into the visible area of the browser window'''
        pass

    def scrollLeft(self):
        ''' Sets or returns the number of pixels an element's content is scrolled horizontally'''
        pass

    def scrollTop(self):
        ''' Sets or returns the number of pixels an element's content is scrolled vertically'''
        pass

    def scrollWidth(self):
        ''' Returns the entire width of an element, including padding'''
        pass

    def setAttribute(self, attribute, value):
        '''Sets or changes the specified attribute, to the specified value'''
        try:
            if attribute[0:1] != '_':
                attribute = '_' + attribute

            self.kwargs[attribute] = value
        except Exception as e:
            print('failed to set attribute', e)

    def setAttributeNode(self, attr):
        ''' Sets or changes the specified attribute node '''
        self.setAttribute(attr.name, attr.value)

    @property
    def style(self):
        ''' returns the value of the style attribute of an element'''
        if self.__style is None:
            self.style = Style()
        return self.__style

    @style.setter
    def style(self, style):
        self.__style = style
        self.__style.__init__(self)  # to set the parent

    # def tabIndex(self):
        ''' Sets or returns the value of the tabindex attribute of an element'''
        # pass

    @property
    def tagName(self):
        return self.name

    def textContent(self):
        ''' Sets or returns the textual content of a node and its descendants'''
        # pass
        # def __str__(self):

        # TODO - not finished. this wont work
        return f" {' '*len(self.name)}{' '*len(self.attributes)} {self.content}  {' '*len(self.name)} "

    @property
    def title(self):
        ''' Sets or returns the value of the title attribute of an element'''
        return self.getAttribute('title')

    @title.setter
    def title(self, newtitle: str):
        ''' Sets or returns the value of the title attribute of an element'''
        self.setAttribute('title', newtitle)

    def toString(self):
        '''Converts an element to a string'''
        pass


class Document(Element):
    """ Baseclass for the html tag """

    def __init__(self, *args, **kwargs):
        # self.doc = doc
        # self.uri = uri
        # self.args = args
        # self.kwargs = kwargs
        # self.documentURI = uri
        # self._documentElement
        # self.raw
        self.body = ""  # ??
        pass

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.__init__(*args, **kwargs)
        instance.documentElement = instance
        instance.URL = domonic.javascript.URL().href
        instance.baseURI = domonic.javascript.URL().href
        return instance

    # TODO - still not great as it also returns 'links' when searching for 'li'
    # @property
    def _get_tags(self, tag):
        ''' returns the tags you want '''
        reg = f"(<{tag}.*?>.+?</{tag}>)"

        closed_tags = ["base", "link", "meta", "hr", "br", "wbr", "img", "embed", "param", "source", "track", "area", "col", "input", "keygen", "command"]
        if tag in closed_tags:
            reg = f"(<{tag}.*?/>)"

        pattern = re.compile(reg)
        tags = re.findall(pattern, str(self))
        return tags

    # def activeElement():
        ''' Returns the currently focused element in the document'''
        # return

    # def adoptNode():
        '''Adopts a node from another document'''
        # return

    def anchors(self):
        ''' Returns a collection of all <a> elements in the document that have a name attribute'''
        tags = self._get_tags('a')
        return [x for x in tags if x.hasAttribute('name')]

    def applets(self):
        ''' Returns a collection of all <applet> elements in the document'''
        return

    @property
    def body(self):
        ''' Sets or returns the document's body (the <body> element)'''
        # print("TESTING:::")
        # print(self)
        tag = "body"
        reg = f"(<{tag}.*?>.+?</{tag}>)"
        pattern = re.compile(reg)
        tags = re.findall(pattern, str(self))
        return tags[0]

    @body.setter
    def body(self, content):
        ''' Sets or returns the document's body (the <body> element)'''
        # tag = "body"
        # reg = f"<{tag}.*?>(.+?)</{tag}>"
        # pattern = re.compile(reg)
        # tags = re.findall(pattern,html)
        # return tags[0]
        print("TODO - setter method on body")
        return

    # def close():
        '''Closes the output stream previously opened with document.open()'''
        # return

    # def cookie():
        ''' Returns all name/value pairs of cookies in the document'''
        # return

    # def charset():
        ''' Deprecated. Use characterSet instead. Returns the character encoding for the document'''
        # return

    # def characterSet():
        ''' Returns the character encoding for the document'''
        # return

    @staticmethod
    def createAttribute(name):
        ''' Creates an attribute node '''
        return Attr(name)

    @staticmethod
    def createComment(message):
        '''Creates a Comment node with the specified text'''
        from domonic.html import comment
        return comment(message)

    # def createDocumentFragment():
        '''Creates an empty DocumentFragment node'''
        # return

    @staticmethod
    def createElement(_type):
        ''' Creates an Element node - WARNING THIS WILL NOT CREATE A 'DOMONIC ELEMENT' (yet), so it wont have features '''
        # TODO - self closing tags - need a 'tag' factory. need the tags in .html package to register with it.
        from domonic.html import tag, tag_init
        el = type(_type, (tag, Element), {'name': _type, '__init__': tag_init})
        return el()

    @staticmethod
    def createEvent(event_type=None):
        '''Creates a new event'''
        if event_type == "MouseEvent":
            return MouseEvent()
        elif event_type == "KeyboardEvent":
            return MouseEvent()
        elif event_type == None:
            return Event()
        return Event()

    # def createTextNode():
        '''Creates a Text node'''
        # return

    # def defaultView(self):
        ''' Returns the window object associated with a document, or null if none is available.'''
        # return

    # def designMode(self):
        ''' Controls whether the entire document should be editable or not.'''
        # return

    def doctype(self):
        ''' Returns the Document Type Declaration associated with the document'''
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

    def embeds(self):
        ''' Returns a collection of all <embed> elements the document'''
        return

    # def execCommand(self):
        '''Invokes the specified clipboard operation on the element currently having focus.'''
        # return

    @property
    def forms(self):
        ''' Returns a collection of all <form> elements in the document'''
        tag = "form"
        reg = f"(<{tag}.*?>.+?</{tag}>)"
        pattern = re.compile(reg)
        tags = re.findall(pattern, str(self))
        return tags

    # def fullscreenElement():
        ''' Returns the current element that is displayed in fullscreen mode'''
        # return

    # def fullscreenEnabled():
        '''Returns a Boolean value indicating whether the document can be viewed in fullscreen mode'''
        # return

    def getElementById(self):
        '''Returns the element that has the ID attribute with the specified value'''
        return

    def getElementsByClassName(self):
        '''Returns a NodeList containing all elements with the specified class name'''
        return

    def getElementsByName(self):
        '''Returns a NodeList containing all elements with a specified name'''
        return

    # def hasFocus():
        '''Returns a Boolean value indicating whether the document has focus'''
        # return

    def head(self):
        ''' Returns the <head> element of the document'''
        return

    @property
    def images(self):
        ''' Returns a collection of all <img> elements in the document'''
        tag = "img"
        reg = f"(<{tag}.*?/>)"
        pattern = re.compile(reg)
        tags = re.findall(pattern, str(self))
        return tags

    # def implementation():
        ''' Returns the DOMImplementation object that handles this document'''
        # return

    # def importNode():
        '''Imports a node from another document'''
        # return

    # def inputEncoding():
        ''' Returns the encoding, character set, used for the document'''
        # return

    # def lastModified():
        ''' Returns the date and time the document was last modified'''
        # return

    def links(self):
        ''' Returns a collection of all <a> and <area> elements in the document that have a href attribute'''
        tag = "a"
        reg = f"(<{tag}.*?/>)"
        pattern = re.compile(reg)
        tags = re.findall(pattern, str(self))
        return tags

    def normalize(self):
        '''Removes empty Text nodes, and joins adjacent nodes'''
        return

    def normalizeDocument(self):
        '''Removes empty Text nodes, and joins adjacent nodes'''
        return

    # def open(self):
        '''Opens an HTML output stream to collect output from document.write()'''
        # return

    def querySelector(self):
        '''Returns the first element that matches a specified CSS selector(s) in the document'''
        return

    def querySelectorAll(self):
        '''Returns a static NodeList containing all elements that matches a specified CSS selector(s) in the document'''
        return

    # def readyState(self):
        ''' Returns the (loading) status of the document'''
        # return

    # def referrer():
        ''' Returns the URL of the document that loaded the current document'''
        # return

    def renameNode(self, node, namespaceURI, nodename):
        '''Renames the specified node'''
        return

    @property
    def scripts(self):
        ''' Returns a collection of <script> elements in the document'''
        tag = "script"
        reg = f"(<{tag}.*?>.+?</{tag}>)"
        pattern = re.compile(reg)
        tags = re.findall(pattern, str(self))
        return tags

    # def strictErrorChecking():
        ''' Sets or returns whether error-checking is enforced or not'''
        # return

    @property
    def title(self) -> str:
        ''' Sets or returns the title of the document'''
        try:
            tag = "title"
            reg = f"(<{tag}.*?>.+?</{tag}>)"
            pattern = re.compile(reg)
            tags = re.findall(pattern, str(self))
            return tags[0]
        except Exception as e:
            print('document has no title', e)
            return ''

    # def URL(self):
    #     ''' Returns the full URL of the HTML document'''
    #     pass

    def write(self, html: str = "") -> None:
        '''Writes HTML expressions or JavaScript code to a document'''
        # doc = html
        from .html import tag
        tag.__init__(self, html)
        # super(tag).__init__(html)

    def writeln(self, html: str = "") -> None:
        '''Same as write(), but adds a newline character after each statement'''
        # doc = html
        pass


document = Document
# doc = Document


class Location():

    def __init__(self, *args, **kwargs):
        pass

    def __str__(self):
        return self.href

    # def __repr__(self):
    #     return self.uri

    def origin(self):
        ''' Returns the protocol, hostname and port number of a URL'''
        return

    def search(self):
        ''' Sets or returns the querystring part of a URL'''
        return

    def assign(self, url: str = "") -> None:
        '''Loads a new document'''
        # TODO - if different download?
        # dom.baseURI = url
        pass

    def reload(self):
        '''Reloads the current document'''
        return

    def replace(self):
        '''Replaces the current document with a new one'''
        return


location = Location


class dom(object):  # don't think this class is need now as the package is the 'dom'
    console = type('console', (console,), {'name': 'console'})
    location = type('location', (location,), {'name': 'location'})
    document = type('document', (document,), {'name': 'document'})

    # @property
    # def location(self):
    #     print("! ===== ======= ============= ================= ============= !")
    #     return self.location

    # @location.setter
    # def location(self, uri: str):
    #     print("! ====== =========== ============== ============ ============ !")
    #     self.location.uri = uri

    @property
    def console(self):
        return self._console

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

        # self.console = dom.console

        # self.location = type('location', (location,), {'name':'location'})
        self.console = type('console', (dom.console,), {'name': 'console'})
        # self.doc = type('document', (DOM,), {'name':'document'})

        # self.attr = type('attribute', (DOM,), {'name':'attribute'})
        # self.el = type('element', (DOM,), {'name':'element'})
        # self.events = type('events', (DOM,), {'name':'events'})
        # self.event.Objects
        # self.geo = type('geo', (DOM,), {'name':'geo'})
        # self.history = type('history', (DOM,), {'name':'history'})
        # self.HTMLCollection
        # self.location = type('location', (DOM,), {'name':'location'})
        # self.navigator = type('navigator', (DOM,), {'name':'navigator'})
        # self.screen = type('screen', (DOM,), {'name':'screen'})
        # self.style = type('style', (DOM,), {'name':'style'})
        # self.window = type('window', (DOM,), {'name':'window'})
        # self.webstorage = type('webstorage', (DOM,), {'name':'webstorage'})

        # self.element = self.el
        # self.document = self.doc
        # self.attribute = self.attr
        pass

    # def __str__(self):
        # return "<!DOCTYPE html>"
