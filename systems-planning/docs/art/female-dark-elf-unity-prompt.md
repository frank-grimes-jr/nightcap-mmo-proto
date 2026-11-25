# Unity production prompt · Female Dark Elf robe review

Use after the [Blender production assignment](female-dark-elf-blender-prompt.md). Build a reusable skinned prefab and static review scene from the delivered robe. Default to Silt Reader. Render the Kiln Oracle or Mourning Veil only if that outfit was delivered. Paths beginning with a workspace folder resolve from `C:/nightcap-development-mmo/`.

## Establish the import

1. Open `character-production/unity-validation/` using its pinned Unity 6000.5.7f1 Built-In editor. Inspect `Assets/NightcapHumans/Female_FieldHuman.fbx` and its importer for the project's accepted female mapping. The separate Lantern importer is an EQ reference tool with its own editor and render pipeline. Use the Nightcap project for this character.
2. Read `character-production/output/dark-elf-female/<robe>/handoff.md`. Take `DarkElfFemale.fbx` and the flattened runtime maps from that directory. Use a new folder at `Assets/NightcapDarkElfFemale/<robe>/` for model, textures, materials, prefab and review scene. Make the prefab self-contained within the project, without references to a working drive containing game archives or a paint program's file cache.
3. Import with file units and scale factor 1. Compare the actual barefoot crown height to the Blender handoff; the female base starts at 1.70 m. With an identity root, boots should contact the ground, Unity up is +Y and forward is +Z. Investigate a height discrepancy over 1% against the actual source measurement. Correct axis and scale at the import boundary. Keep the same character scale in all captures.
4. Create a Humanoid Avatar from the imported rig. Keep the hierarchy exposed for inspection, use four skin influences and disable animation import. Compare the hip, spine, clavicle, head, arm, hand, leg and foot mapping to the accepted female. Inspect bind poses and all renderer bone lists. Confirm that every robe and body renderer resolves to the same skeleton within that instance. If an Animator remains for its Avatar, leave the controller empty and root motion off. Verify a stationary, complete character in Edit and Play.
5. Preserve authored normals and UV0. Match tangent handling to the Blender bake if a normal map was actually delivered. Remap each named material slot deliberately. Check the rear yoke and lining with backface culling on, the face under the hair, mirrored ears, and normals on the turned cuffs. Set bounds large enough for skirt, sleeve and hairstyle. Check the hem near the camera edge for premature culling.

## Translate Hailstone's visual behavior into the existing renderer

Read the [shader and reference observations](female-dark-elf-robe-reference.md) and view the two local captures side by side. Look for the face above the collar, separation of near and far sleeve, and readable bands on the long skirt. Those relationships are the target for the lighting study. The Hailstone numbers document source behavior, while Nightcap's material settings should be chosen by the result on its own meshes.

| Surface | Starting setup | What to judge |
| --- | --- | --- |
| Skin and ears | Use `Nightcap/Painted Character` with the delivered sRGB skin atlas, white tint and the project's accepted starting material values of diffuse wrap 0.35 and indirect gain 1.5. Use the source normal for broad, stable cheek planes. | Both eyelids read under the brow. Ear rim and cheek remain distinguishable from hair and collar under cool fill. Keep skin responsive to shadow. |
| Dyed outer cloth | Use the same opaque painted shader with mipmapped sRGB albedo. The shader exposes painted albedo, tint, wrap and indirect gain. Use the source mesh normals to light the large folds. | A broad fold has a visible crest, a middle tone and a cooler trough. Dark green or indigo should retain its dye identity in shade. The surface stays matte when the key moves. |
| Lining and embroidery | Use authored atlas regions and identical UV placement across editor and export. Preserve color separation through material value and weave scale. Only split a material if it has a distinct lighting requirement. | A cuff remains attached to a sleeve in silhouette. The interior of a slit has thickness and lining. At half distance the larger trim rhythm survives after stitches disappear. |
| Brass weight, fastener or ceramic | Start with painted broad highlights. If the delivered hard accessory needs view-dependent gloss, use a dedicated local Built-In material on that slot. Keep the highlight controlled against the adjacent fabric. | Metal or glaze catches a tighter highlight than wool. With the light reversed the hardware has a believable turn and the robe still accepts cast shadows. |

The painted shader's inputs do not include roughness, normal or emission maps. Assign optional maps only to a compatible material and record their purpose. Import base color as sRGB, scalar data as linear and true tangent normals as Normal Map. Preserve the authored resolution on first inspection, enable mipmaps, then test the intended compression. Pixel-level source detail should simplify naturally into the broad shapes. Inspect for pale halos around the hair, dyed edges bleeding into lining, striped moiré and flat skirt panels that turn glossy under a point light.

## Assemble the expected states

- **Base body.** Show eyes, brows, hair, complete character and practical underlayer. Verify skin on the back of the neck, wrists, ankles and at the ear roots. Compare the profile directly against the Blender head rather than trying to grade the portrait against a game screenshot.
- **Robed character.** Enable the robe, lining, cuffs, belt and selected accessories according to the handoff. Hide only documented body sections underneath. With the same instance and skeleton, restore the base state and switch back. Confirm the side slit still shows the intended underlayer and both boots sit correctly. Keep the selected outfit active in the saved prefab.
- **Diagnostic view.** Create a scene-only material override or duplicate the scene instance for flat tint and unlit albedo checks. The flat view reveals construction and normals. The unlit view reveals seam alignment and whether a directional studio shadow was accidentally painted into the atlas. Restore production materials on the saved prefab.

## Build a repeatable lighting comparison

Create `DarkElfFemale_RobeReview.unity`. Use a matte floor, neutral backdrop and fixed cameras external to the prefab. Capture front three-quarter, side, rear, face/collar and the robe at about 128 screen pixels from crown to floor. Record resolution, camera, projection or FOV, lighting settings and active outfit. Reuse camera transforms between lighting states. Keep exposure, color management and framing fixed for each comparison.

| Condition | Setup and observable acceptance |
| --- | --- |
| Neutral diffuse | Neutral three-quarter key and subdued fill. Check dye color against the Blender render and a small unlit atlas sample. The strongest edge contrast should occur where the character design asks for it, usually near face, collar or turned cuff. |
| Reversed key | Move just the key to the opposite side. The sleeve and skirt folds should visibly turn with it. Embroidery and the dyed flood marks stay on the same panels. If a hard shadow remains on the originally dark side, compare unlit albedo and source paint layers. |
| Cool dusk and local warm light | Use dim cool ambient fill, a warm point near one side, and ordinary shadows. Keep post effects off for the check. The near cuff warms first; the far hem should remain quiet. Tune scene fill or local material response until the hand and face stay readable while the far sleeve is visibly darker. Self-lit cloth or a glowing face fails this check. |
| Distance and mips | Frame the whole figure at the recorded small size. Silt Reader should retain its diagonal wrap and clay opening; Kiln Oracle its high pale collar and orange strip; Mourning Veil its pale capelet over a dark bell. Inspect border breakup, shimmer and silhouette from front and rear. Measure the on-screen figure height in the saved image. |

When a comparison fails, isolate the cause. A bright cuff that crosses a seam in **unlit** view is an atlas or UV issue. A smooth gradient that abruptly reverses under a moving light is a normals issue. A vanished lining seen from inside the slit is a geometry, material assignment or culling issue. A bright glyph that persists under every light needs a paint-layer and shader check. Photograph matched frames before and after each material change.

## Handback

Save and reopen the scene, reimport the FBX and inspect the prefab in a fresh empty scene. Confirm persistent material bindings, one skeleton per character, a usable Avatar, zero motion clips, no missing textures, and no importer or shader errors attributable to these assets. Deliver the prefab, scene, dependencies and metadata, alongside the base/robed and three-light review frames. Record measured height, triangles, skinned renderers, bones, texture dimensions, compression and material count. Include a screenshot at garment scale that demonstrates one original motif wrapping onto the intended seam.

The result to accept is one complete, static, skinned Nightcap character and an original robe material another artist can rebuild from its recipe. Report visual limitations at close range or distance and defer movement, cloth simulation and runtime performance claims until those are tested.
