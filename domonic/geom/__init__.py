"""
domonic.geom
====================================

written by.ai

"""

import math

from domonic.geom.vec2 import vec2


class matrix:
    """matrixs"""

    def __init__(self, m):
        self.m = m

    def translate(self, pt):
        """Translates the point on the vector defined by the vectors m[0] and m[1]."""
        return vec2(self.m[0][0], self.m[0][1]) + pt - self.m[0][0]

    def rotate(self, pt):
        """Rotates the point on the vector defined by the vectors m[0] and m[1]."""
        return vec2(self.m[1][0], self.m[1][1]) + pt - self.m[1][0]

    def scale(self, pt):
        """Scales the point on the vector defined by the vectors m[0] and m[1]."""
        return vec2(self.m[2][0], self.m[2][1]) + pt - self.m[2][0]


class Quaternion:
    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z
        self.q = [w, x, y, z]


class Plotter:
    def __init__(self, canvas=None):
        self.canvas = canvas  # or canvas.Canvas('Example Plotter', 500, 500)
        self.points = []
        self.starting_color = (255, 255, 255)
        self.color = self.starting_color
        self.clear()

    def add_point(self, point):
        self.points.append(point)
        return self

    def clear(self):
        self.points.clear()
        self.color = self.starting_color
        if self.canvas is not None and hasattr(self.canvas, "clear"):
            self.canvas.clear()
        return self

    def plot(self):
        if self.canvas is None:
            return list(self.points)

        draw_point = getattr(self.canvas, "draw_point", None)
        if not callable(draw_point):
            raise AttributeError("Plotter canvas must provide draw_point(point)")

        for point in self.points:
            draw_point(point)
        return self


class Path:
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


# class Cursor:


class Group:
    def __init__(self, shapes=None):
        self.shapes = shapes or []

    def add_shape(self, shape):
        self.shapes.append(shape)

    def get_shapes(self):
        return self.shapes


class Layer:
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

    def _index_of(self, shape):
        for index, candidate in enumerate(self.shapes):
            if candidate is shape:
                return index
        return -1

    def add(self, shape):
        self.shapes.append(shape)
        return self

    def add_at(self, shape, index):
        self.shapes.insert(index, shape)
        return self

    def has(self, shape):
        return self._index_of(shape) != -1

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
        index = self._index_of(shape)
        if index == -1:
            raise ValueError("shape is not in layer")
        self.shapes.pop(index)
        return self

    def remove_at(self, index):
        self.shapes.pop(index)
        return self

    def swap(self, shape1, shape2):
        index1 = self._index_of(shape1)
        index2 = self._index_of(shape2)
        if index1 == -1 or index2 == -1:
            raise ValueError("both shapes must be in layer")
        self.shapes[index1], self.shapes[index2] = (
            self.shapes[index2],
            self.shapes[index1],
        )
        return self

    def swap_at(self, index1, index2):
        self.shapes[index1], self.shapes[index2] = (
            self.shapes[index2],
            self.shapes[index1],
        )
        return self

    def show(self):
        for shape in self.shapes:
            shape.show()
        return self

    def hide(self):  # hide all shapes
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
        for shape in other.shapes:
            if self.has(shape):
                self.remove(shape)
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
        return self.__sub__(other)

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


class Timeline:
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


__all__ = [
    "Circle",
    "Ellipse",
    "Group",
    "Layer",
    "Line",
    "Oval",
    "Particle",
    "Particle3D",
    "Path",
    "Plane",
    "Plotter",
    "Point",
    "Polygon",
    "Polyline",
    "Quaternion",
    "Rect",
    "Shape",
    "Square",
    "Timeline",
    "matrix",
    "vec2",
    "vec3",
    "vec4",
    "vertex",
]

_LAZY_EXPORTS = {
    "Circle": ("domonic.geom.shape", "Circle"),
    "Ellipse": ("domonic.geom.shape", "Ellipse"),
    "Line": ("domonic.geom.shape", "Line"),
    "Oval": ("domonic.geom.shape", "Oval"),
    "Particle": ("domonic.geom.particles", "Particle"),
    "Particle3D": ("domonic.geom.particles", "Particle3D"),
    "Plane": ("domonic.geom.shape", "Plane"),
    "Point": ("domonic.geom.shape", "Point"),
    "Polygon": ("domonic.geom.shape", "Polygon"),
    "Polyline": ("domonic.geom.shape", "Polyline"),
    "Rect": ("domonic.geom.shape", "Rect"),
    "Shape": ("domonic.geom.shape", "Shape"),
    "Square": ("domonic.geom.shape", "Square"),
    "vec3": ("domonic.geom.vec3", "vec3"),
    "vec4": ("domonic.geom.vec4", "vec4"),
    "vertex": ("domonic.geom.shape", "vertex"),
}


def __getattr__(name):
    if name not in _LAZY_EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    module_name, attr_name = _LAZY_EXPORTS[name]
    module = __import__(module_name, fromlist=[attr_name])
    value = getattr(module, attr_name)
    globals()[name] = value
    return value


def __dir__():
    return sorted(set(globals()) | set(__all__))


# class Interactive:#??
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
