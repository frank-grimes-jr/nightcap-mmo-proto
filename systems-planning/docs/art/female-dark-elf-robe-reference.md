# Female Dark Elf robe · reference observations

**November 25, 2026.** For use with the [Blender](female-dark-elf-blender-prompt.md) and [Unity](female-dark-elf-unity-prompt.md) assignments. The captured character and texture previews stay in the local reference workspace. Author new race geometry, garment panels, dye fields and motifs for Nightcap.

## What the dressed figure shows

The local Hailstone model viewer rendered race 6, female (`DAF`), with armor material 10 and helmet hidden. Two runs used the same heading (32), camera position (15, 0, 0.6), look (180°, 0°), animation sample and frame count. Only the requested lighting preset changed. Compare the [classic capture](C:/nightcap-development-mmo/dark-elf-reference-local-20261124/robe-viewer/screenshots/robe-classic.png) and [modern capture](C:/nightcap-development-mmo/dark-elf-reference-local-20261124/robe-viewer/screenshots/robe-modern.png).

At the captured distance the white hair frames the dark face, the sleeves separate from the waist, and the light front opening and hem carry the garment's silhouette. The lighting difference is modest against this neutral viewer backdrop. Both images show a slim ankle-length garment with a long vertical field of color. For Nightcap, retain the readable grouping and change the garment cut, placement of the accent, motif and palette. The actual model and race selector establish the dressed appearance; the two frames do not isolate individual shader terms or establish an active replacement texture pack.

## What the archive shows

Followed the installed Lantern workflow (`nightcap-eq-texture-reference`). Its environment manifest yielded no matching EQ robe or DAF entries. Used the skill's RoF2 PFS reader on the local viewer client rather than a Trilogy intermediate export. The selected archive was `E:/EQ_Local_Dev/artifacts/cairnwright-creation-20261121/client/global_chr.s3d`. Identified the format from the decoded bytes. The fold and border observations below describe the inspected swatches. Exact polygon-to-texture assignments have not been traced. [Local swatch sheet](C:/nightcap-development-mmo/dark-elf-reference-local-20261124/female-robe-references.jpg)

| Entry | Format and size | Observed feature | SHA-256 of original bytes |
| --- | --- | --- | --- |
| `clk0401.bmp` | BMP 64 × 128 | Large red field, narrow bright border and contrasting lower strip. | `7951b7f41166d0ad25bdd3bb262a3b4704a4601ae7f959859321f40004ed5b66` |
| `clk0404.bmp` | BMP 32 × 64 | Fine line of detail above a much broader flat terminal band. | `0ccc06b3ce7216258b92cb9f7ced73d675e1cbad9df52953a1bfd30c5f19ae98` |
| `clk0701.bmp` | BMP 64 × 128 | A broad cyan field carries soft vertical folds; a darker edge anchors it. | `926414f1861de8fb44a391f63a30eebe56d339f6344fc73bb521f9359e151794` |
| `clk0704.bmp` | BMP 32 × 64 | Blue folds stop at a straight warm band and pale fabric. | `f33b89e2030a5b65c5856a07df1186cca66a8fe12169cf2353dd276f8dbba2db` |
| `dafhe0001.bmp` | BMP 64 × 64 | Light hairline, cool dark face and small high-contrast eye accents. | `321d6dce29292aa2363f41876488f4aebc04e6318704f1f62adc47b189ca9a10` |

## What Hailstone does in the reviewed client source

The inspected checkout is the source beside the November Cairnwright preview build. The Unity assignment translates observations into tests using Nightcap's existing shader. It requires no Hailstone shader code or compatible GPU texture layout.

| Source | Behavior in the reviewed path | Consequence for robe authoring |
| --- | --- | --- |
| [Actor vertex shader](E:/EQ_Local_Dev/artifacts/cairnwright-creation-20261121/hailstone-client/shaders/actor.vert:72) | Transforms normals with the bones. Computes a gentle directional term for the classic path and passes the normal onward. | Test the shoulder, cheek and skirt with flat color before adding ornament. A seam in normals can look like a painted stripe. |
| [Modern actor lighting](E:/EQ_Local_Dev/artifacts/cairnwright-creation-20261121/hailstone-client/shaders/actor.frag:182) | Evaluates a wrapped per-pixel directional term using a 0.3 wrap, shadow visibility, sky/ground illumination, probe contribution and nearby local lights. Applies a configurable lower light bound before modulating linearized base color. | Keep broad fold normals and readable midtones. Compare a cool ambient setup with a local warm light; check the far cuff still falls into shadow. |
| [Surface shine](E:/EQ_Local_Dev/artifacts/cairnwright-creation-20261121/hailstone-client/shaders/actor.frag:90) | Surface flags select directional gloss and an optional environment response. Native armor normals can take precedence over a texture-pack normal. | Wool can stay matte. Give a brass clasp or glazed tile its own response only if the highlight improves the silhouette or material distinction. |
| [Offline texture-pack tool](E:/EQ_Local_Dev/artifacts/cairnwright-creation-20261121/hailstone-client/tools/texpack/upscale.py:1) | The default color workflow runs an upscale model and resolves its output to 2× source size. Masked variants and optional normal and roughness maps are separate outputs. | Paint and test the original robe at its intended texel density. Use mipmaps and broad color masses to keep it legible. Enlargement alone does not produce the observed light response. |

The modern viewer log reported 4× MSAA, FSR1 at render scale 1.00 and zero exposure offset. This is a native-scale offline character comparison. For reproducibility, the reviewed `actor.frag` hashes to `9b9f7d817eb70e287cfef60ed29ccf51745e5d100895010705e7b51e7aa9326d` and `upscale.py` to `fd1dc43a5b4e50bc9fc271329f2e4acffe64d9e6f19919c02d335ea0255b5aff`.
