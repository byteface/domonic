"""
    domonic.geom
    ====================================

    written by.ai

"""
import math
from domonic.javascript import Math

# from domonic.vector import vector
from domonic.geom.vec2 import vec2
from domonic.geom.vec3 import vec3
from domonic.geom.vec4 import vec4

# from domonic.mat4 import mat4
# from domonic.mat3 import mat3
# from domonic.quat import quat

# from domonic.color import color

# from domonic.point import point
# from domonic.matrix import matrix
# from domonic.transform import transform
# from domonic.matrix_utils import *
# from domonic.geom_utils import *
# from domonic.geom_math import *
# from domonic.geom_shader import *
# from domonic.geom_shader_utils import *
# from domonic.geom_shader_math import *
# from domonic.geom_shader_math_utils import *

from domonic.geom.shape import Shape
from domonic.geom.shape import Point
from domonic.geom.shape import Line
# from domonic.geom.shape import Plane
from domonic.geom.shape import Circle
from domonic.geom.shape import Polygon
# from domonic.geom.shape import Triangle
# from domonic.geom.shape import Quad
# from domonic.geom.shape import Hexagon
# from domonic.geom.shape import Rectangle
from domonic.geom.shape import Rect
# from domonic.geom.shape import Ellipse
# from domonic.geom.shape import BoundingBox
# from domonic.geom.shape import BoundingCircle



class matrix(object):
    """[matrixs]
    """

    def __init__(self, m):
        self.m = m

    def translate(self, pt):
        """ Translates the point on the vector defined by the vectors m[0] and m[1]."""
        return vec2(self.m[0][0], self.m[0][1]) + pt - self.m[0][0]

    def rotate(self, pt):
        """ Rotates the point on the vector defined by the vectors m[0] and m[1]."""
        return vec2(self.m[1][0], self.m[1][1]) + pt - self.m[1][0]

    def scale(self, pt):
        """ Scales the point on the vector defined by the vectors m[0] and m[1]."""
        return vec2(self.m[2][0], self.m[2][1]) + pt - self.m[2][0]


class Quaternion():

    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z
        self.q = [w, x, y, z]


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

    # def plot(self):
    #     for p in self.points:
    #         self.canvas.draw_point(p)


class Path(object):
    def __init__(self, points=None):
        self.points = points or []

    def add_point(self, point):
        self.points.append(point)

    # def get_points(self):
    #     return self.points

    # def get_points_as_vector(self):
    #     return vec3(self.points)

    # def get_points_as_matrix(self):
    #     return mat3(self.points)


# class Cursor(object):


class Group(object):
    def __init__(self, shapes=None):
        self.shapes = shapes or []

    def add_shape(self, shape):
        self.shapes.append(shape)

    def get_shapes(self):
        return self.shapes


class Layer(object):

    def __init__(self, name=None):
        self.name = name
        self.shapes = []
        self.visible = True
        self.selected = False
        self.parent = None
        self.children = []
        self.parent = None
        self.zindex = 0
        self.color = (0, 0, 0)
        self.alpha = 1.0

    def add(self, shape):
        self.shapes.append(shape)
        return self

    def add_at(self, shape, index):
        self.shapes.insert(index, shape)
        return self

    def has(self, shape):
        return shape in self.shapes

    def get_at(self, index):
        return self.shapes[index]

    def get_by_name(self, name):
        for shape in self.shapes:
            if shape.name == name:
                return shape
        return None

    def get_by_property(self, property):
        return [shape for shape in self.shapes if shape.has_property(property)]

    def remove(self, shape):
        self.shapes.remove(shape)
        return self

    def remove_at(self, index):
        self.shapes.pop(index)
        return self

    def swap(self, shape1, shape2):
        self.shapes[self.shapes.index(shape1)] = shape2

    def swap_at(self, index1, index2):
        self.shapes[index1], self.shapes[index2] = self.shapes[index2], self.shapes[index1]
        return self

    def show(self):
        for shape in self.shapes:
            shape.show()
        return self

    def hide(self): # hide all shapes
        for shape in self.shapes:
            shape.hide()
        return self

    def delete(self):
        for shape in self.shapes:
            shape.delete()
        return self

    def __len__(self):
        return len(self.shapes)

    def __iter__(self):
        return iter(self.shapes)

    def __getitem__(self, key):
        return self.shapes[key]

    def __setitem__(self, key, value):
        self.shapes[key] = value

    def __add__(self, other):
        self.shapes += other.shapes
        return self

    def __sub__(self, other):
        self.shapes -= other.shapes
        return self

    def __mul__(self, other):
        self.shapes *= other
        return self

    def __rmul__(self, other):
        self.shapes *= other
        return self

    def __iadd__(self, other):
        self.shapes += other.shapes
        return self

    def __isub__(self, other):
        self.shapes -= other.shapes
        return self

    def __imul__(self, other):
        self.shapes *= other
        return self

    def __idiv__(self, other):
        self.shapes /= other
        return self

    def __itruediv__(self, other):
        self.shapes /= other
        return self

    def __imod__(self, other):
        self.shapes %= other
        return self

    def __ipow__(self, other):
        self.shapes **= other
        return self

    def __ilshift__(self, other):
        self.shapes <<= other
        return self

    def __irshift__(self, other):
        self.shapes >>= other
        return self

    def __iand__(self, other):
        self.shapes &= other
        return self


class Timeline(object):

    def __init__(self):
        self.layers = []
        # self.current_layer = None
        self.current_frame = 0
        self.enabled = True
        self.is_playing = False
        self.play_speed = 1.0
        self.total_frames = 0
        self.framerate = 0

    def go_to_frame(self, frame):
        self.current_frame = frame

    def next_frame(self):
        self.current_frame += 1

    def prev_frame(self):
        self.current_frame -= 1

    def stop(self):
        self.is_playing = False




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
