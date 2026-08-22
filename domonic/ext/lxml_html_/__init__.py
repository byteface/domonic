"""
domonic.ext.lxml_html_
====================================

Adapter for using lxml.html as a frontend parser while rebuilding a
domonic document tree from the parsed lxml tree.
"""

from __future__ import annotations

from lxml import html

from domonic.ext.html5_parser_.dom import adapt


def parse(source, return_root=True, **kwargs):
    document = html.document_fromstring(source)
    tree = document.getroottree()
    return adapt(tree, return_root=return_root, **kwargs)
