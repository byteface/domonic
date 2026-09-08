"""Regression tests for the optional tl-parser backend."""

import pytest

pytest.importorskip("tl")

from domonic import dom, domonic
from domonic.ext.tl_ import parse


def test_mixed_content():
    page = domonic.parseString(
        '<P TITLE="a&amp;b" disabled>one &lt; <b>two</b> tail<!-- note --></P>',
        parser="tl",
    )
    assert page.tagName == "P"
    assert page.getAttribute("title") == "a&b"
    assert page.getAttribute("disabled") == ""
    assert [n.nodeType for n in page.childNodes] == [3, 1, 3, 8]
    assert [n.textContent for n in page.childNodes] == [
        "one < ",
        "two",
        " tail",
        " note ",
    ]
    assert all(n.parentNode is page for n in page.childNodes)
    assert isinstance(page.ownerDocument, dom.Document)
    assert domonic.get_active_parser() == "tl"


@pytest.mark.parametrize(
    "declaration",
    [
        "<!DOCTYPE html>",
        '<!DOCTYPE html PUBLIC "public-id" "system-id">',
        '<!DOCTYPE html SYSTEM "system-id">',
    ],
)
def test_doctype(declaration):
    page = parse(
        declaration
        + "<html><head><title>Hi</title></head><body><p>yes</p></body></html>",
        return_root=False,
    )
    assert isinstance(page, dom.Document)
    assert page.doctype.name == "html"
    assert page.documentElement.tagName == "HTML"
    assert page.querySelector("p").textContent == "yes"
    assert len(page.childNodes) == 1
    if "public-id" in declaration:
        assert page.doctype.publicId == "public-id"
    if "system-id" in declaration:
        assert page.doctype.systemId == "system-id"


def test_raw_text_and_foreign_namespaces():
    page = parse(
        '<div><SCRIPT>a &amp; b</SCRIPT><textarea>&lt;b&gt;</textarea><svg viewBox="0 0 1 1"><foreignObject><P>x</P></foreignObject></svg><math><mi>x</mi></math></div>'
    )
    assert page.querySelector("script").textContent == "a &amp; b"
    assert page.querySelector("textarea").textContent == "<b>"
    svg = page.querySelector("svg")
    assert svg.namespaceURI == "http://www.w3.org/2000/svg"
    assert svg.getAttribute("viewBox") == "0 0 1 1"
    assert page.querySelector("p").namespaceURI == "http://www.w3.org/1999/xhtml"
    assert page.querySelector("mi").namespaceURI == "http://www.w3.org/1998/Math/MathML"


@pytest.mark.parametrize(
    "source",
    [
        None,
        "",
        "text &amp; text",
        "<p>one</p><p>two</p>",
        "<p>unclosed",
        b"<p>caf\xc3\xa9</p>",
    ],
)
def test_fragments(source):
    assert isinstance(parse(source), dom.Node)


def test_declaration_after_comment_and_inside_script():
    page = parse('<!--before--><!DOCTYPE html PUBLIC "a" "b"><p>x</p>')
    assert page.doctype.publicId == "a"
    assert [n.nodeType for n in page.childNodes] == [8, 1]
    page = parse('<script>"<!DOCTYPE html>"</script>')
    # The declaration extractor must not promote script contents to a doctype.
    # tl itself consumes this declaration in raw text; retain its native tree.
    assert page.tagName == "SCRIPT"
    assert page.__dict__.get("_doctype") is None
    assert page.textContent == '""'


def test_default_and_mutation():
    old = domonic.get_default_parser()
    try:
        domonic.set_default_parser("tl")
        page = domonic.parseString("<p>before</p>")
        assert domonic.get_active_parser() == "tl"
        page.textContent = "after"
        page.setAttribute("id", "changed")
        assert page.textContent == "after"
        assert page.getAttribute("id") == "changed"
    finally:
        domonic.set_default_parser(old)


def test_large_fixture():
    from pathlib import Path
    import tl

    source = (Path(__file__).parents[1] / "benchmarks/html_meaty_page.html").read_text()
    page = parse(source)
    native = tl.parse(source)
    assert page.querySelector("title").textContent == "HTML - Wikipedia"
    assert len(page.querySelectorAll("a")) == len(native.query_selector("a"))


def test_deep_tree():
    page = parse("<div>" * 1500 + "deep" + "</div>" * 1500)
    for _ in range(1500):
        assert page.tagName == "DIV"
        child = page.childNodes[0]
        assert child.parentNode is page
        page = child
    assert page.textContent == "deep"


def test_cached_elements_keep_independent_mutable_state():
    from domonic.events import Event
    from domonic.html import b

    page = parse('<div><p id="first">one</p><p></p><p id="last">three</p></div>')
    first, empty, last = page.childNodes
    assert empty.getAttribute("id") is None
    assert not empty.childNodes
    assert first.textContent == "one"
    assert last.textContent == "three"
    for key in ("kwargs", "listeners", "_listener_options"):
        assert len({id(n.__dict__[key]) for n in page.childNodes}) == 3
    seen = []
    first.addEventListener("probe", lambda event: seen.append("first"))
    empty.dispatchEvent(Event("probe"))
    last.dispatchEvent(Event("probe"))
    assert seen == []
    first.dispatchEvent(Event("probe"))
    assert seen == ["first"]
    empty.appendChild(b("added"))
    assert empty.textContent == "added"
    assert first.textContent == "one"
    assert last.textContent == "three"


def test_cached_elements_preserve_foreign_context():
    page = parse("<div><a>x</a><svg><a>y</a><a>z</a></svg><a>w</a></div>")
    links = page.querySelectorAll("a")
    assert [n.namespaceURI for n in links] == [
        "http://www.w3.org/1999/xhtml",
        "http://www.w3.org/2000/svg",
        "http://www.w3.org/2000/svg",
        "http://www.w3.org/1999/xhtml",
    ]
    assert [n.textContent for n in links] == ["x", "y", "z", "w"]


def test_text_fast_path_preserves_comments_and_entities():
    page = parse(
        "<div><p>&lt;x&gt;</p><p><!--only comment--></p><p>a<!--middle-->b</p><script>&amp;</script><p></p></div>"
    )
    first, comment, mixed, script, empty = page.childNodes
    assert first.textContent == "<x>"
    assert first.childNodes[0].parentNode is first
    assert comment.childNodes[0].nodeType == dom.Node.COMMENT_NODE
    assert [n.nodeType for n in mixed.childNodes] == [3, 8, 3]
    assert script.textContent == "&amp;"
    assert not empty.childNodes


def test_foreign_first_template_does_not_pollute_html():
    page = parse(
        "<div><svg><a>svg</a><foreignObject><a>html</a></foreignObject><a>svg again</a></svg><a>html again</a></div>"
    )
    links = page.querySelectorAll("a")
    assert [n.namespaceURI for n in links] == [
        "http://www.w3.org/2000/svg",
        "http://www.w3.org/1999/xhtml",
        "http://www.w3.org/2000/svg",
        "http://www.w3.org/1999/xhtml",
    ]
    assert [n.textContent for n in links] == ["svg", "html", "svg again", "html again"]
