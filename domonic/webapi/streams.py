"""
domonic.webapi.streams
====================================
https://developer.mozilla.org/en-US/docs/Web/API/Streams_API
"""

from __future__ import annotations

import zlib
from contextlib import suppress
from typing import Any


_FORMAT_WBITS = {
    "gzip": zlib.MAX_WBITS | 16,
    "deflate": zlib.MAX_WBITS,
    "deflate-raw": -zlib.MAX_WBITS,
}


def _normalize_format(format: str) -> str:
    normalized = str(format).lower()
    if normalized not in _FORMAT_WBITS:
        supported = ", ".join(sorted(_FORMAT_WBITS))
        raise TypeError(
            f"Unsupported compression format: {format!r}. Expected one of: {supported}"
        )
    return normalized


def _coerce_bytes(chunk: Any) -> bytes:
    if chunk is None:
        return b""
    if isinstance(chunk, bytes):
        return chunk
    if isinstance(chunk, bytearray):
        return bytes(chunk)
    if isinstance(chunk, memoryview):
        return chunk.tobytes()
    if isinstance(chunk, str):
        return chunk.encode("utf-8")

    blob_bytes = getattr(chunk, "bytes", None)
    if callable(blob_bytes):
        return blob_bytes()

    buffer = getattr(chunk, "buffer", None)
    if buffer is not None:
        nested = getattr(buffer, "buffer", buffer)
        with suppress(TypeError):
            return bytes(nested)

    return bytes(chunk)


def _join_chunks(chunks):
    if not chunks:
        return b""
    try:
        return b"".join(_coerce_bytes(chunk) for chunk in chunks)
    except (TypeError, ValueError):
        return "".join(str(chunk) for chunk in chunks)


def _compress_bytes(format: str, chunk: Any) -> bytes:
    compressor = zlib.compressobj(wbits=_FORMAT_WBITS[_normalize_format(format)])
    return compressor.compress(_coerce_bytes(chunk)) + compressor.flush()


def _decompress_bytes(format: str, chunk: Any) -> bytes:
    decompressor = zlib.decompressobj(wbits=_FORMAT_WBITS[_normalize_format(format)])
    return decompressor.decompress(_coerce_bytes(chunk)) + decompressor.flush()


class ReadableStream:
    """
    https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream
    """

    def __init__(self, *args):
        self.__args = args
        self._chunks = []
        self.readable = self

    def getReader(self):
        """
        https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream/getReader
        """
        if self.__args:
            return self.__args[0]
        return self.read

    def write(self, chunk):
        self._chunks.append(chunk)
        return chunk

    def read(self, size=None):
        if self._chunks:
            output = _join_chunks(self._chunks)
            self._chunks = []
        elif self.__args and callable(self.__args[0]):
            output = self.__args[0]()
        elif self.__args:
            output = self.__args[0]
        else:
            output = b""

        if size is None or size >= len(output):
            return output

        remainder = output[size:]
        if remainder:
            self._chunks.append(remainder)
        return output[:size]

    def pipeThrough(self, transform, options=None):
        """
        https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream/pipeThrough
        """
        if len(self.__args) > 1 and callable(self.__args[1]):
            return self.__args[1](transform, options)

        if hasattr(transform, "write"):
            transform.write(self.read())
            if hasattr(transform, "close"):
                transform.close()
            return getattr(transform, "readable", transform)

        if hasattr(transform, "transform"):
            return ReadableStream(transform.transform(self.read()))

        if callable(transform):
            return transform(self.read())

        raise TypeError("pipeThrough() expects a transform stream or callable")

    def pipeTo(self, dest, options=None):
        """
        https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream/pipeTo
        """
        if len(self.__args) > 2 and callable(self.__args[2]):
            return self.__args[2](dest, options)

        data = self.read()
        if hasattr(dest, "write"):
            result = dest.write(data)
            if hasattr(dest, "close"):
                dest.close()
            return result

        if callable(dest):
            return dest(data)

        raise TypeError("pipeTo() expects a writable stream or callable")


class WritableStream:
    """
    https://developer.mozilla.org/en-US/docs/Web/API/WritableStream
    """

    def __init__(self, sink=None):
        self.sink = sink
        self._chunks = []
        self.closed = False
        self.writable = self

    def getWriter(self):
        """
        https://developer.mozilla.org/en-US/docs/Web/API/WritableStream/getWriter
        """
        return self

    def write(self, chunk):
        if self.closed:
            raise ValueError("Cannot write to a closed WritableStream")

        if hasattr(self.sink, "write"):
            return self.sink.write(chunk)
        if callable(self.sink):
            return self.sink(chunk)

        self._chunks.append(chunk)
        return chunk

    def close(self):
        self.closed = True
        return None

    def read(self, size=None):
        output = _join_chunks(self._chunks)
        self._chunks = []
        if size is None or size >= len(output):
            return output
        self._chunks.append(output[size:])
        return output[:size]


class TransformStream(ReadableStream):
    """
    https://developer.mozilla.org/en-US/docs/Web/API/TransformStream
    """

    def __init__(self, transformer=None):
        super().__init__()
        self.transformer = transformer
        self.readable = self
        self.writable = self

    def transform(self, chunk):
        if hasattr(self.transformer, "transform"):
            return self.transformer.transform(chunk)
        if callable(self.transformer):
            return self.transformer(chunk)
        return chunk

    def write(self, chunk):
        output = self.transform(chunk)
        if output is not None:
            self._chunks.append(output)
        return output

    def close(self):
        if hasattr(self.transformer, "flush"):
            output = self.transformer.flush()
            if output is not None:
                self._chunks.append(output)
            return output
        return None


class CompressionStream(TransformStream):
    """
    https://developer.mozilla.org/en-US/docs/Web/API/CompressionStream
    """

    def __init__(self, format):
        super().__init__()
        self.format = _normalize_format(format)
        self._compressor = zlib.compressobj(wbits=_FORMAT_WBITS[self.format])
        self._closed = False

    def compress(self, chunk):
        return _compress_bytes(self.format, chunk)

    transform = compress

    def write(self, chunk):
        if self._closed:
            raise ValueError("Cannot write to a closed CompressionStream")
        output = self._compressor.compress(_coerce_bytes(chunk))
        if output:
            self._chunks.append(output)
        return output

    def close(self):
        if self._closed:
            return b""
        self._closed = True
        output = self._compressor.flush()
        if output:
            self._chunks.append(output)
        return output


class DecompressionStream(TransformStream):
    """
    https://developer.mozilla.org/en-US/docs/Web/API/DecompressionStream
    """

    def __init__(self, format):
        super().__init__()
        self.format = _normalize_format(format)
        self._decompressor = zlib.decompressobj(wbits=_FORMAT_WBITS[self.format])
        self._closed = False

    def decompress(self, chunk):
        return _decompress_bytes(self.format, chunk)

    transform = decompress

    def write(self, chunk):
        if self._closed:
            raise ValueError("Cannot write to a closed DecompressionStream")
        output = self._decompressor.decompress(_coerce_bytes(chunk))
        if output:
            self._chunks.append(output)
        return output

    def close(self):
        if self._closed:
            return b""
        self._closed = True
        output = self._decompressor.flush()
        if output:
            self._chunks.append(output)
        return output
