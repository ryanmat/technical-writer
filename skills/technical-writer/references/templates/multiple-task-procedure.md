---
type: multiple-task procedure
domain: user documentation
default_audience: engineer
source: Grafana Writers' Toolkit multiple-tasks template (docs/static/templates/multiple-tasks-template.md, grafana/writers-toolkit at 40b4493)
license: Apache-2.0
procedure: true
procedure_section: a task section
h1_pattern: '^(?!(?:The|A|An|How|About|Overview|Introduction)\b)(?!(?!(?:Bring|Ping|Ring|Sing|String|Spring|Swing|Thing|Wing)\b)[A-Z][a-z]*ing\b)[A-Z][a-z]+,? \S'
sections:
  - heading: Before you begin
    level: 2
    evidence:
      pattern: '(?i)(?:\bv?\d+\.\d+(?:\.\d+)?\b|\bpermissions?\b|\blicen[cs]e\b|\brole\b|\bversion\b)'
      missing: a version, permission, or license statement
  - heading_pattern: '^(?!(?:Before you begin$|Verify\b)).+'
    label: a task section
    level: 2
  - heading_pattern: '^Verify\b'
    label: the Verify section
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
# <PROCEDURE_TITLE>

A multiple-task procedure tells one reader how to reach one goal that takes several tasks in
order. It has a verb-first title, a one-sentence summary, an introduction that lists the tasks,
one Before you begin section for every prerequisite, two or more task sections that are each a
procedure, and a Verify section that proves the goal was reached. The front matter above is
what `check_structure.py` enforces; the guidance below is what the skill follows when it
writes.

## Title

The title is the H1 and the only H1. From the source template: "The task title is required.
The task title succinctly describes the goal to accomplish, as the result of following the
instructions. The task title contains a verb and an object. For example: Create a dashboard".
Name the goal, not the first task: Install and verify the agent, not Install the agent. The
`h1_pattern` is the task template's: a bare infinitive opener, never a gerund (with the same
-ing verbs exempted) and never a noun-phrase opener; it cannot tell a verb from a noun, so the
writer owns the verb.

## Summary and introduction

One sentence directly under the title, before the first section. From the source template:
"The introduction is required. Add an introduction to describe what the task is and why it's
important to the user. What is the goal the user accomplishes with this task and in what
context would it be used?" and "Use this template for procedures that contain a series of
related tasks. If you only have one task, start from the task-template.md file instead." and
"Some procedures, such as configuring a data source, have more than one task to accomplish a
goal. Summarize the overall procedures in the introduction using a numbered list. In the
following example, each step matches a task section heading."

After the summary sentence, list the tasks as a numbered list of links to the task sections,
one per section, in the order the reader performs them. The list sits under the title, not in
a section, so the procedure rules do not read it; its items are the section headings.

## Before you begin

Required, and the only prerequisites section in the document. From the source template: "Use
it to identify any prerequisite conditions (such as a specific version, license, or system
requirement), permissions, any necessary decision, or tasks to complete before proceeding."
and "If you have more than one task, include all prerequisites in this section. For example,
if you have a page that configures a widget and several tasks have prerequisites, list all
prerequisites in the Before you begin section. This way users can have everything they need
before they start performing the tasks."

Evidence slot: a version, permission, or license statement, taken from a source the user
supplied or the skill read. When the sources do not say, write the marker in place of the
claim and keep the bullet:

```text
- You have the permission to install the agent. [UNVERIFIED: the permission or role that grants it]
```

Never invent a version number, a role name, or a license tier to fill the slot.

## Task sections

Required: two or more level-two sections, each named as a bare infinitive for the task it
performs, in the order the introduction lists them. The checker requires at least one and
applies the procedure rules to every one; the writer owns the count. From the source template:
"The stem sentence introduces the steps and provides a visual cue for users who scan content,
and it lets them know that the steps are about to begin. A stem sentence begins with the word
'To' and includes the name of the task." and "Numbered steps provide a directive to the user;
they tell the user explicitly what to do." and "To add context that is directly related to a
step, or to add a code block, indent it underneath the step. Doing so properly scopes the added
information to the step."

The procedure rules, each one checked in every task section:

- The last sentence before the first step begins with "To" and names the task.
- The first sentence of a step has at most 20 words.
- A step has at most two sentences: the action, and the expected result when the outcome is not
  obvious. Write the result as what the reader sees, in the present tense.
- One action per step. Two only when they are inseparable, such as copy and paste.
- A warning or caution comes before the step it protects, as a bold **Warning:** or **Caution:**
  paragraph, never after the last step.

An optional task is a section whose heading begins with Optional: and whose first sentence
says when to perform it. From the source template: "If a task is not required but provides
additional features, you can mark that section as optional and describe when it should be
completed." Every command sits in its own code block under its step, and the expected output
follows any command whose output the reader uses (spec R9).

## Verify

Required: the last section, with a heading that begins with Verify, naming what is verified.
From the source template: "Consider adding a verification section so users can validate the
outcome of the tasks." The source marks this section optional; this template requires it
because a goal that takes several tasks needs one check that the whole of it held. Write it as
a procedure when it has steps; the checker does not apply the procedure rules here, so the
checklist carries them.

## Audience

The default audience is the engineer. For an executive, keep the summary, the task list, and
the Verify section, within the cap. The caps count words outside code blocks.

## Source

Structure and the quoted guidance: Grafana Writers' Toolkit,
`docs/static/templates/multiple-tasks-template.md` and `task-template.md`, from the
`grafana/writers-toolkit` repository at commit 40b4493, Apache License 2.0, Copyright 2025
Grafana Labs. Quoted lines are marked with quotation marks; the rest of this file is this
skill's own text. The procedure rules are this skill's rules, stated in spec R6, and cite no
other standard.
