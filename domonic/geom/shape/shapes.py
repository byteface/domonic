"""
    domonic.geom.shape.circle
    ====================================
    written by.ai
"""

from domonic.javascript import Math
from domonic.geom.shape import Shape


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
        return "Circle(%s, %s, %s)" % (self.center, self.radius, self.color)

    # def __repr__(self):
    #     return "Circle(%s, %s, %s)" % (self.center, self.radius, self.color)

    def __getstate__(self):
        return {'center': self.center, 'radius': self.radius}

    def __setstate__(self, state):
        self.center = state['center']
        self.radius = state['radius']

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
