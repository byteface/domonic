"""
domonic.webapi.encoding
====================================
https://developer.mozilla.org/en-US/docs/Web/API/Encoding_API
"""

import array
import codecs
from collections.abc import Sequence

from domonic.javascript import (ArrayBuffer, DataView, Float32Array,
                                Float64Array, Int8Array, Int16Array,
                                Int32Array, Uint8Array, Uint16Array,
                                Uint32Array)
from domonic.webapi.streams import ReadableStream

_BUFFER_VIEW_TYPES = (
    Uint8Array,
    Int8Array,
    Uint16Array,
    Int16Array,
    Int32Array,
    Uint32Array,
    Float32Array,
    Float64Array,
)

_UTF8_BOM = "\ufeff"


def _build_encoding_labels():
    labels = {}

    def add(canonical, codec, *names):
        labels[canonical] = (canonical, codec)
        for name in names:
            labels[name.strip().lower()] = (canonical, codec)

    add(
        "utf-8",
        "utf-8",
        "unicode-1-1-utf-8",
        "unicode11utf8",
        "unicode20utf8",
        "utf8",
        "x-unicode20utf8",
    )
    add("ibm866", "cp866", "866", "cp866", "csibm866")
    add(
        "windows-1252",
        "cp1252",
        "ansi_x3.4-1968",
        "ascii",
        "cp1252",
        "cp819",
        "csisolatin1",
        "ibm819",
        "iso-8859-1",
        "iso-ir-100",
        "iso8859-1",
        "iso88591",
        "iso_8859-1",
        "iso_8859-1:1987",
        "l1",
        "latin-1",
        "latin1",
        "us-ascii",
        "x-cp1252",
    )
    add(
        "iso-8859-2",
        "iso8859_2",
        "csisolatin2",
        "iso-ir-101",
        "iso8859-2",
        "iso88592",
        "iso_8859-2",
        "iso_8859-2:1987",
        "l2",
        "latin2",
    )
    add(
        "iso-8859-3",
        "iso8859_3",
        "csisolatin3",
        "iso-ir-109",
        "iso8859-3",
        "iso88593",
        "iso_8859-3",
        "iso_8859-3:1988",
        "l3",
        "latin3",
    )
    add(
        "iso-8859-4",
        "iso8859_4",
        "csisolatin4",
        "iso-ir-110",
        "iso8859-4",
        "iso88594",
        "iso_8859-4",
        "iso_8859-4:1988",
        "l4",
        "latin4",
    )
    add(
        "iso-8859-5",
        "iso8859_5",
        "csisolatincyrillic",
        "cyrillic",
        "iso-ir-144",
        "iso8859-5",
        "iso88595",
        "iso_8859-5",
        "iso_8859-5:1988",
    )
    add(
        "iso-8859-6",
        "iso8859_6",
        "arabic",
        "asmo-708",
        "csiso88596e",
        "csiso88596i",
        "csisolatinarabic",
        "ecma-114",
        "iso-8859-6-e",
        "iso-8859-6-i",
        "iso-ir-127",
        "iso8859-6",
        "iso88596",
        "iso_8859-6",
        "iso_8859-6:1987",
    )
    add(
        "iso-8859-7",
        "iso8859_7",
        "csisolatingreek",
        "ecma-118",
        "elot_928",
        "greek",
        "greek8",
        "iso-ir-126",
        "iso8859-7",
        "iso88597",
        "iso_8859-7",
        "iso_8859-7:1987",
        "sun_eu_greek",
    )
    add(
        "iso-8859-8",
        "iso8859_8",
        "csiso88598e",
        "csisolatinhebrew",
        "hebrew",
        "iso-8859-8-e",
        "iso-ir-138",
        "iso8859-8",
        "iso88598",
        "iso_8859-8",
        "iso_8859-8:1988",
        "visual",
    )
    add(
        "iso-8859-8-i",
        "iso8859_8",
        "csiso88598i",
        "iso-8859-8-i",
        "logical",
    )
    add(
        "iso-8859-10",
        "iso8859_10",
        "csisolatin6",
        "iso-ir-157",
        "iso8859-10",
        "iso885910",
        "l6",
        "latin6",
    )
    add("iso-8859-13", "iso8859_13", "iso8859-13", "iso885913")
    add(
        "iso-8859-14",
        "iso8859_14",
        "iso8859-14",
        "iso885914",
        "iso-celtic",
        "iso-ir-199",
        "l8",
        "latin8",
    )
    add(
        "iso-8859-15",
        "iso8859_15",
        "csisolatin9",
        "iso8859-15",
        "iso885915",
        "iso_8859-15",
        "l9",
        "latin9",
    )
    add("iso-8859-16", "iso8859_16", "iso8859-16")
    add("koi8-r", "koi8_r", "cskoi8r", "koi", "koi8", "koi8_r")
    add("koi8-u", "koi8_u", "koi8-ru")
    add("macintosh", "mac_roman", "csmacintosh", "mac", "x-mac-roman")
    add(
        "windows-874",
        "cp874",
        "dos-874",
        "iso-8859-11",
        "iso8859-11",
        "iso885911",
        "tis-620",
    )
    add("windows-1250", "cp1250", "cp1250", "x-cp1250")
    add("windows-1251", "cp1251", "cp1251", "x-cp1251")
    add("windows-1253", "cp1253", "cp1253", "x-cp1253")
    add(
        "windows-1254",
        "cp1254",
        "cp1254",
        "csisolatin5",
        "iso-8859-9",
        "iso-ir-148",
        "iso8859-9",
        "iso88599",
        "iso_8859-9",
        "iso_8859-9:1989",
        "l5",
        "latin5",
        "x-cp1254",
    )
    add("windows-1255", "cp1255", "cp1255", "x-cp1255")
    add("windows-1256", "cp1256", "cp1256", "x-cp1256")
    add("windows-1257", "cp1257", "cp1257", "x-cp1257")
    add("windows-1258", "cp1258", "cp1258", "x-cp1258")
    add("x-mac-cyrillic", "mac_cyrillic", "x-mac-ukrainian")
    add(
        "gbk",
        "gbk",
        "chinese",
        "csgb2312",
        "csiso58gb231280",
        "gb2312",
        "gb_2312",
        "gb_2312-80",
        "iso-ir-58",
        "x-gbk",
    )
    add("gb18030", "gb18030")
    add("big5", "big5", "big5-hkscs", "cn-big5", "csbig5", "x-x-big5")
    add("euc-jp", "euc_jp", "cseucpkdfmtjapanese", "x-euc-jp")
    add("iso-2022-jp", "iso2022_jp", "csiso2022jp")
    add(
        "shift_jis",
        "shift_jis",
        "csshiftjis",
        "ms932",
        "ms_kanji",
        "shift-jis",
        "sjis",
        "windows-31j",
        "x-sjis",
    )
    add(
        "euc-kr",
        "euc_kr",
        "cseuckr",
        "csksc56011987",
        "iso-ir-149",
        "korean",
        "ks_c_5601-1987",
        "ks_c_5601-1989",
        "ksc5601",
        "ksc_5601",
        "windows-949",
    )
    add(
        "replacement",
        "replacement",
        "csiso2022kr",
        "hz-gb-2312",
        "iso-2022-cn",
        "iso-2022-cn-ext",
        "iso-2022-kr",
    )
    add("utf-16be", "utf-16-be")
    add("utf-16le", "utf-16-le", "utf-16")
    add("x-user-defined", "x-user-defined")
    return labels


_ENCODING_LABELS = _build_encoding_labels()


def _normalize_encoding(label):
    label = "utf-8" if label is None else str(label).strip().lower()
    if label in _ENCODING_LABELS:
        return _ENCODING_LABELS[label]
    codec = codecs.lookup(label)
    return codec.name, codec.name


def _get_option(options, name, default=False):
    if isinstance(options, dict):
        return options.get(name, default)
    if options is not None and hasattr(options, name):
        return getattr(options, name)
    return default


def _bytes_from_array_buffer(buffer, byte_offset=0, byte_length=None):
    raw = buffer.buffer if isinstance(buffer, ArrayBuffer) else buffer
    if isinstance(raw, array.array):
        data = raw.tobytes()
    elif isinstance(raw, (bytes, bytearray)):
        data = bytes(raw)
    elif isinstance(raw, memoryview):
        data = raw.tobytes()
    else:
        data = bytes(raw)
    byte_offset = int(byte_offset or 0)
    end = None if byte_length is None else byte_offset + int(byte_length)
    return data[byte_offset:end]


def _buffer_to_bytes(buffer):
    if buffer is None:
        return b""
    if isinstance(buffer, ReadableStream) and hasattr(buffer, "read"):
        return _buffer_to_bytes(buffer.read())
    if isinstance(buffer, DataView):
        return _bytes_from_array_buffer(
            buffer.buffer, buffer.byteOffset, buffer.byteLength
        )
    if isinstance(buffer, _BUFFER_VIEW_TYPES):
        return _bytes_from_array_buffer(
            buffer.buffer, buffer.byteOffset, buffer.byteLength
        )
    if isinstance(buffer, ArrayBuffer):
        return _bytes_from_array_buffer(buffer)
    if isinstance(buffer, array.array):
        return buffer.tobytes()
    if isinstance(buffer, memoryview):
        return buffer.tobytes()
    if isinstance(buffer, (bytes, bytearray)):
        return bytes(buffer)
    if isinstance(buffer, Sequence) and not isinstance(buffer, str):
        return bytes(int(item) & 0xFF for item in buffer)
    raise TypeError("TextDecoder.decode() input must be bytes-like")


def _decode_x_user_defined(data):
    return "".join(
        chr(byte) if byte < 0x80 else chr(0xF780 + byte - 0x80) for byte in data
    )


def _decode_replacement(data):
    return "" if not data else "\ufffd"


def _set_buffer_byte(buffer, index, value):
    value = int(value) & 0xFF
    if isinstance(buffer, DataView):
        buffer.setUint8(index, value)
    elif isinstance(buffer, _BUFFER_VIEW_TYPES):
        buffer[index] = value
    elif isinstance(buffer, ArrayBuffer):
        buffer[index] = value
    elif isinstance(buffer, memoryview):
        buffer[index] = value
    elif isinstance(buffer, bytearray):
        buffer[index] = value
    else:
        raise TypeError("encodeInto() destination must be a writable byte buffer")


def _buffer_byte_length(buffer):
    if isinstance(buffer, (DataView, ArrayBuffer)):
        return int(buffer.byteLength)
    if isinstance(buffer, _BUFFER_VIEW_TYPES):
        return int(buffer.byteLength)
    if isinstance(buffer, (bytearray, memoryview)):
        return len(buffer)
    raise TypeError("encodeInto() destination must be a writable byte buffer")


def _utf16_code_units(character):
    return len(character.encode("utf-16-le")) // 2


class TextEncoderEncodeIntoResult(dict):
    def __init__(self, read=0, written=0):
        super().__init__(read=read, written=written)

    @property
    def read(self):
        return self["read"]

    @property
    def written(self):
        return self["written"]


class TextDecoder:
    def __init__(self, encoding="utf-8", options=None, fatal=False, ignoreBOM=False):
        if isinstance(options, dict):
            fatal = options.get("fatal", fatal)
            ignoreBOM = options.get("ignoreBOM", ignoreBOM)
        elif options is not None:
            fatal = _get_option(options, "fatal", fatal)
            ignoreBOM = _get_option(options, "ignoreBOM", ignoreBOM)
        self.encoding, self._codec = _normalize_encoding(encoding)
        if self._codec not in ("replacement", "x-user-defined"):
            codecs.lookup(self._codec)
        self.fatal = bool(fatal)
        self.ignoreBOM = bool(ignoreBOM)
        self._decoder = None
        self._bom_seen = False

    def _apply_bom(self, text, streaming=False):
        if self.ignoreBOM:
            return text
        if streaming:
            if not self._bom_seen:
                if not text:
                    return text
                self._bom_seen = True
                return text[1:] if text.startswith(_UTF8_BOM) else text
            return text
        return text[1:] if text.startswith(_UTF8_BOM) else text

    def _decode_custom(self, data):
        if self._codec == "replacement":
            return _decode_replacement(data)
        if self._codec == "x-user-defined":
            return _decode_x_user_defined(data)
        return None

    def decode(self, bytes_or_buffer=None, options=None, **kwargs):
        stream = bool(kwargs.get("stream", _get_option(options, "stream", False)))
        data = _buffer_to_bytes(bytes_or_buffer)
        errors = "strict" if self.fatal else "replace"
        custom = self._decode_custom(data)
        if custom is not None:
            return self._apply_bom(custom, streaming=stream)

        was_streaming = self._decoder is not None
        if stream or was_streaming:
            if self._decoder is None:
                self._decoder = codecs.getincrementaldecoder(self._codec)(errors=errors)
                self._bom_seen = False
            text = self._decoder.decode(data, final=not stream)
            text = self._apply_bom(text, streaming=True)
            if not stream:
                self._decoder = None
                self._bom_seen = False
            return text
        return self._apply_bom(data.decode(self._codec, errors=errors))

    def __repr__(self):
        return (
            f"<TextDecoder encoding={self.encoding} "
            f"fatal={self.fatal} ignoreBOM={self.ignoreBOM}>"
        )


class TextEncoder:
    def __init__(self, encoding="utf-8"):
        canonical, _ = _normalize_encoding(encoding)
        if canonical != "utf-8":
            raise LookupError("TextEncoder only supports utf-8")
        self.encoding = "utf-8"

    def encode(self, string):
        return str(string).encode("utf-8")

    def encodeInto(self, string, bytes_or_buffer):
        source = str(string)
        read = 0
        written = 0
        capacity = _buffer_byte_length(bytes_or_buffer)
        for character in source:
            encoded = character.encode("utf-8")
            if written + len(encoded) > capacity:
                break
            for byte in encoded:
                _set_buffer_byte(bytes_or_buffer, written, byte)
                written += 1
            read += _utf16_code_units(character)
        return TextEncoderEncodeIntoResult(read=read, written=written)

    def __repr__(self):
        return '<TextEncoder encoding="utf-8">'


class TextDecoderStream(ReadableStream):
    def __init__(self, encoding="utf-8", options=None, fatal=False, ignoreBOM=False):
        super().__init__()
        self.decoder = TextDecoder(encoding, options, fatal=fatal, ignoreBOM=ignoreBOM)
        self.encoding = self.decoder.encoding
        self.fatal = self.decoder.fatal
        self.ignoreBOM = self.decoder.ignoreBOM
        self.readable = self
        self.writable = self
        self._chunks = []

    def write(self, chunk):
        text = self.decoder.decode(chunk, {"stream": True})
        if text:
            self._chunks.append(text)
        return text

    def close(self):
        text = self.decoder.decode()
        if text:
            self._chunks.append(text)
        return text

    def read(self, size=None):
        output = "".join(self._chunks)
        self._chunks = []
        if size is None or size >= len(output):
            return output
        self._chunks.append(output[size:])
        return output[:size]

    def decode(self, chunk):
        return self.decoder.decode(chunk)

    transform = decode

    def __repr__(self):
        return f"<TextDecoderStream encoding={self.decoder.encoding}>"


class TextEncoderStream(ReadableStream):
    def __init__(self, encoding="utf-8"):
        super().__init__()
        self.encoder = TextEncoder(encoding)
        self.encoding = self.encoder.encoding
        self.readable = self
        self.writable = self
        self._chunks = []

    def write(self, chunk):
        data = self.encoder.encode(chunk)
        if data:
            self._chunks.append(data)
        return data

    def close(self):
        return b""

    def read(self, size=None):
        output = b"".join(self._chunks)
        self._chunks = []
        if size is None or size >= len(output):
            return output
        self._chunks.append(output[size:])
        return output[:size]

    def encode(self, chunk):
        return self.encoder.encode(chunk)

    transform = encode

    def __repr__(self):
        return f"<TextEncoderStream encoding={self.encoder.encoding}>"
