"""
domonic.d3.interpolate
====================================

A port of `d3-interpolate <https://github.com/d3/d3-interpolate>`_ (v3).

Every ``interpolateX(a, b)`` returns a function of ``t`` in ``[0, 1]``. The
generic :func:`interpolate` dispatches on the type of ``b``: ``None`` / bool
-> constant, number -> :func:`interpolateNumber`, colour string ->
:func:`interpolateRgb`, ``str`` -> :func:`interpolateString`, list ->
:func:`interpolateArray`, mapping -> :func:`interpolateObject`.
"""

from __future__ import annotations

import math
import re
from datetime import datetime
from typing import Any, Callable, Sequence

from domonic.d3.color import (
    Color,
    Cubehelix,
    Hcl,
    Hsl,
    Lab,
    Rgb,
)
from domonic.d3.color import color as _parse_color
from domonic.d3.color import cubehelix as _cubehelix
from domonic.d3.color import hcl as _hcl
from domonic.d3.color import hsl as _hsl
from domonic.d3.color import lab as _lab
from domonic.d3.color import rgb as _rgb

__all__ = [
    "interpolate", "interpolateNumber", "interpolateRound", "interpolateString",
    "interpolateArray", "interpolateNumberArray", "interpolateObject",
    "interpolateDate", "interpolateBasis", "interpolateBasisClosed",
    "interpolateRgb", "interpolateRgbBasis", "interpolateRgbBasisClosed",
    "interpolateHsl", "interpolateHslLong", "interpolateLab", "interpolateHcl",
    "interpolateHclLong", "interpolateCubehelix", "interpolateCubehelixLong",
    "interpolateHue", "interpolateDiscrete", "piecewise", "quantize",
    "interpolateZoom",
]


def _constant(x: Any) -> Callable[[float], Any]:
    return lambda t: x


# -- number / round / date -------------------------------------------

def interpolateNumber(a: float, b: float) -> Callable[[float], float]:
    a = float(a)
    b = float(b) - a
    return lambda t: a + b * t


def interpolateRound(a: float, b: float) -> Callable[[float], float]:
    a = float(a)
    b = float(b) - a
    return lambda t: round(a + b * t)


def interpolateDate(a: datetime, b: datetime) -> Callable[[float], datetime]:
    ta = a.timestamp()
    tb = b.timestamp()
    return lambda t: datetime.fromtimestamp(ta * (1 - t) + tb * t)


# -- string ---------------------------------------------------------

_RE_NUM = re.compile(
    r"[-+]?(?:\d+\.?\d*|\.?\d+)(?:[eE][-+]?\d+)?"
)


def interpolateString(a: Any, b: Any) -> Callable[[float], str]:
    a, b = str(a), str(b)
    a_numbers = _RE_NUM.finditer(a)
    b_numbers = _RE_NUM.finditer(b)
    parts: list[Any] = []  # string constants and None placeholders
    interps: list[tuple[int, Callable[[float], float]]] = []
    bi = 0

    def append_string(text: str) -> None:
        if parts and isinstance(parts[-1], str):
            parts[-1] += text
        else:
            parts.append(text)

    for am, bm in zip(a_numbers, b_numbers):
        if bm.start() > bi:
            append_string(b[bi:bm.start()])
        an_text, bn_text = am.group(), bm.group()
        if an_text == bn_text:
            append_string(bn_text)
        else:
            parts.append(None)
            interps.append((len(parts) - 1, interpolateNumber(float(an_text), float(bn_text))))
        bi = bm.end()

    if bi < len(b):
        append_string(b[bi:])

    if not interps:
        return _constant(b)
    if len(parts) == 1:
        fn = interps[0][1]
        return lambda t: _format_number(fn(t))

    def interpolate(t: float) -> str:
        rendered = list(parts)
        for idx, fn in interps:
            rendered[idx] = _format_number(fn(t))
        return "".join(rendered)

    return interpolate


def _format_number(x: float) -> str:
    if x == int(x):
        return str(int(x))
    return repr(x)


# -- array / object -----------------------------------------------

def interpolateNumberArray(a: Sequence, b: Sequence) -> Callable[[float], list]:
    n = min(len(a), len(b)) if a is not None else 0
    a = list(a) if a is not None else []
    b = list(b)

    def interpolate(t: float) -> list:
        out = list(b)
        for i in range(n):
            out[i] = a[i] * (1 - t) + b[i] * t
        return out

    return interpolate


def interpolateArray(a: Sequence, b: Sequence) -> Callable[[float], list]:
    if a is not None and _is_number_array(b):
        return interpolateNumberArray(a, b)
    b_list = list(b)
    a_list = list(a) if a is not None else []
    na = min(len(a_list), len(b_list))
    interps: list[Callable[[float], Any]] = [
        interpolate(a_list[i], b_list[i]) for i in range(na)
    ]

    def interp(t: float) -> list:
        out = list(b_list)
        for i in range(na):
            out[i] = interps[i](t)
        return out

    return interp


def _is_number_array(values: Any) -> bool:
    try:
        return len(values) > 0 and all(
            isinstance(v, (int, float)) and not isinstance(v, bool) for v in values
        )
    except TypeError:
        return False


def interpolateObject(a: Any, b: Any) -> Callable[[float], dict]:
    a = a if isinstance(a, dict) else {}
    b = dict(b)
    interps = {k: interpolate(a.get(k), b[k]) for k in b}

    def interp(t: float) -> dict:
        return {k: fn(t) for k, fn in interps.items()}

    return interp


# -- basis (B-spline) -------------------------------------------------

def _basis(t1: float, v0: float, v1: float, v2: float, v3: float) -> float:
    t2 = t1 * t1
    t3 = t2 * t1
    return (
        (1 - 3 * t1 + 3 * t2 - t3) * v0
        + (4 - 6 * t2 + 3 * t3) * v1
        + (1 + 3 * t1 + 3 * t2 - 3 * t3) * v2
        + t3 * v3
    ) / 6


def interpolateBasis(values: Sequence[float]) -> Callable[[float], float]:
    values = [float(v) for v in values]
    n = len(values) - 1

    def interpolate(t: float) -> float:
        i = 0 if t <= 0 else (n - 1 if t >= 1 else int(math.floor(t * n)))
        v1 = values[i]
        v2 = values[i + 1]
        v0 = values[i - 1] if i > 0 else 2 * v1 - v2
        v3 = values[i + 2] if i < n - 1 else 2 * v2 - v1
        return _basis((t - i / n) * n, v0, v1, v2, v3)

    return interpolate


def interpolateBasisClosed(values: Sequence[float]) -> Callable[[float], float]:
    values = [float(v) for v in values]
    n = len(values)

    def interpolate(t: float) -> float:
        i = int(math.floor(((t % 1) + 1) % 1 * n))
        v0 = values[(i + n - 1) % n]
        v1 = values[i % n]
        v2 = values[(i + 1) % n]
        v3 = values[(i + 2) % n]
        return _basis((t - i / n) * n, v0, v1, v2, v3)

    return interpolate


# -- colour ---------------------------------------------------------

def _nogamma(a: float, b: float) -> Callable[[float], float]:
    if a != a:  # NaN start -> hold at b
        return _constant(b)
    d = b - a
    return lambda t: a + t * d


def _hue(a: float, b: float) -> Callable[[float], float]:
    d = b - a
    if d:
        if d > 180 or d < -180:
            d -= 360 * round(d / 360)
        return lambda t: a + t * d
    return _constant(b if b == b else a)


def interpolateRgb(
    a: Any, b: Any, gamma: float = 1.0
) -> Callable[[float], str]:
    ca = _rgb(a)
    cb = _rgb(b)

    def channel(x: float, y: float) -> Callable[[float], float]:
        if x != x:
            return _constant(y)
        d = y - x
        if gamma == 1:
            return lambda t: x + t * d
        yg, xg = y ** gamma, x ** gamma
        dg = yg - xg
        return lambda t: (xg + t * dg) ** (1 / gamma)

    r = channel(ca.r, cb.r)
    g = channel(ca.g, cb.g)
    bl = channel(ca.b, cb.b)
    op = _nogamma(ca.opacity, cb.opacity)

    def interpolate(t: float) -> str:
        c = Rgb(r(t), g(t), bl(t), op(t))
        return c.formatRgb()

    return interpolate


def _rgb_basis(colors: Sequence, closed: bool) -> Callable[[float], str]:
    parsed = [_rgb(c) for c in colors]
    basis = interpolateBasisClosed if closed else interpolateBasis
    r = basis([c.r for c in parsed])
    g = basis([c.g for c in parsed])
    b = basis([c.b for c in parsed])

    def interpolate(t: float) -> str:
        return Rgb(r(t), g(t), b(t), 1).formatRgb()

    return interpolate


def interpolateRgbBasis(colors: Sequence) -> Callable[[float], str]:
    return _rgb_basis(colors, False)


def interpolateRgbBasisClosed(colors: Sequence) -> Callable[[float], str]:
    return _rgb_basis(colors, True)


def _color_space_interpolator(convert, hue_channel, long: bool):
    def make(a: Any, b: Any) -> Callable[[float], str]:
        ca = convert(a)
        cb = convert(b)
        channels = []
        for name in getattr(ca, "_channels", ()):
            va = getattr(ca, name)
            vb = getattr(cb, name)
            if name == hue_channel and not long:
                channels.append((name, _hue(va, vb)))
            else:
                channels.append((name, _nogamma(va, vb)))
        op = _nogamma(ca.opacity, cb.opacity)

        def interpolate(t: float) -> str:
            values = {name: fn(t) for name, fn in channels}
            c = ca.copy(**values, opacity=op(t))
            return c.rgb().formatRgb()

        return interpolate

    return make


interpolateHsl = _color_space_interpolator(_hsl, "h", False)
interpolateHslLong = _color_space_interpolator(_hsl, "h", True)
interpolateLab = _color_space_interpolator(_lab, None, False)
interpolateHcl = _color_space_interpolator(_hcl, "h", False)
interpolateHclLong = _color_space_interpolator(_hcl, "h", True)


def _cubehelix_factory(long: bool):
    def gamma(y: float = 1.0):
        y = float(y)

        def make(a: Any, b: Any) -> Callable[[float], str]:
            ca = _cubehelix(a)
            cb = _cubehelix(b)
            h = (_nogamma if long else _hue)(ca.h, cb.h)
            s = _nogamma(ca.s, cb.s)
            light = _nogamma(ca.l, cb.l)
            op = _nogamma(ca.opacity, cb.opacity)

            def interpolate(t: float) -> str:
                c = Cubehelix(h(t), s(t), light(t ** y), op(t))
                return c.rgb().formatRgb()

            return interpolate

        make.gamma = gamma  # type: ignore[attr-defined]
        return make

    return gamma(1.0)


interpolateCubehelix = _cubehelix_factory(False)
interpolateCubehelixLong = _cubehelix_factory(True)


def interpolateHue(a: float, b: float) -> Callable[[float], float]:
    i = _hue(float(a), float(b))
    return lambda t: _clamp_hue(i(t))


def _clamp_hue(h: float) -> float:
    return h - 360 * math.floor(h / 360)


# -- generic dispatch --------------------------------------------------

def interpolate(a: Any, b: Any) -> Callable[[float], Any]:
    if b is None or isinstance(b, bool):
        return _constant(b)
    if isinstance(b, (int, float)):
        return interpolateNumber(a if isinstance(a, (int, float)) else 0, b)
    if isinstance(b, datetime):
        return interpolateDate(a, b)
    if isinstance(b, str):
        parsed = _parse_color(b)
        if parsed is not None:
            return interpolateRgb(a, b)
        return interpolateString(a, b)
    if isinstance(b, Color):
        return interpolateRgb(a, b)
    if isinstance(b, (list, tuple)):
        return interpolateArray(a, b)
    if hasattr(b, "keys") or isinstance(b, dict):
        return interpolateObject(a, b)
    return interpolateNumber(a, b)


# -- piecewise / quantize / discrete ---------------------------------

def piecewise(*args: Any) -> Callable[[float], Any]:
    if len(args) == 1:
        interpolator_fn = interpolate
        values = list(args[0])
    else:
        interpolator_fn = args[0]
        values = list(args[1])
    n = len(values) - 1
    interpolators = [interpolator_fn(values[i], values[i + 1]) for i in range(n)]

    def scale(t: float) -> Any:
        i = 0 if t <= 0 else (n - 1 if t >= 1 else int(math.floor(t * n)))
        return interpolators[i](t * n - i)

    return scale


def quantize(interpolator: Callable[[float], Any], n: int) -> list:
    return [interpolator(i / (n - 1)) for i in range(n)] if n > 1 else [interpolator(0)]


def interpolateDiscrete(values: Sequence) -> Callable[[float], Any]:
    values = list(values)
    n = len(values)

    def interpolate(t: float) -> Any:
        idx = int(math.floor(t * n))
        return values[max(0, min(n - 1, idx))]

    return interpolate


# -- zoom ----------------------------------------------------------

def interpolateZoom(
    p0: Sequence[float], p1: Sequence[float]
) -> Callable[[float], list]:
    rho = 1.4142135623730951
    rho2 = 2.0
    rho4 = 4.0
    epsilon2 = 1e-12

    ux0, uy0, w0 = float(p0[0]), float(p0[1]), float(p0[2])
    ux1, uy1, w1 = float(p1[0]), float(p1[1]), float(p1[2])
    dx = ux1 - ux0
    dy = uy1 - uy0
    d2 = dx * dx + dy * dy

    if d2 < epsilon2:
        S = math.log(w1 / w0) / rho

        def interp(t: float) -> list:
            return [
                ux0 + t * dx,
                uy0 + t * dy,
                w0 * math.exp(rho * t * S),
            ]
    else:
        d1 = math.sqrt(d2)
        b0 = (w1 * w1 - w0 * w0 + rho4 * d2) / (2 * w0 * rho2 * d1)
        b1 = (w1 * w1 - w0 * w0 - rho4 * d2) / (2 * w1 * rho2 * d1)
        r0 = math.log(math.sqrt(b0 * b0 + 1) - b0)
        r1 = math.log(math.sqrt(b1 * b1 + 1) - b1)
        S = (r1 - r0) / rho

        def _cosh(x: float) -> float:
            return (math.exp(x) + math.exp(-x)) / 2

        def _sinh(x: float) -> float:
            return (math.exp(x) - math.exp(-x)) / 2

        def _tanh(x: float) -> float:
            return _sinh(x) / _cosh(x)

        def interp(t: float) -> list:
            s = t * S
            coshr0 = _cosh(r0)
            u = w0 / (rho2 * d1) * (coshr0 * _tanh(rho * s + r0) - _sinh(r0))
            return [
                ux0 + u * dx,
                uy0 + u * dy,
                w0 * coshr0 / _cosh(rho * s + r0),
            ]

    interp.duration = abs(S) * 1000 * rho  # type: ignore[attr-defined]
    return interp
