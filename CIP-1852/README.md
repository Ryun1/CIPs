---
CIP: 1852
Title: HD (Hierarchy for Deterministic) Wallets for Cardano
Category: Wallets
Status: Active
Authors:
    - Sebastien Guillemot <seba@dcspark.io>,
    - Matthias Benkort <matthias.benkort@cardanofoundation.org>
Implementors: []
Discussions:
    - https://forum.cardano.org/t/cip1852-hd-wallets-for-cardano/41740
    - https://github.com/cardano-foundation/CIPs/pull/33
Created: 2019-10-28
License: CC-BY-4.0
---

## Abstract

Cardano extends the [BIP44](https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki) by adding new chains used for different purposes. This document outlines how key derivation is done and acts as a registry for different chains used by Cardano wallets.

## Motivation: why is this CIP necessary?

For Cardano, we use a new purpose field `1852'` instead of `44'` like in BIP44. There are three main reasons for this:

1) During the Byron-era, `44'` was used. Since Byron wallets use a different algorithm for generating addresses from public keys, using a different purpose type allows software to easily know which address generation algorithm given just the derivation path (ex: given `m / 44' / 1815' / 0' / 0 / 0`, wallet software would know to handle this as a Byron-era wallet and not a Shelley-era wallet).
2) Using a new purpose helps bring attention to the fact Cardano is using `BIP32-Ed25519` and not standard `BIP32`.
3) Using a new purpose allows us to extend this registry to include more Cardano-specific functionality in the future

`1852` was chosen as it is the year of death of Ada Lovelace (following the fact that the `coin_type` value for Cardano is `1815` for her year of birth)

## Specification

### Terminology

#### Derivation style

Cardano does not use [BIP32](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki) but actually uses [BIP32-Ed25519](https://raw.githubusercontent.com/input-output-hk/adrestia/master/user-guide/static/Ed25519_BIP.pdf). The `-Ed25519` suffix is often dropped in practice (ex: we say the Byron release of Cardano supports [BIP44](https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki) but in reality this is BIP44-Ed25519).

The Byron implementation of Cardano uses `purpose = 44'` (note: this was already a slight abuse of notation because Cardano implements BIP44-Ed25519 and not standard BIP44).

There are two (incompatible) implementations of BIP32-Ed25519 in Cardano:

1) HD Random (notably used initially in Daedalus)
2) HD Sequential (notably used initially in Icarus)

The difference is explained in more detail in [CIP3](https://cips.cardano.org/cips/cip3)

Using `1852'` as the purpose field, we defined the following derivation path

```
m / purpose' / coin_type' / account' / role / index
```

Example: `m / 1852' / 1815' / 0' / 0 / 0`

Here, `role` can be the following

| Name           | Value | Description
|----------------|-------|-------------
| External chain | `0`   | Same as defined in [BIP44](https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki)
| Internal chain | `1`   | Same as defined in [BIP44](https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki)
| Staking Key    | `2`   | See [CIP11](https://cips.cardano.org/cips/cip11)

Wallets **MUST** implement this new scheme using the master node derivation algorithm from Icarus with sequential addressing (see [CIP3](https://cips.cardano.org/cips/cip3) for more information)

### Future extensions

As a general pattern, new wallet schemes should use a different purpose if they intend to piggy-back on the same structure but for a different use-case (see for instance [CIP-1854](https://cips.cardano.org/cips/cip1854)).

The `role` can however be extending with new roles so long as they have no overlapping semantic with existing roles. If they do, then they likely fall into the first category of extension and would better be done via a new purpose.

## Rationale: how does this CIP achieve its goals?

## Path to Active

### Acceptance Criteria
<!-- Describes what are the acceptance criteria whereby a proposal becomes 'Active' -->

### Implementation Plan
<!-- A plan to meet those criteria. Or `N/A` if not applicable. -->

## Copyright

This CIP is licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).
