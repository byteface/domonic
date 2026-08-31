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


DEFAULT_SELECTORS = [
    'div#bodyContent a[href^="/wiki/"]',
    "div#bodyContent p a[href]",
    "a[href]",
    "table a[href]",
    "img[src]",
]
DEFAULT_COMPLEX_SELECTORS = [
    'div#bodyContent p:first-child a[href^="/wiki/"]',
    'div#bodyContent table tr:nth-child(2) a[href]',
    'div#bodyContent ul li:last-child a[href]',
    'div#bodyContent a[href*="Python"]',
]
DEFAULT_HREF_RE = r"^/wiki/(?!File:|Special:)"
DEFAULT_CLASS_RE = r"\bmw-|infobox|navbox|sidebar"


def time_call(func: Callable[[], object], iterations: int) -> tuple[list[float], object]:
    timings = []
    result = None
    for _ in range(iterations):
        gc.collect()
        start = time.perf_counter()
        result = func()
        timings.append(time.perf_counter() - start)
    return timings, result


def summarize(timings: list[float], result: object) -> dict[str, object]:
    return {
        "median_ms": statistics.median(timings) * 1000,
        "best_ms": min(timings) * 1000,
        "max_ms": max(timings) * 1000,
        "result": result,
    }


def bench(func: Callable[[], object], iterations: int) -> dict[str, object]:
    timings, result = time_call(func, iterations)
    return summarize(timings, result)


def decompose_matches(soup: object, selector: str) -> int:
    for node in soup.select(selector):
        node.decompose()
    return len(str(soup))


def parent_depth(node: object) -> int:
    return sum(1 for _ in getattr(node, "parents", ()))


def common_cases(
    selectors: list[str],
    href_pattern: str,
    class_pattern: str,
) -> list[tuple[str, Callable[[object], object], Callable[[object], object]]]:
    href_re = re.compile(href_pattern)
    class_re = re.compile(class_pattern)
    return [
        (
            "one CSS selector",
            lambda soup: len(soup.select(selectors[0])),
            lambda soup: len(soup.select(selectors[0])),
        ),
        (
            "five CSS selectors",
            lambda soup: sum(len(soup.select(selector)) for selector in selectors),
            lambda soup: sum(len(soup.select(selector)) for selector in selectors),
        ),
        (
            "complex CSS selectors",
            lambda soup: sum(
                len(soup.select(selector)) for selector in DEFAULT_COMPLEX_SELECTORS
            ),
            lambda soup: sum(
                len(soup.select(selector)) for selector in DEFAULT_COMPLEX_SELECTORS
            ),
        ),
        (
            "select_one id descendant",
            lambda soup: soup.select_one("div#bodyContent a[href]").get("href"),
            lambda soup: soup.select_one("div#bodyContent a[href]").get("href"),
        ),
        (
            "find id",
            lambda soup: soup.find(id="bodyContent").name,
            lambda soup: soup.find(id="bodyContent").name,
        ),
        (
            "find class",
            lambda soup: soup.find(class_="mw-parser-output").name,
            lambda soup: soup.find(class_="mw-parser-output").name,
        ),
        (
            "find_all links",
            lambda soup: len(soup.find_all("a")),
            lambda soup: len(soup.find_all("a")),
        ),
        (
            "find_all links limit 25",
            lambda soup: sum(
                len(link.get("href", "")) for link in soup.find_all("a", limit=25)
            ),
            lambda soup: sum(
                len(link.get("href", "")) for link in soup.find_all("a", limit=25)
            ),
        ),
        (
            "find_all href=True",
            lambda soup: len(soup.find_all("a", href=True)),
            lambda soup: len(soup.find_all("a", href=True)),
        ),
        (
            "regex find_all href",
            lambda soup: len(soup.find_all("a", href=href_re)),
            lambda soup: len(soup.find_all("a", href=href_re)),
        ),
        (
            "regex class find_all",
            lambda soup: len(soup.find_all(class_=class_re)),
            lambda soup: len(soup.find_all(class_=class_re)),
        ),
        (
            "callable find_all links",
            lambda soup: len(
                soup.find_all(lambda tag: getattr(tag, "name", None) == "a")
            ),
            lambda soup: len(
                soup.find_all(lambda tag: getattr(tag, "name", None) == "a")
            ),
        ),
        (
            "list-name find_all",
            lambda soup: len(soup.find_all(["a", "img", "table"])),
            lambda soup: len(soup.find_all(["a", "img", "table"])),
        ),
        (
            "attribute reads over links",
            lambda soup: sum(len(link.get("href", "")) for link in soup.find_all("a")),
            lambda soup: sum(len(link.get("href", "")) for link in soup.find_all("a")),
        ),
        (
            "parent traversal",
            lambda soup: parent_depth(soup.select_one(selectors[0])),
            lambda soup: parent_depth(soup.select_one(selectors[0])),
        ),
        (
            "text extraction",
            lambda soup: len(soup.get_text(" ", strip=True)),
            lambda soup: len(soup.get_text(" ", strip=True)),
        ),
        (
            "remove sidebars",
            lambda soup: decompose_matches(soup, ".sidebar, .navbox"),
            lambda soup: decompose_matches(soup, ".sidebar, .navbox"),
        ),
    ]


def run_end_to_end(
    html: str,
    bs4_parser: str,
    slop_parser: str,
    iterations: int,
    selectors: list[str],
    href_pattern: str,
    class_pattern: str,
) -> list[tuple[str, dict[str, object], dict[str, object]]]:
    cases = [
        (
            "parse only",
            lambda soup: soup.title.string,
            lambda soup: soup.find("title").text,
        ),
    ]
    cases.extend(
        (f"parse + {name}", bs4_op, slop_op)
        for name, bs4_op, slop_op in common_cases(
            selectors,
            href_pattern,
            class_pattern,
        )
    )
    rows = []
    for name, bs4_op, slop_op in cases:
        bs4_result = bench(
            lambda op=bs4_op: op(BeautifulSoup(html, bs4_parser)),
            iterations,
        )
        slop_result = bench(
            lambda op=slop_op: op(BeautifulSlop(html, slop_parser)),
            iterations,
        )
        rows.append((name, bs4_result, slop_result))
    return rows


def run_query_only(
    html: str,
    bs4_parser: str,
    slop_parser: str,
    iterations: int,
    selectors: list[str],
    href_pattern: str,
    class_pattern: str,
) -> list[tuple[str, dict[str, object], dict[str, object]]]:
    bs4_soup = BeautifulSoup(html, bs4_parser)
    slop = BeautifulSlop(html, slop_parser)
    cases = common_cases(selectors, href_pattern, class_pattern)
    return [
        (
            name,
            bench(lambda op=bs4_op: op(bs4_soup), iterations),
            bench(lambda op=slop_op: op(slop), iterations),
        )
        for name, bs4_op, slop_op in cases
    ]


def print_rows(
    title: str,
    rows: list[tuple[str, dict[str, object], dict[str, object]]],
    bs4_label: str,
    slop_label: str,
) -> None:
    print("")
    print(title)
    print(
        f"{'case':<42} {bs4_label:>12} {slop_label:>16} {'winner':>10}  result"
    )
    print("-" * 98)
    for name, bs4, slop in rows:
        winner = "Slop" if slop["median_ms"] < bs4["median_ms"] else "BS4"
        result = (
            bs4["result"]
            if bs4["result"] == slop["result"]
            else f"BS4={bs4['result']} Slop={slop['result']}"
        )
        print(
            f"{name:<42} "
            f"{bs4['median_ms']:>10.2f}ms {slop['median_ms']:>14.2f}ms "
            f"{winner:>10}  {result}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Benchmark BeautifulSlop against Beautiful Soup 4."
    )
    parser.add_argument("page", nargs="?", default="benchmarks/html_meaty_page.html")
    parser.add_argument("--iterations", type=int, default=7)
    parser.add_argument("--bs4-parser", default="html.parser")
    parser.add_argument("--slop-parser", default="selectolax")
    parser.add_argument("--href-regex", default=DEFAULT_HREF_RE)
    parser.add_argument("--class-regex", default=DEFAULT_CLASS_RE)
    args = parser.parse_args()

    page_path = Path(args.page)
    html = page_path.read_text(encoding="utf-8", errors="replace")
    bs4_label = f"BS4+{args.bs4_parser}"
    slop_label = f"Slop+{args.slop_parser}"

    print(f"Benchmark page: {page_path}")
    print(f"HTML size: {len(html):,} bytes")
    print(f"BS4 parser: {args.bs4_parser}")
    print(f"BeautifulSlop parser: {args.slop_parser}")

    print_rows(
        "End-to-end parse workflow",
        run_end_to_end(
            html,
            args.bs4_parser,
            args.slop_parser,
            args.iterations,
            DEFAULT_SELECTORS,
            args.href_regex,
            args.class_regex,
        ),
        bs4_label,
        slop_label,
    )
    print_rows(
        "Query-only after parse",
        run_query_only(
            html,
            args.bs4_parser,
            args.slop_parser,
            args.iterations,
            DEFAULT_SELECTORS,
            args.href_regex,
            args.class_regex,
        ),
        bs4_label,
        slop_label,
    )


if __name__ == "__main__":
    main()
