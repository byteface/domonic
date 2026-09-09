"""Document parsing and serialization regressions from issue #74.

Reported-by: @testmigrator
https://github.com/byteface/domonic/issues/74
"""

import pytest

from domonic import domonic
from domonic.dom import DOMConfig, DOMParser, Document, XMLSerializer
from domonic.html import title


@pytest.mark.parametrize(
    "parser", ["html.parser", "html5lib", "lxml", "selectolax", "justhtml"]
)
def test_doctype_with_omitted_html_preserves_content(parser):
    try:
        doc = domonic.parseString(
            "<!DOCTYPE html><div>Hello World</div>", parser=parser
        )
    except ImportError:
        pytest.skip(f"{parser} is not installed")
    assert isinstance(doc, Document)
    assert doc.querySelector("div").textContent == "Hello World"
    assert doc.doctype.name == "html"
    assert str(doc).startswith("<!DOCTYPE html>")
    assert str(doc).count("<!DOCTYPE html>") == 1
    assert doc.querySelector("title") is None


@pytest.mark.parametrize(
    "source",
    ["", "<div>Hello World</div>", "<!DOCTYPE html>", "<title>T</title><p>P</p>"],
)
def test_domparser_returns_complete_html_document(source):
    doc = DOMParser().parseFromString(source, "text/html")
    assert isinstance(doc, Document)
    assert doc.documentElement.name == "html"
    assert doc.head is not None
    assert doc.body is not None
    assert (doc.doctype is not None) == source.startswith("<!DOCTYPE")
    if doc.doctype is None:
        assert "<!DOCTYPE" not in str(doc)
        assert "<!DOCTYPE" not in format(doc)
    if "Hello World" in source:
        assert doc.body.querySelector("div").textContent == "Hello World"
    if "<title>" in source:
        assert doc.head.querySelector("title").textContent == "T"
        assert doc.body.querySelector("p").textContent == "P"


def test_snippets_still_parse_as_fragments():
    node = domonic.parseString("<div>Hello World</div>", parser="html.parser")
    assert not isinstance(node, Document)
    assert str(node) == "<div>Hello World</div>"


def test_document_and_element_serialization_are_distinct():
    doc = DOMParser().parseFromString("<!DOCTYPE html><div>Hello World</div>")
    assert XMLSerializer().serializeToString(doc) == str(doc)
    assert str(doc).startswith("<!DOCTYPE html>")
    assert not doc.documentElement.outerHTML.startswith("<!DOCTYPE")
    assert "\n" not in str(doc)


def test_pretty_print_example_adds_title_explicitly():
    doc = DOMParser().parseFromString("<!DOCTYPE html><div>Hello World</div>")
    assert doc.querySelector("title") is None
    doc.head.appendChild(title(""))
    output = format(doc).expandtabs(2).strip()
    assert output.startswith("<!DOCTYPE html>\n<html>")
    assert "\n  <head>" in output
    assert "\n    <title></title>" in output
    assert "\n    <div>Hello World</div>" in output
    assert output.count("<!DOCTYPE html>") == 1


def test_doctype_changes_invalidate_cached_document_render():
    previous = DOMConfig.RENDER_CACHE_ENABLED
    DOMConfig.RENDER_CACHE_ENABLED = True
    try:
        doc = DOMParser().parseFromString("<!DOCTYPE html><p>x</p>")
        assert str(doc).startswith("<!DOCTYPE html>")
        doc.doctype = None
        assert str(doc).startswith("<html>")
    finally:
        DOMConfig.RENDER_CACHE_ENABLED = previous
