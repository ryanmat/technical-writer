# Northwind Relay queue stall on 2026-10-03

On 2026-10-03 Northwind Relay stopped delivering messages on every stream for 42 minutes because the queue adapter's connection pool filled with connections Northwind Queue had closed.

## Summary

Between 14:02 and 14:44 UTC on 2026-10-03 the Relay router delivered no messages. Northwind Queue restarted one broker for a planned upgrade; the queue adapter kept the connections that broker had closed and retried on them until its pool was exhausted. The on-call engineer restarted the router instances, which rebuilt the pool. No message was lost: producers kept writing to Northwind Queue and the router drained the backlog by 15:10 UTC.

## Impact

Delivery stopped for 42 minutes on every stream. Every consumer group received nothing in that window and then a 42 minute backlog; the Routes page reported every stream as stalled. [UNVERIFIED: the number of consumer groups and end users affected; the incident channel records none] No message was lost and no producer write failed.

## Root causes and trigger

The queue adapter did not remove a connection from its pool when Northwind Queue closed it; a closed connection stayed eligible for reuse and failed every attempt. The pool had no health check and no cap on consecutive failures per connection, so the broker restart turned one third of the pool into permanent failures and the retries on them held the remaining connections busy.

The trigger was the planned restart of queue broker 2 at 13:58 UTC, which closed every connection the adapter held to it.

## Timeline and recovery

- 2026-10-03T13:58Z: the platform team begins the planned restart of queue broker 2.
- 2026-10-03T14:02Z: the router's delivery rate falls to zero; the stalled-stream count on the Routes page starts climbing.
- 2026-10-03T14:09Z: the stalled-streams alert pages the Relay rotation.
- 2026-10-03T14:21Z: the on-call engineer confirms broker 2 is healthy and the router's pool is full of connections in the closed state.
- 2026-10-03T14:40Z: the three router instances are restarted in turn.
- 2026-10-03T14:44Z: delivery resumes on every stream.
- 2026-10-03T15:10Z: the backlog is drained and the stalled-stream count returns to zero.

Recovery was the 14:40 restart of the three router instances in turn, which rebuilt their connection pools against the healthy brokers; nothing else was changed during the incident.

## Detection

The stalled-streams alert fired seven minutes after delivery stopped. The delivery-rate dashboard showed the drop at 14:02 UTC but no alert reads it. The platform team's restart notice named the broker and the window but Relay's rotation was not on its distribution.

## Action items

- Remove a connection from the queue adapter's pool when the broker closes it, and add a per-connection health check (owner: queue adapter maintainer, priority: P0, RELAY-431).
- Alert on the delivery rate falling below the stream write rate for more than two minutes, so detection does not wait for the stalled-stream count (owner: Relay on-call lead, priority: P1, RELAY-432).
- Add the Relay rotation to the platform team's planned-maintenance distribution (owner: platform team liaison, priority: P2, PLAT-118).
- Rehearse a broker restart against a staging Relay before the next planned upgrade (owner: Relay on-call lead, priority: P2, RELAY-433).

## Lessons learned

What went well: no message was lost, because producers write to Northwind Queue before acknowledgment and the backlog drained in 26 minutes. What went poorly: detection took seven minutes and diagnosis another twelve, because the only alert reads the stalled-stream count, a lagging signal, and the pool state was visible only from a router debug endpoint. Where we got lucky: the restart was a single broker; a rolling restart of all three would have emptied the pool rather than filling it with closed connections, which would have looked like a different failure.
