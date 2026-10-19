---
schema_version: "1.1"
name: release-notes--relay-2-5-0
description: "release notes for engineers from a release summary, an issue export, and a date note, where one listed change has no issue key, so the output carries the version section with its ISO date on the first line, the Keep a Changelog categories, an identifier on each entry, and an UNVERIFIED marker instead of an invented key"
tags: [user-docs, regression]
runs: 2
max_turns: 12
timeout_seconds: 600
allowed_tools: [Skill, Read]
---

Use the technical-writer skill to write the release notes for Northwind Relay 2.5.0 for engineers who run it. Return the finished Markdown document as your final message and nothing else.

Everything you may state about the release is in the three snippets below. Do not add changes, behavior, defaults, or identifiers they do not contain. The third change in the issue export has no issue key; do not invent one.

The release summary, from the product manager:

```text
2.5.0 ships retry on route timeout, lowers the default evaluation interval from 60 to 30 seconds, and fixes the stalled-stream report. The interval change is breaking for routes that relied on the 60 second default. Relay version numbers follow Semantic Versioning.
```

The issue export, from the tracker:

```text
RELAY-412  Added    Routes retry delivery after a timeout, up to the retry limit set on the route.
RELAY-398  Changed  Default evaluation interval is 30 seconds (was 60).
(no key)   Fixed    Routes page no longer reports a stalled stream for a route whose delivery gap is unset.
```

The date note, from the release manager:

```text
Release date: 2026-10-17
```
