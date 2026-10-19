---
type: regex
pattern: "^## Steps"
flags: m
match: contains
---

Verifies: the output carries the task template's Steps section as a level-two heading.
Cannot verify: the order of the sections or the presence of Before you begin; check_structure.py over the output owns both.
