"""Definition-time convenience API; no framework or route registration."""

import inspect

import pytest

from domonic import compile, compiled
from domonic.dom import DOMConfig, Node
from domonic.html import div, p
import domonic.ssr as ssr


@compiled
def standalone(name="World"):
    """A standalone module-level view."""
    return p(name)


def test_module_level_binding_and_metadata():
    assert standalone.is_compiled
    assert standalone is not standalone.__original__
    assert standalone.__original__ is standalone.original
    assert standalone.__wrapped__ is standalone.__original__
    assert standalone.__name__ == "standalone"
    assert standalone.__doc__ == "A standalone module-level view."
    assert standalone.__module__ == __name__
    assert inspect.signature(standalone) == inspect.signature(standalone.__original__)
    assert standalone() == compile(standalone.__original__)() == "<p>World</p>"
    assert standalone(name="Alice") == "<p>Alice</p>"


def test_compiles_during_decoration_and_never_on_first_call(monkeypatch):
    calls = []
    real_compile = ssr.compile

    def tracked(view, **kwargs):
        calls.append(kwargs)
        return real_compile(view, **kwargs)

    monkeypatch.setattr(ssr, "compile", tracked)

    @compiled
    def home(name="World"):
        return div(p(name))

    assert calls == [{"strict": False, "cache_dir": None}]
    assert home.is_compiled

    def forbidden(*args, **kwargs):
        pytest.fail("compilation or DOM construction on the request path")

    monkeypatch.setattr(ssr, "compile", forbidden)
    monkeypatch.setattr(Node, "__init__", forbidden)
    assert home() == "<div><p>World</p></div>"
    assert home("next") == "<div><p>next</p></div>"


def test_parameters_defaults_and_annotations():
    @compiled()
    def view(first: str = "one", *children, title: str = "title", **attrs) -> object:
        return div(first, children, _title=title, _id=attrs["id"])

    assert view(id="example") == str(view.__original__(id="example"))
    args = ("two", "three", "four")
    kwargs = {"title": "other", "id": "value"}
    assert view(*args, **kwargs) == compile(view.__original__)(*args, **kwargs)
    assert view.__annotations__ == view.__original__.__annotations__
    assert view.is_compiled


def test_disk_and_strict_options_pass_through(tmp_path, monkeypatch):
    calls = []
    real_compile = ssr.compile

    def tracked(view, **kwargs):
        calls.append(kwargs)
        return real_compile(view, **kwargs)

    monkeypatch.setattr(ssr, "compile", tracked)

    @compiled(strict=True, cache_dir=tmp_path)
    def view(name="first"):
        return p(name)

    assert calls == [{"strict": True, "cache_dir": tmp_path}]
    assert not view.cache_hit
    again = compiled(view.__original__, strict=True, cache_dir=tmp_path)
    assert again.cache_hit
    assert again("second") == "<p>second</p>"


@pytest.mark.parametrize("autoescape", [False, True])
def test_escaping_parity(monkeypatch, autoescape):
    monkeypatch.setattr(DOMConfig, "GLOBAL_AUTOESCAPE", autoescape)

    @compiled(strict=True)
    def view(value):
        return p(value, _title=value)

    value = '<b>"A&B"</b>'
    assert (
        view(value)
        == compile(view.__original__)(value)
        == str(view.__original__(value))
    )


def test_fallback_and_strict_match_explicit_api():
    def mutating(value):
        node = div()
        node.append(p(value))
        return node

    renderer = compiled(mutating)
    assert not renderer.is_compiled
    assert renderer.__original__ is mutating
    assert renderer("x") == compile(mutating)("x")
    with pytest.raises(ssr.UnsupportedView):
        compiled(mutating, strict=True)


def test_async_has_same_support_boundary_as_compile():
    async def view():
        return p("async")

    for api in (compile, compiled):
        with pytest.raises(TypeError, match="synchronous"):
            api(view)
