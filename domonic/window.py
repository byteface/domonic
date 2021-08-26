"""
    domonic.window
    ====================================

    the new home for window

"""

from domonic.javascript import Window
from domonic.dom import *
from domonic.dom import document


class Window(Window):

    def __init__(self):
        self.customElements = CustomElementsRegistry()
        self.document = document
        super().__init__()

    @propoerty
    def document(self):
        from domonic.dom import document
        return document



# WINDOW
# localStorage  Allows to save key/value pairs in a web browser. Stores the data with no expiration date    Window
# blur()    Removes focus from an element   Element, Window
# closed    Returns a Boolean value indicating whether a window has been closed or not  Window
# close()   Closes the output stream previously opened with document.open() Document, Window
# confirm() Displays a dialog box with a message and an OK and a Cancel button  Window
# defaultStatus Sets or returns the default text in the statusbar of a window   Window
# defaultView   Returns the window object associated with a document, or null if none is available. Document
# document  Returns the Document object for the window (See Document object)    Window
# focus()   Gives focus to an element   Element, Window
# frameElement  Returns the <iframe> element in which the current window is inserted    Window
# getComputedStyle()    Gets the current computed CSS styles applied to an element  Window
# getSelection()    Returns a Selection object representing the range of text selected by the user  Window
# history   Returns the History object for the window (See History object)  Window
# innerHeight   Returns the height of the window's content area (viewport) including scrollbars Window
# innerWidth    Returns the width of a window's content area (viewport) including scrollbars    Window
# location  Returns the Location object for the window (See Location object)    Window
# matchMedia()  Returns a MediaQueryList object representing the specified CSS media query string   Window
# moveBy()  Moves a window relative to its current position Window
# moveTo()  Moves a window to the specified position    Window
# name  Sets or returns an error name   Error, Attribute, Window
# navigator Returns the Navigator object for the window (See Navigator object)  Window
# onpopstate    The event occurs when the window's history changes  PopStateEvent
# open()    Opens an HTML output stream to collect output from document.write() Document, Window
# opener    Returns a reference to the window that created the window   Window
# outerHeight   Returns the height of the browser window, including toolbars/scrollbars Window
# outerWidth    Returns the width of the browser window, including toolbars/scrollbars  Window
# pageXOffset   Returns the pixels the current document has been scrolled (horizontally) from the upper left corner of the window   Window
# pageYOffset   Returns the pixels the current document has been scrolled (vertically) from the upper left corner of the window Window
# parent    Returns the parent window of the current window Window
# _print()   Prints the content of the current window    Window
# resizeBy()    Resizes the window by the specified pixels  Window
# resizeTo()    Resizes the window to the specified width and height    Window
# screen    Returns the Screen object for the window (See Screen object)    Window
# screenLeft    Returns the horizontal coordinate of the window relative to the screen  Window
# screenTop Returns the vertical coordinate of the window relative to the screen    Window
# scroll()  Deprecated. This method has been replaced by the scrollTo() method. Window
# scrollBy()    Scrolls the document by the specified number of pixels  Window
# scrollIntoView()  Scrolls the specified element into the visible area of the browser window   Element
# scrollTo()    Scrolls the document to the specified coordinates   Window
# scrollX   An alias of pageXOffset Window
# scrollY   An alias of pageYOffset Window
# sessionStorage    Allows to save key/value pairs in a web browser. Stores the data for one session    Window
# stop()    Stops the window from loading   Window
# status    Sets or returns the text in the statusbar of a window   Window
# top   Returns the topmost browser window  Window
# view  Returns a reference to the Window object where the event occurred   UiEvent

# TODO - play with this
class CustomElementRegistry():
    """ The CustomElementRegistry interface provides methods for registering custom elements and querying registered elements. 
    To get an instance of it, use the window.customElements property. """

    def __init__(self):
        self.store = {}

    # Defines a new custom element.
    def define(self, name, constructor, options=None):
        """[defines a new custom element.]

        Args:
            name ([str]): [Name for the new custom element. Note that custom element names must contain a hyphen.]
            constructor ([type]): [Constructor for the new custom element.]
            options ([dict]): [Object that controls how the element is defined. One option is currently supported: extends]
        """
        if '-' not in name:
            raise ValueError('Invalid custom element name. Must contain hypen: ' + name)
        # el = document.createElement(name)
        # el.constructor = constructor
        from domonic.html import tag
        from domonic.dom import Element
        el = type(name, (tag, Element), {'name': name, '__init__': constructor})
        if options is not None:
            if 'extends' in options:
                el.extends = options['extends']
        self.store[name] = el
        return el

    def get(self, name):
        """
            Returns the constructor for the named custom element,
            or undefined if the custom element is not defined.
        """
        # see if its in the store or return none
        if name in self.store:
            return self.store[name]
        else:
            return None

    # Upgrades a custom element directly, even before it is connected to its shadow root.
    def upgrade(self):
        pass

    # Returns an empty promise that resolves when a custom element becomes defined with the given name.
    # If such a custom element is already defined, the returned promise is immediately fulfilled.
    def whenDefined(self):
        pass
