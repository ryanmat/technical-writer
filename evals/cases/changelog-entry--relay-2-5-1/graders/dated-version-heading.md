---
type: regex
pattern: "^## \\[2\\.5\\.1\\] - 2026-10-17$"
flags: m
match: contains
---

Verifies: the version section is headed in Keep a Changelog form, the version in brackets with the release date after the hyphen, the one place this type differs from release notes.
Cannot verify: that the categories are only the standard six or that every entry carries an identifier; SECTION_UNKNOWN and the identifier ban in check_structure.py over the output own those.
