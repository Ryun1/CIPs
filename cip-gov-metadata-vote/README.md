---
CIP: ?
Title: Governance Metadata - Votes
Category: Metadata
Status: Proposed
Authors:
    - Ryan Williams <ryan.williams@intersectmbo.org>
Implementors: []
Discussions:
    - https://github.com/cardano-foundation/CIPs/pull/?
Created: 2024-03-10
License: CC-BY-4.0
---

## Abstract
The Conway ledger era ushers in on-chain governance for Cardano via [CIP-1694 | A First Step Towards On-Chain Decentralized Governance](https://github.com/cardano-foundation/CIPs/blob/master/CIP-1694/README.md), with the addition of many new on-chain governance artifacts.
Some of these artifacts support the linking off-chain metadata, as a way to provide context.

The [CIP-100 | Governance Metadata](https://github.com/cardano-foundation/CIPs/tree/master/CIP-0100) standard provides a base framework for how all off-chain governance metadata should be formed and handled.
But this is intentionally limited in scope, so that it can be expanded upon by more specific subsequent CIPs.

This proposal aims to provide a specification for off-chain metadata vocabulary that can be used to give context to votes.
Without a sufficiently detailed standard for votes we introduce the possibility to undermine delegator's ability to adequately assess the voting of DReps, SPOs and Constitutional Committee Members.
Furthermore a lack of such standards risks preventing interoperability between tools, to the detriment of user experiences.

## Motivation: why is this CIP necessary?
Blockchains are poor choices for content databases.
This is why governance metadata anchors were chosen to provide a way to attach long form metadata content to on-chain events.
By only supplying an onchain hash of the off-chain we ensure correctness of data whilst minimizing the amount of data stored chain.

### For Delegators
When observing from the chain level, tooling can only see the content of the vote and it's anchor.
These on-chain components do not give give any context to the motivation nor off-chain discussion of an vote.
Although this information would likely be desired context for voters.
By providing rich contextual metadata we enable voters to make well informed decisions.

### For all participants
By standardizing off-chain metadata formats we facilitate interoperability for tooling which creates and/or renders metadata attached to votes.
This intern promotes a rich user experience between tooling.
This is good for all governance participants.

## Specification
Although there are three types of vote defined via CIP-1694, we focus this proposal on defining core properties which must be attached to all types.
We leave room for future standards to refine and specialize further to cater more specific for each type of vote.

### New `witness` Type
Here we extend the potential witnesses, with a `witnessAlgorithm` that can be set to include support for [CIP-08 | Message Signing](https://github.com/cardano-foundation/CIPs/tree/master/CIP-0008) standard, indicated by `CIP-0008`.
Here we mimic the restrictions as imposed over the CIP-30's implementation in [.signData()](https://github.com/cardano-foundation/CIPs/tree/master/CIP-0030#apisigndataaddr-address-payload-bytes-promisedatasignature).

### Extended Vocabulary
The following properties extend the potential vocabulary of [CIP-100](https://github.com/cardano-foundation/CIPs/tree/master/CIP-0100)'s `body` property.



## Rationale: how does this CIP achieve its goals?
<!-- The rationale fleshes out the specification by describing what motivated the design and what led to particular design decisions. It should describe alternate designs considered and related work. The rationale should provide evidence of consensus within the community and discuss significant objections or concerns raised during the discussion.

It must also explain how the proposal affects the backward compatibility of existing solutions when applicable. If the proposal responds to a CPS, the 'Rationale' section should explain how it addresses the CPS, and answer any questions that the CPS poses for potential solutions.
-->

## Path to Active

### Acceptance Criteria
<!-- Describes what are the acceptance criteria whereby a proposal becomes 'Active' -->

### Implementation Plan
<!-- A plan to meet those criteria or `N/A` if an implementation plan is not applicable. -->

<!-- OPTIONAL SECTIONS: see CIP-0001 > Document > Structure table -->

## Copyright
<!-- The CIP must be explicitly licensed under acceptable copyright terms.  Uncomment the one you wish to use (delete the other one) and ensure it matches the License field in the header:

<!-- This CIP is licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode). -->
<!-- This CIP is licensed under [Apache-2.0](http://www.apache.org/licenses/LICENSE-2.0). -->
