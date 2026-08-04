# Equipment and Itemization

## Design status

Provisional, 2026-08-02. The equipment layers and their intended roles are defined, but category names, numerical budgets, augment behavior, and item frequency remain TBD.

Canonical source: [D-013: Hybrid equipment support](../design/decisions.md#d-013-hybrid-equipment-support).

## Equipment identity begins with the primary class

A character's primary class determines which armor chassis and weapons that character may equip. Secondary and tertiary classes do not unlock additional armor or weapon categories.

This preserves a recognizable equipment identity for the permanent primary class. A heavily protected primary does not gain access to a caster's equipment category merely by selecting a caster subclass.

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

Augments are a secondary mechanism, not a replacement for discovering specialized equipment. Comparable specialization authored directly onto an item should remain stronger than relying on augments alone.

Selected items may contain multiple augment sockets. Each socket holds one augment and declares a broad equipment-family compatibility type. An augment can be installed only in a socket whose family it supports.

Players can install compatible augments anywhere while their character is out of combat. Installation does not require visiting a safe-location service, but it is not free: it costs the same in-game currency payment or prepaid service token used for intact removal, whether performed at a safe location or out in the field.

Installing into a socket that already holds an augment replaces it on the spot, without needing the safe-location service first. The replaced augment survives the swap rather than being destroyed: it goes to the character's inventory if a slot is free, or onto the player's cursor for immediate placement if inventory is full. Replacement is instant and costs the same currency or token payment as installation and removal.

Families keep compatibility predictable instead of giving augments arbitrary item-by-item lists. For example, a provisional jewelry family could let one compatible augment fit sockets on necklaces, rings, and earrings. Final family names and membership remain TBD.

Most augments support exactly one compatibility family. Rare multi-family augments can support more than one family, making broader compatibility an exceptional discovery rather than the normal rule. A multi-family augment is as powerful as a comparable single-family augment; its flexibility does not reduce its statistics. Its rarity and permitted family combinations remain TBD.

An installed augment can be removed intact and reused through a designated service in a safe location. The player pays either ordinary in-game currency at the time of removal or spends one prepaid service token.

Service tokens are purchased only with in-game currency and can be stored for later use by any character on the owning account. They are account-bound, cannot be traded to another player, and cannot be purchased with real money.

The currency price of an augment action scales with the augment's own power, not the item it sits in: moving a weak augment is cheap, while a strong or rare one is a deliberate expense. A prepaid token sidesteps that scaling entirely — one token covers a single action no matter how powerful the augment, so tokens are worth banking for your most valuable augments. The exact currency numbers remain TBD; token behavior does not scale.

Socket maxima and distribution, compatibility families, multi-family augment rarity and permitted family combinations, the numeric currency curve, token vendors, storage limits, and service locations remain TBD.

## Rare universal equipment

Rare items that can be equipped across otherwise separate equipment categories may exist. These are intended as exceptional discoveries, not the default answer for every hybrid build.

Their final terminology, frequency, eligibility, and power limits remain TBD.

## Player-visible details still TBD

- Original names and boundaries for equipment categories.
- Functional statistic categories and their power-budget weights.
- How subclass statistics interact with secondary and tertiary ability scaling.
- Accessory types, eligibility, and power allocation.
- Augment-socket maxima and distribution, compatibility-family taxonomy, multi-family rarity and permitted combinations, the numeric currency curve, service locations, token vendors, and storage limits.
- Frequency and discoverability of specialized hybrid items.
- Rarity and power limits for universally eligible items.
