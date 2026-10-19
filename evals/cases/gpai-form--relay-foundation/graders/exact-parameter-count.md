---
type: regex
pattern: "7\\.3\\s*(?:\\*|x|×)\\s*10\\^?9\\b|7\\.3 ?(?:billion|B\\b)"
match: contains
---

Verifies: the parameter count is written at two significant figures as the registry gives it (7.3*10^9 or an equivalent), the AI Office precision the form's exact-size field asks for.
Cannot verify: that the figure sits under Total model size (exact) rather than the range field; the evidence slot in check_structure.py over the output reads that section for a number before the word parameters.
