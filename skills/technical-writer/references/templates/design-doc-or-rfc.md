---
type: design doc or RFC
domain: engineering
default_audience: engineer
source: Design Docs at Google (Ubl, 2020) for the skeleton; PEP 12, Sample reStructuredText PEP Template, for Backwards Compatibility, Security Implications, Rejected Ideas and Open Issues
license: Ubl paraphrased, no license stated; PEP 12 public domain or CC0-1.0-Universal by its Copyright section, the section names quoted
sections:
  - heading: Context and Scope
    level: 2
  - heading: Goals and Non-goals
    level: 2
  - heading: Design
    level: 2
  - heading: Alternatives Considered
    level: 2
    evidence:
      pattern: '(?i)\b(?:rejected|ruled out|not chosen|set aside|declined)\b'
      missing: at least one alternative named as rejected, with the reason it lost to the design
  - heading: Cross-cutting Concerns
    level: 2
    optional: true
  - heading: Backwards Compatibility
    level: 2
  - heading: Security Implications
    level: 2
  - heading: Rejected Ideas
    level: 2
  - heading: Open Issues
    level: 2
    optional: true
length_caps:
  engineer: 3000
  executive: 600
---
# <WHAT_THE_DESIGN_DOES> for <SYSTEM_NAME>

A design doc proposes one change to a system before it is built: the problem, the goals, the
design, the alternatives it beat, and what it costs in compatibility and security. The skeleton
is the Google design doc as Ubl describes it; the three sections that make the trade-offs
explicit, and the open issues, are PEP 12's. The front matter above is what
`check_structure.py` enforces. A document that describes a system as it is, with no change
proposed, is an architecture description; a record of one decision already taken is an
architecture decision record.

## Title

The H1 and the only H1: what the design does, for which system. A title the user gives is
kept as given. A project that numbers its RFCs puts the number first.

## Summary

One sentence directly under the title that says what the design changes and why. The checker
requires exactly one sentence here. Ubl's rule: skip the document when the solution is
unambiguous; a summary that cannot name a trade-off is the sign that no document is needed.

## Context and Scope

Required. The system as it is, the problem, and the boundary of the change: what the design
touches and what it leaves alone. Facts, each with its source or the marker; no argument for
the design yet.

## Goals and Non-goals

Required. The goals as a list of outcomes a reader can check. The non-goals as things that
could reasonably have been goals and were not taken, each with where they went (a later plan,
another system, the consumer) or why not. A negated goal is not a non-goal.

## Design

Required. The change itself, in prose and diagrams, at the level a reviewer needs to judge it:
the parts, the data that moves between them, the states, the failure cases. Do not paste
schemas or code; name them and say what they hold. A value the sources do not give carries the
marker.

## Alternatives Considered

Required. The designs that were weighed and why the chosen one wins, one paragraph per
alternative, each naming it and saying what it was rejected for.

Evidence slot: at least one alternative named as rejected, ruled out, not chosen, set aside or
declined. A design with no alternative to name writes the marker:
`[UNVERIFIED: the alternatives weighed; the sources name none]`.

## Cross-cutting Concerns

Optional. What the design does about the concerns every change in this system faces: logging,
metrics, configuration, privacy, cost, rollout. One short paragraph per concern it touches,
each adding what Design did not say; a concern Design already settled (a default, a field)
is not repeated here, and a section that would only repeat Design is left out.

## Backwards Compatibility

Required. What breaks for an existing caller, a stored record, an export or a configuration,
and what the migration is. "None." is a complete section when nothing breaks; say it.

## Security Implications

Required. The new trust boundaries, credentials, network paths, inputs and resource limits the
design introduces, and what bounds each. "None." is a complete section when the design adds no
new exposure; say it.

## Rejected Ideas

Required. The ideas raised during review and set aside, each with the reason, so that the
next reader does not raise them again. Alternatives Considered holds the designs that competed
with this one; this section holds the suggestions that did not become designs. An idea whose
reason is one already given above names that reason in a clause (for the reason given against
a global policy) rather than restating it, and a non-goal is not a rejected idea.

## Open Issues

Optional. The questions the design leaves for review or for the build, one line each. A
document with none leaves the section out.

## Prose rules

- Prose for the context, the design and the trade-offs; lists only for goals, non-goals and
  cross-cutting concerns.
- Each fact has one home: the problem in Context and Scope, the mechanism and its values in
  Design, the competing designs in Alternatives Considered, what breaks in Backwards
  Compatibility. A later section that needs a fact names its section in a clause and does not
  restate it; no sentence points the reader to another section without adding something, and
  no sentence says that the design serves a goal already listed.
- Backwards Compatibility and Security Implications: one paragraph per thing that breaks or
  per new exposure, never two subjects in one paragraph.
- Every figure carries its source or the marker.
- The design in the present tense as it will work, the alternatives in the past tense as
  what was weighed.
- The caps count words outside code blocks; a mini design doc runs one to three pages, and
  the executive cap keeps the Summary, Goals and Non-goals, Backwards Compatibility and
  Security Implications.

## Source

Skeleton (Context and scope, Goals and non-goals, the design, Alternatives considered,
Cross-cutting concerns) and the rules on non-goals, pasted code and when to skip the document:
Malte Ubl, Design Docs at Google, 2020, paraphrased, no license stated. The section names
Backwards Compatibility, Security Implications, Rejected Ideas and Open Issues: PEP 12, Sample
reStructuredText PEP Template, placed in the public domain or under CC0-1.0-Universal by its
Copyright section, whichever is more permissive. The rest of this file is this skill's own
text.
