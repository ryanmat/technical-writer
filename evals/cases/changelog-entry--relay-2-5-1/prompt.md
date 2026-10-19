---
schema_version: "1.1"
name: changelog-entry--relay-2-5-1
description: "a changelog entry for engineers from a patch release summary, an issue export and a date note, where one listed change has no issue key, so the output carries the dated version heading in Keep a Changelog form, only the standard categories, an identifier on each entry, and an UNVERIFIED marker instead of an invented key"
tags: [engineering, regression]
runs: 2
max_turns: 12
timeout_seconds: 600
allowed_tools: [Skill, Read]
---

Use the technical-writer skill to write the changelog entry for Northwind Relay 2.5.1, the block the release adds to the project's CHANGELOG.md, for the engineers who read that file. Return the finished Markdown document as your final message and nothing else.

Everything you may state about the release is in the three snippets below. Do not add changes, categories, or identifiers they do not contain. The third change in the issue export has no issue key; do not invent one.

The release summary, from the release manager:

```text
2.5.1 is a patch release: two fixes to the retry policy shipped in 2.5.0 and one hardening of the route registration call. No breaking changes.
```

The issue export, from the tracker:

```text
RELAY-440  Fixed     Routes with a retry limit of zero no longer retry once before reaching the stalled-stream report.
RELAY-438  Fixed     The Routes page shows the attempt count on a stalled-stream row after a replay.
(no key)   Security  The route registration call rejects a retry limit above the platform cap instead of clamping it silently.
```

The date note, from the release manager:

```text
Release date: 2026-10-17
```
