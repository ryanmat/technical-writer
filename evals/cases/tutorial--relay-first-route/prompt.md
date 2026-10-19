---
schema_version: "1.1"
name: tutorial--relay-first-route
description: "a tutorial for engineers from UI strings and a command transcript that omit the version and permission, so the output walks one path to a routed message with a Summary and Next steps and an UNVERIFIED marker in Before you begin instead of an invented version"
tags: [user-docs, regression]
runs: 2
max_turns: 12
timeout_seconds: 600
allowed_tools: [Skill, Read]
---

Use the technical-writer skill to write a tutorial for engineers new to Northwind Relay. The lesson: create a stream, create a route from it to a consumer group, send one message, and see it arrive. Return the finished Markdown document as your final message and nothing else.

Everything you may state about the product is in the three snippets below. Do not add behavior, defaults, versions, or permissions they do not contain. No snippet names the Relay version or the permission the learner needs; do not invent either.

UI strings, from the Streams and Routes screens:

```text
Streams
New stream
Stream name
Save stream
Routes
New route
Stream
Filter key
Filter value
Consumer group
Save route
Active
```

Command transcript, from the quickstart notes:

```text
$ relay send orders --key region --value east "order 1001"
sent to orders (1 route matched)
$ relay tail billing
order 1001
```

Sample values, from the same notes:

```text
Stream name: orders
Filter key: region
Filter value: east
Consumer group: billing
```
