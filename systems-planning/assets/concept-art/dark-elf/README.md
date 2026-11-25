# Dark Elf graphics study

**Exploring · November 24, 2026.** Hailstone is the owner's visual target. This study proposes a character and suit for that target. The costume has three swept plates that meet at a single shoulder pin. A small panel of ochre quilting marks the flexible joint at the ribs. The ivory bob and rust-red split skirt keep the silhouette readable against dark stone.

| Plate | What to look for |
| --- | --- |
| [Character and portrait](character-plate.png) | The eye can follow the diagonal from the waist to the shoulder pin in either view. The full figure shows how little shoulder bulk the design needs. |
| [Armor finishes](armor-finishes.png) | The left study uses blue steel with pale rims. On the right, a broad silver highlight rolls into oxblood shadow across each plate. The right-hand finish is my pick for the next material test because that value transition is closest to the Hailstone capture. |
| [Shellbank Steps](shellbank-steps.png) | The blue suit crosses the wet freight stair below the chalk. Against the steps, the bright hair and split skirt survive at thumbnail size. The figure occupies about three-fifths of the frame height, so a distant party-camera read is still open. |

## Local reference evidence

### Female Dark Elf in robes

The [Blender assignment](../../../docs/art/female-dark-elf-blender-prompt.md) develops one original garment on the established female character, with Silt Reader as the default and Kiln Oracle or Mourning Veil as alternatives. The [Unity assignment](../../../docs/art/female-dark-elf-unity-prompt.md) checks the fitted robe under changing light. The [source notes](../../../docs/art/female-dark-elf-robe-reference.md) document the reference observations used to design those checks.

### Male Dark Elf in lava-forged full plate

The [Blender production prompt](../../../docs/art/male-dark-elf-blender-prompt.md) and [Unity production prompt](../../../docs/art/male-dark-elf-unity-prompt.md) take one of these suits from the original concept-image pixels through a skinned character and static review prefab. Furnace Warden is the default assignment.

Three original endgame suits share a male Dark Elf and the Hailstone-inspired metal finish. Each sheet pairs the full silhouette with the helmet at portrait scale. The built-in image generator used the existing finish study for the first sheet and that sheet for the two variants.

| Plate | Local shaman texture studied | Translation into plate |
| --- | --- | --- |
| [The Last Pour](last-pour.png) | `Mail_RaidShaman_E_01Black_Chest_TU_M.blp` | Orange grooves in dark metal became one casting channel ending in a bead at the jaw. A smooth unbroken visor makes that small defect stand out. |
| [Furnace Warden](furnace-warden.png) | `Mail_RaidShaman_B_01OutlandRed_Chest_TU_M.blp` | The linked chest clasp became a short iron chain spanning two massive square shoulders. The barred helm and shuttered breastplate expose the same banked heat. |
| [Ash Requiem](ash-requiem.png) | `Mail_RaidShaman_F_01Black_Chest_TU_M.blp` | The pale gathered collar and blue inset became a flared ash-enamel gorget and one glass bead. A copper staple closes the still-warm fracture in the mask. |

All three male torso maps were decoded from `E:/Wow_Ascension/Data/common.MPQ`, under `ITEM/TEXTURECOMPONENTS/TorsoUpperTexture/`. Model the Warden's grille, the Requiem crest and the Last Pour shoulder lip. Paint the scale, ash mottling and polished edges. An emissive mask could keep the ember accents readable in shadow. The Warden's shoulders and Requiem's collar need clearance tests with a moving rig. These are Exploring concept sheets.

### Endgame armor

The [three-set lineup](endgame-lineup.png) holds the face, body and lighting steady. The Bellfounder's nested bell-shaped shoulder and bronze interior extend the starting plate. Reedfall folds long green scales down one shoulder and leaves the other arm clear. The Kiln Oracle trades the diagonal for a horizontal collar of copper-stapled ceramic and carries its orange glaze down the robe.

In the [Bell Sill scene](bellfounder-at-the-sill.png), the repeated shoulder rims pick up light against the flooded polder. The character occupies roughly 46% of the frame height. A full party at the gameplay camera distance still needs an engine test. For a first prototype, model the shoulder lips, the reed fan outline and the ceramic collar. Paint the fine brass lines, staple shadows and glaze cracks. Check shoulder clearance during arm raises and the collar against the head-turn animation.

### Ascension vanity references

The three loose transmog JSON files in this install's `Data/Content` were empty. The working lookup was the cached item name and display ID in `Cache/WDB`, followed by `DBFilesClient/ItemDisplayInfo.dbc` in `Data/patch-M.MPQ`, then the BLP texture in `Data/patch-TA.MPQ`. Five textures were decoded and inspected. The three female upper-torso textures are 256 × 128. The two shoulder textures are 256 × 256.

| Appearance | Local display ID | What informed the concept |
| --- | --- | --- |
| Breastplate and Pauldrons of Cyclopean Dread | 126614, 127328 | The blue-black shoulder has warm amber recesses. Bellfounder uses that temperature change inside the rolled bell lips. |
| Verdant Eagletalon Tunic and Shoulderpads | 190270, 190275 | Broad green fields and selectively bright gold borders suggested Reedfall's lacquered scales and fine brass edges. |
| Ruddy Eagletalon Tunic | 190290 | Orange-red panels outlined against a dark ground suggested the Oracle's glazed front panels. Fired ceramic and copper repairs are new to the concept. |

Ascension documents Vanity Sets from the Web Shop and lists a nine-piece Eagletalon Cosmetic Armor set. The local check establishes access to reference pixels. Current realm-specific listings and account unlocks were unverified. [Ascension transmog guide](https://db.ascension.gg/?quest=580137) · [Eagletalon set](https://db.ascension.gg/?itemset=50024)

### Hailstone and starting armor

On November 24 the Nightcap Hailstone preview's offline model viewer loaded race 6, female (`DAF`), from the Cairnwright local EQ client. The viewer reported 492 base triangles, 4× MSAA and FSR1 at render scale 1.00. The cropped torso reference shows bright, soft steel bands falling into dark red-brown recesses, with small repeated rivets. This capture documents the renderer at native internal scale. It does not establish a particular texture upscale pack. The local executable was `E:/EQ_Local_Dev/artifacts/cairnwright-creation-20261121/hs-build/hailstone/hailstone.exe`. The local-only capture and log are in `C:/nightcap-development-mmo/dark-elf-reference-local-20261124/`.

The following 128 × 64 upper-torso texture maps were decoded and visually inspected from `E:/Wow_Ascension/Data/common.MPQ`, under `ITEM/TEXTURECOMPONENTS/TorsoUpperTexture/`. The original plate uses new artwork throughout.

| Local texture | Detail used in the study |
| --- | --- |
| `Plate_A_01Black_Chest_TU_U.blp` | The deep central channel and pale outer face suggested recessed channels and a strong light-to-dark transition. |
| `Plate_Horde_B_02Brass_Chest_TU_M.blp` | Its small warm squares became padded ochre quilting visible between cool plates. |
| `Plate_DungeonWarrior_B_01Darkblue_Chest_TU_M.blp` | Nested light and dark edges suggested doubled bevels. The original suit carries those edges diagonally to the shoulder pin. |

## Production read

Model the hair outline, shoulder cap, three large plate lips and split skirt. Paint the quilting, channels, rivets, bevel highlights and wear into a shared character atlas. Start with a painted reflection and a single scene light. Vary the reflection width on the same mesh under warm and cool light to see whether it still reads as metal. Both finishes could use the same rig and UV layout. The hair, skirt deformation and shoulder overlaps carry the main modeling and skinning work.

The scene proposes modular stair and cliff meshes, tiling rock, a painted distant shore and depth fog. Water reflections and moving foam are the largest unmeasured scene costs. All three plates are generated concept art. The proposed character has yet to be built or profiled on target hardware.

The built-in image generator produced all three plates. The character plate anchored the costume in both follow-ups. The finish comparison also used the Hailstone capture directly. [Generation prompts](prompts.md)
