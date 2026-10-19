---
type: regex
pattern: "Before you begin"
flags: i
match: contains
---

Verifies: the reply names the missing Before you begin section, the seeded structural defect the task template requires.
Cannot verify: that the finding is ranked high or cites the template; the recall layer in run_evals.py records the match and the prose judge reads the ranking.
