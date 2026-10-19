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

A privacy notice written for the data subject audience.

## The template's sections

In the template's order, each with what the template asks of it; the No filler criterion says how a section's job bears on a repeated fact.

- At a glance: The first layer: WP260 paragraph 36 says it "should include the details of the purposes of processing, the identity of controller and a description of the data subject's rights" and "information on the processing which has the most impact on the data subject and processing which could surprise them". One paragraph a reader finishes on one screen, naming who is responsible, what the data is used for, that the reader has rights and where the full notice is. Evidence slot: the word right or rights.
- Who we are: The organisation responsible for the data, by name, and how to reach it and its data protection officer when it has one. Evidence slot: an email address, a URL or a postal address.
- What we use your data for: One bullet per purpose: the data it uses, what it is for, and the legal basis in the GDPR's words (contract, consent, legal obligation, legitimate interest, vital interest, public task). Paragraph 12's good practice example is the model: say what the data does, not that it helps to develop services. Evidence slot: a legal basis named.
- Who we share your data with: The categories of organisation that receive the data and why, and the statement that the data is not sold when that is the case.
- Where your data goes: Where the data is processed, and, for a transfer outside the reader's country or the European Union, the country and the safeguard in plain words; the statement that the data stays where the reader is when that is the case.
- How long we keep your data: One bullet per category of data with its period in days, months or years, or the event that ends it. Evidence slot: a period in everyday units or the criterion. A period the sources do not give is the marker, and so is one the sources call not yet set or under review: the bullet carries `[UNVERIFIED: the retention period for <category>, which <who> has not set]`, never a sentence telling the reader the period is unset.
- Your rights: The rights in plain words: to see, correct, delete, limit, move and object, and to withdraw consent where consent is the basis; how to use them and how long the answer takes.
- How to complain: Who to write to first, and the supervisory authority the reader can complain to, named. Evidence slot: the authority or a complaint contact.
- Where your data comes from (optional): Required when any of the data did not come from the reader (Article 14): the source of each such category.
- Changes to this notice (optional): How the reader learns of a change, and the date of this version.

## How to vote

Begin your answer with one line, `Score: N` with N from 1 to 5, or `Score: Unknown`, then the
evidence sentences the rubric asks for.

PASS if the score is 3 or more.
FAIL if the score is below 3, or if the answer is Unknown.
