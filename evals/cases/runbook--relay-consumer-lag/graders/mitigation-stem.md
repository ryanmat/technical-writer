---
type: regex
pattern: "^## Mitigation$[\\s\\S]*?^To [^\\n]*[:.]$"
flags: m
match: contains
---

Verifies: the Mitigation section is present under its name and opens its steps with a stem sentence on its own line, beginning with To and ending in a colon or a period, the procedure rule the checker enforces on the procedure section (Ryan, 2026-10-18 13:08 EDT).
Cannot verify: the step length, the one action per step, or the expected outputs; check_structure.py over the output owns those and the evidence slot reads the output sentences.
