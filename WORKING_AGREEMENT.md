# Nightcap Development MMO Working Agreement

This is the canonical working agreement for every human and AI contributor to this project. Tool-specific files such as `AGENTS.md` and `CLAUDE.md` must point here rather than duplicating these rules.

## Project phase

The project is currently in design and discovery. Do not treat a conversation, concept image, or prototype as a permanent commitment.

Every material design statement must be classified as one of:

- **Exploring**: alternatives are still being generated and compared.
- **Provisional**: the current working direction; safe to prototype, but inexpensive to change.
- **Confirmed**: accepted as a baseline; changing it requires documenting the consequences.
- **Implemented**: exists in the product and has verification evidence.

When status is unclear, treat the decision as exploring. Never silently promote a decision to confirmed.

## Skill-first development is mandatory

The user's installed and project-local skills are required development workflows, not optional suggestions.

Before any development task, the agent must:

1. Load the available skill catalog and use `using-agent-skills` or the closest available skill-discovery workflow.
2. Identify the smallest set of skills that applies to the task.
3. Read each selected `SKILL.md` completely before taking task actions.
4. Announce which skills are being used and why.
5. Add any skill explicitly named by the user to the working plan.
6. Follow each selected skill through its verification requirements.

If a required skill is unavailable or unreadable, state that plainly and use the safest reasonable fallback. Never claim to have followed a skill that was not loaded.

### Minimum workflow for code changes

Every code change must use, at minimum:

- `using-agent-skills` (or equivalent skill discovery)
- the relevant task skill, such as `spec-driven-development`, `debugging-and-error-recovery`, `frontend-ui-engineering`, or `api-and-interface-design`
- `test-driven-development` for new logic, bug fixes, or behavior changes
- `code-review-and-quality` before merge
- `git-workflow-and-versioning` for branch and commit hygiene

Apply additional skills when their triggers match. Common examples include:

- `idea-refine` and `interview-me` while intent is unclear
- `planning-and-task-breakdown` before multi-part implementation
- `context-engineering` when establishing or changing project context
- `source-driven-development` when framework or library behavior matters
- `incremental-implementation` when more than one file is affected
- `security-and-hardening` for untrusted input, authentication, persistence, or external services
- `performance-optimization` when client, server, database, or network budgets matter
- `observability-and-instrumentation` for production-running systems
- `code-simplification` after behavior is correct
- `documentation-and-adrs` for durable decisions and public contracts
- `shipping-and-launch` before production release

Skills do not override the user's instructions, this agreement, repository-local rules, or safety boundaries. When instructions conflict, surface the conflict rather than guessing.

## Assumptions and ambiguity

Before non-trivial implementation, state material assumptions about requirements, architecture, and scope. If an unanswered question would meaningfully change the result, stop and present two or three options with tradeoffs.

Do not invent product requirements merely to keep coding. Design ambiguity belongs in `docs/design/open-questions.md` until resolved.

## Branch flow

`feature/<name>` -> `dev` -> `test` -> `main`

- **feature branch**: temporary; one system or feature per branch.
- **dev**: agents may merge here after relevant automated verification passes.
- **test**: pause for user-run manual in-game QA. Every promotion must include exact QA steps, locations, actors, inputs, and expected results.
- **main**: promotion requires explicit user sign-off after manual QA.

Agents may create commits, open pull requests, and merge autonomously up to `test` when tests pass and no external approval boundary is crossed. `test` to `main` always requires user approval.

## Commits and pull requests

- Keep commits and pull requests small and reviewable.
- One system or coherent behavior change per commit.
- Behavior changes require tests.
- Do not mix unrelated cleanup with requested work.
- Explain alternatives and tradeoffs when a choice was ambiguous.
- Never commit secrets, credentials, generated private keys, or local environment files.

## Definition of done

A change is not complete until the applicable evidence exists:

- Acceptance criteria are satisfied.
- Automated tests pass.
- The behavior is verified at runtime where practical.
- Relevant security and performance risks have been considered.
- No known regression is left unexplained.
- Documentation and ADRs are current.
- `CHANGES.md` is updated for significant behavior, schema, content, tooling, infrastructure, or visual-pipeline changes.
- Manual QA instructions are supplied for promotion to `test`.

## Documentation duties

- Keep `WORKING_AGREEMENT.md`, `AGENTS.md`, and `CLAUDE.md` accurate.
- Record expensive-to-reverse technical choices as ADRs in `docs/adr/`.
- Maintain design state in `docs/design/` and never present provisional decisions as confirmed.
- Maintain player-facing system explanations in `docs/wiki/`. When a design is coherent enough to explain without inventing unresolved behavior, create or update its wiki page in the same change as the canonical design record.
- Treat wiki pages as derived explanations rather than decision authority. Every page must state its design status, identify unresolved details as TBD, and remain consistent with `docs/design/`, `docs/lore/`, and `docs/art/`.
- End each development phase with `docs/milestones/phase-N-report.md`, including what was built, cut, deferred, and considered risky.
- Maintain world canon and unresolved lore in `docs/lore/structure.md`.
- Maintain the visual target, production constraints, and rejected directions in `docs/art/style-guide.md`.
- Put the newest `CHANGES.md` entry at the top.

## Product boundaries

- This is an original property. Do not copy names, lore, locations, characters, creatures, symbols, interfaces, source code, data, models, textures, sounds, quests, maps, or other protected expression from EverQuest or any other game.
- Inspiration may preserve abstract qualities such as danger, mystery, earned mastery, readable low-poly geometry, large zones, and meaningful travel.
- Performance budgets are product requirements. Do not defer low-spec validation until the end.
- Concept art is not an in-engine performance claim. Every proposed visual target must be assessed for production cost and target-hardware feasibility.
- The client is untrusted. Persistent state, combat outcomes, inventory, currency, trade, and progression must be server-authoritative.
- Back up persistent data before destructive schema or data operations.
- Do not make production deployments, purchases, external announcements, destructive operations, or irreversible migrations without explicit authority.

## Simplicity and scope

Prefer the smallest vertical slice that tests the current assumption. Avoid premature microservices, orchestration platforms, abstraction layers, content volume, and rendering features.

Build the world one coherent, testable slice at a time.
