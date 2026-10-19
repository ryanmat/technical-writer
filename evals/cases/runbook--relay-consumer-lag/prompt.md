---
schema_version: "1.1"
name: runbook--relay-consumer-lag
description: "a runbook for operators from an alert definition, an impact note, a command transcript and an escalation line that gives the target but not when to escalate, so the output keeps the runbook sections, a stem sentence and short steps in Mitigation, the expected output after every command, and an UNVERIFIED marker for the escalation wait instead of an invented time"
tags: [engineering, regression]
runs: 2
max_turns: 12
timeout_seconds: 600
allowed_tools: [Skill, Read]
---

Use the technical-writer skill to write the runbook for the Northwind Relay consumer lag alert, for the operators on the Relay rotation. Return the finished Markdown document as your final message and nothing else.

Everything you may state is in the four snippets below. Do not add commands, flags, outputs, thresholds, or roles they do not contain. The escalation line names whom to page and the state that means the cause is elsewhere, but not how long to wait first; do not invent a time.

The alert definition, from the alerting rules file:

```text
alert: relay-consumer-lag
expr: oldest undelivered message age > 300s for a consumer group
for: 5m
labels: stream, group
pages: relay rotation
```

The impact note, from the Relay service page:

```text
Consumers in the lagging group get messages late; producers on the stream see the backlog grow. Nothing is lost: Northwind Queue keeps every message until the group reads it or it expires. Other groups on the stream are unaffected.
Needs: relay CLI 2.5+ logged in to the production cluster; the relay-operator role for relay route commands.
```

The command transcript, from the last incident:

```text
$ relay route status orders billing
orders -> billing  state=delivering  lag=412s  consumers=0        # consumers=0: no live consumer; state=timed-out: consumers reject every delivery
$ relay group consumers billing
(no output: no consumer connected)
$ relay route restart orders billing                               # when state=timed-out
route orders -> billing restarted
# when consumers=0: the owning team starts a consumer; the route resumes by itself
$ relay route drain orders billing --before 2026-10-03T14:00:00Z   # when the backlog is older than the consumers can process
drained 1204 messages to orders.dead-letter
$ relay route status orders billing                                # verify: lag under 300s within 2 min, alert resolves next evaluation
orders -> billing  state=delivering  lag=12s  consumers=2
$ relay route replay orders billing --from-dead-letter             # rollback of a drain, once consumers are healthy
```

The escalation line, from the rotation handbook:

```text
If state=delivering, consumers are connected, and lag still grows, the cause is in Northwind Queue: page the platform rotation in #platform-oncall.
```
