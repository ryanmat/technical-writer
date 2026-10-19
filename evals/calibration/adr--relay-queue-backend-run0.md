# 0007-store-in-flight-messages-in-northwind-queue

Northwind Relay stores in-flight messages from release 2.5 in Northwind Queue, the in-house broker, instead of a managed cloud queue service.

## Status

Accepted, 2026-10-03.

## Context and Problem Statement

Relay buffers messages between producers and consumers. Release 2.3 kept messages in process memory and lost them on restart. Release 2.5 must survive a consumer outage of up to one hour with no loss, keep the enqueue p99 under 20 ms, and carry an expected 40 million messages a day (source: 2.5 planning note). The question is which backend stores in-flight messages.

## Decision Drivers

- No message loss during a consumer outage of up to one hour (source: 2.5 planning note).
- Enqueue p99 under 20 ms (source: 2.5 planning note).
- Volume of 40 million messages a day (source: 2.5 planning note).
- Operational ownership: who runs the backend and carries the pager.
- Cost: the team weighs it, and no source gives a price for either option. [UNVERIFIED: cost of running Northwind Queue and of the managed cloud queue service]

## Considered Options

- Northwind Queue
- Managed cloud queue service

## Decision Outcome

Chosen option: "Northwind Queue", because it is the only option with measured evidence for both requirements: an enqueue p99 of 12 ms against the 20 ms budget, and zero messages lost when it held one hour of backlog in the 2026-09 soak test.

We will store in-flight messages from release 2.5 in Northwind Queue, operated by the Relay team under its on-call rotation.

## Consequences

- Good, because the measured enqueue p99 of 12 ms leaves 8 ms of headroom under the 20 ms budget (source: 2026-09 benchmark).
- Good, because the soak test held one hour of backlog with zero messages lost, which matches the outage requirement (source: 2026-09 soak test).
- Good, because the broker stays inside the Relay deployment, with no network path outside it and no vendor dependency (source: 2.5 planning note, option two).
- Bad, because the Relay team operates the broker under its on-call rotation, and capacity planning is the team's job, not a provider's.
- Bad, because delivery is at-least-once, so duplicates are possible, and consumers must handle them.
- Neutral, because the soak test covered one hour of backlog, the stated requirement, and no source reports a longer run or a test at 40 million messages a day. [UNVERIFIED: Northwind Queue behavior at the expected daily volume]

## Confirmation

The team confirms the decision by repeating the benchmark and the one-hour soak test against the 2.5 release build and checking that the enqueue p99 stays under 20 ms with zero messages lost. [UNVERIFIED: the owner and the date of this check]

## Pros and Cons of the Options

### Northwind Queue

- Good, because the enqueue p99 measured 12 ms, under the 20 ms budget.
- Good, because the soak test held one hour of backlog with zero messages lost.
- Good, because it adds no network path outside the Relay deployment and no vendor dependency.
- Bad, because the Relay team operates it under its on-call rotation.
- Bad, because delivery is at-least-once and duplicates are possible.
- Bad, because the sources give no cost figure. [UNVERIFIED: cost of running Northwind Queue]

### Managed cloud queue service

- Good, because the provider handles capacity planning.
- Bad, because it adds a network path outside the Relay deployment and a vendor dependency.
- Bad, because no latency measurement was taken, so the 20 ms budget is unverified for this option.
- Bad, because the sources say nothing about its delivery guarantee or its behavior under a one-hour backlog. [UNVERIFIED: delivery semantics and one-hour backlog behavior of the managed cloud queue service]
- Bad, because the sources give no cost figure. [UNVERIFIED: cost of the managed cloud queue service]

## More Information

Sources: the 2.5 planning note and the 2026-09 benchmark and soak test of Northwind Queue. This record supersedes no earlier record.
