"""
domonic.d3.tile
====================================

"""

import math


def defaultScale(t):
    return t.k


def defaultTranslate(t):
    return [t.x, t.y]


def constant(x):
    return lambda: x


class Tiles(list):
    """Tile coordinate list with d3-tile style metadata."""

    def __init__(self, values=(), translate=None, scale=1):
        super().__init__(values)
        self.translate = translate or [0, 0]
        self.scale = scale


class tile:
    def __init__(self, *args):
        self.x0 = 0
        self.y0 = 0
        self.x1 = 960
        self.y1 = 500
        self.clampX = True
        self.clampY = True
        self._tileSize = 256
        self._scale = defaultScale
        self._translate = defaultTranslate
        self._zoomDelta = 0

    def __call__(self, *args):
        scale_ = self._scale(*args)
        translate_ = self._translate(*args)
        z = math.log2(scale_ / self._tileSize)
        z0 = int(math.floor(max(z + self._zoomDelta, 0) + 0.5))
        k = math.pow(2, z - z0) * self._tileSize
        x = translate_[0] - scale_ / 2
        y = translate_[1] - scale_ / 2
        xmin = max(0 if self.clampX else -math.inf, math.floor((self.x0 - x) / k))
        xmax = min(
            1 << z0 if self.clampX else math.inf,
            math.ceil((self.x1 - x) / k),
        )
        ymin = max(0 if self.clampY else -math.inf, math.floor((self.y0 - y) / k))
        ymax = min(
            1 << z0 if self.clampY else math.inf,
            math.ceil((self.y1 - y) / k),
        )
        tiles = []

        for ty in range(int(ymin), int(ymax)):
            for tx in range(int(xmin), int(xmax)):
                tiles.append([tx, ty, z0])

        return Tiles(tiles, translate=[x / k, y / k], scale=k)

    def size(self, value=None):
        if value is None:
            return [self.x1 - self.x0, self.y1 - self.y0]
        self.x0 = self.y0 = 0
        self.x1 = float(value[0])
        self.y1 = float(value[1])
        return self

    def extent(self, value=None):
        if value is None:
            return [[self.x0, self.y0], [self.x1, self.y1]]
        self.x0 = float(value[0][0])
        self.y0 = float(value[0][1])
        self.x1 = float(value[1][0])
        self.y1 = float(value[1][1])
        return self

    def scale(self, value=None):
        if value is None:
            return self._scale
        self._scale = value if callable(value) else constant(float(value))
        return self

    def translate(self, value=None):
        if value is None:
            return self._translate
        self._translate = (
            value
            if callable(value)
            else constant([float(value[0]), float(value[1])])
        )
        return self

    def zoomDelta(self, value=None):
        if value is None:
            return self._zoomDelta
        self._zoomDelta = float(value)
        return self

    def tileSize(self, value=None):
        if value is None:
            return self._tileSize
        self._tileSize = float(value)
        return self

    def clamp(self, value=None):
        if value is None:
            return self.clampX and self.clampY
        self.clampX = bool(value)
        self.clampY = bool(value)
        return self

    def clamp_x(self, value=None):
        if value is None:
            return self.clampX
        self.clampX = bool(value)
        return self

    def clamp_y(self, value=None):
        if value is None:
            return self.clampY
        self.clampY = bool(value)
        return self
