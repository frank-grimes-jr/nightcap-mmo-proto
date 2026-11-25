"""Tailor the Ebb Cantor from the Nightcap female base, using just the body and rest joints."""
from pathlib import Path
import json, math, shutil
from math import sin,cos,pi,exp
import bpy,bmesh,numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

P=Path(__file__).resolve().parents[1];BASE=P/'output/dark-elf-female/silt-reader';OUT=BASE.parent/'ebb-cantor'
T=OUT/'Textures';R=OUT/'Review';V=Vector
bpy.ops.wm.open_mainfile(filepath=str(BASE/'DarkElfFemale.blend'))
sc=bpy.context.scene;rig=bpy.data.objects['Female_GameRig'];suit=bpy.data.collections['05  Silt Reader ensemble']
for obj in list(suit.objects)+[o for o in sc.objects if o.name.startswith('Lining |')]:
    bpy.data.objects.remove(obj,do_unlink=True)
assert not len(suit.objects)
suit.name='05  Ebb Cantor robes'
for filename in ('Indigo-Skin.png','Copper-Iris.png','Auricle.png','Ivory-Locks.png'):
    shutil.copy2(BASE/'Textures'/filename,T/filename)
def mat(name,color,rough,metal=0,texture=None,glow=0):
    rgb=[int(color[i:i+2],16)/255 for i in (0,2,4)]
    rgba=tuple(((x+.055)/1.055)**2.4 if x>.04045 else x/12.92 for x in rgb)+(1,)
    m=bpy.data.materials.new('Cantor | '+name);m.use_nodes=True;m.diffuse_color=rgba
    bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=rgba
    bs.inputs['Roughness'].default_value=rough;bs.inputs['Metallic'].default_value=metal
    if glow:bs.inputs['Emission Color'].default_value=rgba;bs.inputs['Emission Strength'].default_value=glow
    if texture:
        n=m.node_tree.nodes.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(T/texture));m.node_tree.links.new(n.outputs[0],bs.inputs['Base Color'])
    return m
main=mat('Wool and resist print','294448',.88,texture='Ebb-Procession.png')
pall=mat('Pall and dike chart','c4b79a',.86,texture='Ebb-Pall.png')
madder=mat('Madder binding','82422e',.77);ash=mat('Flax cord','b8a786',.90)
dark=mat('Pitch-soaked reed','303d3b',.73);pot=mat('Smoke fired clay','ab6b48',.66)
slip=mat('Chalk slip','c7ae89',.62);copper=mat('Rubbed copper','99715b',.48,.45)
fired=mat('Cut slip and firing clouds','965b42',.71,texture='Ebb-Stoneware.png')
echo=mat('Condensed breath','8fb9ad',.36,glow=.12);wax=mat('Sealing wax','763b32',.43)
bpy.data.materials['Silt | Dyed cloth'].user_remap(main)
def rigid(name):return lambda p:{name:1}
def torso(p):
    a=float(np.clip((p.z-1.035)/.22,0,1));return {'pelvis':1-a,'spine_03':a}
def garment(p):
    if p.z>1.03:return torso(p)
    w=min(.89,max(0,(.94-p.z)/.55))*min(1,abs(p.x)/.075)
    return {'pelvis':1-w,('thigh_l' if p.x>=0 else 'thigh_r'):w}
def uv(box,u,v):
    l,t,r,b=box;return ((l+(r-l)*u)/2048,1-(b-(b-t)*v)/2048)
class Pattern:
    def __init__(self,name,weight):
        self.name=name;self.weight=weight;self.v=[];self.uv=[];self.faces=[];self.materials=[];self.codes=[]
    def vert(self,p,tex=(.5,.5)):
        self.v.append(V(p));self.uv.append(tex);return len(self.v)-1
    def face(self,q,m,smooth=False):
        if m not in self.materials:self.materials.append(m)
        self.faces.append(q);self.codes.append((self.materials.index(m),smooth))
    def fabric(self,fn,nu,nv,m,box,offset,interior,drape=True):
        grid=[]
        for back in (False,True):
            rows=[]
            for j in range(nv+1):
                row=[]
                for i in range(nu+1):
                    u,v=i/nu,j/nv;p=V(fn(u,v))
                    if back:p+=V(offset(u,v))
                    row.append(self.vert(p,uv(box,u,v)))
                rows.append(row)
            grid.append(rows)
            for j in range(nv):
                for i in range(nu):
                    q=(rows[j][i],rows[j][i+1],rows[j+1][i+1],rows[j+1][i])
                    self.face(q[::-1] if back else q,interior if back else m,drape)
        def perimeter(g):return g[0][:-1]+[r[-1] for r in g[:-1]]+g[-1][:0:-1]+[r[0] for r in g[:0:-1]]
        a,b=map(perimeter,grid)
        for i in range(len(a)):self.face((a[i-1],b[i-1],b[i],a[i]),interior)
    def tube(self,points,radii,m,sides=8,ratio=1):
        pts=list(map(V,points));rings=[]
        for j,(p,r) in enumerate(zip(pts,radii)):
            d=(pts[min(len(pts)-1,j+1)]-pts[max(0,j-1)]).normalized()
            a=d.cross(V((0,1,0)) if abs(d.y)<.9 else V((0,0,1))).normalized();b=d.cross(a).normalized()
            rings.append([self.vert(p+r*(a*cos(i*2*pi/sides)+ratio*b*sin(i*2*pi/sides))) for i in range(sides)])
        self.face(rings[0][::-1],m)
        for lo,hi in zip(rings,rings[1:]):
            for i in range(sides):self.face((lo[i-1],lo[i],hi[i],hi[i-1]),m,True)
        self.face(rings[-1],m)
    def cord(self,points,r,m=ash,sides=6):self.tube(points,[r]*len(points),m,sides)
    def finish(self):
        mesh=bpy.data.meshes.new(self.name);mesh.from_pydata(self.v,[],self.faces);mesh.update()
        obj=bpy.data.objects.new(self.name,mesh);suit.objects.link(obj)
        for m in self.materials:mesh.materials.append(m)
        chart=mesh.uv_layers.new(name='UV0')
        for f,(m,smooth) in zip(mesh.polygons,self.codes):
            f.material_index=m;f.use_smooth=smooth
            for i in f.loop_indices:chart.data[i].uv=self.uv[mesh.loops[i].vertex_index]
        bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free()
        for v in mesh.vertices:
            weights=self.weight(v.co);total=sum(weights.values())
            for name,w in weights.items():
                if w>1e-8:(obj.vertex_groups.get(name) or obj.vertex_groups.new(name=name)).add([v.index],w/total,'REPLACE')
        obj.parent=rig;obj.modifiers.new('Female bind','ARMATURE').object=rig
        return obj
def interp(z,rows):return [float(np.interp(z,[r[0] for r in rows],[r[i] for r in rows])) for i in range(1,len(rows[0]))]
stations=[(.10,.306,.196,-.019),(.21,.300,.195,-.019),(.52,.259,.167,-.016),(.76,.217,.148,-.014),
          (.9,.202,.148,-.013),(1.035,.147,.118,-.019),(1.10,.144,.121,-.02),(1.22,.183,.158,-.029),
          (1.294,.184,.133,-.017),(1.349,.187,.109,-.009),(1.375,.143,.091,-.009),(1.40,.076,.073,-.010),(1.429,.057,.057,-.012)]
def outside(a,z,gap=0):
    rx,ry,cy=interp(z,stations);lo=max(0,min(1,(1.03-z)/.75))
    fold=(.003+.013*lo)*(.73*cos(8*a-.65*z)+.39*cos(13*a+.9*z)+.29*sin(5*a))
    return V(((rx+fold+gap)*sin(a),cy-(ry+fold+gap)*cos(a),z))
def inward(a,w=.0025):return (-w*sin(a),w*cos(a),0)
def hem(a):return .127+.029*sin(a+.58)+.010*cos(3*a-.3)
# The undergown opens at the left rear. Its print crosses each actual panel seam.
start=-pi+.48
for i in range(4):
    piece=Pattern('Habit | '+['West breadth','Funeral road front','East breadth','Joined back'][i],garment)
    def body(u,v):
        a=start+(i+u)*pi/2;z=hem(a)+(1.426-hem(a))*v
        return outside(a,z)
    piece.fabric(body,22,39,main,(8+i*508,16,8+(i+1)*508,1489),lambda u,v:inward(start+(i+u)*pi/2),dark)
    piece.finish()
for s,side in [(1,'l'),(-1,'r')]:
    shoulder,el,wr=[rig.data.bones[n+'_'+side].head_local.copy() for n in ('upperarm','lowerarm','hand')]
    def arm(p):
        t=float(np.clip(.5+(p-el).dot((wr-shoulder).normalized())/.14,0,1))
        return {'upperarm_'+side:1-t,'lowerarm_'+side:t}
    sleeve=Pattern('Habit | Cut sleeve '+side,arm)
    path=[shoulder+V((-.056*s,0,.010)),shoulder+V((-.019*s,0,.016)),shoulder.lerp(el,.16),
          shoulder.lerp(el,.40),shoulder.lerp(el,.79),el,el.lerp(wr,.22),el.lerp(wr,.48),el.lerp(wr,.72),el.lerp(wr,.91)]
    sizes=[.034,.062,.081,.069,.060,.063,.061,.055,.050,.043]
    def armring(u,v,thickness=0):
        t=v*(len(path)-1);i=min(len(path)-2,int(t));alpha=t-i
        p=path[i].lerp(path[i+1],alpha);d=(path[min(i+2,len(path)-1)]-path[max(i-1,0)]).normalized()
        axis=d.cross(V((0,1,0))).normalized();b=d.cross(axis).normalized();a=2*pi*u
        radius=sizes[i]*(1-alpha)+sizes[i+1]*alpha+thickness+.002*sin(8*a+5*v)
        return p+(axis*cos(a)+b*sin(a))*radius
    sleeve.fabric(armring,26,24,main,(15,1532,979,2027),lambda u,v:armring(u,v,-.002)-armring(u,v),dark)
    for k in range(5 if s<0 else 2):
        sleeve.cord([armring(j/36,.60+.063*k+.024*j/36,.002) for j in range(37)],.0021,ash if k%3==0 else madder)
    sleeve.finish()
# The madder chart wraps the left hip, overlapping at the back and cutting across the knees.
skirt=Pattern('Habit | Madder sounding chart',garment)
def apron(u,v):
    a=-1.19+u*5.12
    bottom=.344+.237*(.5+.5*cos(a+1.13))+.036*cos(2*a-.8)
    z=bottom+(1.076-bottom)*v
    return outside(a,z,.010+.013*(1-v)+.008*sin(pi*v)*cos(a*7))
skirt.fabric(apron,69,24,pall,(1138,22,2028,2026),lambda u,v:inward(-1.19+u*5.12),madder)
for v in (.009,.029):
    skirt.cord([apron(j/86,v)+V((0,0,.0008)) for j in range(87)],.00165,ash if v<.02 else dark)
skirt.finish()
# Crescent of folded linen. Pleats start close at the neck and open into a deep
# folded edge over the left arm. The two ends land at the opposite hip.
def cape_weight(p):
    mix=float(np.clip((p.x-.115)/.26,0,.70))*float(np.clip((1.47-p.z)/.16,0,1))
    return {**{n:w*(1-mix) for n,w in torso(p).items()},'upperarm_l':mix}
supports=[BVHTree.FromPolygons([v.co for v in o.data.vertices],[f.vertices[:] for f in o.data.polygons])
          for o in suit.objects if o.name.startswith('Habit |') and 'chart' not in o.name]
def fan(u,v):
    a=-.94+u*5.06; side=max(0,sin(a))
    lower=1.066+.215*side+.060*(1-side)*sin(pi*u)**.75
    pleat=1-4*abs((u*17+.1)%1-.5)
    crown=1.412+.020*side
    z=np.interp(v,[0,.18,.57,.82,1],[lower,lower+.047,lower+.66*(crown-lower),crown-.012,crown])
    rx,ry,cy=interp(z,stations)
    # Arm clearance moves rapidly outward after crossing the shoulder top.
    rx+=side*np.interp(v,[0,.28,.6,.82,1],[.164,.138,.095,.054,.0])
    ry+=.010+.006*sin(pi*v)
    stand=(.008+.015*(1-v))*pleat*(.28+.72*sin(pi*u)**.6)
    p=V(((rx+stand+.009)*sin(a),cy-(ry+stand+.005)*cos(a),z+.008*(1-v)*pleat))
    if p.x>.042 and p.z>1.305:
        values=[tree.ray_cast(V((p.x,p.y,1.49)),V((0,0,-1)))[0] for tree in supports]
        p.z=max([p.z]+[q.z+.0055 for q in values if q is not None])
    return p
fancloth=Pattern('Pall | Seventeen gathered folds',cape_weight)
fancloth.fabric(fan,136,22,pall,(15,18,1103,2027),lambda u,v:inward(-.94+5.06*u,.002),ash,False)
for v in (.998,.024):
    fancloth.cord([fan(j/136,v) for j in range(137)],.0023,madder if v>.5 else dark)
fancloth.finish()
# The fastening is a pierced weaver's shuttle. Two rails bridge the folds and
# five copper crosspins carry the actual red lacing through the open slots.
shuttle=Pattern('Pall | Pierced reed shuttle',rigid('spine_03'))
def pin(t,w,lift=0):
    u=.180+.215*t;v=.655+.175*t+w;a=-.94+u*5.06
    return fan(u,v)+V((sin(a),-cos(a),.30))*(.009+lift)
for w in (-.018,.018):
    path=[pin(t/28,w) for t in range(29)]
    shuttle.tube(path,[.0016+.0024*sin(pi*t/28)**.65 for t in range(29)],dark,8)
for j in range(7):
    t=.035+.155*j
    if t>1:continue
    shuttle.cord([pin(t,-.017),pin(t,.018)],.0022,copper)
    if j in (1,2,4,5):
        shuttle.cord([pin(t-.018,-.029,-.004),pin(t-.012,-.009,.002),pin(t+.014,.018,.002),pin(t+.019,.031,-.008)],.0024,madder)
shuttle.finish()
# Belly band, a three-strand cord and one knotted turn round the ceramic rack.
waist=Pattern('Binding | Reed band and ferry knot',rigid('pelvis'))
def girdle(u,v):
    a=2*pi*u;z=1.047+.054*v+.011*sin(a-.3)
    return outside(a,z,.022+.003*sin(pi*v))
waist.fabric(girdle,68,6,main,(1006,1530,1469,2019),lambda u,v:inward(2*pi*u),dark)
for k in range(3):
    p=[]
    for j in range(193):
        a=2*pi*j/192;z=1.073+.011*sin(a-.3)+.005*sin(a*19+k*2*pi/3)
        p.append(outside(a,z,.027+.003*cos(a*19+k*2*pi/3)))
    waist.cord(p,.0033,ash if k!=1 else madder)
anchor=outside(-.91,1.076,.036)
kn=[]
for j in range(65):
    t=j*2*pi/64
    kn.append(anchor+V((.026*sin(t),-.007*cos(2*t),.013*sin(2*t))))
waist.cord(kn,.0038,ash);waist.finish()
# One reed rack supports three clay vessels. Each vessel is a closed lathed wall
# with an interior bowl, a visible aperture, thumb grooves, and off-axis handles.
rack=Pattern('Voices | Reed rack and cords',rigid('pelvis'))
def rod(a,b,r,m):rack.cord([a,b],r,m,9)
vessels=[(-.184,-.122,.929,.050,.091),(-.229,-.060,.889,.041,.073),(-.239,.015,.860,.035,.060)]
mounts=[V((x+.019,y+.034,z+h*.51)) for x,y,z,r,h in vessels]
rack.cord([mounts[0]+V((.020,-.025,.014)),*mounts,mounts[-1]+V((.006,.03,-.006))],.009,dark,10)
for i,(x,y,z,r,h) in enumerate(vessels):
    for s in [-1,1]:
        anchor=outside(-.94-i*.32+s*.065,1.086,.027)
        end=V((x+s*r*.67,y-.007,z+h*.39))
        rack.cord([anchor,anchor.lerp(end,.35)+V((-.009,-.006,0)),anchor.lerp(end,.70)+V((-.011,-.003,0)),end],.0027,ash)
    jar=Pattern('Voices | '+['Open throat','Wax-stopped throat','Small witness'][i],rigid('pelvis'))
    center=V((x,y,z));axis=V((-.13,-.24,1)).normalized();ex=V((1,0,0));ex=(ex-axis*ex.dot(axis)).normalized();ey=axis.cross(ex)
    def ringpoint(a,rad,ht):
        return center+axis*(ht*h)+(ex*cos(a)+ey*sin(a))*(r*rad*(1+.027*sin(5*a+.4*i)))
    profile=[(.02,-1),(.43,-.91),(.78,-.65),(1.0,-.18),(.95,.22),(.76,.48),(.42,.62),(.40,.82),(.51,.86),(.50,.98),(.35,1),(.32,.88),(.31,.64),(.51,.42),(.58,.03),(.02,-.25)]
    rings=[]
    for r0,z0 in profile:
        rings.append([jar.vert(ringpoint(2*pi*j/38+(0,.31,.605)[i]*2*pi,r0,z0),(j/38,(z0+1)/2)) for j in range(39)])
    jar.face(rings[0][:-1][::-1],pot)
    for n,(lo,hi) in enumerate(zip(rings,rings[1:])):
        m=dark if n>=11 else slip if n in (8,9) else fired
        for j in range(38):jar.face((lo[j],lo[j+1],hi[j+1],hi[j]),m,True)
    jar.face(rings[-1][:-1],dark)
    for s in [-1,1]:
        pts=[ringpoint(0 if s>0 else pi,.57+.44*sin(pi*t/12),.60-.43*t/12) for t in range(13)]
        jar.cord(pts,.0045,pot)
    for k in range(2):
        jar.cord([ringpoint(j*2*pi/48,.953+.025*k,-.32+k*.07+.019*sin(j*pi/12+i)) for j in range(49)],.0013,dark)
    if i:
        jar.tube([center+axis*h*.90,center+axis*h*1.035,center+axis*h*1.06],[r*.35,r*.39,r*.30],wax,16)
    jar.finish()
rack.finish()
# In the open throat a drowned voice gathers into an ear, mouth and bowed brow.
# A narrow rising ribbon curls back into the aperture below the chin.
voice=Pattern('Voices | Breath above the open throat',rigid('pelvis'))
c=V((-.196,-.144,1.016))
def stream(t):
    return c+V((-.028*t-.009*sin(t*pi*2),-.019*t-.009*sin(t*pi),.076*t))
path=[stream(t) for t in np.linspace(0,1,24)]
voice.tube(path,[.0012+.0046*sin(pi*j/23)**1.35+.0025*j/23 for j in range(24)],echo,10,.66)
for phase in (0,pi):
    path=[]
    for j in range(25):
        t=j/24;r=.008*sin(pi*t)**.8
        path.append(stream(t)+V((r*cos(2*pi*t+phase),r*sin(2*pi*t+phase),0)))
    voice.tube(path,[.00045+.00065*sin(pi*j/24) for j in range(25)],echo,5)
# A thumbnail-sized modeled death mask, with a forehead, closed lids, a nose
# and parted lips. Its throat tapers back into the water filament.
origin=stream(1)-V((0,0,.004))
sections=[(0,.003,.005),(.008,.008,.009),(.015,.012,.015),(.019,.016,.015),(.023,.018,.017),
          (.028,.020,.018),(.033,.021,.018),(.037,.021,.018),(.043,.022,.020),(.050,.020,.021),(.056,.016,.016),(.061,.008,.009),(.063,.001,.002)]
def maskpoint(a,z,rx,ry):
    f=cos(a);x=rx*sin(a);nose=.008*exp(-((z-.032)/.005)**2)*exp(-(x/.004)**2)*max(0,f)**5
    brow=.0024*exp(-((z-.040)/.0026)**2)*max(0,f)**5
    lip=.0025*exp(-((z-.023)/.0028)**2)*exp(-(x/.010)**2)*max(0,f)**5
    return origin+V((x-.11*z,-ry*f-nose-brow-lip-.1*z,z))
# Only the face caught by each ripple condenses. The missing bands let the
# cloth behind show through the lids and the open mouth.
for z0,z1,arc in [(.001,.019,2.05),(.020,.024,1.72),(.026,.037,1.60),(.039,.049,1.63),(.051,.056,1.21)]:
    def water(u,v):
        a=(u-.5)*arc*2;z=z0+(z1-z0)*v+.0016*sin(a*1.8)
        rx,ry=interp(z,sections)
        return maskpoint(a,z,rx,ry)
    voice.fabric(water,22,4,echo,(0,0,1,1),lambda u,v:(.0001,.0016,0),echo)
for side in (-1,1):
    path=[]
    for z,rx,ry in sections[:-1]:
        path.append(maskpoint(side*(1.30+.41*sin(40*z)),z,rx,ry))
    voice.tube(path,[.0008+.0009*sin(pi*j/(len(path)-1)) for j in range(len(path))],echo,6)
voice.finish()
# Hollow name slips are tied through the edge of the pall. Each has a different tally.
tags=Pattern('Pall | Fired name slips',cape_weight)
for i,u in enumerate((.075,.13,.24,.46,.53,.66,.73,.82,.87,.92)):
    a=-.94+5.06*u;d=V((sin(a),-cos(a),0));side=V((cos(a),sin(a),0))
    anchor=fan(u,.012)+d*.002;size=.018+.009*(i%3)
    center=anchor+d*.005+V((0,0,-size*.85))
    tags.cord([anchor,center+V((0,0,size*.2))],.0015,madder)
    coords=[(-.007,.45),(.007,.45),(.009,-.32),(.004,-.52),(-.006,-.49)]
    front=[tags.vert(center+side*x+V((0,0,z*size))+d*.0017) for x,z in coords]
    back=[tags.vert(center+side*x+V((0,0,z*size))-d*.0017) for x,z in coords]
    tags.face(front,slip);tags.face(back[::-1],pot)
    for j in range(5):tags.face((front[j-1],back[j-1],back[j],front[j]),pot)
    for j in range(1+i%3):
        p=center+d*.0022+V((0,0,(j-1)*.004))
        tags.cord([p-side*.004,p+side*.003+V((0,0,.002))],.00065,dark,4)
tags.finish()
bpy.data.orphans_purge(do_recursive=True)
for im in bpy.data.images:
    if im.source=='FILE' and im.users:
        assert (T/im.name).is_file(),im.name
        if not im.packed_file:im.pack()
        im.filepath='//Textures/'+im.name
runtime=[o for o in sc.objects if o.type=='MESH' and not o.name.startswith('Sculpt |')]
baseline=json.loads((BASE/'Review/Native-bind.json').read_text())
report={k:baseline[k] for k in ('bones','barefoot_m','floor_z_m','source_crown_to_sole_m')}
report['meshes']={o.name:[m.name for m in o.data.materials] for o in runtime}
report['new_costume_meshes']=[o.name for o in suit.objects]
report['minimum_outer_hem_m']=min(v.co.z for o in suit.objects if 'breadth' in o.name or 'Funeral road' in o.name or 'Joined back' in o.name for v in o.data.vertices)
(R/'Native-bind.json').write_text(json.dumps(report,indent=2))
cam=sc.camera;cam.location=(-1.5,-5,1.38);cam.rotation_euler=(V((0,-.033,.86))-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.ortho_scale=1.89;sc.render.filepath='//Review/Three-quarter.png';sc.render.resolution_x=780;sc.render.resolution_y=990
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':area.spaces.active.region_3d.view_rotation=cam.rotation_euler.to_quaternion()
bpy.context.preferences.filepaths.save_version=0;bpy.ops.object.select_all(action='DESELECT')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'DarkElfFemale.blend'),compress=True,relative_remap=False)
rig.hide_set(False);rig.select_set(True);bpy.context.view_layer.objects.active=rig
for o in runtime:o.hide_set(False);o.hide_render=False;o.select_set(True)
bpy.ops.export_scene.fbx(filepath=str(OUT/'DarkElfFemale.fbx'),use_selection=True,object_types={'MESH','ARMATURE'},add_leaf_bones=False,use_armature_deform_only=True,bake_anim=False,use_mesh_modifiers=False,axis_forward='-Z',axis_up='Y',apply_scale_options='FBX_SCALE_UNITS',use_triangles=True,path_mode='RELATIVE')
