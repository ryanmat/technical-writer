# Data protection impact assessment: Relay usage analytics

This assessment records how Northwind Labs assessed the Relay usage analytics project under Article 35 of the GDPR, following the ICO's seven steps, so that an auditor can read each risk, the measure against it and the recorded outcome.

## Identify the need for a DPIA

Relay usage analytics is a new processing of account holders' data at scale: it aggregates route and message metadata across every Relay customer to build usage dashboards and a churn signal per customer company. The project brief NW-PROJ-31, dated 2026-09-15, classified the processing as requiring a DPIA because it combines data across 60 customers, scores accounts, and introduces a new analytics store; the product director asked for this assessment the same day.

## Describe the processing

The nature of the processing is the collection, for every message Relay routes, of the account identifier, the route name, the timestamp and the message count, written to the analytics store; message bodies are not taken. The source is the Relay router's delivery log. The analytics job aggregates the records nightly into per-account and per-customer usage figures and computes a churn score per customer company from the trend. The scope is 1.2 million messages a day across 60 customers. [UNVERIFIED: the number of account holders whose data the processing covers, which the brief does not give] The data is kept in the analytics store for 13 months. The purpose is to show customers their usage, to plan capacity, and to warn the account team when a customer's usage falls. The context is business use of a routing service by employees of customer companies under a contract between Northwind Labs and the company.

## Consultation

The customer advisory group was consulted on 2026-09-30: eight of the 60 customers took part, none objected, and one asked for a way to exclude its accounts from the churn score, which the project accepted as measure M4. The data protection officer was consulted on 2026-10-02 and advised in writing that account identifiers be pseudonymised before they reach the analytics store and that retention be cut from the proposed 25 months to 13 months; both pieces of advice were adopted. The security lead was consulted on 2026-10-03 on the analytics store's access control.

## Necessity and proportionality

The processing achieves its purpose: usage dashboards and capacity planning need the per-account counts, and the churn signal needs the trend per customer. The lawful basis is Northwind Labs' legitimate interest in running and planning the service, which the account holders expect of a routing service they use at work; the balancing test is recorded in NW-LIA-9. Message bodies are excluded, identifiers are pseudonymised, and retention is 13 months, as the data protection officer advised. The privacy notice for Relay accounts tells account holders about the processing, and the customer contract gives each company the right to exclude its accounts from the churn score.

## Identify and assess risks

| Risk | Source | Likelihood | Severity | Overall |
|---|---|---|---|---|
| R1: an account holder is re-identified from a route name combined with the pseudonymised identifier | route names chosen by customers carry personal names | possible | minimal | low |
| R2: a customer uses the per-account figures to monitor an individual employee's performance | per-account usage figures in the dashboard | possible | significant | high |
| R3: the analytics store is breached and 13 months of usage records are exposed | a new store outside the production boundary | remote | significant | medium |

Likelihood is rated remote, possible or probable and severity minimal, significant or severe, as the ICO's guidance describes them; the overall rating follows the two.

## Measures to reduce risk

| Measure | Risk | Effect | Residual risk |
|---|---|---|---|
| M1: account identifiers are pseudonymised with a keyed hash before they reach the analytics store, and the key stays in the router | R1, R3 | reduced | low |
| M2: the customer dashboard shows usage per route and per customer, never per account; per-account figures stay with the account team | R2 | reduced | low |
| M3: the analytics store sits inside the production boundary with access limited to the analytics service account and two named engineers, reviewed quarterly | R3 | reduced | low |
| M4: a customer can exclude its accounts from the churn score through its contract | R2 | reduced | low |
| M5: retention is 13 months, enforced by the store's lifecycle rule | R3 | reduced | low |

## Sign off and record outcomes

The residual risk after the measures is low for every risk, so the ICO is not consulted. The data protection officer's advice was adopted in full, as recorded under Consultation. The measures M1 to M5 are approved and the project proceeds once M1 and M3 are in place, which the engineering lead confirmed on 2026-10-09. The assessment is reviewed when the processing changes and at least every twelve months. Signed off by Priya Anand, product director, on 2026-10-10.
