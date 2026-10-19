---
type: system card
domain: AI governance
default_audience: executive
source: Claude Haiku 5.5 system card (Anthropic, October 2026) for the chapter order and the chapter names, structure only; the card's prose is not quoted
license: all rights reserved (Anthropic); structure and chapter names only, no sentence reproduced
h1_pattern: '^(?=\S+ \S).+ System Card$'
sections:
  - heading: Executive summary
    level: 2
  - heading: Introduction
    level: 2
  - heading: Training data and process
    level: 3
    evidence:
      pattern: '(?i)\bcut-?off\b[^\n]{0,60}\b(?:19|20)\d{2}\b'
      missing: the training data cutoff date
  - heading: Crowd workers
    level: 3
    optional: true
  - heading: Usage policy and support
    level: 3
  - heading: Model evaluations
    level: 3
  - heading: Safeguards
    level: 3
  - heading: External testing
    level: 3
    optional: true
  - heading: Frontier risk evaluations
    level: 2
    optional: true
    evidence:
      pattern: '(?m)^\|[^\n]+\|[ \t]*\n\|[ \t:|-]+\|'
      missing: a results table for the frontier risk evaluations
  - heading: Cyber
    level: 2
    evidence:
      pattern: '(?m)^\|[^\n]+\|[ \t]*\n\|[ \t:|-]+\|'
      missing: a results table for the cyber evaluations
  - heading: Safeguards and harmlessness
    level: 2
    evidence:
      pattern: '(?m)^\|[^\n]+\|[ \t]*\n\|[ \t:|-]+\|'
      missing: a results table for the harmful request, child safety, mental health, bias or integrity evaluations the system was run through
  - heading: Agentic safety
    level: 2
    optional: true
    evidence:
      pattern: '(?m)^\|[^\n]+\|[ \t]*\n\|[ \t:|-]+\|'
      missing: a results table for the agentic safety evaluations
  - heading: Alignment assessment
    level: 2
    evidence:
      pattern: '(?m)^\|[^\n]+\|[ \t]*\n\|[ \t:|-]+\|'
      missing: a results table for the alignment and honesty evaluations
  - heading: Model welfare assessment
    level: 2
    optional: true
  - heading: Capabilities
    level: 2
    evidence:
      pattern: '(?m)^\|[^\n]+\|[ \t]*\n\|[ \t:|-]+\|'
      missing: a results table for the capability evaluations
  - heading: Reliability of this assessment
    level: 2
  - heading: Appendix
    level: 2
    optional: true
length_caps:
  executive: 1000
  regulator: 6000
---
# <SYSTEM_NAME> System Card

A system card reports the pre-deployment evaluation of a deployed system, a model with its
safeguards, its policies and the product around it, to the people who decide whether to
deploy it and to the regulators who ask how that decision was reached. The chapter order is the
Claude Haiku 5.5 system card's: an executive summary, an introduction that holds the training,
policy and safeguard facts, one chapter per risk domain, each ending in its results, then the
assessment's own limits. The chapter names are the card's; its prose is not reproduced. The
front matter above is what `check_structure.py` enforces, at the two heading levels the
template declares, so a level-two or level-three heading the list does not name is a finding.

## Title

`# <SYSTEM_NAME> System Card`, the H1 and the only H1, with the system's name and version
before the words System Card, followed by one sentence that says what the system does and
what the card reports.

## Chapter shape

An evaluation chapter (Frontier risk evaluations through Capabilities) has one shape: its
conclusion first, one sentence that states the result and what it means for the decision; then
the results table, with the set size beside each number; then, only when the table does not
carry it, one sentence naming the set or the method. No chapter opens with a sentence that
restates its heading or says what the evaluation asked, and no chapter closes by repeating or
rounding off its table. The card's chapters carry their method and results under level-three
headings; this template declares none below the evaluation chapters, so the parts are
paragraphs, and a chapter that needs labels uses bold run-in text. A chapter the system was not
evaluated in is left out when the front matter marks it optional, and carries the marker in
place of its table when it is required, with one sentence naming where the results are held.

## Executive summary

Required. What the system is, the decision the card supports, the headline result of each
evaluation chapter with its number, and the open items: every result the sources do not hold
and every finding not yet fixed. An executive reads this chapter and the title alone, so it
carries every number the decision turns on and nothing the chapters do not also hold.

## Introduction

Required. One sentence on what the system is and how it was built; the facts live in the
five subsections, one level down.

### Training data and process

Required. The data sources, the period they cover, their size, the cleaning and the removal
of identifiers, the training or fine-tuning steps, and the knowledge cutoff. Evidence slot:
the cutoff date, written as a date or a month and year after the word cutoff. The GPAI
Model Documentation Form's training data fields ask for the same facts in a table; a system
card gives them in prose.

### Crowd workers

Optional. Who labeled or rated data for the system, under what terms, and what they were
told about the use of their work. Left out when no crowd workers or contracted raters were
used, with a sentence to that effect under Training data and process.

### Usage policy and support

Required. What the system may be used for, what it refuses, and where a user gets help or
escalates to a person. Name the published policy when there is one.

### Model evaluations

Required. The evaluation areas the card reports, one sentence each, and the rule that kept
evaluation data out of training. The chapters below carry the method and the numbers.

### Safeguards

Required. The controls around the model: input and retrieval filters, output classifiers,
rate limits, human review, and how each is maintained. State the control and what it blocks,
and nothing about how well it worked, which is the Safeguards and harmlessness chapter's
result; no sentence previews that chapter.

### External testing

Optional. Who tested the system from outside, when, and what they found: the count of
findings, how many are fixed, and what remains open.

## Frontier risk evaluations

Optional. For a system whose capabilities are measured against a catastrophic-risk threshold
(biological, chemical, nuclear, autonomous research and development): the threshold, the
method, and the results. Evidence slot: a results table. Left out for a narrow system that no
such threshold applies to, with a sentence under Model evaluations saying so.

## Cyber

Required. The conclusion on whether the system can be used to attack and whether it can be
attacked, then the results of the offensive capability evaluations and the mitigations.
Evidence slot: a results table. When the evaluation ran and its results are held elsewhere,
write the marker naming the report in place of the table, never a number the sources do not
give.

## Safeguards and harmlessness

Required. How the safeguards performed: harmful request refusal, child safety, mental health,
bias and integrity, whichever the system was evaluated on, with the set size beside each
result. Evidence slot: a results table.

## Agentic safety

Optional. For a system that acts on behalf of a user or reads content a third party controls:
malicious use of the agent, and prompt injection through the content it reads, measured with
and without the filter. Evidence slot: a results table.

## Alignment assessment

Required. Whether the system does what it was asked and tells the truth: honesty and
hallucination, sycophancy, behavior under evaluation awareness, and the automated audit when
one ran. Evidence slot: a results table. The card's own review of this assessment and the
blind spots of an automated audit belong under Reliability of this assessment.

## Model welfare assessment

Optional. For a frontier model deployment: the model's apparent welfare in training and
deployment, its perception of its circumstances, and its stated preferences. Left out for a
product system built on a contracted model, whose provider's card carries it.

## Capabilities

Required. What the system does well and where it falls short, on the held-out set the chapter
names: accuracy, task completion, latency, and the breakdown by the categories that matter to
the deployment decision. Evidence slot: a results table.

## Reliability of this assessment

Required. The limits of the evaluations above: languages and populations not covered, held-out
sets that share a source with the training data, model judges and how far a hand check
agreed with them, and every chapter whose results are missing. The card's self-review and
the blind spots of its automated audit are this chapter's content. A reader who trusts the
numbers in the chapters above should know from this chapter how far to trust them.

## Appendix

Optional. Blocklists, prompt sets, and the long tables the chapters summarize.

## Audience

The default audience is the executive, who reads the title, the Executive summary and the
chapter tables to decide on deployment; the whole card fits the executive cap, so every chapter
is one paragraph, one table and one conclusion. A regulator gets the same chapters at length,
with exact identifiers, dates, set sizes and two significant figures on every number, within
the regulator cap. The caps count words outside code blocks.

## Source

Chapter order and chapter names: the Claude Haiku 5.5 system card (Anthropic, October 2026),
the chapters Executive summary, Introduction with its six subsections, RSP evaluations, Cyber,
Safeguards and harmlessness, Agentic safety, Alignment assessment, Model welfare assessment,
Capabilities and Appendix, with Reliability of this assessment lifted from the alignment
chapter's last section to a chapter of its own. RSP evaluations is renamed Frontier risk
evaluations, since the Responsible Scaling Policy is Anthropic's instrument. The card carries
no reuse license, so no sentence of it is reproduced. The rest of this file is this skill's
own text.
