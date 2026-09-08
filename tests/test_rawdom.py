"""Shared parser DOM construction preserves state and mutable ownership."""

import pytest

from domonic import dom
from domonic.events import Event
from domonic.ext import _rawdom as raw


def test_text_nodes_have_independent_metadata():
    first = raw._create_text_raw("one")
    second = raw._create_text_raw("two")
    first.kwargs["metadata"] = "first only"
    assert second.kwargs == {}
    assert raw._create_text_raw("three").kwargs == {}
    first.textContent = "changed"
    assert second.textContent == "two"


@pytest.mark.parametrize("value,expected", [(None, ""), (42, "42"), ("<&", "<&")])
def test_text_initialization(value, expected):
    node = raw._create_text_raw(value)
    assert node.textContent == expected
    assert node.parentNode is None
    assert node.namespaceURI == raw.HTML_NAMESPACE
    if value == "<&":
        assert str(node) == "&lt;&amp;"


@pytest.mark.parametrize(
    "namespace", [raw.HTML_NAMESPACE, raw.SVG_NAMESPACE, raw.MATHML_NAMESPACE]
)
def test_element_state_and_events_are_independent(namespace):
    first = raw._create_element_raw("a", namespace)
    second = raw._create_element_raw("a", namespace)
    first.setAttribute("id", "first")
    assert second.getAttribute("id") is None
    assert first.namespaceURI == second.namespaceURI == namespace
    assert first.__dict__["_namespaceURI"] == namespace
    assert not first.childNodes and not second.childNodes
    calls = []
    first.addEventListener("probe", lambda event: calls.append(1))
    second.dispatchEvent(Event("probe"))
    assert not calls
    first.dispatchEvent(Event("probe"))
    assert calls == [1]


def test_element_initializer_retains_unrelated_state():
    from domonic.html import div

    node = object.__new__(div)
    node.__dict__["custom_metadata"] = "retained"
    raw._initialize_element_raw(node, raw.SVG_NAMESPACE)
    assert node.custom_metadata == "retained"
    assert node.name == "div"
    assert node.__dict__["args"] == ()
    assert node.__dict__["_escape_attributes_on_render"] is True


@pytest.mark.parametrize(
    "factory", [raw._create_document_raw, lambda: raw._create_element_raw("html")]
)
def test_document_initialization(factory):
    first, second = factory(), factory()
    assert isinstance(first, dom.Document)
    assert first.documentElement is first
    assert second.documentElement is second
    first.__dict__["_cookie_store"]["a"] = "b"
    assert second.__dict__["_cookie_store"] == {}
