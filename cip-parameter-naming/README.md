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
- [CIP-0009 | Protocol Parameters (Shelley Era)](https://github.com/cardano-foundation/CIPs/tree/master/CIP-0009)

- [CIP-0028 | Protocol Parameters (Alonzo Era)](https://github.com/cardano-foundation/CIPs/tree/master/CIP-0028)

- [CIP-0055 | Protocol Parameters (Babbage Era)](https://github.com/cardano-foundation/CIPs/tree/master/CIP-0055)


## Specification
<!-- The technical specification should describe the proposed improvement in sufficient technical detail. In particular, it should provide enough information that an implementation can be performed solely on the basis of the design in the CIP. This is necessary to facilitate multiple, interoperable implementations. This must include how the CIP should be versioned, if not covered under an optional Versioning main heading. If a proposal defines structure of on-chain data it must include a CDDL schema in its specification.-->


| Name via cardano-cli | Common Name | Description | Name via DBSync | Name via Constitution | added in era |
| --- | --- | --- | --- | --- | --- |
| `protocolVersion` | | Protocol version. Minor versions indicate software updates (will generally be 0). Major version 1 = Byron, 2 = Shelley | | | |
| `nOpt` | K | Target number of pools ("k"). Impacts saturation threshold, encouraging growth in number of stake pools. | | | |


## Rationale: how does this CIP achieve its goals?
<!-- The rationale fleshes out the specification by describing what motivated the design and what led to particular design decisions. It should describe alternate designs considered and related work. The rationale should provide evidence of consensus within the community and discuss significant objections or concerns raised during the discussion.

It must also explain how the proposal affects the backward compatibility of existing solutions when applicable. If the proposal responds to a CPS, the 'Rationale' section should explain how it addresses the CPS, and answer any questions that the CPS poses for potential solutions.
-->

## Path to Active

### Acceptance Criteria
<!-- Describes what are the acceptance criteria whereby a proposal becomes 'Active' -->

### Implementation Plan

N/A

## Copyright

This CIP is licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).
