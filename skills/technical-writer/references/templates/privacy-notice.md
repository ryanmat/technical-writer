---
type: privacy notice
domain: privacy
default_audience: data subject
source: WP260 rev.01, Guidelines on transparency under Regulation 2016/679 (Article 29 Working Party, adopted 2017-11-29, revised 2018-04-11), paragraphs 8, 12, 13, 17, 35 and 36, for the layered form, the first layer's content, the plain-language rule and the five qualifiers; Articles 13 and 14 of Regulation 2016/679 for the information the sections carry
license: statutory (WP260 rev.01 and the GDPR, quoted)
h1_pattern: '(?i)^privacy notice\b'
sections:
  - heading: At a glance
    level: 2
    evidence:
      pattern: '(?i)\bright'
      missing: the data subject's rights, which WP260 paragraph 36 puts in the first layer with the purposes and the controller
  - heading: Who we are
    level: 2
    evidence:
      pattern: '[\w.+-]+@[\w-]+\.[\w.-]+|https?://\S+|\b\d+ [A-Z][\w-]+ (?:Street|Road|Avenue|Lane|Square|Place|Way)\b'
      missing: a way to reach the controller, an email address, a URL or a postal address
  - heading: What we use your data for
    level: 2
    evidence:
      pattern: '(?i)\b(?:contract|consent|legal obligation|legitimate interests?|vital interests?|public task|public interest)\b'
      missing: the legal basis for each purpose, in the GDPR's words
  - heading: Who we share your data with
    level: 2
  - heading: Where your data goes
    level: 2
  - heading: How long we keep your data
    level: 2
    evidence:
      pattern: '(?i)\b\d+\s*(?:days?|weeks?|months?|years?)\b|\b(?:until|for as long as|as long as|when you)\b'
      missing: a retention period in everyday units, or the criterion that decides it
  - heading: Your rights
    level: 2
  - heading: How to complain
    level: 2
    evidence:
      pattern: '(?i)\b(?:supervisory|data protection) (?:authority|commission(?:er)?)\b|\bcommissioner\b|https?://\S+|[\w.+-]+@[\w-]+\.[\w.-]+'
      missing: the supervisory authority or a complaint contact
  - heading: Where your data comes from
    level: 2
    optional: true
  - heading: Changes to this notice
    level: 2
    optional: true
length_caps:
  data subject: 900
  regulator: 2500
  executive: 300
banned_patterns:
  - pattern: '(?i:\b(?:might|some|often|possible)\b)|\bmay\b'
    rule: 'no language qualifier; WP260 paragraph 13 says "may", "might", "some", "often" and "possible" should be avoided in a privacy notice, and a writer who cannot avoid one records why in the notes to the controller'
  - pattern: '(?i)\b(?:data subjects?|controllers?|pursuant to|hereinafter|aforementioned|notwithstanding)\b'
    rule: no legalistic or specialist term in the notice; WP260 paragraph 13 says the information should not contain overly legalistic, technical or specialist language, so the notice says you, we and the company that handles data on our behalf
---
# Privacy notice for <WHAT_THE_NOTICE_COVERS>

A privacy notice tells the people whose data an organisation processes what it does with the
data, why, for how long, who else sees it, and what they can do about it: the information
Articles 13 and 14 of the GDPR require, written as WP260 rev.01 requires, in a "concise,
transparent, intelligible and easily accessible form, using clear and plain language". The
notice is layered: the first section is the first layer, the overview a reader takes in on
one screen, and the sections after it are the full notice, kept in the same document because
WP260 paragraph 17 says "the entirety of the information addressed to data subjects should
also be available to them in one single place or one complete document". The front matter
above is what `check_structure.py` enforces, at the one heading level the template declares,
so a level-two heading the list does not name is a finding.

## Register

The reader is the person whose data is processed, addressed as you; the organisation is we.
WP260 paragraph 12 says the information "should be concrete and definitive; it should not be
phrased in abstract or ambivalent terms or leave room for different interpretations", and
paragraph 13 says "Language qualifiers such as "may", "might", "some", "often" and "possible"
should also be avoided", that "Writing should be in the active instead of the passive form",
and that the information "should not contain overly legalistic, technical or specialist
language or terminology". The checker bans the five qualifiers and the common legal terms;
retention is written in everyday units; and a fact the sources do not give is the marker, not
a qualifier. Where a qualifier cannot be avoided, the writer records why in the notes to the
controller, since paragraph 13 asks the controller to be able to demonstrate it.

## Title

`# Privacy notice for <WHAT_THE_NOTICE_COVERS>`, the H1 and the only H1, opening with the
words Privacy notice, followed by one sentence that says who the notice is for and what it
tells them.

## At a glance

Required. The first layer: WP260 paragraph 36 says it "should include the details of the
purposes of processing, the identity of controller and a description of the data subject's
rights" and "information on the processing which has the most impact on the data subject and
processing which could surprise them". One paragraph a reader finishes on one screen, naming
who is responsible, what the data is used for, that the reader has rights and where the full
notice is. Evidence slot: the word right or rights.

## Who we are

Required. The organisation responsible for the data, by name, and how to reach it and its
data protection officer when it has one. Evidence slot: an email address, a URL or a postal
address.

## What we use your data for

Required. One bullet per purpose: the data it uses, what it is for, and the legal basis in the
GDPR's words (contract, consent, legal obligation, legitimate interest, vital interest, public
task). Paragraph 12's good practice example is the model: say what the data does, not that it
helps to develop services. Evidence slot: a legal basis named.

## Who we share your data with

Required. The categories of organisation that receive the data and why, and the statement
that the data is not sold when that is the case.

## Where your data goes

Required. Where the data is processed, and, for a transfer outside the reader's country or
the European Union, the country and the safeguard in plain words; the statement that the data
stays where the reader is when that is the case.

## How long we keep your data

Required. One bullet per category of data with its period in days, months or years, or the
event that ends it. Evidence slot: a period in everyday units or the criterion. A period the
sources do not give is the marker, and so is one the sources call not yet set or under review:
the bullet carries `[UNVERIFIED: the retention period for <category>, which <who> has not set]`,
never a sentence telling the reader the period is unset.

## Your rights

Required. The rights in plain words: to see, correct, delete, limit, move and object, and to
withdraw consent where consent is the basis; how to use them and how long the answer takes.

## How to complain

Required. Who to write to first, and the supervisory authority the reader can complain to,
named. Evidence slot: the authority or a complaint contact.

## Where your data comes from

Optional. Required when any of the data did not come from the reader (Article 14): the source
of each such category.

## Changes to this notice

Optional. How the reader learns of a change, and the date of this version.

## Audience

The default audience is the data subject, who gets no technical or legal vocabulary and a
notice short enough to read; the first layer fits one screen and the whole notice fits the
data subject cap. A regulator, the supervisory authority reading the notice against Articles
13 and 14, gets the same sections with every category and basis stated within the regulator
cap. An executive gets the first layer within the executive cap. The caps count words outside
code blocks.

## Source

The layered form, the first layer's content, the plain-language rule and the five qualifiers:
WP260 rev.01, Guidelines on transparency under Regulation 2016/679, Article 29 Working Party,
adopted 29 November 2017 and revised 11 April 2018, paragraphs 8, 12, 13, 17, 35 and 36,
quoted, from the PDF the survey read (no copyright or licence clause in the text; a public
authority's guidance). The information each section carries follows Articles 13 and 14 of the
GDPR. The section names, written for the reader, and the legal-term ban are this skill's own
text.
