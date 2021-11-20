"""
    domonic.webapi.XMLHttpRequest
    ====================================
    https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest
"""

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
        # TODO - parse to domonic.
        # if isinstance(form, str):
        #   self._data = domonic.loads(form) # TODO - parser wont be done enough yet
        # if isinstance(form, Node):
            # self._data = form
            # self._formobj = # TODO - serialize to object
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
