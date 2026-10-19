---
type: regex
pattern: "^# .*\\n(?:(?!^\\|)[\\s\\S])*?2\\.4\\.0"
flags: m
match: contains
---

Verifies: the release version from the about dialog box appears after the title and before the first table row, where the template's evidence slot wants it.
Cannot verify: that the version statement is a sentence about the values rather than a stray mention; check_structure.py's slot pattern and the prose judge own that.
