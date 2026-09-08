from types import SimpleNamespace

import pytest

from domonic import compile
from domonic.dom import DOMConfig, Node
from domonic.html import div, h1, p, ul, li, input, script, span
from domonic.ssr import UnsupportedView


@pytest.fixture(autouse=True)
def escape(monkeypatch):
    monkeypatch.setattr(DOMConfig, "GLOBAL_AUTOESCAPE", True)


def profile(user):
    return div(h1("Profile"), p(user.name, _class="bio", _title=user.name))


def test_profile_parity_and_no_nodes(monkeypatch):
    user = SimpleNamespace(name="A & <B> \"C\" 'D'")
    expected = str(profile(user))
    compiled = compile(profile, strict=True)

    def forbidden(*args, **kwargs):
        raise AssertionError("constructed a DOM node on the request path")

    monkeypatch.setattr(Node, "__init__", forbidden)
    assert compiled(user) == expected
    assert "&lt;B&gt;" in expected
    assert compiled.original is profile
    assert compiled.is_compiled
    assert '<div><h1>Profile</h1><p class="bio"' in compiled.source


def test_nested_comprehension_and_conditionals():
    def view(groups, visible=True):
        if visible:
            return div(
                [
                    ul([li(x if x else "empty") for x in group if x is not None])
                    for group in groups
                ]
            )
        return p("hidden")

    renderer = compile(view, strict=True)
    for visible in (True, False):
        assert renderer([["<&", ""], [None, "two"]], visible) == str(
            view([["<&", ""], [None, "two"]], visible)
        )


def test_defaults_and_assignments():
    def view(value="hello", *, title="Title"):
        label = value + "!"
        return p(label, _title=title)

    renderer = compile(view, strict=True)
    assert renderer() == str(view())
    assert renderer("bye", title="Other") == str(view("bye", title="Other"))


@pytest.mark.parametrize("quotes", ['"', "'", None])
@pytest.mark.parametrize("autoescape", [True, False])
def test_attributes_void_and_raw_text(monkeypatch, quotes, autoescape):
    monkeypatch.setattr(DOMConfig, "ATTRIBUTE_QUOTES", quotes)
    monkeypatch.setattr(DOMConfig, "GLOBAL_AUTOESCAPE", autoescape)

    def view(value):
        return div(
            input(_disabled="", _required=True, _value=value),
            script('if (a < b) alert("&");'),
            _class="x&y",
        )

    renderer = compile(view, strict=True)
    assert renderer("<&\"'") == str(view("<&\"'"))


def test_unsupported_mutation_falls_back_once():
    calls = []

    def view(value):
        calls.append(value)
        node = div()
        node.append(p(value))
        return node

    renderer = compile(view)
    assert calls == []
    assert not renderer.is_compiled
    assert renderer.fallback_reason
    assert renderer("x") == "<div><p>x</p></div>"
    assert calls == ["x"]
    with pytest.raises(UnsupportedView):
        compile(view, strict=True)


def test_config_change_falls_back(monkeypatch):
    renderer = compile(profile, strict=True)
    monkeypatch.setattr(DOMConfig, "GLOBAL_AUTOESCAPE", False)
    user = SimpleNamespace(name="<b>raw</b>")
    assert renderer(user) == str(profile(user))


def test_closure_updates_and_tag_rebinding():
    tag = div
    label = "first"

    def view():
        return tag(label)

    renderer = compile(view, strict=True)
    label = "second"
    assert renderer() == "<div>second</div>"
    tag = span
    assert renderer() == "<span>second</span>"


def test_dom_snapshot():
    node = div(p("original"))
    renderer = compile(node)
    node.append(p("later"))
    assert renderer() == "<div><p>original</p></div>"
    assert renderer.original is node


def test_source_unavailable():
    view = eval('lambda: "hello"')
    renderer = compile(view)
    assert not renderer.is_compiled
    assert renderer() == "hello"


def test_lazy_snapshot_does_not_call_at_compile_time(monkeypatch):
    calls = []

    def label():
        calls.append(1)
        return "<dynamic>"

    node = div(h1("Static"), label)
    renderer = compile(node)
    assert calls == []
    monkeypatch.setattr(
        Node, "__init__", lambda *a, **k: pytest.fail("constructed node")
    )
    assert renderer() == "<div><h1>Static</h1>&lt;dynamic&gt;</div>"
    assert calls == [1]


def test_dynamic_callable_child():
    def view(label):
        return p(label)

    renderer = compile(view, strict=True)
    calls = []

    def label():
        calls.append(1)
        return "A&B"

    assert renderer(label) == "<p>A&amp;B</p>"
    assert calls == [1]


def test_no_compile_time_default_or_view_execution():
    calls = []

    def default():
        calls.append(1)
        return "value"

    def view(value=default()):
        return p(value)

    renderer = compile(view, strict=True)
    assert calls == [1]
    assert renderer() == "<p>value</p>"
    assert calls == [1]


def test_element_parameter_shadowing_falls_back():
    def view(div):
        return div("text")

    assert not compile(view).is_compiled


def test_implicit_none_return():
    def view(show):
        if show:
            return p("yes")

    renderer = compile(view, strict=True)
    assert renderer(False) == str(view(False))


def test_comprehension_has_no_node_construction(monkeypatch):
    from examples.ssr.compiled_views import large

    groups = [("one", ["<two>", "three"]), ("four", ["five"])]
    expected = str(large(groups))
    renderer = compile(large, strict=True)
    monkeypatch.setattr(
        Node, "__init__", lambda *a, **k: pytest.fail("constructed node")
    )
    assert renderer(groups) == expected


def test_app_compile_preserves_unsupported_response_handlers():
    from domonic.ssr import CompiledRoutes

    response = object()

    def unsupported():
        return response

    class App(CompiledRoutes):
        def __init__(self):
            self.view_functions = {"profile": profile, "response": unsupported}

    app = App()
    assert app.compile() is app
    assert app.view_functions["profile"].original is profile
    assert app.view_functions["response"] is unsupported
    assert app.view_functions["response"]() is response
    assert not app.compiled_views["response"].is_compiled
    app.compile()
    assert app.view_functions["profile"].original is profile


def test_strict_app_compile_is_atomic():
    from domonic.ssr import CompiledRoutes

    class App(CompiledRoutes):
        view_functions = {"profile": profile, "bad": lambda: "response"}

    app = App()
    with pytest.raises(UnsupportedView):
        app.compile(strict=True)
    assert app.view_functions["profile"] is profile


def test_text_nodes_escape_like_normal_rendering():
    from domonic.dom import Text

    def view(value):
        return p(value)

    renderer = compile(view, strict=True)
    text = Text("<&")
    assert renderer(text) == str(view(text))
    assert compile(p(text))() == str(p(text))


def test_duplicate_normalized_attributes_fall_back():
    def view():
        return div(_id="first", id="second")

    renderer = compile(view)
    assert not renderer.is_compiled
    assert renderer() == str(view())


def test_mixed_html_string_return_falls_back():
    def view(flag):
        return div("safe") if flag else "<b>already rendered</b>"

    renderer = compile(view)
    assert not renderer.is_compiled
    assert renderer(False) == view(False)


def test_child_and_attribute_expressions_keep_argument_order():
    events = []

    class Values:
        @property
        def child(self):
            events.append("child")
            return "text"

        @property
        def title(self):
            events.append("title")
            return "title"

    def view(values):
        return div(p(values.child), _title=values.title)

    renderer = compile(view, strict=True)
    assert events == []
    expected = str(view(Values()))
    assert events == ["child", "title"]
    events.clear()
    assert renderer(Values()) == expected
    assert events == ["child", "title"]


def test_runtime_exception_does_not_retry_view():
    events = []

    class Values:
        @property
        def child(self):
            events.append("called")
            raise RuntimeError("application error")

    def view(values):
        return div(values.child)

    renderer = compile(view, strict=True)
    with pytest.raises(RuntimeError, match="application error"):
        renderer(Values())
    assert events == ["called"]


def test_disk_cache_hit_and_corrupt_entry_rebuild(tmp_path, monkeypatch):
    directory = tmp_path / "cache"
    first = compile(profile, strict=True, cache_dir=directory)
    assert not first.cache_hit
    second = compile(profile, strict=True, cache_dir=directory)
    assert second.cache_hit
    user = SimpleNamespace(name="<fresh request>")
    expected = str(profile(user))
    with monkeypatch.context() as patch:
        patch.setattr(Node, "__init__", lambda *a, **k: pytest.fail("constructed node"))
        assert second(user) == expected
    cache_file = next(directory.glob("*.bin"))
    assert cache_file.stat().st_mode & 0o077 == 0
    cache_file.write_bytes(b"truncated")
    repaired = compile(profile, strict=True, cache_dir=directory)
    assert not repaired.cache_hit
    assert repaired(user) == str(profile(user))
    assert compile(profile, strict=True, cache_dir=directory).cache_hit


def test_disk_cache_keys_include_static_markup_and_settings(tmp_path, monkeypatch):
    def view():
        return p("<static>")

    first = compile(view, strict=True, cache_dir=tmp_path)
    monkeypatch.setattr(DOMConfig, "GLOBAL_AUTOESCAPE", False)
    second = compile(view, strict=True, cache_dir=tmp_path)
    assert not first.cache_hit and not second.cache_hit
    assert second() == "<p><static></p>"
    assert len(list(tmp_path.glob("*.bin"))) == 2


def test_disk_cache_rejects_shared_directory(tmp_path):
    directory = tmp_path / "shared"
    directory.mkdir(mode=0o755)
    directory.chmod(0o755)
    with pytest.raises(ValueError, match="private"):
        compile(profile, cache_dir=directory)


def test_raw_html_parity_and_attribute_escaping(monkeypatch):
    from domonic.html import raw

    def view(content):
        return div(raw(content), p(content), _title=content)

    renderer = compile(view, strict=True)
    content = '<b title="x">A&B</b>'
    expected = str(view(content))
    monkeypatch.setattr(
        Node, "__init__", lambda *a, **k: pytest.fail("constructed node")
    )
    assert renderer(content) == expected
    assert '<b title="x">A&B</b><p>&lt;b' in expected
    assert 'title="&lt;b title=&quot;x&quot;' in expected


def test_raw_marker_in_normal_stream_snapshot_and_attributes():
    from domonic.html import raw

    content = raw("<b>trusted</b>")
    node = div([content], _title=content)
    assert str(node) == '<div title="&lt;b&gt;trusted&lt;/b&gt;"><b>trusted</b></div>'
    assert "".join(node._stream_value(content)) == content
    assert node.innerHTML == content
    assert compile(node)() == str(node)


def test_snapshot_disk_cache_keeps_callables_live(tmp_path):
    value = "one"
    node = div(lambda: value)
    assert not compile(node, cache_dir=tmp_path).cache_hit
    renderer = compile(node, cache_dir=tmp_path)
    assert renderer.cache_hit
    value = "<two>"
    assert renderer() == "<div>&lt;two&gt;</div>"


def test_example_startup_compiles_before_first_http_request(tmp_path, monkeypatch):
    import asyncio

    pytest.importorskip("fastapi")
    from examples.ssr import compiled_views as example

    async def exercise():
        app = example.create_app(cache_dir=tmp_path)
        async with app.router.lifespan_context(app):
            assert all(r.is_compiled for r in app.state.renderers.values())
            assert not any(r.cache_hit for r in app.state.renderers.values())
            expected_home = str(
                example.home(
                    "<visitor>",
                    "<strong>This notice is explicitly trusted HTML.</strong>",
                )
            )
            with monkeypatch.context() as patch:

                def forbidden(*args, **kwargs):
                    pytest.fail("compile or DOM construction during HTTP request")

                patch.setattr(Node, "__init__", forbidden)
                patch.setattr(example, "compile", forbidden)
                for path in ("/", "/profile", "/dashboard", "/large"):
                    messages = []

                    async def receive():
                        return {"type": "http.request", "body": b"", "more_body": False}

                    async def send(message):
                        messages.append(message)

                    await app(
                        {
                            "type": "http",
                            "asgi": {"version": "3.0"},
                            "http_version": "1.1",
                            "method": "GET",
                            "scheme": "http",
                            "path": path,
                            "raw_path": path.encode(),
                            "root_path": "",
                            "query_string": b"name=%3Cvisitor%3E",
                            "headers": [],
                            "server": ("test", 80),
                            "client": ("test", 1),
                        },
                        receive,
                        send,
                    )
                    assert messages[0]["status"] == 200
                    body = b"".join(m.get("body", b"") for m in messages).decode()
                    if path != "/large":
                        assert "&lt;visitor&gt;" in body
                    if path == "/":
                        assert body == expected_home
                        assert (
                            "<strong>This notice is explicitly trusted HTML.</strong>"
                            in body
                        )
        restarted = example.create_app(cache_dir=tmp_path)
        async with restarted.router.lifespan_context(restarted):
            assert all(r.cache_hit for r in restarted.state.renderers.values())

    asyncio.run(exercise())


@pytest.mark.parametrize("quote", ['"', "'", None, False, True, ""])
@pytest.mark.parametrize(
    "value", [None, True, False, 12, 1.5, "", "hidden", "'\"<&> café"]
)
@pytest.mark.parametrize("shortcuts", [(False, False), (True, False), (True, True)])
def test_specialised_dynamic_attributes_match_normal_serialization(
    monkeypatch, quote, value, shortcuts
):
    monkeypatch.setattr(DOMConfig, "ATTRIBUTE_QUOTES", quote)
    monkeypatch.setattr(DOMConfig, "HTMX_ENABLED", shortcuts[0])
    monkeypatch.setattr(DOMConfig, "ALPINE_ENABLED", shortcuts[1])

    def view(value):
        return p(
            value,
            _title=value,
            _hidden=value,
            _hx_get=value,
            _x_data=value,
            _className=value,
        )

    renderer = compile(view, strict=True)
    assert renderer(value) == str(view(value))


def test_specialised_attributes_still_escape_raw_markers():
    from domonic.html import raw

    def view(value):
        return p(value, _title=value)

    value = raw('<b title="x">trusted & content</b>')
    renderer = compile(view, strict=True)
    assert renderer(value) == str(view(value))
    assert 'title="&lt;b title=&quot;x&quot;' in renderer(value)
