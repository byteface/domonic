"""
domonic.d3.shape
====================================

A port of `d3-shape <https://github.com/d3/d3-shape>`_ (v3): the ``line``,
``area``, ``arc``, ``pie``, ``symbol``, ``link`` and ``stack`` generators plus
the standard curve factories.

Generators are callable objects; called with no context they return an SVG path
string. The fluent accessors (``x``, ``y``, ``curve`` ...) return the current
value when called with no argument and ``self`` otherwise.
"""

from __future__ import annotations

import math
from typing import Any, Callable, Sequence

from domonic.d3.path import Path

__all__ = [
    "line", "lineRadial", "area", "areaRadial", "arc", "pie", "symbol",
    "symbolCircle", "symbolCross", "symbolDiamond", "symbolSquare",
    "symbolStar", "symbolTriangle", "symbolWye", "symbolsFill", "symbolsStroke",
    "symbols", "pointRadial", "link", "linkHorizontal", "linkVertical",
    "linkRadial", "stack", "curveLinear", "curveLinearClosed", "curveStep",
    "curveStepBefore", "curveStepAfter", "curveBasis", "curveBasisClosed",
    "curveBasisOpen", "curveCardinal", "curveCatmullRom", "curveNatural",
    "curveMonotoneX", "curveMonotoneY", "curveBumpX", "curveBumpY",
    "stackOffsetNone", "stackOffsetExpand", "stackOffsetDiverging",
    "stackOffsetSilhouette", "stackOffsetWiggle", "stackOrderNone",
    "stackOrderAscending", "stackOrderDescending", "stackOrderInsideOut",
    "stackOrderReverse", "stackOrderAppearance",
]

_TAU = math.tau
_PI = math.pi
_HALF_PI = math.pi / 2
_EPSILON = 1e-12


def _constant(x: Any) -> Callable[..., Any]:
    return lambda *_a: x


def _identity(d: Any, *_a: Any) -> Any:
    return d


def _x_of(p: Any, *_a: Any) -> float:
    return p[0]


def _y_of(p: Any, *_a: Any) -> float:
    return p[1]


def pointRadial(angle: float, radius: float) -> list[float]:
    a = angle - _HALF_PI
    return [radius * math.cos(a), radius * math.sin(a)]


# -- curves --------------------------------------------------------

class _Linear:
    def __init__(self, context):
        self._context = context
        self._point = 0
        self._line = 0

    def areaStart(self):
        self._line = 0

    def areaEnd(self):
        self._line = math.nan

    def lineStart(self):
        self._point = 0

    def lineEnd(self):
        if self._line or (self._line != 0 and self._point == 1):
            self._context.closePath()
        self._line = 1 - self._line

    def point(self, x, y):
        x, y = float(x), float(y)
        if self._point == 0:
            self._point = 1
            (self._context.lineTo if self._line else self._context.moveTo)(x, y)
        elif self._point == 1:
            self._point = 2
            self._context.lineTo(x, y)
        else:
            self._context.lineTo(x, y)


def curveLinear(context):
    return _Linear(context)


class _LinearClosed:
    def __init__(self, context):
        self._context = context
        self._point = 0

    def areaStart(self):
        pass

    areaEnd = areaStart

    def lineStart(self):
        self._point = 0

    def lineEnd(self):
        if self._point:
            self._context.closePath()

    def point(self, x, y):
        x, y = float(x), float(y)
        if self._point:
            self._context.lineTo(x, y)
        else:
            self._point = 1
            self._context.moveTo(x, y)


def curveLinearClosed(context):
    return _LinearClosed(context)


class _Step:
    def __init__(self, context, t):
        self._context = context
        self._t = t
        self._line = 0
        self._point = 0
        self._x = self._y = math.nan

    def areaStart(self):
        self._line = 0

    def areaEnd(self):
        self._line = math.nan

    def lineStart(self):
        self._x = self._y = math.nan
        self._point = 0

    def lineEnd(self):
        if 0 < self._t < 1 and self._point == 2:
            self._context.lineTo(self._x, self._y)
        if self._line or (self._line != 0 and self._point == 1):
            self._context.closePath()
        if self._line >= 0:
            self._t = 1 - self._t
            self._line = 1 - self._line

    def point(self, x, y):
        x, y = float(x), float(y)
        if self._point == 0:
            self._point = 1
            (self._context.lineTo if self._line else self._context.moveTo)(x, y)
        elif self._point == 1:
            self._point = 2
        else:
            if self._t <= 0:
                self._context.lineTo(self._x, y)
                self._context.lineTo(x, y)
            else:
                x1 = self._x * (1 - self._t) + x * self._t
                self._context.lineTo(x1, self._y)
                self._context.lineTo(x1, y)
        self._x, self._y = x, y


def curveStep(context):
    return _Step(context, 0.5)


def curveStepBefore(context):
    return _Step(context, 0)


def curveStepAfter(context):
    return _Step(context, 1)


class _Basis:
    def __init__(self, context):
        self._context = context
        self._line = 0

    def areaStart(self):
        self._line = 0

    def areaEnd(self):
        self._line = math.nan

    def lineStart(self):
        self._x0 = self._x1 = self._y0 = self._y1 = math.nan
        self._point = 0

    def lineEnd(self):
        p = self._point
        if p == 3:
            self._curve(self._x1, self._y1)
            self._context.lineTo(self._x1, self._y1)
        elif p == 2:
            self._context.lineTo(self._x1, self._y1)
        if self._line or (self._line != 0 and self._point == 1):
            self._context.closePath()
        self._line = 1 - self._line

    def _curve(self, x, y):
        self._context.bezierCurveTo(
            (2 * self._x0 + self._x1) / 3,
            (2 * self._y0 + self._y1) / 3,
            (self._x0 + 2 * self._x1) / 3,
            (self._y0 + 2 * self._y1) / 3,
            (self._x0 + 4 * self._x1 + x) / 6,
            (self._y0 + 4 * self._y1 + y) / 6,
        )

    def point(self, x, y):
        x, y = float(x), float(y)
        p = self._point
        if p == 0:
            self._point = 1
            (self._context.lineTo if self._line else self._context.moveTo)(x, y)
        elif p == 1:
            self._point = 2
        elif p == 2:
            self._point = 3
            self._context.lineTo(
                (5 * self._x0 + self._x1) / 6, (5 * self._y0 + self._y1) / 6
            )
            self._curve(x, y)
        else:
            self._curve(x, y)
        self._x0, self._x1 = self._x1, x
        self._y0, self._y1 = self._y1, y


def curveBasis(context):
    return _Basis(context)


class _BasisClosed(_Basis):
    def lineStart(self):
        self._x0 = self._x1 = self._x2 = self._x3 = self._x4 = math.nan
        self._y0 = self._y1 = self._y2 = self._y3 = self._y4 = math.nan
        self._point = 0

    def lineEnd(self):
        p = self._point
        if p == 1:
            self._context.moveTo(self._x2, self._y2)
            self._context.closePath()
        elif p == 2:
            self._context.moveTo((self._x2 + 2 * self._x3) / 3, (self._y2 + 2 * self._y3) / 3)
            self._context.lineTo((self._x3 + 2 * self._x2) / 3, (self._y3 + 2 * self._y2) / 3)
            self._context.closePath()
        elif p == 3:
            self.point(self._x2, self._y2)
            self.point(self._x3, self._y3)
            self.point(self._x4, self._y4)

    def point(self, x, y):
        x, y = float(x), float(y)
        p = self._point
        if p == 0:
            self._point = 1
            self._x2, self._y2 = x, y
        elif p == 1:
            self._point = 2
            self._x3, self._y3 = x, y
        elif p == 2:
            self._point = 3
            self._x4, self._y4 = x, y
            self._context.moveTo((self._x0 + 4 * self._x1 + x) / 6,
                                 (self._y0 + 4 * self._y1 + y) / 6)
        else:
            self._curve(x, y)
        self._x0, self._x1 = self._x1, x
        self._y0, self._y1 = self._y1, y


def curveBasisClosed(context):
    return _BasisClosed(context)


class _BasisOpen(_Basis):
    def lineEnd(self):
        if self._line or (self._line != 0 and self._point == 3):
            self._context.closePath()
        self._line = 1 - self._line

    def point(self, x, y):
        x, y = float(x), float(y)
        p = self._point
        if p == 0:
            self._point = 1
        elif p == 1:
            self._point = 2
        elif p == 2:
            self._point = 3
            x0 = (self._x0 + 4 * self._x1 + x) / 6
            y0 = (self._y0 + 4 * self._y1 + y) / 6
            (self._context.lineTo if self._line else self._context.moveTo)(x0, y0)
        elif p == 3:
            self._point = 4
            self._curve(x, y)
        else:
            self._curve(x, y)
        self._x0, self._x1 = self._x1, x
        self._y0, self._y1 = self._y1, y


def curveBasisOpen(context):
    return _BasisOpen(context)


class _Cardinal:
    def __init__(self, context, tension):
        self._context = context
        self._line = 0
        self._k = (1 - tension) / 6

    def areaStart(self):
        self._line = 0

    def areaEnd(self):
        self._line = math.nan

    def lineStart(self):
        self._x0 = self._x1 = self._x2 = math.nan
        self._y0 = self._y1 = self._y2 = math.nan
        self._point = 0

    def lineEnd(self):
        p = self._point
        if p == 2:
            self._context.lineTo(self._x2, self._y2)
        elif p == 3:
            self._pt(self._x2, self._y2)
        if self._line or (self._line != 0 and self._point == 1):
            self._context.closePath()
        self._line = 1 - self._line

    def _pt(self, x, y):
        self._context.bezierCurveTo(
            self._x1 + self._k * (self._x2 - self._x0),
            self._y1 + self._k * (self._y2 - self._y0),
            self._x2 + self._k * (self._x1 - x),
            self._y2 + self._k * (self._y1 - y),
            self._x2, self._y2,
        )

    def point(self, x, y):
        x, y = float(x), float(y)
        p = self._point
        if p == 0:
            self._point = 1
            (self._context.lineTo if self._line else self._context.moveTo)(x, y)
        elif p == 1:
            self._point = 2
            self._x1, self._y1 = x, y
        elif p == 2:
            self._point = 3
            self._pt(x, y)
        else:
            self._pt(x, y)
        self._x0, self._x1, self._x2 = self._x1, self._x2, x
        self._y0, self._y1, self._y2 = self._y1, self._y2, y


def curveCardinal(context):
    return _Cardinal(context, 0)


class _CatmullRom:
    def __init__(self, context, alpha):
        self._context = context
        self._line = 0
        self._alpha = alpha

    def areaStart(self):
        self._line = 0

    def areaEnd(self):
        self._line = math.nan

    def lineStart(self):
        self._x0 = self._x1 = self._x2 = math.nan
        self._y0 = self._y1 = self._y2 = math.nan
        self._l01_a = self._l12_a = self._l23_a = 0.0
        self._l01_2a = self._l12_2a = self._l23_2a = 0.0
        self._point = 0

    def lineEnd(self):
        p = self._point
        if p == 2:
            self._context.lineTo(self._x2, self._y2)
        elif p == 3:
            self.point(self._x2, self._y2)
        if self._line or (self._line != 0 and self._point == 1):
            self._context.closePath()
        self._line = 1 - self._line

    def point(self, x, y):
        x, y = float(x), float(y)
        if self._point:
            x23 = self._x2 - x
            y23 = self._y2 - y
            self._l23_2a = (x23 * x23 + y23 * y23) ** self._alpha
            self._l23_a = math.sqrt(self._l23_2a)
        p = self._point
        if p == 0:
            self._point = 1
            (self._context.lineTo if self._line else self._context.moveTo)(x, y)
        elif p == 1:
            self._point = 2
        elif p == 2:
            self._point = 3
            self._catmull(x, y)
        else:
            self._catmull(x, y)
        self._l01_a, self._l12_a = self._l12_a, self._l23_a
        self._l01_2a, self._l12_2a = self._l12_2a, self._l23_2a
        self._x0, self._x1, self._x2 = self._x1, self._x2, x
        self._y0, self._y1, self._y2 = self._y1, self._y2, y

    def _catmull(self, x, y):
        x1, y1 = self._x1, self._y1
        x2, y2 = self._x2, self._y2
        if self._l01_a > _EPSILON:
            a = 2 * self._l01_2a + 3 * self._l01_a * self._l12_a + self._l12_2a
            n = 3 * self._l01_a * (self._l01_a + self._l12_a)
            x1 = (x1 * a - self._x0 * self._l12_2a + self._x2 * self._l01_2a) / n
            y1 = (y1 * a - self._y0 * self._l12_2a + self._y2 * self._l01_2a) / n
        if self._l23_a > _EPSILON:
            b = 2 * self._l23_2a + 3 * self._l23_a * self._l12_a + self._l12_2a
            m = 3 * self._l23_a * (self._l23_a + self._l12_a)
            x2 = (x2 * b + self._x1 * self._l23_2a - x * self._l12_2a) / m
            y2 = (y2 * b + self._y1 * self._l23_2a - y * self._l12_2a) / m
        self._context.bezierCurveTo(x1, y1, x2, y2, self._x2, self._y2)


def curveCatmullRom(context):
    return _CatmullRom(context, 0.5)


class _Natural:
    def __init__(self, context):
        self._context = context
        self._line = 0
        self._x: list[float] = []
        self._y: list[float] = []

    def areaStart(self):
        self._line = 0

    def areaEnd(self):
        self._line = math.nan

    def lineStart(self):
        self._x = []
        self._y = []
        self._point = 0

    def lineEnd(self):
        xs, ys = self._x, self._y
        n = len(xs)
        if n:
            (self._context.lineTo if self._line else self._context.moveTo)(xs[0], ys[0])
            if n == 2:
                self._context.lineTo(xs[1], ys[1])
            elif n > 2:
                px = _control_points(xs)
                py = _control_points(ys)
                for i0, i1 in enumerate(range(1, n)):
                    self._context.bezierCurveTo(
                        px[0][i0], py[0][i0], px[1][i0], py[1][i0], xs[i1], ys[i1]
                    )
        if self._line or (self._line != 0 and self._point == 1):
            self._context.closePath()
        self._line = 1 - self._line
        self._x = self._y = []

    def point(self, x, y):
        self._x.append(float(x))
        self._y.append(float(y))


def _control_points(x: list[float]):
    n = len(x) - 1
    a = [0.0] * n
    b = [0.0] * n
    r = [0.0] * n
    a[0], b[0], r[0] = 0, 2, x[0] + 2 * x[1]
    for i in range(1, n - 1):
        a[i], b[i], r[i] = 1, 4, 4 * x[i] + 2 * x[i + 1]
    a[n - 1], b[n - 1], r[n - 1] = 2, 7, 8 * x[n - 1] + x[n]
    for i in range(1, n):
        m = a[i] / b[i - 1]
        b[i] -= m
        r[i] -= m * r[i - 1]
    a[n - 1] = r[n - 1] / b[n - 1]
    for i in range(n - 2, -1, -1):
        a[i] = (r[i] - a[i + 1]) / b[i]
    b[n - 1] = (x[n] + a[n - 1]) / 2
    for i in range(n - 1):
        b[i] = 2 * x[i + 1] - a[i + 1]
    return a, b


def curveNatural(context):
    return _Natural(context)


class _Monotone:
    def __init__(self, context):
        self._context = context
        self._line = 0

    def areaStart(self):
        self._line = 0

    def areaEnd(self):
        self._line = math.nan

    def lineStart(self):
        self._x0 = self._x1 = self._y0 = self._y1 = self._t0 = math.nan
        self._point = 0

    def lineEnd(self):
        p = self._point
        if p == 2:
            self._context.lineTo(self._x1, self._y1)
        elif p == 3:
            self._segment(self._t0, self._slope2(self._t0))
        if self._line or (self._line != 0 and self._point == 1):
            self._context.closePath()
        self._line = 1 - self._line

    def _slope3(self, x2, y2):
        h0 = self._x1 - self._x0
        h1 = x2 - self._x1
        s0 = (self._y1 - self._y0) / (h0 or (1 if h1 < 0 else -1) * _EPSILON)
        s1 = (y2 - self._y1) / (h1 or (1 if h0 < 0 else -1) * _EPSILON)
        p = (s0 * h1 + s1 * h0) / (h0 + h1) if (h0 + h1) else 0
        sign = (0 < s0) - (s0 < 0)
        if sign != (0 < s1) - (s1 < 0):
            return 0.0
        return math.copysign(min(abs(s0), abs(s1), 0.5 * abs(p)), s0 + s1 or p or 1)

    def _slope2(self, t):
        h = self._x1 - self._x0
        return (3 * (self._y1 - self._y0) / h - t) / 2 if h else t

    def _segment(self, t0, t1):
        x0, y0 = self._x0, self._y0
        x1, y1 = self._x1, self._y1
        dx = (x1 - x0) / 3
        self._context.bezierCurveTo(
            x0 + dx, y0 + dx * t0, x1 - dx, y1 - dx * t1, x1, y1
        )

    def point(self, x, y):
        x, y = float(x), float(y)
        t1 = math.nan
        if x == self._x1 and y == self._y1:
            return
        p = self._point
        if p == 0:
            self._point = 1
            (self._context.lineTo if self._line else self._context.moveTo)(x, y)
        elif p == 1:
            self._point = 2
        elif p == 2:
            self._point = 3
            self._segment(self._slope2(t1 := self._slope3(x, y)), t1)
        else:
            self._segment(self._t0, t1 := self._slope3(x, y))
        self._x0, self._x1 = self._x1, x
        self._y0, self._y1 = self._y1, y
        self._t0 = t1


class _MonotoneX(_Monotone):
    pass


class _MonotoneY(_Monotone):
    def __init__(self, context):
        super().__init__(_ReflectContext(context))

    def point(self, x, y):
        super().point(y, x)


class _ReflectContext:
    def __init__(self, context):
        self._context = context

    def moveTo(self, x, y):
        self._context.moveTo(y, x)

    def closePath(self):
        self._context.closePath()

    def lineTo(self, x, y):
        self._context.lineTo(y, x)

    def bezierCurveTo(self, x1, y1, x2, y2, x, y):
        self._context.bezierCurveTo(y1, x1, y2, x2, y, x)


def curveMonotoneX(context):
    return _MonotoneX(context)


def curveMonotoneY(context):
    return _MonotoneY(context)


class _Bump:
    def __init__(self, context, x_axis):
        self._context = context
        self._line = 0
        self._x = x_axis

    def areaStart(self):
        self._line = 0

    def areaEnd(self):
        self._line = math.nan

    def lineStart(self):
        self._point = 0

    def lineEnd(self):
        if self._line or (self._line != 0 and self._point == 1):
            self._context.closePath()
        self._line = 1 - self._line

    def point(self, x, y):
        x, y = float(x), float(y)
        if self._point == 0:
            self._point = 1
            (self._context.lineTo if self._line else self._context.moveTo)(x, y)
        else:
            if self._x:
                mid = (self._x0 + x) / 2
                self._context.bezierCurveTo(mid, self._y0, mid, y, x, y)
            else:
                mid = (self._y0 + y) / 2
                self._context.bezierCurveTo(self._x0, mid, x, mid, x, y)
        self._x0, self._y0 = x, y


def curveBumpX(context):
    return _Bump(context, True)


def curveBumpY(context):
    return _Bump(context, False)


# -- line / area --------------------------------------------------

class Line:
    def __init__(self, x=None, y=None):
        self._x = x if callable(x) else _constant(x) if x is not None else _x_of
        self._y = y if callable(y) else _constant(y) if y is not None else _y_of
        self._defined: Callable = _constant(True)
        self._curve = curveLinear
        self._context = None

    def __call__(self, data: Sequence) -> Any:
        data = list(data)
        buffer = None
        if self._context is None:
            buffer = Path()
            output = self._curve(buffer)
        else:
            output = self._curve(self._context)
        defined0 = False
        n = len(data)
        for i in range(n + 1):
            in_range = i < n and bool(self._defined(data[i], i, data)) if i < n else False
            if (not in_range) == defined0:
                defined0 = not defined0
                if defined0:
                    output.lineStart()
                else:
                    output.lineEnd()
            if defined0:
                output.point(self._x(data[i], i, data), self._y(data[i], i, data))
        if buffer is not None:
            return str(buffer) or None
        return None

    def x(self, value=None):
        if value is None:
            return self._x
        self._x = value if callable(value) else _constant(value)
        return self

    def y(self, value=None):
        if value is None:
            return self._y
        self._y = value if callable(value) else _constant(value)
        return self

    def defined(self, value=None):
        if value is None:
            return self._defined
        self._defined = value if callable(value) else _constant(bool(value))
        return self

    def curve(self, value=None):
        if value is None:
            return self._curve
        self._curve = value
        return self

    def context(self, value=None):
        if value is None:
            return self._context
        self._context = value
        return self


def line(x=None, y=None) -> Line:
    return Line(x, y)


def lineRadial(angle=None, radius=None) -> Line:
    gen = Line(angle, radius)
    base_call = gen.__call__

    def call(data):
        return _radial_reproject(gen, data)

    gen.__call__ = call  # type: ignore[assignment]
    return gen


def _radial_reproject(gen: Line, data):
    pts = list(data)
    a = gen._x
    r = gen._y
    proj = Line()
    proj._defined = gen._defined
    proj._curve = gen._curve
    proj._context = gen._context

    def x(d, i, arr):
        return pointRadial(a(d, i, arr), r(d, i, arr))[0]

    def y(d, i, arr):
        return pointRadial(a(d, i, arr), r(d, i, arr))[1]

    proj._x = x
    proj._y = y
    return proj(pts)


class Area:
    def __init__(self, x0=None, y0=None, y1=None):
        self._x0 = x0 if callable(x0) else _constant(x0) if x0 is not None else _x_of
        self._x1: Callable | None = None
        self._y0 = y0 if callable(y0) else _constant(y0) if y0 is not None else _constant(0)
        self._y1 = y1 if callable(y1) else _constant(y1) if y1 is not None else _y_of
        self._defined: Callable = _constant(True)
        self._curve = curveLinear
        self._context = None

    def __call__(self, data: Sequence) -> Any:
        data = list(data)
        n = len(data)
        x0z = [0.0] * n
        y0z = [0.0] * n
        buffer = None
        if self._context is None:
            buffer = Path()
            output = self._curve(buffer)
        else:
            output = self._curve(self._context)
        defined0 = False
        j0 = 0
        segments: list[tuple[int, int]] = []
        for i in range(n + 1):
            in_range = i < n and bool(self._defined(data[i], i, data)) if i < n else False
            if (not in_range) == defined0:
                defined0 = not defined0
                if defined0:
                    j0 = i
                    output.areaStart()
                    output.lineStart()
                else:
                    output.lineEnd()
                    output.lineStart()
                    for k in range(i - 1, j0 - 1, -1):
                        output.point(x0z[k], y0z[k])
                    output.lineEnd()
                    output.areaEnd()
            if defined0:
                x0v = float(self._x0(data[i], i, data))
                y1v = float(self._y1(data[i], i, data))
                x0z[i] = float(self._x1(data[i], i, data)) if self._x1 else x0v
                y0z[i] = float(self._y0(data[i], i, data))
                output.point(x0v, y1v)
        if buffer is not None:
            return str(buffer) or None
        return None

    def x(self, value=None):
        if value is None:
            return self._x0
        self._x0 = value if callable(value) else _constant(value)
        self._x1 = None
        return self

    def x0(self, value=None):
        if value is None:
            return self._x0
        self._x0 = value if callable(value) else _constant(value)
        return self

    def x1(self, value=None):
        if value is None:
            return self._x1
        self._x1 = value if callable(value) else (_constant(value) if value is not None else None)
        return self

    def y(self, value=None):
        if value is None:
            return self._y1
        self._y0 = _constant(0) if not callable(value) else value
        self._y1 = value if callable(value) else _constant(value)
        return self

    def y0(self, value=None):
        if value is None:
            return self._y0
        self._y0 = value if callable(value) else _constant(value)
        return self

    def y1(self, value=None):
        if value is None:
            return self._y1
        self._y1 = value if callable(value) else _constant(value)
        return self

    def defined(self, value=None):
        if value is None:
            return self._defined
        self._defined = value if callable(value) else _constant(bool(value))
        return self

    def curve(self, value=None):
        if value is None:
            return self._curve
        self._curve = value
        return self

    def context(self, value=None):
        if value is None:
            return self._context
        self._context = value
        return self

    def lineY0(self) -> Line:
        ln = Line()
        ln._x = self._x0
        ln._y = self._y0
        ln._defined = self._defined
        ln._curve = self._curve
        return ln

    def lineY1(self) -> Line:
        ln = Line()
        ln._x = self._x0
        ln._y = self._y1
        ln._defined = self._defined
        ln._curve = self._curve
        return ln


def area(x0=None, y0=None, y1=None) -> Area:
    return Area(x0, y0, y1)


def areaRadial(*args) -> Area:
    return Area(*args)


# -- arc ---------------------------------------------------------

class Arc:
    def __init__(self):
        self._innerRadius: Callable = _constant(0)
        self._outerRadius: Callable = _constant(100)
        self._cornerRadius: Callable = _constant(0)
        self._padRadius: Callable | None = None
        self._startAngle: Callable = _constant(0)
        self._endAngle: Callable = _constant(_TAU)
        self._padAngle: Callable = _constant(0)
        self._context = None

    def __call__(self, *args) -> Any:
        d = args[0] if args else None
        r0 = float(self._innerRadius(d))
        r1 = float(self._outerRadius(d))
        a0 = float(self._startAngle(d)) - _HALF_PI
        a1 = float(self._endAngle(d)) - _HALF_PI
        pad = float(self._padAngle(d))
        context = self._context or Path()

        if r1 < r0:
            r0, r1 = r1, r0
        if not (r1 > _EPSILON):
            context.moveTo(0, 0)
        else:
            da = abs(a1 - a0)
            if da > _TAU - _EPSILON:
                # full annulus
                context.moveTo(r1 * math.cos(a0), r1 * math.sin(a0))
                context.arc(0, 0, r1, a0, a1, a1 < a0)
                if r0 > _EPSILON:
                    context.moveTo(r0 * math.cos(a1), r0 * math.sin(a1))
                    context.arc(0, 0, r0, a1, a0, a0 < a1)
            else:
                ap = pad / 2
                a00 = a0 + ap
                a11 = a1 - ap
                if a11 < a00:
                    a00 = a11 = (a0 + a1) / 2
                context.moveTo(r1 * math.cos(a00), r1 * math.sin(a00))
                context.arc(0, 0, r1, a00, a11, a11 < a00)
                if r0 > _EPSILON:
                    context.lineTo(r0 * math.cos(a11), r0 * math.sin(a11))
                    context.arc(0, 0, r0, a11, a00, a00 < a11)
                else:
                    context.lineTo(0, 0)
            context.closePath()

        if self._context is None:
            return str(context) or None
        return None

    def centroid(self, *args) -> list[float]:
        d = args[0] if args else None
        r = (float(self._innerRadius(d)) + float(self._outerRadius(d))) / 2
        a = (float(self._startAngle(d)) + float(self._endAngle(d))) / 2 - _HALF_PI
        return [math.cos(a) * r, math.sin(a) * r]

    def _acc(self, name, value):
        setattr(self, name, value if callable(value) else _constant(value))
        return self

    def innerRadius(self, v=None):
        return self._innerRadius if v is None else self._acc("_innerRadius", v)

    def outerRadius(self, v=None):
        return self._outerRadius if v is None else self._acc("_outerRadius", v)

    def cornerRadius(self, v=None):
        return self._cornerRadius if v is None else self._acc("_cornerRadius", v)

    def startAngle(self, v=None):
        return self._startAngle if v is None else self._acc("_startAngle", v)

    def endAngle(self, v=None):
        return self._endAngle if v is None else self._acc("_endAngle", v)

    def padAngle(self, v=None):
        return self._padAngle if v is None else self._acc("_padAngle", v)

    def padRadius(self, v=None):
        return self._padRadius if v is None else self._acc("_padRadius", v)

    def context(self, v=None):
        if v is None:
            return self._context
        self._context = v
        return self


def arc() -> Arc:
    return Arc()


# -- pie --------------------------------------------------------

def pie():
    value: Callable = _identity
    sort_values: Callable | None = lambda a, b: (b > a) - (b < a)
    sort: Callable | None = None
    start_angle: Callable = _constant(0)
    end_angle: Callable = _constant(_TAU)
    pad_angle: Callable = _constant(0)

    def gen(data: Sequence) -> list[dict]:
        data = list(data)
        n = len(data)
        total = 0.0
        arcs: list[float] = []
        for i, d in enumerate(data):
            v = float(value(d, i, data))
            arcs.append(v)
            if v > 0:
                total += v
        index = list(range(n))
        if sort_values is not None:
            index.sort(key=_cmp_key(lambda i, j: sort_values(arcs[i], arcs[j])))
        elif sort is not None:
            index.sort(key=_cmp_key(lambda i, j: sort(data[i], data[j])))
        a0 = float(start_angle(data))
        da = min(_TAU, max(-_TAU, float(end_angle(data)) - a0))
        p = min(abs(da) / n, float(pad_angle(data))) if n else 0
        pa = p * (-1 if da < 0 else 1)
        k = (da - n * pa) / total if total else 0
        result: list[dict] = [None] * n  # type: ignore[list-item]
        for pos, j in enumerate(index):
            v = arcs[j]
            a1 = a0 + (v * k if v > 0 else 0) + pa
            result[j] = {
                "data": data[j],
                "index": pos,
                "value": v,
                "startAngle": a0,
                "endAngle": a1,
                "padAngle": p,
            }
            a0 = a1
        return result

    def value_fn(v=None):
        nonlocal value
        if v is None:
            return value
        value = v if callable(v) else _constant(v)
        return gen

    def sort_values_fn(v=None):
        nonlocal sort_values, sort
        if v is None:
            return sort_values
        sort_values = v
        sort = None
        return gen

    def sort_fn(v=None):
        nonlocal sort, sort_values
        if v is None:
            return sort
        sort = v
        sort_values = None
        return gen

    def start_angle_fn(v=None):
        nonlocal start_angle
        if v is None:
            return start_angle
        start_angle = v if callable(v) else _constant(v)
        return gen

    def end_angle_fn(v=None):
        nonlocal end_angle
        if v is None:
            return end_angle
        end_angle = v if callable(v) else _constant(v)
        return gen

    def pad_angle_fn(v=None):
        nonlocal pad_angle
        if v is None:
            return pad_angle
        pad_angle = v if callable(v) else _constant(v)
        return gen

    gen.value = value_fn
    gen.sortValues = sort_values_fn
    gen.sort = sort_fn
    gen.startAngle = start_angle_fn
    gen.endAngle = end_angle_fn
    gen.padAngle = pad_angle_fn
    return gen


def _cmp_key(cmp):
    import functools

    return functools.cmp_to_key(lambda a, b: int((cmp(a, b) > 0) - (cmp(a, b) < 0)))


# -- symbols ---------------------------------------------------

_SQRT3 = math.sqrt(3)


class _SymbolType:
    def __init__(self, draw):
        self.draw = draw


def _draw_circle(context, size):
    r = math.sqrt(size / _PI)
    context.moveTo(r, 0)
    context.arc(0, 0, r, 0, _TAU, False)


def _draw_cross(context, size):
    r = math.sqrt(size / 5) / 2
    context.moveTo(-3 * r, -r)
    for x, y in [(-r, -r), (-r, -3 * r), (r, -3 * r), (r, -r), (3 * r, -r),
                 (3 * r, r), (r, r), (r, 3 * r), (-r, 3 * r), (-r, r),
                 (-3 * r, r)]:
        context.lineTo(x, y)
    context.closePath()


def _draw_diamond(context, size):
    y = math.sqrt(size / (2 * _SQRT3_TAN30()))
    x = y * _SQRT3_TAN30()
    context.moveTo(0, -y)
    context.lineTo(x, 0)
    context.lineTo(0, y)
    context.lineTo(-x, 0)
    context.closePath()


def _SQRT3_TAN30():
    return math.tan(_PI / 6)


def _draw_square(context, size):
    w = math.sqrt(size)
    x = -w / 2
    context.rect(x, x, w, w)


def _draw_star(context, size):
    ka = 0.8908130915292852
    kr = math.sin(_PI / 10) / math.sin(7 * _PI / 10)
    kx = math.sin(_TAU / 10) * kr
    ky = -math.cos(_TAU / 10) * kr
    r = math.sqrt(size * ka)
    x = kx * r
    y = ky * r
    context.moveTo(0, -r)
    context.lineTo(x, y)
    for i in range(1, 5):
        a = _TAU * i / 5
        c, s = math.cos(a), math.sin(a)
        context.lineTo(s * r, -c * r)
        context.lineTo(c * x - s * y, s * x + c * y)
    context.closePath()


def _draw_triangle(context, size):
    y = -math.sqrt(size / (_SQRT3 * 3))
    context.moveTo(0, y * 2)
    context.lineTo(-_SQRT3 * y, -y)
    context.lineTo(_SQRT3 * y, -y)
    context.closePath()


symbolCircle = _SymbolType(_draw_circle)
symbolCross = _SymbolType(_draw_cross)
symbolDiamond = _SymbolType(_draw_diamond)
symbolSquare = _SymbolType(_draw_square)
symbolStar = _SymbolType(_draw_star)
symbolTriangle = _SymbolType(_draw_triangle)
def _draw_wye_shape(context, size):
    # three-armed "Y": arm half-width w, arm length reaching radius r
    r = math.sqrt(size / (3 * _SQRT3))
    w = r / 3
    arm = [(-w, 0.0), (-w, -r * _SQRT3), (w, -r * _SQRT3), (w, 0.0)]
    first = True
    for k in range(3):
        a = _TAU * k / 3
        cos_a, sin_a = math.cos(a), math.sin(a)
        for px, py in arm:
            x = px * cos_a - py * sin_a
            y = px * sin_a + py * cos_a
            if first:
                context.moveTo(x, y)
                first = False
            else:
                context.lineTo(x, y)
    context.closePath()


symbolWye = _SymbolType(_draw_wye_shape)

symbolsFill = [symbolCircle, symbolCross, symbolDiamond, symbolSquare,
               symbolStar, symbolTriangle, symbolWye]
symbolsStroke = [symbolCircle, symbolSquare, symbolDiamond, symbolTriangle,
                 symbolWye]
symbols = symbolsFill


class Symbol:
    def __init__(self, type_=symbolCircle, size=64):
        self._type = type_ if callable(type_) or hasattr(type_, "draw") else _constant(type_)
        self._size = size if callable(size) else _constant(size)
        self._context = None

    def __call__(self, *args) -> Any:
        context = self._context or Path()
        t = self._type(*args) if callable(self._type) else self._type
        s = float(self._size(*args)) if callable(self._size) else float(self._size)
        t.draw(context, s)
        if self._context is None:
            return str(context) or None
        return None

    def type(self, v=None):
        if v is None:
            return self._type
        self._type = v if callable(v) else _constant(v)
        return self

    def size(self, v=None):
        if v is None:
            return self._size
        self._size = v if callable(v) else _constant(v)
        return self

    def context(self, v=None):
        if v is None:
            return self._context
        self._context = v
        return self


def symbol(type_=symbolCircle, size=64) -> Symbol:
    return Symbol(type_, size)


# -- link ------------------------------------------------------

def link(curve):
    source: Callable = lambda d: d["source"] if isinstance(d, dict) else d[0]
    target: Callable = lambda d: d["target"] if isinstance(d, dict) else d[1]
    x: Callable = lambda p: p["x"] if isinstance(p, dict) else p[0]
    y: Callable = lambda p: p["y"] if isinstance(p, dict) else p[1]
    context = [None]

    def gen(d: Any) -> Any:
        s = source(d)
        t = target(d)
        buffer = None
        if context[0] is None:
            buffer = Path()
            out = curve(buffer)
        else:
            out = curve(context[0])
        out.lineStart()
        out.point(float(x(s)), float(y(s)))
        out.point(float(x(t)), float(y(t)))
        out.lineEnd()
        if buffer is not None:
            return str(buffer) or None
        return None

    def _set(attr, v):
        nonlocal source, target, x, y
        if attr == "source":
            source = v if callable(v) else _constant(v)
        elif attr == "target":
            target = v if callable(v) else _constant(v)
        elif attr == "x":
            x = v if callable(v) else _constant(v)
        elif attr == "y":
            y = v if callable(v) else _constant(v)
        return gen

    gen.source = lambda v=None: source if v is None else _set("source", v)
    gen.target = lambda v=None: target if v is None else _set("target", v)
    gen.x = lambda v=None: x if v is None else _set("x", v)
    gen.y = lambda v=None: y if v is None else _set("y", v)

    def context_fn(v=None):
        if v is None:
            return context[0]
        context[0] = v
        return gen

    gen.context = context_fn
    return gen


def linkHorizontal():
    return link(curveBumpX)


def linkVertical():
    return link(curveBumpY)


def linkRadial():
    lnk = link(curveBumpX)
    base_x = lnk.x()
    base_y = lnk.y()

    def rx(p):
        return pointRadial(base_x(p), base_y(p))[0]

    def ry(p):
        return pointRadial(base_x(p), base_y(p))[1]

    lnk.x(lambda p: p["angle"] if isinstance(p, dict) else p[0])
    lnk.y(lambda p: p["radius"] if isinstance(p, dict) else p[1])
    return lnk


# -- stack ----------------------------------------------------

def stackOrderNone(series):
    return list(range(len(series)))


def stackOrderReverse(series):
    return list(range(len(series) - 1, -1, -1))


def stackOrderAscending(series):
    sums = [_series_sum(s) for s in series]
    return sorted(range(len(series)), key=lambda i: sums[i])


def stackOrderDescending(series):
    return stackOrderAscending(series)[::-1]


def stackOrderAppearance(series):
    peaks = [_series_peak(s) for s in series]
    return sorted(range(len(series)), key=lambda i: peaks[i])


def stackOrderInsideOut(series):
    order = stackOrderAppearance(series)
    sums = [_series_sum(series[i]) for i in order]
    top: list[int] = []
    bottom: list[int] = []
    total = 0.0
    for i, idx in enumerate(order):
        if total < sum(sums) / 2:
            bottom.append(idx)
        else:
            top.append(idx)
        total += sums[i]
    return list(reversed(bottom)) + top


def _series_sum(s):
    return sum((p[1] - p[0]) for p in s if p[1] is not None and p[0] is not None)


def _series_peak(s):
    best = -1
    best_v = -math.inf
    for i, p in enumerate(s):
        v = (p[1] - p[0]) if p[1] is not None else 0
        if v > best_v:
            best_v = v
            best = i
    return best


def stackOffsetNone(series, order):
    if len(series) < 2:
        return
    top = series[order[0]]
    for j in range(len(top)):
        acc = 0.0
        for i in order:
            point = series[i][j]
            point[0] = acc
            acc += point[1]
            point[1] = acc


def stackOffsetExpand(series, order):
    if not series:
        return
    n = len(series[0])
    for j in range(n):
        total = sum(series[i][j][1] for i in order) or 1
        for i in order:
            series[i][j][1] /= total
    stackOffsetNone(series, order)


def stackOffsetDiverging(series, order):
    if len(series) < 1:
        return
    n = len(series[0])
    for j in range(n):
        pos = neg = 0.0
        for i in order:
            point = series[i][j]
            dy = point[1] - point[0]
            if dy >= 0:
                point[0] = pos
                pos += dy
                point[1] = pos
            else:
                point[1] = neg
                neg += dy
                point[0] = neg


def stackOffsetSilhouette(series, order):
    if not series:
        return
    n = len(series[0])
    for j in range(n):
        total = sum(series[i][j][1] for i in order)
        shift = -total / 2
        if order:
            series[order[0]][j][0] = shift
    stackOffsetNone(series, order)
    for j in range(n):
        total = sum(
            (series[i][j][1] - series[i][j][0]) for i in order
        )
        shift = -total / 2
        for i in order:
            series[i][j][0] += shift
            series[i][j][1] += shift


def stackOffsetWiggle(series, order):
    stackOffsetNone(series, order)
    if not series or not order:
        return
    n = len(series[0])
    for j in range(1, n):
        s1 = 0.0
        s2 = 0.0
        for oi, i in enumerate(order):
            dy = series[i][j][1] - series[i][j][0]
            dy_prev = series[i][j - 1][1] - series[i][j - 1][0]
            contrib = sum(
                (series[order[k]][j][1] - series[order[k]][j][0])
                for k in range(oi)
            )
            s1 += (contrib + dy / 2) * (dy - dy_prev)
            s2 += dy
        move = -s1 / s2 if s2 else 0
        for i in order:
            series[i][j][0] += move
            series[i][j][1] += move


def stack():
    keys: Callable = _constant([])
    value: Callable = lambda d, key, i, data: (
        d.get(key, 0) if isinstance(d, dict) else 0
    )
    order: Callable = stackOrderNone
    offset: Callable = stackOffsetNone

    def gen(data: Sequence) -> list:
        data = list(data)
        key_list = list(keys(data))
        series = []
        for key in key_list:
            s = []
            for i, d in enumerate(data):
                point = [0.0, float(value(d, key, i, data))]
                # attach data ref loosely
                s.append(point)
            series.append(_KeyedSeries(s, key))
        oz = list(order(series))
        for idx, i in enumerate(oz):
            series[i].index = idx
        offset(series, oz)
        return series

    def keys_fn(v=None):
        nonlocal keys
        if v is None:
            return keys
        keys = v if callable(v) else _constant(list(v))
        return gen

    def value_fn(v=None):
        nonlocal value
        if v is None:
            return value
        value = v if callable(v) else _constant(v)
        return gen

    def order_fn(v=None):
        nonlocal order
        if v is None:
            return order
        order = v if callable(v) else _constant(v)
        return gen

    def offset_fn(v=None):
        nonlocal offset
        if v is None:
            return offset
        offset = v
        return gen

    gen.keys = keys_fn
    gen.value = value_fn
    gen.order = order_fn
    gen.offset = offset_fn
    return gen


class _KeyedSeries(list):
    def __init__(self, points, key):
        super().__init__(points)
        self.key = key
        self.index = 0
