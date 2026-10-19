---
type: regex
pattern: "2026-10-29[^\\n]{0,40}14:00[^\\n]{0,10}UTC"
match: contains
---

Verifies: the public disclosure date is written with its time and time zone as the embargo plan gives it, the line a distributor schedules against.
Cannot verify: that the same date appears as the Timeline's to-be-disclosed field; the evidence slot in check_structure.py over the output reads that section for an ISO date.
