---
type: regex
pattern: "^## Quality Requirements$"
flags: m
match: contains
---

Verifies: the output carries the Quality Requirements section at level two under arc42's name, the section a description most often drops when the sources are thin.
Cannot verify: that the section makes each quality goal testable with a scenario and a measure; check_structure.py over the output owns the other required sections and the prose judge owns the content.
