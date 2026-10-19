---
type: regex
pattern: "^## \\[?v?2\\.5\\.0\\]?"
flags: m
match: contains
---

Verifies: the document carries the template's version section at level two, headed by the version the request names.
Cannot verify: that the release date sits on the first line under it in ISO form; graders/release-date.md owns that, and the evidence slot in check_structure.py over the output reads the same line, where a marker anywhere in the section's prose stands in for it.
