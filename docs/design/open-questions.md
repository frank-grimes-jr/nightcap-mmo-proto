# Open Design Questions

These questions are intentionally unresolved. Do not silently answer them during implementation.

## Audience and release

- What player population and concurrent population should the first vertical slice support?
- What evidence should trigger expansion from the invited community toward a public release?
- Which desktop operating systems are required initially?

## World

- What is the world's central premise, conflict, and emotional tone?
- How are continents, zones, settlements, factions, religions, and cultures organized?
- Are open-world regions seamlessly streamed, visibly zoned, or a deliberate hybrid?
- How do night, weather, navigation, maps, and environmental danger work?

## Character and combat

- Which original classes form the initial roster, and what is each class's identity? (In progress on the working canvas [class-roster.md](class-roster.md); guardrail constraints captured, roster shape and per-class identity still open.)
- At what point does the introductory quest open the secondary and tertiary class slots?
- Which abilities can each class contribute from the secondary and tertiary slots?
- Should a subclass ever expand *weapon or armor eligibility*, contrary to the current guardrail that the primary class alone sets it and subclasses never expand it (D-014, class-roster)? Parking-lot example: a dual-wield-capable rogue-like taken as secondary or tertiary granting dual-wield to a primary otherwise limited to two-handed or one-hand-and-shield. Would require reopening the D-014 eligibility rule.
- What are the exact numeric slot ceilings, point costs and rates, and respec pricing for the three-class advancement system? (Structure resolved in D-012: primary-dominant hierarchy; secondary stronger than tertiary via breadth plus a per-slot depth ceiling; a hybrid spine-plus-choice-node path spending one shared pool; situational-sidegrade forks so no dominant build; and meaningfully-gated, resettable allocations including the primary path.)
- What exact block / parry / guard maneuvers does the use-trained defense skill govern? (Resolved in D-007: a single character-wide defense skill trains the *act* of active defense — execution, timing, uptime — not the numbers, which stay D-015 stats; weapon skills are primary-only with a competent floor and mastery as a proc/damage edge; resources resolved in D-017; base attributes fold into D-015 functional buckets.)
- Balance tension to hold: primary-dominance (D-012, subclasses are a minority/accent) versus solo-capability (D-002, the three-class character must clear all content, which needs subclasses to fill the primary's gaps *enough* to solo). Likely tuned so defensive/support primaries solo viably but slowly; the two pillars must not silently drift apart.
- What original names define the categories, and what are the boundaries for the accessory and universal-eligibility categories? (Armor and weapon structure resolved in D-014: three armor tiers with own-or-lighter eligibility; many per-type weapons that roll up into skill/augment-family groups. Original names, and the weapon group taxonomy, still TBD.)
- What are the exact bucket names, the full statistic list, which statistics are compound, and the numeric power-budget weights? (Structure resolved in D-015: role-based functional buckets, every bucket has a solo expression, procs are a functional dimension, and compound statistics trade spiking for breadth.)
- How effective are subclass-supporting statistics when applied to the stronger secondary slot versus the more limited tertiary slot?
- What are the exact accessory slot count, names, and the numeric per-accessory cross-role ceiling? (Structure resolved in D-014: a broad ~7-8 slot layout where each accessory caps any single cross-role stat below armor/weapon/authored-hybrid levels — breadth, not spikes.)
- What are the exact per-family socket ceilings, and which authored items receive one or more sockets? (Structure resolved: caps vary by equipment family, with accessory families allowing the most sockets and armor/weapon families fewer.)
- What broad augment-compatibility families exist, and which equipment destinations belong to each family?
- How rare should multi-family augments be, and which family combinations may they support?
- What is the numeric currency curve for augment installation, field replacement, and intact removal? (Structure resolved: cost scales with augment power; one token covers one action at any power.)
- Which specific settlements host the augment-removal service and token vendor, and what is the numeric token storage cap? (Structure resolved: both services live together in settlement hubs; token storage is capped.)
- What is the exact size of the discount by which augment correction falls short of comparable specialization authored onto an item? (Structure resolved: augments are always strictly weaker, not merely capped at equal.)
- How frequently should specialized hybrid items appear, and how many clue tiers separate a broad codex entry from an exact one? (Discoverability model resolved in D-016: an account-wide earned-knowledge codex that sharpens progressively from region/foe hints toward the exact source.)
- How rare should universally eligible items be? (Structure resolved in D-014: universal items exist only as accessories, so their power is already bounded by the per-accessory cross-role ceiling; only their drop rarity is TBD.)
- At what rate do characters earn parallel-advancement points from enemies and quests?
- What currency cost or other gate controls subclass replacement, and does that cost change with repeated use?
- How are solo survivability and optional group synergy reconciled?
- How do dungeon encounters scale with party size while preserving solo as the baseline?
- Which open-world bosses use locked enrollment, and how are they communicated to players?
- What role-aware participation thresholds and grace periods trigger open-world boss enrollment?
- Which boss statistics, mechanics, reinforcements, or behaviors change at each enrollment tier?
- What is the maximum supported population for a designated open-world boss encounter?
- How are genuine disconnects handled without creating a downscaling exploit?
- What personal experience premium does each open-world boss tier award?
- How frequently should early attacks miss and spells fizzle?

## Death

- What is the exact grace-band threshold level and the flat experience-loss percentage above it? (Structure resolved in D-003: no loss below an early threshold, then a constant percentage per death.)
- Does the hub corpse summoner use the augment-service token or a separate corpse-recovery token, and does one summon pull a single corpse or all at once? (Recovery model resolved in D-003: corpses stay at death sites for return-trip recovery, plus an NPC corpse summoner in major hubs for currency or tokens.)

## Travel

- Are waypoint discoveries per character or account-wide?
- Is waypoint travel free, currency-funded, cooldown-limited, or constrained in another way?
- Which origin and destination conditions are required?
- How do dungeon waypoints behave after the instance ends?
- What other travel methods eventually coexist with waypoints?

## Dungeon access

- At what level or level band do dungeon unlocks change from discovery to access-key quests?
- Are any optional or exceptional dungeons allowed to use a different access rule?

## Quests and guidance

- Does the map show exact objectives, approximate search areas, or configurable guidance?
- How are dialogue, clues, and discoveries recorded?
- Which quests intentionally permit ambiguity?

## Technology

- Which engine best meets the low-spec fully 3D target and production workflow?
- Which authoritative server architecture supports the vertical slice without premature distributed complexity?
- Which database, patcher, asset pipeline, deployment model, and observability stack are appropriate?
- What exact minimum hardware and frame-time budgets define success?
