---
type: regex
pattern: "^# POST /routes$"
flags: m
match: contains
---

Verifies: the title is the HTTP method and the path with nothing else, the form the template's H1 pattern fixes for an endpoint page, with no code style around it.
Cannot verify: that the summary line under it omits its subject and opens with a verb; the prose judge reads that, and the banned pattern in check_structure.py over the output catches a This endpoint opener.
