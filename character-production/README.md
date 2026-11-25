# Nightcap Dark Elf character studies

The four handoffs contain the editable Blender character, static FBX, textures, paint sources and review frames. The current female and male looks also include Unity prefabs and static review scenes in the pinned Built-In project.

| Character | Production handoff | Unity |
| --- | --- | --- |
| Ebb Cantor | [Current Knellwater warlock robe](output/dark-elf-female/ebb-cantor/handoff.md) | [Lighting checks, original print and package](output/dark-elf-female/ebb-cantor/Unity-handoff.md) |
| Furnace Warden | [Male Dark Elf in banked iron](output/dark-elf-male/furnace-warden/handoff.md) | [Helmet, underlayers and armor lighting](output/dark-elf-male/furnace-warden/Unity-handoff.md) |
| Silt Reader | [Earlier field scholar and fitted underlayer](output/dark-elf-female/silt-reader/handoff.md) | Blender study |
| Vesper Moth | [Superseded silhouette study](output/dark-elf-female/vesper-moth/handoff.md) | Blender study |

The [original concept plates](../systems-planning/assets/concept-art/dark-elf/README.md) document the visual development. The shared starter bind, paint inputs, MPFB asset license and both accepted human mappings accompany the character build and review scripts. Open `unity-validation` with Unity 6000.5.7f1. The two review scenes are included in its build settings.

For publication, two hidden external comparison cards were removed from the male Blender file. Its original Nightcap projection plate, sculpt, armor, paint and FBX remain available. The published file reopened in Blender 5.2 with matching mesh and UV data. The original studio audit records the pre-publication native file. [Publication check and hashes](output/dark-elf-male/furnace-warden/Review/Publication.json)

Regional assignments on the [Race page](https://frank-grimes-jr.github.io/nightcap-mmo-proto/race.html) are costume proposals. The review captures document stationary characters. Movement, simulation, target-hardware performance and owner appearance approval remain open.

The regional plates pose the archived models in Blender and composite their renders onto the original Atlas ground paintings. Open [Ebb Cantor at Knellwater](output/dark-elf-female/ebb-cantor/Review/Knellwater.png) or [Furnace Warden at Ventfold](output/dark-elf-male/furnace-warden/Review/Ventfold.png) for the lossless frames. To reproduce them, run Blender 5.2 in background mode with [render_atlas_portraits.py](scripts/render_atlas_portraits.py), passing the gh-pages checkout, an output folder and 36 samples after `--`.
