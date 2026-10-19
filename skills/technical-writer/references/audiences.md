# Audiences

Every template takes one audience (spec R3), and the audience changes three things: the
register the document is written in, the length it may run to, and the precision its numbers
carry. The seven audiences below are the only values; they are held in one constant,
`AUDIENCES` in `scripts/check_structure.py`, and this file describes them in the same order.
When a request names no audience, the skill picks the type's default from the table at the
end and states the pick in its reply.

## How the three dimensions work

Register is the voice and the vocabulary: who the reader is assumed to be, what they already
know, and whether they want the reason or only the action. Length is the cap each template
carries in its `length_caps` front matter, one number per audience the type supports, counted
in words outside fenced code blocks; the caps scale down for executives and the checker
reports `LENGTH_EXCEEDED` when a document passes its cap. Precision is how a number is written:
exact with units, to a stated number of significant figures, or as a range. The precision
rule comes from the GPAI Model Documentation Form, which fixes precision per reader: the AI
Office gets two significant figures, national competent authorities get ranges and orders of
magnitude, and downstream providers get the integration values regulators do not. The same
pattern applies to every type.

## The seven audiences

### engineer

- Register: a peer who builds or integrates the thing. Exact identifiers, commands, flags, and versions; the reason given once where it changes what they do.
- Length: the type's full cap; task topics run to 1500 words and ADRs to 1200.
- Precision: exact values with units as measured or configured; version numbers complete; no rounding the reader would have to undo.

### operator

- Register: the person running the system when something happens. Imperative, no rationale, the action and its expected result; conditions before instructions.
- Length: the type's full cap, with the procedure rules binding every numbered step.
- Precision: exact thresholds, commands, and identifiers the runbook or advisory needs; a version range only when the fix covers several versions, written as the exact bounds.

### executive

- Register: a decision maker who reads the summary and the consequences. Plain words, the decision and the cost first, no procedure, no implementation detail.
- Length: the type's executive cap, about one third of the engineer cap (task 500, ADR 400, model card 400).
- Precision: ranges and orders of magnitude, one number per claim, with the unit and the period it covers; two significant figures at most.

### regulator

- Register: a competent authority reading against a legal requirement. Exact identifiers, versions, dates, and legal references; every claim traceable to its evidence; defined terms used as the instrument defines them.
- Length: the type's regulator cap, the longest the type supports, since omission is the failure mode (model card 4000); the GPAI form's recommended word counts per field apply when the type carries them.
- Precision: two significant figures for sizes, counts, compute, and energy, following the form's AI Office column; where the reader is a national competent authority rather than the AI Office, the form's range or order of magnitude column applies instead.

### auditor

- Register: a reviewer testing the record against the control. Exact identifiers, dates, owners, and record references; statements of what was done, by whom, and when, not of intent.
- Length: the type's auditor cap, or the regulator cap when the template sets no separate one.
- Precision: numbers as recorded, with their source and the date of the record; no rounding and no derived figures without the inputs beside them.

### data subject

- Register: a person whose data is processed, with no technical or legal vocabulary assumed. Plain layered text: the purpose, the controller, and the rights in the first layer; the full notice as one document as well.
- Length: the type's data subject cap; the first layer short enough to read in full on one screen.
- Precision: plain numbers in everyday units (retention in months, not epochs); no qualifiers such as may, might, some, often, or possible, which WP260 paragraph 13 requires privacy notices to avoid.

### downstream provider

- Register: a builder integrating the model or component into their own system. The integration facts first: modalities, limits, hardware and software required, license category, acceptable use.
- Length: the type's downstream provider cap (model card 2500); the integration fields in full, the training detail by reference.
- Precision: exact integration values (input and output limits, context size, supported formats) and the form's range column for model size and training time, as the GPAI form gives downstream providers.

## Defaults by document type

The default audience per type, from spec Assumption 1: engineer for user documentation,
engineering, and API types, with operator for runbooks and advisories; regulator for Annex IV
and the GPAI form; downstream provider for model cards; executive for system cards; data
subject for privacy notices; auditor for DPIAs. A request that names an audience overrides
the default, and the template's `default_audience` front matter carries the same value.

| Type | Default audience | Reason |
|---|---|---|
| concept | engineer | user documentation is read by the person doing the work |
| task | engineer | user documentation is read by the person doing the work |
| multiple-task procedure | engineer | user documentation is read by the person doing the work |
| reference | engineer | user documentation is read by the person doing the work |
| tutorial | engineer | user documentation is read by the person doing the work |
| troubleshooting | engineer | user documentation is read by the person doing the work |
| release notes | engineer | user documentation is read by the person doing the work |
| architecture decision record | engineer | engineering types are read by the team that builds the system |
| architecture description | engineer | engineering types are read by the team that builds the system |
| design doc or RFC | engineer | engineering types are read by the team that builds the system |
| postmortem | engineer | engineering types are read by the team that builds the system |
| runbook | operator | the reader is on call and wants the action, not the rationale |
| changelog entry | engineer | engineering types are read by the team that builds the system |
| endpoint or field description | engineer | API types are read by the integrating developer |
| error catalog entry | engineer | API types are read by the integrating developer |
| model card | downstream provider | the card's reader integrates the model into their system |
| system card | executive | the card's summary is written for the decision maker; the chapters serve regulators by request |
| Annex IV technical file | regulator | the file exists to answer the authority's request |
| GPAI Model Documentation Form | regulator | the form's columns are the AI Office and national authorities first |
| vulnerability advisory | operator | the reader patches or mitigates and wants the action first |
| disclosure notification | operator | the recipient maintains an affected system and acts under embargo |
| SECURITY.md | engineer | the reader is a researcher or developer reporting a vulnerability |
| privacy notice | data subject | the notice is addressed to the person whose data is processed |
| data protection impact assessment | auditor | the assessment is a record tested against the controller's obligations |
