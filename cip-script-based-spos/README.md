---
CIP: ?
Title: Script-based Stake Pool Operator Credentials
Category: Ledger
Status: Proposed
Authors:
    - Mike Hornan <mr hornan's email>
    - Ryan Williams <ryan.williams@intersectmbo.org>
Implementors: []
Discussions:
    - https://github.com/cardano-foundation/CIPs/pull/?
Created: 2024-03-11
License: CC-BY-4.0
---


## Abstract

As of Cardano's Conway Ledger era Stake Pool Operators (SPOs) are restricted to only be able to use key-based credentials for their 'Cold Key'.
This imposes limitations on how SPOs can operate.
Allowing the use of script-based credentials for SPO cold keys would allow improvements in security and flexibility.

## Motivation: why is this CIP necessary?
<!-- A clear explanation that introduces the reason for a proposal, its use cases and stakeholders. If the CIP changes an established design then it must outline design issues that motivate a rework. For complex proposals, authors must write a Cardano Problem Statement (CPS) as defined in CIP-9999 and link to it as the `Motivation`. -->

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

## Specification
<!-- The technical specification should describe the proposed improvement in sufficient technical detail. In particular, it should provide enough information that an implementation can be performed solely on the basis of the design in the CIP. This is necessary to facilitate multiple, interoperable implementations. This must include how the CIP should be versioned, if not covered under an optional Versioning main heading. If a proposal defines structure of on-chain data it must include a CDDL schema in its specification.-->

We propose a change to the Cardano ledger to change to be a credential, changing `pool_keyhash` to be `pool_credential`.

Current CDDL

```cddl
pool_keyhash = $hash28
```

Proposed CDDL

```cddl
pool_credential = credential
```

where

```cddl
addr_keyhash = $hash28
script_hash = $hash28
credential = [0, addr_keyhash // 1, script_hash]
```

## Rationale: how does this CIP achieve its goals?
<!-- The rationale fleshes out the specification by describing what motivated the design and what led to particular design decisions. It should describe alternate designs considered and related work. The rationale should provide evidence of consensus within the community and discuss significant objections or concerns raised during the discussion.

It must also explain how the proposal affects the backward compatibility of existing solutions when applicable. If the proposal responds to a CPS, the 'Rationale' section should explain how it addresses the CPS, and answer any questions that the CPS poses for potential solutions.
-->

arguements for
- This would align SPOs cold credentials with DRep credentials.

arguments against
- very large ledger up lift
- require a lot of changes to existing tooling
- is the problem worth solving? - potential impact worth it?

## Path to Active

### Acceptance Criteria
<!-- Describes what are the acceptance criteria whereby a proposal becomes 'Active' -->

### Implementation Plan
<!-- A plan to meet those criteria or `N/A` if an implementation plan is not applicable. -->

<!-- OPTIONAL SECTIONS: see CIP-0001 > Document > Structure table -->

## Copyright
<!-- The CIP must be explicitly licensed under acceptable copyright terms.  Uncomment the one you wish to use (delete the other one) and ensure it matches the License field in the header: -->

<!-- This CIP is licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode). -->
<!-- This CIP is licensed under [Apache-2.0](http://www.apache.org/licenses/LICENSE-2.0). -->
