"""
    domonic.webapi.urlpattern
    ====================================
    https://developer.mozilla.org/en-US/docs/Web/API/URLPattern
"""


class URLPattern:

    def __init__(self, pattern):
        """[matches URLs or parts of URLs against a pattern.
        The pattern can contain capturing groups that extract parts of the matched URL.]

        Args:
            pattern (str): [The pattern to match against.]
        """
        self.pattern = pattern
        self.hash = ''
        self.hostname = ''
        self.href = ''
        self.origin = ''
        self.pathname = ''
        self.port = ''
        self.protocol = ''
        self.search = ''
        self.username = ''

    def __str__(self):
        return self.pattern

    # https://developer.mozilla.org/en-US/docs/Web/API/URLPattern/exec #TODO - unit tests from this page
    def exec_(self, input, baseURL=None):
        """[Returns an object with the matched parts of the URL or None if the URL does not match.]

        Args:
            url (str): [The URL or URL parts to match against]
            baseURL (str, optional): [the base URL to use in cases where input is a relative URL]. Defaults to None.
        """
        # if baseURL is None:
        #     baseURL = ''
        # else:
        #     baseURL = baseURL.href
        # if input == self.pattern:
        #     return self.href
        # else:
        #     return None
        raise NotImplementedError

    # TODO - unit tests
    def test(self, url):
        """[summary]

        Args:
            url (str): [description]
        """
        raise NotImplementedError
