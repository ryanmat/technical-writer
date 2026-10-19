# Northwind Relay changelog

All notable changes to Northwind Relay are documented in this file, newest version first.

## [2.5.1] - 2026-10-17

### Fixed

- Routes with a retry limit of zero no longer retry once before reaching the stalled-stream report.
- The Routes page shows the attempt count on a stalled-stream row after a replay.

### Security

- The route registration call rejects a retry limit above the platform cap instead of clamping it silently.
