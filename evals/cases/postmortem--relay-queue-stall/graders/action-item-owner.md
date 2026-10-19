---
type: regex
pattern: "^- .+\\(owner: [^,)]+, priority: P[0-4], [A-Z][A-Z0-9]+-\\d+\\)"
flags: m
match: contains
---

Verifies: at least one action item ends in the template's owner, priority and tracker form, the cheapest sign that the Workbook action item rule was applied.
Cannot verify: that every item carries the form or that owners are roles and not names; the evidence slot in check_structure.py over the output reads the section, and the prose judge reads the wording.
