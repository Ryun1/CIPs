# CPS Validation Rules

This document describes all validation rules applied to Cardano Problem Statement (CPS) documents.

These validations are to be ran automatically via Github workflow using [`/scripts/validate-cps.py`](./scripts/validate-cps.py).

These attempt to codify the guidance described within [CIP-9999 | Cardano Problem Statements](../CIP-9999/README.md).

## File-Level Validations

| Validation | Description |
| ---------- | ----------- |
| File path | Must be in a `CPS-*` directory |
| Directory name | If the `CPS` field has an assigned number (not `?`), the directory must be named `CPS-NNNN` where `NNNN` is the CPS number zero-padded to 4 digits (e.g., `CPS: 12` → `CPS-0012/`) |
| Line endings | Must use UNIX line endings (LF), not Windows (CRLF) or old Mac (CR) |
| Frontmatter | Must have valid YAML frontmatter between `---` delimiters |
| No H1 headings | H1 (`#`) headings are not allowed in the document body |

## Header Field Validations

All 9 fields are **required**,
must appear in order,
and no extra fields are allowed.

| Field | Order | Validation Rules |
| ----- | ----- | ---------------- |
| **CPS** | 1 | Positive integer (`1`, `42`) or `?`/`??`/etc. for unassigned. No leading zeros. |
| **Title** | 2 | 1-100 characters, no backticks (`` ` ``) |
| **Category** | 3 | One of: `Meta`, `Wallets`, `Tokens`, `Metadata`, `Tools`, `Plutus`, `Ledger`, `Consensus`, `Network`, `?` |
| **Status** | 4 | `Open`, `Solved`, or `Inactive` (optionally with reason, e.g., `Inactive (Superseded)`) |
| **Authors** | 5 | Non-empty list, each entry: `Name <email>` |
| **Proposed Solutions** | 6 | List (can be empty), each entry: `Label: URL` |
| **Discussions** | 7 | Non-empty list, each entry: `Label: URL` |
| **Created** | 8 | Date in `YYYY-MM-DD` format |
| **License** | 9 | `CC-BY-4.0` or `Apache-2.0` |

## CIP Label Validation

For the **Proposed Solutions** and **Discussions** fields,
when an entry label matches the `CIP-NNNN` pattern,
extra validation applies:

| Rule | Description |
| ---- | ----------- |
| GitHub URL required | Must be `https://github.com/cardano-foundation/CIPs/...` |
| Valid URL types | `/pull/NNN` (PR) or `/tree/{branch}/CIP-NNNN` or `/blob/{branch}/CIP-NNNN` (merged) |
| `?` suffix for PRs | `CIP-0030?` required when linking to a pull request (candidate) |
| No `?` for merged | `CIP-0030` (without `?`) required when linking to a merged CIP |

Non-CIP labels (e.g., `Forum Post`, `Pull Request`) are allowed with any valid URL.

## Required Sections (H2 Headers)

The following sections must exist in this order with **exact capitalization**.

**No other H2 sections are allowed** except the optional sections listed below.

| Order | Section |
| ----- | ------- |
| 1 | `Abstract` |
| 2 | `Problem` |
| 3 | `Use Cases` |
| 4 | `Goals` |
| 5 | `Open Questions` |
| 6 | `Copyright` |

## Optional Sections

The following sections are allowed with exact capitalization.
They **must** appear after `Open Questions` and before `Copyright`:

- `References`
- `Appendices`
- `Acknowledgments` / `Acknowledgements`

Optional sections appearing before any required section (other than `Copyright`) will cause validation to fail.

## URL Validation

Every URL referenced in a CPS — both in header fields (`Discussions`, `Proposed Solutions`) and in the markdown body (`[text](url)` links, bare URLs) — is checked for liveness by [`/scripts/check-cps-urls.py`](./scripts/check-cps-urls.py).

| Rule | Description |
| ---- | ----------- |
| Scheme | Only `http://` and `https://` URLs are checked. Other schemes (`mailto:`, `ftp:`, anchor-only `#…`) are skipped. |
| Method | HEAD request first; falls back to GET if the server rejects HEAD with 405/501. |
| Redirects | Followed automatically (up to the urllib default). |
| Timeout | 10 seconds per request. |
| Retry | One retry with a 2-second backoff on 5xx or connection errors. |
| Auth-walled | HTTP 401 and 403 are treated as **alive** — the resource exists, just requires authentication. |
| Dead | Any 4xx other than 401/403 (most commonly 404, 410). Fails the workflow. |
| Transient | Persistent 5xx or connection errors after retry. Logged as warnings; does **not** fail the workflow. |
| Skipped | URLs inside fenced code blocks (```` ``` ````), inline code spans (`` ` ``), and HTML comments (`<!-- … -->`) are not checked. |

URLs are deduplicated per file before checking, so a URL that appears many times in one document only costs one request.
