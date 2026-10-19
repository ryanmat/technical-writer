---
type: regex
pattern: "^## (?!Useful links$).+"
flags: m
match: contains
---

Verifies: the output carries at least one level-two body section the writer named, the concept template's one required section.
Cannot verify: that the section explains what and why rather than how, or that Useful links comes last; check_structure.py and the prose judge own those.
