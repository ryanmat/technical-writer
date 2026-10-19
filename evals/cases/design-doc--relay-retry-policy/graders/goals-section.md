---
type: regex
pattern: "^## Goals and Non-goals$"
flags: m
match: contains
---

Verifies: the output carries the Goals and Non-goals section at level two under the template's name, the section that separates a design doc from a description of the system.
Cannot verify: that the non-goals are things that could reasonably have been goals rather than negated goals; the prose judge owns the content and check_structure.py over the output owns the other required sections.
