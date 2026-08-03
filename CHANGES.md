# Changes

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
