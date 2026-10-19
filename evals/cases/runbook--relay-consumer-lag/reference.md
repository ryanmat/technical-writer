# Runbook: Northwind Relay consumer lag

Restore delivery when the `relay-consumer-lag` alert pages, by finding the stalled consumer group and restarting or draining its route.

## Alert or trigger

The alert `relay-consumer-lag` pages the Relay rotation when a consumer group's oldest undelivered message is older than 300 seconds for more than 5 minutes. The alert names the stream and the consumer group in its labels.

## Impact

Consumers in the named group receive messages late, and producers on the stream see the backlog grow. No message is lost: Northwind Queue holds every message until the group reads it or it expires. Other groups on the stream are not affected.

## Prerequisites

- The `relay` CLI version 2.5 or later on your workstation, logged in to the production cluster.
- The `relay-operator` role, which the `relay route` commands require.

## Diagnosis

To find why the group is lagging:

1. Run `relay route status <STREAM> <GROUP>` to show the route's state and lag.

   ```bash
   relay route status orders billing
   ```

   The output reads `orders -> billing  state=delivering  lag=412s  consumers=0`; `consumers=0` means no live consumer, and `state=timed-out` means the consumers reject every delivery.

2. Run `relay group consumers <GROUP>` to count the group's live consumers.

   ```bash
   relay group consumers billing
   ```

   The output is empty when no consumer is connected.

## Mitigation

To restore delivery:

1. If the route state is `timed-out`, run `relay route restart <STREAM> <GROUP>` to restart the route.

   ```bash
   relay route restart orders billing
   ```

   The output reads `route orders -> billing restarted`.

2. If the group has no live consumer, ask the owning team to start one. The route resumes on its own when a consumer connects.

3. If the backlog is older than the consumers can process, run `relay route drain <STREAM> <GROUP> --before <TIMESTAMP>` to move it to the dead-letter stream.

   ```bash
   relay route drain orders billing --before 2026-10-03T14:00:00Z
   ```

   The output prints the count of messages moved, as `drained 1204 messages to orders.dead-letter`.

## Verification

Run `relay route status <STREAM> <GROUP>` again. The lag falls below 300 seconds within two minutes of the fix, and the alert resolves on the next evaluation.

```bash
relay route status orders billing
```

The output reads `orders -> billing  state=delivering  lag=12s  consumers=2`.

## Rollback

A drained message is in the dead-letter stream, not deleted. Run `relay route replay <STREAM> <GROUP> --from-dead-letter` to deliver the drained messages once the consumers are healthy.

## Escalation

Page the platform rotation in `#platform-oncall` when the route state is `delivering`, consumers are connected, and the lag still grows: the cause is then in Northwind Queue, not in Relay. [UNVERIFIED: how long to wait before escalating; the runbook note gives no time]
