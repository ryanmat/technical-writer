---
type: tutorial
domain: user documentation
default_audience: engineer
source: Grafana Writers' Toolkit tutorial template (docs/static/templates/tutorial-template.md, grafana/writers-toolkit at 40b4493)
license: Apache-2.0
procedure: true
procedure_section: a tutorial section
h1_pattern: '^(?!(?:The|A|An|How|About|Overview|Introduction)\b)(?!(?!(?:Bring|Ping|Ring|Sing|String|Spring|Swing|Thing|Wing)\b)[A-Z][a-z]*ing\b)[A-Z][a-z]+,? \S'
sections:
  - heading: Before you begin
    level: 2
    evidence:
      pattern: '(?i)(?:\bv?\d+\.\d+(?:\.\d+)?\b|\bpermissions?\b|\blicen[cs]e\b|\brole\b|\bversion\b)'
      missing: a version, permission, or license statement
  - heading_pattern: '^(?!(?:Before you begin|Summary|Next steps)$).+'
    label: a tutorial section
    level: 2
  - heading: Summary
    level: 2
  - heading: Next steps
    level: 2
length_caps:
  engineer: 3000
  executive: 500
banned_patterns:
  - pattern: '^#{1,6}\s+(?!(?:Bring|Ping|Ring|Sing|String|Spring|Swing|Thing|Wing)\b)[A-Z][a-z]+ing\b'
    rule: task headings start with a bare infinitive, not a gerund
  - pattern: '^#{1,6}\s+Step \d+'
    rule: no Step X in headings
---
# <TUTORIAL_TITLE>

A tutorial takes one learner through one complete, concrete exercise and leaves them with a
working result and the confidence to do the next thing without the page. It has a verb-first
title, a one-sentence summary, an overview, one Before you begin section, two or more task
sections that are each a procedure, a Summary of what the learner built, and Next steps. The
front matter above is what `check_structure.py` enforces; the guidance below is what the
skill follows when it writes.

## Title

The title is the H1 and the only H1. From the source template: "The topic title is required.
The topic title succinctly describes the goal to accomplish, as the result of following the
instructions. The tutorial title contains a verb and an object. For example: Provision
dashboards and data sources". The `h1_pattern` is the task template's: a bare infinitive
opener, never a gerund (with the same -ing verbs exempted) and never a noun-phrase opener; it
cannot tell a verb from a noun, so the writer owns the verb.

## Summary line and overview

One sentence directly under the title, before the first section. From the source template:
"The overview is required. Add an overview to describe what the goal is and why it's important
to the user. You can also add background information -- in what context would it be used?" and
"This section of a tutorial topic can include conceptual material. However, limit conceptual
information to only the tasks at hand." The checker requires exactly one sentence as the
summary; the paragraphs after it carry the overview.

The overview tells the learner what they will have built by the end, in one concrete picture,
before the first task begins. A tutorial is a lesson, not a reference: it names the one path
the learner takes and leaves the options and alternatives to the reference topic it links.
(Diataxis, Tutorials, paraphrased.)

## Before you begin

Required, and the only prerequisites section in the document. From the source template: "Use
it to identify any prerequisite conditions (such as a specific version, license, or system
requirement), permissions, any necessary decision, or tasks to complete before proceeding."
and "If you have more than one task in your tutorial, include all prerequisites in this
section."

Evidence slot: a version, permission, or license statement, taken from a source the user
supplied or the skill read. When the sources do not say, write the marker in place of the
claim and keep the bullet:

```text
- You have Northwind Relay. [UNVERIFIED: the version this tutorial was written against]
```

Never invent a version number, a role name, or a license tier to fill the slot.

## Task sections

Required: two or more level-two sections, each named as a bare infinitive, in the order the
learner performs them, each a procedure. The checker requires at least one and applies the
procedure rules to every one; the writer owns the count. From the source template: "A stem
sentence begins with the word 'To' and includes the name of the task." and "Numbered steps
provide a directive to the user; they tell the user explicitly what to do." and "If a sentence
does not tell the reader to do something, then it is not a step."

The procedure rules, each one checked in every task section:

- The last sentence before the first step begins with "To" and names the task.
- The first sentence of a step has at most 20 words.
- A step has at most two sentences: the action, and the expected result when the outcome is not
  obvious. Write the result as what the reader sees, in the present tense.
- One action per step. Two only when they are inseparable, such as copy and paste.
- A warning or caution comes before the step it protects, as a bold **Warning:** or **Caution:**
  paragraph, never after the last step.

Tutorial rules beyond the procedure rules: every step produces something the learner can see,
and the first task produces a visible result early; the steps work as written on the stated
version, in the order given, every time; the learner is told what they see after each step
that changes the screen or the output; explanation is the minimum the step needs, with the
why deferred to the concept topic the Next steps section links. (Diataxis, Tutorials,
paraphrased.) An optional task is a section whose heading begins with Optional: and whose
first sentence says when to perform it. From the source template: "If a task is not required
but provides additional features, you can mark that section as optional and describe when it
should be completed."

## Summary

Required. From the source template: "To summarize:" followed by one bullet per task performed
and "Now your users can ...". State what the learner built, one bullet per task section in the
same order, then one sentence on what the result lets them do. The source marks this section
optional; this template requires it because a lesson ends by naming what was learned.

## Next steps

Required. From the source template: "Use this section to let the user know about other tasks
they might want to perform." and "Consider completing some other common tasks using this
feature:". List the task topics the learner can do next with what they built, the concept
topic that explains it, and the reference topic that lists its settings, with the exact title
of the linked page as the link text. The source marks this section optional; this template
requires it because the tutorial's purpose is the learner's next move.

## Audience

The default audience is the engineer. For an executive, keep the summary line, the overview,
the Summary, and Next steps, within the cap. The caps count words outside code blocks.

## Source

Structure and the quoted guidance: Grafana Writers' Toolkit,
`docs/static/templates/tutorial-template.md`, from the `grafana/writers-toolkit` repository at
commit 40b4493, Apache License 2.0, Copyright 2025 Grafana Labs. The tutorial rules marked
paraphrased: Diataxis, Tutorials (diataxis.fr), whose license the survey did not record, so no
sentence is reproduced. Quoted lines are marked with quotation marks; the rest of this file
is this skill's own text. The procedure rules are this skill's rules, stated in spec R6, and
cite no other standard.
