---
type: GPAI Model Documentation Form
domain: AI governance
default_audience: regulator
source: Model Documentation Form (European Commission, 2025-07-10), Measure 1.1 of the Transparency Chapter of the General-Purpose AI Code of Practice, for the eight sections, the field names, the audience marks and the recommended word counts
license: statutory (European Commission form, quoted; the DOCX states no license)
h1_pattern: '^Model Documentation Form for \S'
sections:
  - heading: General information
    level: 2
  - {heading: Legal name for the model provider, level: 3}
  - {heading: Model name, level: 3}
  - {heading: Model authenticity, level: 3, optional: true}
  - {heading: Release date, level: 3, evidence: {pattern: '\b(?:19|20)\d{2}-\d{2}-\d{2}\b', missing: the release date in ISO form}}
  - {heading: Union market release date, level: 3}
  - {heading: Model dependencies, level: 3}
  - heading: Model properties
    level: 2
  - {heading: Model architecture, level: 3, max_words: {regulator: 20, downstream provider: 20}}
  - {heading: Design specifications of the model, level: 3, optional: true, max_words: {regulator: 100}}
  - {heading: Input modalities, level: 3, optional: true}
  - {heading: Output modalities, level: 3, optional: true}
  - {heading: Total model size (exact), level: 3, optional: true, evidence: {pattern: '(?i)\d[^\n]{0,40}\bparameters\b', missing: the parameter count with at least two significant figures}}
  - {heading: Total model size (range), level: 3, optional: true}
  - heading: Methods of distribution and licenses
    level: 2
  - {heading: Distribution channels in the Union market, level: 3, optional: true}
  - {heading: Distribution channels available to downstream providers, level: 3, optional: true}
  - {heading: Model license, level: 3, optional: true}
  - {heading: License type for downstream providers, level: 3, optional: true}
  - {heading: Additional assets, level: 3, optional: true}
  - heading: Use
    level: 2
  - {heading: Acceptable Use Policy, level: 3}
  - {heading: Intended uses, level: 3, max_words: {regulator: 200, downstream provider: 200}}
  - {heading: Type and nature of AI systems, level: 3}
  - {heading: Technical means for model integration, level: 3, optional: true, max_words: {downstream provider: 100}}
  - {heading: Required hardware, level: 3, optional: true, max_words: {downstream provider: 100}}
  - {heading: Required software, level: 3, optional: true, max_words: {downstream provider: 100}}
  - heading: Training process
    level: 2
  - {heading: Design specifications of the training process, level: 3, optional: true, max_words: {regulator: 400}}
  - {heading: Decision rationale, level: 3, optional: true, max_words: {regulator: 200}}
  - heading: Information on the data used for training, testing, and validation
    level: 2
  - {heading: Data type and modality, level: 3}
  - {heading: Data provenance, level: 3}
  - {heading: How data was obtained and selected, level: 3, optional: true, max_words: {regulator: 300}}
  - {heading: Number of data points (one significant figure), level: 3, optional: true}
  - {heading: Number of data points (two significant figures), level: 3, optional: true}
  - {heading: Scope and main characteristics, level: 3, optional: true, max_words: {regulator: 200}}
  - {heading: Data curation methodologies, level: 3, max_words: {regulator: 300, downstream provider: 300}}
  - {heading: Measures to detect unsuitability of data sources, level: 3, optional: true, max_words: {regulator: 400}}
  - {heading: Measures to detect identifiable biases, level: 3, optional: true, max_words: {regulator: 200}}
  - heading: Computational resources (during training)
    level: 2
  - {heading: Training time (range), level: 3, optional: true}
  - {heading: Training time (days), level: 3, optional: true}
  - {heading: Amount of computation used for training (order of magnitude), level: 3, optional: true}
  - {heading: Amount of computation used for training (two significant figures), level: 3, optional: true}
  - {heading: Measurement methodology (compute), level: 3, optional: true}
  - heading: Energy consumption (during training and inference)
    level: 2
  - {heading: Amount of energy used for training, level: 3, optional: true}
  - {heading: Measurement methodology (energy), level: 3, optional: true, max_words: {regulator: 100}}
  - {heading: Benchmarked amount of computation used for inference, level: 3, optional: true}
  - {heading: Measurement methodology (inference), level: 3, optional: true}
length_caps:
  regulator: 5000
  downstream provider: 3000
  executive: 600
---
# Model Documentation Form for <MODEL_NAME>

The Model Documentation Form is the European Commission's form for Measure 1.1 of the
Transparency Chapter of the General-Purpose AI Code of Practice: the information a provider
of a general-purpose AI model documents and makes available to the AI Office (AIO), to
national competent authorities (NCAs) on a request through the AI Office, and to downstream
providers (DPs) proactively. The form's eight sections are this template's level-two sections
and its fields are the level-three sections, in the form's order; each field below carries the
form's audience marks and, where the form gives one, its "[Recommended N words]" count as a
`max_words` cap. The front matter above is what `check_structure.py` enforces, at the two
heading levels the template declares, so a heading the list does not name is a finding.

## Markers and N/A

One marker for every unfillable slot: `[UNVERIFIED: what is missing]`. The form allows N/A in
three named places (Model dependencies for a model with no base model, Required hardware for
a model offered through an API, and Amount of energy used for training when the compute or
hardware provider withholds critical information); write N/A there under the form's condition
and the marker everywhere else.

## Title

`# Model Documentation Form for <MODEL_NAME>`, the H1 and the only H1, followed by one
sentence that says what the model is and which reader the document is prepared for, then one
paragraph carrying the form's two header fields, "Date this document was last updated" and
"Document version number", with their values.

## Fields and audiences

A document for the regulator carries every field the form marks for the AI Office, with the
NCA variant of a field (a range or an order of magnitude in place of an exact figure) when the
reader is a national competent authority rather than the AI Office; a document for the
downstream provider carries every field marked DP and none marked only for the authorities,
since the form says those are "only to be made available following a request". The fields the
form marks for all three readers are required here; every other field is optional in the
front matter and required by the audience rule above, so a missing field marked for the
document's reader is a defect the checklist catches.

## Facts once

A figure or a fact has one field: the token count sits under Number of data points and the
training design refers to "the pre-training set" without the count; the fine-tuning set's
authorship sits under How data was obtained and selected and the training design names the
set without the authors; the accelerator sizing sits under Design specifications of the model
and Decision rationale says why a choice was made without restating the size. Write each fact
once in its field and refer to it by field name elsewhere; a fact stated in a third field is
filler. A level-two section heading is followed directly by its first field, with no sentence
previewing the fields.

## General information

Required. The six identity fields, each as a subsection; no sentence under this heading in the document.

### Legal name for the model provider

Required (AIO, NCAs, DPs). The provider's legal name.

### Model name

Required (AIO, NCAs, DPs). "The unique identifier for the model" and "a list of the names of
the publicly available versions".

### Model authenticity

Optional (AIO, NCAs). "Evidence that establishes the provenance and authenticity of the model
(e.g. a secure hash if binaries are distributed, or the URL endpoint in the case of a
service), where available."

### Release date

Required (AIO, NCAs, DPs). Evidence slot: the date in ISO form.

### Union market release date

Required (AIO, NCAs, DPs). The date the model was placed on the Union market, in ISO form.

### Model dependencies

Required (AIO, NCAs, DPs). The base models for a fine-tuned model; "Otherwise write 'N/A'".

## Model properties

Required. The architecture, the design and the size.

### Model architecture

Required (AIO, NCAs, DPs; 20 words). The architecture in one line.

### Design specifications of the model

Optional (AIO, NCAs; 100 words). The design "including rationale and assumptions made".

### Input modalities

Optional (AIO, DPs). Text, Images, Audio, Video or other, with the maximum input size per
modality.

### Output modalities

Optional (AIO, DPs). The same set, with the maximum output size per modality.

### Total model size (exact)

Optional (AIO). The parameter count "recorded with at least two significant figures, e.g.
7.3*10^10 parameters". Evidence slot: a number followed by the word parameters.

### Total model size (range)

Optional (NCAs, DPs). One of the form's ranges: 1-500M, 500M-5B, 5B-15B, 15B-50B, 50B-100B,
100B-500B, 500B-1T, more than 1T parameters.

## Methods of distribution and licenses

Required. Where the model is available and under what license.

### Distribution channels in the Union market

Optional (AIO, NCAs). Every channel through which the model is placed on the Union market.

### Distribution channels available to downstream providers

Optional (DPs). The channels a downstream provider can obtain the model through.

### Model license

Optional (AIO, NCAs). A link to the model license or licenses, "or indicate that no model
license exists".

### License type for downstream providers

Optional (DPs). The type or category: open source, restricted, or proprietary.

### Additional assets

Optional (AIO, DPs). Training data, processing code, training code, inference code and
evaluation code, each with how it can be accessed and under which license, or the statement
that it is not released.

## Use

Required. What the model is for and how it is integrated.

### Acceptable Use Policy

Required (AIO, NCAs, DPs). A link or attachment, or "indicate that none exists".

### Intended uses

Required (AIO, NCAs, DPs; 200 words). The intended uses, and the restricted or prohibited
uses.

### Type and nature of AI systems

Required (AIO, NCAs, DPs). The AI systems the model can be integrated into, and those it
should not be.

### Technical means for model integration

Optional (DPs; 100 words). How a downstream provider integrates the model.

### Required hardware

Optional (DPs; 100 words). "If not applicable (e.g. model offered via an API), 'N/A' should be
entered."

### Required software

Optional (DPs; 100 words). The software a downstream provider needs.

## Training process

Required. How the model was trained and why.

### Design specifications of the training process

Optional (AIO, NCAs; 400 words). The stages, the objectives, the optimiser and schedule, the
batch and precision, and the fine-tuning steps.

### Decision rationale

Optional (AIO, NCAs; 200 words). "How and why key design choices were made in model
training."

## Information on the data used for training, testing, and validation

Required. The data in the form's nine fields.

### Data type and modality

Required (AIO, NCAs, DPs). Text, Images, Audio, Video or other.

### Data provenance

Required (AIO, NCAs, DPs). The form's categories that apply: web crawling; private
non-publicly available datasets obtained from third parties; user data; publicly available
datasets; data collected through other means; synthetic data that is not publicly accessible;
other.

### How data was obtained and selected

Optional (AIO, NCAs; 300 words). Including annotation, synthetic data generation, and how
rights to third-party data were obtained.

### Number of data points (one significant figure)

Optional (NCAs). The count to one significant figure.

### Number of data points (two significant figures)

Optional (AIO). The count to at least two significant figures, in the unit the model counts
(tokens, images, hours).

### Scope and main characteristics

Optional (AIO, NCAs; 200 words). Domain, geography, language and modality coverage, with the
shares.

### Data curation methodologies

Required (AIO, NCAs, DPs; 300 words). Cleaning, normalisation and augmentation.

### Measures to detect unsuitability of data sources

Optional (AIO, NCAs; 400 words). The measures against illegal content, child sexual abuse
material, non-consensual intimate imagery and personal data, named as methods.

### Measures to detect identifiable biases

Optional (AIO, NCAs; 200 words). The methods and what they found.

## Computational resources (during training)

Required. Time and compute, in the form's two precisions.

### Training time (range)

Optional (NCAs). Less than 1 month, 1-3 months, 3-6 months, or more than 6 months.

### Training time (days)

Optional (AIO). Wall-clock days and hardware days, one significant figure each.

### Amount of computation used for training (order of magnitude)

Optional (NCAs). The training compute as a power of ten in floating point operations.

### Amount of computation used for training (two significant figures)

Optional (AIO). The training compute to two significant figures in floating point operations.

### Measurement methodology (compute)

Optional (AIO, NCAs). How the compute figure was measured or estimated.

## Energy consumption (during training and inference)

Required. The energy and the inference compute, with how each was measured.

### Amount of energy used for training

Optional (AIO, NCAs). In MWh to two significant figures, or N/A "if the compute or hardware
provider withholds critical information", in those words and with the reason.

### Measurement methodology (energy)

Optional (AIO, NCAs; 100 words). How the energy figure was measured, or how it would be.

### Benchmarked amount of computation used for inference

Optional (AIO, NCAs). In floating point operations to two significant figures, for the
benchmark task named below; the marker when the benchmark has not run.

### Measurement methodology (inference)

Optional (AIO, NCAs). "A description of a computational task (e.g. generating 100000 tokens)
and the hardware (e.g. 64 Nvidia A100s)".

## Audience

The default audience is the regulator, the AI Office or a national competent authority; the
regulator rule in `audiences.md` applies and the form's own precision column decides the
figure: two significant figures for the AI Office, a range or an order of magnitude for a
national competent authority, written in the field variant that names it. A downstream
provider gets the DP fields with the exact integration values. Each capped field stays within
its recommended word count for the audience; the document caps count words outside code
blocks.

## Source

Section names, field names, audience marks, word counts and the quoted phrases: Model
Documentation Form, European Commission, created 2025-07-09 and modified 2025-07-10, the DOCX
at ec.europa.eu/newsroom/dae/redirection/document/118118, read by the survey from the
document's own XML (superscripts lost in that read are restored here as 10^N). The DOCX states
no license; the form is a Commission document for use under the Code of Practice. The
parenthesised variant names that split one form field by precision, and the audience rule,
are this skill's own text.
