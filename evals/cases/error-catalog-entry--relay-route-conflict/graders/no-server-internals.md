---
type: regex
pattern: "RouteTableConflictException|routes\\.go"
match: not_contains
---

Verifies: the server's exception class and source file from the log line stay out of the entry, the AIP-193 rule that a message must not assume knowledge of the implementation, which the template's Cause section and prose rules carry.
Cannot verify: that the cause and resolution are complete or in the caller's terms; the prose judge reads those.
