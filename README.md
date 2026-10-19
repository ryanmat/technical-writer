# technical-writer

A Claude plugin that writes and reviews technical documents in the structure their audience expects.

[![Release](https://img.shields.io/github/v/tag/ryanmat/technical-writer?label=release&sort=semver)](https://github.com/ryanmat/technical-writer/tags)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)
[![Document types](https://img.shields.io/badge/document%20types-24-informational)](docs/document-types.md)
[![Audiences](https://img.shields.io/badge/audiences-7-informational)](docs/document-types.md#the-seven-audiences)

Tell it what kind of page you need and who will read it. It picks one of 24 document types, writes into that type's template, marks every fact your sources do not give, and checks the structure before it answers. The types cover user documentation, engineering and architecture, API reference text, AI governance, security, and privacy.

**Documentation:** [install](docs/install.md), [how it works](docs/how-it-works.md), [document types and audiences](docs/document-types.md), [troubleshooting](docs/troubleshooting.md), [releasing](docs/releasing.md).

## Install

    /plugin marketplace add ryanmat/technical-writer@v0.2.4
    /plugin install technical-writer@technical-writer

## Use

Ask for a document and attach the sources it should draw on:

    Write a task topic for engineers on creating an alert rule in Relay, from these release notes.

The reply names the type and audience it chose, gives the document, then lists the `[UNVERIFIED: ...]` markers left for you to fill. Where the sources are silent the skill writes a marker, not a guess.

It answers to a verb (write, draft, structure, review) with a document type, to a standard behind a type (MADR, model card, CVE, CVSS, WP260, DPIA), or to an audience for one. Some requests it handles:

    Draft an architecture decision record for choosing Postgres over DynamoDB for the queue backend. Here are the benchmark notes and the design doc.

    I need a model card for our intent classifier, for downstream providers. The eval results and training notes are attached.

    Turn this incident thread into a postmortem.

    Write a runbook for consumer lag on the orders topic; the alert definition and the escalation list are below.

    Draft a privacy notice for the account service, written for the people whose data it holds, from this data map.

    Fill out an Annex IV technical file for the fraud model from these design docs; audience is the regulator.

    Write a vulnerability advisory for this auth bypass; CVSS vector and affected versions are in the ticket.

It also reviews a document you already have:

    Review this README as a task topic and tell me what is missing.

    Check this ADR against MADR and list the findings by severity.

Or classifies without drafting:

    What kind of doc should "docs for the new alert rule feature" be? Do not draft yet.

## How it works

Every request becomes one document type for one audience. The seven audiences are engineer, operator, executive, regulator, auditor, data subject, and downstream provider. The audience decides the register, the length cap, and how precise the numbers are: an engineer gets exact values with units, a regulator gets two significant figures, an executive gets ranges.

Each type has a template. Its YAML front matter lists the required sections in order, the evidence each section has to carry, the caps per audience, and the prose rules. The structure comes from published standards: the Grafana Writers' Toolkit for the user documentation types, MADR for decision records, the Hugging Face card for model cards, the OpenSSF guide for security notices, WP260 and the ICO's DPIA steps for privacy. [attribution.md](skills/technical-writer/references/attribution.md) names each source with its license.

The checker, `scripts/check_structure.py`, reads that same front matter. The skill runs it over its own draft before answering, and the eval graders run it over every eval output, so what the skill promises and what the evals measure are one definition. You can run it on any document:

    uv run python scripts/check_structure.py --template skills/technical-writer/references/templates/task.md --audience engineer draft.md

Exit 0 means the document passes. Exit 1 comes with a JSON list of findings, each with a code, a severity, a line, and the rule broken; [troubleshooting](docs/troubleshooting.md) explains every code. Exit 2 means the checker itself did not run. `scripts/lint.sh <draft.md>` adds `vale` and `markdownlint` when they are on the path and says which were missing.

The skill reads your request, the files you attach, and its own reference files. It fetches nothing from the network, installs nothing, and changes no source you give it. It declines README files, pull request bodies, and penetration test reports, which belong to other tools.

## Evals

Every case lives in its own directory under `evals/holdout/` (written once, never edited) or `evals/cases/`. A run is graded twice: by the case's own graders inside `claude plugin eval`, and by the structural checker over the run's final text. A judge model scores the prose against [the rubric](evals/rubrics/prose.md) and is calibrated against hand-scored documents. A holdout case runs three times and passes at two of three. A regression case passes at half its runs. The release rule is a judge median of at least 4 with no run below 3 on Sonnet 5.5 and Opus 5.

    uv run python evals/gate.py --tag holdout --model claude-sonnet-5-5 --max-cost-usd 10

The v0.2.0 report ran every one of the 27 cases at two runs per model:

| model | cases at bar | runs passed | judge median | judge rule | cost USD |
|---|---|---|---|---|---|
| `claude-sonnet-5-5` | 27 of 27 | 49 of 54 | 4 | PASS | 7.56 |
| `claude-opus-5` | 26 of 27 | 47 of 54 | 4 | PASS | 45.41 |
| `claude-haiku-5-5` | 21 of 27 | 38 of 54 | 4 | recorded | 2.08 |

The reports, what each column means, and the reads behind the later releases are in [evals/reports](evals/reports/README.md).

## Development

    git clone https://github.com/ryanmat/technical-writer.git
    cd technical-writer
    uv sync
    uv run pytest
    uv run sh -c 'set -e; ruff check .; ruff format --check .'

Python 3.12 or later and [uv](https://github.com/astral-sh/uv).

```
technical-writer/
├── .claude-plugin/        plugin and marketplace manifests
├── skills/technical-writer/
│   ├── SKILL.md           the skill body
│   └── references/        style rules, audiences, taxonomy, attribution, one template per type
├── scripts/               check_structure.py (the checker), lint.sh (the linter wrapper)
├── evals/                 cases, holdout, the gate, the grader, the judge, the release reports
├── tests/                 pytest suite
└── docs/                  user documentation, written by the skill itself
```

## Bugs and contributing

File a [GitHub issue](https://github.com/ryanmat/technical-writer/issues) for a template that misreads its standard or a rule that flags a legitimate sentence, with the line that tripped it. Pull requests run the test suite and the linters above. A new template ships with its fixtures and an eval case, as every existing one did.

## License

Apache-2.0; see [LICENSE](LICENSE). The sources the templates quote keep their own licenses, listed in [attribution.md](skills/technical-writer/references/attribution.md).
