# Changelog

All notable changes to this plugin are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the plugin follows
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.4] - 2026-10-18

### Changed

- The README's how-it-works section is prose instead of labeled bullets, the install block
  stands alone, and the Claude Code badge and the Requirements section are gone.
- The v0.2.4 holdout read for Sonnet 5.5 under `evals/reports/` (`20261019T013040Z`): 9 of 9 runs at
  bar, judge median 4.

## [0.2.3] - 2026-10-18

### Changed

- The README is written for a reader arriving from the public repository: badges, a quick
  start, eleven example prompts grouped by drafting, governance and security, review mode and
  classification, and the contributing terms.

- The v0.2.3 holdout read for Sonnet 5.5 under `evals/reports/` (`20261019T005942Z`): 9 of 9 runs at
  bar, judge median 4.

### Fixed

- `docs/releasing.md` says the export runs from the build repository, which alone carries
  `scripts/release.py`; the README layout line no longer lists the export under `scripts/`.

## [0.2.2] - 2026-10-18

### Fixed

- The release tooling, `scripts/release.py` and its test, stays in the build repository: the
  two files spell the private identifiers out, and 0.2.1 had exported them under an exemption.
- Nine internal pointers that survived the 0.2.1 strip in case notes and one grader are gone,
  and the release scan now also looks for the maintainer's first name and the build tooling.
- The release scan decodes every file with replacement instead of skipping one it cannot
  decode, so a file in another encoding is scanned like the rest; a latin-1 test covers it.

## [0.2.1] - 2026-10-18

The public release: the plugin is installed from the public repository `ryanmat/technical-writer`,
which carries the plugin, its tests, its evals and its user documentation and nothing else.

### Added

- User documentation under `docs/`, written by the skill itself for the engineer audience and
  passing the structural checker: install, how it works, document types and audiences,
  troubleshooting the checker's findings, and releasing.
- `LICENSE`: Apache-2.0 for the repository; the sources the templates quote keep their own
  licenses, listed in `skills/technical-writer/references/attribution.md`.
- The v0.2.1 holdout read for Sonnet 5.5 under `evals/reports/` (`20261019T000208Z`): 9 of 9
  runs at bar, judge median 4.
- `scripts/release.py`: exports the tracked tree at a tag into a clone of the public repository
  as one tagged commit, after a scan for identifiers that belong to the build repository.

### Changed

- The README is written for a reader who has never seen the repository and links the five
  documentation pages; the manifests name the author by GitHub handle.
- The skill's out-of-scope list names the README, the pull request body and the assessment
  report; the runbook template cites its section shape as this skill's own.
- `evals/reports/` keeps the release reads (v0.1.0 and v0.2.0 for the three models, the first
  Sonnet v0.2.0 read, and the calibration set's source run); the intermediate reads are gone.

## [0.2.0] - 2026-10-18

Second release: every type in the taxonomy has a template, the optional linters are wired in,
and the three-model report covers all 27 cases.

### Added

- Fifteen templates, each with a regression case: architecture description (arc42 section
  names, the C4 diagram checklist), design doc or RFC (Design Docs at Google, PEP 12), postmortem
  (the SRE Workbook chapter), runbook, changelog entry (Keep a Changelog), endpoint or field
  description (AIP-192), error catalog entry (RFC 9457, AIP-193), vulnerability advisory (the CVE
  CNA rules, CVSS v4.0), disclosure notification and SECURITY.md (the OpenSSF guide), system card,
  Annex IV technical file (Regulation (EU) 2024/1689), GPAI Model Documentation Form (the
  Commission's form), privacy notice (WP260 rev.01, Articles 13 and 14) and data protection
  impact assessment (the ICO's seven steps under the Open Government Licence v3.0).
- `scripts/lint.sh`: detects `vale` and `markdownlint` or `markdownlint-cli2`, runs those
  present with the configs beside the skill and prints one JSON report; a missing linter never
  blocks. The skill's self-check step runs it.
- The Vale configuration under `references/vale/`: the Google package plus the `TechnicalWriter`
  style with seven rules (dashes, subjunctive, recommendations, gerund headings, refer to,
  timeless words, subjective words), the markdownlint config, and an opt-in end-to-end test
  that downloads the Vale release recorded in `tests/fixtures/vale/VERSION`.
- The v0.2.0 reports for Sonnet 5.5, Opus 5 and Haiku 5.5 under `evals/reports/`, with the
  results table in the README.

### Changed

- The skill's step 3 sends the writer to the taxonomy table's Template file column instead of
  a path formed from the type name, after one holdout run drafted from memory.
- The DPIA template's Describe the processing slot requires nature, scope, context and purpose
  together; the privacy notice template treats a retention period the sources call unset as a
  marker, never a plain sentence.
- The vulnerability advisory, privacy notice and GPAI form templates and the system card,
  Annex IV and DPIA references carry the review fixes (the Severity slot lookahead,
  the qualifier ban sparing the month May, the compute figure, the regulator length cap).

## [0.1.0] - 2026-10-17

First release: the user documentation types, the architecture decision record and the model
card, with the checker and the eval harness that gate them.

### Added

- The `technical-writer` skill: classifies a request into a document type, takes one of seven
  audiences, drafts into the type's template, marks every claim its sources do not support as
  `[UNVERIFIED: what is missing]`, self-checks with the structural checker, and reviews an
  existing document against the same rules.
- Nine templates with machine-readable front matter: task, multiple-task procedure, tutorial,
  concept, reference, troubleshooting and release notes (from the Grafana Writers' Toolkit),
  the architecture decision record (MADR with Nygard's prose rules) and the model card (the
  Hugging Face card with Mitchell's disaggregated results).
- Reference files for the style rules, the procedure rules, the audiences, the type taxonomy,
  the checklists and the attribution of every borrowed rule.
- `scripts/check_structure.py`, the structural checker the skill and the eval graders share:
  required sections in order, evidence slots, length caps, heading and prose bans, procedure
  rules, with a JSON report and the three exit codes (pass, fail, apparatus).
- The eval harness over `claude plugin eval`: three holdout cases written attended and never
  edited, six regression drafting cases and three review cases, the gate with its set bars, the
  deterministic grader over every run's final text, and the prose judge with its rubric,
  calibration set and per-model acceptance rule.
- The v0.1.0 reports for Sonnet 5.5, Opus 5 and Haiku 5.5 under `evals/reports/`.

[Unreleased]: https://github.com/ryanmat/technical-writer/compare/v0.2.4...HEAD
[0.2.4]: https://github.com/ryanmat/technical-writer/releases/tag/v0.2.4
[0.2.3]: https://github.com/ryanmat/technical-writer/releases/tag/v0.2.3
[0.2.2]: https://github.com/ryanmat/technical-writer/releases/tag/v0.2.2
[0.2.1]: https://github.com/ryanmat/technical-writer/releases/tag/v0.2.1
[0.2.0]: https://github.com/ryanmat/technical-writer/releases/tag/v0.2.0
[0.1.0]: https://github.com/ryanmat/technical-writer/releases/tag/v0.1.0
