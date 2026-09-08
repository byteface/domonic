"""Run: python -m examples.ssr.localised_view (stdlib gettext; no server)."""

import gettext
from functools import partial
from pathlib import Path

from domonic import compiled
from domonic.dom import DOMConfig
from domonic.html import div, h1, p

DOMConfig.GLOBAL_AUTOESCAPE = True
LOCALES = Path(__file__).with_name("locales")


@compiled(strict=True)
def page(hello, welcome, language="en"):
    # Callable children run when rendering, after the template was compiled.
    return div(h1(hello), p(welcome), _lang=language)


def translations(language):
    if language == "en":
        return gettext.NullTranslations()  # English source messages.
    return gettext.translation("messages", localedir=LOCALES, languages=[language])


def render_language(language):
    _ = translations(language).gettext
    return page(
        partial(_, "Hello world"),
        partial(_, "Welcome, friends & visitors!"),
        language=language,
    )


if __name__ == "__main__":
    print(f"Compiled before choosing a language: {page.is_compiled}")
    # English again demonstrates that the first locale was not frozen/cached.
    for language in ("en", "fr", "de", "en"):
        print(f"{language}: {render_language(language)}")
