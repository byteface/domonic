"""
domonic.atom
====================================

Atom tag constructors for generating feeds with domonic.
"""

from __future__ import annotations

from typing import Any

from domonic.xml._elements import (XMLElement, register_xml_tags,
                                   xml_attribute_aliases, xml_tag_alias)

XMLNS = "http://www.w3.org/2005/Atom"
ATOM_NAMESPACE = XMLNS

atom_tags = [
    "feed",
    "entry",
    "author",
    "category",
    "content",
    "contributor",
    "email",
    "generator",
    "icon",
    "id",
    "link",
    "logo",
    "name",
    "published",
    "rights",
    "source",
    "subtitle",
    "summary",
    "title",
    "updated",
    "uri",
]

atom_attributes = [
    "href",
    "hreflang",
    "label",
    "length",
    "rel",
    "scheme",
    "src",
    "term",
    "title",
    "type",
    "xml:base",
    "xml:lang",
    "xmlns",
]

_ATOM_ATTRIBUTE_ALIASES = xml_attribute_aliases(atom_attributes)
_ATOM_DEFAULTS = {"feed": {"xmlns": XMLNS}}


class AtomElement(XMLElement):
    """Base class for Atom elements."""

    _attribute_aliases = _ATOM_ATTRIBUTE_ALIASES
    _namespace_uri = XMLNS


register_xml_tags(
    globals(),
    atom_tags,
    base=AtomElement,
    defaults_by_tag=_ATOM_DEFAULTS,
    attribute_aliases=_ATOM_ATTRIBUTE_ALIASES,
    namespace_uri=XMLNS,
)
_ATOM_TAG_LOOKUP = frozenset(atom_tags)
_ATOM_ALIAS_TO_TAG = {xml_tag_alias(tag_name): tag_name for tag_name in atom_tags}


def create_element(
    name: str = "atom_element", *args: Any, **kwargs: Any
) -> AtomElement:
    """Create an Atom element by XML tag name or Python constructor alias."""
    tag_name = str(name or "atom_element").strip() or "atom_element"
    tag_name = _ATOM_ALIAS_TO_TAG.get(tag_name, tag_name)
    if tag_name in _ATOM_TAG_LOOKUP:
        return globals()[xml_tag_alias(tag_name)](*args, **kwargs)

    custom_atom_tag = type(
        "atom_element", (AtomElement,), {"name": tag_name, "__module__": __name__}
    )
    return custom_atom_tag(*args, **kwargs)


__all__ = [
    "XMLNS",
    "ATOM_NAMESPACE",
    "AtomElement",
    "atom_tags",
    "atom_attributes",
    "create_element",
    *[xml_tag_alias(tag_name) for tag_name in atom_tags],
]
