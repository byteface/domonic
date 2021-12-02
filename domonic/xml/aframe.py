"""
    domonic.aframe
    ====================================

    Generate aframe tags with python 3
    https://aframe.io/

"""

from domonic.dom import Element


class aframe_tag(Element):
    def __str__(self):
        return f"<a-{self.name}{self.__attributes__}>{self.content}</a-{self.name}>"


entity = type('entity', (aframe_tag, Element,), {'name': 'entity'})
scene = type('scene', (aframe_tag, Element,), {'name': 'scene'})
material = type('material', (aframe_tag, Element,), {'name': 'material'})
appearance = type('appearance', (aframe_tag, Element,), {'name': 'appearance'})

shape = type('shape', (aframe_tag, Element,), {'name': 'shape'})
# transform = type('transform', (aframe_tag, Element,), {'name': 'transform'})
# inline = type('inline', (aframe_tag, Element,), {'name': 'inline'})

sphere = type('sphere', (aframe_tag, Element,), {'name': 'sphere'})
box = type('box', (aframe_tag, Element,), {'name': 'box'})
plane = type('plane', (aframe_tag, Element,), {'name': 'plane'})
sky = type('sky', (aframe_tag, Element,), {'name': 'sky'})

mixin = type('mixin', (aframe_tag, Element,), {'name': 'mixin'})
circle = type('circle', (aframe_tag, Element,), {'name': 'circle'})
camera = type('camera', (aframe_tag, Element,), {'name': 'camera'})
cone = type('cone', (aframe_tag, Element,), {'name': 'cone'})
cursor = type('cursor', (aframe_tag, Element,), {'name': 'cursor'})

curvedimage = type('curvedimage', (aframe_tag, Element,), {'name': 'curvedimage'})
cylinder = type('cylinder', (aframe_tag, Element,), {'name': 'cylinder'})

dodecahedron = type('dodecahedron', (aframe_tag, Element,), {'name': 'dodecahedron'})
icosahedron = type('icosahedron', (aframe_tag, Element,), {'name': 'icosahedron'})
image = type('image', (aframe_tag, Element,), {'name': 'image'})
light = type('light', (aframe_tag, Element,), {'name': 'light'})
alink = type('alink', (aframe_tag, Element,), {'name': 'alink'})
octahedron = type('octahedron', (aframe_tag, Element,), {'name': 'octahedron'})
plane = type('plane', (aframe_tag, Element,), {'name': 'plane'})
ring = type('ring', (aframe_tag, Element,), {'name': 'ring'})
sound = type('sound', (aframe_tag, Element,), {'name': 'sound'})
sphere = type('sphere', (aframe_tag, Element,), {'name': 'sphere'})
tetrahedron = type('tetrahedron', (aframe_tag, Element,), {'name': 'tetrahedron'})
text = type('text', (aframe_tag, Element,), {'name': 'text'})
torus = type('torus', (aframe_tag, Element,), {'name': 'torus'})
triangle = type('triangle', (aframe_tag, Element,), {'name': 'triangle'})
video = type('video', (aframe_tag, Element,), {'name': 'video'})
videosphere = type('videosphere', (aframe_tag, Element,), {'name': 'videosphere'})

gltf = type('gltf', (aframe_tag, Element,), {'name': 'gltf'})
gltf_model = type('gltf_model', (aframe_tag, Element,), {'name': 'gltf_model'})
torus_knot = type('torus_knot', (aframe_tag, Element,), {'name': 'torus_knot'})
obj_model = type('obj_model', (aframe_tag, Element,), {'name': 'obj_model'})

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
