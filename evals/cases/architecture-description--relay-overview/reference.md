# Northwind Relay architecture description

Northwind Relay is a message routing service that delivers each message a producer writes to the consumer groups whose routes match it.

## Introduction and Goals

Relay exists so that a consumer receives only the messages its group asked for. Before routing, every consumer read the whole stream and dropped what it did not need; routing moves the filter into Relay. The quality goals, in the order the Relay team ranks them, are durability (no message is lost across a consumer outage of up to one hour), latency (enqueue at the 99th percentile under 20 milliseconds), and operability (one team runs Relay under one on-call rotation).

The stakeholders are the producer teams that write streams, the consumer teams that own routes, and the Relay team that operates the service.

## Constraints

Relay runs on the Northwind platform's container cluster and uses Northwind Queue as its only durable store; both are decided outside this document. Relay is written in Go, the platform's service language.

## Context and Scope

Diagram: Northwind Relay system context, a C4 system context diagram scoped to Relay, the producers that write to it, the consumers that read from it, and Northwind Queue; key: a box is a software system, a solid arrow is a message flow labeled with what crosses it, and the shaded box is Relay itself.

Producers write messages to named streams over the Relay API. Consumers register routes, each binding a stream to a consumer group through a filter, and read their group's messages. Northwind Queue holds every in-flight message. Nothing else talks to Relay.

## Solution Strategy

Relay evaluates routes at delivery time rather than at write time, so a new route applies to messages the stream already holds. Durability comes from writing every message to Northwind Queue before acknowledging the producer. Latency comes from keeping route evaluation in memory per stream and from a single network hop to the queue.

## Building Block View

Diagram: Northwind Relay containers, a C4 container diagram scoped to the Relay deployment; key: a box is a deployable unit with its technology in brackets, an arrow is a synchronous call unless marked async, and the dashed box is the Northwind Queue cluster Relay does not own.

The API container [Go] accepts writes and route registrations. The router container [Go] evaluates every message against every route on its stream, in route order, and hands each matching consumer group its own copy. The queue adapter [Go] writes to and reads from Northwind Queue. The Routes page [TypeScript] shows route state and the stalled-stream report.

## Runtime View

Diagram: message delivery, a C4 dynamic diagram scoped to one message from write to consumer read; key: a numbered arrow is one step in order, and a box is a container from the Building Block View.

A producer writes a message. The API writes it to Northwind Queue and acknowledges the write. The router reads the message, evaluates the routes on its stream in order, and enqueues one copy per matching consumer group. A consumer reads its group's copy. A message that matches no route stays in the stream until it expires.

## Deployment View

Diagram: Northwind Relay deployment, a C4 deployment diagram scoped to one production region; key: a box with a bold border is a cluster node, a nested box is a container instance, and an arrow is a network path with its protocol.

Relay runs three instances of each container across the platform cluster. Northwind Queue runs as its own cluster in the same region. The Routes page is served from the API container. [UNVERIFIED: the message throughput the deployment is sized for]

## Quality Requirements

Durability: a consumer outage of one hour loses no message; the 2026-09 soak test held one hour of backlog with no loss. Latency: enqueue at the 99th percentile under 20 milliseconds; the 2026-09 benchmark measured 12 milliseconds. Operability: every alert pages the Relay rotation and no other.

## Risks and Technical Debt

At-least-once delivery means a consumer can receive a duplicate after a router restart, and consumers must tolerate it. The Relay team owns the capacity planning of Northwind Queue as well as Relay. Route evaluation is linear in the number of routes on a stream, which has not been measured past 200 routes.

## Glossary

Stream: a named, ordered sequence of messages written by producers. Route: a rule that binds a stream to a consumer group through a filter. Filter: a key and value pair a message must carry for the route to match. Consumer group: a set of consumers that share one route's messages between them.
