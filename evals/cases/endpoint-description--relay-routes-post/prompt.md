---
schema_version: "1.1"
name: endpoint-description--relay-routes-post
description: "an endpoint description for engineers from an API owner's note, a schema export, an error table and a captured exchange, where one optional field's default is stated to exist but not given, so the output carries the method-and-path title, a verb-first summary line, the field table with Type and Default columns, the success and error status codes, the captured example, and an UNVERIFIED marker in the Default cell instead of an invented value"
tags: [api, regression]
runs: 2
max_turns: 12
timeout_seconds: 600
allowed_tools: [Skill, Read]
---

Use the technical-writer skill to write the reference entry for the Northwind Relay route registration call, POST /routes, for the engineers integrating against the API. Return the finished Markdown document as your final message and nothing else.

Everything you may state about the call is in the four snippets below. Do not add fields, defaults, status codes, error identifiers, or example values they do not contain. The schema export says base_gap_ms has a default and does not give its value; do not invent one.

The call note, from the API owner:

```text
POST /routes registers a route: a named subscription that delivers a stream to a consumer group in the caller's project. The call writes the route to the route table and returns the stored route with its server-assigned id. It is not idempotent on its body: a second call with a name that already exists in the project is rejected with 409 and nothing is merged. The token must carry the routes:write scope.
```

The schema export, from the route table schema:

```text
field           type     required  default                                           description
name            string   yes       -                                                 The route's name, unique within the project, 3 to 64 characters.
stream          string   yes       -                                                 The stream the route reads from.
consumer_group  string   yes       -                                                 The consumer group the route delivers to.
retry_limit     integer  no        3                                                 Attempts before a message is written to the stalled-stream report. The platform cap is 10.
base_gap_ms     integer  no        (schema default; value not included in this export)   The gap before the first retry, in milliseconds, doubled on each further timeout.
response        201 Created with the stored route: id (string, server-assigned), the five fields above, created_at (timestamp, RFC 3339, server-assigned).
```

The error table, from the API owner:

```text
400  INVALID_ARGUMENT        a required field is missing, or name is outside 3 to 64 characters
403  PERMISSION_DENIED       the token lacks the routes:write scope
409  ROUTE_CONFLICT          a route with that name already exists in the project
422  RETRY_LIMIT_ABOVE_CAP   retry_limit is above the platform cap of 10
```

The captured exchange, from the integration test log:

```text
> POST /routes
> {"name": "orders-to-billing", "stream": "orders", "consumer_group": "billing", "retry_limit": 5, "base_gap_ms": 500}

< 201 Created
< {"id": "rt_01HZX4Q8M3", "name": "orders-to-billing", "stream": "orders", "consumer_group": "billing", "retry_limit": 5, "base_gap_ms": 500, "created_at": "2026-10-17T14:02:11Z"}
```
