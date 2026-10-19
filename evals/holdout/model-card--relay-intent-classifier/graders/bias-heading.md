---
type: regex
pattern: "^## Bias, Risks, and Limitations"
flags: m
match: contains
---

Verifies: the output carries the Hugging Face Bias, Risks, and Limitations section as a level-two heading, spelled as upstream spells it.
Cannot verify: the other twenty required headings or their order; check_structure.py over the output owns them.
