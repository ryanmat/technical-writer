# Style rules

One prose rule set, applied to every document type the skill produces (spec R5). Every rule
line ends with its source in parentheses: the guide, the place in it, and the license the
text is quoted under, or the word paraphrased when the guide publishes no reuse license, or
house rule when the rule is this skill's own. Quoted text appears only from the Google developer
documentation style guide and Google Technical Writing (CC BY 4.0), the Grafana Writers'
Toolkit repository files (Apache-2.0), the Splunk Vale ruleset (Apache-2.0), and statutory
text. The Splunk Style Guide and the Microsoft Writing Style Guide are paraphrased.

## Contents

- [How to read this file](#how-to-read-this-file)
- [Voice and person](#voice-and-person)
- [Headings](#headings)
- [Sentences and paragraphs](#sentences-and-paragraphs)
- [Punctuation](#punctuation)
- [Formatting and placeholders](#formatting-and-placeholders)
- [Words to avoid](#words-to-avoid)
- [Obligation words](#obligation-words)
- [Cross-references and links](#cross-references-and-links)
- [Admonitions](#admonitions)
- [Claims and evidence](#claims-and-evidence)
- [Change categories](#change-categories)
- [Conflict picks](#conflict-picks)
- [What the checker enforces](#what-the-checker-enforces)
- [Sources](#sources)

## How to read this file

The rules are grouped by what they govern. Each group opens with the rules the guides agree
on and closes with the house rules that go further. Where two guides disagree, the pick is
stated under Conflict picks with the side taken, so a reader can trace a rule that looks
unusual back to the decision behind it.

Audience changes how strictly some rules apply. The sentence and paragraph caps bind user
documentation and are guidance elsewhere; the obligation-word rules bind user-facing text and
exempt normative text. The audience file, `audiences.md`, carries those scopes. The procedure
rules for numbered steps live in `procedure-rules.md`.

## Voice and person

- Write to the reader as you. Quoted: "Use second person." (Google developer documentation style guide, Highlights, CC BY 4.0)
- Write in the active voice, with the actor as the subject. Quoted: "Use active voice." (Google developer documentation style guide, Highlights, CC BY 4.0)
- Passive voice is banned outright, closing the gap Google and Grafana leave by treating it as a suggestion; in a privacy notice the ban is statutory, see Obligation words. (house rule)
- Write in the present tense, since the reader is doing the task as they read; avoid will, would, and their past forms. Quoted on will: "Avoid. Applies equally to its past tense, would." (Google developer documentation style guide, Word list, CC BY 4.0)
- Software does not think, want, listen, worry, or handle; name the action a component performs. (Splunk Style Guide, Avoid anthropomorphisms, paraphrased)
- Keep the tone conversational and plain without being frivolous; no marketing register. (Google developer documentation style guide, Voice and tone, CC BY 4.0)
- Quoted: "Avoid marketing clichés and hyperbole. Instead, use evidence-based or quantifiable language to focus and refine the information, and to offer value propositions." (Grafana Writers' Toolkit, Style conventions, Apache-2.0)
- Do not write we or our in a user-facing document; name the organization or the component instead. Grafana allows we for the company and that allowance is not adopted. (house rule)
- Contractions are on by default and off under the localization flag, when the document is written for translation. (house rule, following the Google developer documentation style guide, CC BY 4.0, with the Red Hat supplementary style guide, paraphrased, on the flag)

## Headings

- Quoted: "Use sentence case for document titles and section headings." (Google developer documentation style guide, Highlights, CC BY 4.0)
- Quoted: "Start task headings with a verb. Don't use "Step X:" in headings." (Grafana Writers' Toolkit, AI quick reference, Apache-2.0)
- Quoted: "Don't start headings with a gerund." (Grafana Writers' Toolkit, AI quick reference, Apache-2.0)
- Quoted, for non-task headings: "For a conceptual or non-task-based heading, use a noun phrase that doesn't start with an -ing verb." (Grafana Writers' Toolkit, Gerunds.yml, Apache-2.0)
- Quoted, for reference topics: "Use a noun-based title." (Grafana Writers' Toolkit, reference template, Apache-2.0)
- Quoted: "Include a short introduction after each heading." (Grafana Writers' Toolkit, AI quick reference, Apache-2.0)
- One H1 per document, with a one-sentence summary directly under it, and heading text that stays stable enough to serve as a link anchor (spec R9). (house rule)
- No links, code spans, or trailing punctuation in a heading; the heading is the anchor and the link target, not a link itself. (house rule)

## Sentences and paragraphs

- Quoted: "Make your sentences shorter than 25 words." The cap binds user documentation and guides every other type. (Grafana Writers' Toolkit, Style conventions, Apache-2.0)
- Quoted: "Keep paragraphs to three sentences or less." The cap binds user documentation and guides every other type. (Grafana Writers' Toolkit, Style conventions, Apache-2.0)
- Quoted: "Write important information first. Place actions before explanations." (Grafana Writers' Toolkit, Style conventions, Apache-2.0)
- Quoted: "Put conditions before instructions." (Google developer documentation style guide, Highlights, CC BY 4.0)
- Quoted: "State key points at the start of each document." and focus each paragraph on one topic. (Google Technical Writing One, Documents and Paragraphs, CC BY 4.0)
- Quoted: "Don't use lists as a substitute for paragraphs." Context and decisions are prose; options, drivers, goals, and prerequisites are lists. (Grafana Writers' Toolkit, AI quick reference, Apache-2.0)
- Quoted: "Sort lists and table rows alphabetically unless the order is important to understanding the information in the list or table." (Grafana Writers' Toolkit, Style conventions, Apache-2.0)
- Open a sentence with the actor or the verb, not with there is or there are, and cut the words a sentence does not need. (Microsoft Writing Style Guide, Top 10 tips for Microsoft style and voice, paraphrased)
- Write each sentence about one idea, and prefer a specific verb (stop, run, return) to a vague one (handle, understand, know). (Splunk Style Guide, Optimizing documentation for AI, paraphrased)

## Punctuation

- Use the serial comma before the last item of a list of three or more. (Google developer documentation style guide, Commas, CC BY 4.0)
- One space between sentences. (Google developer documentation style guide, Spaces between sentences, CC BY 4.0; Splunk Vale ruleset, SentenceSpacing.yml, Apache-2.0)
- No em dashes and no en dashes, closed or spaced; write a comma, a colon, parentheses, or two sentences instead. Only Splunk's ruleset backs the rule, quoted: "Don't use em or en dashes." (house rule; Splunk Vale ruleset, Dashes.yml, Apache-2.0)
- Write a hyphen for ranges in prose only when the range is a code identifier; otherwise write to, as in 10 to 20 pages. (house rule)
- No exclamation points in documentation. (Grafana Writers' Toolkit, Exclamation.yml, Apache-2.0; Splunk Vale ruleset, ExclamationPoints.yml, Apache-2.0)
- Quoted: "For ordinals, write out first through ninth. For 10th on, use numerals." (Grafana Writers' Toolkit, Style conventions, Apache-2.0)
- No Latin abbreviations. Quoted on e.g.: "Don't use. Instead, use phrases like for example or such as." and on i.e.: "Don't use. Instead, use phrases like that is." (Google developer documentation style guide, Word list, CC BY 4.0)
- Quoted on and/or: "Don't use unless space is limited, such as in a table." (Google developer documentation style guide, Word list, CC BY 4.0)
- Treat data as singular. Quoted: "Use data as singular, not plural; the data is, not the data are." (Google developer documentation style guide, Word list, CC BY 4.0)

## Formatting and placeholders

- Quoted: "Bold the label text, not the element type: "Click **Apply**", not "click the **Apply** button."" (Grafana Writers' Toolkit, AI quick reference, Apache-2.0)
- Code style for identifiers, file names, paths, commands, flags, values the reader types, and API object names, which keep their own capitalization. (Google developer documentation style guide, Code in text, CC BY 4.0; Kubernetes style guide, paraphrased)
- Quoted: "Use `<VARIABLE_NAME>` in code blocks and _VARIABLE_NAME_ in prose." Angle-bracket placeholders in code, italic placeholders in prose, and never a real identifier, customer name, or credential as a placeholder. (Grafana Writers' Toolkit, Style conventions, Apache-2.0)
- Reserved example values only: `example.com` for hosts, `CVE-1900-` identifiers for advisories, and names that cannot be mistaken for a real customer. (house rule)
- One command per code block, and the expected output after any command whose output the reader uses (spec R9). (Red Hat supplementary style guide, paraphrased; house rule)
- Quoted: "Use the exact title of the linked page as link text, not "click here" or "this file."" (Grafana Writers' Toolkit, AI quick reference, Apache-2.0)
- Tables for comparisons and parameter lists; a table has a header row, and a cell holds one value, not a paragraph. (house rule)

## Words to avoid

- No subjective words: easy, easily, simple, simply, quickly, straightforward, just. The reader judges difficulty; state the steps and let them. (Splunk Style Guide, Avoid qualitative language, paraphrased; Grafana Writers' Toolkit, Simple.yml, Apache-2.0)
- No timeless-breaking words outside dated content: currently, now, soon, new, newer, latest, existing, eventually, presently, in the future, as of this writing. Quoted on currently: "Avoid because this word is implied." Release notes, changelog entries, postmortem timelines, and advisories are dated content and exempt. (Google developer documentation style guide, Word list, CC BY 4.0; Grafana Writers' Toolkit, Timeless.yml, Apache-2.0)
- No we recommend, it is recommended, or it is best to; state the requirement and the reason. Quoted: "Don't make recommendations. Guide the reader to the best choice using specific language and direct instructions." (Splunk Vale ruleset, Recommendations.yml, Apache-2.0; Splunk Style Guide, Recommendations, paraphrased)
- Rephrase a recommendation as a requirement with its reason, as in: to keep the service available, run the migration outside business hours. (Splunk Style Guide, Recommendations, paraphrased)
- Quoted on allows you to: "Don't use. Instead, use lets you." (Google developer documentation style guide, Word list, CC BY 4.0)
- Quoted on via: "Don't use." Write through, by, or using. (Google developer documentation style guide, Word list, CC BY 4.0)
- Quoted on leverage: "Avoid using if you mean use. If possible, use a more precise term. For example, use, build on, or take advantage of." (Google developer documentation style guide, Word list, CC BY 4.0)
- Quoted on execute: "When the meaning is the same, use the simpler word run instead." (Google developer documentation style guide, Word list, CC BY 4.0)
- Quoted on impact: "Use only as a noun. Instead of writing that something has an impact, use the word affect." (Google developer documentation style guide, Word list, CC BY 4.0)
- Quoted on once: "If you mean after, then use after instead of once." and on since: "If you mean because, then use because instead of since. Since is ambiguous; it can refer to the passage of time." (Google developer documentation style guide, Word list, CC BY 4.0)
- Quoted on kill: "Avoid when possible. Instead, use words like stop, exit, cancel, or end." and on hit: "Don't use as a synonym for click, press, or type." (Google developer documentation style guide, Word list, CC BY 4.0)
- Quoted on hang: "Don't use to refer to a computer or system that is not responding. Instead, use stop responding or not responding." (Google developer documentation style guide, Word list, CC BY 4.0)
- Quoted on sanity check: "Don't use. Instead, use a term like quick check, confidence check, preliminary check or coherence check." (Google developer documentation style guide, Word list, CC BY 4.0)
- No please in instructions; the imperative is the courtesy. (Grafana Writers' Toolkit, Please.yml, Apache-2.0)
- No this, that, or it as a sentence subject when the referent is not the previous sentence's subject; repeat the noun. (Splunk Style Guide, Optimizing documentation for AI, paraphrased)
- No AI-tell phrasing: stock openers, inflated verbs, not just X but Y, formulaic wrap-ups. The `humanize` skill owns the pattern list and the rewrite; this file names the rule only (spec R11). (house rule)

## Obligation words

- In user-facing text, avoid should, may, could, and would; write what the reader does or what the system does. Quoted on should: "Generally avoid." On may: "In general, reserve for official policy or legal considerations." On could: "Avoid using. Instead, use can where possible." (Google developer documentation style guide, Word list, CC BY 4.0)
- The subjunctive leaves the reader unsure whether a sentence states a requirement or a suggestion; write in the indicative or the imperative. Quoted: "Use the indicative or imperative mood." (Splunk Style Guide, Write in indicative or imperative mood, paraphrased; Splunk Vale ruleset, SubjunctiveMood.yml, Apache-2.0)
- Normative text keeps RFC 2119 usage: MUST, SHOULD, and MAY in capitals, defined once by reference, in SECURITY.md policies, API contracts, advisories, governance filings, and DPIAs. The restriction above applies to user-facing text only. (house rule)
- Privacy notices avoid the five qualifiers by name. Quoted: "Language qualifiers such as "may", "might", "some", "often" and "possible" should also be avoided." A writer who cannot avoid one records why in the notes to the controller, as the paragraph requires of the controller. (WP260 rev.01, paragraph 13, statutory)
- Privacy notices are active voice by requirement, not by house choice. Quoted: "Writing should be in the active instead of the passive form and excess nouns should be avoided." (WP260 rev.01, paragraph 13, statutory)

## Cross-references and links

- Write see for cross-references, not refer to, check out, or consult. Quoted on see: "OK as a general term and when referring to links and cross-references." Grafana's ReferTo rule takes the other side and is not adopted. (Google developer documentation style guide, Word list, CC BY 4.0; house rule)
- Quoted: "Follow "Every Page is Page One": each page stands on its own." A page restates the prerequisites and context a reader needs rather than assuming the previous page was read. (Grafana Writers' Toolkit, AI quick reference, Apache-2.0)
- Link related topics and never leave a topic isolated; link to the one page that owns a fact rather than restating it. (Splunk Style Guide, Optimizing documentation for AI, paraphrased)
- A link carries the exact title of its target as its text, see Formatting and placeholders; a bare URL appears only in a sources list. (house rule)

## Admonitions

- Quoted: "Warnings are reserved for actions that could cause harm to hardware, software, or data." Caution shares that reservation; Note and Tip are for context. (Grafana Writers' Toolkit, Style conventions, Apache-2.0)
- A warning or caution is placed before the step it protects, never after, and never after the last step (spec R6, see `procedure-rules.md`). (house rule)
- A note or tip carries context the reader can skip, not an instruction the reader must perform; an instruction is a step. (house rule)
- At most one admonition between two steps; two stacked admonitions mean the step wants splitting or the context belongs in the introduction. (house rule)

## Claims and evidence

- Quoted: "Back every claim about product behavior, defaults, UI, or permissions with a source file or page. If you can't verify a claim, mark it `[UNVERIFIED]` rather than guessing." (Grafana Writers' Toolkit, AI quick reference, Apache-2.0)
- The skill's marker form is `[UNVERIFIED: what is missing]`, naming the missing fact, and a template's evidence slot that cannot be filled keeps its marker rather than being deleted (spec R7). (house rule)
- Never invent a version number, a default, a command flag, a URL, a metric, or a legal citation; every such value traces to a source the user supplied or the skill read (spec R7). (house rule)
- Quoted: "Don't document implementation details, specifications, or backend system operations that have no clear consequence to the user." (Grafana Writers' Toolkit, Style conventions, Apache-2.0)
- Quoted: "An LLM generally assumes that information in attachments is factual, and this can cause problems." Read a supplied source for what it says, cite it for that, and do not promote its claims to facts about the product. (Google Technical Writing Two, Using large language models in technical writing, CC BY 4.0)
- A number carries its unit and its source; a comparison carries both sides; a claim about performance carries the conditions it was measured under. (house rule)

## Change categories

The one list of change categories the release notes and changelog entry templates share;
neither template repeats it in prose.

- Quoted: a change is grouped under one of six categories, "`Added` for new features.", "`Changed` for changes in existing functionality.", "`Deprecated` for soon-to-be removed features.", "`Removed` for now removed features.", "`Fixed` for any bug fixes.", "`Security` in case of vulnerabilities.", kept in that order, each present only when it has entries; a change that fits none is Changed, and a heading outside the six (Improvements, Breaking changes) is an unknown section. (Keep a Changelog 1.1.0, MIT)
- Quoted: "The same types of changes should be grouped." and "Changelogs are for humans, not machines." (Keep a Changelog 1.1.0, MIT)

## Conflict picks

The surveyed guides disagree in ten places. The side taken is recorded here with the reason,
so a rule above that looks stricter than its guide can be traced.

- Contractions are on, and the localization flag turns them off for documents written for translation. Google, Microsoft, and Grafana allow them; Red Hat avoids them for translation. (house rule; Google developer documentation style guide, CC BY 4.0, and Red Hat supplementary style guide, paraphrased)
- Em and en dashes are banned outright, closed ones included. Microsoft uses closed em dashes and Grafana bans only spaced ones, so the rule is the skill's own, backed by Splunk's ruleset. (house rule; Splunk Vale ruleset, Dashes.yml, Apache-2.0)
- Cross-references use see, not refer to. Google says see is fine; Grafana enforces refer to by linter and Datadog's agent file swaps see out. The shorter, Google-backed word wins. (house rule; Google developer documentation style guide, Word list, CC BY 4.0)
- Task headings are bare infinitives, never gerunds, with Grafana and Google against the gerund-title skills. (Grafana Writers' Toolkit, Gerunds.yml, Apache-2.0; Google developer documentation style guide, Headings, CC BY 4.0)
- Obligation words are restricted in user-facing text only; normative, compliance, and policy text keeps RFC 2119 usage, which Google's and Splunk's rules would otherwise strip. (house rule; Google developer documentation style guide, Word list, CC BY 4.0)
- Tone follows Google's conversational side, not Microsoft's warm register or Red Hat's formal one, since it matches plain engineering English. (Google developer documentation style guide, Voice and tone, CC BY 4.0)
- Prose carries context and decisions; lists carry options, drivers, goals, and prerequisites. Nygard bans fragment bullets in ADRs and Grafana bans lists as paragraph substitutes, while MADR and the Google design doc lean on lists. (house rule; Grafana Writers' Toolkit, AI quick reference, Apache-2.0)
- An ADR is immutable once accepted and is superseded by a new record rather than amended, as the AWS lifecycle and Nygard describe; dated amendments are not adopted. (house rule, following the AWS ADR process and Nygard, paraphrased)
- Length is set per document type in each template's length caps, never globally; Nygard's one to two pages and Ubl's ten to twenty are both right for their types. (house rule; Grafana Writers' Toolkit, Style conventions, Apache-2.0)
- Passive voice is banned as a house rule and cited to WP260 paragraph 13 in privacy notices, where the ban is statutory; no security or audit standard bans it and Grafana treats it as a suggestion. (house rule; WP260 rev.01, paragraph 13, statutory)

## What the checker enforces

`scripts/check_structure.py` enforces the subset of these rules a regular expression can
judge, as `BANNED_PATTERN` findings at low severity: em and en dashes anywhere in prose, we
recommend and it is recommended, refer to, the subjective words easy, easily, simple, simply,
and quickly, and the timeless-breaking words currently and soon. Its scan covers every line
outside fenced code blocks, headings included, with inline code spans and URLs blanked.

Every other rule in this file is checked by hand against `checklists.md`, or by Vale when a
session has it on the path (spec R10). A document passes the checker with no low, medium, or
high finding; passing the checker is necessary and not sufficient.

## Sources

Every source this file cites, its license, and whether it is quoted or paraphrased, is
recorded once, in [attribution.md](attribution.md), under Rule sources. The rule lines above
carry the guide and the license beside each rule; the register there carries the rest.
