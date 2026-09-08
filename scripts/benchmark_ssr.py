#!/usr/bin/env python3
"""First-request SSR timings in separate Python processes; no render warmup.

Run: python scripts/benchmark_ssr.py --repeats 5
Compilation, imports and fixture creation occur before the request timer.
"""

import argparse
import json
from pathlib import Path
import statistics
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def worker(size, mode):
    import gc
    from time import perf_counter_ns
    from types import SimpleNamespace
    from domonic import compile
    from domonic.dom import DOMConfig
    from examples.ssr.compiled_views import profile, medium, large

    DOMConfig.GLOBAL_AUTOESCAPE = True
    user = SimpleNamespace(name="Alice & Bob <visitors>")
    fixtures = {
        "small": (profile, (user,)),
        "medium": (medium, (user, ["item <" + str(i) + ">" for i in range(200)])),
        "large": (
            large,
            (
                [
                    (f"Group {i}", [f"item {j} & more" for j in range(50)])
                    for i in range(100)
                ],
            ),
        ),
    }
    view, args = fixtures[size]
    compile_ms = 0.0
    if mode == "compiled":
        start = perf_counter_ns()
        renderer = compile(view, strict=True)
        compile_ms = (perf_counter_ns() - start) / 1e6
    else:
        renderer = view
    gc.collect()
    start = perf_counter_ns()
    result = str(renderer(*args))
    elapsed = (perf_counter_ns() - start) / 1e6
    # Validation deliberately follows the first-request measurement.
    assert result == str(view(*args))
    print(
        json.dumps(
            {"ms": elapsed, "compile_ms": compile_ms, "bytes": len(result.encode())}
        )
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument(
        "--worker", nargs=2, metavar=("SIZE", "MODE"), help=argparse.SUPPRESS
    )
    args = parser.parse_args()
    if args.worker:
        worker(*args.worker)
        return
    if args.repeats < 1:
        parser.error("--repeats must be positive")
    print("Fresh process per sample; first render only; milliseconds, medians.")
    print("size       normal   compiled   speedup   startup compile    bytes")
    for size in ("small", "medium", "large"):
        samples = {"normal": [], "compiled": []}
        for repeat in range(args.repeats):
            for mode in (
                ("normal", "compiled") if repeat % 2 == 0 else ("compiled", "normal")
            ):
                process = subprocess.run(
                    [
                        sys.executable,
                        str(Path(__file__).resolve()),
                        "--worker",
                        size,
                        mode,
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                )
                samples[mode].append(json.loads(process.stdout))
        normal = statistics.median(s["ms"] for s in samples["normal"])
        compiled = statistics.median(s["ms"] for s in samples["compiled"])
        startup = statistics.median(s["compile_ms"] for s in samples["compiled"])
        print(
            f"{size:<10} {normal:8.3f} {compiled:10.3f} {normal/compiled:8.1f}x"
            f' {startup:17.3f} {samples["compiled"][0]["bytes"]:8d}'
        )


if __name__ == "__main__":
    main()
