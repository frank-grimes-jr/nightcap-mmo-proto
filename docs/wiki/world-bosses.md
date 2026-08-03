# World Bosses

## Design status

Provisional, 2026-08-02. This system is not implemented. Values and qualifying bosses remain TBD.

Canonical source: [D-011: Designated open-world boss scaling](../design/decisions.md#d-011-designated-open-world-boss-scaling).

## Overview

World bosses are designated open-world encounters built for solo-first, high-risk play. Every designated world boss begins at a solo difficulty baseline, but genuine assistance can make the encounter harder and more rewarding.

Ordinary open-world enemies never use this scaling system. A creature scales only when the game explicitly designates it as a world boss.

## Locked enrollment

Party size does not determine a world boss's difficulty. The encounter reacts to players who actually participate.

1. A world boss begins an attempt at its solo baseline.
2. A player who intervenes becomes a provisional participant.
3. Sustained, meaningful participation locks that player into the encounter.
4. Each locked enrollment raises the encounter's difficulty.
5. Difficulty cannot decrease until the attempt ends, even if an enrolled player leaves, dies, disconnects, or drops party.
6. A full encounter reset clears all enrollment and restores the solo baseline.

Meaningful participation may include:

- Damaging the boss or its encounter threats.
- Healing or supporting an enrolled combatant.
- Protecting other participants.
- Controlling encounter threats.
- Holding the boss's attention for a sustained period.

Exact thresholds and grace periods are TBD. A single attack, inactive party membership, or last-second appearance will not be enough to earn enrollment or rewards.

## Mid-fight scaling

New players may join an encounter already in progress. If their participation becomes locked, the boss moves to a higher difficulty tier. Any resulting maximum-health increase preserves the boss's current-health percentage, preventing players from waiting until the boss is nearly defeated before increasing the reward tier.

Unexpected reinforcements are not automatically beneficial. For example, additional damage dealers may raise the difficulty beyond what the current healers can sustain. This is an intentional social and tactical risk.

## Experience rewards

Each qualifying participant receives more experience than the equivalent solo victory would award. The higher reward compensates for the increased danger rather than merely dividing a fixed reward pool among more players.

Exact experience premiums, eligibility rules, and treatment of dead or disconnected participants are TBD. Meaningful participation will be required; one-hit tagging will not qualify.

## Player-visible details still TBD

- Which open-world bosses use locked enrollment.
- How provisional and locked participation are communicated.
- Enrollment thresholds for damage, healing, protection, control, and boss attention.
- Difficulty changes at each enrollment tier.
- Maximum encounter population.
- Experience-premium values and final eligibility rules.
- Handling of genuine disconnects.
