---
type: regex
pattern: "^## Escalation$[\\s\\S]*?platform"
flags: m
match: contains
---

Verifies: the Escalation section names the platform rotation the handbook line gives as the target.
Cannot verify: that the condition is stated and the wait is marked rather than invented; the evidence slot in check_structure.py over the output reads the target and condition, and the marker grader reads the wait.
