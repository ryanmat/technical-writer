---
schema_version: "1.1"
name: postmortem--relay-queue-stall
description: "a postmortem for engineers from an incident channel export, a cause note and an action list that give the duration but not how many consumers or users were affected, so the output keeps the SRE Workbook section set, ISO timestamps on the timeline, an owner and priority on every action item, blameless wording, and an UNVERIFIED marker for the user count instead of an invented figure"
tags: [engineering, regression]
runs: 2
max_turns: 12
timeout_seconds: 600
allowed_tools: [Skill, Read]
---

Use the technical-writer skill to write the postmortem for the Northwind Relay queue stall of 2026-10-03, for the engineers who run Relay. Return the finished Markdown document as your final message and nothing else.

Everything you may state is in the three snippets below. Do not add events, figures, causes, or names they do not contain. The export gives the duration and the backlog time but never how many consumer groups or users were affected; do not invent a count. Name no person: the export's handles stand for roles.

The incident channel export (UTC):

```text
2026-10-03 13:58  platform-team: starting planned restart of queue broker 2, window 10 min
2026-10-03 14:02  relay-dashboard: delivery rate 0 msg/s on all streams; stalled-stream count climbing
2026-10-03 14:09  relay-alerts: PAGE stalled-streams > 50 -> relay-oncall
2026-10-03 14:21  relay-oncall: broker 2 healthy; router pool full of connections in CLOSED state, retrying on them
2026-10-03 14:40  relay-oncall: restarting router instances 1, 2, 3 in turn
2026-10-03 14:44  relay-dashboard: delivery resumed on all streams
2026-10-03 15:10  relay-dashboard: backlog drained, stalled-stream count 0
Notes: no producer write failed; no message lost (producers write to Northwind Queue before ack). The delivery-rate dashboard showed the drop at 14:02 but no alert reads it. Relay's rotation was not on the platform team's maintenance notice distribution.
```

The cause note, from the queue adapter maintainer:

```text
The adapter does not remove a connection from its pool when the broker closes it; a CLOSED connection stays eligible and fails every attempt. No health check, no cap on consecutive failures per connection. The broker restart closed one third of the pool; retries on those held the rest busy. Trigger: the planned restart of broker 2 at 13:58.
```

The action list, from the review:

```text
P0  remove closed connections from the pool and add a per-connection health check  (queue adapter maintainer)  RELAY-431
P1  alert when delivery rate < stream write rate for > 2 min                        (Relay on-call lead)        RELAY-432
P2  add the Relay rotation to the platform maintenance distribution                 (platform team liaison)     PLAT-118
P2  rehearse a broker restart against staging Relay before the next upgrade          (Relay on-call lead)        RELAY-433
Went well: nothing lost; backlog drained in 26 min. Went poorly: detection 7 min, diagnosis 12 min more; pool state visible only from a debug endpoint. Lucky: a single broker restarted; a rolling restart of all three would have emptied the pool instead.
```
