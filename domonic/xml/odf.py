"""
domonic.odf
====================================

OpenDocument Format XML tag constructors for domonic.
"""

from __future__ import annotations

from typing import Any

from domonic.xml._elements import (XMLElement, register_xml_tags,
                                   xml_attribute_aliases, xml_tag_alias)

OFFICE = "urn:oasis:names:tc:opendocument:xmlns:office:1.0"
TEXT = "urn:oasis:names:tc:opendocument:xmlns:text:1.0"
TABLE = "urn:oasis:names:tc:opendocument:xmlns:table:1.0"
DRAW = "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
STYLE = "urn:oasis:names:tc:opendocument:xmlns:style:1.0"
FO = "urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
SVG = "urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"
XLINK = "http://www.w3.org/1999/xlink"
META = "urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
MANIFEST = "urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"
CONFIG = "urn:oasis:names:tc:opendocument:xmlns:config:1.0"

ODF_VERSION = "1.2"

odf_namespaces = {
    "office": OFFICE,
    "text": TEXT,
    "table": TABLE,
    "draw": DRAW,
    "style": STYLE,
    "fo": FO,
    "svg": SVG,
    "xlink": XLINK,
    "meta": META,
    "manifest": MANIFEST,
    "config": CONFIG,
}

DEFAULT_NAMESPACES = {
    **{
        f"xmlns:{prefix}": uri
        for prefix, uri in odf_namespaces.items()
        if prefix != "manifest"
    },
    "office:version": ODF_VERSION,
}

odf_tags = [
    "office:document",
    "office:document-content",
    "office:document-meta",
    "office:document-settings",
    "office:document-styles",
    "office:body",
    "office:text",
    "office:spreadsheet",
    "office:presentation",
    "office:automatic-styles",
    "office:master-styles",
    "office:styles",
    "office:font-face-decls",
    "office:meta",
    "office:settings",
    "text:p",
    "text:h",
    "text:span",
    "text:a",
    "text:list",
    "text:list-item",
    "text:section",
    "text:soft-page-break",
    "text:line-break",
    "text:s",
    "text:tab",
    "text:bookmark",
    "text:bookmark-start",
    "text:bookmark-end",
    "table:table",
    "table:table-column",
    "table:table-row",
    "table:table-cell",
    "table:covered-table-cell",
    "draw:page",
    "draw:frame",
    "draw:image",
    "draw:text-box",
    "draw:rect",
    "draw:line",
    "draw:circle",
    "draw:custom-shape",
    "style:style",
    "style:default-style",
    "style:master-page",
    "style:page-layout",
    "style:page-layout-properties",
    "style:text-properties",
    "style:paragraph-properties",
    "style:table-properties",
    "style:table-column-properties",
    "style:table-row-properties",
    "style:table-cell-properties",
    "style:font-face",
    "meta:generator",
    "meta:initial-creator",
    "meta:creation-date",
    "meta:keyword",
    "meta:user-defined",
    "manifest:manifest",
    "manifest:file-entry",
    "config:config-item-set",
    "config:config-item",
]

odf_attributes = [
    "config:name",
    "config:type",
    "draw:name",
    "draw:style-name",
    "draw:text-style-name",
    "fo:break-before",
    "fo:font-size",
    "fo:font-weight",
    "fo:text-align",
    "manifest:full-path",
    "manifest:media-type",
    "manifest:version",
    "meta:name",
    "office:mimetype",
    "office:value",
    "office:value-type",
    "office:version",
    "style:family",
    "style:name",
    "style:parent-style-name",
    "svg:height",
    "svg:width",
    "table:name",
    "table:number-columns-repeated",
    "table:style-name",
    "text:outline-level",
    "text:style-name",
    "xlink:href",
    "xlink:type",
]

_ODF_ATTRIBUTE_ALIASES = xml_attribute_aliases(odf_attributes)
_ODF_DEFAULTS = {
    tag_name: DEFAULT_NAMESPACES
    for tag_name in odf_tags
    if tag_name.startswith("office:document")
}
_ODF_DEFAULTS["manifest:manifest"] = {
    "xmlns:manifest": MANIFEST,
    "manifest:version": ODF_VERSION,
}


class ODFElement(XMLElement):
    """Base class for OpenDocument XML elements."""

    _attribute_aliases = _ODF_ATTRIBUTE_ALIASES
    _prefix_namespaces = odf_namespaces


register_xml_tags(
    globals(),
    odf_tags,
    base=ODFElement,
    defaults_by_tag=_ODF_DEFAULTS,
    attribute_aliases=_ODF_ATTRIBUTE_ALIASES,
    prefix_namespaces=odf_namespaces,
)
odf_tag_aliases = {xml_tag_alias(tag_name): tag_name for tag_name in odf_tags}
_ODF_TAG_LOOKUP = frozenset(odf_tags)


def create_element(name: str = "odf_element", *args: Any, **kwargs: Any) -> ODFElement:
    """Create an ODF element by XML tag name or Python constructor alias."""
    tag_name = str(name or "odf_element").strip() or "odf_element"
    tag_name = odf_tag_aliases.get(tag_name, tag_name)
    if tag_name in _ODF_TAG_LOOKUP:
        return globals()[xml_tag_alias(tag_name)](*args, **kwargs)

    custom_odf_tag = type(
        "odf_element", (ODFElement,), {"name": tag_name, "__module__": __name__}
    )
    return custom_odf_tag(*args, **kwargs)


def create_odf_element(tag_name: str, *args: Any, **kwargs: Any) -> ODFElement:
    """Create an ODF element by its XML tag name."""
    return create_element(tag_name, *args, **kwargs)


__all__ = [
    "OFFICE",
    "TEXT",
    "TABLE",
    "DRAW",
    "STYLE",
    "FO",
    "SVG",
    "XLINK",
    "META",
    "MANIFEST",
    "CONFIG",
    "ODF_VERSION",
    "DEFAULT_NAMESPACES",
    "ODFElement",
    "odf_namespaces",
    "odf_tags",
    "odf_attributes",
    "odf_tag_aliases",
    "create_element",
    "create_odf_element",
    *[xml_tag_alias(tag_name) for tag_name in odf_tags],
]
