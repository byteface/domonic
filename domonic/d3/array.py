"""
domonic.d3.array
====================================

A port of `d3-array <https://github.com/d3/d3-array>`_ (v3): statistics,
search, iterables, transformations, sets, ticks and histogram binning.

The functions follow d3's semantics: ``None`` and ``NaN`` values are skipped by
the statistics helpers, empty inputs return ``None``, and an optional
``valueof(value, index, iterable)`` accessor is accepted wherever d3 takes one.
"""

from __future__ import annotations

import builtins
import functools
import math
import random as _random
from typing import Any, Callable, Iterable, Sequence

_builtin_min = builtins.min
_builtin_max = builtins.max

__all__ = [
    "ascending", "descending", "bisector", "bisect", "bisectLeft",
    "bisectRight", "bisectCenter", "Adder", "fsum", "fcumsum", "min", "minIndex",
    "max", "maxIndex", "extent", "sum", "mean", "median", "medianIndex",
    "cumsum", "mode", "variance", "deviation", "quantile", "quantileSorted",
    "quantileIndex", "range", "ticks", "tickIncrement", "tickStep", "nice",
    "quickselect", "least", "leastIndex", "greatest", "greatestIndex", "group",
    "groups", "index", "indexes", "rollup", "rollups", "flatGroup",
    "flatRollup", "groupSort", "count", "cross", "merge", "pairs", "permute",
    "shuffle", "shuffler", "transpose", "zip", "rank", "difference", "disjoint",
    "intersection", "subset", "superset", "union", "every", "some", "bin",
    "histogram", "thresholdSturges", "thresholdScott",
    "thresholdFreedmanDiaconis",
]


# -- comparators -----------------------------------------------------------

def ascending(a: Any, b: Any) -> float:
    if a is None or b is None:
        return math.nan
    if a < b:
        return -1
    if a > b:
        return 1
    if a >= b:
        return 0
    return math.nan


def descending(a: Any, b: Any) -> float:
    if a is None or b is None:
        return math.nan
    if b < a:
        return -1
    if b > a:
        return 1
    if b >= a:
        return 0
    return math.nan


def _identity(x: Any, *_a: Any) -> Any:
    return x


def _number(x: Any) -> float:
    if x is None:
        return math.nan
    try:
        return float(x)
    except (TypeError, ValueError):
        return math.nan


def _arity(fn: Callable) -> int:
    try:
        import inspect

        params = [
            p
            for p in inspect.signature(fn).parameters.values()
            if p.kind
            in (
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
            )
        ]
        return len(params)
    except (TypeError, ValueError):
        return 1


def _numbers(values: Iterable, valueof: Callable | None):
    if valueof is None:
        for value in values:
            n = _number(value)
            if n == n:  # not NaN
                yield n
    else:
        for index, value in enumerate(values):
            n = _number(valueof(value, index, values))
            if n == n:
                yield n


# -- bisect --------------------------------------------------------------

def bisector(f: Callable):
    """Return an object exposing ``left``, ``right`` and ``center`` bisection
    methods. ``f`` may be an accessor ``f(d)`` or a comparator ``f(d, x)``."""
    if _arity(f) >= 2:
        compare1 = f
        compare2 = f
        delta = lambda d, x: f(d, x)  # noqa: E731
    else:
        compare1 = ascending if f is ascending or f is descending else (
            lambda a, b: ascending(f(a), b)
        )
        compare2 = lambda d, x: ascending(f(d), x)  # noqa: E731
        delta = lambda d, x: ascending(f(d), x)  # noqa: E731
        if f is ascending or f is descending:
            compare1 = f
            compare2 = lambda d, x: f(d, x)  # noqa: E731

    def left(a: Sequence, x: Any, lo: int = 0, hi: int | None = None) -> int:
        if hi is None:
            hi = len(a)
        if lo < hi:
            if compare1(x, x) != 0:
                return hi
            while lo < hi:
                mid = (lo + hi) >> 1
                if compare2(a[mid], x) < 0:
                    lo = mid + 1
                else:
                    hi = mid
        return lo

    def right(a: Sequence, x: Any, lo: int = 0, hi: int | None = None) -> int:
        if hi is None:
            hi = len(a)
        if lo < hi:
            if compare1(x, x) != 0:
                return hi
            while lo < hi:
                mid = (lo + hi) >> 1
                if compare2(a[mid], x) <= 0:
                    lo = mid + 1
                else:
                    hi = mid
        return lo

    def center(a: Sequence, x: Any, lo: int = 0, hi: int | None = None) -> int:
        if hi is None:
            hi = len(a)
        i = left(a, x, lo, _builtin_max(lo, hi - 1))
        if i > lo and delta(a[i - 1], x) > -delta(a[i], x):
            return i - 1
        return i

    return type(
        "Bisector", (), {"left": staticmethod(left), "right": staticmethod(right),
                         "center": staticmethod(center)}
    )


_ascending_bisector = bisector(ascending)
bisectRight = _ascending_bisector.right
bisectLeft = _ascending_bisector.left
bisectCenter = bisector(_number).center


def bisect(a: Sequence, x: Any, lo: int = 0, hi: int | None = None) -> int:
    """Alias for :func:`bisectRight`."""
    return bisectRight(a, x, lo, hi)


# -- neumaier summation --------------------------------------------------

class Adder:
    """Full-precision (Shewchuk / Neumaier) summation, matching d3's ``Adder``."""

    def __init__(self) -> None:
        self._partials: list[float] = [0.0] * 32
        self._n = 0

    def add(self, x: float) -> "Adder":
        p = self._partials
        i = 0
        x = float(x)
        j = 0
        while j < self._n and j < 32:
            y = p[j]
            hi = x + y
            lo = (x - (hi - y)) if abs(x) < abs(y) else (y - (hi - x))
            if lo:
                p[i] = lo
                i += 1
            x = hi
            j += 1
        p[i] = x
        self._n = i + 1
        return self

    def valueOf(self) -> float:
        p = self._partials
        n = self._n
        hi = 0.0
        lo = 0.0
        if n > 0:
            n -= 1
            hi = p[n]
            while n > 0:
                x = hi
                n -= 1
                y = p[n]
                hi = x + y
                lo = y - (hi - x)
                if lo:
                    break
            if n > 0 and (
                (lo < 0 and p[n - 1] < 0) or (lo > 0 and p[n - 1] > 0)
            ):
                y = lo * 2
                x = hi + y
                if y == x - hi:
                    hi = x
        return hi

    def __float__(self) -> float:
        return self.valueOf()

    def __repr__(self) -> str:
        return f"Adder({self.valueOf()!r})"


def fsum(values: Iterable, valueof: Callable | None = None) -> float:
    adder = Adder()
    for n in _numbers(values, valueof):
        adder.add(n)
    return adder.valueOf()


def fcumsum(values: Iterable, valueof: Callable | None = None) -> list[float]:
    adder = Adder()
    out: list[float] = []
    if valueof is None:
        for value in values:
            n = _number(value)
            out.append(adder.add(n if n == n else 0.0).valueOf())
    else:
        for index, value in enumerate(values):
            n = _number(valueof(value, index, values))
            out.append(adder.add(n if n == n else 0.0).valueOf())
    return out


# -- statistics --------------------------------------------------------

def min(values: Iterable, valueof: Callable | None = None):
    result = None
    if valueof is None:
        for value in values:
            if value is not None and (result is None or result > value):
                if value == value:
                    result = value
    else:
        for index, value in enumerate(values):
            value = valueof(value, index, values)
            if value is not None and (result is None or result > value):
                if value == value:
                    result = value
    return result


def max(values: Iterable, valueof: Callable | None = None):
    result = None
    if valueof is None:
        for value in values:
            if value is not None and (result is None or result < value):
                if value == value:
                    result = value
    else:
        for index, value in enumerate(values):
            value = valueof(value, index, values)
            if value is not None and (result is None or result < value):
                if value == value:
                    result = value
    return result


def _extreme_index(values, valueof, better):
    best = None
    best_index = -1
    for index, value in enumerate(values):
        v = value if valueof is None else valueof(value, index, values)
        if v is not None and v == v and (best is None or better(v, best)):
            best = v
            best_index = index
    return best_index


def minIndex(values: Iterable, valueof: Callable | None = None) -> int:
    return _extreme_index(list(values), valueof, lambda a, b: a < b)


def maxIndex(values: Iterable, valueof: Callable | None = None) -> int:
    return _extreme_index(list(values), valueof, lambda a, b: a > b)


def extent(values: Iterable, valueof: Callable | None = None):
    min_v = None
    max_v = None
    items = enumerate(values)
    for index, value in items:
        value = value if valueof is None else valueof(value, index, values)
        if value is not None and value == value:
            if min_v is None:
                min_v = max_v = value
            else:
                if min_v > value:
                    min_v = value
                if max_v < value:
                    max_v = value
    return [min_v, max_v]


def sum(values: Iterable, valueof: Callable | None = None) -> float:
    total = 0.0
    for n in _numbers(values, valueof):
        total += n
    return total


def mean(values: Iterable, valueof: Callable | None = None):
    count_ = 0
    total = 0.0
    for n in _numbers(values, valueof):
        count_ += 1
        total += n
    return total / count_ if count_ else None


def cumsum(values: Iterable, valueof: Callable | None = None) -> list[float]:
    total = 0.0
    out: list[float] = []
    if valueof is None:
        for value in values:
            n = _number(value)
            total += n if n == n else 0.0
            out.append(total)
    else:
        for index, value in enumerate(values):
            n = _number(valueof(value, index, values))
            total += n if n == n else 0.0
            out.append(total)
    return out


def variance(values: Iterable, valueof: Callable | None = None):
    count_ = 0
    delta = 0.0
    mean_ = 0.0
    total = 0.0
    for n in _numbers(values, valueof):
        count_ += 1
        delta = n - mean_
        mean_ += delta / count_
        total += delta * (n - mean_)
    if count_ > 1:
        return total / (count_ - 1)
    return None


def deviation(values: Iterable, valueof: Callable | None = None):
    v = variance(values, valueof)
    return math.sqrt(v) if v is not None else None


def quantileSorted(
    values: Sequence, p: float, valueof: Callable | None = None
) -> float | None:
    n = len(values)
    p = _number(p)
    if not n or p != p:
        return None
    vof = (lambda v, i, a: _number(v)) if valueof is None else (
        lambda v, i, a: _number(valueof(v, i, a))
    )
    if p <= 0 or n < 2:
        return vof(values[0], 0, values)
    if p >= 1:
        return vof(values[n - 1], n - 1, values)
    i = (n - 1) * p
    i0 = math.floor(i)
    value0 = vof(values[i0], i0, values)
    value1 = vof(values[i0 + 1], i0 + 1, values)
    return value0 + (value1 - value0) * (i - i0)


def quantile(
    values: Iterable, p: float, valueof: Callable | None = None
) -> float | None:
    numbers = sorted(_numbers(values, valueof))
    if not numbers:
        return None
    p = _number(p)
    if p != p:
        return None
    if p <= 0 or len(numbers) < 2:
        return numbers[0]
    if p >= 1:
        return numbers[-1]
    i = (len(numbers) - 1) * p
    i0 = math.floor(i)
    return numbers[i0] + (numbers[i0 + 1] - numbers[i0]) * (i - i0)


def quantileIndex(values: Sequence, p: float, valueof: Callable | None = None):
    numbered = [
        (_number(v if valueof is None else valueof(v, i, values)), i)
        for i, v in enumerate(values)
    ]
    numbered = [pair for pair in numbered if pair[0] == pair[0]]
    if not numbered:
        return -1
    p = _number(p)
    if p != p:
        return -1
    numbered.sort()
    if p <= 0 or len(numbered) < 2:
        return numbered[0][1]
    if p >= 1:
        return numbered[-1][1]
    i = (len(numbered) - 1) * p
    i0 = math.floor(i)
    return numbered[i0][1] if i - i0 < 0.5 else numbered[i0 + 1][1]


def median(values: Iterable, valueof: Callable | None = None):
    return quantile(values, 0.5, valueof)


def medianIndex(values: Sequence, valueof: Callable | None = None):
    return quantileIndex(values, 0.5, valueof)


def mode(values: Iterable, valueof: Callable | None = None):
    counts: dict[Any, int] = {}
    best = None
    best_count = 0
    for index, value in enumerate(values):
        value = value if valueof is None else valueof(value, index, values)
        if value is not None and value == value:
            counts[value] = counts.get(value, 0) + 1
            if counts[value] > best_count:
                best_count = counts[value]
                best = value
    return best


def count(values: Iterable, valueof: Callable | None = None) -> int:
    total = 0
    for index, value in enumerate(values):
        value = value if valueof is None else valueof(value, index, values)
        n = _number(value)
        if n == n:
            total += 1
    return total


# -- range, ticks, nice ----------------------------------------------------

def range(*args: float) -> list:
    start: Any
    stop: Any
    step: Any
    if len(args) == 1:
        start, stop, step = 0, args[0], 1
    elif len(args) == 2:
        start, stop, step = args[0], args[1], 1
    else:
        start, stop, step = args[0], args[1], args[2]
    n = _builtin_max(0, math.ceil((stop - start) / step)) if step else 0
    return [start + i * step for i in _int_range(int(n))]


def _int_range(n: int):
    i = 0
    while i < n:
        yield i
        i += 1


_E10 = math.sqrt(50)
_E5 = math.sqrt(10)
_E2 = math.sqrt(2)


def tickIncrement(start: float, stop: float, count: int) -> float:
    step = (stop - start) / _builtin_max(0, count)
    if step <= 0 or not math.isfinite(step):
        return step if step else 0.0
    power = math.floor(math.log10(step))
    error = step / (10 ** power)
    if error >= _E10:
        factor = 10
    elif error >= _E5:
        factor = 5
    elif error >= _E2:
        factor = 2
    else:
        factor = 1
    if power >= 0:
        return factor * (10 ** power)
    return -(10 ** -power) / factor


def tickStep(start: float, stop: float, count: int) -> float:
    step0 = abs(stop - start) / _builtin_max(0, count)
    step1 = 10 ** math.floor(math.log10(step0)) if step0 > 0 else 0
    error = step0 / step1 if step1 else 0
    if error >= _E10:
        step1 *= 10
    elif error >= _E5:
        step1 *= 5
    elif error >= _E2:
        step1 *= 2
    return -step1 if stop < start else step1


def ticks(start: float, stop: float, count: int) -> list[float]:
    start, stop, count = float(start), float(stop), int(count)
    if start == stop and count > 0:
        return [start]
    reverse = stop < start
    if reverse:
        start, stop = stop, start
    step = tickIncrement(start, stop, count)
    if step == 0 or not math.isfinite(step):
        return []
    if step > 0:
        r0 = round(start / step)
        r1 = round(stop / step)
        if r0 * step < start:
            r0 += 1
        if r1 * step > stop:
            r1 -= 1
        out = [(r0 + i) * step for i in _int_range(int(r1 - r0 + 1))]
    else:
        inv = -step
        r0 = round(start * inv)
        r1 = round(stop * inv)
        if r0 / inv < start:
            r0 += 1
        if r1 / inv > stop:
            r1 -= 1
        out = [(r0 + i) / inv for i in _int_range(int(r1 - r0 + 1))]
    if reverse:
        out.reverse()
    return out


def nice(start: float, stop: float, count: int):
    start, stop = float(start), float(stop)
    prestep = None
    while True:
        step = tickIncrement(start, stop, count)
        if step == prestep or step == 0 or not math.isfinite(step):
            return [start, stop]
        if step > 0:
            start = math.floor(start / step) * step
            stop = math.ceil(stop / step) * step
        elif step < 0:
            start = math.ceil(start * step) / step
            stop = math.floor(stop * step) / step
        prestep = step


# -- quickselect --------------------------------------------------------

def quickselect(
    array: list,
    k: int,
    left: int = 0,
    right: int | None = None,
    compare: Callable = ascending,
) -> list:
    if right is None:
        right = len(array) - 1
    while right > left:
        if right - left > 600:
            n = right - left + 1
            m = k - left + 1
            z = math.log(n)
            s = 0.5 * math.exp(2 * z / 3)
            sd = 0.5 * math.sqrt(z * s * (n - s) / n) * (-1 if m - n / 2 < 0 else 1)
            new_left = _builtin_max(left, math.floor(k - m * s / n + sd))
            new_right = _builtin_min(right, math.floor(k + (n - m) * s / n + sd))
            quickselect(array, k, new_left, new_right, compare)
        t = array[k]
        i = left
        j = right
        array[left], array[k] = array[k], array[left]
        if _cmp(compare, array[right], t) > 0:
            array[left], array[right] = array[right], array[left]
        while i < j:
            array[i], array[j] = array[j], array[i]
            i += 1
            j -= 1
            while _cmp(compare, array[i], t) < 0:
                i += 1
            while _cmp(compare, array[j], t) > 0:
                j -= 1
        if _cmp(compare, array[left], t) == 0:
            array[left], array[j] = array[j], array[left]
        else:
            j += 1
            array[j], array[right] = array[right], array[j]
        if j <= k:
            left = j + 1
        if k <= j:
            right = j - 1
    return array


def _cmp(compare: Callable, a: Any, b: Any) -> float:
    r = compare(a, b)
    return 0 if r != r else r


# -- least / greatest --------------------------------------------------

def least(values: Iterable, compare: Callable = ascending):
    min_v = None
    defined = False
    if _arity(compare) == 1:
        keyof = compare
        min_key = None
        for value in values:
            key = keyof(value)
            if not defined:
                if ascending(key, key) == 0:
                    min_v, min_key, defined = value, key, True
            elif ascending(key, min_key) < 0:
                min_v, min_key = value, key
    else:
        for value in values:
            if not defined:
                if compare(value, value) == 0:
                    min_v, defined = value, True
            elif compare(value, min_v) < 0:
                min_v = value
    return min_v


def leastIndex(values: Iterable, compare: Callable = ascending) -> int:
    values = list(values)
    if _arity(compare) == 1:
        return minIndex(values, compare)
    min_index = -1
    min_v = None
    for i, value in enumerate(values):
        if min_index < 0:
            if compare(value, value) == 0:
                min_v, min_index = value, i
        elif compare(value, min_v) < 0:
            min_v, min_index = value, i
    return min_index


def greatest(values: Iterable, compare: Callable = ascending):
    max_v = None
    defined = False
    if _arity(compare) == 1:
        keyof = compare
        max_key = None
        for value in values:
            key = keyof(value)
            if not defined:
                if ascending(key, key) == 0:
                    max_v, max_key, defined = value, key, True
            elif ascending(key, max_key) > 0:
                max_v, max_key = value, key
    else:
        for value in values:
            if not defined:
                if compare(value, value) == 0:
                    max_v, defined = value, True
            elif compare(value, max_v) > 0:
                max_v = value
    return max_v


def greatestIndex(values: Iterable, compare: Callable = ascending) -> int:
    values = list(values)
    if _arity(compare) == 1:
        return maxIndex(values, compare)
    max_index = -1
    max_v = None
    for i, value in enumerate(values):
        if max_index < 0:
            if compare(value, value) == 0:
                max_v, max_index = value, i
        elif compare(value, max_v) > 0:
            max_v, max_index = value, i
    return max_index


# -- group / rollup ----------------------------------------------------

def _nest(values, mapper, reducer, keys):
    def regroup(values, i):
        if i >= len(keys):
            return reducer(values)
        groups: dict[Any, Any] = {}
        keyof = keys[i]
        for index, value in enumerate(values):
            key = keyof(value, index, values)
            groups.setdefault(key, []).append(value)
        for key in list(groups):
            groups[key] = regroup(groups[key], i + 1)
        return mapper(groups)

    return regroup(list(values), 0)


def _as_keys(keys):
    return [k if _arity(k) >= 2 else (lambda v, i, a, k=k: k(v)) for k in keys]


def group(values: Iterable, *keys: Callable) -> dict:
    return _nest(values, _identity, _identity, _as_keys(keys))


def groups(values: Iterable, *keys: Callable) -> list:
    return _nest(values, lambda g: list(g.items()), _identity, _as_keys(keys))


def index(values: Iterable, *keys: Callable) -> dict:
    return _nest(values, _identity, _unique, _as_keys(keys))


def indexes(values: Iterable, *keys: Callable) -> list:
    return _nest(values, lambda g: list(g.items()), _unique, _as_keys(keys))


def _unique(values):
    if len(values) != 1:
        raise ValueError("index: duplicate key")
    return values[0]


def rollup(values: Iterable, reduce: Callable, *keys: Callable) -> dict:
    return _nest(values, _identity, reduce, _as_keys(keys))


def rollups(values: Iterable, reduce: Callable, *keys: Callable) -> list:
    return _nest(values, lambda g: list(g.items()), reduce, _as_keys(keys))


def _flatten(groups, keys, depth=0):
    if depth == len(keys) - 1:
        for key, value in groups.items():
            yield (key, value)
    else:
        for key, value in groups.items():
            for tail in _flatten(value, keys, depth + 1):
                yield (key, *tail)


def flatGroup(values: Iterable, *keys: Callable) -> list:
    g = group(values, *keys)
    return list(_flatten(g, keys)) if keys else []


def flatRollup(values: Iterable, reduce: Callable, *keys: Callable) -> list:
    g = rollup(values, reduce, *keys)
    return list(_flatten(g, keys)) if keys else []


def groupSort(
    values: Iterable, comparator_or_accessor: Callable, key: Callable
) -> list:
    reduced = list(rollup(values, comparator_or_accessor, key).items())
    if _arity(comparator_or_accessor) == 1:
        reduced.sort(key=_functools_cmp(lambda a, b: ascending(a[1], b[1])))
    else:
        reduced.sort(key=_functools_cmp(lambda a, b: comparator_or_accessor(a[1], b[1])))
    return [k for k, _ in reduced]


# -- combinations ----------------------------------------------------------

def cross(*args) -> list:
    reduce = None
    values = list(args)
    if values and callable(values[-1]):
        reduce = values.pop()
    arrays = [list(v) for v in values]
    if not arrays or any(len(a) == 0 for a in arrays):
        return []
    lengths = [len(a) for a in arrays]
    idx = [0] * len(arrays)
    j = len(arrays) - 1
    product: list = []
    while True:
        product.append([arrays[i][idx[i]] for i in _int_range(len(arrays))])
        i = j
        idx[i] += 1
        while idx[i] == lengths[i]:
            if i == 0:
                return [reduce(*p) for p in product] if reduce else product
            idx[i] = 0
            i -= 1
            idx[i] += 1


def merge(arrays: Iterable[Iterable]) -> list:
    out: list = []
    for array in arrays:
        out.extend(array)
    return out


def pairs(values: Iterable, pairof: Callable | None = None) -> list:
    values = list(values)
    if pairof is None:
        pairof = lambda a, b: [a, b]  # noqa: E731
    return [pairof(values[i], values[i + 1]) for i in _int_range(len(values) - 1)]


def permute(source, keys: Iterable):
    return [source[k] for k in keys]


def shuffler(random: Callable):
    def shuffle(array: list, lo: int = 0, hi: int | None = None) -> list:
        if hi is None:
            hi = len(array)
        m = hi - lo
        while m:
            i = int(random() * m)
            m -= 1
            array[m + lo], array[i + lo] = array[i + lo], array[m + lo]
        return array

    return shuffle


shuffle = shuffler(_random.random)


def transpose(matrix: Sequence[Sequence]) -> list:
    matrix = [list(row) for row in matrix]
    if not matrix:
        return []
    n = _builtin_min(len(row) for row in matrix)
    return [[row[j] for row in matrix] for j in _int_range(n)]


def zip(*arrays) -> list:
    return transpose(arrays)


def rank(values: Iterable, comparator: Callable | None = None) -> list:
    values = list(values)
    if comparator is None:
        keyed = list(enumerate(values))
        keyed.sort(key=lambda p: (p[1] is None, p[1]))
    elif _arity(comparator) == 1:
        keyed = list(enumerate(values))
        keyed.sort(key=lambda p: (comparator(p[1]) is None, comparator(p[1])))
    else:
        keyed = sorted(enumerate(values), key=_functools_cmp(
            lambda a, b: comparator(a[1], b[1])
        ))
    out = [math.nan] * len(values)
    r = 0
    prev = object()
    for pos, (orig_index, value) in enumerate(keyed):
        cmp_value = value
        if comparator is not None and _arity(comparator) == 1:
            cmp_value = comparator(value)
        if pos == 0 or cmp_value != prev:
            r = pos
        out[orig_index] = r
        prev = cmp_value
    return out


# -- sets ----------------------------------------------------------------

def difference(values: Iterable, *others: Iterable) -> set:
    result = set(values)
    for other in others:
        for value in other:
            result.discard(value)
    return result


def disjoint(values: Iterable, other: Iterable) -> bool:
    other_set = set(other)
    for value in values:
        if value in other_set:
            return False
    return True


def intersection(*iterables: Iterable) -> set:
    if not iterables:
        return set()
    result = set(iterables[0])
    for other in iterables[1:]:
        result &= set(other)
    return result


def superset(values: Iterable, other: Iterable) -> bool:
    return set(other) <= set(values)


def subset(values: Iterable, other: Iterable) -> bool:
    return set(values) <= set(other)


def union(*iterables: Iterable) -> set:
    result: set = set()
    for iterable in iterables:
        result |= set(iterable)
    return result


# -- iterables ---------------------------------------------------------

def every(values: Iterable, test: Callable) -> bool:
    for index, value in enumerate(values):
        if not test(value, index, values):
            return False
    return True


def some(values: Iterable, test: Callable) -> bool:
    for index, value in enumerate(values):
        if test(value, index, values):
            return True
    return False


# -- histogram (bin) -----------------------------------------------------

class Bin(list):
    x0: Any = None
    x1: Any = None


def thresholdSturges(values, mn=None, mx=None) -> int:
    return _builtin_max(1, math.ceil(math.log2(count(values))) + 1) if count(values) else 1


def thresholdScott(values, mn, mx) -> int:
    c = count(values)
    d = deviation(values)
    if c and d:
        return math.ceil((mx - mn) * (c ** (1 / 3)) / (3.49 * d))
    return 1


def thresholdFreedmanDiaconis(values, mn, mx) -> int:
    c = count(values)
    q3 = quantile(values, 0.75)
    q1 = quantile(values, 0.25)
    d = (q3 - q1) if (q3 is not None and q1 is not None) else 0
    if c and d:
        return math.ceil((mx - mn) / (2 * d * (c ** (-1 / 3))))
    return 1


def bin():
    """Return a configurable histogram binning function (d3's ``bin()``)."""
    value = _identity
    domain = extent
    threshold: Any = thresholdSturges

    def histogram(data):
        data = list(data)
        n = len(data)
        values = [value(data[i], i, data) for i in _int_range(n)]
        xz = domain(values)
        x0, x1 = xz[0], xz[1]
        tz = threshold(values, x0, x1) if callable(threshold) else threshold
        step = math.inf

        if not isinstance(tz, (list, tuple)):
            tn = int(tz)
            if domain is extent:
                x0, x1 = nice(x0, x1, tn)
            tz = ticks(x0, x1, tn)
            if tz and tz[0] <= x0:
                step = tickIncrement(x0, x1, tn)
            if tz and tz[-1] >= x1:
                if domain is extent:
                    inc = tickIncrement(x0, x1, tn)
                    if math.isfinite(inc):
                        if inc > 0:
                            x1 = (math.floor(x1 / inc) + 1) * inc
                        elif inc < 0:
                            x1 = (math.ceil(x1 * -inc) + 1) / -inc
                else:
                    tz = list(tz)
                    tz.pop()
        else:
            tz = list(tz)

        tz = list(tz)
        m = len(tz)
        a = 0
        b = m
        while a < m and tz[a] <= x0:
            a += 1
        while b > 0 and tz[b - 1] > x1:
            b -= 1
        if a or b < m:
            tz = tz[a:b]
            m = b - a

        bins: list[Bin] = []
        for i in _int_range(m + 1):
            bucket = Bin()
            bucket.x0 = tz[i - 1] if i > 0 else x0
            bucket.x1 = tz[i] if i < m else x1
            bins.append(bucket)

        for i in _int_range(n):
            x = values[i]
            if x is not None and x == x and x0 <= x <= x1:
                if math.isfinite(step) and step > 0:
                    j = _builtin_min(m, math.floor((x - x0) / step))
                else:
                    j = bisect(tz, x, 0, m)
                bins[j].append(data[i])
        return bins

    def value_fn(f=None):
        nonlocal value
        if f is None:
            return value
        value = f if _arity(f) >= 2 else (lambda v, i, a: f(v))
        return histogram

    def domain_fn(d=None):
        nonlocal domain
        if d is None:
            return domain
        domain = d if callable(d) else (lambda values: [d[0], d[1]])
        return histogram

    def thresholds_fn(t=None):
        nonlocal threshold
        if t is None:
            return threshold
        if callable(t):
            threshold = t
        elif isinstance(t, (list, tuple)):
            threshold = list(t)
        else:
            threshold = int(t)
        return histogram

    histogram.value = value_fn
    histogram.domain = domain_fn
    histogram.thresholds = thresholds_fn
    return histogram


histogram = bin  # d3 v5 name


# -- small helpers -----------------------------------------------------

def _functools_cmp(cmp):
    return functools.cmp_to_key(lambda x, y: int(_cmp(cmp, x, y)))
