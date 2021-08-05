"""
    domonic.d3.geom.shape
    ====================================

"""

from domonic.geom import vec2
from domonic.svg import *

class vertex(vec2):
    """
    A vertex is a point in the shape.
    """

    # def __init__(self, x=0, y=0):
    #     self.x = x
    #     self.y = y

    def move_to(self, position):
        x, y = position
        self.x = x
        self.y = y

    def move_by(self, dx, dy):
        self.x += dx
        self.y += dy

    # def __str__(self):
    #     return '{} {} {}'.format(self.x, self.y, self.color)

    # def __repr__(self):
    #     return '{} {} {}'.format(self.x, self.y, self.color)

Point = vertex


class Shape(Point):

    def __init__(self, x=0, y=0, color='red', vertices=[]):
        super().__init__(x, y)

        if isinstance(vertices, list):
            self.vertices = vertices

        self.color = color
        self.scale = 1
        self.rotation = 0
        # self.pivot = (0, 0)
        self.id = None
        self.name = None
        self.style = None
        self.locked = False
        self.visible = True
        self.selected = False
        self.clipMask = None
        self.data = None
        self.blendMode = None
        self.opacity = 1.0
        self.strokeColor = None
        self.strokeWidth = 1
        # self.strokeCap = 'butt'
        # self.strokeJoin = 'miter'
        # self.dashOffset = 0
        # self.strokeScaling = 1.0
        # self.dashArray = None
        # self.miterLimit = None
        # self.fillColor = None
        self.shadowColor = None
        self.shadowBlur = None
        self.shadowOffset = None
        self.shadowOpacity = None
        # self.vertcies = []
        # self.width = None
        # self.height = None

    @property
    def position(self):
        return vec2(self.x, self.y)

    @position.setter
    def position(self, pos):
        self.x = pos.x
        self.y = pos.y

    @property
    def width(self):
        """ determine the width of the shape """
        return max(self.vertices, key=lambda v: v.x).x - min(self.vertices, key=lambda v: v.x).x

    @property
    def height(self):
        """ determine the height of the shape """
        return max(self.vertices, key=lambda v: v.y).y - min(self.vertices, key=lambda v: v.y).y

    def rotate(self, angle):
        """ rotate the shape """
        self.rotation += angle

    def draw(self, svg):
        """ draw the shape """
        if self.visible:
            svg.add(svg.polyline(self.vertices, id=self.id, class_=self.name, style=self.style,
                                 fill=self.color, stroke=self.strokeColor, stroke_width=self.strokeWidth,
                                 opacity=self.opacity, fill_opacity=self.opacity,
                                 fill_rule='evenodd'))

    def __len__(self):
        return len(self.vertices)

    def __getitem__(self, index):
        return self.vertices[index]

    def __setitem__(self, index, value):
        self.vertices[index] = value

    def __delitem__(self, index):
        del self.vertices[index]

    def __iter__(self):
        return iter(self.vertices)

    def __reversed__(self):
        return reversed(self.vertices)

    def __contains__(self, item):
        return item in self.vertices

    def __add__(self, other):
        """ add two shapes """
        if isinstance(other, Shape):
            return self.vertices + other.vertices

    # def matrix
    # def clear
    # def pivot
    # def bounds

    # def rasterize(self, rasterizer):
    #     """ rasterize the shape """
    #     pass

    # def contains(self, point):
    #     """ check if the point is inside the shape """
    #     pass

    # def isInside(self, rect):
    #     """ check if the rect is inside the shape """
    #     pass

    # def intersects(item):
    #     """ check if the shape intersects with another """
    #     pass

    # @property
    # def x(self):
    #     return self.__x

    # @x.setter
    # def x(self, x):
    #     self.__x = x

    # @property
    # def y(self):
    #     return self.__y

    # @y.setter
    # def y(self, y):
    #     self.__y = y



class Line(Shape):

    def __init__(self, p1, p2, color=None, *args):
        super().__init__(color)
        # if isinstance(p1, vec2):
        self.p1 = p1
        self.p2 = p2
        self.x = self.p1[0] - self.p2[0]
        self.y = self.p1[1] - self.p2[1]

    def __str__(self):
        return "Line(%s, %s)" % (self.p1, self.p2)

    # def __repr__(self):
    #     return "Line(%s, %s)" % (self.p1, self.p2)

    def __eq__(self, other):
        return self.p1 == other.p1 and self.p2 == other.p2

    def __ne__(self, other):
        return self.p1 != other.p1 or self.p2 != other.p2

    def __hash__(self):
        return hash((self.p1, self.p2))

    def __iter__(self):
        return iter((self.p1, self.p2))

    # def __len__(self):
    #     return 2

    def __getitem__(self, index):
        return (self.p1, self.p2)[index]

    def __setitem__(self, index, value):
        if index == 0:
            self.p1 = value

    def __delitem__(self, index):
        if index == 0:
            self.p1 = None

    def __contains__(self, item):
        return item in (self.p1, self.p2)

    def __add__(self, other):
        return Line(self.p1, other.p2)

    def __sub__(self, other):# self - other
        return Line(self.p1, other.p1)

    def __mul__(self, other):
        return Line(self.p1, other.p2)

    def __rmul__(self, other):
        return Line(self.p1, other.p2)

    def __neg__(self):
        return Line(self.p1, self.p2)

    def __pos__(self):
        return Line(self.p1, self.p2)

    def __abs__(self):
        return Line(self.p1, self.p2)

    # def __bool__(self):
    #     return bool(self.p1 and self.p2)

    # def __nonzero__(self):
    #     return bool(self.p1 and self.p2)

    # def __call__(self, p):
    #     return Line(self.p1, p)

    # def __getattr__(self, name):
    #     if name == 'p1':
    #         return self.p1
    #     elif name == 'p2':
    #         return self.p2
    #     else:
    #         raise AttributeError(name)

    # def __setattr__(self, name, value):
    #     if name == 'p1':
    #         self.p1 = value

    # def __delattr__(self, name):
    #     if name == 'p1':
    #         self.p1 = None
    #     elif name == 'p2':
    #         self.p2 = None
    #     else:
    #         raise AttributeError(name)

    # def __getinitargs__(self):
    #     return (self.p1, self.p2)

    # def __setstate__(self, state):
    #     self.p1 = state['p1']
    #     self.p2 = state['p2']

    def __getstate__(self):
        return {'p1': self.p1, 'p2': self.p2}

    def __reduce__(self):
        return (Line, (self.p1, self.p2))

    def __reduce_ex__(self, protocol):
        return self.__reduce__()

    def __copy__(self):
        return Line(self.p1, self.p2)

    def __deepcopy__(self, memo):
        return Line(self.p1, self.p2)

    def __bool__(self):
        return bool(self.p1 and self.p2)

    def __nonzero__(self):
        return bool(self.p1 and self.p2)


class Plane():

    def __init__(self, normal, distance, color=None, *args):
        """[a plane is defined by its normal vector and a distance from the origin]

        Args:
            normal ([vec2]): [a vector representing the normal vector of the plane]
            distance ([type]): [a scalar representing the distance from the origin]
            color ([vec3], optional): [the color of the plane]
        """
        self.normal = normal
        self.distance = distance
        self.color = color

    def __str__(self):
        return "Plane(%s, %s)" % (self.normal, self.distance)

    # def __repr__(self):
    #     return "Plane(%s, %s)" % (self.normal, self.distance)

    def __eq__(self, other):
        return self.normal == other.normal and self.distance == other.distance

    # def bisectors(self):
    #     return self.normal.cross(self.distance)

    # def with_distance(self, distance):
    #     return Plane(self.normal, distance)

    # def with_normal(self, normal):
    #     return Plane(normal, self.distance)


class Rect(Shape):
    def __init__(self, x=0, y=0, width=1, height=1, color=None):
        super().__init__(color)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, w):
        self._width = w

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, w):
        self._height = w

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

    def get_top_right(self):
        t = self.x + self.width
        b = super().get_bottom_right()
        return (t, b[1])

    def get_center(self):
        c = self.x + self.width / 2
        t = self.y + self.height / 2
        return (c, t)

    def get_center_x(self):
        c = self.x + self.width / 2
        return c

    def get_center_y(self):
        c = self.y + self.height / 2
        return c

    def get_left(self):
        return self.x

    def get_right(self):
        return self.x + self.width

    def get_top(self):
        return self.y

    def get_bottom(self):
        return self.y + self.height

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def __str__(self):
        return "Rect(%s, %s, %s, %s)" % (self.x, self.y, self.width, self.height)

    # def __repr__(self):
    #     return "Rect(%s, %s, %s, %s)" % (self.x, self.y, self.width, self.height)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.width == other.width and self.height == other.height

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y or self.width != other.width or self.height != other.height

    def __hash__(self):
        return hash((self.x, self.y, self.width, self.height))

    def __iter__(self):
        return iter((self.x, self.y, self.width, self.height))

    def __len__(self):
        return 4

    def __getitem__(self, index):
        return (self.x, self.y, self.width, self.height)[index]

    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        elif index == 2:
            self.width = value
        elif index == 3:
            self.height = value

    def __add__(self, other):
        return Rect(self.x + other.x, self.y + other.y, self.width + other.width, self.height + other.height)

    def __sub__(self, other):
        return Rect(self.x - other.x, self.y - other.y, self.width - other.width, self.height - other.height)

    def __mul__(self, other):
        return Rect(self.x * other, self.y * other, self.width * other, self.height * other)

    def __truediv__(self, other):
        return Rect(self.x / other, self.y / other, self.width / other, self.height / other)

    def __floordiv__(self, other):
        return Rect(self.x // other, self.y // other, self.width // other, self.height // other)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.width += other.width
        self.height += other.height
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.width -= other.width
        self.height -= other.height
        return self

    def __imul__(self, other):
        self.x *= other
        self.y *= other
        self.width *= other
        self.height *= other
        return self

    def __idiv__(self, other):
        self.x /= other
        self.y /= other
        self.width /= other
        self.height /= other
        return self

    def __ifloordiv__(self, other):
        self.x //= other
        self.y //= other
        self.width //= other
        self.height //= other
        return self

    # def __getstate__(self):
        # return {'x': self.x, 'y': self.y, 'width': self.width, 'height': self.height}

    # def __setstate__(self, state):
    #     self.x = state['x']
    #     self.y = state['y']
    #     self.width = state['width']
    #     self.height = state['height']

    def __reduce__(self):
        return (Rect, (self.x, self.y, self.width, self.height))

    def __copy__(self):
        return Rect(self.x, self.y, self.width, self.height)

    def __deepcopy__(self, memo):
        return Rect(self.x, self.y, self.width, self.height)

    def __contains__(self, other):
        return self.x <= other.x and self.y <= other.y and self.x + self.width >= other.x + other.width and self.y + self.height >= other.y + other.height

    def __lt__(self, other):
        return self.x < other.x and self.y < other.y and self.width < other.width and self.height < other.height

    def __le__(self, other):
        return self.x <= other.x and self.y <= other.y and self.width <= other.width and self.height <= other.height

    def __gt__(self, other):
        return self.x > other.x and self.y > other.y and self.width > other.width and self.height > other.height

    def __ge__(self, other):
        return self.x >= other.x and self.y >= other.y and self.width >= other.width and self.height >= other.height

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.width == other.width and self.height == other.height

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y or self.width != other.width or self.height != other.height

    def __hash__(self):
        return hash((self.x, self.y, self.width, self.height))


class Square(Rect):
    def __init__(self, x=0, y=0, size=1.0, color=None):
        super().__init__(x, y, size, size, color)

    def get_size(self):
        return self.width

    def set_size(self, size):
        self.width = size
        self.height = size

    def __str__(self):
        return "Square(%s, %s, %s)" % (self.x, self.y, self.width)

    # def __repr__(self):
    #     return "Square(%s, %s, %s)" % (self.x, self.y, self.width)

    # def __getstate__(self):
    #     return {'x': self.x, 'y': self.y, 'size': self.width, 'color': self.color}

    # def __setstate__(self, state):
    #     self.x = state['x']
    #     self.y = state['y']
    #     self.width = state['size']
    #     self.height = state['size']
    #     self.color = state['color']

    # def __reduce__(self):
    #     return (Square, (self.x, self.y, self.width, self.color))

    def __copy__(self):
        return Square(self.x, self.y, self.width, self.color)

    def __deepcopy__(self, memo):
        return Square(self.x, self.y, self.width, self.color)

    def __contains__(self, other):
        return self.x <= other.x and self.y <= other.y and self.x + self.width >= other.x + other.width and self.y + self.height >= other.y + other.height

    def get_vertices(self, x=None, y=None):
        if x is None:
            x = self.x
        if y is None:
            y = self.y
        return [
            (x, y),
            (x + self.width, y),
            (x + self.width, y + self.height),
            (x, y + self.height),
        ]

    def get_vertices_list(self):
        return [
            (self.x, self.y),
            (self.x + self.width, self.y),
            (self.x + self.width, self.y + self.height),
            (self.x, self.y + self.height),
        ]

    def svg(self, x=None, y=None):
        if x is None:
            x = self.x
        if y is None:
            y = self.y
        return '<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (x, y, self.width, self.height, self.color)

    # def draw_to_canvas(self, canvas):
    #     canvas.draw_rect(self.x, self.y, self.width, self.height, self.color)


class Polygon(Shape):
    def __init__(self, points):
        super().__init__()
        self.points = points

    def get_points(self):
        return self.points

    def set_points(self, points):
        self.points = points

    def __str__(self):
        return "Polygon(%s)" % (self.points)

    # def __repr__(self):
    #     return "Polygon(%s)" % (self.points)


class Polyline(Shape):
    def __init__(self, points):
        super().__init__()
        self.points = points

    def get_points(self):
        return self.points

    def set_points(self, points):
        self.points = points

    def __str__(self):
        return "Polyline(%s)" % (self.points)

    # def __repr__(self):
    #     return "Polyline(%s)" % (self.points)

    def __getstate__(self):
        return {'points': self.points}

    def __setstate__(self, state):
        self.points = state['points']

    def __reduce__(self):
        return (Polyline, (self.points,))

    def __copy__(self):
        return Polyline(self.points)

    def __deepcopy__(self, memo):
        return Polyline(self.points)

    def __contains__(self, other):
        return other in self.points

    def __len__(self):
        return len(self.points)

    def __getitem__(self, key):
        return self.points[key]

    def __setitem__(self, key, value):
        self.points[key] = value

    def __iter__(self):
        return iter(self.points)

    def __add__(self, other):
        return Polyline(self.points + other.points)

    def __sub__(self, other):
        return Polyline(self.points - other.points)

    def __mul__(self, other):
        return Polyline(self.points * other)

    def __rmul__(self, other):
        return Polyline(other * self.points)

    def __floordiv__(self, other):
        return Polyline(self.points // other)

    def __mod__(self, other):
        return Polyline(self.points % other)

    def __divmod__(self, other):
        return Polyline(divmod(self.points, other))

    def __pow__(self, other):
        return Polyline(self.points ** other)

    def __lshift__(self, other):
        return Polyline(self.points << other)

    def __rshift__(self, other):
        return Polyline(self.points >> other)

    def __and__(self, other):
        return Polyline(self.points & other)

    def __xor__(self, other):
        return Polyline(self.points ^ other)

    def __or__(self, other):
        return Polyline(self.points | other)

    def __iadd__(self, other):
        self.points += other.points
        return self

    def __isub__(self, other):
        self.points -= other.points
        return self

    def __imul__(self, other):
        self.points *= other
        return self 

    def __imod__(self, other):
        self.points %= other
        return self

    def __idivmod__(self, other):
        self.points //= other
        return self

    def __ipow__(self, other):
        self.points **= other

    def __ilshift__(self, other):
        self.points <<= other

    def __irshift__(self, other):
        self.points >>= other
        return self

    def __iand__(self, other):
        self.points &= other

    def __ixor__(self, other):
        self.points ^= other

    def __ior__(self, other):
        self.points |= other
        return self

    def __neg__(self):
        return Polyline(-self.points)

    def __pos__(self):
        return Polyline(self.points)

    def __abs__(self):
        return Polyline(abs(self.points))

    def __invert__(self):
        return Polyline(~self.points)

    # def __complex__(self):
    #     return complex(self.points)

    def __int__(self):
        return int(self.points)

    def __float__(self):
        return float(self.points)

    def __round__(self):
        return round(self.points)

    # def __reversed__(self):
    #     return Polyline(reversed(self.points))


# class Quad(Shape):
#     def __init__(self, left=Rect(), right=Rect(), front=Rect(), back=Rect()):
#         super().__init__(color='blue')
#         self.left, self.right, self.front, self.back = left, right, front, back

# class Triangle(Shape):
#     def __init__(self):
#         super().__init__(self.color='blue')


# class Wave():

#     def __init__(self, color=None, *args):
#         self.color = color





from domonic.geom.shape.shapes import Circle
from domonic.geom.shape.shapes import Oval
# from domonic.geom.shape.circle import Elipse
