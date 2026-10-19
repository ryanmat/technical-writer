---
type: runbook
domain: engineering
default_audience: operator
source: this skill's house runbook shape (Prerequisites, Procedure, Verification, Rollback, Escalation) for the section shape; Google SRE book, Monitoring Distributed Systems, for the alerting rules; the research records no canonical runbook template, so the body is house prose over those two inputs
license: house (the section shape is this skill's own); CC BY-NC-ND 4.0 (SRE book), the alerting rules paraphrased, no sentence reproduced
procedure: true
procedure_section: Mitigation
sections:
  - heading: Alert or trigger
    level: 2
    evidence:
      pattern: '(?is)\b(?:alert|pages?|fires?|trigger(?:s|ed)?)\b.*?(?:\d|\bwhen\b|\bif\b|\babove\b|\bbelow\b|\bexceeds?\b|\bolder than\b|\bfor more than\b)'
      missing: the alert or trigger by name and the condition that fires it, with its threshold
  - heading: Impact
    level: 2
  - heading: Prerequisites
    level: 2
    evidence:
      pattern: '(?i)(?:\bv?\d+\.\d+(?:\.\d+)?\b|\baccess\b|\bpermissions?\b|\brole\b|\bcredentials?\b|\btoken\b|\bversion\b|\binstalled\b|\blogged in\b)'
      missing: the access, role, credential or tool version the operator needs before step 1
  - heading: Diagnosis
    level: 2
    evidence:
      pattern: '(?is)\A(?:(?!```).)*\Z|```.*?```[^\S\n]*\n\s*(?:\d+\.[ \t]+)?[^.!?\n]*?(?-i:\b(?:output|prints?|returns?|reads|shows|responds?|answers?)\b)'
      missing: the expected output after each diagnosis command
  - heading: Mitigation
    level: 2
    evidence:
      pattern: '(?is)\A(?:(?!```).)*\Z|```.*?```[^\S\n]*\n\s*(?:\d+\.[ \t]+)?[^.!?\n]*?(?-i:\b(?:output|prints?|returns?|reads|shows|responds?|answers?)\b)'
      missing: the expected output after each mitigation command
  - heading: Verification
    level: 2
  - heading: Rollback
    level: 2
    optional: true
  - heading: Escalation
    level: 2
    evidence:
      pattern: '(?is)\b(?:rotation|on-call|oncall|team|channel|owner|pager)\b.*?\b(?:after|when|if|within|unless|minutes?|hours?|still)\b'
      missing: who to escalate to and the condition or time after which to escalate
length_caps:
  operator: 1500
  engineer: 1500
  executive: 400
banned_patterns:
  - pattern: '^#{1,6}\s+Step \d+'
    rule: no Step X in headings
---
# Runbook: <SYSTEM_NAME> <CONDITION>

A runbook is the page an operator runs under pressure: what paged, what it costs while it
lasts, what to check, what to do, how to know it worked, and whom to call when it did not. The
section shape is the house runbook with Alert or trigger, Impact and Diagnosis added;
the three alerting rules are the SRE book's. The front matter above is what
`check_structure.py` enforces, and the procedure rules in `procedure-rules.md` bind the
Mitigation steps.

## Title

The H1 and the only H1: Runbook, a colon, the system and the condition the page is for, as the
alert names it. A title the user gives is kept as given.

## Summary line

One sentence directly under the title that says what the runbook restores and how. The
checker requires exactly one sentence here.

## Alert or trigger

Required. The alert by its exact name, the condition that fires it with its threshold and its
duration, and the labels it carries that the steps use. Every page is actionable: a page the
operator can do nothing about is a bug in the alert, and the runbook says so rather than
inventing a step. Alert on symptoms (what users see), and name the cause in Diagnosis.

Evidence slot: the alert or trigger name and its condition with a figure or a comparison word.

## Impact

Required. What users and dependent systems see while the condition lasts, and what is and is
not at risk (lost, delayed, duplicated). Two to four sentences. A figure the sources do not
give carries the marker.

## Prerequisites

Required. What the operator needs before step 1, one item each: the tool and its version, the
access or role, the cluster or environment, the credential. Parallel fragments or sentences.

Evidence slot: a version, access, role, credential or tool statement.

## Diagnosis

Required. How to find which cause is present: a stem sentence, then numbered steps, each one
command or one check with the exact output that points at each cause. The procedure rules
apply by hand here; the checker applies them to Mitigation.

Evidence slot: the expected output after each diagnosis command, as the first sentence after
its code block, opening with a lowercase verb (the output reads, the command prints, returns,
shows). A section with no command needs no output sentence.

## Mitigation

Required. The procedure section: a stem sentence beginning with To and ending in a colon, in
its own paragraph directly before step 1 (a warning goes in the paragraph before it), then
numbered steps, each
one action of at most 20 words, each command in its own code block with the expected output
after it, and a condition before the action it governs (If the route state is timed-out,
restart the route). A step is at most two sentences: the action, with its condition, and the
output sentence after the code block, which is the step's last sentence. Nothing follows the
output sentence inside the step: a warning is its own paragraph placed before the numbered
step it protects, never inside it; where moved data goes is Rollback's sentence; a value the
operator must choose and how is a Prerequisites item or the marker in the action sentence; a
pointer to another section is a clause in the action, not a sentence of its own. The steps are
ordered from the cheapest reversible action to the most expensive. Automate rote responses: a
step the operator always runs the same way belongs in the alert's automation, and the runbook
names it as already automated or as the action item that will automate it.

Evidence slot: the expected output after each mitigation command, as in Diagnosis.

## Verification

Required. The command or the dashboard that shows the condition is gone, with the exact value
or text that confirms it and how long to wait for it. The alert resolving is the last check,
never the only one.

## Rollback

Optional. How to undo a mitigation step that made things worse or that moved data (a drain, a
replay, a failover), and where the moved data is until then.

## Escalation

Required. Whom to page or call, in which channel, and the condition or the time after which
to do it: the state that means the cause is outside this system, and the wait after the last
mitigation step. A time the sources do not give is the marker. The condition is stated here
once; a Diagnosis step that reaches it says go to Escalation and does not repeat it.

Evidence slot: an escalation target (a rotation, a team, a channel, an owner) and a condition
or time.

## Prose rules

- Imperative, no rationale, the action and its expected result; a reason appears only where
  it changes what the operator does.
- Exact thresholds, commands and identifiers; a placeholder in a command is
  `<ANGLE_BRACKETS>` and the example below it is a real value.
- Every figure (a threshold, a wait, a count) carries its source or the marker.
- The caps count words outside code blocks; the executive cap keeps Alert or trigger, Impact
  and Escalation.

## Source

Section shape (Prerequisites, Procedure, Verification, Rollback, Escalation): this skill's
own house shape; this template
splits Procedure into Diagnosis and Mitigation and adds Alert or trigger and Impact. The three
alerting rules (every page actionable; alert on symptoms, not causes; automate rote
responses): Google SRE book, Monitoring Distributed Systems, CC BY-NC-ND 4.0, paraphrased, no
sentence reproduced. The research survey found no canonical citable runbook template, so the
rest of this file is this skill's own text.
