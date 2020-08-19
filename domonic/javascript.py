"""    
    domonic.javascript
    ~~~~~~~~~~~~~~~~
    - https://www.w3schools.com/jsref/jsref_reference.asp
"""

# from typing import *
import urllib.parse
from dateutil.parser import parse
import datetime
import time
from urllib.parse import unquote, quote
import math
import random
import typing

# from domonic import dom
# from .dom import *


class js_object(object):

    def valueOf(self):
        """ Returns the primitive value of an array Array, Boolean, Date, Number, String"""
        pass

    # def prototype:
        """ Allows you to add properties and methods to an Array object Array, Boolean, Date"""
        # pass


class Math(js_object):

    # CONSTANTS
    PI = 3.141592653589793
    E = 2.718281828459045
    LN2 = 0.6931471805599453
    LN10 = 2.302585092994046
    LOG2E = 1.4426950408889634
    LOG10E = 0.4342944819032518
    SQRT1_2 = 0.7071067811865476
    SQRT2 = 1.4142135623730951

    # TODO - pass what types of validation?
    # i.e force numbers
    # i.e positive/negative numbers allowed
    # convert bool/string to number?
    def validate(func):
        def validation_decorator(*args, **kwargs):
            for n in args:
                if type(n) != float and type(n) != int:
                    raise ValueError("Value passed was NaN")
            return func(*args)
        return validation_decorator

    @staticmethod
    @validate
    def abs(x):
        """ Returns the absolute value of x """
        return abs(x)

    @staticmethod
    @validate
    def acos(x):
        """ Returns the arccosine of x, in radians """
        return math.acos(x)

    @staticmethod
    @validate
    def acosh(x):
        """ Returns the hyperbolic arccosine of x """
        return math.acosh(x)

    @staticmethod
    @validate
    def asin(x):
        """ Returns the arcsine of x, in radians """
        return math.asin(x)

    @staticmethod
    @validate
    def asinh(x):
        """ Returns the hyperbolic arcsine of x """
        return math.asinh(x)

    @staticmethod
    @validate
    def atan(x):
        """ Returns the arctangent of x as a numeric value between -PI/2 and PI/2 radians """
        return math.atan(x)

    @staticmethod
    @validate
    def atan2(x, y):
        """ Returns the arctangent of the quotient of its arguments """
        return math.atan2(x, y)

    @staticmethod
    @validate
    def atanh(x):
        """ Returns the hyperbolic arctangent of x """
        return math.atanh(x)

    @staticmethod
    @validate
    def cbrt(x):
        """ Returns the cubic root of x """
        # return math.cbrt(x)
        return round(math.pow(x, 1 / 3))

    @staticmethod
    @validate
    def ceil(x):
        """ Returns x, rounded upwards to the nearest integer """
        return math.ceil(x)

    @staticmethod
    @validate
    def cos(x):
        """ Returns the cosine of x (x is in radians) """
        return math.cos(x)

    @staticmethod
    @validate
    def cosh(x):
        """ Returns the hyperbolic cosine of x """
        return math.cosh(x)

    @staticmethod
    @validate
    def exp(x):
        """ Returns the value of Ex """
        return math.exp(x)

    @staticmethod
    @validate
    def floor(x):
        """ Returns x, rounded downwards to the nearest integer """
        return math.floor(x)

    @staticmethod
    @validate
    def log(x, y):
        """ Returns the natural logarithm (base E) of x """
        return math.log(x, y)

    @staticmethod
    @validate
    def max(x, y):
        """ Returns the number with the highest value """
        return max(x, y)

    @staticmethod
    @validate
    def min(x, y):
        """ Returns the number with the lowest value """
        return min(x, y)

    @staticmethod
    @validate
    def random():
        """ Returns a random number between 0 and 1 """
        # return math.random(x)
        return random.random()

    @staticmethod
    @validate
    def round(x):
        """ Rounds x to the nearest integer """
        return round(x)

    @staticmethod
    @validate
    def pow(x, y):
        """ Returns the value of x to the power of y """
        return math.pow(x, y)

    @staticmethod
    @validate
    def sin(x):
        """ Returns the sine of x (x is in radians) """
        return math.sin(x)

    @staticmethod
    @validate
    def sinh(x):
        """ Returns the hyperbolic sine of x """
        return math.sinh(x)

    @staticmethod
    @validate
    def sqrt(x):
        """ Returns the square root of x """
        return math.sqrt(x)

    @staticmethod
    @validate
    def tan(x):
        """ Returns the tangent of an angle """
        return math.tan(x)

    @staticmethod
    @validate
    def tanh(x):
        """ Returns the hyperbolic tangent of a number """
        return math.tanh(x)

    @staticmethod
    @validate
    def trunc(x):
        """ Returns the integer part of a number (x) """
        return math.trunc(x)


# import urllib


class Global(object):

    NaN = "NaN"

    # TODO - https://stackoverflow.com/questions/747641/what-is-the-difference-between-decodeuricomponent-and-decodeuri

    @staticmethod
    def decodeURI(x):
        """ Decodes a URI """
        return unquote(x)

    @staticmethod
    def decodeURIComponent(x):
        """ Decodes a URI component """
        return unquote(x, encoding="utf-8")

    @staticmethod
    def encodeURI(x):
        """ Encodes a URI """
        return quote(str(x), safe='~@#$&()*!+=:;,.?/\'')

    @staticmethod
    def encodeURIComponent(x):
        """ Encodes a URI component """
        return quote(str(x), safe='~()*!.\'')

    # @staticmethod
    # def escape():
        """ Deprecated in version 1.5. Use encodeURI() or encodeURIComponent() """
        # pass

    # @staticmethod
    # def eval():
        """ Evaluates a string and executes it as if it was script code """
        # pass

    # def global

    # def Infinity:
    # pass
    """A numeric value that represents positive/negative infinity """
    # pass

    @staticmethod
    def isFinite():
        """ Determines whether a value is a finite, legal number """
        pass

    @staticmethod
    def isNaN(x):
        """ Determines whether a value is an illegal number """
        if type(x) != float and type(x) != int:
            return True

        # TODO - math.isnan

        return False

    def NaN(self):
        """ "Not-a-Number" value """
        return "NaN"

    @staticmethod
    def Number(x):
        """ Converts an object's value to a number """
        try:
            if type(x) == float or type(x) == int:  # or type(x) == long:
                return x

            if type(x) == str:
                if '.' in x:
                    return float(x)
                else:
                    return int(x)
        except Exception:
            return "NaN"
        return "NaN"

    @staticmethod
    def parseFloat(x):
        """ Parses a string and returns a floating point number """
        return float(x)

    @staticmethod
    def parseInt(x):
        """ Parses a string and returns an integer """
        return int(x)

    @staticmethod
    def String(x):
        """ Converts an object's value to a string """
        return str(x)

    def undefined(self):
        """ Indicates that a variable has not been assigned a value """
        return None

    # @staticmethod
    # def unescape():
        """ Deprecated in version 1.5. Use decodeURI() or decodeURIComponent() instead """
        # pass


class Date(js_object):

    def __init__(self, date: str = None, formatter='python'):
        if date is None:
            self.date = datetime.datetime.now()
        else:
            self.date = self.parse_date(date)

    def parse_date(self, date_string):
        self.date = parse(date_string)
        return self.date

    def getDate(self):
        """ Returns the day of the month (from 1-31) """
        return self.date.day
        # TODO - do for a date object passed in. this only does today

    def getDay(self):
        """  Returns the day of the week (from 0-6) """
        day = self.date.isoweekday()
        return day if (day < 7) else 0
        # TODO - do for a date object passed in. this only does today

    def getFullYear(self):
        """ Returns the year """
        return self.date.now().year

    def getHours(self):
        """  Returns the hour (from 0-23) """
        return self.date.now().hour

    def getMilliseconds(self):
        """ Returns the milliseconds (from 0-999) """
        return round(self.date.now().microsecond / 1000)

    def getMinutes(self):
        """  Returns the minutes (from 0-59) """
        return self.date.now().minute

    def getMonth(self):
        """ Returns the month (from 0-11) """
        return self.date.now().month - 1

    def getSeconds(self):
        """  Returns the seconds (from 0-59) """
        return self.date.now().second

    def getTime(self):
        """ Returns the number of milliseconds since midnight Jan 1 1970, and a specified date """
        return int(str(time.time()).split('.')[0])
        # TODO - whats difference between this and 'now()' ?

    # def getTimezoneOffset(self):
        """ Returns the time difference between UTC time and local time, in minutes """
        # pass

    def getUTCDate(self):
        """ Returns the day of the month, according to universal time (from 1-31) """
        pass

    def getUTCDay(self):
        """ Returns the day of the week, according to universal time (from 0-6) """
        pass

    def getUTCFullYear(self):
        """ Returns the year, according to universal time """
        return self.date.utcnow().year

    def getUTCHours(self):
        """ Returns the hour, according to universal time (from 0-23) """
        return self.date.utcnow().hour

    def getUTCMilliseconds(self):
        """ Returns the milliseconds, according to universal time (from 0-999) """
        pass

    def getUTCMinutes(self):
        """ Returns the minutes, according to universal time (from 0-59) """
        return self.date.utcnow().minute

    def getUTCMonth(self):
        """ Returns the month, according to universal time (from 0-11) """
        return self.date.utcnow().month - 1

    def getUTCSeconds(self):
        """ Returns the seconds, according to universal time (from 0-59) """
        return self.date.utcnow().second

    def getYear(self):
        """ Deprecated. Use the getFullYear() method instead """
        return self.date.now().year

    def now(self):
        """ Returns the number of milliseconds since midnight Jan 1, 1970 """
        return round(time.time() * 1000)

    # def onstorage(self):
        """ The event occurs when a Web Storage area is updated StorageEvent"""
        # pass

    # def ontimeupdate(self):
        """ The event occurs when the playing position has changed (like when the user fast forwards to a different point in the media) Event"""
        # pass

    def parse(self, date_string):
        """ Parses a date string and returns the number of milliseconds since January 1, 1970 """
        self.date = self.parse_date(str(date_string))
        # return self.date.getTime()

    def setDate(self, day):
        """ Sets the day of the month of a date object """
        self.date.replace(day=int(day))
        # return self.date.getTime()

    def setFullYear(self, year):
        """ Sets the year of a date object """
        self.date.replace(year=int(year))
        # return self.date.getTime()

    def setHours(self, hours):
        """ Sets the hour of a date object """
        self.date.replace(hour=int(hours))
        # return self.date.getTime()

    # def setItem(self):
        """ Adds that key to the storage, or update that key's value if it already exists   Storage"""
        # pass

    def setMilliseconds(self, milliseconds):
        """ Sets the milliseconds of a date object """
        # self.date.replace(millisecond=int(milliseconds))
        # return self.now()
        print('TODO: setMilliseconds')
        pass

    # TODO - , seconds = None, milliseconds = None):
    def setMinutes(self, minutes):
        """  Set the minutes of a date object """
        self.date.replace(minute=int(minutes))
        # return self.now()

    def setMonth(self, month):
        """ Sets the month of a date object """
        self.date.replace(month=int(month))
        # return self.now()

    def setSeconds(self, seconds):
        """ Sets the seconds of a date object """
        self.date.replace(second=int(seconds))
        # return self.now()

    def setTime(self):
        """ Sets a date to a specified number of milliseconds after/before January 1, 1970 """
        pass

    def setUTCDate(self, day):
        """  Sets the day of the month of a date object, according to universal time """
        self.setDate(day)
        # return self.getTime()

    def setUTCFullYear(self, year):
        """  Sets the year of a date object, according to universal time """
        self.setFullYear(year)
        # return self.getTime()

    def setUTCHours(self, hour):
        """ Sets the hour of a date object, according to universal time """
        self.setHours(hour)
        # return self.getTime()

    def setUTCMilliseconds(self, milliseconds):
        """  Sets the milliseconds of a date object, according to universal time """
        self.setMilliseconds(milliseconds)
        # return self.getTime()

    def setUTCMinutes(self, minutes):
        """   Set the minutes of a date object, according to universal time """
        self.setMinutes(minutes)
        # return self.getTime()

    def setUTCMonth(self, month):
        """ Sets the month of a date object, according to universal time """
        self.setMonth(month)
        # return self.getTime()

    def setUTCSeconds(self, seconds):
        """   Set the seconds of a date object, according to universal time """
        self.setSeconds(seconds)
        # return self.getTime()

    def setYear(self, year):
        """ Deprecated. Use the setFullYear() method instead """
        self.date.replace(year=int(year))
        # return self.getTime()
        # TODO - there may not be a date object already?

    def toDateString(self):
        """ Converts the date portion of a Date object into a readable string """
        pass

    def toGMTString(self):
        """ Deprecated. Use the toUTCString() method instead """
        pass

    def toJSON(self):
        """  Returns the date as a string, formatted as a JSON date """

        # def default(o):
        #     if isinstance(o, (datetime.date, datetime.datetime)):
        #         return o.isoformat()

        pass

    def toISOString(self):
        """ Returns the date as a string, using the ISO standard """
        pass

    def toLocaleDateString(self):
        """ Returns the date portion of a Date object as a string, using locale conventions """
        pass

    def toLocaleString(self):
        """ Converts a Date object to a string, using locale conventions """
        pass

    def toLocaleTimeString(self):
        """ Returns the time portion of a Date object as a string, using locale conventions """
        pass

    def toTimeString(self):
        """ Converts the time portion of a Date object to a string """
        pass

    def toUTCString(self):
        """ Converts a Date object to a string, according to universal time """
        pass

    def UTC(self):
        """ Returns the number of milliseconds in a date since midnight of January 1, 1970, according to UTC time """
        pass

    # def valueOf():
    """ Returns the primitive value of an array Array, Boolean, Date, Number, String"""
    # pass


class MouseEvent(object):
    def __init__(self, *args, **kwargs):
        # self.args = args
        # self.kwargs = kwargs
        pass

    # MOUSE_EVENT
    # altKey    Returns whether the "ALT" key was pressed when the mouse event was triggered    MouseEvent, KeyboardEvent, TouchEvent
    # button    Returns which mouse button was pressed when the mouse event was triggered   MouseEvent
    # buttons   Returns which mouse buttons were pressed when the mouse event was triggered MouseEvent
    # ctrlKey   Returns whether the "CTRL" key was pressed when the mouse event was triggered   MouseEvent, KeyboardEvent, TouchEvent
    # getModifierState()    Returns an array containing target ranges that will be affected by the insertion/deletion   MouseEvent
    # metaKey   Returns whether the "META" key was pressed when an event was triggered  MouseEvent, KeyboardEvent, TouchEvent
    # MovementX Returns the horizontal coordinate of the mouse pointer relative to the position of the last mousemove event MouseEvent
    # MovementY Returns the vertical coordinate of the mouse pointer relative to the position of the last mousemove event   MouseEvent
    # offsetX   Returns the horizontal coordinate of the mouse pointer relative to the position of the edge of the target element   MouseEvent
    # offsetY   Returns the vertical coordinate of the mouse pointer relative to the position of the edge of the target element MouseEvent
    # onclick   The event occurs when the user clicks on an element MouseEvent
    # oncontextmenu The event occurs when the user right-clicks on an element to open a context menu    MouseEvent
    # ondblclick    The event occurs when the user double-clicks on an element  MouseEvent
    # onmousedown   The event occurs when the user presses a mouse button over an element   MouseEvent
    # onmouseenter  The event occurs when the pointer is moved onto an element  MouseEvent
    # onmouseleave  The event occurs when the pointer is moved out of an element    MouseEvent
    # onmousemove   The event occurs when the pointer is moving while it is over an element MouseEvent
    # onmouseover   The event occurs when the pointer is moved onto an element, or onto one of its children MouseEvent
    # onmouseout    The event occurs when a user moves the mouse pointer out of an element, or out of one of its children   MouseEvent
    # onmouseup The event occurs when a user releases a mouse button over an element    MouseEvent
    # pageX Returns the horizontal coordinate of the mouse pointer, relative to the document, when the mouse event was triggered    MouseEvent
    # pageY Returns the vertical coordinate of the mouse pointer, relative to the document, when the mouse event was triggered  MouseEvent
    # region        MouseEvent
    # relatedTarget Returns the element related to the element that triggered the mouse event   MouseEvent, FocusEvent
    # shiftKey  Returns whether the "SHIFT" key was pressed when an event was triggered MouseEvent, KeyboardEvent, TouchEvent
    # which Returns which mouse button was pressed when the mouse event was triggered   MouseEvent, KeyboardEvent


class KeyboardEvent(object):
    def __init__(self, *args, **kwargs):
        # self.args = args
        # self.kwargs = kwargs
        pass

    # @property
    # def location(self):

    # KeyboardEvent
    # altKey    Returns whether the "ALT" key was pressed when the mouse event was triggered    MouseEvent, KeyboardEvent, TouchEvent
    # ctrlKey   Returns whether the "CTRL" key was pressed when the mouse event was triggered   MouseEvent, KeyboardEvent, TouchEvent
    # metaKey   Returns whether the "META" key was pressed when an event was triggered  MouseEvent, KeyboardEvent, TouchEvent
    # shiftKey  Returns whether the "SHIFT" key was pressed when an event was triggered MouseEvent, KeyboardEvent, TouchEvent
    # which Returns which mouse button was pressed when the mouse event was triggered   MouseEvent, KeyboardEvent
    # charCode  Returns the Unicode character code of the key that triggered the onkeypress event   KeyboardEvent
    # code  Returns the code of the key that triggered the event    KeyboardEvent
    # isComposing   Returns whether the state of the event is composing or not  InputEvent, KeyboardEvent
    # key   Returns the key value of the key represented by the event   KeyboardEvent, StorageEvent
    # keyCode   Returns the Unicode character code of the key that triggered the onkeypress event, or the Unicode key code of the key that triggered the onkeydown or onkeyup event KeyboardEvent
    # location  Returns the location of a key on the keyboard or device KeyboardEvent
    # onkeydown The event occurs when the user is pressing a key    KeyboardEvent
    # onkeypress    The event occurs when the user presses a key    KeyboardEvent
    # onkeyup   The event occurs when the user releases a key   KeyboardEvent
    # repeat    Returns whether a key is being hold down repeatedly, or not KeyboardEvent


class Screen(object):

    # wrap a lib?
    # https://github.com/rr-/screeninfo?

    def __init__(self):
        # from sys import platform
        # if platform == "linux" or platform == "linux2":
        #     # linux
        # import subprocess
        # resuls = subprocess.Popen(['xrandr'],stdout=subprocess.PIPE).communicate()[0].split("current")[1].split(",")[0]
        # width = resuls.split("x")[0].strip()
        # heigth = resuls.split("x")[1].strip()
        # print width + "x" + heigth
        # elif platform == "darwin":
        #     # OS X
        # results = str(subprocess.Popen(['system_profiler SPDisplaysDataType'],stdout=subprocess.PIPE, shell=True).communicate()[0])
        # res = re.search('Resolution: \d* x \d*', results).group(0).split(' ')
        # width, height = res[1], res[3]
        # return width, height
        # elif platform == "win32":
        # from win32api import GetSystemMetrics
        # print("Width =", GetSystemMetrics(0))
        # print("Height =", GetSystemMetrics(1))
        pass

    def availHeight(self):
        ''' Returns the height of the screen (excluding the Windows Taskbar) '''
        raise NotImplementedError

    def availWidth(self):
        ''' Returns the width of the screen (excluding the Windows Taskbar) '''
        raise NotImplementedError

    def colorDepth(self):
        ''' Returns the colorDepth '''
        raise NotImplementedError

    def height(self):
        ''' Returns the total height of the screen '''
        raise NotImplementedError

    def pixelDepth(self):
        ''' Returns the pixelDepth '''
        raise NotImplementedError

    def width(self):
        ''' Returns the total width of the screen  '''
        raise NotImplementedError




import threading, time, signal
from datetime import timedelta

class ProgramKilled(Exception):
    pass

class Job(threading.Thread):
    def __init__(self, interval, execute, *args, **kwargs):
        threading.Thread.__init__(self)
        self.daemon = False
        self.stopped = threading.Event()
        self.interval = interval
        self.execute = execute
        self.args = args
        self.kwargs = kwargs

    def stop(self):
        self.stopped.set()
        self.join()
    
    def run(self):
        while not self.stopped.wait(self.interval.total_seconds()):
            self.execute(*self.args, **self.kwargs)

class SetInterval(object):

    def signal_handler(signum, frame):
        raise ProgramKilled

    def __init__(self, time, function, *args, **kwargs):
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)
        self.job = Job(interval=timedelta(seconds=time), execute=function)
        self.job.start()


class Window(object):

    def __init__(self, *args, **kwargs):
        print('window here!')
        # print(type(dom))
        # self.args = args
        # self.kwargs = kwargs
        # self.console = dom.console
        # self.document = dom.document
        # self.location = ''#dom.location
        self.location = None

    @property
    def location(self):
        # print("@@@@@@@@@@@@@@@@@@@@@@")
        return self.__location

    @location.setter
    def location(self, x):
        # print("====================>>>>>>>", x)
        # dom.location = x
        # dom.location = dom.location(x)#Location(x)
        # from .dom import Location
        # print('test::::-------------------------------------------------------',Location)
        # print("xxxxxxxx>>>>>>", dom.location)
        # self.__location = dom.location
        # import requests.
        pass

    @staticmethod
    def alert(msg):
        """ Displays an alert box with a message and an OK button """
        print(msg)
        return

    @staticmethod
    def prompt(msg, default_text=""):
        """ Displays a dialog box that prompts the visitor for input """
        print(msg)
        data = input()
        return data

    # TODO - clearTimeout.
    @staticmethod
    def setTimeout(time, function):
        """ Calls a function or evaluates an expression after a specified number of milliseconds """
        time.sleep(time)  # blocks
        function()
        return

    def clearInterval(job):
        job.stop()

    def setInterval(time, function, *args, **kwargs):
        interval_ID = SetInterval(time, function, *args, **kwargs)
        return interval_ID.job



    # @staticmethod
    # @getter
    # def navigator():
        """ Returns the Navigator object for the window (See Navigator object) """
        # return

# WINDOW
# localStorage  Allows to save key/value pairs in a web browser. Stores the data with no expiration date    Window
# requestAnimationFrame()   Requests the browser to call a function to update an animation before the next repaint  Window
# atob()    Decodes a base-64 encoded string    Window
# blur()    Removes focus from an element   Element, Window
# btoa()    Encodes a string in base-64 Window
# clearInterval()   Clears a timer set with setInterval()   Window
# clearTimeout()    Clears a timer set with setTimeout()    Window
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
# print()   Prints the content of the current window    Window
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
# self  Returns the current window  Window
# sessionStorage    Allows to save key/value pairs in a web browser. Stores the data for one session    Window
# setInterval() Calls a function or evaluates an expression at specified intervals (in milliseconds)    Window
# setTimeout()  Calls a function or evaluates an expression after a specified number of milliseconds    Window
# stop()    Stops the window from loading   Window
# status    Sets or returns the text in the statusbar of a window   Window
# top   Returns the topmost browser window  Window
# view  Returns a reference to the Window object where the event occurred   UiEvent


window = Window


class Array(object):

    def __init__(self, *args):
        self.args = list(args)

    def __getitem__(self, index):
        return self.args[index]

    def __setitem__(self, index, value):
        self.args[index] = value

    def __len__(self):
        return len(self.args)

        # TODO - all the dunder methods

    def __str___(self):
        return self.args

    def __repr__(self):
        return str(self.args)

    def toString(self):
        ''' Converts an array to a string, and returns the result '''
        return str(self.ars)  # TODO - check what js does

    @property
    def length(self):
        """ Sets or returns the number of elements in an array """
        return len(self.args)

    def concat(self, value):
        """ Joins two or more arrays, and returns a copy of the joined arrays """
        return self.args.extend(value)

    def fill(self):
        """ Fill the elements in an array with a static value """
        raise NotImplementedError

    def includes(self, value):
        """ Check if an array contains the specified element """
        if value in self.args:
            return True
        else:
            return False

    def indexOf(self, value):
        """ Search the array for an element and returns its position """
        # for count, each in enumerate(self.args):
        #     if each == value:
        #         return count
        try:
            return self.args.index(value)
        except ValueError:
            return -1
        except Exception as e:
            print(e)
            return -1

    def isArray(self):
        """ Checks whether an object is an array  """
        raise NotImplementedError

    def join(self, value):
        """ Joins all elements of an array into a string  """
        # TODO - get passed param names
        return value.join([str(x) for x in self.args])

    def lastIndexOf(self, value):
        """ Search the array for an element, starting at the end, and returns its position """
        try:
            return len(self.args) - self.args[::-1].index(value) - 1
        except Exception as e:
            print(e)
            return None

    def map(self):
        """ Creates a new array with the result of calling a function for each array element """
        raise NotImplementedError

    def pop(self):
        """ Removes the last element of an array, and returns that element """
        # item = self.args[len(self.args)-1]
        # del self.args[len(self.args)-1]
        return self.args.pop()

    def push(self, value):
        """ Adds new elements to the end of an array, and returns the new length """
        self.args.append(value)
        return len(self.args)

    def reduce(self):
        """ Reduce the values of an array to a single value (going left-to-right) """
        raise NotImplementedError

    def reduceRight(self):
        """ Reduce the values of an array to a single value (going right-to-left) """
        raise NotImplementedError

    def reverse(self):
        """ Reverses the order of the elements in an array """
        self.args = self.args[::-1]
        return self.args

    def slice(self, start, stop, step=1):
        """ Selects a part of an array, and returns the new array """
        self.args.slice(start, stop, step)

    def splice(self, start, delete_count=None, *items):
        """ Selects a part of an array, and returns the new array """
        if delete_count == None:
            delete_count = len(self.args) - start

        total = start + delete_count
        removed = self.args[start:total]
        self.args[start:total] = items
        return removed
        # return self.args

    def some(self):
        """ Checks if any of the elements in an array pass a test """
        raise NotImplementedError

    def sort(self):
        """ Sorts the elements of an array """
        raise NotImplementedError

    def unshift(self, *args):
        """ Adds new elements to the beginning of an array, and returns the new length """
        for i in reversed(args):
            self.args.insert(0, i)
        return len(self.args)

    def shift(self):
        """ removes the first element from an array and returns that removed element """
        item = self.args[0]
        del self.args[0]
        return item


class Navigator(object):

    # Determines whether cookies are enabled in the browser
    cookieEnabled = False

    # Determines whether the browser is online
    onLine = False

    def __init__(self, *args, **kwargs):
        # self.args = args
        # self.kwargs = kwargs
        pass

    # appCodeName   Returns the code name of the browser    Navigator
    # appName   Returns the name of the browser Navigator
    # appVersion    Returns the version information of the browser  Navigator
    # geolocation   Returns a Geolocation object that can be used to locate the user's position Navigator
    # language  Returns the language of the browser Navigator
    # platform  Returns for which platform the browser is compiled  Navigator
    # product   Returns the engine name of the browser  Navigator
    # userAgent Returns the user-agent header sent by the browser to the server Navigator


class String(object):

    def __init__(self, x="", *args, **kwargs):
        # self.args = args
        # self.kwargs = kwargs
        self.x = x

    def repeat(self, count):
        ''' Returns a new string with a specified number of copies of an existing string '''
        return self.x*count

    def startsWith(self, x, start, end):
        ''' Checks whether a string begins with specified characters '''

        if end is None:
            end = len(x)

        if start is None:
            start = 0

        self.x.startswith(x, beg=start, end=end)

    def substring(self):
        ''' Extracts the characters from a string, between two specified indices '''
        pass

    def endsWith(self, x, start, end):
        ''' Checks whether a string ends with specified string/characters '''

        # TODO - should take array. or any length string
        # return x[len(x)] == x
        self.x.endswith(x, start, end)

    def toLowerCase() -> str:
        '''Converts a string to lowercase letters'''
        return self.x.lower()

    def toUpperCase() -> str:
        '''Converts a string to uppercase letters'''
        return self.x.upper()

    def trim() -> str:
        '''Removes whitespace from both ends of a string'''
        return self.x.strip()


# fromCharCode()    Converts Unicode values to characters   String
# localeCompare()   Compares two strings in the current locale  String
# replace() Searches a string for a specified value, or a regular expression, and returns a new string where the specified values are replaced  String
# search()  Searches a string for a specified value, or regular expression, and returns the position of the match   String
# substr()  Extracts the characters from a string, beginning at a specified start position, and through the specified number of character   String
# toLocaleLowerCase()   Converts a string to lowercase letters, according to the host's locale  String
# toLocaleUpperCase()   Converts a string to uppercase letters, according to the host's locale  String
# compile() Deprecated in version 1.5. Compiles a regular expression    RegExp
# lastIndex Specifies the index at which to start the next match    RegExp
# test()    Tests for a match in a string. Returns true or false    RegExp


# https://developer.mozilla.org/en-US/docs/Web/API/URL

class URL(object):
    def __update__(self):
        # print( "update URL:", type(self), self  )
        try:
            # make obj with all old props
            new = {}
            new['protocol'] = self.url.scheme
            new['hostname'] = self.url.hostname
            new['port'] = self.url.port
            new['host'] = ''  # self.url.hostname
            new['pathname'] = self.url.path
            new['hash'] = ''  # self.url.hash

            # update it with all the new ones
            new = {}
            new['protocol'] = self.protocol
            new['hostname'] = self.hostname
            new['port'] = self.port
            new['host'] = self.host
            new['pathname'] = self.pathname
            new['hash'] = self.hash  # self.hash

            # rebuild
            self.url = urllib.parse.urlsplit(
                new['protocol'] + "://" + new['host'] + new['pathname'] + new['hash'])

            # reset
            self.href = self.url.geturl()
        except Exception as e:
            # print('fails on props called by init as they dont exist yet')
            # print(e)
            pass

    def __init__(self, url: str = "", *args, **kwargs):  # TODO - relative to
        self.url = urllib.parse.urlsplit(url)
        self.href = self.url.geturl()

        self.protocol = self.url.scheme
        self.hostname = self.url.hostname
        self.port = self.url.port
        self.host = self.url.hostname
        self.pathname = self.url.path
        self.hash = ''

    def toString(self):
        return self.href

    # def toJson

    # @property
    # def href(self):
    #     return self.href

    # @href.setter
    # def href(self, href:str):
    #     self.url = href
    #     self.href = href

    @property
    def protocol(self):
        return self.__protocol

    @protocol.setter
    def protocol(self, p: str):
        self.__protocol = p
        # if self.ready : self.__update__() # TODO - this instead of silent err?
        self.__update__()

    @property
    def hostname(self):
        return self.__hostname

    @hostname.setter
    def hostname(self, h: str):
        if h is None:
            return
        if ":" in h:
            h = h.split(':')[0]
        self.__hostname = h
        self.__update__()

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, p: str):
        self.__port = p
        self.__update__()

    @property
    def host(self):
        if self.port is not None:
            return self.hostname + ":" + str(self.port)
        else:
            return self.hostname

    @host.setter
    def host(self, h: str):
        if h is None:
            return
        p = self.port
        if ":" in h:
            p = int(h.split(':')[1])
            h = h.split(':')[0]
        self.__host = h
        self.hostname = h
        self.port = p
        self.__update__()

    @property
    def pathname(self):
        return self.__pathname

    @pathname.setter
    def pathname(self, p: str):
        self.__pathname = p
        self.__update__()

    @property
    def hash(self):
        ''' hash Sets or returns the anchor part (#) of a URL '''
        if '#' in self.href:
            return '#'+self.href.split('#')[1]
        # return ''
        return self.__hash

    @hash.setter
    def hash(self, h: str):
        self.__hash = h
        self.__update__()

    # @property
    # def origin(self):
        '''# origin    Returns the protocol, hostname and port number of a URL Location'''


# clipboardData Returns an object containing the data affected by the clipboard operation   ClipboardData

# animationName Returns the name of the animation   AnimationEvent

# back()    Loads the previous URL in the history list  History

# break Exits a switch or a loop    Statements

# bubbles   Returns whether or not a specific event is a bubbling event Event

# cancelable    Returns whether or not an event can have its default action prevented   Event

# changeTouches Returns a list of all the touch objects whose state changed between the previous touch and this touch   TouchEvent

# charAt()  Returns the character at the specified index (position) String

# charCodeAt()  Returns the Unicode of the character at the specified index String

# clear()   Clears the console  Console, Storage

# clearWatch()  Unregister location/error monitoring handlers previously installed using Geolocation.watchPosition()    Geolocation

# composed  Returns whether the event is composed or not    Event

# const Declares a variable with a constant value   Statements

# continue  Breaks one iteration (in the loop) if a specified condition occurs, and continues with the next iteration in the loop   Statements

# coordinates   Returns the position and altitude of the device on Earth    Geolocation

# copyWithin()  Copies array elements within the array, to and from specified positions Array

# currentTarget Returns the element whose event listeners triggered the event   Event

# data  Returns the inserted characters InputEvent

# dataTransfer  Returns an object containing the data being dragged/dropped, or inserted/deleted    DragEvent, InputEvent

# debugger  Stops the execution of JavaScript, and calls (if available) the debugging function  Statements

# defaultPrevented  Returns whether or not the preventDefault() method was called for the event Event

# deltaX    Returns the horizontal scroll amount of a mouse wheel (x-axis)  WheelEvent

# deltaY    Returns the vertical scroll amount of a mouse wheel (y-axis)    WheelEvent

# deltaZ    Returns the scroll amount of a mouse wheel for the z-axis   WheelEvent

# deltaMode Returns a number that represents the unit of measurements for delta values (pixels, lines or pages) WheelEvent

# detail    Returns a number that indicates how many times the mouse was clicked    UiEvent

# do ... while  Executes a block of statements and repeats the block while a condition is true  Statements

# elapsedTime   Returns the number of seconds an animation has been running AnimationEvent

# elapsedTime   Returns the number of seconds a transition has been running

# entries() Returns a key/value pair Array Iteration Object Array

# error()   Outputs an error message to the console Console

# eventPhase    Returns which phase of the event flow is currently being evaluated  Event

# every()   Checks if every element in an array pass a test Array

# exec()    Tests for a match in a string. Returns the first match  RegExp

# filter()  Creates a new array with every element in an array that pass a test Array

# find()    Returns the value of the first element in an array that pass a test Array

# findIndex()   Returns the index of the first element in an array that pass a test Array

# for   Marks a block of statements to be executed as long as a condition is true   Statements

# for ... in    Marks a block of statements to be executed for each element of an object (or array) Statements

# forEach() Calls a function for each array element Array

# forms Returns a collection of all <form> elements in the document Document

# forward() Loads the next URL in the history list  History

# from()    Creates an array from an object Array

# function  Declares a function Statements

# geolocation   Returns a Geolocation object that can be used to locate the user's position Navigator

# getCurrentPosition()  Returns the current position of the device  Geolocation

# getItem() Returns the value of the specified key name Storage

# getNamedItem()    Returns a specified attribute node from a NamedNodeMap  Attribute

# getTargetRanges() Returns an array containing target ranges that will be affected by the insertion/deletion   InputEvent

# go()  Loads a specific URL from the history list  History

# id    Sets or returns the value of the id attribute of an element Element

# if ... else ... else if   Marks a block of statements to be executed depending on a condition Statements

# ignoreCase    Checks whether the "i" modifier is set  RegExp

# inputType Returns the type of the change (i.e "inserting" or "deleting")  InputEvent

# isId  Returns true if the attribute is of type Id, otherwise it returns false Attribute

# isInteger()   Checks whether a value is an integer    Number

# isSafeInteger()   Checks whether a value is a safe integer    Number

# isTrusted Returns whether or not an event is trusted  Event

# item()    Returns the attribute node at a specified index in a NamedNodeMap   Attribute, HTMLCollection

# key() Returns the name of the nth key in the storage  Storage

# keys()    Returns a Array Iteration Object, containing the keys of the original array Array

# language  Returns the language of the browser Navigator

# lengthComputable  Returns whether the length of the progress can be computable or not ProgressEvent

# let   Declares a variable inside brackets {} scope    Statements

# loaded    Returns how much work has been loaded   ProgressEvent

# match()   Searches a string for a match against a regular expression, and returns the matches String

# MAX_VALUE Returns the largest number possible in JavaScript   Number

# message   Sets or returns an error message (a string) Error

# multiline Checks whether the "m" modifier is set  RegExp

# MIN_VALUE Returns the smallest number possible in JavaScript  Number

# namedItem()   Returns the element with the specified ID, or name, in an HTMLCollection    HTMLCollection

# NEGATIVE_INFINITY Represents negative infinity (returned on overflow) Number

# newURL    Returns the URL of the document, after the hash has been changed    HasChangeEvent

# newValue  Returns the new value of the changed storage item   StorageEvent

# oldURL    Returns the URL of the document, before the hash was changed    HasChangeEvent

# oldValue  Returns the old value of the changed storage item   StorageEvent

# onabort   The event occurs when the loading of a media is aborted UiEvent, Event

# onafterprint  The event occurs when a page has started printing, or if the print dialogue box has been closed Event

# onanimationend    The event occurs when a CSS animation has completed AnimationEvent

# onanimationiteration  The event occurs when a CSS animation is repeated   AnimationEvent

# onanimationstart  The event occurs when a CSS animation has started   AnimationEvent

# onbeforeprint The event occurs when a page is about to be printed Event

# onbeforeunload    The event occurs before the document is about to be unloaded    UiEvent, Event

# onblur    The event occurs when an element loses focus    FocusEvent

# oncanplay The event occurs when the browser can start playing the media (when it has buffered enough to begin)    Event

# oncanplaythrough  The event occurs when the browser can play through the media without stopping for buffering Event

# onchange  The event occurs when the content of a form element, the selection, or the checked state have changed (for <input>, <select>, and <textarea>)   Event

# oncopy    The event occurs when the user copies the content of an element ClipboardEvent

# oncut The event occurs when the user cuts the content of an element   ClipboardEvent

# ondrag    The event occurs when an element is being dragged   DragEvent

# ondragend The event occurs when the user has finished dragging an element DragEvent

# ondragenter   The event occurs when the dragged element enters the drop target    DragEvent

# ondragleave   The event occurs when the dragged element leaves the drop target    DragEvent

# ondragover    The event occurs when the dragged element is over the drop target   DragEvent

# ondragstart   The event occurs when the user starts to drag an element    DragEvent

# ondrop    The event occurs when the dragged element is dropped on the drop target DragEvent

# ondurationchange  The event occurs when the duration of the media is changed  Event

# onemptied The event occurs when something bad happens and the media file is suddenly unavailable (like unexpectedly disconnects)

# onended   The event occurs when the media has reach the end (useful for messages like "thanks for listening") Event

# onerror   The event occurs when an error occurs while loading an external file    ProgressEvent, UiEvent, Event

# onfocus   The event occurs when an element gets focus FocusEvent

# onfocusin The event occurs when an element is about to get focus  FocusEvent

# onfocusout    The event occurs when an element is about to lose focus FocusEvent

# onfullscreenchange    The event occurs when an element is displayed in fullscreen mode    Event

# onfullscreenerror The event occurs when an element can not be displayed in fullscreen mode    Event

# onhashchange  The event occurs when there has been changes to the anchor part of a URL    HashChangeEvent

# oninput   The event occurs when an element gets user input    InputEvent, Event

# oninvalid The event occurs when an element is invalid Event

# onLine    Determines whether the browser is online    Navigator

# onload    The event occurs when an object has loaded  UiEvent, Event

# onloadeddata  The event occurs when media data is loaded  Event

# onloadedmetadata  The event occurs when meta data (like dimensions and duration) are loaded   Event

# onloadstart   The event occurs when the browser starts looking for the specified media    ProgressEvent

# onmessage The event occurs when a message is received through the event source    Event

# onmousewheel  Deprecated. Use the wheel event instead WheelEvent

# onoffline The event occurs when the browser starts to work offline    Event

# ononline  The event occurs when the browser starts to work online Event

# onopen    The event occurs when a connection with the event source is opened  Event

# onpagehide    The event occurs when the user navigates away from a webpage    PageTransitionEvent

# onpageshow    The event occurs when the user navigates to a webpage   PageTransitionEvent

# onpaste   The event occurs when the user pastes some content in an element    ClipboardEvent

# onpause   The event occurs when the media is paused either by the user or programmatically    Event

# onplay    The event occurs when the media has been started or is no longer paused Event

# onplaying The event occurs when the media is playing after having been paused or stopped for buffering    Event

# onprogress    The event occurs when the browser is in the process of getting the media data (downloading the media)   Event

# onratechange  The event occurs when the playing speed of the media is changed Event

# onresize  The event occurs when the document view is resized  UiEvent, Event

# onreset   The event occurs when a form is reset   Event

# onscroll  The event occurs when an element's scrollbar is being scrolled  UiEvent, Event

# onsearch  The event occurs when the user writes something in a search field (for <input="search">)    Event

# onseeked  The event occurs when the user is finished moving/skipping to a new position in the media   Event

# onseeking The event occurs when the user starts moving/skipping to a new position in the media    Event

# onselect  The event occurs after the user selects some text (for <input> and <textarea>)  UiEvent, Event

# onshow    The event occurs when a <menu> element is shown as a context menu   Event

# onstalled The event occurs when the browser is trying to get media data, but data is not available    Event

# onsubmit  The event occurs when a form is submitted   Event

# onsuspend The event occurs when the browser is intentionally not getting media data   Event

# ontoggle  The event occurs when the user opens or closes the <details> element    Event

# ontouchcancel The event occurs when the touch is interrupted  TouchEvent

# ontouchend    The event occurs when a finger is removed from a touch screen   TouchEvent

# ontouchmove   The event occurs when a finger is dragged across the screen TouchEvent

# ontouchstart  The event occurs when a finger is placed on a touch screen  TouchEvent

# ontransitionend   The event occurs when a CSS transition has completed    TransitionEvent

# onunload  The event occurs once a page has unloaded (for <body>)  UiEvent, Event

# onvolumechange    The event occurs when the volume of the media has changed (includes setting the volume to "mute")   Event

# onwaiting The event occurs when the media has paused but is expected to resume (like when the media pauses to buffer more data)   Event

# onwheel   The event occurs when the mouse wheel rolls up or down over an element  WheelEvent

# origin    Returns the protocol, hostname and port number of a URL Location

# persisted Returns whether the webpage was cached by the browser   PageTransitionEvent

# position  Returns the position of the concerned device at a given time    Geolocation

# positionError Returns the reason of an error occurring when using the geolocating device  Geolocation

# positionOptions   Describes an object containing option properties to pass as a parameter of Geolocation.getCurrentPosition() and Geolocation.watchPosition() Geolocation

# POSITIVE_INFINITY Represents infinity (returned on overflow)  Number

# preventDefault()  Cancels the event if it is cancelable, meaning that the default action that belongs to the event will not occur Event

# propertyName  Returns the name of the CSS property associated with the animation or transition    AnimationEvent, TransitionEvent

# pseudoElement Returns the name of the pseudo-element of the animation or transition   AnimationEvent, TransitionEvent

# removeItem()  Removes that key from the storage   Storage

# repeat    Returns whether a key is being hold down repeatedly, or not KeyboardEvent

# return    Stops the execution of a function and returns a value from that function    Statements

# prototype Allows you to add properties and methods to an object   Number

# removeNamedItem() Removes a specified attribute node  Attribute

# search    Sets or returns the querystring part of a URL   Location

# setNamedItem()    Sets the specified attribute node (by name) Attribute

# source    Returns the text of the RegExp pattern  RegExp

# specified Returns true if the attribute has been specified, otherwise it returns false    Attribute

# state Returns an object containing a copy of the history entries  PopStateEvent

# storageArea   Returns an object representing the affected storage object  StorageEvent

# switch    Marks a block of statements to be executed depending on different cases Statements

# targetTouches Returns a list of all the touch objects that are in contact with the surface and where the touchstart event occured on the same target element as the current target element    TouchEvent

# throw Throws (generates) an error Statements

# timeStamp Returns the time (in milliseconds relative to the epoch) at which the event was created Event

# toExponential()   Converts a number into an exponential notation  Number

# toFixed(x)    Formats a number with x numbers of digits after the decimal point   Number

# toPrecision(x)    Formats a number to x length    Number

# total Returns the total amount of work that will be loaded    ProgressEvent

# touches   Returns a list of all the touch objects that are currently in contact with the surface  TouchEvent

# transitionend The event occurs when a CSS transition has completed    TransitionEvent

# try ... catch ... finally Marks the block of statements to be executed when an error occurs in a try block, and implements error handling Statements

# url   Returns the URL of the changed item's document  StorageEvent

# value Sets or returns the value of the attribute  Attribute

# var   Declares a variable Statements

# watchPosition()   Returns a watch ID value that then can be used to unregister the handler by passing it to the Geolocation.clearWatch() method   Geolocation

# while Marks a block of statements to be executed while a condition is true    Statements
