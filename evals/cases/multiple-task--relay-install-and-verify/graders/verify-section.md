---
type: regex
pattern: "^## Verify\\b"
flags: m
match: contains
---

Verifies: the output closes with a level-two Verify section, the section the multiple-task template requires and the task template lacks.
Cannot verify: that it comes last or that its steps carry a stem sentence; check_structure.py and the by-hand checklist own those.
