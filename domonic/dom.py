"""
    domonic.dom
    ~~~~~~~~~

    methods on the dom

"""

from typing import *
import re

class Event(object):

    def __init__(self):
        self.bubbles = None
        self.cancelable = None
        self.cancelBubble = None
        self.composed = None
        self.currentTarget = None
        self.defaultPrevented = False
        self.eventPhase = None
        self.explicitOriginalTarget = None
        self.isTrusted = None
        self.originalTarget = None
        self.returnValue = None
        self.srcElement = None
        self.target = None
        self.timeStamp = None
        self.type = None

        # composedPath
        # createEvent
        # initEvent
        # msConvertURL()
        # preventDefault
        # stopImmediatePropagation
        # stopPropagation


class EventTarget:

    def __init__(self):
        self.listeners = {}

    # TODO - event: str, function, useCapture: bool
    def addEventListener(self, _type, callback):
        if _type not in self.listeners:
            self.listeners[_type] = []
        self.listeners[_type].append(callback)

    def removeEventListener(self, _type, callback):
        if _type not in self.listeners:
            return

        stack = self.listeners[_type]

        for thing in stack:
            if thing == callback:
                # stack.splice(i, 1)
                stack.remove(thing)
                return

    def dispatchEvent(self, event):
        if event._type not in self.listeners:
            return True

        stack = self.listeners[event._type]#.slice()

        for thing in stack:
            thing(event)
            # type(thing, (Event,), self) 

        return not event.defaultPrevented


class Node(EventTarget):

    def __init__(self, *args, **kwargs):
        # self.args = args
        # self.kwargs = kwargs
        self.baseURI = 'eventual.technology'
        self.baseURIObject = None
        self.childNodes = None
        self.firstChild = None
        self.isConnected = None
        self.lastChild = None
        self.localName = None
        self.namespaceURI = None
        self.nextSibling = None
        self.nodeName = None
        self.nodePrincipal = None
        self.nodeType = None
        self.nodeValue = None
        self.outerText = None
        self.ownerDocument = None
        self.parentElement = None
        self.parentNode = None
        self.prefix = None
        self.previousSibling = None
        self.rootNode = None
        self.textContent = None
        pass

        # appendChild() # TODO - append.?.< why missed?
        # cloneNode()
        # compareDocumentPosition()
        # contains()
        # getRootNode()
        # getUserData()
        # hasChildNodes()
        # insertBefore()
        # isDefaultNamespace()
        # isEqualNode()
        # isSameNode()
        # isSupported()
        # lookupNamespaceURI()
        # lookupPrefix()
        # normalize()
        # removeChild()
        # replaceChild()
        # setUserData()


class Console(object):

    log = lambda msg : print(msg)

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








class Element(Node):

    def __init__(self, *args, **kwargs):
        self.content = None
        self.attributes = None
        pass

    # def accessKey( key: str ): -> None
        # ''' Sets or returns the accesskey attribute of an element'''
        # return        
        # example
        # dom.getElementById("myAnchor").accessKey = "w";

    def addEventListener(self, event: str, function, useCapture: bool) -> None:
        '''Attaches an event handler to the specified element'''
        # return
        # example
        # document.getElementById("myBtn").addEventListener("click", function(){
        #   document.getElementById("demo").innerHTML = "Hello World";
        # });
        pass

    def appendChild(self, item):
        '''Adds a new child node, to an element, as the last child node'''
        # self.content = self.content + item.__str__()
        # return
        pass

    def attributes(self) -> List :
        ''' Returns a List of an element's attributes'''
        return self.attributes

    def innerHTML(self, *args) -> str :
        ''' Sets or returns the content of an element'''
        self.content = ''.join([each.__str__() for each in args])
        return self.content

    def html(self, *args) -> str : return self.innerHTML(*args) # jquery

    def blur(self):
        '''Removes focus from an element'''
        pass
    def childElementCount(self):
        ''' Returns the number of child elements an element has'''
        pass
    def childNodes(self):
        ''' Returns a collection of an element's child nodes (including text and comment nodes)'''
        pass
    def children(self):
        ''' Returns a collection of an element's child element (excluding text and comment nodes)'''
        pass
    def classList(self):
        ''' Returns the class name(s) of an element'''
        pass
    def className(self):
        ''' Sets or returns the value of the class attribute of an element'''
        pass
    def click(self):
        '''Simulates a mouse-click on an element'''
        pass
    
    def clientHeight(self):
        ''' Returns the height of an element, including padding'''
        pass

    def clientLeft(self):
        ''' Returns the width of the left border of an element'''
        pass
    def clientTop(self):
        ''' Returns the width of the top border of an element'''
        pass
    def clientWidth(self):
        ''' Returns the width of an element, including padding'''
        pass
    def cloneNode(self):
        '''Clones an element'''
        pass

    def compareDocumentPosition(self):
        '''Compares the document position of two elements'''
        pass

    def contains(self):
        '''Returns true if a node is a descendant of a node, otherwise false'''
        pass

    def contentEditable(self):
        ''' Sets or returns whether the content of an element is editable or not'''
        pass

    def dir(self):
        ''' Sets or returns the value of the dir attribute of an element'''
        pass

    def exitFullscreen(self):
        '''Cancels an element in fullscreen mode'''
        pass

    def firstChild(self):
        ''' Returns the first child node of an element'''
        pass

    def firstElementChild(self):
        ''' Returns the first child element of an element'''
        pass

    def focus(self):
        '''Gives focus to an element'''
        pass

    def getAttribute(self, attribute: str) -> str:
        '''Returns the specified attribute value of an element node'''
        try:
            return self.kwargs[attribute]
        except Exception as e:
            print('failed to get attribute')
            return ''

    def getAttributeNode(self, attribute: str) -> str:
        '''Returns the specified attribute node'''
        try:
            return f"{attribute}={self.kwargs[attribute]}"
        except Exception as e:
            print('failed to get attribute')
            return ''

    def getBoundingClientRect(self):
        '''Returns the size of an element and its position relative to the viewport'''
        pass

    def getElementsByClassName(self):
        '''Returns a collection of all child elements with the specified class name'''
        pass
        
    def getElementsByTagName(self, tag : str) -> List:
        '''Returns a collection of all child elements with the specified tag name'''
        reg = f"(<{tag}.*?>.+?</{tag}>)"

        closed_tags = ["base","link","meta","hr","br","wbr","img","embed","param","source","track","area","col","input","keygen","command"]
        if tag in closed_tags:
            reg = f"(<{tag}.*?/>)"

        pattern = re.compile(reg)
        tags = re.findall(pattern,str(self))
        return tags

    def hasAttribute(self, attribute: str) -> str:
        '''Returns true if an element has the specified attribute, otherwise false'''
        try:
            return f"{attribute}={self.kwargs[attribute]}"
        except Exception as e:
            print('failed to get attribute')
            return ''

    def hasAttributes(self) -> bool:
        '''Returns true if an element has any attributes, otherwise false'''
        if len(self.kwargs)>0:
            return True
        else:
            return False

    def hasChildNodes(self):
        '''Returns true if an element has any child nodes, otherwise false'''
        pass

    def id(self):
        ''' Sets or returns the value of the id attribute of an element'''
        pass

    def innerText(self):
        ''' Sets or returns the text content of a node and its descendants'''
        pass

    def insertAdjacentElement(self):
        '''Inserts a HTML element at the specified position relative to the current element'''
        pass

    def insertAdjacentHTML(self):
        '''Inserts a HTML formatted text at the specified position relative to the current element'''
        pass

    def insertAdjacentText(self):
        '''Inserts text into the specified position relative to the current element'''
        pass

    def insertBefore(self):
        '''Inserts a new child node before a specified, existing, child node'''
        pass

    def isContentEditable(self):
        ''' Returns true if the content of an element is editable, otherwise false'''
        pass

    def isDefaultNamespace(self):
        '''Returns true if a specified namespaceURI is the default, otherwise false'''
        pass

    def isEqualNode(self):
        '''Checks if two elements are equal'''
        pass

    def isSameNode(self):
        '''Checks if two elements are the same node'''
        pass

    def isSupported(self):
        '''Returns true if a specified feature is supported on the element'''
        pass

    def lang(self):
        ''' Sets or returns the value of the lang attribute of an element'''
        pass

    def lastChild(self):
        ''' Returns the last child node of an element'''
        pass

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

    def nodeName(self):
        ''' Returns the name of a node'''
        pass

    def nodeType(self):
        ''' Returns the node type of a node'''
        pass

    def nodeValue(self):
        ''' Sets or returns the value of a node'''
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

    def removeAttribute(self):
        '''Removes a specified attribute from an element'''
        pass

    def removeAttributeNode(self):
        '''Removes a specified attribute node, and returns the removed node'''
        pass

    def removeChild(self):
        '''Removes a child node from an element'''
        pass

    def removeEventListener(self):
        '''Removes an event handler that has been attached with the addEventListener() method'''
        pass

    def replaceChild(self):
        '''Replaces a child node in an element'''
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

    def setAttribute(self):
        '''Sets or changes the specified attribute, to the specified value'''
        pass

    def setAttributeNode(self):
        '''Sets or changes the specified attribute node'''
        pass

    def style(self):
        ''' Sets or returns the value of the style attribute of an element'''
        pass

    def tabIndex(self):
        ''' Sets or returns the value of the tabindex attribute of an element'''
        pass

    def tagName(self):
        ''' Returns the tag name of an element'''
        pass

    def textContent(self):
        ''' Sets or returns the textual content of a node and its descendants'''
        pass

    def title(self):
        ''' Sets or returns the value of the title attribute of an element'''
        pass

    def toString(self):
        '''Converts an element to a string'''
        pass



class Document(Element):

    # baseURI = "eventual.technology"

    def __init__(self, *args, **kwargs):
        # self.doc = doc
        # self.uri = uri
        # self.args = args
        # self.kwargs = kwargs
        # self.documentURI = uri
        # self.baseURI = ""

        # self.raw
        self.body = "" #???
        pass


    # TODO - still not great as it also returns 'links' when searching for 'li'
    # @property
    def _get_tags(self, tag):
        ''' returns the tags you want '''
        reg = f"(<{tag}.*?>.+?</{tag}>)"

        closed_tags = ["base","link","meta","hr","br","wbr","img","embed","param","source","track","area","col","input","keygen","command"]
        if tag in closed_tags:
            reg = f"(<{tag}.*?/>)"

        pattern = re.compile(reg)
        tags = re.findall(pattern,str(self))
        return tags


    # def activeElement():
        ''' Returns the currently focused element in the document'''
        # return

    # def addEventListener( event: str, function, useCapture: bool ) -> None:
        '''Attaches an event handler to the document'''
        # return

    # def adoptNode():
        '''Adopts a node from another document'''
        # return

    def anchors(self):
        ''' Returns a collection of all <a> elements in the document that have a name attribute'''
        print('hi')
        return

    def applets(self):
        ''' Returns a collection of all <applet> elements in the document'''
        return

    # def baseURI(self):
        ''' Returns the absolute base URI of a document'''
        # return self.uri

    @property
    def body(self):
        ''' Sets or returns the document's body (the <body> element)'''
        # print("TESTING:::")
        # print(self)
        tag = "body"
        reg = f"(<{tag}.*?>.+?</{tag}>)"
        pattern = re.compile(reg)
        tags = re.findall(pattern,str(self))
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

    # def createAttribute():
        '''Creates an attribute node'''
        # return

    # def createComment():
        '''Creates a Comment node with the specified text'''
        # return

    # def createDocumentFragment():
        '''Creates an empty DocumentFragment node'''
        # return

    # def createElement():
        '''Creates an Element node'''
        # return

    # def createEvent():
        '''Creates a new event'''
        # return

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

    def documentElement(self):
        ''' Returns the Document Element of the document (the <html> element)'''
        return

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
             # print(self)
        tag = "form"
        reg = f"(<{tag}.*?>.+?</{tag}>)"
        pattern = re.compile(reg)
        tags = re.findall(pattern,str(self))
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
        tags = re.findall(pattern,str(self))
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
        tags = re.findall(pattern,str(self))
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

    # def removeEventListener():
        '''Removes an event handler from the document (that has been attached with the addEventListener() method)'''
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
        tags = re.findall(pattern,str(self))
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
            tags = re.findall(pattern,str(self))
            return tags[0]
        except Exception as e:
            print('document has no title')
            return ''

    def URL(self):
        ''' Returns the full URL of the HTML document'''
        pass

    def write(self, html: str = "" ) -> None:
        '''Writes HTML expressions or JavaScript code to a document'''
        # doc = html
        pass

    def writeln( self, html: str = "" ) -> None:
        '''Same as write(), but adds a newline character after each statement'''
        # doc = html
        pass


document = Document
# doc = Document


# class Bar(object):
#     def __init__(self):
#         self.value = ''
#     def __get__(self, instance, owner):
#         print "returned from descriptor object"
#         return self.value
#     def __set__(self, instance, value):
#         print "set in descriptor object"
#         self.value = value
#     def __delete__(self, instance):
#         print "deleted in descriptor object"
#         del self.value



class Location(object):

    # href = static_function(document.baseURI)
    href = lambda:Location.some_func()

    @staticmethod
    def some_func(self):
        # ''' Sets or returns the hostname and port number of a URL'''
        print("some_func ran")
        return


    def __init__(self, *args, **kwargs):
        # self.args = args
        # self.kwargs = kwargs
        pass

    # def __str__(self):
    #     return self.uri

    # def __repr__(self):
    #     return self.uri


    ''' Sets or returns the anchor part (#) of a URL'''
    # hash = lambda : dom.baseURI.split("#")[1]

    # host = lambda : dom.baseURI.split(":")[1] if ":" in dom.baseURI else 80

    def host(self):
        # ''' Sets or returns the hostname and port number of a URL'''
        return

    def hostname(self):
        ''' Sets or returns the hostname of a URL'''
        return

    # @property
    # @staticmethod
    # def href(self):
        ''' Sets or returns the entire URL'''
        # return self.uri

    def origin(self):
        ''' Returns the protocol, hostname and port number of a URL'''
        return

    def pathname(self):
        ''' Sets or returns the path name of a URL'''
        return

    def port(self):
        ''' Sets or returns the port number of a URL'''
        return

    def protocol(self):
        ''' Sets or returns the protocol of a URL'''
        return

    def search(self):
        ''' Sets or returns the querystring part of a URL'''
        return

    def assign( self, url: str = "" ) -> None:
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



class dom(object):

    console = type('console', (console,), {'name':'console'})
    document = type('document', (document,), {'name':'document'})
    location = type('location', (location,), {'name':'location'})

    # @property
    # def location(self):
    #     print("====================================================================================")
    #     return self.location

    # @location.setter
    # def location(self, uri: str):
    #     print("================================================!====================================")
    #     self.location.uri = uri

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

        # self.location = type('location', (location,), {'name':'location'})
        # self.console = type('console', (dom.console,), {'name':'console'})
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

    def __str__(self):
        # return "HTML DOM"
        return f"<!DOCTYPE html>"
