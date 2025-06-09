---
CIP: ?
Title: Governance Polling
Category: Tools
Status: Proposed
Authors:
    - Ryan Williams <ryan.williams@intersectmbo.org>
Implementors: []
Discussions:
    - https://github.com/cardano-foundation/CIPs/pull/?
Created: 2025-03-26
License: CC-BY-4.0
---

## Abstract

Cardano has seen many on-chain/off-chain hybrid governance tools.
These tools have been designed for specific use cases,
and whilst sometimes common in approach have not used ecosystem standards.

With the emergence of Cardano protocol governance via [CIP-1694 | A First Step Towards On-Chain Decentralized Governance](https://github.com/cardano-foundation/CIPs/blob/master/CIP-1694/README.md),
the need for pre-on-chain governance has become clear.

Leveraging existing on-chain/off-chain governance decision tooling,
we propose a set of transaction metadata standards to create and participate on governance polls,
which can be used to inform the creation of fine-tuned governance actions.

## Motivation: why is this CIP necessary?
<!-- A clear explanation that introduces the reason for a proposal, its use cases and stakeholders. If the CIP changes an established design then it must outline design issues that motivate a rework. For complex proposals, authors must write a Cardano Problem Statement (CPS) as defined in CIP-9999 and link to it as the `Motivation`. -->

### Limited Scope of governance actions

On-chain governance decisions via CIP-1694 are limited to a strict set of [governance actions](https://github.com/cardano-foundation/CIPs/blob/master/CIP-1694/README.md#governance-actions), with a current high barrier to entry of one hundred thousand ada.
On-chain governance gives path for iteration of complex governance actions,
such as an election of new constitutional committee or a budget process prior to treasury withdrawal(s).

- hard to add new types of governance action

### Lots of existing tooling but not standardized

- CIP94
- cardano-ballot
- clarity dao governance
- summon platform
- sundae governance

## Specification
<!-- The technical specification should describe the proposed improvement in sufficient technical detail. In particular, it should provide enough information that an implementation can be performed solely on the basis of the design in the CIP. This is necessary to facilitate multiple, interoperable implementations. This must include how the CIP should be versioned, if not covered under an optional Versioning main heading. If a proposal defines structure of on-chain data it must include a CDDL schema in its specification.-->

### Overview

- Tools follow Cardano networks for transactions containing poll creation metadata
- Different types of poll are permitted
- Tools show users active polls
- Tools allow users in specified voter groups to create votes, which are submitted to Cardano networks
- Tools follow networks for votes, showing tallies of valid votes
- Tools shows results of a poll when poll expires

what we need to define

- Types of poll, and their parameters
  - CC elections, budget proposals
- Types of votes, and how to validate (different per type of voter/credential) 
  - Voters: SPO keys + calidus keys, DRep credentials, stake credentials, cc credentials
- Vote tallying techniques

### On-chain definitions

#### Poll Structure

- poll description (+ link to off-chain metadata)
- poll question
- poll choices
- poll desired voters/credentials
- poll lifetime
- nonce
- votes via cardano network or hydra?

#### Vote Structure

- refers to a poll (hash)
- providers an answer to poll
- providers a authorizing witness/signature
- nonce?

### Vote Validations and Tallying

- which voters which credentials
- how are votes validated
- how to treat invalid votes

## Rationale: how does this CIP achieve its goals?
<!-- The rationale fleshes out the specification by describing what motivated the design and what led to particular design decisions. It should describe alternate designs considered and related work. The rationale should provide evidence of consensus within the community and discuss significant objections or concerns raised during the discussion.

It must also explain how the proposal affects the backward compatibility of existing solutions when applicable. If the proposal responds to a CPS, the 'Rationale' section should explain how it addresses the CPS, and answer any questions that the CPS poses for potential solutions.
-->

## Path to Active

### Acceptance Criteria
<!-- Describes what are the acceptance criteria whereby a proposal becomes 'Active' -->

### Implementation Plan
<!-- A plan to meet those criteria or `N/A` if an implementation plan is not applicable. -->


## Copyright

This CIP is licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).
