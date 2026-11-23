"""
domonic.webapi.sanitizer
====================================
https://developer.mozilla.org/en-US/docs/Web/API/HTML_Sanitizer_API
"""

from __future__ import annotations

import copy
import re
from typing import Any

from domonic.dom import CDATASection, Comment, Document, DocumentFragment, Element, Node, Text

_UNSAFE_ELEMENTS = frozenset({"script", "frame", "iframe", "embed", "object", "use"})
# SVG animation elements can set an attribute to a ``javascript:`` URL
# (``<animate attributeName="href" values="javascript:...">``), so their
# ``attributeName`` may not name a URL attribute.
_SVG_ANIMATION_ELEMENTS = frozenset({"animate", "animatemotion", "animatetransform", "set"})
_ANIMATABLE_URL_ATTRIBUTES = frozenset({"href", "xlink:href"})
# Text that looks like markup, in a raw-text element or a comment. Parsers
# don't all agree on where raw text starts (``<style>`` inside ``<select>``,
# ``<noscript>`` with scripting on or off), so in safe mode such content is
# removed rather than trusted to be read as text. The same rule as DOMPurify.
_MARKUP_IN_TEXT = re.compile(r"<[/\w]")
_URL_ATTRIBUTES = frozenset(
    {
        "action",
        "background",
        "cite",
        "codebase",
        "data",
        "formaction",
        "href",
        "longdesc",
        "lowsrc",
        "manifest",
        "poster",
        "src",
        "srcset",
        "xlink:href",
    }
)
_UNSAFE_SCHEMES = ("javascript:", "vbscript:")
_CONFIG_KEYS = frozenset(
    {
        "elements",
        "removeElements",
        "replaceWithChildrenElements",
        "attributes",
        "removeAttributes",
        "comments",
        "dataAttributes",
        "allowCustomElements",
    }
)
_LEGACY_KEYS = {
    "allowElements": "elements",
    "dropElements": "removeElements",
    "blockElements": "replaceWithChildrenElements",
    "allowAttributes": "attributes",
    "dropAttributes": "removeAttributes",
    "allowComments": "comments",
}


def _normalize_element_name(name: Any) -> str:
    return str(name or "").strip().lower()


def _normalize_attribute_name(name: Any) -> str:
    return str(name or "").strip().lower().lstrip("_").replace("_", "-")


def _normalise_unique_strings(values: Any, key: str) -> set[str]:
    if values is None:
        return set()
    if isinstance(values, str):
        values = [values]

    seen: set[str] = set()
    for value in values:
        item = _normalize_element_name(value)
        if not item:
            continue
        if item in seen:
            raise TypeError(f"Duplicate {key} entry: {item}")
        seen.add(item)
    return seen


def _normalize_attribute_rules(rules: Any, key: str) -> dict[str, set[str]] | None:
    if rules is None:
        return None

    normalized: dict[str, set[str]] = {}

    def add_rule(attribute: Any, elements: Any = None) -> None:
        attr = _normalize_attribute_name(attribute)
        if not attr:
            return
        if elements is None:
            targets = {"*"}
        elif isinstance(elements, str):
            targets = {_normalize_element_name(elements) or "*"}
        else:
            targets = {
                _normalize_element_name(element) or "*"
                for element in elements
                if _normalize_element_name(element) or element == "*"
            }
            if not targets:
                targets = {"*"}
        normalized.setdefault(attr, set()).update(targets)

    if isinstance(rules, dict):
        for attribute, elements in rules.items():
            add_rule(attribute, elements)
        return normalized

    if isinstance(rules, str):
        add_rule(rules)
        return normalized

    for item in rules:
        if isinstance(item, str):
            add_rule(item)
            continue
        if isinstance(item, dict):
            attribute = item.get("name", item.get("attribute"))
            elements = item.get("elements", item.get("element"))
            add_rule(attribute, elements)
            continue
        raise TypeError(f"{key} entries must be strings or dictionaries")

    return normalized


def _attribute_rule_applies(rules: dict[str, set[str]] | None, attribute: str, element: str) -> bool:
    if rules is None:
        return False
    for key in (attribute, "*"):
        targets = rules.get(key)
        if targets and ("*" in targets or element in targets):
            return True
    return False


def _attribute_rules_to_config(
    rules: dict[str, set[str]] | None,
) -> dict[str, list[str]] | None:
    if rules is None:
        return None
    return {name: sorted(targets) for name, targets in sorted(rules.items())}


def _has_overlaps(label: str, first: set[str], second: set[str]) -> None:
    overlap = first.intersection(second)
    if overlap:
        joined = ", ".join(sorted(overlap))
        raise TypeError(f"{label} entries conflict: {joined}")


def _is_custom_element(name: str) -> bool:
    return "-" in name


def _is_dangerous_url(value: Any) -> bool:
    compact = re.sub(r"[\x00-\x20]+", "", str(value or "")).lower()
    return compact.startswith(_UNSAFE_SCHEMES)


def _is_unsafe_attribute(name: str, value: Any) -> bool:
    if name.startswith("on"):
        return True
    if name == "srcdoc":
        return True
    if name in _URL_ATTRIBUTES and _is_dangerous_url(value):
        return True
    if name == "style" and re.search(
        r"(expression\s*\(|url\s*\(\s*['\"]?\s*(?:javascript|vbscript):)",
        str(value or ""),
        re.IGNORECASE,
    ):
        return True
    return False


def _text(data: Any) -> Text:
    """A text node that ``str()`` escapes, as it does parsed text."""
    node = Text(str(data))
    node._escape_text_on_render = True
    return node


class Sanitizer:
    """Configurable HTML fragment sanitizer.

    The implementation follows the current Sanitizer API shape while retaining
    domonic's older ``allowElements``/``dropElements``/``allowAttributes`` names
    as aliases. Input is parsed by domonic's HTML parser, the same one that
    ``innerHTML`` uses, and the resulting tree is then cleaned: what is left is
    exactly what a browser will build when it reads the output.
    """

    def __init__(self, config: dict[str, Any] | "Sanitizer" | None = None) -> None:
        self._allow_elements: set[str] | None = None
        self._remove_elements: set[str] = set()
        self._replace_with_children_elements: set[str] = set()
        self._allow_attributes: dict[str, set[str]] | None = None
        self._remove_attributes: dict[str, set[str]] | None = {}
        self.comments = False
        self.dataAttributes = False
        self.allowCustomElements = True
        self._remove_unsafe = True

        if isinstance(config, Sanitizer):
            self._allow_elements = copy.deepcopy(config._allow_elements)
            self._remove_elements = copy.deepcopy(config._remove_elements)
            self._replace_with_children_elements = copy.deepcopy(config._replace_with_children_elements)
            self._allow_attributes = copy.deepcopy(config._allow_attributes)
            self._remove_attributes = copy.deepcopy(config._remove_attributes)
            self.comments = config.comments
            self.dataAttributes = config.dataAttributes
            self.allowCustomElements = config.allowCustomElements
            self._remove_unsafe = config._remove_unsafe
            return

        if config is None:
            self._remove_elements = set(_UNSAFE_ELEMENTS)
            return

        if not isinstance(config, dict):
            raise TypeError("Sanitizer configuration must be a dictionary")

        normalized = self._normalize_config(config)
        if not normalized:
            self.comments = True
            self.dataAttributes = True
            self._remove_unsafe = False
            return

        self._apply_config(normalized)

    @staticmethod
    def _normalize_config(config: dict[str, Any]) -> dict[str, Any]:
        normalized: dict[str, Any] = {}
        for key, value in config.items():
            key = _LEGACY_KEYS.get(key, key)
            if key in _CONFIG_KEYS:
                normalized[key] = value
        return normalized

    @classmethod
    def _empty_configuration(cls) -> dict[str, Any]:
        return {
            "comments": True,
            "dataAttributes": True,
            "removeAttributes": {},
            "removeElements": [],
            "replaceWithChildrenElements": [],
        }

    @classmethod
    def _default_configuration(cls) -> dict[str, Any]:
        config = cls._empty_configuration()
        config.update(
            {
                "comments": False,
                "dataAttributes": False,
                "removeElements": sorted(_UNSAFE_ELEMENTS),
            }
        )
        return config

    @staticmethod
    def getDefaultConfiguration() -> dict[str, Any]:
        """Return domonic's default XSS-safe Sanitizer configuration."""
        return Sanitizer._default_configuration()

    def get(self) -> dict[str, Any]:
        """Return a normalized copy of the current Sanitizer configuration."""
        config = {
            "comments": self.comments,
            "dataAttributes": self.dataAttributes,
            "removeElements": sorted(self._remove_elements),
            "replaceWithChildrenElements": sorted(self._replace_with_children_elements),
            "removeAttributes": _attribute_rules_to_config(self._remove_attributes),
        }
        if self._allow_elements is not None:
            config["elements"] = sorted(self._allow_elements)
        if self._allow_attributes is not None:
            config["attributes"] = _attribute_rules_to_config(self._allow_attributes)
        if self.allowCustomElements is not True:
            config["allowCustomElements"] = self.allowCustomElements
        return copy.deepcopy(config)

    def getConfiguration(self) -> dict[str, Any]:
        """Backward-compatible alias for ``get()``."""
        return self.get()

    def _apply_config(self, config: dict[str, Any]) -> None:
        if "elements" in config and "removeElements" in config:
            raise TypeError("Sanitizer config cannot contain both elements and removeElements")
        if "attributes" in config and "removeAttributes" in config:
            raise TypeError("Sanitizer config cannot contain both attributes and removeAttributes")

        self._allow_elements = (
            _normalise_unique_strings(config["elements"], "elements") if "elements" in config else None
        )
        self._remove_elements = (
            _normalise_unique_strings(config["removeElements"], "removeElements")
            if "removeElements" in config
            else set(_UNSAFE_ELEMENTS)
        )
        self._replace_with_children_elements = _normalise_unique_strings(
            config.get("replaceWithChildrenElements", []),
            "replaceWithChildrenElements",
        )
        if self._allow_elements is not None:
            _has_overlaps(
                "replaceWithChildrenElements",
                self._replace_with_children_elements,
                self._allow_elements,
            )
        _has_overlaps(
            "replaceWithChildrenElements",
            self._replace_with_children_elements,
            self._remove_elements,
        )

        self._allow_attributes = _normalize_attribute_rules(config.get("attributes"), "attributes")
        self._remove_attributes = _normalize_attribute_rules(config.get("removeAttributes"), "removeAttributes") or {}
        self.comments = bool(config.get("comments", False))
        self.dataAttributes = bool(config.get("dataAttributes", False))
        self.allowCustomElements = bool(config.get("allowCustomElements", True))

    def allowElement(
        self,
        name: str,
        attributes: Any = None,
        removeAttributes: Any = None,
    ) -> "Sanitizer":
        """Allow an element name and optionally attach attribute rules to it."""
        element = _normalize_element_name(name)
        if not element:
            return self
        if self._allow_elements is None:
            self._allow_elements = set()
        self._allow_elements.add(element)
        self._remove_elements.discard(element)
        self._replace_with_children_elements.discard(element)
        if attributes is not None:
            for attribute in _normalize_attribute_rules(attributes, "attributes") or {}:
                self.allowAttribute(attribute, [element])
        if removeAttributes is not None:
            for attribute in _normalize_attribute_rules(removeAttributes, "removeAttributes") or {}:
                self.removeAttribute(attribute, [element])
        return self

    def removeElement(self, name: str) -> "Sanitizer":
        """Remove an element and all of its children."""
        element = _normalize_element_name(name)
        if not element:
            return self
        if self._allow_elements is not None:
            self._allow_elements.discard(element)
        self._replace_with_children_elements.discard(element)
        self._remove_elements.add(element)
        return self

    def replaceElementWithChildren(self, name: str) -> "Sanitizer":
        """Remove an element but keep its sanitized children."""
        element = _normalize_element_name(name)
        if not element:
            return self
        if self._allow_elements is not None:
            self._allow_elements.discard(element)
        self._remove_elements.discard(element)
        self._replace_with_children_elements.add(element)
        return self

    def allowAttribute(self, name: str, elements: Any = None) -> "Sanitizer":
        """Allow an attribute globally or on selected elements."""
        if self._allow_attributes is None:
            self._allow_attributes = {}
        rules = _normalize_attribute_rules({name: elements or ["*"]}, "attributes") or {}
        for attribute, targets in rules.items():
            self._allow_attributes.setdefault(attribute, set()).update(targets)
            if self._remove_attributes is not None:
                remove_targets = self._remove_attributes.get(attribute)
                if remove_targets:
                    remove_targets.difference_update(targets)
                    if not remove_targets:
                        self._remove_attributes.pop(attribute, None)
        return self

    def removeAttribute(self, name: str, elements: Any = None) -> "Sanitizer":
        """Remove an attribute globally or on selected elements."""
        if self._remove_attributes is None:
            self._remove_attributes = {}
        rules = _normalize_attribute_rules({name: elements or ["*"]}, "removeAttributes") or {}
        for attribute, targets in rules.items():
            self._remove_attributes.setdefault(attribute, set()).update(targets)
            if self._allow_attributes is not None:
                allow_targets = self._allow_attributes.get(attribute)
                if allow_targets:
                    allow_targets.difference_update(targets)
                    if not allow_targets:
                        self._allow_attributes.pop(attribute, None)
        return self

    def setComments(self, allow: bool) -> "Sanitizer":
        """Allow or remove HTML comments."""
        self.comments = bool(allow)
        return self

    def setDataAttributes(self, allow: bool) -> "Sanitizer":
        """Allow or remove ``data-*`` attributes."""
        self.dataAttributes = bool(allow)
        return self

    def removeUnsafe(self) -> "Sanitizer":
        """Force removal of elements and attributes that can execute script."""
        self._remove_unsafe = True
        self._remove_elements.update(_UNSAFE_ELEMENTS)
        return self

    def _element_action(self, tag: str) -> str:
        if self._remove_unsafe and tag in _UNSAFE_ELEMENTS:
            return "drop"
        if tag in self._remove_elements:
            return "drop"
        if tag in self._replace_with_children_elements:
            return "unwrap"
        if self._allow_elements is not None and tag not in self._allow_elements:
            return "unwrap"
        if not self.allowCustomElements and _is_custom_element(tag):
            return "unwrap"
        return "keep"

    def _allow_attribute(self, tag: str, name: str, value: Any) -> bool:
        if self._remove_unsafe and _is_unsafe_attribute(name, value):
            return False
        if _attribute_rule_applies(self._remove_attributes, name, tag):
            return False
        if name.startswith("data-") and not self.dataAttributes:
            if not _attribute_rule_applies(self._allow_attributes, name, tag):
                return False
        if self._allow_attributes is not None:
            return _attribute_rule_applies(self._allow_attributes, name, tag)
        return True

    def _clean_attributes(self, element: Element, tag: str) -> None:
        kwargs = element.kwargs
        if not kwargs:
            return
        seen: set[str] = set()
        for key in list(kwargs):
            name = _normalize_attribute_name(key)
            value = kwargs[key]
            if not name or name in seen or not self._allow_attribute(tag, name, value):
                del kwargs[key]
                continue
            if (
                self._remove_unsafe
                and tag in _SVG_ANIMATION_ELEMENTS
                and name == "attributename"
                and str(value).strip().lower() in _ANIMATABLE_URL_ATTRIBUTES
            ):
                del kwargs[key]
                continue
            seen.add(name)

    @staticmethod
    def _hides_markup(element: Element, tag: str) -> bool:
        """Whether ``element`` is written out as raw text that contains markup."""
        from domonic.dom import _serializes_raw

        if not _serializes_raw(element, tag):
            return False
        text = "".join(
            str(child.data) if isinstance(child, Text) else child
            for child in element.args
            if isinstance(child, (Text, str))
        )
        return _MARKUP_IN_TEXT.search(text) is not None

    def _clean(self, root: Node) -> None:
        """Clean ``root``'s subtree in place. Iterative, so a deeply nested
        input can't exhaust the stack."""
        pending: list[Any] = [root]
        while pending:
            parent = pending.pop()
            queue = list(getattr(parent, "args", None) or ())
            queue.reverse()
            kept: list[Any] = []
            changed = False
            while queue:
                child = queue.pop()
                if isinstance(child, Element):
                    tag = _normalize_element_name(child.name)
                    action = self._element_action(tag)
                    if action == "drop":
                        changed = True
                        continue
                    if action == "unwrap":
                        changed = True
                        grandchildren = list(child.args or ())
                        grandchildren.reverse()
                        queue.extend(grandchildren)
                        continue
                    if self._remove_unsafe and self._hides_markup(child, tag):
                        changed = True
                        continue
                    self._clean_attributes(child, tag)
                    kept.append(child)
                    pending.append(child)
                    content = child.__dict__.get("_template_content")
                    if content is not None:
                        pending.append(content)
                elif isinstance(child, Comment):
                    if self.comments and not (self._remove_unsafe and _MARKUP_IN_TEXT.search(str(child.data))):
                        kept.append(child)
                    else:
                        changed = True
                elif isinstance(child, Text):
                    child._escape_text_on_render = True
                    kept.append(child)
                elif isinstance(child, CDATASection):
                    kept.append(_text(child.data))
                    changed = True
                elif isinstance(child, Node):
                    # doctypes, processing instructions, nested fragments
                    changed = True
                else:
                    # a bare string child: domonic writes those out verbatim,
                    # so make it a text node that is escaped like parsed text
                    kept.append(_text(child))
                    changed = True
            if changed:
                parent.replaceChildren(*kept)

    def sanitize(self, input: Any) -> DocumentFragment:
        """Return a sanitized ``DocumentFragment`` for a string or DOM node."""
        from domonic.html import create_element

        text = "" if input is None else str(input)
        fragment = DocumentFragment(*create_element("div")._parse_html_fragment(text))
        self._clean(fragment)
        return fragment

    def sanitizeToString(self, input: Any) -> str:
        """Return a sanitized HTML string."""
        return str(self.sanitize(input))

    def sanitizeFor(self, element: str | Element, input: Any) -> Element:
        """Sanitize a fragment and place it in a new element."""
        tag = element.tagName if isinstance(element, Element) else str(element)
        from domonic.html import create_element

        node = create_element(tag)
        node.replaceChildren(*self.sanitize(input).args)
        return node


def _coerce_sanitizer(options: Any = None, *, safe: bool = True) -> Sanitizer | None:
    if isinstance(options, Sanitizer):
        sanitizer = Sanitizer(options)
    elif isinstance(options, dict) and "sanitizer" in options:
        raw = options.get("sanitizer")
        if raw in (None, "default"):
            sanitizer = Sanitizer()
        elif isinstance(raw, Sanitizer):
            sanitizer = Sanitizer(raw)
        elif isinstance(raw, dict):
            sanitizer = Sanitizer(raw)
        else:
            raise TypeError("options['sanitizer'] must be a Sanitizer or dictionary")
    elif isinstance(options, dict):
        sanitizer = Sanitizer(options)
    elif options is None:
        sanitizer = Sanitizer() if safe else Sanitizer({})
    else:
        raise TypeError("options must be a dictionary or Sanitizer")

    if safe and sanitizer is not None:
        sanitizer.removeUnsafe()
    return sanitizer


def sanitize_html_fragment(input: Any, options: Any = None, *, safe: bool = True) -> DocumentFragment:
    """Sanitize or parse an HTML fragment using Sanitizer-style options."""
    sanitizer = _coerce_sanitizer(options, safe=safe)
    return sanitizer.sanitize(input) if sanitizer is not None else DocumentFragment()


def parse_html_document(input: Any, options: Any = None, *, safe: bool = True) -> Document:
    """Parse a sanitized HTML fragment into a domonic HTMLDocument."""
    from domonic.dom import HTMLDocument
    from domonic.html import body, head

    fragment = sanitize_html_fragment(input, options, safe=safe)
    return HTMLDocument(head(), body(*fragment.args))


__all__ = ["Sanitizer", "sanitize_html_fragment", "parse_html_document"]
