# Nightcap human starter package

Male and female human characters with base clothing and Wayfarer starter equipment, using an earthy EQ-inspired palette and painted MMORPG readability. This package is the current implementation baseline, not final animation or MMO performance acceptance.

## Import and use

1. Use Unity 6000.5.7f1 with the Built-In render pipeline, the configuration used to build and test these assets. Other Unity versions and URP/HDRP are unverified; the custom painted shader needs adaptation for those pipelines.
2. Import `NightcapHumans_Starter.unitypackage` through Assets > Import Package > Custom Package. Keep the included scripts, shader, materials, textures, models, controllers and prefabs together. Unity references use GUIDs; do not copy only the prefab files.
3. Drag a base prefab (`Assets/NightcapHumans/Male_LODHuman.prefab` or `Female_LODHuman.prefab`) or an equipped prefab (`Assets/NightcapHumans/Equipment/Male_WayfarerHuman.prefab` or `Female_WayfarerHuman.prefab`) into your scene. Their existing prefab inheritance preserves the base character.
4. Use Linear color space and scene lighting. Matte surfaces use `Nightcap/Painted Character`; the included metallic materials use Standard. For a preview, add ambient light and a directional light. Characters do not emit light.
5. Drive the Animator float parameter `Speed`: 0 for idle, 1.05 for the authored walk, 2.8 for run, with interpolation between them. Clips are in-place: your game controller must move and rotate the character. Keep `applyRootMotion` off for this setup. No player controller, collision capsule, camera or combat system is included in this prefab package.

Male height is approximately 1.82 metres; female approximately 1.70 metres. Both use a shared naming scheme with 53 deform bones and Humanoid avatars. Each base character has three mesh LODs. The equipped variants add one equipment skin to each LOD. Material and geometry references remain editable through ordinary prefab/model import settings.

The existing automatic blink component is included because the prefabs reference it; further facial work is deferred. The package contains the accepted runtime facial contract, not the later experimental expression exports.

## Equipment

Wayfarer leather vest, shoulder pads, bracers, boot guards, sheathed short sword and oak buckler. Equipment uses five materials and 12,698 triangles per character. Native authoring keeps the pieces separate, but the current Unity equipment export consolidates them into one skinned mesh. Individual item swapping, unsheathing, combat grips and equipment-specific LODs require the next integration pass.

Walking/running quality and equipment carrying poses are provisional, explicitly deferred while gameplay mechanics develop. Basic rig/material/deformation and movement checks pass; complete animation-cycle clipping review and crowd-performance testing remain outstanding. Do not interpret the test yard or clean import check as proof of those items.

## Editable source and provenance

The native source is supplied separately as `NightcapHumans_StarterEquipment.blend` in the project workspace, with packed material textures and separate equipment pieces. The complete authoring history and scripts remain in the character-production worktree. See the adjacent PROVENANCE.md and MPFB-LICENSE.md for the foundation and reference history.
