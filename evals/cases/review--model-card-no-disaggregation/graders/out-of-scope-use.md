---
type: regex
pattern: "Out-of-Scope Use"
flags: i
match: contains
---

Verifies: the reply names the missing Out-of-Scope Use section, the structural defect the Hugging Face headings require.
Cannot verify: that the finding is ranked high or cites the template; the recall layer in run_evals.py records the match and the prose judge reads the ranking.
