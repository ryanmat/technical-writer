---
schema_version: "1.1"
name: security-md--relay
description: "a SECURITY.md for the engineers and researchers who report to a project, from a maintainers' note that gives the supported lines, the two reporting channels, the acknowledgement window and the disclosure timeline, and mentions a key for encrypted reports without its fingerprint, so the output carries the version table, the reporting paragraph with address, form and window, the disclosure policy, the update channels, and an UNVERIFIED marker for the fingerprint instead of an invented one"
tags: [security, regression]
runs: 2
max_turns: 12
timeout_seconds: 600
allowed_tools: [Skill, Read]
---

Use the technical-writer skill to write the SECURITY.md for the Northwind Relay repository, for the engineers and researchers who will report a vulnerability to the project. Return the finished Markdown document as your final message and nothing else.

Everything you may state is in the maintainers' note below. Do not add versions, addresses, links, windows, or timelines it does not contain. The note says a key for encrypted reports exists and does not give its fingerprint; do not invent one.

The maintainers' note:

```text
Supported: 2.5.x gets all fixes. 2.4.x gets security fixes only, until 2027-01-31. 2.3 and earlier: nothing.
Reporting: email security@relay.example.com, or use the private vulnerability reporting form at https://github.com/example/relay/security/advisories/new (we prefer the form). Include what the issue is, the steps to reproduce it, the affected versions, and any mitigation you know of. We acknowledge within 3 working days and say whether it is confirmed within 10 working days. There is a PGP key for encrypted email; I do not have the fingerprint in front of me.
Disclosure: 90 day timeline from the acknowledgement. We confirm, fix, request a CVE through GitHub, and write the advisory. Reporters are credited by name and affiliation unless they ask us not to. If the fix needs longer than 90 days we tell the reporter the new date before the 90 days end.
Updates: fixes land in 2.5.x first, then 2.4.x while it is supported. Announced as GitHub security advisories at https://github.com/example/relay/security/advisories and in the release notes at https://relay.example.com/releases.
```
