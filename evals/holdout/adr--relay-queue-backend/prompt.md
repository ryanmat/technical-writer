---
schema_version: "1.1"
name: adr--relay-queue-backend
description: "an architecture decision record for engineers from two sourced options and a decision date, with one driver left unsourced so the output marks it UNVERIFIED instead of inventing a number"
tags: [engineering, holdout]
runs: 2
max_turns: 12
timeout_seconds: 600
allowed_tools: [Skill, Read]
---

Use the technical-writer skill to write an architecture decision record for the engineers on Northwind Relay. The decision: which backend stores in-flight messages from release 2.5. The team chose Northwind Queue over a managed cloud queue service and accepted the decision on 2026-10-03. Number the record 0007. Return the finished Markdown document as your final message and nothing else.

Everything you may state is in the snippets below. Cost matters to the team, but no snippet gives a price; do not invent one.

Problem, from the 2.5 planning note:

```text
Relay buffers messages between producers and consumers.
Release 2.3 kept messages in process memory and lost them on restart.
Requirement for 2.5: survive a consumer outage of up to one hour with no loss.
Latency budget: enqueue p99 under 20 ms.
Expected volume: 40 million messages a day.
```

Option one, from the 2026-09 benchmark and soak test of Northwind Queue:

```text
Northwind Queue: in-house broker, operated by the Relay team under its on-call rotation.
Delivery: at-least-once (duplicates possible).
Enqueue latency p99: 12 ms.
Soak test: one hour of backlog held, zero messages lost.
```

Option two, from the same planning note:

```text
Managed cloud queue service: provider handles capacity planning.
Adds a network path outside the Relay deployment and a vendor dependency.
No latency measurement taken.
```
