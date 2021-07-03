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

    def add(self, pt):
        """ Adds a point to this point. returns new one """
        return vec2(self.x + pt.x, self.y + pt.y)

    def __add__(self, other):
        self.add(other)

    def subtract(self, pt):
        """ Subtract from this point. returns new one """
        return vec2(self.x - pt.x, self.y - pt.y)

    def __sub__(self, other):
        if isinstance(other, vec2):
            return self.x - other.x and self.y - other.y
        else:
            return self.x - other and self.y - other

    def __eq__(self, other):
        if isinstance(other, vec2):
            return self.x == other.x and self.y == other.y
        else:
            return self.x == other and self.y == other

    def __ne__(self, other):
        if isinstance(other, vec2):
            return self.x != other.x or self.y != other.y
        else:
            return self.x != other and self.y != other

    def __gt__(self, other):
        if isinstance(other, vec2):
            return self.x > other.x or self.y > other.y
        else:
            return self.x > other and self.y > other

    def __ge__(self, other):
        if isinstance(other, vec2):
            return self.x >= other.x or self.y >= other.y
        else:
            return self.x >= other and self.y >= other

    def __lt__(self, other):
        if isinstance(other, vec2):
            return self.x < other.x or self.y < other.y
        else:
            return self.x < other and self.y < other

    def __le__(self, other):
        if isinstance(other, vec2):
            return self.x <= other.x or self.y <= other.y
        else:
            return self.x <= other and self.y <= other

    def __mul__(self, other):
        if isinstance(other, vec2):
            return self.__class__((self.x * other.x, self.y * other.y))
        else:
            return self.__class__((self.x * other, self.y * other))

    def __truediv__(self, other):
        if isinstance(other, vec2):
            return self.__class__((self.x / other.x, self.y / other.y))
        else:
            return self.__class__((self.x / other, self.y / other))

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

    def rotateAround(self, target, angle):
        """Rotates the vector around another point. In fact it returns the other point."""
        dot = self.dot(target)
        s = math.sin(angle / 2)
        c = math.cos(angle / 2)
        x = s * (self.x - dot * c) + c
        y = s * (self.y - dot * c) - c
        return vec2(x, y)

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

    def __str__(self):
        return str(self.x) + " " + str(self.y)


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


class vec4():
    """[vec2]
    """

    def __init__(self, x=0, y=0, z=0, w=0, n=1):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.n = n

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


class matrix(object):
    """[matrixs]
    """

    def __init__(self, m):
        self.m = m

    def translate(self, pt):
        """ Translates the point on the vector defined by the vectors m[0] and m[1]."""
        return vec2(self.m[0][0], self.m[0][1]) + pt - self.m[0][0]


# class Quaternion():

class vertex(object):
    
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def move_to(self, position):
        x, y = position
        self.x = x
        self.y = y


Point = vertex


class Shape(Point):

    def __init__(self, x=0, y=0, color='red'):
        super().__init__(x, y)
        self.color = color
        # self.id
        # self.name
        # self.style
        # self.locked
        # self.visible
        # self.blendMode
        # self.opacity
        # self.selected
        # self.clipMask
        # self.data

        # self.strokeColor
        # self.strokeWidth
        # self.strokeCap
        # self.strokeJoin
        # self.dashOffset
        # self.strokeScaling
        # self.dashArray
        # self.miterLimit

        # self.fillColor

        # self.shadowColor
        # self.shadowBlur
        # self.shadowOffset

    # def scale_to(self, scale):
        # self.size *= scale

    # def draw(self):
    # def clear(self):

    @property
    def position(self):
        return Point(self.x, self.y)

    # def pivot
    # def bounds
    # def strokeBounds
    # def handleBounds
    # def internalBounds
    # def rotation
    # def scaling
    # def matrix
    # def globalMatrix
    # def viewMatrix
    # def applyMatrix

    # def rasterize()

    # def contains(point)
    # def isInside(rect)
    # def intersects(item)


class Line(Shape):
    def __init__(self, p1, p2, color=None):
        super().__init__(color)
        self.p1 = p1
        self.p2 = p2
        self.x = self.p1[0] - self.p2[0]
        self.y = self.p1[1] - self.p2[1]


class Rect(Shape):
    def __init__(self, x=0, y=0, width=1, height=1, color=None):
        super().__init__(color)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_bottom_right(self):
        d = self.x + self.width
        t = self.y + self.height
        return (d, t)

    def get_bottom_left(self):
        b = self.get_bottom_right()
        l = super().get_bottom_right()
        return (b[0], l[0])

    def get_top_left(self):
        t = self.x
        b = super().get_bottom_right()
        return (t, b[1])


class Square(Rect):
    def __init__(self, x=0, y=0, size=1.0, color=None):
        super().__init__(x, y, size, size, color)


class Polygon(Shape):
    def __init__(self, points):
        super().__init__()
        self.points = points


class Polyline(Shape):
    def __init__(self, points):
        super().__init__()
        self.points = points


# class Quad(Shape):
#     def __init__(self, left=Rect(), right=Rect(), front=Rect(), back=Rect()):
#         super().__init__(color='blue')
#         self.left, self.right, self.front, self.back = left, right, front, back

# class Triangle(Shape):
#     def __init__(self):
#         super().__init__(self.color='blue')


class Circle(Shape):

    def __init__(self, x, y, radius=1.0, color=None):
        super().__init__(color)
        self.radius = radius  # Create an instance variable radius

    @property
    def area(self):
        return self.radius * self.radius * Math.PI

    @property
    def perimeter(self):
        return 2 * self.radius * Math.PI

    @property
    def average_circumference(self):
        return 2 * self.radius

    @property
    def center(self):
        x, y = self.center = [self.radius, self.radius]
        return x, y


class Oval(Circle):
    def __init__(self, radius=2.5, size=3):
        super().__init__(size, 'green')
        self.radius = radius
        self.x = self.width / 2 - self.radius / 2
        self.y = self.width / 2 + self.radius / 2


class Ellipse(Shape):
    def __init__(self, x, y, width, height, color=None):
        super().__init__(color)
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class Plotter(object):
    def __init__(self, canvas=None):
        self.canvas = canvas  # or canvas.Canvas('Example Plotter', 500, 500)
        self.points = []
        self.starting_color = (255, 255, 255)
        self.color = self.starting_color
        self.clear()

    def add_point(self, point):
        self.points.append(point)

    # def clear(self):
    #     pass


# class Path(object):
# class Cursor(object):
# class Group(object):
# class Layer(object):


# class Interactive(object):#??
    # def handle_click_event(self):

    # onFrame
    # onMouseDown
    # onMouseDrag
    # onMouseUp
    # onClick
    # onDoubleClick
    # onMouseMove
    # onMouseEnter
    # onMouseLeave
