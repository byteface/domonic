"""
benchmark_javascript
~~~~~~~~~~~~~~~~~~~~~
Stress the hot paths of ``domonic.javascript`` and print per-op timings next
to the raw-Python equivalent, so pathological overhead (e.g. from the UTF-16
code-unit work or per-call signature inspection) stands out.

    python scripts/benchmark_javascript.py
"""
from __future__ import annotations

import re
import statistics
import sys
import time
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from domonic.javascript import Array, Number, RegExp, String


@dataclass
class Result:
    label: str
    js_ns: float
    py_ns: float | None

    @property
    def ratio(self) -> float | None:
        if self.py_ns in (None, 0):
            return None
        return self.js_ns / self.py_ns


def _time(fn, iterations: int, inner: int = 1) -> float:
    """Nanoseconds per logical op (median of several runs)."""
    samples = []
    for _ in range(5):
        start = time.perf_counter_ns()
        for _ in range(iterations):
            fn()
        samples.append((time.perf_counter_ns() - start) / (iterations * inner))
    return statistics.median(samples)


RESULTS: list[Result] = []


def bench(label, js_fn, py_fn=None, iterations=2000, inner=1):
    js = _time(js_fn, iterations, inner)
    py = _time(py_fn, iterations, inner) if py_fn else None
    RESULTS.append(Result(label, js, py))


# ---------------------------------------------------------------------------
# String -- the UTF-16 code-unit path
# ---------------------------------------------------------------------------
BMP = "the quick brown fox jumps over the lazy dog. " * 400  # ~18 KB, pure BMP
ASTRAL = ("hello 😀 world 汉字 " * 200)                        # astral chars
S_BMP = String(BMP)
S_ASTRAL = String(ASTRAL)


def _tokenize(s: String) -> int:
    """A tokenizer-style scan: charCodeAt over the whole string once."""
    n = s.length
    total = 0
    for i in range(n):
        total += s.charCodeAt(i)
    return total


def _tokenize_py(s: str) -> int:
    total = 0
    for i in range(len(s)):
        total += ord(s[i])
    return total


bench(
    "String.charCodeAt scan (18KB BMP, reused)",
    lambda: _tokenize(S_BMP),
    lambda: _tokenize_py(BMP),
    iterations=20,
    inner=len(BMP),
)
bench(
    "String.charCodeAt scan (astral, reused)",
    lambda: _tokenize(S_ASTRAL),
    lambda: _tokenize_py(ASTRAL),
    iterations=20,
    inner=len(ASTRAL),
)
bench(
    "String(src) fresh each call + .length",
    lambda: String(BMP).length,
    lambda: len(BMP),
    iterations=2000,
)
bench(
    "String.slice (reused, BMP)",
    lambda: S_BMP.slice(100, 200),
    lambda: BMP[100:200],
    iterations=20000,
)
bench(
    "String.indexOf (reused, BMP)",
    lambda: S_BMP.indexOf("lazy"),
    lambda: BMP.find("lazy"),
    iterations=20000,
)
bench(
    "String.charAt (reused, BMP)",
    lambda: S_BMP.charAt(5000),
    lambda: BMP[5000],
    iterations=50000,
)
bench(
    "String.replace regex /g (reused)",
    lambda: S_BMP.replace(RegExp(r"o", "g"), "0"),
    lambda: BMP.replace("o", "0"),
    iterations=200,
)

# ---------------------------------------------------------------------------
# Array iteration -- the _js_iteratee path
# ---------------------------------------------------------------------------
NUMS = list(range(5000))
A_NUMS = Array(*NUMS)

bench(
    "Array.map (5000, 1-arg cb)",
    lambda: A_NUMS.map(lambda x: x * 2),
    lambda: [x * 2 for x in NUMS],
    iterations=200,
    inner=len(NUMS),
)
bench(
    "Array.map (5000, 3-arg cb)",
    lambda: A_NUMS.map(lambda x, i, a: x + i),
    lambda: [x + i for i, x in enumerate(NUMS)],
    iterations=200,
    inner=len(NUMS),
)
bench(
    "Array.filter (5000)",
    lambda: A_NUMS.filter(lambda x: x % 2 == 0),
    lambda: [x for x in NUMS if x % 2 == 0],
    iterations=200,
    inner=len(NUMS),
)
bench(
    "Array.forEach (5000)",
    lambda: A_NUMS.forEach(lambda x: None),
    lambda: [None for x in NUMS],
    iterations=200,
    inner=len(NUMS),
)
bench(
    "Array.reduce (5000)",
    lambda: A_NUMS.reduce(lambda acc, x: acc + x, 0),
    lambda: sum(NUMS),
    iterations=200,
    inner=len(NUMS),
)
def _push_many():
    a = Array()
    for i in range(1000):
        a.push(i)
    return a


def _push_many_py():
    a = []
    for i in range(1000):
        a.append(i)
    return a


bench(
    "Array.push x1000 (fresh)",
    _push_many,
    _push_many_py,
    iterations=200,
    inner=1000,
)


# ---------------------------------------------------------------------------
# RegExp -- translation + exec/test loops
# ---------------------------------------------------------------------------
TEXT = "abc123 def456 ghi789 " * 300
_RX = RegExp(r"\d{3}")
_PY_RX = re.compile(r"\d{3}")


def _exec_loop():
    r = RegExp(r"\d+", "g")
    count = 0
    m = r.exec(TEXT)
    while m:
        count += 1
        m = r.exec(TEXT)
    return count


def _exec_loop_py():
    return len(re.findall(r"\d+", TEXT))


bench("RegExp construct + compile (cold)", lambda: RegExp(r"(\d{3})-(\w+)", "gi")._compiled(), None, iterations=5000)
bench("RegExp reused .test", lambda: _RX.test(TEXT), lambda: bool(_PY_RX.search(TEXT)), iterations=20000)
bench("RegExp exec /g full loop", _exec_loop, _exec_loop_py, iterations=500)
bench(
    r"RegExp \p{L} translate (cold each time)",
    lambda: RegExp(r"\p{L}+", "gu"),
    None,
    iterations=200,
)


# ---------------------------------------------------------------------------
# Number
# ---------------------------------------------------------------------------
bench("Number(x).toFixed(2)", lambda: Number(3.14159).toFixed(2), lambda: f"{3.14159:.2f}", iterations=20000)
bench("Number(x).toString(16)", lambda: Number(0xDEADBEEF).toString(16), lambda: format(0xDEADBEEF, "x"), iterations=20000)
bench("Number arithmetic (a+b)", lambda: Number(2) + Number(3), lambda: 2 + 3, iterations=50000)


# ---------------------------------------------------------------------------
# report
# ---------------------------------------------------------------------------
def _fmt(ns: float) -> str:
    if ns < 1000:
        return f"{ns:7.1f} ns"
    if ns < 1_000_000:
        return f"{ns/1000:7.2f} us"
    return f"{ns/1_000_000:7.2f} ms"


print(f"\n{'operation':<44} {'domonic':>12} {'python':>12} {'x':>7}")
print("-" * 80)
for r in RESULTS:
    py = _fmt(r.py_ns) if r.py_ns is not None else " " * 12
    ratio = f"{r.ratio:6.1f}x" if r.ratio is not None else "     -"
    flag = "  <-- slow" if (r.ratio or 0) > 25 else ""
    print(f"{r.label:<44} {_fmt(r.js_ns):>12} {py:>12} {ratio:>7}{flag}")
print()
