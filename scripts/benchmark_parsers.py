from __future__ import annotations

import argparse
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from domonic import domonic

DEFAULT_PARSERS = [
    "selectolax",
    "turbohtml",
    "lxml_html",
    "markupever",
    "html5_parser",
    "html.parser",
    "html5lib",
    "justhtml",
    "expat",
]


def benchmark_parser(html: str, parser_name: str, iterations: int) -> dict[str, object]:
    timings: list[float] = []
    title_text = ""
    error = None

    for _ in range(iterations):
        start = time.perf_counter()
        try:
            page = domonic.parseString(html, parser=parser_name)
            elapsed = time.perf_counter() - start
            timings.append(elapsed)
            if not title_text and page is not None:
                title = page.querySelector("title")
                title_text = title.text if title is not None else ""
        except Exception as exc:  # pragma: no cover - benchmark reporting path
            error = f"{type(exc).__name__}: {exc}"
            break

    if error is not None:
        return {"parser": parser_name, "ok": False, "error": error}

    return {
        "parser": parser_name,
        "ok": True,
        "iterations": iterations,
        "mean_ms": statistics.mean(timings) * 1000,
        "median_ms": statistics.median(timings) * 1000,
        "min_ms": min(timings) * 1000,
        "max_ms": max(timings) * 1000,
        "title": title_text.strip(),
    }


def print_results(results: list[dict[str, object]], page_path: Path, html: str) -> None:
    print(f"Benchmark page: {page_path}")
    print(f"HTML size: {len(html):,} bytes")
    print("")
    print(
        f"{'parser':<14} {'status':<8} {'mean ms':>10} {'median ms':>10} {'min ms':>10} {'max ms':>10}  title"
    )
    print("-" * 96)
    for row in results:
        if not row["ok"]:
            print(
                f"{row['parser']:<14} {'FAIL':<8} {'-':>10} {'-':>10} {'-':>10} {'-':>10}  {row['error']}"
            )
            continue
        print(
            f"{row['parser']:<14} {'OK':<8} "
            f"{row['mean_ms']:>10.2f} {row['median_ms']:>10.2f} {row['min_ms']:>10.2f} {row['max_ms']:>10.2f}  "
            f"{row['title']}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Benchmark domonic parser backends on a saved HTML page."
    )
    parser.add_argument("page", nargs="?", default="benchmarks/html_meaty_page.html")
    parser.add_argument("--iterations", type=int, default=7)
    parser.add_argument("--parsers", nargs="*", default=DEFAULT_PARSERS)
    args = parser.parse_args()

    page_path = Path(args.page)
    html = page_path.read_text(encoding="utf-8")

    results = [
        benchmark_parser(html, parser_name, args.iterations)
        for parser_name in args.parsers
    ]
    print_results(results, page_path, html)


if __name__ == "__main__":
    main()
