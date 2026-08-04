# Design Decisions

This document records product decisions before they are expensive enough to require formal ADRs. Status values are Exploring, Provisional, Confirmed, or Implemented.

## D-001: Fully 3D low-spec presentation

- **Status:** Provisional
- **Date:** 2026-08-02
- Use a fully polygonal 3D world rather than fixed-camera 2.5D.
- Permit first-person and scroll-wheel-controlled third-person camera distances.
- Target approximately the technical simplicity of early polygonal MMORPGs: low-poly geometry, low-resolution painted textures, simple lighting, sparse environments, fog, and strong landmarks.
- Do not copy visual designs or assets from existing games.

## D-002: Solo-capable content

- **Status:** Provisional
- **Date:** 2026-08-02
- All required content, including end-game dungeon encounters, must be completable by one player.
- Dungeon encounters and their bosses become more difficult when played by a group.
- Each qualifying group member receives more experience than the equivalent solo victory would award.
- Exact dungeon difficulty scaling, participation rules, and experience premiums remain unresolved.
- Solo-capable does not mean automatically safe or universally level-scaled.

## D-003: Death and experience recovery

- **Status:** Provisional
- **Date:** 2026-08-02
- Death respawns the character with all gear and inventory.
- Death removes experience and can de-level the character.
- Each corpse retains the exact experience lost from that death.
- Recovering the corpse within 48 hours of real time restores its retained experience.
- Multiple-corpse behavior, maintenance handling, experience-loss scale, and instance-expiration behavior remain unresolved.

## D-004: Zone waypoints

- **Status:** Provisional
- **Date:** 2026-08-02
- Every zone contains exactly one waypoint.
- The waypoint is permanently located in the same place for every character.
- It is hidden in a meaningful location rather than placed obviously at the zone entrance.
- Standing on it discovers and activates it for future fast travel.
- Account-wide versus character-specific discovery, travel costs, and cooldowns remain unresolved.

## D-005: Instanced-dungeon waypoints

- **Status:** Provisional
- **Date:** 2026-08-02
- A dungeon waypoint only functions after the player enters their dungeon instance normally.
- It cannot be used from outside to bypass the dungeon entrance.
- Checkpoint, persistence, and corpse-recovery details remain unresolved.

## D-006: Quest guidance

- **Status:** Provisional
- **Date:** 2026-08-02
- Quest guidance should be closer to World of Warcraft than early EverQuest.
- The game should preserve adventure without relying on ultra-ambiguous dialogue.
- Exact journal, map-marker, search-area, and tracking behavior will be revisited.

## D-007: Skill progression

- **Status:** Provisional
- **Date:** 2026-08-02
- Skills improve through relevant use.
- Skill caps are tied to the character's current level or level band.
- Failure rates lessen as the skill approaches the maximum for that level range.
- Exact rates, failure floors, and bad-luck protection remain unresolved.

## D-008: Original intellectual property

- **Status:** Confirmed
- **Date:** 2026-08-02
- The project may draw inspiration from abstract experiential qualities of older MMORPGs.
- It will not copy protected expression, data, code, assets, lore, names, locations, characters, creatures, interfaces, symbols, or designs from EverQuest or any other game.

## D-009: Initial audience and growth direction

- **Status:** Provisional
- **Date:** 2026-08-02
- The first playable release is intended for a small invited community.
- The project should preserve a viable path toward a later public release without prematurely building for public-scale population.
- Early success means consistent engagement, players progressing independently without assistance, and players earning dungeon access for their own accounts.

## D-010: Dungeon access

- **Status:** Provisional
- **Date:** 2026-08-02
- Lower-level dungeons unlock through physical discovery.
- Higher-level dungeons require access-key quests; the level boundary remains unresolved.
- Dungeon access is shared by all characters on the account that earned it.
- Every participating account must have its own access. Party membership cannot bypass another account's missing unlock.

## D-011: Designated open-world boss scaling

- **Status:** Provisional
- **Date:** 2026-08-02
- Ordinary open-world enemies do not scale with party size or player participation.
- Only specifically designated open-world bosses use participation-based scaling.
- Designated bosses begin from a solo baseline. Party membership alone does not affect difficulty.
- Damage, healing, protection, control, and sustained boss attention can make a player a provisional participant.
- Sustained, meaningful, role-aware participation locks that player into the encounter and raises its difficulty.
- Difficulty can rise but cannot fall during an active attempt. Leaving, dying, disconnecting, or dropping party does not remove an enrolled player from the scaling count.
- When scaling raises maximum health during combat, the boss retains the same current-health percentage.
- A full encounter reset clears enrollment and restores the solo baseline.
- Meaningfully participating players receive a personal experience premium over the solo encounter reward. Exact eligibility rules and experience scaling remain unresolved.
- Locked enrollment deliberately allows genuine outside assistance to make a fight harder. Intentional abandonment remains a social risk rather than a reason to permit mid-fight downscaling.

## D-012: Three-class character identity and parallel advancement

- **Status:** Provisional
- **Date:** 2026-08-02
- Every character begins with one primary class selected at character creation. The initial class roster remains unresolved.
- The primary class is permanent and grants its complete ability set.
- An introductory in-world quest opens a secondary and a tertiary class slot.
- The primary, secondary, and tertiary slots must contain three distinct classes. The same class cannot occupy more than one slot on a character.
- Any eligible class may serve as a primary class on one character or a subclass on another.
- Subclasses grant curated subsets of their complete class kits. The secondary class is mechanically stronger than the tertiary class; exact ability access and scaling remain unresolved.
- Combat and quest completion award a separate pool of parallel-advancement points at a substantially slower rate than standard leveling experience.
- Each class has dedicated advancement options that enhance its abilities. One character-wide point pool can be allocated across the primary, secondary, and tertiary class paths.
- Point allocation can emphasize solo utility such as damage or self-sustain, or deepen a group role such as survivability.
- The primary class cannot be replaced. Secondary and tertiary classes can be replaced only at a safe location and after paying currency or satisfying another meaningful gate.
- Completing the introductory subclass quest makes every level-eligible subclass available for later replacement; individual subclasses do not require separate unlock quests.
- Replacing a subclass removes its active abilities and returns all points allocated to that subclass to the character's unspent pool. Earned points are not destroyed.
- Exact class names and expressions must be original. References to classes from existing games are mechanical shorthand only and are not candidates for final names, lore, or ability designs.

## D-013: Hybrid equipment support

- **Status:** Provisional
- **Date:** 2026-08-02
- A character's primary class determines armor-chassis and weapon eligibility. Secondary and tertiary classes do not independently unlock additional armor or weapon categories.
- Equipment eligibility and equipment statistics are separate concerns. An eligible item may carry fixed, functional statistics that support abilities associated with any class slot, even when those statistics are unusual for the item's chassis.
- Loot is authored and fixed rather than personalized or adaptively generated for the character who finds it.
- Specialized hybrid items are intentional, fixed discoveries in the world. Their uncommon combinations of chassis and statistics support particular cross-role builds without requiring one unique item family for every possible three-class combination.
- Accessories provide a broader source of cross-role statistics than armor and weapons.
- Augments provide a limited secondary way to correct or sharpen a build. They do not replace the hunt for naturally specialized equipment. An augment is always meaningfully weaker than the same specialization authored directly onto an item of the same tier — a deliberate discount, not merely a cap at equal power. The exact size of that discount remains unresolved.
- Selected authored items may contain multiple augment sockets. Each socket holds no more than one augment.
- The maximum socket count is capped per equipment family rather than by one global ceiling or by item tier. The per-family ceilings follow the cross-role support hierarchy: accessory families allow the most sockets, armor and weapon families fewer. Exact per-family ceilings and which authored items receive sockets remain unresolved.
- Every augment socket declares a broad equipment-family compatibility type. An augment can be installed only when it supports that family.
- A compatible augment can be installed anywhere while the character is out of combat. Installation does not require a safe-location service.
- Installing into an occupied socket replaces its current augment on the spot, without requiring the safe-location removal service first. The replaced augment is not destroyed.
- The replaced augment goes to the character's inventory if a slot is free, or onto the player's cursor for immediate placement if inventory is full.
- Installing an augment into an empty socket and replacing an augment in an occupied socket are both instant actions. Both require the same in-game currency payment or one prepaid service token used for intact removal, regardless of whether the action happens at a safe location or in the field.
- The currency cost of any augment action (install, field replacement, intact removal) scales with the augment's own power tier, not with the host item. A weak augment is cheap to move; a strong or rare augment is a deliberate expense.
- A prepaid service token covers exactly one action regardless of augment power. Tokens are a flat hedge whose value is greatest when banked for the strongest augments. The exact currency curve remains unresolved; token behavior does not scale.
- Compatibility families group logically related equipment destinations rather than relying on arbitrary item-by-item lists. For example, a provisional jewelry family could cover necklaces, rings, and earrings; final family names and membership remain unresolved.
- Most augments support exactly one compatibility family. Rare multi-family augments may support more than one family as intentional exceptions.
- A multi-family augment has the same effect strength as a comparable single-family augment. Broader compatibility does not impose a statistical power penalty.
- An installed augment can be removed intact and reused through a designated safe-location service. Removal requires either an in-game currency payment or one prepaid service token.
- Service tokens are purchased only with in-game currency, can be stored for later use, and are shared across the owning account. They are account-bound and cannot be traded to another player.
- The intact-removal service and the token vendor both live in settlement hubs, in the same safe places, so town remains the augment maintenance loop. The exact settlements remain unresolved.
- An account can store only a capped number of tokens, preventing an infinite stockpile that would bypass the power-scaled currency sink. The exact cap remains unresolved.
- Augment-service tokens have no real-money purchase path.
- Every item has a fixed power budget. Subclass-supporting statistics displace defense, offense, or other value rather than appearing as free additional power.
- Item statistics use a functional vocabulary that can support multiple classes and combinations rather than naming every statistic for one class.
- Rare universally eligible items may exist, but they are exceptions rather than the normal solution to hybrid equipment needs.
- Exact equipment categories, statistic vocabulary and weights, accessory rules, socket maxima and family taxonomy, multi-family augment rarity and permitted family combinations, the numeric currency curve for augment actions, service locations, token vendors and storage caps, hybrid-item frequency, and universal-item rarity remain unresolved.

## D-014: Equipment category taxonomy

- **Status:** Provisional
- **Date:** 2026-08-04
- Defines the original names and boundaries for the armor-chassis, weapon, accessory, and universal-eligibility categories referenced by D-013. Resolved axis by axis; weapon, accessory, and universal categories remain unresolved.
- **Armor chassis:** three broad chassis tiers (a light / medium / heavy-style spread) rather than two or four. Original names remain unresolved.
- A primary class may equip its own chassis tier or any lighter tier, up to a maximum. A heavy-eligible class can also wear medium or light armor; it cannot wear anything heavier than its maximum. This provides fallback options when ideal gear is scarce, at some cost to fixed defensive identity.
- Chassis eligibility still derives solely from the permanent primary class, consistent with D-013. Secondary and tertiary classes do not raise or change a character's maximum chassis tier.
- **Weapons:** organized as many specific weapon types (blade, axe, mace, bow, staff, and their eventual original equivalents) rather than a few broad archetype families. Each type carries its own per-class eligibility. Original type names and boundaries remain unresolved.
- Specific weapon types roll up into broader weapon groups. Groups, not individual types, drive weapon-skill progression (D-007) and augment-family compatibility (D-013), so switching to another type within a group does not reset skill and shares an augment family. Eligibility and flavor remain per-type. The exact group taxonomy and which types belong to each group remain unresolved.
- Weapon eligibility, like armor, derives solely from the permanent primary class. Subclasses do not unlock additional weapon types.
- **Accessories:** a broad slot layout (roughly neck, two rings, two earrings, cloak, belt, and a charm/trinket — about seven to eight slots; original names and exact count remain unresolved). This gives accessories room to be the primary hybrid canvas, consistent with D-013.
- Each accessory caps the magnitude of any single cross-role statistic below what armor, weapons, or authored hybrid items can reach. Accessories deliver breadth, not spikes: they round out a build across roles but cannot max any one cross-role role by themselves. This bounds the broad slot layout's power structurally rather than through a new aggregate cap, and preserves primary-class identity. The exact ceiling remains unresolved.
