---
type: regex
pattern: "^# Embargoed notification: "
flags: m
match: contains
---

Verifies: the title opens with the embargo variant's words, the marker the template's H1 pattern reads to tell the two forms apart.
Cannot verify: that the confidentiality terms follow the summary line or that the Disclosure section carries the embargo form's content; the prose judge reads the first, and the evidence slot in check_structure.py over the output reads the second for a date and a contact.
