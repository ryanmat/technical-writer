---
type: regex
pattern: "Considered Options"
flags: i
match: contains
---

Verifies: the reply names the missing Considered Options section, the structural defect MADR requires and the template lists as required.
Cannot verify: that the finding is ranked high or cites the template; the recall layer in run_evals.py records the match and the prose judge reads the ranking.
