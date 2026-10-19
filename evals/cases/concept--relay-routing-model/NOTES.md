# concept--relay-routing-model

Seed: the first regression case, written on 2026-10-17 after the skill body exists; spec R1 (the request is classified as a concept, not a task, although the subject is a mechanism), R4 (the Grafana concept shape: a noun-phrase title, a one-sentence summary, writer-named body sections, Useful links last), R5 (noun-phrase headings with no gerund or How to opener), and R7 (the snippets never give the retention period, so the output carries an UNVERIFIED marker for it rather than a number).

Expected shape: a noun-phrase H1 naming the product and the feature, a one-sentence summary, an introduction carrying the why from the release announcement, body sections for the terms and the delivery behavior, the retention marker beside the expiry sentence, and Useful links pointing to the task and reference topics. reference.md is one document in that shape; it passes check_structure.py under the concept template at the engineer audience with no finding: the template declares no evidence slot, so the marker is text the checker does not count, and the marker grader in run_evals.py is what reads it.

First read: none yet. The gate records the first regression run here.
