from __future__ import annotations

import argparse
import gc
import re
import statistics
import sys
import time
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bs4 import BeautifulSoup

from domonic.bs4 import BeautifulSlop


DEFAULT_SELECTOR = 'div#bodyContent a[href^="/wiki/"]'
DEFAULT_HREF_RE = r"^/wiki/(?!File:|Special:)"


def time_call(func: Callable[[], object], iterations: int) -> tuple[list[float], object]:
    timings = []
    result = None
    for _ in range(iterations):
        gc.collect()
        start = time.perf_counter()
        result = func()
        timings.append(time.perf_counter() - start)
    return timings, result


def summarize(label: str, timings: list[float], result: object) -> dict[str, object]:
    return {
        "case": label,
        "median_ms": statistics.median(timings) * 1000,
        "best_ms": min(timings) * 1000,
        "max_ms": max(timings) * 1000,
        "result": result,
    }


def run_benchmarks(
    html: str,
    slop_parser: str,
    iterations: int,
    selector: str,
    href_pattern: str,
) -> list[dict[str, object]]:
    href_re = re.compile(href_pattern)
    rows = []

    timings, result = time_call(
        lambda: BeautifulSoup(html, "html.parser").title.string,
        iterations,
    )
    rows.append(summarize("BS4 parse only", timings, result))

    timings, result = time_call(
        lambda: BeautifulSlop(html, slop_parser).find("title").text,
        iterations,
    )
    rows.append(summarize(f"BeautifulSlop {slop_parser} parse only", timings, result))

    bs4_soup = BeautifulSoup(html, "html.parser")
    slop = BeautifulSlop(html, slop_parser)

    timings, result = time_call(lambda: len(bs4_soup.select(selector)), iterations)
    rows.append(summarize("BS4 CSS query only", timings, result))

    timings, result = time_call(lambda: len(slop.select(selector)), iterations)
    rows.append(summarize("BeautifulSlop CSS query only", timings, result))

    timings, result = time_call(
        lambda: len(bs4_soup.find_all("a", href=href_re)),
        iterations,
    )
    rows.append(summarize("BS4 regex find_all only", timings, result))

    timings, result = time_call(
        lambda: len(slop.find_all("a", href=href_re)),
        iterations,
    )
    rows.append(summarize("BeautifulSlop regex find_all only", timings, result))
    return rows


def print_results(rows: list[dict[str, object]], page_path: Path, html: str) -> None:
    print(f"Benchmark page: {page_path}")
    print(f"HTML size: {len(html):,} bytes")
    print("")
    print(f"{'case':<38} {'median ms':>10} {'best ms':>10} {'max ms':>10}  result")
    print("-" * 84)
    for row in rows:
        print(
            f"{row['case']:<38} "
            f"{row['median_ms']:>10.2f} {row['best_ms']:>10.2f} {row['max_ms']:>10.2f}  "
            f"{row['result']}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Benchmark BeautifulSlop against Beautiful Soup 4."
    )
    parser.add_argument("page", nargs="?", default="benchmarks/html_meaty_page.html")
    parser.add_argument("--iterations", type=int, default=5)
    parser.add_argument("--slop-parser", default="markupever")
    parser.add_argument("--selector", default=DEFAULT_SELECTOR)
    parser.add_argument("--href-regex", default=DEFAULT_HREF_RE)
    args = parser.parse_args()

    page_path = Path(args.page)
    html = page_path.read_text(encoding="utf-8", errors="replace")
    rows = run_benchmarks(
        html,
        args.slop_parser,
        args.iterations,
        args.selector,
        args.href_regex,
    )
    print_results(rows, page_path, html)


if __name__ == "__main__":
    main()
