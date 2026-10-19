---
type: regex
pattern: "^## Rejected Ideas$"
flags: m
match: contains
---

Verifies: the output carries PEP 12's Rejected Ideas section at level two, the section a draft most often folds into Alternatives Considered.
Cannot verify: that the section holds the review items and not the competing designs; the prose judge owns that split, and the evidence slot in check_structure.py over the output reads Alternatives Considered for a rejected option.
