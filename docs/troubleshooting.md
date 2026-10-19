<!-- template: troubleshooting; audience: engineer -->
# Troubleshoot checker findings

Each entry below is one finding code from the structural checker's report, with what causes it and how to clear it.

The checker, `scripts/check_structure.py`, prints one JSON object with the keys `template`, `audience`, `pass`, `findings`, and `counts`. Each finding carries a `code`, a `severity` (`high`, `medium`, `low`, or `info`), the `line` or `heading` it points at, the `rule` broken, and a `message`. The command exits 0 when the document passes, 1 when it has findings, and 2 when the checker itself did not run. A document passes when it has no `high`, `medium`, or `low` finding; `info` findings are the evidence markers, listed for their owner. The entries are in the order a writer meets them, from the sections down to the words.

## `SECTION_MISSING`

### Symptom

A `high` finding whose message reads `required section 'Steps' is missing`, naming the section the template requires.

### Cause

The document has no heading with the template's exact text at the template's level, or the heading sits inside a fenced code block. A heading spelled differently (`Step` for `Steps`, `Before You Begin` for `Before you begin`) is not matched.

### Resolution

Add the section with the heading text and level the template declares, in its place in the template order, then run the checker again:

```bash
uv run python scripts/check_structure.py --template skills/technical-writer/references/templates/task.md draft.md
```

The command prints a report whose `pass` key reads `true` and whose `findings` list carries only `info` entries.

## `SECTION_ORDER`

### Symptom

A `medium` finding whose message reads `section 'Steps' comes after 'Next steps'; the template puts 'Steps' first`.

### Cause

Two required sections appear in the document in the opposite order from the template.

### Resolution

Move the sections into the template's order. Optional sections do not take part in the check, but each belongs where its template places it.

## `SECTION_UNKNOWN`

### Symptom

A `medium` finding whose message reads `line 41: heading 'Troubleshooting' is not a section of the task template`.

### Cause

A heading at a level the template declares matches none of the template's sections. Headings one level deeper than the deepest the template names are the writer's own subdivisions and are not reported.

### Resolution

Rename the heading to the template's text, demote it one level under the section it belongs to, or move its content into a document of the type that has such a section.

## `H1_COUNT`

### Symptom

A `medium` finding whose message reads `found 2 H1 headings; exactly one is required`, or the same with 0.

### Cause

The document has more than one line starting with a single `#`, or none. Zero H1 together with every section reported missing is the signature of a document wrapped whole in a code fence: the checker reads no headings inside a fence.

### Resolution

Keep one H1 as the title and demote the others. For a fenced document, remove the fence around it.

## `H1_PATTERN`

### Symptom

A `medium` finding whose message reads `line 2: title 'Creating a dashboard' does not match the task template's title pattern`, followed by the pattern.

### Cause

The title breaks the template's title rule. Task titles start with a bare infinitive, so a gerund (`Creating`) or `How to` fails; concept, reference, and troubleshooting titles are noun phrases of at least two words that do not open with an -ing verb, `How to`, `What is`, or `Using`.

### Resolution

Rewrite the title in the template's form: `Create a dashboard` for a task, `Dashboard permissions` for a concept or reference.

## `SUMMARY_MISSING`

### Symptom

A `medium` finding whose message reads `the line under the title has 2 sentences; write exactly one`, or `no summary line follows the title`.

### Cause

The first non-empty line under the H1 is a heading, is empty, or holds more or fewer than one sentence. The checker counts sentence terminators (`.`, `!`, `?`) followed by a space or the end of the line, so an abbreviation such as `e.g.` counts as a terminator.

### Resolution

Write one sentence directly under the title that says what the document is for or what was decided. Put the rest of the introduction in the paragraphs after it.

## `EVIDENCE_MISSING`

### Symptom

A `high` finding whose message reads `section 'Before you begin' lacks a version, permission, or license statement; fill it or write [UNVERIFIED: a version, permission, or license statement]`.

### Cause

A section with an evidence slot contains neither text that matches the slot's pattern nor an `[UNVERIFIED: ...]` marker. The slot is searched across the whole section, subheadings included, but not inside fenced code.

### Resolution

Add the fact from a source you have, or write the marker in place of the claim with the missing fact named after the colon. Never invent the value to fill the slot.

## `EVIDENCE_UNVERIFIED`

### Symptom

An `info` finding whose message reads `[UNVERIFIED: the permission or role that grants it] awaits its owner`, one per marker in the document.

### Cause

The document carries a marker. This is not a defect: the document passes, and the list tells its owner what to supply.

### Resolution

Replace each marker with the fact once a source gives it. Leave the marker in place until then; deleting it to make the document look complete turns an `info` finding into a `high` one.

## `BANNED_PATTERN`

### Symptom

A `low` finding whose message reads `line 17: 'refer to' breaks the rule: write see for cross-references`, with the matched text and the rule.

### Cause

Prose outside code spans and fenced blocks matches one of the global bans (em dash, en dash, `we recommend`, `it is recommended`, `refer to`, `easy`, `easily`, `simple`, `simply`, `quickly`, `currently`, `soon`) or a ban the template adds, such as a gerund heading in a task.

### Resolution

Rewrite the sentence under the rule the message names: a comma, colon, or two sentences for a dash; the requirement and its reason for a recommendation; `see` for a cross-reference; the fact for a subjective or time-bound word.

## `LENGTH_EXCEEDED`

### Symptom

A `medium` finding whose message reads `1620 words outside code blocks; the task template caps engineer documents at 1500`, or the same for one section when the template caps a section.

### Cause

The document, or a capped section, runs past the word cap the template sets for the audience. Words inside fenced code blocks do not count; table rows do.

### Resolution

Cut to the cap for the audience, or split the document into two of the type the content needs. For an executive, keep the summary and the decisions and drop the mechanics; the caps per type and audience are in [Document types and audiences](document-types.md).

## `STEM_MISSING`

### Symptom

A `medium` finding on the procedure section whose message says the paragraph before the first step does not begin with `To` and end in a colon.

### Cause

The procedure section (`Steps` in a task, `Mitigation` in a runbook) has numbered steps with no stem sentence directly before step 1, or the stem shares its paragraph with a warning or a context sentence. The checker accepts a period in place of the colon and nothing else.

### Resolution

Write the stem as its own paragraph, the last before step 1, in the form `To create an alert rule:`. Put any condition or warning in a paragraph before it.

## `STEP_TOO_LONG`

### Symptom

A `medium` finding whose message names the step and reads that its first sentence has more than 20 words.

### Cause

The action sentence of a numbered step runs past 20 words, usually because it explains a field or a default on the way to the action.

### Resolution

Keep the action to one sentence of at most 20 words. Move the field's meaning or default into the result sentence after it, once, and never into a paragraph before the steps.

## `STEP_TOO_MANY_SENTENCES`

### Symptom

A `medium` finding whose message names the step and reads that it has more than 2 sentences.

### Cause

A step carries more than the action and one result sentence: a second action, a note after the result, or a warning written inside the step. In a runbook, a sentence after the expected-output sentence counts the same way.

### Resolution

End the step at its result sentence. Split a second action into its own step, and move a warning into a bold paragraph before the step it protects.

## `WARNING_AFTER_STEP`

### Symptom

A `medium` finding whose message points at a `**Warning:**` or `**Caution:**` paragraph that follows the last numbered step.

### Cause

An admonition sits after the step it protects, where a reader acting step by step meets it too late.

### Resolution

Move the admonition before the step it protects, as its own paragraph. Reserve warnings for harm to hardware, software, or data.

## Exit 2 with an `error` body

### Symptom

The command exits 2 and prints a JSON object with a single `error` key, such as `unknown audience 'reader'; audiences are engineer, operator, executive, regulator, auditor, data subject, downstream provider`, and no `findings`.

### Cause

The checker did not run: the template path does not exist or its front matter fails to load, the document cannot be read, or `--audience` names a value outside the seven. Nothing about the document's structure has been judged.

### Resolution

Fix the path, the audience value, or the template file the message names and run the command again. A template message names the file and the front matter key that failed.

## Related

- [The technical-writer workflow](how-it-works.md)
- [Document types and audiences](document-types.md)
