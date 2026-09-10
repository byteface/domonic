"""Shared pytest configuration.

``--parser-backend`` (or the ``DOMONIC_TEST_PARSER`` environment variable)
forces :func:`domonic.parseString`'s default backend for the whole run, so the
suite can be exercised against every installed HTML parser::

    pytest tests/ --parser-backend=html5lib
    DOMONIC_TEST_PARSER=lxml_html pytest tests/

Tests that pass ``parser=`` explicitly are unaffected -- they stay pinned to the
backend they name. Tests that build the DOM programmatically (most of the WPT
ports) never parse and so are backend-independent by construction.

``scripts/test_all_backends.sh`` loops the whole suite over every backend.
"""

import os

import pytest

from domonic import domonic

_SUPPORTED_BACKENDS = (
    "turbohtml",
    "html.parser",
    "html5lib",
    "lxml_html",
    "selectolax",
    "markupever",
    "justhtml",
    "reliq",
    "tl",
    "expat",
)


def pytest_addoption(parser):
    parser.addoption(
        "--parser-backend",
        action="store",
        default=os.environ.get("DOMONIC_TEST_PARSER"),
        help=(
            "Force domonic.parseString's default backend for the whole run "
            "(one of: " + ", ".join(_SUPPORTED_BACKENDS) + "). Tests passing "
            "parser= explicitly are unaffected."
        ),
    )


def pytest_configure(config):
    backend = config.getoption("--parser-backend")
    if not backend:
        return
    try:
        domonic.parseString("<p>probe</p>", parser=backend)
    except ValueError as exc:  # unknown name
        raise pytest.UsageError(str(exc))
    except Exception as exc:  # not installed / import failure
        raise pytest.UsageError(f"parser backend {backend!r} is not usable here: {exc}")
    config._domonic_prev_parser = domonic.get_default_parser()
    domonic.set_default_parser(backend)
    config._domonic_forced_parser = backend


def pytest_unconfigure(config):
    prev = getattr(config, "_domonic_prev_parser", None)
    if prev is not None:
        domonic.set_default_parser(prev)


def pytest_report_header(config):
    backend = getattr(config, "_domonic_forced_parser", None)
    if backend:
        return f"domonic default parser forced to: {backend}"
    return None
