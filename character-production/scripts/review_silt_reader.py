"""Review the saved female sculpt and compare its FBX skin in an empty scene."""
import bpy,json,sys,math,hashlib
from collections import defaultdict
from pathlib import Path
from mathutils import Vector
from mathutils.kdtree import KDTree
import numpy as np

P=Path(__file__).resolve().parents[1]
outfit=sys.argv[sys.argv.index('--outfit')+1] if '--outfit' in sys.argv else 'silt-reader'
O=P/'output/dark-elf-female'/outfit;R=O/'Review'
bpy.ops.wm.open_mainfile(filepath=str(O/'DarkElfFemale.blend'))
sc=bpy.context.scene; native=json.loads((R/'Native-bind.json').read_text())
def point(o,v):return o.matrix_world@v.co
def stats(o):
    me=o.data;me.calc_loop_triangles()
    pts=[point(o,v) for v in me.vertices]
    w=[{o.vertex_groups[g.group].name:g.weight for g in v.groups if g.weight>0} for v in me.vertices]
    return pts,w,[(pts[l.vertex_index],tuple(me.uv_layers[0].data[l.index].uv)) for l in me.loops],len(me.loop_triangles),[m.name for m in me.materials]
def index(values):
    kd=KDTree(len(values))
    for i,v in enumerate(values):kd.insert(v,i)
    kd.balance();return kd
def audit():
    objs={n:stats(bpy.data.objects[n]) for n in native['meshes']}
    assert all(o.packed_file for o in bpy.data.images if o.source=='FILE' and o.users)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=str(O/'DarkElfFemale.fbx'),use_anim=False)
    rigs=[o for o in bpy.context.scene.objects if o.type=='ARMATURE'];assert len(rigs)==1
    rig=rigs[0];objects={o.name:o for o in bpy.context.scene.objects if o.type=='MESH'}
    assert objects.keys()==objs.keys(),objects.keys()^objs.keys()
    rows={};err_head=0;err_axis=0
    assert len(rig.data.bones)==len(native['bones'])==53
    for b in rig.data.bones:
        src=native['bones'][b.name]
        assert (b.parent.name if b.parent else None)==src['parent']
        a=np.array(rig.matrix_world@b.matrix_local);want=np.array(src['rest'])
        err_head=max(err_head,float(np.linalg.norm(a[:3,3]-want[:3,3])))
        err_axis=max(err_axis,float(abs(a[:3,:3]/np.linalg.norm(a[:3,:3],axis=0)-want[:3,:3]).max()))
    for n,o in objects.items():
        pts,w,uv,tris,materials=stats(o);source,sw,suv,st,sm=objs[n]
        kd=index(source);corner=index([p for p,uv in suv]);du=dw=dp=0
        for q,ws in zip(pts,w):
            _,_,d=kd.find(q);dp=max(dp,d)
            matches=kd.find_range(q,2e-5)
            dw=max(dw,min(max(abs(ws.get(k,0)-sw[i].get(k,0)) for k in ws.keys()|sw[i].keys()) for _,i,_ in matches))
        for q,coord in uv:
            matches=corner.find_range(q,2e-5)
            du=max(du,min(max(abs(a-b) for a,b in zip(coord,suv[i][1])) for _,i,_ in matches))
        invalid_side=0
        if 'sleeve ' in n or 'cuff ' in n or 'Cuff woven' in n:
            side=n.split()[-1][0]
            invalid_side=sum(any(not (g in {'upperarm_'+side,'lowerarm_'+side}) for g in row) for row in w)
        if n.startswith('Robe |') and any('thigh_' in g for row in w for g in row):
            invalid_side+=sum(any(g.startswith('thigh_') and (g.endswith('_l')!=(p.x>0)) and abs(p.x)>.0001 for g in row) for p,row in zip(pts,w))
        rows[n]=dict(triangles=tris,material_slots=materials,position_error_m=dp,weight_error=dw,uv_error=du,
                      joint_influences=max(map(len,w)),weight_sum_error=max(abs(1-sum(x.values())) for x in w),
                      missing_weights=sum(not x for x in w),wrong_side_weights=invalid_side,
                      geometry_and_slots_match=tris==st and materials==sm,armature_bind=o.find_armature()==rig)
    images={i.name:Path(bpy.path.abspath(i.filepath)).is_file() for i in bpy.data.images if i.source=='FILE' and i.users}
    covered='Skin | Covered limbs and torso'
    bodypts=[p.z for n in ('Skin | Head neck and hands',covered) for p in stats(objects[n])[0]]
    visible=[p.z for n,o in objects.items() if n!=covered for p in stats(o)[0]]
    result={'source_reopened':True,'empty_scene_import':True,'blender':bpy.app.version_string,'skeletons':len(rigs),
        'bones':len(rig.data.bones),'joint_center_error_m':err_head,'rest_axis_error':err_axis,'animation_clips':len(bpy.data.actions),
        'materials':len({m.name for o in objects.values() for m in o.data.materials}),'skinned_meshes':len(objects),
        'triangles':sum(r['triangles'] for r in rows.values()),'dressed_triangles':sum(r['triangles'] for n,r in rows.items() if n not in (covered,'Underlayer | Fitted linen shift')),
        'imported_barefoot_m':max(bodypts)-min(bodypts),'imported_dressed_height_m':max(visible)-min(visible),'imported_floor_z_m':min(visible),
        'external_images_resolve':images,'meshes':rows,'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [O/'DarkElfFemale.blend',O/'DarkElfFemale.fbx']}}
    result['passed']=bool(all(images.values()) and images and err_head<2e-5 and err_axis<2e-4 and result['animation_clips']==0 and
        abs(result['imported_barefoot_m']-native['barefoot_m'])<2e-5 and abs(min(visible)-native['floor_z_m'])<2e-5 and
        all(r['armature_bind'] and r['geometry_and_slots_match'] and r['wrong_side_weights']==r['missing_weights']==0 and
            r['joint_influences']<=4 and max(r[k] for k in ('weight_sum_error','weight_error','uv_error','position_error_m'))<2e-5 for r in rows.values()))
    (R/'FBX-roundtrip.json').write_text(json.dumps(result,indent=2));print('ROUNDTRIP',result['passed'],flush=True)
    assert result['passed'], 'See FBX-roundtrip.json'

def render(name,dir,center,scale,width,height,samples=9):
    if '--base-only' in sys.argv and name not in ('Head-front','Head-profile','Underlayer'):return
    cam=sc.camera;cam.location=Vector(center)+Vector(dir).normalized()*5
    cam.rotation_euler=(Vector(center)-cam.location).to_track_quat('-Z','Y').to_euler()
    cam.data.ortho_scale=scale;sc.cycles.samples=samples
    sc.render.resolution_x=width;sc.render.resolution_y=height;sc.render.resolution_percentage=100
    sc.render.image_settings.color_mode='RGBA';sc.render.filepath=str(R/(name+'.png'))
    bpy.ops.render.render(write_still=True)
def views():
    direction=(.42,-1.65,.13);center=(0,-.035,.855)
    render('Three-quarter',direction,center,1.91,720,920)
    render('Uncovered-head',(-.46,-1.65,.12),(0,-.051,1.563),.345,700,730)
    render('Front',(0,-1,.012),center,1.91,680,900)
    render('Profile',(-1,0,.015),center,1.91,640,900)
    render('Rear',(.10,1,.055),center,1.91,680,900)
    render('Cuff',(.65,-1.05,.35),(.389,-.154,1.072),.32,620,620)
    render('Flood-register',(.33,-1.35,.075),(.085,-.120,.395),.64,650,720)
    render('Gameplay-128',direction,center,1.75,106,130,20)
    # Capture the uncovered landmarks at the same scale for the two axes.
    robe=bpy.data.collections['05  Silt Reader ensemble'];under=bpy.data.collections['04  Linen and boots']
    robe.hide_render=True;under.hide_render=True
    sc.objects['Skin | Covered limbs and torso'].hide_render=False
    render('Head-front',(0,-1,0),(0,-.052,1.563),.35,560,560)
    render('Head-profile',(-1,0,0),(0,-.052,1.563),.35,560,560)
    under.hide_render=False
    shift=sc.objects['Underlayer | Fitted linen shift'];shift.hide_render=False
    fittings=[o for o in under.objects if o.name.startswith('Lining |')]
    for o in fittings:o.hide_render=True
    render('Underlayer',direction,center,1.91,550,700)
    for o in fittings:o.hide_render=False
    shift.hide_render=True;sc.objects['Skin | Covered limbs and torso'].hide_render=True
    robe.hide_render=False
    key=bpy.data.objects['Key | Parchment'];color=key.data.color[:];key.data.color=(.56,.70,1)
    render('Cool-128',direction,center,1.75,106,130,16);key.data.color=color
    mats={s.material for o in sc.objects if o.type=='MESH' for s in o.material_slots if s.material}
    clay=bpy.data.materials.new('Kiln clay');clay.diffuse_color=(.42,.36,.32,1);sc.view_layers[0].material_override=clay
    render('Clay',direction,center,1.91,620,810)
    render('Head-clay',(-.46,-1.65,.12),(0,-.051,1.563),.345,600,620)
    sc.view_layers[0].material_override=None;key=bpy.data.objects['Key | Parchment'];key.location.x*=-1
    key.rotation_euler=(Vector((0,0,.98))-key.location).to_track_quat('-Z','Y').to_euler()
    render('Reversed-key',(-.27,-1.65,.08),(0,-.051,1.563),.345,600,620)
    for m in mats:
        nt=m.node_tree;bs=nt.nodes.get('Principled BSDF');out=nt.nodes.get('Material Output')
        em=nt.nodes.new('ShaderNodeEmission');color=bs.inputs['Base Color']
        if color.is_linked:nt.links.new(color.links[0].from_socket,em.inputs[0])
        else:em.inputs[0].default_value=color.default_value
        nt.links.new(em.outputs[0],out.inputs[0])
    sc.view_settings.view_transform='Standard';sc.view_settings.look='None'
    render('Unlit',direction,center,1.91,640,850)
    render('Head-unlit',(-.46,-1.65,.12),(0,-.051,1.563),.345,600,620)
    for m in mats:
        nt=m.node_tree;out=nt.nodes.get('Material Output');orig=out.inputs[0].links[0].from_socket
        geo=nt.nodes.new('ShaderNodeNewGeometry');mix=nt.nodes.new('ShaderNodeMixShader')
        transparent=nt.nodes.new('ShaderNodeBsdfTransparent')
        nt.links.new(geo.outputs['Backfacing'],mix.inputs[0]);nt.links.new(orig,mix.inputs[1])
        nt.links.new(transparent.outputs[0],mix.inputs[2]);nt.links.new(mix.outputs[0],out.inputs[0])
    render('Hem-culling',(.68,-1.4,-.65),(.074,-.052,.164),.60,620,560)
    # Evaluate the actual deform assignments on both sides of the cloth.
    for o in robe.objects:
        if o.type!='MESH':continue
        wmat=bpy.data.materials.new('Weight inspection '+o.name);wmat.use_nodes=True
        attr=o.data.color_attributes.new(name='Deform preview',type='FLOAT_COLOR',domain='POINT')
        for vert in o.data.vertices:
            rgb=np.array([.018,.025,.04])
            for g in vert.groups:
                n=o.vertex_groups[g.group].name
                channel=[.04,.68,.59] if n.endswith('_l') else [.95,.21,.095] if n.endswith('_r') else [.42,.30,.58] if n=='pelvis' else [.22,.23,.28]
                rgb+=g.weight*np.array(channel)
            attr.data[vert.index].color=(*rgb,1)
        nt=wmat.node_tree;vc=nt.nodes.new('ShaderNodeVertexColor');vc.layer_name=attr.name
        em=nt.nodes.new('ShaderNodeEmission');nt.links.new(vc.outputs['Color'],em.inputs[0]);nt.links.new(em.outputs[0],nt.nodes['Material Output'].inputs[0])
        o.data.materials.clear();o.data.materials.append(wmat)
    render('Weights-front',(0,-1,.01),center,1.91,430,560)
    render('Weights-rear',(0,1,.01),center,1.91,430,560)
if '--mip' in sys.argv:
    bpy.data.images['SiltReader-BaseColor.png'].scale(256,256)
    render('Atlas-256',(.62,-1.8,.20),(.09,-.12,.44),.84,420,510,6)
elif '--render' in sys.argv:views()
else:audit()
