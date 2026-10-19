---
type: troubleshooting
domain: user documentation
default_audience: engineer
source: GitLab Documentation Style Guide, troubleshooting topic type (docs.gitlab.com/development/documentation/topic_types/troubleshooting), structure and section names only; the research holds no quotable troubleshooting template, so the body is house prose
license: CC BY-SA 4.0 (GitLab, structure and section names only, no prose reproduced); the body is this skill's own text
h1_pattern: '^(?!(?:How to|What is|Using)\b)(?!(?!(?:Alerting|Batching|Billing|Caching|Indexing|Logging|Monitoring|Pricing|Queuing|Routing|Sampling|Scaling|Scheduling|Sharding|Streaming|Throttling|Timing|Tracing)\b)[A-Z][a-z]*ing\b)\S+ \S'
sections:
  - heading_pattern: '^(?!Related$).+'
    label: a problem section
    level: 2
  - heading: Symptom
    level: 3
  - heading: Cause
    level: 3
  - heading: Resolution
    level: 3
    evidence:
      pattern: '(?is)\A(?:(?!```).)*\Z|```.*?```[^\S\n]*\n\s*(?:\d+\.[ \t]+)?[^.!?\n]*?(?-i:\b(?:output|prints?|returns?|reads|shows|responds?|answers?)\b)'
      missing: the expected output after the resolution's command
  - heading: Related
    level: 2
    optional: true
length_caps:
  engineer: 3000
  executive: 500
banned_patterns:
  - pattern: '^#{1,6}\s+(?!(?:Alerting|Batching|Billing|Caching|Indexing|Logging|Monitoring|Pricing|Queuing|Routing|Sampling|Scaling|Scheduling|Sharding|Streaming|Throttling|Timing|Tracing)\b)[A-Z][a-z]+ing\b'
    rule: troubleshooting headings are a bare infinitive or a noun phrase, never an -ing opener
  - pattern: '^#{1,6}\s+How to\b'
    rule: no How to in headings; an entry is named by its symptom, and its Resolution says how
---
# <TROUBLESHOOTING_TITLE>

A troubleshooting topic takes one reader from a symptom they can see to a fix they can verify.
It has a title naming the feature, a one-sentence summary, one entry per symptom with a
Symptom, a Cause, and a Resolution, and an optional Related section. The front matter above is
what `check_structure.py` enforces; the guidance below is what the skill follows when it
writes. The structure follows GitLab's troubleshooting topic type (one entry per message,
named by the message, with a cause and a resolution); every sentence here is this skill's own,
since GitLab's text is ShareAlike and the research holds no quotable troubleshooting template.

## Title

The title is the H1 and the only H1. Name the feature the entries belong to as a bare
infinitive or a noun phrase: Troubleshoot routes in Northwind Relay, or Route errors in
Northwind Relay. GitLab names the page Troubleshooting with the feature; the gerund opener is
rejected here by the heading rule the Google developer documentation style guide and the
Grafana Writers' Toolkit share, so write Troubleshoot. The `h1_pattern` rejects an -ing
opener, with the product-area nouns exempted, and the openers How to, What is, and Using; it
requires at least two words.

## Summary

One sentence directly under the title, before the first entry, saying what the page fixes and
where the reader sees the symptoms. The checker requires exactly one sentence here.

## Entries

Required: at least one level-two section per symptom, named by the symptom in the reader's
words or by the message they see. Open the heading with the message type when there is one,
Error: or Warning:, then the message in code style, cut to the part that identifies it when it
runs long. One symptom per entry, the entries in the order a reader meets them, the most common
first. Five or more entries on a feature page make a page of their own. Each entry carries the
three sections below, at level three, in this order; the checker requires each one once in the
document and reads the first entry's, so the writer owns the later entries.

### Symptom

Required. What the reader sees, in the reader's terms: the page state, the exact message in
code style, the command and what it printed. No cause and no fix here. A symptom the sources do
not give verbatim is written as the marker rather than a reconstructed message.

### Cause

Required. Why it happens, in one or two sentences the reader can test against their system.
When several causes share a symptom, list them, each with the check that tells it apart. Every
default, limit, or timeout the cause names traces to a source; one the sources do not give is
the marker in place of the number:

```text
The consumer group acknowledged no message within the route timeout. [UNVERIFIED: the default route timeout]
```

### Resolution

Required. The fix as a procedure when it has steps, under the procedure rules in
`procedure-rules.md`, with a stem sentence beginning with To. Use resolution for a permanent
fix and workaround for a temporary one, and say which it is. Every command sits in its own
code block, and the expected output follows each command whose output the reader uses (spec
R9): that line is the evidence slot, read as the first sentence after a code block with the verb
in lowercase (prints, returns, reads, shows, output), and a Resolution with a command block and
no such sentence fails it; a step that opens with Return or Open after the block is not output. A Resolution with no command, a UI fix, fills the
slot by having nothing to verify at the command line; state what the page shows instead. A
command that changes data carries a bold **Warning:** paragraph before the step that runs it.

## Related

Optional. The concept topic that explains the mechanism, the task that configures it, and the
reference that lists its settings, with the exact title of the linked page as the link text.
This section comes last.

## Audience

The default audience is the engineer. For an operator, keep the same entries and put the
check that tells causes apart first in each Cause. For an executive, keep the summary and one
sentence per entry, within the cap. The caps count words outside code blocks.

## Source

Structure and section names: GitLab Documentation Style Guide, troubleshooting topic type,
`docs.gitlab.com/development/documentation/topic_types/troubleshooting`, CC BY-SA 4.0; names
only, no sentence reproduced, so this file inherits no ShareAlike obligation. The heading rule:
Google developer documentation style guide, Headings and titles, CC BY 4.0, and Grafana
Writers' Toolkit, Gerunds.yml, Apache-2.0. The word rules are the global bans in
`style-rules.md`. The expected-output slot is this skill's rule, stated in spec R9. The rest
of this file is this skill's own text.
