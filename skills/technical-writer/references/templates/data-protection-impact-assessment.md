---
type: data protection impact assessment
domain: privacy
default_audience: auditor
source: ICO, Data protection impact assessments, How do we do a DPIA? (ico.org.uk, read 2026-10-18), the seven steps as sections and the rules for assessing risk, recording measures and concluding; Article 35 of Regulation 2016/679 for the obligation
license: Open Government Licence v3.0 (ICO, quoted with attribution); the GDPR, statutory
h1_pattern: '^Data protection impact assessment\b'
sections:
  - heading: Identify the need for a DPIA
    level: 2
  - heading: Describe the processing
    level: 2
    evidence:
      pattern: '(?s)\A(?=.*(?i:\bnature\b))(?=.*(?i:\bscope\b))(?=.*(?i:\bcontext\b))(?=.*(?i:\bpurposes?\b))'
      missing: the nature, scope, context and purposes of the processing
  - heading: Consultation
    level: 2
  - heading: Necessity and proportionality
    level: 2
    evidence:
      pattern: '(?i)\b(?:lawful|legal) basis\b|\b(?:contract|consent|legal obligation|legitimate interests?|vital interests?|public task|public interest)\b'
      missing: the lawful basis for the processing
  - heading: Identify and assess risks
    level: 2
    evidence:
      pattern: '(?s)\A(?=.*(?i:\blikelihood\b))(?=.*(?i:\bseverity\b))'
      missing: the likelihood and the severity of each risk
  - heading: Measures to reduce risk
    level: 2
    evidence:
      pattern: '(?i)\bresidual\b'
      missing: the residual risk after each measure
  - heading: Sign off and record outcomes
    level: 2
    evidence:
      pattern: '(?s)\A(?=.*(?i:\bsign(?:ed|ature|atory|-off| off)\b))(?=.*\b(?:19|20)\d{2}-\d{2}-\d{2}\b)'
      missing: the sign-off line with the name, the role and the date
length_caps:
  auditor: 3500
  regulator: 3500
  executive: 500
---
# Data protection impact assessment: <PROJECT_NAME>

A data protection impact assessment is the record Article 35 of the GDPR requires before
processing that is likely to result in a high risk to individuals, and the record an auditor
tests afterwards. The sections are the ICO's seven steps, in order: identify the need, describe
the processing, consult, assess necessity and proportionality, identify and assess risks,
identify measures, and conclude by signing off and recording the outcomes. The ICO's text is
reproduced here under the Open Government Licence v3.0 with attribution. The front matter above
is what `check_structure.py` enforces, at the one heading level the template declares, so a
level-two heading the list does not name is a finding.

## Title

`# Data protection impact assessment: <PROJECT_NAME>`, the H1 and the only H1, followed by one
sentence that says what the assessment covers, under which obligation, and for whom the record
is written.

## Identify the need for a DPIA

Required. Why this processing needs an assessment: the project, in one paragraph, and the
criteria it meets. The ICO says "If you have any major project that involves the use of
personal data, it is good practice to do a DPIA." Name the brief or decision that triggered
the assessment, with its date.

## Describe the processing

Required. The ICO says "Describe how and why you plan to use the personal data" and that the
description covers "the nature, scope, context and purposes of the processing": the data items,
their source, what is done with them, how many people and records, for how long, the purpose,
and the relationship with the people. Evidence slot: all four words, nature, scope, context
and purpose, stated in the section; a section naming three of them is the finding. A count the
sources do not give is the marker.

## Consultation

Required. The ICO says "You should seek and document the views of individuals (or their
representatives) unless there is a good reason not to" and "You should consult all relevant
internal stakeholders, in particular anyone with responsibility for information security."
Each consultation with its date, who took part, what they said, and what the project did with
it; the data protection officer's advice is recorded here in its own words, and the ICO says
"If you decide not to follow their advice, you need to record your reasons."

## Necessity and proportionality

Required. Whether the processing achieves its purpose ("Do your plans help to achieve your
purpose?") and whether a less intrusive way exists; the lawful basis, named; the data
minimisation, retention and transparency measures; and how the people's rights are met.
Evidence slot: the lawful basis.

## Identify and assess risks

Required. The ICO says "To assess whether the risk is a high risk, you need to consider both
the likelihood and severity of the possible harm." One row per risk, with its source ("Against
each risk identified, record its source"), its likelihood, its severity and the overall rating,
on the scale the assessment names. Evidence slot: the words likelihood and severity.

## Measures to reduce risk

Required. One row per measure, naming the risk it addresses, its effect (eliminated, reduced or
accepted) and the residual risk after it, as the ICO asks the conclusion to record. Evidence
slot: the word residual.

## Sign off and record outcomes

Required. The ICO says the conclusion records the additional measures, whether each risk is
eliminated, reduced or accepted, and "the overall level of 'residual risk' after taking
additional measures", and that "if there is still a high risk, you need to consult the ICO
before you can go ahead with the processing". Record the overall residual risk and whether the
supervisory authority is consulted, that the DPO's advice was followed or why not, the
approval and its conditions, the review trigger and interval, and the sign-off line: who
signed, in what role, on what date. Evidence slot: a sign-off word and an ISO date.

## Audience

The default audience is the auditor, who tests the record against the control: exact
identifiers, dates, owners and record references, and statements of what was done, by whom and
when, never of intent. The regulator reads the same record at the auditor cap. An executive
gets the title, the need, the risk table's overall column and the outcome within the executive
cap. The caps count words outside code blocks.

## Source

The seven steps, their order and the quoted sentences: Information Commissioner's Office, Data
protection impact assessments, How do we do a DPIA?, at ico.org.uk, read 2026-10-18, text
available under the Open Government Licence v3.0; this template reproduces it with that
attribution. The obligation is Article 35 of Regulation 2016/679. The section names in their
imperative form, the table shapes and the audience rule are this skill's own text.
