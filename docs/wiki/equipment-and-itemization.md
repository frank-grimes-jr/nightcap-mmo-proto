# Equipment and Itemization

## Design status

Provisional, 2026-08-02. The equipment layers and their intended roles are defined, but category names, numerical budgets, augment behavior, and item frequency remain TBD.

Canonical source: [D-013: Hybrid equipment support](../design/decisions.md#d-013-hybrid-equipment-support).

## Equipment identity begins with the primary class

A character's primary class determines which armor chassis and weapons that character may equip. Secondary and tertiary classes do not unlock additional armor or weapon categories.

This preserves a recognizable equipment identity for the permanent primary class. A heavily protected primary does not gain access to a caster's equipment category merely by selecting a caster subclass.

Armor comes in three broad chassis tiers — a light, medium, and heavy-style spread (original names TBD). A primary class is eligible for its own tier and any lighter one: a heavy-armor class can also wear medium or light, but never anything heavier than its maximum. That gives a fallback when the ideal chassis is scarce without letting a class exceed its intended protection ceiling. Only the primary class sets this ceiling; subclasses never raise it.

Weapons work differently. Rather than a few broad families, there are many specific weapon types (blades, axes, maces, bows, staves, and the setting's eventual original equivalents), each with its own per-class eligibility. Those specific types roll up into broader weapon groups, and it is the group — not the individual type — that carries weapon-skill progression and augment-family compatibility. Switching between two types in the same group keeps your skill and shares an augment family, while each type keeps its own look and eligibility. As with armor, only the primary class determines which weapons a character may wield. The original type names and the group taxonomy remain TBD.

## Statistics can support the whole build

Equipment eligibility and equipment statistics are separate. An item that fits the primary class may carry statistics supporting abilities from any of the character's three class slots.

Statistics describe useful functions rather than belonging exclusively to one named class. This lets one healing statistic, for example, support multiple original classes with healing abilities instead of requiring a separate statistic and item set for every possible combination.

Subclass-supporting statistics are not free bonuses. Every item has a fixed power budget, so adding healing, damage, control, or another specialized benefit reduces the room available for defense, offense, or other statistics.

## Fixed discoveries, not adaptive loot

Loot is authored in advance. An item's statistics do not change to match the character or party that finds it.

Some specialized hybrid items are fixed discoveries placed intentionally in the world. Learning where a useful item comes from, overcoming its source, and deciding whether its tradeoffs fit a build are part of progression.

The design does not require a unique item family for every three-class combination. Items instead use functional statistics that can serve several builds.

## Accessories

Accessories provide broader access to cross-role statistics than armor and weapons. Jewelry, relics, charms, or the setting's eventual original equivalents can help a character support subclass abilities without changing primary-class equipment eligibility.

The final accessory categories, eligibility rules, and share of a build's total power remain TBD.

## Augments

Augments offer limited correction when a build needs a statistic that its current equipment does not naturally provide. They may also sharpen an existing specialization.

Augments are a secondary mechanism, not a replacement for discovering specialized equipment. An augment always delivers meaningfully less of a stat than the same specialization authored directly onto an item of the same tier — a deliberate gap, not a coin-flip that could match found gear. This keeps hunting for naturally specialized equipment the primary path, with augments there to correct or nudge a build. The exact size of the discount remains TBD.

Selected items may contain multiple augment sockets. Each socket holds one augment and declares a broad equipment-family compatibility type. An augment can be installed only in a socket whose family it supports.

How many sockets an item may carry is capped per equipment family rather than by a single global limit. Those ceilings follow the same hierarchy as cross-role support: accessory families allow the most sockets, while armor and weapon families allow fewer. This keeps accessories the natural home for flexibility. The exact per-family ceilings and which items receive sockets remain TBD.

Players can install compatible augments anywhere while their character is out of combat. Installation does not require visiting a safe-location service, but it is not free: it costs the same in-game currency payment or prepaid service token used for intact removal, whether performed at a safe location or out in the field.

Installing into a socket that already holds an augment replaces it on the spot, without needing the safe-location service first. The replaced augment survives the swap rather than being destroyed: it goes to the character's inventory if a slot is free, or onto the player's cursor for immediate placement if inventory is full. Replacement is instant and costs the same currency or token payment as installation and removal.

Families keep compatibility predictable instead of giving augments arbitrary item-by-item lists. For example, a provisional jewelry family could let one compatible augment fit sockets on necklaces, rings, and earrings. Final family names and membership remain TBD.

Most augments support exactly one compatibility family. Rare multi-family augments can support more than one family, making broader compatibility an exceptional discovery rather than the normal rule. A multi-family augment is as powerful as a comparable single-family augment; its flexibility does not reduce its statistics. Its rarity and permitted family combinations remain TBD.

An installed augment can be removed intact and reused through a designated service in a safe location. The player pays either ordinary in-game currency at the time of removal or spends one prepaid service token.

Service tokens are purchased only with in-game currency and can be stored for later use by any character on the owning account. They are account-bound, cannot be traded to another player, and cannot be purchased with real money. An account can hold only a capped number of tokens at once, so tokens stay a rolling convenience rather than a permanent stockpile. The removal service and the token vendor both live in settlement hubs, in the same safe places, keeping town the natural stop for augment upkeep. Which settlements host them, and the exact token cap, remain TBD.

The currency price of an augment action scales with the augment's own power, not the item it sits in: moving a weak augment is cheap, while a strong or rare one is a deliberate expense. A prepaid token sidesteps that scaling entirely — one token covers a single action no matter how powerful the augment, so tokens are worth banking for your most valuable augments. The exact currency numbers remain TBD; token behavior does not scale.

Exact per-family socket ceilings and distribution, compatibility families, multi-family augment rarity and permitted family combinations, the numeric currency curve, the exact token storage cap, and which settlements host the services remain TBD.

## Rare universal equipment

Rare items that can be equipped across otherwise separate equipment categories may exist. These are intended as exceptional discoveries, not the default answer for every hybrid build.

Their final terminology, frequency, eligibility, and power limits remain TBD.

## Player-visible details still TBD

- Original names for the three armor chassis and the weapon types, the weapon group taxonomy, and the names and boundaries for accessory and universal-eligibility categories.
- Functional statistic categories and their power-budget weights.
- How subclass statistics interact with secondary and tertiary ability scaling.
- Accessory types, eligibility, and power allocation.
- Exact per-family augment-socket ceilings and distribution, compatibility-family taxonomy, multi-family rarity and permitted combinations, the numeric currency curve, which settlements host the services, and the exact token storage cap.
- Frequency and discoverability of specialized hybrid items.
- Rarity and power limits for universally eligible items.
