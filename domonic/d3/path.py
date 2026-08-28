"""
domonic.d3.path
====================================

"""

from domonic.javascript import Math

pi = Math.PI
tau = 2 * pi
epsilon = 1e-6
tauEpsilon = tau - epsilon


def _number(value):
    return float(value)


def _format_number(value):
    number = _number(value)
    if Math.abs(number) < epsilon:
        number = 0.0
    rounded = round(number)
    if Math.abs(number - rounded) < epsilon:
        number = float(rounded)
    return str(int(number)) if number.is_integer() else f"{number:.12g}"


def _flag(value):
    return "1" if value else "0"


def _normalize_angle_delta(delta):
    while delta < 0:
        delta += tau
    return delta


class Path:
    def __init__(self):
        self._x0 = None
        self._y0 = None
        self._x1 = None
        self._y1 = None
        self._ = ""

    def moveTo(self, x, y):
        x = _number(x)
        y = _number(y)
        self._x0 = self._x1 = x
        self._y0 = self._y1 = y
        self._ += "M" + _format_number(x) + "," + _format_number(y)

    def closePath(self):
        if self._x1 is not None:
            self._x1 = self._x0
            self._y1 = self._y0
            self._ += "Z"

    def lineTo(self, x, y):
        x = _number(x)
        y = _number(y)
        self._x1 = x
        self._y1 = y
        self._ += "L" + _format_number(x) + "," + _format_number(y)

    def quadraticCurveTo(self, x1, y1, x, y):
        x1 = _number(x1)
        y1 = _number(y1)
        x = _number(x)
        y = _number(y)
        self._x1 = x
        self._y1 = y
        self._ += (
            "Q"
            + _format_number(x1)
            + ","
            + _format_number(y1)
            + ","
            + _format_number(x)
            + ","
            + _format_number(y)
        )

    def bezierCurveTo(self, x1, y1, x2, y2, x, y):
        x1 = _number(x1)
        y1 = _number(y1)
        x2 = _number(x2)
        y2 = _number(y2)
        x = _number(x)
        y = _number(y)
        self._x1 = x
        self._y1 = y
        self._ += (
            "C"
            + _format_number(x1)
            + ","
            + _format_number(y1)
            + ","
            + _format_number(x2)
            + ","
            + _format_number(y2)
            + ","
            + _format_number(x)
            + ","
            + _format_number(y)
        )

    def arcTo(self, x1, y1, x2, y2, r):
        x1 = _number(x1)
        y1 = _number(y1)
        x2 = _number(x2)
        y2 = _number(y2)
        r = _number(r)

        if r < 0:
            raise Exception("negative radius: " + _format_number(r))

        if self._x1 is None:
            self._x1 = x1
            self._y1 = y1
            self._x0 = x1
            self._y0 = y1
            self._ += "M" + _format_number(x1) + "," + _format_number(y1)
            return

        x0 = self._x1
        y0 = self._y1
        x21 = x2 - x1
        y21 = y2 - y1
        x01 = x0 - x1
        y01 = y0 - y1
        l01_2 = x01 * x01 + y01 * y01

        if not (l01_2 > epsilon):
            return

        if not (Math.abs(y01 * x21 - y21 * x01) > epsilon) or not r:
            self._x1 = x1
            self._y1 = y1
            self._ += "L" + _format_number(x1) + "," + _format_number(y1)
            return

        x20 = x2 - x0
        y20 = y2 - y0
        l21_2 = x21 * x21 + y21 * y21
        l20_2 = x20 * x20 + y20 * y20
        l21 = Math.sqrt(l21_2)
        l01 = Math.sqrt(l01_2)
        l = r * Math.tan(
            (pi - Math.acos((l21_2 + l01_2 - l20_2) / (2 * l21 * l01))) / 2
        )
        t01 = l / l01
        t21 = l / l21

        if Math.abs(t01 - 1) > epsilon:
            self._ += (
                "L"
                + _format_number(x1 + t01 * x01)
                + ","
                + _format_number(y1 + t01 * y01)
            )

        self._x1 = x1 + t21 * x21
        self._y1 = y1 + t21 * y21
        self._ += (
            "A"
            + _format_number(r)
            + ","
            + _format_number(r)
            + ",0,0,"
            + _flag(y01 * x20 > x01 * y20)
            + ","
            + _format_number(self._x1)
            + ","
            + _format_number(self._y1)
        )

    def arc(self, x, y, r, a0, a1, ccw):
        x = _number(x)
        y = _number(y)
        r = _number(r)
        a0 = _number(a0)
        a1 = _number(a1)
        ccw = bool(ccw)
        dx = r * Math.cos(a0)
        dy = r * Math.sin(a0)
        x0 = x + dx
        y0 = y + dy
        cw = 0 if ccw else 1
        da = a0 - a1 if ccw else a1 - a0

        # Is the radius negative? Exception.
        if r < 0:
            raise Exception("negative radius: " + _format_number(r))

        # Is self path empty? Move to (x0,y0).
        if self._x1 is None:
            self._x0 = self._x1 = x0
            self._y0 = self._y1 = y0
            self._ += "M" + _format_number(x0) + "," + _format_number(y0)

        # Or, is (x0,y0) not coincident with the previous point? Line to (x0,y0).
        elif Math.abs(self._x1 - x0) > epsilon or Math.abs(self._y1 - y0) > epsilon:
            self._x1 = x0
            self._y1 = y0
            self._ += "L" + _format_number(x0) + "," + _format_number(y0)

        # Is self arc empty? We’re done.
        if not r:
            return

        # Does the angle go the wrong way? Flip the direction.
        if da < 0:
            da = _normalize_angle_delta(da)

        # Is self a complete circle? Draw two arcs to complete the circle.
        if da > tauEpsilon:
            self._x1 = x0
            self._y1 = y0
            self._ += (
                "A"
                + _format_number(r)
                + ","
                + _format_number(r)
                + ",0,1,"
                + _flag(cw)
                + ","
                + _format_number(x - dx)
                + ","
                + _format_number(y - dy)
                + "A"
                + _format_number(r)
                + ","
                + _format_number(r)
                + ",0,1,"
                + _flag(cw)
                + ","
                + _format_number(x0)
                + ","
                + _format_number(y0)
            )

        # Is self arc non-empty? Draw an arc!
        elif da > epsilon:
            self._x1 = x + r * Math.cos(a1)
            self._y1 = y + r * Math.sin(a1)
            self._ += (
                "A"
                + _format_number(r)
                + ","
                + _format_number(r)
                + ",0,"
                + _flag(da >= pi)
                + ","
                + _flag(cw)
                + ","
                + _format_number(self._x1)
                + ","
                + _format_number(self._y1)
            )

    def rect(self, x, y, w, h):
        x = _number(x)
        y = _number(y)
        w = _number(w)
        h = _number(h)
        self._x0 = self._x1 = x
        self._y0 = self._y1 = y
        self._ += (
            "M"
            + _format_number(x)
            + ","
            + _format_number(y)
            + "h"
            + _format_number(w)
            + "v"
            + _format_number(h)
            + "h"
            + _format_number(-w)
            + "Z"
        )

    def toString(self):
        return self._

    def __str__(self):
        return self._

    # def __repr__(self):
    #     return self._


# def path():
#     return Path

path = Path
