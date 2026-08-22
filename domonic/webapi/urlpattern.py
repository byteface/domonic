"""
domonic.webapi.urlpattern
====================================
https://developer.mozilla.org/en-US/docs/Web/API/URLPattern
"""

from __future__ import annotations

import re
import urllib.parse
from typing import Any


class URLPattern:
    """Match URLs or URL parts against URLPattern-style patterns."""

    _components = (
        "protocol",
        "username",
        "password",
        "hostname",
        "port",
        "pathname",
        "search",
        "hash",
    )

    def __init__(self, pattern: str | dict[str, Any], baseURL: str | None = None):
        self.inputs = [pattern] if baseURL is None else [pattern, baseURL]
        self._regexes: dict[str, re.Pattern[str]] = {}
        self._group_names: dict[str, list[str]] = {}
        self.hasRegExpGroups = False

        parts = self._pattern_to_parts(pattern, baseURL)
        for component in self._components:
            value = str(parts.get(component, "*"))
            setattr(self, component, value)
            regex, groups, has_regex = self._compile_component(value, component)
            self._regexes[component] = regex
            self._group_names[component] = groups
            self.hasRegExpGroups = self.hasRegExpGroups or has_regex

    def __str__(self) -> str:
        return self.pathname if self.pathname != "*" else self.hostname

    @classmethod
    def _empty_parts(cls) -> dict[str, str]:
        return {component: "*" for component in cls._components}

    @classmethod
    def _url_to_parts(cls, url: str, baseURL: str | None = None) -> dict[str, str]:
        if baseURL is not None:
            url = urllib.parse.urljoin(str(baseURL), str(url))
        parsed = urllib.parse.urlsplit(str(url))
        return {
            "protocol": parsed.scheme,
            "username": parsed.username or "",
            "password": parsed.password or "",
            "hostname": parsed.hostname or "",
            "port": str(parsed.port or ""),
            "pathname": parsed.path or "/",
            "search": parsed.query or "",
            "hash": parsed.fragment or "",
        }

    @classmethod
    def _pattern_to_parts(
        cls, pattern: str | dict[str, Any], baseURL: str | None = None
    ) -> dict[str, str]:
        parts = cls._empty_parts()
        if isinstance(pattern, dict):
            base = pattern.get("baseURL", baseURL)
            if base:
                parts.update(cls._url_to_parts(str(base)))
            for component in cls._components:
                if component in pattern:
                    value = str(pattern[component])
                    if component == "protocol":
                        value = value.rstrip(":")
                    elif component == "search":
                        value = value.lstrip("?")
                    elif component == "hash":
                        value = value.lstrip("#")
                    parts[component] = value
            return parts

        text = str(pattern)
        if baseURL and not urllib.parse.urlsplit(text).scheme:
            parsed_parts = cls._url_to_parts(text, baseURL)
            parts.update(parsed_parts)
            return parts

        if "://" in text:
            protocol, rest = text.split("://", 1)
            parsed = urllib.parse.urlsplit("scheme://" + rest)
            parts.update(
                {
                    "protocol": protocol,
                    "username": parsed.username or "*",
                    "password": parsed.password or "*",
                    "hostname": parsed.hostname or "",
                    "port": str(parsed.port or ""),
                    "pathname": parsed.path or "/",
                    "search": parsed.query or "*",
                    "hash": parsed.fragment or "*",
                }
            )
            return parts

        if text.startswith("/"):
            parts["pathname"] = text
            return parts

        parsed = urllib.parse.urlsplit(text)
        if parsed.scheme:
            parts.update(cls._url_to_parts(text))
        else:
            parts["pathname"] = text
        return parts

    @staticmethod
    def _read_regex(pattern: str, start: int) -> tuple[str, int]:
        depth = 1
        index = start
        value = []
        while index < len(pattern):
            char = pattern[index]
            if char == "\\" and index + 1 < len(pattern):
                value.extend([char, pattern[index + 1]])
                index += 2
                continue
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    return "".join(value), index + 1
            value.append(char)
            index += 1
        raise ValueError("Unclosed URLPattern regex group")

    @staticmethod
    def _default_group_pattern(component: str, modifier: str = "") -> str:
        if component == "pathname":
            return ".+" if modifier in ("+", "*") else "[^/]+"
        if component == "hostname":
            return "[^.]+"
        return ".+"

    @classmethod
    def _compile_component(
        cls, pattern: str, component: str
    ) -> tuple[re.Pattern[str], list[str], bool]:
        if pattern == "*":
            return re.compile(r"^(.*)$"), ["0"], False

        output: list[str] = []
        groups: list[str] = []
        has_regex = False
        unnamed = 0
        index = 0

        while index < len(pattern):
            char = pattern[index]
            if char == "*":
                output.append("(.*)")
                groups.append(str(unnamed))
                unnamed += 1
                index += 1
                continue

            if char == ":":
                match = re.match(r":([A-Za-z_][A-Za-z0-9_]*)", pattern[index:])
                if not match:
                    output.append(re.escape(char))
                    index += 1
                    continue
                name = match.group(1)
                index += len(match.group(0))
                regex = ""
                if index < len(pattern) and pattern[index] == "(":
                    regex, index = cls._read_regex(pattern, index + 1)
                    has_regex = True
                modifier = (
                    pattern[index]
                    if index < len(pattern) and pattern[index] in "?+*"
                    else ""
                )
                if modifier:
                    index += 1
                regex = regex or cls._default_group_pattern(component, modifier)
                if modifier == "?":
                    output.append(f"({regex})?")
                elif modifier == "*":
                    output.append(f"({regex})*")
                elif modifier == "+":
                    output.append(f"({regex})+")
                else:
                    output.append(f"({regex})")
                groups.append(name)
                continue

            if char == "(":
                regex, index = cls._read_regex(pattern, index + 1)
                output.append(f"({regex})")
                groups.append(str(unnamed))
                unnamed += 1
                has_regex = True
                continue

            output.append(re.escape(char))
            index += 1

        flags = re.IGNORECASE if component in ("protocol", "hostname") else 0
        return re.compile("^" + "".join(output) + "$", flags), groups, has_regex

    @classmethod
    def _input_to_parts(
        cls, input: str | dict[str, Any], baseURL: str | None = None
    ) -> dict[str, str]:
        if isinstance(input, dict):
            base = input.get("baseURL", baseURL)
            parts = (
                cls._url_to_parts(str(base))
                if base
                else {component: "" for component in cls._components}
            )
            for component in cls._components:
                if component in input:
                    value = str(input[component])
                    if component == "protocol":
                        value = value.rstrip(":")
                    elif component == "search":
                        value = value.lstrip("?")
                    elif component == "hash":
                        value = value.lstrip("#")
                    parts[component] = value
            return parts
        if baseURL is None and not urllib.parse.urlsplit(str(input)).scheme:
            return {}
        return cls._url_to_parts(str(input), baseURL)

    def exec_(
        self, input: str | dict[str, Any], baseURL: str | None = None
    ) -> dict[str, Any] | None:
        """Return matched URL parts and groups, or ``None`` if there is no match."""
        parts = self._input_to_parts(input, baseURL)
        if not parts:
            return None

        result: dict[str, Any] = {
            "inputs": [input] if baseURL is None else [input, baseURL]
        }
        for component in self._components:
            value = parts.get(component, "")
            match = self._regexes[component].match(value)
            if not match:
                return None
            names = self._group_names[component]
            result[component] = {
                "input": value,
                "groups": {
                    name: match.group(index + 1) or ""
                    for index, name in enumerate(names)
                },
            }
        return result

    def test(self, input: str | dict[str, Any], baseURL: str | None = None) -> bool:
        """Return whether ``input`` matches this pattern."""
        return self.exec_(input, baseURL) is not None


setattr(URLPattern, "exec", URLPattern.exec_)
