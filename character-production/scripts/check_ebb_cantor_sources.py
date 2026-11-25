"""Compare exact local mesh and map fingerprints with the two earlier outfit studies."""
from pathlib import Path
import bpy,hashlib,json
import numpy as np
from mathutils.bvhtree import BVHTree
root=Path(__file__).resolve().parents[1]/'output/dark-elf-female'
def read(folder):
    bpy.ops.wm.open_mainfile(filepath=str(root/folder/'DarkElfFemale.blend'))
    col=next(c for c in bpy.data.collections if c.name.startswith('05 '))
    meshes={}
    for o in col.objects:
        me=o.data;h=hashlib.sha256()
        h.update(np.array([v.co[:] for v in me.vertices],dtype='<f4').tobytes())
        h.update(np.array([l.vertex_index for l in me.loops],dtype='<i4').tobytes())
        meshes[o.name]=h.hexdigest()
    return meshes
earlier={f:read(f) for f in ('silt-reader','vesper-moth')}
new=read('ebb-cantor');current=root/'ebb-cantor'
equal={f:[n for n,h in new.items() if h in other.values()] for f,other in earlier.items()}
maps={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (current/'Textures').glob('Ebb-*.png')}
other_hashes={hashlib.sha256(p.read_bytes()).hexdigest() for f in earlier for p in (root/f/'Textures').glob('*.png')}
assert len(new)==16 and not any(equal.values()) and len(maps)==3 and not (set(maps.values())&other_hashes)
def trees(objs):
    return [BVHTree.FromPolygons([v.co for v in o.data.vertices],[f.vertices[:] for f in o.data.polygons]) for o in objs]
def gap(verts,objs):
    surfaces=trees(objs);return min(t.find_nearest(p)[3] for t in surfaces for p in verts)
scene=bpy.context.scene;full=scene.objects['Sculpt | Continuous female base']
hands=[v.co for v in full.data.vertices if abs(v.co.x)>.436 and v.co.y<-.177 and v.co.z<1.065]
jaw=[v.co for v in full.data.vertices if abs(v.co.x)<.055 and v.co.y<-.080 and 1.461<v.co.z<1.533]
braid=[v.co for o in scene.objects if 'Braid strand' in o.name for v in o.data.vertices]
outfit=[scene.objects[n] for n in new]
report={'comparison':'SHA-256 over local vertex coordinates and face-loop indices, scoped to costume collection 05 in each native file',
        'new_costume_meshes':new,'exact_earlier_mesh_matches':equal,'fresh_map_sha256':maps,'exact_earlier_map_matches':[],
        'reused_character_parts':['female skeleton','continuous body and skin sections','eyes, brows and ears','hair and ferrules','boots and fitted shift'],
        'braid_to_outfit_m':gap(braid,outfit),'distal_hand_to_sleeve_m':gap(hands,[o for o in outfit if 'Cut sleeve' in o.name]),
        'jaw_to_pall_m':gap(jaw,[scene.objects['Pall | Seventeen gathered folds']])}
(current/'Review/Source-and-fit.json').write_text(json.dumps(report,indent=2))
print('ORIGINAL SOURCES',len(new),len(maps),report['braid_to_outfit_m'],report['distal_hand_to_sleeve_m'],report['jaw_to_pall_m'])
