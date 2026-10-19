---
schema_version: "1.1"
name: task--relay-alert-rule
description: "a task topic for engineers from source snippets that omit the required permission, so the output carries an UNVERIFIED marker instead of an invented role"
tags: [user-docs, holdout]
runs: 2
max_turns: 12
timeout_seconds: 600
allowed_tools: [Skill, Read]
---

Use the technical-writer skill to write a task topic for engineers who run Northwind Relay. The task: create an alert rule that fires when a stream stops delivering messages. Return the finished Markdown document as your final message and nothing else.

Everything you may state about the product is in the three snippets below. Do not add behavior, defaults, versions, or permissions they do not contain.

UI strings, from the Alert rules screens:

```text
Alert rules
New alert rule
Condition
Stream
Evaluation interval
Delivery gap
Save rule
Normal
```

Release line, from the product's about dialog box:

```text
Northwind Relay 2.4.0
Alert rules are available from 2.4.0.
```

One setting, from the rule editor's help text:

```text
Evaluation interval: how often the rule checks the stream, in seconds. Default: 60.
```
