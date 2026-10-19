---
schema_version: "1.1"
name: privacy-notice--relay-account
description: "a layered privacy notice for the people who hold Relay accounts, from a data map, a retention schedule and a contacts note, where legal has not set the retention period for support messages, so the output carries a first-layer summary, plain sections for the controller, purposes and legal bases, recipients, transfers, retention, rights, complaints and sources, no WP260 paragraph 13 qualifier, and an UNVERIFIED marker for the unset period"
tags: [privacy, regression]
runs: 2
max_turns: 12
timeout_seconds: 600
allowed_tools: [Skill, Read]
---

Use the technical-writer skill to write the privacy notice for the people who hold Northwind Relay accounts, the notice they read in the Relay console. Return the finished Markdown document as your final message and nothing else.

Everything you may state is in the three snippets below. Do not add purposes, recipients, periods, countries or contacts they do not contain. The retention schedule says legal has not set the period for support messages; do not invent one.

The data map, from the privacy lead:

```text
Controller: Northwind Labs, 12 Harbour Street, Dublin 2, Ireland. Data protection officer: privacy@relay.example.com.
Account data (name, work email, company): to run the account and deliver Relay; basis: contract with the account holder's company. Comes from the account holder and from the company administrator who created the account.
Routes and access logs (routes created, sign-ins, API calls): to keep Relay secure and find faults; basis: legitimate interest in a secure service.
Support messages: to answer support requests; basis: contract.
Product emails (name, work email): only with consent given in account settings, withdrawable there.
Invoices (company, account holder): legal obligation to keep accounting records.
Recipients: the cloud provider hosting Relay in the EU; the email provider; the payment processor; authorities when the law requires. No sale of data; no advertisers.
Transfers: Relay runs in the EU. The email provider processes name and work email in the United States under standard contractual clauses approved by the European Commission.
```

The retention schedule, from the privacy lead:

```text
Account data: life of the account plus 90 days. Routes and access logs: 13 months. Invoices: 7 years (accounting law). Support messages: under review; legal has not set the period.
```

The contacts note, from the privacy lead:

```text
Rights: access, correction, deletion, restriction, portability, objection where we rely on legitimate interest, withdrawal of consent; requests to privacy@relay.example.com, answered within one month.
Complaints: the DPO first; the data protection authority where the person lives; lead authority the Data Protection Commission (Ireland).
```
