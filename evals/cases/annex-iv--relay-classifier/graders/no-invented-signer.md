---
type: regex
pattern: "(?:signed|signature|signatory|sign-off)[^\\n\\[]{0,40}\\b(?:by|of)\\s+(?!the\\b|a\\b|its\\b)[A-Z][a-z]+ [A-Z][a-z]+"
match: not_contains
---

Verifies: no person's name follows the words signed, signature, signatory or sign-off outside a marker, since the test summary says the responsible person has not signed and names no one; the slot is filled by the marker, not by a signer written from habit.
Cannot verify: that the marker names the signature of TR-0912; the prose judge reads the marker's text for vagueness.
