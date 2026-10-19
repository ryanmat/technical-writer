# Route name already in use

Rejects a route registration whose name exists in the project, and the caller reuses the existing route or picks another name.

## Problem details

| Member | Value |
|---|---|
| type | https://api.example.com/problems/route-conflict |
| status | 409 |
| title | Route name already in use |
| reason | ROUTE_CONFLICT |
| domain | relay.example.com |

## Cause

A `POST /routes` call named a route that already exists in the caller's project. Route names are unique within a project, and the call does not merge the new fields into the existing route.

## Example response

```http
HTTP/1.1 409 Conflict
Content-Type: application/problem+json

{"type": "https://api.example.com/problems/route-conflict", "title": "Route name already in use", "status": 409, "detail": "A route named orders-to-billing already exists in project p_7Q2.", "instance": "/routes/requests/req_01HZX4Q8M3"}
```
