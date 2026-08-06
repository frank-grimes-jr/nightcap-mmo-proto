# Class Roster (Working Canvas)

## Status

**Exploring**, opened 2026-08-05.

This is a deliberately mutable working document. The class roster is expected to change repeatedly — classes will be added, split, merged, renamed, and rebalanced — so this canvas is safe to rewrite freely and is **not** canonical. Only stable structural facts graduate from here into a `docs/design/decisions.md` decision (for example, "the roster is N classes" once that count is actually settled). Until then, nothing on this page is a commitment.

Canonical class structure lives in [D-012: Three-class character identity and parallel advancement](decisions.md#d-012-three-class-character-identity-and-parallel-advancement). This page develops the roster that fills that structure.

## How we build the roster

In layers, each revisable without redoing the ones beneath it:

1. **Guardrails** — the fixed constraints below. Done first so every roster idea can be checked against rails that do not move.
2. **Roster shape** — how many classes, and the archetype/role space they need to cover.
3. **Per-class identity** — each class's fantasy, primary-kit role, and subclass contribution, one at a time.

## Guardrails: what every class must satisfy

These come from decisions already made. They constrain every class on this page and are not up for revision here — if one needs to change, that happens in its source decision, not on this canvas.

### From D-012 — three-class identity

- Every class must work in two forms: as a **permanent primary** granting its complete ability set, and as a **curated subclass subset** when chosen as someone else's secondary or tertiary.
- The secondary form must be mechanically stronger than the tertiary form, so each class needs a sensible "stronger subset" and "more limited subset," not just an all-or-nothing kit.
- Primary, secondary, and tertiary are always three distinct classes; no class occupies two slots on one character.
- Each class has dedicated parallel-advancement options that enhance its abilities, allocable from one shared character-wide point pool.

### From D-014 — equipment eligibility

- A class's **armor chassis** eligibility is one of three tiers (light / medium / heavy-style), and the class may wear its own tier or any lighter one. The primary class alone sets this ceiling.
- A class's **weapon** eligibility is expressed as specific weapon types that roll up into weapon groups (groups drive skill and augment-family compatibility). The primary class alone sets weapon eligibility.
- Subclasses never expand armor or weapon eligibility.

### From D-015 — functional statistics

- A class's needs are expressed in **role-based functional buckets** (offense, defense, control, sustain, utility) rather than class-coded stats. There is no strength/intelligence attribute layer.
- **Every class must have a solo-facing expression.** Whatever a class does in a group, it must also have a self-directed form (self-sustain, self-protection, personal control/utility) so it can stand alone.

### From D-002 — solo-capable

- Every class must be able to complete all required content, including end-game dungeon encounters, solo. No class may depend on a group to function.

### From D-007 — skills

- Class abilities and weapon skills improve through relevant use, with caps tied to the character's level band.

### From D-008 — original IP

- All class names, lore, and ability designs must be original. Any resemblance to existing games' classes is mechanical shorthand for discussion only and is never a candidate for final names or designs.

## Design principles (what we do better than the reference)

EverQuest's archetypes are the analytical reference (shorthand only, per D-008). These principles capture the lessons we are deliberately applying differently. They are the roster's north star; every class is checked against them.

1. **The three-class system is the fix for role-lock pain.** The reference's worst problems — a tank with no toolkit, a healer who cannot solo, a nuker who can only nuke — all came from being locked to one class for life. Because our characters combine a primary with a secondary and tertiary (D-012), archetypes are designed with **intentional gaps that subclasses fill**, not as self-sufficient monoliths. This is what makes combining three classes matter rather than merely stacking power.
2. **No mandatory roles, ever.** The reference gated hard content behind must-have healing, crowd control, and slows. That violates solo-capable content (D-002). Support and healing are **force multipliers, never gates**: a group wants them, but no fight ever requires them to be possible.
3. **Every archetype ships with a solo identity — including tank and healer.** This honors the D-015 solo-expression rule at the archetype level. But "solo-capable" (D-002) is a property of the *character*, and a character is always three classes (D-012) — so an archetype's solo identity is its self-directed *baseline*, not full solo-clear power. A character's clearing power comes from its full three-class kit. Tanks get self-sustain and a modest self-directed offensive baseline; healers get real offense.
4. **Differentiate within an archetype by method, not theme.** Classes sharing a role must feel distinct through *how* they perform it (for healers: reactive burst vs. prevention/HoT vs. lifesteal vs. absorb-shields), not merely through cosmetic flavor.
5. **Keep the exciting mechanics, cap their tyranny.** Charm, mez, slow, and shielding stay thrilling, but are designed against must-have status through diminishing returns, solo-scaled potency, and never being the only path through a fight.

## Roster shape

**Four archetypes**, defined by role rather than by melee/caster split:

- **Tank** — holds threat and survives punishment; differentiated by the flavor and toolkit around mitigation.
- **Damage** — primary job is dealing damage; differentiated by damage *pattern* (burst, sustained/damage-over-time, pet-commander, opportunist/execute) rather than by melee vs. caster.
- **Support** — a first-class role of its own (not leftover utility): fundamentally a *controller*, differentiated by control method (lockdown / attrition-debuff / redirection), with ally amplification (haste/buffs/resources) as a shared baseline rather than a class. May produce situational damage spikes but primarily enables others.
- **Healer** — keeps allies alive; differentiated by *method* (reactive big-heals, prevention/heal-over-time, lifesteal/leech, damage-absorb shields), each with its own offensive/solo identity.

How many classes total, and how many sit in each archetype, remain TBD — to be set after or alongside the first per-archetype pass.

## Per-class identity

Developed one archetype at a time. **Tank first**, as the clearest showcase for principle 1 (gaps that subclasses fill).

### Tank archetype

Archetype-level identity, shared by every future tank class, followed by the method axis that differentiates individual tank classes (principle 4).

**Core fantasy.** The immovable body a fight breaks against — gathers danger, absorbs it, refuses to fall. Not a killer; a *foundation* other classes build lethality on top of.

**Threat model — hybrid.** Everyone lives under baseline behavioral aggro (proximity plus threat-over-time from damage/healing). Tanks get strong threat-*biasing* tools — redirect, guard-an-ally, mockery — that heavily influence but never hard-lock a target. A group is far better off with a tank; no fight ever *requires* one (principle 2).

**Spine — what every tank keeps:**

- Survivability.
- Threat control, single **and** multi-target — a tank can gather and hold a pack.
- Modest self-sustain.
- Slow attrition offense, single-target *and* AoE.
- Melee range.

**Deliberate gaps — what a tank-primary lacks so subclasses matter (principle 1):**

- Burst / killing throughput → **Damage** subclass.
- Crowd control (mez / root / charm / hard stun) → **Support** subclass.
- Party healing beyond self-sustain → **Healer** subclass.
- Ranged engagement / reach → a ranged subclass.

**Two-sided value.**

- *Solo-facing* (D-015 solo expression): survivability + self-sustain + slow single-target-and-AoE attrition. Enough to not be helpless in the pre-subclass intro window; nowhere near max-level solo-clear power, which comes from the full three-class kit. Threat tools are essentially inert solo — nothing to redirect when everything already targets you.
- *Group-facing* (the force multiplier, principle 2): the threat-control toolkit. This is *why* a group wants a real tank-primary, and exactly what tank-as-subclass does not grant.

**Tank as someone else's subclass (D-012 curated subset).** Lends *personal* durability only — a defensive/guard cooldown plus passive mitigation — never the group-facing threat toolkit, so a subclass cannot counterfeit a real tank-primary.

- *Secondary form* (stronger): a defensive cooldown + passive mitigation.
- *Tertiary form* (more limited): the thinner passive layer alone.

#### Differentiation: survival method

Individual tank classes are differentiated by **survival method** — *how each refuses to die* (principle 4). This axis is self-facing, so it holds up solo (D-002) and doubles as borrowable durability when the class is slotted as someone else's subclass (personal durability only, per the tank-as-subclass rule above).

Three candidate tank classes, one per method (names TBD, original per D-008):

| Method | Feel / rhythm | As a borrowed subclass, it lends… |
|---|---|---|
| **Flat mitigation** | Armor / block / damage reduction: steady, low-variance "wall," easiest for a group to heal. | passive damage reduction / effective-HP. |
| **Proactive shields / wards** | Pre-loaded absorb pools; rewards anticipation and rotation, caster-flavored. | an absorb-shield cooldown. |
| **Lifesteal bruiser** | Take the hits and heal them back through leech/self-heal; aggressive, sustain by throughput rather than prevention. Kept distinct from the lifesteal *healer* method. | a leech / self-heal on-damage effect. |

**Avoidance is a stat, not a tank class.** Dodge/parry-style avoidance is a defense-bucket statistic (D-015) itemized through accessories and augments (D-014), available to any class. No tank monopolizes it; other archetypes' modest survival bits (e.g. a rogue's small dodge) layer on top of a survival method rather than duplicating a tank.

Two rules follow from the method axis:

- A tank's *as-subclass* durability is **flavored by its method** — the three methods give three different self-protection styles a squishier primary can borrow, which is where much of the three-class combination variety comes from.
- **No method is a strict upgrade of another.** They trade variance, predictability, resource-cost, and aggression, so the choice is a genuine preference rather than a power ranking.

**Still TBD for tanks:** final class count (whether all three ship or the roster trims), names, and each class's stronger-secondary vs. more-limited-tertiary subset shape. Deferred to the roster-shape and per-class layers.

### Healer archetype

Archetype-level identity shared by every future healer class, followed by the method axis that differentiates them (principle 4).

**Core fantasy.** The reason the party is still standing — restores and preserves life. It has real offense of its own, but its throughput is *keeping others alive*, not killing.

**Solo identity — self-sustain attrition.** A healer solos by healing through fights while chipping the enemy down with modest ranged offense: "I outlast you because I out-heal your damage." The mirror of the tank's attrition — safety comes from self-healing rather than mitigation. As with every archetype, this is a self-directed baseline, not full solo-clear power (which comes from the full three-class kit).

**Spine — what every healer keeps:**

- Party healing, single **and** AoE.
- Self-sustain.
- Modest ranged attrition offense.
- Self-tanking via heals — survives its own focus by healing through it, at the opportunity cost of not healing the group meanwhile.

**Deliberate gaps — what a healer-primary lacks so subclasses matter (principle 1):**

- Burst / killing throughput → **Damage** subclass.
- Crowd control (mez / root / charm / hard stun) → **Support** subclass.
- Amplification / buffs (haste, damage buffs, resource support) → **Support** subclass.

Durability under focus and ranged reach are deliberately *not* gaps — the self-sustain identity already covers both. The opportunity cost of self-tanking is what still makes a group want a tank (principle 2: a force multiplier that frees the healer's throughput for the party), without healing ever being required.

**Healer as someone else's subclass (D-012 curated subset).** Lends *self-healing* only — personal sustain to keep the borrower alive — never the throughput to keep a party alive, so a subclass cannot counterfeit a real healer-primary.

- *Secondary form* (stronger): a real self-heal.
- *Tertiary form* (more limited): a thinner self-heal.

#### Differentiation: healing method

Individual healer classes are differentiated by **healing method** — *how and when healing is delivered* (principle 4). Three candidate healer classes, one per method (names TBD, original per D-008):

| Method | Feel | As a borrowed subclass, its self-heal is flavored as… |
|---|---|---|
| **Reactive big-heals** | Triage: watch health bars, clutch-save with large targeted heals. Strongest single-target emergency recovery. | a burst self-heal cooldown. |
| **Prevention / heal-over-time** | Proactive rolling HoTs and pre-heals; steady, low-spike; efficient against sustained damage, weaker at sudden spikes. | a self-HoT / regen. |
| **Absorb / damage-shields (ally-facing)** | Shield allies *before* damage lands — prevent rather than restore; rewards anticipation. | a self-shield. |

**Cross-archetype rule — self vs. ally.** Tank methods are self-facing *survival*; healer methods are ally-facing *healing*. Same mechanics, different beneficiary — a tank's lifesteal or ward protects only itself, a healer's shield is cast on allies — so shields and lifesteal never collide across archetypes.

**Lifesteal is not a healer class.** It remains a self-facing (tank) survival concept; whether ally-facing lifesteal survives as a minor itemized or ability effect is TBD.

Two rules follow from the method axis (mirroring tank):

- A healer's *as-subclass* self-heal is **flavored by its method** — the three methods give three different self-sustain styles a borrower can slot.
- **No method is a strict upgrade of another.** They trade reaction, anticipation, and steadiness, so the choice is a genuine preference rather than a power ranking.

**Still TBD for healers:** final class count, names, and each class's stronger-secondary vs. more-limited-tertiary subset shape. Deferred to the roster-shape and per-class layers.

### Support archetype

Archetype-level identity shared by every future support class, followed by the method axis that differentiates them (principle 4). Support is where principle 2 (no mandatory roles) and principle 5 (cap the tyranny of charm/mez/slow) are stress-tested hardest.

**Core fantasy.** The hand on the fight's dial — bends the battlefield so allies win: stops, slows, turns, and lifts. It has real situational damage, but its throughput is *manipulating the fight*, not ending it.

**Solo identity — control-based safety.** A support solos by not taking the hit at all: it locks, slows, or turns the enemy so it rarely acts, then chips it down with modest offense. This completes the archetypes' four-way symmetry on incoming damage — the tank survives it (mitigation), the healer undoes it (healing), damage pre-empts it (kill fast), and support *prevents* it (control). Solo-scaled per principle 5, and a self-directed baseline, not full solo-clear power.

**Spine — what every support keeps:**

- Control — a specialized method (below) plus a baseline of soft control.
- Baseline amplification — some ally buffs (haste, damage, resources); every support has this, none is "the buff class."
- Situational damage spikes.
- Graceful-degradation self-defense — soft control and debuffs still land partially on control-immune foes, so its safety never drops to zero.

**Deliberate gaps — what a support-primary lacks so subclasses matter (principle 1):**

- Killing throughput → **Damage** subclass.
- Party healing → **Healer** subclass.

Durability is deliberately *not* a gap — a support's control *is* its defense, and it degrades gracefully (hard control is resisted by elites, but soft control/debuffs still soften them) rather than vanishing.

**Support as someone else's subclass (D-012 curated subset).** Lends a *personal control tool* only — a self-protective peel (root / slow / stun / interrupt one enemy) — never party-wide amplification or AoE lockdown, so a subclass cannot counterfeit a real support-primary.

- *Secondary form* (stronger): a reliable single-target control.
- *Tertiary form* (more limited): a brief slow or interrupt.

#### Differentiation: control method

Individual support classes are differentiated by **control method** — *how each bends the fight* (principle 4). Three candidate support classes, one per method (names TBD, original per D-008):

| Method | Feel | Personal control tool it lends as a subclass |
|---|---|---|
| **Lockdown** | Hard CC — mez / root / stun; stop enemies acting outright. Most negated by control-immune elites. | a personal hard-CC peel (stun/root one enemy). |
| **Attrition** | Soft control — slow / weaken / damage-reduction; grind a feeble enemy down. Degrades most gracefully against control-immunity. | a personal slow / weaken. |
| **Redirection** | Charm / fear — turn enemies on each other or drive them off. The principle-5 hotspot. | a brief personal charm / fear. |

**Rules:**

- **Amplification is a shared support baseline, not a differentiator** — every support buffs allies somewhat; no class is the dedicated buffer.
- **Principle 5, front and center.** Mez, slow, and charm all get diminishing returns, solo-scaled potency, and are never the only path through a fight — charm/redirection most of all.
- Every support keeps some **soft-control baseline** so its self-defense degrades gracefully and is never fully negated.
- A support's *as-subclass* personal control tool is **flavored by its method**, and **no method is a strict upgrade of another** — they trade stopping, weakening, and turning.

**Still TBD for support:** final class count, names, and each class's stronger-secondary vs. more-limited-tertiary subset shape. Deferred to the roster-shape and per-class layers.

### Damage archetype

Archetype-level identity shared by every future damage class, followed by the method axis that differentiates them (principle 4). Damage is the archetype that fills every other archetype's throughput gap.

**Core fantasy.** The finisher — the archetype that *ends* fights. Everyone else manages the fight; damage removes the reason to.

**Solo identity — glass cannon.** Kills before it is killed; its defense *is* the short fight. Highest risk/reward, and — uniquely — the most self-sufficient soloer, because offense self-solves most problems. A self-directed baseline like every archetype, not full solo-clear power.

**Spine — what every damage class keeps:**

- Killing throughput, burst **and** sustained — the thing every other archetype lacks.
- Lethality-as-control — a dead enemy needs no crowd control.
- Pattern-based endurance — its own sustained/DoT pattern carries long fights.
- Durability via speed — killing fast is its answer to incoming damage.

**Lone deliberate gap (principle 1):** self-sustain / recovery → **Healer** subclass. Offense can dish damage and win the sprint, but it can never *un-take* damage already dealt — the one problem raw offense cannot solve. Durability, crowd control, and endurance are self-solved rather than gaps, which makes damage the most solo-independent archetype and the sharpest reason a long attrition fight wants a healer.

**Damage as someone else's subclass (D-012 curated subset).** Lends supplementary offensive throughput, *method-flavored* (a burst nuke / a DoT / a pet / an execute), scaled below a damage-primary's ceiling — this is what fills the tank/healer/support throughput gaps. Unlike the other archetypes, damage reserves **magnitude, not a group-facing role**, since dealing damage is inherently self-produced.

- *Secondary form* (stronger): stronger supplementary damage.
- *Tertiary form* (more limited): a lighter offensive touch.

#### Differentiation: damage pattern

Individual damage classes are differentiated by **damage pattern** — explicitly not melee vs. caster (principle 4). Four candidate damage classes, one per pattern (names TBD, original per D-008):

| Pattern | Feel | Subclass lend |
|---|---|---|
| **Burst** | Front-loaded spike in a window; nail it or be exposed with cooldowns down. High risk/reward. | a burst nuke. |
| **Sustained / DoT** | Steady ramping damage; wins attrition — the pattern that makes endurance a non-gap. | a DoT. |
| **Pet-commander** | Damage via directed pet(s); the pet soaks danger, softening glass-cannon fragility. | a pet. |
| **Opportunist / execute** | Conditional spikes on vulnerable / low-health / flanked / debuffed targets; thrives on openings, its own or a support's. | an execute / conditional strike. |

Two rules follow from the method axis (mirroring the other archetypes):

- A damage class's *as-subclass* lend is **flavored by its pattern**, and **no pattern is a strict upgrade of another** — they trade spike, floor, pet-durability, and conditionality.
- Per-pattern texture: pet-commander is the least fragile (the pet soaks), and opportunist has the strongest combination hooks (it synergizes with support debuffs and its own).

**Still TBD for damage:** final class count, names, and each class's stronger-secondary vs. more-limited-tertiary subset shape. Deferred to the roster-shape and per-class layers.

## Open threads specific to the roster

- How many classes form the initial roster.
- Which archetypes/roles the roster must cover for the three-class system to produce varied, non-redundant combinations.
- Each class's fantasy, primary-kit identity, stronger-secondary subset, and more-limited-tertiary subset.
- Each class's armor tier and weapon-group eligibility.
- Each class's parallel-advancement options.
