---
type: release notes
domain: user documentation
default_audience: engineer
source: Keep a Changelog 1.1.0 (keepachangelog.com/en/1.1.0) for the guiding principles, the six categories, and the date rule
license: MIT
h1_pattern: '(?i)^(?=\S+ \S)(?:.*\brelease notes\b.*|what.s new\b.*)$'
sections:
  - heading_pattern: '^\[?v?\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?\]?(?: \[YANKED\])?$'
    label: the version section
    level: 2
    evidence:
      pattern: '\A\s*[^\n]*\b\d{4}-\d{2}-\d{2}\b'
      missing: the release date in ISO 8601 form on the first line under the version heading
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
# <RELEASE_NOTES_TITLE>

Release notes tell one reader what changed in one released version and what it means for
them. They have a title naming the product, a one-sentence summary, one section per released
version with its date on the first line, and the change entries grouped under the six Keep a
Changelog categories. The front matter above is what `check_structure.py` enforces; the
guidance below is what the skill follows when it writes. The shape follows Keep a Changelog
1.1.0, whose principles and categories are quoted here under its MIT license; the differences
from a changelog are stated where they apply.

## Title

The title is the H1 and the only H1. Name the product and the kind of page: Northwind Relay
2.5.0 release notes, or What's new in Northwind Relay. The `h1_pattern` requires release notes
or What's new and at least two words. A release notes page is dated content, so the version
may appear in the title; a page that collects several releases leaves it out.

## Summary

One sentence directly under the title naming what the release adds, changes, and fixes, in
the reader's terms. The checker requires exactly one sentence here.

## Version sections

Required: one level-two section per released version, the latest first. From the source:
"There should be an entry for every single version." and "Versions and sections should be
linkable." and "The latest version comes first." The heading carries the version alone, in
the source's bracketed form, `## [2.5.0]`, with `[YANKED]` after it for a release that was
pulled: "Yanked releases are versions that had to be pulled because of a serious bug or
security issue." The source puts the date on the heading line, `## [1.1.1] - 2023-03-05`;
this template moves it to the first line under the heading so the heading stays a stable link
anchor and the checker, which reads section bodies, can require it. An `[Unreleased]` section
belongs to the changelog, not to release notes, and the checker reports it as an unknown
section.

Evidence slot, on the first version section: the release date in the form `2026-10-17` on the
first line under the heading. From the source: "The release date of each version is
displayed." and, on the date form, "These reasons, and the fact this date format is an ISO
standard, are why it is the recommended date format for changelog entries." The same line
states whether the project follows Semantic Versioning, which the source asks for: "Mention
whether you follow Semantic Versioning." A date the sources do not give is the marker on that
line, never a guess:

```text
[UNVERIFIED: the release date] Northwind Relay follows Semantic Versioning.
```

The checker reads the slot for the first version section only; the writer owns the later
ones.

## Categories

Required: at least one level-three category under each version, from the source's six and no
other, quoted once in [style-rules.md](../style-rules.md#change-categories) and shared with the
changelog entry template. Keep that order, and include a category only when it has entries. A
heading outside the six, such as Improvements or Breaking changes, is an unknown section; a
change that fits none of the six is Changed.

## Entries

One bullet per notable change, written for the reader, not from the commit log. From the
source: "Changelogs are for humans, not machines." and "The purpose of a changelog entry is to
document the noteworthy difference, often across multiple commits, to communicate them clearly
to end users." Every entry names the issue, pull request, or commit that made the change, as
plain text or as link text in parentheses at the end: `(RELAY-412)`, `([#412](url))`, or a
commit hash of seven or more characters. The checker reads prose with code spans blanked, so
an identifier in code style counts as missing. An entry whose sources give no identifier
carries the marker instead:

```text
- The Routes page no longer reports a stalled stream for a route whose delivery gap is unset. [UNVERIFIED: the issue or pull request that made this change]
```

## Breaking changes

The source has no breaking category and says instead: "If you do nothing else, list
deprecations, removals, and any breaking changes in your changelog." Here an entry that breaks
compatibility opens with **Breaking:** in bold under Changed or Removed, states what the
reader must do, and the release line under the version heading says how many breaking changes
the release carries. A deprecation names the version in which the removal lands; the checker
bans soon, and the house rules ban the other timeless-breaking words outside the dated line.

## Audience

The default audience is the engineer. For an operator, keep every entry and put the breaking
changes first within their category. For an executive, keep the summary, the release line,
and the breaking entries, within the cap. The caps count words outside code blocks.

## Source

Structure and the quoted guidance: Keep a Changelog 1.1.0, `keepachangelog.com/en/1.1.0`,
created and maintained by Olivier Lacan, MIT licensed. Quoted lines are marked with quotation
marks; the rest of this file is this skill's own text. The move of the date from the heading
to the first body line, the identifier rule, and the Breaking convention are this skill's
rules, the first stated in spec R9 (stable heading anchors), and cite no other standard.
