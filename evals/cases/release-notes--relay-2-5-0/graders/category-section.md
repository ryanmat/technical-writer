---
type: regex
pattern: "^### (?:Added|Changed|Deprecated|Removed|Fixed|Security)$"
flags: m
match: contains
---

Verifies: at least one of the six Keep a Changelog categories appears at level three, the grouping a changelog has and a task topic never does.
Cannot verify: that no category outside the six appears or that every entry carries an identifier; SECTION_UNKNOWN and the identifier ban in check_structure.py over the output own those.
