---
type: concept
domain: user documentation
default_audience: engineer
source: Grafana Writers' Toolkit concept template (docs/static/templates/concept-template.md, grafana/writers-toolkit at 40b4493)
license: Apache-2.0
h1_pattern: '^(?!(?:How to|What is|Using)\b)(?!(?!(?:Alerting|Batching|Billing|Caching|Indexing|Logging|Monitoring|Pricing|Queuing|Routing|Sampling|Scaling|Scheduling|Sharding|Streaming|Throttling|Timing|Tracing)\b)[A-Z][a-z]*ing\b)\S+ \S'
sections:
  - heading_pattern: '^(?!Useful links$).+'
    label: a body section
    level: 2
  - heading: Useful links
    level: 2
    optional: true
length_caps:
  engineer: 1500
  executive: 500
banned_patterns:
  - pattern: '^#{1,6}\s+(?!(?:Alerting|Batching|Billing|Caching|Indexing|Logging|Monitoring|Pricing|Queuing|Routing|Sampling|Scaling|Scheduling|Sharding|Streaming|Throttling|Timing|Tracing)\b)[A-Z][a-z]+ing\b'
    rule: concept headings are noun phrases that do not start with an -ing verb
  - pattern: '^#{1,6}\s+How to\b'
    rule: no How to in headings; a concept explains what and why, a task explains how
---
# <CONCEPT_TITLE>

A concept topic tells one reader what something is and why it matters. It has a noun-phrase
title, a one-sentence summary, body sections the writer names, and an optional list of the
task and reference topics it leads to. The front matter above is what `check_structure.py`
enforces; the guidance below is what the skill follows when it writes.

## Title

The title is the H1 and the only H1. From the source template: "The concept title is required.
Use a noun-based title that includes the name of the product or feature. For example: Alerting
fundamentals." From the Google developer documentation style guide, Headings and titles: "For
a conceptual or non-task-based heading, use a noun phrase that doesn't start with an -ing
verb." The `h1_pattern` rejects a gerund opener, with the -ing nouns a product area is named
by exempted (Alerting, Batching, Billing, Caching, Indexing, Logging, Monitoring, Pricing,
Queuing, Routing, Sampling, Scaling, Scheduling, Sharding, Streaming, Throttling, Timing,
Tracing), and the openers How to, What is, and Using; it requires at least two words. It
cannot tell a verb from a noun, so the writer owns the noun phrase; a heading on another -ing
noun is a finding to read past, or a word to add to the list in every template that carries it.

## Summary

One sentence directly under the title, before the first section. From the source template:
"The introduction is required. Add an introduction to the concept to summarize the purpose or
main point of the feature." The checker requires exactly one sentence here. The paragraphs
that follow it, before the first section, carry the rest of the introduction.

## Body sections

Required: at least one level-two section, named by the writer. From the source template: "Add
sections replacing **Sections** with subtitles for each section. Concept topics or sections
explain what and why. They do not explain how." and "A concept provides an overview and
background information to help users understand a product, interface, or task. Concepts
answer the question "what is it?". Readers learn about features through concepts. Concepts do
not include step-by-step procedures or reference material but often link to those materials."

Name each section as a noun phrase for the part of the concept it explains: the parts, the
lifecycle, the limits, the terms. The heading ban rejects an -ing opener and How to. A
numbered procedure or a field-by-field table belongs in the task or reference topic the
Useful links section points to; when the request wants both, say so in the reply and produce
two documents. Level-three headings under a section are the writer's and are not checked.

Every claim about behavior, defaults, or limits traces to a source the user supplied or the
skill read. The template declares no evidence slot, so a fact the sources do not give is
written as the marker in place of the claim:

```text
A stream holds a message until it expires. [UNVERIFIED: the retention period]
```

Never invent a default, a limit, or a version number to complete an explanation.

## Useful links

Optional. From the source template: "Link out to task or reference topics related to the
concept." List the task that puts the concept to use and the reference that enumerates its
settings, with the exact title of the linked page as the link text. This section comes last.

## Audience

The default audience is the engineer. For an executive, keep the summary and the sections
that state what the thing is and why it exists, and cut the mechanics, within the cap. The
caps count words outside code blocks.

## Source

Structure and the quoted guidance: Grafana Writers' Toolkit,
`docs/static/templates/concept-template.md`, from the `grafana/writers-toolkit` repository at
commit 40b4493, Apache License 2.0, Copyright 2025 Grafana Labs. The noun-phrase heading rule:
Google developer documentation style guide, Headings and titles, CC BY 4.0. Quoted lines are
marked with quotation marks; the rest of this file is this skill's own text.
