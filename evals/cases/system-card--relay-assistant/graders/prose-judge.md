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

A system card written for the executive audience.

## The template's sections

In the template's order, each with what the template asks of it; the No filler criterion says how a section's job bears on a repeated fact.

- Executive summary: What the system is, the decision the card supports, the headline result of each evaluation chapter with its number, and the open items: every result the sources do not hold and every finding not yet fixed. An executive reads this chapter and the title alone, so it carries every number the decision turns on and nothing the chapters do not also hold.
- Introduction: One sentence on what the system is and how it was built; the facts live in the five subsections, one level down.
- Training data and process: The data sources, the period they cover, their size, the cleaning and the removal of identifiers, the training or fine-tuning steps, and the knowledge cutoff. Evidence slot: the cutoff date, written as a date or a month and year after the word cutoff. The GPAI Model Documentation Form's training data fields ask for the same facts in a table; a system card gives them in prose.
- Crowd workers (optional): Who labeled or rated data for the system, under what terms, and what they were told about the use of their work. Left out when no crowd workers or contracted raters were used, with a sentence to that effect under Training data and process.
- Usage policy and support: What the system may be used for, what it refuses, and where a user gets help or escalates to a person. Name the published policy when there is one.
- Model evaluations: The evaluation areas the card reports, one sentence each, and the rule that kept evaluation data out of training. The chapters below carry the method and the numbers.
- Safeguards: The controls around the model: input and retrieval filters, output classifiers, rate limits, human review, and how each is maintained. State the control and what it blocks, and nothing about how well it worked, which is the Safeguards and harmlessness chapter's result; no sentence previews that chapter.
- External testing (optional): Who tested the system from outside, when, and what they found: the count of findings, how many are fixed, and what remains open.
- Frontier risk evaluations (optional): For a system whose capabilities are measured against a catastrophic-risk threshold (biological, chemical, nuclear, autonomous research and development): the threshold, the method, and the results. Evidence slot: a results table. Left out for a narrow system that no such threshold applies to, with a sentence under Model evaluations saying so.
- Cyber: The conclusion on whether the system can be used to attack and whether it can be attacked, then the results of the offensive capability evaluations and the mitigations. Evidence slot: a results table. When the evaluation ran and its results are held elsewhere, write the marker naming the report in place of the table, never a number the sources do not give.
- Safeguards and harmlessness: How the safeguards performed: harmful request refusal, child safety, mental health, bias and integrity, whichever the system was evaluated on, with the set size beside each result. Evidence slot: a results table.
- Agentic safety (optional): For a system that acts on behalf of a user or reads content a third party controls: malicious use of the agent, and prompt injection through the content it reads, measured with and without the filter. Evidence slot: a results table.
- Alignment assessment: Whether the system does what it was asked and tells the truth: honesty and hallucination, sycophancy, behavior under evaluation awareness, and the automated audit when one ran. Evidence slot: a results table. The card's own review of this assessment and the blind spots of an automated audit belong under Reliability of this assessment.
- Model welfare assessment (optional): For a frontier model deployment: the model's apparent welfare in training and deployment, its perception of its circumstances, and its stated preferences. Left out for a product system built on a contracted model, whose provider's card carries it.
- Capabilities: What the system does well and where it falls short, on the held-out set the chapter names: accuracy, task completion, latency, and the breakdown by the categories that matter to the deployment decision. Evidence slot: a results table.
- Reliability of this assessment: The limits of the evaluations above: languages and populations not covered, held-out sets that share a source with the training data, model judges and how far a hand check agreed with them, and every chapter whose results are missing. The card's self-review and the blind spots of its automated audit are this chapter's content. A reader who trusts the numbers in the chapters above should know from this chapter how far to trust them.
- Appendix (optional): Blocklists, prompt sets, and the long tables the chapters summarize.

## How to vote

Begin your answer with one line, `Score: N` with N from 1 to 5, or `Score: Unknown`, then the
evidence sentences the rubric asks for.

PASS if the score is 3 or more.
FAIL if the score is below 3, or if the answer is Unknown.
