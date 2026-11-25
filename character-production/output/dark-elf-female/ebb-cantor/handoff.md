# Ebb Cantor

**Knellwater Polder · Female Dark Elf warlock · Blender 5.2 · November 25, 2026**

Open `DarkElfFemale.blend` for the dressed character and continuous editable body. Import `DarkElfFemale.fbx` for the static, switchable skin on the 53-bone female rig. [Character plate](Review/Ebb-Cantor.jpg) · [Front](Review/Front.png) · [Rear](Review/Rear.png) · [Profile](Review/Profile.png)

## Design and authorship

At Knellwater, the dry dike stands above a drowned funeral road. As the lower steps emerge, bearers carry their dead against the ebb. The cantor is a costume proposal arising from that scene. She persuades a drowned voice to surface, catches it in a clay vessel and closes the throat with wax. On the open vessel, interrupted sheets of water briefly take the shape of the speaker’s face. The other vessels carry different stamps so she can identify them by touch. [Nightcap lore](../../../../systems-planning/docs/lore/structure.md) · [Funeral stair art brief](../../../../systems-planning/docs/art/image-generation-prompt.md) · [Vessel detail](Review/Vessels.png)

Seventeen folds of ash linen cross one shoulder. A pierced reed shuttle gathers the cloth under madder lacing. Fired tally slips weight its edge. At the opposite hip, three vessels hang from a corded reed rack. The madder chart wraps around the skirt on a rising bias. Its roofless bell gable, surveyed banks and exposed steps are drawn in cut lines. Four bowed bearers carry a shroud around the dark hem. [Pall fastening](Review/Pall.png) · [Printed hem](Review/Hem.png) · [Flat block proofs](Review/Block-proofs.jpg)

The build opens the Nightcap female source, clears the previous outer outfit and lining meshes, and constructs the entire cantor costume from new panel coordinates, pleats, lathe profiles and cord paths. It retains the female body, rig, eyes, ears, hair, boots and fitted shift. The graphics are drawn from blank fields using the checked-in paint source. The build uses no Warcraft graphics, models, UV layouts or image projections. A separate check found zero exact matches for the 16 new costume meshes or three costume maps against either earlier outfit. The silhouette sheet shows the design change on the same body, in the same stance. [Silhouette comparison](Review/Silhouettes.jpg) · [Source inventory and fit measurements](Review/Source-and-fit.json)

## Costume switches

| View | Setup |
| --- | --- |
| Dressed | Enable **05 Ebb Cantor robes**, exposed skin, face, hair and boots. Disable `Skin \| Covered limbs and torso` and `Underlayer \| Fitted linen shift`. Set these two switches on the imported FBX renderers. |
| Shift and boots | Hide all 16 pieces of the cantor costume. Enable the covered skin and fitted shift. Keep the exposed skin, face, hair and boots visible. [Restored view](Review/Restored.png) |
| Continuous sculpt | In the native file, show `Sculpt \| Continuous female base` under **06 Body restoration** and hide both runtime skin sections. |

## Editable graphics

All maps use sRGB. The two textile atlases are 2048². The stoneware strip is 1024 × 512. Its three turned placements bring a different cut-slip stamp to the front of each vessel.

| Surface | Base color | Layered paint source |
| --- | --- | --- |
| Reed-black habit, printed procession, stitching | [Ebb-Procession.png](Textures/Ebb-Procession.png) | [Ebb-Procession.ora](Paint/Ebb-Procession.ora) |
| Linen pall, sedge, gable and madder chart | [Ebb-Pall.png](Textures/Ebb-Pall.png) | [Ebb-Pall.ora](Paint/Ebb-Pall.ora) |
| Firing clouds, throwing rings, slip stamps and knife nicks | [Ebb-Stoneware.png](Textures/Ebb-Stoneware.png) | [Ebb-Stoneware.ora](Paint/Ebb-Stoneware.ora) |

The habit starts at RGB 35, 63, 65. Four quarter-width UV panels run across the upper 1,510 pixels of the atlas. The lower block lays down sedge, the bearers, a shroud and a stepped road, followed by the edge stitching. The pall atlas splits at x = 1,120. Ash linen starts at RGB 200, 190, 161 and the madder chart at 138, 66, 47. Copper, flax, wax and the inner jar surfaces use constant material values. A faint emission on the small water face gives it a cooler value than the ceramic. Cloth and character eyes use ordinary scene lighting. [Unlit render](Review/Unlit.png) · [Clay render](Review/Clay.png)

The four character maps are [indigo skin](Textures/Indigo-Skin.png), [ear paint](Textures/Auricle.png), [copper iris](Textures/Copper-Iris.png) and [ivory hair](Textures/Ivory-Locks.png). For the Unity Built-In handoff, start with the project painted-character shader on cloth and skin, white tint and mipmapped base color. Match the copper, ceramic and small water figure using their dedicated native material settings.

## Verification

The native file reopened, and its FBX reimported in an empty scene with **one armature, 53 bones, 34 skinned meshes, 17 materials and zero clips**. The file contains 131,488 triangles across both states. The dressed configuration draws 109,276. All seven external images resolve. Vertex weights are normalized and use at most four influences. World positions, bind matrices, parent hierarchy, per-corner UVs and material slots passed comparison. Unity static import and Play checks passed. Motion, performance and owner appearance review remain open. [Unity prefab, package and review evidence](Unity-handoff.md) This offline costume has no player-wiki, launcher or server-reload impact. [FBX report and asset hashes](Review/FBX-roundtrip.json) · [Gameplay-size view](Review/Gameplay.png)

The barefoot body measures 1.700 m, and the dressed figure measures 1.714 m including the hair. In bind stance the lowest outer hem clears the floor by 96.4 mm. The sampled distal hand clears the sleeve by 19.9 mm, the lower jaw clears the pall by 45.7 mm, and the braid clears the outfit by 41.6 mm. [Native bind inventory](Review/Native-bind.json)

## Rebuild

Run `python scripts/ebb_cantor_paint.py` from the character-production checkout. In Blender background mode run `-P scripts/build_ebb_cantor.py`, then `-P scripts/review_silt_reader.py -- --outfit ebb-cantor` for the empty-scene FBX comparison. Run `-P scripts/check_ebb_cantor_sources.py` for the geometry, map and fit inventory, and `-P scripts/review_ebb_cantor.py` for the cameras. Finish with `python scripts/ebb_cantor_plate.py`. [Paint](../../../scripts/ebb_cantor_paint.py) · [Garment construction](../../../scripts/build_ebb_cantor.py) · [Source check](../../../scripts/check_ebb_cantor_sources.py)
