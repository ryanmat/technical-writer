# Eval reports

The committed release reads of the technical-writer plugin, one report pair (`.json` and `.md`)
per run. The gate writes them; see `../gate.py` and the Evals section of the repository README
for how a run is graded.

## The v0.2.0 report

Every one of the 27 cases at two runs per model, run from the working tree at `4b58de6` with the judge pinned to `claude-sonnet-5-5`. A holdout case is at its bar when both runs pass (at two runs a single miss fails the forced 2 of 3 bar) and a regression case when at least one does; a review case also needs full recall of its seeded defects. Cost is the CLI's list-price estimate for the arm.

| model | report | cases at bar | runs passed | judge median | judge min | judge rule | cost USD |
|---|---|---|---|---|---|---|---|
| `claude-sonnet-5-5` | `20261018T195606Z-v0.2.0-sonnet` | 27 of 27 | 49 of 54 | 4 | 3 | PASS | 7.56 |
| `claude-opus-5` | `20261018T195609Z-v0.2.0-opus` | 26 of 27 | 47 of 54 | 4 | 3 | PASS | 45.41 |
| `claude-haiku-5-5` | `20261018T175333Z-v0.2.0-haiku` | 21 of 27 | 38 of 54 | 4 | 3 | recorded | 2.08 |

The v0.2.1, v0.2.2 and v0.2.3 releases changed documentation, packaging and the skill's
out-of-scope list, not the templates; their holdout reads (`20261019T000208Z`,
`20261019T001747Z` and `20261019T005942Z`, Sonnet 5.5) each passed 9 of 9 runs with a judge median of 4.

The case notes under `evals/cases/` and `evals/holdout/` cite the intermediate reads taken while
each case was written; those reports are kept in the build repository only, and this tree carries
the release reads alone.

The cases at bar and runs passed columns are the gate's own verdicts from its run log, which count a run only when the structural checker and the case's own graders both pass it; the committed report rows carry the checker layer alone, so they read higher (Opus 48 and Haiku 41 runs of 54).

Opus 5's one case below its bar is the model-card holdout, where one run wrote the carbon figure's marker as grams of CO2eq beside the Carbon Emitted label and the deterministic marker grader reads for the word carbon inside the marker; accepted on that evidence. Haiku 5.5's six cases below bar are register and discipline slips: two replies wrapped in a code fence (zero H1), the vendor diligence sentence in both advisory runs, two-sentence summary lines, a three-sentence step, and no diagram statement in either architecture run.

The Sonnet and Opus rows are reruns. The first Sonnet read (`20261018T175338Z-v0.2.0-sonnet`, kept under `evals/reports/`) missed the ADR holdout, where one run opened a guessed template path and drafted MADR from memory, and the privacy notice, where both runs wrote the unset support retention as a plain sentence instead of the marker. Between the reads the skill was pointed at the taxonomy's Template file column and the privacy notice template names an unset retention period as the marker. The v0.1.0 rows are in `20261018T014620Z-v0.1.0-sonnet`, `20261018T014618Z-v0.1.0-opus` and `20261018T014622Z-v0.1.0-haiku`; the calibration set's source run is `20261017T233258Z`.

## Reading a report

The header line records the Claude Code version, the plugin version, the git HEAD the run was
taken at and whether the working tree was dirty. A report taken inside a release step always
reads dirty, since the version bump is uncommitted at run time; the release's Status note in the
build repository says what the uncommitted diff held. Each row is one run: the case, the model,
the run index, the checker verdict with its finding counts by severity, the cost, the judge
score and a note for a failed grader.
