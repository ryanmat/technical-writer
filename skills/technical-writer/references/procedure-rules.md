# Procedure rules

Rules for numbered steps (spec R6). They bind the task and multiple-task procedure templates
and apply to any numbered procedure in any other type: the steps of a runbook, a tutorial, or
a troubleshooting topic. `scripts/check_structure.py` enforces four of them over every section a
template names as its `procedure_section`, one Steps section in a task and each task section
in a multiple-task procedure; the rest are checked by hand against `checklists.md`. The style rules in `style-rules.md` apply to every sentence here as well.

## The stem sentence

A procedure opens with one sentence that begins with To and names the goal, placed directly
before the first step. From the Grafana task template: "A stem sentence begins with the word
'To' and includes the name of the task." Write it as a sentence that ends in a colon, as in:
To create an alert rule:. A paragraph of context may come before it, but the stem is its own
paragraph, the last before step 1, and a warning between the stem and step 1 does not displace
it. The checker reads the paragraph before the first step as the stem: it must begin with To
and end in a colon or a period (the Grafana template's own stem is a full sentence, "To create
an alert rule, complete the following steps."); a context sentence in the same paragraph as the
stem is a `STEM_MISSING` finding.

## One action per step

Each step tells the reader to do one thing. From the Grafana task template: "Write steps so
that they contain one action, or possibly two related actions, such as _Copy and paste a
value._ or _Save and quit the program._" Two actions share a step only when the reader cannot
do one without the other. A sentence that does not tell the reader to do something is not a
step; from the same template: "If a sentence does not tell the reader to do something, then
it is not a step." Context goes in the introduction, the result goes in the result sentence,
and a decision the reader must make goes in Before you begin.

## Step length

The first sentence of a step, the action, has at most 20 words. Words are counted outside
inline code, with each code span counted as one word, so a long command does not break the
cap. When an action does not fit in 20 words, it is two steps, or the explanatory words
belong in the introduction. A step has at most two sentences: the action and, when the
outcome is not obvious, the expected result.

## Expected results

After any step whose outcome the reader cannot predict, state what they see: the page that
opens, the message the command prints, the state the status column shows. The result is the
step's second sentence, in the present tense, and it names the exact text or value where the
reader has to compare against something. A step whose result is obvious (Click **Save**) has
no result sentence.

## Prerequisites before the steps

Everything the reader needs before step 1 goes in the Before you begin section, which comes
before the Steps section in every procedure template: the version or edition, the permission
or role, the license, the decision to make, and any task to finish first. From the Grafana
task template: "Write each prerequisite as a full sentence or sentence fragment, using
parallel structures." The template's evidence slot requires a version, permission, or
license statement there, so a reader can tell before starting whether the procedure applies.

## Warnings before the step

A warning or caution is placed before the step it protects, never after it, and never after
the last step. Warnings are reserved for harm to hardware, software, or data, and a caution
shares that reservation; everything else is a note or belongs in the step. Write the
admonition as a paragraph that opens with bold Warning or Caution, optionally inside a
blockquote, so the checker and the reader both find it.

## Optional steps

From the Grafana task template: "If a step is not required but provides additional features,
you can mark that step as optional and describe when it should be completed." Open the step
with Optional: and then the action, and say in the result sentence or the introduction what
the reader gains by doing it. A procedure whose steps are mostly optional is a reference topic
or a set of separate tasks, not one procedure.

## The title and the headings

The title is a bare infinitive with its object (Create a dashboard), never a gerund and never
How to. Subheadings inside the Steps section, when a long procedure needs them, follow the
same rule and never read Step 1 or Step 2. Numbered steps restart at 1 under each subheading.

## What the checker enforces

The checker reads the whole procedure section, subheadings included, and reports one finding
per cause, each at medium severity: `STEM_MISSING` when no sentence before the first step
begins with To; `STEP_TOO_LONG` when a step's first sentence has more than 20 words;
`STEP_TOO_MANY_SENTENCES` when a step has more than two sentences; `WARNING_AFTER_STEP` when a
warning or caution follows the last step. A procedure section with no numbered list raises no
procedure finding, and a section the document never opens is reported as `SECTION_MISSING`.
The expected-result rule, the prerequisite content, and the optional-step form are checked
by hand.
