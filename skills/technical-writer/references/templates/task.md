---
type: task
domain: user documentation
default_audience: engineer
source: Grafana Writers' Toolkit task template (docs/static/templates/task-template.md, grafana/writers-toolkit at 40b4493)
license: Apache-2.0
procedure: true
procedure_section: Steps
h1_pattern: '^(?!(?:The|A|An|How|About|Overview|Introduction)\b)(?!(?!(?:Bring|Ping|Ring|Sing|String|Spring|Swing|Thing|Wing)\b)[A-Z][a-z]*ing\b)[A-Z][a-z]+,? \S'
sections:
  - heading: Before you begin
    level: 2
    evidence:
      pattern: '(?i)(?:\bv?\d+\.\d+(?:\.\d+)?\b|\bpermissions?\b|\blicen[cs]e\b|\brole\b|\bversion\b)'
      missing: a version, permission, or license statement
  - heading: Steps
    level: 2
  - heading: Next steps
    level: 2
    optional: true
length_caps:
  engineer: 1500
  executive: 500
banned_patterns:
  - pattern: '^#{1,6}\s+(?!(?:Bring|Ping|Ring|Sing|String|Spring|Swing|Thing|Wing)\b)[A-Z][a-z]+ing\b'
    rule: task headings start with a bare infinitive, not a gerund
  - pattern: '^#{1,6}\s+Step \d+'
    rule: no Step X in headings
---
# <TASK_TITLE>

A task topic tells one reader how to reach one goal. It has a verb-first title, a one-sentence
summary, the prerequisites, the steps, and what to do next. The front matter above is what
`check_structure.py` enforces; the guidance below is what the skill follows when it writes.

## Title

The title is the H1 and the only H1. From the source template: "The task title is required. The
task title succinctly describes the goal to accomplish, as the result of following the
instructions. The task title contains a verb and an object. For example: Create a dashboard".
Start with a bare infinitive (Create, Configure, Install), never a gerund (Creating) and never
"How to". The `h1_pattern` rejects gerunds, with the same -ing verbs exempted as the heading ban
(Bring, Ping, Ring, Sing, String, Spring, Swing, Thing, Wing), and the common noun-phrase
openers; it cannot tell a verb from a noun, so the writer owns the verb.

## Summary

One sentence directly under the title, before the first section. From the source template: "The
introduction is required. Add an introduction to describe what the task is and why it's important
to the user." and "If you find yourself writing a long introduction, consider creating a concept
topic, and then write a shorter form of that concept in the task introduction." The checker
requires exactly one sentence here; longer context belongs in a concept topic.

## Before you begin

Required. From the source template: "Use it to identify any prerequisite conditions (such as a
specific version, license, or system requirement), permissions, any necessary decision, or tasks
to complete before proceeding." and "Write each prerequisite as a full sentence or sentence
fragment, using parallel structures." The source marks this section optional; this template
requires it because every procedure states its version and its prerequisites before the steps.

Evidence slot: a version, permission, or license statement, taken from a source the user supplied
or the skill read. When the sources do not say which version, permission, or license applies,
write the marker in place of the claim and keep the bullet:

```text
- You have the permission to create <OBJECT>. [UNVERIFIED: the permission or role that grants it]
```

Never invent a version number, a role name, or a license tier to fill the slot.

## Steps

Required. The section the procedure rules apply to.

From the source template: "A stem sentence begins with the word 'To' and includes the name of the
task." "Write steps so that they contain one action, or possibly two related actions, such as
_Copy and paste a value._ or _Save and quit the program._" "If a sentence does not tell the reader
to do something, then it is not a step." "If a step is not required but provides additional
features, you can mark that step as optional and describe when it should be completed."

The procedure rules, each one checked:

- The last sentence before the first step begins with "To" and names the task.
- The first sentence of a step has at most 20 words.
- A step has at most two sentences: the action, and the expected result when the outcome is not
  obvious. Write the result as what the reader sees, in the present tense.
- One action per step. Two only when they are inseparable, such as copy and paste.
- A warning or caution comes before the step it protects, as a bold **Warning:** or **Caution:**
  paragraph, never after the last step. Warnings are reserved for harm to hardware, software, or
  data.

Bold the label text of a UI element, not the element type: click **Save**, not click the **Save**
button. Spell every label exactly as the source gives it. Put commands and identifiers in code
style, and placeholders as `<PLACEHOLDER_NAME>` in code blocks and _placeholder name_ in prose.
A long procedure may subdivide this section with level-three headings; the rules still apply
across all of them.

## Next steps

Optional. Tell the reader what to do once the task is done: the task that follows, how to confirm
the result held, or the reference topic that explains the settings. Do not assume the reader knows
the next step or the outcome.

## Audience

The default audience is the engineer. For an executive, keep the same sections and cut the steps
to the decision points, within the cap. The caps count words outside code blocks.

## Source

Structure and the quoted guidance: Grafana Writers' Toolkit, `docs/static/templates/task-template.md`
and the AI quick reference, from the `grafana/writers-toolkit` repository at commit 40b4493,
Apache License 2.0, Copyright 2025 Grafana Labs. Quoted lines are marked with quotation marks;
the rest of this file is this skill's own text. The procedure rules are this skill's rules, stated
in spec R6, and cite no other standard.
