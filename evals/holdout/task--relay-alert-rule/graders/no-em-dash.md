---
type: regex
pattern: "—"
match: not_contains
---

Verifies: no em dash appears anywhere in the output, the one prose rule cheap enough to check without the structural grader.
Cannot verify: the other banned patterns (en dashes, subjective words, refer to); check_structure.py over the output owns the full set.
