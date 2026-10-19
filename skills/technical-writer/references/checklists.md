# Checklists

The checks the skill runs by hand before it returns a document, and the checks review mode
(spec R8) walks when it reads one. The checker, `scripts/check_structure.py`, covers the
section structure, the evidence slots, the H1, the summary line, the length cap, the four
procedure rules, and the regular-expression bans; everything here is what it cannot judge, or
what to look at when it cannot run. Run the checker first when the session can, then the
checklist for the document's type, then the two checklists every type shares.

## Contents

- [Task](#task)
- [Concept](#concept)
- [Reference](#reference)
- [Multiple-task procedure](#multiple-task-procedure)
- [Tutorial](#tutorial)
- [Troubleshooting](#troubleshooting)
- [Release notes](#release-notes)
- [Architecture decision record](#architecture-decision-record)
- [Architecture description](#architecture-description)
- [Design doc or RFC](#design-doc-or-rfc)
- [Postmortem](#postmortem)
- [Runbook](#runbook)
- [Changelog entry](#changelog-entry)
- [Endpoint or field description](#endpoint-or-field-description)
- [Error catalog entry](#error-catalog-entry)
- [Vulnerability advisory](#vulnerability-advisory)
- [Disclosure notification](#disclosure-notification)
- [SECURITY.md](#securitymd)
- [Model card](#model-card)
- [System card](#system-card)
- [Annex IV technical file](#annex-iv-technical-file)
- [GPAI Model Documentation Form](#gpai-model-documentation-form)
- [Privacy notice](#privacy-notice)
- [Data protection impact assessment](#data-protection-impact-assessment)
- [Structure, every type](#structure-every-type)
- [Prose, every type](#prose-every-type)
- [Evidence, every type](#evidence-every-type)
- [Review mode](#review-mode)

## Task

The template is [templates/task.md](templates/task.md); the procedure rules are in
[procedure-rules.md](procedure-rules.md).

- Title: a bare infinitive with its object, the goal the reader reaches, never a gerund and never How to.
- Summary line: one sentence directly under the title saying what the task is and why the reader does it; a long introduction means a concept topic is missing.
- Before you begin: the version or edition, the permission or role, the license, and any task to finish first, each as a parallel sentence or fragment; the evidence slot requires one of version, permission, or license.
- Steps: a stem sentence beginning with To directly before step 1; one action per step; at most 20 words in the action sentence; an expected result after any step whose outcome is not obvious; a warning or caution before the step it protects.
- Steps: every code block has one command and the expected output follows any command whose output the reader uses.
- Next steps: when present, what the reader does with the result, as links to the next task or the concept behind it; never a restatement of what they just did.
- Headings: no gerund headings and no Step N headings anywhere in the topic; the checker bans both.
- Length: 1500 words outside code blocks for engineers, 500 for executives.

## Concept

The template is [templates/concept.md](templates/concept.md).

- Title: a noun phrase naming the product or feature, never a gerund opener, never How to, What is, or Using; at least two words.
- Summary line: one sentence under the title stating the purpose or main point of the feature; the paragraphs before the first section carry the rest of the introduction and the why.
- Body sections: at least one level-two section the writer names as a noun phrase; each explains what and why, never how; no numbered procedure and no field-by-field table, which belong in the task or reference topic.
- Claims: every behavior, default, or limit traces to a source; a fact the sources do not give carries the marker in place of the claim, since the template declares no evidence slot to catch it.
- Useful links: when present, last; the task that uses the concept and the reference that lists its settings, with the exact title of the linked page as the link text.
- Headings: no -ing opener and no How to anywhere in the topic; the checker bans both.
- Length: 1500 words outside code blocks for engineers, 500 for executives.

## Reference

The template is [templates/reference.md](templates/reference.md).

- Title: a noun phrase naming the product and the kind of thing listed, never a gerund opener, never How to, What is, or Using; at least two words.
- Summary line: one sentence under the title saying what the page lists and when the reader uses it.
- Introduction: the version or source the values hold for, stated before the first table; the evidence slot on the introduction requires a version number, the word version, sourced from, taken from, or as of, and the marker when the sources give none.
- Body sections: at least one level-two section the writer names for the kind of thing it lists; each opens with one sentence saying what the table or list holds; rows sorted alphabetically unless the source fixes an order.
- Tables: one row per item, the name as the source spells it, the default, and what it does; a default the sources do not give is the marker in the cell.
- API documentation: when present, last; a document that is only an endpoint or field description is its own type.
- Headings: no -ing opener and no How to anywhere in the topic; the checker bans both.
- Length: 3000 words outside code blocks for engineers, table rows included, 500 for executives.

## Multiple-task procedure

The template is [templates/multiple-task-procedure.md](templates/multiple-task-procedure.md);
the procedure rules are in [procedure-rules.md](procedure-rules.md).

- Title: a bare infinitive with its object, naming the goal the tasks reach together, never the first task alone, never a gerund and never How to.
- Summary line: one sentence under the title saying what the procedure achieves and why; the numbered list of task links follows it, one item per task section, in order.
- Before you begin: the one prerequisites section for the whole document; the version or edition, the permission or role, the license, and any task to finish first; the evidence slot requires one of version, permission, or license.
- Task sections: two or more, each a bare infinitive, in the order the introduction lists them; each opens with a stem sentence beginning with To; one action per step; at most 20 words in the action sentence; an expected result after any step whose outcome is not obvious; a warning or caution before the step it protects; the checker applies these rules to every task section.
- Optional tasks: a heading beginning with Optional: and a first sentence saying when to perform the task.
- Commands: one command per code block under its step, and the expected output after any command whose output the reader uses.
- Verify: last, with a heading beginning with Verify; a procedure when it has steps, under the same rules, which the checker does not apply here.
- Headings: no gerund headings and no Step N headings anywhere in the topic; the checker bans both.
- Length: 3000 words outside code blocks for engineers, 500 for executives.

## Tutorial

The template is [templates/tutorial.md](templates/tutorial.md); the procedure rules are in
[procedure-rules.md](procedure-rules.md).

- Title: a bare infinitive with its object, naming what the learner builds, never a gerund and never How to.
- Summary line and overview: one sentence under the title; the overview names the result the learner has at the end, in one concrete picture, and limits concepts to the tasks at hand.
- Before you begin: the one prerequisites section; the version or edition, the permission or role, the license, and any task to finish first; the evidence slot requires one of version, permission, or license.
- Task sections: two or more, each a bare infinitive, in the order the learner performs them; a stem sentence beginning with To; one action per step; at most 20 words in the action sentence; an expected result after any step whose outcome is not obvious; the first task produces a visible result early; the checker applies the procedure rules to every task section.
- One path: no options or alternatives inside the steps; every step works as written on the stated version, in order, every time; explanation is the minimum the step needs.
- Commands: one command per code block under its step, and the expected output after any command whose output the reader uses.
- Summary: one bullet per task section, in order, then one sentence on what the result lets the learner do.
- Next steps: last; the task topics the learner can do next, the concept behind the exercise, and the reference that lists the settings, each with the exact title of the linked page.
- Headings: no gerund headings and no Step N headings anywhere in the topic; the checker bans both.
- Length: 3000 words outside code blocks for engineers, 500 for executives.

## Troubleshooting

The template is [templates/troubleshooting.md](templates/troubleshooting.md); the procedure
rules for a Resolution with steps are in [procedure-rules.md](procedure-rules.md).

- Title: Troubleshoot with the feature, or a noun phrase naming the feature's errors; never the gerund Troubleshooting, never How to; at least two words.
- Summary line: one sentence under the title saying what the page fixes and where the reader sees the symptoms.
- Entries: one level-two section per symptom, named by the message the reader sees, opening with Error: or Warning: when there is a type, the message in code style; the most common first; five or more entries make a page of their own.
- Symptom: what the reader sees and nothing else; the exact message, the page state, the command and what it printed; a message the sources do not give verbatim is the marker.
- Cause: why it happens, testable against the reader's system; several causes each with the check that tells them apart; every default, limit, or timeout traces to a source or is the marker.
- Resolution: resolution for a permanent fix, workaround for a temporary one, and which it is; a To stem when it has steps; one command per code block with its expected output after it, which the evidence slot reads for the first entry; a Warning: before any command that changes data.
- Every entry after the first: the same three sections in the same order, which the checker does not read.
- Related: when present, last; the concept, the task, and the reference, each with the exact title of the linked page.
- Headings: no -ing opener and no How to anywhere in the topic; the checker bans both.
- Length: 3000 words outside code blocks for engineers, 500 for executives.

## Release notes

The template is [templates/release-notes.md](templates/release-notes.md).

- Title: the product and release notes, or What's new in the product; the version may appear, since the page is dated content; at least two words.
- Summary line: one sentence under the title naming what the release adds, changes, and fixes.
- Version sections: one level-two heading per released version, the latest first, the version alone in the heading in the form [2.5.0], with [YANKED] after it for a pulled release; no Unreleased section, which belongs to the changelog and which the checker reports as unknown.
- Release line: the first line under the version heading carries the date as YYYY-MM-DD, states whether the project follows Semantic Versioning, and counts the breaking changes; a date the sources do not give is the marker on that line, which the evidence slot reads for the first version.
- Categories: only Added, Changed, Deprecated, Removed, Fixed, and Security at level three, in that order, each present only when it has entries; a change that fits none is Changed; the checker reports any other level-three heading as unknown.
- Entries: one bullet per notable change in the reader's terms, closing with the issue, pull request, or commit in parentheses as plain text or link text, or carrying the marker; an identifier in code style is blanked before the check and counts as missing.
- Breaking changes: an entry that breaks compatibility opens with Breaking: in bold under Changed or Removed and says what the reader must do; a deprecation names the version in which the removal lands, never soon.
- Every version after the first: the same shape; the checker reads its categories and entries but not its release line.
- Length: 2000 words outside code blocks for engineers, 400 for executives.

## Architecture decision record

The template is
[templates/architecture-decision-record.md](templates/architecture-decision-record.md).

- Title: the decision as a short noun phrase, numbered NNNN- when the project numbers its records; a title the user gave stays as given.
- Summary line: one sentence under the title stating the decision taken.
- Status: one of proposed, accepted, rejected, or superseded by NNNN, with the ISO date it took effect; an accepted record is never edited afterwards, it is superseded.
- Context and Problem Statement: prose, two to three paragraphs, the forces in play and the question being decided; no bullet fragments here.
- Decision Drivers: when present, a list of the forces, each a phrase the options are judged against.
- Considered Options: a list naming every option weighed, including the one chosen.
- Decision Outcome: opens with a Chosen option line naming the option and the reason it won over the others, in prose.
- Consequences, Confirmation, Pros and Cons of the Options, More Information: optional; when present, in that order, each at level two, with per-option headings under Pros and Cons at level three.
- Length: 1200 words outside code blocks for engineers, 400 for executives; one to two pages is the target.

## Architecture description

The template is
[templates/architecture-description.md](templates/architecture-description.md).

- Title: the system's name followed by architecture description; a title the user gave stays as given.
- Summary line: one sentence under the title saying what the system does.
- Introduction and Goals: what the system is for, the quality goals ranked as the team ranks them, and the stakeholders with what each expects; a goal the sources do not quantify carries the marker in place of the figure.
- Context and Scope: the boundary and what crosses it; opens with a Diagram: line naming the diagram's title, its C4 type, its scope and its key; the checker reads the word diagram followed by the word key.
- Solution Strategy: the few decisions that shape the whole, one paragraph each, pointing to the decision record when one exists.
- Building Block View: each container or component with its name, its technology in brackets and what it does; opens with a Diagram: line as Context and Scope does.
- Runtime View and Deployment View: when present, each opens with a Diagram: line; a sizing figure carries its source or the marker.
- Quality Requirements: each goal from the introduction made testable, with the measurement taken or the marker.
- Risks and Technical Debt: the known problems ranked by the team, each with its cost and the plan for it.
- Constraints, Crosscutting Concepts, Architecture Decisions, Glossary: optional, in arc42's order; headings stay as arc42 names them.
- Diagrams: a drawn diagram stands under its statement, never in place of it; every element has a name, a type and a description, every line has a label and an arrow head, and every acronym is in the Glossary (the C4 diagram checklist).
- Facts once: each fact lives in the view that owns it (goals in the introduction, the boundary in Context and Scope, decisions in Solution Strategy, technologies in Building Block View, counts in Deployment View, measurements in Quality Requirements), and a later section names the block or section in a clause instead of restating it; no sentence names the reader, counts the blocks ahead of their list, or previews a later section.
- Length: 3000 words outside code blocks for engineers, 600 for executives.

## Design doc or RFC

The template is [templates/design-doc-or-rfc.md](templates/design-doc-or-rfc.md).

- Title: what the design does, for which system; a project that numbers its RFCs puts the number first; a title the user gave stays as given.
- Summary line: one sentence under the title saying what the design changes and why; a summary that can name no trade-off means no document is needed.
- Context and Scope: the system as it is, the problem, and the boundary of the change, as facts with their sources; no argument for the design yet.
- Goals and Non-goals: goals a reader can check; non-goals that could reasonably have been goals, each with where it went or why not; a negated goal is not a non-goal.
- Design: the change at the level a reviewer needs, in prose and diagrams; no pasted schemas or code; a value the sources do not give carries the marker.
- Alternatives Considered: one paragraph per competing design, each named and said to be rejected with its reason; the evidence slot reads rejected, ruled out, not chosen, set aside or declined, and the marker when the sources name no alternative.
- Cross-cutting Concerns: when present, one short paragraph per concern the design touches.
- Backwards Compatibility and Security Implications: what breaks and the migration; the new exposure and what bounds it; None. is a complete section when there is nothing, written out.
- Rejected Ideas: the review suggestions set aside with their reasons, kept apart from the competing designs above.
- Open Issues: when present, one line per question left for review or the build.
- Facts once: the problem in Context and Scope, the mechanism and its values in Design, the competing designs in Alternatives Considered, what breaks in Backwards Compatibility; Cross-cutting Concerns and Rejected Ideas add to those sections and never repeat them, a later section names an earlier one in a clause, and no sentence restates a goal or points elsewhere without adding something.
- Length: 3000 words outside code blocks for engineers, 600 for executives; one to three pages for a mini design doc.

## Postmortem

The template is [templates/postmortem.md](templates/postmortem.md).

- Title: the system, what happened and the date; a title the user gave stays as given.
- Summary line: one sentence under the title saying what stopped, for how long and why.
- Summary: the incident in one paragraph for a reader who reads nothing else.
- Impact: the duration and a count of who or what was reached, each a figure with its source, or the marker for a count the sources do not give; the evidence slot reads a duration unit and a count unit.
- Root causes and trigger: the conditions in the system, each about a component or a process, then the one event that set them off, in a closing sentence with its time.
- Timeline and recovery: one entry per event in order, each opening with an ISO timestamp and its zone, facts only; then one paragraph naming the action that ended the incident by its entry and what cleared its effects.
- Detection: how the incident was noticed, how long that took, and which signal fired or did not.
- Action items: one sentence per fix ending (owner: <role or team>, priority: P<n>, <tracker id>); one owner each, a role or a team, never a name; systemic fixes before behavior changes; a missing tracker id is the marker.
- Lessons learned: what went well, what went poorly, where we got lucky, each point tracing to the timeline or a cause.
- Facts once: the window and the loss in Summary, the counts in Impact, the conditions and the event in Root causes and trigger, the times and the ending action in Timeline and recovery, the signals in Detection; the trigger is one sentence, the recovery paragraph points at its entry, and a lesson is a judgment that names its entry or cause rather than restating it.
- Blameless: no person's judgment named as the cause; the checker bans careless, negligent, should have, blame and at fault, and the by-hand read catches the same stance in other words; no end-user identifiers anywhere.
- Length: 2500 words outside code blocks for engineers, 500 for executives.

## Runbook

The template is [templates/runbook.md](templates/runbook.md); the procedure rules are in
[procedure-rules.md](procedure-rules.md) and bind the Mitigation steps in the checker and the Diagnosis steps by hand.

- Title: Runbook, a colon, the system and the condition as the alert names it; a title the user gave stays as given.
- Summary line: one sentence under the title saying what the runbook restores and how.
- Alert or trigger: the alert's exact name, its condition with the threshold and the duration, and the labels the steps use; a page the operator can act on, or the statement that the alert is the bug.
- Impact: what users and dependent systems see and what is at risk, two to four sentences, figures sourced or marked.
- Prerequisites: the tool and version, the access or role, the environment, the credential, one item each; the evidence slot reads a version, access, role, credential or tool statement.
- Diagnosis: a stem sentence and numbered steps, one command or check each, with the exact output that points at each cause as the first sentence after the code block, opening with a lowercase verb.
- Mitigation: the procedure section; a stem sentence beginning with To; one action per step, at most 20 words; a condition before the action it governs; a command in its own code block with its expected output after it as the step's last sentence, nothing after it inside the step; a warning as its own paragraph before the numbered step it protects, never inside it; where moved data goes stated in Rollback, not in the step; steps ordered from the cheapest reversible action to the most expensive; a rote step named as automated or as the item that will automate it.
- Verification: the command or dashboard with the exact value that confirms the condition is gone and how long to wait; the alert resolving is never the only check.
- Rollback: when present, how to undo a step that moved data and where the data is until then.
- Escalation: the rotation, team or channel and the condition or the time after which to escalate, stated once here while Diagnosis says go to Escalation; a time the sources do not give is the marker.
- Headings: no Step N headings; the checker bans them.
- Length: 1500 words outside code blocks for operators and engineers, 400 for executives.

## Changelog entry

The template is [templates/changelog-entry.md](templates/changelog-entry.md); the category list is in [style-rules.md](style-rules.md#change-categories).

- Title: the project name and changelog, the file's own title; a title the user gave stays as given.
- Summary line: one sentence under the title saying what the file documents.
- Version section: one level-two heading per version in the entry, newest first, in the form [2.5.1] - 2026-10-17 with [YANKED] after the date for a pulled release, or [Unreleased] with no date; an undated version heading is an unknown section; a date the sources do not give means the entry goes under Unreleased.
- Categories: only the six from style-rules.md at level three, in that order, each present only when it has entries; a change that fits none is Changed; the checker reports any other level-three heading as unknown.
- Entries: one bullet per noteworthy difference, in the reader's terms, closing with the issue, pull request or commit in parentheses as plain text or link text, or carrying the marker; an identifier in code style is blanked before the check and counts as missing; the version section's evidence slot reads for at least one identifier.
- Breaking changes: an entry that breaks compatibility opens with Breaking: in bold under Changed or Removed and says what the reader must do.
- Length: 2000 words outside code blocks for engineers, 400 for executives.

## Endpoint or field description

The template is [templates/endpoint-description.md](templates/endpoint-description.md).

- Title: the HTTP method in capitals and the path for an endpoint, or the field's name as the schema spells it for a field, with no code style; a title the user gave stays when it has that form.
- Summary line: one sentence under the title with its subject omitted and its verb in the third-person present (Registers a route and returns it with its identifier).
- Summary: the side effects, whether the call is idempotent, the scope or permission it needs, the units and accepted range, in that order and only the ones the sources give; nothing the summary line already states; a deprecated call or field opens with Deprecated: and the alternative or the reason.
- Request: a table with Field, Type, Required, Default and Description columns in that order; no empty cell, since the checker reads the header row only; Default is the value, none for a required field, or the marker when the sources say a default exists and withhold it; every Description cell opens with its verb or its noun, never This field, which the checker bans; a constraint carries its figure; a call with no body says so and tables its parameters instead.
- Response: the success status code first in the form 201 Created, then a Field, Type and Description table or the sentence that there is no body; a server-assigned field says so; an echoed field is marked echoed and not described again.
- Errors: a Status, Error and When table, one row per error the sources give, the identifier as the error catalog spells it, no resolution text; the evidence slot reads for a 4xx or 5xx code.
- Example: one request and its response, or one example value, in fenced code blocks, the values taken from the sources and never invented; reserved identifiers and example.com hosts, no credential.
- Units and bounds: every figure with its unit, every range with both bounds or its one bound and the behavior at it.
- Length: 1500 words outside code blocks for engineers and downstream providers, 300 for executives.

## Error catalog entry

The template is [templates/error-catalog-entry.md](templates/error-catalog-entry.md).

- Title: the problem type's title, two or more words, no code style, no status code and no reason in it; a title the user gave stays when it has that form.
- Summary line: one sentence under the title saying what the server rejects or fails and what the caller does, subject omitted, verb in the third-person present.
- Problem details: a Member and Value table with type (a URI), status (the code), title (the H1's words) in that order, then reason in UPPER_SNAKE_CASE and domain when the API follows AIP-193; detail and instance are not rows; the evidence slot reads the three required rows.
- Cause: the condition in the caller's terms and the calls that return it; no exception class, stack frame, file, line, host or component name the caller cannot see; a cause the sources name and do not describe is the marker.
- Resolution: the action first, the call or field it uses second, one paragraph per condition when they differ, and one sentence on whether a retry of the same request can succeed.
- Example response: the status line, the application/problem+json content type and the body with type, title, status, detail and instance, in a fenced code block, from a capture or fixture in the sources; a value a client needs is a member of its own, never a phrase inside detail; example.com hosts and reserved identifiers.
- Length: 800 words outside code blocks for engineers and downstream providers, 200 for executives.

## Vulnerability advisory

The template is [templates/vulnerability-advisory.md](templates/vulnerability-advisory.md); the procedure rules in [procedure-rules.md](procedure-rules.md) bind any numbered mitigation steps by hand.

- Title: the product, the component and the flaw in plain words; no identifier, no severity, no code style; a title the user gave stays when it has that form.
- Summary line: one sentence under the title with the flaw type, the component, who can do what, the affected range and the fixed version.
- Summary: the CVE identifier as the record writes it, or the sentence that one is requested or not assigned, then one paragraph with the product and component, the type or cause with its CWE when given, and the trigger; it credits no person and no tool, carries no advertising, no thanks and no diligence sentence, and contradicts no other section; an example identifier is in the CVE-1900- range.
- Affected versions: exact bounds, lower bound first, operators with one space (>= 2.4.0, < 2.5.1) or the same bounds in words; one line per product or package; a lower bound omitted only when every earlier version is affected and the text says so; a bound the sources do not give is the marker.
- Severity: the rating, the score and its CVSS-B, CVSS-BT, CVSS-BE or CVSS-BTE label on the first line, the CVSS:4.0/ vector string after it, the rating on the specification's scale; one sentence that a Base score is not the deployment's risk when only CVSS-B is given; a score, vector or label the sources do not give is the marker, never computed.
- Description: the code path or configuration, the input that reaches it, the check that fails, the versions the path exists in; searchable identifiers; no exploit code; the Summary's facts named in a clause, not repeated.
- Impact: what an actor gains under which preconditions, matching the vector's privilege, network and interaction metrics; one paragraph per outcome; no worst case the sources do not establish.
- Remediation: the fixed version and where to get it first, then the mitigation for a system that cannot upgrade as numbered steps when there is more than one action or the sentence that none exists, then the check that confirms the fix; a mitigation the sources mention and do not give is the marker.
- Credits: present only when the sources name somebody; name and affiliation as they asked, one line each; the only section that names a person.
- References: one public reference per line, the fix release or commit, the record, the issue; the evidence slot reads for a URL.
- Length: 1200 words outside code blocks for operators, 1500 for engineers, 300 for executives.

## Disclosure notification

The template is [templates/disclosure-notification.md](templates/disclosure-notification.md); the two forms, embargo and public, share it.

- Title: Embargoed notification: or Public disclosure: followed by the product and the flaw in plain words; the opening words are the variant and appear nowhere else but the Disclosure terms.
- Summary line: one sentence under the title with the flaw type, the product, the range and, under embargo, the disclosure date or, in public, the fixed version; under embargo the quoted confidentiality paragraph follows it, in public nothing does.
- Summary: one technical paragraph the vendor can assess the bug from, then the bold CVE, Affected versions and Reporter lines; the range with both bounds, lower bound first; the reporter as they asked to be named or the statement that they asked not to be; an example identifier is in the CVE-1900- range.
- Severity: the rating word with the motivation or attack scenario; a CVSS score only with its vector phrase, both from the sources or neither.
- Proof of concept: the commands or code that reproduce the issue in a fenced block, the observed result after it; example.com hosts, reserved identifiers, no credential; a reproduction the sources do not give is the marker, never an exploit written by the skill.
- Remediation and mitigation: under embargo, the planned patch with when or where it will be available; in public, the fixing version; a mitigation after the fix when one exists; a missing date, link or version is the marker.
- Further analysis: present only when there is context the other sections do not hold; in public, exploitation in the wild when the sources say so.
- Timeline: the bold Date reported, Date fixed and Date to be disclosed or Date disclosed lines with ISO 8601 dates, a marker for any date the sources do not give, the communication summary after them when given.
- Disclosure: under embargo, the disclosure date with time and time zone, the contact for questions and the quoted closing terms; in public, the disclosure date and the advisory link; the evidence slot reads for a date and an address or a link.
- Length: 1200 words outside code blocks for operators, 1500 for engineers, 300 for executives.

## SECURITY.md

The template is [templates/security-md.md](templates/security-md.md).

- Title: the project name and security policy, or security policy alone; no date, no version.
- Summary line: one sentence under the title with where a report goes, how fast the project answers and the disclosure timeline.
- Supported versions: a Version and Supported table, newest first, every line the project will fix, yes, no or the end date in the Supported cell; a status the sources do not give is the marker.
- Reporting a vulnerability: the address or the form, the form first when the project prefers it, the four things a report carries (the issue, the steps, the affected versions, known mitigations), the acknowledgement window in working days as the sources give it, what follows the acknowledgement, and a key for encrypted reports with its fingerprint or the marker; the evidence slot reads for an address or URL and a number of days or hours.
- Disclosure policy: the timeline in days, what the project does during it, whether and how the reporter is credited, and what happens when the fix needs longer; RFC 2119 words keep their sense here.
- Security updates: the version line a fix lands in first, the advisory channel, the release notes and any list or feed, each with its link; nothing about past issues.
- Voice: second person, the reporter is the reader; no diligence statement, no thanks in advance.
- Length: 800 words outside code blocks for engineers and operators, 200 for executives.

## Model card

The template is [templates/model-card.md](templates/model-card.md).

- Title: Model Card for followed by the model's identifier, the upstream form.
- Model Details and Model Description: the Developed by and License fields each carry a value; Funded by, Shared by, Model type, Language, and Finetuned from carry values or the marker; Model Sources is optional.
- Uses, Direct Use, and Out-of-Scope Use: the intended users and uses, then what the model is not for and what counts as misuse; Downstream Use is optional and names the systems the model is meant to be integrated into.
- Bias, Risks, and Limitations with its Recommendations: the known failure modes by group or input, and what a deployer does about each.
- How to Get Started with the Model: a code block the reader can run, or the marker.
- Training Details with Training Data, Training Procedure, and Training Hyperparameters: the data's source and size, the regime, the hyperparameters; Preprocessing and Speeds, Sizes, Times are optional.
- Evaluation with Testing Data, Factors & Metrics and its Testing Data, Factors, and Metrics: the held-out data, the factors the results are disaggregated by, and why each metric was chosen.
- Results with its Summary: a table disaggregated by the factors named under Factors; the summary states what the table shows in one paragraph.
- Environmental Impact: the Carbon Emitted field as a number in grams of CO2eq, with the hardware, hours, and cloud region beside it, or the marker.
- Model Card Contact: an email address or URL for questions.
- Marker: `[UNVERIFIED: what is missing]` in every slot the sources do not fill; the upstream `[More Information Needed]` never appears, and the checker bans it.
- Length: 2500 words outside code blocks for the downstream provider, 4000 for the regulator, 400 for the executive.

## System card

The template is [templates/system-card.md](templates/system-card.md).

- Title: the system's name and version followed by System Card; one sentence under it saying what the system does and what the card reports.
- Executive summary: the decision the card supports, the headline number from every evaluated chapter, and the open items: results the sources do not hold and findings not yet fixed; nothing a chapter does not also hold.
- Introduction: one sentence, then Training data and process with the sources, period, size, identifier removal and the cutoff date (the evidence slot reads for the word cutoff and a year); Usage policy and support; Model evaluations naming the areas and the rule that kept evaluation data out of training; Safeguards naming each control and what it blocks; Crowd workers and External testing when the sources give them.
- Evaluation chapters in the template's order: Cyber, Safeguards and harmlessness, Alignment assessment and Capabilities always; Frontier risk evaluations and Agentic safety when the system was evaluated in them; each a paragraph on what was asked and on which set, a results table with the set size beside each number, and a conclusion; no level-three heading below a chapter.
- Missing results: a chapter the sources name without numbers carries the marker in place of its table, naming where the results are held; no number is written from habit.
- Model welfare assessment: left out for a product on a contracted model; the provider's card carries it.
- Reliability of this assessment: languages and populations not covered, held-out sets that share a source with training, model judges with the hand-check agreement, and every chapter whose results are missing.
- Length: 1000 words outside code blocks for the executive, 6000 for the regulator.

## Annex IV technical file

The template is [templates/annex-iv-technical-file.md](templates/annex-iv-technical-file.md).

- Title: Technical documentation for followed by the system's name and version; one sentence under it naming the regulation, the system, the provider and the request the file answers.
- General description of the AI system: the seven bold fields in the Annex's order (intended purpose, provider and version; interaction with hardware and software; software and firmware versions; forms of placing on the market; hardware; component of products; user interface and instructions for use); a field that does not apply says so; the version as a number (the evidence slot reads for the word version and a number).
- Elements of the AI system and the development process: one sentence, then the eight subsections in the Annex's order; Development methods and steps names every third-party model or tool with its version and what was done to it; Design specifications states what the system optimises for, the key choices with their rationale and the trade-offs; System architecture and computational resources gives the components and the devices and hours; Data requirements and datasheets gives provenance, scope, selection, labelling and cleaning and names the datasheet; Human oversight states each measure and the moment it applies; Pre-determined changes is present when the system has one; Cybersecurity measures gives each control and what it prevents.
- Validation and testing: the data and its characteristics, the metrics with their values, the discriminatory impact finding, and the test report with its identifier, its ISO date and the signature of the responsible person; a signature the sources do not show is the marker, never a name the writer supplies (the evidence slot reads for an ISO date and the word signed, signature, signatory or sign-off).
- Monitoring, functioning and control: the overall accuracy and the accuracy per group or language, the foreseeable unintended outcomes with the risks to health and safety, fundamental rights and discrimination, the oversight measures by reference, and the input data specification.
- Appropriateness of the performance metrics: why the reported metrics fit this system and its intended purpose, in the system's terms.
- Risk management system: the register or document named, with its review cycle and what it holds.
- Changes through the lifecycle: one change per version, dated.
- Harmonised standards and other technical specifications: the harmonised standards applied, or the statement that none was applied with the solutions and the other standards and specifications.
- EU declaration of conformity: the declaration by identifier and date, attached or referenced, not reproduced as prose.
- Post-market monitoring: the plan by name with its sampling, its threshold and what an alert triggers.
- Register: exact identifiers, versions, dates and legal references; defined terms as the regulation defines them; two significant figures on sizes, counts, compute and energy; no estimate for a figure the sources do not hold.
- Length: 8000 words outside code blocks for the regulator, 800 for the executive.

## GPAI Model Documentation Form

The template is [templates/gpai-model-documentation-form.md](templates/gpai-model-documentation-form.md).

- Title: Model Documentation Form for followed by the model's name; one sentence under it saying what the model is and which reader the form is prepared for; then the header fields Date this document was last updated and Document version number with their values.
- Fields for the reader: every field the form marks for the document's audience is present as a level-three heading in the form's order, the AI Office variant for the AI Office (Total model size (exact), Number of data points (two significant figures), Training time (days), Amount of computation used for training (two significant figures)), the NCA variant (Total model size (range), Number of data points (one significant figure), Training time (range), Amount of computation used for training (order of magnitude)) for a national competent authority, and the DP fields (Distribution channels available to downstream providers, License type for downstream providers, Technical means for model integration, Required hardware, Required software) for a downstream provider only; a field the form marks for another reader is left out.
- General information: Legal name for the model provider, Model name with the public version names, Model authenticity when available (a hash or the endpoint), Release date and Union market release date in ISO form (the Release date slot reads for one), Model dependencies or N/A for a model with no base model.
- Model properties: Model architecture in 20 words; Design specifications of the model with rationale and assumptions in 100; Input modalities and Output modalities with the maximum size per modality; the size field in the reader's precision (the exact-size slot reads for a number before the word parameters).
- Methods of distribution and licenses: the channels for the reader, Model license as a link or the statement that none exists, Additional assets each with access and license or the statement that it is not released.
- Use: Acceptable Use Policy as a link or attachment or the statement that none exists; Intended uses with the restricted or prohibited uses in 200 words; Type and nature of AI systems the model can and should not be integrated into; the three DP integration fields in 100 words each.
- Training process: Design specifications of the training process in 400 words; Decision rationale in 200.
- Information on the data used for training, testing, and validation: Data type and modality; Data provenance from the form's categories; How data was obtained and selected in 300 words including rights to third-party data; the data point count in the reader's precision with its unit; Scope and main characteristics in 200 with the shares; Data curation methodologies in 300; Measures to detect unsuitability of data sources in 400 as named methods; Measures to detect identifiable biases in 200 with what they found.
- Computational resources (during training): the time and compute fields in the reader's precision; Measurement methodology (compute).
- Energy consumption (during training and inference): Amount of energy used for training in MWh at two significant figures, or N/A with the reason when the provider withholds critical information; Measurement methodology (energy) in 100 words; Benchmarked amount of computation used for inference or the marker when the benchmark has not run; Measurement methodology (inference) naming the task and the hardware.
- Precision: two significant figures for the AI Office, a range or an order of magnitude for a national competent authority, exact integration values for a downstream provider; no estimate for a figure the sources do not hold; N/A only in the three places the form names it.
- Length: 5000 words outside code blocks for the regulator, 3000 for the downstream provider, 600 for the executive; each capped field within its recommended count (the checker reports a field over its max_words as LENGTH_EXCEEDED naming the field).

## Privacy notice

The template is [templates/privacy-notice.md](templates/privacy-notice.md).

- Title: Privacy notice for followed by what the notice covers; one sentence under it saying who the notice is for and what it tells them.
- At a glance: the first layer in one paragraph a reader finishes on one screen, naming who is responsible, what the data is used for, that the reader has rights, the processing with the most impact or surprise, and that the full notice follows (the evidence slot reads for the word right).
- Who we are: the organisation by name with an email address, a URL or a postal address, and the data protection officer when there is one.
- What we use your data for: one bullet per purpose with the data, what it is for and the legal basis in the GDPR's words; the purpose says what the data does, never that it helps develop services.
- Who we share your data with: each category of recipient with why, and the no-sale statement when true.
- Where your data goes: where the data is processed and, for a transfer out of the reader's country or the EU, the country and the safeguard in plain words.
- How long we keep your data: one bullet per category with a period in days, months or years or the event that ends it; an unset period is the marker.
- Your rights: see, correct, delete, limit, move, object, withdraw consent; how to use them and how long the answer takes.
- How to complain: who to write to first and the supervisory authority by name.
- Where your data comes from: present when any data did not come from the reader; Changes to this notice when the notice is versioned.
- Register: you and we throughout; no may, might, some, often or possible (WP260 paragraph 13; a qualifier that cannot be avoided is explained in the notes to the controller, never left in the notice); no data subject, controller or other legal term; active voice; the layers say the same thing.
- Length: 900 words outside code blocks for the data subject, 2500 for the regulator, 300 for the executive.

## Data protection impact assessment

The template is [templates/data-protection-impact-assessment.md](templates/data-protection-impact-assessment.md).

- Title: Data protection impact assessment: followed by the project; one sentence under it saying what the assessment covers, under which obligation and for whom.
- Identify the need for a DPIA: the project in one paragraph and the criteria it meets; the brief or decision that triggered the assessment, with its date.
- Describe the processing: the data items, their source, what is done with them, the counts of people and records, the retention, the purpose and the relationship with the people; the words nature, scope, context and purpose each answered (the evidence slot reads for them); a count the sources do not give is the marker.
- Consultation: each consultation with its date, who took part, what they said and what the project did with it; the DPO's advice in its own words, and the reasons where it was not followed.
- Necessity and proportionality: whether the processing achieves its purpose and whether a less intrusive way exists; the lawful basis named (the evidence slot reads for it); minimisation, retention, transparency and rights.
- Identify and assess risks: one row per risk with its source, likelihood, severity and overall rating on a named scale (the evidence slot reads for likelihood and severity).
- Measures to reduce risk: one row per measure with the risk it addresses, its effect (eliminated, reduced or accepted) and the residual risk (the evidence slot reads for residual).
- Sign off and record outcomes: the overall residual risk and whether the supervisory authority is consulted; the DPO's advice followed or the reasons; the approval and its conditions; the review trigger and interval; the sign-off line with name, role and ISO date (the evidence slot reads for a sign-off word and a date).
- Register: exact identifiers, dates, owners and record references; what was done, by whom and when; numbers as recorded with their source.
- Length: 3500 words outside code blocks for the auditor and the regulator, 500 for the executive.

## Structure, every type

- One H1, and it is the title; the one-sentence summary sits directly under it.
- Every required section of the template is present, at its level, in the template's order; an optional section that is present is in its place.
- No heading the template does not declare at or above its deepest level; subdivisions below that level are the writer's.
- Prerequisites and version statements come before any procedure; expected output follows each command (spec R9).
- Heading text is stable enough to be a link anchor: no dates, no version numbers, no trailing punctuation.
- The audience is stated in the reply when the request named none, and the document's register, length, and precision match it per [audiences.md](audiences.md).
- The `llms.txt` line, when asked for, reads `[Title](url.md) - description` with the summary sentence as the description.

## Prose, every type

The rules and their sources are in [style-rules.md](style-rules.md). The checker catches em
and en dashes, we recommend and it is recommended, refer to, easy, easily, simple, simply,
quickly, currently, and soon. Everything below is read by hand.

- Second person, active voice, present tense; no passive sentences outside a quoted source.
- Leads with the point: the summary sentence says what the document is for or decides; every section opens with its conclusion or action; a section whose heading asks for its own point (a check, a decision, a next step) states it rather than repeating an earlier section.
- No filler: no sentence restates the title or a heading, previews a later section, closes a section with its own summary, or repeats under a later heading a fact stated above; no field or control explained before the steps, only a condition or a consequence the reader needs first; a required Summary carries only what its template asks for.
- Timeless words outside dated content: `now`, `new`, `newer`, `latest`, `existing`, `eventually`, `presently`, `in the future`, `as of this writing`; dated content (release notes, changelogs, postmortem timelines, advisories) is exempt.
- Obligation words in user-facing text: `should`, `may`, `could`, `would`; normative text keeps MUST, SHOULD, and MAY in capitals.
- Word list substitutions: `allows you to`, `via`, `leverage`, `execute`, `impact` as a verb, `once` for after, `since` for because, `kill`, `hit`, `hang`, `sanity check`, `e.g.`, `i.e.`, `and/or`.
- Subjective words the checker misses: `straightforward`, `just`, `obviously`, `of course`.
- No we or our in user-facing text; no please in instructions; no exclamation points.
- Sentences under 25 words and paragraphs under three sentences in user documentation; elsewhere, flag the outliers.
- Sentence-case headings; task headings verb-first; concept and reference headings noun phrases.
- Bold for UI labels only; code style for identifiers, paths, commands, and values; angle-bracket placeholders in code and italic placeholders in prose; reserved example values only.
- Lists carry parallel items; prose carries context and decisions; no list stands in for a paragraph.
- Warnings and cautions only for harm to hardware, software, or data, placed before the step they protect.
- AI-tell phrasing: hand the document to `humanize` when it leaves the org; this checklist does not restate that skill's patterns.

## Evidence, every type

- Every claim about behavior, defaults, UI, permissions, versions, or numbers traces to a source the user supplied or the skill read, cited inline or in a sources list.
- Every evidence slot the template declares is filled from a source or carries `[UNVERIFIED: what is missing]` naming the missing fact; no slot is deleted.
- No version number, default, flag, URL, metric, or legal citation was invented; each one was read somewhere the reply can name.
- A supplied source is cited for what it says; its claims are not promoted to facts about the product.
- Numbers carry their unit and their source; comparisons carry both sides; performance claims carry their conditions.
- The reply lists every marker left in the document, so the user knows what to supply.

## Review mode

Review mode classifies the document, loads its template, and reports findings ranked by
severity with the location and the rule for each, without rewriting unless asked (spec R8).

- high: a required section or an evidence slot is missing.
- medium: a structural rule is broken: section order, an unknown section, the H1 count or pattern, the summary line, a length cap, a procedure rule.
- low: a prose rule is broken: a banned pattern, or a by-hand rule from the prose checklist.
- info: an `[UNVERIFIED: ...]` marker is present; listed so the owner can fill it.
- A document passes with no high, medium, or low finding; info findings never fail it.
- Each finding names the line or the heading, the rule, and the file in this directory that carries the rule.
