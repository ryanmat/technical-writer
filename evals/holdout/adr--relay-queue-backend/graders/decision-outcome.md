---
type: regex
pattern: "^## Decision Outcome"
flags: m
match: contains
---

Verifies: the output carries the MADR Decision Outcome section as a level-two heading.
Cannot verify: the sections before it or their order; check_structure.py over the output owns both.
