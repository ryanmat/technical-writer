# 0007-store-in-flight-messages-in-northwind-queue

Northwind Relay 2.5 stores in-flight messages in Northwind Queue, the in-house broker, instead of a managed cloud queue service.

## Status

Accepted, 2026-10-03.

## Context and Problem Statement

Relay buffers messages between producers and consumers. Release 2.3 kept them in process memory and lost them on restart. Release 2.5 must survive a consumer outage of up to one hour with no loss, keep enqueue p99 latency under 20 ms, and handle an expected 40 million messages a day (source: 2.5 planning note). Which backend stores in-flight messages from release 2.5?

## Decision Drivers

- No message loss during a consumer outage of up to one hour (source: 2.5 planning note).
- Enqueue p99 latency under 20 ms (source: 2.5 planning note).
- Capacity for 40 million messages a day (source: 2.5 planning note).
- Operational ownership: who plans capacity and who is paged.
- Cost: the team weighs it, but no source gives a figure. [UNVERIFIED: the cost of either option]

## Considered Options

- Northwind Queue
- Managed cloud queue service

## Decision Outcome

Chosen option: "Northwind Queue", because it is the only option with measured evidence for the drivers: the 2026-09 benchmark recorded an enqueue p99 of 12 ms against the 20 ms budget, and the soak test held one hour of backlog with zero messages lost.

We will store in-flight messages from release 2.5 in Northwind Queue, operated by the Relay team under its on-call rotation.

## Consequences

- Good, because the measured enqueue p99 of 12 ms leaves 8 ms of headroom under the 20 ms budget.
- Good, because the one-hour backlog soak test matches the one-hour outage requirement.
- Good, because messages stay inside the Relay deployment, with no added network path and no vendor dependency.
- Bad, because the Relay team owns capacity planning and carries the on-call load for the broker.
- Bad, because delivery is at-least-once, so duplicates are possible and consumers must tolerate them.
- Neutral, because the cost comparison is open until a figure exists for each option. [UNVERIFIED: the cost of either option]

## Confirmation

The 2026-09 benchmark and soak test of Northwind Queue are the evidence for this decision. [UNVERIFIED: whether the soak test load matched 40 million messages a day] [UNVERIFIED: how the team will confirm the 2.5 release meets the latency and no-loss requirements in production]

## Pros and Cons of the Options

### Northwind Queue

- Good, because enqueue p99 measured 12 ms, under the 20 ms budget.
- Good, because the soak test held one hour of backlog with zero messages lost.
- Good, because the Relay team operates it, so it adds no external network path or vendor dependency.
- Bad, because delivery is at-least-once and duplicates are possible.
- Bad, because the Relay team runs it under its own on-call rotation.

### Managed cloud queue service

- Good, because the provider handles capacity planning.
- Bad, because it adds a network path outside the Relay deployment and a vendor dependency.
- Bad, because no latency measurement was taken, so the 20 ms budget is unconfirmed.
- Bad, because the sources say nothing about its delivery guarantee or its behavior during a one-hour backlog. [UNVERIFIED: delivery semantics and backlog retention of the managed service]

## More Information

Sources: the 2.5 planning note and the 2026-09 benchmark and soak test of Northwind Queue. This record supersedes no earlier record.
