"""
domonic.geom.vec3
====================================

"""

import math


class vec3:
    """vec3"""

    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x: float = x
        self.y: float = y
        self.z: float = z

    def __add__(self, other):
        if isinstance(other, vec3):
            return vec3(self.x + other.x, self.y + other.y, self.z + other.z)
        if isinstance(other, (int, float)):
            return vec3(self.x + other, self.y + other, self.z + other)
        raise ValueError("Unsupported operand type for addition")

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, vec3):
            return vec3(self.x - other.x, self.y - other.y, self.z - other.z)
        if isinstance(other, (int, float)):
            return vec3(self.x - other, self.y - other, self.z - other)
        raise ValueError("Unsupported operand type for subtraction")

    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            return vec3(other - self.x, other - self.y, other - self.z)
        raise ValueError("Unsupported operand type for subtraction")

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return vec3(self.x * other, self.y * other, self.z * other)
        if isinstance(other, vec3):
            return vec3(self.x * other.x, self.y * other.y, self.z * other.z)
        raise ValueError("Unsupported operand type for multiplication")

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return vec3(self.x / other, self.y / other, self.z / other)
        if isinstance(other, vec3):
            return vec3(self.x / other.x, self.y / other.y, self.z / other.z)
        raise ValueError("Unsupported operand type for division")

    def __floordiv__(self, other):
        if isinstance(other, (int, float)):
            return vec3(self.x // other, self.y // other, self.z // other)
        if isinstance(other, vec3):
            return vec3(self.x // other.x, self.y // other.y, self.z // other.z)
        raise ValueError("Unsupported operand type for division")

    def __neg__(self):
        return vec3(-self.x, -self.y, -self.z)

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

    def __setitem__(self, key, value):
        if key in (0, "x"):
            self.x = value
        elif key in (1, "y"):
            self.y = value
        elif key in (2, "z"):
            self.z = value
        else:
            raise KeyError(f"Invalid key: {key}")

    def __len__(self):
        return 3

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __call__(self):
        return self.x, self.y, self.z

    def __iadd__(self, other):
        if isinstance(other, vec3):
            self.x += other.x
            self.y += other.y
            self.z += other.z
        elif isinstance(other, (int, float)):
            self.x += other
            self.y += other
            self.z += other
        else:
            raise ValueError("Unsupported operand type for addition")
        return self

    def __isub__(self, other):
        if isinstance(other, vec3):
            self.x -= other.x
            self.y -= other.y
            self.z -= other.z
        elif isinstance(other, (int, float)):
            self.x -= other
            self.y -= other
            self.z -= other
        else:
            raise ValueError("Unsupported operand type for subtraction")
        return self

    def __imul__(self, other):
        if isinstance(other, vec3):
            self.x *= other.x
            self.y *= other.y
            self.z *= other.z
        elif isinstance(other, (int, float)):
            self.x *= other
            self.y *= other
            self.z *= other
        else:
            raise ValueError("Unsupported operand type for multiplication")
        return self

    def __itruediv__(self, other):
        if isinstance(other, vec3):
            self.x /= other.x
            self.y /= other.y
            self.z /= other.z
        elif isinstance(other, (int, float)):
            self.x /= other
            self.y /= other
            self.z /= other
        else:
            raise ValueError("Unsupported operand type for division")
        return self

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
        return vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def mul(self, v):
        return v.x * self.x + v.y * self.y + v.z * self.z

    def copy(self):
        """Creates a copy of this object."""
        return vec3(self.x, self.y, self.z)

    def angleBetween(self, other):
        length_product = self.length() * other.length()
        if length_product == 0:
            raise ValueError("Cannot calculate an angle with a zero-length vector")
        cosine = self.dot(other) / length_product
        cosine = max(-1, min(1, cosine))
        return math.acos(cosine)

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def squaredLength(self):
        return self.x * self.x + self.y * self.y + self.z * self.z

    def normalize(self):
        length = self.length()
        if length == 0:
            return vec3()
        return self / length

    def distance(self, other):
        """Returns the distance between this point and another vector3."""
        return math.sqrt(self.distanceSquared(other))

    def distanceSquared(self, other):
        """Returns the squared distance between this point and another vector3."""
        return (
            (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2
        )

    squareDistance = distanceSquared

    def equals(self, other):
        """Determine whether two objects are identical."""
        return self.x == other.x and self.y == other.y and self.z == other.z

    def intersects(self, other, tolerance=0):
        """Returns True when another vector is at the same point."""
        if not isinstance(other, vec3):
            return False
        tolerance = max(0, float(tolerance))
        return self.distanceSquared(other) <= tolerance * tolerance

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

    def obj(self):
        """Returns a dict representation of this vector."""
        return {"x": self.x, "y": self.y, "z": self.z}

    def json(self):
        """Returns a string representation compatible with the old vec helpers."""
        return str(self.obj())

    def __str__(self):
        return str(self.x) + " " + str(self.y) + " " + str(self.z)

    def __repr__(self):
        return f"vec3({self.x}, {self.y}, {self.z})"

    def __eq__(self, other):
        if isinstance(other, vec3):
            return self.x == other.x and self.y == other.y and self.z == other.z
        return False

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.x, self.y, self.z))
