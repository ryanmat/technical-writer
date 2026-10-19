---
type: regex
pattern: "^### Resolution"
flags: m
match: contains
---

Verifies: the entry carries the template's Resolution section at level three.
Cannot verify: that the restart command is followed by its printed output; the evidence slot in check_structure.py over the output owns that.
