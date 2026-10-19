# reference--relay-settings

Seed: the second regression case, written on 2026-10-17; spec R1 (the request is classified as a reference, not a task, although it concerns the rule editor), R4 (the Grafana reference shape: a noun-phrase title, a one-sentence summary, a table section the writer names, API documentation optional), R7 (the help text shows no default for Delivery gap, so the cell carries an UNVERIFIED marker rather than a number), and R9 (the version statement comes before the table, which the template's evidence slot on the introduction enforces).

Expected shape: a noun-phrase H1 naming the product and the settings, a one-sentence summary, an introduction stating the 2.4.0 version from the release line before any table, one Settings section with a table of five rows carrying the labels in bold as the help text spells them, the Delivery gap default as the marker, and no API documentation section. reference.md is one document in that shape; it passes check_structure.py under the reference template at the engineer audience with no finding: the version statement fills the introduction's slot, so the marker in the table is text the checker does not count, and the marker grader in run_evals.py is what reads it.

First read: none yet. The gate records the first regression run here.
