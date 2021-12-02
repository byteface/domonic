"""
    domonic.collada
    ====================================
    Generate Collada with python 3

"""

from domonic.html import closed_tag
from domonic.dom import Element


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


COLLADA = type('COLLADA', (Element,), {'name': 'COLLADA'})

asset = type('asset', (Element,), {'name': 'asset'})
library_cameras = type('library_cameras', (Element,), {'name': 'library_cameras'})
library_lights = type('library_lights', (Element,), {'name': 'library_lights'})
library_materials = type('library_materials', (Element,), {'name': 'library_materials'})
library_effects = type('library_effects', (Element,), {'name': 'library_effects'})
library_geometries = type('library_geometries', (Element,), {'name': 'library_geometries'})
library_visual_scenes = type('library_visual_scenes', (Element,), {'name': 'library_visual_scenes'})
scene = type('scene', (Element,), {'name': 'scene'})
extra = type('extra', (Element,), {'name': 'extra'})
author = type('author', (Element,), {'name': 'author'})
up_axis = type('up_axis', (Element,), {'name': 'up_axis'})
camera = type('camera', (Element,), {'name': 'camera'})
optics = type('optics', (Element,), {'name': 'optics'})
technique = type('technique', (Element,), {'name': 'technique'})
technique_common = type('technique_common', (Element,), {'name': 'technique_common'})
aspect_ratio = type('aspect_ratio', (Element,), {'name': 'aspect_ratio'})
light = type('light', (Element,), {'name': 'light'})
constant_attenuation = type('constant_attenuation', (Element,), {'name': 'constant_attenuation'})
linear_attenuation = type('linear_attenuation', (Element,), {'name': 'linear_attenuation'})
quadratic_attenuation = type('quadratic_attenuation', (Element,), {'name': 'quadratic_attenuation'})
material = type('material', (Element,), {'name': 'material'})
effect = type('effect', (Element,), {'name': 'effect'})
profile_COMMON = type('profile_COMMON', (Element,), {'name': 'profile_COMMON'})
phong = type('phong', (Element,), {'name': 'phong'})
emission = type('emission', (Element,), {'name': 'emission'})
geometry = type('geometry', (Element,), {'name': 'geometry'})
mesh = type('mesh', (Element,), {'name': 'mesh'})
source = type('source', (Element,), {'name': 'source'})
vertices = type('vertices', (Element,), {'name': 'vertices'})
polylist = type('polylist', (Element,), {'name': 'polylist'})
vcount = type('vcount', (Element,), {'name': 'vcount'})
p = type('p', (Element,), {'name': 'p'})
library_visual_scenes = type('library_visual_scenes', (Element,), {'name': 'library_visual_scenes'})
visual_scene = type('visual_scene', (Element,), {'name': 'visual_scene'})
node = type('node', (Element,), {'name': 'node'})
instance_visual_scene = type('instance_visual_scene', (Element,), {'name': 'instance_visual_scene'})
test_element = type('test_element', (Element,), {'name': 'test_element'})
instance_effect = type('instance_effect', (closed_tag,), {'name': 'instance_effect'})
texture_unit = type('texture_unit', (closed_tag,), {'name': 'texture_unit'})
tapered_cylinder = type('tapered_cylinder', (closed_tag,), {'name': 'tapered_cylinder'})
tapered_capsule = type('tapered_capsule', (closed_tag,), {'name': 'tapered_capsule'})
format_hint = type('format_hint', (closed_tag,), {'name': 'format_hint'})
revisions = type('revisions', (closed_tag,), {'name': 'revisions'})
contributer = type('contributer', (closed_tag,), {'name': 'contributer'})
acceleration = type('acceleration', (Element,), {'name': 'acceleration'})
axis_info = type('axis_info', (Element,), {'name': 'axis_info'})
accessor = type('accessor', (Element,), {'name': 'accessor'})
active = type('active', (Element,), {'name': 'active'})
alpha_func = type('alpha_func', (Element,), {'name': 'alpha_func'})
alpha_test_enable = type('alpha_test_enable', (Element,), {'name': 'alpha_test_enable'})
alpha = type('alpha', (Element,), {'name': 'alpha'})
altitude = type('altitude', (Element,), {'name': 'altitude'})
ambient = type('ambient', (Element,), {'name': 'ambient'})
angle = type('angle', (Element,), {'name': 'angle'})
angular_velocity = type('angular_velocity', (Element,), {'name': 'angular_velocity'})
angular = type('angular', (Element,), {'name': 'angular'})
animation_clip = type('animation_clip', (Element,), {'name': 'animation_clip'})
animation = type('animation', (Element,), {'name': 'animation'})
annotate = type('annotate', (Element,), {'name': 'annotate'})
argument = type('argument', (Element,), {'name': 'argument'})
array = type('array', (Element,), {'name': 'array'})
articulated_system = type('articulated_system', (Element,), {'name': 'articulated_system'})
perspective = type('perspective', (Element,), {'name': 'perspective'})
asset = type('asset', (Element,), {'name': 'asset'})
se = type('se', (Element,), {'name': 'se'})
attachment_end = type('attachment_end', (Element,), {'name': 'attachment_end'})
attachment_full = type('attachment_full', (Element,), {'name': 'attachment_full'})
attachment_start = type('attachment_start', (Element,), {'name': 'attachment_start'})
attachment = type('attachment', (Element,), {'name': 'attachment'})
author_email = type('author_email', (Element,), {'name': 'author_email'})
author_website = type('author_website', (Element,), {'name': 'author_website'})
author = type('author', (Element,), {'name': 'author'})
authoring_tool = type('authoring_tool', (Element,), {'name': 'authoring_tool'})
auto_normal_enable = type('auto_normal_enable', (Element,), {'name': 'auto_normal_enable'})
axis_info = type('axis_info', (Element,), {'name': 'axis_info'})
axis = type('axis', (Element,), {'name': 'axis'})
prismatic = type('prismatic', (Element,), {'name': 'prismatic'})
revolute = type('revolute', (Element,), {'name': 'revolute'})
swept_surface = type('swept_surface', (Element,), {'name': 'swept_surface'})
binary = type('binary', (Element,), {'name': 'binary'})
bind_attribute = type('bind_attribute', (Element,), {'name': 'bind_attribute'})
bind_joint_axis = type('bind_joint_axis', (Element,), {'name': 'bind_joint_axis'})
bind_kinematics_model = type('bind_kinematics_model', (Element,), {'name': 'bind_kinematics_model'})
bind_shape_matrix = type('bind_shape_matrix', (Element,), {'name': 'bind_shape_matrix'})
bind_uniform = type('bind_uniform', (Element,), {'name': 'bind_uniform'})
bind_vertex_input = type('bind_vertex_input', (Element,), {'name': 'bind_vertex_input'})
bind = type('bind', (Element,), {'name': 'bind'})
bind = type('bind', (Element,), {'name': 'bind'})
blend_color = type('blend_color', (Element,), {'name': 'blend_color'})
blend_enable = type('blend_enable', (Element,), {'name': 'blend_enable'})
blend_equation_separate = type('blend_equation_separate', (Element,), {'name': 'blend_equation_separate'})
blend_equation = type('blend_equation', (Element,), {'name': 'blend_equation'})
blend_func_separate = type('blend_func_separate', (Element,), {'name': 'blend_func_separate'})
blend_func = type('blend_func', (Element,), {'name': 'blend_func'})
blinn = type('blinn', (Element,), {'name': 'blinn'})
bool_array = type('bool_array', (Element,), {'name': 'bool_array'})
border_color = type('border_color', (Element,), {'name': 'border_color'})
box = type('box', (Element,), {'name': 'box'})
brep = type('brep', (Element,), {'name': 'brep'})
camera = type('camera', (Element,), {'name': 'camera'})
capsule = type('capsule', (Element,), {'name': 'capsule'})
channel = type('channel', (Element,), {'name': 'channel'})
arget = type('arget', (Element,), {'name': 'arget'})
circle = type('circle', (Element,), {'name': 'circle'})
clip_plane_enable = type('clip_plane_enable', (Element,), {'name': 'clip_plane_enable'})
clip_plane = type('clip_plane', (Element,), {'name': 'clip_plane'})
code = type('code', (Element,), {'name': 'code'})
color_clear = type('color_clear', (Element,), {'name': 'color_clear'})
color_logic_op_enable = type('color_logic_op_enable', (Element,), {'name': 'color_logic_op_enable'})
color_mask = type('color_mask', (Element,), {'name': 'color_mask'})
color_material_enable = type('color_material_enable', (Element,), {'name': 'color_material_enable'})
color_material = type('color_material', (Element,), {'name': 'color_material'})
color_target = type('color_target', (Element,), {'name': 'color_target'})
color = type('color', (Element,), {'name': 'color'})
comments = type('comments', (Element,), {'name': 'comments'})
compiler = type('compiler', (Element,), {'name': 'compiler'})
cone = type('cone', (Element,), {'name': 'cone'})
connect_param = type('connect_param', (Element,), {'name': 'connect_param'})
point = type('point', (Element,), {'name': 'point'})
spot = type('spot', (Element,), {'name': 'spot'})
constant = type('constant', (Element,), {'name': 'constant'})
constant = type('constant', (Element,), {'name': 'constant'})
contributor = type('contributor', (Element,), {'name': 'contributor'})
control_vertices = type('control_vertices', (Element,), {'name': 'control_vertices'})
controller = type('controller', (Element,), {'name': 'controller'})
convex_mesh = type('convex_mesh', (Element,), {'name': 'convex_mesh'})
copyright = type('copyright', (Element,), {'name': 'copyright'})
coverage = type('coverage', (Element,), {'name': 'coverage'})
create_2d = type('create_2d', (Element,), {'name': 'create_2d'})
create_3d = type('create_3d', (Element,), {'name': 'create_3d'})
create_cube = type('create_cube', (Element,), {'name': 'create_cube'})
created = type('created', (Element,), {'name': 'created'})
cull_face_enable = type('cull_face_enable', (Element,), {'name': 'cull_face_enable'})
cull_face = type('cull_face', (Element,), {'name': 'cull_face'})
curve = type('curve', (Element,), {'name': 'curve'})
curves = type('curves', (Element,), {'name': 'curves'})
cylinder = type('cylinder', (Element,), {'name': 'cylinder'})
cylinder = type('cylinder', (Element,), {'name': 'cylinder'})
damping = type('damping', (Element,), {'name': 'damping'})
deceleration = type('deceleration', (Element,), {'name': 'deceleration'})
axis_info = type('axis_info', (Element,), {'name': 'axis_info'})
effector_info = type('effector_info', (Element,), {'name': 'effector_info'})
density = type('density', (Element,), {'name': 'density'})
depth_bounds_enable = type('depth_bounds_enable', (Element,), {'name': 'depth_bounds_enable'})
depth_bounds = type('depth_bounds', (Element,), {'name': 'depth_bounds'})
depth_clamp_enable = type('depth_clamp_enable', (Element,), {'name': 'depth_clamp_enable'})
depth_clear = type('depth_clear', (Element,), {'name': 'depth_clear'})
depth_func = type('depth_func', (Element,), {'name': 'depth_func'})
depth_mask = type('depth_mask', (Element,), {'name': 'depth_mask'})
depth_range = type('depth_range', (Element,), {'name': 'depth_range'})
depth_target = type('depth_target', (Element,), {'name': 'depth_target'})
depth_test_enable = type('depth_test_enable', (Element,), {'name': 'depth_test_enable'})
diffuse = type('diffuse', (Element,), {'name': 'diffuse'})
direction = type('direction', (Element,), {'name': 'direction'})
line = type('line', (Element,), {'name': 'line'})
swept_surface = type('swept_surface', (Element,), {'name': 'swept_surface'})
directional = type('directional', (Element,), {'name': 'directional'})
dither_enable = type('dither_enable', (Element,), {'name': 'dither_enable'})
draw = type('draw', (Element,), {'name': 'draw'})
dynamic_friction = type('dynamic_friction', (Element,), {'name': 'dynamic_friction'})
dynamic = type('dynamic', (Element,), {'name': 'dynamic'})
edges = type('edges', (Element,), {'name': 'edges'})
effect = type('effect', (Element,), {'name': 'effect'})
effector_info = type('effector_info', (Element,), {'name': 'effector_info'})
ellipse = type('ellipse', (Element,), {'name': 'ellipse'})
emission = type('emission', (Element,), {'name': 'emission'})
enabled = type('enabled', (Element,), {'name': 'enabled'})
equation = type('equation', (Element,), {'name': 'equation'})
evaluate_scene = type('evaluate_scene', (Element,), {'name': 'evaluate_scene'})
evaluate = type('evaluate', (Element,), {'name': 'evaluate'})
exact = type('exact', (Element,), {'name': 'exact'})
extra = type('extra', (Element,), {'name': 'extra'})
faces = type('faces', (Element,), {'name': 'faces'})
falloff_angle = type('falloff_angle', (Element,), {'name': 'falloff_angle'})
falloff_exponent = type('falloff_exponent', (Element,), {'name': 'falloff_exponent'})
float_array = type('float_array', (Element,), {'name': 'float_array'})
focal = type('focal', (Element,), {'name': 'focal'})
fog_color = type('fog_color', (Element,), {'name': 'fog_color'})
fog_coord_src = type('fog_coord_src', (Element,), {'name': 'fog_coord_src'})
fog_density = type('fog_density', (Element,), {'name': 'fog_density'})
fog_enable = type('fog_enable', (Element,), {'name': 'fog_enable'})
fog_end = type('fog_end', (Element,), {'name': 'fog_end'})
fog_mode = type('fog_mode', (Element,), {'name': 'fog_mode'})
fog_state = type('fog_state', (Element,), {'name': 'fog_state'})
force_field = type('force_field', (Element,), {'name': 'force_field'})
formula = type('formula', (Element,), {'name': 'formula'})
frame_object = type('frame_object', (Element,), {'name': 'frame_object'})
frame_origin = type('frame_origin', (Element,), {'name': 'frame_origin'})
frame_tcp = type('frame_tcp', (Element,), {'name': 'frame_tcp'})
frame_tip = type('frame_tip', (Element,), {'name': 'frame_tip'})
front_face = type('front_face', (Element,), {'name': 'front_face'})
func = type('func', (Element,), {'name': 'func'})
geographic_location = type('geographic_location', (Element,), {'name': 'geographic_location'})
geometry = type('geometry', (Element,), {'name': 'geometry'})
gravity = type('gravity', (Element,), {'name': 'gravity'})
h = type('h', (Element,), {'name': 'h'})
half_extents = type('half_extents', (Element,), {'name': 'half_extents'})
height = type('height', (Element,), {'name': 'height'})
capsule = type('capsule', (Element,), {'name': 'capsule'})
binary = type('binary', (Element,), {'name': 'binary'})
init_from = type('init_from', (Element,), {'name': 'init_from'})
hint = type('hint', (Element,), {'name': 'hint'})
hollow = type('hollow', (Element,), {'name': 'hollow'})
IDREF_array = type('IDREF_array', (Element,), {'name': 'IDREF_array'})
image = type('image', (Element,), {'name': 'image'})
imager = type('imager', (Element,), {'name': 'imager'})
include = type('include', (Element,), {'name': 'include'})
index_of_refraction = type('index_of_refraction', (Element,), {'name': 'index_of_refraction'})
index = type('index', (Element,), {'name': 'index'})
inertia = type('inertia', (Element,), {'name': 'inertia'})
instance_rigid_body = type('instance_rigid_body', (Element,), {'name': 'instance_rigid_body'})
init_from = type('init_from', (Element,), {'name': 'init_from'})
inline = type('inline', (Element,), {'name': 'inline'})
emantic = type('emantic', (Element,), {'name': 'emantic'})
emantics = type('emantics', (Element,), {'name': 'emantics'})
instance_animation = type('instance_animation', (Element,), {'name': 'instance_animation'})
instance_articulated_system = type('instance_articulated_system', (Element,), {'name': 'instance_articulated_system'})
instance_camera = type('instance_camera', (Element,), {'name': 'instance_camera'})
instance_controller = type('instance_controller', (Element,), {'name': 'instance_controller'})
instance_effect = type('instance_effect', (Element,), {'name': 'instance_effect'})
instance_force_field = type('instance_force_field', (Element,), {'name': 'instance_force_field'})
instance_formula = type('instance_formula', (Element,), {'name': 'instance_formula'})
instance_geometry = type('instance_geometry', (Element,), {'name': 'instance_geometry'})
instance_image = type('instance_image', (Element,), {'name': 'instance_image'})
instance_joint = type('instance_joint', (Element,), {'name': 'instance_joint'})
instance_kinematics_model = type('instance_kinematics_model', (Element,), {'name': 'instance_kinematics_model'})
instance_kinematics_scene = type('instance_kinematics_scene', (Element,), {'name': 'instance_kinematics_scene'})
instance_light = type('instance_light', (Element,), {'name': 'instance_light'})
instance_material = type('instance_material', (Element,), {'name': 'instance_material'})
instance_material = type('instance_material', (Element,), {'name': 'instance_material'})
instance_node = type('instance_node', (Element,), {'name': 'instance_node'})
instance_physics_material = type('instance_physics_material', (Element,), {'name': 'instance_physics_material'})
instance_physics_model = type('instance_physics_model', (Element,), {'name': 'instance_physics_model'})
instance_physics_scene = type('instance_physics_scene', (Element,), {'name': 'instance_physics_scene'})
instance_rigid_body = type('instance_rigid_body', (Element,), {'name': 'instance_rigid_body'})
instance_rigid_constraint = type('instance_rigid_constraint', (Element,), {'name': 'instance_rigid_constraint'})
instance_visual_scene = type('instance_visual_scene', (Element,), {'name': 'instance_visual_scene'})
int_array = type('int_array', (Element,), {'name': 'int_array'})
interpenetrate = type('interpenetrate', (Element,), {'name': 'interpenetrate'})
jerk = type('jerk', (Element,), {'name': 'jerk'})
axis_info = type('axis_info', (Element,), {'name': 'axis_info'})
joint = type('joint', (Element,), {'name': 'joint'})
joints = type('joints', (Element,), {'name': 'joints'})
keywords = type('keywords', (Element,), {'name': 'keywords'})
kinematics_model = type('kinematics_model', (Element,), {'name': 'kinematics_model'})
kinematics_scene = type('kinematics_scene', (Element,), {'name': 'kinematics_scene'})
kinematics = type('kinematics', (Element,), {'name': 'kinematics'})
lambert = type('lambert', (Element,), {'name': 'lambert'})
latitude = type('latitude', (Element,), {'name': 'latitude'})
layer = type('layer', (Element,), {'name': 'layer'})
library_animation_clips = type('library_animation_clips', (Element,), {'name': 'library_animation_clips'})
library_animations = type('library_animations', (Element,), {'name': 'library_animations'})
library_articulated_systems = type('library_articulated_systems', (Element,), {'name': 'library_articulated_systems'})
library_cameras = type('library_cameras', (Element,), {'name': 'library_cameras'})
library_controllers = type('library_controllers', (Element,), {'name': 'library_controllers'})
library_effects = type('library_effects', (Element,), {'name': 'library_effects'})
library_force_fields = type('library_force_fields', (Element,), {'name': 'library_force_fields'})
library_formulas = type('library_formulas', (Element,), {'name': 'library_formulas'})
library_geometries = type('library_geometries', (Element,), {'name': 'library_geometries'})
library_images = type('library_images', (Element,), {'name': 'library_images'})
library_joints = type('library_joints', (Element,), {'name': 'library_joints'})
library_kinematics_models = type('library_kinematics_models', (Element,), {'name': 'library_kinematics_models'})
library_kinematics_scenes = type('library_kinematics_scenes', (Element,), {'name': 'library_kinematics_scenes'})
library_nodes = type('library_nodes', (Element,), {'name': 'library_nodes'})
library_physics_materials = type('library_physics_materials', (Element,), {'name': 'library_physics_materials'})
library_physics_models = type('library_physics_models', (Element,), {'name': 'library_physics_models'})
library_physics_scenes = type('library_physics_scenes', (Element,), {'name': 'library_physics_scenes'})
library_visual_scenes = type('library_visual_scenes', (Element,), {'name': 'library_visual_scenes'})
light_ambient = type('light_ambient', (Element,), {'name': 'light_ambient'})
light_constant_attenuation = type('light_constant_attenuation', (Element,), {'name': 'light_constant_attenuation'})
light_diffuse = type('light_diffuse', (Element,), {'name': 'light_diffuse'})
light_enable = type('light_enable', (Element,), {'name': 'light_enable'})
light_linear_attenuation = type('light_linear_attenuation', (Element,), {'name': 'light_linear_attenuation'})
light_model_ambient = type('light_model_ambient', (Element,), {'name': 'light_model_ambient'})
light_model_color_control = type('light_model_color_control', (Element,), {'name': 'light_model_color_control'})
light_model_local_viewer_enable = type('light_model_local_viewer_enable', (Element,), {'name': 'light_model_local_viewer_enable'})
light_model_two_side_enable = type('light_model_two_side_enable', (Element,), {'name': 'light_model_two_side_enable'})
light_position = type('light_position', (Element,), {'name': 'light_position'})
light_quadratic_attenuation = type('light_quadratic_attenuation', (Element,), {'name': 'light_quadratic_attenuation'})
light_specular = type('light_specular', (Element,), {'name': 'light_specular'})
light_spot_cutoff = type('light_spot_cutoff', (Element,), {'name': 'light_spot_cutoff'})
light_spot_direction = type('light_spot_direction', (Element,), {'name': 'light_spot_direction'})
light_spot_exponent = type('light_spot_exponent', (Element,), {'name': 'light_spot_exponent'})
lighting_enable = type('lighting_enable', (Element,), {'name': 'lighting_enable'})
lights = type('lights', (Element,), {'name': 'lights'})
limits = type('limits', (Element,), {'name': 'limits'})
axis_info = type('axis_info', (Element,), {'name': 'axis_info'})
prismatic = type('prismatic', (Element,), {'name': 'prismatic'})
revolute = type('revolute', (Element,), {'name': 'revolute'})
line_smooth_enable = type('line_smooth_enable', (Element,), {'name': 'line_smooth_enable'})
line_stipple_enable = type('line_stipple_enable', (Element,), {'name': 'line_stipple_enable'})
line_stipple = type('line_stipple', (Element,), {'name': 'line_stipple'})
line_width = type('line_width', (Element,), {'name': 'line_width'})
line = type('line', (Element,), {'name': 'line'})
linear_attenuation = type('linear_attenuation', (Element,), {'name': 'linear_attenuation'})
spot = type('spot', (Element,), {'name': 'spot'})
linear = type('linear', (Element,), {'name': 'linear'})
lines = type('lines', (Element,), {'name': 'lines'})
linestrips = type('linestrips', (Element,), {'name': 'linestrips'})
link = type('link', (Element,), {'name': 'link'})
linker = type('linker', (Element,), {'name': 'linker'})
locked = type('locked', (Element,), {'name': 'locked'})
logic_op_enable = type('logic_op_enable', (Element,), {'name': 'logic_op_enable'})
logic_op = type('logic_op', (Element,), {'name': 'logic_op'})
longitude = type('longitude', (Element,), {'name': 'longitude'})
lookout = type('lookout', (Element,), {'name': 'lookout'})
magfilter = type('magfilter', (Element,), {'name': 'magfilter'})
mass_frame = type('mass_frame', (Element,), {'name': 'mass_frame'})
rigid_body = type('rigid_body', (Element,), {'name': 'rigid_body'})
mass = type('mass', (Element,), {'name': 'mass'})
shape = type('shape', (Element,), {'name': 'shape'})
material_ambient = type('material_ambient', (Element,), {'name': 'material_ambient'})
material_diffuse = type('material_diffuse', (Element,), {'name': 'material_diffuse'})
material_emission = type('material_emission', (Element,), {'name': 'material_emission'})
material_shininess = type('material_shininess', (Element,), {'name': 'material_shininess'})
material_specular = type('material_specular', (Element,), {'name': 'material_specular'})
material = type('material', (Element,), {'name': 'material'})
matrix = type('matrix', (Element,), {'name': 'matrix'})
max_anisotropy = type('max_anisotropy', (Element,), {'name': 'max_anisotropy'})
mesh = type('mesh', (Element,), {'name': 'mesh'})
minfilter = type('minfilter', (Element,), {'name': 'minfilter'})
mip_bias = type('mip_bias', (Element,), {'name': 'mip_bias'})
mip_max_level = type('mip_max_level', (Element,), {'name': 'mip_max_level'})
mip_min_level = type('mip_min_level', (Element,), {'name': 'mip_min_level'})
mipfilter = type('mipfilter', (Element,), {'name': 'mipfilter'})
mips = type('mips', (Element,), {'name': 'mips'})
create_cube = type('create_cube', (Element,), {'name': 'create_cube'})
create2d = type('create2d', (Element,), {'name': 'create2d'})
create3d = type('create3d', (Element,), {'name': 'create3d'})
model_view_matrix = type('model_view_matrix', (Element,), {'name': 'model_view_matrix'})
modified = type('modified', (Element,), {'name': 'modified'})
modifier = type('modifier', (Element,), {'name': 'modifier'})
morph = type('morph', (Element,), {'name': 'morph'})
motion = type('motion', (Element,), {'name': 'motion'})
multisample_enable = type('multisample_enable', (Element,), {'name': 'multisample_enable'})
Name_array = type('Name_array', (Element,), {'name': 'Name_array'})
emantic = type('emantic', (Element,), {'name': 'emantic'})
newparam = type('newparam', (Element,), {'name': 'newparam'})
ommon = type('ommon', (Element,), {'name': 'ommon'})
node = type('node', (Element,), {'name': 'node'})
normalize_enable = type('normalize_enable', (Element,), {'name': 'normalize_enable'})
nurbs_surface = type('nurbs_surface', (Element,), {'name': 'nurbs_surface'})
nurbs = type('nurbs', (Element,), {'name': 'nurbs'})
optics = type('optics', (Element,), {'name': 'optics'})
orient = type('orient', (Element,), {'name': 'orient'})
origin = type('origin', (Element,), {'name': 'origin'})
orthographic = type('orthographic', (Element,), {'name': 'orthographic'})
p = type('p', (Element,), {'name': 'p'})
edges = type('edges', (Element,), {'name': 'edges'})
faces = type('faces', (Element,), {'name': 'faces'})
lines = type('lines', (Element,), {'name': 'lines'})
pcurves = type('pcurves', (Element,), {'name': 'pcurves'})
ph = type('ph', (Element,), {'name': 'ph'})
solids = type('solids', (Element,), {'name': 'solids'})
triangles = type('triangles', (Element,), {'name': 'triangles'})
trifans = type('trifans', (Element,), {'name': 'trifans'})
tristrips = type('tristrips', (Element,), {'name': 'tristrips'})
wires = type('wires', (Element,), {'name': 'wires'})
parabola = type('parabola', (Element,), {'name': 'parabola'})
param = type('param', (Element,), {'name': 'param'})
ph = type('ph', (Element,), {'name': 'ph'})
phong = type('phong', (Element,), {'name': 'phong'})
physics_material = type('physics_material', (Element,), {'name': 'physics_material'})
physics_model = type('physics_model', (Element,), {'name': 'physics_model'})
physics_scene = type('physics_scene', (Element,), {'name': 'physics_scene'})
plane = type('plane', (Element,), {'name': 'plane'})
point_distance_attenuation = type('point_distance_attenuation', (Element,), {'name': 'point_distance_attenuation'})
point_fade_threshold_size = type('point_fade_threshold_size', (Element,), {'name': 'point_fade_threshold_size'})
point_size_max = type('point_size_max', (Element,), {'name': 'point_size_max'})
point_size_min = type('point_size_min', (Element,), {'name': 'point_size_min'})
point_size = type('point_size', (Element,), {'name': 'point_size'})
point_smooth_enable = type('point_smooth_enable', (Element,), {'name': 'point_smooth_enable'})
polygon_mode = type('polygon_mode', (Element,), {'name': 'polygon_mode'})
polygon_offset_fill_enable = type('polygon_offset_fill_enable', (Element,), {'name': 'polygon_offset_fill_enable'})
polygon_offset_line_enable = type('polygon_offset_line_enable', (Element,), {'name': 'polygon_offset_line_enable'})
polygon_offset_point_enable = type('polygon_offset_point_enable', (Element,), {'name': 'polygon_offset_point_enable'})
polygon_offset = type('polygon_offset', (Element,), {'name': 'polygon_offset'})
polygon_smooth_enable = type('polygon_smooth_enable', (Element,), {'name': 'polygon_smooth_enable'})
polygon_stipple_enable = type('polygon_stipple_enable', (Element,), {'name': 'polygon_stipple_enable'})
polygons = type('polygons', (Element,), {'name': 'polygons'})
polylist = type('polylist', (Element,), {'name': 'polylist'})
prismatic = type('prismatic', (Element,), {'name': 'prismatic'})
profile_BRIDGE = type('profile_BRIDGE', (Element,), {'name': 'profile_BRIDGE'})
profile_CG = type('profile_CG', (Element,), {'name': 'profile_CG'})
profile_COMMON = type('profile_COMMON', (Element,), {'name': 'profile_COMMON'})
verview = type('verview', (Element,), {'name': 'verview'})
profile_GLES = type('profile_GLES', (Element,), {'name': 'profile_GLES'})
profile_GLES2 = type('profile_GLES2', (Element,), {'name': 'profile_GLES2'})
profile_GLSL = type('profile_GLSL', (Element,), {'name': 'profile_GLSL'})
program = type('program', (Element,), {'name': 'program'})
projection_matrix = type('projection_matrix', (Element,), {'name': 'projection_matrix'})
quadratic_attenuation = type('quadratic_attenuation', (Element,), {'name': 'quadratic_attenuation'})
point = type('point', (Element,), {'name': 'point'})
radius = type('radius', (Element,), {'name': 'radius'})
capsule = type('capsule', (Element,), {'name': 'capsule'})
circle = type('circle', (Element,), {'name': 'circle'})
cone = type('cone', (Element,), {'name': 'cone'})
cylinder = type('cylinder', (Element,), {'name': 'cylinder'})
ellipse = type('ellipse', (Element,), {'name': 'ellipse'})
hyperbola = type('hyperbola', (Element,), {'name': 'hyperbola'})
torus = type('torus', (Element,), {'name': 'torus'})
ref_attachment = type('ref_attachment', (Element,), {'name': 'ref_attachment'})
ref = type('ref', (Element,), {'name': 'ref'})
binary = type('binary', (Element,), {'name': 'binary'})
init_from = type('init_from', (Element,), {'name': 'init_from'})
reflective = type('reflective', (Element,), {'name': 'reflective'})
reflectivity = type('reflectivity', (Element,), {'name': 'reflectivity'})
render = type('render', (Element,), {'name': 'render'})
renderable = type('renderable', (Element,), {'name': 'renderable'})
rescale_normal_enable = type('rescale_normal_enable', (Element,), {'name': 'rescale_normal_enable'})
restitution = type('restitution', (Element,), {'name': 'restitution'})
revision = type('revision', (Element,), {'name': 'revision'})
revolute = type('revolute', (Element,), {'name': 'revolute'})
RGB = type('RGB', (Element,), {'name': 'RGB'})
rigid_constraint = type('rigid_constraint', (Element,), {'name': 'rigid_constraint'})
rotate = type('rotate', (Element,), {'name': 'rotate'})
sample_alpha_to_coverage_enable = type('sample_alpha_to_coverage_enable', (Element,), {'name': 'sample_alpha_to_coverage_enable'})
sample_alpha_to_one_enable = type('sample_alpha_to_one_enable', (Element,), {'name': 'sample_alpha_to_one_enable'})
sample_coverage_enable = type('sample_coverage_enable', (Element,), {'name': 'sample_coverage_enable'})
sample_coverage = type('sample_coverage', (Element,), {'name': 'sample_coverage'})
sampler_image = type('sampler_image', (Element,), {'name': 'sampler_image'})
sampler_states = type('sampler_states', (Element,), {'name': 'sampler_states'})
sampler = type('sampler', (Element,), {'name': 'sampler'})
nterpolation = type('nterpolation', (Element,), {'name': 'nterpolation'})
sampler1D = type('sampler1D', (Element,), {'name': 'sampler1D'})
sampler2D = type('sampler2D', (Element,), {'name': 'sampler2D'})
sampler3D = type('sampler3D', (Element,), {'name': 'sampler3D'})
samplerCUBE = type('samplerCUBE', (Element,), {'name': 'samplerCUBE'})
samplerDEPTH = type('samplerDEPTH', (Element,), {'name': 'samplerDEPTH'})
samplerRECT = type('samplerRECT', (Element,), {'name': 'samplerRECT'})
scale = type('scale', (Element,), {'name': 'scale'})
scene = type('scene', (Element,), {'name': 'scene'})
scissor_test_enable = type('scissor_test_enable', (Element,), {'name': 'scissor_test_enable'})
scissor = type('scissor', (Element,), {'name': 'scissor'})
semantic = type('semantic', (Element,), {'name': 'semantic'})
setparam = type('setparam', (Element,), {'name': 'setparam'})
shade_model = type('shade_model', (Element,), {'name': 'shade_model'})
shader = type('shader', (Element,), {'name': 'shader'})
shape = type('shape', (Element,), {'name': 'shape'})
shells = type('shells', (Element,), {'name': 'shells'})
shininess = type('shininess', (Element,), {'name': 'shininess'})
SIDREF_array = type('SIDREF_array', (Element,), {'name': 'SIDREF_array'})
size_exact = type('size_exact', (Element,), {'name': 'size_exact'})
size_ratio = type('size_ratio', (Element,), {'name': 'size_ratio'})
size = type('size', (Element,), {'name': 'size'})
create_cube = type('create_cube', (Element,), {'name': 'create_cube'})
create3d = type('create3d', (Element,), {'name': 'create3d'})
skeleton = type('skeleton', (Element,), {'name': 'skeleton'})
skew = type('skew', (Element,), {'name': 'skew'})
skin = type('skin', (Element,), {'name': 'skin'})
source_data = type('source_data', (Element,), {'name': 'source_data'})
source = type('source', (Element,), {'name': 'source'})
sources = type('sources', (Element,), {'name': 'sources'})
specular = type('specular', (Element,), {'name': 'specular'})
speed = type('speed', (Element,), {'name': 'speed'})
sphere = type('sphere', (Element,), {'name': 'sphere'})
spline = type('spline', (Element,), {'name': 'spline'})
nterpolation = type('nterpolation', (Element,), {'name': 'nterpolation'})
spot = type('spot', (Element,), {'name': 'spot'})
spring = type('spring', (Element,), {'name': 'spring'})
states = type('states', (Element,), {'name': 'states'})
static_friction = type('static_friction', (Element,), {'name': 'static_friction'})
stencil_clear = type('stencil_clear', (Element,), {'name': 'stencil_clear'})
stencil_func_separate = type('stencil_func_separate', (Element,), {'name': 'stencil_func_separate'})
stencil_func = type('stencil_func', (Element,), {'name': 'stencil_func'})
stencil_mask_separate = type('stencil_mask_separate', (Element,), {'name': 'stencil_mask_separate'})
stencil_mask = type('stencil_mask', (Element,), {'name': 'stencil_mask'})
stencil_op_separate = type('stencil_op_separate', (Element,), {'name': 'stencil_op_separate'})
stencil_op = type('stencil_op', (Element,), {'name': 'stencil_op'})
stencil_target = type('stencil_target', (Element,), {'name': 'stencil_target'})
stencil_test_enable = type('stencil_test_enable', (Element,), {'name': 'stencil_test_enable'})
stiffness = type('stiffness', (Element,), {'name': 'stiffness'})
subject = type('subject', (Element,), {'name': 'subject'})
surface_curves = type('surface_curves', (Element,), {'name': 'surface_curves'})
surface = type('surface', (Element,), {'name': 'surface'})
surfaces = type('surfaces', (Element,), {'name': 'surfaces'})
swept_surface = type('swept_surface', (Element,), {'name': 'swept_surface'})
swing_cone_and_twist = type('swing_cone_and_twist', (Element,), {'name': 'swing_cone_and_twist'})
target_value = type('target_value', (Element,), {'name': 'target_value'})
target = type('target', (Element,), {'name': 'target'})
targets = type('targets', (Element,), {'name': 'targets'})
bind_material = type('bind_material', (Element,), {'name': 'bind_material'})
formula = type('formula', (Element,), {'name': 'formula'})
instance_rigid_body = type('instance_rigid_body', (Element,), {'name': 'instance_rigid_body'})
kinematics_model = type('kinematics_model', (Element,), {'name': 'kinematics_model'})
kinematics = type('kinematics', (Element,), {'name': 'kinematics'})
light = type('light', (Element,), {'name': 'light'})
motion = type('motion', (Element,), {'name': 'motion'})
optics = type('optics', (Element,), {'name': 'optics'})
rigid_body = type('rigid_body', (Element,), {'name': 'rigid_body'})
verview = type('verview', (Element,), {'name': 'verview'})
technique_hint = type('technique_hint', (Element,), {'name': 'technique_hint'})
technique_override = type('technique_override', (Element,), {'name': 'technique_override'})
texcombiner = type('texcombiner', (Element,), {'name': 'texcombiner'})
texcoord = type('texcoord', (Element,), {'name': 'texcoord'})
texenv = type('texenv', (Element,), {'name': 'texenv'})
texture_env_color = type('texture_env_color', (Element,), {'name': 'texture_env_color'})
texture_env_mode = type('texture_env_mode', (Element,), {'name': 'texture_env_mode'})
texture_pipeline = type('texture_pipeline', (Element,), {'name': 'texture_pipeline'})
texture = type('texture', (Element,), {'name': 'texture'})
texture1D_enable = type('texture1D_enable', (Element,), {'name': 'texture1D_enable'})
texture1D = type('texture1D', (Element,), {'name': 'texture1D'})
texture2D_enable = type('texture2D_enable', (Element,), {'name': 'texture2D_enable'})
texture2D = type('texture2D', (Element,), {'name': 'texture2D'})
texture3D_enable = type('texture3D_enable', (Element,), {'name': 'texture3D_enable'})
texture3D = type('texture3D', (Element,), {'name': 'texture3D'})
textureCUBE_enable = type('textureCUBE_enable', (Element,), {'name': 'textureCUBE_enable'})
textureCUBE = type('textureCUBE', (Element,), {'name': 'textureCUBE'})
textureDEPTH_enable = type('textureDEPTH_enable', (Element,), {'name': 'textureDEPTH_enable'})
textureDEPTH = type('textureDEPTH', (Element,), {'name': 'textureDEPTH'})
textureRECT_enable = type('textureRECT_enable', (Element,), {'name': 'textureRECT_enable'})
textureRECT = type('textureRECT', (Element,), {'name': 'textureRECT'})
time_step = type('time_step', (Element,), {'name': 'time_step'})
title = type('title', (Element,), {'name': 'title'})
translate = type('translate', (Element,), {'name': 'translate'})
transparency = type('transparency', (Element,), {'name': 'transparency'})
transparent = type('transparent', (Element,), {'name': 'transparent'})
unit = type('unit', (Element,), {'name': 'unit'})
unnormalized = type('unnormalized', (Element,), {'name': 'unnormalized'})
usertype = type('usertype', (Element,), {'name': 'usertype'})
v = type('v', (Element,), {'name': 'v'})
value = type('value', (Element,), {'name': 'value'})
velocity = type('velocity', (Element,), {'name': 'velocity'})
vertex_weights = type('vertex_weights', (Element,), {'name': 'vertex_weights'})
wrap_p = type('wrap_p', (Element,), {'name': 'wrap_p'})
wrap_s = type('wrap_s', (Element,), {'name': 'wrap_s'})
wrap_t = type('wrap_t', (Element,), {'name': 'wrap_t'})
xfov = type('xfov', (Element,), {'name': 'xfov'})
xmag = type('xmag', (Element,), {'name': 'xmag'})
yfov = type('yfov', (Element,), {'name': 'yfov'})
ymag = type('ymag', (Element,), {'name': 'ymag'})
zfar = type('zfar', (Element,), {'name': 'zfar'})
znear = type('znear', (Element,), {'name': 'znear'})

# builtins require an underscore.
_input = type('input', (closed_tag,), {'name': 'input'})
_float = type('float', (Element,), {'name': 'float'})
_pass = type('pass', (Element,), {'name': 'pass'})
_max = type('max', (Element,), {'name': 'max'})
_min = type('min', (Element,), {'name': 'min'})
_import = type('import', (Element,), {'name': 'import'})
_hex = type('hex', (Element,), {'name': 'hex'})
_format = type('format', (Element,), {'name': 'format'})


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
