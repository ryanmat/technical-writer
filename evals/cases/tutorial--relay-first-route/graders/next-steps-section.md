---
type: regex
pattern: "^## Next steps"
flags: m
match: contains
---

Verifies: the output carries the tutorial template's required Next steps section as a level-two heading.
Cannot verify: that it is last or that it links a task, a concept, and a reference; check_structure.py and the prose judge own those.
