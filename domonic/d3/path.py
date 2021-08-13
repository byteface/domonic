"""
    domonic.d3.path
    ====================================

"""

from domonic.javascript import Math

pi = Math.PI
tau = 2 * pi
epsilon = 1e-6
tauEpsilon = tau - epsilon


class Path():

    def __init__(self):
        self._x0 = None
        self._y0 = None
        self._x1 = None
        self._y1 = None
        self._ = ""

    def moveTo(self, x, y):
        self._x0 = self._x1 = x
        self._y0 = self._y1 = y
        self._ += "M" + str(x) + "," + str(y)

    def closePath(self):
        if self._x1 != None:
            self._x1 = self._x0
            self._y1 = self._y0
            self._ += "Z"

    def lineTo(self, x, y):
        self._x1 = x
        self._y1 = y
        self._ += "L" + str(x) + "," + str(y)

    def quadraticCurveTo(self, x1, y1, x, y):
        self._x1 = x
        self._y1 = y
        self._ += "Q" + str(x1) + "," + str(y1) + "," + str(x) + "," + str(y)

    def bezierCurveTo(self, x1, y1, x2, y2, x, y):
        self._x1 = x
        self._y1 = y
        self._ += "C" + str(x1) + "," + str(y1) + "," + str(x2) + "," + str(y2) + "," + str(x) + "," + str(y)

    def arcTo(self, x1, y1, x2, y2, r):
        x1 = x1
        y1 = y1
        x2 = x2
        y2 = y2
        r = r
        x0 = self._x1
        y0 = self._y1
        x21 = x2 - x1
        y21 = y2 - y1
        x01 = x0 - x1
        y01 = y0 - y1
        l01_2 = x01 * x01 + y01 * y01

        # Is the radius negative? Exception.
        if r < 0:
            raise Exception("negative radius: " + r)

        # Is self path empty? Move to (x1,y1).
        if self._x1 == None:
            self._x1 = x1
            self._y1 = y1
            self._ += "M" + str(x1) + "," + str(y1)

        # Or, is (x1,y1) coincident with (x0,y0)? Do nothing.
        elif not (l01_2 > epsilon):
            pass

        # Or, are (x0,y0), (x1,y1) and (x2,y2) collinear?
        # Equivalently, is (x1,y1) coincident with (x2,y2)?
        # Or, is the radius zero? Line to (x1,y1).
        elif not (Math.abs(y01 * x21 - y21 * x01) > epsilon) or not r:
            self._x1 = x1
            self._y1 = y1
            self._ += "L" + str(x1) + "," + str(y1)

        # Otherwise, draw an arc!
        else:
            x20 = x2 - x0
            y20 = y2 - y0
            l21_2 = x21 * x21 + y21 * y21
            l20_2 = x20 * x20 + y20 * y20
            l21 = Math.sqrt(l21_2)
            l01 = Math.sqrt(l01_2)
            l = r * Math.tan((pi - Math.acos((l21_2 + l01_2 - l20_2) / (2 * l21 * l01))) / 2)
            t01 = l / l01
            t21 = l / l21

        # If the start tangent is not coincident with (x0,y0), line to.
        if (Math.abs(t01 - 1) > epsilon):
            self._ += "L" + str(x1 + t01 * x01) + "," + str(y1 + t01 * y01)

        self._x1 = x1 + t21 * x21
        self._y1 = y1 + t21 * y21
        self._ += "A" + str(r) + "," + str(r) + ",0,0," + str(y01 * x20 > x01 * y20) + "," + str(x1 + t21 * x21) + "," + str(y1 + t21 * y21)

    def arc(self, x, y, r, a0, a1, ccw):
        x = x
        y = y
        r = r
        ccw = False  # !!ccw
        dx = r * Math.cos(a0)
        dy = r * Math.sin(a0)
        x0 = x + dx
        y0 = y + dy
        cw = 1 ^ ccw
        da = a0 - a1 if ccw else a1 - a0

        # Is the radius negative? Exception.
        if (r < 0):
            raise Exception("negative radius: " + r)

        # Is self path empty? Move to (x0,y0).
        if (self._x1 == None):
            self._ += "M" + str(x0) + "," + str(y0)

        # Or, is (x0,y0) not coincident with the previous point? Line to (x0,y0).
        elif (Math.abs(self._x1 - x0) > epsilon or Math.abs(self._y1 - y0) > epsilon):
            self._ += "L" + str(x0) + "," + str(y0)

        # Is self arc empty? We’re done.
        if not r:
            return

        # Does the angle go the wrong way? Flip the direction.
        if da < 0:
            da = da % tau + tau

        # Is self a complete circle? Draw two arcs to complete the circle.
        if (da > tauEpsilon):
            self._x1 = x0
            self._y1 = y0
            self._ += "A" + str(r) + "," + str(r) + ",0,1," + str(cw) + "," + str(x - dx) + "," + str(y - dy) + "A" + str(r) + "," + r + ",0,1," + str(cw) + "," + str(x0) + "," + str(y0)

        # Is self arc non-empty? Draw an arc!
        elif da > epsilon:
            self._x1 = x + r * Math.cos(a1)
            self._y1 = y + r * Math.sin(a1)
            self._ += "A" + r + "," + r + ",0," + (da >= pi) + "," + cw + "," + (x + r * Math.cos(a1)) + "," + (y + r * Math.sin(a1))

    def rect(self, x, y, w, h):
        self._x0 = self._x1 = x
        self._y0 = self._y1 = y
        self._ += "M" + x + "," + y + "h" + w + "v" + h + "h" + w + "Z"

    def toString(self):
        return self._

    def __str__(self):
        return self._

    # def __repr__(self):
    #     return self._


# def path():
#     return Path

path = Path
