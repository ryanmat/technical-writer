---
schema_version: "1.1"
name: disclosure-notification--relay-embargo
description: "an embargoed disclosure notification for the operators on a distributor list, from an embargo plan, a triage note and a reproduction log, where the triage note says the fix was merged last week without the date, so the output carries the embargoed title, the confidentiality terms, the CVE and version range in the Summary, the rating with its vector, the reproduction in a code block, the patch link, the timeline with an UNVERIFIED marker for the fix date, and the disclosure date, time, time zone and contact"
tags: [security, regression]
runs: 2
max_turns: 12
timeout_seconds: 600
allowed_tools: [Skill, Read]
---

Use the technical-writer skill to write the embargoed disclosure notification for the Northwind Relay route registration authorization bypass, to be sent to the distributors and service providers on the embargo list, who run Relay deployments. Return the finished Markdown document as your final message and nothing else.

Everything you may state is in the three snippets below. Do not add versions, dates, scores, identifiers, links, or addresses they do not contain. The triage note says the fix was merged last week and does not give the date; do not invent it.

The embargo plan, from the security lead:

```text
Public disclosure: 2026-10-29 at 14:00 UTC, with the 2.5.1 release and the advisory for CVE-1900-0417.
Patch for the list: https://relay.example.com/embargo/CVE-1900-0417/patch (available to list members until the release).
Questions: security@relay.example.com.
Reported: 2026-10-09, by Dana Okafor (Fieldstone Labs), credited by name and affiliation.
Fix: merged last week; I would have to look up the exact date.
```

The triage note, from the security lead:

```text
Identifier: CVE-1900-0417 (reserved).
Component: the route registration call, POST /routes, in the router.
Flaw: the handler checks the routes:write scope only when the request body carries a project field. A request that omits the field is authorized against the token's project and the scope comparison never runs. CWE-863, incorrect authorization.
Affected: 2.4.0 through 2.5.0. Fixed in 2.5.1.
Impact: a project member holding any token for the project, with or without routes:write, can register a route that delivers any stream in the project to a consumer group of their choosing. No user interaction. No access to other projects.
Severity: High. CVSS v4.0 Base (CVSS-B) 8.7, vector CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N.
```

The reproduction log, from the security lead's test run against 2.5.0:

```text
$ curl -s -o /dev/null -w "%{http_code}\n" -X POST https://relay.example.com/routes -H "Authorization: Bearer <READ_ONLY_TOKEN>" -H "Content-Type: application/json" -d '{"name": "poc-route", "stream": "orders", "consumer_group": "poc"}'
201
# the same request against a 2.5.1 build:
403
```
