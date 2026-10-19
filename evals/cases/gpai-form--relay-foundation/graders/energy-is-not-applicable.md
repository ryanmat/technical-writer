---
type: regex
pattern: "^#+ Amount of energy used for training\\b(?:(?!^#+ )[\\s\\S])*?\\bN/A\\b"
flags: m
match: contains
---

Verifies: the energy field reads N/A before the next heading, the form's own answer when the compute or hardware provider withholds critical information, so no energy figure is estimated.
Cannot verify: that the reason for N/A is stated beside it; the prose judge reads the field for a bare N/A with no reason.
