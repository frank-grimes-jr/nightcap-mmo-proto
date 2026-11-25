# Vesper Moth

**Superseded visual study.** The owner found this silhouette too close to Classic Warcraft warlock armor. The current Nightcap rebuild is [Ebb Cantor](../ebb-cantor/handoff.md).

**Female Dark Elf warlock vestments · Blender 5.2 · static bind · November 25, 2026**

Open `DarkElfFemale.blend` for the dressed, editable character. `DarkElfFemale.fbx` contains one female deform skeleton with separately switchable skin, hair, robe, glass settings, shoulder assemblies and chains. [Character plate](Review/Vesper-Moth.jpg) · [Comparison with Silt Reader](Review/Costume-comparison.jpg) · [Rear](Review/Rear.png) · [Profile](Review/Profile.png)

## Design

The shoulder silhouette uses three swept, banded horns on each side, above overlapping courses of mulberry enamel and chased gold. A split collar rises behind the ivory bob. Slit-pupil witchglass settings anchor the shoulder fronts, pectoral chains and waist. The front embroidery and rear train depict a death’s-head moth with scalloped wings. Smaller wing-shaped panels fall from the hips, and the bell sleeves expose a pomegranate lining at the wrist. [Shoulders and chest](Review/Reliquary.png) · [Front embroidery](Review/Orphrey.png) · [Gameplay size](Review/Gameplay.png)

Ascension’s documented shop catalog lists Revenant’s Robes and the Necromancers Soulreaper Ensemble. It informed the choice to coordinate the shoulders, cuffs, belt and skirt as a full caster set. Ascension’s Season 9 spellcaster showcase informed the use of dark purple, gold edging and a concentrated magical accent. The live shop URL returned a 404 during this study. The horn profiles, chainwork, moth illustration, brocade repeat and panel cuts were authored for Nightcap. [Shop catalog](https://project-ascension.fandom.com/wiki/Donation_Items) · [Season 9 showcase](https://ascension.gg/en/news/season-9-chapter-4/486)

## Costume switches

| View | Configuration |
| --- | --- |
| Dressed | Enable the exposed skin, face, hair, boots, three lining meshes and all meshes in **05 Vesper Moth regalia**. Disable `Skin \| Covered limbs and torso` and `Underlayer \| Fitted linen shift`. Apply these two renderer switches after importing the FBX. |
| Shift and boots | Hide the regalia and the three meshes whose names begin with `Lining`. Show the covered skin and fitted shift. Keep the eyes, pinnae, brows and hair visible. [Restored view](Review/Restored.png) |
| Editable body | In the native file, enable `Sculpt \| Continuous female base` under **06 Body restoration**, then hide both runtime skin sections. |

## Paint and materials

Two 2048² sRGB maps carry the costume. The first contains the blackberry silk, low-contrast moth repeat, couched hem arches and cuff borders. The second holds the unique embroidery for the front panel, back train, hip pieces and sleeve falls. Its four beds span x = 0–703, 704–1295, 1296–1743 and 1744–2047. The long axis follows the fall of the cloth. Both masters open in an OpenRaster editor with their named layers intact.

| Surface | Base color | Editable source |
| --- | --- | --- |
| Main gown, linings, cuffs and boots | [Vesper-Brocade.png](Textures/Vesper-Brocade.png) | [Vesper-Brocade.ora](Paint/Vesper-Brocade.ora) |
| Embroidered panels | [Vesper-Orphrey.png](Textures/Vesper-Orphrey.png) | [Vesper-Orphrey.ora](Paint/Vesper-Orphrey.ora) |
| Skin and ears | [Indigo-Skin.png](Textures/Indigo-Skin.png) · [Auricle.png](Textures/Auricle.png) | Shared female base |
| Hair and eyes | [Ivory-Locks.png](Textures/Ivory-Locks.png) · [Copper-Iris.png](Textures/Copper-Iris.png) | Shared female base |

For Unity Built-In, start the cloth, skin and hair on `Nightcap/Painted Character` with white tint and mipmapped sRGB color. The gold, bronze, enamel, horn and glass use constant material colors. Match the native roughness and metallic values on compatible local materials. The brighter witchglass facets use teal `#299E88`, roughness 0.22, metallic 0.32 and emission strength 0.16 in Blender. The dark facets use `#176C69`. The iris and cloth receive ordinary scene lighting. [Neutral](Review/Three-quarter.png) · [Clay](Review/Clay.png) · [Unlit](Review/Unlit.png)

## Verification

The saved Blender file reopened. Its FBX reimported into an empty scene with **53 bones, 48 skinned meshes, 15 materials and zero clips**. Both clothing states are present in the 178,316-triangle file. The dressed configuration draws **156,104 triangles**. The original female base measures 1.700 m barefoot, and the dressed model measures 1.714 m. The lowest boot sole reimported within 0.001 mm of the floor.

The comparison checked mesh names, triangles, material slots, per-corner UVs, positions, weights, hierarchy and bind axes. Each vertex has one to four normalized influences, and all six external image paths resolve. The maximum joint-center difference was 0.00034 mm. Unity import, animated deformation, runtime performance and owner appearance approval remain open. This offline art revision has no player-wiki or service-reload impact. [FBX audit and file hashes](Review/FBX-roundtrip.json)

## Rebuild

From the character-production checkout, run `python scripts/vesper_moth_paint.py`, then run Blender in background mode with `--python-exit-code 1 -P scripts/build_vesper_moth.py`. Use `-P scripts/review_silt_reader.py -- --outfit vesper-moth` for the shared female-bind comparison. Run `-P scripts/review_vesper_moth.py` for the dressed cameras and append `-- --restore` for the shift view. Finally run `python scripts/vesper_moth_plate.py` to compose the plates. [Paint source](../../../scripts/vesper_moth_paint.py) · [Geometry source](../../../scripts/build_vesper_moth.py) · [Review cameras](../../../scripts/review_vesper_moth.py)
