"""
domonic.xml._elements
====================================

Shared helpers for XML tag constructor modules.
"""

from __future__ import annotations

from typing import Any

from domonic.dom import Element


def xml_tag_alias(tag_name: str) -> str:
    """Return the Python constructor name for an XML tag name."""
    return tag_name.replace(":", "_").replace("-", "_")


def xml_attribute_aliases(attributes: list[str] | tuple[str, ...]) -> dict[str, str]:
    """Build Python-friendly aliases for namespaced and hyphenated XML attributes."""
    aliases: dict[str, str] = {}
    for attribute in attributes:
        alias = attribute.replace(":", "_").replace("-", "_")
        if alias != attribute:
            aliases[alias] = attribute
    return aliases


class XMLElement(Element):
    """Base element for generated XML tag constructors."""

    _attribute_aliases: dict[str, str] = {}
    _defaults: dict[str, Any] = {}
    _namespace_uri: str | None = None
    _prefix_namespaces: dict[str, str] = {}

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        attrs = dict(self._defaults)
        attrs.update(self._normalize_attrs(kwargs))
        super().__init__(*args, **attrs)
        self.namespaceURI = self._resolve_namespace_uri()

    @classmethod
    def _normalize_attrs(cls, kwargs: dict[str, Any]) -> dict[str, Any]:
        attrs: dict[str, Any] = {}
        for key, value in kwargs.items():
            name = key[1:] if key.startswith("_") else key
            name = cls._attribute_aliases.get(name, name)
            attrs[name] = value
        return attrs

    def _resolve_namespace_uri(self) -> str:
        if self._namespace_uri is not None:
            return self._namespace_uri
        prefix = self.name.split(":", 1)[0] if ":" in self.name else ""
        return self._prefix_namespaces.get(prefix, "")


def make_xml_constructor(
    tag_name: str,
    *,
    base: type[XMLElement] = XMLElement,
    defaults: dict[str, Any] | None = None,
    attribute_aliases: dict[str, str] | None = None,
    namespace_uri: str | None = None,
    prefix_namespaces: dict[str, str] | None = None,
    module_name: str | None = None,
) -> type[XMLElement]:
    """Create a domonic Element subclass for an XML tag name."""
    class_name = xml_tag_alias(tag_name)
    return type(
        class_name,
        (base,),
        {
            "__module__": module_name or base.__module__,
            "name": tag_name,
            "_attribute_aliases": attribute_aliases or {},
            "_defaults": defaults or {},
            "_namespace_uri": namespace_uri,
            "_prefix_namespaces": prefix_namespaces or {},
        },
    )


def register_xml_tags(
    namespace: dict[str, Any],
    tags: list[str],
    *,
    base: type[XMLElement] = XMLElement,
    defaults_by_tag: dict[str, dict[str, Any]] | None = None,
    attribute_aliases: dict[str, str] | None = None,
    namespace_uri: str | None = None,
    prefix_namespaces: dict[str, str] | None = None,
) -> dict[str, type[XMLElement]]:
    """Register generated XML constructors in a module namespace."""
    constructors: dict[str, type[XMLElement]] = {}
    defaults_by_tag = defaults_by_tag or {}
    module_name = namespace.get("__name__")
    for tag_name in tags:
        constructor = make_xml_constructor(
            tag_name,
            base=base,
            defaults=defaults_by_tag.get(tag_name),
            attribute_aliases=attribute_aliases,
            namespace_uri=namespace_uri,
            prefix_namespaces=prefix_namespaces,
            module_name=module_name,
        )
        alias = xml_tag_alias(tag_name)
        namespace[alias] = constructor
        namespace[tag_name] = constructor
        constructors[alias] = constructor
    return constructors
