# Prose judge calibration set

Six documents the holdout cases produced, scored by hand on `../rubrics/prose.md`, so that
the prose judge can be checked against a human reading before its scores gate a
release. Ruled 2026-10-17 10:22 EDT; written attended, like the holdout, and never edited
afterwards except to fill `scores.yaml`.

## Contents

Each `<case>-run<n>.md` is the final document of one run of a holdout case, copied verbatim
from the trace of the holdout-green run at `evals/results/20261017T233258Z` (report
`evals/reports/20261017T233258Z.json`, Sonnet 5.5, git head 5651424). Every one of the six
passed the structural checker, so the rubric's four criteria are the only thing left to score.

`scores.yaml` carries one entry per document: its case, template and audience as the holdout
`expected.json` names them, a `score` of 1 to 5, and free-text `notes`. Fill every `score`
and set `scored_on` before the judge is calibrated.

## How to score

1. Read `../rubrics/prose.md` once.
2. For each document, read it as the named audience, score it as the rubric says (weakest
   criterion first, then at most one point of adjustment), and write one line of notes
   quoting the sentence that decided the score.
3. Do not look at a run's sibling before scoring it; the two runs of a case are scored
   independently and compared only afterwards.

## What the scores gate

The agreement test reads `scores.yaml` beside the judge's own scores over the same six files and
fails when any pair differs by more than one point or when any hand score is still null.
A rubric that cannot get within one point of a careful human reading is not fit to gate a
release, and the fix is to the rubric wording, never to the hand scores.

The judge's scores are `judge.json`, written by `uv run python evals/calibrate.py`, which sends
each document with its template and audience to the judge model through the same criteria the
`graders/prose-judge.md` files carry. Run it again after every change to the rubric, then
`uv run python evals/prose_judge.py` to re-render the graders.
