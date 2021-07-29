"""
    domonic.geom
    ====================================

    much of this was written by.ai
    (https://6b.eleuther.ai/)

    most of this code was derivied by continually pasting back into eleuther

    # TODO - tests for all these new functions. sadly the ai didn't generate those.

"""
import math
from domonic.javascript import Math


class vec2():
    """[vec2]
    """

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __mul__(self, other):
        """[vec2] * [number] or [vec2] * [vec2]]

        Args:
            other ([vec2]): [multiply this vector by this vector or by a number]

        Returns:
            [vec2]: [new vector]
        """
        if isinstance(other, vec2):
            return self.__class__((self.x * other.x, self.y * other.y))
        else:
            return self.__class__((self.x * other, self.y * other))

    def __div__(self, other):
        if isinstance(other, vec2):
            return self.__class__((self.x / other.x, self.y / other.y))
        else:
            return self.__class__((self.x / other, self.y / other))

    def __mod__(self, other):
        if isinstance(other, vec2):
            return self.__class__(self.x % other.x, self.y % other.y)
        else:
            return self.__class__(self.x % other, self.y % other)

    def __getitem__(self, item):
        if isinstance(item, int):
            if item == 0:
                return self.x
            elif item == 1:
                return self.y
        elif isinstance(item, str):
            if item == 'x':
                return self.x
            elif item == 'y':
                return self.y

    def __len__(self):
        return 2

    def __add__(self, other):
        if isinstance(other, vec2):
            return vec2(self.x + other.x, self.y + other.y)
        else:
            return vec2(self.x + other, self.y + other)

    def __sub__(self, other):
        if isinstance(other, vec2):
            return vec2(self.x - other.x, self.y - other.y)
        else:
            return vec2(self.x - other, self.y - other)

    def __truediv__(self, other):
        if isinstance(other, vec2):
            return vec2(self.x / other.x, self.y / other.y)
        else:
            return vec2(self.x / other, self.y / other)

    def __floordiv__(self, other):
        if isinstance(other, vec2):
            return vec2(self.x // other.x, self.y // other.y)
        else:
            return vec2(self.x // other, self.y // other)

    def __neg__(self):
        return vec2(-self.x, -self.y)

    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y)

    def __ne__(self, other):
        return (self.x != other.x or self.y != other.y)

    def __lt__(self, other):
        return (self.x < other.x and self.y < other.y)

    def __le__(self, other):
        return (self.x <= other.x and self.y <= other.y)

    def __gt__(self, other):    
        return (self.x > other.x and self.y > other.y)

    def __ge__(self, other):
        return (self.x >= other.x and self.y >= other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError("Index out of range")

    def __iter__(self):
        yield self.x
        yield self.y

    def __call__(self, *args, **kwargs):
        return self.x, self.y

    def __getstate__(self):
        return self.x, self.y

    def __copy__(self):
        return vec2(self.x, self.y)

    def __deepcopy__(self, memo):
        return vec2(self.x, self.y)

    def __round__(self, n):
        return vec2(round(self.x, n), round(self.y, n))

    def __str__(self):
        return str(self.x) + " " + str(self.y)

    def add(self, pt):
        """ Adds a point to this point. returns new one """
        return vec2(self.x + pt.x, self.y + pt.y)

    def subtract(self, pt):
        """ Subtract from this point. returns new one """
        return vec2(self.x - pt.x, self.y - pt.y)

    def copy(self):
        """ Creates a copy of this Point object. """
        return vec2(self.x, self.y)

    def dot(self, other):
        """ Returns the dot product of these two vectors """
        x1 = self.x
        y1 = self.y
        x2 = other.x
        y2 = other.y
        return x1 * x2 + y1 * y2

    def cross(self, other):
        """ Returns the cross product of this and other. The cross product is considered 0
        perpendicular to each other point """
        x1 = self.x
        y1 = self.y
        x2 = other.x
        y2 = other.y
        return x1 * y2 - y1 * x2

    def negative(self):
        """ return vector but negative version """
        return vec2(-self.x, -self.y)

    def distance(self, other):
        x_dot = self.x - other.x
        y_dot = self.y - other.y
        return math.sqrt(x_dot * x_dot + y_dot * y_dot)

    def squareDistance(self, other):
        return self.distance(self) * self.distance(other)

    def equals(self, other):
        """ Returns true if all vectors components are the same """
        return (self.x == other.x and self.y == other.y)

    def interpolate(self, pt1, pt2, t):
        """ Calculates the point that would be reached by this Point
        if we moved by a given distance vector over time t.
        Only floats are handled here. """
        return vec2(self.x * (1 - t) + pt1.x * t, self.y * (1 - t) + pt1.y * t)

    def copyRotateAround(self, target, angle):
        """moves the vector then rotate"""
        self.rotateAround(target, angle)
        return vec2(self.x, self.y)

    def mirrorHorizontally(self):
        return self.rotateAround(vec2(1, 0), 90)

    def mirrorVertically(self):
        return self.rotateAround(vec2(0, 1), 90)

    def negate(self):
        """Negate a vector. This results in vector with the same direction but different length"""
        return vec2(-self.x, -self.y)

    def length(self):
        """ returns the length of this vector """
        return self.x

    def squaredlength(self):
        """ returns the squared length of this vector """
        return self.x * self.x + self.y * self.y

    def normalize(self):
        """ returns a normalized vector """
        return self / self.length()

    def obj(self):
        """ returns a obj representation of this vector """
        return {"x": self.x, "y": self.y}

    # def __repr__(self):
    #     return str(self.x) + " " + str(self.y)

    def json(self):
        """ returns a json representation of this vector """
        return str({"x": self.x, "y": self.y})

    def angle(self):
        """ returns the angle of this vector in radians """
        return math.atan2(self.y, self.x)

    def angleBetween(self, other):
        """ returns the angle between this and another vector in radians """
        return math.acos(self.dot(other) / (self.length() * other.length()))

    def rotate(self, angle):
        """ rotates this vector by an angle in radians """
        x = self.x
        y = self.y
        self.x = x * math.cos(angle) - y * math.sin(angle)
        self.y = y * math.cos(angle) + x * math.sin(angle)

    def rotateAround(self, target, angle):
        """Rotates the vector around another point. In fact it returns the other point."""
        dot = self.dot(target)
        s = math.sin(angle / 2)
        c = math.cos(angle / 2)
        x = s * (self.x - dot * c) + c
        y = s * (self.y - dot * c) - c
        return vec2(x, y)

    @staticmethod
    def cmp(a, b):
        """ Compare two vectors. """
        return (a > b) - (a < b)

    # @staticmethod
    # def random():
    #     """ returns a random vector """
    #     return vec2(random.random(), random.random())

    @staticmethod
    def random(min_x, max_x, min_y, max_y):
        """ returns a random vector """
        import random
        return vec2(random.uniform(min_x, max_x), random.uniform(min_y, max_y))

    @staticmethod
    def random_unit_vector(min_x, max_x, min_y, max_y):
        """ returns a random unit vector """
        vec = vec2.random(min_x, max_x, min_y, max_y)
        return vec.normalize()

    @staticmethod
    def random_point_in_circle(center, radius):
        """ returns a random point in a circle """
        vec = vec2.random(0, radius)
        return vec.add(center)

    @staticmethod
    def random_point_in_rectangle(min_x, max_x, min_y, max_y):
        """ returns a random point in a rectangle """
        vec = vec2.random(min_x, max_x, min_y, max_y)
        return vec.add(vec2.random(0, 1))



    # def rotateAround(self, target, angle):
    #     """ Rotates the vector around another point. In fact it returns the other point."""
    #     dot = self.dot(target)
    #     s = math.sin(angle)
    #     c = math.cos(angle)
    #     x = s * (self.x - dot * c) + c
    #     y = s * (self.y - dot * c) - c
    #     return vec2(x, y)

    # def rotateAroundLocal(self, point, angle):
    #     """ Rotates the vector around a point. In fact it returns itself."""
    #     dot = self.dot(point)
    #     s = math.sin(angle)
    #     c = math.cos(angle)
    #     x = s * (self.x - dot * c) + c
    #     y = s * (self.y - dot * c) - c
    #     return vec2(x, y)

    # def rotateLocal(self, point, angle):
    #     """ Rotates the vector around a point. In fact it returns itself."""
    #     dot = self.dot(point)
    #     s = math.sin(angle)
    #     c = math.cos(angle)
    #     x = s * (self.x - dot * c) + c
    #     y = s * (self.y - dot * c) - c
    #     self.x = x
    #     self.y = y
    #     return self
