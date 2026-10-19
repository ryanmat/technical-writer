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

A model card written for the downstream provider audience.

## The template's sections

In the template's order, each with what the template asks of it; the No filler criterion says how a section's job bears on a repeated fact.

- Model Details
- Model Description: The upstream fields, as a bulleted list with the field name in bold: Developed by; Funded by (optional); Shared by (optional); Model type; Language(s) (NLP); License; Finetuned from model (optional). Evidence slot: the Developed by and License fields, each with a value after its colon, filled from a source or marked.
- Model Sources (optional): Repository; Paper (optional); Demo (optional).
- Uses
- Direct Use: The use the model was built for, as a sentence a downstream provider can check their own use against.
- Downstream Use (optional): Uses after fine-tuning or inside a larger system.
- Out-of-Scope Use: What the model must not be used for and what it was not evaluated on. Mitchell's primary intended users and out-of-scope use cases land here and in Direct Use.
- Bias, Risks, and Limitations: The technical and the sociotechnical limits: where the model performs worse, which groups or conditions were not evaluated, and what a wrong output costs. Point at the Results table for every claim about performance.
- Recommendations: What the deployer does about each limit above: thresholds, human review, excluded inputs, release checks. State the action, not a wish.
- How to Get Started with the Model: A code block that loads the model at a named revision and runs one example.
- Training Details
- Training Data: The data's source, period, size, labeling, and the removal of identifiers. Mitchell allows less here than under evaluation data when the detail cannot be given; give the distribution over the factors at least.
- Training Procedure
- Preprocessing (optional)
- Training Hyperparameters: Training regime (precision), epochs, learning rate, batch size, and whatever else the run log records.
- Speeds, Sizes, Times (optional)
- Evaluation
- Testing Data, Factors & Metrics
- Testing Data: The held-out data and its relation to the training data.
- Factors: The groups, conditions, or attributes the results are broken down by. Name them here exactly as the Results table's columns name them.
- Metrics: The metrics and why they reflect the model's effect in use; decision thresholds when there are any.
- Results: A Markdown table broken down by the factors named above, with the unitary results (each factor alone) or the intersectional results (each pair) and the all-up row. Evidence slot: the table. When the evaluation report gives no breakdown, write the all-up numbers and the marker for the breakdown.
- Summary: The overall result and the weakest cell, in two sentences.
- Model Examination (optional): Interpretability work.
- Environmental Impact: The upstream fields: Hardware Type; Hours used; Cloud Provider; Compute Region; Carbon Emitted (grams of CO2eq). Evidence slot: the carbon figure as a number after the field's colon. When the sources give hardware and hours but no carbon figure, do not estimate it; write the marker on the Carbon Emitted line.
- Technical Specifications (optional): Model Architecture and Objective; Compute Infrastructure with Hardware and Software.
- Model Architecture and Objective (optional)
- Compute Infrastructure (optional)
- Hardware (optional)
- Software (optional)
- Citation (optional): BibTeX and APA.
- Glossary (optional)
- More Information (optional)
- Model Card Authors (optional)
- Model Card Contact: Evidence slot: an email address or a URL where questions about the model are answered.

## How to vote

Begin your answer with one line, `Score: N` with N from 1 to 5, or `Score: Unknown`, then the
evidence sentences the rubric asks for.

PASS if the score is 3 or more.
FAIL if the score is below 3, or if the answer is Unknown.
