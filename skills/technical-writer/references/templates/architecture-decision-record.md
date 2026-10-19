---
type: architecture decision record
domain: engineering
default_audience: engineer
source: MADR 4.0.0 (adr.github.io/madr) for the sections; Nygard, Documenting Architecture Decisions (2011) for the prose rules; AWS Prescriptive Guidance, ADR process, for the lifecycle
license: MIT or CC0 (MADR, quoted); Nygard and AWS paraphrased, no license
sections:
  - heading: Status
    level: 2
    evidence:
      pattern: '(?is)\b(?:proposed|accepted|rejected|superseded by \d{4})\b.*?\b\d{4}-\d{2}-\d{2}\b'
      missing: a status word (proposed, accepted, rejected, or superseded by NNNN) and the ISO date it took effect
  - heading: Context and Problem Statement
    level: 2
  - heading: Decision Drivers
    level: 2
    optional: true
  - heading: Considered Options
    level: 2
  - heading: Decision Outcome
    level: 2
    evidence:
      pattern: 'Chosen option:'
      missing: a Chosen option line naming the option and the reason
  - heading: Consequences
    level: 2
    optional: true
  - heading: Confirmation
    level: 2
    optional: true
  - heading: Pros and Cons of the Options
    level: 2
    optional: true
  - heading: More Information
    level: 2
    optional: true
length_caps:
  engineer: 1200
  executive: 400
---
# <NNNN>-<short-title-with-dashes>

An architecture decision record captures one decision, the problem it answers, the options
weighed, and what follows from it. The sections and the "Good, because" form are MADR 4.0.0; the
prose rules are Nygard's; the lifecycle is the AWS one. The front matter above is what
`check_structure.py` enforces.

## Title

The H1 and the only H1. MADR names the title "short title, representative of solved problem and
found solution" and numbers the file `NNNN-title-with-dashes.md`. Number the record when the
project numbers its records, and never reuse a number, even for a record later rejected or
superseded. A title the user gives is kept as given.

## Summary

One sentence directly under the title that states the decision. The checker requires exactly one
sentence here.

## Status

Required. One of proposed, accepted, rejected, or superseded by NNNN, with the ISO date the status
took effect, and the decision-makers when the sources name them. MADR 4.0.0 keeps these in YAML
front matter (status, date, decision-makers, consulted, informed); this template keeps them in a
section so the reader and the checker see them in the body.

Evidence slot: the status word and the date. When the sources give no date, write the status and
the marker: `Accepted. [UNVERIFIED: the date the decision was accepted]`.

Lifecycle: an accepted record is immutable. A reversal or a change is a new record whose Status
reads superseded by NNNN on the old one and whose More Information names the record it replaces.

## Context and Problem Statement

Required. Two to three sentences, in prose, that describe the forces at play and the question
being answered. Keep it value-neutral: state facts, constraints, and measurements, not a case for
one option. Every number carries its source or the marker.

## Decision Drivers

Optional. A list of the concerns that decide the question, one per item, each with its source.
A driver the team weighs but the sources do not quantify stays in the list with the marker in
place of the figure.

## Considered Options

Required. A list of the options, one per item, named as the Pros and Cons section names them.

## Decision Outcome

Required. Opens with the MADR line, then the decision in Nygard's active voice:

```text
Chosen option: "<OPTION>", because <THE REASON THE DRIVERS DECIDE IT>.

We will <THE DECISION AS A FULL SENTENCE>.
```

Evidence slot: the `Chosen option:` line. One decision per record; a second decision is a second
record.

## Consequences

Optional, as a level-two section after Decision Outcome. MADR 4.0.0 nests Consequences and
Confirmation under Decision Outcome as level-three headings; this template lifts them one level
so the checker sees them. One item per consequence, each opening "Good, because" or "Bad,
because", as MADR writes them. Include the negative and the
neutral consequences, not only the ones that favor the choice.

## Confirmation

Optional. How the team will know the decision was carried out: the test, the review, or the
measurement that confirms it.

## Pros and Cons of the Options

Optional. One level-three heading per option, in the order of Considered Options, each with
"Good, because" and "Bad, because" items drawn from the sources. An option the sources say
nothing about on a driver gets a "Bad, because" item that says so.

## More Information

Optional. The records this one supersedes or relates to, the review date, and anything the
reader needs that the sections above do not hold.

## Prose rules

- Full sentences throughout; lists only for options, drivers, and consequences.
- The decision in active voice, as "We will".
- The context value-neutral.
- One decision per record. Never reuse a number.
- One to two pages. The caps count words outside code blocks; the executive cap keeps the
  Status, Context, and Decision Outcome and drops the option analysis.

## Source

Sections and the quoted phrases "Chosen option:", "Good, because", and "Bad, because": MADR
4.0.0, adr.github.io/madr, MIT or CC0. Prose rules paraphrased from Michael Nygard, Documenting
Architecture Decisions, 2011. Lifecycle paraphrased from AWS Prescriptive Guidance, ADR process.
The rest of this file is this skill's own text.
