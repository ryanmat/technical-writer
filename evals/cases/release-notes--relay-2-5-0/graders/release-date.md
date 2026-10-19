---
type: regex
pattern: "^## \\[?v?2\\.5\\.0\\]?[^\\n]*\\n\\s*(?=\\S)[^\\n]*\\b\\d{4}-\\d{2}-\\d{2}\\b"
flags: m
match: contains
---

Verifies: the first non-blank line under the version heading carries a date in ISO 8601 form, the release line the template puts there; a run that drops the line, or moves the date under a category, fails here even when a marker elsewhere in the section fills the evidence slot.
Cannot verify: that the date is the one the sources give or that the line states the versioning scheme and the breaking-change count; the reader of the report owns the first and the template guidance the second.
