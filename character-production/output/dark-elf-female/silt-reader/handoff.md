# Silt Reader

**Female Dark Elf · Knellwater field scholar · Blender 5.2.0 LTS · November 25, 2026**

Open `DarkElfFemale.blend` for the dressed bind pose. Import `DarkElfFemale.fbx` for the single deform skeleton and switchable meshes. The complete body, fitted linen shift, separate eyes, swept bob and bound braid all use the female starter rig. This handoff covers the static Blender asset. Unity import, motion, runtime cost and owner appearance review are open.

[Character plate](Review/Silt-Reader.jpg) · [Turnaround](Review/Turnaround.jpg) · [Underlayer](Review/Underlayer.png) · [Cuff](Review/Cuff.png) · [Flood register](Review/Flood-register.png)

## Assembly

| State | Mesh switches |
| --- | --- |
| Dressed | Enable the exposed head, neck and hands, face pieces, eyes, hair, boots, all three lining pieces, robe and plumb weight. Disable `Skin \| Covered limbs and torso` and `Underlayer \| Fitted linen shift`. Set these switches on the imported renderers. The native scene opens in this state. |
| Fitted linen shift | Enable the covered skin and fitted shift. Keep the boots, exposed skin, face and hair. Disable the entire Silt Reader ensemble and the three `Lining` meshes. The clay-colored shift has two flax shoulder straps. |
| Editable continuous body | In the native file, show `Sculpt \| Continuous female base` under **06 Body restoration**. Hide both runtime skin sections. The two runtime sections reconstruct the same complete surface in the FBX. Keep the pinnae, eyes, brows and hair for the full character. |

The back is cut in joined panels. A center inverted pleat deepens below the sash. The short shoulder yoke crosses both sleeve caps, sits higher in front and carries its own bound edge. The front wrap crosses from the wearer's left collarbone toward the right waist. A separate opening on her left reveals the clay inset. The brass plummet hangs from a waxed cord at the sash keeper. The underside of the outer panels, cuff turns, slit inset and collar lip have geometry.

## Fit and bind

| Measurement in rest stance | Result |
| --- | ---: |
| Source and finished crown to sole, barefoot | 1.7000 m |
| Dressed height, including hair | 1.7140 m |
| Lowest boot sole | 0.0000 m |
| Lowest outer hem above floor | 115.1 mm |
| Cuff to hand | 21.3 mm |
| Collar to jaw | 44.2 mm |
| Braid strands to nearest ensemble mesh | 37.7 mm |

The cuff figure samples the hand beyond the wrist. The jaw figure samples the lower front jaw surface. Both use the closest point on a garment triangle. The editable assembly uses Blender Z up and faces −Y. The centered FBX uses −Z forward, Y up, unit scaling, deform bones only and zero animation clips. [Native measurements and matrices](Review/Native-bind.json)

The FBX reimported into an empty Blender scene with **one skeleton, 53 bones, 49 skinned meshes and seven materials**. It contains 100,784 triangles across both clothing states. The dressed switch set draws **78,572 triangles**. All groups resolve to bones. Every vertex has one to four normalized influences. Each sleeve and cuff uses its own arm chain. The skirt grades from pelvis into its own thigh, with a pelvis-dominant center overlap. The check compared material slots, per-corner UVs, world positions, weights, bone parents and bind axes with the reopened native file. The largest joint-center difference was 0.00034 mm. All five external image paths resolved. [FBX comparison and file hashes](Review/FBX-roundtrip.json) · [Front weights](Review/Weights-front.png) · [Rear weights](Review/Weights-rear.png)

## Paint and material pairing

All delivered images below use **sRGB**. In the Unity Built-In project, use the existing `Nightcap/Painted Character` shader with a white tint, diffuse wrap 0.35 and indirect gain 1.5 as the starting point. Preserve UV0 and enable mipmaps. Use the dedicated brass slot for its narrower highlight. Keep cloth and eyes non-emissive. The delivery includes color maps only.

| Material | Image | Authoring size |
| --- | --- | ---: |
| Dyed cloth, linings, sash and boots | [SiltReader-BaseColor.png](Textures/SiltReader-BaseColor.png) | 2048² |
| Indigo skin | [Indigo-Skin.png](Textures/Indigo-Skin.png) | 1024² |
| Ear surfaces | [Auricle.png](Textures/Auricle.png) | 512² |
| Bob, forelocks and braid | [Ivory-Locks.png](Textures/Ivory-Locks.png) | 512² |
| Eyes | [Copper-Iris.png](Textures/Copper-Iris.png) | 512² |
| Worn brass and ash brows | Parameter colors, respectively `#AE8653` and `#453A4B` | — |

Open [SiltReader.ora](Paint/SiltReader.ora) in an OpenRaster editor to edit the layered master. The dye fields start with wrap `#4C5068`, left panel `#4A4D62`, back `#494C61`, inside front `#494D63`, yoke `#373C50`, clay `#A25242`, flax `#C2A888` and sash `#473538`. Brush coordinates and layer definitions are in [the paint source](../../../scripts/silt_reader_paint.py).

1. Block the four long pattern pieces into atlas columns. At the hem their approximate developed widths are 40, 52, 34 and 32 cm. In pixel space the main fields occupy x = 0–474, 475–1051, 1052–1408 and 1409–2047. They run from y = 0–1430, with the hem at the bottom. The remaining strip holds sleeves, yoke, lining, cuffs, sash, facing and boots. The field colors extend 18 px beyond the UV edges. [Cutting study](Review/Cutting-study.png) · [Panel map](Review/Panel-map.png) · [Measured cut stations](Paint/Cut-stations.json)
2. Add low-amplitude dye variation, long value changes near the hem and a broken wet-to-dry tide line. Use restrained changes in hue and value across the wool. The broad fold highlights on the character come from the modeled surface.
3. Lay in the clay selvage. Draw three long bars, leave a gap, then draw one short bar. Paint the lines 5–7 px wide. Interrupt one bar at the pieced seam and leave rubbed interruptions in the resist. Place the new darn across the older stain and pick out its edge with 2 px needle marks. The bars sit on one lower panel. A short broken continuation reaches the adjoining strip. [Original register scrap](Paint/Register-scrap.png)
4. Overlay the [24 × 24 wool repeat](Paint/Wool-repeat.png) at its native scale. Pale picks use alpha 16/255 and dark picks 18/255. A repeat spans about 22 mm down the hanging panel and about 20 mm along the sleeve. Make motif or wear edits on their own layers before compositing the low-contrast weave. [3 × 3 repeat](Review/Wool-3x3.png) · [Reduced 256 px atlas on the garment](Review/Atlas-256.png)

## Visual evidence and provenance

The Nightcap character plate supplied the angular jaw, indigo and copper relationship, side-swept ivory bob and single braid with two bindings. In the matched Hailstone DAF captures, the ear emerges around brow height, the pale temple frames the dark eye socket and the jaw remains visible over a close collar. The Nightcap head extends the pinna farther laterally, sweeps the hair diagonally over one temple and leaves visible neck above the yoke. The aligned local comparison is in `dark-elf-reference-local-20261124/silt-reader-eye-line.jpg` at the workspace root. [Front and profile landmarks](Review/Head-landmarks.png) · [Restored head in profile](Review/Head-profile.png)

The dated RoF2 PFS lookup verified all five original-byte SHA-256 values listed in the [study notes](../../../../systems-planning/docs/art/female-dark-elf-robe-reference.md). The four cloak swatches informed the relative widths of a field and its border. The DAF face swatch and assembled viewer informed light/dark grouping. The wrap cut, back pleat, plummet, flood tally, stain, repair and final paint are original to Silt Reader. Source reference images stay in the local study area.

The clay and reversed-key frames show the brow, eye socket, jaw and ear thickness under different lighting. The unlit frames isolate the atlas color and individual materials. In the 128 px studies the copper and needlework shrink first. The ivory head, pale cuff pair, vertical wrap edge and clay slit retain their positions. [Clay](Review/Head-clay.png) · [Reversed key](Review/Reversed-key.png) · [Unlit](Review/Unlit.png) · [Hem with back faces culled](Review/Hem-culling.png) · [Gameplay thumbnail](Review/Gameplay-128.png) · [Local color, value and cool key](Review/Palette-128.png)

## Rebuild

From the character-production checkout, run `python scripts/silt_reader_paint.py`, then run Blender 5.2 in background mode with `--python-exit-code 1 -P scripts/build_silt_reader.py`. The build opens the starter equipment file, immediately saves a work copy, then writes the sculpt, maps, measurements and FBX. Run Blender again with `-P scripts/review_silt_reader.py` for the independent reimport check and with `-P scripts/review_silt_reader.py -- --render` for the camera views. Run `python scripts/silt_reader_folio.py` to compose the review plates. [Build](../../../scripts/build_silt_reader.py) · [Verification](../../../scripts/review_silt_reader.py)
