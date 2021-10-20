"""
    domonic.webapi.history
    ====================================
    https://developer.mozilla.org/en-US/docs/Web/API/History
"""

# class History():
    # def __init__():
        # pass
    # def back():
    #     """ Loads the previous URL in the history list """
    #     raise NotImplementedError
    # def forward():
    #     """ Loads the next URL in the history list """
    #     raise NotImplementedError
    # def go():
    #     """ Loads a specific URL from the history list """
    #     raise NotImplementedError


# from domonic.html import *
# from domonic.js import *
# from domonic.css import *
# from domonic.events import *
# from domonic.internal import _get_window
# from domonic.internal import _get_document
# from domonic.internal import _get_location
# from domonic.internal import _get_history
# from domonic.internal import _get_navigator
# from domonic.internal import _get_screen
# from domonic.internal import _get_screen_left
# from domonic.internal import _get_screen_top
# from domonic.internal import _get_screen_width
# from domonic.internal import _get_screen_height
# from domonic.internal import _get_screen_avail_width
# from domonic.internal import _get_screen_avail_height
# from domonic.internal import _get_screen_pixel_ratio

# nice ideas from copilot

# but it also cheats... this will not work

# class History:

#     def __init__(self, window):
#         self._window = window

#     def back(self):
#         self._window.history.back()

#     def forward(self):
#         self._window.history.forward()

#     def go(self, steps):
#         self._window.history.go(steps)

#     def pushState(self, data, title, url):
#         self._window.history.pushState(data, title, url)

#     def replaceState(self, data, title, url):
#         self._window.history.replaceState(data, title, url)

#     def state(self):
#         return self._window.history.state()

#     def length(self):
#         return self._window.history.length()