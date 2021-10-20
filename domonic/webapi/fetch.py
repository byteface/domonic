"""
    domonic.webapi.fetch
    ====================================
    https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
"""

# TODO - untested. moving these over from javascript module
# TODO - check if promise also needs to come to this package

# @staticmethod
def fetch(url: str, **kwargs):
    # undocumented - warning. use at own risk
    # note - kinda pointless atm. just use requests directly and you wont have to muck about with a Promise
    if type(url) is not str:
        raise ValueError('fetch takes a single url string. use fetch_set, fetch_threaded or fetch_pooled')
    f = Promise()
    r = window._do_request(url, f, *kwargs)
    return f.resolve(r)

# @staticmethod
def fetch_set(urls: list, callback_function=None, error_handler=None, **kwargs):
    # undocumented - warning. use at own risk
    # note - still blocks. just gets all before continuing
    # problems - all urls can only have 1 associated callback, error and set of kwargs
    if type(urls) is str:
        urls = [urls]  # leniency
    f = FetchedSet()
    for url in urls:
        r = window.fetch(url, **kwargs).then(callback_function)
        f.results.append(r.data)
    return f

# @staticmethod
def fetch_threaded(urls: list, callback_function=None, error_handler=None, **kwargs):
    # undocumented - warning. use at own risk
    # note - still blocks. just gets all before continuing using threads
    # problems - all urls can only have 1 associated callback, error and set of kwargs
    if type(urls) is str:
        urls = [urls]  # leniency
    f = FetchedSet()
    jobs = []
    for url in urls:
        thread = threading.Thread(target=window._do_request(url, f, **kwargs))
        thread.setDaemon(True)
        jobs.append(thread)
    map(lambda j: j.start(), jobs)
    map(lambda j: j.join(), jobs)
    # f = FetchedSet()
    return f

# @staticmethod
def fetch_pooled(urls: list, callback_function=None, error_handler=None, **kwargs):
    # undocumented - warning. use at own risk
    # note - still blocks. just gets all before continuing using a pool
    # problems - all urls can only have 1 associated callback, error and set of kwargs
    if type(urls) is str:
        urls = [urls]  # leniency
    f = FetchedSet()

    def _do_request_wrapper(obj):
        url = obj['url']
        f = obj['f']
        kwargs = obj['k']
        kwargs['callback_function'] = obj['c']
        kwargs['error_handler'] = obj['e']
        window._do_request(url, f, **kwargs)

    jobs = []
    p = Pool()
    urls = [{'url': url, 'f': f, 'c': callback_function, 'e': error_handler, 'k': kwargs} for url in urls]
    results = p.map(_do_request_wrapper, urls)
    p.close()
    p.join()
    return f

# def fetch_aysnc( urls: list, options={}, type="async" ):
    # TODO - a version using async/await


class Headers():
    def __init__(self, headers=None):
        self.headers = headers

    def get(self, name):
        return self.headers[name]

    def set(self, name, value):
        self.headers[name] = value

    def has(self, name):
        return name in self.headers

    def keys(self):
        return self.headers.keys()

    def values(self):
        return self.headers.values()

    def entries(self):
        return self.headers.entries()

    def delete(self, name):
        del self.headers[name]

    def forEach(self, callback, thisArg=None):
        for name, value in self.headers.items():
            callback(value, name, self)

    def map(self, callback, thisArg=None):
        return [callback(value, name, self) for name, value in self.headers.items()]

    def filter(self, callback, thisArg=None):
        return [callback(value, name, self) for name, value in self.headers.items() if callback(value, name, self)]

    def reduce(self, callback, initialValue):
        return [callback(initialValue, value, name, self) for name, value in self.headers.items()]

    def toString(self):
        return str(self.headers)

    def toObject(self):
        return self.headers

    def toJSON(self):
        return self.headers

    def __str__(self):
        return str(self.headers)

    def __repr__(self):
        return str(self.headers)

    def __iter__(self):
        return self.headers.__iter__()

    def __next__(self):
        return self.headers.__next__()

    def __getitem__(self, key):
        return self.headers[key]

    def __setitem__(self, key, value):
        self.headers[key] = value

    def __delitem__(self, key):
        del self.headers[key]

    def __contains__(self, key):
        return key in self.headers


class Response():
    def __init__(self, url=None, status=None, statusText=None, headers=None, body=None):
        self.url = url
        self.status = status
        self.statusText = statusText
        self.headers = headers
        self.body = body

    def arrayBuffer(self):
        return self.body

    def blob(self):
        return self.body

    def formData(self):
        return self.body

    def json(self):
        return self.body

    def text(self):
        return self.body

    def clone(self):
        return Response(self.url, self.status, self.statusText, self.headers, self.body)

    def __str__(self):
        return str(self.body)

    def __repr__(self):
        return str(self.body)

    def __iter__(self):
        return self.body.__iter__()

    def __next__(self):
        return self.body.__next__()

    def __getitem__(self, key):
        return self.body[key]

    def __setitem__(self, key, value):
        self.body[key] = value

    def __delitem__(self, key):
        del self.body[key]

    def __contains__(self, key):
        return key in self.body


class Request():
    def __init__(self, url=None, method=None, headers=None, body=None, mode=None, credentials=None, cache=None):
        self.url = url
        self.method = method
        self.headers = headers
        self.body = body
        self.mode = mode
        self.credentials = credentials
        self.cache = cache

    def clone(self):
        return Request(self.url, self.method, self.headers, self.body, self.mode, self.credentials, self.cache)

    def arrayBuffer(self):
        return self.body
