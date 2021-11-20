"""
    domonic.geom.vec4
    ====================================
    written by.ai
"""
import math
from domonic.javascript import Math


class vec4():
    """[vec4]
    """

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0, w: float = 0.0, n: float = 1.0):
        self.x: float = x
        self.y: float = y
        self.z: float = z
        self.w: float = w
        self.n: float = n

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        w = self.w + other.w
        return vec4(x, y, z, w)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        w = self.w - other.w
        return vec4(x, y, z, w)

    def __mul__(self, other):
        n = self.n * other.n
        a = self.x * other.x + self.y * other.y + self.z * other.z
        b = self.x * other.y - self.y * other.x + self.z * other.w
        c = self.x * other.z - self.z * other.x + self.y * other.w
        d = self.w * other.n - self.x * other.w
        x = a + b * n
        y = b - a * n
        z = c + d * n
        w = d - c * n
        return vec4(x, y, z, w)
