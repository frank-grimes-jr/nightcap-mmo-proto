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

- Which original classes form the initial roster, and what is each class's identity?
- At what point does the introductory quest open the secondary and tertiary class slots?
- Which abilities can each class contribute from the secondary and tertiary slots?
- What power ratios or restrictions make the secondary subclass stronger than the tertiary without making either choice trivial?
- How do class resources, weapon skills, armor proficiency, and base attributes interact across three classes?
- What original names and boundaries define the armor-chassis, weapon, accessory, and universal-eligibility categories?
- Which functional statistic categories can support abilities across class slots, and how are their power-budget weights compared?
- How effective are subclass-supporting statistics when applied to the stronger secondary slot versus the more limited tertiary slot?
- Which accessory types are broadly eligible, and how much of a hybrid build's support should come from accessories?
- What maximum number of augment sockets may an item have, and which authored items receive one or more sockets?
- What broad augment-compatibility families exist, and which equipment destinations belong to each family?
- How rare should multi-family augments be, and which family combinations may they support?
- What is the numeric currency curve for augment installation, field replacement, and intact removal? (Structure resolved: cost scales with augment power; one token covers one action at any power.)
- Which specific settlements host the augment-removal service and token vendor, and what is the numeric token storage cap? (Structure resolved: both services live together in settlement hubs; token storage is capped.)
- How much weaker must augment-based correction be than comparable specialization authored directly onto an item?
- How frequently should specialized hybrid items appear, and how discoverable should their fixed world sources be?
- How rare and powerful may universally eligible items become without erasing primary-class equipment identity?
- At what rate do characters earn parallel-advancement points from enemies and quests?
- What point caps, prerequisites, exclusions, or diminishing returns keep the shared advancement pool balanceable?
- Can primary-class advancement allocations be reset even though the primary class itself is permanent?
- What currency cost or other gate controls subclass replacement, and does that cost change with repeated use?
- How are three-class combinations balanced without erasing class identity or requiring external build guides?
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

- What percentage or quantity of experience is lost at each level?
- How are multiple corpses represented and recovered?
- Does planned or unplanned server downtime pause the 48-hour real-time timer?
- What happens to abilities and equipment requirements after de-leveling?
- How is a corpse recovered after its original dungeon instance expires?
- What prevents severe low-level death spirals?

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
