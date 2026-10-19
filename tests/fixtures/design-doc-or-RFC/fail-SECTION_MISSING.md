# Retry policy for Northwind Relay route delivery

This design adds a per-route retry on delivery timeout so that a consumer's transient outage no longer drops the message to the stalled-stream report.

## Context and Scope

Northwind Relay delivers each message to the consumer groups whose routes match it. Today a delivery that times out is written to the stalled-stream report and not attempted again, so a consumer that is unreachable for a few seconds loses the message until an operator replays it. The 2.5 plan ranks durability first among Relay's quality goals. This design covers delivery from the router to a consumer group; it does not change how producers write to streams or how routes are evaluated.

## Goals and Non-goals

Goals: a delivery that times out is retried without operator action; the retry count and the gap between attempts are set per route; a message that exhausts its retries reaches the stalled-stream report with the attempt count. Non-goals: ordering across retried and later messages, which the at-least-once model already leaves to the consumer; a dead-letter stream, which the 2.6 plan owns; retry on consumer errors other than timeout.

## Design

The router keeps, per route, a retry limit and a base gap. On a delivery timeout the router schedules the message again after the base gap, doubling the gap on each further timeout up to a ceiling. [UNVERIFIED: the ceiling on the retry gap; the design note names a doubling rule and no upper bound] When the attempt count reaches the route's retry limit the message is written to the stalled-stream report with the count, as today's single failure is. Retry state lives in the router's in-memory route table and is rebuilt from Northwind Queue on restart, so a restart repeats at most one attempt.

The Routes page shows the two new fields on each route and the attempt count on each stalled-stream row.

## Alternatives Considered

A fixed gap between attempts was rejected because the 2026-09 soak test showed consumer restarts clustering at 10 to 40 seconds, which a doubling gap covers with fewer attempts. A global retry policy was rejected because routes to batch consumers and routes to interactive consumers want different limits. Retrying inside the queue adapter was rejected because the adapter has no view of the route and so of the limit.

## Cross-cutting Concerns

Logging: every retry writes one line with the route, the attempt number and the gap. Metrics: a counter of retries per route and a counter of exhausted messages per route, both on the existing Relay dashboard. Configuration: the two fields default to the values in the route table schema and are set through the route registration call.

## Backwards Compatibility

A route registered before this change has no retry fields and keeps today's behavior, one attempt. The stalled-stream report gains a column; a consumer of its export that reads columns by position breaks and one that reads by name does not.

## Security Implications

A retry limit set high on a route to an unreachable consumer holds messages in the router's memory longer. The limit is capped by the route registration call at the value the platform team sets. No new network path and no new credential.

## Open Issues

Whether the attempt count in the stalled-stream report should reset when an operator replays the message.
