"""Measure the Warden's actual rest fit in the opened production Blender scene."""
import json
import hashlib
from pathlib import Path

import bpy
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree


class Surface:
    def __init__(self, obj, verts=None):
        ob = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
        mesh = ob.to_mesh()
        mesh.calc_loop_triangles()
        indices = sorted(verts) if verts is not None else list(range(len(mesh.vertices)))
        self.name = obj.name
        local = {v:i for i,v in enumerate(indices)}
        self.xyz = [ob.matrix_world @ mesh.vertices[i].co for i in indices]
        self.points = np.array(self.xyz)
        triangles = [[local[i] for i in tri.vertices] for tri in mesh.loop_triangles if tri.vertices[0] in local]
        edges = sorted({tuple(sorted((a,b))) for a,b,c in triangles for a,b in [(a,b),(b,c),(c,a)]})
        self.segments = self.points[np.array(edges)]
        self.tree = BVHTree.FromPolygons(self.xyz, triangles, all_triangles=True)
        ob.to_mesh_clear()


def components(obj):
    adjacency = [[] for _ in obj.data.vertices]
    for edge in obj.data.edges:
        a,b = edge.vertices
        adjacency[a].append(b)
        adjacency[b].append(a)
    seen = set(); pieces = []
    for i in range(len(adjacency)):
        if i in seen:
            continue
        verts = {i}; stack=[i]
        while stack:
            for j in adjacency[stack.pop()]:
                if j not in verts:
                    verts.add(j)
                    stack.append(j)
        seen.update(verts)
        pieces.append(verts)
    return sorted(pieces, key=lambda ids:sum(obj.data.vertices[i].co.x for i in ids)/len(ids))


def distance(a,b):
    """Exact triangle distance via crossings, vertex/triangle and interior edge/edge pairs."""
    overlaps = a.tree.overlap(b.tree)
    if overlaps:
        return {'millimetres':0., 'crossing_triangle_pairs':len(overlaps)}
    best = min(min(b.tree.find_nearest(p)[3] for p in a.xyz),
               min(a.tree.find_nearest(p)[3] for p in b.xyz))
    # Edge endpoints already have their exact nearest-face tests above.
    b0,b1 = b.segments[:,0],b.segments[:,1]
    db = b1-b0
    bb = np.sum(db*db,axis=1)
    low,high = np.minimum(b0,b1),np.maximum(b0,b1)
    for p,q in a.segments:
        keep = np.all((low<=np.maximum(p,q)+best)&(high>=np.minimum(p,q)-best),axis=1)
        if not np.any(keep):
            continue
        da=q-p; ew=db[keep];v=p-b0[keep];aa=da@da
        av=v@da; bv=np.sum(v*ew,axis=1); ab=ew@da
        denom=aa*bb[keep]-ab*ab
        valid=np.abs(denom)>1.e-16
        denom=np.where(valid,denom,1.)
        ta=(ab*bv-bb[keep]*av)/denom
        tb=(aa*bv-ab*av)/denom
        valid &= (ta>0)&(ta<1)&(tb>0)&(tb<1)
        if np.any(valid):
            ds=v[valid]+ta[valid,None]*da-tb[valid,None]*ew[valid]
            best=min(best,float(np.min(np.linalg.norm(ds,axis=1))))
    return {'millimetres':round(best*1000,4),'crossing_triangle_pairs':0}


objects=bpy.data.objects
source=Path(bpy.data.filepath)
eye=objects['DarkElf_AmberEyes']
eyesurface=Surface(eye)
solids={o.name:Surface(o) for o in objects if o.get('warden_group')=='Helm'}
solids['DarkElf_HeadAndNeck']=Surface(objects['DarkElf_HeadAndNeck'])
rays=[]
for sign,side in [(1,'left'),(-1,'right')]:
    points=[p for p in eyesurface.xyz if p.x*sign>0]
    x=sum(p.x for p in points)/len(points);z=sum(p.z for p in points)/len(points)
    origin=Vector((x,-.50,z));direction=Vector((0,1,0))
    point,_,_,d=eyesurface.tree.ray_cast(origin,direction)
    if point is None:
        raise RuntimeError(f'{side} eye center ray missed eye sphere')
    blocks=[]
    for name,surf in solids.items():
        hit,_,_,di=surf.tree.ray_cast(origin,direction,d-.00001)
        if hit is not None:
            blocks.append({'name':name,'hit':list(hit),'metres_before_eye':round(d-di,6)})
    rays.append({'eye':side,'origin_m':list(origin),'direction':list(direction),'cornea_hit_m':list(point),'blocking_surfaces':blocks})

feet={}
for tag in ('l','r'):
    surface=Surface(objects['Warden_Sabatons_'+tag]);zz=surface.points[:,2]
    sole=surface.points[zz<=zz.min()+.00001]
    feet[tag]={'lowest_z_mm':round(float(zz.min())*1000,4),'contact_vertices':len(sole),'contact_span_xy_mm':[round(float(v)*1000,2) for v in np.ptp(sole[:,:2],axis=0)]}

chain_obj=objects['Warden_LoadChain']
links=[Surface(chain_obj,ids) for ids in components(chain_obj)]
chain=Surface(chain_obj)
harness={name:distance(chain,Surface(objects['Warden_'+name])) for name in ['MantleAndSpine','RibHarness','FurnaceShutters','BoxPauldron_l','BoxPauldron_r']}
adjacent=[distance(a,b) for a,b in zip(links,links[1:])]
anchors={side:distance(links[-1 if side=='l' else 0],Surface(objects['Warden_FistSocket_'+side])) for side in ('l','r')}
cuffs={side:distance(Surface(objects['Warden_GauntletBack_'+side]),Surface(objects['Warden_Vambrace_'+side])) for side in ('l','r')}
with source.open('rb') as stream:
    fingerprint=hashlib.file_digest(stream,'sha256').hexdigest()
report={
    'source':source.name,
    'sha256':fingerprint,
    'units':'metres unless explicitly mm',
    'eye_test':'Orthographic frontal rays through the rest-space centers of the actual eyeball meshes, testing all helm parts and head surface before the first eye hit.',
    'distance_test':'Triangle crossings, both vertex-to-triangle directions and interior edge-to-edge distance on world-space triangulated rest meshes.',
    'eyes':rays,
    'boot_ground':feet,
    'chain_to_body_armor':harness,
    'adjacent_links_right_to_left':adjacent,
    'terminal_link_to_socket':anchors,
    'gauntlet_cuff_to_vambrace':cuffs,
    'socket_design':'The terminal links are captured inside each closed fist. Their embedded sections meet the iron of the sockets.',
    'fit_pass':len(links)==7 and not any(r['blocking_surfaces'] for r in rays)
               and all(abs(f['lowest_z_mm'])<.1 for f in feet.values())
               and all(not h['crossing_triangle_pairs'] for h in harness.values())
               and all(not x['crossing_triangle_pairs'] and x['millimetres']<1 for x in adjacent)
               and all(anchor['millimetres']<.1 for anchor in anchors.values())
               and all(not cuff['crossing_triangle_pairs'] and cuff['millimetres']>0 for cuff in cuffs.values())
}
out=source.parent/'Review'/'Armor-fit.json'
out.write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report),flush=True)
