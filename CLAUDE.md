# CLAUDE.md

This file provides Claude Code-specific entry guidance for Nightcap Development MMO.

## Required first reads

Before taking project actions:

1. Read `WORKING_AGREEMENT.md` completely. It is the canonical authority for workflow, skills, approvals, documentation, testing, and branch flow.
2. Read only the relevant material under `docs/` for the current task.
3. Inspect the user's installed skills and project-local skills, then follow the mandatory skill-first workflow in the working agreement.

## Current state

- Phase: design and discovery.
- No engine, programming language, database, network protocol, build system, or deployment platform is confirmed.
- Do not scaffold application code until a relevant specification and acceptance criteria are approved.
- Current design statements are tracked in `docs/design/decisions.md` with explicit statuses.

## Skill rules

- Use the available skill-discovery workflow before development work.
- Read selected skill instructions completely before acting.
- User-named skills are mandatory and must appear in the plan.
- Apply the minimum code-change workflow defined in `WORKING_AGREEMENT.md`.
- If a required skill is unavailable, say so and use the safest fallback; never silently skip it.

## Sources of truth

- Collaboration and delivery: `WORKING_AGREEMENT.md`
- Product vision: `docs/design/vision.md`
- Decision status: `docs/design/decisions.md`
- Unresolved design: `docs/design/open-questions.md`
- Player-facing design explanations: `docs/wiki/`
- Visual direction: `docs/art/style-guide.md`
- Lore canon: `docs/lore/structure.md`
- Significant history: `CHANGES.md`

Update these documents as decisions are made. Do not duplicate their contents into this file.
