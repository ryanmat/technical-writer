---
type: llm
focus: last_message
weight: 1
---

Verifies: the prose of the final document against evals/rubrics/prose.md (leads with the point, one idea per paragraph, no filler, register fits the audience), scored 1 to 5 by the judge model; the run passes this grader at 3 or more, and run_evals reads the score for the median rule.
Cannot verify: structure, evidence slots, length and banned words; check_structure.py owns those, and a marker's presence is the marker grader's.

# Prose rubric

Score the prose of one finished document from 1 to 5, or answer Unknown. The structural
checker has already ruled on headings, section order, evidence slots, length and banned
words, so none of those count here. This rubric scores four things the checker cannot read:
whether the document leads with the point, whether each paragraph carries one idea, whether
the text is free of filler, and whether the register fits the named audience. The same text
is read by a person and by the judge model, and the two scores must land within one point of
each other.

## What you are given

- The document, as Markdown.
- Its template type and its audience, one of the seven in
  `skills/technical-writer/references/audiences.md`.
- The template's sections, in order, each with what the template asks of it, so that a
  section doing its job can be told from filler.

Read the whole document once before scoring. Score the document as a reader of that audience
would receive it, not as its author.

## The four criteria

### Leads with the point

The first sentence under the title says what the document is for or what was decided, and
each section opens with its conclusion or its action before any explanation. A reader who
stops after the first line of any section still has its main point. A section whose heading
asks for a point of its own (a check, a decision, a next step) and whose text instead repeats
what an earlier section already said fails this criterion, even when every sentence in it is
true: the reader looks for the point and does not find it.

### One idea per paragraph

Each paragraph is about one thing. A paragraph that states a fact, then qualifies it, then
turns to a second subject is two paragraphs written as one. Numbered steps count: one action
per step, with its expected result at most.

### No filler

Every sentence changes what the reader knows or does. Filler is a sentence that restates the
heading or the title, previews the next section, repeats under a later heading a fact an
earlier section already stated, praises the product, hedges a fact the source states plainly,
or rounds off a section with a summary of the section itself. Preamble before the first
instruction is filler unless it names a condition the reader must check first; an explanation
of a field or a control before the steps is preamble, not a condition. Count every filler
sentence; two in one document are two places.

A section is not filler for supplying what the template asks of it, even when that means
stating a fact an earlier section holds: a Summary that tells the whole story in one
paragraph, a Pros and Cons section that repeats a consequence under its option, a recovery
sentence that names the restart the timeline lists. The section list you are given says what
each section asks for. Judge a section on the sentences beyond its job, not on its
existence. A sentence that repeats a fact its own section does not ask for is filler in any
section, and a fact that appears in a third section is filler wherever it stands: no
template asks for a fact three times.

### Register fits the audience

Vocabulary, precision and depth match the named audience as `audiences.md` describes it. An
engineer gets exact identifiers and the reason once where it changes what they do. An operator
gets the action and its result and no rationale. An executive gets the decision, its cost and
its risk in plain words. A regulator or auditor gets the statement the obligation asks for,
traceable to its evidence. A data subject gets no jargon and no qualifiers. A downstream
provider gets the integration facts first. A document written for one audience in the voice of
another fails this criterion even when the facts are right.

An `[UNVERIFIED: ...]` marker is not a prose defect. It is the correct way to leave a fact
the sources do not supply, and a document carrying several markers can still score 5. A
marker whose text is vague (`[UNVERIFIED: details]`) is a register defect, since the reader
cannot tell what to go and find.

## The scale

Score the document as a whole. Start from the weakest criterion, then adjust by one point
at most for the others.

| Score | Meaning |
|---|---|
| 5 | Every criterion holds throughout. A reader of the named audience would use the document as written. |
| 4 | One criterion slips in one place: a paragraph with two ideas, one filler sentence, one section that explains before it states. Nothing a reader has to work around. |
| 3 | One criterion fails in two or more places, or two criteria slip once each. The reader gets what they need but has to dig for it or skip past text. |
| 2 | Two or more criteria fail repeatedly, or the register is wrong for the audience throughout. The reader has to rewrite the document in their head to use it. |
| 1 | The document does not lead with its point anywhere, or most of its text is filler, or it is written for a different audience than the one named. |

## Unknown

Answer Unknown instead of a score when any of these holds, and say which:

- The document is not a finished document: it is a reply about the document, a refusal, a
  partial draft, or a review findings list.
- The audience is not named or is not one of the seven.
- The text is truncated or not readable as Markdown.

Unknown is not a low score. A run that returns Unknown is reported separately and never
counts toward the median.

## How to answer

Give the score, or Unknown with its reason, then one sentence per criterion naming the
strongest evidence for the score: the sentence or paragraph that held or slipped. Quote the
text; do not paraphrase it. Do not suggest rewrites.

## The document

A runbook written for the operator audience.

## The template's sections

In the template's order, each with what the template asks of it; the No filler criterion says how a section's job bears on a repeated fact.

- Alert or trigger: The alert by its exact name, the condition that fires it with its threshold and its duration, and the labels it carries that the steps use. Every page is actionable: a page the operator can do nothing about is a bug in the alert, and the runbook says so rather than inventing a step. Alert on symptoms (what users see), and name the cause in Diagnosis.
- Impact: What users and dependent systems see while the condition lasts, and what is and is not at risk (lost, delayed, duplicated). Two to four sentences. A figure the sources do not give carries the marker.
- Prerequisites: What the operator needs before step 1, one item each: the tool and its version, the access or role, the cluster or environment, the credential. Parallel fragments or sentences.
- Diagnosis: How to find which cause is present: a stem sentence, then numbered steps, each one command or one check with the exact output that points at each cause. The procedure rules apply by hand here; the checker applies them to Mitigation.
- Mitigation: The procedure section: a stem sentence beginning with To and ending in a colon, in its own paragraph directly before step 1 (a warning goes in the paragraph before it), then numbered steps, each one action of at most 20 words, each command in its own code block with the expected output after it, and a condition before the action it governs (If the route state is timed-out, restart the route). A step is at most two sentences: the action, with its condition, and the output sentence after the code block, which is the step's last sentence. Nothing follows the output sentence inside the step: a warning is its own paragraph placed before the numbered step it protects, never inside it; where moved data goes is Rollback's sentence; a value the operator must choose and how is a Prerequisites item or the marker in the action sentence; a pointer to another section is a clause in the action, not a sentence of its own. The steps are ordered from the cheapest reversible action to the most expensive. Automate rote responses: a step the operator always runs the same way belongs in the alert's automation, and the runbook names it as already automated or as the action item that will automate it.
- Verification: The command or the dashboard that shows the condition is gone, with the exact value or text that confirms it and how long to wait for it. The alert resolving is the last check, never the only one.
- Rollback (optional): How to undo a mitigation step that made things worse or that moved data (a drain, a replay, a failover), and where the moved data is until then.
- Escalation: Whom to page or call, in which channel, and the condition or the time after which to do it: the state that means the cause is outside this system, and the wait after the last mitigation step. A time the sources do not give is the marker. The condition is stated here once; a Diagnosis step that reaches it says go to Escalation and does not repeat it.

## How to vote

Begin your answer with one line, `Score: N` with N from 1 to 5, or `Score: Unknown`, then the
evidence sentences the rubric asks for.

PASS if the score is 3 or more.
FAIL if the score is below 3, or if the answer is Unknown.
