# technical-writer

A Claude plugin that writes and reviews technical documents.

[![Release](https://img.shields.io/github/v/tag/ryanmat/technical-writer?label=release&sort=semver)](https://github.com/ryanmat/technical-writer/tags)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue)](pyproject.toml)
[![Claude Code plugin](https://img.shields.io/badge/Claude%20Code-plugin-black)](https://code.claude.com/docs/en/plugins)
[![Document types](https://img.shields.io/badge/document%20types-24-informational)](docs/document-types.md)
[![Audiences](https://img.shields.io/badge/audiences-7-informational)](docs/document-types.md#the-seven-audiences)

You name the kind of page and the reader; the skill picks one of 24 document types, loads that type's template, drafts into its required sections, marks every fact its sources do not give, and checks the structure before it answers. It covers user documentation, engineering and architecture, API reference text, AI governance, security, and privacy.

**Start with the documentation:** [install](docs/install.md), [how it works](docs/how-it-works.md), [document types and audiences](docs/document-types.md), [troubleshooting](docs/troubleshooting.md), [releasing](docs/releasing.md).

## Get started

Inside Claude Code, add the marketplace at the release tag and install the plugin:

    /plugin marketplace add ryanmat/technical-writer@v0.2.3
    /plugin install technical-writer@technical-writer

The same two commands work from a shell as `claude plugin marketplace add ...` and `claude plugin install ...`. Pin the tag; `main` is not an install target.

Then ask for a document, with the source material attached or pasted:

    Write a task topic for engineers on creating an alert rule in Relay, from these release notes.

The reply opens with the type and audience it chose, the document follows, and the reply closes with every `[UNVERIFIED: ...]` marker left for you to fill. Anything the sources do not say comes back as a marker, never as a guess.

## Example prompts

The skill triggers on a verb (write, draft, structure, review) with a document type, a standard behind a type (MADR, model card, CVE, CVSS, WP260, DPIA), or an audience for one.

    Draft an architecture decision record for choosing Postgres over DynamoDB for the queue backend. Here are the benchmark notes and the design doc.

    I need a model card for our intent classifier, for downstream providers. The eval results and training notes are attached.

    Turn this incident thread into a postmortem.

    Write a runbook for consumer lag on the orders topic; the alert definition and the escalation list are below.

    Draft a privacy notice for the account service, written for the people whose data it holds, from this data map.

    Fill out an Annex IV technical file for the fraud model from these design docs; audience is the regulator.

    Write a vulnerability advisory for this auth bypass; CVSS vector and affected versions are in the ticket.

Review an existing document instead of writing one:

    Review this README as a task topic and tell me what is missing.

    Check this ADR against MADR and list the findings by severity.

Ask for the classification alone:

    What kind of doc should "docs for the new alert rule feature" be? Do not draft yet.

## How it works

- **One type, one audience.** Every request becomes one of 24 types across six domains, for one of seven audiences (engineer, operator, executive, regulator, auditor, data subject, downstream provider). The audience sets the register, the length cap, and how precise the numbers are.
- **The template is the contract.** Each type has a template whose YAML front matter fixes the required sections in order, the evidence each section must carry, the caps per audience, and the prose rules. The templates take their structure from published standards: the Grafana Writers' Toolkit, MADR, the Hugging Face model card, the OpenSSF disclosure guide, WP260, the ICO's DPIA steps, and others listed with their licenses in [attribution.md](skills/technical-writer/references/attribution.md).
- **No guessing.** A claim the sources do not support is written as `[UNVERIFIED: what is missing]`, inline, and listed in the reply.
- **The checker is the grader.** `scripts/check_structure.py` reads the same front matter the skill drafts from, so the self-check and the eval graders cannot disagree about what a conforming document is.

To run the checker yourself:

    uv run python scripts/check_structure.py --template skills/technical-writer/references/templates/task.md --audience engineer draft.md

It prints a JSON report and exits 0 when the document passes, 1 when it has findings, 2 when the checker did not run. `scripts/lint.sh <draft.md>` runs `vale` and `markdownlint` when they are on the path and reports which were missing; neither is required.

## What the plugin does and does not do

The skill reads the request, the files you attach, and its own reference files. It fetches nothing from the network, installs nothing, and modifies no source you give it. The scripts are standard-library Python; `vale` and `markdownlint` are optional and detected, never installed. The skill declines three document kinds that belong to other tools: README files, pull request bodies, and penetration test or assessment reports.

## Evals

Every case lives in its own directory under `evals/holdout/` (written once, never edited) or `evals/cases/`. A run is graded twice, by the case's own graders inside `claude plugin eval` and by the structural checker over the run's final text; a judge model scores the prose against [the rubric](evals/rubrics/prose.md), calibrated against hand-scored documents. A holdout case runs three times and passes at two of three; a regression case passes at half its runs. The release rule is a judge median of at least 4 with no run below 3 on Sonnet 5.5 and Opus 5.

    uv run python evals/gate.py --tag holdout --model claude-sonnet-5-5 --max-cost-usd 10

The v0.2.0 report ran every one of the 27 cases at two runs per model:

| model | cases at bar | runs passed | judge median | judge rule | cost USD |
|---|---|---|---|---|---|
| `claude-sonnet-5-5` | 27 of 27 | 49 of 54 | 4 | PASS | 7.56 |
| `claude-opus-5` | 26 of 27 | 47 of 54 | 4 | PASS | 45.41 |
| `claude-haiku-5-5` | 21 of 27 | 38 of 54 | 4 | recorded | 2.08 |

The reports, what each column means, and the reads behind the later releases are in [evals/reports](evals/reports/README.md).

## Requirements

- Claude Code with plugin support; the current release was tested with 2.1.302.
- For development: Python 3.12 or later and [uv](https://github.com/astral-sh/uv).

## Development

    git clone https://github.com/ryanmat/technical-writer.git
    cd technical-writer
    uv sync
    uv run pytest
    uv run sh -c 'set -e; ruff check .; ruff format --check .'

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

## Reporting bugs and contributing

File a [GitHub issue](https://github.com/ryanmat/technical-writer/issues) for a template that misreads its standard or a rule that flags a legitimate sentence, with the line that tripped it. Pull requests run the test suite and the linters above; a new template ships with its fixtures and an eval case, as every existing one did.

## License

Apache-2.0; see [LICENSE](LICENSE). The sources the templates quote keep their own licenses, listed in [attribution.md](skills/technical-writer/references/attribution.md).
