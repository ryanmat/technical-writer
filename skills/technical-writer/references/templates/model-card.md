---
type: model card
domain: AI governance
default_audience: downstream provider
source: Hugging Face model card template (huggingface_hub src/huggingface_hub/templates/modelcard_template.md at 926f6d8) for the headings; Mitchell et al., Model Cards for Model Reporting (2019), for the disaggregated results requirement
license: Apache-2.0 (Hugging Face, quoted); Mitchell paraphrased, ACM copyright
h1_pattern: '^Model Card for \S'
sections:
  - heading: Model Details
    level: 2
  - heading: Model Description
    level: 3
    evidence:
      pattern: '(?ims)^[^\w\n]*developed by[^:\n]*:[ \t*]*[^\s\[*:].*?^[^\w\n]*license[^:\n]*:[ \t*]*[^\s\[*:]'
      missing: the Developed by and License fields, each with a value
  - heading: Model Sources
    level: 3
    optional: true
  - heading: Uses
    level: 2
  - heading: Direct Use
    level: 3
  - heading: Downstream Use
    level: 3
    optional: true
  - heading: Out-of-Scope Use
    level: 3
  - heading: Bias, Risks, and Limitations
    level: 2
  - heading: Recommendations
    level: 3
  - heading: How to Get Started with the Model
    level: 2
  - heading: Training Details
    level: 2
  - heading: Training Data
    level: 3
  - heading: Training Procedure
    level: 3
  - heading: Preprocessing
    level: 4
    optional: true
  - heading: Training Hyperparameters
    level: 4
  - heading: Speeds, Sizes, Times
    level: 4
    optional: true
  - heading: Evaluation
    level: 2
  - heading: Testing Data, Factors & Metrics
    level: 3
  - heading: Testing Data
    level: 4
  - heading: Factors
    level: 4
  - heading: Metrics
    level: 4
  - heading: Results
    level: 3
    evidence:
      pattern: '(?m)^\|[^\n]+\|[ \t]*\n\|[ \t:|-]+\|'
      missing: a results table disaggregated by the factors named under Factors
  - heading: Summary
    level: 4
  - heading: Model Examination
    level: 2
    optional: true
  - heading: Environmental Impact
    level: 2
    evidence:
      pattern: '(?im)^[^\w\n]*carbon emitted[^:\n]*:[^\n\[]*\d'
      missing: the carbon emitted, as a number in grams of CO2eq
  - heading: Technical Specifications
    level: 2
    optional: true
  - heading: Model Architecture and Objective
    level: 3
    optional: true
  - heading: Compute Infrastructure
    level: 3
    optional: true
  - heading: Hardware
    level: 4
    optional: true
  - heading: Software
    level: 4
    optional: true
  - heading: Citation
    level: 2
    optional: true
  - heading: Glossary
    level: 2
    optional: true
  - heading: More Information
    level: 2
    optional: true
  - heading: Model Card Authors
    level: 2
    optional: true
  - heading: Model Card Contact
    level: 2
    evidence:
      pattern: '[\w.+-]+@[\w-]+\.[\w.-]+|https?://\S+'
      missing: an email address or URL for questions about the model
length_caps:
  downstream provider: 2500
  regulator: 4000
  executive: 400
banned_patterns:
  - pattern: '\[More Information Needed\]'
    rule: 'write [UNVERIFIED: what is missing], never the upstream [More Information Needed]'
---
# Model Card for <MODEL_NAME>

A model card tells the people who deploy, audit, or are affected by a model what it is, what it
is for, how it was trained, how it performs across the groups and conditions that matter, and
whom to ask. The headings are the Hugging Face template's, verbatim and in its order; the
requirement that results be broken down by factor is Mitchell's. The front matter above is what
`check_structure.py` enforces, at every heading level the template declares, so a heading at
levels two to four that the list does not name is a finding.

## Markers

One marker for every unfillable slot: `[UNVERIFIED: what is missing]`. The upstream template
defaults every unfilled field to `[More Information Needed]`; that string is the upstream
equivalent of this skill's marker and is never written in a card this skill produces. The
checker bans it.

## Title

`# Model Card for <MODEL_NAME>`, the H1 and the only H1, followed by one sentence that says
what the model does and for whom.

## Optional headings

The upstream template writes `[optional]` in the heading text of the sections it does not
require. This template drops the tag from the heading and marks the section optional in the
front matter, so a card's headings read clean. Optional: Model Sources, Downstream Use,
Preprocessing, Speeds Sizes Times, Model Examination, Technical Specifications and its
children, Citation, Glossary, More Information, Model Card Authors. Every other heading is
required.

## Model Details

### Model Description

The upstream fields, as a bulleted list with the field name in bold: Developed by; Funded by
(optional); Shared by (optional); Model type; Language(s) (NLP); License; Finetuned from model
(optional). Evidence slot: the Developed by and License fields, each with a value after its
colon, filled from a source or marked.

### Model Sources

Optional. Repository; Paper (optional); Demo (optional).

## Uses

### Direct Use

The use the model was built for, as a sentence a downstream provider can check their own use
against.

### Downstream Use

Optional. Uses after fine-tuning or inside a larger system.

### Out-of-Scope Use

Required. What the model must not be used for and what it was not evaluated on. Mitchell's
primary intended users and out-of-scope use cases land here and in Direct Use.

## Bias, Risks, and Limitations

Required. The technical and the sociotechnical limits: where the model performs worse, which
groups or conditions were not evaluated, and what a wrong output costs. Point at the Results
table for every claim about performance.

### Recommendations

Required. What the deployer does about each limit above: thresholds, human review, excluded
inputs, release checks. State the action, not a wish.

## How to Get Started with the Model

Required. A code block that loads the model at a named revision and runs one example.

## Training Details

### Training Data

The data's source, period, size, labeling, and the removal of identifiers. Mitchell allows
less here than under evaluation data when the detail cannot be given; give the distribution
over the factors at least.

### Training Procedure

#### Preprocessing

Optional.

#### Training Hyperparameters

Required. Training regime (precision), epochs, learning rate, batch size, and whatever else the
run log records.

#### Speeds, Sizes, Times

Optional.

## Evaluation

### Testing Data, Factors & Metrics

#### Testing Data

The held-out data and its relation to the training data.

#### Factors

The groups, conditions, or attributes the results are broken down by. Name them here exactly as
the Results table's columns name them.

#### Metrics

The metrics and why they reflect the model's effect in use; decision thresholds when there are
any.

### Results

Required. A Markdown table broken down by the factors named above, with the unitary results
(each factor alone) or the intersectional results (each pair) and the all-up row. Evidence
slot: the table. When the evaluation report gives no breakdown, write the all-up numbers and the
marker for the breakdown.

#### Summary

Required. The overall result and the weakest cell, in two sentences.

## Model Examination

Optional. Interpretability work.

## Environmental Impact

Required. The upstream fields: Hardware Type; Hours used; Cloud Provider; Compute Region;
Carbon Emitted (grams of CO2eq). Evidence slot: the carbon figure as a number after the field's
colon. When the sources
give hardware and hours but no carbon figure, do not estimate it; write the marker on the
Carbon Emitted line.

## Technical Specifications

Optional. Model Architecture and Objective; Compute Infrastructure with Hardware and Software.

## Citation

Optional. BibTeX and APA.

## Glossary

Optional.

## More Information

Optional.

## Model Card Authors

Optional.

## Model Card Contact

Required. Evidence slot: an email address or a URL where questions about the model are
answered.

## Audience

The default audience is the downstream provider, who integrates the model and needs every
section. A regulator gets the same sections with exact identifiers, versions, dates, and two
significant figures on every number. An executive gets the title, Model Description, Direct
Use, Out-of-Scope Use, Bias, Risks, and Limitations with Recommendations, and the Results
summary, within the cap. The caps count words outside code blocks.

## Source

Headings, their order, and the field names: Hugging Face `huggingface_hub`,
`src/huggingface_hub/templates/modelcard_template.md` at commit 926f6d8, Apache License 2.0.
The disaggregated results requirement and the intended-use framing are paraphrased from
Mitchell et al., Model Cards for Model Reporting, 2019 (ACM copyright; no prose lifted). The
rest of this file is this skill's own text.
