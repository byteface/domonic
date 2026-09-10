"""``domonic.register_parser`` -- plug an external HTML parser backend in by name.

Covers the myjs / htmlparser2 use case: a third-party backend that fully
replaces domonic's parsing and needs to receive ``document=`` (and any future
option) without its call signature breaking.
"""

import pytest

from domonic import domonic
from domonic.dom import DOMParser
from domonic.html import div


@pytest.fixture
def clean_registry():
    before = dict(domonic._CUSTOM_PARSERS)
    prev_default = domonic.get_default_parser()
    yield
    domonic._CUSTOM_PARSERS.clear()
    domonic._CUSTOM_PARSERS.update(before)
    domonic.set_default_parser(prev_default)


def test_registered_backend_is_used_by_name(clean_registry):
    seen = []

    def backend(source, **options):
        seen.append((source, options))
        return div("custom", _id="c")

    domonic.register_parser("mytest", backend)
    page = domonic.parseString("<p>hi</p>", parser="mytest")

    assert str(page) == '<div id="c">custom</div>'
    assert seen[0][0] == "<p>hi</p>"
    assert domonic.get_active_parser() == "mytest"


def test_options_are_forwarded_as_keywords(clean_registry):
    seen = []

    def backend(source, **options):
        seen.append(options)
        return div()

    domonic.register_parser("mytest", backend)

    domonic.parseString("<p>hi</p>", parser="mytest")
    assert seen[-1] == {"document": False, "debug": False}

    domonic.parseString("<p>hi</p>", parser="mytest", document=True)
    assert seen[-1]["document"] is True


def test_document_true_reaches_a_default_custom_backend(clean_registry):
    # The regression that hit myjs: document=True must not be coerced to
    # html5lib before a registered backend (set as the default) sees it.
    seen = []

    def backend(source, **options):
        seen.append(options.get("document"))
        return div()

    domonic.register_parser("mytest", backend)
    domonic.set_default_parser("mytest")

    domonic.parseString("<p>hi</p>", document=True)
    assert seen[-1] is True


def test_dom_parser_parsefromstring_uses_a_registered_default(clean_registry):
    seen = []

    def backend(source, **options):
        seen.append(options)
        return div("doc")

    domonic.register_parser("mytest", backend)
    domonic.set_default_parser("mytest")

    DOMParser().parseFromString("<p>hi</p>", "text/html")
    assert seen and seen[-1]["document"] is True


def test_explicit_builtin_with_document_true_still_raises(clean_registry):
    with pytest.raises(ValueError):
        domonic.parseString("<p>hi</p>", parser="html.parser", document=True)


def test_set_default_parser_accepts_a_registered_name(clean_registry):
    domonic.register_parser("mytest", lambda s, **o: div())
    domonic.set_default_parser("mytest")
    assert domonic.get_default_parser() == "mytest"


def test_set_default_parser_still_rejects_unknown_names(clean_registry):
    with pytest.raises(ValueError):
        domonic.set_default_parser("no-such-backend")


def test_auto_true_puts_the_backend_at_the_front_of_the_cascade(clean_registry):
    domonic.register_parser("firstinline", lambda s, **o: div("cascade"), auto=True)
    domonic.parseString("<p>hi</p>")  # parser="auto"
    assert domonic.get_active_parser() == "firstinline"


def test_a_registered_name_can_shadow_a_builtin(clean_registry):
    domonic.register_parser("html.parser", lambda s, **o: div("shadowed"))
    assert str(domonic.parseString("<p>hi</p>", parser="html.parser")) == "<div>shadowed</div>"


def test_register_parser_guards(clean_registry):
    with pytest.raises(ValueError):
        domonic.register_parser("auto", lambda s, **o: div())
    with pytest.raises(ValueError):
        domonic.register_parser("", lambda s, **o: div())
    with pytest.raises(TypeError):
        domonic.register_parser("x", "not callable")


def test_unregister_parser_reports_removal(clean_registry):
    domonic.register_parser("mytest", lambda s, **o: div())
    assert domonic.unregister_parser("mytest") is True
    assert domonic.unregister_parser("mytest") is False
    assert "mytest" not in domonic.registered_parsers()
