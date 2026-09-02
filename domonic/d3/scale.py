"""
domonic.d3.scale
====================================

A port of `d3-scale <https://github.com/d3/d3-scale>`_ (v4): continuous scales
(linear, pow, sqrt, log, symlog, identity, radial), sequential and diverging
scales, and the discrete quantize / quantile / threshold / ordinal / band /
point scales.

Scales are callable objects. The fluent setters (``domain``, ``range``,
``clamp`` ...) return ``self`` when given an argument and the current value
otherwise, matching d3.
"""

from __future__ import annotations

import math
from datetime import datetime
from typing import Any, Callable, Sequence

from domonic.d3.array import bisect, quantile, quantileSorted, ticks, tickIncrement
from domonic.d3.interpolate import (
    interpolate as interpolateValue,
    interpolateNumber,
    interpolateRound,
)

__all__ = [
    "scaleLinear", "scaleIdentity", "scaleRadial", "scalePow", "scaleSqrt",
    "scaleLog", "scaleSymlog", "scaleQuantize", "scaleQuantile",
    "scaleThreshold", "scaleOrdinal", "scaleBand", "scalePoint",
    "scaleSequential", "scaleDiverging", "scaleImplicit", "tickFormat",
    "scaleTime", "scaleUtc",
]


def _identity(x: Any) -> Any:
    return x


def _constant(x: Any) -> Callable[[Any], Any]:
    return lambda _: x


def _number(x: Any) -> float:
    return math.nan if x is None else float(x)


def _normalize(a: float, b: float) -> Callable[[float], float]:
    b = b - a
    if b:
        return lambda x: (x - a) / b
    return _constant(0.5 if b == b else math.nan)


def _clamper(a: float, b: float) -> Callable[[float], float]:
    if a > b:
        a, b = b, a
    return lambda x: max(a, min(b, x))


def _bimap(domain, range_, interpolate):
    d0, d1 = domain[0], domain[1]
    r0, r1 = range_[0], range_[1]
    if d1 < d0:
        d0f = _normalize(d1, d0)
        r0f = interpolate(r1, r0)
    else:
        d0f = _normalize(d0, d1)
        r0f = interpolate(r0, r1)
    return lambda x: r0f(d0f(x))


def _polymap(domain, range_, interpolate):
    domain = list(domain)
    range_ = list(range_)
    if domain[-1] < domain[0]:
        domain = domain[::-1]
        range_ = range_[::-1]
    j = min(len(domain), len(range_)) - 1
    d = [_normalize(domain[i], domain[i + 1]) for i in range(j)]
    r = [interpolate(range_[i], range_[i + 1]) for i in range(j)]

    def piecewise(x: float) -> Any:
        i = bisect(domain, x, 1, j) - 1
        return r[i](d[i](x))

    return piecewise


# -- continuous ------------------------------------------------------

class ContinuousScale:
    def __init__(self, transform=_identity, untransform=_identity):
        self._transform = transform
        self._untransform = untransform
        self._domain: list = [0.0, 1.0]
        self._range: list = [0.0, 1.0]
        self._interpolate = interpolateValue
        self._clamp: Callable[[float], float] | None = None
        self._unknown: Any = None
        self._piecewise = None
        self._output = None
        self._input = None

    # internal
    def _rescale(self):
        clamp = self._clamp
        n = min(len(self._domain), len(self._range))
        if clamp is not None and clamp is not _identity:
            self._clamp = _clamper(self._domain[0], self._domain[n - 1])
        self._piecewise = _polymap if n > 2 else _bimap
        self._output = self._input = None
        return self

    def _clamp_fn(self, x: float) -> float:
        return self._clamp(x) if self._clamp is not None else x

    def __call__(self, x: Any) -> Any:
        if x is None:
            return self._unknown
        try:
            xf = float(x)
        except (TypeError, ValueError):
            return self._unknown
        if xf != xf:
            return self._unknown
        if self._output is None:
            self._output = (self._piecewise or _bimap)(
                [self._transform(d) for d in self._domain],
                self._range,
                self._interpolate,
            )
        return self._output(self._transform(self._clamp_fn(xf)))

    def invert(self, y: Any) -> float:
        if self._input is None:
            self._input = (self._piecewise or _bimap)(
                self._range,
                [self._transform(d) for d in self._domain],
                interpolateNumber,
            )
        return self._clamp_fn(self._untransform(self._input(float(y))))

    def domain(self, values: Sequence | None = None):
        if values is None:
            return list(self._domain)
        self._domain = [_number(v) for v in values]
        return self._rescale()

    def range(self, values: Sequence | None = None):
        if values is None:
            return list(self._range)
        self._range = list(values)
        return self._rescale()

    def rangeRound(self, values: Sequence):
        self._range = list(values)
        self._interpolate = interpolateRound
        return self._rescale()

    def clamp(self, value: bool | None = None):
        if value is None:
            return self._clamp is not None and self._clamp is not _identity
        self._clamp = _clamper(self._domain[0], self._domain[-1]) if value else None
        return self._rescale()

    def interpolate(self, fn: Callable | None = None):
        if fn is None:
            return self._interpolate
        self._interpolate = fn
        return self._rescale()

    def unknown(self, value: Any = _identity):
        if value is _identity:
            return self._unknown
        self._unknown = value
        return self

    def copy(self):
        clone = type(self)(self._transform, self._untransform)
        clone._domain = list(self._domain)
        clone._range = list(self._range)
        clone._interpolate = self._interpolate
        clone._unknown = self._unknown
        clone._clamp = self._clamp
        return clone._rescale()


class LinearishScale(ContinuousScale):
    def ticks(self, count: int | None = None) -> list:
        d = self._domain
        return ticks(d[0], d[-1], 10 if count is None else count)

    def tickFormat(self, count: int | None = None, specifier: str | None = None):
        d = self._domain
        return tickFormat(d[0], d[-1], 10 if count is None else count, specifier)

    def nice(self, count: int | None = None):
        count = 10 if count is None else count
        d = list(self._domain)
        i0, i1 = 0, len(d) - 1
        start, stop = d[i0], d[i1]
        if stop < start:
            start, stop = stop, start
            i0, i1 = i1, i0
        prestep = None
        for _ in range(10):
            step = tickIncrement(start, stop, count)
            if step == prestep:
                d[i0], d[i1] = start, stop
                return self.domain(d)
            if step > 0:
                start = math.floor(start / step) * step
                stop = math.ceil(stop / step) * step
            elif step < 0:
                start = math.ceil(start * step) / step
                stop = math.floor(stop * step) / step
            else:
                break
            prestep = step
        return self


def scaleLinear(*args) -> LinearishScale:
    scale = LinearishScale()._rescale()
    return _init_range_domain(scale, args)


def _init_range_domain(scale, args):
    if len(args) == 1:
        scale.range(args[0])
    elif len(args) >= 2:
        scale.domain(args[0]).range(args[1])
    return scale


# -- identity / radial ---------------------------------------------

class IdentityScale(LinearishScale):
    def __call__(self, x: Any) -> Any:
        if x is None:
            return self._unknown
        try:
            xf = float(x)
        except (TypeError, ValueError):
            return self._unknown
        return self._unknown if xf != xf else xf

    def invert(self, y: Any) -> float:
        return float(y)

    def range(self, values: Sequence | None = None):
        if values is None:
            return list(self._domain)
        self._domain = [_number(v) for v in values]
        return self


def scaleIdentity(*args) -> IdentityScale:
    scale = IdentityScale()
    if args:
        scale.domain(args[0])
    return scale


class RadialScale(LinearishScale):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._squared = LinearishScale()._rescale()
        self._round = False

    def _sign_square(self, x):
        return -((-x) ** 2) if x < 0 else x * x

    def _sign_sqrt(self, x):
        return -math.sqrt(-x) if x < 0 else math.sqrt(x)

    def __call__(self, x):
        y = self._squared(_number(x))
        if y != y:
            return self._unknown
        return round(y) if self._round else y

    def invert(self, y):
        return self._squared.invert(self._sign_square(_number(y)))

    def domain(self, values=None):
        if values is None:
            return self._squared.domain()
        self._squared.domain([self._sign_square(_number(v)) for v in values])
        return self

    def range(self, values=None):
        if values is None:
            return self._squared.range()
        self._squared.range([self._sign_square(_number(v)) for v in values])
        return self

    def rangeRound(self, values):
        self.range(values)
        self._round = True
        return self

    def round(self, value=None):
        if value is None:
            return self._round
        self._round = bool(value)
        return self


def scaleRadial(*args) -> RadialScale:
    scale = RadialScale()
    return _init_range_domain(scale, args)


# -- power / sqrt -------------------------------------------------

class PowScale(LinearishScale):
    def __init__(self, *a, **k):
        self._exponent = 1.0
        super().__init__(*a, **k)
        self._update_transform()

    def _update_transform(self):
        e = self._exponent
        if e == 1:
            self._transform = self._untransform = _identity
        elif e == 0.5:
            self._transform = self._transform_sqrt
            self._untransform = self._untransform_sqrt
        else:
            self._transform = lambda x: -((-x) ** e) if x < 0 else x ** e
            self._untransform = (
                lambda x: -((-x) ** (1 / e)) if x < 0 else x ** (1 / e)
            )
        self._output = self._input = None

    @staticmethod
    def _transform_sqrt(x):
        return -math.sqrt(-x) if x < 0 else math.sqrt(x)

    @staticmethod
    def _untransform_sqrt(x):
        return -(x * x) if x < 0 else x * x

    def exponent(self, value: float | None = None):
        if value is None:
            return self._exponent
        self._exponent = float(value)
        self._update_transform()
        return self._rescale()

    def copy(self):
        clone = super().copy()
        clone._exponent = self._exponent
        clone._update_transform()
        return clone._rescale()


def scalePow(*args) -> PowScale:
    scale = PowScale()._rescale()
    return _init_range_domain(scale, args)


def scaleSqrt(*args) -> PowScale:
    return scalePow(*args).exponent(0.5)


# -- log ---------------------------------------------------------

class LogScale(ContinuousScale):
    def __init__(self, *a, **k):
        self._base = 10.0
        super().__init__(math.log, math.exp)
        self._domain = [1.0, 10.0]
        self._set_base_transform()
        self._rescale()

    def _set_base_transform(self):
        b = self._base
        if b == math.e:
            self._transform, self._untransform = math.log, math.exp
        elif b == 10:
            self._transform = math.log10
            self._untransform = lambda x: 10 ** x
        elif b == 2:
            self._transform = math.log2
            self._untransform = lambda x: 2 ** x
        else:
            lb = math.log(b)
            self._transform = lambda x: math.log(x) / lb
            self._untransform = lambda x: b ** x
        # handle negative domains by reflecting
        if self._domain and self._domain[0] < 0:
            t, u = self._transform, self._untransform
            self._transform = lambda x: -t(-x)
            self._untransform = lambda x: -u(-x)
        self._output = self._input = None

    def base(self, value: float | None = None):
        if value is None:
            return self._base
        self._base = float(value)
        self._set_base_transform()
        return self._rescale()

    def domain(self, values=None):
        result = super().domain(values)
        if values is not None:
            self._set_base_transform()
            self._rescale()
        return result

    def _logs(self, x: float) -> float:
        return math.log(abs(x)) / math.log(self._base)

    def _pows(self, x: float) -> float:
        return self._base ** x

    def ticks(self, count: int | None = None) -> list:
        d = self._domain
        u, v = d[0], d[-1]
        reverse = v < u
        if reverse:
            u, v = v, u
        n = 10 if count is None else int(count)
        i = self._logs(u)
        j = self._logs(v)
        base = self._base
        out: list = []
        if not (base % 1) and (j - i) < n:
            i, j = math.floor(i), math.ceil(j)
            if u > 0:
                ii = i
                while ii <= j:
                    for k in range(1, int(base)):
                        t = k / self._pows(-ii) if ii < 0 else k * self._pows(ii)
                        if t < u:
                            continue
                        if t > v:
                            break
                        out.append(t)
                    ii += 1
            else:
                ii = i
                while ii <= j:
                    for k in range(int(base) - 1, 0, -1):
                        t = k / self._pows(-ii) if ii > 0 else k * self._pows(ii)
                        if -t < u:
                            continue
                        if -t > v:
                            break
                        out.append(-t)
                    ii += 1
            if len(out) * 2 < n:
                out = ticks(u, v, n)
        else:
            out = [self._pows(x) for x in ticks(i, j, min(int(j - i), n))]
        if reverse:
            out.reverse()
        return out

    def tickFormat(self, count: int | None = None, specifier: Any = None):
        from domonic.d3.format import format as d3_format

        if specifier is None:
            specifier = "s" if self._base == 10 else ","
        if not callable(specifier):
            fmt = d3_format(specifier)  # type: ignore[misc]
        else:
            fmt = specifier
        if count is None:
            return fmt
        k = max(1, self._base * (count / len(self.ticks())) if self.ticks() else 1)

        def f(d):
            e = d / self._untransform(round(self._transform(d)))
            if e * self._base < self._base - 0.5:
                e *= self._base
            return fmt(d) if e <= k else ""

        return f

    def nice(self, count: int | None = None):
        d = self._domain
        lo = self._untransform(math.floor(self._transform(d[0])))
        hi = self._untransform(math.ceil(self._transform(d[-1])))
        self._domain = [lo] + list(d[1:-1]) + [hi] if len(d) > 2 else [lo, hi]
        self._set_base_transform()
        return self._rescale()


def scaleLog(*args) -> LogScale:
    scale = LogScale()
    scale = _init_range_domain(scale, args)
    return scale


# -- symlog ----------------------------------------------------

class SymlogScale(LinearishScale):
    def __init__(self, *a, **k):
        self._C = 1.0
        super().__init__()
        self._update_transform()
        self._rescale()

    def _update_transform(self):
        c = self._C
        self._transform = lambda x: math.copysign(math.log1p(abs(x / c)), x)
        self._untransform = lambda x: math.copysign(math.expm1(abs(x)) * c, x)
        self._output = self._input = None

    def constant(self, value: float | None = None):
        if value is None:
            return self._C
        self._C = float(value)
        self._update_transform()
        return self._rescale()


def scaleSymlog(*args) -> SymlogScale:
    scale = SymlogScale()
    return _init_range_domain(scale, args)


# -- quantize -------------------------------------------------

class QuantizeScale:
    def __init__(self):
        self._x0 = 0.0
        self._x1 = 1.0
        self._range: list = [0, 1]
        self._unknown: Any = None
        self._rescale()

    def _rescale(self):
        n = len(self._range) - 1
        self._thresholds = [
            self._x0 + (i + 1) * (self._x1 - self._x0) / (n + 1) for i in range(n)
        ]
        return self

    def __call__(self, x: Any) -> Any:
        try:
            xf = float(x)
        except (TypeError, ValueError):
            return self._unknown
        if xf != xf:
            return self._unknown
        return self._range[bisect(self._thresholds, xf)]

    def invertExtent(self, y: Any) -> list:
        i = self._range.index(y) if y in self._range else -1
        t = self._thresholds
        if i < 0:
            return [math.nan, math.nan]
        lo = t[i - 1] if i > 0 else self._x0
        hi = t[i] if i < len(t) else self._x1
        return [lo, hi]

    def domain(self, values: Sequence | None = None):
        if values is None:
            return [self._x0, self._x1]
        self._x0, self._x1 = float(values[0]), float(values[1])
        return self._rescale()

    def range(self, values: Sequence | None = None):
        if values is None:
            return list(self._range)
        self._range = list(values)
        return self._rescale()

    def thresholds(self) -> list:
        return list(self._thresholds)

    def ticks(self, count: int | None = None) -> list:
        return ticks(self._x0, self._x1, 10 if count is None else count)

    def tickFormat(self, count: int | None = None, specifier: Any = None):
        return tickFormat(self._x0, self._x1, 10 if count is None else count, specifier)

    def nice(self, count: int | None = None):
        d = LinearishScale().domain([self._x0, self._x1]).nice(count).domain()
        return self.domain(d)

    def unknown(self, value: Any = _identity):
        if value is _identity:
            return self._unknown
        self._unknown = value
        return self

    def copy(self):
        clone = QuantizeScale()
        clone._x0, clone._x1 = self._x0, self._x1
        clone._range = list(self._range)
        clone._unknown = self._unknown
        return clone._rescale()


def scaleQuantize(*args) -> QuantizeScale:
    scale = QuantizeScale()
    return _init_range_domain(scale, args)


# -- quantile -------------------------------------------------

class QuantileScale:
    def __init__(self):
        self._domain: list = []
        self._range: list = []
        self._thresholds: list = []
        self._unknown: Any = None

    def _rescale(self):
        n = max(1, len(self._range))
        self._thresholds = [
            quantileSorted(self._domain, (i + 1) / n) for i in range(n - 1)
        ] if self._domain else []
        return self

    def __call__(self, x: Any) -> Any:
        try:
            xf = float(x)
        except (TypeError, ValueError):
            return self._unknown
        if xf != xf:
            return self._unknown
        return self._range[bisect(self._thresholds, xf)]

    def invertExtent(self, y: Any) -> list:
        i = self._range.index(y) if y in self._range else -1
        if i < 0:
            return [math.nan, math.nan]
        lo = self._thresholds[i - 1] if i > 0 else self._domain[0]
        hi = self._thresholds[i] if i < len(self._thresholds) else self._domain[-1]
        return [lo, hi]

    def domain(self, values: Sequence | None = None):
        if values is None:
            return list(self._domain)
        self._domain = sorted(
            float(v) for v in values if v is not None and float(v) == float(v)
        )
        return self._rescale()

    def range(self, values: Sequence | None = None):
        if values is None:
            return list(self._range)
        self._range = list(values)
        return self._rescale()

    def quantiles(self) -> list:
        return list(self._thresholds)

    def unknown(self, value: Any = _identity):
        if value is _identity:
            return self._unknown
        self._unknown = value
        return self

    def copy(self):
        clone = QuantileScale()
        clone._domain = list(self._domain)
        clone._range = list(self._range)
        clone._unknown = self._unknown
        return clone._rescale()


def scaleQuantile(*args) -> QuantileScale:
    scale = QuantileScale()
    return _init_range_domain(scale, args)


# -- threshold -----------------------------------------------

class ThresholdScale:
    def __init__(self):
        self._domain: list = [0.5]
        self._range: list = [0, 1]
        self._unknown: Any = None

    def __call__(self, x: Any) -> Any:
        try:
            xf = float(x)
        except (TypeError, ValueError):
            return self._unknown
        if xf != xf:
            return self._unknown
        return self._range[bisect(self._domain, xf, 0, len(self._range) - 1)]

    def invertExtent(self, y: Any) -> list:
        i = self._range.index(y) if y in self._range else -1
        return [
            self._domain[i - 1] if 0 < i < len(self._domain) + 1 and i - 1 >= 0 else math.nan,
            self._domain[i] if i < len(self._domain) else math.nan,
        ]

    def domain(self, values: Sequence | None = None):
        if values is None:
            return list(self._domain)
        self._domain = list(values)
        return self

    def range(self, values: Sequence | None = None):
        if values is None:
            return list(self._range)
        self._range = list(values)
        return self

    def unknown(self, value: Any = _identity):
        if value is _identity:
            return self._unknown
        self._unknown = value
        return self

    def copy(self):
        clone = ThresholdScale()
        clone._domain = list(self._domain)
        clone._range = list(self._range)
        clone._unknown = self._unknown
        return clone


def scaleThreshold(*args) -> ThresholdScale:
    scale = ThresholdScale()
    return _init_range_domain(scale, args)


# -- ordinal / band / point ---------------------------------

scaleImplicit = "__implicit__"


class OrdinalScale:
    def __init__(self):
        self._domain: list = []
        self._index: dict = {}
        self._range: list = []
        self._unknown: Any = scaleImplicit

    def __call__(self, x: Any) -> Any:
        key = x
        if key not in self._index:
            if self._unknown is not scaleImplicit:
                return self._unknown
            self._index[key] = len(self._domain)
            self._domain.append(key)
        i = self._index[key]
        return self._range[i % len(self._range)] if self._range else self._unknown

    def domain(self, values: Sequence | None = None):
        if values is None:
            return list(self._domain)
        self._domain = []
        self._index = {}
        for v in values:
            if v not in self._index:
                self._index[v] = len(self._domain)
                self._domain.append(v)
        return self

    def range(self, values: Sequence | None = None):
        if values is None:
            return list(self._range)
        self._range = list(values)
        return self

    def unknown(self, value: Any = _identity):
        if value is _identity:
            return self._unknown
        self._unknown = value
        return self

    def copy(self):
        clone = OrdinalScale()
        clone.domain(self._domain)
        clone._range = list(self._range)
        clone._unknown = self._unknown
        return clone


def scaleOrdinal(*args) -> OrdinalScale:
    scale = OrdinalScale()
    return _init_range_domain(scale, args)


class BandScale:
    def __init__(self):
        self._domain: list = []
        self._index: dict = {}
        self._ordinal_range: list = []
        self._r0 = 0.0
        self._r1 = 1.0
        self._round = False
        self._padding_inner = 0.0
        self._padding_outer = 0.0
        self._align = 0.5
        self._step = 0.0
        self._bandwidth = 0.0
        self._unknown: Any = None
        self._rescale()

    def _rescale(self):
        n = len(self._domain)
        if not n:
            return self
        reverse = self._r1 < self._r0
        start, stop = (self._r1, self._r0) if reverse else (self._r0, self._r1)
        step = (stop - start) / max(
            1, n - self._padding_inner + self._padding_outer * 2
        )
        if self._round:
            step = math.floor(step)
        start += (
            stop - start - step * (n - self._padding_inner)
        ) * self._align
        bandwidth = step * (1 - self._padding_inner)
        if self._round:
            start = round(start)
            bandwidth = round(bandwidth)
        values = [start + step * i for i in range(n)]
        if reverse:
            values.reverse()
        self._step = step
        self._bandwidth = bandwidth
        self._ordinal_range = values
        return self

    def __call__(self, x: Any) -> Any:
        i = self._index.get(x)
        return self._ordinal_range[i] if i is not None else self._unknown

    def domain(self, values: Sequence | None = None):
        if values is None:
            return list(self._domain)
        self._domain = []
        self._index = {}
        for v in values:
            if v not in self._index:
                self._index[v] = len(self._domain)
                self._domain.append(v)
        return self._rescale()

    def range(self, values: Sequence | None = None):
        if values is None:
            return [self._r0, self._r1]
        self._r0, self._r1 = float(values[0]), float(values[1])
        return self._rescale()

    def rangeRound(self, values: Sequence):
        self._r0, self._r1 = float(values[0]), float(values[1])
        self._round = True
        return self._rescale()

    def bandwidth(self) -> float:
        return self._bandwidth

    def step(self) -> float:
        return self._step

    def round(self, value: bool | None = None):
        if value is None:
            return self._round
        self._round = bool(value)
        return self._rescale()

    def padding(self, value: float | None = None):
        if value is None:
            return self._padding_inner
        self._padding_inner = min(1.0, float(value))
        self._padding_outer = self._padding_inner
        return self._rescale()

    def paddingInner(self, value: float | None = None):
        if value is None:
            return self._padding_inner
        self._padding_inner = min(1.0, float(value))
        return self._rescale()

    def paddingOuter(self, value: float | None = None):
        if value is None:
            return self._padding_outer
        self._padding_outer = float(value)
        return self._rescale()

    def align(self, value: float | None = None):
        if value is None:
            return self._align
        self._align = max(0.0, min(1.0, float(value)))
        return self._rescale()

    def copy(self):
        clone = BandScale()
        clone.domain(self._domain)
        clone._r0, clone._r1 = self._r0, self._r1
        clone._round = self._round
        clone._padding_inner = self._padding_inner
        clone._padding_outer = self._padding_outer
        clone._align = self._align
        return clone._rescale()


def scaleBand(*args) -> BandScale:
    scale = BandScale()
    return _init_range_domain(scale, args)


class PointScale:
    def __init__(self):
        self._band = BandScale().paddingInner(1.0)

    def __call__(self, x: Any) -> Any:
        return self._band(x)

    def __getattr__(self, name):
        return getattr(self._band, name)

    def domain(self, values=None):
        result = self._band.domain(values)
        return self if values is not None else result

    def range(self, values=None):
        result = self._band.range(values)
        return self if values is not None else result

    def padding(self, value=None):
        if value is None:
            return self._band.paddingOuter()
        self._band.paddingOuter(value)
        return self

    def copy(self):
        clone = PointScale()
        clone._band = self._band.copy()
        return clone


def scalePoint(*args) -> PointScale:
    scale = PointScale()
    if len(args) == 1:
        scale.range(args[0])
    elif len(args) >= 2:
        scale.domain(args[0]).range(args[1])
    return scale


# -- sequential / diverging -------------------------------

class SequentialScale:
    def __init__(self, interpolator: Callable[[float], Any] = _identity):
        self._x0 = 0.0
        self._x1 = 1.0
        self._interpolator = interpolator
        self._clamp = False
        self._unknown: Any = None

    def __call__(self, x: Any) -> Any:
        try:
            xf = float(x)
        except (TypeError, ValueError):
            return self._unknown
        if xf != xf:
            return self._unknown
        t = (xf - self._x0) / (self._x1 - self._x0) if self._x1 != self._x0 else 0.5
        if self._clamp:
            t = max(0.0, min(1.0, t))
        return self._interpolator(t)

    def domain(self, values: Sequence | None = None):
        if values is None:
            return [self._x0, self._x1]
        self._x0, self._x1 = float(values[0]), float(values[1])
        return self

    def clamp(self, value: bool | None = None):
        if value is None:
            return self._clamp
        self._clamp = bool(value)
        return self

    def interpolator(self, fn: Callable | None = None):
        if fn is None:
            return self._interpolator
        self._interpolator = fn
        return self

    def range(self, values: Sequence | None = None):
        if values is None:
            r0, r1 = self._interpolator(0), self._interpolator(1)
            return [r0, r1]
        r0, r1 = values[0], values[1]
        self._interpolator = interpolateValue(r0, r1)
        return self

    def rangeRound(self, values: Sequence):
        self._interpolator = interpolateRound(values[0], values[1])
        return self

    def ticks(self, count: int | None = None) -> list:
        return ticks(self._x0, self._x1, 10 if count is None else count)

    def tickFormat(self, count: int | None = None, specifier: Any = None):
        return tickFormat(self._x0, self._x1, 10 if count is None else count, specifier)

    def nice(self, count: int | None = None):
        d = LinearishScale().domain([self._x0, self._x1]).nice(count).domain()
        self._x0, self._x1 = d[0], d[-1]
        return self

    def copy(self):
        clone = SequentialScale(self._interpolator)
        clone._x0, clone._x1 = self._x0, self._x1
        clone._clamp = self._clamp
        clone._unknown = self._unknown
        return clone


def scaleSequential(*args) -> SequentialScale:
    interpolator = _identity
    domain = None
    for arg in args:
        if callable(arg):
            interpolator = arg
        elif isinstance(arg, (list, tuple)):
            domain = arg
    scale = SequentialScale(interpolator)
    if domain is not None:
        scale.domain(domain)
    return scale


class DivergingScale:
    def __init__(self, interpolator: Callable[[float], Any] = _identity):
        self._x0 = 0.0
        self._x1 = 0.5
        self._x2 = 1.0
        self._interpolator = interpolator
        self._clamp = False
        self._unknown: Any = None

    def __call__(self, x: Any) -> Any:
        try:
            xf = float(x)
        except (TypeError, ValueError):
            return self._unknown
        if xf != xf:
            return self._unknown
        if xf < self._x1:
            t = 0.5 * (
                (xf - self._x0) / (self._x1 - self._x0) if self._x1 != self._x0 else 0
            )
        else:
            t = 0.5 + 0.5 * (
                (xf - self._x1) / (self._x2 - self._x1) if self._x2 != self._x1 else 0
            )
        if self._clamp:
            t = max(0.0, min(1.0, t))
        return self._interpolator(t)

    def domain(self, values: Sequence | None = None):
        if values is None:
            return [self._x0, self._x1, self._x2]
        self._x0, self._x1, self._x2 = (float(v) for v in values[:3])
        return self

    def clamp(self, value: bool | None = None):
        if value is None:
            return self._clamp
        self._clamp = bool(value)
        return self

    def interpolator(self, fn: Callable | None = None):
        if fn is None:
            return self._interpolator
        self._interpolator = fn
        return self

    def copy(self):
        clone = DivergingScale(self._interpolator)
        clone._x0, clone._x1, clone._x2 = self._x0, self._x1, self._x2
        clone._clamp = self._clamp
        return clone


def scaleDiverging(*args) -> DivergingScale:
    interpolator = _identity
    domain = None
    for arg in args:
        if callable(arg):
            interpolator = arg
        elif isinstance(arg, (list, tuple)):
            domain = arg
    scale = DivergingScale(interpolator)
    if domain is not None:
        scale.domain(domain)
    return scale


# -- time ---------------------------------------------------------

def _multiscale_time_format(date) -> str:
    """A compact d3-style multi-scale date format via ``strftime``."""
    from domonic.d3.time import (
        timeSecond as _tS, timeMinute as _tMi, timeHour as _tH,
        timeDay as _tD, timeWeek as _tW, timeMonth as _tMo, timeYear as _tY,
    )

    if _tS(date) < date:
        return date.strftime(".%f")[:4]
    if _tMi(date) < date:
        return date.strftime(":%S")
    if _tH(date) < date:
        return date.strftime("%H:%M")
    if _tD(date) < date:
        return date.strftime("%H:%M")
    if _tMo(date) < date:
        if _tW(date) < date:
            return date.strftime("%a %d")
        return date.strftime("%b %d")
    if _tY(date) < date:
        return date.strftime("%B")
    return date.strftime("%Y")


class TimeScale(LinearishScale):
    """Continuous scale with a temporal domain (``datetime`` endpoints)."""

    _utc = False

    def _to_number(self, x):
        return x.timestamp() if isinstance(x, datetime) else float(x)

    def _to_date(self, n):
        return datetime.fromtimestamp(n)

    def domain(self, values=None):
        if values is None:
            return [self._to_date(d) for d in self._domain]
        self._domain = [self._to_number(v) for v in values]
        return self._rescale()

    def __call__(self, x):
        return super().__call__(self._to_number(x))

    def invert(self, y):
        return self._to_date(super().invert(y))

    def ticks(self, count: int | None = None):
        from domonic.d3.time import timeTicks as _tt, utcTicks as _ut

        d = self.domain()
        fn = _ut if self._utc else _tt
        return fn(d[0], d[-1], 10 if count is None else count)

    def tickFormat(self, count=None, specifier=None):
        if specifier is not None:
            def strf(date):
                return date.strftime(specifier)
            return strf
        return _multiscale_time_format

    def nice(self, count: int | None = None):
        from domonic.d3.time import (
            timeTickInterval as _tti, utcTickInterval as _uti,
        )

        d = self.domain()
        interval: Any = count
        if not hasattr(interval, "range"):
            interval = (_uti if self._utc else _tti)(
                d[0], d[-1], 10 if count is None else count
            )
        if interval is not None:
            self.domain([interval.floor(d[0]), interval.ceil(d[-1])])
        return self

    def copy(self):
        clone = type(self)()
        clone._domain = list(self._domain)
        clone._range = list(self._range)
        clone._interpolate = self._interpolate
        clone._clamp = self._clamp
        clone._unknown = self._unknown
        return clone._rescale()


class UtcScale(TimeScale):
    _utc = True


def scaleTime(*args) -> TimeScale:
    scale = TimeScale()._rescale()
    scale._domain = _DEFAULT_TIME_DOMAIN()
    return _init_range_domain(scale, args)


def scaleUtc(*args) -> UtcScale:
    scale = UtcScale()._rescale()
    scale._domain = _DEFAULT_TIME_DOMAIN()
    return _init_range_domain(scale, args)


def _DEFAULT_TIME_DOMAIN() -> list:
    return [
        datetime(2000, 1, 1).timestamp(),
        datetime(2000, 1, 2).timestamp(),
    ]


# -- tick format ---------------------------------------------

def tickFormat(start: float, stop: float, count: int, specifier: Any = None):
    """Return a function that formats a tick value.

    With no specifier the precision is derived from the tick step (``d3``'s
    default behaviour). A non-empty specifier is passed straight to
    :func:`domonic.d3.format.format`.
    """
    from domonic.d3.array import tickStep

    if callable(specifier):
        return specifier
    if specifier:
        try:
            from domonic.d3.format import format as d3_format

            return d3_format(str(specifier))  # type: ignore[misc]
        except Exception:
            pass

    step = abs(tickStep(start, stop, count if count else 10))
    if not step or not math.isfinite(step):
        precision = 0
    else:
        precision = max(0, -math.floor(math.log10(step) + 1e-12))

    def fmt(x: Any) -> str:
        try:
            value = float(x)
        except (TypeError, ValueError):
            return str(x)
        return f"{value:,.{precision}f}"

    return fmt
