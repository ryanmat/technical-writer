---
type: disclosure notification
domain: security
default_audience: operator
source: OpenSSF vulnerability disclosure guide, notification templates (templates/notifications/embargo.md and disclosure.md, ossf/oss-vulnerability-guide at 40ecfe2), for the section set, the embargo terms and the timeline fields
license: CC BY 4.0
h1_pattern: '^(?:Embargoed notification|Public disclosure): \S.*$'
sections:
  - heading: Summary
    level: 2
    evidence:
      pattern: '(?i)(?:[<>]=?\s*v?\d+\.\d+)|(?:\b(?:before|prior to|through|up to|earlier than)\s+v?\d+\.\d+)|(?:\bv?\d+\.\d+(?:\.\d+)?\s+(?:and earlier|and later|through)\b)|(?:\bversions?\b[^\n]{0,20}\bv?\d+\.\d+)'
      missing: the affected versions, as a range with its bounds
  - heading: Severity
    level: 2
    evidence:
      pattern: '\b(?:Low|Medium|High|Critical)\b'
      missing: the rating, Low, Medium, High or Critical, with its reasoning
  - heading: Proof of concept
    level: 2
    evidence:
      pattern: '(?m)^[ ]{0,3}(?:`{3,}|~{3,})'
      missing: the code or command lines that reproduce the issue, in a code block
  - heading: Remediation and mitigation
    level: 2
    evidence:
      pattern: '(?i)\bv?\d+\.\d+(?:\.\d+)?\b|\b\d{4}-\d{2}-\d{2}\b|https?://\S+'
      missing: the version that fixes it, or the date or the link where the patch is or will be available
  - heading: Further analysis
    level: 2
    optional: true
  - heading: Timeline
    level: 2
    evidence:
      pattern: '\b\d{4}-\d{2}-\d{2}\b'
      missing: the dates reported, fixed and disclosed or to be disclosed, in ISO 8601 form
  - heading: Disclosure
    level: 2
    evidence:
      pattern: '(?s)\A(?=.*\b\d{4}-\d{2}-\d{2}\b)(?=.*(?:https?://\S+|[\w.+-]+@[\w-]+(?:\.[\w-]+)+))'
      missing: the disclosure date and, under embargo, the contact for questions, or, once public, the advisory link
length_caps:
  operator: 1200
  engineer: 1500
  executive: 300
---
# Embargoed notification: <PRODUCT> <FLAW_IN_FIVE_WORDS>

Embargoed notification of <FLAW_TYPE> in <PRODUCT> <RANGE>, to be disclosed on <DATE>.

A disclosure notification is the message a project sends about one vulnerability: under
embargo to the distributors and service providers who must patch before the public knows,
or in public once the fix is out. The two forms share one section set, the source's, and
differ in the title's opening words, the paragraph under the summary line, and what the
Disclosure section carries. The front matter above is what `check_structure.py` enforces;
the body says what each section holds and where the two forms part.

## Title

The H1 and the only H1, opening with the variant: `Embargoed notification: ` or
`Public disclosure: `, then the product and the flaw in plain words, no code style. The
checker reads the opening words as the variant. The source titles the public form "Security
advisory for $CVEID"; this skill reserves advisory for the vulnerability advisory type and
names the identifier in the Summary instead.

## Summary line

One sentence directly under the title: the flaw type, the product, the affected range and,
under embargo, the disclosure date, or, in public, the fixed version. The checker requires
exactly one sentence here.

Under embargo, the paragraph after it is the source's terms, quoted: "This notification is
sent to let distributors and service providers plan for applying patches to reduce the time
of user exposure. Information below should be kept confidential until the listed embargo
date. Please do not forward this information to other parties." In public there is no such
paragraph.

## Summary

Required. The source asks for "a brief (as short as possible, about a paragraph) summary of
the vulnerability using technical details", whose goal "is to allow the vendor to do a quick
assessment of what the bug is about", then three lines in bold: **CVE:** the identifier or
the statement that one is requested; **Affected versions:** the range with its bounds, lower
bound first, as the vulnerability advisory template writes it; **Reporter:** the name and
affiliation as the reporter asked to be named, or the statement that the reporter asked not
to be named. An identifier in an example is a reserved `CVE-1900-` value.

Evidence slot: the affected versions as a range or a version statement.

## Severity

Required. The rating, Low, Medium, High or Critical, and the source's instruction:
"Accompany your assessment with a motivation, and even a good attack scenario to explain the
risk associated with the vulnerability." A CVSS score is optional; when one is given, "also
include the vector phrase", in the form the vulnerability advisory template fixes, and the
sources supply both or neither.

Evidence slot: a rating word.

## Proof of concept

Required. The source wants "a concrete, usable, and repeatable way for the vendor to reproduce
the issue" so they can test fixes and mitigations: the commands or code in a fenced block,
with the observed result after it. Example values use `example.com` hosts and reserved
identifiers, and no credential. A reproduction the sources do not supply is the marker; the
skill never writes an exploit.

Evidence slot: a fenced code block.

## Remediation and mitigation

Required. Under embargo: the "known remediation or planned patch", with "when patch will be
available OR links to where the patch is/will be available". In public: the "known
remediations", and "if one is a software update, note the version(s) that fix it". A
mitigation for a system that cannot patch, when there is one, follows the fix. A date, link
or version the sources do not give is the marker.

Evidence slot: a version, a date or a link.

## Further analysis

Optional. Context the sections above do not hold, after them as the source asks, and, in
public, whether the vulnerability "has been exploited in the wild" when the sources say so.
No section when there is nothing to add.

## Timeline

Required. The source's three fields in bold, one per line, ISO 8601 dates: **Date reported:**,
**Date fixed:**, and **Date to be disclosed:** under embargo or **Date disclosed:** in public;
a communication and updates summary after them when the sources give one. A date the
sources do not give is the marker, not a blank.

Evidence slot: an ISO 8601 date.

## Disclosure

Required, the one section whose content the variant changes. Under embargo: the public
disclosure date with its time and time zone, the contact for questions, and the source's
closing terms, quoted: "Please do not make the issue public, issue user communications,
share this information with others, or issue public patches before the disclosure date. We
will notify this list immediately if the disclosure date is at risk or changes." In public:
the disclosure date and the link to the published advisory or the security advisory entry.

Evidence slot: a date, and a contact address or a link.

## Prose rules

- The variant is stated once, in the title; no section says embargoed or public again except
  the Disclosure terms.
- No advertising and no diligence statement, as the vulnerability advisory rules say; the
  notification says what is wrong, how to reproduce it and what to do.
- The caps count words outside code blocks.

## Source

Section set, field names, the embargo terms and the quoted instructions: OpenSSF
vulnerability disclosure guide, `templates/notifications/embargo.md` and `disclosure.md` in
`github.com/ossf/oss-vulnerability-guide` at commit 40ecfe2, licensed CC BY 4.0, quoted. The
variant marker in the title, the Disclosure section and the slot rules are this skill's own.
The rest of this file is this skill's own text.
