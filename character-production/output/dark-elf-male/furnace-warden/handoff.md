# Furnace Warden

The male Dark Elf stands 1.820 m barefoot and 1.857 m in the closed helm and sabatons. This is the neutral bind pose. One metre equals one Blender unit. The figure faces −Y with Z up in Blender. FBX uses −Z forward, Y up and FBX unit scaling.

[Character plate](Review/Furnace-Warden.jpg) · [Editable source](DarkElfMale.blend) · [Static FBX](DarkElfMale.fbx)

## Outfit switches

The FBX contains one **Male_GameRig**, 53 bones and 38 independently switchable render meshes. Enable these combinations after import. The full model contains 52,884 triangles. The default dressed state draws 31,324.

| State | Visible pieces |
| --- | --- |
| Closed helm | HeadAndNeck, AmberEyes, Brows, quilted jack and hose, and all plate groups. Hide CoveredBody and SweptIvory. |
| Helm removed | Closed-helm state with all four Helm renderers disabled and SweptIvory enabled. |
| Underlayers | All DarkElf renderers, plus Warden_QuiltedJackAndHose. |
| Skin sculpt | In Blender, isolate DarkElf_ContinuousSculpt in the sculpt source collection. It retains the complete joined skin, rear ear surfaces, fingers and feet. |

The render body splits at the neck inside the guard. The original joint centers, hand chains and rest hierarchy come from the MPFB-derived Nightcap male in NightcapHumans_StarterEquipment.blend. The narrow waist, jaw and cheek edits and the thick, swept pinnae change the skin around those joints. The ivory scalp and locks share a hair renderer.

## Paint and material setup

| Slot | Runtime map | Treatment |
| --- | --- | --- |
| Dark Elf • indigo skin | Textures/DarkElf-Skin.png, 2048² | sRGB. The existing male facial paint supplies local features. Violet shadow and lit-cheek samples come from character-plate.png. |
| Dark Elf • copper amber | Textures/DarkElf-Amber.png, 512² | sRGB. Painted radial copper iris, pupil and small pale catchlight. |
| Dark Elf • brushed ivory | Textures/DarkElf-Ivory.png, 512² | sRGB. Nightcap strand paint remapped to an ivory ramp on the scalp and locks. |
| Dark Elf • ash brows | Material color | Matte ash brown. |
| Furnace Warden • banked iron | Textures/Warden-Plate.png, 2048² | sRGB. The recessed orange is included in albedo. |
| Furnace Warden • banked iron | Textures/Warden-Heat.png, 2048² | Linear single-channel mask. In the target shader use albedo × mask × intensity for emission. Native intensity is 0.85. Set it to zero for the cooled read. |

The native file packs the textures. Runtime meshes use UV0. The FBX carries base-color connections. Reconnect the separate linear heat mask in the destination material. The editable source stores DonorProjection as a second UV layer on the suit. The two projection cameras and native-size concept texture are in the hidden References collection.

[Editable donor layers](Paint/Warden-donor-layers.ora) contain sixteen labeled surface swatches. [Donor register](Paint/donors.json) records native pixel quadrilaterals, destinations and the skin palette. Fit the stencil on the visible plane of each surface. The portrait supplies the hood rim, grille, shoulder wear and hot interior. The full figure supplies tasset and greave spacing. [Destination mask](Paint/UV0-donor-region-ids.png) identifies their exact footprint in UV0. Values 1–16 correspond to register order. The bake adds unique oxide variation in world space and extends island colors 16 pixels. [Mip review](Review/Plate-mips.jpg).

The nape closure, stepped spine overlap, reachable flank fasteners, palms and soles are inferred from construction. The rear iron is quieter and cooler. These surfaces use modified interior samples, authored strokes and value ramps. The Hailstone and Ascension studies informed proportions and material grouping. Their pixels stay on the reference board. Hailstone's upright, shorter pinna and the Ascension models' longer profiles informed the rearward sweep. The final chin carries depth without widening the jaw. The shoulder pivot stays within the heavy shell.

## Bind review

The saved file reopened with its paint packed. A fresh-scene FBX import reproduced the named mesh set, hierarchy, bind dimensions, used vertex groups, triangle counts, material slots and UV orientation. Maximum joint-center difference was 0.000344 mm. The imported meshes have at most four deform influences per vertex and zero unweighted vertices. Both frontal rays reach the corneas through the visor. Each boot has a sole contact patch on the ground plane. The short chain uses seven alternating links terminating inside the fists.

[Native rest matrices and mesh measurements](Review/Native-bind.json) · [FBX round-trip audit](Review/FBX-roundtrip.json) · [Visor, chain and sole measurements](Review/Armor-fit.json)

The forearm lip clears each cuff by 3.806 mm. The chain clears the chest mantle by 4.228 mm. Adjacent link gaps range from 0.059 to 0.156 mm at rest. A position-matched comparison found zero difference in the imported deform weights.

Review contains front, profile, rear and three-quarter views, the helm, uncovered head, underside, underlayer body, clay, unlit color, reversed key and a 128-pixel full figure. The Blender renders use the imported geometry and source paint shaders. The static character has also passed Unity import and Play-mode review. [Unity handoff, prefab and captures](Unity-handoff.md)

## Runtime renderer index

| Group | Renderer | Triangles |
| --- | --- | ---: |
| Body | DarkElf_HeadAndNeck | 8,844 |
| Body | DarkElf_CoveredBody | 17,912 |
| Eyes and brows | DarkElf_AmberEyes | 280 |
| Eyes and brows | DarkElf_Brows | 256 |
| Hair | DarkElf_SweptIvory | 3,648 |
| Underlayer | Warden_QuiltedJackAndHose | 13,712 |
| Helm | Warden_ForgeHood | 88 |
| Helm | Warden_Visor_Grille | 364 |
| Helm | Warden_TempleAndNape | 178 |
| Helm | Warden_NeckGuard | 144 |
| Torso and Shoulders | Warden_RibHarness | 480 |
| Torso and Shoulders | Warden_FurnaceShutters | 252 |
| Torso and Shoulders | Warden_MantleAndSpine | 738 |
| Torso and Shoulders | Warden_BoxPauldron_l | 140 |
| Torso and Shoulders | Warden_FistSocket_l | 256 |
| Torso and Shoulders | Warden_BoxPauldron_r | 140 |
| Torso and Shoulders | Warden_FistSocket_r | 256 |
| Torso and Shoulders | Warden_LoadChain | 672 |
| Arms and Hands | Warden_Rerebrace_l | 140 |
| Arms and Hands | Warden_ElbowCop_l | 160 |
| Arms and Hands | Warden_Vambrace_l | 180 |
| Arms and Hands | Warden_GauntletBack_l | 140 |
| Arms and Hands | Warden_FingerLames_l | 510 |
| Arms and Hands | Warden_Rerebrace_r | 140 |
| Arms and Hands | Warden_ElbowCop_r | 160 |
| Arms and Hands | Warden_Vambrace_r | 180 |
| Arms and Hands | Warden_GauntletBack_r | 140 |
| Arms and Hands | Warden_FingerLames_r | 510 |
| Legs and Feet | Warden_BeltAndFauld | 236 |
| Legs and Feet | Warden_TassetApron | 304 |
| Legs and Feet | Warden_Cuisses_l | 160 |
| Legs and Feet | Warden_Poleyn_l | 172 |
| Legs and Feet | Warden_Greave_l | 246 |
| Legs and Feet | Warden_Sabatons_l | 284 |
| Legs and Feet | Warden_Cuisses_r | 160 |
| Legs and Feet | Warden_Poleyn_r | 172 |
| Legs and Feet | Warden_Greave_r | 246 |
| Legs and Feet | Warden_Sabatons_r | 284 |
