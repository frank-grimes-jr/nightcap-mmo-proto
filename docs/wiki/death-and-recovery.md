# Death and Recovery

## Design status

Provisional, 2026-08-05. The structure of death, experience loss, de-leveling, and corpse recovery is decided. Exact numbers — the grace-band level, the loss percentage, summon costs, and which token the summoner uses — remain TBD.

Canonical source: [D-003: Death and experience recovery](../design/decisions.md#d-003-death-and-experience-recovery).

## What death costs you

When you die, you respawn with all of your gear and inventory intact. Dying never strips your equipment. What a death takes is experience.

Below an early threshold level, death costs you no experience at all — a grace band that keeps new characters from spiraling. Above that threshold, each death removes a set percentage of your current level's experience, and losing enough can drop you a level. The threshold and the exact percentage are still being tuned.

## De-leveling is soft

Dropping a level never locks you out of your character. You keep every ability and every item you had already earned, even ones whose level requirement you no longer meet. What de-leveling actually costs is power: your level-scaled statistics fall, and skill caps tied to your level band come down with them.

Because you can always keep fighting with the kit you know, a bad death never becomes a trap you cannot climb out of.

## Corpses and your lost experience

Each death leaves a corpse where you fell, and that corpse holds the exact experience that death cost you. Recover the corpse and you get that experience back.

You have 48 hours of real time to do it. That clock keeps running while you are logged off, so a corpse is not something to forget about — but it pauses whenever the game's servers are down, planned or not, so you are never punished for time you could not have played.

If you die several times, each corpse waits at its own death site, holding its own experience. Since your gear is never at stake, a corpse run only ever risks the experience on that one corpse.

## Getting a corpse back

There are two ways to recover a corpse:

- **Return to where you fell.** Travel back to the death site and reclaim it. The waypoint network usually puts you close.
- **Use a corpse summoner.** An NPC corpse summoner in every major settlement hub can pull your corpse to you for a fee of in-game currency or a service token — a faster path when the trip back is long or dangerous.

Corpses left inside a dungeon instance work the same way while that instance still exists: walk back in to recover them. Once the instance expires, its death site is gone, and the hub corpse summoner becomes the only way to bring that corpse back.

## Player-visible details still TBD

- The grace-band threshold level and the experience-loss percentage above it.
- The corpse summoner's cost, whether it uses the augment-service token or a separate corpse-recovery token, and whether one summon retrieves a single corpse or all of them.
