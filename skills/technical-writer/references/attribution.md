# Attribution

Every source a template or a rule cites, its license, and whether the skill quotes it or
paraphrases it (spec R12). Verbatim text appears only from sources licensed CC BY, Apache-2.0,
MIT, CC0, or the Open Government Licence v3.0 (spec R12 as amended 2026-10-18 13:20 EDT), and
from statutory or standards text. The Splunk Style Guide, the Microsoft
Writing Style Guide, Elastic, New Relic, Software Engineering at Google, and the Mitchell
paper are paraphrased. GitLab and arc42 contribute structure and rule names, not prose, so the
skill inherits no ShareAlike obligation. A source whose license the survey did not record is
treated as paraphrase-only until it is.

## Contents

- [Template sources](#template-sources)
- [Rule sources](#rule-sources)
- [Sources for planned templates](#sources-for-planned-templates)
- [License notes](#license-notes)
- [Related files](#related-files)

## Template sources

The Source column repeats each template's `source` front matter value as the template cites
it, so a reader can match the two without opening the template.

| Template | Source | License and use |
|---|---|---|
| task | Grafana Writers' Toolkit task template (docs/static/templates/task-template.md, grafana/writers-toolkit at 40b4493) | Apache-2.0, quoted |
| concept | Grafana Writers' Toolkit concept template (docs/static/templates/concept-template.md, grafana/writers-toolkit at 40b4493) | Apache-2.0, quoted; the noun-phrase heading rule from the Google developer documentation style guide, CC BY 4.0, quoted |
| reference | Grafana Writers' Toolkit reference template (docs/static/templates/reference-template.md, grafana/writers-toolkit at 40b4493) | Apache-2.0, quoted; the noun-phrase heading rule from the Google developer documentation style guide, CC BY 4.0, quoted |
| multiple-task procedure | Grafana Writers' Toolkit multiple-tasks template (docs/static/templates/multiple-tasks-template.md, grafana/writers-toolkit at 40b4493) | Apache-2.0, quoted |
| tutorial | Grafana Writers' Toolkit tutorial template (docs/static/templates/tutorial-template.md, grafana/writers-toolkit at 40b4493) | Apache-2.0, quoted; the tutorial rules from Diataxis, paraphrased, no license recorded |
| troubleshooting | GitLab Documentation Style Guide, troubleshooting topic type (docs.gitlab.com/development/documentation/topic_types/troubleshooting), structure and section names only; the research holds no quotable troubleshooting template, so the body is house prose | CC BY-SA 4.0 (GitLab), structure and section names only, paraphrased into house prose with no sentence reproduced, so no ShareAlike obligation is inherited; the heading rule cited to the Google developer documentation style guide, Headings and titles, CC BY 4.0, and to Grafana Writers' Toolkit Gerunds.yml, Apache-2.0, both paraphrased |
| release notes | Keep a Changelog 1.1.0 (keepachangelog.com/en/1.1.0) for the guiding principles, the six categories, and the date rule | MIT, quoted |
| architecture decision record | MADR 4.0.0 (adr.github.io/madr) for the sections; Nygard, Documenting Architecture Decisions (2011) for the prose rules; AWS Prescriptive Guidance, ADR process, for the lifecycle | MIT or CC0 (MADR), quoted; Nygard and AWS paraphrased, no license published |
| architecture description | arc42 (docs.arc42.org) for the section names, lean form; C4 model diagram checklist (c4model.com/diagrams/checklist) for the diagram evidence slots | CC BY-SA 4.0 (arc42), section names only, no prose, so no ShareAlike obligation is inherited; CC BY 4.0 (C4), the checklist questions quoted |
| design doc or RFC | Design Docs at Google (Ubl, 2020) for the skeleton; PEP 12, Sample reStructuredText PEP Template, for Backwards Compatibility, Security Implications, Rejected Ideas and Open Issues | Ubl paraphrased, no license stated; PEP 12 public domain or CC0-1.0-Universal by its Copyright section, CC0, the section names quoted |
| postmortem | Google SRE Workbook, postmortem chapter, for the section set and the action item rule; Google SRE book, Postmortem Culture, for the blameless rule | CC BY-NC-ND 4.0 (both), section names and rules paraphrased, no sentence reproduced |
| runbook | this skill's house runbook shape (Prerequisites, Procedure, Verification, Rollback, Escalation) for the section shape; Google SRE book, Monitoring Distributed Systems, for the alerting rules; the research records no canonical runbook template, so the body is house prose over those two inputs | house (the section shape is this skill's own); CC BY-NC-ND 4.0 (SRE book), the alerting rules paraphrased, no sentence reproduced |
| changelog entry | Keep a Changelog 1.1.0 (keepachangelog.com/en/1.1.0) for the file shape, the version heading with its date, the Unreleased section and the entry rule; the six categories by reference to style-rules.md | MIT, quoted |
| endpoint or field description | AIP-192, API documentation (google.aip.dev/192), for the description rules (the first sentence omits the subject and is in the third-person present, brief but complete, the questions a description answers, the Deprecated opener); the page shape is this skill's own | CC BY 4.0 (AIP-192, the page footer read 2026-10-18), quoted; the five sections and the field table are this skill's rules |
| error catalog entry | RFC 9457, Problem Details for HTTP APIs, for the problem details members and the rule for defining a problem type (a type URI, a title, the status code); AIP-193, Errors (google.aip.dev/193), for the message rules and the UPPER_SNAKE_CASE reason | standards (RFC 9457, IETF Trust Legal Provisions), quoted; CC BY 4.0 (AIP-193, the site footer read 2026-10-18), quoted; the four sections and the member table are this skill's rules |
| vulnerability advisory | CVE CNA Operational Rules v4.2.0, rule 5.2, for the description rules (summarize the vulnerability, credit no person or tool, no advertising or irrelevant content) and the CVE-1900- example identifiers; CVSS v4.0 specification (FIRST) for the severity label, the vector string and the rating scale | standards (CVE CNA rules), paraphrased from the survey's record in research/raw-lane-governance.md, the PDF not re-read on 2026-10-18; standards (CVSS v4.0, FIRST, licensed to the public for use with attribution), quoted; the GitHub advisory database's version range syntax, structured fields with no prose, paraphrased; the section set is this skill's own |
| disclosure notification | OpenSSF vulnerability disclosure guide, notification templates (templates/notifications/embargo.md and disclosure.md, ossf/oss-vulnerability-guide at 40ecfe2), for the section set, the embargo terms and the timeline fields | CC BY 4.0, quoted; the variant marker in the title and the Disclosure section are this skill's rules |
| SECURITY.md | OpenSSF vulnerability disclosure guide, SECURITY.md templates (templates/security_policies, ossf/oss-vulnerability-guide at 40ecfe2), for the reporting paragraph, the acknowledgement window and the disclosure timeline | CC BY 4.0, quoted; the four sections and the version table are this skill's rules |
| model card | Hugging Face model card template (huggingface_hub src/huggingface_hub/templates/modelcard_template.md at 926f6d8) for the headings; Mitchell et al., Model Cards for Model Reporting (2019), for the disaggregated results requirement | Apache-2.0 (Hugging Face), quoted; Mitchell paraphrased, ACM copyright |
| system card | Claude Haiku 5.5 system card (Anthropic, October 2026) for the chapter order and the chapter names, structure only; the card's prose is not quoted | all rights reserved (Anthropic); structure and chapter names only, paraphrased into house prose with no sentence reproduced; Reliability of this assessment is lifted from the alignment chapter to a chapter of its own, RSP evaluations is renamed Frontier risk evaluations, and the chapter shape and the audience rule are this skill's own |
| Annex IV technical file | Regulation (EU) 2024/1689 (the AI Act), Annex IV, Technical documentation referred to in Article 11(1), for the nine items as sections and the sub-points of items 1 and 2 as fields and subsections; the text read at artificialintelligenceact.eu/annex/4 on 2026-10-18 | statutory (EU legislation, quoted); the field names, the subsection names and the evidence rules are this skill's own |
| GPAI Model Documentation Form | Model Documentation Form (European Commission, 2025-07-10), Measure 1.1 of the Transparency Chapter of the General-Purpose AI Code of Practice, for the eight sections, the field names, the audience marks and the recommended word counts | statutory (European Commission form, quoted; the DOCX states no license); the parenthesised variant names that split a field by precision and the audience rule are this skill's own |
| privacy notice | WP260 rev.01, Guidelines on transparency under Regulation 2016/679 (Article 29 Working Party, adopted 2017-11-29, revised 2018-04-11), paragraphs 8, 12, 13, 17, 35 and 36, for the layered form, the first layer's content, the plain-language rule and the five qualifiers; Articles 13 and 14 of Regulation 2016/679 for the information the sections carry | statutory (WP260 rev.01 and the GDPR, quoted); the reader-facing section names and the legal-term ban are this skill's own |
| data protection impact assessment | ICO, Data protection impact assessments, How do we do a DPIA? (ico.org.uk, read 2026-10-18), the seven steps as sections and the rules for assessing risk, recording measures and concluding; Article 35 of Regulation 2016/679 for the obligation | Open Government Licence v3.0 (ICO; the page states all text content is available under it), quoted with attribution; statutory (the GDPR); the imperative section names, the table shapes and the audience rule are this skill's own |

## Rule sources

The sources [style-rules.md](style-rules.md), [procedure-rules.md](procedure-rules.md),
[audiences.md](audiences.md) and the Vale rules under `vale/styles/TechnicalWriter/` cite, with
the use each file makes of them.

| Source | License | Use | Cited by |
|---|---|---|---|
| Google developer documentation style guide, including the word list (developers.google.com/style) | CC BY 4.0 | quoted | style-rules.md, the concept, reference, and troubleshooting templates |
| Google Technical Writing One and Two (developers.google.com/tech-writing) | CC BY 4.0 | quoted | style-rules.md |
| Grafana Writers' Toolkit, repository grafana/writers-toolkit at 40b4493: style guide pages, AI quick reference, Vale rules, topic templates | Apache-2.0 for the repository files; the rendered site carries an all-rights-reserved notice, see License notes | quoted | style-rules.md, procedure-rules.md, the task, concept, reference, multiple-task procedure, tutorial, and troubleshooting templates; the Vale rules Gerunds.yml (regex and message quoted), Timeless.yml (message quoted), ReferTo.yml (message form quoted, the swap reversed) and Subjective.yml (after Simple.yml, message in our words) |
| Splunk Vale ruleset, repository splunk/vale-splunk-style-guide | Apache-2.0 | quoted | style-rules.md; the Vale rules Recommendations.yml, Dashes.yml and Subjunctive.yml (after the Splunk rules, token lists reused, messages in our words) |
| Google Vale package, repository errata-ai/Google (the Google developer documentation style guide as Vale rules) | MIT (the repository license, read 2026-10-18) | configuration only: `vale/.vale.ini` names the package and `vale sync` fetches it into `vale/styles/Google/`, which is never committed; no rule text is copied | vale/.vale.ini |
| Keep a Changelog 1.1.0 (keepachangelog.com/en/1.1.0) | MIT | quoted | style-rules.md, the release notes and changelog entry templates |
| Splunk Style Guide (help.splunk.com) | all rights reserved | paraphrased | style-rules.md |
| Microsoft Writing Style Guide (learn.microsoft.com/style-guide) | no reuse license published | paraphrased | style-rules.md |
| Red Hat supplementary style guide | no license recorded | paraphrased | style-rules.md |
| Kubernetes style guide | not recorded in the survey | paraphrased | style-rules.md |
| Datadog documentation repository AGENTS.md | Apache-2.0 | paraphrased | style-rules.md, Conflict picks |
| Nygard, Documenting Architecture Decisions (2011) | no license published | paraphrased | style-rules.md, the ADR template |
| AWS Prescriptive Guidance, ADR process | AWS site terms | paraphrased | style-rules.md, the ADR template |
| Diataxis (diataxis.fr) | not stated | structure only, the classification split; the tutorial rules paraphrased | taxonomy.md, the tutorial template |
| WP260 rev.01, Guidelines on transparency under Regulation 2016/679 (Article 29 Working Party, 2018) | statutory | quoted | style-rules.md, audiences.md |
| GPAI Model Documentation Form (European Commission, 2025) | statutory | quoted | audiences.md |

## Sources for planned templates

Every type in spec R2's table has a shipped template as of 2026-10-18, so this
section holds no rows; each source it once listed now sits in the Template sources table above
with the license and use the shipped template records. A type added to the taxonomy later
lists its source here until its template ships.

## License notes

Grafana. The repository LICENSE is Apache-2.0 with no documentation carve-out, and the
grafana.com copyright notice says all Grafana Labs documentation is all rights reserved. The
skill reads the Apache grant as covering the Markdown source distributed in the repository,
cites the repository and commit rather than the site, and keeps the question for
docs@grafana.com for the point at which the skill is promoted to the org marketplace.

Splunk. The Vale ruleset is Apache-2.0 and its rule messages are quoted; the style guide text
on help.splunk.com is all rights reserved and is paraphrased.

ShareAlike. GitLab's documentation and arc42 are CC BY-SA 4.0. The skill takes section names
and rule names from them and writes its own prose, so no file here is a derivative work.

No derivatives. Software Engineering at Google and the SRE books are CC BY-NC-ND 4.0; Elastic
is CC BY-NC-ND and New Relic CC BY-NC-SA. Ideas are paraphrased; no sentence is reproduced.

Unrecorded. Where the survey recorded no license (Kubernetes, Red Hat, Diataxis, Ubl), the
source is paraphrased until a later step reads and records the license here. The survey did
not record AIP's license either; the google.aip.dev footer, read 2026-10-18, licenses the page
content CC BY 4.0 and its code samples Apache-2.0, so AIP-192 and AIP-193 are quoted.
PEP 12's license is not in the survey either; its own Copyright section places it in the public
domain or under CC0-1.0-Universal, whichever is more permissive, and the template cites that.

## Related files

- [taxonomy.md](taxonomy.md): the types each source serves and their template status.
- [style-rules.md](style-rules.md): the rules, each ending with its source and license.
