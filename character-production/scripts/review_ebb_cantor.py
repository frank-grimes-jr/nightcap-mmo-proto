"""Photograph the Ebb Cantor on the inherited neutral studio set."""
from pathlib import Path
import sys,bpy
from mathutils import Vector
O=Path(__file__).resolve().parents[1]/'output/dark-elf-female/ebb-cantor';R=O/'Review'
bpy.ops.wm.open_mainfile(filepath=str(O/'DarkElfFemale.blend'))
sc=bpy.context.scene;cam=sc.camera
def shot(name,direction,target,scale,w,h,samples=10):
    cam.location=Vector(target)+Vector(direction).normalized()*5
    cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale
    sc.render.resolution_x=w;sc.render.resolution_y=h;sc.render.resolution_percentage=100
    sc.cycles.samples=samples;sc.render.image_settings.color_mode='RGBA';sc.render.filepath=str(R/(name+'.png'))
    bpy.ops.render.render(write_still=True)
center=(0,-.03,.86);three=(-.58,-1.8,.14)
shot('Three-quarter',three,center,1.87,800,1024)
shot('Front',(0,-1,.012),center,1.87,720,940)
shot('Vessels',(-.95,-1.5,.46),(-.148,-.087,.993),.46,760,730)
if '--proof' in sys.argv:sys.exit(0)
shot('Rear',(.38,1.55,.13),center,1.86,710,930)
shot('Profile',(-1,0,.025),center,1.88,650,870)
shot('Pall',(.55,-1.7,.18),(.025,-.03,1.31),.78,720,730)
shot('Hem',(-.16,-1.45,.05),(0,-.08,.298),.72,830,640)
shot('Head',(-.43,-1.65,.12),(0,-.05,1.56),.38,520,570)
shot('Gameplay',three,center,1.75,105,130,16)
clay=bpy.data.materials.new('Warm clay inspection');clay.diffuse_color=(.39,.34,.30,1)
sc.view_layers[0].material_override=clay;shot('Clay',three,center,1.87,540,700);sc.view_layers[0].material_override=None
suit=bpy.data.collections['05  Ebb Cantor robes'];suit.hide_render=True
for n in ('Skin | Covered limbs and torso','Underlayer | Fitted linen shift'):sc.objects[n].hide_render=False
shot('Restored',three,center,1.87,540,700)
for n in ('Skin | Covered limbs and torso','Underlayer | Fitted linen shift'):sc.objects[n].hide_render=True
suit.hide_render=False
for m in {slot.material for o in sc.objects if o.type=='MESH' for slot in o.material_slots if slot.material}:
    nt=m.node_tree;bs=nt.nodes.get('Principled BSDF');out=nt.nodes.get('Material Output')
    c=bs.inputs['Base Color'];em=nt.nodes.new('ShaderNodeEmission')
    if c.is_linked:nt.links.new(c.links[0].from_socket,em.inputs[0])
    else:em.inputs[0].default_value=c.default_value
    nt.links.new(em.outputs[0],out.inputs[0])
sc.view_settings.view_transform='Standard';sc.view_settings.look='None'
shot('Unlit',three,center,1.87,540,700)
