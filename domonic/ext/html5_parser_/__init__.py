#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: Apache 2.0 Copyright: 2017, Kovid Goyal <kovid at kovidgoyal.net>

import codecs
import importlib
import sys
from locale import getpreferredencoding
from typing import Final, NamedTuple


class Version(NamedTuple):
    major: int
    minor: int
    patch: int


if not hasattr(sys, "generating_docs_via_sphinx"):
    from lxml import \
        etree  # Must be imported before html_parser to initialize libxml

    try:
        # from . import html_parser
        from html5_parser import html_parser
    except ImportError:
        raise
    else:
        version = Version(html_parser.MAJOR, html_parser.MINOR, html_parser.PATCH)

        if not hasattr(etree, "adopt_external_document"):
            raise ImportError(
                "Your version of lxml is too old, version 3.8.0 is minimum"
            )

        LIBXML_VERSION = (
            (html_parser.LIBXML_VERSION // 10000) % 100,
            (html_parser.LIBXML_VERSION // 100) % 100,
            html_parser.LIBXML_VERSION % 100,
        )
        if LIBXML_VERSION[:2] != etree.LIBXML_VERSION[:2]:
            raise RuntimeError(
                "html5-parser and lxml are using different versions of libxml2."
                " This happens commonly when using pip installed versions of lxml."
                " Use pip install --no-binary lxml lxml instead."
                " libxml2 versions: html5-parser: {} != lxml: {}".format(
                    LIBXML_VERSION, etree.LIBXML_VERSION
                )
            )

BOMS: Final[tuple[bytes, ...]] = (
    codecs.BOM_UTF8,
    codecs.BOM_UTF16_BE,
    codecs.BOM_UTF16_LE,
)


def check_bom(data):
    for bom in BOMS:
        if data.startswith(bom):
            return bom


def check_for_meta_charset(raw):
    from .encoding_parser import EncodingParser  # delay load

    q = raw[: 10 * 1024]
    parser = EncodingParser(q)
    encoding = parser()
    if encoding in ("utf-16", "utf-16be", "utf-16le"):
        encoding = "utf-8"
    return encoding


def detect_encoding(raw):
    from chardet import detect  # delay load

    q = raw[: 50 * 1024]
    return detect(q)["encoding"]


PASSTHROUGH_ENCODINGS: Final[frozenset[str]] = frozenset(("utf-8", "utf8", "ascii"))


def safe_get_preferred_encoding():
    try:
        ans = getpreferredencoding(False)
    except Exception:
        return None
    else:
        try:
            return codecs.lookup(ans).name
        except LookupError:
            return None


def as_utf8(bytes_or_unicode, transport_encoding=None, fallback_encoding=None):
    if isinstance(bytes_or_unicode, bytes):
        data = bytes_or_unicode
        if transport_encoding:
            if transport_encoding.lower() not in PASSTHROUGH_ENCODINGS:
                data = bytes_or_unicode.decode(transport_encoding).encode("utf-8")
        else:
            # See
            # https://www.w3.org/TR/2011/WD-html5-20110113/parsing.html#determining-the-character-encoding
            bom = check_bom(data)
            if bom is not None:
                data = data[len(bom) :]
                if bom is not codecs.BOM_UTF8:
                    data = data.decode(bom).encode("utf-8")
            else:
                encoding = (
                    check_for_meta_charset(data)
                    or detect_encoding(data)
                    or fallback_encoding
                    or safe_get_preferred_encoding()
                    or "cp-1252"
                )
                if encoding and encoding.lower() not in PASSTHROUGH_ENCODINGS:
                    if encoding == "x-user-defined":
                        # https://encoding.spec.whatwg.org/#x-user-defined
                        buf = (
                            b if b <= 0x7F else 0xF780 + b - 0x80
                            for b in bytearray(data)
                        )
                        chr_func = globals().get("unichr", chr)
                        data = "".join(map(chr_func, buf))
                    else:
                        data = data.decode(encoding).encode("utf-8")
    else:
        data = bytes_or_unicode.encode("utf-8")
    return data


def normalize_treebuilder(x):
    if hasattr(x, "lower"):
        x = x.lower()
    return {"lxml.etree": "lxml", "etree": "stdlib_etree"}.get(x, x)


NAMESPACE_SUPPORTING_BUILDERS: Final[frozenset[str]] = frozenset(
    "lxml stdlib_etree dom lxml_html".split()
)


def parse(
    html,
    transport_encoding=None,
    namespace_elements=False,
    treebuilder="lxml",
    fallback_encoding=None,
    keep_doctype=True,
    maybe_xhtml=False,
    return_root=True,
    line_number_attr=None,
    sanitize_names=True,
    stack_size=16 * 1024,
    fragment_context=None,
):
    """Parse HTML with ``html5_parser`` and return the selected tree type.

    Args:
        html: HTML as ``bytes`` or ``str``.
        transport_encoding: Encoding to assume for byte input.
        namespace_elements: Add XML namespaces so the resulting tree is XHTML.
        treebuilder: Output tree type. Supported values include ``lxml``,
            ``lxml_html``, ``etree``, ``dom`` and ``soup``.
        fallback_encoding: Encoding used when detection fails.
        keep_doctype: Preserve the document type node when present.
        maybe_xhtml: Handle markup that may actually be XHTML.
        return_root: Return the root element instead of the full tree object.
        line_number_attr: Optional attribute name used to store element line
            numbers.
        sanitize_names: Replace invalid tag or attribute name characters.
        stack_size: Initial parser stack size.
        fragment_context: Tag name used when parsing a fragment.
    """
    data = as_utf8(html or b"", transport_encoding, fallback_encoding)
    treebuilder = normalize_treebuilder(treebuilder)
    if treebuilder == "soup":
        from .soup import parse

        return parse(
            data,
            return_root=return_root,
            keep_doctype=keep_doctype,
            stack_size=stack_size,
        )
    if treebuilder not in NAMESPACE_SUPPORTING_BUILDERS:
        namespace_elements = False
    fragment_namespace = html_parser.GUMBO_NAMESPACE_HTML
    if fragment_context:
        fragment_context = fragment_context.lower()
        if ":" in fragment_context:
            ns, fragment_context = fragment_context.split(":", 1)
            fragment_namespace = {
                "svg": html_parser.GUMBO_NAMESPACE_SVG,
                "math": html_parser.GUMBO_NAMESPACE_MATHML,
                "html": html_parser.GUMBO_NAMESPACE_HTML,
            }[ns]

    capsule = html_parser.parse(
        data,
        namespace_elements=namespace_elements or maybe_xhtml,
        keep_doctype=keep_doctype,
        maybe_xhtml=maybe_xhtml,
        line_number_attr=line_number_attr,
        sanitize_names=sanitize_names,
        stack_size=stack_size,
        fragment_context=fragment_context,
        fragment_namespace=fragment_namespace,
    )

    interpreter = None
    if treebuilder == "lxml_html":
        from lxml.html import HTMLParser

        interpreter = HTMLParser()
    ans = etree.adopt_external_document(capsule, parser=interpreter)
    if treebuilder in ("lxml", "lxml_html"):
        return ans.getroot() if return_root else ans

    if treebuilder == "domonic":
        m = importlib.import_module("domonic.ext.lxml_dom")
        return m.adapt(ans, return_root=return_root)

    m = importlib.import_module("html5_parser." + treebuilder)
    return m.adapt(ans, return_root=return_root)
