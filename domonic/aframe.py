"""
    domonic.aframe
    ====================================
    Generate aframe tags with python 3

    https://aframe.io/

"""

from domonic.html import tag  # , closed_tag
from domonic.dom import Node, ParentNode


class aframe_tag(tag):
    def __str__(self):
        return f"<a-{self.name}{self.attributes}>{self.content}</a-{self.name}>"


def aframe_init(self, *args, **kwargs):
    tag.__init__(self, *args, **kwargs)
    Node.__init__(self, *args, **kwargs)


entity = type('entity', (aframe_tag, Node, ParentNode), {'name': 'entity', '__init__': aframe_init})
scene = type('scene', (aframe_tag, Node, ParentNode), {'name': 'scene', '__init__': aframe_init})
material = type('material', (aframe_tag, Node, ParentNode), {'name': 'material', '__init__': aframe_init})
appearance = type('appearance', (aframe_tag, Node, ParentNode), {'name': 'appearance', '__init__': aframe_init})

shape = type('shape', (aframe_tag, Node, ParentNode), {'name': 'shape', '__init__': aframe_init})
# transform = type('transform', (aframe_tag, Node, ParentNode), {'name': 'transform', '__init__': aframe_init})
# inline = type('inline', (aframe_tag, Node, ParentNode), {'name': 'inline', '__init__': aframe_init})

sphere = type('sphere', (aframe_tag, Node, ParentNode), {'name': 'sphere', '__init__': aframe_init})
box = type('box', (aframe_tag, Node, ParentNode), {'name': 'box', '__init__': aframe_init})
plane = type('plane', (aframe_tag, Node, ParentNode), {'name': 'plane', '__init__': aframe_init})
sky = type('sky', (aframe_tag, Node, ParentNode), {'name': 'sky', '__init__': aframe_init})

mixin = type('mixin', (aframe_tag, Node, ParentNode), {'name': 'mixin', '__init__': aframe_init})
circle = type('circle', (aframe_tag, Node, ParentNode), {'name': 'circle', '__init__': aframe_init})
camera = type('camera', (aframe_tag, Node, ParentNode), {'name': 'camera', '__init__': aframe_init})
cone = type('cone', (aframe_tag, Node, ParentNode), {'name': 'cone', '__init__': aframe_init})
cursor = type('cursor', (aframe_tag, Node, ParentNode), {'name': 'cursor', '__init__': aframe_init})

curvedimage = type('curvedimage', (aframe_tag, Node, ParentNode), {'name': 'curvedimage', '__init__': aframe_init})
cylinder = type('cylinder', (aframe_tag, Node, ParentNode), {'name': 'cylinder', '__init__': aframe_init})

dodecahedron = type('dodecahedron', (aframe_tag, Node, ParentNode), {'name': 'dodecahedron', '__init__': aframe_init})
icosahedron = type('icosahedron', (aframe_tag, Node, ParentNode), {'name': 'icosahedron', '__init__': aframe_init})
image = type('image', (aframe_tag, Node, ParentNode), {'name': 'image', '__init__': aframe_init})
light = type('light', (aframe_tag, Node, ParentNode), {'name': 'light', '__init__': aframe_init})
alink = type('alink', (aframe_tag, Node, ParentNode), {'name': 'alink', '__init__': aframe_init})
octahedron = type('octahedron', (aframe_tag, Node, ParentNode), {'name': 'octahedron', '__init__': aframe_init})
plane = type('plane', (aframe_tag, Node, ParentNode), {'name': 'plane', '__init__': aframe_init})
ring = type('ring', (aframe_tag, Node, ParentNode), {'name': 'ring', '__init__': aframe_init})
sound = type('sound', (aframe_tag, Node, ParentNode), {'name': 'sound', '__init__': aframe_init})
sphere = type('sphere', (aframe_tag, Node, ParentNode), {'name': 'sphere', '__init__': aframe_init})
tetrahedron = type('tetrahedron', (aframe_tag, Node, ParentNode), {'name': 'tetrahedron', '__init__': aframe_init})
text = type('text', (aframe_tag, Node, ParentNode), {'name': 'text', '__init__': aframe_init})
torus = type('torus', (aframe_tag, Node, ParentNode), {'name': 'torus', '__init__': aframe_init})
triangle = type('triangle', (aframe_tag, Node, ParentNode), {'name': 'triangle', '__init__': aframe_init})
video = type('video', (aframe_tag, Node, ParentNode), {'name': 'video', '__init__': aframe_init})
videosphere = type('videosphere', (aframe_tag, Node, ParentNode), {'name': 'videosphere', '__init__': aframe_init})

gltf = type('gltf', (aframe_tag, Node, ParentNode), {'name': 'gltf', '__init__': aframe_init})
gltf_model = type('gltf_model', (aframe_tag, Node, ParentNode), {'name': 'gltf_model', '__init__': aframe_init})
torus_knot = type('torus_knot', (aframe_tag, Node, ParentNode), {'name': 'torus_knot', '__init__': aframe_init})
obj_model = type('obj_model', (aframe_tag, Node, ParentNode), {'name': 'obj_model', '__init__': aframe_init})

# <a-box>
# <a-camera>
# <a-circle>
# <a-cone>
# <a-cursor>
# <a-curvedimage>
# <a-cylinder>
# <a-dodecahedron>
# <a-gltf-model>
# <a-icosahedron>
# <a-image>
# <a-light>
# <a-link>
# <a-obj-model>
# <a-octahedron>
# <a-plane>
# <a-ring>
# <a-sky>
# <a-sound>
# <a-sphere>
# <a-tetrahedron>
# <a-text>
# <a-torus-knot>
# <a-torus>
# <a-triangle>
# <a-video>
# <a-videosphere>
