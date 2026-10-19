---
type: regex
pattern: "TR-0912[^\\n]{0,80}2026-09-12|2026-09-12[^\\n]{0,80}TR-0912"
match: contains
---

Verifies: the test report is named with its identifier and its date on one line as the test summary gives them, the dated half of the item 2(g) slot.
Cannot verify: that the signature is marked rather than invented; the marker grader reads the output for a marker naming the signature, and the next grader reads for a signer.
