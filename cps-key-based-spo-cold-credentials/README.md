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

As of Cardano's Conway Ledger era Stake Pool Operators (SPOs) are restricted to only be able to use key-based credentials for their 'Cold Key'.
This imposes limitations on how SPOs can operate.
Allowing the use of script-based credentials for SPO cold keys would allow improvements in security and flexibility.

## Problem

The motivation behind this CPS arises from the current limitations faced by Stake Pool Operators (SPOs) within the Cardano ecosystem.
At present, SPOs are restricted to using key-based credentials for their 'Cold Key',
which prevents the use of script-based credentials to share ownership and control of the stake pool.
This limitation creates challenges in terms of security and multi-party management.

By enabling script-based credentials for the pool keyhash, SPOs would have the ability to implement multiple signers, significantly enhancing security.
With this approach, if one signer’s key is compromised, it would be possible to rotate the keys without needing to change the script hash,
ensuring continuity and reducing the risk of security breaches.
Moreover, this would allow a more collaborative form of pool ownership, enabling multiple parties to jointly control the pool,
rather than relying on a single key-holder for all decisions and changes.
This flexibility would foster greater decentralization, improve operational resilience,
and mitigate risks associated with single points of failure.

The [current ledger design](https://github.com/IntersectMBO/cardano-ledger/blob/master/eras/conway/impl/cddl-files/conway.cddl) associates five types of credential with stake pool operators:
- `pool_keyhash`
- `hot_vkey`
- `vrf_keyhash`
- `reward_account`
- `pool_owners` (set of `addr_keyhash`)

`pool_keyhash` known as SPO cold key, is used as *the* identifier for a pool, referenced by delegators and is used to register and retire the pool.

`hot_vkey` known as hot key are keys which can be rotated they are authorized by the cold key.

`vrf_keyhash` / `vrf_vkey` are temporary keys which are used within blockheaders to X, they are authorized by the cold key.

`reward_account` known as X, it is an account where block rewards are sent to the pool, this can be controlled by a key or script.

`pool_owners` is a set of keys used to identify payment credentials associated with the SPO.

- one key, one point of failure
- scripts give a lot of flexibility - nice for governance voting


## Use cases
<!-- A concrete set of examples written from a user's perspective, describing what and why they are trying to do. When they exist, this section should give a sense of the current alternatives and highlight why they are not suitable. -->

1. Multi-party stake pools


2. Smart Contract stake pools
- programmability


## Goals
<!-- A list of goals and non-goals a project is pursuing, ranked by importance. These goals should help understand the design space for the solution and what the underlying project is ultimately trying to achieve.

Goals may also contain requirements for the project. For example, they may include anything from a deadline to a budget (in terms of complexity or time) to security concerns.

Finally, goals may also serve as evaluation metrics to assess how good a proposed solution is. -->

## Open Questions
<!-- A set of questions to which any proposed solution should find an answer. Questions should help guide solutions design by highlighting some foreseen vulnerabilities or design flaws. Solutions in the form of CIP should thereby include these questions as part of their 'Rationale' section and provide an argued answer to each. -->

<!-- OPTIONAL SECTIONS: see CIP-9999 > Specification > CPS > Structure table -->

arguments for
- This would align SPOs cold credentials with DRep credentials.
- this is the case for all other credentials

arguments against
- very large ledger up lift
- require a lot of changes to existing tooling
- is the problem worth solving? - potential impact worth it?

## Copyright

This CPS is licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).
