"""Build the static Silt Reader at the original female joint centers. Run with Blender 5.2."""
import bpy, bmesh, gzip, math, json, sys
from collections import defaultdict
from pathlib import Path
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree
import numpy as np
from math import sin, cos, pi, exp

P=Path(__file__).resolve().parents[1]
OUT=P/'output/dark-elf-female/silt-reader'
T=OUT/'Textures'; R=OUT/'Review'
sc=bpy.context.scene
bpy.ops.wm.open_mainfile(filepath=str(P/'output/NightcapHumans_StarterEquipment.blend'))
sc=bpy.context.scene
bpy.context.preferences.filepaths.save_version=0
# Establish the separate work file before modifying the source scene.
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'DarkElfFemale.blend'),compress=True)
rig=bpy.data.objects['Female_GameRig']; body=bpy.data.objects['Female_Editable_MPFB']
rig.animation_data_clear(); rig.data.pose_position='REST'
parts=[o for o in sc.objects if o.name.startswith('Female_') and
       (o==body or o.name.startswith(('Female_HairLock','Female_HairUnderlayer')) or
        o.name.endswith(('_Eye','_AuthoredBrow','_LeatherBoot','_BootSole','_BootCuff')))]
for o in list(bpy.data.objects):
    if o not in parts and o!=rig:bpy.data.objects.remove(o,do_unlink=True)
def collection(name):
    c=bpy.data.collections.new(name); sc.collection.children.link(c); return c
bind=collection('01  Skeleton'); skincol=collection('02  Skin and features')
haircol=collection('03  Ivory bob and braid'); under=collection('04  Linen and boots')
suit=collection('05  Silt Reader ensemble'); archive=collection('06  Body restoration')
studio=collection('07  Portrait studio')
def move(o,c):
    for old in list(o.users_collection):old.objects.unlink(o)
    c.objects.link(o); o.hide_set(False); o.hide_render=False; o.hide_viewport=False
move(rig,bind)
for o in parts:move(o,skincol)
for c in list(bpy.data.collections):
    if c not in (bind,skincol,haircol,under,suit,archive,studio) and not len(c.all_objects):bpy.data.collections.remove(c)
bpy.context.view_layer.update()
def bind_to(o):
    mod=o.modifiers.new('Female bind','ARMATURE'); mod.object=rig; o.parent=rig
def weights(o):
    for g in list(o.vertex_groups):
        if g.name not in rig.data.bones:o.vertex_groups.remove(g)
    for v in o.data.vertices:
        w=sorted([(g.group,g.weight) for g in v.groups if g.weight>.00001],key=lambda v:-v[1])[:4]
        assert w,(o.name,v.index)
        for g in list(v.groups):o.vertex_groups[g.group].remove([v.index])
        for i,k in w:o.vertex_groups[i].add([v.index],k/sum(wt for _,wt in w),'REPLACE')
for mod in list(body.modifiers):
    if mod.name!='Hide helpers':body.modifiers.remove(mod)
def evaluated(o):
    bpy.context.view_layer.update()
    deps=bpy.context.evaluated_depsgraph_get()
    return bpy.data.meshes.new_from_object(o.evaluated_get(deps),depsgraph=deps,preserve_all_data_layers=True)
def xyz(o):return np.array([v.co[:] for v in o.data.vertices])
initial=evaluated(body); local=rig.matrix_world.inverted()@body.matrix_world
basepts=np.array([list(local@v.co) for v in initial.vertices]); bpy.data.meshes.remove(initial)
key=body.shape_key_add(name='Silt Reader swept pinnae',from_mix=False)
targets=P/'source/mpfb-2.0.17/mpfb2-2.0.17/src/mpfb/data/targets/ears'
for side,sign in [('l',1),('r',-1)]:
    for row in gzip.open(targets/(side+'-ear-shape-pointed.target.gz'),'rt'):
        if row.startswith('#') or not row.strip():continue
        i,x,z,y=row.split(); f=max(0,float(z)/.186)
        key.data[int(i)].co+=Vector((sign*.078*f,.042*f-float(y)*.075,.057*f))
key.value=.18
for o in parts:
    local=rig.matrix_world.inverted()@o.matrix_world
    for mod in list(o.modifiers):
        if mod.type=='ARMATURE':o.modifiers.remove(mod)
    me=evaluated(o); o.modifiers.clear(); o.data=me; me.transform(local)
    o.parent=rig; o.matrix_parent_inverse=Matrix.Identity(4); o.matrix_basis=Matrix.Identity(4)
    weights(o); bind_to(o)
rig.location.x=0; rig.show_in_front=False; rig.data.display_type='STICK'
for b in rig.pose.bones:b.matrix_basis=Matrix.Identity(4)
rig.data.pose_position='REST'; bpy.context.view_layer.update()
def gauss(v,s):return exp(-(v/s)**2)
def front(x,y,z):return max(0,min(1,(-y-.045)/.05))
for v in body.data.vertices:
    x,y,z=v.co; f=front(x,y,z)
    if 1.47<z<1.64 and abs(x)<.093:
        jaw=gauss(z-1.519,.031)*f
        v.co.x*=1-.106*jaw; v.co.z-=.004*jaw*gauss(x,.033)
        v.co.y-=f*(.0048*gauss(abs(x)-.052,.022)*gauss(z-1.557,.018)
                   +.0027*gauss(x,.012)*gauss(z-1.567,.030)
                   +.0025*gauss(abs(x)-.033,.028)*gauss(z-1.602,.012))
def mat(name,hexcolor,rough=.8,metal=0,file=None):
    m=bpy.data.materials.new(name); m.use_nodes=True
    rgb=[int(hexcolor[i:i+2],16)/255 for i in (0,2,4)]
    rgba=tuple(((v+.055)/1.055)**2.4 if v>.04045 else v/12.92 for v in rgb)+(1,)
    m.diffuse_color=rgba; bs=m.node_tree.nodes.get('Principled BSDF'); bs.inputs['Base Color'].default_value=rgba
    bs.inputs['Roughness'].default_value=rough; bs.inputs['Metallic'].default_value=metal
    if file:
        n=m.node_tree.nodes.new('ShaderNodeTexImage'); n.image=bpy.data.images.load(str(T/file),check_existing=True)
        m.node_tree.links.new(n.outputs['Color'],bs.inputs['Base Color'])
    m.use_backface_culling=True
    return m
def assign(o,m,uv=None):
    o.data.materials.clear(); o.data.materials.append(m)
    for p in o.data.polygons:p.material_index=0
    layers=o.data.uv_layers
    if layers:
        name=(layers.get(uv) if uv else layers.active).name
        for l in list(layers):
            if l.name!=name:layers.remove(l)
        layers[0].name='UV0';layers[0].active_render=True
skin=mat('Silt | Indigo skin','655674',.71)
hair=mat('Silt | Combed ivory','cfc5b2',.58,file='Ivory-Locks.png')
eye=mat('Silt | Copper iris','a46c3a',.34,file='Copper-Iris.png')
brow=mat('Silt | Ash brows','453a4b')
wool=mat('Silt | Dyed cloth','4c5068',.91,file='SiltReader-BaseColor.png')
metal=mat('Silt | Worn brass','ae8653',.39,.65)
assign(body,skin,'UVMap')
# Bake a newly authored, spatially painted skin field onto the canonical body UV.
nt=skin.node_tree; bs=nt.nodes.get('Principled BSDF'); out=nt.nodes.get('Material Output')
attr=body.data.color_attributes.new(name='Fresh indigo paint',type='FLOAT_COLOR',domain='POINT')
for v in body.data.vertices:
    x,y,z=v.co; ax=abs(x); f=front(x,y,z)
    rgb=np.array([88.,74.,110.])
    rgb+=np.array([12.,6.,8.])*gauss(ax-.050,.035)*gauss(z-1.56,.037)*f
    rgb+=np.array([15.,-1.,-2.])*gauss(ax-.097,.042)*gauss(z-1.587,.045)
    rgb+=np.array([-30.,-31.,-21.])*gauss(z-1.583,.012)*gauss(ax-.033,.023)*f
    rgb+=np.array([-9.,-28.,-20.])*gauss(z-1.518,.0068)*gauss(x,.030)*f
    rgb+=np.array([17.,0.,2.])*gauss(z-1.512,.0045)*gauss(x,.022)*f
    cheek=gauss(ax-.051,.021)*gauss(z-1.548-.28*(ax-.05),.013)*f
    rgb+=np.array([-12.,-13.,-9.])*cheek
    rgb+=np.array([6.,5.,5.])*gauss(ax-.054,.023)*gauss(z-1.561,.009)*f
    rgb+=np.array([-7.,-7.,-4.])*gauss(ax-.012,.005)*gauss(z-1.555,.016)*f
    rgb+=2.2*cos(z*19+x*23)*cos(y*16)
    attr.data[v.index].color=tuple(((rgb/255+.055)/1.055)**2.4)+(1,)
vc=nt.nodes.new('ShaderNodeVertexColor');vc.layer_name=attr.name
em=nt.nodes.new('ShaderNodeEmission');nt.links.new(vc.outputs['Color'],em.inputs[0]);nt.links.new(em.outputs[0],out.inputs['Surface'])
im=bpy.data.images.new('Indigo-Skin.png',1024,1024,alpha=False)
im.generated_color=(.14,.10,.21,1)
imgnode=nt.nodes.new('ShaderNodeTexImage');imgnode.image=im;nt.nodes.active=imgnode
bpy.ops.object.select_all(action='DESELECT');body.select_set(True);bpy.context.view_layer.objects.active=body
sc.render.engine='CYCLES';sc.cycles.samples=1
bpy.ops.object.bake(type='EMIT',margin=12,use_clear=False)
im.filepath_raw=str(T/'Indigo-Skin.png');im.file_format='PNG';im.save()
nt.nodes.remove(vc);nt.nodes.remove(em);nt.links.new(imgnode.outputs['Color'],bs.inputs['Base Color']);nt.links.new(bs.outputs[0],out.inputs['Surface'])
def join(objects,name,c):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects:o.select_set(True)
    bpy.context.view_layer.objects.active=objects[0]
    if len(objects)>1:bpy.ops.object.join()
    o=bpy.context.view_layer.objects.active;o.name=name;move(o,c);return o
locks=[o for o in parts if 'Hair' in o.name]
eyes=[o for o in parts if o.name.endswith('_Eye')]
brows=[o for o in parts if o.name.endswith('_AuthoredBrow')]
boots=[o for o in parts if 'Boot' in o.name]
for o in locks:assign(o,hair)
for o in eyes:
    assign(o,eye,'EyePaint')
    for u in o.data.uv_layers[0].data:u.uv=[min(.999,max(.001,(c-.5)*.66+.5)) for c in u.uv]
face_tree=BVHTree.FromPolygons([v.co for v in body.data.vertices],[p.vertices[:] for p in body.data.polygons])
def front_y(tree,x,z):
    hit=tree.ray_cast(Vector((x,-1,z)),Vector((0,1,0)))[0]
    return hit.y if hit else 1
for o in brows:
    assign(o,brow)
    for v in o.data.vertices:
        x,y,z=v.co
        arch=1.602+.005*sin(pi*min(1,max(0,(abs(x)-.011)/.052)))
        z=arch+(z-arch)*.64+.005*(abs(x)-.028)/.04-.002
        v.co.z=z;v.co.y=min(y-.0016,front_y(face_tree,x,z)-.0016)
def mapped(name,u,v):
    boxes={'Wrap':(0,0,474,1430),'Left':(475,0,1051,1430),'Back':(1052,0,1408,1430),'Inside':(1409,0,2047,1430),'Sleeve':(0,1431,490,2047),'Yoke':(491,1431,995,2047),'Clay':(996,1431,1241,2047),'Flax':(1242,1431,1469,2047),'Sash':(1470,1431,1663,2047),'Facing':(1664,1431,1855,2047),'Boot':(1856,1431,2047,2047)}
    x,y,X,Y=boxes[name];return ((x+18+u*(X-x-36))/2048,1-(Y-18-v*(Y-y-36))/2048)
for o in boots:
    assign(o,wool)
    for uv in o.data.uv_layers[0].data:uv.uv=mapped('Boot',*(min(1,max(0,c)) for c in uv.uv))
    for v in o.data.vertices:v.co.z-=.004
bootobj=join(boots,'Underlayer | River leather boots',under)
bob=join(locks,'Hair | Swept ivory bob',haircol)
eyesobj=join(eyes,'Eyes | Copper pair',skincol)
browsobj=join(brows,'Face | Ash brows',skincol)
def partition(name,predicate,c):
    o=body.copy();o.data=body.data.copy();c.objects.link(o);o.name=name
    bm=bmesh.new();bm.from_mesh(o.data)
    bmesh.ops.delete(bm,geom=[f for f in bm.faces if not predicate(*f.calc_center_median())],context='FACES')
    bm.to_mesh(o.data);bm.free();return o
def exposed(x,y,z):return z>1.465 or (z>1.394 and abs(x)<.053 and -.095<y<.057) or abs(x)>.408 and y<-.135
show=partition('Skin | Head neck and hands',exposed,skincol)
covered=partition('Skin | Covered limbs and torso',lambda x,y,z:not exposed(x,y,z),archive)
body.name='Sculpt | Continuous female base';move(body,archive)
body.hide_set(True);body.hide_render=True
def wrap_w(p):
    x,y,z=p
    if z>1.05:
        a=min(1,(z-1.05)/.14);return {'spine_02':1-a,'spine_03':a}
    t=min(.88,max(0,(.93-z)/.48)); side='l' if x>0 else 'r'
    t*=min(1,abs(x)/.036)
    return {'pelvis':1-t,'thigh_'+side:t}
def rigid(n):return lambda p:{n:1}
def surface(name,nu,nv,point,uvbed,weight=wrap_w,c=suit,m=wool,thickness=.002,smooth=True,flip=False):
    vs=[];uvs=[];faces=[]
    for j in range(nv+1):
        for i in range(nu+1):
            u=i/nu;v=j/nv;vs.append(tuple(point(u,v)));uvs.append(mapped(uvbed,u,v) if uvbed else (u,v))
    for j in range(nv):
        for i in range(nu):
            a=j*(nu+1)+i;q=(a,a+1,a+nu+2,a+nu+1);faces.append(q[::-1] if flip else q)
    me=bpy.data.meshes.new(name);me.from_pydata(vs,[],faces);me.update()
    o=bpy.data.objects.new(name,me);c.objects.link(o);me.materials.append(m)
    uv=me.uv_layers.new(name='UV0')
    for p in me.polygons:
        p.use_smooth=smooth
        for li in p.loop_indices:uv.data[li].uv=uvs[me.loops[li].vertex_index]
    for i,p in enumerate(vs):
        for n,w in weight(p).items():
            if w>0:(o.vertex_groups.get(n) or o.vertex_groups.new(name=n)).add([i],w,'REPLACE')
    # The cylindrical seam is a UV split. Weld the coincident geometry before
    # building the inside so no radial wall doubles up along the seam.
    bm=bmesh.new();bm.from_mesh(me)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.000002)
    bm.to_mesh(me);bm.free();me.update()
    if thickness:
        sol=o.modifiers.new('Turned inner surface','SOLIDIFY');sol.thickness=thickness;sol.offset=-1
        sol.use_even_offset=True;me2=evaluated(o);o.modifiers.clear();o.data=me2
    # The inner and outer lips can cross the center plane at the back pleat.
    # Assign those solidified vertices from their final side of the garment.
    if weight is wrap_w:
        for v in o.data.vertices:
            for g in list(v.groups):o.vertex_groups[g.group].remove([v.index])
            for n,w in weight(v.co).items():
                if w>0:(o.vertex_groups.get(n) or o.vertex_groups.new(name=n)).add([v.index],w,'REPLACE')
    bind_to(o);return o
def tube(name,centers,radii,bed,wt,c=suit,material=wool,n=16):
    pts=[Vector(p) for p in centers]
    def pt(u,v):
        j=min(len(pts)-1,round(v*(len(pts)-1)))
        axis=(pts[min(j+1,len(pts)-1)]-pts[max(0,j-1)]).normalized()
        axis1=axis.cross(Vector((0,1,0))).normalized();axis2=axis.cross(axis1).normalized()
        return pts[j]+radii[j][0]*axis1*cos(2*pi*u)+radii[j][1]*axis2*sin(2*pi*u)
    return surface(name,n,len(pts)-1,pt,bed,wt,c,material,.0014)
# An inverted pleat breaks the quiet back, deepening below the sash.
profile=np.array([
 (.126,.280,.169,-.027),(.150,.279,.168,-.027),(.32,.258,.154,-.025),
 (.54,.231,.146,-.020),(.76,.205,.137,-.015),(.88,.199,.144,-.011),
 (.97,.170,.135,-.015),(1.056,.143,.115,-.020),(1.097,.144,.117,-.020),
 (1.15,.155,.135,-.022),(1.225,.174,.155,-.027),(1.29,.184,.134,-.018),
 (1.346,.181,.104,-.009),(1.375,.146,.092,-.009),(1.400,.077,.072,-.009),
 (1.424,.063,.062,-.010)])
def shell(a,z,extra=0):
    rx,ry,cy=[np.interp(z,profile[:,0],profile[:,i]) for i in [1,2,3]]
    amp=np.interp(z,[.126,.55,.95,1.07,1.25,1.424],[.015,.012,.004,.001,.004,.001])
    fold=amp*(.77*cos(9*a+.35*z)+.43*cos(13*a-.7*z)+.22*sin(5*a))
    fold+=.0055*gauss(z-1.059,.081)*sin(81*z+3.8*sin(a+.4))
    back=(a-pi+pi)%(2*pi)-pi
    fold+=.018*max(0,min(1,(1.17-z)/.55))*(gauss(abs(back)-.16,.095)-1.2*gauss(back,.075))
    return Vector(((rx+fold+extra)*sin(a),cy-(ry+fold+extra)*cos(a),z))
def hem(a):return .129+.009*cos(3*a+.2)+.005*cos(7*a)
def diag(z):return np.interp(z,[.12,1.055,1.15,1.26,1.34,1.4,1.424],[-.59,-.70,-.39,.02,.30,.72,.87])
def slit(z):return max(0,min(1,(.66-z)/.48))*.14
def ends(i,z):
    return [(diag(z),.94-slit(z)),(.94+slit(z),pi),(pi,4.38),(4.38,2*pi+diag(z))][i]
def panel(i,u,v):
    z=.13+v*1.294
    a0,a1=ends(i,z);a=a0+(a1-a0)*u
    z+=(hem(a)-.13)*(1-v)**4
    return shell(a,z,.001 if i==0 else 0)
for i,bed in enumerate(['Wrap','Left','Back','Inside']):
    surface('Robe | '+['Outer wrap front','Left skirt and side','Joined back pleat','Inside wrap front'][i], [24,31,20,26][i],37,lambda u,v,i=i:panel(i,u,v),bed)
surface('Lining | Clay slit inset',12,26,lambda u,v:shell(.94+(u-.5)*.48,.13+.60*v,-.011),'Clay',c=under)
surface('Lining | Inner wrap return',8,48,lambda u,v:shell(diag(.13+1.294*v)-.032+u*.14,.13+1.294*v,-.004),'Clay',c=under)
surface('Robe | Bound diagonal placket',5,60,lambda u,v:shell(diag(.133+1.291*v)+.006+u*.082,.133+1.291*v,.0038),'Facing')
surface('Robe | Narrow placket selvage',2,60,lambda u,v:shell(diag(.133+1.291*v)+.077+u*.012,.133+1.291*v,.005),'Flax',thickness=.0007)
def collar(u,v):
    a=.60+u*(2*pi-1.20)
    return shell(a,1.399+v*(.033+.007*(1-cos(a))),.004+.003*v)
surface('Robe | Open bound collar',45,6,collar,'Facing',rigid('spine_03'))
def sash(u,v):
    a=2*pi*u;z=1.045+.047*v+.009*sin(a+.3);return shell(a,z,.010+.003*sin(pi*v))
surface('Robe | Double turn sash',80,8,sash,'Sash')
for j in (0,1):
    surface('Robe | Sash cord '+str(j+1),72,3,lambda u,v,j=j:shell(u*2*pi,1.052+j*.030+.003*v+.009*sin(u*2*pi+.3),.0145),'Facing')
for side,sign in [('l',1),('r',-1)]:
    joint=lambda key:rig.data.bones[key+'_'+side].head_local.copy()
    shoulder,elbow,wrist=map(joint,['upperarm','lowerarm','hand'])
    start=shoulder+Vector((-.030*sign,.002,.010)); target=wrist.lerp(elbow,.102)
    pts=[start+Vector((-.016*sign,0,0)),start,shoulder.lerp(elbow,.15),shoulder.lerp(elbow,.36),shoulder.lerp(elbow,.73),elbow,
         elbow.lerp(wrist,.12),elbow.lerp(wrist,.39),elbow.lerp(wrist,.66),elbow.lerp(wrist,.82),target]
    sizes=[(.015,.021),(.054,.065),(.077,.080),(.066,.063),(.056,.054),(.056,.053),(.058,.054),(.048,.050),(.043,.043),(.042,.041),(.041,.039)]
    def armwt(p):
        # Project onto the two own-side bind segments around the elbow.
        w=min(1,max(0,.5+(Vector(p)-elbow).dot((wrist-shoulder).normalized())/.13))
        return {'upperarm_'+side:1-w,'lowerarm_'+side:w}
    tube('Robe | Tapered sleeve '+side,pts,sizes,'Sleeve',armwt,n=28)
    cf=[elbow.lerp(wrist,t) for t in [.72,.73,.80,.86,.90]]
    tube('Robe | Turned flax cuff '+side,cf,[(.047,.045),(.049,.047),(.047,.046),(.045,.044),(.043,.042)],'Flax',rigid('lowerarm_'+side),n=28)
    for j,t in enumerate((.746,.769,.875)):
        tube(f'Robe | Cuff woven line {side}{j}',[elbow.lerp(wrist,t),elbow.lerp(wrist,t+.009)],[(.049,.048),(.049,.048)] if j<2 else [(.0445,.044)]*2,'Facing',rigid('lowerarm_'+side),n=24)
# Fit the yoke over both sleeve heads, keeping the parallel topstitch on the same surface.
shoulder_meshes=[o for o in suit.objects if any(s in o.name for s in ('sleeve','wrap front','Left skirt','Joined back'))]
shoulder_trees=[BVHTree.FromPolygons([v.co for v in o.data.vertices],[p.vertices[:] for p in o.data.polygons]) for o in shoulder_meshes]
def yoke(u,v):
    a=2*pi*u;t=1-v
    rx=.061+.172*t;ry=.061+(.067+.007*cos(a))*t
    x=rx*sin(a);y=-.012-ry*cos(a)
    z=1.425-.048*t-.043*t*t
    hits=[tr.ray_cast(Vector((x,y,1.55)),Vector((0,0,-1)))[0] for tr in shoulder_trees]
    hit=max([p.z for p in hits if p]+[1.29])
    lo=1.30+.047*(1+cos(a))*.5
    z=max(z,hit+.0048)*(1-t**5)+(lo+.0048)*t**5
    # Trace the last centimeter to the actual cloth so the hem settles on the
    # shoulder. The front yoke stays high and the lower back spans the pleat.
    ray=Vector((sin(a),-cos(a),0))
    hits=[tr.ray_cast(Vector((0,-.012,z))+ray*.35,-ray)[0] for tr in shoulder_trees]
    outer=max([q for q in hits if q],key=lambda q:(q-Vector((0,-.012,z))).dot(ray),default=None)
    if outer:
        blend=t**3; x=x*(1-blend)+(outer.x+.0045*ray.x)*blend;y=y*(1-blend)+(outer.y+.0045*ray.y)*blend
    return Vector((x,y,z))
surface('Robe | Shaped shoulder yoke',72,15,yoke,'Yoke',rigid('spine_03'),thickness=.0028)
surface('Robe | Yoke binding',72,3,lambda u,v:yoke(u,.021+.017*v)+Vector((.0011*sin(2*pi*u),-.0011*cos(2*pi*u),.0015)),'Facing',rigid('spine_03'),thickness=.0008)
surface('Lining | Collar inner lip',64,3,lambda u,v:((.049+.018*v)*sin(2*pi*u),-.011-(.055+.012*v)*cos(2*pi*u),1.418+.006*v),'Facing',rigid('spine_03'),c=under)
# Thick leaf-shaped pinnae with a raised helix and a warm bowl on each ear.
earmat=mat('Silt | Auricle paint','695571',.78,file='Auricle.png')
for side,sign in [('l',1),('r',-1)]:
    def pinna(u,v):
        t=u;root=sin(pi*t)**.72
        low=1.548+.073*t-.011*root
        high=1.596+.025*t+.004*root
        x=sign*(.071+.085*t);z=low+(high-low)*v
        rim=exp(-((v-.84)/.11)**2)+.53*exp(-((v-.16)/.12)**2)
        y=-.075+.081*t+(.005-.010*rim-.006*exp(-((v-.47-.12*t)/.13)**2))*root
        return (x,y,z)
    surface('Face | Modelled pinna '+side,28,14,pinna,None,rigid('head'),skincol,earmat,.0035,flip=sign<0)
# Broad side-parted locks follow the existing skull and taper toward the right temple.
bobtree=BVHTree.FromPolygons([v.co for v in bob.data.vertices],[p.vertices[:] for p in bob.data.polygons])
for k,(startx,startz,endx,endz,width) in enumerate([
    (.046,1.689,-.070,1.577,.020),(.040,1.699,-.080,1.565,.022),
    (.034,1.705,-.085,1.556,.020),(.050,1.679,-.056,1.609,.011)]):
    def fringe(u,t):
        x=(1-t)*startx+t*endx-.008*sin(pi*t)
        z=startz*(1-t)+endz*t+.014*sin(pi*t)
        norm=(width*(.035+.965*sin(pi*t)**.60))*(u-.5)
        x+=norm;z-=norm*.95
        y=min(front_y(face_tree,x,z),front_y(bobtree,x,z))
        if y>.15:y=-.092
        y-=.002+.0031*sin(pi*u)*sin(pi*t)+.0007*k
        return (x,y,z)
    surface('Hair | Swept forelock '+str(k+1),8,28,fringe,None,rigid('head'),haircol,hair,.0015,flip=True)
# One temple braid, woven from three locks under two rolled brass ferrules.
def braid_center(t):return Vector((-.081-.024*t,-.103-.009*t+.005*cos(pi*t),1.608-.190*t))
for j in range(3):
    centers=[];rr=[]
    for i in range(54):
        t=i/53;phase=2*pi*(t*3.8+j/3); q=braid_center(t)
        q+=Vector((.0062*cos(phase),.0048*sin(phase),0));centers.append(q);rr.append((.0058-.0013*t, .0063-.0016*t))
    tube('Hair | Braid strand '+str(j+1),centers,rr,None,rigid('head'),haircol,hair,10)
for j,t in enumerate((.18,.89)):
    tube('Hair | Bound ferrule '+str(j+1),[braid_center(t+dt) for dt in [-.003,0,.039,.042]],[(.012,.0105),(.0128,.011),(.0128,.011),(.012,.0105)],None,rigid('head'),haircol,metal,16)
def pendant(u,v):
    t=2*pi*u;radius=np.interp(v,[0,.13,.32,.75,.91,1],[.001,.010,.012,.009,.005,.003])
    return (-.110+radius*cos(t),-.140+radius*sin(t),.914+v*.058)
tube('Accessory | Waxed plumb line',[(-.102,-.120,1.063),(-.110,-.138,1.033),(-.110,-.140,.971)],[(.003,.003)]*3,'Sash',rigid('pelvis'))
surface('Robe | Sash keeper',6,10,lambda u,v:shell(-.73+(u-.5)*.12+.031*(v-.5),1.034+.059*v,.019+.002*sin(pi*v)),'Sash',rigid('pelvis'))
surface('Robe | Folded sash end',6,12,lambda u,v:shell(-.84+.15*u+.09*v,.988+.068*v+.008*u,.014+.004*cos(1.6*pi*u)),'Sash',rigid('pelvis'))
surface('Accessory | Graduated brass plummet',12,12,pendant,None,rigid('pelvis'),suit,metal,.001,smooth=False)
for i in (0,1):
    tube('Accessory | Plumb weight collar '+str(i+1),[(-.110,-.140,.945+i*.008),(-.110,-.140,.947+i*.008)],[(.012,.012)]*2,None,rigid('pelvis'),suit,metal)
# The removable shift follows measured horizontal sections through the body.
# A convex cloth section spans both legs below the seat and bridges the bust.
def hull2(points):
    pts=sorted(set(points))
    def half(seq):
        h=[]
        for p in seq:
            while len(h)>1:
                a,b=h[-2:]
                if (b[0]-a[0])*(p[1]-a[1])>(b[1]-a[1])*(p[0]-a[0]):break
                h.pop()
            h.append(p)
        return h
    return half(pts)[:-1]+half(pts[::-1])[:-1]
pts=xyz(body);edges=np.array([e.vertices[:] for e in body.data.edges]);A=pts[edges[:,0]];B=pts[edges[:,1]]
shift_levels=np.linspace(.626,1.279,32);shift_sections=[]
for z in shift_levels:
    cross=((A[:,2]<=z)&(B[:,2]>z))|((B[:,2]<=z)&(A[:,2]>z))
    a,b=A[cross],B[cross];cut=a+(b-a)*((z-a[:,2])/(b[:,2]-a[:,2]))[:,None]
    width=np.interp(z,[.626,.95,1.12,1.279],[.26,.24,.208,.19])
    hull=hull2([tuple(p[:2]) for p in cut if abs(p[0])<width])
    shift_sections.append(hull)
def shift(u,v):
    j=round(v*(len(shift_levels)-1));a=2*pi*u;d=Vector((sin(a),-cos(a)));c=Vector((0,-.022))
    hull=shift_sections[j];hit=0
    for p,q in zip(hull,hull[1:]+hull[:1]):
        p,q=Vector(p),Vector(q);edge=q-p;den=d.cross(edge)
        if abs(den)<1e-8:continue
        t=(p-c).cross(edge)/den;s=(p-c).cross(d)/den
        if -.00001<=s<=1.00001:hit=max(hit,t)
    radius=hit+.012+.008*(1-v)**2+.002*cos(11*a)*(1-v)
    xy=c+d*radius
    return (xy.x,xy.y,shift_levels[j])
shiftobj=surface('Underlayer | Fitted linen shift',72,31,shift,'Clay',c=under)
top_loop=[shift(i/72,1) for i in range(73)]
def shoulderstrap(u,v,side):
    x=side*(.081+.026*(u-.5))
    ys=[a[1]+(b[1]-a[1])*(x-a[0])/(b[0]-a[0]) for a,b in zip(top_loop,top_loop[1:])
        if min(a[0],b[0])<=x<max(a[0],b[0])]
    y=min(ys)-.002+(max(ys)-min(ys)+.004)*v
    hit=face_tree.ray_cast(Vector((x,y,1.49)),Vector((0,0,-1)))[0]
    z=max(1.259,min(1.442,hit.z+.008)) if hit else 1.259
    # The ends are sewn into the bandeau at its front and rear edges.
    if v<.04:z=1.27+(z-1.27)*v/.04
    if v>.96:z=1.27+(z-1.27)*(1-v)/.04
    ptside=Vector((x,y,z));return ptside
shiftparts=[shiftobj]
for side,sign in [('left',1),('right',-1)]:
    shiftparts.append(surface('Underlayer | Linen strap '+side,5,32,lambda u,v,s=sign:shoulderstrap(u,v,s),'Flax',rigid('spine_03'),c=under,flip=sign<0))
shiftobj=join(shiftparts,'Underlayer | Fitted linen shift',under)
# Retain the exact full upper surface outside the garment. The complimentary
# section exports for restoration and is switched off in dressed inspections.
runtime=[o for o in sc.objects if o.type=='MESH' and o!=body]
for o in runtime:weights(o)
covered.hide_render=True;covered.hide_set(True)
shiftobj.hide_render=True;shiftobj.hide_set(True)
sc.unit_settings.system='METRIC';sc.unit_settings.scale_length=1
def studio_obj(name,data):
    o=bpy.data.objects.new(name,data);studio.objects.link(o);return o
cam=studio_obj('Silt portrait',bpy.data.cameras.new('Silt orthographic'));sc.camera=cam
def aim(o,pt):o.rotation_euler=(Vector(pt)-o.location).to_track_quat('-Z','Y').to_euler()
cam.location=(2.0,-6,1.85);aim(cam,(0,-.025,.86));cam.data.type='ORTHO';cam.data.ortho_scale=1.94
def lamp(name,loc,power,color,size):
    d=bpy.data.lights.new(name,'AREA');o=studio_obj(name,d);o.location=loc;d.energy=power;d.color=color;d.shape='DISK';d.size=size;aim(o,(0,0,.98));return o
lamp('Key | Parchment',(-2.4,-3.6,3.4),320,(1,.90,.81),3)
lamp('Fill | Overcast',(2,-1.5,2),156,(.77,.85,1),2.5)
lamp('Rim | Window',(.7,2.0,2.5),268,(1,.88,.72),1.8)
sc.world=bpy.data.worlds.new('Neutral portrait world');sc.world.use_nodes=True
sc.world.node_tree.nodes['Background'].inputs[0].default_value=(.27,.30,.34,1)
sc.world.node_tree.nodes['Background'].inputs[1].default_value=.38
sc.render.engine='CYCLES';sc.cycles.samples=12;sc.cycles.use_denoising=True
sc.render.film_transparent=True;sc.render.resolution_percentage=100
sc.render.resolution_x=720;sc.render.resolution_y=900;sc.render.image_settings.file_format='PNG'
sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast'
for a in list(bpy.data.actions):bpy.data.actions.remove(a)
for im in bpy.data.images:im.use_fake_user=False
for m in bpy.data.materials:m.use_fake_user=False
bpy.data.orphans_purge(do_recursive=True)
for im in bpy.data.images:
    if im.source=='FILE':
        im.pack();im.filepath='//Textures/'+Path(im.filepath).name
rig.hide_set(True);studio.hide_viewport=False
for o in studio.objects:o.hide_set(True)
for screen in bpy.data.screens:
    for ar in screen.areas:
        if ar.type=='VIEW_3D':
            sp=ar.spaces.active;sp.region_3d.view_rotation=cam.rotation_euler.to_quaternion()
            sp.region_3d.view_distance=2.85;sp.region_3d.view_location=(0,0,.86);sp.region_3d.view_perspective='ORTHO'
            sp.shading.color_type='TEXTURE';sp.overlay.show_overlays=False
bpy.ops.object.select_all(action='DESELECT');bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'DarkElfFemale.blend'),compress=True,relative_remap=False)
def worldpts(o):return np.array([list(o.matrix_world@v.co) for v in o.data.vertices])
def row(o):
    me=o.data;me.calc_loop_triangles()
    return {'triangles':len(me.loop_triangles),'materials':[m.name for m in me.materials],'groups':[g.name for g in o.vertex_groups if any(a.group==g.index and a.weight>0 for v in me.vertices for a in v.groups)],'collection':o.users_collection[0].name}
def distance(objs,target):
    trees=[BVHTree.FromPolygons([q.co for q in o.data.vertices],[p.vertices[:] for p in o.data.polygons]) for o in target]
    return min(tree.find_nearest(v.co)[3] for tree in trees for o in objs for v in o.data.vertices)
def has(s):return [o for o in runtime if s in o.name]
def tree_points(pts,objs):
    tr=[BVHTree.FromPolygons([q.co for q in o.data.vertices],[p.vertices[:] for p in o.data.polygons]) for o in objs]
    return min(t.find_nearest(Vector(p))[3] for p in pts for t in tr)
pts=xyz(body);hands=pts[(abs(pts[:,0])>.436)&(pts[:,1]<-.177)&(pts[:,2]<1.065)]
jaw=pts[(abs(pts[:,0])<.055)&(pts[:,1]<-.080)&(pts[:,2]>1.461)&(pts[:,2]<1.533)]
report={'bones':{b.name:{'parent':b.parent.name if b.parent else None,'rest':[list(r) for r in rig.matrix_world@b.matrix_local]} for b in rig.data.bones},
 'meshes':{o.name:row(o) for o in runtime},'barefoot_m':float(np.ptp(pts[:,2])),'source_crown_to_sole_m':float(np.ptp(basepts[:,2])),
 'floor_z_m':float(min(worldpts(o)[:,2].min() for o in runtime if o!=covered)),'hem_min_m':float(min(worldpts(o)[:,2].min() for o in has('Outer wrap front')+has('Left skirt')+has('Joined back')+has('Inside wrap front'))),
 'cuff_to_hand_m':tree_points(hands,has('Turned flax')),'collar_to_jaw_m':tree_points(jaw,has('Open bound collar')),
 'braid_to_garment_m':distance(has('Braid strand'),[o for o in suit.objects if o.type=='MESH']),
 'body_min_z_m':float(worldpts(body)[:,2].min()),'dressed_max_z_m':float(max(worldpts(o)[:,2].max() for o in runtime if o!=covered))}
(R/'Native-bind.json').write_text(json.dumps(report,indent=2))
pattern=['Robe | Outer wrap front','Robe | Left skirt and side','Robe | Joined back pleat','Robe | Inside wrap front',
         'Robe | Tapered sleeve l','Robe | Turned flax cuff l','Robe | Shaped shoulder yoke','Robe | Bound diagonal placket',
         'Robe | Double turn sash','Lining | Clay slit inset']
stations={}
for name in pattern:
    me=bpy.data.objects[name].data;table=defaultdict(dict)
    for poly in list(me.polygons)[:len(me.polygons)//2]:
        for li in poly.loop_indices:
            u,v=me.uv_layers[0].data[li].uv
            table[round(v,5)].setdefault(round(u,5),me.vertices[me.loops[li].vertex_index].co.copy())
    rows=[]
    for v,samples in sorted(table.items()):
        coords=[p for _,p in sorted(samples.items())]
        if len(coords)>2:
            rows.append([v,sum((a-b).length for a,b in zip(coords,coords[1:])),list(coords[0]),list(coords[-1])])
    stations[name]=rows
(OUT/'Paint/Cut-stations.json').write_text(json.dumps(stations,indent=1))
rig.hide_set(False);rig.select_set(True);bpy.context.view_layer.objects.active=rig
for o in runtime:o.hide_set(False);o.hide_render=False;o.select_set(True)
bpy.ops.export_scene.fbx(filepath=str(OUT/'DarkElfFemale.fbx'),use_selection=True,object_types={'ARMATURE','MESH'},add_leaf_bones=False,use_armature_deform_only=True,bake_anim=False,use_mesh_modifiers=False,axis_forward='-Z',axis_up='Y',apply_scale_options='FBX_SCALE_UNITS',use_triangles=True,path_mode='RELATIVE')
print('SILT FINISHED',len(runtime),report['barefoot_m'],flush=True)
