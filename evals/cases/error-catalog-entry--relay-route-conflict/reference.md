# Route name already in use

Rejects a route registration or rename whose name exists in the project, and the caller reuses the existing route or picks a free name.

## Problem details

| Member | Value |
|---|---|
| type | https://api.example.com/problems/route-conflict |
| status | 409 |
| title | Route name already in use |
| reason | ROUTE_CONFLICT |
| domain | relay.example.com |

## Cause

A `POST /routes` call named a route that already exists in the caller's project, or a `PATCH /routes/{id}` call renamed a route to a name another route holds. Route names are unique within a project. Nothing is merged: the existing route is untouched and the new fields are dropped. The rename call has returned the error since [UNVERIFIED: the version that added renaming].

## Resolution

Find the existing route with `GET /routes?name=<NAME>` and reuse it, or register the route under a name the project does not hold. A retry of the identical request returns the same error until one of those is done.

## Example response

```http
HTTP/1.1 409 Conflict
Content-Type: application/problem+json

{"type": "https://api.example.com/problems/route-conflict", "title": "Route name already in use", "status": 409, "detail": "A route named orders-to-billing already exists in project p_7Q2.", "instance": "/routes/requests/req_01HZX4Q8M3"}
```
