"""
    domonic.rss
    ====================================

    RSS tag constructors for generating feeds with domonic.
"""

from __future__ import annotations

from typing import Any

from domonic.xml._elements import XMLElement, register_xml_tags, xml_attribute_aliases, xml_tag_alias


RSS_VERSION = "2.0"
XMLNS_ATOM = "http://www.w3.org/2005/Atom"
XMLNS_CONTENT = "http://purl.org/rss/1.0/modules/content/"
XMLNS_DC = "http://purl.org/dc/elements/1.1/"
XMLNS_MEDIA = "http://search.yahoo.com/mrss/"
XMLNS_SY = "http://purl.org/rss/1.0/modules/syndication/"

rss_namespaces = {
    "atom": XMLNS_ATOM,
    "content": XMLNS_CONTENT,
    "dc": XMLNS_DC,
    "media": XMLNS_MEDIA,
    "sy": XMLNS_SY,
}

rss_tags = [
    "rss",
    "channel",
    "title",
    "link",
    "description",
    "item",
    "language",
    "copyright",
    "managingEditor",
    "webMaster",
    "pubDate",
    "lastBuildDate",
    "category",
    "generator",
    "docs",
    "cloud",
    "ttl",
    "image",
    "url",
    "rating",
    "textInput",
    "name",
    "skipHours",
    "skipDays",
    "hour",
    "day",
    "author",
    "comments",
    "enclosure",
    "guid",
    "source",
    "atom:link",
    "content:encoded",
    "dc:creator",
    "dc:date",
    "media:content",
    "media:thumbnail",
    "sy:updatePeriod",
    "sy:updateFrequency",
]

rss_attributes = [
    "domain",
    "height",
    "href",
    "isPermaLink",
    "length",
    "rel",
    "type",
    "url",
    "version",
    "width",
    "xmlns:atom",
    "xmlns:content",
    "xmlns:dc",
    "xmlns:media",
    "xmlns:sy",
]

_RSS_ATTRIBUTE_ALIASES = {
    **xml_attribute_aliases(rss_attributes),
    "is_perma_link": "isPermaLink",
}
_RSS_DEFAULTS = {"rss": {"version": RSS_VERSION}}


class RSSElement(XMLElement):
    """Base class for RSS elements."""

    _attribute_aliases = _RSS_ATTRIBUTE_ALIASES
    _prefix_namespaces = rss_namespaces


register_xml_tags(
    globals(),
    rss_tags,
    base=RSSElement,
    defaults_by_tag=_RSS_DEFAULTS,
    attribute_aliases=_RSS_ATTRIBUTE_ALIASES,
    prefix_namespaces=rss_namespaces,
)
_RSS_TAG_LOOKUP = frozenset(rss_tags)
_RSS_ALIAS_TO_TAG = {xml_tag_alias(tag_name): tag_name for tag_name in rss_tags}


def create_element(name: str = "rss_element", *args: Any, **kwargs: Any) -> RSSElement:
    """Create an RSS element by XML tag name or Python constructor alias."""
    tag_name = str(name or "rss_element").strip() or "rss_element"
    tag_name = _RSS_ALIAS_TO_TAG.get(tag_name, tag_name)
    if tag_name in _RSS_TAG_LOOKUP:
        return globals()[xml_tag_alias(tag_name)](*args, **kwargs)

    custom_rss_tag = type("rss_element", (RSSElement,), {"name": tag_name, "__module__": __name__})
    return custom_rss_tag(*args, **kwargs)


__all__ = [
    "RSS_VERSION",
    "XMLNS_ATOM",
    "XMLNS_CONTENT",
    "XMLNS_DC",
    "XMLNS_MEDIA",
    "XMLNS_SY",
    "RSSElement",
    "rss_namespaces",
    "rss_tags",
    "rss_attributes",
    "create_element",
    *[xml_tag_alias(tag_name) for tag_name in rss_tags],
]
