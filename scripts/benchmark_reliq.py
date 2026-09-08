"""Separate native parsing from DOM adaptation, with controlled GC and warmup.

Optionally compare the local htmlparser2 port using --htmlparser2-path PATH,
where PATH contains the htmlparser2 package (e.g. domonic-ui/src).
"""

from __future__ import annotations

import argparse
import gc
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from domonic import domonic


def measure(operation, iterations):
    result = operation()  # import and cache warmup outside the measurements
    del result
    timings = []
    was_enabled = gc.isenabled()
    for _ in range(iterations):
        gc.collect()
        gc.disable()
        try:
            start = time.perf_counter()
            result = operation()
            timings.append((time.perf_counter() - start) * 1000)
        finally:
            if was_enabled:
                gc.enable()
        del result
    return statistics.median(timings)


def measure_interleaved(operations, iterations):
    available = []
    for name, operation in operations:
        try:
            result = operation()
            del result
        except ImportError as exc:
            print(f"{name:<24} SKIP: {exc}")
        else:
            available.append((name, operation))
    if not available:
        return {}
    timings = {name: [] for name, _ in available}
    was_enabled = gc.isenabled()
    for iteration in range(iterations):
        # Rotate the starting backend each round to reduce ordering bias.
        offset = iteration % len(available)
        for name, operation in available[offset:] + available[:offset]:
            gc.collect()
            gc.disable()
            try:
                start = time.perf_counter()
                result = operation()
                timings[name].append((time.perf_counter() - start) * 1000)
            finally:
                if was_enabled:
                    gc.enable()
            del result
    return {name: statistics.median(values) for name, values in timings.items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("page", nargs="?", default="benchmarks/html_meaty_page.html")
    parser.add_argument("--iterations", type=int, default=15)
    parser.add_argument("--htmlparser2-path", type=Path)
    parser.add_argument(
        "--interleave",
        action="store_true",
        help="rotate backend order each timing round",
    )
    args = parser.parse_args()
    if args.iterations < 1:
        parser.error("--iterations must be positive")
    source = Path(args.page).read_text(encoding="utf-8")

    from reliq import reliq
    from domonic.ext.reliq_ import _native_api, _packed_layout, _parse_public

    operations = [
        ("reliq native", lambda: reliq(source)),
        ("reliq public adapter", lambda: _parse_public(reliq(source))),
        ("reliq domonic", lambda: domonic.parseString(source, parser="reliq")),
    ]
    try:
        from selectolax.lexbor import LexborHTMLParser

        operations.append(("selectolax native", lambda: LexborHTMLParser(source)))
    except ImportError:
        pass
    try:
        import tl

        operations.extend(
            [
                ("tl native", lambda: tl.parse(source)),
                ("tl domonic", lambda: domonic.parseString(source, parser="tl")),
            ]
        )
    except ImportError:
        pass
    for backend in ("selectolax", "turbohtml", "lxml_html", "html.parser"):
        operations.append(
            (
                backend + " domonic",
                lambda backend=backend: domonic.parseString(source, parser=backend),
            )
        )
    if args.htmlparser2_path:
        sys.path.insert(1, str(args.htmlparser2_path.resolve()))
        from htmlparser2.domonic_adapter import parse as htmlparser2_parse

        operations.append(("htmlparser2 domonic", lambda: htmlparser2_parse(source)))

    print(f"Page: {args.page} ({len(source.encode('utf-8')):,} bytes)")
    print(
        f"{args.iterations} iterations; one warmup; GC collected before, disabled during each timing"
    )
    print(f"Reliq native adapter enabled: {_native_api() is not None}")
    print(f"Reliq packed-array reads enabled: {_packed_layout()}")
    if args.interleave:
        print("Backend order rotates each round")
        for name, elapsed in measure_interleaved(operations, args.iterations).items():
            print(f"{name:<24} {elapsed:9.3f} ms")
        return
    for name, operation in operations:
        try:
            elapsed = measure(operation, args.iterations)
        except ImportError as exc:
            print(f"{name:<24} SKIP: {exc}")
        else:
            print(f"{name:<24} {elapsed:9.3f} ms")


if __name__ == "__main__":
    main()
