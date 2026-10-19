---
type: regex
pattern: "disaggregat|results table|by (?:language|channel|factor)"
flags: i
match: contains
---

Verifies: the reply reports that Results carries one aggregate number and no table broken out by the factors the card names, the Mitchell et al. requirement the evidence slot enforces.
Cannot verify: that the reply names both factors; the recall layer mirrors this pattern and the prose judge reads the rest.
