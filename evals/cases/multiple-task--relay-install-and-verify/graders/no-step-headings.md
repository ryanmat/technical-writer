---
type: regex
pattern: "^#{1,6} Step \\d"
flags: m
match: not_contains
---

Verifies: no heading reads Step N, the cheapest sign that the task sections are named for what they do.
Cannot verify: that each task heading is a bare infinitive; the template's heading ban in check_structure.py owns the gerund check.
