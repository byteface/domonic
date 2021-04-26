"""
    domonic.geom
    ====================================

"""


class vec2():

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def add(self, pt):
        """ Adds a point to this point. returns new one """
        # raise NotImplementedError
        return vec2(self.x + pt.x, self.y + pt.y)

    def __add__(self, other):
        self.add(other)

    def subtract(self, pt):
        """ Subtract from this point. returns new one """
        return vec2(self.x - pt.x, self.y - pt.y)

    def __sub__(self, other):
        self.subtract(other)

    def copy(self):
        """ Creates a copy of this Point object. """
        raise NotImplementedError

    def distance(self, pt1, pt2):
        """ Returns the distance between pt1 and pt2. """
        raise NotImplementedError

    def equals(self, pt):
        """ Determines whether two points are equal. """
        raise NotImplementedError

    def interpolate(self, pt1, pt2, f):
        """ Determines a point between two specified points."""
        raise NotImplementedError

    def __str__(self):
        return str(self.x) + " " + str(self.y)


class vec3():

    def __init__(self, x=0, y=0, z=0, w=0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def add(self, a):
        raise NotImplementedError

    def subtract(self, v):
        """ Subtract from this point. """
        raise NotImplementedError

    def copy(self):
        """ Creates a copy of this object. """
        raise NotImplementedError

    def angleBetween(self, a, b):
        """ Returns the angle in radians between two vectors """

    def crossProduct(self, a):
        """ Returns a new vec3 """
        raise NotImplementedError

    def distance(self, pt1, pt2):
        """ Returns the distance between two Vector3D objects."""
        raise NotImplementedError

    def equals(self, pt):
        """ Determines whether two points are equal. """
        raise NotImplementedError

    def __str__(self):
        return str(self.x) + " " + str(self.y) + " " + str(self.z)
