---
schema_version: "1.1"
name: review--adr-superseded-without-link
description: "a review of a pasted architecture decision record seeded with a Status that reads superseded and names no record, a Decision Outcome in the passive voice, and a missing Considered Options section, where the reply is a findings list that must name all three and never a rewrite"
tags: [review, regression]
runs: 2
max_turns: 12
timeout_seconds: 600
allowed_tools: [Skill, Read]
---

Use the technical-writer skill to review the architecture decision record below for the engineers on the Northwind Relay team. Return your findings as your final message and nothing else: one finding per line, ranked by severity, each naming the location, the rule broken, and the reference file that carries the rule. Do not rewrite the record and do not return a corrected copy.

The record under review:

```markdown
# 0004-store-relay-sessions-in-redis

Northwind Relay keeps consumer session state in Redis rather than in the broker.

## Status

Superseded, 2026-10-10. Decision-makers: the Relay team.

## Context and Problem Statement

Northwind Relay tracks which consumer holds each stream and where it last acknowledged. The 2.2 release kept this state in the broker's metadata store, which blocked broker upgrades while any consumer was connected. We need session state that survives a broker upgrade.

## Decision Drivers

- Broker upgrades with no consumer disconnects, the 2.3 release goal.
- Session lookup under 5 milliseconds at the 99th percentile.

## Decision Outcome

Chosen option: "Redis", because the latency budget was met in the 2026-05 benchmark and broker upgrades no longer wait for consumers. It was decided that session state would be stored in Redis and that the broker's metadata store would be left for topic configuration only.

## Consequences

- Good, because broker upgrades no longer wait for consumers to disconnect.
- Bad, because a second stateful service is added to the Relay deployment.
```
