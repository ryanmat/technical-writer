---
type: endpoint or field description
domain: API
default_audience: engineer
source: AIP-192, API documentation (google.aip.dev/192), for the description rules (the first sentence omits the subject and is in the third-person present, brief but complete, the questions a description answers, the Deprecated opener); the page shape is this skill's own
license: CC BY 4.0
h1_pattern: '^(?:(?:GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS) /\S*|[A-Za-z_][A-Za-z0-9_.-]*)$'
sections:
  - heading: Summary
    level: 2
  - heading: Request
    level: 2
    evidence:
      pattern: '(?im)^\|[^\n]*\btype\b[^\n]*\bdefault\b[^\n]*\|[ \t]*$'
      missing: a field table whose header row carries a Type column and a Default column
  - heading: Response
    level: 2
    evidence:
      pattern: '\b(?:200|201|202|204)\b'
      missing: the status code of the successful response
  - heading: Errors
    level: 2
    evidence:
      pattern: '\b[45]\d\d\b'
      missing: the status code of each error the call returns
  - heading: Example
    level: 2
    evidence:
      pattern: '(?m)^[ ]{0,3}(?:`{3,}|~{3,})'
      missing: an example request and response, or an example value, in a code block
length_caps:
  engineer: 1500
  downstream provider: 1500
  executive: 300
banned_patterns:
  - pattern: '\bThis (?:field|parameter|property|attribute|endpoint|method|operation|call|resource|value)\b'
    rule: a description opens with its verb or with the noun it describes, never This field or This endpoint; the source's first-sentence rule omits the subject
---
# POST /<RESOURCE>

Registers a <RESOURCE> under the given <PARENT> and returns it with its identifier.

An endpoint or field description is the reference entry an integrating developer reads for
one call, or for one field of a request or response message. The front matter above is what
`check_structure.py` enforces; the body says what each section holds. The description rules
come from AIP-192; the page shape, the five sections and the field table, is this skill's
own, since AIP-192 governs the comment on a field or a method and bans headings and tables
only there, where they break the tools that render proto comments.

## Title

The H1 and the only H1. For an endpoint, the HTTP method in capitals and the path, with a
space between and nothing else: `POST /routes`, `GET /routes/{id}`. For a field, the field's
name as the schema spells it, dotted for a nested field: `retry_limit`, `route.retry_limit`.
No code style in the heading, since the heading is the link anchor and the checker reads it as
text. A title the user gives is kept when it has this form.

## Summary line

One sentence directly under the title, written as the source writes the first sentence of a
description: the subject omitted and the verb in the third-person present. "Creates a book
under the given publisher." is the source's example; "Registers a route and returns it with
its identifier." and "Caps the attempts before a message is written to the stalled-stream
report." are this template's. The checker requires exactly one sentence here.

## Summary

Required. What the call or field does beyond its first sentence, answering the source's
questions in the order they matter to the caller: what the side effects are, whether the call
is idempotent, what permission or scope it needs, what the units and the accepted range are,
and what a caller does differently because of each. A sentence the first line already states
is not repeated here. A deprecated call or field opens this section with `Deprecated:` and
names the alternative, or the reason when there is none, as the source requires.

## Request

Required. The fields of the request, or the one field the page describes, as a table with the
columns Field, Type, Required, Default and Description, in that order. Type is the schema's
type word (`string`, `integer`, `boolean`, `object`, `array`, `timestamp`); Required is yes or
no; Default is the value the server applies when the field is omitted, `none` for a required
field, or the marker when the sources state that a default exists and not what it is. The
Description cell is one or two sentences in the summary line's form: the verb or the noun
first, never This field. A constraint the server enforces (a length, a range, a cap) goes in
the Description cell with its figure. A call with no request body says so in one sentence and
tables its path and query parameters instead.

Evidence slot: a table header row carrying a Type column and a Default column. The checker
reads the header row only; an empty Type or Default cell is the checklist's to catch, and the
rule above says what goes there instead of a blank.

## Response

Required. The status code of the successful response first, in the form `201 Created`, then
the body as a field table with the columns Field, Type and Description, or the sentence that
there is no body. A field the server assigns (an identifier, a timestamp) says so in its
Description cell. A field the response echoes from the request is listed again with its type
and the word echoed, not described a second time.

Evidence slot: the success status code.

## Errors

Required. One row per error the call returns, as a table with the columns Status, Error and
When: the status code, the error identifier the API's error catalog uses, and the condition
that produces it, written as the caller would see it. An error whose entry exists in the
catalog links to it; the page never restates the catalog's resolution text.

Evidence slot: at least one 4xx or 5xx status code.

## Example

Required. One request and its response, or for a field page one example value in its context,
in fenced code blocks, taken from the sources: a captured exchange, a test fixture, or a
schema example. The values are the source's own; an example the sources do not supply is the
marker, never an invented one. Example values use `example.com` hosts and reserved
identifiers, and never a credential.

Evidence slot: a fenced code block.

## Prose rules

- Descriptions are complete sentences that open with the verb or the noun; This field, This
  endpoint and their kin are banned by the checker.
- Every unit is stated with its figure (`500`, in milliseconds), and every range or cap with
  both bounds or its one bound and the behavior at it.
- A default the sources state exists but do not give is the marker in the Default cell, never
  a guess and never a blank.
- The caps count words outside code blocks.

## Source

The description rules: AIP-192, API documentation, `google.aip.dev/192`, licensed CC BY 4.0
(the page footer, read 2026-10-18), quoted where this file quotes it. The five sections, the
field table and the identifier conventions are this skill's rules. The rest of this file is
this skill's own text.
