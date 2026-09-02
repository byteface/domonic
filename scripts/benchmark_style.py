"""
Micro-benchmark for domonic's CSSOM layer (``domonic.style``).

Covers the operations that show up in style-heavy code: creating declaration
blocks, shorthand expansion / reconstruction, ``cssText`` round-trips, and
``window.getComputedStyle`` cascade resolution over a real page.

    python scripts/benchmark_style.py
"""

from __future__ import annotations

import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from domonic import domonic  # noqa: E402
from domonic.style import CSSStyleDeclaration  # noqa: E402
from domonic.window import window  # noqa: E402

BENCH_DIR = Path(__file__).resolve().parents[1] / "benchmarks"


def bench(label, fn, n=2000, warmup=50):
    for _ in range(warmup):
        fn()
    samples = []
    for _ in range(5):
        start = time.perf_counter()
        for _ in range(n):
            fn()
        samples.append((time.perf_counter() - start) / n)
    best = min(samples)
    unit = "us" if best < 1e-3 else "ms"
    scaled = best * (1e6 if unit == "us" else 1e3)
    print(f"{label:<44} {scaled:8.2f} {unit}")


def main() -> None:
    print("CSSOM micro-benchmark\n" + "-" * 54)

    bench("CSSStyleDeclaration() construction", CSSStyleDeclaration)

    def parse_inline():
        s = CSSStyleDeclaration()
        s.cssText = "color: red; margin: 10px 5px; padding: 1rem; font-size: 14px"
        return s

    bench("cssText parse (4 declarations)", parse_inline, n=1000)

    def shorthand_expand():
        s = CSSStyleDeclaration()
        s.setProperty("border", "1px solid red")
        s.setProperty("margin", "10px")
        _ = s.getPropertyValue("border-color")
        _ = s.getPropertyValue("margin-top")

    bench("shorthand expand + longhand read", shorthand_expand, n=1000)

    def shorthand_reconstruct():
        s = CSSStyleDeclaration()
        for prop in ("padding-top", "padding-right", "padding-bottom", "padding-left"):
            s.setProperty(prop, "1rem")
        _ = s.getPropertyValue("padding")

    bench("4 longhands -> shorthand reconstruct", shorthand_reconstruct, n=1000)

    def set_camel():
        s = CSSStyleDeclaration()
        s.color = "blue"
        s.marginTop = "10px"

    bench("camelCase property set (x2)", set_camel, n=2000)

    # -- getComputedStyle over a real page --------------------------------
    page_path = BENCH_DIR / "html_meaty_page.html"
    if page_path.exists():
        page = domonic.parseString(
            page_path.read_text(encoding="utf-8", errors="replace"),
            parser="selectolax",
        )
        targets = page.querySelectorAll("p, a, div")[:400]
        n_rules = sum(len(s.cssRules) for s in (page.styleSheets or []))
        print(f"\ngetComputedStyle over {page_path.name}  "
              f"({len(targets)} elements, {n_rules} author rules)")

        # warm the document rule index once
        window.getComputedStyle(targets[0])
        counter = {"i": 0}

        def computed_next():
            el = targets[counter["i"] % len(targets)]
            counter["i"] += 1
            window.getComputedStyle(el).getPropertyValue("color")

        bench("  per element (warm rule index)", computed_next, n=200, warmup=20)
    else:
        print("\n(skip getComputedStyle bench - run make_bench_fixtures.py)")


if __name__ == "__main__":
    main()
