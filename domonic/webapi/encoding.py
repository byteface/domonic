"""
    domonic.webapi.encoding
    ====================================
    https://developer.mozilla.org/en-US/docs/Web/API/Encoding_API
"""

from domonic.webapi.streams import ReadableStream
from domonic.javascript import (Uint8Array, Int8Array, Uint16Array, Int16Array, Int32Array, Uint32Array, Float32Array, Float64Array, DataView)
from domonic.javascript import String, Function
from domonic.javascript import ArrayBuffer
# from domonic.javascript import ArrayBufferView


class TextDecoder:
    def __init__(self, encoding="utf-8"):
        self.encoding = encoding

    def decode(self, bytes_or_buffer):
        if self.encoding == "utf-8":
            # get the bytes from the buffer
            if isinstance(bytes_or_buffer, ReadableStream):
                bytes_or_buffer = bytes_or_buffer.read()
            if isinstance(bytes_or_buffer, ArrayBuffer):
                bytes_or_buffer = bytes_or_buffer.buffer
            if isinstance(bytes_or_buffer, (Uint8Array, Int8Array, Uint16Array, Int16Array, Int32Array, Uint32Array, Float32Array, Float64Array, DataView)):
                bytes_or_buffer = bytes_or_buffer.buffer
            # if isinstance(bytes_or_buffer, ArrayBufferView):

            # convert the bytes to a string
            # return bytes_or_buffer.decode("utf-8")
            # return "".join([b.decode('UTF-8') for b in bytes_or_buffer])
            b = bytearray(bytes_or_buffer)
            return b.decode("utf-8")
            # return b.decode("utf-16")

    # def __repr__(self):
    #     return f"<TextDecoder encoding={self.encoding}>"


class TextEncoder:
    def __init__(self, encoding="utf-8"):
        self.encoding = encoding

    def encode(self, string):
        return string.encode(self.encoding)

    def encodeInto(self, string, bytes_or_buffer):
        return bytes_or_buffer.encode(self.encoding)

    def __repr__(self):
        return f"<TextEncoder encoding={self.encoding}>"


class TextDecoderStream(ReadableStream):
    def __init__(self, encoding="utf-8"):
        super().__init__()
        # self.decoder = TextDecoder(encoding)
        self.encoding = encoding
        self.readable = True
        self.writable = False
        self.ignoreBOM = False


    def read(self, size=None):
        return self.decoder.decode(super().read(size))

    def __repr__(self):
        return f"<TextDecoderStream encoding={self.decoder.encoding}>"


class TextEncoderStream(ReadableStream):
    def __init__(self, encoding="utf-8"):
        super().__init__()
        # self.encoder = TextEncoder(encoding)
        self.encoding = encoding
        self.readable = True
        self.writable = False

    def read(self, size=None):
        return self.encoder.encode(super().read(size))

    def __repr__(self):
        return f"<TextEncoderStream encoding={self.encoder.encoding}>"