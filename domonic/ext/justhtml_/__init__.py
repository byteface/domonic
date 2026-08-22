"""
domonic.ext.justhtml_
====================================

Adapter for using justhtml as a frontend parser while rebuilding a
domonic document tree from the parsed output.
"""

from __future__ import annotations

from html5lib import HTMLParser

from domonic.ext.html5lib_ import getTreeBuilder


def _serialize(node) -> str:
    for attr in ("to_html", "serialize", "html", "to_string"):
        candidate = getattr(node, attr, None)
        if callable(candidate):
            try:
                return candidate(pretty=False)
            except TypeError:
                return candidate()
        if isinstance(candidate, str):
            return candidate
    return str(node)


def parse(html, return_root=True, **kwargs):
    from justhtml import JustHTML

    parsed = JustHTML(html, fragment=False, sanitize=False)
    serialized = _serialize(parsed)
    parser = HTMLParser(tree=getTreeBuilder())
    document = parser.parse(serialized)
    return document.documentElement if return_root else document
