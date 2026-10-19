---
schema_version: "1.1"
name: case
description: "synthetic case that proves the eval-case harness; the eval runner never sees it"
tags: [engineering, regression]
runs: 1
max_turns: 4
timeout_seconds: 120
allowed_tools: [Skill]
---

Use the technical-writer skill to write a harness document for engineers about the
synthetic service at example.com. The document has a Context section and an Outcome
section and nothing else.
