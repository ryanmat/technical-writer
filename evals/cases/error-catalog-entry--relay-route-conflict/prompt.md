---
schema_version: "1.1"
name: error-catalog-entry--relay-route-conflict
description: "an error catalog entry for engineers from a problem type registration, an API owner's note and a captured occurrence whose log line names a server exception class, where the note says a second call also returns the error since a version it does not name, so the output carries the title as the H1, the type URI, status and title in the Problem details table, a cause and resolution with no internal name, the captured problem+json body, and an UNVERIFIED marker for the version instead of an invented one"
tags: [api, regression]
runs: 2
max_turns: 12
timeout_seconds: 600
allowed_tools: [Skill, Read]
---

Use the technical-writer skill to write the error catalog entry for the Northwind Relay route conflict error, for the engineers integrating against the API. Return the finished Markdown document as your final message and nothing else.

Everything you may state about the error is in the three snippets below. Do not add members, status codes, calls, or example values they do not contain. The owner's note says the rename call has returned the error since a version it does not name; do not invent the version.

The problem type registration, from the API's problem registry:

```text
type:    https://api.example.com/problems/route-conflict
status:  409
title:   Route name already in use
reason:  ROUTE_CONFLICT
domain:  relay.example.com
```

The owner's note:

```text
ROUTE_CONFLICT comes back from POST /routes when the name already exists in the caller's project. Names are unique per project. Nothing is merged: the existing route is untouched and the new fields are dropped. PATCH /routes/{id} returns the same error when a rename targets a taken name; it has done so since the version that added renaming, which I would have to look up. Resolution: GET /routes?name=<NAME> finds the existing route; the caller reuses it or registers under a free name. Retrying the identical request returns the same error until one of those happens.
```

The captured occurrence, from the integration test log:

```text
< HTTP/1.1 409 Conflict
< Content-Type: application/problem+json
<
< {"type": "https://api.example.com/problems/route-conflict", "title": "Route name already in use", "status": 409, "detail": "A route named orders-to-billing already exists in project p_7Q2.", "instance": "/routes/requests/req_01HZX4Q8M3"}

router[2211]: RouteTableConflictException at routes.register (routes.go:212): name orders-to-billing held by rt_01HZX4Q8M3
```
