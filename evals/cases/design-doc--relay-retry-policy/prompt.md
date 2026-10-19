---
schema_version: "1.1"
name: design-doc--relay-retry-policy
description: "a design doc for engineers from a problem statement, a design note and a review log that give a doubling retry gap and are silent on its ceiling, so the output carries the Google skeleton with PEP 12's compatibility, security and rejected-ideas sections, names a rejected alternative, and marks the gap ceiling UNVERIFIED instead of inventing it"
tags: [engineering, regression]
runs: 2
max_turns: 12
timeout_seconds: 600
allowed_tools: [Skill, Read]
---

Use the technical-writer skill to write the design doc for a retry policy on Northwind Relay route delivery, for the engineers who will review and build it. Return the finished Markdown document as your final message and nothing else.

Everything you may state is in the three snippets below. Do not add behavior, defaults, figures, or components they do not contain. The design note gives a doubling rule for the gap between attempts and is silent on any ceiling for it; do not invent one.

The problem statement, from the 2.5 plan:

```text
A delivery that times out is written to the stalled-stream report and not attempted again, so a consumer unreachable for a few seconds loses the message until an operator replays it. Durability is the first-ranked quality goal. Scope: delivery from the router to a consumer group. Out of scope: how producers write, how routes are evaluated, message ordering across retries (the at-least-once model leaves it to the consumer), a dead-letter stream (owned by the 2.6 plan), retry on consumer errors other than timeout.
```

The design note, from the router owner:

```text
Per route: a retry limit and a base gap, set through the route registration call, defaulting from the route table schema. On timeout, schedule the message again after the base gap and double the gap on each further timeout. When the attempt count reaches the limit, write the message to the stalled-stream report with the count. Retry state is in the router's in-memory route table, rebuilt from Northwind Queue on restart, so a restart repeats at most one attempt. The Routes page shows the two fields and the attempt count. Each retry logs one line (route, attempt, gap); two counters per route (retries, exhausted) on the Relay dashboard.
Compatibility: a route registered before the change has no retry fields and keeps one attempt. The stalled-stream export gains a column.
Security: a high limit on a route to an unreachable consumer holds messages in router memory longer; the registration call caps the limit at the platform team's value. No new network path or credential.
```

The review log, from the design review:

```text
Rejected: a fixed gap (the 2026-09 soak test showed consumer restarts clustering at 10 to 40 seconds, which a doubling gap covers with fewer attempts); a global retry policy (batch and interactive consumers want different limits); retrying inside the queue adapter (it has no view of the route or the limit).
Set aside in review: retrying on every consumer error (a content rejection repeats on every attempt; the report is the right place); a stream-level limit (same reason as the global policy).
Open: whether the attempt count resets when an operator replays the message.
```
