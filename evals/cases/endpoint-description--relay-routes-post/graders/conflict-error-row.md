---
type: regex
pattern: "409[^\\n]*ROUTE_CONFLICT|ROUTE_CONFLICT[^\\n]*409"
match: contains
---

Verifies: the Errors section carries the name conflict as the error table gives it, the status code and the catalog identifier on one line, the row an integrator looks up first for a registration call.
Cannot verify: that all four errors are present or that none was added; the evidence slot in check_structure.py over the output reads the section for a status code, and the prose judge reads completeness against the sources.
