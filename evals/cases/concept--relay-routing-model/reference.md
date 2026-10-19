# Routing model in Northwind Relay

The routing model decides which consumer groups receive each message a producer writes to a stream.

Before routing, every consumer read the whole stream and dropped what it did not need. Routing moves the filter into Relay, so a consumer receives only the messages its group asked for.

## Streams, routes, and consumer groups

A stream is a named, ordered sequence of messages written by producers. A route is a rule that binds a stream to a consumer group through a filter. The filter is a key and value pair a message must carry for the route to match. A consumer group is a set of consumers that share one route's messages between them.

## Route evaluation

Relay evaluates every message against every route on its stream, in route order. A message can match more than one route, and each matching consumer group receives its own copy. A message that matches no route stays in the stream until it expires. [UNVERIFIED: the retention period for an unmatched message]

Routes are evaluated at delivery time. A new route therefore applies to messages the stream already holds, not only to messages written after it.

## Useful links

- [Create a route](create-a-route.md)
- [Route settings](route-settings.md)
