"""
domonic.ext._encoding
====================================

Decoding HTML bytes the way a browser does
(https://html.spec.whatwg.org/#determining-the-character-encoding): a byte
order mark wins, then the transport's charset (the HTTP header), then the
page's own ``<meta charset>`` in its first kilobyte. With none of those,
bytes that are valid UTF-8 are UTF-8 and anything else is windows-1252,
which is what a browser in an English locale falls back to.
"""

from __future__ import annotations

import codecs
import re

PRESCAN_BYTES = 1024
FALLBACK_ENCODING = "windows-1252"

_BOMS: tuple[tuple[bytes, str], ...] = (
    (b"\xef\xbb\xbf", "utf-8"),
    (b"\xff\xfe", "utf-16-le"),
    (b"\xfe\xff", "utf-16-be"),
)
_COMMENT = re.compile(rb"<!--.*?-->", re.S)
# ``<meta charset=x>`` and ``<meta http-equiv=... content="...; charset=x">``
_META_CHARSET = re.compile(rb"""<meta\s[^>]*?charset\s*=\s*["']?\s*([A-Za-z0-9_.:-]+)""", re.I)


def codec_for_label(label: str | None) -> str | None:
    """The Python codec for an encoding label, by the Encoding Standard's
    label table where it has one (so ``latin1`` means windows-1252, as in a
    browser), else by Python's own lookup. ``None`` if nothing matches."""
    if not label:
        return None
    text = str(label).strip().lower()
    if not text:
        return None
    try:
        from domonic.webapi.encoding import _normalize_encoding

        name = _normalize_encoding(text)[0]
    except Exception:
        try:
            name = codecs.lookup(text).name
        except LookupError:
            return None
    if name in ("latin-1", "latin_1", "iso8859-1", "iso-8859-1", "ascii", "us-ascii", "x-user-defined"):
        return FALLBACK_ENCODING
    try:
        return codecs.lookup(name).name
    except LookupError:
        return None


def bom_encoding(data: bytes) -> tuple[str | None, int]:
    """The encoding a byte order mark declares, and the mark's length."""
    for bom, name in _BOMS:
        if data.startswith(bom):
            return name, len(bom)
    return None, 0


def prescan(data: bytes) -> str | None:
    """The encoding the first kilobyte of markup declares in a ``<meta>``."""
    head = _COMMENT.sub(b"", data[:PRESCAN_BYTES])
    match = _META_CHARSET.search(head)
    if match is None:
        return None
    name = codec_for_label(match.group(1).decode("ascii", "replace"))
    if name is None:
        return None
    # a UTF-16 declaration in the bytes themselves is self-evidently wrong
    return "utf-8" if name.startswith("utf-16") else name


def looks_like_utf8(data: bytes) -> bool:
    try:
        codecs.getincrementaldecoder("utf-8")().decode(data[:65536], final=False)
    except UnicodeDecodeError:
        return False
    return True


def sniff_encoding(data: bytes, transport: str | None = None) -> str:
    """The encoding to decode ``data`` with; see the module docstring."""
    name, _ = bom_encoding(data)
    if name is not None:
        return name
    name = codec_for_label(transport)
    if name is not None:
        return name
    name = prescan(data)
    if name is not None:
        return name
    return "utf-8" if looks_like_utf8(data) else FALLBACK_ENCODING


_WHATWG_NAMES = {
    "utf-8": "UTF-8",
    "utf-16-le": "UTF-16LE",
    "utf-16-be": "UTF-16BE",
    "cp1252": "windows-1252",
    "cp1251": "windows-1251",
    "cp1250": "windows-1250",
    "shift_jis": "Shift_JIS",
    "euc_jp": "EUC-JP",
    "euc_kr": "EUC-KR",
    "gbk": "GBK",
    "gb18030": "gb18030",
    "big5": "Big5",
    "koi8-r": "KOI8-R",
}


def whatwg_name(codec: str) -> str:
    """The Encoding Standard's name for a Python codec (what ``document.characterSet`` reports)."""
    try:
        name = codecs.lookup(codec).name
    except LookupError:
        name = codec
    return _WHATWG_NAMES.get(name, name)


def decode_html(data: bytes, transport: str | None = None) -> tuple[str, str]:
    """Decode HTML bytes; returns the text and the encoding used."""
    encoding = sniff_encoding(data, transport)
    _, bom_length = bom_encoding(data)
    return data[bom_length:].decode(encoding, errors="replace"), encoding
