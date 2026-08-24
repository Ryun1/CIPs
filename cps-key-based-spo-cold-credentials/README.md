---
CPS: ???
Title: Key-based Stake Pool Operator Cold Credentials
Status: Open
Category: Ledger
Authors:
    - Mike Hornan <mike.hornan@able-pool.io>
    - Ryan Williams <ryan.williams@intersectmbo.org>
Proposed Solutions: []
Discussions:
    - https://github.com/cardano-foundation/CIPs/pull/?
Created: 2024-03-11
License: CC-BY-4.0
---

## Abstract

Within Cardano's Ledger design Stake Pool Operators (SPOs) are restricted to only be able to use key-based credentials for their 'Cold Keys'.
This imposes limitations on how SPOs can operate.
Allowing the use of script-based credentials for SPO cold keys would allow improvements in security and flexibility.

## Problem

The motivation behind this CPS arises from the current limitations faced by SPOs within the Cardano ecosystem.
At present, SPOs are restricted to using key-based credentials for their 'Cold Key',
which prevents the use of script-based credentials for programmability of cold keys.
This limitation creates challenges in terms of security and multi-party management.

By enabling script-based credentials for the pool cold keys,
SPOs would have the ability to implement multiple authorization schemes,
significantly enhancing security.
With this approach, if one signing key is compromised,
it would be possible to rotate the keys without needing to change the script hash,
ensuring continuity and reducing the risk of security breaches.

Moreover, this would allow a more collaborative form of pool ownership,
enabling multiple parties to jointly control the pool,
rather than relying on a single key-holder for all decisions and changes.
This flexibility would foster greater decentralization, improve operational resilience,
and mitigate risks associated with single points of failure.

## Use cases
<!-- A concrete set of examples written from a user's perspective, describing what and why they are trying to do. When they exist, this section should give a sense of the current alternatives and highlight why they are not suitable. -->

### 1. Multi-party Stake Pools

It is common practice for multiple individuals to collaborate on the operation of a stake pool.
Currently the control of the cold key is limited to the control of a single key.
This presents challenges of access, as it is undesirable for individuals to share access to a single key.

Script-based credentials using native multi-sig scripts would allow multiple key-holders to control a single credential.
This would allow multiple individuals to collaborate on the creation of a cold key multi-signature script.
For operations requiring the cold key, these individuals would each independently produce witnesses and combine into a valid transaction.

Such multi-party control would be enforced by the ledger design.
Preventing the need for trust on a single key-holder.

### 2. Smart Contract Stake Pools

Smart contracts on Cardano allow for expressive logic to be applied to control script-based credentials.
Being able to apply such logic to pool operations would facilitate a set of complex upcases.

### 3. Less hassle when interacting with tools

- colkeys are sometimes used for other governance tooling stuff
- scripts are easy to use than getting a key out of a safe

## Goals
<!-- A list of goals and non-goals a project is pursuing, ranked by importance. These goals should help understand the design space for the solution and what the underlying project is ultimately trying to achieve.

Goals may also contain requirements for the project. For example, they may include anything from a deadline to a budget (in terms of complexity or time) to security concerns.

Finally, goals may also serve as evaluation metrics to assess how good a proposed solution is. -->

1. Multi-party control (without sharing secret material)

2. Application of smart contract logic to control

## Open Questions
<!-- A set of questions to which any proposed solution should find an answer. Questions should help guide solutions design by highlighting some foreseen vulnerabilities or design flaws. Solutions in the form of CIP should thereby include these questions as part of their 'Rationale' section and provide an argued answer to each. -->

<!-- OPTIONAL SECTIONS: see CIP-9999 > Specification > CPS > Structure table -->

### 1. What is the technical uplift required to implement this within the Cardano Ledger codebase?

Is the uplift so great, that it outweighs the potential benefits?

2. What is the technical uplift required to implement this within supporting tooling?

arguments for
- This would align SPOs cold credentials with DRep credentials.
- this is the case for all other credentials

arguments against
- very large ledger up lift
- require a lot of changes to existing tooling
- is the problem worth solving? - potential impact worth it?

## Copyright

This CPS is licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).
