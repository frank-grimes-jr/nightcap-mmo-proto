"""Build a standalone editable Furnace Warden and static skin from the Nightcap male rig."""
import bpy, bmesh, gzip, json, math, os, subprocess, sys, tempfile
from mathutils import Vector, Matrix
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parents[1]; ROOT=P.parent
OUT=P/'output/dark-elf-male/furnace-warden'; TEX=OUT/'Textures'; REVIEW=OUT/'Review'
sys.path.insert(0,str(P/'scripts'))
from dark_elf_warden_armor import build_armor
bpy.ops.wm.open_mainfile(filepath=str(P/'output/NightcapHumans_StarterEquipment.blend'))
sc=bpy.context.scene
rig=bpy.data.objects['Male_GameRig']; body=bpy.data.objects['Male_Editable_MPFB']
hair=[o for o in sc.objects if o.name.startswith(('Male_HairUnderlayer','Male_HairLock_'))]
eyes=[bpy.data.objects['Male_'+s+'_Eye'] for s in ('l','r')]
brows=[bpy.data.objects['Male_'+s+'_AuthoredBrow'] for s in ('l','r')]
keep=[rig,body]+hair+eyes+brows
rig.animation_data_clear();rig.data.pose_position='REST'
for o in list(bpy.data.objects):
    if o not in keep:bpy.data.objects.remove(o,do_unlink=True)
def collection(name):
    c=bpy.data.collections.new(name);sc.collection.children.link(c);return c
def move(o,c):
    for old in list(o.users_collection):old.objects.unlink(o)
    c.objects.link(o);o.hide_set(False);o.hide_viewport=False;o.hide_render=False
rigcol=collection('Skeleton'); bodycol=collection('Body'); haircol=collection('Hair'); eyecol=collection('Eyes and brows')
archive=collection('Sculpt source (full body)');refcol=collection('References (non-export)')
for o in keep:move(o,rigcol if o==rig else haircol if o in hair else eyecol if o in eyes+brows else bodycol)
for c in list(bpy.data.collections):
    if not len(c.all_objects) and c not in (archive,refcol):bpy.data.collections.remove(c)
bpy.context.view_layer.update()
def mat(name,file=None,rough=.55,metal=0,color=None,heat=None):
    m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;l=m.node_tree.links
    bs=n.get('Principled BSDF');bs.inputs['Roughness'].default_value=rough;bs.inputs['Metallic'].default_value=metal
    if color:bs.inputs['Base Color'].default_value=color;m.diffuse_color=color
    if file:
        t=n.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(file),check_existing=True)
        t.location=(-420,200);l.new(t.outputs['Color'],bs.inputs['Base Color'])
        if heat:
            q=n.new('ShaderNodeTexImage');q.image=bpy.data.images.load(str(heat),check_existing=True);q.image.colorspace_settings.name='Non-Color'
            q.location=(-600,-160);l.new(t.outputs['Color'],bs.inputs['Emission Color'])
            gain=n.new('ShaderNodeMath');gain.operation='MULTIPLY';gain.inputs[1].default_value=.85;gain.label='Banked heat intensity';gain.location=(-250,-120)
            l.new(q.outputs['Color'],gain.inputs[0]);l.new(gain.outputs[0],bs.inputs['Emission Strength'])
    return m
skin=mat('Dark Elf • indigo skin',TEX/'DarkElf-Skin.png',.69)
ivory=mat('Dark Elf • brushed ivory',TEX/'DarkElf-Ivory.png',.53)
amber=mat('Dark Elf • copper amber',TEX/'DarkElf-Amber.png',.39)
browmat=mat('Dark Elf • ash brows',color=(.100,.077,.090,1))
donor=mat('Warden • projection master',OUT/'Paint/Warden-donor-color.png')
def one_mat(o,m):
    o.data.materials.clear();o.data.materials.append(m)
    for p in o.data.polygons:p.material_index=0
def single_uv(o,name=None):
    uv=o.data.uv_layers
    if not uv:return
    take=uv.get(name) if name else uv.active
    take=take or uv[0];keepname=take.name
    for layer in list(uv):
        if layer.name!=keepname:uv.remove(layer)
    uv[0].name='UV0';uv[0].active_render=True
def skeleton(o):
    m=o.modifiers.new('Male_GameRig bind','ARMATURE');m.object=rig
def mesh_eval(o):
    deps=bpy.context.evaluated_depsgraph_get()
    mesh=bpy.data.meshes.new_from_object(o.evaluated_get(deps),depsgraph=deps,preserve_all_data_layers=True)
    o.modifiers.clear();o.data=mesh
def weights(o):
    for g in list(o.vertex_groups):
        if g.name not in rig.data.bones:o.vertex_groups.remove(g)
    for v in o.data.vertices:
        w=sorted([(g.group,g.weight) for g in v.groups if g.weight>.00001],key=lambda t:-t[1])[:4]
        if not w:
            g=o.vertex_groups.get('head') or o.vertex_groups.new(name='head')
            if o==body:raise RuntimeError('Unweighted body vertex '+str(v.index))
            w=[(g.index,1)]
        for g in list(v.groups):o.vertex_groups[g.group].remove([v.index])
        total=sum(t[1] for t in w)
        for i,val in w:o.vertex_groups[i].add([v.index],val/total,'REPLACE')
# Bake the source's neutral facial mix, preserving actual skin under its clothes.
for m in list(body.modifiers):
    if m.name!='Hide helpers':body.modifiers.remove(m)
key=body.shape_key_add(name='Warden • pinna sweep',from_mix=False)
ear_data=P/'source/mpfb-2.0.17/mpfb2-2.0.17/src/mpfb/data/targets/ears'
for side,sign in [('l',1),('r',-1)]:
    for line in gzip.open(ear_data/(side+'-ear-shape-pointed.target.gz'),'rt'):
        if line.startswith('#') or not line.strip():continue
        i,x,z,y=line.split(); tip=max(0,float(z)/.186)
        key.data[int(i)].co+=Vector((sign*.078*tip,.036*tip-float(y)*.08,.065*tip))
key.value=1
bpy.context.view_layer.update()
# Freeze source objects into the rig coordinate system; the rig itself is centered afterward.
for o in [body]+eyes+hair+brows:
    local=rig.matrix_world.inverted()@o.matrix_world
    for m in list(o.modifiers):
        if m.type=='ARMATURE':o.modifiers.remove(m)
    mesh_eval(o);o.data.transform(local);o.parent=rig;o.matrix_parent_inverse=Matrix.Identity(4);o.matrix_basis=Matrix.Identity(4)
    weights(o);skeleton(o)
rig.location.x=0
rig.hide_render=True;rig.show_in_front=False;rig.data.display_type='STICK'
bpy.context.view_layer.update()
def gauss(x,s):return math.exp(-(x/s)**2)
for v in body.data.vertices:
    x,y,z=v.co
    # Pull waist and jaw inward while preserving limb joints and eye sockets.
    if abs(x)<.20 and 1.03<z<1.39:
        v.co.x*=1-.079*gauss(z-1.17,.103)
    if abs(x)<.086 and y<-.015 and 1.55<z<1.72:
        jaw=gauss(z-1.620,.036)*gauss(y+.100,.065)
        v.co.x*=1-.133*jaw
        v.co.z-=.006*jaw*gauss(x,.050)
        cheek=gauss(abs(x)-.055,.018)*gauss(z-1.677,.020)
        v.co.y-=.005*cheek
        v.co.y-=.003*gauss(x,.009)*gauss(z-1.687,.028)
for o in hair:
    for v in o.data.vertices:
        x,y,z=v.co;amount=max(0,min(1,(z-1.698)/.110))
        v.co.y+=.017*amount**1.5
        v.co.z+=.004*amount
    single_uv(o);one_mat(o,ivory)
for o in eyes:
    single_uv(o,'EyePaint')
    for uv in o.data.uv_layers[0].data:
        uv.uv=(np.array(uv.uv)-.5)*.405+.5
        uv.uv=[min(.999,max(.001,c)) for c in uv.uv]
    one_mat(o,amber)
for o in brows:
    single_uv(o);one_mat(o,browmat)
single_uv(body,'UVMap');one_mat(body,skin)
def join(objs,name):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:o.select_set(True)
    bpy.context.view_layer.objects.active=objs[0]
    if len(objs)>1:bpy.ops.object.join()
    obj=bpy.context.view_layer.objects.active;obj.name=name;return obj
hair_obj=join(hair,'DarkElf_SweptIvory');eyes_obj=join(eyes,'DarkElf_AmberEyes');brows_obj=join(brows,'DarkElf_Brows')
body.name='DarkElf_ContinuousSculpt'
bpy.context.view_layer.update()
armor=build_armor(rig,body,{'suit':donor})
print('SUIT BUILT',len(armor),flush=True)
def part(name,upper):
    obj=body.copy();obj.data=body.data.copy();bodycol.objects.link(obj);obj.name=name
    bm=bmesh.new();bm.from_mesh(obj.data)
    faces=[f for f in bm.faces if (f.calc_center_median().z>=1.518)!=upper]
    bmesh.ops.delete(bm,geom=faces,context='FACES')
    bm.to_mesh(obj.data);bm.free()
    return obj
head=part('DarkElf_HeadAndNeck',True);covered=part('DarkElf_CoveredBody',False)
move(body,archive);body.hide_render=True;body.hide_set(True)
# FBX is Y-up; source is Z-up and faces -Y.
sc.unit_settings.system='METRIC';sc.unit_settings.scale_length=1
runtime=[head,covered,eyes_obj,brows_obj,hair_obj]+armor
# Keep the two orthographic projector fits as editable guides. Visible front
# faces receive one continuous stencil across tessellation and plate divisions.
def stencil_camera(name,focus,delta,span):
    camera=bpy.data.cameras.new(name);camera.type='ORTHO';camera.ortho_scale=span
    obj=bpy.data.objects.new(name,camera);refcol.objects.link(obj)
    obj.location=Vector(focus)+Vector(delta);obj.rotation_euler=(-Vector(delta)).to_track_quat('-Z','Y').to_euler()
    return obj
figure_proj=stencil_camera('Projection • figure',(0,-.04,.93),(.45,-5,.14),2.02)
portrait_proj=stencil_camera('Projection • portrait',(0,-.08,1.62),(1.05,-4,.38),.72)
bpy.context.view_layer.update()
def stencil(o,tile,cam):
    me=o.data;uv=me.uv_layers.active.data
    def native_tile(p):
        u,v=uv[p.loop_start].uv
        return int(u*4)+(3-int(v*4))*4
    toward=(cam.location-Vector((0,0,1))).normalized()
    faces=[p for p in me.polygons if native_tile(p)==tile and p.normal.dot(toward)>.40]
    if not faces:return
    inv=cam.matrix_world.inverted()
    positions={i:(inv@(o.matrix_world@me.vertices[i].co)).xy for p in faces for i in p.vertices}
    low=np.min(list(positions.values()),axis=0);span=np.maximum(np.ptp(list(positions.values()),axis=0),.0001)
    for p in faces:
        for li in p.loop_indices:
            q=(np.array(positions[me.loops[li].vertex_index])-low)/span
            uv[li].uv=((tile%4+.05+.90*q[0])/4,(3-tile//4+.05+.90*q[1])/4)
for o in armor:
    if 'BoxPauldron' in o.name:stencil(o,1,portrait_proj)
    if 'Greave_' in o.name:stencil(o,10,figure_proj)
    if 'TassetApron' in o.name:stencil(o,9,figure_proj)
def project_uv():
    bpy.ops.object.select_all(action='DESELECT')
    for o in armor:
        layer=o.data.uv_layers[0];layer.name='DonorProjection'
        o.data.uv_layers.new(name='AtlasUV');o.data.uv_layers.active=o.data.uv_layers['AtlasUV']
        o.select_set(True)
    bpy.context.view_layer.objects.active=armor[0]
    bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(58),island_margin=.002,area_weight=.4)
    bpy.ops.uv.select_all(action='SELECT');bpy.ops.uv.average_islands_scale()
    bpy.ops.uv.pack_islands(rotate=True,scale=True,margin=.0035,margin_method='FRACTION',shape_method='AABB')
    bpy.ops.object.mode_set(mode='OBJECT')
    old=[];new=[];positions=[]
    for o in armor:
        mesh=o.data;mesh.calc_loop_triangles()
        for tri in mesh.loop_triangles:
            old.append([tuple(mesh.uv_layers['DonorProjection'].data[i].uv) for i in tri.loops])
            new.append([tuple(mesh.uv_layers['AtlasUV'].data[i].uv) for i in tri.loops])
            positions.append([tuple(mesh.vertices[i].co) for i in tri.vertices])
    temp=Path(tempfile.gettempdir())/'nightcap-warden-uv.npz'
    np.savez(temp,old=np.array(old),new=np.array(new),positions=np.array(positions))
    subprocess.run([os.environ['WARDEN_PAINT_PY'],str(P/'scripts/warden_bake.py'),str(OUT),str(temp)],check=True)
    temp.unlink()
project_uv()
print('COLOR + HEAT BAKED',flush=True)
plate=mat('Furnace Warden • banked iron',TEX/'Warden-Plate.png',.48,.28,heat=TEX/'Warden-Heat.png')
for o in armor:
    one_mat(o,plate)
    # Keep the projection coordinates in the source as an editable secondary layer.
    mesh=o.data
    old=[tuple(v.uv) for v in mesh.uv_layers['DonorProjection'].data]
    new=[tuple(v.uv) for v in mesh.uv_layers['AtlasUV'].data]
    mesh.uv_layers.remove(mesh.uv_layers['AtlasUV']);mesh.uv_layers[0].name='UV0'
    for u,xy in zip(mesh.uv_layers[0].data,new):u.uv=xy
    layer=mesh.uv_layers.new(name='DonorProjection')
    for u,xy in zip(layer.data,old):u.uv=xy
    mesh.uv_layers.active=mesh.uv_layers['UV0'];mesh.uv_layers['UV0'].active_render=True
# Set up editable reference plane and study cards.
art=ROOT/'systems-planning/assets/concept-art/dark-elf'
def reference_plane(name,path,x,z,w):
    bpy.ops.mesh.primitive_plane_add(size=1,location=(x,1.4,z),rotation=(math.pi/2,0,0))
    o=bpy.context.object;o.name=name;move(o,refcol)
    m=mat(name,path);one_mat(o,m);im=next(n.image for n in m.node_tree.nodes if n.type=='TEX_IMAGE')
    o.scale=(w,w*im.size[1]/im.size[0],1);o.hide_render=True;return o
reference_plane('Warden • original native projection plate',art/'furnace-warden.png',2.4,1.0,2.1)
refcol.hide_viewport=True;refcol.hide_render=True
# Rig rest record makes the reimport comparison independent of FBX bone display lengths.
bones={b.name:{'parent':b.parent.name if b.parent else None,'rest':[list(row) for row in b.matrix_local]} for b in rig.data.bones}
def data_row(o):
    mesh=o.data;mesh.calc_loop_triangles()
    deform={g.index for g in o.vertex_groups if g.name in rig.data.bones}
    vw=[[g.weight for g in v.groups if g.group in deform and g.weight>0] for v in mesh.vertices]
    used={inf.group for v in mesh.vertices for inf in v.groups if inf.weight>0}
    assert all(w and len(w)<=4 and abs(1-sum(w))<1e-5 for w in vw),o.name
    return {'vertices':len(mesh.vertices),'triangles':len(mesh.loop_triangles),'materials':[m.name for m in mesh.materials],
            'groups':sorted(g.name for g in o.vertex_groups if g.index in used),
            'max_influences':max(map(len,vw)),'category':o.get('warden_group',o.users_collection[0].name)}
coords=lambda objects:[o.matrix_world@v.co for o in objects for v in o.data.vertices]
bounds=lambda ps:([min(v[i] for v in ps) for i in range(3)],[max(v[i] for v in ps) for i in range(3)])
report={'bones':bones,'meshes':{o.name:data_row(o) for o in runtime},'body_bounds':bounds(coords([body])),'dressed_bounds':bounds(coords([head,eyes_obj,brows_obj]+armor)),'axis':'Blender -Y / FBX -Z forward, Y up','animation':False}
(REVIEW/'Native-bind.json').write_text(json.dumps(report,indent=2))
# Save only packed, used art. Remap paths relative to the delivery directory.
for action in list(bpy.data.actions):bpy.data.actions.remove(action)
for image in bpy.data.images:image.use_fake_user=False
for material in bpy.data.materials:material.use_fake_user=False
bpy.data.orphans_purge(do_recursive=True)
for im in bpy.data.images:
    if im.source=='FILE':
        try:im.pack()
        except RuntimeError:pass
        if im.filepath:im.filepath='//'+os.path.relpath(bpy.path.abspath(im.filepath),str(OUT)).replace('\\','/')
for obj in [hair_obj,covered]:obj.hide_render=True;obj.hide_set(True)
sc.render.film_transparent=True;sc.render.engine='CYCLES';sc.cycles.samples=12
sc.world=bpy.data.worlds.new('Portrait studio');sc.world.use_nodes=True
sc.world.node_tree.nodes['Background'].inputs[0].default_value=(.42,.37,.45,1)
sc.world.node_tree.nodes['Background'].inputs[1].default_value=.36
def studio_light(name,xyz,target,color,power,size):
    light=bpy.data.lights.new(name,'AREA');light.energy=power;light.color=color;light.shape='DISK';light.size=size
    ob=bpy.data.objects.new(name,light);sc.collection.objects.link(ob);ob.location=xyz
    ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler()
for args in [('Pale forge window',(-2.4,-3.4,4.1),(0,0,1.15),(.86,.91,1),245,2.6),('Copper bounce',(2,-2.3,2.1),(0,0,1.1),(1,.76,.65),73,2.2),('Edge light',(1,.9,2.8),(0,0,1.2),(.74,.80,1),145,1.8)]:studio_light(*args)
cam=bpy.data.cameras.new('Portrait lens');camera=bpy.data.objects.new('Review camera',cam);sc.collection.objects.link(camera)
sc.camera=camera;cam.type='ORTHO';cam.ortho_scale=2.18
target=Vector((0,0,.93));camera.location=(2.0,-6.5,1.77);camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
sc.render.resolution_x=650;sc.render.resolution_y=820;sc.render.resolution_percentage=100
sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast'
bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active=head
for area in bpy.context.screen.areas:
    if area.type=='VIEW_3D':
        s=area.spaces.active;s.region_3d.view_perspective='CAMERA';s.shading.type='MATERIAL';s.overlay.show_overlays=False
sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA'
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'DarkElfMale.blend'),compress=True,relative_remap=False)
# Convert the export copy to exactly the runtime surface layout.
for o in runtime:
    o.hide_render=False;o.hide_set(False);o.select_set(True)
    single_uv(o,'UV0')
rig.select_set(True);bpy.context.view_layer.objects.active=rig
bpy.ops.export_scene.fbx(filepath=str(OUT/'DarkElfMale.fbx'),use_selection=True,object_types={'MESH','ARMATURE'},add_leaf_bones=False,use_armature_deform_only=True,bake_anim=False,use_mesh_modifiers=True,axis_forward='-Z',axis_up='Y',apply_scale_options='FBX_SCALE_UNITS',use_triangles=True,path_mode='RELATIVE')
print('WARDEN EXPORTED',flush=True)

