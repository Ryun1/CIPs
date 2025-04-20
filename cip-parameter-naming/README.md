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

#### Updatable Parameters

Created from [updatable-params.json](./updatable-params.json)

todo - add a script that generates a markdown table from the json

##### Non-Updatable Parameters

todo


### Protocol Parameter Updates

todo

## Rationale: how does this CIP achieve its goals?
<!-- The rationale fleshes out the specification by describing what motivated the design and what led to particular design decisions. It should describe alternate designs considered and related work. The rationale should provide evidence of consensus within the community and discuss significant objections or concerns raised during the discussion.

It must also explain how the proposal affects the backward compatibility of existing solutions when applicable. If the proposal responds to a CPS, the 'Rationale' section should explain how it addresses the CPS, and answer any questions that the CPS poses for potential solutions.
-->

## Open Questions

- [x] Are markdown tables the best solution?
  - Probably not, a JSON representation will be provided alongside the markdown

- Should we include parameters pre-shelley?

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