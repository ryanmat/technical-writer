---
type: SECURITY.md
domain: security
default_audience: engineer
source: OpenSSF vulnerability disclosure guide, SECURITY.md templates (templates/security_policies, ossf/oss-vulnerability-guide at 40ecfe2), for the reporting paragraph, the acknowledgement window and the disclosure timeline
license: CC BY 4.0
h1_pattern: '(?i)^(?:\S.* )?security policy$'
sections:
  - heading: Supported versions
    level: 2
    evidence:
      pattern: '(?m)^\|[^\n]*\d+\.\d+[^\n]*\|[ \t]*$'
      missing: a table of versions, one row each, saying which receive security fixes
  - heading: Reporting a vulnerability
    level: 2
    evidence:
      pattern: '(?s)\A(?=.*(?:https?://\S+|[\w.+-]+@[\w-]+(?:\.[\w-]+)+))(?=.*\b\d+\s*(?:working |business |calendar )?(?:days?|hours?|weeks?)\b)'
      missing: the address or form URL to report to, and the number of days or hours within which the project responds
  - heading: Disclosure policy
    level: 2
  - heading: Security updates
    level: 2
length_caps:
  engineer: 800
  operator: 800
  executive: 200
---
# <PROJECT_NAME> security policy

Reports a security issue in <PROJECT_NAME> privately to <ADDRESS>, which acknowledges it within <N> working days and discloses it under a <N>-day timeline.

A SECURITY.md is the file a reporter reads before sending a vulnerability: which versions
the project fixes, where to send the report and what happens next, when the issue becomes
public, and how fixes reach users. The front matter above is what `check_structure.py`
enforces; the body says what each section holds. The reporting paragraph, the acknowledgement
window and the disclosure timeline follow the OpenSSF templates; the four sections and the
version table are this skill's own, since the source gives a paragraph and GitHub reads the
file as the repository's security policy.

## Title

The H1 and the only H1: the project name and the words security policy, or the words alone:
`Northwind Relay security policy`. GitHub shows the file under its own heading, so the title
carries no date and no version. A title the user gives is kept when it has this form.

## Summary line

One sentence directly under the title: where a report goes, how fast the project answers, and
the disclosure timeline, the three facts a reporter needs. The checker requires exactly one
sentence here.

## Supported versions

Required. A table with the columns Version and Supported, one row per release line the
project still ships or recently shipped, newest first: the version or range as the project
names it (`2.5.x`), and yes, no, or the date support ends. A line whose status the sources do
not give is the marker in its Supported cell. Every version the project will fix is in the
table, so a reporter with an older version knows before writing.

Evidence slot: a table row carrying a version.

## Reporting a vulnerability

Required. The source's paragraph, adapted to the project: "To report a security issue,
please email" the project's address, or "please visit" the form, "with a description of the
issue, the steps you took to create the issue, affected versions, and, if known, mitigations
for the issue." Then the acknowledgement commitment as the source states it, "within 3
working days", with the project's own number; then what the reporter can expect after the
acknowledgement (confirmation, a fix timeline, an advisory). Both channels when the project
has both, the form first when the project prefers it. A key for encrypted reports is named
with its fingerprint, or carries the marker. A window the sources do not give is the marker,
not a round number.

Evidence slot: an address or a URL, and a number of days or hours.

## Disclosure policy

Required. The timeline, as the source states it: "This project follows a 90 day disclosure
timeline", with the project's own number; what the project does during it (confirms, fixes,
requests an identifier, prepares the advisory); whether the reporter is credited and how
they say so; and what happens when the fix needs longer. In normative text the obligation
words keep their RFC 2119 sense.

## Security updates

Required. How a fix reaches users and how they hear of it: the advisory channel, the release
notes, a mailing list or feed, with the link for each, and the version line a fix lands in
first. Nothing about past issues; the advisories hold those.

## Prose rules

- Second person throughout: the reader is the reporter.
- No diligence statement and no thanks in advance; the file says what to do and what happens.
- The caps count words outside code blocks.

## Source

The reporting paragraph, the acknowledgement window and the disclosure timeline, with the
quoted lines: OpenSSF vulnerability disclosure guide, `templates/security_policies/
email_intake.md`, `github_security_policy.md` and `other_intake_systems.md` in
`github.com/ossf/oss-vulnerability-guide` at commit 40ecfe2, licensed CC BY 4.0, quoted. The
four sections, the version table and the slot rules are this skill's own. The rest of this
file is this skill's own text.
