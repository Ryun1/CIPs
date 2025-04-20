---
CIP: ?
Title: Cardano Protocol Parameter Definitions
Category: Ledger
Status: Proposed
Authors:
    - Ryan Williams <ryan.williams@intersectmbo.org>
Implementors: N/A
Discussions:
    - https://github.com/cardano-foundation/CIPs/pull/?
Created: 2025-03-13
License: CC-BY-4.0
---

## Abstract

Cardano networks have many parameters which control their execution.
Different tools identify these parameters by different names, this results in confusion.
Past efforts have not offered a convenient place to track on-going updates.

Here we consolidate the common naming for Cardano parameters
and define a basic system to track parameter changes.

## Motivation: why is this CIP necessary?

Discussing Cardano parameters is made difficult with varied vernaculars.
Different tools calling the same parameters by different names results in confusing and difficult discussions for users.
This problem has become prevalent with the emergence of on-chain governance, where DReps, SPOs and the CC are evaluating protocol parameter change governance actions.

Previous efforts via the CIP process have offered good descriptions but lack offerings of common alternate namings.
Furthermore these proposals, lack the recent Conway Era or tracking for on-chain governance changes.

See:

- [CIP-0009 | Protocol Parameters (Shelley Era)][CIP-0009]

- [CIP-0028 | Protocol Parameters (Alonzo Era)][CIP-0028]

- [CIP-0055 | Protocol Parameters (Babbage Era)][CIP-0055]


## Specification

### Definitions

These definitions should be maintained for future Cardano ledger eras.

#### Shelley Era

Information based-on [CIP-0009 | Protocol Parameters (Shelley Era)][CIP-0009].

##### Updatable Parameters

| Common Name              | Name via Spec            | Name via `cardano-cli`  | Name via `DB-Sync`  | Name via Constitution | Definition |
|--------------------------|--------------------------|--------------------------|----------------------|------------------------|------------|
| Protocol Version         |                          | `protocolVersion`        | `{protocol_major, protocol_minor}` | major and minor protocol versions  | Protocol version. Minor versions indicate software updates (will generally be 0). Major version 1 = Byron, 2 = Shelley |
| K                        | `nOpt`     | `stakePoolTargetNum`                    | `optimal_pool_count` | *stakePoolTargetNum* | Target number of pools ("k"). Impacts saturation threshold, encouraging growth in number of stake pools. |
| Influence Factor         | `a0`    | `poolPledgeInfluence`                     | `influence` | *poolPledgeInfluence* | "Influence Factor". Governs how much impact the pledge has on rewards. |
| Min Pool Cost            |                          | `minPoolCost`            |                      |                        | Minimum Pool Cost per epoch (in lovelace). Enables pledge effect. |
| Decentralization Param   |                          | `decentralisationParam`  |                      |                        | Level of decentralisation. Starts at 1. Block production is fully decentralised when this reaches 0. |
| Max Block Body Size      |                          | `maxBlockBodySize`       |                      |                        | Maximum size of a block body. Limits blockchain storage size, and communication costs. |
| Max Block Header Size    |                          | `maxBlockHeaderSize`     |                      |                        | Maximum size of the block header. Should be significantly less than the maximum block size. |
| Max Tx Size              |                          | `maxTxSize`              |                      |                        | Maximum size of a transaction. Several transactions may be included in a block. Must be strictly less than the max. block body size. |
| Treasury Rate            | `tau`            | `treasuryCut`                    |                      |                        | Treasury rate (0.2 = 20%). Proportion of total rewards allocated to treasury each epoch before remaining rewards are distributed to pools. |
| Monetary Expansion       | `rho`      | `monetaryExpansion`                    |                      |                        | Monetary expansion rate per epoch. Governs the rewards that are returned from reserves to the ecosystem (treasury, stake pools and delegators). |
| Pool Deposit             | `poolDeposit`       | `stakePoolDeposit`            |                      |                        | Pool deposit (in lovelace) |
| Key Deposit              |                          | `keyDeposit`             |                      |                        | Deposit charged for stake keys (in Lovelace). Ensures that unused keys are returned, so freeing resources. |
| Min Fee B                |                          | `minFeeB`                |                      |                        | Base transaction fee (in lovelace). |
| Min Fee A                |                          | `minFeeA`                |                      |                        | Additional transaction fee per byte of data (in lovelace). |
| Min UTxO Value           |                          | `minUTxOValue`           |                      |                        | Minimum allowed value in a UTxO. Security-related parameter used to prevent the creation of many small UTxOs that could use excessive resource to process. |
| Extra Entropy            |                          | `extraEntropy`           |                      |                        | Should additional entropy be included in the initial phases. This provides additional certainty that the blockchain has not been compromised by the seed key holders. Redundant once the system is sufficiently decentralised. |
| Epoch Max (eMax)         | `eMax`     | `poolRetireMaxEpoch`                   |                      |                        | Maximum number of epochs within which a pool can be announced to retire, starting from the next epoch. |

##### Non-Updatable Parameters

todo

#### Alonzo Era

Information based-on [CIP-0028 | Protocol Parameters (Alonzo Era)][CIP-0028].

todo

#### Babbage Era

Information based-on [CIP-0055 | Protocol Parameters (Babbage Era)][CIP-0055].

todo

#### Conway Era

todo

### Protocol Parameter Updates

todo

## Rationale: how does this CIP achieve its goals?
<!-- The rationale fleshes out the specification by describing what motivated the design and what led to particular design decisions. It should describe alternate designs considered and related work. The rationale should provide evidence of consensus within the community and discuss significant objections or concerns raised during the discussion.

It must also explain how the proposal affects the backward compatibility of existing solutions when applicable. If the proposal responds to a CPS, the 'Rationale' section should explain how it addresses the CPS, and answer any questions that the CPS poses for potential solutions.
-->

## Open Questions

- are markdown tables the best solution?
- should we include parameters pre-shelley?

## Path to Active

### Acceptance Criteria

- [ ] This proposal receives community feedback on common naming, for current parameters.

- [ ] This proposal is maintained with one new ledger era being added.

- [ ] This proposal is updated twice with two protocol parameter updates.

### Implementation Plan

N/A

## Copyright

Formatting on the markdown tables was assisted by ChatGPT using GPT-4o. 

This CIP is licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

<!-- In-line references -->

[CIP-0009]:https://github.com/cardano-foundation/CIPs/tree/master/CIP-0009

[CIP-0028]:https://github.com/cardano-foundation/CIPs/tree/master/CIP-0028

[CIP-0055]:https://github.com/cardano-foundation/CIPs/tree/master/CIP-0055