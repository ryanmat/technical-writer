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

A GPAI Model Documentation Form written for the regulator audience.

## The template's sections

In the template's order, each with what the template asks of it; the No filler criterion says how a section's job bears on a repeated fact.

- General information: The six identity fields, each as a subsection; no sentence under this heading in the document.
- Legal name for the model provider: Required (AIO, NCAs, DPs). The provider's legal name.
- Model name: Required (AIO, NCAs, DPs). "The unique identifier for the model" and "a list of the names of the publicly available versions".
- Model authenticity (optional): Optional (AIO, NCAs). "Evidence that establishes the provenance and authenticity of the model (e.g. a secure hash if binaries are distributed, or the URL endpoint in the case of a service), where available."
- Release date: Required (AIO, NCAs, DPs). Evidence slot: the date in ISO form.
- Union market release date: Required (AIO, NCAs, DPs). The date the model was placed on the Union market, in ISO form.
- Model dependencies: Required (AIO, NCAs, DPs). The base models for a fine-tuned model; "Otherwise write 'N/A'".
- Model properties: The architecture, the design and the size.
- Model architecture: Required (AIO, NCAs, DPs; 20 words). The architecture in one line.
- Design specifications of the model (optional): Optional (AIO, NCAs; 100 words). The design "including rationale and assumptions made".
- Input modalities (optional): Optional (AIO, DPs). Text, Images, Audio, Video or other, with the maximum input size per modality.
- Output modalities (optional): Optional (AIO, DPs). The same set, with the maximum output size per modality.
- Total model size (exact) (optional): Optional (AIO). The parameter count "recorded with at least two significant figures, e.g. 7.3*10^10 parameters". Evidence slot: a number followed by the word parameters.
- Total model size (range) (optional): Optional (NCAs, DPs). One of the form's ranges: 1-500M, 500M-5B, 5B-15B, 15B-50B, 50B-100B, 100B-500B, 500B-1T, more than 1T parameters.
- Methods of distribution and licenses: Where the model is available and under what license.
- Distribution channels in the Union market (optional): Optional (AIO, NCAs). Every channel through which the model is placed on the Union market.
- Distribution channels available to downstream providers (optional): Optional (DPs). The channels a downstream provider can obtain the model through.
- Model license (optional): Optional (AIO, NCAs). A link to the model license or licenses, "or indicate that no model license exists".
- License type for downstream providers (optional): Optional (DPs). The type or category: open source, restricted, or proprietary.
- Additional assets (optional): Optional (AIO, DPs). Training data, processing code, training code, inference code and evaluation code, each with how it can be accessed and under which license, or the statement that it is not released.
- Use: What the model is for and how it is integrated.
- Acceptable Use Policy: Required (AIO, NCAs, DPs). A link or attachment, or "indicate that none exists".
- Intended uses: Required (AIO, NCAs, DPs; 200 words). The intended uses, and the restricted or prohibited uses.
- Type and nature of AI systems: Required (AIO, NCAs, DPs). The AI systems the model can be integrated into, and those it should not be.
- Technical means for model integration (optional): Optional (DPs; 100 words). How a downstream provider integrates the model.
- Required hardware (optional): Optional (DPs; 100 words). "If not applicable (e.g. model offered via an API), 'N/A' should be entered."
- Required software (optional): Optional (DPs; 100 words). The software a downstream provider needs.
- Training process: How the model was trained and why.
- Design specifications of the training process (optional): Optional (AIO, NCAs; 400 words). The stages, the objectives, the optimiser and schedule, the batch and precision, and the fine-tuning steps.
- Decision rationale (optional): Optional (AIO, NCAs; 200 words). "How and why key design choices were made in model training."
- Information on the data used for training, testing, and validation: The data in the form's nine fields.
- Data type and modality: Required (AIO, NCAs, DPs). Text, Images, Audio, Video or other.
- Data provenance: Required (AIO, NCAs, DPs). The form's categories that apply: web crawling; private non-publicly available datasets obtained from third parties; user data; publicly available datasets; data collected through other means; synthetic data that is not publicly accessible; other.
- How data was obtained and selected (optional): Optional (AIO, NCAs; 300 words). Including annotation, synthetic data generation, and how rights to third-party data were obtained.
- Number of data points (one significant figure) (optional): Optional (NCAs). The count to one significant figure.
- Number of data points (two significant figures) (optional): Optional (AIO). The count to at least two significant figures, in the unit the model counts (tokens, images, hours).
- Scope and main characteristics (optional): Optional (AIO, NCAs; 200 words). Domain, geography, language and modality coverage, with the shares.
- Data curation methodologies: Required (AIO, NCAs, DPs; 300 words). Cleaning, normalisation and augmentation.
- Measures to detect unsuitability of data sources (optional): Optional (AIO, NCAs; 400 words). The measures against illegal content, child sexual abuse material, non-consensual intimate imagery and personal data, named as methods.
- Measures to detect identifiable biases (optional): Optional (AIO, NCAs; 200 words). The methods and what they found.
- Computational resources (during training): Time and compute, in the form's two precisions.
- Training time (range) (optional): Optional (NCAs). Less than 1 month, 1-3 months, 3-6 months, or more than 6 months.
- Training time (days) (optional): Optional (AIO). Wall-clock days and hardware days, one significant figure each.
- Amount of computation used for training (order of magnitude) (optional): Optional (NCAs). The training compute as a power of ten in floating point operations.
- Amount of computation used for training (two significant figures) (optional): Optional (AIO). The training compute to two significant figures in floating point operations.
- Measurement methodology (compute) (optional): Optional (AIO, NCAs). How the compute figure was measured or estimated.
- Energy consumption (during training and inference): The energy and the inference compute, with how each was measured.
- Amount of energy used for training (optional): Optional (AIO, NCAs). In MWh to two significant figures, or N/A "if the compute or hardware provider withholds critical information", in those words and with the reason.
- Measurement methodology (energy) (optional): Optional (AIO, NCAs; 100 words). How the energy figure was measured, or how it would be.
- Benchmarked amount of computation used for inference (optional): Optional (AIO, NCAs). In floating point operations to two significant figures, for the benchmark task named below; the marker when the benchmark has not run.
- Measurement methodology (inference) (optional): Optional (AIO, NCAs). "A description of a computational task (e.g. generating 100000 tokens) and the hardware (e.g. 64 Nvidia A100s)".

## How to vote

Begin your answer with one line, `Score: N` with N from 1 to 5, or `Score: Unknown`, then the
evidence sentences the rubric asks for.

PASS if the score is 3 or more.
FAIL if the score is below 3, or if the answer is Unknown.
