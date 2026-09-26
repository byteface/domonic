#!/usr/bin/env python
"""Benchmark the DOM mutation path on a connected document.

Times the common mutation loops (append, insert, remove, replace, attribute
and text writes) against a document with some depth, so a change to
``appendChild`` / ``removeChild`` / ``_connect_tree`` and friends can be
measured rather than guessed at::

    python scripts/benchmark_mutation.py
    python scripts/benchmark_mutation.py --iterations 9 --n 4000

Absolute numbers move with machine load and thermal throttling; compare two
versions of the code interleaved in the same minute, not runs an hour apart.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from domonic.html import body, div, html, p, span  # noqa: E402


def best(func, iterations: int) -> float:
    timings = []
    for _ in range(iterations):
        start = time.perf_counter()
        func()
        timings.append((time.perf_counter() - start) * 1000)
    return min(timings)


def page(rows: int):
    """``html > body > div#c > (p > span)*rows`` -- a connected document."""
    container = div(*[p(span("x")) for _ in range(rows)], _id="c")
    html(body(container))
    return container


def cases(n: int):
    def append_child_fresh():
        container = page(50)
        for _ in range(n):
            container.appendChild(div())

    def append_fresh():
        container = page(50)
        for _ in range(n):
            container.append(div())

    def append_child_subtree():
        container = page(50)
        for _ in range(n // 4):
            container.appendChild(div(p(span("a")), p(span("b"))))

    def insert_before_first():
        container = page(50)
        first = container.firstChild
        for _ in range(n // 4):
            container.insertBefore(div(), first)

    def remove_child_back():
        container = page(n)
        while container.args:
            container.removeChild(container.args[-1])

    def remove_child_front():
        container = page(n)
        while container.args:
            container.removeChild(container.args[0])

    def remove_method():
        container = page(n)
        for child in list(container.args):
            child.remove()

    def replace_child_all():
        container = page(n // 4)
        for child in list(container.args):
            container.replaceChild(div(), child)

    def set_attribute_loop():
        container = page(n)
        for child in container.args:
            child.setAttribute("class", "k")

    def text_content_set():
        container = page(n)
        for child in container.args:
            child.textContent = "t"

    def inner_html_set():
        container = page(n // 4)
        for child in container.args:
            child.innerHTML = "<b>x</b>"

    def detached_append_child():
        container = div()
        for _ in range(n):
            container.appendChild(div())

    return [
        append_child_fresh,
        append_fresh,
        append_child_subtree,
        insert_before_first,
        remove_child_back,
        remove_child_front,
        remove_method,
        replace_child_all,
        set_attribute_loop,
        text_content_set,
        inner_html_set,
        detached_append_child,
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--iterations", type=int, default=5)
    parser.add_argument("--n", type=int, default=2000, help="operations per case")
    args = parser.parse_args()
    print("%-24s %10s" % ("case", "min ms"))
    for case in cases(args.n):
        print("%-24s %10.1f" % (case.__name__, best(case, args.iterations)))


if __name__ == "__main__":
    main()
