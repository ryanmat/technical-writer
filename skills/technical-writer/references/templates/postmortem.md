---
type: postmortem
domain: engineering
default_audience: engineer
source: Google SRE Workbook, postmortem chapter, for the section set and the action item rule; Google SRE book, Postmortem Culture, for the blameless rule
license: CC BY-NC-ND 4.0 (both), section names and rules paraphrased, no sentence reproduced
sections:
  - heading: Summary
    level: 2
  - heading: Impact
    level: 2
    evidence:
      pattern: '(?is)(?=.*\b\d+[\s-]*(?:seconds?|minutes?|hours?|days?)\b)(?=.*(?<![\w:.,-])\d[\d,.]*\s*(?:%|percent|(?![\d:-])(?!(?:seconds?|minutes?|hours?|days?|of|more|to|and|or|at|on|in|the|a|an|by|for|with|from|per|until|through|utc|z|ms|s|m|h|k|kb|mb|gb|tb|rps|qps|req)\b)[a-z]+)\b)'
      missing: the duration of the impact and a count of who or what it reached (users, consumers, requests, orders), each a figure with its unit
  - heading: Root causes and trigger
    level: 2
  - heading: Timeline and recovery
    level: 2
    evidence:
      pattern: '\b\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}'
      missing: ISO timestamps on the timeline entries (YYYY-MM-DDTHH:MMZ, or with a zone offset)
  - heading: Detection
    level: 2
  - heading: Action items
    level: 2
    evidence:
      pattern: '(?is)\bowner:\s*\S.*?\bpriority:\s*P[0-4]\b'
      missing: 'an owner and a priority on each action item, in the form (owner: <WHO>, priority: P1, <TRACKER-ID>)'
  - heading: Lessons learned
    level: 2
length_caps:
  engineer: 2500
  executive: 500
banned_patterns:
  - pattern: '(?i)\b(?:careless(?:ly|ness)?|negligen(?:t|ce)|should have|blame[sd]?|at fault|the fault (?:is|was|lies))\b'
    rule: blameless postmortem; name the system or the process that failed, never a person's judgment
---
# <SYSTEM_NAME> <WHAT_HAPPENED> on <YYYY-MM-DD>

A postmortem records one incident so that the systems and processes behind it get fixed: what
happened, whom it reached and for how long, the causes and their trigger, the timeline and
the recovery, how it was found, and the owned work that follows. The section set and the action item rule are the SRE
Workbook's, paraphrased; the blameless rule is the SRE book's. The front matter above is what
`check_structure.py` enforces.

## Title

The H1 and the only H1: the system, what happened, and the date. A title the user gives is
kept as given.

## Summary line

One sentence directly under the title that says what stopped working, for how long, and why.
The checker requires exactly one sentence here.

## Summary

Required. The incident in one paragraph for a reader who reads nothing else: the window, what
users saw, the cause in one clause, how it ended, and whether anything was lost. Every figure
carries its source or the marker. The Summary is the one place the whole story is told; the
sections below add detail to it and do not repeat its sentences.

## Impact

Required. Who and what the incident reached and for how long: the duration, the count of
users, consumers or requests affected, the data lost or delayed, and the revenue or
obligation touched when the sources give it.

Evidence slot: a duration in seconds, minutes, hours or days and a count with its unit. A
count the sources do not give is the marker: `[UNVERIFIED: the number of users affected]`.

## Root causes and trigger

Required. The conditions in the system that let an ordinary event become an incident, each a
sentence about a component or a process: what it did, what it lacked. More than one cause is
normal, and a cause the sources leave open carries the marker. The section closes with the
trigger in one sentence: the event that set the causes off (the deploy, the restart, the
traffic change, the expiry) and its time. What the event did to the system is the causes'
sentences, not the trigger's.

## Timeline and recovery

Required. One entry per event, in order, each opening with its ISO timestamp (the zone named,
Z for UTC): when the trigger happened, when the symptom started, when the alert fired, when a
person acted, when service returned, when the backlog cleared. Facts only; the judgment goes
in Detection and Lessons learned. After the entries, one paragraph names the action that
ended the incident by its entry (the 14:40 restart) and what was done afterwards to clear
its effects; the times stay in the entries.

Evidence slot: ISO timestamps on the entries.

## Detection

Required. How the incident was noticed, how long that took from the symptom's start, what
signal fired and what signal did not.

## Action items

Required. One item per fix, each a complete sentence naming the change, with its owner, its
priority and its tracker identifier in parentheses at the end:

```text
- <THE CHANGE, AS A SENTENCE> (owner: <ROLE OR TEAM>, priority: P1, <TRACKER-ID>).
```

One owner per item, a role or a team, never a person's name. A priority from P0 (before any
other work) to P4 (when convenient). An item with no tracker identifier carries the marker in
its place. Systemic fixes before behavior changes: an item that asks a person to be more
careful is not an action item.

Evidence slot: the owner and priority form on the items.

## Lessons learned

Required. Three paragraphs or three labeled lists: what went well, what went poorly, and
where we got lucky. Each point is a judgment the sections above do not make, naming the
timeline entry or the cause it draws on in a clause; a point that restates a figure or a cause
already given is not a lesson.

## Prose rules

- Blameless: name the system or the process that failed, never a person's judgment. The
  checker bans careless, negligent, should have, blame and at fault; the by-hand check reads
  for the same stance in other words.
- No end-user identifiers: a user is a count, a role or a tenant, never a name or an account.
- Every figure (a duration, a count, a rate) carries its source or the marker.
- Past tense for what happened, present tense for what the system does.
- Each fact has one home: the window and the loss in Summary, the counts in Impact, the
  conditions and the event in Root causes and trigger, the times and the ending action in
  Timeline and recovery, the signals in Detection. A later section names the earlier one in a
  clause and does not restate its fact; a figure appears once with its unit.
- The caps count words outside code blocks; the executive cap keeps the Summary, Impact and
  Action items.

## Source

Section set (summary, impact, root causes and trigger, timeline and recovery, detection, action
items, lessons learned as what went well, what went poorly and where we got lucky) and the
action item rule (each item has an owner, a priority and a tracking identifier; one
accountable owner; systemic fixes over behavior changes): Google SRE Workbook, Postmortem
Culture chapter, paraphrased. The blameless rule and the no-identifiers rule: Google SRE book,
Postmortem Culture chapter, paraphrased. Both CC BY-NC-ND 4.0; no sentence is reproduced. The
rest of this file is this skill's own text.
