# Routing model in Northwind Relay

Northwind Relay routes every message from the stream a producer writes to the consumers whose routes match it.

## Understanding routes

A route names a stream, a filter, and a consumer group. A message that matches no route stays in the stream until it expires.

## Useful links

- [Create a route](create-a-route.md)
