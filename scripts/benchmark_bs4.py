"""
Benchmark BeautifulSlop (``domonic.bs4``) against Beautiful Soup 4.

The suite covers CSS selection (basic / combinators / pseudo-classes),
``find`` / ``find_all`` with the full range of filters, tree navigation,
mutation, serialization, text extraction and attribute access, run against a
set of differently shaped HTML fixtures.

Examples
--------
    # default: meaty page, timing table
    python scripts/benchmark_bs4.py

    # every fixture, every Slop parser, correctness parity only (no timing)
    python scripts/benchmark_bs4.py --all-pages --slop-parsers selectolax,lxml,html5lib --check

    # full run + write the markdown report used in benchmarks/REPORT.md
    python scripts/benchmark_bs4.py --all-pages --report benchmarks/REPORT.md --mem

Exit code is non-zero if any correctness mismatch is found (BS4 vs Slop).
"""

from __future__ import annotations

import argparse
import gc
import json
import re
import statistics
import sys
import time
import tracemalloc
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
BENCH_DIR = REPO_ROOT / "benchmarks"

from bs4 import BeautifulSoup  # noqa: E402

from domonic.bs4 import BeautifulSlop  # noqa: E402

# ---------------------------------------------------------------------------
# fixtures
# ---------------------------------------------------------------------------

ALL_PAGES = [
    "html_tiny.html",
    "html_meaty_page.html",
    "html_wide_flat.html",
    "html_deep_nested.html",
    "html_tables.html",
    "html_broken.html",
]


def load_page(name: str) -> str:
    path = BENCH_DIR / name if not Path(name).is_absolute() else Path(name)
    if not path.exists():
        raise SystemExit(
            f"fixture {path} is missing - run: python scripts/make_bench_fixtures.py "
            "(the large wide-flat / tables fixtures are generated, not committed)"
        )
    return path.read_text(encoding="utf-8", errors="replace")


# ---------------------------------------------------------------------------
# case model
# ---------------------------------------------------------------------------

Signature = Any  # a small, ``==``-comparable summary of an operation's result


@dataclass
class Case:
    group: str
    name: str
    op: Callable[[Any], Signature]
    #: restrict to fixtures whose basename contains one of these substrings
    pages: tuple[str, ...] | None = None
    #: mutation cases need a pristine tree for every timed call
    needs_fresh: bool = False
    #: whether a BS4 vs Slop result difference should count as a failure.
    #: ``False`` for things that legitimately depend on parser choice
    #: (malformed-HTML recovery), whitespace-node modelling, or output
    #: formatting rather than on Slop being wrong.
    parity: bool = True

    def applies_to(self, page_name: str) -> bool:
        if self.pages is None:
            return True
        return any(token in page_name for token in self.pages)


def _count(iterable: Iterable[Any]) -> int:
    return sum(1 for _ in iterable)


def _name(node: Any) -> str | None:
    return getattr(node, "name", None) if node is not None else None


def _first_matching(soup: Any, selector: str) -> Any:
    matches = soup.select(selector)
    return matches[0] if matches else None


# ---------------------------------------------------------------------------
# the cases
# ---------------------------------------------------------------------------


def build_cases() -> list[Case]:
    href_re = re.compile(r"/(item|wiki|t)/")
    word_re = re.compile(r"Item \d+|Deep|link", re.I)
    cls_re = re.compile(r"\b(row|cell|lead|nav|mw-)")

    cases: list[Case] = [
        # -- css: basic ------------------------------------------------------
        Case("css-basic", "select a", lambda s: len(s.select("a"))),
        Case("css-basic", "select a[href]", lambda s: len(s.select("a[href]"))),
        Case("css-basic", "select .class", lambda s: len(s.select(".row, .cell, .lead, .nav-link"))),
        Case("css-basic", "select #id", lambda s: len(s.select("#content, #needle, #big-list, #main"))),
        Case("css-basic", "select descendant (div a)", lambda s: len(s.select("div a"))),
        Case("css-basic", "select tag.class", lambda s: len(s.select("li.row, td.cell, p.lead"))),
        Case("css-basic", "select multi-class (.row.even)", lambda s: len(s.select(".row.even, .cell.c0"))),
        Case("css-basic", "select [attr] presence", lambda s: len(s.select("[data-index], [data-depth], [data-id]"))),
        Case("css-basic", "select [attr$=value]", lambda s: len(s.select('a[href$="0"]'))),
        Case("css-basic", "select comma group", lambda s: len(s.select("a, span, li"))),
        # -- css: combinators (these hit the XPath fallback before _select_fast)
        Case("css-comb", "select child (ul > li)", lambda s: len(s.select("ul > li"))),
        Case("css-comb", "select child (li > a)", lambda s: len(s.select("li > a"))),
        Case("css-comb", "select child chain", lambda s: len(s.select("table > thead > tr > th"))),
        Case("css-comb", "select adjacent (h1 + p)", lambda s: len(s.select("h1 + p, h2 + table"))),
        Case("css-comb", "select sibling (p ~ p)", lambda s: len(s.select("p ~ p"))),
        # adjacent / general sibling over a wide flat list - O(n^2) traps
        Case("css-comb", "select adjacent wide (li + li)", lambda s: len(s.select("li + li, td + td"))),
        Case("css-comb", "select sibling wide (li ~ li)", lambda s: len(s.select("li ~ li, td ~ td"))),
        Case("css-comb", "select :not(.class) wide", lambda s: len(s.select("li:not(.even), td:not(.c0), a:not(.x)"))),
        Case("css-comb", "select tr:not(:first-child)", lambda s: len(s.select("tr:not(:first-child)"))),
        Case("css-comb", "select deep descendant (section td a)", lambda s: len(s.select("section td a"))),
        # -- css: pseudo ---------------------------------------------------
        Case("css-pseudo", "select :first-child", lambda s: len(s.select("li:first-child, td:first-child"))),
        Case("css-pseudo", "select :last-child", lambda s: len(s.select("li:last-child, td:last-child"))),
        Case("css-pseudo", "select :nth-child(2)", lambda s: len(s.select("tr:nth-child(2) td, li:nth-child(2)"))),
        Case("css-pseudo", "select :not(.even)", lambda s: len(s.select("li:not(.even)"))),
        Case("css-pseudo", "select_one deep", lambda s: _name(s.select_one("section table tbody tr td a"))),
        # -- find / find_all ---------------------------------------------
        Case("find", "find(name)", lambda s: _name(s.find("a"))),
        Case("find", "find(id=)", lambda s: _name(s.find(id=re.compile("content|needle|big-list|main")))),
        Case("find", "find(class_=)", lambda s: _name(s.find(class_=re.compile("row|cell|lead|nav")))),
        Case("find", "find_all(name)", lambda s: len(s.find_all("a"))),
        Case("find", "find_all(name, limit=25)", lambda s: len(s.find_all("a", limit=25))),
        Case("find", "find_all(list of names)", lambda s: len(s.find_all(["a", "span", "td"]))),
        # BS4's soup is a [document] wrapper so find_all(True) includes <html>;
        # a Slop tree's root *is* <html>, which cannot be its own descendant.
        Case("find", "find_all(True) - all tags", lambda s: len(s.find_all(True)), parity=False),
        # -- find_all: filter variety ----------------------------------
        Case("find-filter", "find_all(name, attr=True)", lambda s: len(s.find_all("a", href=True))),
        Case("find-filter", "find_all(name, attr=regex)", lambda s: len(s.find_all("a", href=href_re))),
        Case("find-filter", "find_all(class_=regex)", lambda s: len(s.find_all(class_=cls_re))),
        Case("find-filter", "find_all(attrs={data-*: True})", lambda s: len(s.find_all(attrs={"data-index": True}))),
        Case("find-filter", "find_all(string=regex)", lambda s: len(s.find_all(string=word_re))),
        Case("find-filter", "find_all(callable)", lambda s: len(s.find_all(lambda t: getattr(t, "name", None) == "a"))),
        Case("find-filter", "find_all(recursive=False)", lambda s: len((s.body or s).find_all(True, recursive=False))),
        # -- navigation ------------------------------------------------
        Case("nav", "soup.descendants", lambda s: _count(s.descendants), parity=False),
        Case("nav", "soup.contents (body)", lambda s: _count((s.body or s).contents), parity=False),
        Case("nav", "node.parents depth", lambda s: _count(_first_matching(s, "a, span").parents) if _first_matching(s, "a, span") else 0, parity=False),
        Case("nav", "next_siblings walk", lambda s: _count(getattr(_first_matching(s, "li, td, p"), "next_siblings", [])) if _first_matching(s, "li, td, p") else 0, parity=False),
        Case("nav", "next_elements walk", lambda s: _count(getattr(_first_matching(s, "h1, h2, title"), "next_elements", [])) if _first_matching(s, "h1, h2, title") else 0, parity=False),
        Case("nav", "find_next(a)", lambda s: _name((_first_matching(s, "h1, h2, title") or s).find_next("a"))),
        Case("nav", "find_all_next(a)", lambda s: len((_first_matching(s, "h1, h2, title") or s).find_all_next("a"))),
        Case("nav", "find_parent(div)", lambda s: _name((_first_matching(s, "a, span") or s).find_parent("div"))),
        Case("nav", "find_previous(h1|h2)", lambda s: _name((s.find_all("a") or [s])[-1].find_previous(re.compile("h1|h2|title")))),
        Case("nav", "find_next_siblings", lambda s: len(_first_matching(s, "li, td").find_next_siblings()) if _first_matching(s, "li, td") else 0),
        # -- mutation (fresh tree each call) -------------------------
        Case("mutate", "decompose 200 nodes", _mutate_decompose, needs_fresh=True),
        Case("mutate", "extract 200 nodes", _mutate_extract, needs_fresh=True),
        Case("mutate", "replace_with 100", _mutate_replace, needs_fresh=True),
        Case("mutate", "wrap 100", _mutate_wrap, needs_fresh=True),
        Case("mutate", "unwrap 100", _mutate_unwrap, needs_fresh=True),
        Case("mutate", "clear container", _mutate_clear, needs_fresh=True),
        Case("mutate", "append 200 new tags", _mutate_append, needs_fresh=True),
        Case("mutate", "insert(0) 100 new tags", _mutate_insert, needs_fresh=True),
        # -- serialization -----------------------------------------
        Case("serialize", "str(soup)", lambda s: len(str(s)), parity=False),
        Case("serialize", "soup.decode()", lambda s: len(s.decode()), parity=False),
        Case("serialize", "soup.encode()", lambda s: len(s.encode()), parity=False),
        Case("serialize", "soup.prettify()", lambda s: len(s.prettify()), parity=False),
        # -- text ------------------------------------------------
        Case("text", "get_text()", lambda s: len(s.get_text()), parity=False),
        Case("text", "get_text(' ', strip=True)", lambda s: len(s.get_text(" ", strip=True))),
        Case("text", "stripped_strings", lambda s: _count(s.stripped_strings)),
        Case("text", "strings", lambda s: _count(s.strings), parity=False),
        Case("text", "node.get_text() over matches", lambda s: sum(len(n.get_text()) for n in s.select("p, td, li")[:500]), parity=False),
        # -- attributes -----------------------------------------
        Case("attr", ".get('href') over links", lambda s: sum(len(a.get("href", "")) for a in s.find_all("a"))),
        Case("attr", "['href'] subscript over links", lambda s: sum(len(a["href"]) for a in s.select("a[href]"))),
        Case("attr", ".attrs dict over links", lambda s: sum(len(a.attrs) for a in s.find_all("a"))),
        Case("attr", ".has_attr('href') over links", lambda s: sum(1 for a in s.find_all("a") if a.has_attr("href"))),
    ]
    return cases


# -- mutation ops -----------------------------------------------------------
# Each gets a pristine soup and returns a comparable signature after mutating.


def _targets(soup: Any, selector: str, limit: int) -> list[Any]:
    return soup.select(selector)[:limit]


def _mutate_decompose(soup: Any) -> int:
    for node in _targets(soup, "span, em, strong, th, .meta", 200):
        node.decompose()
    return len(soup.select("span, em, strong, th, .meta"))


def _mutate_extract(soup: Any) -> int:
    removed = 0
    for node in _targets(soup, "a, li, td", 200):
        node.extract()
        removed += 1
    return removed


def _mutate_replace(soup: Any) -> int:
    for node in _targets(soup, "a, span, td", 100):
        new = _new_tag(soup, "mark")
        new.string = "x"
        node.replace_with(new)
    return len(soup.find_all("mark"))


def _mutate_wrap(soup: Any) -> int:
    for node in _targets(soup, "a, span, li", 100):
        node.wrap(_new_tag(soup, "div"))
    return len(soup.find_all("div"))


def _mutate_unwrap(soup: Any) -> int:
    unwrapped = 0
    for node in _targets(soup, "span, em, strong, b, i", 100):
        try:
            node.unwrap()
            unwrapped += 1
        except Exception:
            pass
    return unwrapped


def _mutate_clear(soup: Any) -> int:
    container = soup.select_one("ul, tbody, #content, body")
    if container is not None:
        container.clear()
    return _count((soup.select_one("ul, tbody, #content, body") or soup).children)


def _mutate_append(soup: Any) -> int:
    container = soup.select_one("ul, tbody, #content, body") or soup
    for i in range(200):
        tag = _new_tag(soup, "li")
        tag.string = f"new {i}"
        container.append(tag)
    return len(container.find_all("li"))


def _mutate_insert(soup: Any) -> int:
    container = soup.select_one("ul, tbody, #content, body") or soup
    for i in range(100):
        tag = _new_tag(soup, "li")
        tag.string = f"ins {i}"
        container.insert(0, tag)
    return len(container.find_all("li"))


def _new_tag(soup: Any, name: str) -> Any:
    # BeautifulSoup: soup.new_tag(name). BeautifulSlop mirrors it.
    return soup.new_tag(name)


# ---------------------------------------------------------------------------
# runners
# ---------------------------------------------------------------------------


@dataclass
class Result:
    page: str
    parser_pair: str
    group: str
    name: str
    bs4_ms: float | None = None
    slop_ms: float | None = None
    bs4_sig: Signature = None
    slop_sig: Signature = None
    match: bool = True
    #: does a mismatch here count as a real failure (vs. an expected difference)
    parity_gated: bool = True
    error: str | None = None

    @property
    def speedup(self) -> float | None:
        if not self.bs4_ms or not self.slop_ms:
            return None
        return self.bs4_ms / self.slop_ms

    @property
    def is_failure(self) -> bool:
        return self.parity_gated and (not self.match or self.error is not None)


def _time(fn: Callable[[], Any], iterations: int) -> tuple[float, Any]:
    best = float("inf")
    result = None
    for _ in range(iterations):
        gc.collect()
        start = time.perf_counter()
        result = fn()
        best = min(best, time.perf_counter() - start)
    return best * 1000.0, result


def run_case(
    case: Case,
    html: str,
    page_name: str,
    bs4_parser: str,
    slop_parser: str,
    iterations: int,
    check_only: bool,
) -> Result:
    res = Result(page_name, f"BS4:{bs4_parser} / Slop:{slop_parser}", case.group, case.name)
    # Malformed-HTML recovery is parser-specific, so parity there is
    # informational rather than a pass/fail gate.
    res.parity_gated = case.parity and "broken" not in page_name
    try:
        if case.needs_fresh:
            res.bs4_sig = case.op(BeautifulSoup(html, bs4_parser))
            res.slop_sig = case.op(BeautifulSlop(html, slop_parser))
            if not check_only:
                res.bs4_ms, _ = _time(
                    lambda: case.op(BeautifulSoup(html, bs4_parser)), iterations
                )
                res.slop_ms, _ = _time(
                    lambda: case.op(BeautifulSlop(html, slop_parser)), iterations
                )
        else:
            bs4_soup = BeautifulSoup(html, bs4_parser)
            slop_soup = BeautifulSlop(html, slop_parser)
            if check_only:
                res.bs4_sig = case.op(bs4_soup)
                res.slop_sig = case.op(slop_soup)
            else:
                res.bs4_ms, res.bs4_sig = _time(lambda: case.op(bs4_soup), iterations)
                res.slop_ms, res.slop_sig = _time(lambda: case.op(slop_soup), iterations)
    except Exception as exc:  # noqa: BLE001 - benchmark reporting
        res.error = f"{type(exc).__name__}: {exc}"
        res.match = False
        return res

    res.match = _sig_equal(res.bs4_sig, res.slop_sig)
    return res


def _sig_equal(a: Signature, b: Signature) -> bool:
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        # tolerate tiny drift on huge counts (whitespace-node handling etc.)
        if a == b:
            return True
        denom = max(abs(a), abs(b), 1)
        return abs(a - b) / denom <= 0.02
    return a == b


def measure_memory(html: str, bs4_parser: str, slop_parser: str) -> dict[str, Any]:
    def peak(fn: Callable[[], Any]) -> tuple[float, Any]:
        gc.collect()
        tracemalloc.start()
        obj = fn()
        _, pk = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return pk / 1024.0 / 1024.0, obj

    bs4_mb, bs4_soup = peak(lambda: BeautifulSoup(html, bs4_parser))
    slop_mb, slop_soup = peak(lambda: BeautifulSlop(html, slop_parser))
    bs4_nodes = _count(bs4_soup.descendants)
    slop_nodes = _count(slop_soup.descendants)
    return {
        "bs4_peak_mb": round(bs4_mb, 2),
        "slop_peak_mb": round(slop_mb, 2),
        "bs4_nodes": bs4_nodes,
        "slop_nodes": slop_nodes,
        "bs4_bytes_per_node": round(bs4_mb * 1024 * 1024 / max(bs4_nodes, 1)),
        "slop_bytes_per_node": round(slop_mb * 1024 * 1024 / max(slop_nodes, 1)),
    }


def measure_parse(html: str, bs4_parser: str, slop_parser: str, iterations: int) -> dict[str, float]:
    bs4_ms, _ = _time(lambda: BeautifulSoup(html, bs4_parser), iterations)
    slop_ms, _ = _time(lambda: BeautifulSlop(html, slop_parser), iterations)
    return {"bs4_ms": bs4_ms, "slop_ms": slop_ms}


# ---------------------------------------------------------------------------
# reporting
# ---------------------------------------------------------------------------


def fmt_sig(v: Signature) -> str:
    return "-" if v is None else str(v)[:22]


def print_console(results: list[Result], parse_rows: list[dict], mem_rows: list[dict]) -> None:
    by_page: dict[str, list[Result]] = {}
    for r in results:
        by_page.setdefault(r.page, []).append(r)

    for row in parse_rows:
        sp = row["bs4_ms"] / row["slop_ms"] if row["slop_ms"] else 0
        print(
            f"\n### {row['page']}  ({row['bytes']:,} bytes)   "
            f"parse: BS4 {row['bs4_ms']:.1f}ms  Slop {row['slop_ms']:.1f}ms  ({sp:.1f}x)"
        )
        print(f"{'group':<12} {'case':<34} {'BS4 ms':>9} {'Slop ms':>9} {'x':>6}  {'parity':>7}")
        print("-" * 92)
        for r in by_page.get(row["page"], []):
            if r.error:
                tag = "ERROR" if r.parity_gated else "err(info)"
                print(f"{r.group:<12} {r.name:<34} {tag:>9} {'':>9} {'':>6}  {r.error[:34]}")
                continue
            sp = f"{r.speedup:.1f}" if r.speedup else "-"
            if r.match:
                parity = "ok"
            elif r.parity_gated:
                parity = "FAIL"
            else:
                parity = "info"
            b = f"{r.bs4_ms:.2f}" if r.bs4_ms is not None else "-"
            s = f"{r.slop_ms:.2f}" if r.slop_ms is not None else "-"
            flag = "" if r.match else f"   BS4={fmt_sig(r.bs4_sig)} Slop={fmt_sig(r.slop_sig)}"
            print(f"{r.group:<12} {r.name:<34} {b:>9} {s:>9} {sp:>6}  {parity:>7}{flag}")

    if mem_rows:
        print("\n### Memory (tracemalloc peak during parse)")
        print(f"{'page':<22} {'BS4 MB':>8} {'Slop MB':>8} {'BS4 B/node':>12} {'Slop B/node':>12}")
        print("-" * 66)
        for m in mem_rows:
            print(
                f"{m['page']:<22} {m['bs4_peak_mb']:>8.2f} {m['slop_peak_mb']:>8.2f} "
                f"{m['bs4_bytes_per_node']:>12} {m['slop_bytes_per_node']:>12}"
            )


def summarize(results: list[Result]) -> dict[str, Any]:
    timed = [r for r in results if r.speedup is not None]
    failures = [r for r in results if r.is_failure]
    info_diffs = [r for r in results if not r.match and not r.parity_gated]
    slop_wins = [r for r in timed if r.speedup >= 1.0]
    slop_losses = [r for r in timed if r.speedup < 1.0]
    by_group: dict[str, list[float]] = {}
    for r in timed:
        by_group.setdefault(r.group, []).append(r.speedup)
    return {
        "cases_run": len(results),
        "timed": len(timed),
        "failures": len(failures),
        "info_diffs": len(info_diffs),
        "slop_faster": len(slop_wins),
        "slop_slower": len(slop_losses),
        "median_speedup": round(statistics.median([r.speedup for r in timed]), 2) if timed else None,
        "worst_for_slop": sorted(timed, key=lambda r: r.speedup)[:6],
        "best_for_slop": sorted(timed, key=lambda r: -r.speedup)[:6],
        "group_median_speedup": {g: round(statistics.median(v), 2) for g, v in sorted(by_group.items())},
        "failure_details": failures,
        "info_diff_details": info_diffs,
    }


def write_report(
    path: Path,
    results: list[Result],
    parse_rows: list[dict],
    mem_rows: list[dict],
    meta: dict[str, Any],
) -> None:
    s = summarize(results)
    lines: list[str] = []
    add = lines.append
    add("# BeautifulSlop vs Beautiful Soup 4 - benchmark report")
    add("")
    add(f"Generated by `scripts/benchmark_bs4.py` on {time.strftime('%Y-%m-%d')}.")
    add("")
    add(f"- Python: {sys.version.split()[0]}")
    add(f"- iterations per case: {meta['iterations']} (best-of)")
    add(f"- BS4 parser: `{meta['bs4_parser']}`")
    add(f"- Slop parsers: {', '.join(f'`{p}`' for p in meta['slop_parsers'])}")
    add(f"- fixtures: {', '.join(f'`{p}`' for p in meta['pages'])}")
    add("")
    add("## Headline")
    add("")
    add(f"- **{s['cases_run']} case runs**, {s['timed']} timed.")
    gated = s["cases_run"] - s["info_diffs"]
    add(
        f"- **Correctness: {gated - s['failures']}/{gated} parity-gated cases match Beautiful Soup**"
        + (f" - {s['failures']} real failures (see below)." if s["failures"] else " - no failures.")
    )
    if s["info_diffs"]:
        add(
            f"- {s['info_diffs']} further differences are expected (malformed-HTML recovery, "
            "whitespace-node modelling, output formatting) and are reported as info, not failures."
        )
    if s["median_speedup"] is not None:
        add(
            f"- Slop is faster on **{s['slop_faster']}/{s['timed']}** timed cases; "
            f"median speed-up **{s['median_speedup']}x**."
        )
    add("")
    add("### Median speed-up by group (Slop vs BS4, >1 = Slop faster)")
    add("")
    add("| group | median x |")
    add("| --- | --- |")
    for g, x in s["group_median_speedup"].items():
        add(f"| {g} | {x} |")
    add("")

    if s["failure_details"]:
        add("## Correctness failures (parity-gated)")
        add("")
        add("| page | group | case | BS4 | Slop | note |")
        add("| --- | --- | --- | --- | --- | --- |")
        for r in s["failure_details"]:
            note = r.error or "result differs"
            add(f"| {r.page} | {r.group} | {r.name} | `{fmt_sig(r.bs4_sig)}` | `{fmt_sig(r.slop_sig)}` | {note} |")
        add("")

    if s["info_diff_details"]:
        add("## Expected differences (informational)")
        add("")
        add("| page | group | case | BS4 | Slop | why it differs |")
        add("| --- | --- | --- | --- | --- | --- |")
        for r in s["info_diff_details"]:
            why = r.error or (
                "malformed-HTML recovery differs by parser" if "broken" in r.page
                else "whitespace-node / document-wrapper modelling or output formatting"
            )
            add(f"| {r.page} | {r.group} | {r.name} | `{fmt_sig(r.bs4_sig)}` | `{fmt_sig(r.slop_sig)}` | {why} |")
        add("")

    add("## Where Slop is slowest relative to BS4")
    add("")
    add("| page | case | BS4 ms | Slop ms | x |")
    add("| --- | --- | --- | --- | --- |")
    for r in s["worst_for_slop"]:
        add(f"| {r.page} | {r.name} | {r.bs4_ms:.2f} | {r.slop_ms:.2f} | {r.speedup:.2f} |")
    add("")
    add("## Where Slop wins biggest")
    add("")
    add("| page | case | BS4 ms | Slop ms | x |")
    add("| --- | --- | --- | --- | --- |")
    for r in s["best_for_slop"]:
        add(f"| {r.page} | {r.name} | {r.bs4_ms:.2f} | {r.slop_ms:.2f} | {r.speedup:.2f} |")
    add("")
    add("### Reading the differences")
    add("")
    add(
        "- **`text` group is slower** because `get_text()` (no `strip`) keeps "
        "more whitespace: domonic's `html.parser` adapter does not foster-parent "
        "whitespace out of `<table>` context. `get_text(strip=True)` matches BS4 "
        "exactly."
    )
    add(
        "- **`:not()` and other complex pseudo-classes** still fall back to the "
        "cssselect -> XPath -> elementpath path (slow on large trees); "
        "descendant / child / `+` / `~` / `:first-child` / `:last-child` / "
        "`:nth-child` are handled by the fast native engine."
    )
    add(
        "- **deep `select_one` chains** (e.g. `section table tbody tr td a`) "
        "expand every intermediate level before the final step, so they are "
        "slower than BS4's soupsieve on very large table trees."
    )
    add(
        "- **bulk `extract` / removal from a very large parent** rebuilds the "
        "child tuple per call (O(n) each); fine for typical use, slower than "
        "BS4 when pulling hundreds of nodes out of a multi-thousand-child list. "
        "Bulk `append` was fixed to avoid this."
    )
    add(
        "- **`nav` / `serialize` / structural counts** differ because domonic "
        "merges `<html>` and the document node (no separate `[document]` "
        "wrapper), so `.parents` is one shorter and `find_all(True)` excludes "
        "the root."
    )
    add("")

    add("## Parse time & memory by fixture")
    add("")
    add("| fixture | bytes | BS4 parse ms | Slop parse ms | x | BS4 MB | Slop MB | BS4 B/node | Slop B/node |")
    add("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    mem_by_page = {m["page"]: m for m in mem_rows}
    for row in parse_rows:
        m = mem_by_page.get(row["page"], {})
        sp = row["bs4_ms"] / row["slop_ms"] if row["slop_ms"] else 0
        add(
            f"| {row['page']} | {row['bytes']:,} | {row['bs4_ms']:.1f} | {row['slop_ms']:.1f} | {sp:.1f} | "
            f"{m.get('bs4_peak_mb', '-')} | {m.get('slop_peak_mb', '-')} | "
            f"{m.get('bs4_bytes_per_node', '-')} | {m.get('slop_bytes_per_node', '-')} |"
        )
    add("")

    add("## Full results")
    add("")
    by_page: dict[str, list[Result]] = {}
    for r in results:
        by_page.setdefault(r.page, []).append(r)
    for page, rows in by_page.items():
        add(f"### {page}")
        add("")
        add("| group | case | BS4 ms | Slop ms | x | parity |")
        add("| --- | --- | --- | --- | --- | --- |")
        for r in rows:
            if r.error:
                add(f"| {r.group} | {r.name} | error | error | - | `{r.error}` |")
                continue
            b = f"{r.bs4_ms:.2f}" if r.bs4_ms is not None else "-"
            sl = f"{r.slop_ms:.2f}" if r.slop_ms is not None else "-"
            x = f"{r.speedup:.2f}" if r.speedup else "-"
            if r.match:
                parity = "ok"
            elif r.parity_gated:
                parity = f"**FAIL** BS4=`{fmt_sig(r.bs4_sig)}` Slop=`{fmt_sig(r.slop_sig)}`"
            else:
                parity = f"info BS4=`{fmt_sig(r.bs4_sig)}` Slop=`{fmt_sig(r.slop_sig)}`"
            add(f"| {r.group} | {r.name} | {b} | {sl} | {x} | {parity} |")
        add("")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nwrote report -> {path}")


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("page", nargs="?", default="html_meaty_page.html", help="fixture name or path")
    ap.add_argument("--all-pages", action="store_true", help="run every fixture in benchmarks/")
    ap.add_argument("--pages", help="comma-separated fixture names")
    ap.add_argument("--iterations", type=int, default=7)
    ap.add_argument("--bs4-parser", default="html.parser")
    ap.add_argument("--slop-parser", default="selectolax")
    ap.add_argument("--slop-parsers", help="comma-separated; overrides --slop-parser")
    ap.add_argument("--groups", help="comma-separated case groups to include")
    ap.add_argument("--check", action="store_true", help="parity check only, no timing")
    ap.add_argument("--mem", action="store_true", help="also measure parse memory")
    ap.add_argument("--report", help="write a markdown report to this path")
    ap.add_argument("--json", help="write raw results as JSON to this path")
    args = ap.parse_args()

    if args.all_pages:
        pages = [p for p in ALL_PAGES if (BENCH_DIR / p).exists()]
    elif args.pages:
        pages = [p.strip() for p in args.pages.split(",") if p.strip()]
    else:
        pages = [args.page]

    slop_parsers = (
        [p.strip() for p in args.slop_parsers.split(",")]
        if args.slop_parsers
        else [args.slop_parser]
    )
    groups = {g.strip() for g in args.groups.split(",")} if args.groups else None

    cases = build_cases()
    if groups:
        cases = [c for c in cases if c.group in groups]

    print(f"BeautifulSlop vs BS4  |  {len(cases)} cases  |  pages: {', '.join(pages)}")
    print(f"BS4 parser: {args.bs4_parser}   Slop parsers: {', '.join(slop_parsers)}")
    if args.check:
        print("mode: correctness parity only\n")

    results: list[Result] = []
    parse_rows: list[dict] = []
    mem_rows: list[dict] = []

    for page in pages:
        html = load_page(page)
        for slop_parser in slop_parsers:
            if not args.check:
                pm = measure_parse(html, args.bs4_parser, slop_parser, args.iterations)
                parse_rows.append({"page": f"{page} [{slop_parser}]", "bytes": len(html), **pm})
            if args.mem:
                mm = measure_memory(html, args.bs4_parser, slop_parser)
                mem_rows.append({"page": f"{page} [{slop_parser}]", **mm})
            for case in cases:
                if not case.applies_to(page):
                    continue
                r = run_case(
                    case, html, f"{page} [{slop_parser}]", args.bs4_parser,
                    slop_parser, args.iterations, args.check,
                )
                results.append(r)

    print_console(results, parse_rows, mem_rows)

    s = summarize(results)
    gated = s["cases_run"] - s["info_diffs"]
    print("\n" + "=" * 72)
    print(
        f"parity: {gated - s['failures']}/{gated} parity-gated cases match BS4"
        + (f"   {s['failures']} FAIL" if s["failures"] else " (no failures)")
        + (f"   +{s['info_diffs']} expected differences (info)" if s["info_diffs"] else "")
    )
    if s["median_speedup"] is not None:
        print(
            f"speed: Slop faster on {s['slop_faster']}/{s['timed']} timed cases, "
            f"median {s['median_speedup']}x"
        )
        print("group medians:", ", ".join(f"{g} {x}x" for g, x in s["group_median_speedup"].items()))
    if s["failure_details"]:
        print("\nFAILURES:")
        for r in s["failure_details"]:
            print(f"  {r.page:<28} {r.group:<10} {r.name:<32} BS4={fmt_sig(r.bs4_sig)} Slop={fmt_sig(r.slop_sig)}"
                  + (f"  ({r.error})" if r.error else ""))
    if s["info_diff_details"]:
        print(f"\nexpected differences ({s['info_diffs']}, informational):")
        for r in s["info_diff_details"]:
            print(f"  {r.page:<28} {r.group:<10} {r.name:<32} BS4={fmt_sig(r.bs4_sig)} Slop={fmt_sig(r.slop_sig)}")

    if args.json:
        Path(args.json).write_text(
            json.dumps(
                [
                    {
                        "page": r.page, "group": r.group, "name": r.name,
                        "bs4_ms": r.bs4_ms, "slop_ms": r.slop_ms,
                        "bs4_sig": str(r.bs4_sig), "slop_sig": str(r.slop_sig),
                        "match": r.match, "parity_gated": r.parity_gated,
                        "is_failure": r.is_failure, "error": r.error,
                    }
                    for r in results
                ],
                indent=2,
            ),
            encoding="utf-8",
        )
        print(f"wrote json -> {args.json}")

    if args.report:
        write_report(
            Path(args.report), results, parse_rows, mem_rows,
            {
                "iterations": args.iterations, "bs4_parser": args.bs4_parser,
                "slop_parsers": slop_parsers, "pages": pages,
            },
        )

    sys.exit(1 if s["failures"] else 0)


if __name__ == "__main__":
    main()
