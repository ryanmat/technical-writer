# POST /routes

Registers a route in the project and returns it with its identifier.

## Summary

Writes the route to the route table and returns it with its server-assigned identifier. A second call with the same name is rejected with 409 rather than merged, so the call is not idempotent on its body. The token needs the `routes:write` scope.

## Request

| Field | Required | Description |
|---|---|---|
| name | yes | The route's name, unique in the project, 3 to 64 characters. |
| stream | yes | The stream the route reads from. |
| consumer_group | yes | The consumer group the route delivers to. |
| retry_limit | no | Attempts before a message is written to the stalled-stream report; the platform cap is 10. |

## Response

`201 Created` with the route object.

| Field | Type | Description |
|---|---|---|
| id | string | Server-assigned identifier of the route. |
| name | string | Echoed. |
| created_at | timestamp | Server-assigned creation time in RFC 3339 form. |

## Errors

| Status | Error | When |
|---|---|---|
| 409 | ROUTE_CONFLICT | A route with that name exists in the project. |

## Example

```http
POST /routes
{"name": "orders-to-billing", "stream": "orders", "consumer_group": "billing", "retry_limit": 5}
```

```http
201 Created
{"id": "rt_01HZX4Q8M3", "name": "orders-to-billing", "stream": "orders", "consumer_group": "billing", "retry_limit": 5, "created_at": "2026-10-17T14:02:11Z"}
```
