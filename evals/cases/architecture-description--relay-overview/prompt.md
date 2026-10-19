---
schema_version: "1.1"
name: architecture-description--relay-overview
description: "an architecture description for engineers from a system summary, a component list, a quality note and a deployment note that give no throughput figure, so the output keeps arc42's section names, carries a C4 diagram statement in every view section, and marks the sizing figure UNVERIFIED instead of inventing it"
tags: [engineering, regression]
runs: 2
max_turns: 12
timeout_seconds: 600
allowed_tools: [Skill, Read]
---

Use the technical-writer skill to write the architecture description of Northwind Relay for the engineers who build and run it. Return the finished Markdown document as your final message and nothing else.

Everything you may state about the system is in the four snippets below. Do not add components, behavior, figures, or technologies they do not contain. No snippet gives the message throughput the deployment is sized for; do not invent one.

The system summary, from the Relay README:

```text
Northwind Relay is a message routing service. Producers write messages to named streams. Consumers register routes, each binding a stream to a consumer group through a filter, and read their group's messages. Relay evaluates routes at delivery time, so a new route applies to messages the stream already holds. Every in-flight message is written to Northwind Queue before the producer is acknowledged. Before routing, every consumer read the whole stream and dropped what it did not need.
```

The component list, from the Relay repository:

```text
api        Go          accepts writes and route registrations
router     Go          evaluates every message against every route on its stream, in route order; one copy per matching consumer group
queue-adapter  Go      writes to and reads from Northwind Queue
routes-page    TypeScript  shows route state and the stalled-stream report; served by api
Constraints: runs on the Northwind platform container cluster; Northwind Queue is the only durable store; Go is the platform service language.
```

The quality note, from the 2.5 plan:

```text
Quality goals, ranked: durability (no message lost across a consumer outage of up to one hour; the 2026-09 soak test held one hour of backlog with no loss), latency (enqueue p99 under 20 ms; the 2026-09 benchmark measured 12 ms), operability (one team, one on-call rotation).
Known risks: at-least-once delivery means a consumer can see a duplicate after a router restart; the Relay team owns Northwind Queue capacity planning; route evaluation is linear in routes per stream and has not been measured past 200 routes.
```

The deployment note, from the platform runbook:

```text
Production runs three instances of each Relay container across the platform cluster in one region. Northwind Queue runs as its own cluster in the same region. The Routes page is served from the api container.
```
