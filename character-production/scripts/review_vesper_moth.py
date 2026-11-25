"""Render the saved Vesper Moth asset under neutral light, including real unlit and clay passes."""
import bpy
from mathutils import Vector
from pathlib import Path
import sys
O=Path(__file__).resolve().parents[1]/'output/dark-elf-female/vesper-moth'
bpy.ops.wm.open_mainfile(filepath=str(O/'DarkElfFemale.blend'))
s=bpy.context.scene;c=s.camera
def frame(name,direction,center,scale,w,h,samples=12):
    c.location=Vector(center)+Vector(direction).normalized()*5
    c.rotation_euler=(Vector(center)-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=scale
    s.render.resolution_x=w;s.render.resolution_y=h;s.render.resolution_percentage=100
    s.cycles.samples=samples;s.render.image_settings.color_mode='RGBA';s.render.filepath=str(O/'Review'/(name+'.png'))
    bpy.ops.render.render(write_still=True)
center=(0,-.04,.86);three=(.50,-1.8,.13)
if '--restore' in sys.argv:
    bpy.data.collections['05  Vesper Moth regalia'].hide_render=True
    for obj in s.objects:
        if obj.name.startswith('Lining |'):obj.hide_render=True
        if obj.name in ('Skin | Covered limbs and torso','Underlayer | Fitted linen shift'):obj.hide_render=False
    frame('Restored',three,center,1.88,550,720)
    sys.exit(0)
frame('Three-quarter',three,center,1.86,790,1024)
frame('Reliquary',(.35,-1.65,.24),(0,-.025,1.40),.83,930,730)
frame('Front',(0,-1,.018),center,1.88,720,940)
frame('Rear',(-.22,1.6,.15),center,1.88,720,940)
frame('Profile',(1,-.045,.04),center,1.88,630,900)
frame('Orphrey',(.19,-1.4,.13),(.01,-.14,.64),1.09,550,800)
frame('Gameplay',three,center,1.75,108,130)
frame('Head',(-.45,-1.65,.14),(0,-.05,1.565),.40,560,600)
key=bpy.data.objects['Key | Parchment'];fill=bpy.data.objects['Fill | Overcast'];rim=bpy.data.objects['Rim | Window']
levels=[(l.data.energy,l.data.color[:]) for l in (key,fill,rim)]
key.data.energy=265;key.data.color=(1,.79,.67)
fill.data.energy=78;fill.data.color=(.53,.72,1)
rim.data.energy=370;rim.data.color=(.78,.87,1)
frame('Portrait-light',(-.52,-1.82,.13),center,1.86,820,1080,18)
for light,(energy,color) in zip((key,fill,rim),levels):light.data.energy=energy;light.data.color=color
clay=bpy.data.materials.new('Review clay');clay.diffuse_color=(.36,.31,.29,1)
s.view_layers[0].material_override=clay
frame('Clay',three,center,1.88,590,770)
s.view_layers[0].material_override=None
for m in {slot.material for o in s.objects if o.type=='MESH' for slot in o.material_slots if slot.material}:
    nt=m.node_tree;bs=nt.nodes.get('Principled BSDF');out=nt.nodes.get('Material Output')
    em=nt.nodes.new('ShaderNodeEmission');channel=bs.inputs['Base Color']
    if channel.is_linked:nt.links.new(channel.links[0].from_socket,em.inputs[0])
    else:em.inputs[0].default_value=channel.default_value
    nt.links.new(em.outputs[0],out.inputs[0])
s.view_settings.view_transform='Standard';s.view_settings.look='None'
frame('Unlit',three,center,1.88,590,770)
