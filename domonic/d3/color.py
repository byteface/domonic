"""
domonic.d3.color
====================================

A port of `d3-color <https://github.com/d3/d3-color>`_ (v3): the ``color()``
parser and the ``Rgb``, ``Hsl``, ``Lab``, ``Hcl`` and ``Cubehelix`` colour
spaces, each with ``brighter`` / ``darker`` / ``rgb`` / ``formatHex`` /
``formatRgb`` / ``toString``.
"""

from __future__ import annotations

import math
import re
from typing import Any

__all__ = [
    "color", "rgb", "hsl", "lab", "hcl", "lch", "gray", "cubehelix",
    "Color", "Rgb", "Hsl", "Lab", "Hcl", "Cubehelix",
]

_DARKER = 0.7
_BRIGHTER = 1 / _DARKER

_REI = r"\s*([+-]?\d+)\s*"
_REN = r"\s*([+-]?(?:\d*\.)?\d+(?:[eE][+-]?\d+)?)\s*"
_REP = r"\s*([+-]?(?:\d*\.)?\d+(?:[eE][+-]?\d+)?)%\s*"

_RE_HEX = re.compile(r"^#([0-9a-f]{3,8})$")
_RE_RGB_INT = re.compile(rf"^rgb\({_REI},{_REI},{_REI}\)$")
_RE_RGB_PCT = re.compile(rf"^rgb\({_REP},{_REP},{_REP}\)$")
_RE_RGBA_INT = re.compile(rf"^rgba\({_REI},{_REI},{_REI},{_REN}\)$")
_RE_RGBA_PCT = re.compile(rf"^rgba\({_REP},{_REP},{_REP},{_REN}\)$")
_RE_HSL_PCT = re.compile(rf"^hsl\({_REN},{_REP},{_REP}\)$")
_RE_HSLA_PCT = re.compile(rf"^hsla\({_REN},{_REP},{_REP},{_REN}\)$")

NAMED_COLORS: dict[str, int] = {
    "aliceblue": 0xF0F8FF, "antiquewhite": 0xFAEBD7, "aqua": 0x00FFFF,
    "aquamarine": 0x7FFFD4, "azure": 0xF0FFFF, "beige": 0xF5F5DC,
    "bisque": 0xFFE4C4, "black": 0x000000, "blanchedalmond": 0xFFEBCD,
    "blue": 0x0000FF, "blueviolet": 0x8A2BE2, "brown": 0xA52A2A,
    "burlywood": 0xDEB887, "cadetblue": 0x5F9EA0, "chartreuse": 0x7FFF00,
    "chocolate": 0xD2691E, "coral": 0xFF7F50, "cornflowerblue": 0x6495ED,
    "cornsilk": 0xFFF8DC, "crimson": 0xDC143C, "cyan": 0x00FFFF,
    "darkblue": 0x00008B, "darkcyan": 0x008B8B, "darkgoldenrod": 0xB8860B,
    "darkgray": 0xA9A9A9, "darkgreen": 0x006400, "darkgrey": 0xA9A9A9,
    "darkkhaki": 0xBDB76B, "darkmagenta": 0x8B008B, "darkolivegreen": 0x556B2F,
    "darkorange": 0xFF8C00, "darkorchid": 0x9932CC, "darkred": 0x8B0000,
    "darksalmon": 0xE9967A, "darkseagreen": 0x8FBC8F, "darkslateblue": 0x483D8B,
    "darkslategray": 0x2F4F4F, "darkslategrey": 0x2F4F4F,
    "darkturquoise": 0x00CED1, "darkviolet": 0x9400D3, "deeppink": 0xFF1493,
    "deepskyblue": 0x00BFFF, "dimgray": 0x696969, "dimgrey": 0x696969,
    "dodgerblue": 0x1E90FF, "firebrick": 0xB22222, "floralwhite": 0xFFFAF0,
    "forestgreen": 0x228B22, "fuchsia": 0xFF00FF, "gainsboro": 0xDCDCDC,
    "ghostwhite": 0xF8F8FF, "gold": 0xFFD700, "goldenrod": 0xDAA520,
    "gray": 0x808080, "green": 0x008000, "greenyellow": 0xADFF2F,
    "grey": 0x808080, "honeydew": 0xF0FFF0, "hotpink": 0xFF69B4,
    "indianred": 0xCD5C5C, "indigo": 0x4B0082, "ivory": 0xFFFFF0,
    "khaki": 0xF0E68C, "lavender": 0xE6E6FA, "lavenderblush": 0xFFF0F5,
    "lawngreen": 0x7CFC00, "lemonchiffon": 0xFFFACD, "lightblue": 0xADD8E6,
    "lightcoral": 0xF08080, "lightcyan": 0xE0FFFF,
    "lightgoldenrodyellow": 0xFAFAD2, "lightgray": 0xD3D3D3,
    "lightgreen": 0x90EE90, "lightgrey": 0xD3D3D3, "lightpink": 0xFFB6C1,
    "lightsalmon": 0xFFA07A, "lightseagreen": 0x20B2AA,
    "lightskyblue": 0x87CEFA, "lightslategray": 0x778899,
    "lightslategrey": 0x778899, "lightsteelblue": 0xB0C4DE,
    "lightyellow": 0xFFFFE0, "lime": 0x00FF00, "limegreen": 0x32CD32,
    "linen": 0xFAF0E6, "magenta": 0xFF00FF, "maroon": 0x800000,
    "mediumaquamarine": 0x66CDAA, "mediumblue": 0x0000CD,
    "mediumorchid": 0xBA55D3, "mediumpurple": 0x9370DB,
    "mediumseagreen": 0x3CB371, "mediumslateblue": 0x7B68EE,
    "mediumspringgreen": 0x00FA9A, "mediumturquoise": 0x48D1CC,
    "mediumvioletred": 0xC71585, "midnightblue": 0x191970,
    "mintcream": 0xF5FFFA, "mistyrose": 0xFFE4E1, "moccasin": 0xFFE4B5,
    "navajowhite": 0xFFDEAD, "navy": 0x000080, "oldlace": 0xFDF5E6,
    "olive": 0x808000, "olivedrab": 0x6B8E23, "orange": 0xFFA500,
    "orangered": 0xFF4500, "orchid": 0xDA70D6, "palegoldenrod": 0xEEE8AA,
    "palegreen": 0x98FB98, "paleturquoise": 0xAFEEEE,
    "palevioletred": 0xDB7093, "papayawhip": 0xFFEFD5, "peachpuff": 0xFFDAB9,
    "peru": 0xCD853F, "pink": 0xFFC0CB, "plum": 0xDDA0DD, "powderblue": 0xB0E0E6,
    "purple": 0x800080, "rebeccapurple": 0x663399, "red": 0xFF0000,
    "rosybrown": 0xBC8F8F, "royalblue": 0x4169E1, "saddlebrown": 0x8B4513,
    "salmon": 0xFA8072, "sandybrown": 0xF4A460, "seagreen": 0x2E8B57,
    "seashell": 0xFFF5EE, "sienna": 0xA0522D, "silver": 0xC0C0C0,
    "skyblue": 0x87CEEB, "slateblue": 0x6A5ACD, "slategray": 0x708090,
    "slategrey": 0x708090, "snow": 0xFFFAFA, "springgreen": 0x00FF7F,
    "steelblue": 0x4682B4, "tan": 0xD2B48C, "teal": 0x008080,
    "thistle": 0xD8BFD8, "tomato": 0xFF6347, "turquoise": 0x40E0D0,
    "violet": 0xEE82EE, "wheat": 0xF5DEB3, "white": 0xFFFFFF,
    "whitesmoke": 0xF5F5F5, "yellow": 0xFFFF00, "yellowgreen": 0x9ACD32,
}


def _clampi(value: float) -> int:
    if value is None or value != value:
        return 0
    return max(0, min(255, round(value)))


def _hex2(value: float) -> str:
    return f"{_clampi(value):02x}"


class Color:
    def rgb(self) -> "Rgb":  # overridden by every concrete colour space
        raise NotImplementedError

    def displayable(self) -> bool:
        return self.rgb().displayable()

    def formatHex(self) -> str:
        return self.rgb().formatHex()

    def formatHex8(self) -> str:
        return self.rgb().formatHex8()

    def formatHsl(self) -> str:
        return hslConvert(self).formatHsl()

    def formatRgb(self) -> str:
        return self.rgb().formatRgb()

    def __str__(self) -> str:
        return self.formatRgb()

    def hex(self) -> str:  # deprecated d3 alias
        return self.formatHex()


def color(specifier: Any):
    """Parse a CSS colour string (hex, ``rgb()``/``rgba()``, ``hsl()``/``hsla()``
    or a named colour) and return an ``Rgb`` / ``Hsl``, or ``None``."""
    if specifier is None:
        return None
    if isinstance(specifier, Color):
        return specifier.rgb() if not isinstance(specifier, Rgb) else Rgb(
            specifier.r, specifier.g, specifier.b, specifier.opacity
        )
    s = str(specifier).strip().lower()
    m = _RE_HEX.match(s)
    if m:
        h = m.group(1)
        length = len(h)
        n = int(h, 16)
        if length == 6:
            return _rgbn(n)
        if length == 3:
            return Rgb(
                ((n >> 8) & 0xF) * 0x11,
                ((n >> 4) & 0xF) * 0x11,
                (n & 0xF) * 0x11,
                1,
            )
        if length == 8:
            return Rgb(
                (n >> 24) & 0xFF,
                (n >> 16) & 0xFF,
                (n >> 8) & 0xFF,
                (n & 0xFF) / 0xFF,
            )
        if length == 4:
            return Rgb(
                ((n >> 12) & 0xF) * 0x11,
                ((n >> 8) & 0xF) * 0x11,
                ((n >> 4) & 0xF) * 0x11,
                (((n & 0xF) * 0x11) / 0xFF),
            )
        return None
    for regex, pct in ((_RE_RGB_INT, False), (_RE_RGB_PCT, True)):
        m = regex.match(s)
        if m:
            r, g, b = (float(x) for x in m.groups())
            if pct:
                r, g, b = r * 255 / 100, g * 255 / 100, b * 255 / 100
            return Rgb(r, g, b, 1)
    for regex, pct in ((_RE_RGBA_INT, False), (_RE_RGBA_PCT, True)):
        m = regex.match(s)
        if m:
            r, g, b, a = (float(x) for x in m.groups())
            if pct:
                r, g, b = r * 255 / 100, g * 255 / 100, b * 255 / 100
            return Rgb(r, g, b, a)
    for regex in (_RE_HSL_PCT, _RE_HSLA_PCT):
        m = regex.match(s)
        if m:
            groups = [float(x) for x in m.groups()]
            h, sat, light = groups[0], groups[1] / 100, groups[2] / 100
            a = groups[3] if len(groups) > 3 else 1
            return Hsl(h, sat, light, a)
    if s == "transparent":
        return Rgb(math.nan, math.nan, math.nan, 0)
    if s in NAMED_COLORS:
        return _rgbn(NAMED_COLORS[s])
    return None


def _rgbn(n: int) -> "Rgb":
    return Rgb((n >> 16) & 0xFF, (n >> 8) & 0xFF, n & 0xFF, 1)


def _coerce_opacity(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 1.0


class Rgb(Color):
    _channels = ("r", "g", "b")

    def __init__(self, r: float, g: float, b: float, opacity: float = 1.0) -> None:
        self.r = float(r)
        self.g = float(g)
        self.b = float(b)
        self.opacity = _coerce_opacity(opacity)

    def brighter(self, k: float | None = None) -> "Rgb":
        factor = _BRIGHTER ** (1 if k is None else k)
        return Rgb(self.r * factor, self.g * factor, self.b * factor, self.opacity)

    def darker(self, k: float | None = None) -> "Rgb":
        factor = _DARKER ** (1 if k is None else k)
        return Rgb(self.r * factor, self.g * factor, self.b * factor, self.opacity)

    def rgb(self) -> "Rgb":
        return self

    def clamp(self) -> "Rgb":
        return Rgb(_clampi(self.r), _clampi(self.g), _clampi(self.b),
                   max(0.0, min(1.0, self.opacity)))

    def displayable(self) -> bool:
        return (
            -0.5 <= self.r < 255.5
            and -0.5 <= self.g < 255.5
            and -0.5 <= self.b < 255.5
            and 0 <= self.opacity <= 1
        )

    def formatHex(self) -> str:
        return f"#{_hex2(self.r)}{_hex2(self.g)}{_hex2(self.b)}"

    def formatHex8(self) -> str:
        alpha = round(max(0.0, min(1.0, self.opacity)) * 255)
        return f"#{_hex2(self.r)}{_hex2(self.g)}{_hex2(self.b)}{alpha:02x}"

    def formatRgb(self) -> str:
        a = max(0.0, min(1.0, self.opacity))
        if a == 1:
            return f"rgb({_clampi(self.r)}, {_clampi(self.g)}, {_clampi(self.b)})"
        return f"rgba({_clampi(self.r)}, {_clampi(self.g)}, {_clampi(self.b)}, {a})"

    def copy(self, **kw: Any) -> "Rgb":
        return Rgb(kw.get("r", self.r), kw.get("g", self.g), kw.get("b", self.b),
                   kw.get("opacity", self.opacity))


def rgb(*args: Any) -> Rgb:
    if len(args) == 1:
        parsed = color(args[0])
        if parsed is None:
            return Rgb(math.nan, math.nan, math.nan, 1)
        c = parsed.rgb()
        return Rgb(c.r, c.g, c.b, c.opacity)
    if len(args) >= 3:
        return Rgb(args[0], args[1], args[2], args[3] if len(args) > 3 else 1)
    return Rgb(math.nan, math.nan, math.nan, 1)


class Hsl(Color):
    _channels = ("h", "s", "l")

    def __init__(self, h: float, s: float, l: float, opacity: float = 1.0) -> None:
        self.h = float(h)
        self.s = float(s)
        self.l = float(l)
        self.opacity = _coerce_opacity(opacity)

    def brighter(self, k: float | None = None) -> "Hsl":
        factor = _BRIGHTER ** (1 if k is None else k)
        return Hsl(self.h, self.s, self.l * factor, self.opacity)

    def darker(self, k: float | None = None) -> "Hsl":
        factor = _DARKER ** (1 if k is None else k)
        return Hsl(self.h, self.s, self.l * factor, self.opacity)

    def rgb(self) -> Rgb:
        h = (self.h % 360) + (360 if self.h < 0 else 0)
        s = 0 if (h != h or self.l != self.l) else self.s
        m2 = self.l + (self.l if self.l < 0.5 else 1 - self.l) * s
        m1 = 2 * self.l - m2
        return Rgb(
            _hsl2rgb(h + 120, m1, m2),
            _hsl2rgb(h, m1, m2),
            _hsl2rgb(h - 120, m1, m2),
            self.opacity,
        )

    def clamp(self) -> "Hsl":
        return Hsl(
            _clamph(self.h),
            max(0.0, min(1.0, self.s)),
            max(0.0, min(1.0, self.l)),
            max(0.0, min(1.0, self.opacity)),
        )

    def displayable(self) -> bool:
        return (
            (0 <= self.s <= 1 or self.s != self.s)
            and 0 <= self.l <= 1
            and 0 <= self.opacity <= 1
        )

    def formatHsl(self) -> str:
        a = max(0.0, min(1.0, self.opacity))
        head = "hsl(" if a == 1 else "hsla("
        tail = ")" if a == 1 else f", {a})"
        return (
            f"{head}{_clamph(self.h)}, "
            f"{max(0.0, min(1.0, self.s)) * 100}%, "
            f"{max(0.0, min(1.0, self.l)) * 100}%{tail}"
        )

    def copy(self, **kw: Any) -> "Hsl":
        return Hsl(kw.get("h", self.h), kw.get("s", self.s), kw.get("l", self.l),
                   kw.get("opacity", self.opacity))


def _clamph(value: float) -> float:
    value = value % 360
    return value + 360 if value < 0 else value


def _hsl2rgb(h: float, m1: float, m2: float) -> float:
    h = (h % 360) + (360 if h < 0 else 0)
    if h < 60:
        return (m1 + (m2 - m1) * h / 60) * 255
    if h < 180:
        return m2 * 255
    if h < 240:
        return (m1 + (m2 - m1) * (240 - h) / 60) * 255
    return m1 * 255


def hslConvert(o: Any) -> Hsl:
    if isinstance(o, Hsl):
        return Hsl(o.h, o.s, o.l, o.opacity)
    if not isinstance(o, Color):
        parsed = color(o)
        if parsed is None:
            return Hsl(math.nan, math.nan, math.nan, 1)
        o = parsed
    if isinstance(o, Hsl):
        return Hsl(o.h, o.s, o.l, o.opacity)
    c = o.rgb()
    r, g, b = c.r / 255, c.g / 255, c.b / 255
    mn = min(r, g, b)
    mx = max(r, g, b)
    h = math.nan
    s = mx - mn
    light = (mx + mn) / 2
    if s:
        if r == mx:
            h = (g - b) / s + (6 if g < b else 0)
        elif g == mx:
            h = (b - r) / s + 2
        else:
            h = (r - g) / s + 4
        s /= (2 - mx - mn) if light > 0.5 else (mx + mn)
        h *= 60
    else:
        s = 0 if 0 < light < 1 else h
    return Hsl(h, s, light, c.opacity)


def hsl(*args: Any) -> Hsl:
    if len(args) == 1:
        return hslConvert(args[0])
    if len(args) >= 3:
        return Hsl(args[0], args[1], args[2], args[3] if len(args) > 3 else 1)
    return Hsl(math.nan, math.nan, math.nan, 1)


# -- CIELAB / CIELCH ---------------------------------------------------

_Kn = 18
_Xn = 0.96422
_Yn = 1.0
_Zn = 0.82521
_t0 = 4 / 29
_t1 = 6 / 29
_t2 = 3 * _t1 * _t1
_t3 = _t1 * _t1 * _t1


class Lab(Color):
    _channels = ("l", "a", "b")

    def __init__(self, l: float, a: float, b: float, opacity: float = 1.0) -> None:
        self.l = float(l)
        self.a = float(a)
        self.b = float(b)
        self.opacity = _coerce_opacity(opacity)

    def brighter(self, k: float | None = None) -> "Lab":
        return Lab(self.l + _Kn * (1 if k is None else k), self.a, self.b, self.opacity)

    def darker(self, k: float | None = None) -> "Lab":
        return Lab(self.l - _Kn * (1 if k is None else k), self.a, self.b, self.opacity)

    def rgb(self) -> Rgb:
        y = (self.l + 16) / 116
        x = y if self.a != self.a else y + self.a / 500
        z = y if self.b != self.b else y - self.b / 200
        x = _Xn * _lab2xyz(x)
        y = _Yn * _lab2xyz(y)
        z = _Zn * _lab2xyz(z)
        return Rgb(
            _xyz2rgb(3.1338561 * x - 1.6168667 * y - 0.4906146 * z),
            _xyz2rgb(-0.9787684 * x + 1.9161415 * y + 0.0334540 * z),
            _xyz2rgb(0.0719453 * x - 0.2289914 * y + 1.4052427 * z),
            self.opacity,
        )

    def copy(self, **kw: Any) -> "Lab":
        return Lab(kw.get("l", self.l), kw.get("a", self.a), kw.get("b", self.b),
                   kw.get("opacity", self.opacity))


def _lab2xyz(t: float) -> float:
    return t * t * t if t > _t1 else _t2 * (t - _t0)


def _xyz2lab(t: float) -> float:
    return t ** (1 / 3) if t > _t3 else t / _t2 + _t0


def _xyz2rgb(x: float) -> float:
    v = 12.92 * x if x <= 0.0031308 else 1.055 * (x ** (1 / 2.4)) - 0.055
    return 255 * v


def _rgb2lrgb(x: float) -> float:
    x = x / 255
    return x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4


def labConvert(o: Any) -> Lab:
    if isinstance(o, Lab):
        return Lab(o.l, o.a, o.b, o.opacity)
    if isinstance(o, (Hcl,)):
        return _hcl2lab(o)
    if not isinstance(o, Rgb):
        parsed = o if isinstance(o, Color) else color(o)
        if parsed is None:
            return Lab(math.nan, math.nan, math.nan, 1)
        o = parsed.rgb()
    r = _rgb2lrgb(o.r)
    g = _rgb2lrgb(o.g)
    b = _rgb2lrgb(o.b)
    y = _xyz2lab((0.2225045 * r + 0.7168786 * g + 0.0606169 * b) / _Yn)
    if r == g == b:
        x = z = y
    else:
        x = _xyz2lab((0.4360747 * r + 0.3850649 * g + 0.1430804 * b) / _Xn)
        z = _xyz2lab((0.0139322 * r + 0.0971045 * g + 0.7141733 * b) / _Zn)
    return Lab(116 * y - 16, 500 * (x - y), 200 * (y - z), o.opacity)


def lab(*args: Any) -> Lab:
    if len(args) == 1:
        return labConvert(args[0])
    if len(args) >= 3:
        return Lab(args[0], args[1], args[2], args[3] if len(args) > 3 else 1)
    return Lab(math.nan, math.nan, math.nan, 1)


def gray(l: float, opacity: float = 1.0) -> Lab:
    return Lab(l, 0, 0, opacity)


class Hcl(Color):
    _channels = ("h", "c", "l")

    def __init__(self, h: float, c: float, l: float, opacity: float = 1.0) -> None:
        self.h = float(h)
        self.c = float(c)
        self.l = float(l)
        self.opacity = _coerce_opacity(opacity)

    def brighter(self, k: float | None = None) -> "Hcl":
        return Hcl(self.h, self.c, self.l + _Kn * (1 if k is None else k), self.opacity)

    def darker(self, k: float | None = None) -> "Hcl":
        return Hcl(self.h, self.c, self.l - _Kn * (1 if k is None else k), self.opacity)

    def rgb(self) -> Rgb:
        return _hcl2lab(self).rgb()

    def copy(self, **kw: Any) -> "Hcl":
        return Hcl(kw.get("h", self.h), kw.get("c", self.c), kw.get("l", self.l),
                   kw.get("opacity", self.opacity))


def _hcl2lab(o: Hcl) -> Lab:
    if o.h != o.h:
        return Lab(o.l, 0, 0, o.opacity)
    h = o.h * math.pi / 180
    return Lab(o.l, math.cos(h) * o.c, math.sin(h) * o.c, o.opacity)


def hclConvert(o: Any) -> Hcl:
    if isinstance(o, Hcl):
        return Hcl(o.h, o.c, o.l, o.opacity)
    labo = o if isinstance(o, Lab) else labConvert(o)
    if labo.a == 0 and labo.b == 0:
        return Hcl(math.nan, 0 if 0 < labo.l < 100 else math.nan, labo.l, labo.opacity)
    h = math.atan2(labo.b, labo.a) * 180 / math.pi
    return Hcl(h + 360 if h < 0 else h, math.hypot(labo.a, labo.b), labo.l, labo.opacity)


def hcl(*args: Any) -> Hcl:
    if len(args) == 1:
        return hclConvert(args[0])
    if len(args) >= 3:
        return Hcl(args[0], args[1], args[2], args[3] if len(args) > 3 else 1)
    return Hcl(math.nan, math.nan, math.nan, 1)


def lch(*args: Any) -> Hcl:
    values = list(args)
    if len(values) >= 3:
        values[0], values[2] = values[2], values[0]
    return hcl(*values)


# -- Cubehelix -------------------------------------------------------

_A = -0.14861
_B = 1.78277
_C = -0.29227
_D = -0.90649
_E = 1.97294
_ED = _E * _D
_EB = _E * _B
_BC_DA = _B * _C - _D * _A


class Cubehelix(Color):
    _channels = ("h", "s", "l")

    def __init__(self, h: float, s: float, l: float, opacity: float = 1.0) -> None:
        self.h = float(h)
        self.s = float(s)
        self.l = float(l)
        self.opacity = _coerce_opacity(opacity)

    def brighter(self, k: float | None = None) -> "Cubehelix":
        factor = _BRIGHTER ** (1 if k is None else k)
        return Cubehelix(self.h, self.s, self.l * factor, self.opacity)

    def darker(self, k: float | None = None) -> "Cubehelix":
        factor = _DARKER ** (1 if k is None else k)
        return Cubehelix(self.h, self.s, self.l * factor, self.opacity)

    def rgb(self) -> Rgb:
        h = math.nan if self.h != self.h else (self.h + 120) * math.pi / 180
        light = self.l
        a = (math.nan if self.s != self.s else self.s) * light * (1 - light)
        cosh = 0.0 if h != h else math.cos(h)
        sinh = 0.0 if h != h else math.sin(h)
        return Rgb(
            255 * (light + a * (_A * cosh + _B * sinh)),
            255 * (light + a * (_C * cosh + _D * sinh)),
            255 * (light + a * (_E * cosh)),
            self.opacity,
        )

    def copy(self, **kw: Any) -> "Cubehelix":
        return Cubehelix(kw.get("h", self.h), kw.get("s", self.s),
                         kw.get("l", self.l), kw.get("opacity", self.opacity))


def cubehelixConvert(o: Any) -> Cubehelix:
    if isinstance(o, Cubehelix):
        return Cubehelix(o.h, o.s, o.l, o.opacity)
    c = o if isinstance(o, Rgb) else rgb(o)
    r, g, b = c.r / 255, c.g / 255, c.b / 255
    light = (_BC_DA * b + _ED * r - _EB * g) / (_BC_DA + _ED - _EB)
    bl = b - light
    k = (_E * (g - light) - _C * bl) / _D
    denom = light * (1 - light)
    s = math.sqrt(k * k + bl * bl) / (_E * denom) if denom else math.nan
    h = math.atan2(k, bl) * 180 / math.pi - 120 if s else math.nan
    return Cubehelix(h + 360 if h is not None and h < 0 else h, s, light, c.opacity)


def cubehelix(*args: Any) -> Cubehelix:
    if len(args) == 1:
        return cubehelixConvert(args[0])
    if len(args) >= 3:
        return Cubehelix(args[0], args[1], args[2], args[3] if len(args) > 3 else 1)
    return Cubehelix(math.nan, math.nan, math.nan, 1)
