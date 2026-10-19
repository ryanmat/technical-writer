# 0007-use-northwind-queue-as-the-relay-message-backend

Northwind Relay stores in-flight messages in Northwind Queue rather than in a managed cloud queue.

## Status

Accepted, 2026-10-03. Decision-makers: the Relay team.

## Context and Problem Statement

Northwind Relay buffers messages between producers and consumers and has to survive a consumer outage of up to one hour without loss. The 2.3 release kept messages in process memory, which lost them on restart. We need a durable backend for the 2.5 release.

## Decision Drivers

- Durability across a one-hour consumer outage, measured in the 2026-09 soak test.
- Enqueue latency at the 99th percentile under 20 milliseconds, the budget the 2.5 plan sets.
- Operating cost at the expected volume of 40 million messages a day. [UNVERIFIED: the cost per million messages for either option; the sources give no prices]
- Operational ownership inside the Relay team.

## Decision Outcome

Chosen option: "Northwind Queue", because it met the latency budget in the 2026-09 benchmark (12 milliseconds at the 99th percentile), it held one hour of backlog with no loss in the soak test, and it already runs under the Relay team's on-call rotation. We will store every in-flight message in Northwind Queue from release 2.5.

## Considered Options

- Northwind Queue, the in-house broker the Relay team already operates.
- A managed cloud queue service.

## Consequences

- Good, because messages survive a consumer restart; the 2026-09 soak test held one hour of backlog with no loss.
- Good, because no vendor dependency or network path outside the Relay deployment is added.
- Bad, because the Relay team owns the broker's capacity planning as well as Relay itself.
- Bad, because at-least-once delivery means duplicates can reach consumers.

## Pros and Cons of the Options

### Northwind Queue

- Good, because the 2026-09 benchmark measured 12 milliseconds at the 99th percentile for enqueue.
- Good, because the Relay team operates it already, under its on-call rotation.
- Bad, because at-least-once delivery means duplicates are possible.

### A managed cloud queue service

- Good, because capacity planning moves to the provider.
- Bad, because no latency measurement was taken, so the budget cannot be shown to hold.
- Bad, because it adds a network path outside the Relay deployment and a vendor dependency.

## More Information

This record supersedes nothing. A reversal is a new record that marks this one superseded.
