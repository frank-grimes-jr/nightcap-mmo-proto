"""Furnace Warden plate built in Male_GameRig rest space (metres)."""
import math
import bpy
import bmesh
from mathutils import Vector

PI = math.pi
V = Vector
TRIM, HEAT, IRON, CHAIN, QUILT, CHEST, TASSET, GREAVE, GLOVE, BACK, RIVET, DARK, BOOT = 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15

def atlas(tile, u, v):
    return ((tile % 4 + .04 + .92 * u) / 4, (3 - tile // 4 + .04 + .92 * v) / 4)

def corners(hw, hh, cut=.18):
    c = min(hw, hh) * cut
    return [(-hw+c,-hh),(hw-c,-hh),(hw,-hh+c),(hw,hh-c),
            (hw-c,hh),(-hw+c,hh),(-hw,hh-c),(-hw,-hh+c)]

class Forge:
    def __init__(self, rig, material):
        self.rig = rig
        self.material = material
        self.objects = []
        self.groups = {}
        self.group = 'Torso and Shoulders'
        self.open('Cuirass','spine_03')

    def open(self,name,bone):
        self.name, self.bone = name, bone
        self.verts, self.faces, self.uv, self.bones = [],[],[],[]

    def ring(self, points, bone=None):
        start = len(self.verts)
        self.verts.extend(V(p) for p in points)
        self.bones.extend([bone or self.bone]*len(points))
        return list(range(start,len(self.verts)))

    def face(self, ids, tile, coords=None):
        if coords is None:
            a = [self.verts[i] for i in ids]
            normal = (a[1]-a[0]).cross(a[-1]-a[0])
            axes = sorted(range(3), key=lambda k:abs(normal[k]))[:2]
            axes.sort()
            ar = [(p[axes[0]],p[axes[1]]) for p in a]
            xr = [p[0] for p in ar]; yr = [p[1] for p in ar]
            coords = [((x-min(xr))/max(max(xr)-min(xr),1.e-7),(y-min(yr))/max(max(yr)-min(yr),1.e-7)) for x,y in ar]
        self.faces.append(tuple(ids))
        self.uv.append([atlas(tile, u,v) for u,v in coords])

    def bridge(self, a,b,tile,uvrange=None):
        n=len(a)
        for i in range(n):
            j=(i+1)%n
            coords=None
            if uvrange is not None:
                lo,hi=uvrange
                coords=[(i/n,lo),((i+1)/n,lo),((i+1)/n,hi),(i/n,hi)]
            self.face((a[i],a[j],b[j],b[i]),tile[i] if isinstance(tile,list) else tile,coords)

    def finish(self):
        me=bpy.data.meshes.new(self.name)
        me.from_pydata(self.verts,[],self.faces)
        me.materials.append(self.material)
        layer=me.uv_layers.new(name='UV0')
        for poly,coords in zip(me.polygons,self.uv):
            for idx,uv in zip(poly.loop_indices,coords):
                layer.data[idx].uv=uv
        bm=bmesh.new();bm.from_mesh(me)
        bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
        bm.to_mesh(me);bm.free();me.update()
        obj=bpy.data.objects.new('Warden_'+self.name,me)
        if self.group not in self.groups:
            col=bpy.data.collections.new('Warden | '+self.group)
            bpy.context.scene.collection.children.link(col)
            self.groups[self.group]=col
        self.groups[self.group].objects.link(obj)
        obj['warden_group']=self.group
        obj.parent=self.rig
        by_name={}
        for idx,bone in enumerate(self.bones):
            if isinstance(bone,str):
                by_name.setdefault(bone,[]).append(idx)
        vgs={}
        for bone,ids in by_name.items():
            vgs[bone]=obj.vertex_groups.new(name=bone)
            vgs[bone].add(ids,1.,'REPLACE')
        for i,weights in enumerate(self.bones):
            if isinstance(weights,str):
                continue
            for name,w in weights:
                if name not in vgs:
                    vgs[name]=obj.vertex_groups.new(name=name)
                vgs[name].add([i],w,'REPLACE')
        mod=obj.modifiers.new('Male rest skeleton','ARMATURE');mod.object=self.rig
        self.objects.append(obj)
        return obj

    def plate(self, contour, center, xaxis, upaxis, normal, depth, tile, edge=TRIM, ridge=0., bevel=.09):
        """Faceted raised plate on a local plane, points ordered around the outer edge."""
        c=V(center); ex=V(xaxis); ez=V(upaxis); no=V(normal)
        mx=sum(p[0] for p in contour)/len(contour); mz=sum(p[1] for p in contour)/len(contour)
        def layer(scale,d):
            return self.ring([c+ex*(mx+(x-mx)*scale)+ez*(mz+(z-mz)*scale)+no*d for x,z in contour])
        rear=layer(.97,-depth*.52); perimeter=layer(1,depth*.12);front=layer(1-bevel,depth*.52)
        self.face(rear,DARK)
        self.bridge(rear,perimeter,IRON);self.bridge(perimeter,front,edge)
        if ridge:
            mid=self.ring([c+ex*mx+ez*mz+no*(depth*.52+ridge)])[0]
            x0=min(x for x,z in contour);x1=max(x for x,z in contour); z0=min(z for x,z in contour);z1=max(z for x,z in contour)
            uv=[((x-x0)/(x1-x0),(z-z0)/(z1-z0)) for x,z in contour]
            for i,a in enumerate(front):
                j=(i+1)%len(front)
                self.face((a,front[j],mid),tile,[uv[i],uv[j],((mx-x0)/(x1-x0),(mz-z0)/(z1-z0))])
        else:
            self.face(front,tile)

    def front(self, outline, center, depth, tile, **kw):
        self.plate(outline,center,(1,0,0),(0,0,1),(0,-1,0),depth,tile,**kw)

    def sleeve(self, start,end,rows,tile,n=10,angle=0,section=None):
        """Hollow along a joint with flared and stepped sections. x is lateral, y posterior."""
        a=V(start);d=V(end)-a;axis=d.normalized()
        side=V((1,0,0));side=(side-axis*side.dot(axis)).normalized()
        depth=side.cross(axis).normalized()
        if depth.y<0: depth.negate()
        if section is None:
            section=[(math.sin(2*PI*i/n+angle),-math.cos(2*PI*i/n+angle)) for i in range(n)]
        outer=[];inner=[]
        for t,rx,ry,*extra in rows:
            dip=extra[0] if extra else 0.
            center=a+t*d
            outer.append(self.ring([center+side*(x*rx)+depth*(y*ry)+axis*(dip*max(-y,0)**3) for x,y in section]))
        for i in range(len(outer)-1):
            bandtile=tile[i] if isinstance(tile,list) else tile
            self.bridge(outer[i],outer[i+1],bandtile,(i/(len(rows)-1),(i+1)/(len(rows)-1)))
        for k in (0,len(rows)-1):
            t,rx,ry,*ex=rows[k];dip=ex[0] if ex else 0.
            center=a+t*d
            inner.append(self.ring([center+side*(x*rx*.91)+depth*(y*ry*.91)+axis*(dip*max(-y,0)**3) for x,y in section]))
            self.bridge(outer[k],inner[-1],TRIM)
        self.bridge(inner[0],inner[1],DARK)

    def torso(self,rows,tiles,n=12):
        rings=[]
        for z,rx,ry,cy,*ex in rows:
            rings.append(self.ring([(rx*math.sin(2*PI*i/n),cy-ry*math.cos(2*PI*i/n),
                   z+(ex[0] if ex else 0.)*max(0,math.cos(2*PI*i/n))**3) for i in range(n)]))
        for k in range(len(rows)-1):
            tile=tiles[k] if isinstance(tiles,list) else tiles
            self.bridge(rings[k],rings[k+1],tile,(k/(len(rows)-1),(k+1)/(len(rows)-1)))
        # Rolled rims leave an open neck and hem.
        for k in (0,len(rings)-1):
            z,rx,ry,cy,*ex=rows[k]
            inner=self.ring([(self.verts[i].x*.96,cy+(self.verts[i].y-cy)*.96,self.verts[i].z) for i in rings[k]])
            self.bridge(inner,rings[k],TRIM)

def make_helm(f):
    f.group='Helm'
    f.open('ForgeHood','head')
    # Unequal front and rear lengths match the angled hood in the portrait.
    low=[(0,-.202,1.718),(.074,-.171,1.731),(.105,-.110,1.727),
         (.110,-.025,1.748),(.088,.046,1.729),(0,.071,1.718),
         (-.088,.046,1.729),(-.110,-.025,1.748),(-.105,-.110,1.727),(-.074,-.171,1.731)]
    mid=[(x*.97,-.048+(y+.048)*.97,z+.009) for x,y,z in low]
    top=[(x*.57,-.035+(y+.048)*.46,1.841+(.008 if y>0 else 0.)) for x,y,z in low]
    apex=[(x*.49,-.031+(y+.048)*.36,1.851+(.006 if y>0 else 0.)) for x,y,z in low]
    inner=[(x*.94,-.054+(y+.054)*.925,z+.001) for x,y,z in low]
    rims=[f.ring(row) for row in (inner,low,mid,top,apex)]
    f.bridge(rims[0],rims[1],DARK)
    f.bridge(rims[1],rims[2],TRIM,(.41,.55))
    # The portrait stencil crosses the entire front plane, including both sides
    # of the central crest. Nape and side faces unwrap as one authored cool return.
    for lower,upper in zip(rims[2:-1],rims[3:]):
        for i in range(len(low)):
            j=(i+1)%len(low)
            face=(lower[i],lower[j],upper[j],upper[i])
            if i in (8,9,0,1):
                uv=[((f.verts[k].x+.110)/.220,(f.verts[k].z-1.718)/.144) for k in face]
                f.face(face,0,uv)
            else:
                us=((i-2)/6,(i-1)/6,(i-1)/6,(i-2)/6)
                uv=[(u,(f.verts[k].z-1.718)/.144) for u,k in zip(us,face)]
                f.face(face,BACK,uv)
    f.face(rims[-1],BACK)
    f.finish()
    f.open('Visor_Grille','head')
    # Metal cavity projects beyond the nose, terminating beneath both irises.
    mask=[(-.076,.038),(-.068,-.035),(-.052,-.055),(0,-.068),(.052,-.055),(.068,-.035),(.076,.038),(.044,.052),(0,.047),(-.044,.052)]
    f.front(mask,(0,-.183,1.645),.008,DARK,edge=IRON)
    # A bowed inset sits behind all four openings and ahead of the bridge of the nose.
    xs=[-.066,-.042,-.014,.014,.042,.066]
    for xa,xb in zip(xs,xs[1:]):
        corners3=[(x,-.198+.007*(abs(x)/.066)**1.8,z+.005*abs(x)/.066)
                  for x,z in [(xa,1.587),(xb,1.587),(xb,1.688),(xa,1.688)]]
        f.face(f.ring(corners3),HEAT,[(0,0),(1,0),(1,1),(0,1)])
    for i in range(-2,3):
        x=i*.028
        h=.058-abs(i)*.0028
        profile=[(-.008,h-.003),(.002,h+.004),(.010,h-.001),(.009,-h+.007),(.001,-h-.005),(-.008,-h+.002)]
        f.front(profile,(x,-.210+.009*abs(i)/2,1.643+abs(i)*.001),.015,4,ridge=.0022,bevel=.16)
    # Wrap the grille into the jaw and leave two deliberate eye slits.
    for s in (-1,1):
        cheek=[(.058,1.692),(.072,1.711),(.091,1.718),(.094,1.682),(.080,1.624),(.065,1.607)]
        verts=[(s*x,-.194+(x-.058)*1.62,z) for x,z in cheek]
        outer=f.ring(verts); inner=f.ring([(x,y+.009,z) for x,y,z in verts])
        f.face(outer,4);f.face(inner,IRON);f.bridge(outer,inner,IRON)
        arch=[(.002,1.720),(.064,1.731),(.086,1.722),(.074,1.714),(.047,1.717),(.022,1.716),(.006,1.709)]
        verts=[(s*x,-.198+.031*(x/.086)**1.5,z) for x,z in arch]
        outer=f.ring(verts);inner=f.ring([(x,y+.009,z+.001) for x,y,z in verts])
        f.face(outer,0);f.face(inner,DARK);f.bridge(outer,inner,IRON)
        cheekband=[(.003,1.698),(.023,1.702),(.048,1.701),(.070,1.710),(.073,1.690),(.019,1.688)]
        verts=[(s*x,-.198+.016*(x/.073)**1.5,z) for x,z in cheekband]
        outer=f.ring(verts);inner=f.ring([(x,y+.007,z) for x,y,z in verts])
        f.face(outer,4);f.face(inner,DARK);f.bridge(outer,inner,IRON)
    f.finish()
    f.open('TempleAndNape','head')
    for s in (-1,1):
        # The two cheeks terminate in front of each ear. Nape is independent behind ear cutout.
        p=[(-.040,.040),(.295*.1,.038),(.024,-.015),(.006,-.060),(-.012,-.052),(-.029,-.008)]
        f.plate(p,(s*.087,-.128,1.689),(0,s,0),(0,0,1),(s,0,0),.015,0,edge=IRON,ridge=.002)
        p=[(-.044,.039),(.024,.042),(.043,.030),(.041,-.059),(-.014,-.065),(-.023,-.035)]
        f.plate(p,(s*.075,.022,1.679),(0,1,0),(0,0,1),(s,0,0),.024,BACK,edge=IRON)
    f.plate(corners(.066,.066,.32),(0,.055,1.668),(1,0,0),(0,0,1),(0,1,0),.022,BACK,ridge=.005)
    f.finish()
    f.open('NeckGuard','spine_03')
    f.torso([(1.506,.139,.123,-.058,-.017),(1.524,.147,.143,-.055,-.020),
             (1.540,.145,.146,-.054,-.012),(1.594,.122,.151,-.052,-.036),
             (1.634,.116,.148,-.053,-.051)], [IRON,TRIM,IRON,0],12)
    f.finish()

def link(f,center,hw,hh,thick,tilt,lean=0.):
    """Forged rectangular chain, bevels follow both internal and external corners."""
    c=V(center);ex=V((math.cos(lean),0,math.sin(lean)))
    up=V((-math.sin(lean)*math.cos(tilt),math.sin(tilt),math.cos(lean)*math.cos(tilt)))
    norm=ex.cross(up).normalized()
    layers=[]
    for w,h,dep in [(hw,hh,0),(hw-.002,hh-.002,thick*.45),
                      (hw-thick+.002,hh-thick+.002,thick*.45),(hw-thick,hh-thick,0),
                      (hw-thick+.002,hh-thick+.002,-thick*.45),(hw-.002,hh-.002,-thick*.45)]:
        layers.append(f.ring([c+ex*x+up*z+norm*dep for x,z in corners(w,h,.45)]))
    for i in range(6):
        f.bridge(layers[i],layers[(i+1)%6],[CHAIN,CHAIN,TRIM,IRON,CHAIN,CHAIN][i])

def make_torso(f):
    f.group='Torso and Shoulders'
    f.open('RibHarness','spine_03')
    f.torso([(1.083,.155,.139,-.036,-.010),(1.104,.168,.145,-.033,-.008),
             (1.214,.171,.143,-.030),(1.341,.213,.151,-.027),
             (1.433,.222,.137,-.022),(1.50,.187,.119,-.018),
             (1.555,.102,.099,-.020)], [TRIM,BACK,IRON,CHEST,CHEST,BACK])
    # Stepped rib lames; broad flanges show beyond the shutter frame.
    for i in range(3):
        z=1.105+.059*i;w=.158+.012*i;d=.147+.002*i
        f.torso([(z,w+.010,d+.003,-.035),(z+.010,w+.011,d+.005,-.035),
                 (z+.062,w,d,-.034)], [TRIM,IRON])
    f.finish()
    f.open('FurnaceShutters','spine_03')
    f.front([(-.112,-.089),(.112,-.089),(.122,.098),(-.122,.098)],(0,-.191,1.235),.014,DARK,edge=IRON)
    f.front([(-.093,-.069),(.093,-.069),(.102,.084),(-.102,.084)],(0,-.201,1.237),.004,HEAT,edge=DARK,bevel=.055)
    for s in (-1,1):
        f.front([(s*x,z) for x,z in [(.084,-.091),(.102,-.086),(.117,.101),(.098,.100)]],
                (0,-.211,1.236),.022,CHEST,edge=TRIM,bevel=.09)
    for i in range(4):
        z=1.156+i*.043; hw=.096+i*.003
        # Horizontal slats tilt towards the viewer, lower corners fall into the cavity.
        outline=[(-hw,-.011),(0,-.015),(hw,-.011),(hw+.001,.014),
                 (0,.012),(-hw-.001,.014)]
        f.plate(outline,(0,-.214,z),(1,0,0),(0,.42,1),(0,-1,0),.014,CHEST,
                edge=TRIM,bevel=.065)
    f.front(corners(.116,.008,.5),(0,-.211,1.332),.021,IRON)
    f.finish()
    f.open('MantleAndSpine','spine_03')
    for s in (-1,1):
        p=[(.012,1.462),(.086,1.527),(.163,1.528),(.204,1.489),(.174,1.403),(.110,1.348),(.011,1.355)]
        f.front([(s*x,z-1.43) for x,z in p],(0,-.160,1.43),.030,CHEST,edge=IRON,ridge=.014)
    spine=[(-.060,.127),(.060,.127),(.077,.103),(.059,.020),(.043,-.116),(0,-.137),(-.043,-.116),(-.059,.020),(-.077,.103)]
    f.plate(spine,(0,.114,1.35),(1,0,0),(0,0,1),(0,1,0),.032,BACK,ridge=.012)
    for i in range(3):
        f.plate([(-.046,.015),(.046,.015),(.042,-.012),(0,-.021),(-.042,-.012)],
                (0,.139-i*.001,1.387-i*.057),(1,0,0),(0,0,1),(0,1,0),.008,IRON,edge=BACK)
    for s in (-1,1):
        for z in (1.165,1.23,1.30):
            x=s*(.165+(z-1.165)*.28)
            f.plate(corners(.035,.011,.42),(x,.002,z),(0,1,0),(0,0,1),(s,0,0),.010,GLOVE,edge=IRON)
            f.plate(corners(.010,.010,.55),(x+s*.006,-.010,z),(0,1,0),(0,0,1),(s,0,0),.010,RIVET,edge=TRIM)
    f.finish()

def make_shoulders(f):
    f.group='Torso and Shoulders'
    for s,side in ((1,'l'),(-1,'r')):
        f.open('BoxPauldron_'+side,'clavicle_'+side)
        # Rings form a deep, square cast shell. Outer slope and lower bite follow the full figure.
        poly=[(-.125,-.080),(-.085,-.100),(.100,-.115),(.136,-.095),
              (.133,.075),(.099,.115),(-.090,.129),(-.125,.097)]
        center=V((s*.272,-.022,1.495))
        def shell(scale, y, dz, offset=0.):
            return f.ring([center+V((s*(x*scale+offset),y,z*scale+dz)) for x,z in poly])
        rear=shell(.91,.135,.006);rear_bevel=shell(1,.112,.004)
        front_edge=shell(1,-.119,0.);front=shell(.946,-.144,-.003)
        opening=shell(.59,-.146,-.006,.015);inside=shell(.55,-.106,-.005,.015)
        # Open underside under the outer return with fully modeled beveled rim.
        for a,b,t in ((rear,rear_bevel,BACK),(front_edge,front,TRIM),(opening,inside,IRON)):
            f.bridge(a,b,t)
        for i in range(len(poly)):
            j=(i+1)%len(poly)
            ids=(rear_bevel[i],rear_bevel[j],front_edge[j],front_edge[i])
            if i not in (1,3):
                f.face(ids,1)
                continue
            # The underside and the outside wall expose the deep hollow inside the casting.
            pts=[f.verts[idx] for idx in ids]
            ctr=sum(pts,V((0,0,0)))/4
            cut=f.ring([ctr+(p-ctr)*(.81 if i==1 else .70) for p in pts])
            direction=V((0,0,.058)) if i==1 else V((-s*.052,0,0))
            wall=f.ring([f.verts[idx]+direction for idx in cut])
            f.bridge(ids,cut,1)
            f.bridge(cut,wall,IRON)
            f.face(wall,DARK)
        # Continuous front-plane sampling across all eight facets of the square frame.
        for i in range(len(front)):
            j=(i+1)%len(front);ids=(front[i],front[j],opening[j],opening[i])
            uv=[((s*(f.verts[idx].x-center.x)+.125)/.261,
                 (f.verts[idx].z-center.z+.118)/.248) for idx in ids]
            f.face(ids,1,uv)
        f.face(inside,DARK)
        # Rear closure includes a shallow stamped hollow.
        inrear=shell(.68,.137,.007)
        f.bridge(rear,inrear,1);f.face(inrear,BACK)
        f.finish()
        f.open('FistSocket_'+side,'clavicle_'+side)
        anchor=s*.246
        f.front(corners(.047,.047,.32),(anchor,-.148,1.474),.050,IRON,ridge=.006)
        for j in range(4):
            xx=anchor+s*((j-1.5)*.021);h=.028+(1-abs(j-1.5)/2)*.008
            f.front(corners(.011,h,.58),(xx,-.181,1.491+(1-abs(j-1.5)/2)*.004),.031,CHAIN,
                    edge=TRIM,bevel=.15,ridge=.0018)
        f.front([(-.016,-.018),(.017,-.013),(.019,.010),(.004,.020),(-.022,.011)],
                (anchor-s*.023,-.194,1.454),.028,CHAIN,edge=IRON)
        f.finish()
    f.open('LoadChain','spine_03')
    for i in range(-3,4):
        # Bear each alternating bevel against its neighbor as the end links rise into the fists.
        x=math.copysign((0.,.0692,.13815,.2050)[abs(i)],i)
        link(f,(x,-.223+.004*abs(i),1.420+.0040*i*i),.047,.029,
             .012,math.radians(64 if i%2 else 3),i*.099)
    f.finish()

def bone_axis(f,name):
    bone=f.rig.data.bones[name]
    return bone.head_local.copy(),bone.tail_local.copy()

def make_arms(f):
    f.group='Arms and Hands'
    for s,tag in ((1,'l'),(-1,'r')):
        upper='upperarm_'+tag;lower='lowerarm_'+tag;hand='hand_'+tag
        a,b=bone_axis(f,upper);e,w=bone_axis(f,lower)
        f.open('Rerebrace_'+tag,upper)
        f.sleeve(a,b,[(.28,.081,.094),(.33,.083,.095),(.65,.072,.074),(.74,.080,.081,.006),(.79,.078,.078,.006)], [TRIM,IRON,1,TRIM])
        f.finish()
        f.open('ElbowCop_'+tag,lower)
        f.sleeve(e,w,[(-.09,.071,.074),(-.055,.079,.082),(.08,.078,.078),(.16,.070,.069)], [IRON,GREAVE,TRIM])
        shield=[(-.049,.036),(-.021,.054),(.037,.044),(.059,.005),(.034,-.041),(-.012,-.063),(-.054,-.018)]
        f.plate(shield,e+V((s*.047,.004,.002)),(0,1,0),(0,0,1),(s,0,0),.041,1,ridge=.018)
        f.finish()
        f.open('Vambrace_'+tag,lower)
        f.sleeve(e,w,[(.17,.071,.067),(.20,.079,.074),(.25,.080,.073),(.33,.074,.068),(.78,.053,.049),(.89,.052,.048,.006),(.94,.057,.052,.003)], [IRON,TRIM,1,GREAVE,GREAVE,TRIM])
        f.finish()
        # Palm axis follows the thumb/index/pinky spread of the rest hand.
        p0=f.rig.data.bones['index_01_'+tag].head_local.copy()
        p1=f.rig.data.bones['pinky_01_'+tag].head_local.copy()
        knuckle=(p0+p1)*.5
        up=(knuckle-w).normalized();wide=(p0-p1).normalized();wide=(wide-up*wide.dot(up)).normalized()
        outward=wide.cross(up).normalized()
        if outward.x*s<0: outward.negate()
        f.open('GauntletBack_'+tag,hand)
        length=(knuckle-w).length
        pts=[(-.028,0),(.028,0),(.040,length*.65),(.036,length),(.015,length*.97),(-.025,length),(-.039,length*.80)]
        f.plate(pts,w+outward*.024,wide,up,outward,.016,IRON,edge=TRIM,ridge=.008)
        f.sleeve(e,w,[(.965,.055,.052),(.98,.057,.051),(1.045,.052,.047)], [TRIM,GLOVE])
        f.finish()
        f.open('FingerLames_'+tag,hand)
        for digit in ('index','middle','ring','pinky','thumb'):
            for j in (1,2,3):
                f.bone=f'{digit}_{j:02d}_{tag}';p,q=bone_axis(f,f.bone)
                d=(q-p).normalized();no=(outward-d*d.dot(outward))
                if no.length<.02: no=V((s,0,0))
                no.normalize();wx=d.cross(no).normalized();length=(q-p).length
                radius={'thumb':.011,'index':.009,'middle':.009,'ring':.008,'pinky':.007}[digit]*(1-.09*(j-1))
                points=[(-radius,.001),(radius,.001),(radius*.89,length*.70),(radius*.55,length*.88),(-radius*.7,length*.90),(-radius*.93,length*.68)]
                f.plate(points,p+no*radius*.80,wx,d,no,radius*.62,IRON,edge=TRIM,ridge=.0012,bevel=.12)
        f.finish()

def make_legs(f):
    f.group='Legs and Feet'
    f.open('BeltAndFauld','pelvis')
    f.torso([(1.016,.163,.154,-.027,.004),(1.028,.169,.156,-.029,.003),
             (1.085,.166,.150,-.032),(1.098,.159,.145,-.031)], [IRON,GLOVE,TRIM])
    f.front([(-.043,.025),(.043,.025),(.041,-.020),(0,-.038),(-.041,-.020)],
            (0,-.189,1.061),.026,CHAIN,ridge=.007)
    for s in (-1,1):
        f.front(corners(.007,.013,.5),(s*.067,-.18,1.056),.011,RIVET)
    f.finish()
    f.open('TassetApron','pelvis')
    central=[(-.049,.080),(.049,.080),(.056,-.061),(0,-.083),(-.056,-.061)]
    f.plate(central,(0,-.172,.94),(1,0,0),(0,.08,1),(0,-1,0),.022,TASSET,ridge=.010)
    central=[(-.044,.015),(.044,.015),(.055,-.174),(0,-.201),(-.055,-.174)]
    f.plate(central,(0,-.168,.882),(1,0,0),(0,.13,1),(0,-1,0),.017,TASSET,ridge=.011)
    for s in (-1,1):
        for k in range(2):
            theta=math.radians(45+k*40);normal=V((s*math.sin(theta),-math.cos(theta),0))
            horiz=V((s*math.cos(theta),math.sin(theta),0)); up=V((-s*.16,-.02,1))
            center=V((s*(.105+.064*k),-.021-(.105 if k==0 else .020),.910))
            outline=[(-.045,.108),(.046,.099),(.057,-.082),(.010,-.115),(-.051,-.093)]
            f.plate(outline,center,horiz,up,normal,.024,TASSET,edge=IRON,ridge=.009)
            outline=[(-.044,.033),(.043,.026),(.049,-.042),(-.038,-.056)]
            f.plate(outline,center+V((0,0,.042))+normal*.010,horiz,up,normal,.012,IRON,edge=TRIM)
        f.plate([(-.056,.082),(.056,.082),(.064,-.074),(.018,-.107),(-.056,-.086)],
                (s*.085,.110,.932),(1,0,0),(0,-.09,1),(0,1,0),.019,BACK,edge=IRON,ridge=.008)
    f.finish()
    for s,tag in ((1,'l'),(-1,'r')):
        thigh='thigh_'+tag;calf='calf_'+tag;foot='foot_'+tag
        a,k=bone_axis(f,thigh);k,e=bone_axis(f,calf)
        f.open('Cuisses_'+tag,thigh)
        f.sleeve(a,k,[(.23,.106,.119),(.29,.110,.120),(.41,.103,.111),(.70,.090,.094),(.77,.095,.101,.022),(.80,.093,.099,.024)],
                 [IRON,1,TASSET,TASSET,TRIM],10)
        f.finish()
        f.open('Poleyn_'+tag,calf)
        f.sleeve(k,e,[(-.10,.080,.087),(-.075,.082,.089),(.070,.087,.093),(.12,.079,.083)], [TRIM,IRON,BACK])
        poly=[(-.078,.045),(-.052,.076),(.014,.083),(.075,.050),(.080,-.006),(.025,-.050),(0,-.098),(-.043,-.046),(-.080,-.010)]
        f.front([(s*x,z) for x,z in poly],(k.x,k.y-.086,k.z),.042,GREAVE,edge=TRIM,ridge=.041)
        f.finish()
        f.open('Greave_'+tag,calf)
        # Crest follows tibia; proud upper lip and swept ankle maintain the front silhouette.
        rows=[(.145,.080,.091,.012),(.180,.086,.100,.010),(.235,.089,.100,.020),
              (.38,.081,.083),(.67,.058,.058),(.80,.056,.056),(.86,.063,.065,.010),(.89,.061,.066,.016)]
        f.sleeve(k,e,rows,[TRIM,1,GREAVE,GREAVE,GREAVE,GREAVE,TRIM],10)
        p=k.lerp(e,.53);p.y-=.064
        slim=[(-.039,.104),(0,.132),(.039,.104),(.023,-.068),(.016,-.117),(0,-.123),(-.016,-.117),(-.023,-.068)]
        f.front(slim,p,.017,GREAVE,edge=IRON,ridge=.010)
        f.finish()
        f.open('Sabatons_'+tag,foot)
        fx=e.x
        # Cross-sections run from square heel to toe, with flat load-bearing sole.
        def bootrow(y,hw,h,floor=0.):
            shape=[(-.84,0),(.84,0),(1,.14),(.90,.64),(.48,.90),(0,1),(-.48,.90),(-.90,.64),(-1,.14)]
            return f.ring([(fx+s*x*hw,y,floor+z*h) for x,z in shape])
        layers=[bootrow(y,hw,h) for y,hw,h in [(.067,.047,.115),(.055,.055,.131),
                  (-.016,.063,.145),(-.080,.065,.116),(-.143,.068,.083),(-.200,.065,.056),(-.246,.048,.033),(-.261,.025,.022)]]
        f.face(layers[0],BACK);f.face(layers[-1],BOOT)
        for i in range(len(layers)-1):
            f.bridge(layers[i],layers[i+1],[DARK,BOOT,BOOT,BOOT,BOOT,BOOT,BOOT,BOOT,BOOT])
        steps=[(-.009,.157,.064,-.083,.127,.068),(-.077,.132,.066,-.149,.088,.072),
               (-.145,.094,.073,-.202,.061,.068),(-.196,.066,.068,-.251,.042,.052)]
        for sy,sh,sw,ey,eh,ew in steps:
            rings=[bootrow(sy,sw,sh,.008),bootrow(ey+.004,ew,eh+.004,.008),bootrow(ey,ew,eh,.008)]
            f.bridge(rings[0],rings[1],[DARK,IRON,BOOT,BOOT,BOOT,BOOT,BOOT,BOOT,IRON])
            f.bridge(rings[1],rings[2],TRIM)
        f.finish()

def make_underlayer(f,body):
    f.group='Underlayer'
    f.open('QuiltedJackAndHose','pelvis')
    dep=bpy.context.evaluated_depsgraph_get()
    ob=body.evaluated_get(dep);me=ob.to_mesh()
    transform=f.rig.matrix_world.inverted()@ob.matrix_world
    normals=transform.to_3x3().inverted().transposed()
    xyz=[transform@v.co for v in me.vertices]
    groups={g.index:g.name for g in ob.vertex_groups if g.name in f.rig.data.bones}
    indices={}
    for face in me.polygons:
        points=[xyz[i] for i in face.vertices]; center=sum(points,V((0,0,0)))/len(points)
        lateral=abs(center.x)
        # Close-fitted D-shaped neck; open distal sole keeps the unclad feet inspectable.
        neck=1.523+.024*min(lateral/.15,1.)
        if center.z>=neck or center.z<.102: continue
        # Gloves are a separate material region on the same continuous weight-matched shell.
        is_glove=lateral>.49 and center.z<1.18
        which=GLOVE if is_glove else QUILT
        verts=[]
        for idx in face.vertices:
            if idx not in indices:
                v=me.vertices[idx]
                norm=(normals@v.normal).normalized()
                ids=f.ring([xyz[idx]+norm*(.0019 if is_glove else .0037)])
                weights=sorted([(groups[g.group],g.weight) for g in v.groups if g.group in groups and g.weight>.0001],key=lambda x:-x[1])[:4]
                total=sum(w for _,w in weights)
                if total:
                    f.bones[ids[0]]=[(n,w/total) for n,w in weights]
                indices[idx]=ids[0]
            verts.append(indices[idx])
        # Box projection over 14cm squares keeps visible diamond padding at cloth scale.
        axis=max(range(3),key=lambda k:abs(face.normal[k]))
        dirs=[d for d in range(3) if d!=axis]
        vals=[(p[dirs[0]]/.17,p[dirs[1]]/.17) for p in points]
        avg=[sum(q[d] for q in vals)/len(vals) for d in (0,1)]
        uv=[(max(0,min(1,.5+(x-avg[0])*.74+(avg[0]%1-.5)*.63)),max(0,min(1,.5+(y-avg[1])*.74+(avg[1]%1-.5)*.63))) for x,y in vals]
        f.face(verts,which,uv)
    ob.to_mesh_clear()
    f.finish()

def build_armor(rig,body,materials):
    forge=Forge(rig,materials['suit'])
    make_underlayer(forge,body)
    make_helm(forge)
    make_torso(forge)
    make_shoulders(forge)
    make_arms(forge)
    make_legs(forge)
    return forge.objects
