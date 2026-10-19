# technical-writer

A Claude Code plugin whose single skill writes and reviews technical documents in the structure their audience expects.

## Overview

Ask Claude Code for documentation and the skill first names the document type (one of 24, from a task topic to a model card or a privacy notice), takes one audience from a fixed set of seven, and loads the type's template. The template's YAML front matter fixes the required sections, the evidence each section must carry, the length cap per audience, and the prose rules; the skill drafts into it, writes `[UNVERIFIED: what is missing]` wherever its sources give no fact, and runs a deterministic structural checker over the draft before it answers. The same checker grades the eval suite, so what the skill promises is what the evals measure. In review mode it checks an existing document against the same rules and returns ranked findings.

Six domains are covered: user documentation, engineering and architecture, API reference text, AI governance, security, and privacy. The templates take their structure from published standards (the Grafana Writers' Toolkit, MADR, the Hugging Face model card, the OpenSSF disclosure guide, WP260, and the ICO's DPIA steps, among others); `skills/technical-writer/references/attribution.md` records each source and its license.

## Setup

Install by tag; the current tag is `v0.2.2`:

    claude plugin marketplace add ryanmat/technical-writer@v0.2.2
    claude plugin install technical-writer@technical-writer

For a development checkout:

    uv sync
    uv run pytest
    uv run sh -c 'set -e; ruff check .; ruff format --check .'

## Usage

In Claude Code, name the document and the reader:

    Write a task topic for engineers on creating an alert rule in Relay, from the attached release notes.

The reply opens with the type and audience chosen, the document follows, and the reply closes with every `[UNVERIFIED: ...]` marker left for you to fill. To check a document yourself against a template:

    uv run python scripts/check_structure.py --template skills/technical-writer/references/templates/task.md --audience engineer draft.md

It prints a JSON report and exits 0 when the document passes, 1 when it has findings, 2 when the checker did not run. `scripts/lint.sh <draft.md>` runs `vale` and `markdownlint` over a draft when they are on the path and reports which were missing; neither is required.

## Documentation

- [Install the technical-writer plugin](docs/install.md)
- [The technical-writer workflow](docs/how-it-works.md): classification, the audience parameter, templates, evidence markers, and the self-check.
- [Document types and audiences](docs/document-types.md): the 24 types, the length caps, the seven audiences, and the marker.
- [Troubleshoot checker findings](docs/troubleshooting.md): every finding code with its cause and fix.
- [Release a new version](docs/releasing.md)

## Evals

Every eval case lives in its own directory under `evals/holdout/` (written once, never edited) or `evals/cases/`, and a run is graded twice: by the case's own graders inside `claude plugin eval`, and by the structural checker over each run's final text. A holdout case runs three times and passes when two of three runs pass; a regression case passes when at least half its runs do. The gate exits 0 when every case clears its bar, 1 when one falls below it, and 2 when the apparatus produced no verdict:

    uv run python evals/gate.py --tag holdout --model claude-sonnet-5-5 --max-cost-usd 10

Prose is scored separately by a judge model against `evals/rubrics/prose.md` (leads with the point, one idea per paragraph, no filler, register fits the audience; 1 to 5). The judge is calibrated against six holdout outputs scored by hand in `evals/calibration/scores.yaml`, and the test suite fails when the judge and the hand score differ by more than one point on any of them. The acceptance rule for a release is a median of at least 4 with no run below 3 on Sonnet 5.5 and Opus 5; Haiku 5.5 is recorded.

### Results

The v0.2.0 report, every one of the 27 cases at two runs per model, run from the working tree at `4b58de6` with the judge pinned to `claude-sonnet-5-5`. A holdout case is at its bar when both runs pass (at two runs a single miss fails the forced 2 of 3 bar) and a regression case when at least one does; a review case also needs full recall of its seeded defects. Cost is the CLI's list-price estimate for the arm.

| model | report | cases at bar | runs passed | judge median | judge min | judge rule | cost USD |
|---|---|---|---|---|---|---|---|
| `claude-sonnet-5-5` | `20261018T195606Z-v0.2.0-sonnet` | 27 of 27 | 49 of 54 | 4 | 3 | PASS | 7.56 |
| `claude-opus-5` | `20261018T195609Z-v0.2.0-opus` | 26 of 27 | 47 of 54 | 4 | 3 | PASS | 45.41 |
| `claude-haiku-5-5` | `20261018T175333Z-v0.2.0-haiku` | 21 of 27 | 38 of 54 | 4 | 3 | recorded | 2.08 |

The v0.2.1 and v0.2.2 releases changed documentation, packaging and the skill's out-of-scope
list, not the templates; their holdout reads (`20261019T000208Z` and `20261019T001747Z`, Sonnet
5.5) each passed 9 of 9 runs with a judge median of 4.

The case notes under `evals/cases/` and `evals/holdout/` cite the intermediate reads taken while
each case was written; those reports are kept in the build repository only, and this tree carries
the release reads alone.

The cases at bar and runs passed columns are the gate's own verdicts from its run log, which count a run only when the structural checker and the case's own graders both pass it; the committed report rows carry the checker layer alone, so they read higher (Opus 48 and Haiku 41 runs of 54).

Opus 5's one case below its bar is the model-card holdout, where one run wrote the carbon figure's marker as grams of CO2eq beside the Carbon Emitted label and the deterministic marker grader reads for the word carbon inside the marker; accepted on that evidence. Haiku 5.5's six cases below bar are register and discipline slips: two replies wrapped in a code fence (zero H1), the vendor diligence sentence in both advisory runs, two-sentence summary lines, a three-sentence step, and no diagram statement in either architecture run.

The Sonnet and Opus rows are reruns. The first Sonnet read (`20261018T175338Z-v0.2.0-sonnet`, kept under `evals/reports/`) missed the ADR holdout, where one run opened a guessed template path and drafted MADR from memory, and the privacy notice, where both runs wrote the unset support retention as a plain sentence instead of the marker. Between the reads the skill was pointed at the taxonomy's Template file column and the privacy notice template names an unset retention period as the marker. The v0.1.0 rows are in `20261018T014620Z-v0.1.0-sonnet`, `20261018T014618Z-v0.1.0-opus` and `20261018T014622Z-v0.1.0-haiku`; the calibration set's source run is `20261017T233258Z`.

## Layout

- `.claude-plugin/` - plugin and marketplace manifests.
- `skills/technical-writer/` - the skill body, its reference files, and one template per document type.
- `scripts/` - the structural checker shared by the skill and the evals, the linter wrapper, and the release export.
- `evals/` - eval cases, the gate, the result grader, the prose judge, and the committed release reports.
- `tests/` - pytest suite.
- `docs/` - the user documentation, written by the skill itself for the engineer audience.

## License

Apache-2.0; see [LICENSE](LICENSE). The sources the templates quote are listed with their licenses in `skills/technical-writer/references/attribution.md`.
