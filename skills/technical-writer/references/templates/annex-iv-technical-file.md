---
type: Annex IV technical file
domain: AI governance
default_audience: regulator
source: Regulation (EU) 2024/1689 (the AI Act), Annex IV, Technical documentation referred to in Article 11(1), for the nine items as sections and the sub-points of items 1 and 2 as fields and subsections; the text read at artificialintelligenceact.eu/annex/4 on 2026-10-18
license: statutory (EU legislation, quoted)
h1_pattern: '^Technical documentation for \S'
sections:
  - heading: General description of the AI system
    level: 2
    evidence:
      pattern: '(?i)\bversion\b[^\n]{0,60}\b\d+\.\d+'
      missing: the version of the system reflecting its relation to previous versions, item 1(a)
  - heading: Elements of the AI system and the development process
    level: 2
  - heading: Development methods and steps
    level: 3
  - heading: Design specifications
    level: 3
  - heading: System architecture and computational resources
    level: 3
  - heading: Data requirements and datasheets
    level: 3
  - heading: Human oversight
    level: 3
  - heading: Pre-determined changes
    level: 3
    optional: true
  - heading: Validation and testing
    level: 3
    evidence:
      pattern: '(?s)\A(?=.*\b(?:19|20)\d{2}-\d{2}-\d{2}\b)(?=.*(?i:\bsign(?:ed|ature|atory|-off)\b))'
      missing: the test logs and test reports dated and signed by the responsible persons, item 2(g)
  - heading: Cybersecurity measures
    level: 3
  - heading: Monitoring, functioning and control
    level: 2
  - heading: Appropriateness of the performance metrics
    level: 2
  - heading: Risk management system
    level: 2
  - heading: Changes through the lifecycle
    level: 2
  - heading: Harmonised standards and other technical specifications
    level: 2
  - heading: EU declaration of conformity
    level: 2
  - heading: Post-market monitoring
    level: 2
length_caps:
  regulator: 8000
  executive: 800
---
# Technical documentation for <SYSTEM_NAME> <VERSION>

An Annex IV technical file is the documentation a provider of a high-risk AI system draws up
under Article 11(1) of Regulation (EU) 2024/1689 and hands to a market surveillance authority
on request. Annex IV says the documentation "shall contain at least the following information,
as applicable to the relevant AI system" and lists nine items; this template makes each item a
section, in the Annex's order, with the sub-points of item 1 as bold fields and the sub-points
of item 2 as subsections, since item 2 is where the evidence lives. The front matter above is
what `check_structure.py` enforces, at the two heading levels the template declares, so a
level-two or level-three heading the list does not name is a finding.

## Title

`# Technical documentation for <SYSTEM_NAME> <VERSION>`, the H1 and the only H1, followed by
one sentence naming the regulation, the system, its provider and the request or obligation the
file answers.

## Facts once

Annex IV asks for related facts under several items: the software versions under 1(c) and the
cybersecurity measures under 2(h) both touch image signing; pre-determined changes under 2(f),
the metrics under item 4 and post-market monitoring under item 9 all touch the retrain gate;
human oversight under 2(e) and item 3 touch the same measures. Write each fact in full once, in
the item whose sub-point names it, and elsewhere refer to it by item name in a clause of the
sentence that needs it ("the gate under Pre-determined changes"), never in a pointer sentence
of its own and never as a third statement of the fact. Item 3 names the oversight measures by
reference, as its paragraph below says.

## General description of the AI system

Required. Item 1, "A general description of the AI system including" eight sub-points, written
as bold fields in the Annex's order: Intended purpose, provider and version (1(a), "its
intended purpose, the name of the provider and the version of the system reflecting its
relation to previous versions"); Interaction with hardware and software (1(b)); Software and
firmware versions (1(c)); Forms of placing on the market (1(d), "such as software packages
embedded into hardware, downloads, or APIs"); Hardware (1(e)); Component of products (1(f),
photographs or illustrations, or the statement that the system is not a component of a
product); User interface and instructions for use (1(g) and 1(h)). Evidence slot: the version,
as a number after the word version. A sub-point that does not apply says so in one sentence
rather than disappearing, since the authority reads the list against the Annex.

## Elements of the AI system and the development process

Required. Item 2, "A detailed description of the elements of the AI system and of the process
for its development". One sentence that names the system's kind and its development path; the
content lives in the eight subsections, one per sub-point.

### Development methods and steps

Required. Item 2(a): "the methods and steps performed for the development of the AI system,
including, where relevant, recourse to pre-trained systems or tools provided by third parties
and how those were used, integrated or modified by the provider." Name every third-party model
or tool with its version and what was done to it.

### Design specifications

Required. Item 2(b): the general logic of the system and its algorithms, the key design choices
with their rationale and assumptions, the main classification choices, "what the system is
designed to optimise for, and the relevance of the different parameters", the expected output
and its quality, and the trade-offs made to meet Chapter III, Section 2.

### System architecture and computational resources

Required. Item 2(c): how the software components build on or feed into each other, and "the
computational resources used to develop, train, test and validate the AI system", as counts of
devices and hours.

### Data requirements and datasheets

Required. Item 2(d): the training data sets with their provenance, scope and main
characteristics, how the data was obtained and selected, the labelling procedures and the data
cleaning methodologies. Name the datasheet when one exists.

### Human oversight

Required. Item 2(e): the human oversight measures under Article 14 and the technical measures
that let deployers interpret the outputs under Article 13(3), point (d). State the measure and
the moment it applies.

### Pre-determined changes

Optional, item 2(f), "where applicable": the changes to the system and its performance that
are decided in advance, with the technical solutions that keep the system compliant through
them. Left out when the system has no pre-determined change.

### Validation and testing

Required. Item 2(g): the validation and testing procedures, the validation and testing data
and their main characteristics, the metrics for accuracy, robustness and compliance with
Chapter III, Section 2, the potentially discriminatory impacts, and "test logs and all test
reports dated and signed by the responsible persons". Evidence slot: a date in ISO form and
the word signed, signature, signatory or sign-off in the section. A report whose signature the
sources do not show gets the marker naming the signature, never a name supplied by the writer.

### Cybersecurity measures

Required. Item 2(h): "cybersecurity measures put in place", each as a control and what it
prevents.

## Monitoring, functioning and control

Required. Item 3: the capabilities and limitations in performance, "including the degrees of
accuracy for specific persons or groups of persons on which the system is intended to be used
and the overall expected level of accuracy in relation to its intended purpose"; the
foreseeable unintended outcomes and sources of risks to health and safety, fundamental rights
and discrimination; the human oversight measures, by reference to the subsection above; and
the specifications on input data.

## Appropriateness of the performance metrics

Required. Item 4: why the metrics reported under Validation and testing are the right ones for
this system and its intended purpose.

## Risk management system

Required. Item 5: the risk management system under Article 9, named by its register or
document, with its review cycle and what it holds.

## Changes through the lifecycle

Required. Item 6: the relevant changes the provider made to the system through its lifecycle,
one per version, dated.

## Harmonised standards and other technical specifications

Required. Item 7: the harmonised standards applied whose references are published in the
Official Journal of the European Union, or, where none were applied, the solutions adopted to
meet Chapter III, Section 2 and the other standards and technical specifications applied.
Write the statement that no harmonised standard was applied in those words when that is the
case.

## EU declaration of conformity

Required. Item 8: the EU declaration of conformity under Article 47, named with its identifier
and date and attached or referenced. The copy itself is an attachment, not prose in this
section.

## Post-market monitoring

Required. Item 9: the system in place to evaluate the AI system's performance in the
post-market phase under Article 72, including the post-market monitoring plan under Article
72(3), named; the sampling, the thresholds and what an alert triggers.

## Audience

The default audience is the regulator, the market surveillance authority reading the file
against Annex IV. The regulator rule in `audiences.md` applies: exact identifiers, versions,
dates and legal references; every claim traceable to its evidence; defined terms used as the
regulation defines them (provider, deployer, intended purpose, instructions for use); and two
significant figures on sizes, counts, compute and energy. Omission is the failure mode, so the
regulator cap is the longest the skill supports. An executive gets the title, the General
description and the Monitoring, functioning and control section in plain words within the
executive cap. The caps count words outside code blocks.

## Source

Section names, their order and the quoted phrases: Regulation (EU) 2024/1689, Annex IV,
Technical documentation referred to in Article 11(1), items 1 to 9 and the sub-points of items
1 and 2, read at artificialintelligenceact.eu/annex/4 on 2026-10-18 (an unofficial consolidated
text; EUR-Lex holds the authentic one). EU legislation carries no copyright restriction on
reuse. The field names, the subsection names and the evidence rules are this skill's own text.
