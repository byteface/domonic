"""
domonic._fontmetrics
====================================

Off-DOM text measurement for ``SVGElement.getBBox()`` /
``getComputedTextLength()`` -- the number a browser would read back after
laying out a ``<text>`` element.

The advance-width tables are Adobe's public-domain Helvetica / Helvetica-Bold
Core-14 metrics (units of 1/1000 em), the canonical "sans-serif" proxy used by
headless renderers such as ReportLab and PDFKit. A single sans-serif table
tracks real browser output for common labels closely enough for layout; it is
not a substitute for a real shaping engine.
"""

from __future__ import annotations

import re
from functools import lru_cache

# Advance widths, 1/1000 em, for printable ASCII 32..126.
_HELVETICA = (
    278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333, 278,
    278, 556, 556, 556, 556, 556, 556, 556, 556, 556, 556, 278, 278, 584, 584,
    584, 556, 1015, 667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556,
    833, 722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 278,
    278, 278, 469, 556, 333, 556, 556, 500, 556, 556, 278, 556, 556, 222, 222,
    500, 222, 833, 556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500,
    500, 334, 260, 334, 584,
)

_HELVETICA_BOLD = (
    278, 333, 474, 556, 556, 889, 722, 238, 333, 333, 389, 584, 278, 333, 278,
    278, 556, 556, 556, 556, 556, 556, 556, 556, 556, 556, 333, 333, 584, 584,
    584, 611, 975, 722, 722, 722, 722, 667, 611, 778, 722, 278, 556, 722, 611,
    833, 722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 333,
    278, 333, 584, 556, 333, 556, 611, 556, 611, 556, 333, 611, 611, 278, 278,
    556, 278, 889, 611, 611, 611, 611, 389, 556, 333, 611, 556, 778, 556, 556,
    500, 389, 280, 389, 584,
)

_DEFAULT_ADVANCE = 600  # code points outside the ASCII table
# browser getBBox().height / font-size for a single line of Helvetica; the
# ascent / descent split matches the usual 0.8 / 0.2 metrics.
_LINE_HEIGHT_RATIO = 1.15
_ASCENT_RATIO = 0.905
_DESCENT_RATIO = _LINE_HEIGHT_RATIO - _ASCENT_RATIO

_FONT_SIZE_RE = re.compile(r"(-?[\d.]+)\s*(px|pt|em|rem|%)?")
_BOLD_NAMES = {"bold", "bolder", "600", "700", "800", "900"}


def is_bold(weight) -> bool:
    if weight is None:
        return False
    if isinstance(weight, str):
        text = weight.strip().lower()
        if text in _BOLD_NAMES:
            return True
        match = _FONT_SIZE_RE.match(text)
        if match:
            try:
                return float(match.group(1)) >= 600
            except ValueError:
                return False
        return False
    try:
        return float(weight) >= 600
    except (TypeError, ValueError):
        return False


def parse_length(value, default: float = 16.0, em: float = 16.0) -> float:
    """Parse a CSS length / bare number into pixels."""
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return float(value)
    match = _FONT_SIZE_RE.match(str(value).strip())
    if not match:
        return default
    number = float(match.group(1))
    unit = (match.group(2) or "px").lower()
    if unit in ("px", "pt"):  # treat pt ~ px for layout purposes
        return number
    if unit in ("em", "rem"):
        return number * em
    if unit == "%":
        return number / 100 * em
    return number


@lru_cache(maxsize=8192)
def _advance_units(text: str, bold: bool) -> int:
    table = _HELVETICA_BOLD if bold else _HELVETICA
    total = 0
    for ch in text:
        code = ord(ch)
        if 32 <= code <= 126:
            total += table[code - 32]
        elif ch == "\t":
            total += table[0] * 4
        elif code < 32:
            continue
        else:
            total += _DEFAULT_ADVANCE
    return total


def advance_width(text: str, font_size: float, bold: bool = False) -> float:
    """Advance width of a single line of *text* at *font_size* px."""
    if not text:
        return 0.0
    return _advance_units(text, bool(bold)) / 1000.0 * float(font_size)


def text_extent(
    text: str, font_size: float, bold: bool = False, line_height: float | None = None
) -> tuple[float, float, float, float]:
    """Return ``(width, height, ascent, descent)`` in px for (multi-line) *text*.

    ``width`` is the widest line's advance; ``height`` covers every line at the
    line box height; ``ascent`` / ``descent`` are for the first line and are
    what SVG uses to place ``getBBox().y`` relative to the text baseline.
    """
    font_size = float(font_size)
    per_line = font_size * (
        _LINE_HEIGHT_RATIO if line_height is None else float(line_height)
    )
    lines = re.split(r"\r\n|\r|\n", text) if text else [""]
    width = max((advance_width(line, font_size, bold) for line in lines), default=0.0)
    height = per_line * len(lines)
    ascent = font_size * _ASCENT_RATIO
    descent = font_size * _DESCENT_RATIO
    return width, height, ascent, descent
