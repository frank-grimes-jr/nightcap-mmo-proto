# Dungeons

## Design status

Provisional, 2026-08-02. Dungeon access and solo-first grouping principles are defined, but exact levels, scaling, rewards, and instance behavior remain TBD.

Canonical sources: [D-002: Solo-capable content](../design/decisions.md#d-002-solo-capable-content), [D-005: Instanced-dungeon waypoints](../design/decisions.md#d-005-instanced-dungeon-waypoints), and [D-010: Dungeon access](../design/decisions.md#d-010-dungeon-access).

## Access

Lower-level dungeons unlock when a player physically discovers them. Higher-level dungeons require an access-key quest. The level or level band where this changes is TBD.

An unlock applies to every character on the account that earned it. It does not transfer to another account: every player entering a dungeon must have personally unlocked access on their own account. Joining another player's party cannot bypass this requirement.

## Solo and grouped play

Every required dungeon encounter, including end-game bosses, can be completed solo. Solo is the baseline experience rather than a reduced or fallback mode.

Grouping is optional high-risk, high-reward play. Dungeon encounters and bosses become harder when additional players participate, and every qualifying group member receives more experience than the equivalent solo victory would award. Exact scaling, participation rules, and experience premiums are TBD.

## Waypoints

A dungeon waypoint cannot be used from outside to bypass the entrance. It functions only after the player enters their dungeon instance normally. Checkpoint, persistence, and corpse-recovery behavior remain TBD.

## Player-visible details still TBD

- The boundary between discovery-based and access-key dungeon unlocks.
- Any exceptional dungeons that use different access rules.
- Group participation and locked-roster rules inside dungeons.
- Difficulty changes for each group size.
- Experience-premium values and eligibility.
- Checkpoint, waypoint, instance-expiration, and corpse-recovery behavior.
