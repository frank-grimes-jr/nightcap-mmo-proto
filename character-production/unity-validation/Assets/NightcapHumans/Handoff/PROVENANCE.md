# Character source notes

The human foundation uses MPFB 2.0.17 CC0 topology and shape targets, customized with saved male/female profiles. It is not a claim of base topology modeled from scratch. The user explicitly suggested MPFB after rejecting earlier character sources. Neither Man_Mesh.FBX, Basic Bandit nor the rejected mannequin supplies geometry to these characters.

MPFB source release: https://github.com/makehumancommunity/mpfb2/releases/tag/v2.0.17 . A byte-for-byte copy of that source distribution's LICENSE.md is included as MPFB-LICENSE.md; consult it for the distinction between tool source code, bundled assets and output. The MPFB add-on code is not included in this Unity package.

Hair, base clothing, boots and starter equipment were authored in the local character project. Character surface painting includes generated/repainted skin, facial, clothing and hair textures, applied to the authored UV layouts. Original starter equipment geometry was fitted to the accepted character pair and weighted to their existing rigs.

Leather, iron and oak reuse the user's approved Nightcap texture studies. Those materials were generated/repainted using EQ/WoW visual references for palette and readability. They are reference-guided designs; combining or repainting textures does not establish independent provenance by itself. Historical extraction labels and generation records remain in the texture-lab project. No raw EQ/WoW texture archive is bundled here.

Detailed source paths, hashes and painting records are retained in the character-production worktree's `textures/approved-material-sources.json`, `textures/*PROVENANCE.json` and the texture-lab `unity/Assets/NightcapTextureStudy/PROVENANCE.md`. This handoff records origins; it does not assign a new blanket license to the whole package.
