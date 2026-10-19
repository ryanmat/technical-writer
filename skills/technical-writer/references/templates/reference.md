---
type: reference
domain: user documentation
default_audience: engineer
source: Grafana Writers' Toolkit reference template (docs/static/templates/reference-template.md, grafana/writers-toolkit at 40b4493)
license: Apache-2.0
h1_pattern: '^(?!(?:How to|What is|Using)\b)(?!(?!(?:Alerting|Batching|Billing|Caching|Indexing|Logging|Monitoring|Pricing|Queuing|Routing|Sampling|Scaling|Scheduling|Sharding|Streaming|Throttling|Timing|Tracing)\b)[A-Z][a-z]*ing\b)\S+ \S'
sections:
  - heading_pattern: '.+'
    label: the introduction
    level: 1
    evidence:
      pattern: '(?is)\A(?:(?!\n\|).)*?(?:\bv?\d+\.\d+(?:\.\d+)?\b|\bversions?\b|\bas of\b)'
      missing: a version or source statement in the introduction, before the first table
  - heading_pattern: '^(?!API documentation$).+'
    label: a reference section
    level: 2
  - heading: API documentation
    level: 2
    optional: true
length_caps:
  engineer: 3000
  executive: 500
banned_patterns:
  - pattern: '^#{1,6}\s+(?!(?:Alerting|Batching|Billing|Caching|Indexing|Logging|Monitoring|Pricing|Queuing|Routing|Sampling|Scaling|Scheduling|Sharding|Streaming|Throttling|Timing|Tracing)\b)[A-Z][a-z]+ing\b'
    rule: reference headings are noun phrases that do not start with an -ing verb
  - pattern: '^#{1,6}\s+How to\b'
    rule: no How to in headings; a reference lists what there is, a task explains how
---
# <REFERENCE_TITLE>

A reference topic gives one reader every value of one kind to look up: the settings, the
fields, the commands, the codes. It has a noun-phrase title, a one-sentence summary, an
introduction that says which version or source the values come from, sections of tables or
lists the writer names, and an optional API documentation section. The front matter above is
what `check_structure.py` enforces; the guidance below is what the skill follows when it
writes.

## Title

The title is the H1 and the only H1. From the source template: "The reference title is
required. Use a noun-based title." From the Google developer documentation style guide,
Headings and titles: "For a conceptual or non-task-based heading, use a noun phrase that
doesn't start with an -ing verb." The `h1_pattern` rejects a gerund opener, with the -ing
nouns a product area is named by exempted (Alerting, Batching, Billing, Caching, Indexing,
Logging, Monitoring, Pricing, Queuing, Routing, Sampling, Scaling, Scheduling, Sharding,
Streaming, Throttling, Timing, Tracing), and the openers How to, What is, and Using; it
requires at least two words. It cannot tell a verb from a noun, so the writer owns the noun
phrase; the same list sits in the concept and troubleshooting templates.

## Summary and introduction

One sentence directly under the title, before the first section. From the source template:
"The introduction is required. Include reference information, such as extensive tables, lists,
or other information that is used as support for a task. Reference topics are also designed
for API information." and "Often reference topics are linked from _task_ topics, because they
contain information the user needs when performing a task." The checker requires exactly one
sentence as the summary; the paragraphs after it carry the rest of the introduction.

Evidence slot, on the introduction: the version or source the values hold for, stated before
the first table in the document. A table of defaults with no version is a table the reader
cannot trust. The slot accepts a version number, the word version, or as of followed by the
date or release the values hold for, each read from a source the user supplied or the skill
read; a bare sourced from or taken from names no source and does not fill it. When the sources
do not say which version the values hold for, write the marker in the introduction:

```text
The defaults below hold for one release of Northwind Relay. [UNVERIFIED: the version the settings list describes]
```

Never invent a version number to fill the slot.

## Body sections

Required: at least one level-two section, named by the writer for the kind of thing it lists.
From the source template: "Lists of commands or parameters are often organized in reference
topics. The information you need to present will dictate the format." and "If you have a
large list of things to store in a table, then you are probably dealing with reference
information." and "Although you might not need a heading for each table, headings are a way
to chunk information if you have several tables. Headings also make content easy to skim. Use
headings (or introductory paragraphs such as this one) to provide the reader with context
about the information in the table and its use."

Open each section with one sentence saying what the table or list holds and when the reader
uses it. In a table of settings, one row per setting, with the name as the source spells it in
code style, the default, and what it does; a default the sources do not give is the marker in
the cell, never a guess. Sort rows alphabetically unless the source fixes an order the reader
needs. Level-three headings under a section are the writer's and are not checked. A numbered
procedure belongs in the task topic that links here.

## API documentation

Optional. From the source template: "Although API documentation is a reference topic, rather
than a task topic, it has its own guidelines." Use it for the endpoint and field descriptions
that accompany a settings reference; a document that is only an endpoint or field description
is its own type, with its own template. This section comes last.

## Audience

The default audience is the engineer. For an executive, keep the summary, the version
statement, and the table columns that carry decisions (the setting and what it does), within
the cap. The caps count words outside code blocks; table rows count.

## Source

Structure and the quoted guidance: Grafana Writers' Toolkit,
`docs/static/templates/reference-template.md`, from the `grafana/writers-toolkit` repository
at commit 40b4493, Apache License 2.0, Copyright 2025 Grafana Labs. The noun-phrase heading
rule: Google developer documentation style guide, Headings and titles, CC BY 4.0. Quoted lines
are marked with quotation marks; the rest of this file is this skill's own text. The version
slot is this skill's rule, stated in spec R9, and cites no other standard.
