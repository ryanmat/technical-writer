---
type: regex
pattern: "^\\|.*\\|\\s*$"
flags: m
match: contains
---

Verifies: the output carries a Markdown table, the form a settings reference takes.
Cannot verify: that every setting from the help text has a row or that the columns carry the default; the prose judge reads that.
