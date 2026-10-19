# multiple-task--relay-install-and-verify

Seed: the third regression case, written on 2026-10-17; spec R1 (the request is classified as a multiple-task procedure, since the goal takes three tasks in order, not a task), R4 (the Grafana multiple-tasks shape: a task list in the introduction, one Before you begin section, a task section per task, Verify last), R6 (the procedure rules in every task section, which the checker applies through the pattern-named procedure_section), R7 (the snippets never give the health endpoint's port, so the output carries an UNVERIFIED marker rather than a number), and R9 (expected output follows each command).

Expected shape: a verb-first H1 naming the goal, a one-sentence summary, a numbered list of the three task sections, Before you begin stating the 2.4.0 version and the root requirement from the snippets and marking the port unverified, three sections each opening with a To stem and one command per code block with its printed output, and Verify last. reference.md is one document in that shape; it passes check_structure.py under the template at the engineer audience with no finding: the version statement fills the Before you begin slot, so the port marker is text the checker does not count, and the marker grader in run_evals.py is what reads it.

First read: none yet. The gate records the first regression run here.
