---
type: regex
pattern: "^#+ Cyber\\b(?:(?!^#+ )[\\s\\S])*?(?:\\d+(?:\\.\\d+)?\\s*(?:%|percent)|\\d+ of \\d+)"
flags: m
match: not_contains
---

Verifies: the Cyber chapter carries no percentage and no count before the next heading, since the evaluation summary holds the date of the run and not its results; the chapter's slot is filled by the UNVERIFIED marker the marker grader reads, not by a number written from habit.
Cannot verify: that the marker names the security team's report; the prose judge reads the marker's text for vagueness.
