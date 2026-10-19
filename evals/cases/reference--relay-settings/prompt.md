---
schema_version: "1.1"
name: reference--relay-settings
description: "a reference topic for engineers from a settings list where one default is missing, so the output tables the settings under a version statement and marks the missing default UNVERIFIED instead of inventing it"
tags: [user-docs, regression]
runs: 2
max_turns: 12
timeout_seconds: 600
allowed_tools: [Skill, Read]
---

Use the technical-writer skill to write a reference topic for engineers who run Northwind Relay. The reference: every setting an alert rule accepts, with its default and what it does. Return the finished Markdown document as your final message and nothing else.

Everything you may state about the product is in the two snippets below. Do not add settings, defaults, ranges, or versions they do not contain. One setting's default is not given; do not invent it.

Release line, from the product's about dialog box:

```text
Northwind Relay 2.4.0
Alert rules are available from 2.4.0.
```

Settings, from the rule editor's help text:

```text
Stream: the stream the rule watches. Required; no default.
Evaluation interval: how often the rule checks the stream, in seconds. Default: 60.
Delivery gap: the gap, in seconds, at which the rule fires. Default: not shown.
Severity: the label the alert carries when the rule fires. One of info, warning, critical. Default: warning.
Notification channel: where the alert is sent. Default: the workspace channel.
```
