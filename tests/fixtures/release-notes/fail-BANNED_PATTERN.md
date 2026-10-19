# Northwind Relay 2.5.0 release notes

Northwind Relay 2.5.0 adds retry on route timeout and fixes the stalled-stream report.

## [2.5.0]

Released 2026-10-17. Northwind Relay follows Semantic Versioning.

### Added

- Routes retry delivery after a timeout (RELAY-412).

### Fixed

- The Routes page no longer reports a stalled stream for a route whose delivery gap is unset.
