---
type: regex
pattern: "\\b(?:careless|negligen|should have|blame|at fault)"
flags: i
match: not_contains
---

Verifies: the document carries none of the blame words the template bans, so the maintainer named in the cause note is not blamed in the postmortem.
Cannot verify: a blaming stance in other words; the prose judge owns that, and check_structure.py over the output applies the same ban at the low severity.
