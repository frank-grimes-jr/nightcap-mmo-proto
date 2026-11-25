"""Reopen the native source, import the FBX in an empty scene and render its bind surfaces."""
from pathlib import Path
import bpy, numpy as np, json, math, sys
from mathutils import Vector
from mathutils.kdtree import KDTree
P=Path(__file__).resolve().parents[1];OUT=P/'output/dark-elf-male/furnace-warden';R=OUT/'Review'
native=json.loads((R/'Native-bind.json').read_text())
bpy.ops.wm.open_mainfile(filepath=str(OUT/'DarkElfMale.blend'))
def points(o):return np.array([list(o.matrix_world@v.co) for v in o.data.vertices])
def corners(o):
    if not o.data.uv_layers:return set()
    pts=points(o);ids=[l.vertex_index for l in o.data.loops]
    uv=np.array([list(c.uv) for c in o.data.uv_layers[0].data])
    return {tuple(row) for row in np.round(np.column_stack([pts[ids],uv]),5)}
original={n:(points(bpy.data.objects[n]),corners(bpy.data.objects[n])) for n in native['meshes']}
def weight_rows(obj):
    names=[g.name for g in obj.vertex_groups]
    return [{names[g.group]:g.weight for g in v.groups if g.weight>0} for v in obj.data.vertices]
original_weights={n:weight_rows(bpy.data.objects[n]) for n in native['meshes']}
packed={im.name:bool(im.packed_file) for im in bpy.data.images if im.source=='FILE' and im.users}
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=str(OUT/'DarkElfMale.fbx'),use_anim=False,ignore_leaf_bones=False)
sc=bpy.context.scene
rigs=[o for o in sc.objects if o.type=='ARMATURE'];assert len(rigs)==1
rig=rigs[0]
objs={o.name:o for o in sc.objects if o.type=='MESH'}
assert objs.keys()==native['meshes'].keys(),objs.keys()^native['meshes'].keys()
result={}; max_bounds_error=0
for name,o in objs.items():
    want=native['meshes'][name];p=points(o);p0,uv0=original[name]
    o.data.calc_loop_triangles()
    extent_error=float(max(abs(p.min(0)-p0.min(0)).max(),abs(p.max(0)-p0.max(0)).max()))
    max_bounds_error=max(max_bounds_error,extent_error)
    uv=corners(o)
    # FBX perimeter vertices sometimes round across the last decimal. Check
    # each remaining UV/position against nearby native samples without flipping V.
    missing=uv-uv0
    nearest=0
    if missing and uv0:
        a=np.array(list(uv0))
        for row in missing:
            nearest=max(nearest,float(np.abs(a-np.array(row)).max(axis=1).min()))
    groups={g.name for g in o.vertex_groups}
    weights=[[g.weight for g in v.groups if g.weight>0] for v in o.data.vertices]
    kd=KDTree(len(p0))
    for i,xyz in enumerate(p0):kd.insert(xyz,i)
    kd.balance()
    wr=original_weights[name];weight_delta=0
    for xyz,got in zip(p,weight_rows(o)):
        near=kd.find_range(xyz,2e-5)
        if not near:weight_delta=1;break
        delta=min(max(abs(got.get(g,0)-wr[i].get(g,0)) for g in got.keys()|wr[i].keys()) for _,i,_ in near)
        weight_delta=max(weight_delta,delta)
    err=max(abs(1-sum(w)) for w in weights)
    row={'triangles':len(o.data.loop_triangles),'vertices':len(p),'world_bounds_error_m':extent_error,'uv_position_max_error':nearest,'materials':[m.name for m in o.data.materials],'missing_used_groups':[n for n in want['groups'] if n not in groups and not n.startswith('Nightcap')],'weight_sum_max_error':err,'max_influences':max(map(len,weights)),'unweighted':sum(not w for w in weights)}
    row['passes_surface']=row['triangles']==want['triangles'] and extent_error<.00002 and nearest<.00003 and row['materials']==want['materials'] and not row['unweighted'] and not row['missing_used_groups'] and row['max_influences']<=4 and err<1e-5
    result[name]=row
    row['max_native_to_fbx_weight_error']=weight_delta
    row['passes_surface'] &= weight_delta<1e-5
hierarchy={b.name:(b.parent.name if b.parent else None) for b in rig.data.bones}
heads=[]
rest_frames=[]
for b in rig.data.bones:
    if b.name in native['bones']:
        local=native['bones'][b.name]['rest']
        heads.append((rig.matrix_world@b.head_local-Vector([row[3] for row in local[:3]])).length)
        actual=np.array(rig.matrix_world@b.matrix_local)[:3,:3]
        actual=actual/np.linalg.norm(actual,axis=0)
        wanted=np.array(local)[:3,:3]
        rest_frames.append(float(np.max(abs(actual-wanted))))
loaded_images={i.name:bool(i.has_data or Path(bpy.path.abspath(i.filepath)).is_file()) for i in bpy.data.images if i.source=='FILE'}
audit={'blender':bpy.app.version_string,'source_reopened':True,'native_images_packed':packed,'imported_image_paths_resolve':loaded_images,'armatures':len(rigs),'bones':len(hierarchy),'hierarchy_match':hierarchy=={n:b['parent'] for n,b in native['bones'].items()},'worst_joint_head_error_m':max(heads),'max_bounds_error_m':max_bounds_error,'actions':len(bpy.data.actions),'meshes':result}
audit['passed']=all(row['passes_surface'] for row in result.values()) and audit['hierarchy_match'] and max(heads)<2e-5 and all(packed.values()) and all(loaded_images.values()) and audit['actions']==0
audit['max_rest_axis_component_delta']=max(rest_frames)
(R/'FBX-roundtrip.json').write_text(json.dumps(audit,indent=2))
print('ROUNDTRIP',audit['passed'],[k for k,row in result.items() if not row['passes_surface']],audit['hierarchy_match'],max(heads),flush=True)
if '--audit-only' in sys.argv:
    if not audit['passed']:raise RuntimeError('FBX comparison failed')
    sys.exit(0)
# FBX has no node graph for mask gain. Relink the packed native paint shaders for review.
names={n for row in native['meshes'].values() for n in row['materials']}
for m in list(bpy.data.materials):m.name='Imported '+m.name
with bpy.data.libraries.load(str(OUT/'DarkElfMale.blend'),link=False) as (src,dst):
    dst.materials=list(names)
    dst.objects=[n for n in src.objects if n in ('Review camera','Pale forge window','Copper bounce','Edge light')]
    dst.worlds=['Portrait studio']
for o in dst.objects:sc.collection.objects.link(o)
sc.world=dst.worlds[0];sc.camera=bpy.data.objects['Review camera']
for name,o in objs.items():
    o.data.materials.clear()
    for m in native['meshes'][name]['materials']:o.data.materials.append(bpy.data.materials[m])
sc.render.engine='CYCLES';sc.cycles.samples=12;sc.cycles.use_denoising=True
sc.render.film_transparent=True;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA'
sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast'
cam=sc.camera
def render(name,direction,focus,scale,w,h):
    cam.location=Vector(focus)+Vector(direction).normalized()*6
    cam.rotation_euler=(Vector(focus)-cam.location).to_track_quat('-Z','Y').to_euler()
    cam.data.type='ORTHO';cam.data.ortho_scale=scale
    sc.render.resolution_x=w;sc.render.resolution_y=h;sc.render.resolution_percentage=100
    sc.render.filepath=str(R/(name+'.png'))
    bpy.ops.render.render(write_still=True)
def outfit(mode):
    for n,o in objs.items():
        group=native['meshes'][n]['category']
        if n=='DarkElf_SweptIvory':show=mode!='helm'
        elif n=='DarkElf_CoveredBody':show=mode=='body'
        elif group=='Helm':show=mode=='helm'
        elif n.startswith('Warden_'):show=group=='Underlayer' or mode!='body'
        else:show=True
        o.hide_render=not show
outfit('helm')
for name,d in [('Three-quarter',(.52,-1.8,.25)),('Front',(0,-1,.018)),('Side',(1,0,.02)),('Rear',(.08,1,.07))]:
    render(name,d,(0,-.045,.93),2.08,720,900)
render('Helmet-detail',(.43,-1.8,.20),(0,-.060,1.62),.62,850,780)
plate=bpy.data.materials['Furnace Warden • banked iron']
gain=next(n for n in plate.node_tree.nodes if n.label=='Banked heat intensity')
level=gain.inputs[1].default_value;gain.inputs[1].default_value=0
render('Helmet-heat-off',(.43,-1.8,.20),(0,-.060,1.62),.62,710,650)
gain.inputs[1].default_value=level
outfit('bare')
render('Uncovered-head',(.49,-1.65,.16),(0,-.054,1.68),.41,760,800)
render('Head-profile',(1,-.08,.045),(0,-.025,1.69),.40,720,750)
render('Head-underside',(.14,-1,-.46),(0,-.055,1.68),.39,660,680)
outfit('body')
render('Body-blockout',(.28,-1.8,.10),(0,-.05,.92),2.04,700,860)
render('Body-profile',(1,0,.02),(0,-.05,.92),2.04,610,820)
outfit('helm')
clay=bpy.data.materials.new('Warm sculpt clay');clay.diffuse_color=(.37,.31,.28,1)
sc.view_layers[0].material_override=clay
render('Clay',(.55,-1.6,.24),(0,-.04,.93),2.08,670,850)
sc.view_layers[0].material_override=None
key=bpy.data.objects['Pale forge window'];key.location.x*=-1;key.rotation_euler=(Vector((0,0,1.1))-key.location).to_track_quat('-Z','Y').to_euler()
render('Reversed-key',(-.48,-1.6,.21),(0,-.06,1.56),.74,680,760)
for m in dst.materials:
    nt=m.node_tree;bs=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED');out=next(n for n in nt.nodes if n.type=='OUTPUT_MATERIAL')
    emit=nt.nodes.new('ShaderNodeEmission');c=bs.inputs['Base Color']
    if c.is_linked:nt.links.new(c.links[0].from_socket,emit.inputs[0])
    else:emit.inputs[0].default_value=c.default_value
    nt.links.new(emit.outputs[0],out.inputs[0])
sc.view_settings.view_transform='Standard';sc.view_settings.look='None'
render('Unlit-color',(.34,-1.65,.15),(0,-.035,.93),2.08,670,850)
print('REVIEW COMPLETE')

