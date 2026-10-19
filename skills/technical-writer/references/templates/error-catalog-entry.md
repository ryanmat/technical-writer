---
type: error catalog entry
domain: API
default_audience: engineer
source: RFC 9457, Problem Details for HTTP APIs, for the problem details members and the rule for defining a problem type (a type URI, a title, the status code); AIP-193, Errors (google.aip.dev/193), for the message rules and the UPPER_SNAKE_CASE reason
license: standards (RFC 9457, IETF Trust) and CC BY 4.0 (AIP-193)
h1_pattern: '^(?=\S+ \S)[^`]+$'
sections:
  - heading: Problem details
    level: 2
    evidence:
      pattern: '(?is)\A(?=.*\btype\b[^\n]*(?:https?://|urn:|about:blank)\S*)(?=.*\bstatus\b[^\n]*\b[1-5]\d\d\b)(?=.*\btitle\b[^\n]*\S)'
      missing: the type URI, the status code and the title of the problem type, one per row
  - heading: Cause
    level: 2
  - heading: Resolution
    level: 2
  - heading: Example response
    level: 2
    evidence:
      pattern: '(?m)^[ ]{0,3}(?:`{3,}|~{3,})'
      missing: one occurrence of the problem as the server returns it, in a code block
length_caps:
  engineer: 800
  downstream provider: 800
  executive: 200
---
# <ERROR_TITLE>

Rejects the request because <CONDITION>, and the caller <WHAT_TO_DO>.

An error catalog entry is the page an integrating developer lands on from an error response:
one problem type, what produces it, what the caller does about it, and one occurrence as the
server returns it. The front matter above is what `check_structure.py` enforces; the body says
what each section holds. The members and the definition rule come from RFC 9457; the message
rules and the reason form come from AIP-193; the four sections are this skill's own.

## Title

The H1 and the only H1: the problem type's title, the source's "short, human-readable summary
of the problem type", which "SHOULD NOT change from occurrence to occurrence of the problem,
except for localization". Two or more words, no code style, no status code and no identifier
in it: `Route name already in use`, not `409` and not `ROUTE_CONFLICT`. A title the user
gives is kept when it has this form.

## Summary line

One sentence directly under the title: what the server rejects or fails and what the caller
does, in the voice of the endpoint description's first line, the subject omitted and the verb
in the third-person present. The checker requires exactly one sentence here.

## Problem details

Required. A table with the columns Member and Value, one row per member the problem type
fixes, in this order: `type`, the URI that identifies the problem type (the source's
definition of a problem type documents "a type URI (typically, with the "http" or "https"
scheme)", and `about:blank` names the type whose only meaning is its status code); `status`,
"the HTTP status code for it to be used with"; `title`, the H1 repeated as the server sends
it; and, when the API follows AIP-193, `reason`, the identifier in UPPER_SNAKE_CASE "without
leading or trailing underscores, and without leading digits", at most 63 characters, and
`domain`, the service name that makes the reason unique. The `detail` and `instance` members
vary per occurrence and are not rows here; the Example response shows them.

Evidence slot: the `type` row with a URI, the `status` row with a code, and the `title` row
with its text.

## Cause

Required. The condition that produces the error, written as the caller sees it: the request
shape, the state of the resource, or the permission that was missing, and which calls return
it. The entry "must not assume that the user will know anything about its underlying
implementation": no exception class, no file or line, no component name the caller cannot see.
A cause the sources state exists but do not describe is the marker.

## Resolution

Required. What the caller does to resolve the error, as the source asks of a message: "brief
but actionable", enough for "a reasonably technical user" to "understand and resolve the
issue". The first sentence is the action; a second names the call or the field it uses. When
the resolution differs by condition, one short paragraph per condition, the condition first.
Whether a retry of the same request can succeed is stated in one sentence, since it is the
first thing a client author decides.

## Example response

Required. One occurrence of the problem as the server returns it: the status line, the
`Content-Type: application/problem+json` header, and the body with its `type`, `title`,
`status`, `detail` and `instance` members, in a fenced code block, taken from a capture or a
test fixture in the sources. The `detail` member is "a human-readable explanation specific to
this occurrence of the problem", which "Consumers SHOULD NOT parse", so a value a client needs
is a member of its own, not a phrase inside `detail`. An occurrence the sources do not supply
is the marker, never an invented body. Example values use `example.com` hosts and reserved
identifiers.

Evidence slot: a fenced code block.

## Prose rules

- The title and the `title` member are the same words; the status code and the reason stay
  out of the title.
- No internal name reaches the entry: no exception class, stack frame, file, line, or host.
- The caps count words outside code blocks.

## Source

The members, the definition rule and the quoted lines: RFC 9457, Problem Details for HTTP
APIs, July 2023, standards text under the IETF Trust Legal Provisions, quoted. The message
rules and the reason form: AIP-193, Errors, `google.aip.dev/193`, licensed CC BY 4.0 (the
site footer, read 2026-10-18), quoted. The four sections and the member table are this
skill's rules. The rest of this file is this skill's own text.
