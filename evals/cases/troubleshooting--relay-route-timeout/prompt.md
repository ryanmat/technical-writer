---
schema_version: "1.1"
name: troubleshooting--relay-route-timeout
description: "a troubleshooting topic for engineers from an error message, a cause note, and a command transcript that omit the timeout's value, so the output carries Symptom, Cause, and Resolution with the command's output and an UNVERIFIED marker instead of an invented default"
tags: [user-docs, regression]
runs: 2
max_turns: 12
timeout_seconds: 600
allowed_tools: [Skill, Read]
---

Use the technical-writer skill to write a troubleshooting topic for engineers who run Northwind Relay. The topic covers one problem: a route that reports timed out. Return the finished Markdown document as your final message and nothing else.

Everything you may state about the product is in the three snippets below. Do not add behavior, defaults, commands, or versions they do not contain. No snippet gives the route timeout's value; do not invent one.

What the engineer sees, from the Routes page and the command line:

```text
Routes page, State column: Timed out
$ relay route status billing
route billing: timed out
```

Why it happens, from the routing design note:

```text
A route times out when its consumer group acknowledges no message within the route timeout.
A timed out route stops delivering until it is restarted.
```

How to fix it, from the operations runbook:

```text
$ relay route restart billing
route billing: Active
$ relay route status billing
route billing: Active
```
