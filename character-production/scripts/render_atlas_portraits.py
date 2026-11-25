"""Render the archived Dark Elf meshes over the corresponding Atlas ground paintings.

blender -b -P render_atlas_portraits.py -- <Pages checkout> <output directory> [samples]
"""
from pathlib import Path
import math
import sys
import bpy
from mathutils import Matrix, Vector
from bpy_extras.object_utils import world_to_camera_view

pages, output, *options = sys.argv[sys.argv.index("--") + 1:]
plates = Path(pages).resolve() / "assets/concept-art/the-sill"
out = Path(output).resolve()
out.mkdir(parents=True, exist_ok=True)
production = Path(__file__).resolve().parents[1]
samples = int(options[0]) if options else 32


def aim_limb(rig, name, child, direction):
    joint = rig.pose.bones[name]
    axis = rig.pose.bones[child].head - joint.head
    rotation = axis.rotation_difference(Vector(direction).normalized()).to_matrix().to_4x4()
    pivot = Matrix.Translation(joint.head)
    joint.matrix = pivot @ rotation @ pivot.inverted() @ joint.matrix
    bpy.context.view_layer.update()


def area(name, pos, power, size, color):
    data = bpy.data.lights.new(name, "AREA")
    data.energy, data.shape, data.size, data.color = power, "DISK", size, color
    obj = bpy.data.objects.new(name, data)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = pos
    obj.rotation_euler = (Vector((0, 0, 1)) - obj.location).to_track_quat("-Z", "Y").to_euler()


def place_camera(scene, direction, height, screen_height, foot_x, foot_y):
    camera = scene.camera
    camera.data.type = "PERSP"
    camera.data.sensor_fit = "HORIZONTAL"
    camera.data.shift_x = camera.data.shift_y = 0
    aspect = scene.render.resolution_x / scene.render.resolution_y
    target = Vector((0, 0, height / 2))
    camera.location = target + Vector(direction).normalized() * 6
    camera.rotation_euler = (target - camera.location).to_track_quat("-Z", "Y").to_euler()
    camera.data.lens = 6 * camera.data.sensor_width * screen_height / (height * aspect)
    bpy.context.view_layer.update()
    foot = world_to_camera_view(scene, camera, Vector((0, 0, 0)))
    camera.data.shift_x = foot.x - foot_x
    camera.data.shift_y = (foot.y - (1 - foot_y)) / aspect


def render(cantor):
    stem = "knellwater-funeral-road" if cantor else "ventfold-heatworks"
    source = ("dark-elf-female/ebb-cantor/DarkElfFemale.blend" if cantor else
              "dark-elf-male/furnace-warden/DarkElfMale.blend")
    bpy.ops.wm.open_mainfile(filepath=str(production / "output" / source))
    scene = bpy.context.scene
    for light in [o for o in scene.objects if o.type == "LIGHT"]:
        light.hide_render = True
    rig, = [o for o in scene.objects if o.type == "ARMATURE"]
    rig.data.pose_position = "POSE"
    for bone in rig.pose.bones:
        bone.matrix_basis = Matrix.Identity(4)
    bpy.context.view_layer.update()
    for side, sign in [("l", 1), ("r", -1)]:
        aim_limb(rig, "upperarm_"+side, "lowerarm_"+side,
                 (sign*(.24 if cantor else .40), .035, -1))
        extension = -.57 if cantor and side == "r" else -.25
        aim_limb(rig, "lowerarm_"+side, "hand_"+side, (sign*.06, extension, -1))
    if cantor:
        # Look down the funeral road from the edge of the foreground stone stair.
        head = rig.pose.bones["head"]
        pivot = Matrix.Translation(head.head)
        head.matrix = pivot @ Matrix.Rotation(math.radians(4),4,"Z") @ pivot.inverted() @ head.matrix
    else:
        head = rig.pose.bones["head"]
        pivot = Matrix.Translation(head.head)
        head.matrix = pivot @ Matrix.Rotation(math.radians(9),4,"X") @ pivot.inverted() @ head.matrix
    bg = bpy.data.images.load(str(plates / ("l4-knellwater.webp" if cantor else "l4-flue.webp")))
    scene.render.resolution_x, scene.render.resolution_y = bg.size[:]
    scene.render.resolution_percentage = 100
    if cantor:
        place_camera(scene, (-.85,-1,.095), 1.714, .78, .231, .962)
        area("Cloud light over the polder", (-3.5,-3.5,6), 335, 5.2, (.77,.81,1))
        area("Ebb light from the horizon", (3,2,3), 205, 4, (1,.70,.53))
        ambient = (.45,.47,.55,.32)
        bpy.ops.mesh.primitive_plane_add(size=3.4,location=(0,0,-.002))
        bpy.context.object.is_shadow_catcher = True
    else:
        place_camera(scene, (.72,-1,.055), 1.857, 1.19, .835, 1.285)
        area("Sun above the flues", (-3,-1.8,5.5), 650, 1.6, (1,.84,.65))
        area("Cool light off the terrace", (1.8,-4,3.7), 255, 4, (.75,.83,1))
        area("Fired clay bounce", (2.2,.5,1.5), 68, 3, (1,.59,.34))
        ambient = (.50,.54,.62,.32)
    sky = scene.world.node_tree.nodes.get("Background")
    sky.inputs["Color"].default_value = (*ambient[:3],1)
    sky.inputs["Strength"].default_value = ambient[3]
    scene.render.engine = "CYCLES"
    scene.cycles.samples = samples
    scene.cycles.use_denoising = True
    scene.render.film_transparent = True
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "None"
    scene.view_settings.exposure = 0
    scene.view_settings.gamma = 1
    tree = bpy.data.node_groups.new("Atlas ground plate and posed character","CompositorNodeTree")
    scene.compositing_node_group = tree
    tree.interface.new_socket(name="Image",in_out="OUTPUT",socket_type="NodeSocketColor")
    result = tree.nodes.new("NodeGroupOutput")
    over = tree.nodes.new("CompositorNodeAlphaOver")
    layers = tree.nodes.new("CompositorNodeRLayers")
    ground = tree.nodes.new("CompositorNodeImage")
    ground.image = bg
    color_inputs = [sock for sock in over.inputs if sock.type=="RGBA"]
    tree.links.new(ground.outputs["Image"],color_inputs[0])
    tree.links.new(layers.outputs["Image"],color_inputs[1])
    tree.links.new(over.outputs[0],result.inputs["Image"])
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    scene.render.filepath = str(out / (stem+".png"))
    bpy.ops.render.render(write_still=True)


for character in (True, False):
    render(character)
