---
schema_version: "1.1"
name: concept--relay-routing-model
description: "a concept topic for engineers from source snippets that omit the retention period, so the output explains what routes are and why without inventing the number or turning into a procedure"
tags: [user-docs, regression]
runs: 2
max_turns: 12
timeout_seconds: 600
allowed_tools: [Skill, Read]
---

Use the technical-writer skill to write a concept topic for engineers who run Northwind Relay. The concept: the routing model, which decides which consumers receive a message. Return the finished Markdown document as your final message and nothing else.

Everything you may state about the product is in the three snippets below. Do not add behavior, defaults, limits, or versions they do not contain. The snippets never say how long a stream keeps an unmatched message; do not invent a retention period.

Terms, from the product glossary:

```text
Stream: a named, ordered sequence of messages written by producers.
Route: a rule that binds a stream to a consumer group through a filter.
Filter: a key and value pair a message must carry for the route to match.
Consumer group: a set of consumers that share one route's messages between them.
```

Behavior, from the routing design note:

```text
Every message is evaluated against every route on its stream, in route order.
A message can match more than one route; each matching consumer group receives its own copy.
A message that matches no route stays in the stream until it expires.
Routes are evaluated at delivery time, so a new route applies to messages the stream already holds.
```

Why routing exists, from the 2.0 release announcement:

```text
Before routing, every consumer read the whole stream and dropped what it did not need.
Routing moves the filter into Relay, so a consumer receives only the messages its group asked for.
```
