"""
    domonic.d3.tile
    ====================================

    # TODO - completely untested

"""

from domonic.javascript import Math


def defaultScale(t):
    return t.k


def defaultTranslate(t):
    return [t.x, t.y]


def constant(x):
    return lambda: x


class tile():

    def __init__(self, *args):
        self.x0 = 0
        self.y0 = 0
        self.x1 = 960
        self.y1 = 500
        self.clampX = True
        self.clampY = True
        self.tileSize = 256
        self.scale = defaultScale
        self.translate = defaultTranslate
        self.zoomDelta = 0

    def __call__(self, *args):
        scale_ = self.scale.apply(self, args)
        translate_ = self.translate.apply(self, args)
        z = Math.log2(scale_ / self.tileSize)
        z0 = Math.round(Math.max(z + self.zoomDelta, 0))
        k = Math.pow(2, z - z0) * self.tileSize
        x = translate_[0] - scale_ / 2
        y = translate_[1] - scale_ / 2
        xmin = Math.max(0 if self.clampX else -Infinity, Math.floor((self.x0 - x) / k))
        xmax = Math.min(1 << z0 if self.clampX else Infinity, Math.ceil((self.x1 - x) / k))
        ymin = Math.max(0 if self.clampY else -Infinity, Math.floor((self.y0 - y) / k))
        ymax = Math.min(1 << z0 if self.clampY else Infinity, Math.ceil((self.y1 - y) / k))
        tiles = []

        for y in range(ymin, ymax):
            for x in range(xmin, xmax):
                tiles.append([x, y, z0])

        tiles.translate = [x / k, y / k]
        tiles.scale = k
        return tiles

    def size(_, *args):
        return (x0 = y0 = 0, x1 = +_[0], y1 = +_[1], tile) if Global.Boolean(args) else [x1 - x0, y1 - y0]

    def extent(_, *args):
        return (x0 = +_[0][0], y0 = +_[0][1], x1 = +_[1][0], y1 = +_[1][1], tile) if Global.Boolean(args) else [[x0, y0], [x1, y1]]

    # def scale(_, *args):
    #     return Global.Boolean(args) ? (scale = typeof _ === "function" ? _ : constant(+_), tile) : scale

    # def translate(_, *args):
    #     return Global.Boolean(args) ? (translate = typeof _ === "function" ? _ : constant([+_[0], +_[1]]), tile) : translate

    def zoomDelta(_, *args):
        return (zoomDelta = +_, tile) if Global.Boolean(args) else zoomDelta

    def tileSize(_, *args):
        return (tileSize = +_, tile) if Global.Boolean(args) else tileSize

    # def clamp(_, *args):
    #     return (clampX = clampY = !!_, tile) if Global.Boolean(args) else clampX and clampY

    # def clampX(_, *args):
    #     return (clampX = !!_, tile) if Global.Boolean(args) else clampX

    # def clampY(_, *args):
    #     return (clampY = !!_, tile) if Global.Boolean(args) else clampY

#   return tile