"""
    domonic.collada
    ====================================
    Generate Collada with python 3

"""

from domonic.html import tag, closed_tag
from domonic.dom import Node


def write(inp, outp='output'):
    """write

    Renders the input to string or .dae file

    Args:
        inp (obj): domonic.collada tags
        outp (str): An optional filename for the .dae file that gets produced

    Returns:
        str: A HTML rendered string
    """
    if outp != '':
        with open(outp, "w+") as f:
            f.write(str(inp) + ".dae")
    return str(inp)


def collada_init(self, *args, **kwargs):
    tag.__init__(self, *args, **kwargs)
    Node.__init__(self, *args, **kwargs)


COLLADA = type('COLLADA', (tag, Node), {'name': 'COLLADA', '__init__': collada_init})

asset = type('asset', (tag, Node), {'name': 'asset', '__init__': collada_init})
library_cameras = type('library_cameras', (tag, Node), {'name': 'library_cameras', '__init__': collada_init})
library_lights = type('library_lights', (tag, Node), {'name': 'library_lights', '__init__': collada_init})
library_materials = type('library_materials', (tag, Node), {'name': 'library_materials', '__init__': collada_init})
library_effects = type('library_effects', (tag, Node), {'name': 'library_effects', '__init__': collada_init})
library_geometries = type('library_geometries', (tag, Node), {'name': 'library_geometries', '__init__': collada_init})
library_visual_scenes = type('library_visual_scenes', (tag, Node), {'name': 'library_visual_scenes', '__init__': collada_init})
scene = type('scene', (tag, Node), {'name': 'scene', '__init__': collada_init})
extra = type('extra', (tag, Node), {'name': 'extra', '__init__': collada_init})
author = type('author', (tag, Node), {'name': 'author', '__init__': collada_init})
up_axis = type('up_axis', (tag, Node), {'name': 'up_axis', '__init__': collada_init})
camera = type('camera', (tag, Node), {'name': 'camera', '__init__': collada_init})
optics = type('optics', (tag, Node), {'name': 'optics', '__init__': collada_init})
technique = type('technique', (tag, Node), {'name': 'technique', '__init__': collada_init})
technique_common = type('technique_common', (tag, Node), {'name': 'technique_common', '__init__': collada_init})
aspect_ratio = type('aspect_ratio', (tag, Node), {'name': 'aspect_ratio', '__init__': collada_init})
light = type('light', (tag, Node), {'name': 'light', '__init__': collada_init})
constant_attenuation = type('constant_attenuation', (tag, Node), {'name': 'constant_attenuation', '__init__': collada_init})
linear_attenuation = type('linear_attenuation', (tag, Node), {'name': 'linear_attenuation', '__init__': collada_init})
quadratic_attenuation = type('quadratic_attenuation', (tag, Node), {'name': 'quadratic_attenuation', '__init__': collada_init})
material = type('material', (tag, Node), {'name': 'material', '__init__': collada_init})
effect = type('effect', (tag, Node), {'name': 'effect', '__init__': collada_init})
profile_COMMON = type('profile_COMMON', (tag, Node), {'name': 'profile_COMMON', '__init__': collada_init})
phong = type('phong', (tag, Node), {'name': 'phong', '__init__': collada_init})
emission = type('emission', (tag, Node), {'name': 'emission', '__init__': collada_init})
geometry = type('geometry', (tag, Node), {'name': 'geometry', '__init__': collada_init})
mesh = type('mesh', (tag, Node), {'name': 'mesh', '__init__': collada_init})
source = type('source', (tag, Node), {'name': 'source', '__init__': collada_init})
vertices = type('vertices', (tag, Node), {'name': 'vertices', '__init__': collada_init})
polylist = type('polylist', (tag, Node), {'name': 'polylist', '__init__': collada_init})
vcount = type('vcount', (tag, Node), {'name': 'vcount', '__init__': collada_init})
p = type('p', (tag, Node), {'name': 'p', '__init__': collada_init})
library_visual_scenes = type('library_visual_scenes', (tag, Node), {'name': 'library_visual_scenes', '__init__': collada_init})
visual_scene = type('visual_scene', (tag, Node), {'name': 'visual_scene', '__init__': collada_init})
node = type('node', (tag, Node), {'name': 'node', '__init__': collada_init})
instance_visual_scene = type('instance_visual_scene', (tag, Node), {'name': 'instance_visual_scene', '__init__': collada_init})
test_element = type('test_element', (tag, Node), {'name': 'test_element', '__init__': collada_init})
instance_effect = type('instance_effect', (closed_tag, Node), {'name': 'instance_effect', '__init__': collada_init})
texture_unit = type('texture_unit', (closed_tag, Node), {'name': 'texture_unit', '__init__': collada_init})
tapered_cylinder = type('tapered_cylinder', (closed_tag, Node), {'name': 'tapered_cylinder', '__init__': collada_init})
tapered_capsule = type('tapered_capsule', (closed_tag, Node), {'name': 'tapered_capsule', '__init__': collada_init})
format_hint = type('format_hint', (closed_tag, Node), {'name': 'format_hint', '__init__': collada_init})
revisions = type('revisions', (closed_tag, Node), {'name': 'revisions', '__init__': collada_init})
contributer = type('contributer', (closed_tag, Node), {'name': 'contributer', '__init__': collada_init})
acceleration = type('acceleration', (tag, Node), {'name': 'acceleration', '__init__': collada_init})
axis_info = type('axis_info', (tag, Node), {'name': 'axis_info', '__init__': collada_init})
accessor = type('accessor', (tag, Node), {'name': 'accessor', '__init__': collada_init})
active = type('active', (tag, Node), {'name': 'active', '__init__': collada_init})
alpha_func = type('alpha_func', (tag, Node), {'name': 'alpha_func', '__init__': collada_init})
alpha_test_enable = type('alpha_test_enable', (tag, Node), {'name': 'alpha_test_enable', '__init__': collada_init})
alpha = type('alpha', (tag, Node), {'name': 'alpha', '__init__': collada_init})
altitude = type('altitude', (tag, Node), {'name': 'altitude', '__init__': collada_init})
ambient = type('ambient', (tag, Node), {'name': 'ambient', '__init__': collada_init})
angle = type('angle', (tag, Node), {'name': 'angle', '__init__': collada_init})
angular_velocity = type('angular_velocity', (tag, Node), {'name': 'angular_velocity', '__init__': collada_init})
angular = type('angular', (tag, Node), {'name': 'angular', '__init__': collada_init})
animation_clip = type('animation_clip', (tag, Node), {'name': 'animation_clip', '__init__': collada_init})
animation = type('animation', (tag, Node), {'name': 'animation', '__init__': collada_init})
annotate = type('annotate', (tag, Node), {'name': 'annotate', '__init__': collada_init})
argument = type('argument', (tag, Node), {'name': 'argument', '__init__': collada_init})
array = type('array', (tag, Node), {'name': 'array', '__init__': collada_init})
articulated_system = type('articulated_system', (tag, Node), {'name': 'articulated_system', '__init__': collada_init})
perspective = type('perspective', (tag, Node), {'name': 'perspective', '__init__': collada_init})
asset = type('asset', (tag, Node), {'name': 'asset', '__init__': collada_init})
se = type('se', (tag, Node), {'name': 'se', '__init__': collada_init})
attachment_end = type('attachment_end', (tag, Node), {'name': 'attachment_end', '__init__': collada_init})
attachment_full = type('attachment_full', (tag, Node), {'name': 'attachment_full', '__init__': collada_init})
attachment_start = type('attachment_start', (tag, Node), {'name': 'attachment_start', '__init__': collada_init})
attachment = type('attachment', (tag, Node), {'name': 'attachment', '__init__': collada_init})
author_email = type('author_email', (tag, Node), {'name': 'author_email', '__init__': collada_init})
author_website = type('author_website', (tag, Node), {'name': 'author_website', '__init__': collada_init})
author = type('author', (tag, Node), {'name': 'author', '__init__': collada_init})
authoring_tool = type('authoring_tool', (tag, Node), {'name': 'authoring_tool', '__init__': collada_init})
auto_normal_enable = type('auto_normal_enable', (tag, Node), {'name': 'auto_normal_enable', '__init__': collada_init})
axis_info = type('axis_info', (tag, Node), {'name': 'axis_info', '__init__': collada_init})
axis = type('axis', (tag, Node), {'name': 'axis', '__init__': collada_init})
prismatic = type('prismatic', (tag, Node), {'name': 'prismatic', '__init__': collada_init})
revolute = type('revolute', (tag, Node), {'name': 'revolute', '__init__': collada_init})
swept_surface = type('swept_surface', (tag, Node), {'name': 'swept_surface', '__init__': collada_init})
binary = type('binary', (tag, Node), {'name': 'binary', '__init__': collada_init})
bind_attribute = type('bind_attribute', (tag, Node), {'name': 'bind_attribute', '__init__': collada_init})
bind_joint_axis = type('bind_joint_axis', (tag, Node), {'name': 'bind_joint_axis', '__init__': collada_init})
bind_kinematics_model = type('bind_kinematics_model', (tag, Node), {'name': 'bind_kinematics_model', '__init__': collada_init})
bind_shape_matrix = type('bind_shape_matrix', (tag, Node), {'name': 'bind_shape_matrix', '__init__': collada_init})
bind_uniform = type('bind_uniform', (tag, Node), {'name': 'bind_uniform', '__init__': collada_init})
bind_vertex_input = type('bind_vertex_input', (tag, Node), {'name': 'bind_vertex_input', '__init__': collada_init})
bind = type('bind', (tag, Node), {'name': 'bind', '__init__': collada_init})
bind = type('bind', (tag, Node), {'name': 'bind', '__init__': collada_init})
blend_color = type('blend_color', (tag, Node), {'name': 'blend_color', '__init__': collada_init})
blend_enable = type('blend_enable', (tag, Node), {'name': 'blend_enable', '__init__': collada_init})
blend_equation_separate = type('blend_equation_separate', (tag, Node), {'name': 'blend_equation_separate', '__init__': collada_init})
blend_equation = type('blend_equation', (tag, Node), {'name': 'blend_equation', '__init__': collada_init})
blend_func_separate = type('blend_func_separate', (tag, Node), {'name': 'blend_func_separate', '__init__': collada_init})
blend_func = type('blend_func', (tag, Node), {'name': 'blend_func', '__init__': collada_init})
blinn = type('blinn', (tag, Node), {'name': 'blinn', '__init__': collada_init})
bool_array = type('bool_array', (tag, Node), {'name': 'bool_array', '__init__': collada_init})
border_color = type('border_color', (tag, Node), {'name': 'border_color', '__init__': collada_init})
box = type('box', (tag, Node), {'name': 'box', '__init__': collada_init})
brep = type('brep', (tag, Node), {'name': 'brep', '__init__': collada_init})
camera = type('camera', (tag, Node), {'name': 'camera', '__init__': collada_init})
capsule = type('capsule', (tag, Node), {'name': 'capsule', '__init__': collada_init})
channel = type('channel', (tag, Node), {'name': 'channel', '__init__': collada_init})
arget = type('arget', (tag, Node), {'name': 'arget', '__init__': collada_init})
circle = type('circle', (tag, Node), {'name': 'circle', '__init__': collada_init})
clip_plane_enable = type('clip_plane_enable', (tag, Node), {'name': 'clip_plane_enable', '__init__': collada_init})
clip_plane = type('clip_plane', (tag, Node), {'name': 'clip_plane', '__init__': collada_init})
code = type('code', (tag, Node), {'name': 'code', '__init__': collada_init})
color_clear = type('color_clear', (tag, Node), {'name': 'color_clear', '__init__': collada_init})
color_logic_op_enable = type('color_logic_op_enable', (tag, Node), {'name': 'color_logic_op_enable', '__init__': collada_init})
color_mask = type('color_mask', (tag, Node), {'name': 'color_mask', '__init__': collada_init})
color_material_enable = type('color_material_enable', (tag, Node), {'name': 'color_material_enable', '__init__': collada_init})
color_material = type('color_material', (tag, Node), {'name': 'color_material', '__init__': collada_init})
color_target = type('color_target', (tag, Node), {'name': 'color_target', '__init__': collada_init})
color = type('color', (tag, Node), {'name': 'color', '__init__': collada_init})
comments = type('comments', (tag, Node), {'name': 'comments', '__init__': collada_init})
compiler = type('compiler', (tag, Node), {'name': 'compiler', '__init__': collada_init})
cone = type('cone', (tag, Node), {'name': 'cone', '__init__': collada_init})
connect_param = type('connect_param', (tag, Node), {'name': 'connect_param', '__init__': collada_init})
point = type('point', (tag, Node), {'name': 'point', '__init__': collada_init})
spot = type('spot', (tag, Node), {'name': 'spot', '__init__': collada_init})
constant = type('constant', (tag, Node), {'name': 'constant', '__init__': collada_init})
constant = type('constant', (tag, Node), {'name': 'constant', '__init__': collada_init})
contributor = type('contributor', (tag, Node), {'name': 'contributor', '__init__': collada_init})
control_vertices = type('control_vertices', (tag, Node), {'name': 'control_vertices', '__init__': collada_init})
controller = type('controller', (tag, Node), {'name': 'controller', '__init__': collada_init})
convex_mesh = type('convex_mesh', (tag, Node), {'name': 'convex_mesh', '__init__': collada_init})
copyright = type('copyright', (tag, Node), {'name': 'copyright', '__init__': collada_init})
coverage = type('coverage', (tag, Node), {'name': 'coverage', '__init__': collada_init})
create_2d = type('create_2d', (tag, Node), {'name': 'create_2d', '__init__': collada_init})
create_3d = type('create_3d', (tag, Node), {'name': 'create_3d', '__init__': collada_init})
create_cube = type('create_cube', (tag, Node), {'name': 'create_cube', '__init__': collada_init})
created = type('created', (tag, Node), {'name': 'created', '__init__': collada_init})
cull_face_enable = type('cull_face_enable', (tag, Node), {'name': 'cull_face_enable', '__init__': collada_init})
cull_face = type('cull_face', (tag, Node), {'name': 'cull_face', '__init__': collada_init})
curve = type('curve', (tag, Node), {'name': 'curve', '__init__': collada_init})
curves = type('curves', (tag, Node), {'name': 'curves', '__init__': collada_init})
cylinder = type('cylinder', (tag, Node), {'name': 'cylinder', '__init__': collada_init})
cylinder = type('cylinder', (tag, Node), {'name': 'cylinder', '__init__': collada_init})
damping = type('damping', (tag, Node), {'name': 'damping', '__init__': collada_init})
deceleration = type('deceleration', (tag, Node), {'name': 'deceleration', '__init__': collada_init})
axis_info = type('axis_info', (tag, Node), {'name': 'axis_info', '__init__': collada_init})
effector_info = type('effector_info', (tag, Node), {'name': 'effector_info', '__init__': collada_init})
density = type('density', (tag, Node), {'name': 'density', '__init__': collada_init})
depth_bounds_enable = type('depth_bounds_enable', (tag, Node), {'name': 'depth_bounds_enable', '__init__': collada_init})
depth_bounds = type('depth_bounds', (tag, Node), {'name': 'depth_bounds', '__init__': collada_init})
depth_clamp_enable = type('depth_clamp_enable', (tag, Node), {'name': 'depth_clamp_enable', '__init__': collada_init})
depth_clear = type('depth_clear', (tag, Node), {'name': 'depth_clear', '__init__': collada_init})
depth_func = type('depth_func', (tag, Node), {'name': 'depth_func', '__init__': collada_init})
depth_mask = type('depth_mask', (tag, Node), {'name': 'depth_mask', '__init__': collada_init})
depth_range = type('depth_range', (tag, Node), {'name': 'depth_range', '__init__': collada_init})
depth_target = type('depth_target', (tag, Node), {'name': 'depth_target', '__init__': collada_init})
depth_test_enable = type('depth_test_enable', (tag, Node), {'name': 'depth_test_enable', '__init__': collada_init})
diffuse = type('diffuse', (tag, Node), {'name': 'diffuse', '__init__': collada_init})
direction = type('direction', (tag, Node), {'name': 'direction', '__init__': collada_init})
line = type('line', (tag, Node), {'name': 'line', '__init__': collada_init})
swept_surface = type('swept_surface', (tag, Node), {'name': 'swept_surface', '__init__': collada_init})
directional = type('directional', (tag, Node), {'name': 'directional', '__init__': collada_init})
dither_enable = type('dither_enable', (tag, Node), {'name': 'dither_enable', '__init__': collada_init})
draw = type('draw', (tag, Node), {'name': 'draw', '__init__': collada_init})
dynamic_friction = type('dynamic_friction', (tag, Node), {'name': 'dynamic_friction', '__init__': collada_init})
dynamic = type('dynamic', (tag, Node), {'name': 'dynamic', '__init__': collada_init})
edges = type('edges', (tag, Node), {'name': 'edges', '__init__': collada_init})
effect = type('effect', (tag, Node), {'name': 'effect', '__init__': collada_init})
effector_info = type('effector_info', (tag, Node), {'name': 'effector_info', '__init__': collada_init})
ellipse = type('ellipse', (tag, Node), {'name': 'ellipse', '__init__': collada_init})
emission = type('emission', (tag, Node), {'name': 'emission', '__init__': collada_init})
enabled = type('enabled', (tag, Node), {'name': 'enabled', '__init__': collada_init})
equation = type('equation', (tag, Node), {'name': 'equation', '__init__': collada_init})
evaluate_scene = type('evaluate_scene', (tag, Node), {'name': 'evaluate_scene', '__init__': collada_init})
evaluate = type('evaluate', (tag, Node), {'name': 'evaluate', '__init__': collada_init})
exact = type('exact', (tag, Node), {'name': 'exact', '__init__': collada_init})
extra = type('extra', (tag, Node), {'name': 'extra', '__init__': collada_init})
faces = type('faces', (tag, Node), {'name': 'faces', '__init__': collada_init})
falloff_angle = type('falloff_angle', (tag, Node), {'name': 'falloff_angle', '__init__': collada_init})
falloff_exponent = type('falloff_exponent', (tag, Node), {'name': 'falloff_exponent', '__init__': collada_init})
float_array = type('float_array', (tag, Node), {'name': 'float_array', '__init__': collada_init})
focal = type('focal', (tag, Node), {'name': 'focal', '__init__': collada_init})
fog_color = type('fog_color', (tag, Node), {'name': 'fog_color', '__init__': collada_init})
fog_coord_src = type('fog_coord_src', (tag, Node), {'name': 'fog_coord_src', '__init__': collada_init})
fog_density = type('fog_density', (tag, Node), {'name': 'fog_density', '__init__': collada_init})
fog_enable = type('fog_enable', (tag, Node), {'name': 'fog_enable', '__init__': collada_init})
fog_end = type('fog_end', (tag, Node), {'name': 'fog_end', '__init__': collada_init})
fog_mode = type('fog_mode', (tag, Node), {'name': 'fog_mode', '__init__': collada_init})
fog_state = type('fog_state', (tag, Node), {'name': 'fog_state', '__init__': collada_init})
force_field = type('force_field', (tag, Node), {'name': 'force_field', '__init__': collada_init})
formula = type('formula', (tag, Node), {'name': 'formula', '__init__': collada_init})
frame_object = type('frame_object', (tag, Node), {'name': 'frame_object', '__init__': collada_init})
frame_origin = type('frame_origin', (tag, Node), {'name': 'frame_origin', '__init__': collada_init})
frame_tcp = type('frame_tcp', (tag, Node), {'name': 'frame_tcp', '__init__': collada_init})
frame_tip = type('frame_tip', (tag, Node), {'name': 'frame_tip', '__init__': collada_init})
front_face = type('front_face', (tag, Node), {'name': 'front_face', '__init__': collada_init})
func = type('func', (tag, Node), {'name': 'func', '__init__': collada_init})
geographic_location = type('geographic_location', (tag, Node), {'name': 'geographic_location', '__init__': collada_init})
geometry = type('geometry', (tag, Node), {'name': 'geometry', '__init__': collada_init})
gravity = type('gravity', (tag, Node), {'name': 'gravity', '__init__': collada_init})
h = type('h', (tag, Node), {'name': 'h', '__init__': collada_init})
half_extents = type('half_extents', (tag, Node), {'name': 'half_extents', '__init__': collada_init})
height = type('height', (tag, Node), {'name': 'height', '__init__': collada_init})
capsule = type('capsule', (tag, Node), {'name': 'capsule', '__init__': collada_init})
binary = type('binary', (tag, Node), {'name': 'binary', '__init__': collada_init})
init_from = type('init_from', (tag, Node), {'name': 'init_from', '__init__': collada_init})
hint = type('hint', (tag, Node), {'name': 'hint', '__init__': collada_init})
hollow = type('hollow', (tag, Node), {'name': 'hollow', '__init__': collada_init})
IDREF_array = type('IDREF_array', (tag, Node), {'name': 'IDREF_array', '__init__': collada_init})
image = type('image', (tag, Node), {'name': 'image', '__init__': collada_init})
imager = type('imager', (tag, Node), {'name': 'imager', '__init__': collada_init})
include = type('include', (tag, Node), {'name': 'include', '__init__': collada_init})
index_of_refraction = type('index_of_refraction', (tag, Node), {'name': 'index_of_refraction', '__init__': collada_init})
index = type('index', (tag, Node), {'name': 'index', '__init__': collada_init})
inertia = type('inertia', (tag, Node), {'name': 'inertia', '__init__': collada_init})
instance_rigid_body = type('instance_rigid_body', (tag, Node), {'name': 'instance_rigid_body', '__init__': collada_init})
init_from = type('init_from', (tag, Node), {'name': 'init_from', '__init__': collada_init})
inline = type('inline', (tag, Node), {'name': 'inline', '__init__': collada_init})
emantic = type('emantic', (tag, Node), {'name': 'emantic', '__init__': collada_init})
emantics = type('emantics', (tag, Node), {'name': 'emantics', '__init__': collada_init})
instance_animation = type('instance_animation', (tag, Node), {'name': 'instance_animation', '__init__': collada_init})
instance_articulated_system = type('instance_articulated_system', (tag, Node), {'name': 'instance_articulated_system', '__init__': collada_init})
instance_camera = type('instance_camera', (tag, Node), {'name': 'instance_camera', '__init__': collada_init})
instance_controller = type('instance_controller', (tag, Node), {'name': 'instance_controller', '__init__': collada_init})
instance_effect = type('instance_effect', (tag, Node), {'name': 'instance_effect', '__init__': collada_init})
instance_force_field = type('instance_force_field', (tag, Node), {'name': 'instance_force_field', '__init__': collada_init})
instance_formula = type('instance_formula', (tag, Node), {'name': 'instance_formula', '__init__': collada_init})
instance_geometry = type('instance_geometry', (tag, Node), {'name': 'instance_geometry', '__init__': collada_init})
instance_image = type('instance_image', (tag, Node), {'name': 'instance_image', '__init__': collada_init})
instance_joint = type('instance_joint', (tag, Node), {'name': 'instance_joint', '__init__': collada_init})
instance_kinematics_model = type('instance_kinematics_model', (tag, Node), {'name': 'instance_kinematics_model', '__init__': collada_init})
instance_kinematics_scene = type('instance_kinematics_scene', (tag, Node), {'name': 'instance_kinematics_scene', '__init__': collada_init})
instance_light = type('instance_light', (tag, Node), {'name': 'instance_light', '__init__': collada_init})
instance_material = type('instance_material', (tag, Node), {'name': 'instance_material', '__init__': collada_init})
instance_material = type('instance_material', (tag, Node), {'name': 'instance_material', '__init__': collada_init})
instance_node = type('instance_node', (tag, Node), {'name': 'instance_node', '__init__': collada_init})
instance_physics_material = type('instance_physics_material', (tag, Node), {'name': 'instance_physics_material', '__init__': collada_init})
instance_physics_model = type('instance_physics_model', (tag, Node), {'name': 'instance_physics_model', '__init__': collada_init})
instance_physics_scene = type('instance_physics_scene', (tag, Node), {'name': 'instance_physics_scene', '__init__': collada_init})
instance_rigid_body = type('instance_rigid_body', (tag, Node), {'name': 'instance_rigid_body', '__init__': collada_init})
instance_rigid_constraint = type('instance_rigid_constraint', (tag, Node), {'name': 'instance_rigid_constraint', '__init__': collada_init})
instance_visual_scene = type('instance_visual_scene', (tag, Node), {'name': 'instance_visual_scene', '__init__': collada_init})
int_array = type('int_array', (tag, Node), {'name': 'int_array', '__init__': collada_init})
interpenetrate = type('interpenetrate', (tag, Node), {'name': 'interpenetrate', '__init__': collada_init})
jerk = type('jerk', (tag, Node), {'name': 'jerk', '__init__': collada_init})
axis_info = type('axis_info', (tag, Node), {'name': 'axis_info', '__init__': collada_init})
joint = type('joint', (tag, Node), {'name': 'joint', '__init__': collada_init})
joints = type('joints', (tag, Node), {'name': 'joints', '__init__': collada_init})
keywords = type('keywords', (tag, Node), {'name': 'keywords', '__init__': collada_init})
kinematics_model = type('kinematics_model', (tag, Node), {'name': 'kinematics_model', '__init__': collada_init})
kinematics_scene = type('kinematics_scene', (tag, Node), {'name': 'kinematics_scene', '__init__': collada_init})
kinematics = type('kinematics', (tag, Node), {'name': 'kinematics', '__init__': collada_init})
lambert = type('lambert', (tag, Node), {'name': 'lambert', '__init__': collada_init})
latitude = type('latitude', (tag, Node), {'name': 'latitude', '__init__': collada_init})
layer = type('layer', (tag, Node), {'name': 'layer', '__init__': collada_init})
library_animation_clips = type('library_animation_clips', (tag, Node), {'name': 'library_animation_clips', '__init__': collada_init})
library_animations = type('library_animations', (tag, Node), {'name': 'library_animations', '__init__': collada_init})
library_articulated_systems = type('library_articulated_systems', (tag, Node), {'name': 'library_articulated_systems', '__init__': collada_init})
library_cameras = type('library_cameras', (tag, Node), {'name': 'library_cameras', '__init__': collada_init})
library_controllers = type('library_controllers', (tag, Node), {'name': 'library_controllers', '__init__': collada_init})
library_effects = type('library_effects', (tag, Node), {'name': 'library_effects', '__init__': collada_init})
library_force_fields = type('library_force_fields', (tag, Node), {'name': 'library_force_fields', '__init__': collada_init})
library_formulas = type('library_formulas', (tag, Node), {'name': 'library_formulas', '__init__': collada_init})
library_geometries = type('library_geometries', (tag, Node), {'name': 'library_geometries', '__init__': collada_init})
library_images = type('library_images', (tag, Node), {'name': 'library_images', '__init__': collada_init})
library_joints = type('library_joints', (tag, Node), {'name': 'library_joints', '__init__': collada_init})
library_kinematics_models = type('library_kinematics_models', (tag, Node), {'name': 'library_kinematics_models', '__init__': collada_init})
library_kinematics_scenes = type('library_kinematics_scenes', (tag, Node), {'name': 'library_kinematics_scenes', '__init__': collada_init})
library_nodes = type('library_nodes', (tag, Node), {'name': 'library_nodes', '__init__': collada_init})
library_physics_materials = type('library_physics_materials', (tag, Node), {'name': 'library_physics_materials', '__init__': collada_init})
library_physics_models = type('library_physics_models', (tag, Node), {'name': 'library_physics_models', '__init__': collada_init})
library_physics_scenes = type('library_physics_scenes', (tag, Node), {'name': 'library_physics_scenes', '__init__': collada_init})
library_visual_scenes = type('library_visual_scenes', (tag, Node), {'name': 'library_visual_scenes', '__init__': collada_init})
light_ambient = type('light_ambient', (tag, Node), {'name': 'light_ambient', '__init__': collada_init})
light_constant_attenuation = type('light_constant_attenuation', (tag, Node), {'name': 'light_constant_attenuation', '__init__': collada_init})
light_diffuse = type('light_diffuse', (tag, Node), {'name': 'light_diffuse', '__init__': collada_init})
light_enable = type('light_enable', (tag, Node), {'name': 'light_enable', '__init__': collada_init})
light_linear_attenuation = type('light_linear_attenuation', (tag, Node), {'name': 'light_linear_attenuation', '__init__': collada_init})
light_model_ambient = type('light_model_ambient', (tag, Node), {'name': 'light_model_ambient', '__init__': collada_init})
light_model_color_control = type('light_model_color_control', (tag, Node), {'name': 'light_model_color_control', '__init__': collada_init})
light_model_local_viewer_enable = type('light_model_local_viewer_enable', (tag, Node), {'name': 'light_model_local_viewer_enable', '__init__': collada_init})
light_model_two_side_enable = type('light_model_two_side_enable', (tag, Node), {'name': 'light_model_two_side_enable', '__init__': collada_init})
light_position = type('light_position', (tag, Node), {'name': 'light_position', '__init__': collada_init})
light_quadratic_attenuation = type('light_quadratic_attenuation', (tag, Node), {'name': 'light_quadratic_attenuation', '__init__': collada_init})
light_specular = type('light_specular', (tag, Node), {'name': 'light_specular', '__init__': collada_init})
light_spot_cutoff = type('light_spot_cutoff', (tag, Node), {'name': 'light_spot_cutoff', '__init__': collada_init})
light_spot_direction = type('light_spot_direction', (tag, Node), {'name': 'light_spot_direction', '__init__': collada_init})
light_spot_exponent = type('light_spot_exponent', (tag, Node), {'name': 'light_spot_exponent', '__init__': collada_init})
lighting_enable = type('lighting_enable', (tag, Node), {'name': 'lighting_enable', '__init__': collada_init})
lights = type('lights', (tag, Node), {'name': 'lights', '__init__': collada_init})
limits = type('limits', (tag, Node), {'name': 'limits', '__init__': collada_init})
axis_info = type('axis_info', (tag, Node), {'name': 'axis_info', '__init__': collada_init})
prismatic = type('prismatic', (tag, Node), {'name': 'prismatic', '__init__': collada_init})
revolute = type('revolute', (tag, Node), {'name': 'revolute', '__init__': collada_init})
line_smooth_enable = type('line_smooth_enable', (tag, Node), {'name': 'line_smooth_enable', '__init__': collada_init})
line_stipple_enable = type('line_stipple_enable', (tag, Node), {'name': 'line_stipple_enable', '__init__': collada_init})
line_stipple = type('line_stipple', (tag, Node), {'name': 'line_stipple', '__init__': collada_init})
line_width = type('line_width', (tag, Node), {'name': 'line_width', '__init__': collada_init})
line = type('line', (tag, Node), {'name': 'line', '__init__': collada_init})
linear_attenuation = type('linear_attenuation', (tag, Node), {'name': 'linear_attenuation', '__init__': collada_init})
spot = type('spot', (tag, Node), {'name': 'spot', '__init__': collada_init})
linear = type('linear', (tag, Node), {'name': 'linear', '__init__': collada_init})
lines = type('lines', (tag, Node), {'name': 'lines', '__init__': collada_init})
linestrips = type('linestrips', (tag, Node), {'name': 'linestrips', '__init__': collada_init})
link = type('link', (tag, Node), {'name': 'link', '__init__': collada_init})
linker = type('linker', (tag, Node), {'name': 'linker', '__init__': collada_init})
locked = type('locked', (tag, Node), {'name': 'locked', '__init__': collada_init})
logic_op_enable = type('logic_op_enable', (tag, Node), {'name': 'logic_op_enable', '__init__': collada_init})
logic_op = type('logic_op', (tag, Node), {'name': 'logic_op', '__init__': collada_init})
longitude = type('longitude', (tag, Node), {'name': 'longitude', '__init__': collada_init})
lookout = type('lookout', (tag, Node), {'name': 'lookout', '__init__': collada_init})
magfilter = type('magfilter', (tag, Node), {'name': 'magfilter', '__init__': collada_init})
mass_frame = type('mass_frame', (tag, Node), {'name': 'mass_frame', '__init__': collada_init})
rigid_body = type('rigid_body', (tag, Node), {'name': 'rigid_body', '__init__': collada_init})
mass = type('mass', (tag, Node), {'name': 'mass', '__init__': collada_init})
shape = type('shape', (tag, Node), {'name': 'shape', '__init__': collada_init})
material_ambient = type('material_ambient', (tag, Node), {'name': 'material_ambient', '__init__': collada_init})
material_diffuse = type('material_diffuse', (tag, Node), {'name': 'material_diffuse', '__init__': collada_init})
material_emission = type('material_emission', (tag, Node), {'name': 'material_emission', '__init__': collada_init})
material_shininess = type('material_shininess', (tag, Node), {'name': 'material_shininess', '__init__': collada_init})
material_specular = type('material_specular', (tag, Node), {'name': 'material_specular', '__init__': collada_init})
material = type('material', (tag, Node), {'name': 'material', '__init__': collada_init})
matrix = type('matrix', (tag, Node), {'name': 'matrix', '__init__': collada_init})
max_anisotropy = type('max_anisotropy', (tag, Node), {'name': 'max_anisotropy', '__init__': collada_init})
mesh = type('mesh', (tag, Node), {'name': 'mesh', '__init__': collada_init})
minfilter = type('minfilter', (tag, Node), {'name': 'minfilter', '__init__': collada_init})
mip_bias = type('mip_bias', (tag, Node), {'name': 'mip_bias', '__init__': collada_init})
mip_max_level = type('mip_max_level', (tag, Node), {'name': 'mip_max_level', '__init__': collada_init})
mip_min_level = type('mip_min_level', (tag, Node), {'name': 'mip_min_level', '__init__': collada_init})
mipfilter = type('mipfilter', (tag, Node), {'name': 'mipfilter', '__init__': collada_init})
mips = type('mips', (tag, Node), {'name': 'mips', '__init__': collada_init})
create_cube = type('create_cube', (tag, Node), {'name': 'create_cube', '__init__': collada_init})
create2d = type('create2d', (tag, Node), {'name': 'create2d', '__init__': collada_init})
create3d = type('create3d', (tag, Node), {'name': 'create3d', '__init__': collada_init})
model_view_matrix = type('model_view_matrix', (tag, Node), {'name': 'model_view_matrix', '__init__': collada_init})
modified = type('modified', (tag, Node), {'name': 'modified', '__init__': collada_init})
modifier = type('modifier', (tag, Node), {'name': 'modifier', '__init__': collada_init})
morph = type('morph', (tag, Node), {'name': 'morph', '__init__': collada_init})
motion = type('motion', (tag, Node), {'name': 'motion', '__init__': collada_init})
multisample_enable = type('multisample_enable', (tag, Node), {'name': 'multisample_enable', '__init__': collada_init})
Name_array = type('Name_array', (tag, Node), {'name': 'Name_array', '__init__': collada_init})
emantic = type('emantic', (tag, Node), {'name': 'emantic', '__init__': collada_init})
newparam = type('newparam', (tag, Node), {'name': 'newparam', '__init__': collada_init})
ommon = type('ommon', (tag, Node), {'name': 'ommon', '__init__': collada_init})
node = type('node', (tag, Node), {'name': 'node', '__init__': collada_init})
normalize_enable = type('normalize_enable', (tag, Node), {'name': 'normalize_enable', '__init__': collada_init})
nurbs_surface = type('nurbs_surface', (tag, Node), {'name': 'nurbs_surface', '__init__': collada_init})
nurbs = type('nurbs', (tag, Node), {'name': 'nurbs', '__init__': collada_init})
optics = type('optics', (tag, Node), {'name': 'optics', '__init__': collada_init})
orient = type('orient', (tag, Node), {'name': 'orient', '__init__': collada_init})
origin = type('origin', (tag, Node), {'name': 'origin', '__init__': collada_init})
orthographic = type('orthographic', (tag, Node), {'name': 'orthographic', '__init__': collada_init})
p = type('p', (tag, Node), {'name': 'p', '__init__': collada_init})
edges = type('edges', (tag, Node), {'name': 'edges', '__init__': collada_init})
faces = type('faces', (tag, Node), {'name': 'faces', '__init__': collada_init})
lines = type('lines', (tag, Node), {'name': 'lines', '__init__': collada_init})
pcurves = type('pcurves', (tag, Node), {'name': 'pcurves', '__init__': collada_init})
ph = type('ph', (tag, Node), {'name': 'ph', '__init__': collada_init})
solids = type('solids', (tag, Node), {'name': 'solids', '__init__': collada_init})
triangles = type('triangles', (tag, Node), {'name': 'triangles', '__init__': collada_init})
trifans = type('trifans', (tag, Node), {'name': 'trifans', '__init__': collada_init})
tristrips = type('tristrips', (tag, Node), {'name': 'tristrips', '__init__': collada_init})
wires = type('wires', (tag, Node), {'name': 'wires', '__init__': collada_init})
parabola = type('parabola', (tag, Node), {'name': 'parabola', '__init__': collada_init})
param = type('param', (tag, Node), {'name': 'param', '__init__': collada_init})
ph = type('ph', (tag, Node), {'name': 'ph', '__init__': collada_init})
phong = type('phong', (tag, Node), {'name': 'phong', '__init__': collada_init})
physics_material = type('physics_material', (tag, Node), {'name': 'physics_material', '__init__': collada_init})
physics_model = type('physics_model', (tag, Node), {'name': 'physics_model', '__init__': collada_init})
physics_scene = type('physics_scene', (tag, Node), {'name': 'physics_scene', '__init__': collada_init})
plane = type('plane', (tag, Node), {'name': 'plane', '__init__': collada_init})
point_distance_attenuation = type('point_distance_attenuation', (tag, Node), {'name': 'point_distance_attenuation', '__init__': collada_init})
point_fade_threshold_size = type('point_fade_threshold_size', (tag, Node), {'name': 'point_fade_threshold_size', '__init__': collada_init})
point_size_max = type('point_size_max', (tag, Node), {'name': 'point_size_max', '__init__': collada_init})
point_size_min = type('point_size_min', (tag, Node), {'name': 'point_size_min', '__init__': collada_init})
point_size = type('point_size', (tag, Node), {'name': 'point_size', '__init__': collada_init})
point_smooth_enable = type('point_smooth_enable', (tag, Node), {'name': 'point_smooth_enable', '__init__': collada_init})
polygon_mode = type('polygon_mode', (tag, Node), {'name': 'polygon_mode', '__init__': collada_init})
polygon_offset_fill_enable = type('polygon_offset_fill_enable', (tag, Node), {'name': 'polygon_offset_fill_enable', '__init__': collada_init})
polygon_offset_line_enable = type('polygon_offset_line_enable', (tag, Node), {'name': 'polygon_offset_line_enable', '__init__': collada_init})
polygon_offset_point_enable = type('polygon_offset_point_enable', (tag, Node), {'name': 'polygon_offset_point_enable', '__init__': collada_init})
polygon_offset = type('polygon_offset', (tag, Node), {'name': 'polygon_offset', '__init__': collada_init})
polygon_smooth_enable = type('polygon_smooth_enable', (tag, Node), {'name': 'polygon_smooth_enable', '__init__': collada_init})
polygon_stipple_enable = type('polygon_stipple_enable', (tag, Node), {'name': 'polygon_stipple_enable', '__init__': collada_init})
polygons = type('polygons', (tag, Node), {'name': 'polygons', '__init__': collada_init})
polylist = type('polylist', (tag, Node), {'name': 'polylist', '__init__': collada_init})
prismatic = type('prismatic', (tag, Node), {'name': 'prismatic', '__init__': collada_init})
profile_BRIDGE = type('profile_BRIDGE', (tag, Node), {'name': 'profile_BRIDGE', '__init__': collada_init})
profile_CG = type('profile_CG', (tag, Node), {'name': 'profile_CG', '__init__': collada_init})
profile_COMMON = type('profile_COMMON', (tag, Node), {'name': 'profile_COMMON', '__init__': collada_init})
verview = type('verview', (tag, Node), {'name': 'verview', '__init__': collada_init})
profile_GLES = type('profile_GLES', (tag, Node), {'name': 'profile_GLES', '__init__': collada_init})
profile_GLES2 = type('profile_GLES2', (tag, Node), {'name': 'profile_GLES2', '__init__': collada_init})
profile_GLSL = type('profile_GLSL', (tag, Node), {'name': 'profile_GLSL', '__init__': collada_init})
program = type('program', (tag, Node), {'name': 'program', '__init__': collada_init})
projection_matrix = type('projection_matrix', (tag, Node), {'name': 'projection_matrix', '__init__': collada_init})
quadratic_attenuation = type('quadratic_attenuation', (tag, Node), {'name': 'quadratic_attenuation', '__init__': collada_init})
point = type('point', (tag, Node), {'name': 'point', '__init__': collada_init})
radius = type('radius', (tag, Node), {'name': 'radius', '__init__': collada_init})
capsule = type('capsule', (tag, Node), {'name': 'capsule', '__init__': collada_init})
circle = type('circle', (tag, Node), {'name': 'circle', '__init__': collada_init})
cone = type('cone', (tag, Node), {'name': 'cone', '__init__': collada_init})
cylinder = type('cylinder', (tag, Node), {'name': 'cylinder', '__init__': collada_init})
ellipse = type('ellipse', (tag, Node), {'name': 'ellipse', '__init__': collada_init})
hyperbola = type('hyperbola', (tag, Node), {'name': 'hyperbola', '__init__': collada_init})
torus = type('torus', (tag, Node), {'name': 'torus', '__init__': collada_init})
ref_attachment = type('ref_attachment', (tag, Node), {'name': 'ref_attachment', '__init__': collada_init})
ref = type('ref', (tag, Node), {'name': 'ref', '__init__': collada_init})
binary = type('binary', (tag, Node), {'name': 'binary', '__init__': collada_init})
init_from = type('init_from', (tag, Node), {'name': 'init_from', '__init__': collada_init})
reflective = type('reflective', (tag, Node), {'name': 'reflective', '__init__': collada_init})
reflectivity = type('reflectivity', (tag, Node), {'name': 'reflectivity', '__init__': collada_init})
render = type('render', (tag, Node), {'name': 'render', '__init__': collada_init})
renderable = type('renderable', (tag, Node), {'name': 'renderable', '__init__': collada_init})
rescale_normal_enable = type('rescale_normal_enable', (tag, Node), {'name': 'rescale_normal_enable', '__init__': collada_init})
restitution = type('restitution', (tag, Node), {'name': 'restitution', '__init__': collada_init})
revision = type('revision', (tag, Node), {'name': 'revision', '__init__': collada_init})
revolute = type('revolute', (tag, Node), {'name': 'revolute', '__init__': collada_init})
RGB = type('RGB', (tag, Node), {'name': 'RGB', '__init__': collada_init})
rigid_constraint = type('rigid_constraint', (tag, Node), {'name': 'rigid_constraint', '__init__': collada_init})
rotate = type('rotate', (tag, Node), {'name': 'rotate', '__init__': collada_init})
sample_alpha_to_coverage_enable = type('sample_alpha_to_coverage_enable', (tag, Node), {'name': 'sample_alpha_to_coverage_enable', '__init__': collada_init})
sample_alpha_to_one_enable = type('sample_alpha_to_one_enable', (tag, Node), {'name': 'sample_alpha_to_one_enable', '__init__': collada_init})
sample_coverage_enable = type('sample_coverage_enable', (tag, Node), {'name': 'sample_coverage_enable', '__init__': collada_init})
sample_coverage = type('sample_coverage', (tag, Node), {'name': 'sample_coverage', '__init__': collada_init})
sampler_image = type('sampler_image', (tag, Node), {'name': 'sampler_image', '__init__': collada_init})
sampler_states = type('sampler_states', (tag, Node), {'name': 'sampler_states', '__init__': collada_init})
sampler = type('sampler', (tag, Node), {'name': 'sampler', '__init__': collada_init})
nterpolation = type('nterpolation', (tag, Node), {'name': 'nterpolation', '__init__': collada_init})
sampler1D = type('sampler1D', (tag, Node), {'name': 'sampler1D', '__init__': collada_init})
sampler2D = type('sampler2D', (tag, Node), {'name': 'sampler2D', '__init__': collada_init})
sampler3D = type('sampler3D', (tag, Node), {'name': 'sampler3D', '__init__': collada_init})
samplerCUBE = type('samplerCUBE', (tag, Node), {'name': 'samplerCUBE', '__init__': collada_init})
samplerDEPTH = type('samplerDEPTH', (tag, Node), {'name': 'samplerDEPTH', '__init__': collada_init})
samplerRECT = type('samplerRECT', (tag, Node), {'name': 'samplerRECT', '__init__': collada_init})
scale = type('scale', (tag, Node), {'name': 'scale', '__init__': collada_init})
scene = type('scene', (tag, Node), {'name': 'scene', '__init__': collada_init})
scissor_test_enable = type('scissor_test_enable', (tag, Node), {'name': 'scissor_test_enable', '__init__': collada_init})
scissor = type('scissor', (tag, Node), {'name': 'scissor', '__init__': collada_init})
semantic = type('semantic', (tag, Node), {'name': 'semantic', '__init__': collada_init})
setparam = type('setparam', (tag, Node), {'name': 'setparam', '__init__': collada_init})
shade_model = type('shade_model', (tag, Node), {'name': 'shade_model', '__init__': collada_init})
shader = type('shader', (tag, Node), {'name': 'shader', '__init__': collada_init})
shape = type('shape', (tag, Node), {'name': 'shape', '__init__': collada_init})
shells = type('shells', (tag, Node), {'name': 'shells', '__init__': collada_init})
shininess = type('shininess', (tag, Node), {'name': 'shininess', '__init__': collada_init})
SIDREF_array = type('SIDREF_array', (tag, Node), {'name': 'SIDREF_array', '__init__': collada_init})
size_exact = type('size_exact', (tag, Node), {'name': 'size_exact', '__init__': collada_init})
size_ratio = type('size_ratio', (tag, Node), {'name': 'size_ratio', '__init__': collada_init})
size = type('size', (tag, Node), {'name': 'size', '__init__': collada_init})
create_cube = type('create_cube', (tag, Node), {'name': 'create_cube', '__init__': collada_init})
create3d = type('create3d', (tag, Node), {'name': 'create3d', '__init__': collada_init})
skeleton = type('skeleton', (tag, Node), {'name': 'skeleton', '__init__': collada_init})
skew = type('skew', (tag, Node), {'name': 'skew', '__init__': collada_init})
skin = type('skin', (tag, Node), {'name': 'skin', '__init__': collada_init})
source_data = type('source_data', (tag, Node), {'name': 'source_data', '__init__': collada_init})
source = type('source', (tag, Node), {'name': 'source', '__init__': collada_init})
sources = type('sources', (tag, Node), {'name': 'sources', '__init__': collada_init})
specular = type('specular', (tag, Node), {'name': 'specular', '__init__': collada_init})
speed = type('speed', (tag, Node), {'name': 'speed', '__init__': collada_init})
sphere = type('sphere', (tag, Node), {'name': 'sphere', '__init__': collada_init})
spline = type('spline', (tag, Node), {'name': 'spline', '__init__': collada_init})
nterpolation = type('nterpolation', (tag, Node), {'name': 'nterpolation', '__init__': collada_init})
spot = type('spot', (tag, Node), {'name': 'spot', '__init__': collada_init})
spring = type('spring', (tag, Node), {'name': 'spring', '__init__': collada_init})
states = type('states', (tag, Node), {'name': 'states', '__init__': collada_init})
static_friction = type('static_friction', (tag, Node), {'name': 'static_friction', '__init__': collada_init})
stencil_clear = type('stencil_clear', (tag, Node), {'name': 'stencil_clear', '__init__': collada_init})
stencil_func_separate = type('stencil_func_separate', (tag, Node), {'name': 'stencil_func_separate', '__init__': collada_init})
stencil_func = type('stencil_func', (tag, Node), {'name': 'stencil_func', '__init__': collada_init})
stencil_mask_separate = type('stencil_mask_separate', (tag, Node), {'name': 'stencil_mask_separate', '__init__': collada_init})
stencil_mask = type('stencil_mask', (tag, Node), {'name': 'stencil_mask', '__init__': collada_init})
stencil_op_separate = type('stencil_op_separate', (tag, Node), {'name': 'stencil_op_separate', '__init__': collada_init})
stencil_op = type('stencil_op', (tag, Node), {'name': 'stencil_op', '__init__': collada_init})
stencil_target = type('stencil_target', (tag, Node), {'name': 'stencil_target', '__init__': collada_init})
stencil_test_enable = type('stencil_test_enable', (tag, Node), {'name': 'stencil_test_enable', '__init__': collada_init})
stiffness = type('stiffness', (tag, Node), {'name': 'stiffness', '__init__': collada_init})
subject = type('subject', (tag, Node), {'name': 'subject', '__init__': collada_init})
surface_curves = type('surface_curves', (tag, Node), {'name': 'surface_curves', '__init__': collada_init})
surface = type('surface', (tag, Node), {'name': 'surface', '__init__': collada_init})
surfaces = type('surfaces', (tag, Node), {'name': 'surfaces', '__init__': collada_init})
swept_surface = type('swept_surface', (tag, Node), {'name': 'swept_surface', '__init__': collada_init})
swing_cone_and_twist = type('swing_cone_and_twist', (tag, Node), {'name': 'swing_cone_and_twist', '__init__': collada_init})
target_value = type('target_value', (tag, Node), {'name': 'target_value', '__init__': collada_init})
target = type('target', (tag, Node), {'name': 'target', '__init__': collada_init})
targets = type('targets', (tag, Node), {'name': 'targets', '__init__': collada_init})
bind_material = type('bind_material', (tag, Node), {'name': 'bind_material', '__init__': collada_init})
formula = type('formula', (tag, Node), {'name': 'formula', '__init__': collada_init})
instance_rigid_body = type('instance_rigid_body', (tag, Node), {'name': 'instance_rigid_body', '__init__': collada_init})
kinematics_model = type('kinematics_model', (tag, Node), {'name': 'kinematics_model', '__init__': collada_init})
kinematics = type('kinematics', (tag, Node), {'name': 'kinematics', '__init__': collada_init})
light = type('light', (tag, Node), {'name': 'light', '__init__': collada_init})
motion = type('motion', (tag, Node), {'name': 'motion', '__init__': collada_init})
optics = type('optics', (tag, Node), {'name': 'optics', '__init__': collada_init})
rigid_body = type('rigid_body', (tag, Node), {'name': 'rigid_body', '__init__': collada_init})
verview = type('verview', (tag, Node), {'name': 'verview', '__init__': collada_init})
technique_hint = type('technique_hint', (tag, Node), {'name': 'technique_hint', '__init__': collada_init})
technique_override = type('technique_override', (tag, Node), {'name': 'technique_override', '__init__': collada_init})
texcombiner = type('texcombiner', (tag, Node), {'name': 'texcombiner', '__init__': collada_init})
texcoord = type('texcoord', (tag, Node), {'name': 'texcoord', '__init__': collada_init})
texenv = type('texenv', (tag, Node), {'name': 'texenv', '__init__': collada_init})
texture_env_color = type('texture_env_color', (tag, Node), {'name': 'texture_env_color', '__init__': collada_init})
texture_env_mode = type('texture_env_mode', (tag, Node), {'name': 'texture_env_mode', '__init__': collada_init})
texture_pipeline = type('texture_pipeline', (tag, Node), {'name': 'texture_pipeline', '__init__': collada_init})
texture = type('texture', (tag, Node), {'name': 'texture', '__init__': collada_init})
texture1D_enable = type('texture1D_enable', (tag, Node), {'name': 'texture1D_enable', '__init__': collada_init})
texture1D = type('texture1D', (tag, Node), {'name': 'texture1D', '__init__': collada_init})
texture2D_enable = type('texture2D_enable', (tag, Node), {'name': 'texture2D_enable', '__init__': collada_init})
texture2D = type('texture2D', (tag, Node), {'name': 'texture2D', '__init__': collada_init})
texture3D_enable = type('texture3D_enable', (tag, Node), {'name': 'texture3D_enable', '__init__': collada_init})
texture3D = type('texture3D', (tag, Node), {'name': 'texture3D', '__init__': collada_init})
textureCUBE_enable = type('textureCUBE_enable', (tag, Node), {'name': 'textureCUBE_enable', '__init__': collada_init})
textureCUBE = type('textureCUBE', (tag, Node), {'name': 'textureCUBE', '__init__': collada_init})
textureDEPTH_enable = type('textureDEPTH_enable', (tag, Node), {'name': 'textureDEPTH_enable', '__init__': collada_init})
textureDEPTH = type('textureDEPTH', (tag, Node), {'name': 'textureDEPTH', '__init__': collada_init})
textureRECT_enable = type('textureRECT_enable', (tag, Node), {'name': 'textureRECT_enable', '__init__': collada_init})
textureRECT = type('textureRECT', (tag, Node), {'name': 'textureRECT', '__init__': collada_init})
time_step = type('time_step', (tag, Node), {'name': 'time_step', '__init__': collada_init})
title = type('title', (tag, Node), {'name': 'title', '__init__': collada_init})
translate = type('translate', (tag, Node), {'name': 'translate', '__init__': collada_init})
transparency = type('transparency', (tag, Node), {'name': 'transparency', '__init__': collada_init})
transparent = type('transparent', (tag, Node), {'name': 'transparent', '__init__': collada_init})
unit = type('unit', (tag, Node), {'name': 'unit', '__init__': collada_init})
unnormalized = type('unnormalized', (tag, Node), {'name': 'unnormalized', '__init__': collada_init})
usertype = type('usertype', (tag, Node), {'name': 'usertype', '__init__': collada_init})
v = type('v', (tag, Node), {'name': 'v', '__init__': collada_init})
value = type('value', (tag, Node), {'name': 'value', '__init__': collada_init})
velocity = type('velocity', (tag, Node), {'name': 'velocity', '__init__': collada_init})
vertex_weights = type('vertex_weights', (tag, Node), {'name': 'vertex_weights', '__init__': collada_init})
wrap_p = type('wrap_p', (tag, Node), {'name': 'wrap_p', '__init__': collada_init})
wrap_s = type('wrap_s', (tag, Node), {'name': 'wrap_s', '__init__': collada_init})
wrap_t = type('wrap_t', (tag, Node), {'name': 'wrap_t', '__init__': collada_init})
xfov = type('xfov', (tag, Node), {'name': 'xfov', '__init__': collada_init})
xmag = type('xmag', (tag, Node), {'name': 'xmag', '__init__': collada_init})
yfov = type('yfov', (tag, Node), {'name': 'yfov', '__init__': collada_init})
ymag = type('ymag', (tag, Node), {'name': 'ymag', '__init__': collada_init})
zfar = type('zfar', (tag, Node), {'name': 'zfar', '__init__': collada_init})
znear = type('znear', (tag, Node), {'name': 'znear', '__init__': collada_init})

# builtins require an underscore.
_input = type('input', (closed_tag, Node), {'name': 'input', '__init__': collada_init})
_float = type('float', (tag, Node), {'name': 'float', '__init__': collada_init})
_pass = type('pass', (tag, Node), {'name': 'pass', '__init__': collada_init})
_max = type('max', (tag, Node), {'name': 'max', '__init__': collada_init})
_min = type('min', (tag, Node), {'name': 'min', '__init__': collada_init})
_import = type('import', (tag, Node), {'name': 'import', '__init__': collada_init})
_hex = type('hex', (tag, Node), {'name': 'hex', '__init__': collada_init})
_format = type('format', (tag, Node), {'name': 'format', '__init__': collada_init})


class xml_header():
    """xml

    Returns:
        str: <?xml version="1.0"?>
    """
    def __str__(self):
        return '<?xml version="1.0"?>'



'''

# The asset tag describes the author and environment of the file
TMP_ASSET = asset(
    author("alorino"),
    up_axis("Y_UP")
)

# common cameras are perspective or orthographic
LIB_CAMERAS = library_cameras(
    camera(_id="PerspCamera", _name="PerspCamera").appendChild(
        optics(
            technique_common(
                perspective(
                    yfov(37.8493),
                    aspect_ratio(1),
                    znear(10),
                    zfar(1000)
                )
            )
        )
    )
)

# Common lights are point, spot or directional
LIB_LIGHTS = library_lights(
    light(_id="pointLightShape1-lib", _name="pointLightShape1").appendChild(
        technique_common(
            point(
                color("1 1 1"),  # need to figure this out
                constant_attenuation(1),
                linear_attenuation(0),
                quadratic_attenuation(0)
            )
        )
    )
)

# Materials instance effects
LIB_MAT = library_materials(
    material(_id="Blue", _name="Blue").appendChild(
        instance_effect(_url="#Blue-fx")
    )
)

# Common effects act like the OpenGL 1 state
LIB_FX = library_effects(
    effect(_id="Blue-fx").appendChild(
        profile_COMMON(
            technique(_sid="common").appendChild(
                phong(
                    emission(
                        color("0 0 0 1"),
                        index_of_refraction(
                            _float(0)
                        )
                    )
                )
            )
        )
    )
)

# Geometry describes the OpenGL attributes
LIB_GEOM = library_geometries(
    geometry(_id="box-lib", _name="box").appendChild(
        mesh(
            source(_id="box-lib-positions", _name="position"),
            source(_id="box-lib-normals", _name="normal"),
            vertices(_id="box-lib-vertices").appendChild(
                _input(_semantic="POSITION", _source="#box-lib-positions")
            ),
            polylist(_count="6", _material="BlueSG").appendChild(
                _input(_offset="0", _semantic="VERTEX", _source="#box-lib-vertices"),
                _input(_offset="1", _semantic="NORMAL", _source="#box-lib-normals"),
                vcount("4 4 4 4 4 4"),
                p("0 0 2 1 3 2 1 3 0 4 1 5 5 6 4 7")
            )
        )
    )
)

# The scene tag specifies a visual scene and sometimes a phyiscs scene
LIB_SCENES = library_visual_scenes(
    visual_scene(_id="VisualSceneNode", _name="untitled").appendChild(
        node(_id="Camera", _name="Camera")
    )
)

TMP_SCENE = scene(
    instance_visual_scene(_url="#VisualSceneNode")
)

# Extras are a way of extending the format
TMP_EXTRA = extra(
    technique(_profile="steveT").appendChild(
        test_element(_id="my_test_element", _attr1="value1", _attr2="value2").appendChild(
            "this is some text"
        )
    )
)

'''

"""

library_cameras(
    camera(_id="Camera-camera", _name="Camera").html(
        optics(
            technique_common(
                perspective(
                    xfov("49.13434", _sid="xfov")
                    aspect_ratio("1.777778")  # NOTE - underscored attributes?. - likely to break?
                    znear("0.1", _sid="znear")
                    zfar("100", _sid="zfar")
                )
            )
        )
    )
)

source(_id="Cube-mesh-normals").html(
    float_array(_id="Cube-mesh-normals-array", _count="18").html("0 0 -1 0 0 1 1 -2.83e-7 0 -2.83e-7 -1 0 -1 2.23e-7 -1.34e-7 2.38e-7 1 2.08e-7"),
        technique_common(
            accessor(_source="#Cube-mesh-normals-array", _count="6", _stride="3").html(
                param(_name="X" type="float"),
                param(_name="Y" type="float"),
            param(_name="Z" type="float")
        )
    )
)

vertices(_id="Cube-mesh-vertices").html(
    input(_semantic="POSITION", _source="#Cube-mesh-positions")
)


COLLADA(
    asset(
        created("2005-06-27T21:00:00Z"),
        keywords("COLLADA inthange"),
        created("2005-06-27T21:00:00Z"),
        unit(_name="nautical_league", _meter="5556.0"),
        up_axis("Z_UP")
    )
)

light(_id="blue").html(
    technique_common(
        directional(
        color(0.1 0.1 0.5)
        )
    )
)


camera(_name="eyepoint").html(
    optics(
        technique_common("....")
        technique profile="MyFancyGIRenderer">
            param("180.0", _name="FocalLength", _type="float")
            param("5.6", _name="Aperture", _type="float")
        )
    ),
    imager(
        technique(_profile="MyFancyGIRenderer").html(
            param("200.0", _name="ShutterSpeed", _type="float")
            param("0.2", _name="RedGain", _type="float")
            param("0.22", _name="GreenGain", _type="float")
            param("0.25", _name="BlueGain", _type="float")
            param("2.2", _name="RedGamma", _type="float")
            param("2.1", _name="GreenGamma", _type="float")
            param("2.17", _name="BlueGamma", _type="float")
            param("0.17", _name="BloomPixelLeak", _type="float")
            param("InvSquare", _name="BloomFalloff", _type="Name")
        )
    )
)


+ asset
+ + contributor
+ + + author
+ + + authoring_tool
+ + + created
+ + + unit
+ + + up_axi
+ library_cameras
+ + camera
+ + + optics
+ + + + technique_common
+ + + + + perspective
+ + + + + + xfov
+ + + + + + aspect_ratio
+ + + + + + znear
+ + + + + + zfar
+ library_lights
+ + light
+ + + technique_common
+ + + + point
+ + + + + color
+ + + + + constant_attenuation
+ + + + + linear_attenuation
+ + + + + quadratic_attenuation
+ + + extra
+ + + + technique
............
+ library_visual_scenes
+ + visual_scene
+ + + node
+ + + + translate
+ + + + rotate
+ + + + rotate
+ + + + rotate
+ + + + scale
+ + + + instance_geometry
+ + + + + bind_material
+ + + + + + technique_common
+ + + + + + + instance_material
+ + + node
+ + + + translate
+ + + + rotate
+ + + + rotate
+ + + + rotate
+ + + + scale
+ + + + instance_camera
+ scene
+ + instance_visual_scene

"""
