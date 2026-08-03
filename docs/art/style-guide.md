# Art and Rendering Direction

## Status

Exploring, 2026-08-02.

Nothing in this document is an approved final art style.

## Current direction

- Fully polygonal 3D world with free camera movement and zoom.
- Technical simplicity comparable to early polygonal MMORPGs, without copying their protected designs.
- Visible polygons are acceptable.
- Low-resolution, hand-painted textures are preferred over photographic materials.
- Realistic or grounded proportions rather than cartoon exaggeration.
- Sparse environments use scale, silhouette, color, fog, sound, and landmark composition to create breadth.
- Visual richness should come from art direction rather than expensive rendering features.

## Performance principles

- Integrated graphics support is a product requirement.
- Establish representative minimum hardware before production art begins.
- Define triangle, material, texture-memory, animation, particle, lighting, shadow, draw-call, and streaming budgets through profiling rather than intuition.
- Prefer simple diffuse materials, limited dynamic lights, limited shadows, baked or authored lighting, level of detail, billboards, impostors, instancing, occlusion, and regional streaming.
- Validate normal gameplay views, not only staged screenshots.

## Concept-art rule

Concept art communicates mood and direction; it does not prove production feasibility. Every proposed visual anchor must identify:

- Which elements are real-time geometry.
- Which elements are textures, billboards, sky, fog, or impostors.
- Which lighting is dynamic versus baked or painted.
- Expected asset-production effort.
- Expected target-hardware cost.

## Rejected or cautioned directions

- Fixed-camera 2.5D as the primary gameplay presentation: conflicts with the desired spatial exploration.
- Cartoon exaggeration: does not match the desired grounded tone.
- Modern AAA or ESO-like realism: too expensive and visually farther from the desired identity.
- Treating polished generated concept art as an achievable gameplay screenshot without verification.

## Originality boundary

Do not recreate recognizable EverQuest races, armor, creatures, locations, architecture, symbols, textures, interfaces, or other expression. Preserve only abstract qualities such as danger, scale, mystery, sparse wilderness, and readable low-poly form.
