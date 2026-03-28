"""
    domonic.ext.markupever_
    ====================================

    Fast hybrid adapter for using markupever as a frontend parser and then
    rebuilding a domonic tree via the lxml_html adapter.
"""

from __future__ import annotations

from domonic.ext.lxml_html_ import parse as lxml_html_parse


def parse(html, return_root=True, **kwargs):
    import markupever

    normalized_html = markupever.parse(html).serialize(indent=0, is_html=True)
    return lxml_html_parse(normalized_html, return_root=return_root, **kwargs)
