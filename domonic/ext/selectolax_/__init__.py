"""
    domonic.ext.selectolax_
    ====================================

    Fast hybrid adapter for using selectolax as a frontend parser and then
    rebuilding a domonic tree via the lxml_html adapter.
"""

from __future__ import annotations

from domonic.ext.lxml_html_ import parse as lxml_html_parse


def parse(html, return_root=True, **kwargs):
    try:
        from selectolax.lexbor import LexborHTMLParser
    except ImportError:
        from selectolax.parser import HTMLParser as LexborHTMLParser

    normalized_html = LexborHTMLParser(html).raw_html
    if isinstance(normalized_html, (bytes, bytearray)):
        normalized_html = normalized_html.decode("utf-8", errors="replace")
    return lxml_html_parse(normalized_html, return_root=return_root, **kwargs)
