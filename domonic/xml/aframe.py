"""
    domonic.aframe
    ====================================

    Generate aframe tags with python 3
    https://aframe.io/

"""

from domonic.dom import Node, ParentNode


class aframe_tag(Node):
    def __str__(self):
        return f"<a-{self.name}{self.__attributes__}>{self.content}</a-{self.name}>"


entity = type('entity', (aframe_tag, Node, ParentNode), {'name': 'entity'})
scene = type('scene', (aframe_tag, Node, ParentNode), {'name': 'scene'})
material = type('material', (aframe_tag, Node, ParentNode), {'name': 'material'})
appearance = type('appearance', (aframe_tag, Node, ParentNode), {'name': 'appearance'})

shape = type('shape', (aframe_tag, Node, ParentNode), {'name': 'shape'})
# transform = type('transform', (aframe_tag, Node, ParentNode), {'name': 'transform'})
# inline = type('inline', (aframe_tag, Node, ParentNode), {'name': 'inline'})

sphere = type('sphere', (aframe_tag, Node, ParentNode), {'name': 'sphere'})
box = type('box', (aframe_tag, Node, ParentNode), {'name': 'box'})
plane = type('plane', (aframe_tag, Node, ParentNode), {'name': 'plane'})
sky = type('sky', (aframe_tag, Node, ParentNode), {'name': 'sky'})

mixin = type('mixin', (aframe_tag, Node, ParentNode), {'name': 'mixin'})
circle = type('circle', (aframe_tag, Node, ParentNode), {'name': 'circle'})
camera = type('camera', (aframe_tag, Node, ParentNode), {'name': 'camera'})
cone = type('cone', (aframe_tag, Node, ParentNode), {'name': 'cone'})
cursor = type('cursor', (aframe_tag, Node, ParentNode), {'name': 'cursor'})

curvedimage = type('curvedimage', (aframe_tag, Node, ParentNode), {'name': 'curvedimage'})
cylinder = type('cylinder', (aframe_tag, Node, ParentNode), {'name': 'cylinder'})

dodecahedron = type('dodecahedron', (aframe_tag, Node, ParentNode), {'name': 'dodecahedron'})
icosahedron = type('icosahedron', (aframe_tag, Node, ParentNode), {'name': 'icosahedron'})
image = type('image', (aframe_tag, Node, ParentNode), {'name': 'image'})
light = type('light', (aframe_tag, Node, ParentNode), {'name': 'light'})
alink = type('alink', (aframe_tag, Node, ParentNode), {'name': 'alink'})
octahedron = type('octahedron', (aframe_tag, Node, ParentNode), {'name': 'octahedron'})
plane = type('plane', (aframe_tag, Node, ParentNode), {'name': 'plane'})
ring = type('ring', (aframe_tag, Node, ParentNode), {'name': 'ring'})
sound = type('sound', (aframe_tag, Node, ParentNode), {'name': 'sound'})
sphere = type('sphere', (aframe_tag, Node, ParentNode), {'name': 'sphere'})
tetrahedron = type('tetrahedron', (aframe_tag, Node, ParentNode), {'name': 'tetrahedron'})
text = type('text', (aframe_tag, Node, ParentNode), {'name': 'text'})
torus = type('torus', (aframe_tag, Node, ParentNode), {'name': 'torus'})
triangle = type('triangle', (aframe_tag, Node, ParentNode), {'name': 'triangle'})
video = type('video', (aframe_tag, Node, ParentNode), {'name': 'video'})
videosphere = type('videosphere', (aframe_tag, Node, ParentNode), {'name': 'videosphere'})

gltf = type('gltf', (aframe_tag, Node, ParentNode), {'name': 'gltf'})
gltf_model = type('gltf_model', (aframe_tag, Node, ParentNode), {'name': 'gltf_model'})
torus_knot = type('torus_knot', (aframe_tag, Node, ParentNode), {'name': 'torus_knot'})
obj_model = type('obj_model', (aframe_tag, Node, ParentNode), {'name': 'obj_model'})

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
