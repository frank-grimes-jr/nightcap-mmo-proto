"""Fit the Vesper Moth warlock regalia to the saved Nightcap female bind."""
from pathlib import Path
import bpy, bmesh, json, math, shutil, sys
from math import sin,cos,pi
from mathutils import Vector
from mathutils.bvhtree import BVHTree

P=Path(__file__).resolve().parents[1];BASE=P/'output/dark-elf-female/silt-reader'
OUT=BASE.parent/'vesper-moth';T=OUT/'Textures';R=OUT/'Review'
bpy.ops.wm.open_mainfile(filepath=str(BASE/'DarkElfFemale.blend'))
sc=bpy.context.scene;rig=bpy.data.objects['Female_GameRig'];suit=bpy.data.collections['05  Silt Reader ensemble']
suit.name='05  Vesper Moth regalia'
for o in list(suit.objects):
    if any(s in o.name for s in ['Accessory |','placket','selvage','Sash keeper','Folded sash','Cuff woven line']):
        bpy.data.objects.remove(o,do_unlink=True)
for im in bpy.data.images:
    if im.source!='FILE' or not im.users:continue
    if 'SiltReader-BaseColor' in im.name:continue
    src=BASE/'Textures'/im.name
    if src.is_file():shutil.copy2(src,T/src.name)
def linear(h):
    c=[int(h[k:k+2],16)/255 for k in (0,2,4)]
    return tuple(((v+.055)/1.055)**2.4 if v>.04045 else v/12.92 for v in c)+(1,)
def material(name,color,rough,metal=0,texture=None,emission=0):
    m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=linear(color)
    bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=m.diffuse_color
    bs.inputs['Roughness'].default_value=rough;bs.inputs['Metallic'].default_value=metal
    if emission:bs.inputs['Emission Color'].default_value=m.diffuse_color;bs.inputs['Emission Strength'].default_value=emission
    if texture:
        n=m.node_tree.nodes.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(T/texture),check_existing=True)
        m.node_tree.links.new(n.outputs['Color'],bs.inputs['Base Color'])
    return m
old=bpy.data.materials['Silt | Dyed cloth']
cloth=material('Vesper | Figured blackberry silk','422338',.75,texture='Vesper-Brocade.png')
old.user_remap(cloth)
orph=material('Vesper | Goldwork on velvet','64344c',.79,texture='Vesper-Orphrey.png')
gold=material('Vesper | Chased old gold','c39862',.35,.69)
bronze=material('Vesper | Shadow bronze','684a49',.40,.62)
enamel=material('Vesper | Mulberry enamel','582843',.32,.47)
jet=material('Vesper | Black horn','342b3d',.35,.26)
jade=material('Vesper | Witchglass','299e88',.22,.32,emission=.16)
glass_shadow=material('Vesper | Cut teal facets','176c69',.27,.36)
lining=material('Vesper | Pomegranate lining','802c4c',.70)
V=Vector
def weights_skirt(p):
    side='l' if p.x>=0 else 'r'
    w=min(.86,max(0,(.97-p.z)/.53))*min(1,abs(p.x)/.08)
    return {'pelvis':1-w,'thigh_'+side:w}
def train_weights(p):
    upper=max(0,min(1,(p.z-1.04)/.17))
    return {**{n:w*(1-upper) for n,w in weights_skirt(p).items()},'spine_03':upper}
def rigid(n):return lambda p:{n:1}
class Piece:
    def __init__(self,name,weight):
        self.name=name;self.weight=weight;self.pts=[];self.faces=[];self.mats=[];self.rows=[];self.uv=[]
    def vertex(self,p,uv=(.5,.5)):
        self.pts.append(V(p));self.uv.append(uv);return len(self.pts)-1
    def face(self,indices,mat,smooth=False):
        if mat not in self.mats:self.mats.append(mat)
        self.faces.append(tuple(indices));self.rows.append((self.mats.index(mat),smooth))
    def grid(self,nu,nv,fn,mat,uvfn=lambda u,v:(u,v),thick=None):
        grids=[]
        for back in range(2 if thick else 1):
            g=[]
            for j in range(nv+1):
                row=[]
                for i in range(nu+1):
                    u=i/nu;v=j/nv;p=V(fn(u,v))
                    if back:p+=V(thick(u,v))
                    row.append(self.vertex(p,uvfn(u,v)))
                g.append(row)
            grids.append(g)
            for j in range(nv):
                for i in range(nu):
                    f=(g[j][i],g[j][i+1],g[j+1][i+1],g[j+1][i])
                    self.face(f[::-1] if back else f,lining if back else mat,True)
        if thick:
            def rim(g):return g[0][:-1]+[r[-1] for r in g[:-1]]+g[-1][:0:-1]+[r[0] for r in g[:0:-1]]
            a,b=map(rim,grids)
            for i in range(len(a)):self.face((a[i-1],b[i-1],b[i],a[i]),gold)
    def tube(self,points,radii,mat,n=8,smooth=True,ratio=1):
        ps=list(map(V,points));rings=[]
        for i,(p,r) in enumerate(zip(ps,radii)):
            tangent=(ps[min(i+1,len(ps)-1)]-ps[max(0,i-1)]).normalized()
            ref=V((0,1,0)) if abs(tangent.y)<.92 else V((0,0,1))
            a=tangent.cross(ref).normalized();b=tangent.cross(a).normalized()
            rings.append([self.vertex(p+r*(a*cos(j*2*pi/n)+b*ratio*sin(j*2*pi/n)),(j/n,i/(len(ps)-1))) for j in range(n)])
        self.face(rings[0][::-1],mat)
        for lo,hi in zip(rings,rings[1:]):
            for i in range(n):self.face((lo[i-1],lo[i],hi[i],hi[i-1]),mat,smooth)
        self.face(rings[-1],mat)
    def line(self,pts,r,m=gold,n=6):self.tube(pts,[r]*len(pts),m,n)
    def gem(self,center,width,height,depth,normal,mat=jade):
        c=V(center);normal=V(normal).normalized()
        h=(V((0,0,1))-normal*normal.z).normalized();right=h.cross(normal).normalized();rings=[]
        for scale,offset in [(1.18,-.003),(1.16,0),(1,.003),(.95,.004),(.54,depth)]:
            rings.append([self.vertex(c+right*(width*scale*sin(j*pi/4))+h*(height*scale*cos(j*pi/4))+normal*offset) for j in range(8)])
        self.face(rings[0][::-1],bronze)
        for k,(lo,hi) in enumerate(zip(rings,rings[1:])):
            for i in range(8):
                face_mat=glass_shadow if k==3 and i in (1,2,6) and mat==jade else [bronze,gold,jet,mat][k]
                self.face((lo[i-1],lo[i],hi[i],hi[i-1]),face_mat)
        self.face(rings[-1],mat)
        if mat==jade and width>.016:
            crown=c+normal*(depth+.0004)
            slit=[self.vertex(crown+h*y*height+right*x*width) for x,y in [(0,.40),(.105,.05),(.075,-.14),(0,-.41),(-.105,-.04),(-.07,.18)]]
            self.face(slit,jet)
    def finish(self):
        me=bpy.data.meshes.new(self.name);me.from_pydata(self.pts,[],self.faces);me.update()
        obj=bpy.data.objects.new(self.name,me);suit.objects.link(obj)
        for m in self.mats:me.materials.append(m)
        uv=me.uv_layers.new(name='UV0')
        for poly,(idx,smooth) in zip(me.polygons,self.rows):
            poly.material_index=idx;poly.use_smooth=smooth
            for li in poly.loop_indices:uv.data[li].uv=self.uv[me.loops[li].vertex_index]
        bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
        for v in me.vertices:
            for n,w in self.weight(v.co).items():
                if w>1e-7:(obj.vertex_groups.get(n) or obj.vertex_groups.new(name=n)).add([v.index],w,'REPLACE')
        obj.parent=rig;mod=obj.modifiers.new('Female bind','ARMATURE');mod.object=rig
        return obj
def bez(a,b,c,d,t):
    return V(a)*(1-t)**3+V(b)*3*t*(1-t)**2+V(c)*3*t*t*(1-t)+V(d)*t**3
shells=[o for o in sc.objects if o.name.startswith('Robe |') and any(n in o.name for n in ('wrap front','Left skirt','Joined back','yoke'))]
trees=[BVHTree.FromPolygons([v.co for v in o.data.vertices],[p.vertices[:] for p in o.data.polygons]) for o in shells]
inset=bpy.data.objects['Lining | Clay slit inset'];trees.append(BVHTree.FromPolygons([v.co for v in inset.data.vertices],[p.vertices[:] for p in inset.data.polygons]))
def shell(angle,z,stand):
    d=V((sin(angle),-cos(angle),0));ctr=V((0,-.018,z))
    hits=[t.ray_cast(ctr+.5*d,-d)[0] for t in trees]
    rad=max([float((p-ctr).dot(d)) for p in hits if p is not None]+[.059])
    return ctr+d*(rad+stand)
spans=[(0,704),(704,1296),(1296,1744),(1744,2048)]
def uvbed(k,u,v):
    x,X=spans[k];return ((x+16+(X-x-32)*u)/2048,(16+2016*v)/2048)
# Four panels hang free of the skirt, with a separate crimson underside.
for name,angle,lo,hi,spread,bed in [('Moth orphrey',0,.153,1.079,.52,0),('Processional train',pi,.103,1.362,.69,1),
                                     ('Left wing lappet',1.32,.51,1.068,.67,2),('Right wing lappet',-1.32,.51,1.068,.67,2)]:
    piece=Piece('Vestment | '+name,train_weights if bed==1 else weights_skirt)
    def clothpoint(u,v):
        tip=abs(2*u-1);bottom=lo+(.13 if bed<2 else .16)*tip**1.35
        z=bottom+(hi-bottom)*v
        theta=angle+(u-.5)*2*spread*(.75+.25*sin(v*pi))
        extra=.014+(.023 if bed==2 else .009)*(1-v)+.008*sin(pi*v)*cos(pi*(2*u-1))
        if bed==1:extra+=.027*sin(pi*v)
        return shell(theta,max(.133,z),extra)+V((0,0,min(0,z-.133)))
    piece.grid(18,44,clothpoint,orph,lambda u,v:uvbed(bed,u,v),lambda u,v:(-.0028*sin(angle+(u-.5)*spread*2),.0028*cos(angle+(u-.5)*spread*2),0))
    for u in (.017,.983):piece.line([clothpoint(u,j/42)+V((.0006*sin(angle),-.0006*cos(angle),0)) for j in range(43)],.00145)
    for v in (.009,):piece.line([clothpoint(j/24,v) for j in range(25)],.0019)
    piece.finish()
# Pointed cuirass courses nest over the cloth bodice and converge around the seal.
bib=Piece('Regalia | Ribbed gorget and pectoral',rigid('spine_03'))
for k in range(3):
    def breast(u,v):
        a=(u-.5)*(2.40-.16*k);d=abs(2*u-1)
        z=1.187+.053*k+.087*d**.8+.032*v+.010*sin(pi*d)
        return shell(a,z,.014+.003*k+.005*sin(pi*v))
    bib.grid(38,5,breast,enamel,thick=lambda u,v:(0,.0025,0))
    bib.line([breast(j/56,.06) for j in range(57)],.0029)
    bib.line([breast(j/56,.85) for j in range(57)],.0012,bronze)
for s in (-1,1):
    for k in range(4):
        aa=s*(.25+.21*k);z=1.301+.010*k
        bib.gem(shell(aa,z,.023),.0043,.007,.002,(sin(aa),-cos(aa),.1),gold)
jewel=shell(0,1.303,.032);bib.gem(jewel,.027,.044,.010,(0,-1,.12))
for s in (-1,1):
    path=[bez(jewel+V((s*.004,-.004,-.040)),jewel+V((s*.045,-.008,-.001)),jewel+V((s*.038,.003,.030)),jewel+V((s*.015,.004,.051)),t/18) for t in range(19)]
    bib.tube(path,[.001+.003*sin(pi*i/18) for i in range(19)],gold)
bib.finish()
# The standing collar grows from a narrow roll at the nape into two petalled peaks.
collar=Piece('Regalia | Split standing collar',rigid('spine_03'))
def neck(u,v):
    a=1.07+u*(2*pi-2.14)
    peak=math.exp(-((abs(a-pi)-1.10)/.52)**2)
    h=(.061+.077*peak)*sin(pi*u)**.46
    rx=.071+v*(.047+.022*peak);ry=.058+.065*v
    return V((rx*sin(a),-.005-ry*cos(a)+.026*v,1.412+h*v))
collar.grid(54,10,neck,enamel,thick=lambda u,v:(-.0025*sin(1.07+u*(2*pi-2.14)),.0025*cos(1.07+u*(2*pi-2.14)),0))
collar.line([neck(i/72,.995) for i in range(73)],.0023)
for k in range(1,10):
    u=k/10
    collar.line([neck(u+.019*sin(pi*j/14)*(1 if u<.5 else -1),.08+.87*j/14) for j in range(15)],.00155,bronze)
collar.finish()
# Domed enamel shoulders, scalloped gilded courses, swept outer horns and inset witchglass.
for s,side in [(1,'l'),(-1,'r')]:
    pa=Piece('Regalia | Horned reliquary '+side,rigid('upperarm_'+side))
    def dome(a,t,layer):
        width=.123+.010*layer;depth=.111+.002*layer
        x=.203+width*cos(a)*t; y=-.013+depth*sin(a)*t
        z=1.421+.025*(1-t*t)-.040*t*t-.018*layer-.021*(x-.20)/.12
        z-=.016*t**4*(.5+.5*cos(6*a+.4))**3
        return V((s*x,y,z))
    for k in (2,1,0):
        pa.grid(42,5,lambda u,v,k=k:dome(2*pi*u,.025+.975*v,k),enamel if k!=1 else jet,thick=lambda u,v:(0,0,-.004))
        pa.line([dome(2*pi*j/72,1,k)+V((0,0,.002)) for j in range(73)],.0035 if k==0 else .0027)
    for j in range(9):
        a=j*2*pi/9
        pa.line([dome(a+.12*sin(pi*t/14),.12+.81*t/14,0)+V((0,0,.002)) for t in range(15)],.0017)
    for idx,(bx,by,h,w,ox,oy) in enumerate([(.215,.022,.178,.035,.081,.024),(.269,-.004,.116,.025,.083,-.005),(.179,.065,.099,.021,.020,.035)]):
        z=1.426-(.01 if idx==1 else 0)
        path=[bez((s*bx,by,z),(s*(bx+ox*.60),by+oy*.15,z+h*.15),(s*(bx+ox*1.23),by+oy*.7,z+h*.63),(s*(bx+ox*.68),by+oy,z+h),i/22) for i in range(23)]
        sizes=[w*(1-i/22)**.79+.0005 for i in range(23)]
        pa.tube(path,sizes,jet,12,False,.82)
        for at in [0,2,4,7,10]:
            pa.tube(path[at:at+2],[sizes[at]+.0016,sizes[at+1]+.0016],gold if at<4 else bronze,12,False,.84)
        for sign in [-1,1]:
            pa.tube([p+V((s*.31*r,sign*.69*r,0)) for p,r in zip(path,sizes)],[.0004+.0018*(1-i/22) for i in range(23)],bronze,5)
    c=V((s*.223,-.138,1.373));pa.gem(c,.026,.034,.010,(s*.22,-1,.17))
    for sign in (-1,1):
        pts=[bez(c+V((s*sign*.006,0,-.043)),c+V((s*sign*.041,-.005,-.022)),c+V((s*sign*.046,.008,.019)),c+V((s*sign*.018,.008,.042)),t/16) for t in range(17)]
        pa.tube(pts,[.001+.003*sin(pi*j/16) for j in range(17)],gold)
    pa.finish()
    # A curved, lined sleeve fall opens behind the wrist and frames the hands.
    fore=Piece('Vestment | Bell fall '+side,rigid('lowerarm_'+side))
    el=rig.data.bones['lowerarm_'+side].head_local;wr=rig.data.bones['hand_'+side].head_local
    axis=(wr-el).normalized();up=(V((0,0,1))-axis*axis.z).normalized();across=axis.cross(up).normalized()
    def sleeve(u,v):
        a=2*pi*u;h=.5-.5*cos(a);p=el.lerp(wr,.34+.53*(1-v))
        r=.052+.012*(1-v)+.032*(1-v)**2*(.35+.65*h)
        return p+(up*cos(a)+across*sin(a))*r+V((0,.024,-.106))*h*h*(1-v)**2
    fore.grid(28,14,sleeve,orph,lambda u,v:uvbed(3,u,v),lambda u,v:tuple(-.002*(up*cos(2*pi*u)+across*sin(2*pi*u))))
    fore.line([sleeve(j/48,0) for j in range(49)],.0024)
    fore.line([sleeve(j/48,.91)+.0018*(up*cos(2*pi*j/48)+across*sin(2*pi*j/48)) for j in range(49)],.0022)
    for k in range(8):
        u=k/8
        fore.line([sleeve(u+.016*sin(pi*t/10),.64+.27*t/10)+.001*(up*cos(2*pi*u)+across*sin(2*pi*u)) for t in range(11)],.0014,bronze)
    fore.finish()
# Real linked gold chains terminate at the belt and brooch settings.
def chain(piece,start,control,end,count,radius):
    def pos(t):return (1-t)**2*start+2*(1-t)*t*control+t*t*end
    for i in range(count):
        t=(i+.5)/count;c=pos(t);a=(pos(t+.001)-pos(t-.001)).normalized()
        b=a.cross(V((0,1,0))).normalized()
        b=(b*.58+a.cross(b)*(.82 if i%2 else -.82)).normalized()
        hw=(pos((i+1)/count)-pos(i/count)).length*.66
        points=[c+a*(hw*cos(k*2*pi/9))+b*(radius*sin(k*2*pi/9)) for k in range(10)]
        piece.line(points,.00115,gold,4)
belt=Piece('Regalia | Waist seal and votive chains',rigid('pelvis'))
for s in (-1,1):
    for course in range(2):
        a=shell(s*.19,1.069,.024);b=shell(s*1.49,1.067,.026)
        chain(belt,a,V((s*.137,-.167,.930+.052*course)),b,19,.0031)
    for k in range(3):
        a=shell(s*(.78+k*.24),1.054,.032);end=a+V((s*.012,-.011,-(.078-.016*k)))
        chain(belt,a,(a+end)*.5+V((0,-.006,0)),end,8-k,.0023)
        belt.gem(end,.0055,.012,.003,(s*.5,-1,.1))
center=shell(0,1.067,.031);belt.gem(center,.034,.032,.009,(0,-1,.07))
for s in (-1,1):
    for j in range(3):
        p0=center+V((s*.018,0,.008-j*.007));p3=center+V((s*(.079-j*.009),.013,.034-j*.017))
        p1=p0+V((s*.020,-.006,-.006));p2=p3+V((-s*.017,-.002,-.025))
        belt.tube([bez(p0,p1,p2,p3,i/16) for i in range(17)],[.0008+.005*sin(pi*i/16) for i in range(17)],gold,7,False)
belt.finish()
back=Piece('Regalia | Back clasp and chains',rigid('spine_03'));c=shell(pi,1.338,.020)
back.gem(c,.022,.035,.008,(0,1,.05))
for s in (-1,1):
    a=V((s*.195,.065,1.377));chain(back,a,V((s*.093,.155,1.260)),c,25,.0033)
back.finish()
festoon=Piece('Regalia | Pectoral chainwork',rigid('spine_03'))
for s in (-1,1):
    start=V((s*.177,-.128,1.353));end=jewel+V((s*.017,-.002,.016))
    chain(festoon,start,V((s*.119,-.202,1.275)),end,20,.0023)
    anchor=shell(s*.55,1.332,.025)
    chain(festoon,anchor,V((s*.073,-.196,1.284)),end,12,.0019)
festoon.finish()
for im in list(bpy.data.images):
    if im.source=='FILE' and im.users:
        if (T/im.name).is_file():
            if not im.packed_file:im.pack()
            im.filepath='//Textures/'+im.name
bpy.data.orphans_purge(do_recursive=True)
runtime=[o for o in sc.objects if o.type=='MESH' and not o.name.startswith('Sculpt |')]
native=json.loads((BASE/'Review/Native-bind.json').read_text())
native={k:native[k] for k in ['bones','barefoot_m','floor_z_m','source_crown_to_sole_m']}
native['meshes']={o.name:[m.name for m in o.data.materials] for o in runtime}
(R/'Native-bind.json').write_text(json.dumps(native,indent=2))
sc.camera.data.ortho_scale=1.92;sc.render.resolution_x=820;sc.render.resolution_y=1024
sc.render.filepath='//Review/Three-quarter.png';bpy.context.preferences.filepaths.save_version=0
bpy.ops.object.select_all(action='DESELECT');bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'DarkElfFemale.blend'),compress=True,relative_remap=False)
rig.hide_set(False);rig.select_set(True);bpy.context.view_layer.objects.active=rig
for o in runtime:o.hide_set(False);o.hide_render=False;o.select_set(True)
bpy.ops.export_scene.fbx(filepath=str(OUT/'DarkElfFemale.fbx'),use_selection=True,object_types={'MESH','ARMATURE'},add_leaf_bones=False,use_armature_deform_only=True,bake_anim=False,use_mesh_modifiers=False,axis_forward='-Z',axis_up='Y',apply_scale_options='FBX_SCALE_UNITS',use_triangles=True,path_mode='RELATIVE')
print('VESPER EXPORT',len(runtime),flush=True)
