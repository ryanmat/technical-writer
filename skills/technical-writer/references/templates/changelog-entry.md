---
type: changelog entry
domain: engineering
default_audience: engineer
source: Keep a Changelog 1.1.0 (keepachangelog.com/en/1.1.0) for the file shape, the version heading with its date, the Unreleased section and the entry rule; the six categories by reference to style-rules.md
license: MIT
h1_pattern: '(?i)^(?=\S+ \S).*\bchangelog\b.*$'
sections:
  - heading_pattern: '^(?:\[Unreleased\]|\[?v?\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?\]? - \d{4}-\d{2}-\d{2}(?: \[YANKED\])?)$'
    label: the version section
    level: 2
    evidence:
      pattern: '(?:#\d+|\b(?!(?:SHA|UTF|MD|AES|RSA|HMAC|CRC|CVE|ISO|RFC|TLS|SSL|HTTP|IPV|OAUTH)-)[A-Z][A-Z0-9]*-\d+\b|\b(?=[0-9a-f]*[a-f])[0-9a-f]{7,40}\b)'
      missing: the issue, pull request or commit each entry names
  - heading_pattern: '^(?:Added|Changed|Deprecated|Removed|Fixed|Security)$'
    label: a category section
    level: 3
length_caps:
  engineer: 2000
  executive: 400
banned_patterns:
  - pattern: '^\s*[-*+]\s+(?!.*(?:#\d+|\b(?!(?:SHA|UTF|MD|AES|RSA|HMAC|CRC|CVE|ISO|RFC|TLS|SSL|HTTP|IPV|OAUTH)-)[A-Z][A-Z0-9]*-\d+\b|\b(?=[0-9a-f]*[a-f])[0-9a-f]{7,40}\b|\[UNVERIFIED:)).*$'
    rule: every entry names the issue, pull request, or commit that made the change as plain text or link text, or carries the marker; an algorithm or standard name (SHA-256, UTF-8, CVE-1900-0001, RFC-9110) is not a key, and a commit hash carries at least one letter, so a bare number is not one
---
# <PROJECT_NAME> changelog

A changelog entry is the block a release adds to the project's `CHANGELOG.md`: one version
section with its date, or the Unreleased section, and the changes grouped under the Keep a
Changelog categories. The skill writes the block as a standalone document with the file's
title and summary so the checker can read it; the user pastes the version section into the
file above the previous version. The front matter above is what `check_structure.py`
enforces. Release notes, the dated page a reader visits, are a different type with their own
template; the two share the category list in
[style-rules.md](../style-rules.md#change-categories).

## Title

The H1 and the only H1: the project name and the word changelog, as the file's own title. A
title the user gives is kept as given.

## Summary line

One sentence directly under the title. The source opens its file with "All notable changes to
this project will be documented in this file."; this template writes it as the project's own
sentence. The checker requires exactly one sentence here.

## Version section

Required, one per version in the entry, newest first. The heading is the version in brackets,
a space, a hyphen, a space and the release date in ISO 8601 form, as the source writes it:
`## [2.5.1] - 2026-10-17`, with ` [YANKED]` after the date for a pulled release. The source's
unreleased block is `## [Unreleased]` with no date, kept at the top of the file for the changes
not yet released. A version heading without its date, or a date in another form, matches no
section and is reported as unknown. A release date the sources do not give is a reason to
write the entry under Unreleased, never to invent the date.

Evidence slot: an issue, pull request or commit identifier somewhere in the section, which the
entries below supply.

## Categories

Required: at least one level-three category under each version, from the six in
[style-rules.md](../style-rules.md#change-categories), in that order, each present only when it
has entries. A heading outside the six is an unknown section; a change that fits none of the six
is Changed.

## Entries

One bullet per notable change, written for the reader, not from the commit log. Every entry
names the issue, pull request or commit that made the change, in parentheses at the end as
plain text or as link text: `(RELAY-440)`, `([#440](url))`, or a commit hash of seven or more
characters. The checker reads prose with code spans blanked, so an identifier in code style
counts as missing. An entry whose sources give no identifier carries the marker instead:

```text
- The route registration call rejects a retry limit above the platform cap. [UNVERIFIED: the issue or pull request that made this change]
```

An entry that breaks compatibility opens with Breaking: in bold under Changed or Removed and
says what the reader must do, as the release notes template writes it.

## Prose rules

- One entry per noteworthy difference, often across several commits; never one entry per
  commit.
- The reader's terms, not the code's: what changed for them, not which function moved.
- No Unreleased section in release notes and no undated version in a changelog; the two types
  are not interchanged.
- The caps count words outside code blocks.

## Source

File shape, the version heading with its date, the Unreleased section, the YANKED mark and the
quoted lines: Keep a Changelog 1.1.0, `keepachangelog.com/en/1.1.0`, created and maintained by
Olivier Lacan, MIT licensed. The six categories are quoted once, in style-rules.md, and
referenced here. The identifier rule and the Breaking convention are this skill's rules,
shared with the release notes template. The rest of this file is this skill's own text.
