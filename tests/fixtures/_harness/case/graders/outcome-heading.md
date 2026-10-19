---
type: regex
pattern: "^## Outcome"
flags: m
match: contains
---

Verifies: the output carries the Outcome section as a level-two heading.
Cannot verify: the section's content or its order after Context; the structural grader owns both.
