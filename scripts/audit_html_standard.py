#!/usr/bin/env python3
"""Compare domonic's HTML surface with the WHATWG HTML index."""

from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import urlopen

HTML_INDEX_URL = "https://html.spec.whatwg.org/multipage/indices.html"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


class HTMLIndexParser(HTMLParser):
    """Small parser for WHATWG's mostly-end-tag-optional index tables."""

    def __init__(self):
        super().__init__()
        self.current_caption = ""
        self._caption_text = []
        self._in_caption = False
        self._row = None
        self._cell = None
        self._in_code = False
        self._code_text = []
        self.rows = []

    def _close_cell(self):
        if self._cell is not None:
            self._row.append(self._cell)
            self._cell = None

    def _close_row(self):
        if self._row is not None:
            self._close_cell()
            self.rows.append((self.current_caption, self._row))
            self._row = None

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self._close_row()
            self.current_caption = ""
        elif tag == "caption":
            self._in_caption = True
            self._caption_text = []
        elif tag == "tr":
            self._close_row()
            self._row = []
        elif tag in ("td", "th") and self._row is not None:
            self._close_cell()
            self._cell = {"text": [], "codes": []}
        elif tag == "code" and self._cell is not None:
            self._in_code = True
            self._code_text = []

    def handle_data(self, data):
        if self._in_caption:
            self._caption_text.append(data)
        if self._cell is not None:
            self._cell["text"].append(data)
            if self._in_code:
                self._code_text.append(data)

    def handle_endtag(self, tag):
        if tag == "caption":
            self._in_caption = False
            self.current_caption = _clean_text(self._caption_text)
        elif tag == "code" and self._cell is not None and self._in_code:
            self._cell["codes"].append(_clean_text(self._code_text))
            self._in_code = False
        elif tag in ("td", "th"):
            self._close_cell()
        elif tag == "tr":
            self._close_row()
        elif tag == "table":
            self._close_row()

    def close(self):
        super().close()
        self._close_row()


def _clean_text(parts):
    return " ".join("".join(parts).split())


def _cell_text(cell):
    return _clean_text(cell["text"])


def _load_html(source):
    if source:
        return Path(source).read_text(encoding="utf-8")
    with urlopen(HTML_INDEX_URL, timeout=30) as response:
        return response.read().decode("utf-8")


def _parse_index(html):
    parser = HTMLIndexParser()
    parser.feed(html)
    parser.close()

    elements = set()
    attributes = set()
    event_handlers = set()
    events = set()

    for caption, row in parser.rows:
        if not row or not row[0]["codes"]:
            continue

        first = _cell_text(row[0])
        first_code = row[0]["codes"][0]

        if caption == "List of elements" and first not in ("Element", "autonomous custom elements"):
            if not first.startswith(("MathML ", "SVG ")):
                for code in row[0]["codes"]:
                    if re.match(r"^[a-z][a-z0-9]*$", code):
                        elements.add(code)
        elif caption == "List of attributes (excluding event handler content attributes)" and first != "Attribute":
            attributes.add(first_code)
        elif caption == "List of event handler content attributes" and first != "Attribute":
            event_handlers.add(first_code)
        elif caption == "List of events" and first != "Event":
            events.add(first_code)

    return elements, attributes, event_handlers, events


def audit(source=None):
    from domonic.events import Event, GlobalEventHandler, WindowEventHandler
    from domonic.html import html_attributes, html_tags

    elements, attributes, event_handlers, events = _parse_index(_load_html(source))
    event_values = {value for name, value in Event.__dict__.items() if name.isupper() and isinstance(value, str)}
    handler_values = set(GlobalEventHandler._handler_names) | set(WindowEventHandler._handler_names)

    return {
        "elements": sorted(elements - set(html_tags)),
        "attributes": sorted(attributes - set(html_attributes)),
        "event constants": sorted(events - event_values),
        "event handlers": sorted(event_handlers - handler_values),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        help="Use a local copy of the WHATWG indices page instead of fetching it.",
    )
    args = parser.parse_args(argv)

    missing = audit(args.source)
    failed = False
    for label, values in missing.items():
        print(f"missing {label}: {values}")
        failed = failed or bool(values)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
