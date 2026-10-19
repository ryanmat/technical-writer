---
type: regex
pattern: "unverified|source"
flags: i
match: contains
---

Verifies: the reply reports the version claim in the summary as unsupported, either by asking for its source or by naming the UNVERIFIED marker.
Cannot verify: that the finding points at the 2.4.0 claim rather than another line; the recall layer mirrors this pattern and the prose judge reads the location.
