# Embargoed notification: Northwind Relay route registration authorization bypass

Embargoed notification of an authorization bypass in Northwind Relay 2.4.0 through 2.5.0, to be disclosed on 2026-10-29.

This notification is sent to let distributors and service providers plan for applying patches to reduce the time of user exposure. Information below should be kept confidential until the listed embargo date. Please do not forward this information to other parties.

## Summary

The route registration call, `POST /routes`, in the router checks the `routes:write` scope only when the request body carries a `project` field; a request that omits the field is authorized against the token's project and the scope comparison never runs (CWE-863, incorrect authorization).

**CVE:** CVE-1900-0417

**Affected versions:** >= 2.4.0, < 2.5.1

**Reporter:** Dana Okafor, Fieldstone Labs

## Severity

High. A project member holding any token for the project, with or without `routes:write`, can register a route that delivers any stream in the project to a consumer group of their choosing, with no user interaction; the flaw gives no access to other projects. CVSS-B 8.7, CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N.

## Proof of concept

```bash
curl -s -o /dev/null -w "%{http_code}\n" -X POST https://relay.example.com/routes -H "Authorization: Bearer <READ_ONLY_TOKEN>" -H "Content-Type: application/json" -d '{"name": "poc-route", "stream": "orders", "consumer_group": "poc"}'
```

Against 2.5.0 the command prints `201`; against a 2.5.1 build it prints `403`.

## Remediation and mitigation

The fix ships in 2.5.1 with the public disclosure on 2026-10-29. Until then the patch is available to this list at https://relay.example.com/embargo/CVE-1900-0417/patch.

## Timeline

**Date reported:** 2026-10-09

**Date fixed:** [UNVERIFIED: the date the fix was merged, which the plan places last week and does not give]

**Date to be disclosed:** 2026-10-29

## Disclosure

Public disclosure date: 2026-10-29 at 14:00 UTC, with the 2.5.1 release and the advisory for CVE-1900-0417. Questions go to security@relay.example.com. Please do not make the issue public, issue user communications, share this information with others, or issue public patches before the disclosure date. We will notify this list immediately if the disclosure date is at risk or changes.
