---
schema_version: "1.1"
name: dpia--relay-analytics
description: "a data protection impact assessment for the auditor who tests the record, from a project brief, a consultation note, a risk register and a sign-off note, where the brief gives the message volume and the customer count but not the number of account holders, so the output carries the ICO's seven steps as sections with likelihood and severity per risk, residual risk per measure, a dated sign-off, and an UNVERIFIED marker for the count of people affected"
tags: [privacy, regression]
runs: 2
max_turns: 12
timeout_seconds: 600
allowed_tools: [Skill, Read]
---

Use the technical-writer skill to write the data protection impact assessment for the Relay usage analytics project at Northwind Labs, for the internal auditor who will test the record. Return the finished Markdown document as your final message and nothing else.

Everything you may state is in the four snippets below. Do not add risks, measures, dates, names, ratings or counts they do not contain. The brief gives the daily message volume and the number of customers but not the number of account holders; do not estimate it.

The project brief, NW-PROJ-31, from the product director:

```text
Project: Relay usage analytics. Dated 2026-09-15. DPIA required: combines data across 60 customers, scores accounts, introduces a new analytics store; the product director requested the assessment the same day.
Processing: for every routed message, take the account identifier, route name, timestamp and message count from the router's delivery log into the analytics store; no message bodies. Nightly aggregation into per-account and per-customer usage figures; a churn score per customer company from the trend.
Scale: 1.2 million messages a day, 60 customers. Number of account holders: not in the brief.
Retention: proposed 25 months. Purpose: usage dashboards for customers, capacity planning, a warning to the account team when a customer's usage falls. Context: employees of customer companies using a routing service at work under the company's contract with Northwind Labs.
Lawful basis: legitimate interest in running and planning the service; balancing test NW-LIA-9. The Relay privacy notice tells account holders about the processing; the customer contract lets a company exclude its accounts from the churn score.
```

The consultation note, from the privacy lead:

```text
Customer advisory group, 2026-09-30: 8 of 60 customers took part; no objections; one asked for a way to exclude its accounts from the churn score, accepted as measure M4.
DPO, 2026-10-02, written advice: pseudonymise account identifiers before they reach the analytics store; cut retention from 25 months to 13 months. Both adopted.
Security lead, 2026-10-03: consulted on the analytics store's access control.
```

The risk register, from the privacy lead (likelihood: remote, possible, probable; severity: minimal, significant, severe):

```text
R1: an account holder is re-identified from a route name combined with the pseudonymised identifier. Source: customers choose route names that carry personal names. Likelihood possible, severity minimal, overall low.
R2: a customer uses per-account figures to monitor an individual employee's performance. Source: per-account usage figures in the dashboard. Likelihood possible, severity significant, overall high.
R3: the analytics store is breached and 13 months of usage records are exposed. Source: a new store outside the production boundary. Likelihood remote, severity significant, overall medium.
M1: keyed-hash pseudonymisation of account identifiers before the store, key kept in the router (R1, R3; reduced; residual low).
M2: the customer dashboard shows usage per route and per customer, never per account; per-account figures stay with the account team (R2; reduced; residual low).
M3: the store sits inside the production boundary; access limited to the analytics service account and two named engineers, reviewed quarterly (R3; reduced; residual low).
M4: a customer can exclude its accounts from the churn score through its contract (R2; reduced; residual low).
M5: retention 13 months, enforced by the store's lifecycle rule (R3; reduced; residual low).
```

The sign-off note, from the product director:

```text
Residual risk low for every risk; no ICO consultation needed. DPO advice adopted in full. M1 to M5 approved; the project proceeds once M1 and M3 are in place, confirmed by the engineering lead on 2026-10-09. Review when the processing changes and at least every twelve months. Signed off by Priya Anand, product director, 2026-10-10.
```
