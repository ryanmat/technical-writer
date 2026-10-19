# Technical documentation for Relay Intent Classifier 1.2.0

This file is the technical documentation under Article 11(1) and Annex IV of Regulation (EU) 2024/1689 for Relay Intent Classifier 1.2.0, the model that assigns each Northwind Relay support message to one of twelve intent queues, as the compliance lead requested on 2026-10-18.

## General description of the AI system

**Intended purpose, provider and version:** the system labels each incoming support message with one of twelve intents so that the Relay router delivers it to the matching queue. The provider is Northwind Labs. Version 1.2.0 replaces 1.1.3; it keeps the 1.1 architecture and intent set and was retrained on a larger set.

**Interaction with hardware and software:** the system receives messages from the Relay router over gRPC and returns a label and a confidence; it calls no other AI system.

**Software and firmware versions:** inference service 3.4.1; the model store accepts only images signed by the Northwind release key, and a version update requires a new signed image.

**Forms of placing on the market:** a container image for the customer's Relay cluster, and the hosted Relay API.

**Hardware:** the customer's Kubernetes cluster, one CPU core and 2 GB of memory per replica; no accelerator at inference.

**Component of products:** not applicable; the system is software with no physical product.

**User interface and instructions for use:** the deployer sees the queue label and the confidence beside each message in the Relay console; the instructions for use are the Relay operator guide 1.2.

## Elements of the AI system and the development process

### Development methods and steps

The system is a fine-tuned classifier on the Fieldstone base encoder 2.1, a pre-trained text encoder licensed from Fieldstone Labs and used unmodified; Northwind Labs trained a twelve-way linear head on it and froze the encoder.

### Design specifications

The system optimises macro F1 over the twelve intents, since the queues are unequal in size and a frequency-weighted score would hide the small queues. The key design choice is the confidence threshold of 0.60: a message below it goes to the human triage queue. The expected output is one label and one confidence per message. The trade-off recorded is between recall on the billing-dispute intent and the size of the human queue; the threshold was set so that the human queue stays under 15 percent of traffic.

### System architecture and computational resources

The encoder feeds the linear head inside the Relay inference service, which the router calls per message. Training used four A10 GPUs for about eight GPU-hours; validation and testing ran on CPU.

### Data requirements and datasheets

The training set is 48,000 resolved support threads from January 2025 to June 2026 from six customers, labeled by the Northwind support team; 10 percent was double-labeled with an agreement of 0.91. Names, addresses and account identifiers were removed and near-duplicate threads dropped before training. The datasheet is NW-DS-12.

### Human oversight

A message below the 0.60 confidence goes to a person, and a support agent can override any label from the console; overrides are logged with the original label so the deployer can read where the system errs. The confidence beside each label is the interpretation measure under Article 13(3), point (d).

### Pre-determined changes

The system is retrained monthly on the previous month's resolved threads within the same architecture and intent set; a retrained model ships only when its held-out accuracy is at or above 0.88, so the change is pre-determined and bounded.

### Validation and testing

Validation and testing used 6,000 held-out threads from the same period and customers as the training set, with the resolution removed. Accuracy was 0.91 and macro F1 0.89; accuracy by language was 0.93 in English, 0.88 in German and 0.86 in French. No discriminatory impact was found between the six customers' traffic. The test logs and test report TR-0912 are held by the QA team.

### Cybersecurity measures

Model images are signed with the Northwind release key and the model store is read-only at runtime; input is limited to 4,000 characters; the inference service accepts calls from the router's service account only.

## Monitoring, functioning and control

The system's accuracy is 0.91 overall and 0.93, 0.88 and 0.86 in English, German and French, so a French-speaking customer's message is misrouted about one time in seven. The foreseeable unintended outcome is a billing dispute routed to a general queue and its refund delayed; no risk to health or safety was identified, and the risk to fundamental rights is the delay itself. The human oversight measures are the threshold and the override under Human oversight above. Input data is UTF-8 text of up to 4,000 characters in English, German or French.

## Appropriateness of the performance metrics

Macro F1 is the right metric because the twelve queues differ in size by a factor of 40 and the cost of a misroute is the same in every queue; accuracy is reported beside it because the deployer reads accuracy. Per-language accuracy is reported because language is the factor the error rate varies by.

## Risk management system

The risk register NW-RISK-14 is maintained under Article 9 and reviewed quarterly; it holds the misrouting risk per intent with its likelihood and severity, the threshold and the override as the measures, and the residual delay as the accepted risk.

## Changes through the lifecycle

Version 1.0 shipped in September 2025 with English only; 1.1 added German and French in February 2026; 1.2.0 retrained the head on the larger set in September 2026 with the same architecture and intent set.

## Harmonised standards and other technical specifications

No harmonised standard with a reference published in the Official Journal of the European Union was applied. The solutions adopted follow ISO/IEC 42001:2023 clauses 6 and 8 and the internal specification NW-SPEC-7.

## EU declaration of conformity

The EU declaration of conformity NW-DoC-0007 under Article 47, dated 2026-09-20, is attached to this file.

## Post-market monitoring

Each week 200 routed messages are sampled and re-labeled by the support team; an accuracy below 0.88 raises an alert to the model owner and stops the monthly retrain from shipping. Serious incidents are reported under Article 73. The post-market monitoring plan under Article 72(3) is NW-PMM-3.
