"""A single compiled template must keep gettext lookups dynamic."""

from functools import partial

from domonic.dom import DOMConfig, Node


def test_languages_change_without_recompiling_or_constructing_nodes(monkeypatch):
    monkeypatch.setattr(DOMConfig, "GLOBAL_AUTOESCAPE", True)
    from examples.ssr import localised_view as example

    renderer = example.page
    assert renderer.is_compiled
    expected = {}
    for language in ("en", "fr", "de"):
        translate = example.translations(language).gettext
        expected[language] = str(
            renderer.__original__(
                partial(translate, "Hello world"),
                partial(translate, "Welcome, friends & visitors!"),
                language,
            )
        )

    def forbidden(*args, **kwargs):
        raise AssertionError("DOM construction during compiled rendering")

    monkeypatch.setattr(Node, "__init__", forbidden)
    for language in ("en", "fr", "de", "en"):
        assert example.page is renderer
        result = example.render_language(language)
        assert result == expected[language]
        assert "&amp;" in result
    assert "Bonjour le monde" in expected["fr"]
    assert "Hallo Welt" in expected["de"]
    assert "Gäste" in expected["de"]
    assert "Hello world" in expected["en"]


def test_gettext_callbacks_run_each_render(monkeypatch):
    monkeypatch.setattr(DOMConfig, "GLOBAL_AUTOESCAPE", True)
    from examples.ssr.localised_view import page, translations

    calls = []
    language = "fr"

    def hello():
        calls.append(language)
        return translations(language).gettext("Hello world")

    assert calls == []
    assert "Bonjour le monde" in page(hello, "welcome")
    language = "de"
    assert "Hallo Welt" in page(hello, "welcome")
    assert calls == ["fr", "de"]
