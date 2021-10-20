"""
    domonic.webapi.streams
    ====================================
    https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API
"""


class ReadableStream:
    """
    https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream
    """

    def __init__(self, *args):
        self.__args = args

    def getReader(self):
        """
        https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream/getReader
        """
        return self.__args[0]

    def pipeThrough(self, transform, options=None):
        """
        https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream/pipeThrough
        """
        return self.__args[1](transform, options)

    def pipeTo(self, dest, options=None):
        """
        https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream/pipeTo
        """
        return self.__args[2](dest, options)


# class WritableStream:
#     """
#     https://developer.mozilla.org/en-US/docs/Web/API/WritableStream
#     """

#     def __init__(self, *args):
#         self.__args = args

#     def getWriter(self):
#         """
#         https://developer.mozilla.org/en-US/docs/Web/API/WritableStream/getWriter
#         """
#         return self.__args[0]