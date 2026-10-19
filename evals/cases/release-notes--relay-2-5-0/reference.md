# Northwind Relay 2.5.0 release notes

Northwind Relay 2.5.0 adds retry on route timeout, lowers the default evaluation interval, and fixes the stalled-stream report on the **Routes** page.

## [2.5.0]

Released 2026-10-17. Northwind Relay follows Semantic Versioning. This release carries one breaking change, under Changed.

### Added

- Routes retry delivery after a timeout, up to the retry limit set on the route (RELAY-412).

### Changed

- **Breaking:** the default evaluation interval is 30 seconds, down from 60. A route that relied on the 60 second default evaluates twice as often after the upgrade (RELAY-398).

### Fixed

- The **Routes** page no longer reports a stalled stream for a route whose delivery gap is unset. [UNVERIFIED: the issue or pull request that made this change]
