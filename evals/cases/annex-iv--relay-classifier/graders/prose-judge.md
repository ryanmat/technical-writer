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

An Annex IV technical file written for the regulator audience.

## The template's sections

In the template's order, each with what the template asks of it; the No filler criterion says how a section's job bears on a repeated fact.

- General description of the AI system: Item 1, "A general description of the AI system including" eight sub-points, written as bold fields in the Annex's order: Intended purpose, provider and version (1(a), "its intended purpose, the name of the provider and the version of the system reflecting its relation to previous versions"); Interaction with hardware and software (1(b)); Software and firmware versions (1(c)); Forms of placing on the market (1(d), "such as software packages embedded into hardware, downloads, or APIs"); Hardware (1(e)); Component of products (1(f), photographs or illustrations, or the statement that the system is not a component of a product); User interface and instructions for use (1(g) and 1(h)). Evidence slot: the version, as a number after the word version. A sub-point that does not apply says so in one sentence rather than disappearing, since the authority reads the list against the Annex.
- Elements of the AI system and the development process: Item 2, "A detailed description of the elements of the AI system and of the process for its development". One sentence that names the system's kind and its development path; the content lives in the eight subsections, one per sub-point.
- Development methods and steps: Item 2(a): "the methods and steps performed for the development of the AI system, including, where relevant, recourse to pre-trained systems or tools provided by third parties and how those were used, integrated or modified by the provider." Name every third-party model or tool with its version and what was done to it.
- Design specifications: Item 2(b): the general logic of the system and its algorithms, the key design choices with their rationale and assumptions, the main classification choices, "what the system is designed to optimise for, and the relevance of the different parameters", the expected output and its quality, and the trade-offs made to meet Chapter III, Section 2.
- System architecture and computational resources: Item 2(c): how the software components build on or feed into each other, and "the computational resources used to develop, train, test and validate the AI system", as counts of devices and hours.
- Data requirements and datasheets: Item 2(d): the training data sets with their provenance, scope and main characteristics, how the data was obtained and selected, the labelling procedures and the data cleaning methodologies. Name the datasheet when one exists.
- Human oversight: Item 2(e): the human oversight measures under Article 14 and the technical measures that let deployers interpret the outputs under Article 13(3), point (d). State the measure and the moment it applies.
- Pre-determined changes (optional): Optional, item 2(f), "where applicable": the changes to the system and its performance that are decided in advance, with the technical solutions that keep the system compliant through them. Left out when the system has no pre-determined change.
- Validation and testing: Item 2(g): the validation and testing procedures, the validation and testing data and their main characteristics, the metrics for accuracy, robustness and compliance with Chapter III, Section 2, the potentially discriminatory impacts, and "test logs and all test reports dated and signed by the responsible persons". Evidence slot: a date in ISO form and the word signed, signature, signatory or sign-off in the section. A report whose signature the sources do not show gets the marker naming the signature, never a name supplied by the writer.
- Cybersecurity measures: Item 2(h): "cybersecurity measures put in place", each as a control and what it prevents.
- Monitoring, functioning and control: Item 3: the capabilities and limitations in performance, "including the degrees of accuracy for specific persons or groups of persons on which the system is intended to be used and the overall expected level of accuracy in relation to its intended purpose"; the foreseeable unintended outcomes and sources of risks to health and safety, fundamental rights and discrimination; the human oversight measures, by reference to the subsection above; and the specifications on input data.
- Appropriateness of the performance metrics: Item 4: why the metrics reported under Validation and testing are the right ones for this system and its intended purpose.
- Risk management system: Item 5: the risk management system under Article 9, named by its register or document, with its review cycle and what it holds.
- Changes through the lifecycle: Item 6: the relevant changes the provider made to the system through its lifecycle, one per version, dated.
- Harmonised standards and other technical specifications: Item 7: the harmonised standards applied whose references are published in the Official Journal of the European Union, or, where none were applied, the solutions adopted to meet Chapter III, Section 2 and the other standards and technical specifications applied. Write the statement that no harmonised standard was applied in those words when that is the case.
- EU declaration of conformity: Item 8: the EU declaration of conformity under Article 47, named with its identifier and date and attached or referenced. The copy itself is an attachment, not prose in this section.
- Post-market monitoring: Item 9: the system in place to evaluate the AI system's performance in the post-market phase under Article 72, including the post-market monitoring plan under Article 72(3), named; the sampling, the thresholds and what an alert triggers.

## How to vote

Begin your answer with one line, `Score: N` with N from 1 to 5, or `Score: Unknown`, then the
evidence sentences the rubric asks for.

PASS if the score is 3 or more.
FAIL if the score is below 3, or if the answer is Unknown.
