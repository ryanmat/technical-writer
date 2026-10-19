---
type: architecture description
domain: engineering
default_audience: engineer
source: arc42 (docs.arc42.org) for the section names, lean form; C4 model diagram checklist (c4model.com/diagrams/checklist) for the diagram evidence slots
license: CC BY-SA 4.0 (arc42), section names only, no prose; CC BY 4.0 (C4), quoted
sections:
  - heading: Introduction and Goals
    level: 2
  - heading: Constraints
    level: 2
    optional: true
  - heading: Context and Scope
    level: 2
    evidence:
      pattern: '(?im)^Diagram:[^\n]*\bkey:[ \t]*\S'
      missing: a diagram statement naming the diagram's title, type and scope, and its key (the C4 diagram checklist)
  - heading: Solution Strategy
    level: 2
  - heading: Building Block View
    level: 2
    evidence:
      pattern: '(?im)^Diagram:[^\n]*\bkey:[ \t]*\S'
      missing: a diagram statement naming the diagram's title, type and scope, and its key (the C4 diagram checklist)
  - heading: Runtime View
    level: 2
    optional: true
    evidence:
      pattern: '(?im)^Diagram:[^\n]*\bkey:[ \t]*\S'
      missing: a diagram statement naming the diagram's title, type and scope, and its key (the C4 diagram checklist)
  - heading: Deployment View
    level: 2
    optional: true
    evidence:
      pattern: '(?im)^Diagram:[^\n]*\bkey:[ \t]*\S'
      missing: a diagram statement naming the diagram's title, type and scope, and its key (the C4 diagram checklist)
  - heading: Crosscutting Concepts
    level: 2
    optional: true
  - heading: Architecture Decisions
    level: 2
    optional: true
  - heading: Quality Requirements
    level: 2
  - heading: Risks and Technical Debt
    level: 2
  - heading: Glossary
    level: 2
    optional: true
length_caps:
  engineer: 3000
  executive: 600
---
# <SYSTEM_NAME> architecture description

An architecture description tells an engineer what a system is for, what it is made of, how its
parts run together, and what quality it has to reach. The section names are arc42's, in the
lean form that keeps the six sections every description needs and makes the other six optional;
each view section carries a diagram statement written to the C4 diagram checklist. The front
matter above is what `check_structure.py` enforces.

## Title

The H1 and the only H1: the system's name followed by "architecture description". A title the
user gives is kept as given.

## Summary

One sentence directly under the title that says what the system does. The checker requires
exactly one sentence here.

## Introduction and Goals

Required. What the system is for, the quality goals in the order the team ranks them (arc42
asks every description to state its quality goals), and the stakeholders who read this
document and what each expects from it. A goal the sources rank but do not quantify is stated
with the marker in place of the figure.

## Constraints

Optional. The decisions made outside this document that the architecture has to respect: the
platform, the languages, the stores, the regulations. Each with its source.

## Context and Scope

Required. The system's boundary: the people and systems it exchanges data with and what crosses
each boundary. The C4 system context diagram belongs here.

Evidence slot: a diagram statement. Every view section carries one, written to the C4 diagram
checklist, which asks of a diagram: "Does the diagram have a title?", "Do you understand the
diagram type?", "Do you understand the scope of the diagram?", "Does the diagram have a key or
legend?", and of its elements and lines: "Does every element have a name?", "Do you understand
the type of every element?", "Does every element have a description?", "Do you understand the
technology choices?", "Does every line have a label describing the intent of the relationship?",
"Does every line have an arrow head?" and "Do you understand the meaning of all acronyms and
abbreviations?" The statement answers the first four in one line:

```text
Diagram: <TITLE>, a C4 <TYPE> diagram scoped to <SCOPE>; key: <WHAT EACH SHAPE, LINE AND COLOR MEANS>.
```

The checker reads a line of the section that opens with `Diagram:` and carries `key:` with text after it; the words diagram and key in ordinary prose fill nothing. When the sources
give no diagram and nothing to draw one from, the section keeps its prose and carries
`[UNVERIFIED: the <TYPE> diagram for this view and its key]`. A drawn diagram (Mermaid,
PlantUML, an image) stands under its statement, never in place of it: the statement is what a
reader without the image, and the checker, can verify.

## Solution Strategy

Required. The few decisions that shape the whole: the technology, the decomposition, and how
the quality goals are reached. One paragraph per decision, each pointing to the record in
Architecture Decisions when one exists.

## Building Block View

Required. The static decomposition: the containers or components, each with its name, its
technology in brackets, and what it does. The C4 container diagram belongs here; a component
diagram per container follows only when the sources describe the components.

Evidence slot: a diagram statement, as in Context and Scope.

## Runtime View

Optional. The scenarios that matter: one numbered or ordered walk-through per scenario,
naming the building blocks it crosses. The C4 dynamic diagram belongs here.

Evidence slot: a diagram statement, as in Context and Scope.

## Deployment View

Optional. Where the building blocks run: the nodes, the instances, the network paths. The C4
deployment diagram belongs here. Sizing figures carry their source or the marker.

Evidence slot: a diagram statement, as in Context and Scope.

## Crosscutting Concepts

Optional. The rules that hold across building blocks: the domain model, security, error
handling, logging, configuration. One short section per concept, never a repeat of a building
block's description.

## Architecture Decisions

Optional. A list of the decisions this description rests on, each a link to its architecture
decision record. A decision with no record is one line here with its date or the marker.

## Quality Requirements

Required. The quality goals from the introduction made testable: for each, the scenario and
the measure, with the measurement that was taken or the marker for one that was not.

## Risks and Technical Debt

Required. What could go wrong and what is already known to be wrong, each with what it costs
and what the team plans to do about it. A list of known problems ranked by the team, never a
list of everything that could happen.

## Glossary

Optional. The domain and technical terms a reader needs, one line each, in the source's
spelling.

## Prose rules

- Every section says what is, not what should be; a plan belongs in a design doc.
- Each fact has one home. Introduction and Goals holds the purpose, the ranked goals and the
  stakeholders; Context and Scope holds the boundary and what crosses it; Solution Strategy
  names the decisions and the quality goal each serves, not the components; Building Block
  View holds each block's technology and job; Runtime View holds the scenarios' steps;
  Deployment View holds the nodes and instance counts; Quality Requirements holds the
  measurements. A later section that needs a fact names the block or the section in a clause
  (the queue adapter, see Building Block View) and does not restate the fact.
- No sentence names the reader of the document, says how many blocks there are before the
  list that shows them, previews a later section, or repeats a marker in prose.
- Runtime View lists only the scenarios the sources describe; a scenario the sources name
  without steps is one line and the marker.
- Every figure (a latency, a count, a size) carries its source or the marker.
- Headings stay as arc42 names them, so a reader who knows arc42 finds each section.
- The caps count words outside code blocks; the executive cap keeps Introduction and Goals,
  Context and Scope, Solution Strategy, Quality Requirements and Risks and Technical Debt.

## Source

Section names: arc42, docs.arc42.org, CC BY-SA 4.0. The names alone are taken; every sentence
in this file is this skill's own, so no ShareAlike obligation is inherited. The C4 diagram
checklist questions are quoted from c4model.com/diagrams/checklist, CC BY 4.0. The rest of this
file is this skill's own text.
