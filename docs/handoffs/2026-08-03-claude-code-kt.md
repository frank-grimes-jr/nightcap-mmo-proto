# Claude Code Knowledge Transfer - 2026-08-03

## Purpose and authority

This document is a restart aid for Claude Code. It is not a new source of design authority and does not change any decision status. If this summary conflicts with the repository, follow the canonical files linked below and report the discrepancy before proceeding.

This remains a design-and-discovery session. The handoff does **not** authorize application scaffolding, engine selection, dependency installation, implementation, deployment, purchases, or remote Git operations.

## Required resume sequence

1. Read [CLAUDE.md](../../CLAUDE.md) and [WORKING_AGREEMENT.md](../../WORKING_AGREEMENT.md) completely.
2. Inspect the available installed and project-local skills. Follow the agreement's mandatory skill-first workflow and read every selected skill file completely.
3. Read only the canonical and player-facing documents relevant to the next design question.
4. Inspect Git status, branch topology, and remote-tracking state read-only. Report any difference from the snapshot below before changing files.
5. Briefly confirm the project context and repository state.
6. Resume the one-question-at-a-time design interview at the unanswered question in this handoff. Do not infer its answer.

## Repository snapshot

Snapshot verified after `git fetch --prune origin` on 2026-08-03, immediately before creating this handoff commit:

- Repository: `C:\nightcap-development-mmo`
- Canonical remote: `https://github.com/frank-grimes-jr/nightcap-mmo-proto.git`
- Working tree: clean
- Design branch: local `dev`
- Latest design commit: `38525a0` (`docs: allow field augment installation`)
- Remote `dev`, `test`, and `main`: `393b973`
- Local `test` and `main`: `393b973`
- Local `dev` was three commits ahead of `origin/dev` with no remote divergence.
- This handoff's documentation commit will sit on top of those design commits after it is fast-forwarded into local `dev`; verify the resulting `HEAD` rather than assuming a hash.

The three unpushed design commits are:

1. `33485f0` - `docs: allow rare multi-family augments`
2. `7d33da0` - `docs: equalize multi-family augment power`
3. `38525a0` - `docs: allow field augment installation`

Do not discard, rewrite, or assume these commits are already on GitHub. No push or promotion to `test` or `main` is authorized by this handoff.

Git may emit a non-blocking warning that it cannot access `C:\Users\verre\.config\git\ignore`. Repository commands have otherwise succeeded. Use `-c safe.directory=C:/nightcap-development-mmo` for Git commands. Network Git operations, when explicitly authorized, must use `-c http.sslVerify=true`.

## Source map

- Collaboration, skills, approvals, and branch flow: [WORKING_AGREEMENT.md](../../WORKING_AGREEMENT.md)
- Product vision: [vision.md](../design/vision.md)
- Canonical decision statuses: [decisions.md](../design/decisions.md)
- Unresolved design: [open-questions.md](../design/open-questions.md)
- Player-facing explanations: [wiki index](../wiki/README.md)
- Visual direction and feasibility limits: [style-guide.md](../art/style-guide.md)
- Lore canon and unresolved worldbuilding: [structure.md](../lore/structure.md)
- Significant history: [CHANGES.md](../../CHANGES.md)

## Project identity and non-negotiable boundaries

- Build an original, ground-up MMORPG. Do not copy protected expression, assets, data, lore, names, characters, creatures, interfaces, maps, symbols, or code from EverQuest or any other game.
- The emotional center is early-MMORPG danger, earned competence, mystery, memorable towns, meaningful exploration, and the feeling of inhabiting a new world.
- Modernize controls and feedback without making the world automatically safe.
- Every required activity, including end-game dungeon encounters, must be completable solo. Solo play is the baseline, not a hindered fallback.
- Optional grouping increases encounter difficulty and qualifying-player experience. Exact scaling remains TBD.
- The intended initial audience is a small invited community, with a path to later public scale.
- No engine, language, database, network protocol, build system, deployment platform, or maximum level is confirmed.
- The client will eventually be untrusted and persistent gameplay state server-authoritative, but no technical architecture is approved.

## Presentation direction

- Fully polygonal 3D with free first-person and scroll-wheel-controlled third-person camera distances.
- Explore approximately early polygonal-MMORPG technical simplicity: low-poly geometry, low-resolution painted textures, simple lighting, fog, sparse large zones, and strong landmarks.
- Integrated graphics support is a product requirement.
- Concept art is mood guidance, never proof of an achievable runtime target.
- The final art style remains Exploring rather than approved.

## Compact canonical decision ledger

The canonical wording and status always live in [decisions.md](../design/decisions.md).

- **D-001, Provisional:** fully 3D, low-spec presentation.
- **D-002, Provisional:** all required content is solo-capable; grouped dungeon play is harder and gives each qualifying member an experience premium.
- **D-003, Provisional:** respawn with gear and inventory; lose experience and may de-level; each corpse retains that death's lost experience for recovery within 48 real-time hours.
- **D-004, Provisional:** one fixed, non-obvious, discoverable waypoint per zone, activated by standing on it.
- **D-005, Provisional:** a dungeon waypoint works only after normal entry into the player's instance.
- **D-006, Provisional:** quest guidance is closer to World of Warcraft clarity than early EverQuest ambiguity; exact guidance remains TBD.
- **D-007, Provisional:** skills improve through use within level or level-band caps, with failure rates decreasing toward the cap.
- **D-008, Confirmed:** original intellectual property and original expression throughout.
- **D-009, Provisional:** small invited initial community; early success means engagement, independent progression, and self-earned dungeon access.
- **D-010, Provisional:** low-level dungeons unlock through discovery; higher-level dungeons use access-key quests; unlocks are account-wide but every participating account needs its own access.
- **D-011, Provisional:** ordinary open-world enemies never scale by participation; only designated world bosses use locked, role-aware enrollment that can raise but never lower active-attempt difficulty.
- **D-012, Provisional:** three distinct classes per character: permanent full-kit primary, stronger secondary subset, weaker tertiary subset; shared slower parallel-advancement pool; gated safe-location subclass replacement refunds the replaced subclass's allocated points.
- **D-013, Provisional:** primary class controls armor and weapon eligibility; fixed authored equipment may support any class slot through functional statistics; hybrid items, accessories, and limited typed augments support cross-role builds within fixed item power budgets.

## Current design focus: equipment and augments

The authoritative details are in [D-013](../design/decisions.md#d-013-hybrid-equipment-support), with the derived player explanation in [Equipment and Itemization](../wiki/equipment-and-itemization.md).

Current Provisional rules:

- Loot is authored and fixed, not personalized or adaptively generated for the finder.
- Specialized hybrid items are fixed world discoveries.
- Accessories provide broad cross-role support.
- Augments are a secondary correction or specialization mechanism and should not replace naturally specialized equipment.
- Selected items may have multiple sockets; each socket holds at most one augment.
- Each socket declares a broad equipment-family type, and the augment must support that family.
- Compatibility uses coherent broad families rather than arbitrary per-item lists. Jewelry covering necklaces, rings, and earrings is only a provisional example, not final terminology.
- Most augments support one family. Rare augments may support multiple families.
- A comparable rare multi-family augment is as powerful as a single-family augment; broader compatibility does not impose a statistical penalty.
- Compatible augments may be installed anywhere while the character is out of combat. Installation does not require a safe-location service.
- Intact augment removal requires a designated safe-location service and either in-game currency or one prepaid service token.
- Service tokens are bought only with in-game currency, stored for later use, shared across the account, account-bound, and non-tradable. There is no real-money purchase path.

Still TBD within this system:

- Occupied-socket replacement behavior.
- Installation cost, activation time, and interruption behavior.
- Socket maxima and which authored items receive sockets.
- Final compatibility-family names, membership, and permitted multi-family combinations.
- Multi-family augment rarity and sources.
- Exact removal prices, vendors, service locations, token storage limits, and cost scaling.
- Exact augment strength relative to comparable specialization authored directly into an item.
- Equipment categories, statistic vocabulary and weights, accessory rules, hybrid-item frequency, and universal-item rarity.

## Exact restart point

The user answered the previous question with:

> You can install anywhere outside of combat.

That answer is documented and committed. The next question was asked but **not answered** because the user requested this handoff:

> If a socket is occupied, may the player overwrite its augment in the field--destroying the old augment--or must they use the safe-location removal service first?

The prior assistant guessed that field overwrite should be allowed while out of combat and should destroy the old augment, leaving the paid service valuable because it preserves the augment. That guess is **not a decision**. Present the question again with the guess clearly labeled, then wait for the user's answer.

## Other notable future design work

- The user wants original class design addressed later; existing class names used conversationally were mechanical references only and are not candidates for final names or lore.
- A future reputation/faction system is desired and may create both player problems and rewards, but its rules are not yet defined canonically.
- Dungeon scaling values, open-world boss thresholds, parallel-advancement balance, death edge cases, waypoint economics, quest guidance, lore, and the entire technical stack remain unresolved.
- Use [open-questions.md](../design/open-questions.md) rather than reconstructing unresolved work from conversation history.

## Expected collaboration pattern

- Continue the design interview one focused question at a time, with a concise guess attached.
- Treat new answers as Provisional unless the user explicitly assigns another status.
- Never silently fill gaps or promote a decision to Confirmed.
- When a coherent answer changes the design, update the canonical decision, relevant open questions, the corresponding player wiki page, and `CHANGES.md` together.
- Use a focused `feature/<name>` branch based on local `dev`, validate and review the documentation, commit atomically, and fast-forward local `dev`.
- Do not push, promote to `test`, or promote to `main` without the applicable authority. Promotion from `test` to `main` always requires explicit user sign-off.
- Do not scaffold or implement game code until an approved specification and acceptance criteria exist.

## Documentation verification used in this phase

For documentation-only changes, the project has used:

- `git diff --check`
- Relative Markdown-link resolution across the repository
- Verification that every player-facing wiki system page declares a design status
- Targeted searches for stale resolved questions and required new wording
- Credential-like string scans of staged diffs
- Five-axis review, with code-only security and performance checks marked not applicable where appropriate

There is no application build or automated runtime test suite because no implementation stack exists.
