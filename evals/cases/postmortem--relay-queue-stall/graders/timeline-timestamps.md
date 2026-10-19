---
type: regex
pattern: "^- 2026-10-03[T ]1[345]:\\d{2}"
flags: m
match: contains
---

Verifies: the timeline entries open with ISO timestamps on the incident's date, with T or a space between date and time as the template's evidence slot accepts both.
Cannot verify: that every export line became an entry in order; the evidence slot in check_structure.py over the output reads the section for a timestamp, and the prose judge reads completeness.
