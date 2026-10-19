# Taxonomy

The 24 document types the skill produces and reviews, grouped by domain (spec R2), with the
default audience each takes from [audiences.md](audiences.md) and whether its template has
shipped. The skill names one of these types before it writes anything (spec R1). A template
that reads `shipped` is a file under [templates/](templates/) whose front matter the checker
enforces; one that reads `planned` has a plan step and no file yet.

## Contents

- [Classification](#classification)
- [Supported types](#supported-types)
- [Out of scope by ownership](#out-of-scope-by-ownership)
- [What a template status means](#what-a-template-status-means)
- [Related files](#related-files)

## Classification

Classify by what the reader will do with the page, not by what the request calls it. A
request for "docs for the alert rule feature" is a concept (what it is), a task (how to set
one up), a reference (every field), or several of these as separate pages; it is never one
page that mixes them. The user documentation types follow the Diataxis split that Grafana's
topic types also follow: concept and tutorial for learning, task and multiple-task procedure
for doing, reference for looking up, troubleshooting for repair. The domain types are fixed by
their standards and are recognized by the document the request names or the obligation it
answers.

When two types with different section structures both fit, ask one question and name the two
candidates in it. When a request needs two types, produce two documents or state the split in
the reply before drafting. When the request names a type whose template is `planned`, say so,
and draft under the house style rules only after the user accepts that no template structure
will be enforced.

## Supported types

| Type | Domain | Default audience | Template | Template file or plan step |
|---|---|---|---|---|
| concept | user documentation | engineer | shipped | [templates/concept.md](templates/concept.md) |
| task | user documentation | engineer | shipped | [templates/task.md](templates/task.md) |
| multiple-task procedure | user documentation | engineer | shipped | [templates/multiple-task-procedure.md](templates/multiple-task-procedure.md) |
| reference | user documentation | engineer | shipped | [templates/reference.md](templates/reference.md) |
| tutorial | user documentation | engineer | shipped | [templates/tutorial.md](templates/tutorial.md) |
| troubleshooting | user documentation | engineer | shipped | [templates/troubleshooting.md](templates/troubleshooting.md) |
| release notes | user documentation | engineer | shipped | [templates/release-notes.md](templates/release-notes.md) |
| architecture decision record | engineering | engineer | shipped | [templates/architecture-decision-record.md](templates/architecture-decision-record.md) |
| architecture description | engineering | engineer | shipped | [templates/architecture-description.md](templates/architecture-description.md) |
| design doc or RFC | engineering | engineer | shipped | [templates/design-doc-or-rfc.md](templates/design-doc-or-rfc.md) |
| postmortem | engineering | engineer | shipped | [templates/postmortem.md](templates/postmortem.md) |
| runbook | engineering | operator | shipped | [templates/runbook.md](templates/runbook.md) |
| changelog entry | engineering | engineer | shipped | [templates/changelog-entry.md](templates/changelog-entry.md) |
| endpoint or field description | API | engineer | shipped | [templates/endpoint-description.md](templates/endpoint-description.md) |
| error catalog entry | API | engineer | shipped | [templates/error-catalog-entry.md](templates/error-catalog-entry.md) |
| model card | AI governance | downstream provider | shipped | [templates/model-card.md](templates/model-card.md) |
| system card | AI governance | executive | shipped | [templates/system-card.md](templates/system-card.md) |
| Annex IV technical file | AI governance | regulator | shipped | [templates/annex-iv-technical-file.md](templates/annex-iv-technical-file.md) |
| GPAI Model Documentation Form | AI governance | regulator | shipped | [templates/gpai-model-documentation-form.md](templates/gpai-model-documentation-form.md) |
| vulnerability advisory | security | operator | shipped | [templates/vulnerability-advisory.md](templates/vulnerability-advisory.md) |
| disclosure notification | security | operator | shipped | [templates/disclosure-notification.md](templates/disclosure-notification.md) |
| SECURITY.md | security | engineer | shipped | [templates/security-md.md](templates/security-md.md) |
| privacy notice | privacy | data subject | shipped | [templates/privacy-notice.md](templates/privacy-notice.md) |
| data protection impact assessment | privacy | auditor | shipped | [templates/data-protection-impact-assessment.md](templates/data-protection-impact-assessment.md) |

The disclosure notification type covers both the embargoed notification to affected parties
and the public one; the template carries both forms. The source standard behind each type and
its license are in [attribution.md](attribution.md).

## Out of scope by ownership

Three document kinds belong to other skills. Asked for one of these, the skill names the owner
and stops; it does not draft a competing version.

| Document | Owner | Why |
|---|---|---|
| README | `github` | the canonical README format lives there, with the PR body |
| pull request body | `github` | same skill, same format |
| penetration test or assessment report | `pentest-report` | PTES structure and the findings register live there |

Voice is also owned elsewhere: `humanize` removes AI-tell phrasing, `writing-style-review`
reviews against the house style guide. This skill owns structure and domain convention and names those owners
when asked for a voice pass (spec R11).

## What a template status means

A `shipped` type has a template file whose YAML front matter the checker reads: the required
sections in order, the optional ones, the evidence slot per section, the length caps per
audience, the H1 pattern, and any type-specific banned patterns. The skill loads it before
drafting and runs `scripts/check_structure.py` against the draft when the session can run
scripts. Review mode (spec R8) checks an existing document against the same file.

A `planned` type has a row here and a step in the plan. Until the step lands, the skill can
classify a request as that type and say the template is not yet shipped, and it drafts only on
the user's acceptance, under the rules in [style-rules.md](style-rules.md) and, for numbered
steps, [procedure-rules.md](procedure-rules.md), with no section structure enforced.

## Related files

- [style-rules.md](style-rules.md): the prose rules every type follows, each with its source.
- [procedure-rules.md](procedure-rules.md): the rules for numbered steps.
- [audiences.md](audiences.md): the seven audiences and the defaults table this file repeats.
- [checklists.md](checklists.md): the by-hand checks per shipped template and for every document.
- [attribution.md](attribution.md): every source, its license, and whether it is quoted or paraphrased.
