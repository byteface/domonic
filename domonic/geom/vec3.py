"""
    domonic.geom.vec3
    ====================================
    written by.ai
"""
import math
from domonic.javascript import Math

class vec3():
    """[vec3]
    """

    def __init__(self, x=0, y=0, z=0, w=0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __add__(self, other):
        if isinstance(other, vec3):
            return self.__class__((self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w))
        else:
            return self.__class__((self.x + other, self.y + other, self.z + other, self.w + other))

    def __sub__(self, other):
        if isinstance(other, vec3):
            return self.__class__((self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w))
        else:
            return self.__class__((self.x - other, self.y - other, self.z - other, self.w - other))

    def __mul__(self, other):
        if isinstance(other, vec3):
            return self.__class__((self.x * other.x, self.y * other.y, self.z * other.z, self.w * other.w))
        else:
            return self.__class__((self.x * other, self.y * other, self.z * other, self.w * other))

    # def __rmul__(self, other):
    #     return vec3(other.x * self.x, other.y * self.y, other.z * self.z, other.w * self.w)

    def __truediv__(self, other):
        if isinstance(other, vec3):
            return self.__class__(self.x / other.x, self.y / other.y, self.z / other.z, self.w / other.w)
        else:
            return self.__class__(self.x / other, self.y / other, self.z / other, self.w / other)

    # def __pow__(self, other):
    #     return vec3(self.x ** other.x, self.y ** other.y, self.z ** other.z, self.w ** other.w)

    # def __mod__(self, other):
    #     return vec3(self.x % other.x, self.y % other.y, self.z % other.z, self.w % other.w)

    def __getitem__(self, item):
        if isinstance(item, int):
            if item == 0:
                return self.x
            elif item == 1:
                return self.y
            elif item == 2:
                return self.z
            elif item == 3:
                return self.w
        elif isinstance(item, str):
            if item == 'x':
                return self.x
            elif item == 'y':
                return self.y
            elif item == 'z':
                return self.z
            elif item == 'w':
                return self.w

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        self.w += other.w

    def add(self, point):
        self.x += point.x
        self.y += point.y
        self.z += point.z
        return self

    def subtract(self, point):
        """ Subtract from this point. """
        self.x -= point.x
        self.y -= point.y
        self.z -= point.z
        return self

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z + self.w * other.w

    def cross(self, other):
        return self.x * other.y - self.y * other.x, self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z

    def mul(self, v):
        return (v.x * self.x + v.y * self.y + v.z * self.z + v.w * self.w)

    def copy(self):
        """ Creates a copy of this object. """
        return vec3(self.x, self.y, self.z, self.w)

    def angleBetween(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return math.sqrt(dx * dx + dy * dy + dz * dz)

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z + self.w * self.w)

    def distance(self, other):
        """ Returns the distance between this point and another vector3."""
        return (self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2 + (self.w - other.w)**2
        # return sqrt(pow(self.x - other.x, 2) + pow(self.y - other.y, 2) + pow(self.z - other.z, 2) + pow(self.w - other.w, 2))

    def equals(self, other):
        """ Determine whether two objects are identical. """
        return self.x == other.x and self.y == other.y and self.z == other.z and self.w == other.w

    def intersects(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        dw = self.w - other.w
        return (dx * dy - dy * dz) > 0 and (dx * dw - dw * dz) > 0 and (dx * dz + dz * dw) > 0 and (dy * dw - dw * dy) > 0 and (dy * dw - dw * dw) > 0

    def clone(self):
        """ Returns a new instance of this vector3. """
        return vec3(self.x, self.y, self.z, self.w)

    def apply(self, point, amount):
        """ Moves the points x,y,z,w by amount. """
        return vec3(point.x + amount.x, point.y + amount.y, point.z + amount.z, point.w + amount.w)

    def __str__(self):
        return str(self.x) + " " + str(self.y) + " " + str(self.z)
