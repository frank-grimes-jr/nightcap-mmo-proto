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
- Difficulty-scaling rules remain unresolved.
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
