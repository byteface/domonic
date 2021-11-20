"""
    domonic.webapi.url
    ====================================
    https://developer.mozilla.org/en-US/docs/Web/API/URL

    # TODO - move the unit tests for this class from javascript to webapi
    # TODO - untested

"""

import urllib


class URL(object):
    """ a-tag extends from URL """

    def __update__(self):
        # print( "update URL:", type(self), self  )
        try:
            # make obj with all old props
            new = {}
            new['protocol'] = self.url.scheme
            new['hostname'] = self.url.hostname
            new['href'] = self.url.geturl()
            new['port'] = self.url.port
            new['host'] = ''  # self.url.hostname
            new['pathname'] = self.url.path
            new['hash'] = ''  # self.url.hash
            new['search'] = ''  # self.url.hash

            # update it with all the new ones
            new = {}
            new['protocol'] = self.protocol
            new['hostname'] = self.hostname
            new['href'] = self.href
            new['port'] = self.port
            new['host'] = self.host
            new['pathname'] = self.pathname
            new['hash'] = self.hash  # self.hash
            new['search'] = self.search  # self.url.query
            new['_searchParams'] = self._searchParams  # URLSearchParams(self.url.query)
            # NOTE - rebuild happening here
            self.url = urllib.parse.urlsplit(
                new['protocol'] + "://" + new['host'] + new['pathname'] + new['hash'] + new['search'])

            self.href = self.url.geturl()

        except Exception:  # as e:
            # print('fails on props called by init as they dont exist yet')
            # print(e)
            pass

    def __init__(self, url: str = "", *args, **kwargs):  # TODO - relative to
        """URL

        builds a url

        Args:
            url (str): a url
        """
        self.url = urllib.parse.urlsplit(url)
        self.href = url  # self.url.geturl()
        self.protocol = self.url.scheme
        self.hostname = self.url.hostname
        self.port = self.url.port
        self.host = self.url.hostname
        self.pathname = self.url.path
        self.hash = ''
        self.search = self.url.query
        self._searchParams = URLSearchParams(self.url.query)

    @property
    def searchParams(self):
        return self._searchParams.toString()

    def toString(self):
        return str(self.href)

    # def toJson

    # @property
    # def href(self):
    # TODO - check js vs tag. does js version remove query?. if so detect self.
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
        """" hash Sets or returns the anchor part (#) of a URL """
        if '#' in self.href:
            return '#' + self.href.split('#')[1]
        # return ''
        return self.__hash

    @hash.setter
    def hash(self, h: str):
        self.__hash = h
        self.__update__()

    # @property
    # def origin(self):
        '''# origin    Returns the protocol, hostname and port number of a URL Location'''

    def __str__(self):
        return str(self.href)

    # NOTE - node -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    # @staticmethod
    # def domainToASCII(domain: str):
    #     """[It returns the Punycode ASCII serialization of the domain.
    #     If domain is an invalid domain, the empty string is returned.]

    #     Args:
    #         domain (str): [description]
    #     """
    #     pass

    # @staticmethod
    # def domainToUnicode(domain: str):
    #     """[returns the Unicode serialization of the domain.
    #     If the domain is invalid, the empty string is returned]

    #     Args:
    #         domain (str): [description]
    #     """
    #     pass

    # @staticmethod
    # def fileURLToPath(url: str):
    #     """[ensures the correct decodings of percent-encoded characters as well as
    #     ensuring a cross-platform valid absolute path string.]

    #     Args:
    #         url (str): [The fully-resolved platform-specific file path.]
    #     """
    #     if url is None:
    #         return
    #     return urllib.parse.unquote(url)

    # @staticmethod
    # def format(URL, options):
    #     """[summary]

    #     Args:
    #         URL ([type]): [description]
    #         options ([type]): [description]
    #     """
    #     pass

    # @staticmethod
    # def pathToFileURL(path: str):
    #     """[summary]

    #     Args:
    #         path (str): [description]
    #     """
    #     pass

    # @staticmethod
    # def urlToHttpOptions(url: str):
    #     """[summary]

    #     Args:
    #         url (str): [description]
    #     """
    #     pass


class URLSearchParams:
    """[utility methods to work with the query string of a URL]
    """

    def __init__(self, paramString):  # , **paramsObj):
        """[Returns a URLSearchParams object instance.]

        Args:
            paramString ([type]): [ i.e. q=URLUtils.searchParams&topic=api]
        """
        # TODO - escape
        # import ast
        # TODO - dont think i can do this cant urls params have duplicate keys?
        # self.params = ast.literal_eval(paramString)
        if isinstance(paramString, str):
            if paramString.startswith('?'):
                paramString = paramString[1:len(paramString)]

            import urllib
            self.params = urllib.parse.parse_qs(paramString)
        elif hasattr(paramString, '__iter__'):
            self.params = [item for sublist in paramString for item in sublist]
        elif isinstance(paramString, dict):
            self.params = dict([(key, item) for key, item in paramString.iteritems()])
        else:
            raise TypeError("Malformed paramString.  Must be a string or a dict with dict like items. Got: %s" % paramString)

    def __iter__(self):
        for attr in self.params.items():  # dir(self.params.items()):
            # if not attr.startswith("__"):
            yield attr

    def append(self, key, value):
        """ Appends a specified key/value pair as a new search parameter """
        # TODO - ordereddict?
        self.params[key].append(value)  # [key]=value

    def delete(self, key):
        """ Deletes the given search parameter, and its associated value, from the list of all search parameters. """
        del self.params[key]

    def has(self, key):
        """ Returns a Boolean indicating if such a given parameter exists. """
        return key in self.params

    def entries(self):
        """ Returns an iterator allowing iteration through all key/value pairs contained in this object. """
        return self.params.items()

    def forEach(self, func):
        """ Allows iteration through all values contained in this object via a callback function. """
        for key, value in self.params.items():
            func(key, value)

    def keys(self):
        """ Returns an iterator allowing iteration through all keys of the key/value pairs contained in this object. """
        return self.params.keys()

    def get(self, key):
        """ Returns the first value associated with the given search parameter. """
        try:
            return self.params.get(key, None)[0]
        except Exception:
            return None

    def sort(self):
        """ Sorts all key/value pairs, if any, by their keys. """
        self.params.sort()

    def values(self):
        """ Returns an iterator allowing iteration through all values of the key/value pairs
        contained in this object. """
        return self.params.values()

    def toString(self):
        """ Returns a string containing a query string suitable for use in a URL. """
        # return '&'.join([str(x) for x in self.params])
        return urllib.parse.urlencode(self.params, doseq=True)
        # return str(self.params)

    def set(self, key, value):
        """ Sets the value associated with a given search parameter to the given value.
        If there are several values, the others are deleted. """
        self.params[key] = (value)

    def getAll(self, key):
        """ Returns all the values associated with a given search parameter. """
        return self.params.get(key)

    def __str__(self):
        return urllib.parse.urlencode(self.params, doseq=True)
