---
type: regex
pattern: "^## \\[Unreleased\\]"
flags: m
match: not_contains
---

Verifies: the entry for a dated release carries no Unreleased section, which belongs to changes not yet released.
Cannot verify: anything about the entries themselves; the category grader of the release notes case and check_structure.py over the output own those.
