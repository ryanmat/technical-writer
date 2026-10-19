---
schema_version: "1.1"
name: annex-iv--relay-classifier
description: "an Annex IV technical file for a market surveillance authority, from a registry entry, a development note, a test summary and a compliance note, where the test report is dated but its responsible-person signature is pending, so the output carries the nine Annex IV items as sections with item 2's sub-points as subsections, exact versions and dates, and an UNVERIFIED marker for the signature under Validation and testing"
tags: [ai-governance, regression]
runs: 2
max_turns: 12
timeout_seconds: 600
allowed_tools: [Skill, Read]
---

Use the technical-writer skill to write the Annex IV technical file for Relay Intent Classifier 1.2.0, the model that assigns each Northwind Relay support message to one of twelve intent queues, for the market surveillance authority the compliance lead expects a request from. Return the finished Markdown document as your final message and nothing else.

Everything you may state is in the four snippets below. Do not add versions, dates, identifiers, standards, numbers or names they do not contain. The test summary says the QA lead has not yet signed test report TR-0912; do not name a signer or a signing date.

The registry entry, from the model registry:

```text
System: Relay Intent Classifier 1.2.0. Provider: Northwind Labs. Replaces 1.1.3; same architecture and intent set, retrained on a larger set.
Purpose: labels each incoming support message with one of twelve intents so the Relay router delivers it to the matching queue.
Interfaces: receives messages from the Relay router over gRPC; returns a label and a confidence; calls no other AI system.
Software: inference service 3.4.1; the model store accepts only images signed by the Northwind release key; a version update requires a new signed image.
Delivery: a container image for the customer's Relay cluster, and the hosted Relay API.
Hardware: the customer's Kubernetes cluster, one CPU core and 2 GB memory per replica, no accelerator at inference. Not a component of a physical product.
Deployer UI: the queue label and the confidence beside each message in the Relay console. Instructions for use: the Relay operator guide 1.2.
Lifecycle: 1.0 September 2025, English only; 1.1 February 2026, added German and French; 1.2.0 September 2026, retrained head.
```

The development note, from the model owner:

```text
Base: Fieldstone base encoder 2.1 (licensed from Fieldstone Labs, used unmodified, frozen); Northwind trained a twelve-way linear head on it.
Objective: macro F1 over twelve intents (queues differ in size by a factor of 40). Confidence threshold 0.60: below it the message goes to the human triage queue; chosen so the human queue stays under 15% of traffic; trade-off against recall on the billing-dispute intent.
Architecture: encoder feeds the head inside the Relay inference service, called by the router per message. Training: four A10 GPUs, about eight GPU-hours; validation and testing on CPU.
Data: 48,000 resolved support threads, January 2025 to June 2026, six customers; labeled by the support team, 10% double-labeled, agreement 0.91; names, addresses and account identifiers removed; near-duplicates dropped. Datasheet NW-DS-12.
Oversight: threshold routing to a person; agents can override any label from the console; overrides logged with the original label; the confidence is the interpretation measure.
Pre-determined change: monthly retrain on the previous month's threads, same architecture and intent set; ships only at held-out accuracy >= 0.88.
Security: signed images, read-only model store at runtime, input limited to 4,000 characters, calls accepted from the router's service account only.
Input: UTF-8 text up to 4,000 characters, English, German or French.
```

The test summary, from the QA lead:

```text
Held-out set: 6,000 threads, same period and customers as training, resolution removed.
Accuracy 0.914; macro F1 0.89. By language: English 0.93, German 0.88, French 0.86. No discriminatory impact found between the six customers' traffic.
Foreseeable unintended outcome: a billing dispute routed to a general queue, refund delayed. No health or safety risk identified; the fundamental-rights risk is the delay.
Test report TR-0912 dated 2026-09-12. Responsible-person signature: pending, I have not signed it yet.
Post-market: 200 routed messages sampled and re-labeled weekly; accuracy below 0.88 alerts the model owner and blocks the monthly retrain from shipping; serious incidents reported under Article 73; plan NW-PMM-3.
```

The compliance note, from the compliance lead:

```text
Risk management under Article 9: register NW-RISK-14, reviewed quarterly; holds the misrouting risk per intent with likelihood and severity, the threshold and override as measures, the residual delay as accepted risk.
Harmonised standards: none applied. Solutions follow ISO/IEC 42001:2023 clauses 6 and 8 and internal specification NW-SPEC-7.
EU declaration of conformity NW-DoC-0007 under Article 47, dated 2026-09-20, attached.
```
