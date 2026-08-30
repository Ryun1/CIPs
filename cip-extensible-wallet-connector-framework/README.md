---
CIP: ?
Title: Extensible Wallet Connector Framework
Category: Wallets
Status: Proposed
Authors:
    - Ryan Williams <ryan.williams@intersectmbo.org>
Implementors: []
Discussions:
    - https://github.com/cardano-foundation/CIPs/pull/?
Created: 2024-04-19
License: CC-BY-4.0
---

## Abstract

Wallets are some of the most significant infrastructure we have in Web3.
Wallet connectors define how wallets can communicate with client stacks (i.e., dApps), facilitating a range of specialized functions, that wallets cannot easily provide.

## Motivation: why is this CIP necessary?

While Cardano's current set of wallet connectors enabled the launch of dApps on Cardano, the ecosystem has outgrown them.

Current issues include;
- Dependency on Javascript-based stacks
- Dependency on web-based wallets
- Weakly defined specifications
- Limited inflexible scopes

We wish to outline a extensible framework which better fits the current needs of the Cardano ecosystem whilst addressing the current issues of Cardano's connectors.

We want a APIs which are agnostic to connection mechanisms, so we want a universal messaging language.

For full motivation see [CPS-0010 | Wallet Connectors](https://github.com/cardano-foundation/CIPs/blob/master/CPS-0010/README.md).

## Specification

This specification describes an extensible wallet connector framework.
We intend for future authors to proposal new CIPs which expand the functionalities of this proposal.

### Connection Mechanism

- Connection mechanisms that comply with this standard must be described via a CIP.
- Connection mechanisms must be able to support the passing of JOSN-RPC messages between wallets and clients.
- Connection mechanisms should be decentralized, striving to avoid the need for centralized coordinators.

We envision a wide range of possible connection mechanisms to be proposed.

#### API Structure

##### Request

```json
{
    "jsonrpc": "2.0",
    "method": "",
    "params": {},
    "id": "xxx"
}
```

##### Response

```json
{
    "jsonrpc": "2.0",
    "result": "addr1..",
    "id": 1
}
```

##### Error

```json
{
    "jsonrpc": "2.0",
    "error": {
        "code": -32601,
        "message": "Method not found"
    },
    "id": 1
}
```

#### Connection API

Once connection has been established via the [Connection Mechanism](#connection-mechanisms).
The wallet should offer the first message.

#### Request Connection

```json
{
    "jsonrpc": "2.0",
    "method": "connect",
    "params": {
        "name" : "",
        "description" : "",
        "url" : "",
        "icons" : [ "" ] 
    },
    "id": 1
}
```
##### Connection Response

```json
{
    "jsonrpc": "2.0",
    "response": {
        "walletFramework" : "CIPxxxx",
        "walletDisplayName" : "xxxx",
        "walletIcon" : "xxxx",
        "connectionInstanceUUID" : "xxxx",
        "networks" : [
            "mainnet",
            "testnet"
        ]
    },
    "id": 1
}
```

Wallets SHOULD let users know that connection has been established.

#### Request Methods

Wallets COULD give users the ability to choose which APIs are shared.

```json
{
    "jsonrpc": "2.0",
    "method": "methods",
    "params": { },
    "id": 1
}
```

##### Request Methods Response

```json
{
    "jsonrpc": "2.0",
    "result":{
        "methods": {
            "cip302": [
                "cip302.getUsedAddresses",
                "cip302.signTx"
            ],
            "cip95": [
                "cip95.getDRepKey",
                "cip95.signTx"
            ],
            "cip1234": [
                "cip1234.verifyZK"
            ]
        }
    },
    "id": 1
}
```
 
#### API Extensions

- must be CIPs 
- should have succinct scope
- optional

## Rationale: how does this CIP achieve its goals?

- JSON-RPC is a widely used protocol for communication between applications
- probably doesnt have to be the most high performance

## Path to Active

### Acceptance Criteria

- [ ] Have two connection mechanisms be proposed.
- [ ] Have two APIs proposed.

### Implementation Plan

- [ ] Present this proposal to the Wallets Working Group
- [ ] Seek input from at least five wallet implementors

## Open Questions
- Async by default and APIs can define sync/ real time?

## Copyright

This CIP is licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).
