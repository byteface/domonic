"""
    domonic.webapi.XMLHttpRequest
    ====================================
    https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest

"""

import json
import os
import sys
import time
import traceback
import urllib.parse
import uuid
from io import BytesIO
from typing import Any, Callable, Dict, List, Optional, Union

from domonic.javascript import Global

# class XMLHttpRequest():
#     def __init__(self, url=None, responseType=None, withCredentials=False, timeout=0, onload=None, onerror=None, onprogress=None, ontimeout=None):
#         self.url = url
#         self.responseType = responseType
#         self.withCredentials = withCredentials
#         self.timeout = timeout
#         self.onload = onload
#         self.onerror = onerror
#         self.onprogress = onprogress
#         self.ontimeout = ontimeout
#         self.response = None
#         self.status = None


class FormData(object):

    def __init__(self, form):
        """ creates a new FormData object. """

        if isinstance(form, str):
            import domonic
            page = domonic.domonic.parseString(form)
            form = page.querySelector('form')

        print(form)
        print(form.nodeName)
        if form.nodeName.lower() != "form":
            print('not a form')
            return

        q = []
        for el in form:

            if el.nodeName.lower() == "#text":
                continue

            if el.getAttribute('name') == "":
                continue

            if el.nodeName.lower() == 'input':
                if el.type in ['email', 'text', 'hidden', 'password', 'reset', 'email']:
                    q.append(el.getAttribute('name') + "=" + Global.encodeURIComponent(el.nodeValue))
                elif el.type in ['checkbox', 'radio']:
                    if el.checked:
                        q.append(el.getAttribute('name') + "=" + Global.encodeURIComponent(el.nodeValue))
            elif el.nodeName.lower() == 'textarea':
                q.append(el.getAttribute('name') + "=" + Global.encodeURIComponent(el.nodeValue))
            elif el.nodeName.lower() == 'select':
                if el.getAttribute('multiple') != None:
                    for option in el.getElementsByTagName('option'):
                        if option.getAttribute('selected') != None:
                            q.append(el.getAttribute('name') + "=" + Global.encodeURIComponent(option.nodeValue))
                else:
                    q.append(el.getAttribute('name') + "=" + Global.encodeURIComponent(el.nodeValue))
            elif el.nodeName.lower() == 'button':
                if el.type in ['reset', 'submit', 'button']:
                    try:
                        q.append(el.getAttribute('name') + "=" + Global.encodeURIComponent(el.nodeValue))
                    except:
                        pass # ? we dont pass submit button do we?

        # return "&".join(q)
        self._data = "&".join(q)
        print(self._data)
        self._formobj = form

    def __str__(self) -> str:
        return self._data

    def toString(self):
        """ Returns a string representing the FormData object. """
        raise NotImplementedError

    def append(self, name, value, filename):
        """ Appends a new value onto an existing key inside a FormData object,
        or adds the key if it does not already exist. """
        raise NotImplementedError

    def delete(self, name):
        """ Deletes a key/value pair from a FormData object. """
        raise NotImplementedError

    def entries(self):
        """ Returns an iterator allowing to go through all key/value pairs contained in this object. """
        raise NotImplementedError

    def get(self, name):
        """ Returns the first value associated with a given key from within a FormData object. """
        raise NotImplementedError

    def getAll(self, name):
        """ Returns an array of all the values associated with a given key from within a FormData """
        raise NotImplementedError

    def has(self, name):
        """ Returns a boolean stating whether a FormData object contains a certain key."""
        raise NotImplementedError

    def keys(self):
        """ Returns an iterator allowing to go through all keys of the key/value pairs contained in this object."""
        raise NotImplementedError

    def set(self, name, value, filename):
        """ Sets a new value for an existing key inside a FormData object,
        or adds the key/value if it does not already exist."""
        raise NotImplementedError

    def values(self):
        """ Returns an iterator allowing to go through all values  contained in this object."""
        raise NotImplementedError
