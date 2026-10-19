# changelog-entry--relay-2-5-1

Seed: the eleventh regression case, written on 2026-10-17; spec R1 (the request is classified as a changelog entry, the block added to CHANGELOG.md, not release notes for a reader's page), R4 (the Keep a Changelog file shape: the dated version heading as the source writes it, the categories from the shared list in style-rules.md and no other, an identifier on every entry), and R7 (the issue export gives no key for the registration hardening, so that entry carries an UNVERIFIED marker rather than an invented key). It is the sibling of release-notes--relay-2-5-0: the same product, the next release, the type whose heading carries the date.

Expected shape: an H1 naming the product and changelog, a one-sentence summary saying what the file documents, one level-two heading [2.5.1] - 2026-10-17, the categories Fixed and Security at level three in that order, one entry per change with its RELAY key in parentheses, and the Security entry carrying the marker in place of a key. reference.md is one document in that shape; it passes check_structure.py under the changelog entry template at the engineer audience with one info finding, the key marker on the Security entry; the two keyed entries fill the version section's evidence slot and the marker grader in run_evals.py reads the marker as a pattern (issue, pull request, commit, key, identifier, ticket).

First read (report 20261018T032812Z-chunk-j-engineering, Sonnet 5.5): 2 of 2 runs at bar, every grader passed, the marker found both times; judge 5 and 4.

Later reads: Reads 20261018T033707Z, 20261018T134844Z and 20261018T135632Z-chunk-j-engineering-4: 2 of 2 each time, judge 4,5 then 5,4 then 4,4; the short two-section type the judge reads highest.
