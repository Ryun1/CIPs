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
Complex governance decisions such as constitutional committee elections or budget processes
benefit from community input before formal on-chain governance actions are submitted.

Leveraging existing on-chain/off-chain governance decision tooling,
we propose a set of transaction metadata standards to create and participate on governance polls,
which can be used to inform the creation of fine-tuned governance actions.

## Motivation: why is this CIP necessary?

### Limited Scope of On-Chain Governance Actions

On-chain governance decisions via CIP-1694 are limited to a strict set of [governance actions](https://github.com/cardano-foundation/CIPs/blob/master/CIP-1694/README.md#governance-actions),
with a current high barrier to entry of one hundred thousand ada.

Although for many complex governance decisions benefit from community input before a formal on-chain action is
submitted. For example:

- Electing a new constitutional committee requires understanding candidate positions
- Budget processes need community insights before treasury withdrawal proposals
- Protocol parameter changes may need pre-consensus on values
- New constitutional provisions require community input

The current system doesn't provide a standardized way to gather this input.

### Need for Pre-On-Chain Governance Consensus

Complex governance actions often require multiple stakeholders to align before formal submission:

**Constitutional Committee Elections**: The Update committee action requires proposing
a complete committee for a binary Yes/No approval. This binary choice is inadequate when there are many candidates
and the community needs to first narrow down to a subset.

**Budget and Treasury Processes**: Large budgets or treasury withdrawals require careful consideration. Pre-on-chain polls
allow communities to evaluate proposals, estimate costs, and build alignment before submitting a governance action for final approval and enactments.

**Protocol Parameter Adjustments**: Technical parameters often have cascading effects. Pre-on-chain polls enable
technical discussion, impact analysis, and consensus-building around specific values or ranges.

**General setting of rules or approach**:

### Existing Tooling Lacks Interoperability

Many Cardano tools have been developed for polling,
but they lack standardization or are small in feature set:

- [CIP-94| On-chain SPO polls](CIP-0094/README.md)
- Ekklesia
- Cardano Ballot
- Clarity DAO Governance
- Summon Platform
- SundaeSwap Governance

While these tools serve their communities,
the lack of an ecosystem-wide standard means:

- Votes cannot be aggregated across tools
- Different tools use incompatible data formats
- Dashboard integration is fragmented

A standardized approach would enable aggregation of poll results across tools.

## Specification

### Overview

This CIP extends the approach taken in [CIP-94](CIP-0094/README.md) to support
multiple types of governance polls beyond SPO-only polls.
Like CIP-94, polls will be multiple-choice questions with pre-defined answers
to choose from.

Here's an example of a poll question and answers:

- _Should the Constitutional Committee be expanded to 9 members?_
  - [ ] Yes  
  - [ ] No  
  - [ ] Abstain

The poll and its choices will be posted on-chain via transaction metadata.
Votes are provided on-chain by eligible voters via transaction metadata referring to:

- The poll identifier (hash of the poll metadata)
- The index of the chosen answer from the available choices
- A digital signature from the voter's credential (SPO cold key, SPO Calidus key, DRep credential, CC hot credential, or stake credential)

> [!NOTE]
> In this document, every time we refer to a _serialized object_, we refer to its **canonical** CBOR representation. In particular, keys in a map are always ordered alphabetically.

### Poll structure

A poll is posted in a transaction's metadata using the metadatum label `XXXX`, using the following metadata structure:

```cbor
poll =
  { 0: prompt
  , 1: [ * choice ]
  , 2: voter_groups
  , 3: tally_method
  , 4: start_epoch
  , 5: end_epoch
  , ? 6: max_choices_selected
  , ? 7: metadata_url
  , ? 8: metadata_hash
  , ? "_": nonce
  }

prompt =
  [ * text .size (0..64) ]

choice =
  [ * text .size (0..64) ]

voter_groups =
  [ * voter_group ]

voter_group = 0       ; Stake Pool Operators
            / 1       ; DReps  
            / 2       ; Constitutional Committee
            / 3       ; Stake credentials

tally_method = 0       ; One-per-voter
           / 1         ; Stake weighted

max_choices_selected =
  uint  ; Maximum number of choices a voter can select (default: 1)

metadata_url =
  text

metadata_hash =
  bytes .size 32

start_epoch =
  uint

end_epoch =
  uint

nonce =
  uint
```

The transaction carrying a poll **should** be signed by the poll creator's credential.
This credential is not captured in the metadata but in the transaction itself as a signatory.
An optional nonce can be included to provide non-replayability should the same question and answers be asked multiple times over different periods.

### Vote structure

Similarly, a vote is posted as transaction's metadata using the same label `XXX` and the following metadata structure:

```cbor
vote =
  { 2: poll_hash
  , 3: choices_selected
  }

poll_hash =
  bytes .size 32

choices_selected = uint            ; Single choice index (0-based)
                / [ * uint ]      ; Array of choice indices (0-based)
```

1. The field `2` (`poll_hash`) is a blake2b-256 hash digest, whose preimage is the entire serialised poll metadata payload (with the top-level label).
2. The field `3` represents either:
   - A single 0-based index of the chosen answer from the available choices (when voting for one choice)
   - An array of 0-based indices of chosen answers (when voting for multiple choices)
3. The number of choices selected must not exceed the poll's `max_choices_selected` field (if present) or 1 (if absent).
4. Each choice index must reference a valid choice in the poll (be less than the total number of choices).

The transaction carrying the vote metadata must then **be signed using one of the voter's credentials** based on the poll's `voter_groups` field:

- If poll allows SPOs (group 0): requires stake pool cold key witness
- If poll allows DReps (group 1): requires DRep credential witness
- If poll allows Constitutional Committee (group 2): requires CC hot credential witness
- If poll allows Stakeholders (group 3): requires stake credential witness

### Procedure & Duration

A poll starts when a valid transaction with poll metadata is posted on-chain.
Votes can be submitted until the end of the `end_epoch` specified in the poll.
The poll organizer is responsible for specifying appropriate `start_epoch` and
`end_epoch` values to allow adequate time for voting.

### Tallying Methods

#### One per Voter Tallying (method 0)

For one-per-voter tallying, each eligible voter contributes exactly one vote regardless of their stake or delegation. All votes carry equal weight of 1.

Todo: decide is multiple votes can be cast by the same voter

#### Stake Weighted (method 1)

For stake-weighted tallying, each vote's weight is calculated based on the voter's delegated or controlled stake at the time of poll close.

For SPOs, the weight is the total stake delegated to their pool.
For DReps, the weight is the total stake voting rights delegated to them.
For stake credentials, the weight is their controlled stake.
For Constitutional Committee members, the weight is 1 (one vote per member).

todo: maybe a nicer way to handle this?
todo: should poll proposers share a snapshot at time of poll creation?

### How to validate a vote

todo

### Outcome

The outcome of a poll depends on the tallying method chosen and the votes cast. Polls are explicitly called polls/surveys and not votes to dispel any possible confusion.

How poll data is interpreted is considered out of scope for this CIP,
which aims mainly at producing standardized data points on-chain.

Poll proposers should aim to take poll results seriously.

todo: is a poll proposal deposit needed? to have a bar of entry. Could be a treasury donation.

## Rationale: how does this CIP achieve its goals?

This CIP provides a standardized approach to pre-on-chain governance polling that addresses the
identified needs while maintaining flexibility for different use cases.

### Design Decisions

#### Metadata-Based Approach

Following the pattern established by CIP-94 and adopted in other Cardano metadata standards,
this CIP uses transaction metadata rather than on-chain state.

- **Simplicity**: No ledger modifications required
- **Flexibility**: Tools can implement different tallying and display logic
- **Backward Compatibility**: Existing tools continue to function independently

#### Flexibility in Poll Types and Tallying

Rather than prescribing a single poll format, this CIP supports multiple poll types and tallying methods
This flexibility ensures the standard remains useful across diverse governance scenarios.

#### Credential-Based Authentication

Different voter groups authenticate using different credentials.

### Alternatives Considered

#### 1. Info Governance Action Enhancement

Rather than creating a new poll standard,
metadata could be added to Info governance actions under CIP-1694.

**Pros**: Uses existing governance infrastructure; leverages formal on-chain ratification  
**Cons**: Requires 100,000 ada deposit per poll (with current protocol parameters); inflexible for ephemeral polls; mixes pre-on-chain and on-chain concerns

todo: discuss more, this could be more straight forward tbh

### Backward Compatibility

This CIP does not modify any existing standards or ledger behavior.
Implementations of this CIP:

- Can coexist with existing polling tools (CIP-94, Cardano Ballot, etc.)
- Do not interfere with on-chain governance under CIP-1694
- Can be adopted incrementally by different tools

The standard is designed to be complementary to, rather than replacement for,
existing governance tools.

## Path to Active

### Acceptance Criteria

For this CIP to become Active, the following criteria must be met:

- [ ] **Metadata Label Assignment**: A metadata label number is assigned through the CIP process and documented in the specification
- [ ] **Community Review**: At least XXX weeks of public review with community feedback addressed
- [ ] **Reference Implementation**: At least one open-source reference implementation demonstrates:
  - Poll creation transaction construction
  - Vote transaction construction  
  - Vote validation logic
  - Poll discovery and indexing
  - Results tallying and display
- [ ] **Community Adoption Signals**
- [ ] **Test Poll Execution**: At least one functional poll is executed on mainnet or testnet
   demonstrating the full lifecycle from creation through tallying

### Implementation Plan

#### Specification Refinement

- [ ] Draft

#### Reference Implementation

- [ ]

#### Deployment

- [ ]

#### Ecosystem Integration

- [ ]

## Copyright

This CIP is licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).
