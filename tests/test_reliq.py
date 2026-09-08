"""Optional Reliq integration: preserve mixed content and native tree structure."""

import pytest

pytest.importorskip("reliq")

from domonic import dom, domonic
from domonic.ext.reliq_ import parse


def test_mixed_content_and_entities():
    page = domonic.parseString(
        '<p title="a&amp;b">one &lt; <b>two</b> tail<!-- note --></p>', parser="reliq"
    )
    assert page.tagName == "P"
    assert page.getAttribute("title") == "a&b"
    assert [node.nodeType for node in page.childNodes] == [3, 1, 3, 8]
    assert page.childNodes[0].textContent == "one < "
    assert page.childNodes[2].textContent == " tail"
    assert page.childNodes[3].textContent == " note "
    assert all(node.parentNode is page for node in page.childNodes)
    assert isinstance(page.ownerDocument, dom.Document)
    assert domonic.get_active_parser() == "reliq"


def test_document_and_doctype():
    page = parse(
        "<!DOCTYPE html><html><head><title>Hi</title></head><body><p>yes</p></body></html>",
        return_root=False,
    )
    assert isinstance(page, dom.Document)
    assert page.doctype.name == "html"
    assert page.documentElement.tagName == "HTML"
    assert page.querySelector("p").textContent == "yes"


def test_raw_text_and_namespaces():
    page = parse(
        "<div><script>a &amp; b</script><textarea>a &amp; b</textarea><svg><circle/></svg></div>"
    )
    assert page.querySelector("script").textContent == "a &amp; b"
    assert page.querySelector("textarea").textContent == "a & b"
    assert page.querySelector("circle").namespaceURI == "http://www.w3.org/2000/svg"


@pytest.mark.parametrize(
    "source",
    [
        "",
        "plain &amp; text",
        "<p>one</p><p>two</p>",
        "<p>unclosed",
        "<!DOCTYPE html><p>retained</p>",
    ],
)
def test_fragments_and_recovery(source):
    page = domonic.parseString(source, parser="reliq")
    assert isinstance(page, dom.Node)
    if "retained" in source:
        assert page.querySelector("p").textContent == "retained"


def test_default_parser():
    previous = domonic.get_default_parser()
    try:
        domonic.set_default_parser("reliq")
        assert domonic.parseString("<b>hello</b>").textContent == "hello"
        assert domonic.get_active_parser() == "reliq"
    finally:
        domonic.set_default_parser(previous)


def _snapshot(root):
    """Compare DOM data and parent links without recursive serialization."""
    result = []
    stack = [(root, 0)]
    while stack:
        node, depth = stack.pop()
        state = node.__dict__
        result.append(
            (
                depth,
                node.nodeType,
                state.get("name"),
                state.get("namespaceURI"),
                dict(state.get("kwargs", {})),
                node.nodeValue,
            )
        )
        children = tuple(node.childNodes)
        for child in children:
            assert child.parentNode is node
        stack.extend((child, depth + 1) for child in reversed(children))
    doctype = root.__dict__.get("_doctype")
    return result, str(doctype) if doctype is not None else None


@pytest.fixture(params=["packed", "converted"])
def native_mode(request, monkeypatch):
    from domonic.ext import reliq_ as adapter

    if request.param == "packed":
        if not adapter._packed_layout():
            pytest.skip("requires the checked packed layout")
    else:
        monkeypatch.setattr(adapter, "_packed_layout", lambda: False)


@pytest.mark.parametrize(
    "source",
    [
        "",
        " \n\t",
        "plain &amp; text",
        "<!-- -->",
        "<!DOCTYPE html>",
        '<!DOCTYPE html PUBLIC "abc" "def"><html><body>🙂 café 漢字</body></html>',
        "<div><b>one</b> tail <i>two</i></div><p>end</p>",
        '<DIV CLASS="one" class="two" empty disabled><BR><IMG src=x></DIV>',
        '<p foo="a" _foo="b" foo="c" data-x="&amp;" data-x="&lt;">x</p>',
        '<p a="&am" a="p;" a="">x</p>',
        "<script>a &amp; b</script><style>a &gt; b {}</style><textarea>&lt;b&gt;</textarea>",
        '<svg viewBox="0 0 1 1"><foreignObject><p>x</p></foreignObject><circle/></svg>',
        '<math><annotation-xml encoding="text/html"><div>x</div></annotation-xml></math>',
        "<!--before--><p>unclosed<b>bold<!--after-->",
        "<ul><li>one<li>two</ul><table><tr><td>x</table>",
        "<!bogus><?pi value?><p>a\x00b</p>",
        '<p title="unterminated',
        b'<p title="caf\xc3\xa9">\xf0\x9f\x99\x82 &amp;</p>',
    ],
)
def test_native_matches_public(source, native_mode):
    from reliq import reliq
    from domonic.ext.reliq_ import _native_api, _parse_native, _parse_public

    if _native_api() is None:
        pytest.skip("native conversion is enabled only for the checked Reliq version")
    parsed = reliq(source)
    assert _snapshot(_parse_native(parsed)) == _snapshot(_parse_public(parsed))


def test_native_matches_public_large_page(native_mode):
    from pathlib import Path
    from reliq import reliq
    from domonic.ext.reliq_ import _native_api, _parse_native, _parse_public

    if _native_api() is None:
        pytest.skip("native conversion is enabled only for the checked Reliq version")
    parsed = reliq(
        (Path(__file__).parents[1] / "benchmarks/html_meaty_page.html").read_text()
    )
    assert _snapshot(_parse_native(parsed)) == _snapshot(_parse_public(parsed))


def test_unknown_version_uses_public_api(monkeypatch):
    from domonic.ext import reliq_ as adapter

    adapter._native_api.cache_clear()
    monkeypatch.setattr(adapter, "version", lambda name: "99.0.0")
    try:
        assert adapter._native_api() is None
        assert (
            adapter.parse("<p>fallback &amp; works</p>").textContent
            == "fallback & works"
        )
    finally:
        adapter._native_api.cache_clear()


def test_result_owns_strings_after_native_tree_is_freed():
    import gc

    page = parse('<p data-x="café">🙂 <b>retained</b></p>')
    gc.collect()
    assert page.getAttribute("data-x") == "café"
    assert page.textContent == "🙂 retained"
    page.querySelector("b").textContent = "changed"
    assert page.textContent == "🙂 changed"


def test_native_handles_deep_tree_without_python_recursion(native_mode):
    from domonic.ext.reliq_ import _native_api

    if _native_api() is None:
        pytest.skip("requires native conversion")
    page = parse("<div>" * 1500 + "deep" + "</div>" * 1500)
    for _ in range(1500):
        assert page.tagName == "DIV"
        child = page.childNodes[0]
        assert child.parentNode is page
        page = child
    assert page.textContent == "deep"


def test_existing_reliq_subtree_retains_context():
    from reliq import reliq

    parsed = reliq("<div><p>selected</p><b>excluded</b></div>")
    page = parse(parsed[0][0])
    assert page.tagName == "P"
    assert page.textContent == "selected"


@pytest.mark.parametrize("sizes", [(33, 9), (32, 10)])
def test_unrecognized_native_layout_uses_conversion(sizes, monkeypatch):
    from types import SimpleNamespace
    from domonic.ext import reliq_ as adapter

    adapter._packed_layout.cache_clear()
    monkeypatch.setattr(
        adapter,
        "_native_api",
        lambda: SimpleNamespace(chnode_sz=sizes[0], cattrib_sz=sizes[1]),
    )
    try:
        assert adapter._packed_layout() is False
    finally:
        adapter._packed_layout.cache_clear()


def test_large_packed_fields(native_mode):
    from reliq import reliq
    from domonic.ext.reliq_ import _native_api, _parse_native, _parse_public

    if _native_api() is None:
        pytest.skip("requires checked Reliq version")
    # Exercise lengths beyond a single byte / 16 bits, and multibyte data.
    source = (
        "<long-"
        + "x" * 300
        + ' title="'
        + "é" * 40000
        + '">hello</long-'
        + "x" * 300
        + ">"
    )
    parsed = reliq(source)
    assert _snapshot(_parse_native(parsed)) == _snapshot(_parse_public(parsed))
