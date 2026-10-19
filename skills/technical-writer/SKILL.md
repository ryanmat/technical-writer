---
name: technical-writer
description: >-
  Produces and reviews technical documents in the structure their audience expects, across
  six domains: user documentation (concept, task, reference, tutorial, troubleshooting,
  release notes), engineering and architecture (decision record, architecture description,
  design doc, postmortem, runbook, changelog entry), API reference text, AI governance
  (model card, system card, Annex IV file, GPAI form), security (advisory, disclosure
  notification, SECURITY.md), and privacy (privacy notice, DPIA). Use it when asked to
  write, draft, structure, or review any of these, or when a request names a document type,
  a standard behind one (MADR, the Hugging Face model card, CVE, CVSS, WP260, the ICO DPIA),
  or an audience for one. Classifies the type before drafting, takes one audience, fills the
  type's template with its evidence slots, marks every claim it cannot source as UNVERIFIED,
  and checks the structure. Not for README or PR bodies or assessment reports, which other
  skills own.
---

# Technical writer

This skill writes and reviews technical documents by template. It owns the structure of each
document type and the conventions of its domain: which sections appear, in what order, what
evidence each section must carry, and which prose rules apply. It does not own voice: AI-tell
removal belongs to `humanize` and house-voice review to `writing-style-review`. When asked for a voice pass, it names the owner.

Every reference this skill relies on is a file beside it. Read them when the workflow says to,
not all at once:

- [references/taxonomy.md](references/taxonomy.md): the 24 types, their domains, defaults, and template status, and the three kinds other skills own.
- [references/audiences.md](references/audiences.md): the seven audiences and what each changes.
- [references/style-rules.md](references/style-rules.md): every prose rule with its source.
- [references/procedure-rules.md](references/procedure-rules.md): the rules for numbered steps.
- [references/checklists.md](references/checklists.md): the by-hand checks per template and for every document.
- [references/attribution.md](references/attribution.md): every source, its license, quoted or paraphrased.
- `references/templates/`: one template per shipped type, YAML front matter plus guidance; the taxonomy table's Template file column names each file.

## Workflow

Work the seven steps in order. Steps 1 and 2 happen before any drafting and their outcome is
stated in the reply.

### 1. Classify

Read the taxonomy and name one document type before writing anything. Classify by what the
reader will do with the page, not by the words in the request. Then apply the first rule
that fits:

- The type is one of the three another skill owns (README and PR body, `github`; penetration test or assessment report, `pentest-report`): name the owner and stop. No partial draft.
- Two types with different section structures both fit: ask one question that names both types and what differs between them. Do not draft until it is answered.
- The request needs two types: produce two documents, or state the split in the reply before drafting. Never one page that mixes types.
- The type is not in the taxonomy: say so, offer the nearest type, and draft under the house style rules only if the user accepts.
- The type is in the taxonomy and its template reads `planned`: say the template has not shipped and draft under the style rules, with no section structure enforced, only if the user accepts.

### 2. Set the audience

Every document has one audience, from the seven:
engineer, operator, executive, regulator, auditor, data subject, downstream provider.
Take the one the request names. When it names none, take the type's default from the
taxonomy table and state the pick in the reply. Read
the audience's entry in `audiences.md` for what it changes: the register the document is
written in, the length cap the template applies, and the precision its numbers carry
(regulators get two significant figures, executives and national authorities get ranges,
downstream providers get the integration values).

### 3. Load the template

Read the template file the taxonomy table's Template file column names for the type, in full;
the file names are not the type names, so take the path from that column rather than guessing
one from the type. The front matter is the structure the checker
enforces: the required sections in order and at their levels, the optional ones, the evidence
slot each section must carry, the length caps per audience, the H1 pattern, and any
type-specific banned patterns. The body is the guidance the writer follows for each section.
Use the section headings exactly as the template spells them, since the headings are what the
checker and the readers' links depend on.

### 4. Gather the sources

Everything the document states about behavior, defaults, UI, permissions, versions, numbers,
or law comes from material the user supplied or a file this session read. Read the sources
before drafting and note which fact each one supports. Sources are read, never modified. The
skill fetches nothing from the network and installs nothing. A supplied source is cited for
what it says; its claims are not promoted to facts about the product because they were
attached. Material under an unknown license is paraphrased, never quoted.

### 5. Draft

Write the document in the template's sections, in order, under the rules in `style-rules.md`
and, for any numbered steps, `procedure-rules.md`. The rules that bite most often:

- One H1, the title, with a one-sentence summary directly under it that says what the document is for or what was decided, never what it contains.
- Lead with the point: every section opens with its conclusion or its action, and context comes after it. A section whose heading asks for a point of its own (a check, a decision, a next step) states that point, never a repeat of an earlier section.
- No filler: no sentence that restates the title or a heading, previews a later section (This procedure has three parts), rounds off a section with its own summary, or repeats under a later heading a fact an earlier section already stated. A required Summary carries only what its template asks for (what the reader built; the overall figure and the weakest group) and nothing the sections above it already said.
- Each fact has one home: the section whose job the template says it is. A later section that needs the fact names that section in a clause (the restart, see Timeline and recovery) and does not restate it; a figure appears once with its unit; and no fact appears in a third section, whatever the sections are. A Lessons learned, Risks, Consequences or Cross-cutting Concerns point is a judgment the earlier sections do not make, not a second telling of their facts.
- Every required section of the loaded template is present with the template's exact heading text at its level, Steps included: numbered steps sit under the Steps heading, never directly under the title or under Before you begin.
- Second person, active voice, present tense; no we in user-facing text.
- Sentence-case headings; task headings are bare infinitives (Create a dashboard), never gerunds, never Step N.
- No em dashes or en dashes anywhere; a comma, a colon, or two sentences instead.
- No we recommend or it is recommended; state the requirement and the reason.
- No easy, simple, quickly, or just; no currently, now, soon, or new outside dated content.
- See for cross-references, not refer to.
- Bold for UI labels, code style for identifiers and paths, `<ANGLE_BRACKET>` placeholders in code and italic placeholders in prose, `example.com` and `CVE-1900-` reserved values in examples.
- Should, may, could, and would avoided in user-facing text; MUST, SHOULD, and MAY kept in normative text.
- A procedure opens with a stem sentence that begins with To and ends in a colon, placed inside the Steps section as its own paragraph, the last before step 1, never above the heading and never in the same paragraph as a warning or a context sentence; the checker accepts a period in place of the colon, and nothing else.
- Each numbered step is one action sentence of at most 20 words, plus one result sentence when the outcome is not obvious. A field's meaning or default goes in that result sentence, once, never in a paragraph before the steps; the paragraph before the stem holds only what the reader must know before acting (a condition, a consequence), and a procedure with nothing of that kind goes straight from the heading to the stem.
- Warnings only for harm to hardware, software, or data, placed before the step they protect.
- A runbook's Mitigation step is one action with its command in its own code block and the expected output as the step's last sentence; nothing follows that sentence inside the step, a condition goes before the action, and a warning is its own paragraph before the numbered step, never inside it.

Evidence is the rule that overrides all others. A claim with no source is written as
`[UNVERIFIED: what is missing]`, the marker naming the fact that is missing, inline where the
claim would stand. An evidence slot the sources cannot fill keeps its heading and carries the
marker; a required section is never dropped and a marker is never deleted to make the document
look complete. The skill never invents a version number, a default, a command flag, a URL, a
metric, a price, or a legal citation. The Hugging Face `[More Information Needed]` is the
upstream equivalent of the marker and never appears.

A user instruction that conflicts with a rule wins; the reply notes which rule was set aside.

### 6. Self-check

Run the checker when the session can run scripts and `uv` is on the path. From the plugin
root, the directory above `skills/`:

```bash
uv run python scripts/check_structure.py --template <template file> --audience "<audience>" <draft.md>
```

Exit 0 means no finding above info. Exit 1 prints a JSON report of findings with a code, a
severity, a line, and a message each; fix every high, medium, and low finding and run it
again. Exit 2 is a JSON error body about the apparatus (an unreadable file, an unknown
audience); report it in prose and continue with the checklist. When the session cannot run
scripts, or `uv` or Python is missing, skip the script, say so, and continue.

Then read the draft once for facts, not structure: for each figure and each claim, find every section that states it, keep it in its home section and cut or shorten the others to a clause that names the home. A fact in three sections is the one defect the checker cannot see and the prose judge counts every time.

Then run the linters, when the session can run scripts, from the same plugin root:

```bash
sh scripts/lint.sh <draft.md>
```

It detects `vale` and `markdownlint` (or `markdownlint-cli2`), runs those present with the
configs under `references/vale/` and `references/markdownlint.jsonc`, and prints one JSON
object: `ran`, `missing`, a `notes` entry for a linter on the path that could not run (Vale
before its `vale sync`, with the command to run), and each tool's exit and output under
`results`. Exit 0 means every tool that ran was clean; exit 1 means one reported findings, so
fix them and run it again; exit 2 is a JSON error body about the apparatus. Report what ran,
what was missing and any note. A missing linter is never an error and never blocks the
document: the by-hand checklist covers what it would have checked.

Then walk `checklists.md`: the section for the document's type, then Structure and Prose and
Evidence for every type.

### 7. Report

Deliver the document as Markdown to the path the user named, else to the working directory,
or as the reply itself when the request asks for the document and nothing else. A document
delivered in the reply is plain Markdown text, never wrapped in a code fence: a fenced
document has no headings to any reader or tool, and the structural checker counts zero H1
and every section missing. The reply also carries, in this order and briefly: the type and audience chosen, with the default noted
when the request named none; every `[UNVERIFIED: ...]` marker left in the document, so the
user knows what to supply; any rule set aside on the user's instruction; which linters were
missing, if any. Close with the composition pointer: a document leaving the organization
gets a `humanize` pass next, and house-voice review is `writing-style-review`. Restate none of
their rules.

## Machine readers

Documents are read by search, summarization, and retrieval systems as well as people. Every
produced document therefore has a single H1, a one-sentence summary directly under it,
prerequisites and version statements before any procedure, the expected output after each
command, and heading text stable enough to serve as a link anchor: no dates, versions, or
trailing punctuation in headings. On request, emit the document's `llms.txt` entry on one
line in the form `[Title](url.md) - description`, with the summary sentence as the
description and the URL the user gives, or the file name when they give none.

## Review mode

Given an existing document, classify it as in step 1, load its template, and check it against
the template, the style rules, and the procedure rules. Return findings ranked by severity,
each naming the location (the line or the heading) and the rule, with the reference file that
carries the rule:

- high: a required section or an evidence slot is missing.
- medium: a structural rule is broken: section order, an unknown section, the H1 count or pattern, the summary line, a length cap, a procedure rule.
- low: a prose rule is broken: a banned pattern or a by-hand rule from the prose checklist.
- info: an `[UNVERIFIED: ...]` marker is present, listed so its owner can fill it.

A document passes with no high, medium, or low finding. Run the checker when the session can,
and read its findings into the ranking; the by-hand checklist supplies the rest. Name each
broken rule in the checker's own words, the `rule` text of its finding (one H1 title;
sections in template order; heading listed in template), and then say what the reader
changes; a paraphrase such as no dashes leaves the reader unable to find the
rule in the reference file. Review mode does not rewrite unless asked. Findings go in the reply, not in a file, unless the user gives a
path. When the document matches no type in the taxonomy, report the classification failure as
the first finding and check the prose rules only.

## Boundaries

- No network access and nothing installed; the skill works from the request, the supplied sources, and these files.
- No state between runs.
- Templates and examples carry no customer names, credentials, or real identifiers; reserved example values only.
- Sources are read, never modified; the output goes where the user says.
- Scripts exit non-zero with a JSON error body; the skill reads it and reports in prose. No condition surfaces an exception to the user.
