---
type: regex
pattern: "## Results[\\s\\S]*?\\n\\|[^\\n]+\\|"
match: contains
---

Verifies: a Markdown table row follows the Results heading, the disaggregated form Mitchell requires.
Cannot verify: that the table is broken down by both factors or that its numbers match the report; the Step 24 prose judge reads that.
