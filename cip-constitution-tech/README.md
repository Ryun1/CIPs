---
CIP: ?
Title: Constitution form
Category: Metadata
Status: Proposed
Authors:
    - Ryan Williams <ryan.williams@intersectmbo.org>
Implementors: []
Discussions:
    - https://github.com/cardano-foundation/CIPs/pull/796
Created: 2024-03-19
License: CC-BY-4.0
---

## Abstract

Cardano's minimum viable governance model as described within [CIP-1694 | A First Step Towards On-Chain Decentralized Governance](https://github.com/cardano-foundation/CIPs/blob/master/CIP-1694/README.md) introduces the concept of a Cardano constitution.
Although CIP-1694 gives no definition to the constitution's content or form.

This proposal aims to describe a standardized technical form for the Cardano Constitution to enhance the accessibility and safety of the document.

> **Note:** This proposal only covers the technical form of the constitution, this standard is agnostic to the content of the constitution.

## Motivation: why is this CIP necessary?

CIP-1694 defines the on-chain anchor mechanism used to link the off-chain Constitution document to on-chain actions.
This mechanism was chosen due to its simplicity and cost effectiveness, moving the potentially large Cardano constitution off-chain, leaving only a hash digest and URI on-chain.
This is the extent to which CIP-1694 outlines the Cardano Constitution: CIP-1694 does not provide suggestions around hashing algorithm, off-chain storage best practices or use of rich text styling.

By formalizing the form of the constitution and its iterations, we aim to promote its longevity and accessibility.
This is essential to ensure the effectiveness of the CIP-1694 governance model.

This standard will impact how ada holders read the constitution but the main stakeholders for this are the tool makers who wish to read, render and write the constitution.

### Safety

Without describing best practices for the form and handling of the constitution, we risk the constitution document being stored in an insecure manner.
By storing the constitution on a decentralized platform, we can ensure it's immutability and permissionless access.
This is a step to improve the longevity and accessibility of each constitution iteration.

### Interoperability

By defining a file extension and formatting rules for the constitution we ensure that tooling reading and writing the constitution will be interoperable.
Furthermore we aim to make the role of constitution iteration comparison tools easier, by minimizing formatting and style changes between iterations.
This will reduce compatibility issues between tools, promoting the accessibility of the constitution.

### Usability

Rich text formatting greatly enhances the readability of text, especially in large complex documents.
Without the ability to format text, it could easily become cumbersome to read, negatively effecting the accessability of the Cardano constitution.

## Specification

The following specification SHOULD be applied to all constitution iterations.
This standard could be augmented in the future via a separate CIP which aims to replace this one.

### Sentences

The constitution text MUST only contain at maximum one sentence per line.
Each sentence MUST be followed by a newline.

Each sentence SHOULD start on its own line with a capitalized letter.

Example:

```md
This is a short sentence on one line.

This is a long sentence and I have valid reasons for it being so long,
such as being an example of a long sentence.
```

It is recommended that each line is ended by either a full stop or comma.

### File Type

The constitution file MUST be a text file named `constitution.txt`.

### Hashing

When supplying a constitution hash digest to chain, the algorithm used MUST be Blake2b-256.
Before creating a hash digest the constitution plain text MUST be in its raw text, including any [Rich Text Formatting](#rich-text-formatting) related characters.

### Storage

The each ratified constitution MUST be stored, immutably on a distributed storage mechanism such as IPFS.
Where backups can be easily made in a permissionless manner by interested parties.
This storage platform MUST be easily accessible, with strong tooling support.
Authors SHOULD NOT specify the use of centralized gateways to access the constitution plain text.

// only ascii

### Rich Text Formatting

The constitution text MAY include a strict subset of rich text styling as defined in this specification.
Tooling rendering the constitution SHOULD recognize these and render them faithfully.

#### Headers

Headers are denoted via a hashtag character `#` followed by a space ` `.
There are six levels to headers with, each being defined via a extra `#`.
Headers are ended via a line break.
Headers SHOULD be followed below by a blank line.
Headers SHOULD not be preceded by whitespace.

The lower the number of `#` the larger order the text SHOULD be rendered.

Example:
```md
# H1

## H2

### H3

#### H4

##### H5

###### H6

```

If text is in a header no other formatting can be applied.

#### Emphasis

Emphasis is applied to text between single or double asterisks, without space between asterisks and text.
Italicized emphasis is shown via single asterisk (`*`).
Bold emphasis is shown via double asterisks (`**`).

Emphasis cannot span multiple lines.

Examples:
```md
Emphasis, aka italics, with single *asterisks*.

Strong emphasis, aka bold, with double **asterisks**.
```

The text contained within headings can be emphasized.

Both italicized and bold cannot be applied to the same text.

#### Code and Syntax Highlighting

Texted can be highlighted as code, when encased without spaces by backticks.
This MUST not contain line breaks.

Example:
```md
Inline `code` has `back-ticks around` it.
```

The text contained within headings or emphasis cannot be highlighted as code.


#### Unordered Lists

// todo

#### Line Breaks / Paragraphs

To create paragraphs, use a blank line to separate one or more lines of text.

Examples:
```md
Here's a line for us to start with.

This line is separated from the one above by two newlines, so it will be a *separate paragraph*.

This line is also a separate paragraph, but...
This line is only separated by a single newline, so it's a separate line in the *same paragraph*.
```

### Best Practices
- when hash doesnt match
- when unrecognised formatting/style
- Keep lines left-aligned without unneeded whitespace or tabs
- tabs vs spaces

## Rationale: how does this CIP achieve its goals?

Just like CIP-1694, we aim to define a minimal viable set of standards to ensure governance can be achieved.

### Sentences
- improve the readability of diff views

### Versioning
- why not build in options in hashalgo (like CIP100)
- why a whole replacement?

### File Type
- just simple and easy

### Hashing
- we choose blake2b-256 as it is a standard for hashing in Cardano
- standard, lots of tools already use it 

### Storage
- The constitution is the most important document for Cardano (?), ensuring its permissionless accessibly is paramount
- Storing each iteration immutably is just as important, to allow access of past constitutions
- IPFS is well known already with good tooling support -> improve accessibility

### Rich Text Formatting
- why not all markdown?
- wanted to keep a bare minimum spec, no images or videos
- also dont want people to be able to attack consumers by attacks utilizing the HTML
- wanted to allow standard markdown libs to work

## Open Questions
- [x] How can we support multi-languages?
  - The Cardano constitution will be in English, but we will add best practice guidelines via [Best Practices](#best-practices).
- [ ] Should we specify any standardization for the proposal policy?
- [x] How can we add page breaks?
  - We wont, instead we will prioritize a minimum set of rich text formatting. We can provide some guidance via [Best Practices](#best-practices).
- [x] Do we want a mechanism for specifying authors? (similar to CIP-100)
  - No, as CIP-100 compliant metadata can be supplied at time of constitution update.
- [ ] What should we name the constitution file? we could embed some nice naming or metadata.

## Path to Active

### Acceptance Criteria

- [ ] This standard is followed for the interim Cardano constitution
- [ ] This standard is utilized by two tools reading constitution data from chain

### Implementation Plan

#### Solicitation of feedback

- [ ] Answer all [Open Questions](#open-questions)
- [ ] Review from the Civics Committee
- [ ] Review from X working group

#### Test vector

- [ ] Author to provide a test vector file with examples.

## Acknowledgements

<details>
  <summary><strong>First draft</strong></summary>
  
  We would like to thank those who reviewed the first draft of this proposal;
    - Danielle Stanko
    - Kevin Hammond
    - Steven Johnson 

</details>

## Copyright

This CIP is licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).