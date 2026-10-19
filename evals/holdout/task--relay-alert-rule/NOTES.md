# task--relay-alert-rule

Seed: the first holdout case, written attended on 2026-10-17 before the skill body exists, so the skill is written against it rather than tuned to it; spec R1 (the request is classified as a task), R6 (the Steps section follows the procedure rules: a To stem, one action per step, an expected result where the outcome is not obvious), and R7 (the source snippets omit the permission the Before you begin section requires, so the output must carry an UNVERIFIED marker for it rather than an invented role).

Expected shape: a verb-first H1, a one-sentence summary, Before you begin stating the 2.4.0 version requirement from the release line and marking the permission unverified, Steps with a stem beginning with To and the UI labels in bold exactly as the snippets spell them, and Next steps. reference.md is one document in that shape; it passes check_structure.py under the task template at the engineer audience with no finding: the version statement fills the Before you begin slot, so the permission marker is text the checker does not count, and the marker grader is what reads it.

First read: none yet. The first holdout run records its read here.
