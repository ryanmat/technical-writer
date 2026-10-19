<!-- template: concept; audience: engineer -->
# The technical-writer workflow

The skill turns a request into a document of one named type, for one named audience, in the structure that type's template fixes, with every unsourced claim marked.

Most documentation requests arrive as "write the docs for X". The skill does not answer that with one page. It decides what kind of page the reader needs, who that reader is, and what the page must contain before it writes a sentence, and it checks the result against rules a machine can read.

## Classification

Every request becomes one of 24 document types across six domains: user documentation, engineering and architecture, API reference text, AI governance, security, and privacy. The skill classifies by what the reader will do with the page, not by the words in the request. A request for "docs for the alert rule feature" is a concept (what it is), a task (how to set one up), a reference (every field), or several of these as separate pages. When two types with different structures both fit, the skill asks one question naming both. When a request needs two types, it produces two documents. Three kinds of document belong to other skills and are declined by name: README and pull request bodies, and penetration test or assessment reports.

## The audience parameter

Each document has one audience from a fixed set of seven: engineer, operator, executive, regulator, auditor, data subject, and downstream provider. The audience changes three things. Register is who the reader is assumed to be and whether they want the reason or only the action. Length is the word cap the template carries for that audience, counted outside code blocks. Precision is how numbers are written: exact values with units for an engineer, two significant figures for a regulator, ranges for an executive. A request that names no audience gets the type's default, and the reply says so.

## Templates as the single source of truth

Each type has one template file with two parts. The YAML front matter is machine-readable: the required sections in order and at their heading levels, the optional ones, the evidence slot a section must fill, the length caps per audience, the pattern the title must match, and any type-specific banned patterns. The Markdown body is the guidance the writer follows for each section, with the source standard it comes from. The structural checker reads the same front matter, so the skill and the checker cannot disagree about what a conforming document is. The templates take their structure from published standards (the Grafana Writers' Toolkit topic types, MADR, the Hugging Face model card, the OpenSSF disclosure guide, WP260, and the ICO's DPIA steps, among others), and `references/attribution.md` records each source and its license.

## Evidence markers

Every statement about behavior, defaults, versions, numbers, or law comes from material the user supplied or a file the session read. A claim with no source is written as `[UNVERIFIED: what is missing]`, inline in place of the claim, naming the fact that is missing. An evidence slot the sources cannot fill keeps its heading and carries the marker. A required section is never dropped to make a document look complete, and the skill invents no version number, default, flag, URL, metric, or legal citation. The reply lists every marker left in the document so the owner knows what to supply.

## The self-check and the evals

After drafting, the skill runs `scripts/check_structure.py` over the draft against the template and fixes every finding above info, then walks the by-hand checklist for the rules a regular expression cannot judge. The same checker grades the eval suite. Each eval case runs the skill through `claude plugin eval`, and a run passes only when the case's own graders and the structural checker both pass it. A separate judge model scores the prose on four criteria and is calibrated against hand-scored documents. The committed reports under `evals/reports/` record each release's results per model.

## Useful links

- [Install the technical-writer plugin](install.md)
- [Document types and audiences](document-types.md)
- [Troubleshoot checker findings](troubleshooting.md)
