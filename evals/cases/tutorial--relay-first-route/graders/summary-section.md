---
type: regex
pattern: "^## Summary"
flags: m
match: contains
---

Verifies: the output carries the tutorial template's Summary section as a level-two heading, the section that separates a tutorial from a multiple-task procedure.
Cannot verify: that it follows the task sections or lists one bullet per task; check_structure.py over the output owns the order.
