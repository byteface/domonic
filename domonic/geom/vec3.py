"""
    domonic.geom.vec3
    ====================================

"""
import math


class vec3:
    """[vec3]"""

    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x: float = x
        self.y: float = y
        self.z: float = z

    def __add__(self, other):
        if isinstance(other, vec3):
            return vec3(self.x + other.x, self.y + other.y, self.z + other.z)
        raise ValueError("Can only add vec3 to vec3")

    def __sub__(self, other):
        if isinstance(other, vec3):
            return vec3(self.x - other.x, self.y - other.y, self.z - other.z)
        if isinstance(other, (int, float)):
            return vec3(self.x - other, self.y - other, self.z - other)
        raise ValueError("Unsupported operand type for subtraction")

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return vec3(self.x * other, self.y * other, self.z * other)
        if isinstance(other, vec3):
            return vec3(self.x * other.x, self.y * other.y, self.z * other.z)
        raise ValueError("Unsupported operand type for multiplication")

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return vec3(self.x / other, self.y / other, self.z / other)
        if isinstance(other, vec3):
            return vec3(self.x / other.x, self.y / other.y, self.z / other.z)
        raise ValueError("Unsupported operand type for division")

    def __getitem__(self, item):
        if isinstance(item, int):
            if item == 0:
                return self.x
            elif item == 1:
                return self.y
            elif item == 2:
                return self.z
        elif isinstance(item, str):
            if item == "x":
                return self.x
            elif item == "y":
                return self.y
            elif item == "z":
                return self.z
        raise KeyError(f"Invalid key: {item}")

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z

    def add(self, point):
        self.x += point.x
        self.y += point.y
        self.z += point.z
        return self

    def subtract(self, point):
        """Subtract from this point."""
        self.x -= point.x
        self.y -= point.y
        self.z -= point.z
        return self

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return (
            self.x * other.y - self.y * other.x,
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
        )

    def mul(self, v):
        return v.x * self.x + v.y * self.y + v.z * self.z

    def copy(self):
        """Creates a copy of this object."""
        return vec3(self.x, self.y, self.z)

    def angleBetween(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return math.sqrt(dx * dx + dy * dy + dz * dz)

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def distance(self, other):
        """Returns the distance between this point and another vector3."""
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2

    def equals(self, other):
        """Determine whether two objects are identical."""
        return self.x == other.x and self.y == other.y and self.z == other.z

    def intersects(self, other):
        pass

    def clone(self):
        """Returns a new instance of this vector3."""
        return vec3(self.x, self.y, self.z)

    def apply(self, point, amount):
        """Moves the points x,y,z by amount."""
        return vec3(
            point.x + amount.x,
            point.y + amount.y,
            point.z + amount.z,
        )

    # def __str__(self):
    #     return str(self.x) + " " + str(self.y) + " " + str(self.z)

    # def __repr__(self):
    #     return f"vec3({self.x}, {self.y}, {self.z})"

    def __eq__(self, other):
        if isinstance(other, vec3):
            return self.x == other.x and self.y == other.y and self.z == other.z
        return False
