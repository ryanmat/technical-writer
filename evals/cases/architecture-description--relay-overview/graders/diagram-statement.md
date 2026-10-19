---
type: regex
pattern: "^Diagram: .+\\bkey: \\S"
flags: m
match: contains
---

Verifies: at least one view section opens with a diagram statement in the template's form, the line naming the diagram and its key, the cheapest sign that the C4 checklist was applied.
Cannot verify: that every view section carries one; the evidence slot in check_structure.py over the output reads each section, where a marker in the section stands in for the statement.
