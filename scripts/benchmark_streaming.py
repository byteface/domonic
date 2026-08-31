#!/usr/bin/env python
"""Benchmark domonic string rendering versus streamed rendering."""

from __future__ import annotations

import argparse
import gc
import statistics
import sys
import time
import tracemalloc
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from domonic.html import body, html, table, td, tr


class NullWriter:
    def __init__(self) -> None:
        self.length = 0

    def write(self, chunk: str) -> int:
        self.length += len(chunk)
        return len(chunk)


def lazy_rows(count: int):
    for index in range(count):
        yield tr(td(f"Row {index}"), td(f"Data {index}"))


def lazy_page(row_count: int):
    return html(body(table(lazy_rows(row_count))))


def render_to_string(row_count: int) -> int:
    return len(str(lazy_page(row_count)))


def render_to_stream(row_count: int) -> int:
    writer = NullWriter()
    for chunk in lazy_page(row_count).stream():
        writer.write(chunk)
    return writer.length


def measure(func: Callable[[int], int], row_count: int, iterations: int):
    timings = []
    peaks = []
    result = 0
    for _ in range(iterations):
        gc.collect()
        tracemalloc.start()
        start = time.perf_counter()
        result = func(row_count)
        timings.append((time.perf_counter() - start) * 1000)
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        peaks.append(peak)
    return {
        "median_ms": statistics.median(timings),
        "peak_bytes": statistics.median(peaks),
        "result": result,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", type=int, default=10000)
    parser.add_argument("--iterations", type=int, default=5)
    args = parser.parse_args()

    cases = [
        ("str(join stream)", render_to_string),
        ("stream to writer", render_to_stream),
    ]
    print(f"Rows: {args.rows:,}")
    print(f"{'case':<18} {'median ms':>10} {'peak KiB':>10} {'chars':>10}")
    print("-" * 54)
    for name, func in cases:
        result = measure(func, args.rows, args.iterations)
        print(
            f"{name:<18} "
            f"{result['median_ms']:>10.2f} "
            f"{result['peak_bytes'] / 1024:>10.1f} "
            f"{result['result']:>10}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
