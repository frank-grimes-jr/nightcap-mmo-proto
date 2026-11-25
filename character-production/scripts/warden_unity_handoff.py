"""Assemble the Unity handoff from measured editor results and actual GPU captures."""
from pathlib import Path
import hashlib, json
import numpy as np
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parents[1]
O=P/'output/dark-elf-male/furnace-warden';R=O/'UnityReview'
U=P/'unity-validation/Assets/NightcapDarkElfMale/furnace-warden'
def rgb(path):return Image.open(path).convert('RGB')
def font(size,serif=False):return ImageFont.truetype('C:/Windows/Fonts/'+('georgia.ttf' if serif else 'segoeui.ttf'),size)
def image_panel(sheet,name,box):
    pic=rgb(R/(name+'.png'))
    from PIL import ImageOps
    sheet.paste(ImageOps.fit(pic,(box[2],box[3]),method=Image.Resampling.LANCZOS),box[:2])
def overview():
    sheet=Image.new('RGB',(1510,960),'#28252d');d=ImageDraw.Draw(sheet)
    d.text((48,26),'N I G H T C A P     /     U N I T Y   C H A R A C T E R   R E V I E W',font=font(16),fill='#d8bba4')
    d.text((44,65),'Furnace Warden',font=font(61,True),fill='#efe9dd')
    d.text((1178,102),'Built-In forward   /   Humanoid',font=font(18),fill='#bcafb0')
    d.line((45,155,1465,155),fill='#65575d')
    image_panel(sheet,'Neutral-three-quarter',(45,180,582,676))
    image_panel(sheet,'Helm-detail',(656,180,389,315))
    image_panel(sheet,'Uncovered-head',(1071,180,394,315))
    image_panel(sheet,'Reversed-key',(656,551,252,305))
    image_panel(sheet,'Forge',(933,551,252,305))
    image_panel(sheet,'Base',(1213,551,252,305))
    for x,y,s in [(45,875,'Armored   /   neutral light'),(656,505,'Closed helm'),(1071,505,'Helm removed'),(656,875,'Reversed key'),(933,875,'Forge light'),(1213,875,'Underlayers')]:
        d.text((x,y),s,font=font(20,True),fill='#eaded1')
    sheet.save(R/'Unity-Warden.jpg',quality=95,subsampling=0)
def comparisons():
    comparison=Image.new('RGB',(980,465),'#28252d');d=ImageDraw.Draw(comparison)
    d.text((25,17),'Distance and paint comparison',font=font(30,True),fill='#eee2d6')
    plate=rgb(P.parent/'systems-planning/assets/concept-art/dark-elf/furnace-warden.png')
    concept=plate.crop((29,18,550,977)).resize((70,128),Image.Resampling.LANCZOS)
    blender=Image.open(O/'Review/Front.png').convert('RGBA');blender=blender.crop(blender.getbbox())
    blender=blender.resize((round(blender.width*128/blender.height),128),Image.Resampling.LANCZOS)
    distance=rgb(R/'Distance-128.png')
    comparison.paste(concept,(53,135));comparison.paste(blender,(221,135),blender)
    comparison.paste(distance.crop((414,290,546,430)),(362,129))
    for x,s in [(32,'Concept'),(199,'Blender'),(370,'Unity')]:d.text((x,305),s,font=font(18),fill='#e8d8c8')
    d.text((28,375),'128 px figure height',font=font(17),fill='#c4b2a9')
    for i,(p,s) in enumerate([(O/'Review/Unlit-color.png','Blender unlit'),(R/'Unlit-Blender-match.png','Unity unlit')]):
        im=Image.open(p).convert('RGBA')
        # Same orthographic frame and projection for both crops.
        im=im.crop((175,35,495,380));im.thumbnail((195,218),Image.Resampling.LANCZOS)
        comparison.paste(im,(535+i*215,99),im)
        d.text((541+i*215,305),s,font=font(18),fill='#e8d8c8')
    comparison.save(R/'Scale-and-paint.png')

def metrics():
    d=json.loads((R/'import-audit.json').read_text());play=json.loads((R/'play-audit.json').read_text())
    av=json.loads((R/'avatar-configuration.json').read_text())
    assert d['passed'] and play['passed'] and av['returnedToReview']
    src=json.loads((O/'Review/Native-bind.json').read_text())['meshes']
    slots={'Dark Elf • indigo skin':'Indigo Skin','Dark Elf • copper amber':'Amber Eyes','Dark Elf • brushed ivory':'Swept Ivory','Dark Elf • ash brows':'Ash Brows','Furnace Warden • banked iron':'Banked Iron'}
    assert {m['name'] for m in d['meshes']}==set(src)
    for m in d['meshes']:
        s=src[m['name']]
        assert s['triangles']==m['triangles'] and s['max_influences']==m['influences'] and slots[s['materials'][0]]==m['material'],m['name']
    replay=np.abs(np.asarray(rgb(R/'Edit-mode.png')).astype(int)-np.asarray(rgb(R/'Play-mode.png')).astype(int))
    initial=np.array(rgb(R/'Full-resolution-before-compression.png'),float)
    compressed=np.array(rgb(R/'Helm-detail.png'),float)
    delta=np.abs(initial-compressed);edited=np.max(delta,axis=-1)>0
    srcim=np.array(Image.open(O/'Review/Unlit-color.png').convert('RGBA')).astype(float)
    dstim=np.array(Image.open(R/'Unlit-Blender-match.png').convert('RGBA')).astype(float)
    mask=(srcim[:,:,3]>192)&(dstim[:,:,3]>192)
    overlap=mask.sum()/((srcim[:,:,3]>192)|(dstim[:,:,3]>192)).sum()
    diff=np.abs(srcim[:,:,:3]-dstim[:,:,:3])[mask]
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    for t in (O/'Textures').glob('*.png'):assert sha(t)==sha(U/'Textures'/t.name)
    for f in U.rglob('*'):
        if f.suffix!='.meta':assert Path(str(f)+'.meta').exists(),f
    assert sha(O/'DarkElfMale.fbx')==sha(U/'Model/DarkElfMale.fbx')
    review=dict(fbx_sha256=sha(O/'DarkElfMale.fbx'),blend_sha256=sha(O/'DarkElfMale.blend'),
        all_source_slots_and_triangle_counts_match=True,source_texture_bytes_match=True,
        stopped_vs_play_max_code_delta=int(replay.max()),stopped_vs_play_fraction_changed=float((replay.max(2)>0).mean()),
        before_vs_after_BC7_mean_code_delta=float(delta.mean()),before_vs_after_BC7_p99=float(np.percentile(delta,99)),
        unlit_silhouette_iou=float(overlap),unlit_overlap_median_absolute_sRGB_delta=float(np.median(diff)),
        unlit_overlap_p95_absolute_sRGB_delta=float(np.percentile(diff,95)))
    (R/'comparison.json').write_text(json.dumps(review,indent=2))
    return d,review
def handoff(d,review):
    asset='../../../unity-validation/Assets/NightcapDarkElfMale/furnace-warden'
    bones=len(d['mapping'])
    maps='\n'.join(f"| {m['name']} | {m['size']}² | {'sRGB' if m['sRGB'] else 'Linear'} | {m['format']} | {m['mips']} |" for m in d['textures'])
    md=f"""# Furnace Warden in Unity

Open [DarkElfMale_Review.unity]({asset}/Review/DarkElfMale_Review.unity) in the existing Built-In validation project with Unity {d['unity']}. Drag [DarkElfMale.prefab]({asset}/Prefab/DarkElfMale.prefab) into another scene to use the dressed character. The prefab depends on the imported model, five materials, the supplied textures, the project painted shader and the suit-local heat shader. The floor, camera and key belong to the review scene.

![Neutral Warden, helmet detail, uncovered head and alternate lighting](UnityReview/Unity-Warden.jpg)

## Inspect the character

The scene opens in **Armored - helm on**. To compare outfits, deactivate the visible root and activate **Armored - helm off** or **Base - underlayers** in the Hierarchy. All three are instances of the same prefab. Their renderer overrides restore the hair, covered skin and four helmet pieces. Each instance has its own one-skeleton pose and shares the imported meshes and materials.

| Measurement | Blender bind | Unity skinned vertices |
| --- | ---: | ---: |
| Barefoot, crown to sole | 1.820 m | {d['barefoot']:.6f} m |
| Equipped height | 1.857 m | {d['equipped']:.6f} m |
| Left / right boot sole Y | 0 / 0 m | {d['leftSole']:.7f} / {d['rightSole']:.7f} m |
| Bones | 53 | {d['rigTransforms']} |
| All / dressed triangles | 52,884 / 31,324 | {d['allTriangles']:,} / {d['dressedTriangles']:,} |

The prefab has {d['renderers']} skinned renderers, five character materials, an identity root and +Z forward. The importer uses file units, scale 1, imported normals, UV0 and up to four normalized weights. Tangents are omitted for this albedo-only surface treatment. The valid Humanoid Avatar was created from the FBX with the accepted male mapping. The Avatar configuration stage resolved {bones} assignments, including all 30 finger segments. The disabled Animator retains that Avatar with an empty controller and root motion off. Clip count is {d['clips']}.

All {d['renderers']} triangle counts and source material slots match the Blender register. Each bound mesh references the one rig in its instance. All baked vertices fell inside their renderer bounds. At the frustum edge the figure retained {100*d['edgePixelRetention']:.1f}% of its center-frame silhouette pixels. The stopped and playing captures had a maximum RGB difference of {review['stopped_vs_play_max_code_delta']} code values out of 255. [Import measurements](UnityReview/import-audit.json) · [Avatar configuration](UnityReview/avatar-configuration.json) · [Play check](UnityReview/play-audit.json) · [Image comparison](UnityReview/comparison.json)

## Paint and lighting

The skin, eyes, brows and hair use Nightcap/Painted Character. The plate and underlayer share its local Painted Heat variant. Diffuse wrap is 0.35 and indirect gain is 1.5. Textured materials have white tint, tiling 1 and offset 0. The brows retain an ash-brown tint. Emission adds painted albedo × linear mask × intensity to the existing lighting response. The shipped intensity is 0.85. [Heat disabled](UnityReview/Helm-albedo-heat.png) · [Heat enabled](UnityReview/Helm-detail.png)

| Map | Resolution | Color space | Windows GPU format | Mip levels |
| --- | ---: | --- | --- | ---: |
{maps}

All maps use trilinear filtering, clamp, anisotropy 4 and full authored resolution. Source PNGs and FBX match the Blender handoff byte for byte. The portrait was captured once uncompressed and again with high-quality compression. Mean absolute RGB difference across that frame was {review['before_vs_after_BC7_mean_code_delta']:.2f} / 255. [Uncompressed](UnityReview/Full-resolution-before-compression.png) · [Compressed](UnityReview/Helm-detail.png)

The review uses a matte floor at Y=0, a gray camera background, one directional key, flat ambient fill and soft shadows. The orthographic three-quarter camera targets (0, 0.925, 0.025) with half-height 1.045 m. Its direction from the target is (1.55, 0.33, 4.5), normalized. All three lighting comparisons use that camera. Fog, HDR and post-processing are off.

| Lighting | Key travel direction, normalized on use | Key RGB / intensity | Ambient RGB |
| --- | --- | --- | --- |
| [Neutral](UnityReview/Neutral-three-quarter.png) | (0.64, −0.82, −0.82) | (1, .96, .92) / 1.25 | (.49, .49, .52) |
| [Reversed](UnityReview/Reversed-key.png) | (−0.64, −0.82, −0.82) | (1, .96, .92) / 1.25 | (.49, .49, .52) |
| [Forge](UnityReview/Forge.png) | (.94, −.42, −.36) | (1, .61, .35) / .85 | (.28, .33, .43) |

## Visual review

The square shoulders and barred hood carry the silhouette at distance. The chest shutters keep their orange separation, while individual links and fine wear merge at {d['distancePixels']} pixels. In the close-up the amber eyes sit behind the shelf, the ears clear the hood, and the orange falls behind the dark bars. With the helmet removed, the ivory hair and violet cheek separate from the collar. The armor reads more angular and its wear more mottled than the concept. The bind pose also holds the arms wider. [Concept, Blender and Unity](UnityReview/Scale-and-paint.png) · [960 × 720 distance frame](UnityReview/Distance-128.png) · [Reversed key](UnityReview/Reversed-key.png)

[Front](UnityReview/Front.png) · [Side](UnityReview/Side.png) · [Rear](UnityReview/Rear.png) · [Helm off](UnityReview/Armored-helm-off.png) · [Uncovered portrait](UnityReview/Uncovered-head.png) · [Grazing profile](UnityReview/Head-profile.png) · [Base](UnityReview/Base.png) · [Base rear](UnityReview/Base-rear.png)

The source-matched unlit camera uses Blender's 670 × 850 framing. The two silhouettes overlap by {100*review['unlit_silhouette_iou']:.2f}% intersection over union. Within their common foreground, the median absolute RGB channel difference is {review['unlit_overlap_median_absolute_sRGB_delta']:.0f} / 255. Silver wear on the hood, orange shutters and asymmetric tasset marks retain their orientation. [Blender unlit](Review/Unlit-color.png) · [Unity unlit](UnityReview/Unlit-Blender-match.png)

## Reproduce

The project wrapper runs four editor stages, Build, Review, Avatar and Play. Build recreates the assets. Review reimports and measures the saved model and scene and captures the shots. Avatar opens Unity's configuration stage, checks its assignments and returns to the review scene. Play compares the default state in Edit and Play modes. The Python handoff script compares the captures, source checksums and per-renderer counts. [Wrapper](../../../scripts/run_furnace_warden_unity.ps1) · [Handoff check](../../../scripts/warden_unity_handoff.py)

The final build, reimport, Avatar and Play checks completed without an error attributable to the character. Meshes, materials, shaders and textures resolved after reopening. The raw editor logs are retained locally under `character-production/evidence/diagnostics/furnace-warden-unity/`. The accepted local human FBX supplied the mapping and scale conventions. [Unity model settings](https://docs.unity3d.com/6000.0/Documentation/Manual/FBXImporter-Model.html) · [Unity rig settings](https://docs.unity3d.com/6000.0/Documentation/Manual/FBXImporter-Rig.html)

Blender input SHA-256 is `{review['blend_sha256']}`. FBX input SHA-256 is `{review['fbx_sha256']}`. The validation covers this static character in Unity. Gameplay integration, animated deformation and populated-scene performance remain separate milestones. [Blender handoff](handoff.md)
"""
    (O/'Unity-handoff.md').write_text(md,encoding='utf-8')

if __name__=='__main__':
    overview();comparisons();d,review=metrics();handoff(d,review);print(json.dumps(review,indent=2))

