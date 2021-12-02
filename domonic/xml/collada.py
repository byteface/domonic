"""
    domonic.collada
    ====================================
    Generate Collada with python 3

"""

from domonic.html import closed_tag
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


COLLADA = type('COLLADA', (Node,), {'name': 'COLLADA'})

asset = type('asset', (Node,), {'name': 'asset'})
library_cameras = type('library_cameras', (Node,), {'name': 'library_cameras'})
library_lights = type('library_lights', (Node,), {'name': 'library_lights'})
library_materials = type('library_materials', (Node,), {'name': 'library_materials'})
library_effects = type('library_effects', (Node,), {'name': 'library_effects'})
library_geometries = type('library_geometries', (Node,), {'name': 'library_geometries'})
library_visual_scenes = type('library_visual_scenes', (Node,), {'name': 'library_visual_scenes'})
scene = type('scene', (Node,), {'name': 'scene'})
extra = type('extra', (Node,), {'name': 'extra'})
author = type('author', (Node,), {'name': 'author'})
up_axis = type('up_axis', (Node,), {'name': 'up_axis'})
camera = type('camera', (Node,), {'name': 'camera'})
optics = type('optics', (Node,), {'name': 'optics'})
technique = type('technique', (Node,), {'name': 'technique'})
technique_common = type('technique_common', (Node,), {'name': 'technique_common'})
aspect_ratio = type('aspect_ratio', (Node,), {'name': 'aspect_ratio'})
light = type('light', (Node,), {'name': 'light'})
constant_attenuation = type('constant_attenuation', (Node,), {'name': 'constant_attenuation'})
linear_attenuation = type('linear_attenuation', (Node,), {'name': 'linear_attenuation'})
quadratic_attenuation = type('quadratic_attenuation', (Node,), {'name': 'quadratic_attenuation'})
material = type('material', (Node,), {'name': 'material'})
effect = type('effect', (Node,), {'name': 'effect'})
profile_COMMON = type('profile_COMMON', (Node,), {'name': 'profile_COMMON'})
phong = type('phong', (Node,), {'name': 'phong'})
emission = type('emission', (Node,), {'name': 'emission'})
geometry = type('geometry', (Node,), {'name': 'geometry'})
mesh = type('mesh', (Node,), {'name': 'mesh'})
source = type('source', (Node,), {'name': 'source'})
vertices = type('vertices', (Node,), {'name': 'vertices'})
polylist = type('polylist', (Node,), {'name': 'polylist'})
vcount = type('vcount', (Node,), {'name': 'vcount'})
p = type('p', (Node,), {'name': 'p'})
library_visual_scenes = type('library_visual_scenes', (Node,), {'name': 'library_visual_scenes'})
visual_scene = type('visual_scene', (Node,), {'name': 'visual_scene'})
node = type('node', (Node,), {'name': 'node'})
instance_visual_scene = type('instance_visual_scene', (Node,), {'name': 'instance_visual_scene'})
test_element = type('test_element', (Node,), {'name': 'test_element'})
instance_effect = type('instance_effect', (closed_tag,), {'name': 'instance_effect'})
texture_unit = type('texture_unit', (closed_tag,), {'name': 'texture_unit'})
tapered_cylinder = type('tapered_cylinder', (closed_tag,), {'name': 'tapered_cylinder'})
tapered_capsule = type('tapered_capsule', (closed_tag,), {'name': 'tapered_capsule'})
format_hint = type('format_hint', (closed_tag,), {'name': 'format_hint'})
revisions = type('revisions', (closed_tag,), {'name': 'revisions'})
contributer = type('contributer', (closed_tag,), {'name': 'contributer'})
acceleration = type('acceleration', (Node,), {'name': 'acceleration'})
axis_info = type('axis_info', (Node,), {'name': 'axis_info'})
accessor = type('accessor', (Node,), {'name': 'accessor'})
active = type('active', (Node,), {'name': 'active'})
alpha_func = type('alpha_func', (Node,), {'name': 'alpha_func'})
alpha_test_enable = type('alpha_test_enable', (Node,), {'name': 'alpha_test_enable'})
alpha = type('alpha', (Node,), {'name': 'alpha'})
altitude = type('altitude', (Node,), {'name': 'altitude'})
ambient = type('ambient', (Node,), {'name': 'ambient'})
angle = type('angle', (Node,), {'name': 'angle'})
angular_velocity = type('angular_velocity', (Node,), {'name': 'angular_velocity'})
angular = type('angular', (Node,), {'name': 'angular'})
animation_clip = type('animation_clip', (Node,), {'name': 'animation_clip'})
animation = type('animation', (Node,), {'name': 'animation'})
annotate = type('annotate', (Node,), {'name': 'annotate'})
argument = type('argument', (Node,), {'name': 'argument'})
array = type('array', (Node,), {'name': 'array'})
articulated_system = type('articulated_system', (Node,), {'name': 'articulated_system'})
perspective = type('perspective', (Node,), {'name': 'perspective'})
asset = type('asset', (Node,), {'name': 'asset'})
se = type('se', (Node,), {'name': 'se'})
attachment_end = type('attachment_end', (Node,), {'name': 'attachment_end'})
attachment_full = type('attachment_full', (Node,), {'name': 'attachment_full'})
attachment_start = type('attachment_start', (Node,), {'name': 'attachment_start'})
attachment = type('attachment', (Node,), {'name': 'attachment'})
author_email = type('author_email', (Node,), {'name': 'author_email'})
author_website = type('author_website', (Node,), {'name': 'author_website'})
author = type('author', (Node,), {'name': 'author'})
authoring_tool = type('authoring_tool', (Node,), {'name': 'authoring_tool'})
auto_normal_enable = type('auto_normal_enable', (Node,), {'name': 'auto_normal_enable'})
axis_info = type('axis_info', (Node,), {'name': 'axis_info'})
axis = type('axis', (Node,), {'name': 'axis'})
prismatic = type('prismatic', (Node,), {'name': 'prismatic'})
revolute = type('revolute', (Node,), {'name': 'revolute'})
swept_surface = type('swept_surface', (Node,), {'name': 'swept_surface'})
binary = type('binary', (Node,), {'name': 'binary'})
bind_attribute = type('bind_attribute', (Node,), {'name': 'bind_attribute'})
bind_joint_axis = type('bind_joint_axis', (Node,), {'name': 'bind_joint_axis'})
bind_kinematics_model = type('bind_kinematics_model', (Node,), {'name': 'bind_kinematics_model'})
bind_shape_matrix = type('bind_shape_matrix', (Node,), {'name': 'bind_shape_matrix'})
bind_uniform = type('bind_uniform', (Node,), {'name': 'bind_uniform'})
bind_vertex_input = type('bind_vertex_input', (Node,), {'name': 'bind_vertex_input'})
bind = type('bind', (Node,), {'name': 'bind'})
bind = type('bind', (Node,), {'name': 'bind'})
blend_color = type('blend_color', (Node,), {'name': 'blend_color'})
blend_enable = type('blend_enable', (Node,), {'name': 'blend_enable'})
blend_equation_separate = type('blend_equation_separate', (Node,), {'name': 'blend_equation_separate'})
blend_equation = type('blend_equation', (Node,), {'name': 'blend_equation'})
blend_func_separate = type('blend_func_separate', (Node,), {'name': 'blend_func_separate'})
blend_func = type('blend_func', (Node,), {'name': 'blend_func'})
blinn = type('blinn', (Node,), {'name': 'blinn'})
bool_array = type('bool_array', (Node,), {'name': 'bool_array'})
border_color = type('border_color', (Node,), {'name': 'border_color'})
box = type('box', (Node,), {'name': 'box'})
brep = type('brep', (Node,), {'name': 'brep'})
camera = type('camera', (Node,), {'name': 'camera'})
capsule = type('capsule', (Node,), {'name': 'capsule'})
channel = type('channel', (Node,), {'name': 'channel'})
arget = type('arget', (Node,), {'name': 'arget'})
circle = type('circle', (Node,), {'name': 'circle'})
clip_plane_enable = type('clip_plane_enable', (Node,), {'name': 'clip_plane_enable'})
clip_plane = type('clip_plane', (Node,), {'name': 'clip_plane'})
code = type('code', (Node,), {'name': 'code'})
color_clear = type('color_clear', (Node,), {'name': 'color_clear'})
color_logic_op_enable = type('color_logic_op_enable', (Node,), {'name': 'color_logic_op_enable'})
color_mask = type('color_mask', (Node,), {'name': 'color_mask'})
color_material_enable = type('color_material_enable', (Node,), {'name': 'color_material_enable'})
color_material = type('color_material', (Node,), {'name': 'color_material'})
color_target = type('color_target', (Node,), {'name': 'color_target'})
color = type('color', (Node,), {'name': 'color'})
comments = type('comments', (Node,), {'name': 'comments'})
compiler = type('compiler', (Node,), {'name': 'compiler'})
cone = type('cone', (Node,), {'name': 'cone'})
connect_param = type('connect_param', (Node,), {'name': 'connect_param'})
point = type('point', (Node,), {'name': 'point'})
spot = type('spot', (Node,), {'name': 'spot'})
constant = type('constant', (Node,), {'name': 'constant'})
constant = type('constant', (Node,), {'name': 'constant'})
contributor = type('contributor', (Node,), {'name': 'contributor'})
control_vertices = type('control_vertices', (Node,), {'name': 'control_vertices'})
controller = type('controller', (Node,), {'name': 'controller'})
convex_mesh = type('convex_mesh', (Node,), {'name': 'convex_mesh'})
copyright = type('copyright', (Node,), {'name': 'copyright'})
coverage = type('coverage', (Node,), {'name': 'coverage'})
create_2d = type('create_2d', (Node,), {'name': 'create_2d'})
create_3d = type('create_3d', (Node,), {'name': 'create_3d'})
create_cube = type('create_cube', (Node,), {'name': 'create_cube'})
created = type('created', (Node,), {'name': 'created'})
cull_face_enable = type('cull_face_enable', (Node,), {'name': 'cull_face_enable'})
cull_face = type('cull_face', (Node,), {'name': 'cull_face'})
curve = type('curve', (Node,), {'name': 'curve'})
curves = type('curves', (Node,), {'name': 'curves'})
cylinder = type('cylinder', (Node,), {'name': 'cylinder'})
cylinder = type('cylinder', (Node,), {'name': 'cylinder'})
damping = type('damping', (Node,), {'name': 'damping'})
deceleration = type('deceleration', (Node,), {'name': 'deceleration'})
axis_info = type('axis_info', (Node,), {'name': 'axis_info'})
effector_info = type('effector_info', (Node,), {'name': 'effector_info'})
density = type('density', (Node,), {'name': 'density'})
depth_bounds_enable = type('depth_bounds_enable', (Node,), {'name': 'depth_bounds_enable'})
depth_bounds = type('depth_bounds', (Node,), {'name': 'depth_bounds'})
depth_clamp_enable = type('depth_clamp_enable', (Node,), {'name': 'depth_clamp_enable'})
depth_clear = type('depth_clear', (Node,), {'name': 'depth_clear'})
depth_func = type('depth_func', (Node,), {'name': 'depth_func'})
depth_mask = type('depth_mask', (Node,), {'name': 'depth_mask'})
depth_range = type('depth_range', (Node,), {'name': 'depth_range'})
depth_target = type('depth_target', (Node,), {'name': 'depth_target'})
depth_test_enable = type('depth_test_enable', (Node,), {'name': 'depth_test_enable'})
diffuse = type('diffuse', (Node,), {'name': 'diffuse'})
direction = type('direction', (Node,), {'name': 'direction'})
line = type('line', (Node,), {'name': 'line'})
swept_surface = type('swept_surface', (Node,), {'name': 'swept_surface'})
directional = type('directional', (Node,), {'name': 'directional'})
dither_enable = type('dither_enable', (Node,), {'name': 'dither_enable'})
draw = type('draw', (Node,), {'name': 'draw'})
dynamic_friction = type('dynamic_friction', (Node,), {'name': 'dynamic_friction'})
dynamic = type('dynamic', (Node,), {'name': 'dynamic'})
edges = type('edges', (Node,), {'name': 'edges'})
effect = type('effect', (Node,), {'name': 'effect'})
effector_info = type('effector_info', (Node,), {'name': 'effector_info'})
ellipse = type('ellipse', (Node,), {'name': 'ellipse'})
emission = type('emission', (Node,), {'name': 'emission'})
enabled = type('enabled', (Node,), {'name': 'enabled'})
equation = type('equation', (Node,), {'name': 'equation'})
evaluate_scene = type('evaluate_scene', (Node,), {'name': 'evaluate_scene'})
evaluate = type('evaluate', (Node,), {'name': 'evaluate'})
exact = type('exact', (Node,), {'name': 'exact'})
extra = type('extra', (Node,), {'name': 'extra'})
faces = type('faces', (Node,), {'name': 'faces'})
falloff_angle = type('falloff_angle', (Node,), {'name': 'falloff_angle'})
falloff_exponent = type('falloff_exponent', (Node,), {'name': 'falloff_exponent'})
float_array = type('float_array', (Node,), {'name': 'float_array'})
focal = type('focal', (Node,), {'name': 'focal'})
fog_color = type('fog_color', (Node,), {'name': 'fog_color'})
fog_coord_src = type('fog_coord_src', (Node,), {'name': 'fog_coord_src'})
fog_density = type('fog_density', (Node,), {'name': 'fog_density'})
fog_enable = type('fog_enable', (Node,), {'name': 'fog_enable'})
fog_end = type('fog_end', (Node,), {'name': 'fog_end'})
fog_mode = type('fog_mode', (Node,), {'name': 'fog_mode'})
fog_state = type('fog_state', (Node,), {'name': 'fog_state'})
force_field = type('force_field', (Node,), {'name': 'force_field'})
formula = type('formula', (Node,), {'name': 'formula'})
frame_object = type('frame_object', (Node,), {'name': 'frame_object'})
frame_origin = type('frame_origin', (Node,), {'name': 'frame_origin'})
frame_tcp = type('frame_tcp', (Node,), {'name': 'frame_tcp'})
frame_tip = type('frame_tip', (Node,), {'name': 'frame_tip'})
front_face = type('front_face', (Node,), {'name': 'front_face'})
func = type('func', (Node,), {'name': 'func'})
geographic_location = type('geographic_location', (Node,), {'name': 'geographic_location'})
geometry = type('geometry', (Node,), {'name': 'geometry'})
gravity = type('gravity', (Node,), {'name': 'gravity'})
h = type('h', (Node,), {'name': 'h'})
half_extents = type('half_extents', (Node,), {'name': 'half_extents'})
height = type('height', (Node,), {'name': 'height'})
capsule = type('capsule', (Node,), {'name': 'capsule'})
binary = type('binary', (Node,), {'name': 'binary'})
init_from = type('init_from', (Node,), {'name': 'init_from'})
hint = type('hint', (Node,), {'name': 'hint'})
hollow = type('hollow', (Node,), {'name': 'hollow'})
IDREF_array = type('IDREF_array', (Node,), {'name': 'IDREF_array'})
image = type('image', (Node,), {'name': 'image'})
imager = type('imager', (Node,), {'name': 'imager'})
include = type('include', (Node,), {'name': 'include'})
index_of_refraction = type('index_of_refraction', (Node,), {'name': 'index_of_refraction'})
index = type('index', (Node,), {'name': 'index'})
inertia = type('inertia', (Node,), {'name': 'inertia'})
instance_rigid_body = type('instance_rigid_body', (Node,), {'name': 'instance_rigid_body'})
init_from = type('init_from', (Node,), {'name': 'init_from'})
inline = type('inline', (Node,), {'name': 'inline'})
emantic = type('emantic', (Node,), {'name': 'emantic'})
emantics = type('emantics', (Node,), {'name': 'emantics'})
instance_animation = type('instance_animation', (Node,), {'name': 'instance_animation'})
instance_articulated_system = type('instance_articulated_system', (Node,), {'name': 'instance_articulated_system'})
instance_camera = type('instance_camera', (Node,), {'name': 'instance_camera'})
instance_controller = type('instance_controller', (Node,), {'name': 'instance_controller'})
instance_effect = type('instance_effect', (Node,), {'name': 'instance_effect'})
instance_force_field = type('instance_force_field', (Node,), {'name': 'instance_force_field'})
instance_formula = type('instance_formula', (Node,), {'name': 'instance_formula'})
instance_geometry = type('instance_geometry', (Node,), {'name': 'instance_geometry'})
instance_image = type('instance_image', (Node,), {'name': 'instance_image'})
instance_joint = type('instance_joint', (Node,), {'name': 'instance_joint'})
instance_kinematics_model = type('instance_kinematics_model', (Node,), {'name': 'instance_kinematics_model'})
instance_kinematics_scene = type('instance_kinematics_scene', (Node,), {'name': 'instance_kinematics_scene'})
instance_light = type('instance_light', (Node,), {'name': 'instance_light'})
instance_material = type('instance_material', (Node,), {'name': 'instance_material'})
instance_material = type('instance_material', (Node,), {'name': 'instance_material'})
instance_node = type('instance_node', (Node,), {'name': 'instance_node'})
instance_physics_material = type('instance_physics_material', (Node,), {'name': 'instance_physics_material'})
instance_physics_model = type('instance_physics_model', (Node,), {'name': 'instance_physics_model'})
instance_physics_scene = type('instance_physics_scene', (Node,), {'name': 'instance_physics_scene'})
instance_rigid_body = type('instance_rigid_body', (Node,), {'name': 'instance_rigid_body'})
instance_rigid_constraint = type('instance_rigid_constraint', (Node,), {'name': 'instance_rigid_constraint'})
instance_visual_scene = type('instance_visual_scene', (Node,), {'name': 'instance_visual_scene'})
int_array = type('int_array', (Node,), {'name': 'int_array'})
interpenetrate = type('interpenetrate', (Node,), {'name': 'interpenetrate'})
jerk = type('jerk', (Node,), {'name': 'jerk'})
axis_info = type('axis_info', (Node,), {'name': 'axis_info'})
joint = type('joint', (Node,), {'name': 'joint'})
joints = type('joints', (Node,), {'name': 'joints'})
keywords = type('keywords', (Node,), {'name': 'keywords'})
kinematics_model = type('kinematics_model', (Node,), {'name': 'kinematics_model'})
kinematics_scene = type('kinematics_scene', (Node,), {'name': 'kinematics_scene'})
kinematics = type('kinematics', (Node,), {'name': 'kinematics'})
lambert = type('lambert', (Node,), {'name': 'lambert'})
latitude = type('latitude', (Node,), {'name': 'latitude'})
layer = type('layer', (Node,), {'name': 'layer'})
library_animation_clips = type('library_animation_clips', (Node,), {'name': 'library_animation_clips'})
library_animations = type('library_animations', (Node,), {'name': 'library_animations'})
library_articulated_systems = type('library_articulated_systems', (Node,), {'name': 'library_articulated_systems'})
library_cameras = type('library_cameras', (Node,), {'name': 'library_cameras'})
library_controllers = type('library_controllers', (Node,), {'name': 'library_controllers'})
library_effects = type('library_effects', (Node,), {'name': 'library_effects'})
library_force_fields = type('library_force_fields', (Node,), {'name': 'library_force_fields'})
library_formulas = type('library_formulas', (Node,), {'name': 'library_formulas'})
library_geometries = type('library_geometries', (Node,), {'name': 'library_geometries'})
library_images = type('library_images', (Node,), {'name': 'library_images'})
library_joints = type('library_joints', (Node,), {'name': 'library_joints'})
library_kinematics_models = type('library_kinematics_models', (Node,), {'name': 'library_kinematics_models'})
library_kinematics_scenes = type('library_kinematics_scenes', (Node,), {'name': 'library_kinematics_scenes'})
library_nodes = type('library_nodes', (Node,), {'name': 'library_nodes'})
library_physics_materials = type('library_physics_materials', (Node,), {'name': 'library_physics_materials'})
library_physics_models = type('library_physics_models', (Node,), {'name': 'library_physics_models'})
library_physics_scenes = type('library_physics_scenes', (Node,), {'name': 'library_physics_scenes'})
library_visual_scenes = type('library_visual_scenes', (Node,), {'name': 'library_visual_scenes'})
light_ambient = type('light_ambient', (Node,), {'name': 'light_ambient'})
light_constant_attenuation = type('light_constant_attenuation', (Node,), {'name': 'light_constant_attenuation'})
light_diffuse = type('light_diffuse', (Node,), {'name': 'light_diffuse'})
light_enable = type('light_enable', (Node,), {'name': 'light_enable'})
light_linear_attenuation = type('light_linear_attenuation', (Node,), {'name': 'light_linear_attenuation'})
light_model_ambient = type('light_model_ambient', (Node,), {'name': 'light_model_ambient'})
light_model_color_control = type('light_model_color_control', (Node,), {'name': 'light_model_color_control'})
light_model_local_viewer_enable = type('light_model_local_viewer_enable', (Node,), {'name': 'light_model_local_viewer_enable'})
light_model_two_side_enable = type('light_model_two_side_enable', (Node,), {'name': 'light_model_two_side_enable'})
light_position = type('light_position', (Node,), {'name': 'light_position'})
light_quadratic_attenuation = type('light_quadratic_attenuation', (Node,), {'name': 'light_quadratic_attenuation'})
light_specular = type('light_specular', (Node,), {'name': 'light_specular'})
light_spot_cutoff = type('light_spot_cutoff', (Node,), {'name': 'light_spot_cutoff'})
light_spot_direction = type('light_spot_direction', (Node,), {'name': 'light_spot_direction'})
light_spot_exponent = type('light_spot_exponent', (Node,), {'name': 'light_spot_exponent'})
lighting_enable = type('lighting_enable', (Node,), {'name': 'lighting_enable'})
lights = type('lights', (Node,), {'name': 'lights'})
limits = type('limits', (Node,), {'name': 'limits'})
axis_info = type('axis_info', (Node,), {'name': 'axis_info'})
prismatic = type('prismatic', (Node,), {'name': 'prismatic'})
revolute = type('revolute', (Node,), {'name': 'revolute'})
line_smooth_enable = type('line_smooth_enable', (Node,), {'name': 'line_smooth_enable'})
line_stipple_enable = type('line_stipple_enable', (Node,), {'name': 'line_stipple_enable'})
line_stipple = type('line_stipple', (Node,), {'name': 'line_stipple'})
line_width = type('line_width', (Node,), {'name': 'line_width'})
line = type('line', (Node,), {'name': 'line'})
linear_attenuation = type('linear_attenuation', (Node,), {'name': 'linear_attenuation'})
spot = type('spot', (Node,), {'name': 'spot'})
linear = type('linear', (Node,), {'name': 'linear'})
lines = type('lines', (Node,), {'name': 'lines'})
linestrips = type('linestrips', (Node,), {'name': 'linestrips'})
link = type('link', (Node,), {'name': 'link'})
linker = type('linker', (Node,), {'name': 'linker'})
locked = type('locked', (Node,), {'name': 'locked'})
logic_op_enable = type('logic_op_enable', (Node,), {'name': 'logic_op_enable'})
logic_op = type('logic_op', (Node,), {'name': 'logic_op'})
longitude = type('longitude', (Node,), {'name': 'longitude'})
lookout = type('lookout', (Node,), {'name': 'lookout'})
magfilter = type('magfilter', (Node,), {'name': 'magfilter'})
mass_frame = type('mass_frame', (Node,), {'name': 'mass_frame'})
rigid_body = type('rigid_body', (Node,), {'name': 'rigid_body'})
mass = type('mass', (Node,), {'name': 'mass'})
shape = type('shape', (Node,), {'name': 'shape'})
material_ambient = type('material_ambient', (Node,), {'name': 'material_ambient'})
material_diffuse = type('material_diffuse', (Node,), {'name': 'material_diffuse'})
material_emission = type('material_emission', (Node,), {'name': 'material_emission'})
material_shininess = type('material_shininess', (Node,), {'name': 'material_shininess'})
material_specular = type('material_specular', (Node,), {'name': 'material_specular'})
material = type('material', (Node,), {'name': 'material'})
matrix = type('matrix', (Node,), {'name': 'matrix'})
max_anisotropy = type('max_anisotropy', (Node,), {'name': 'max_anisotropy'})
mesh = type('mesh', (Node,), {'name': 'mesh'})
minfilter = type('minfilter', (Node,), {'name': 'minfilter'})
mip_bias = type('mip_bias', (Node,), {'name': 'mip_bias'})
mip_max_level = type('mip_max_level', (Node,), {'name': 'mip_max_level'})
mip_min_level = type('mip_min_level', (Node,), {'name': 'mip_min_level'})
mipfilter = type('mipfilter', (Node,), {'name': 'mipfilter'})
mips = type('mips', (Node,), {'name': 'mips'})
create_cube = type('create_cube', (Node,), {'name': 'create_cube'})
create2d = type('create2d', (Node,), {'name': 'create2d'})
create3d = type('create3d', (Node,), {'name': 'create3d'})
model_view_matrix = type('model_view_matrix', (Node,), {'name': 'model_view_matrix'})
modified = type('modified', (Node,), {'name': 'modified'})
modifier = type('modifier', (Node,), {'name': 'modifier'})
morph = type('morph', (Node,), {'name': 'morph'})
motion = type('motion', (Node,), {'name': 'motion'})
multisample_enable = type('multisample_enable', (Node,), {'name': 'multisample_enable'})
Name_array = type('Name_array', (Node,), {'name': 'Name_array'})
emantic = type('emantic', (Node,), {'name': 'emantic'})
newparam = type('newparam', (Node,), {'name': 'newparam'})
ommon = type('ommon', (Node,), {'name': 'ommon'})
node = type('node', (Node,), {'name': 'node'})
normalize_enable = type('normalize_enable', (Node,), {'name': 'normalize_enable'})
nurbs_surface = type('nurbs_surface', (Node,), {'name': 'nurbs_surface'})
nurbs = type('nurbs', (Node,), {'name': 'nurbs'})
optics = type('optics', (Node,), {'name': 'optics'})
orient = type('orient', (Node,), {'name': 'orient'})
origin = type('origin', (Node,), {'name': 'origin'})
orthographic = type('orthographic', (Node,), {'name': 'orthographic'})
p = type('p', (Node,), {'name': 'p'})
edges = type('edges', (Node,), {'name': 'edges'})
faces = type('faces', (Node,), {'name': 'faces'})
lines = type('lines', (Node,), {'name': 'lines'})
pcurves = type('pcurves', (Node,), {'name': 'pcurves'})
ph = type('ph', (Node,), {'name': 'ph'})
solids = type('solids', (Node,), {'name': 'solids'})
triangles = type('triangles', (Node,), {'name': 'triangles'})
trifans = type('trifans', (Node,), {'name': 'trifans'})
tristrips = type('tristrips', (Node,), {'name': 'tristrips'})
wires = type('wires', (Node,), {'name': 'wires'})
parabola = type('parabola', (Node,), {'name': 'parabola'})
param = type('param', (Node,), {'name': 'param'})
ph = type('ph', (Node,), {'name': 'ph'})
phong = type('phong', (Node,), {'name': 'phong'})
physics_material = type('physics_material', (Node,), {'name': 'physics_material'})
physics_model = type('physics_model', (Node,), {'name': 'physics_model'})
physics_scene = type('physics_scene', (Node,), {'name': 'physics_scene'})
plane = type('plane', (Node,), {'name': 'plane'})
point_distance_attenuation = type('point_distance_attenuation', (Node,), {'name': 'point_distance_attenuation'})
point_fade_threshold_size = type('point_fade_threshold_size', (Node,), {'name': 'point_fade_threshold_size'})
point_size_max = type('point_size_max', (Node,), {'name': 'point_size_max'})
point_size_min = type('point_size_min', (Node,), {'name': 'point_size_min'})
point_size = type('point_size', (Node,), {'name': 'point_size'})
point_smooth_enable = type('point_smooth_enable', (Node,), {'name': 'point_smooth_enable'})
polygon_mode = type('polygon_mode', (Node,), {'name': 'polygon_mode'})
polygon_offset_fill_enable = type('polygon_offset_fill_enable', (Node,), {'name': 'polygon_offset_fill_enable'})
polygon_offset_line_enable = type('polygon_offset_line_enable', (Node,), {'name': 'polygon_offset_line_enable'})
polygon_offset_point_enable = type('polygon_offset_point_enable', (Node,), {'name': 'polygon_offset_point_enable'})
polygon_offset = type('polygon_offset', (Node,), {'name': 'polygon_offset'})
polygon_smooth_enable = type('polygon_smooth_enable', (Node,), {'name': 'polygon_smooth_enable'})
polygon_stipple_enable = type('polygon_stipple_enable', (Node,), {'name': 'polygon_stipple_enable'})
polygons = type('polygons', (Node,), {'name': 'polygons'})
polylist = type('polylist', (Node,), {'name': 'polylist'})
prismatic = type('prismatic', (Node,), {'name': 'prismatic'})
profile_BRIDGE = type('profile_BRIDGE', (Node,), {'name': 'profile_BRIDGE'})
profile_CG = type('profile_CG', (Node,), {'name': 'profile_CG'})
profile_COMMON = type('profile_COMMON', (Node,), {'name': 'profile_COMMON'})
verview = type('verview', (Node,), {'name': 'verview'})
profile_GLES = type('profile_GLES', (Node,), {'name': 'profile_GLES'})
profile_GLES2 = type('profile_GLES2', (Node,), {'name': 'profile_GLES2'})
profile_GLSL = type('profile_GLSL', (Node,), {'name': 'profile_GLSL'})
program = type('program', (Node,), {'name': 'program'})
projection_matrix = type('projection_matrix', (Node,), {'name': 'projection_matrix'})
quadratic_attenuation = type('quadratic_attenuation', (Node,), {'name': 'quadratic_attenuation'})
point = type('point', (Node,), {'name': 'point'})
radius = type('radius', (Node,), {'name': 'radius'})
capsule = type('capsule', (Node,), {'name': 'capsule'})
circle = type('circle', (Node,), {'name': 'circle'})
cone = type('cone', (Node,), {'name': 'cone'})
cylinder = type('cylinder', (Node,), {'name': 'cylinder'})
ellipse = type('ellipse', (Node,), {'name': 'ellipse'})
hyperbola = type('hyperbola', (Node,), {'name': 'hyperbola'})
torus = type('torus', (Node,), {'name': 'torus'})
ref_attachment = type('ref_attachment', (Node,), {'name': 'ref_attachment'})
ref = type('ref', (Node,), {'name': 'ref'})
binary = type('binary', (Node,), {'name': 'binary'})
init_from = type('init_from', (Node,), {'name': 'init_from'})
reflective = type('reflective', (Node,), {'name': 'reflective'})
reflectivity = type('reflectivity', (Node,), {'name': 'reflectivity'})
render = type('render', (Node,), {'name': 'render'})
renderable = type('renderable', (Node,), {'name': 'renderable'})
rescale_normal_enable = type('rescale_normal_enable', (Node,), {'name': 'rescale_normal_enable'})
restitution = type('restitution', (Node,), {'name': 'restitution'})
revision = type('revision', (Node,), {'name': 'revision'})
revolute = type('revolute', (Node,), {'name': 'revolute'})
RGB = type('RGB', (Node,), {'name': 'RGB'})
rigid_constraint = type('rigid_constraint', (Node,), {'name': 'rigid_constraint'})
rotate = type('rotate', (Node,), {'name': 'rotate'})
sample_alpha_to_coverage_enable = type('sample_alpha_to_coverage_enable', (Node,), {'name': 'sample_alpha_to_coverage_enable'})
sample_alpha_to_one_enable = type('sample_alpha_to_one_enable', (Node,), {'name': 'sample_alpha_to_one_enable'})
sample_coverage_enable = type('sample_coverage_enable', (Node,), {'name': 'sample_coverage_enable'})
sample_coverage = type('sample_coverage', (Node,), {'name': 'sample_coverage'})
sampler_image = type('sampler_image', (Node,), {'name': 'sampler_image'})
sampler_states = type('sampler_states', (Node,), {'name': 'sampler_states'})
sampler = type('sampler', (Node,), {'name': 'sampler'})
nterpolation = type('nterpolation', (Node,), {'name': 'nterpolation'})
sampler1D = type('sampler1D', (Node,), {'name': 'sampler1D'})
sampler2D = type('sampler2D', (Node,), {'name': 'sampler2D'})
sampler3D = type('sampler3D', (Node,), {'name': 'sampler3D'})
samplerCUBE = type('samplerCUBE', (Node,), {'name': 'samplerCUBE'})
samplerDEPTH = type('samplerDEPTH', (Node,), {'name': 'samplerDEPTH'})
samplerRECT = type('samplerRECT', (Node,), {'name': 'samplerRECT'})
scale = type('scale', (Node,), {'name': 'scale'})
scene = type('scene', (Node,), {'name': 'scene'})
scissor_test_enable = type('scissor_test_enable', (Node,), {'name': 'scissor_test_enable'})
scissor = type('scissor', (Node,), {'name': 'scissor'})
semantic = type('semantic', (Node,), {'name': 'semantic'})
setparam = type('setparam', (Node,), {'name': 'setparam'})
shade_model = type('shade_model', (Node,), {'name': 'shade_model'})
shader = type('shader', (Node,), {'name': 'shader'})
shape = type('shape', (Node,), {'name': 'shape'})
shells = type('shells', (Node,), {'name': 'shells'})
shininess = type('shininess', (Node,), {'name': 'shininess'})
SIDREF_array = type('SIDREF_array', (Node,), {'name': 'SIDREF_array'})
size_exact = type('size_exact', (Node,), {'name': 'size_exact'})
size_ratio = type('size_ratio', (Node,), {'name': 'size_ratio'})
size = type('size', (Node,), {'name': 'size'})
create_cube = type('create_cube', (Node,), {'name': 'create_cube'})
create3d = type('create3d', (Node,), {'name': 'create3d'})
skeleton = type('skeleton', (Node,), {'name': 'skeleton'})
skew = type('skew', (Node,), {'name': 'skew'})
skin = type('skin', (Node,), {'name': 'skin'})
source_data = type('source_data', (Node,), {'name': 'source_data'})
source = type('source', (Node,), {'name': 'source'})
sources = type('sources', (Node,), {'name': 'sources'})
specular = type('specular', (Node,), {'name': 'specular'})
speed = type('speed', (Node,), {'name': 'speed'})
sphere = type('sphere', (Node,), {'name': 'sphere'})
spline = type('spline', (Node,), {'name': 'spline'})
nterpolation = type('nterpolation', (Node,), {'name': 'nterpolation'})
spot = type('spot', (Node,), {'name': 'spot'})
spring = type('spring', (Node,), {'name': 'spring'})
states = type('states', (Node,), {'name': 'states'})
static_friction = type('static_friction', (Node,), {'name': 'static_friction'})
stencil_clear = type('stencil_clear', (Node,), {'name': 'stencil_clear'})
stencil_func_separate = type('stencil_func_separate', (Node,), {'name': 'stencil_func_separate'})
stencil_func = type('stencil_func', (Node,), {'name': 'stencil_func'})
stencil_mask_separate = type('stencil_mask_separate', (Node,), {'name': 'stencil_mask_separate'})
stencil_mask = type('stencil_mask', (Node,), {'name': 'stencil_mask'})
stencil_op_separate = type('stencil_op_separate', (Node,), {'name': 'stencil_op_separate'})
stencil_op = type('stencil_op', (Node,), {'name': 'stencil_op'})
stencil_target = type('stencil_target', (Node,), {'name': 'stencil_target'})
stencil_test_enable = type('stencil_test_enable', (Node,), {'name': 'stencil_test_enable'})
stiffness = type('stiffness', (Node,), {'name': 'stiffness'})
subject = type('subject', (Node,), {'name': 'subject'})
surface_curves = type('surface_curves', (Node,), {'name': 'surface_curves'})
surface = type('surface', (Node,), {'name': 'surface'})
surfaces = type('surfaces', (Node,), {'name': 'surfaces'})
swept_surface = type('swept_surface', (Node,), {'name': 'swept_surface'})
swing_cone_and_twist = type('swing_cone_and_twist', (Node,), {'name': 'swing_cone_and_twist'})
target_value = type('target_value', (Node,), {'name': 'target_value'})
target = type('target', (Node,), {'name': 'target'})
targets = type('targets', (Node,), {'name': 'targets'})
bind_material = type('bind_material', (Node,), {'name': 'bind_material'})
formula = type('formula', (Node,), {'name': 'formula'})
instance_rigid_body = type('instance_rigid_body', (Node,), {'name': 'instance_rigid_body'})
kinematics_model = type('kinematics_model', (Node,), {'name': 'kinematics_model'})
kinematics = type('kinematics', (Node,), {'name': 'kinematics'})
light = type('light', (Node,), {'name': 'light'})
motion = type('motion', (Node,), {'name': 'motion'})
optics = type('optics', (Node,), {'name': 'optics'})
rigid_body = type('rigid_body', (Node,), {'name': 'rigid_body'})
verview = type('verview', (Node,), {'name': 'verview'})
technique_hint = type('technique_hint', (Node,), {'name': 'technique_hint'})
technique_override = type('technique_override', (Node,), {'name': 'technique_override'})
texcombiner = type('texcombiner', (Node,), {'name': 'texcombiner'})
texcoord = type('texcoord', (Node,), {'name': 'texcoord'})
texenv = type('texenv', (Node,), {'name': 'texenv'})
texture_env_color = type('texture_env_color', (Node,), {'name': 'texture_env_color'})
texture_env_mode = type('texture_env_mode', (Node,), {'name': 'texture_env_mode'})
texture_pipeline = type('texture_pipeline', (Node,), {'name': 'texture_pipeline'})
texture = type('texture', (Node,), {'name': 'texture'})
texture1D_enable = type('texture1D_enable', (Node,), {'name': 'texture1D_enable'})
texture1D = type('texture1D', (Node,), {'name': 'texture1D'})
texture2D_enable = type('texture2D_enable', (Node,), {'name': 'texture2D_enable'})
texture2D = type('texture2D', (Node,), {'name': 'texture2D'})
texture3D_enable = type('texture3D_enable', (Node,), {'name': 'texture3D_enable'})
texture3D = type('texture3D', (Node,), {'name': 'texture3D'})
textureCUBE_enable = type('textureCUBE_enable', (Node,), {'name': 'textureCUBE_enable'})
textureCUBE = type('textureCUBE', (Node,), {'name': 'textureCUBE'})
textureDEPTH_enable = type('textureDEPTH_enable', (Node,), {'name': 'textureDEPTH_enable'})
textureDEPTH = type('textureDEPTH', (Node,), {'name': 'textureDEPTH'})
textureRECT_enable = type('textureRECT_enable', (Node,), {'name': 'textureRECT_enable'})
textureRECT = type('textureRECT', (Node,), {'name': 'textureRECT'})
time_step = type('time_step', (Node,), {'name': 'time_step'})
title = type('title', (Node,), {'name': 'title'})
translate = type('translate', (Node,), {'name': 'translate'})
transparency = type('transparency', (Node,), {'name': 'transparency'})
transparent = type('transparent', (Node,), {'name': 'transparent'})
unit = type('unit', (Node,), {'name': 'unit'})
unnormalized = type('unnormalized', (Node,), {'name': 'unnormalized'})
usertype = type('usertype', (Node,), {'name': 'usertype'})
v = type('v', (Node,), {'name': 'v'})
value = type('value', (Node,), {'name': 'value'})
velocity = type('velocity', (Node,), {'name': 'velocity'})
vertex_weights = type('vertex_weights', (Node,), {'name': 'vertex_weights'})
wrap_p = type('wrap_p', (Node,), {'name': 'wrap_p'})
wrap_s = type('wrap_s', (Node,), {'name': 'wrap_s'})
wrap_t = type('wrap_t', (Node,), {'name': 'wrap_t'})
xfov = type('xfov', (Node,), {'name': 'xfov'})
xmag = type('xmag', (Node,), {'name': 'xmag'})
yfov = type('yfov', (Node,), {'name': 'yfov'})
ymag = type('ymag', (Node,), {'name': 'ymag'})
zfar = type('zfar', (Node,), {'name': 'zfar'})
znear = type('znear', (Node,), {'name': 'znear'})

# builtins require an underscore.
_input = type('input', (closed_tag,), {'name': 'input'})
_float = type('float', (Node,), {'name': 'float'})
_pass = type('pass', (Node,), {'name': 'pass'})
_max = type('max', (Node,), {'name': 'max'})
_min = type('min', (Node,), {'name': 'min'})
_import = type('import', (Node,), {'name': 'import'})
_hex = type('hex', (Node,), {'name': 'hex'})
_format = type('format', (Node,), {'name': 'format'})


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
