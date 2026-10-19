---
type: regex
pattern: "https://api\\.example\\.com/problems/route-conflict"
match: contains
---

Verifies: the entry carries the problem type's URI as the registry gives it, the member RFC 9457 makes the identity of a problem type and the one a client matches on.
Cannot verify: that the URI sits in the Problem details table beside the status and the title; the evidence slot in check_structure.py over the output reads that section for the three.
