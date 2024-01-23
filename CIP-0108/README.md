---
CIP: 108
Title: Governance Metadata - Governance Actions
Category: Metadata
Status: Proposed
Authors:
  - Ryan Williams <ryan.williams@intersectmbo.org>
Implementors: [ ]
Discussions:
  - https://github.com/cardano-foundation/cips/pulls/632
Created: 2023-11-23
License: CC-BY-4.0
---

## Abstract
The conway ledger era ushers in on-chain governance for Cardano via [CIP-1694 | A First Step Towards On-Chain Decentralized Governance](https://github.com/cardano-foundation/CIPs/blob/master/CIP-1694/README.md), with the addition of many new on-chain governance artifacts.
Some of these artifacts support the linking off-chain metadata, as a way to provide context.

The [CIP-100 | Governance Metadata](https://github.com/cardano-foundation/CIPs/tree/master/CIP-0100) standard provides a base framework for how all off-chain governance metadata should be formed and handled.
But this is intentionally limited in scope, so that it can be expanded upon by more specific subsequent CIPs.

This proposal aims to provide a specification for off-chain metadata vocabulary can be used to give context to governance actions, CIP-100.
Without a sufficiently detailed standard for governance actions we introduce the possibility to undermine voters ability to adequately assess governance actions.
Furthermore a lack of such standards risks preventing interoperability between tools, to the detriment of user experiences.

### Acknowledgments

<details>
  <summary><strong>Governance Metadata Working Group - Workshop #1 2023-12-04</strong></summary>

  I would like to thank those that contributed to the Governance Metadata Working Group Workshop #1 hosted by Ryan Williams ([see presentation slides with notes](https://docs.google.com/presentation/d/18OK3vXexCc8ZXq-dC00RDPPKcy2Zu4DiMo8PeIZ47_4/)).

  Thank you to the co-hosts:
  - Adam Dean
  - Thomas Upfield

  Thank you to the participants:
  - Carlos Lopez de Lara
  - Igor Veličković
  - Johnny Kelly
  - Kenric Nelson
  - Kevin Hammond
  - Lorenzo Bruno
  - Mike Susko
  - Rhys Morgan
  - Eric Alton
  - Samuel Leathers
  - Vladimir Kalnitsky

</details>

<details>
  <summary><strong>Governance Metadata Working Group - Workshop #2 2023-12-14</strong></summary>

  I would like to thank those that contributed to the Governance Metadata Working Group Workshop #2 hosted by Ryan Williams ([see presentation slides with notes](https://docs.google.com/presentation/d/1tFsyQnONjwyTm7zKrnxxedzWsoonO6-8vXw5vYzB3qs)).

  Thank you to the co-host:
  - Adam Dean

  Thank you to the participants:
  - Mark Byers
  - Nils Codes

  Thank you to the bots that joined also.

</details>

## Motivation: why is this CIP necessary?
Blockchains are poor choices to act as content databases.
This is why governance metadata anchors were chosen to provide a way to attach long form metadata content to on-chain events.
By only supplying an onchain hash of the off-chain we ensure correctness of data whilst minimizing the amount of data posted to the chain.

### For voters
When observing from the chain level, tooling can only see the content of the governance action and it's anchor.
These on-chain components do not give give any context to the motivation nor off-chain discussion of an governance action.
Although this information would likely be desired context for voters.
By providing rich contextual metadata we enable voters to make well informed decisions.

### For all participants
By standardizing off-chain metadata formats we facilitate interoperability for tooling which creates and/or renders metadata attached to governance actions.
This intern promotes a rich user experience between tooling.
This is good for all governance participants.

## Specification
Although there are seven types of governance action defined via CIP-1694, we focus this proposal on defining core properties which must be attached to all types.
We leave room for future standards to refine and specialize further to cater more specific for each type of governance action.

### Markdown Text Styling
This standard introduces the possibility of using [Github markdown text styling](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#styling-text) within fields.

### Extended Vocabulary
The following properties extend the potential vocabulary of [CIP-100](https://github.com/cardano-foundation/CIPs/tree/master/CIP-0100)'s `body` property.

#### `title`
- A very short freefrom text field. Limited to `80` characters.
- This SHOULD NOT support markdown text styling.
- Authors SHOULD use this field to succinctly describe the governance action and its motivation.
- Authors SHOULD attempt to make this field unique whilst also avoiding hyperbolic language.
- i.e; Increase K protocol parameter to `100,000` to increase decentralization of Cardano.

#### `abstract`
- A short freefrom text field. Limited to `2500` characters.
- This SHOULD support markdown text styling.
- Authors SHOULD use this field to expand upon their `title` by describing the contents of the governance action, its motivation and rationale.

#### `motivation`
- A freeform text field.
- This SHOULD support markdown text styling.
- This SHOULD be used by the author to encapsulate all context around the problem that is being solved by the on-chain action.
- This SHOULD be used to outline the related stakeholders and use cases. 

#### `rationale`
- A freeform text field.
- This SHOULD support markdown text styling.
- This SHOULD be used by the author to discuss how the content of the governance action addresses the problem outlined within the `motivation`.
- This field SHOULD justify the changes being made to Cardano.
- i.e "by decreasing X parameter by Y we increase Ada earned by SPOs, thus incentivising more people to become SPOs, leading to a more diverse network"
- This SHOULD provide evidence of consensus within the community and discuss significant objections or concerns raised during the discussion.
- This SHOULD include discussion of alternative solutions and related topics/ governance actions.
- This SHOULD include any recommendations made by relevant organizations or committees.

#### `references`
- We extend CIP-100's references field.
- This SHOULD NOT support markdown text styling.
- To be an OPTIONAL set of objects, using the `@set` property.
- Each object MUST have a `title` field to describe the reference, such as; "blog - Why we must continue to fund Catalyst".
- Each object MUST have a `uri` field.
- Each object MAY have a OPTIONAL `URIHash` object.
  - Each object MUST have a `hash` field.
  - Each object MUST have a `hashAlgo` field.
- This should be used by the author to link related or supporting work via the URI, and reference this via the index within their freefrom text fields.

### Application
Governance action metadata must include all compulsory fields to be considered CIP-0108 compliant.
Unlike with CIP-0100, here we prescribe that authors MUST include all fields.

### Test Vector
See [test-vector.md](./test-vector.md) for examples.

### Versioning
This proposal should not be versioned, to update this standard a new CIP should be proposed.
Although through the JSON-LD mechanism further CIPs can add to the common governance metadata vocabulary,

## Rationale: how does this CIP achieve its goals?
We intentionally have kept this proposal brief and uncomplicated.
This was to reduce the time to develop and deploy this standard.
We think it is better to have a base standard which can be improved, rather than meticulously craft a perfect single standard.
This way we enable tooling which depends on this standard to start development.
Furthermore, it is very difficult to predict future wants/needs now, so by allowing upgrades we build in the ability to improve the standard as new wants/needs arrive.

The fields which have been chosen for this standard heavily inspired to those used for CIPs.
We did this for two reasons; familiarity and competency.
Those who are involved in Cardano are familiar with the CIP format, meaning they will be intuitively understand these fields being reused here.
These fields in combination have also been fairly battle tested via the CIPs process and thus act as a good standard to describe problems and their solutions.

### Character Limits
With this design, we wanted to allow for quick and easy differentiation between governance actions.
We achieve this by facilitating users "layers of investigation", where some fields are limited in size.
This encourages tooling providers to show users the small fields before allowing deep investigation of the larger fields.
By allowing this we aim to improve the experience of prospective voters, when sorting though many governance actions.

The downside of highlighting some fields over others is that we incentivize hyperbolic and eye catching phrases. 
Where authors want their governance action to standout in tooling so use overly dramatic phrasing.
This creates an environment where there is a race to the bottom on voter's attention.
Overall this could decrease the perceived legitimacy of the system.
The counter argument is that tooling providers should not use metadata to solely highlight proposals, rather other means such as cryptographically verified submitters.

### `title`
This should be used by voters to quickly and easily differentiate between two governance actions which may be having the same or similar on-chain effects.
This is why we have chosen a short character limit, as longer titles would reduce the ability for quick reading.

### `abstract`
This gives voters one step more detail beyond the `title`.
This allows for a compact description of the what, why and how without the voter having to read the larger fields.

### `motivation`
The `motivation` is a chance for the author to fully describe the problem that is being solved by the governance action.
This is important as all governance actions are a solution to a problem and thus this is a universal field.
By showing relation to stakeholders the author is able to show that they have performed adequate research on the problem.
Voters can use this field to determine if the problem is sizable enough to warrant voting on.

### `rationale`
This field gives the author the opportunity to explain how the onchain action is addressing the problem outlined in the motivation.
This gives the author a place to discuss any alternative designs or completing governance actions.
Voters should be able to use this field to evaluate the applicability of the solution to the problem.

### `references`
References give the author ability to point to supporting research or related work.
These should be used by voters to verify the content of supporting research.
The inclusion of a hash allows for the supporting documentation to be cryptographically verified.

### Open Questions
- <s>Should fields be optional or compulsory?</s>
  - Title, abstract, motivation and rationale should be compulsory as they should be very important to the ability 
- <s>How much vocabulary can be extended to other onchain governance events?</s>
  - It is hard to predict how the scope of future standards before they have been developed.
- <s>How to integrate custom set of HTML tags? to allow formatting of longer text fields.</s>
  - Since CIP-100 does not intend to support rich text fields such an inclusion would not fit, so we have included such format here.

## Path to Active

### Acceptance Criteria
- [ ] This standard is supported by two different tooling providers used to submit governance actions to chain.
- [ ] This standard is supported by two different chain indexing tools, used to read and render metadata.

### Implementation Plan
Solicitation of feedback
- [x] Run two online workshops to gather insights from stakeholders.
- [ ] Seek community answers on all [Open Questions](#open-questions).
Implementation
- [ ] Author to provide example metadata and schema files.

## Copyright
This CIP is licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).