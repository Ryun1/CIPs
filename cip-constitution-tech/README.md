---
CIP: ?
Title: Constitution storage and tooling
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

This proposal aims to describe a standardized technical form for the Cardano constitution.
Aiming to enhance the accessibility and safety of the document.

> **Note:** This proposal only covers the technical form of the constitution, this standard is agnostic to the content of the constitution.

## Motivation: why is this CIP necessary?

CIP-1694 defines the on-chain anchor mechanism used to link the off-chain constitution document to on-chain actions.
This mechanism was chosen due to its simplicity and cost effectiveness, moving the potentially large Cardano constitution off-chain, leaving only a a hash digest and URI on-chain.
This is the extent to which CIP-1694 outlines the constitution, it does provide suggestions around hashing algorithm, off-chain storage location, rich text styling.

By formalizing the form of the constitution and it's iterations, we aim to promote it's longevity and accessibility.
This is essential to ensure the effectiveness of the CIP-1694 governance model.

This standard will impact how ada holders read the constitution but the main stakeholders for this are the tool makers who wish to read and write the constitution.

### Safety

Without describing best practices for the form and handling of the constitution, we risk the constitution document being stored in an insecure manner.
By storing the constitution on a decentralized platform, we can ensure it's immutability and permissionless access.
This is a step to ensuing the longevity and accessibility of each constitution iteration.

### Interoperability

By defining a file extension and formatting rules for the constitution we ensure that tooling reading and writing the constitution will be interoperable.
Furthermore we aim to make the role of constitution iteration comparison tools easier, by minimizing formatting and style changes between iterations.
This will reduce compatibility issues between tools, promoting the accessibility of the constitution.

### Usability

Rich text formatting greatly enhances the readability of text, especially in large complex documents.
Without the ability to format text, it could easily become cumbersome to read, negatively effecting the accessability of the Cardano constitution.

## Specification

The following specification should be applied to all constitution iterations.
This standard could be augmented in the future via a separate CIP which aims to replace this one.

### Sentences

The constitution text must only contain one sentence per line.
Each sentence must be followed by a newline.

### File Type

The constitution file must be a text (`.txt`) file.

### Hashing

When supplying a constitution hash digest to chain, the algorithm used MUST be Blake2b-256.
Before creating a hash digest the constitution plain text must be in its raw text, including any [Rich Text Formatting](#rich-text-formatting).

### Storage

The each ratified constitution MUST be stored, immutably on a distributed storage mechanism (such as IPFS).
Where backups can be easily made in a permission less manner by interested parties.
Must be easily accessible, normal tooling can support it.
Authors SHOULD NOT specify the use of centralized gateways to access the constitution plain text.

### Rich Text Formatting

The constitution text MAY include a subset of markdown text styling as defined in this specification.
Tooling rendering the constitution for users, should recognize these and render them faithfully.

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

Alternative headers using an underline-ish style are not supported.

#### Emphasis

Emphasis is applied to text between single or double asterisks, without space between asterisks and text.
Italicized emphasis is shown via single asterisk (`*`).
Bold emphasis is shown via double asterisks (`**`).

Italicized and bold text can be shown using a combination, resulting in three asterisks on either side of the text.

The text contained within headings can be emphasized.

Examples:
```md
Emphasis, aka italics, with single *asterisks*.

Strong emphasis, aka bold, with double **asterisks**.

Combined emphasis, with triple ***asterisks***.
```

Alternate emphasis using underscores are not supported, nor is strikethrough emphasis.

#### Links

Text can be hyperlinked by being encased with square brackets and then be immediately followed by a URL in parentheses.
Link text cannot contain line breaks.
URLs cannot contain line breaks or spaces.

To emphasize links, add asterisks before and after the brackets and parentheses. To denote links as code, add backticks in the brackets.
Headings can  be linked, but the the brackets must enclose the text and not the hash character.

Examples:
```md
[I'm an inline-style link](https://www.google.com)

**[I'm an emphasized inline-style link](https://www.google.com)**

# [I'm an inline-style link in a heading](https://www.google.com)
```

Link titles are not supported, nor is using angled brackets for links.
Reference style links are also not supported.

#### Code and Syntax Highlighting

Texted can be highlighted as code, when encased without spaces by backticks.
This must not contain line breaks.

Example:
```md
Inline `code` has `back-ticks around` it.
```

Code blocks are not allowed.

#### Line Breaks / Paragraphs

To create paragraphs, use a blank line to separate one or more lines of text

Examples:
```md
Here's a line for us to start with.

This line is separated from the one above by two newlines, so it will be a *separate paragraph*.

This line is also a separate paragraph, but...
This line is only separated by a single newline, so it's a separate line in the *same paragraph*.
```

#### Not supported

All other markdown formatting is not permitted.
Including;
- Tables
- Lists
- Backquotes
- Horizontal rules
- Images
- Inline HTML
- Footnotes

### Best Practices

- when hash doesnt match
- when unrecognised formatting/style
- how to render -> page breaks
- table of contents?
- Keep lines left-aligned without unneeded whitespace or tabs

## Rationale: how does this CIP achieve its goals?
<!-- The rationale fleshes out the specification by describing what motivated the design and what led to particular design decisions. It should describe alternate designs considered and related work. The rationale should provide evidence of consensus within the community and discuss significant objections or concerns raised during the discussion.

It must also explain how the proposal affects the backward compatibility of existing solutions when applicable. If the proposal responds to a CPS, the 'Rationale' section should explain how it addresses the CPS, and answer any questions that the CPS poses for potential solutions.
-->

Just like CIP-1694, we aim to define a minimal viable set of standards to ensure governance can be achieved.

### Versioning
- why not build in options in hashalgo (like CIP100)
- why a whole replacement?

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
- why not all markdown?
- wanted to keep a bare minimum spec, no images or videos
- also dont want people to be able to attack consumers by attacks utilizing the HTML

## Open Questions
- [x] How can we support multi-languages?
  - The Cardano constitution will be in English, but we will add best practice guidelines via [Best Practices](#best-practices).
- [ ] Should we specify any standardization for the proposal policy?
- [x] How can we add page breaks?
  - We wont should instead prioritize a minimum set of rich text formatting. We can provide some guidance via [Best Practices](#best-practices).
- [x] Do we want a mechanism for specifying authors? (similar to CIP-100)
  - No, as CIP-100 compliant metadata can be supplied at time of constitution update.

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

## Copyright

This CIP is licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).
