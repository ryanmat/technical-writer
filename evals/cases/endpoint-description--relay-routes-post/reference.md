# POST /routes

Registers a route in the caller's project and returns the stored route with its identifier.

## Summary

Writes a named subscription that delivers a stream to a consumer group into the route table and returns it with its server-assigned `id`. The call is not idempotent on its body: a second call with a name that exists in the project is rejected with `409` and nothing is merged. The token must carry the `routes:write` scope.

## Request

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| name | string | yes | none | The route's name, unique within the project, 3 to 64 characters. |
| stream | string | yes | none | The stream the route reads from. |
| consumer_group | string | yes | none | The consumer group the route delivers to. |
| retry_limit | integer | no | 3 | Attempts before a message is written to the stalled-stream report; the platform cap is 10. |
| base_gap_ms | integer | no | [UNVERIFIED: the schema default of base_gap_ms, which the export names and does not give] | The gap before the first retry, in milliseconds, doubled on each further timeout. |

## Response

`201 Created` with the stored route.

| Field | Type | Description |
|---|---|---|
| id | string | Server-assigned identifier of the route. |
| name | string | Echoed. |
| stream | string | Echoed. |
| consumer_group | string | Echoed. |
| retry_limit | integer | Echoed, or the default when omitted. |
| base_gap_ms | integer | Echoed, or the default when omitted. |
| created_at | timestamp | Server-assigned creation time in RFC 3339 form. |

## Errors

| Status | Error | When |
|---|---|---|
| 400 | INVALID_ARGUMENT | A required field is missing, or `name` is outside 3 to 64 characters. |
| 403 | PERMISSION_DENIED | The token lacks the `routes:write` scope. |
| 409 | ROUTE_CONFLICT | A route with that name exists in the project. |
| 422 | RETRY_LIMIT_ABOVE_CAP | `retry_limit` is above the platform cap of 10. |

## Example

Request:

```http
POST /routes
{"name": "orders-to-billing", "stream": "orders", "consumer_group": "billing", "retry_limit": 5, "base_gap_ms": 500}
```

Response:

```http
201 Created
{"id": "rt_01HZX4Q8M3", "name": "orders-to-billing", "stream": "orders", "consumer_group": "billing", "retry_limit": 5, "base_gap_ms": 500, "created_at": "2026-10-17T14:02:11Z"}
```
