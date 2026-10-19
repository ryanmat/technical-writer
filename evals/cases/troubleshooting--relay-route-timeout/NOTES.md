# troubleshooting--relay-route-timeout

Seed: the fifth regression case, written on 2026-10-17; spec R1 (the request is classified as troubleshooting, a symptom to a verified fix, not a task), R4 (the GitLab-shaped entry: a heading naming the message, Symptom, Cause, Resolution, Related last), R7 (the design note names the route timeout but gives no value, so the Cause carries an UNVERIFIED marker rather than a number), and R9 (the Resolution's commands are followed by the output the runbook transcript shows, which the evidence slot reads).

Expected shape: an H1 beginning Troubleshoot or a noun phrase, a one-sentence summary, one entry headed Error: with the message in code style, a Symptom quoting the page state and the status command's output, a Cause from the design note with the timeout marked unverified, a Resolution with a To stem, the restart and status commands each followed by their printed output, and Related last. reference.md is one document in that shape; it passes check_structure.py under the troubleshooting template at the engineer audience with no finding: the Resolution's output statements fill its slot, and the marker in the Cause is text the checker does not count, which the marker grader in run_evals.py reads.

First read: none yet. The gate records the first regression run here.
