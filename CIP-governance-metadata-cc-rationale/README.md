---
CIP: ?
Title: Governance metadata - Constitutional Committee votes
Category: Metadata
Status: Proposed
Authors:
    - Ryan Williams <ryan.williams@intersectmbo.org>
    - Eystein Magnus Hansen <eysteinsofus@gmail.com>
Implementors: []
Discussions:
    - https://github.com/cardano-foundation/CIPs/pull/878
Created: 2024-07-17
License: CC-BY-4.0
---

## Abstract

The Conway ledger era ushers in on-chain governance for Cardano via [CIP-1694 | A First Step Towards On-Chain Decentralized Governance](https://github.com/cardano-foundation/CIPs/blob/master/CIP-1694/README.md), with the addition of many new on-chain governance artifacts.
Some of these artifacts support the linking of off-chain metadata, as a way to provide context to on-chain actions.

The [CIP-100 | Governance Metadata](https://github.com/cardano-foundation/CIPs/tree/master/CIP-0100) standard provides a base framework for how all off-chain governance metadata can be formed and handled.
But this standard was intentionally limited in scope, so that it can be expanded upon by more specific subsequent CIPs.

This proposal aims to provide a specification for the off-chain metadata vocabulary that can be used to give context to Constitutional Committee (CC) votes.

## Motivation: why is this CIP necessary?

The high-level motivation for this proposal is to provide a standard which improves legitimacy of Cardano's governance system.

### Clarity for governance action authors

Governance action authors are likely to have dedicated a significant amount of time to making their action meaningful and effective (as well as locking a significant deposit).
If this action is not able to be ratified by the CC, it is fair for the author to expect a reasonable explanation from the CC.

Without reasonable context being provided by the CC votes, authors may struggle to iterate upon their actions, until they are deemed constitutional.
This situation would could decrease perceived legitimacy in Cardano's governance.

### Context for other voting bodies

By producing a standard we hope to encourage all CC members to attach rich contextual metadata to their votes.
This context should show CC member's decision making is fair and reasonable.

This context allows the other voting bodies to adequately check the power of the CC.
The on-chain technical checks of power for the 

### CC Votes are different to other types of vote
- little overlap between this and other types of vote, so we cant reuse standards as easily
- CIP100 comment field is fine, but not up to the requirements

### Inclusion in interim constitution

- Article VI Section 4 of the Interim Constitution

### Tooling

- Allows rationales to be machine-readable (e.g. AI training)
- Allows rationale sections to be queryable
- Provides a structured breakdown so it is easier to maintain contexts when translating rationales

## Specification

We define an initial specification for fields which SHOULD be added to CC votes.

### Extended Vocabulary

The following properties extend the potential vocabulary of [CIP-100](https://github.com/cardano-foundation/CIPs/tree/master/CIP-0100)'s `body` property.

#### `summary`

- A short text field. Limited to `200` characters.
- Authors SHOULD use this field to clearly state their stance on the issue.
- Authors SHOULD use this field to succinctly describe their rationale.
- Authors SHOULD give a brief overview of the main arguments will support your position.
- This SHOULD NOT support markdown text styling.
- Compulsory

#### `rationale-statement`

- A long text field.
- Authors SHOULD use this field to fully describe their rationale.
- Authors SHOULD discuss their the arguments in full detail.
- This SHOULD support markdown text styling.
- Compulsory

#### `precedent-discussion`

- A long text field.
- The author SHOULD use this field to discuss what they feel is relevant precedent.
- directly passed similar proposals (history of proposals)
- (consider precedents can discarded when constitutions change?)
- This SHOULD support markdown text styling.
- Optional

#### `counterarguments-discussion`

- A long text field.
- The author SHOULD use this field to discuss significant counter arguments to the position taken.
- This SHOULD support markdown text styling.
- Optional

#### `references`

- We extend CIP-100's references field.
- We add to CIP-100's `@type`s, with a type of `relevant-articles`.
- Authors SHOULD use this field to list the relevant constitution articles to their argument.
- Optional

### Application

CC must include all compulsory fields to be considered CIP-XXX compliant.
As this is an extension to CIP-100, all CIP-100 fields can be included within CIP-XXX compliant metadata.

### Test Vector

// todo

See [test-vector.md](./test-vector.md) for examples.

### Versioning

This proposal should not be versioned, to update this standard a new CIP should be proposed.
Although through the JSON-LD mechanism further CIPs can add to the common governance metadata vocabulary.

## Rationale: how does this CIP achieve its goals?

// todo - fill in details

### `summary`

- useful for users to quickly see a preview of the whole rationale
- gives tooling the option to show a high level intro

#### No `conclusion`

- probably not needed

## Path to Active

### Acceptance Criteria

- [ ] This standard is supported by two different tooling providers used to submit governance actions to chain.
- [ ] This standard is supported by two different chain indexing tools, used to read and render metadata.

### Implementation Plan

#### Solicitation of feedback

- [ ] Run two online workshops to gather insights from stakeholders.
- [ ] Seek community answers on all [Open Questions](#open-questions).

#### Implementation

- [ ] Author to provide example metadata and schema files.

## Copyright

This CIP is licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).
