"""
    domonic.geom.shape
    ====================================

"""

from domonic.geom.vec2 import vec2
from domonic.svg import *
from domonic.javascript import Math

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
    def __init__(self, x=0, y=0, color="red", vertices=[]):
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
        """determine the width of the shape"""
        return max(self.vertices, key=lambda v: v.x).x - min(self.vertices, key=lambda v: v.x).x

    @property
    def height(self):
        """determine the height of the shape"""
        return max(self.vertices, key=lambda v: v.y).y - min(self.vertices, key=lambda v: v.y).y

    def rotate(self, angle):
        """rotate the shape"""
        self.rotation += angle

    def draw(self, svg):
        """draw the shape"""
        if self.visible:
            svg.add(
                svg.polyline(
                    self.vertices,
                    id=self.id,
                    class_=self.name,
                    style=self.style,
                    fill=self.color,
                    stroke=self.strokeColor,
                    stroke_width=self.strokeWidth,
                    opacity=self.opacity,
                    fill_opacity=self.opacity,
                    fill_rule="evenodd",
                )
            )

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
        """add two shapes"""
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
    def __init__(self, start, end, color=None, *args):
        super().__init__(color)
        # if isinstance(p1, vec2):
        self.start = start
        self.end = end
        self.x = self.start[0] - self.end[0]
        self.y = self.start[1] - self.end[1]

    def __str__(self):
        return f"Line({self.start}, {self.end})"

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __ne__(self, other):
        return self.start != other.start or self.end != other.end

    def __hash__(self):
        return hash((self.start, self.end))

    def __iter__(self):
        return iter((self.start, self.end))

    # def __len__(self):
    #     return 2

    def __getitem__(self, index):
        return (self.start, self.end)[index]

    def __setitem__(self, index, value):
        if index == 0:
            self.start = value

    def __delitem__(self, index):
        if index == 0:
            self.start = None

    def __contains__(self, item):
        return item in (self.start, self.end)

    def __add__(self, other):
        return Line(self.start, other.end)

    def __sub__(self, other):  # self - other
        return Line(self.start, other.start)

    def __mul__(self, other):
        return Line(self.start, other.end)

    def __rmul__(self, other):
        return Line(self.start, other.end)

    def __neg__(self):
        return Line(self.start, self.end)

    def __pos__(self):
        return Line(self.start, self.end)

    def __abs__(self):
        return Line(self.start, self.end)

    # def __bool__(self):
    #     return bool(self.start and self.end)

    # def __nonzero__(self):
    #     return bool(self.start and self.end)

    # def __call__(self, p):
    #     return Line(self.start, p)

    # def __getattr__(self, name):
    #     if name == 'p1':
    #         return self.start
    #     elif name == 'p2':
    #         return self.end
    #     else:
    #         raise AttributeError(name)

    # def __setattr__(self, name, value):
    #     if name == 'p1':
    #         self.start = value

    # def __delattr__(self, name):
    #     if name == 'p1':
    #         self.start = None
    #     elif name == 'p2':
    #         self.end = None
    #     else:
    #         raise AttributeError(name)

    # def __getinitargs__(self):
    #     return (self.start, self.end)

    # def __setstate__(self, state):
    #     self.start = state['p1']
    #     self.end = state['p2']

    def __getstate__(self):
        return {"p1": self.start, "p2": self.end}

    def __reduce__(self):
        return (Line, (self.start, self.end))

    def __reduce_ex__(self, protocol):
        return self.__reduce__()

    def __copy__(self):
        return Line(self.start, self.end)

    def __deepcopy__(self, memo):
        return Line(self.start, self.end)

    def __bool__(self):
        return bool(self.start and self.end)

    def __nonzero__(self):
        return bool(self.start and self.end)


class Plane:
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
        return f"Plane({self.normal}, {self.distance})"

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
        return f"Rect({self.x}, {self.y}, {self.width}, {self.height})"

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
        return Rect(
            self.x + other.x,
            self.y + other.y,
            self.width + other.width,
            self.height + other.height,
        )

    def __sub__(self, other):
        return Rect(
            self.x - other.x,
            self.y - other.y,
            self.width - other.width,
            self.height - other.height,
        )

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
        return (
            self.x <= other.x
            and self.y <= other.y
            and self.x + self.width >= other.x + other.width
            and self.y + self.height >= other.y + other.height
        )

    def __lt__(self, other):
        return self.x < other.x and self.y < other.y and self.width < other.width and self.height < other.height

    def __le__(self, other):
        return self.x <= other.x and self.y <= other.y and self.width <= other.width and self.height <= other.height

    def __gt__(self, other):
        return self.x > other.x and self.y > other.y and self.width > other.width and self.height > other.height

    def __ge__(self, other):
        return self.x >= other.x and self.y >= other.y and self.width >= other.width and self.height >= other.height

    # def __eq__(self, other):
    #     return self.x == other.x and self.y == other.y and self.width == other.width and self.height == other.height

    # def __ne__(self, other):
    #     return self.x != other.x or self.y != other.y or self.width != other.width or self.height != other.height

    # def __hash__(self):
    #     return hash((self.x, self.y, self.width, self.height))


class Square(Rect):
    def __init__(self, x=0, y=0, size=1.0, color=None):
        super().__init__(x, y, size, size, color)

    def get_size(self):
        return self.width

    def set_size(self, size):
        self.width = size
        self.height = size

    def __str__(self):
        return f"Square({self.x}, {self.y}, {self.width})"

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
        return (
            self.x <= other.x
            and self.y <= other.y
            and self.x + self.width >= other.x + other.width
            and self.y + self.height >= other.y + other.height
        )

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
        return f'<rect x="{x}" y="{y}" width="{self.width}" height="{self.height}" fill="{self.color}"/>'

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
        return f"Polygon({(self.points)})"


class Polyline(Shape):
    def __init__(self, points):
        super().__init__()
        self.points = points

    def get_points(self):
        return self.points

    def set_points(self, points):
        self.points = points

    def __str__(self):
        return f"Polyline({(self.points)})"

    def __getstate__(self):
        return {"points": self.points}

    def __setstate__(self, state):
        self.points = state["points"]

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
        return Polyline(self.points**other)

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


class Circle(Shape):
    def __init__(self, x: float, y: float, radius: float = 1.0, color=None) -> None:
        """[Circle(x, y, radius=1.0, color=None)]

        Args:
            x ([float]): [the x coordinate of the center of the circle]
            y ([float]): [the y coordinate of the center of the circle]
            radius (float, optional): [description]. Defaults to 1.0.
            color ([type], optional): [description]. Defaults to None.
        """
        super().__init__(color)
        self.radius = radius  # Create an instance variable radius

    @property
    def area(self) -> float:
        """[area]

        Returns:
            [float]: [the area of the circle]
        """
        return self.radius * self.radius * Math.PI

    @property
    def perimeter(self) -> float:
        """[perimeter]

        Returns:
            [float]: [the perimeter of the circle]
        """
        return 2 * self.radius * Math.PI

    @property
    def average_circumference(self):
        return 2 * self.radius

    @property
    def center(self):
        x, y = self.center = [self.radius, self.radius]
        return x, y

    @center.setter
    def center(self, center):
        self._center = center

    def __str__(self):
        return f"Circle({self.center}, {self.radius}, {self.color})"

    def __getstate__(self):
        return {"center": self.center, "radius": self.radius}

    def __setstate__(self, state):
        self.center = state["center"]
        self.radius = state["radius"]

    def __copy__(self):
        return Circle(self.center, self.radius, self.color)

    def __deepcopy__(self, memo):
        return Circle(self.center, self.radius, self.color)

    def __contains__(self, other):
        return other in self.center

    def __len__(self):
        return len(self.center)

    def __getitem__(self, key):
        return self.center[key]

    def __setitem__(self, key, value):
        self.center[key] = value

    def __iter__(self):
        return iter(self.center)

    def __add__(self, other):
        return Circle(self.center + other.center, self.radius + other.radius)

    def __sub__(self, other):
        return Circle(self.center - other.center, self.radius - other.radius)

    def __mul__(self, other):
        return Circle(self.center * other, self.radius * other)

    # def __rmul__(self, other):
    #     return Circle(self.center * other, self.radius * other


class Oval(Circle):
    def __init__(self, radius=2.5, size=3):
        super().__init__(size, "green")
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
