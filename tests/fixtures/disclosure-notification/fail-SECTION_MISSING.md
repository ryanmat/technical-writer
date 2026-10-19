# Embargoed notification: Northwind Relay route registration authorization bypass

Embargoed notification of an authorization bypass in Northwind Relay 2.4.0 through 2.5.0, to be disclosed on 2026-10-29.

This notification is sent to let distributors and service providers plan for applying patches to reduce the time of user exposure. Information below should be kept confidential until the listed embargo date. Please do not forward this information to other parties.

## Summary

The route registration call, `POST /routes`, checks the `routes:write` scope only when the request body carries a `project` field; a request that omits the field is authorized against the token's project and the scope comparison never runs (CWE-863).

**CVE:** CVE-1900-0417

**Affected versions:** >= 2.4.0, < 2.5.1

**Reporter:** Dana Okafor, Fieldstone Labs

## Severity

High. Any project member with a token can register a route that delivers any stream in the project to a consumer group of their choosing, with no user interaction; the flaw gives no access to other projects. CVSS-B 8.7, CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N.

## Proof of concept

```bash
curl -X POST https://relay.example.com/routes -H "Authorization: Bearer <READ_ONLY_TOKEN>" -d '{"name": "poc", "stream": "orders", "consumer_group": "poc"}'
```

An affected version returns `201 Created` with the stored route; a fixed version returns `403 PERMISSION_DENIED`.

## Remediation and mitigation

The fix is in 2.5.1, released on the disclosure date; the patch is available to this list at https://relay.example.com/embargo/CVE-1900-0417/patch until then.

## Timeline

**Date reported:** 2026-10-09

**Date fixed:** [UNVERIFIED: the date the fix was merged]

**Date to be disclosed:** 2026-10-29
