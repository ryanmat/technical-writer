<!-- template: reference; audience: engineer -->
# Document types and audiences

The 24 document types the skill produces, the seven audiences it writes for, the length caps that pair them, and the marker it writes for a claim it cannot source.

The tables hold for version 0.2.4 of the plugin. The values come from the template front matter under `skills/technical-writer/references/templates/`, which the structural checker reads, so a table here and the checker never disagree. A type's default audience applies when a request names none.

## The 24 document types

One row per type with its domain, the audience it defaults to, and the template file that fixes its structure. Use the table to name a type in a request, or to find the template whose sections a document must carry.

| Type | Domain | Default audience | Template file |
|---|---|---|---|
| Annex IV technical file | AI governance | regulator | `annex-iv-technical-file.md` |
| architecture decision record | engineering | engineer | `architecture-decision-record.md` |
| architecture description | engineering | engineer | `architecture-description.md` |
| changelog entry | engineering | engineer | `changelog-entry.md` |
| concept | user documentation | engineer | `concept.md` |
| data protection impact assessment | privacy | auditor | `data-protection-impact-assessment.md` |
| design doc or RFC | engineering | engineer | `design-doc-or-rfc.md` |
| disclosure notification | security | operator | `disclosure-notification.md` |
| endpoint or field description | API | engineer | `endpoint-description.md` |
| error catalog entry | API | engineer | `error-catalog-entry.md` |
| GPAI Model Documentation Form | AI governance | regulator | `gpai-model-documentation-form.md` |
| model card | AI governance | downstream provider | `model-card.md` |
| multiple-task procedure | user documentation | engineer | `multiple-task-procedure.md` |
| postmortem | engineering | engineer | `postmortem.md` |
| privacy notice | privacy | data subject | `privacy-notice.md` |
| reference | user documentation | engineer | `reference.md` |
| release notes | user documentation | engineer | `release-notes.md` |
| runbook | engineering | operator | `runbook.md` |
| SECURITY.md | security | engineer | `security-md.md` |
| system card | AI governance | executive | `system-card.md` |
| task | user documentation | engineer | `task.md` |
| troubleshooting | user documentation | engineer | `troubleshooting.md` |
| tutorial | user documentation | engineer | `tutorial.md` |
| vulnerability advisory | security | operator | `vulnerability-advisory.md` |

## Length caps by audience

One row per type with the word cap for each audience its template supports, counted outside fenced code blocks; table rows count. A document for an audience the template does not list has no cap. The checker reports `LENGTH_EXCEEDED` when a document passes its cap.

| Type | Caps in words |
|---|---|
| Annex IV technical file | regulator 8000, executive 800 |
| architecture decision record | engineer 1200, executive 400 |
| architecture description | engineer 3000, executive 600 |
| changelog entry | engineer 2000, executive 400 |
| concept | engineer 1500, executive 500 |
| data protection impact assessment | auditor 3500, regulator 3500, executive 500 |
| design doc or RFC | engineer 3000, executive 600 |
| disclosure notification | operator 1200, engineer 1500, executive 300 |
| endpoint or field description | engineer 1500, downstream provider 1500, executive 300 |
| error catalog entry | engineer 800, downstream provider 800, executive 200 |
| GPAI Model Documentation Form | regulator 5000, downstream provider 3000, executive 600 |
| model card | downstream provider 2500, regulator 4000, executive 400 |
| multiple-task procedure | engineer 3000, executive 500 |
| postmortem | engineer 2500, executive 500 |
| privacy notice | data subject 900, regulator 2500, executive 300 |
| reference | engineer 3000, executive 500 |
| release notes | engineer 2000, executive 400 |
| runbook | operator 1500, engineer 1500, executive 400 |
| SECURITY.md | engineer 800, operator 800, executive 200 |
| system card | executive 1000, regulator 6000 |
| task | engineer 1500, executive 500 |
| troubleshooting | engineer 3000, executive 500 |
| tutorial | engineer 3000, executive 500 |
| vulnerability advisory | operator 1200, engineer 1500, executive 300 |

## The seven audiences

One row per audience with the reader it stands for and the precision its numbers carry. The audience names are the only values the `--audience` option of the checker accepts.

| Audience | Reader and register | Precision |
|---|---|---|
| engineer | a peer who builds or integrates the thing; exact identifiers, commands, and versions, the reason given once where it changes what they do | exact values with units; complete version numbers |
| operator | the person running the system when something happens; the action and its expected result, conditions before instructions, no rationale | exact thresholds, commands, and identifiers; a version range only as its exact bounds |
| executive | a decision maker who reads the summary and the consequences; plain words, the decision and the cost first, no procedure | ranges and orders of magnitude, one number per claim with its unit and period; two significant figures at most |
| regulator | a competent authority reading against a legal requirement; exact identifiers, dates, and legal references, every claim traceable to its evidence | two significant figures for sizes, counts, compute, and energy; ranges where the reader is a national authority |
| auditor | a reviewer testing the record against the control; what was done, by whom, and when, not what was intended | numbers as recorded, with their source and date; no derived figure without its inputs beside it |
| data subject | a person whose data is processed, with no technical or legal vocabulary assumed; layered plain text with the purpose, the controller, and the rights first | plain numbers in everyday units; none of the qualifiers may, might, some, often, or possible |
| downstream provider | a builder integrating the model or component into their own system; modalities, limits, hardware, software, license category, and acceptable use first | exact integration values; ranges for model size and training time |

## The evidence marker

The marker for a fact the sources do not give is `[UNVERIFIED: what is missing]`, written inline in place of the claim, with the text after the colon naming the missing fact. The checker lists every marker at the `info` severity and a document with markers still passes; a section whose evidence slot has neither the evidence nor a marker fails with `EVIDENCE_MISSING` at `high`. The Hugging Face `[More Information Needed]` is the upstream equivalent and never appears in a document the skill writes.

```text
- You have the permission to create an alert rule. [UNVERIFIED: the permission or role that grants it]
```
