---
CIP: ?
Title: Governance Metadata - Constitution
Category: Metadata
Status: Proposed
Authors:
    - Ryan Williams <ryan.williams@intersectmbo.org>
Implementors: []
Discussions:
    - https://github.com/cardano-foundation/CIPs/pull/?
Created: 2024-03-19
License: CC-BY-4.0
---

## Abstract

Cardano's minimum viable governance model as described within [CIP-1694 | A First Step Towards On-Chain Decentralized Governance](https://github.com/cardano-foundation/CIPs/blob/master/CIP-1694/README.md) introduces the concept of a Cardano constitution.
Although CIP-1694 gives no definition to the constitution's content or form.

This proposal aims to describe a standardized form for the Cardano constitution.
Aiming to enhance the accessibility, readability and safety of the document.

> **Note:** This proposal only covers the technical form of the constitution, this standard is agnostic to the content of the constitution.

## Motivation: why is this CIP necessary?

CIP-1694 defines the on-chain anchor mechanism used to link the off-chain constitution document to on-chain actions.
This mechanism was chosen due to its simplicity and cost effectiveness, moving the potentially large Cardano constitution off chain, referencing it via a hash digest and URI.
This is the extent to which CIP-1694 outlines the constitution, it does provide suggestions around hashing algorithm, off-chain storage location, rich text styling.

By formalizing the form of the constitution and it's iterations, we aim to promote it's longevity and accessibility.
This is essential for the governance model

Like the Cardano constitution this standard impacts every ada holder.

### Safety

Without describing best practices for the form and handling of the constitution, we risk the constitution document being stored in an insecure manner.
By storing the constitution on a decentralized platform, we can ensure it's immutability and permissionless access.
This is a step to ensuing the longevity and accessibility of each constitution iteration.

### Interoperability

By defining a file extension and formatting rules for the constitution we ensure that tooling reading and writing the constitution will be interoperable.
Furthermore we aim to make roles constitution iteration comparison tools easy, by minimizing formatting and style changes between iterations.
This will reduce compatibility issues between tools, promoting the accessibility of the constitution.

### Usability

Rich text formatting greatly enhances the readability of text, especially in large complex documents.
Without the ability to format text, it could easily become cumbersome to read, negatively effecting the accessability of the Cardano constitution.

## Specification

The following specification should be applied to all constitution iterations.
This standard could be augmented in the future via a separate CIP which aims to replace this one.

### File Type
// todo - any suggestions?

### Hashing

When supplying a constitution hash digest to chain, the algorithm used MUST be Blake2b-256.
Before creating a hash digest the constitution plain text must be in its raw un-rendered format.

- add a way to change algorithm?

### Storage

The each ratified constitution MUST be stored, immutably on a distributed storage mechanism (such as IPFS).
Where backups can be easily made in a permission less manor by interested parties.
Must be easily accessible, normal tooling can support it.
Authors SHOULD NOT specify the use of centralized gateways to access the constitution plain text.

### Rich Text Formatting

The constitution text MAY include a subset of markdown text styling.
Tooling rendering the constitution for users, should recognize these and render them faithfully.

#### Headers

```md
# H1
## H2
### H3
#### H4
##### H5
###### H6

Alternatively, for H1 and H2, an underline-ish style:

Alt-H1
======

Alt-H2
------
```

#### Emphasis

```md
Emphasis, aka italics, with *asterisks* or _underscores_.

Strong emphasis, aka bold, with **asterisks** or __underscores__.

Combined emphasis with **asterisks and _underscores_**.

Strikethrough uses two tildes. ~~Scratch this.~~
```

#### Lists

```md
1. First ordered list item
2. Another item
⋅⋅* Unordered sub-list. 
1. Actual numbers don't matter, just that it's a number
⋅⋅1. Ordered sub-list
4. And another item.
```

#### Links

```md
[I'm an inline-style link](https://www.google.com)
```

#### Code and Syntax Highlighting

```md
Inline `code` has `back-ticks around` it.
```

#### Tables

```md
Colons can be used to align columns.

| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |

There must be at least 3 dashes separating each header cell.
The outer pipes (|) are optional, and you don't need to make the 
raw Markdown line up prettily. You can also use inline Markdown.

Markdown | Less | Pretty
--- | --- | ---
*Still* | `renders` | **nicely**
1 | 2 | 3
```

#### Blockquotes

```md
> Blockquotes are very handy in email to emulate reply text.
> This line is part of the same quote.

Quote break.

> This is a very long line that will still be quoted properly when it wraps. Oh boy let's keep writing to make sure this is long enough to actually wrap for everyone. Oh, you can *put* **Markdown** into a blockquote. 
```

#### Horizontal Rule

```md
Three or more...

---

Hyphens

***

Asterisks

___

Underscores
```

#### Line Breaks

```md
Here's a line for us to start with.

This line is separated from the one above by two newlines, so it will be a *separate paragraph*.

This line is also a separate paragraph, but...
This line is only separated by a single newline, so it's a separate line in the *same paragraph*.
```

#### Not supported
- Images
- Inline HTML
- Footnotes (it is a github specific addition to markdown)

### Best Practices

Where there are multiple ways to use markdown to represent the same structure via markdown authors should strive to ensure the document is consistent in ones use.
- when hash doesnt match
- when unrecognised formatting/style
- 

## Rationale: how does this CIP achieve its goals?
<!-- The rationale fleshes out the specification by describing what motivated the design and what led to particular design decisions. It should describe alternate designs considered and related work. The rationale should provide evidence of consensus within the community and discuss significant objections or concerns raised during the discussion.

It must also explain how the proposal affects the backward compatibility of existing solutions when applicable. If the proposal responds to a CPS, the 'Rationale' section should explain how it addresses the CPS, and answer any questions that the CPS poses for potential solutions.
-->

Just like CIP-1694, we aim to define a minimal viable set of standards to ensure governance can be achieved.

### Why no enforcement on the structure
// todo

### File Type
// todo

### Hashing
- we choose blake2b-256 as it is a standard for hashing in Cardano
- normalizing the constitution data before hashing ensures that regardless of tooling rendering, the hashes can be deterministicly produced between tools
- standard, lots of tools already use it 

### Storage
- The constitution is the most important document for Cardano (?), ensuring its permissionless accessibly is paramount
- Storing each iteration immutably is just as important, to allow access of past constitutions
- IPFS is well known already with good tooling support -> improve accessibility

### Rich Text Formatting
- wanted to keep a bare minimum spec, no images or videos
- also dont want people to be able to attack consumers by attacks utilizing the HTML

## Path to Active

### Acceptance Criteria

- [ ] This standard is followed for the interim Cardano constitution
- [ ] This standard is utilized by two tools reading constitution data from chain

### Implementation Plan

#### Solicitation of feedback

- [ ] Review from the Civics Committee
- [ ] Review from X working group

#### Test vector

- [ ] Author to provide a test vector file with multiple examples

## Copyright

This CIP is licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).
