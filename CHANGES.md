# Changes

## 2026-08-04 - Functional statistic vocabulary

- Opened D-015: organized statistics into role-based functional buckets (offense/defense/control/sustain/utility; names TBD) with no separate classic-attribute layer, so effects like intelligence collapse into the functions they powered.
- Required every bucket to have a solo-facing expression, keeping role-based stats from forcing group identity and holding D-002 solo-capable content.
- Made weapon procs a first-class functional dimension via proc-chance/proc-power statistics.
- Added compound statistics (e.g. a dexterity-like stat feeding hit, proc rate, and attack speed) that cost budget for every function they feed and trade spiking for breadth, mirroring the accessory rule.

Gotcha: exact bucket names, the statistic list, compound-stat membership, and numeric power-budget weights remain TBD.

## 2026-08-04 - Universal items are accessory-only

- Restricted universally-eligible items to accessories, with no universal armor or weapons, so chassis and weapon-type gates are never bypassed.
- Bounded universal-item power through the existing per-accessory cross-role ceiling rather than a new rule, leaving only drop rarity as a tuning question.
- Completed D-014's structural axes: armor, weapons, accessories, and universal eligibility.

Gotcha: original category names, the weapon group taxonomy, exact slot/socket counts, numeric ceilings, and universal drop rarity remain TBD.

## 2026-08-04 - Accessory taxonomy and cross-role ceiling

- Set a broad accessory slot layout (~7-8 slots; names and exact count TBD), making accessories the primary hybrid canvas.
- Capped the magnitude of any single cross-role statistic on an accessory below armor/weapon/authored-hybrid levels, so accessories give breadth without spikes and cannot erode primary-class identity.
- Resolved the open question of how much hybrid support comes from accessories via this structural per-accessory ceiling rather than a global aggregate cap.

Gotcha: the exact slot count, names, and numeric ceiling remain TBD.

## 2026-08-04 - Weapon taxonomy

- Organized weapons as many specific per-type categories rather than a few broad archetype families, with eligibility anchored to the primary class.
- Rolled specific weapon types up into broader groups that drive weapon-skill progression (D-007) and augment-family compatibility (D-013), while keeping eligibility and flavor per-type.

Gotcha: original weapon-type names, the group taxonomy, and which types belong to each group remain TBD.

## 2026-08-04 - Armor chassis taxonomy

- Opened D-014 for the equipment category taxonomy, to be resolved axis by axis (armor, weapon, accessory, universal).
- Set three broad armor chassis tiers (light/medium/heavy-style; names TBD) rather than two or four.
- Let a primary class equip its own chassis tier or any lighter one, up to a maximum, while keeping chassis eligibility anchored to the primary class alone.

Gotcha: original chassis names and the weapon, accessory, and universal categories remain TBD.

## 2026-08-04 - Augments strictly weaker than built-in specialization

- Sharpened the augment power rule from "not stronger than" to "always meaningfully weaker than" comparable specialization authored onto an item of the same tier.
- Kept found, naturally specialized equipment the primary path, with augments as correction rather than a rival to it.

Gotcha: the exact size of the discount remains TBD.

## 2026-08-04 - Per-family augment socket caps

- Capped augment socket counts per equipment family rather than by one global ceiling or by item tier.
- Ordered the per-family ceilings to follow the cross-role support hierarchy: accessory families allow the most sockets, armor and weapon families fewer.

Gotcha: the exact per-family ceilings and which authored items receive sockets remain TBD.

## 2026-08-04 - Augment services live in settlement hubs

- Placed the intact-removal service and the token vendor together in settlement hubs, keeping town the augment maintenance loop.
- Capped how many prepaid service tokens an account may store, preventing a stockpile that would bypass the power-scaled currency sink.

Gotcha: the specific settlements and the numeric token cap remain TBD.

## 2026-08-04 - Augment cost scales with augment power

- Made the currency cost of every augment action (install, field replacement, intact removal) scale with the augment's own power tier, independent of the host item.
- Kept a prepaid service token as a flat one-action hedge that covers any augment at any power.

Gotcha: the exact currency curve remains TBD, as do token vendor locations and account storage caps.

## 2026-08-03 - Universal augment action cost

- Required the same in-game currency or prepaid service token payment for installation, field replacement, and intact removal, regardless of location.
- Kept installation and field replacement instant, with no separate activation time.

Gotcha: exact prices and whether they scale with item or augment power remain TBD; whether the service location retains any distinct advantage over field actions is unresolved.

## 2026-08-03 - Displaced-augment destination

- Sent a replaced augment to the character's inventory when a slot is free.
- Sent a replaced augment to the player's cursor for immediate placement when inventory is full.

Gotcha: this assumes a cursor-based item-placement UI convention; exact inventory-full edge cases (e.g. cursor already occupied) remain TBD.

## 2026-08-03 - Field augment replacement

- Allowed players to replace an augment already occupying a socket directly in the field, without requiring the safe-location removal service first.
- Kept the replaced augment intact rather than destroying it on replacement.

Gotcha: where the replaced augment goes after being displaced remains TBD.

## 2026-08-03 - Field augment installation

- Allowed compatible augments to be installed anywhere while the character is out of combat.
- Kept safe-location services specific to intact augment removal rather than installation.

Gotcha: installation cost, timing, interruption behavior, and occupied-socket replacement remain TBD.

## 2026-08-03 - Equal multi-family augment power

- Made rare multi-family augments equally powerful as comparable single-family augments.
- Prevented broader compatibility from imposing a statistical power penalty.

Gotcha: exact augment values, rarity, sources, and permitted family combinations remain TBD.

## 2026-08-03 - Rare multi-family augments

- Made single-family compatibility the standard rule for augments.
- Allowed rare augments to support more than one compatibility family as intentional exceptions.
- Kept their exact rarity and permitted family combinations TBD.

Gotcha: broader compatibility does not establish final augment power, drop-rate, or family-taxonomy values.

## 2026-08-02 - Distinct class slots

- Required every character's primary, secondary, and tertiary selections to be three distinct classes.
- Removed the stale duplicate-class question from the canonical open questions and player-facing wiki.

Gotcha: the initial class roster, subclass ability access, and slot power ratios remain provisional or TBD.

## 2026-08-02 - Typed augment sockets

- Allowed selected authored items to contain multiple augment sockets, with one augment per socket.
- Required every socket and augment to match through broad equipment-family compatibility.
- Chose coherent families over arbitrary item-by-item compatibility lists.
- Kept final family names, membership, socket maxima, and multi-family augment eligibility TBD.

Gotcha: the provisional jewelry example illustrates the family rule but does not establish final equipment terminology or taxonomy.

## 2026-08-02 - Reusable augment service

- Made installed augments removable intact and reusable through a designated safe-location service.
- Allowed payment through direct in-game currency or a prepaid, storable service token.
- Made service tokens account-shared, account-bound, and non-tradable.
- Excluded any real-money purchase path for augment-service tokens.

Gotcha: exact prices, token vendors, storage limits, service locations, installation rules, and cost scaling remain provisional or TBD.

## 2026-08-02 - Hybrid equipment support

- Kept armor-chassis and weapon eligibility anchored to the permanent primary class.
- Separated equipment eligibility from statistics so fixed items can support legal cross-role subclass builds.
- Defined authored hybrid items, flexible accessories, and limited augments as complementary itemization paths.
- Required fixed item power budgets so subclass support always carries an opportunity cost.
- Added the corresponding player-facing equipment and itemization wiki page.

Gotcha: equipment categories, statistic weights, accessory rules, augment behavior, hybrid-item frequency, and universal-item rarity remain provisional or TBD.

## 2026-08-02 - Three-class character progression

- Defined a permanent full-kit primary class with stronger secondary and more limited tertiary subclasses.
- Added an introductory subclass-selection quest followed by safe-location, gated subclass replacement from the full level-eligible roster.
- Defined a slower shared parallel-advancement point pool spanning all three class paths.
- Preserved earned progression by refunding points allocated to a replaced subclass.
- Added the corresponding player-facing classes and advancement wiki page.

Gotcha: class names, roster, abilities, slot scaling, point balance, and respecialization cost remain provisional or TBD. Existing-game class names are reference shorthand only.

## 2026-08-02 - Player-facing wiki and world-boss scaling

- Made player-facing wiki updates a documentation duty when a system is coherent enough to explain.
- Added a wiki index and player-facing system pages for dungeons and world bosses.
- Recorded the initial invited-community audience, account-wide dungeon-access rules, and designated open-world boss scaling.
- Chose locked, role-aware encounter enrollment to prevent party-padding, one-hit tagging, late reward farming, and mid-fight downscaling exploits.

Gotcha: these designs are provisional and not implemented. Exact scaling, thresholds, qualifying bosses, experience premiums, and disconnect handling remain unresolved.

## 2026-08-02 - Project foundation

- Established the standalone Nightcap Development MMO documentation scaffold.
- Connected the project to its canonical GitHub repository: `frank-grimes-jr/nightcap-mmo-proto`.
- Added a canonical working agreement shared by Codex and Claude Code.
- Made skill-first development mandatory for all future code changes.
- Recorded the current experiential vision and provisional design decisions.
- Added explicit original-IP, low-spec performance, documentation, verification, and manual-QA boundaries.

Gotcha: the project remains in design and discovery. No engine or technical stack is confirmed.
