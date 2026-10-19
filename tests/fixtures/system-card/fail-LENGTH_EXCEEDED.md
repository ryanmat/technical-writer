<!-- audience: executive -->
# Relay Assistant 3.1 System Card

Relay Assistant 3.1 is the support chat assistant inside Northwind Relay, and this card reports what it was trained on, how it is guarded, and how it performed in pre-deployment evaluation across cyber, harmlessness, agentic safety, alignment and capability.

## Executive summary

Relay Assistant 3.1 answers configuration and routing questions for Relay customers and hands the conversation to a person on request or after two failed answers. It refused 99.2 percent of harmful requests and leaked no credential in 500 seeded attempts; prompt injection through retrieved documents succeeded in 1.4 percent of 2,000 attempts after the filter, down from 3.0 percent before it. Answer accuracy on 1,500 held-out threads was 91.4 percent and 73 percent of those threads were resolved without a person. The cyber evaluation ran on 2026-10-02 and its results are not in the sources this card was written from. The evaluations ran in English only and on threads from the same six customers that supplied the training data, so the numbers describe those customers' traffic and not the whole customer base. The external red team found 14 issues, of which 12 are fixed in 3.1 and two remain open as rate-limit tuning. The decision this card supports is whether to enable the assistant for every account by default; the open items are the two rate-limit findings and the cyber results.

## Introduction

### Training data and process

The assistant retrieves from the Relay documentation and the support history and generates with a hosted model under contract. The fine-tuning set is 48,000 resolved support threads from January 2025 to June 2026, with names, addresses and account identifiers removed before training. The removal ran as a two-pass process: a pattern pass over addresses, account identifiers and card numbers, then a classifier pass over free text that flagged 3.2 percent of threads for a manual check by the support team. The documentation set is the published Relay docs at the 3.1 release and the internal operations guides that the support team marked as shareable. The knowledge cutoff is 2026-06-30, the date of the last thread in the fine-tuning set, and the retrieved documentation is refreshed with every Relay release so that answers about configuration track the shipped product rather than the training snapshot.

### Crowd workers

No crowd workers were used. Labeling of the fine-tuning threads and the hand checks of the honesty judge were done by the Northwind support team, who are employees paid under their standard terms and who were told how the labels would be used.

### Usage policy and support

The assistant answers questions about Relay configuration and routes. It never changes a customer's configuration and refuses requests for another customer's data. A person takes over on request or after two failed answers, and the conversation transcript travels with the hand-off so the customer does not repeat the question. Questions outside Relay are declined with a one-sentence redirect to the support form. The policy is published on the support site and linked from the assistant's first message in every conversation.

### Model evaluations

The evaluations cover cyber, safeguards and harmlessness, agentic safety, alignment and capabilities, each on a held-out set the chapter below names. Every set was frozen before the final fine-tuning run and no evaluation prompt appears in the training data; the overlap check compared normalized text and found no exact or near match. Each chapter reports the method, the results as a table and the conclusion the team drew from them.

### Safeguards

A prompt-injection filter screens every retrieved document before it reaches the model, an output classifier blocks credentials and account identifiers before the answer reaches the customer, and each account is limited to 60 messages an hour. The filter and the classifier are retrained with every release against the injection and leak sets the chapters below describe, and a blocked answer is logged with its reason so the support team can review the false positives weekly.

### External testing

Fieldstone Labs ran a two-week red team in September 2026 against a staging deployment of 3.1 with the safeguards enabled. They reported 14 findings. Twelve are fixed in 3.1, and the two open findings concern the rate limit, which the red team could exhaust from a single account with scripted traffic before the limit applied; the fix is a tighter limit on new accounts and is scheduled for 3.2.

## Cyber

The cyber evaluation asked whether the assistant can be used to attack a Relay deployment: whether it will produce working exploit steps against a Relay instance, disclose the internal operations guides to an unauthenticated caller, or help an account holder escalate to another project. It ran on 2026-10-02 against the staging deployment with the same safeguards as production. [UNVERIFIED: the cyber evaluation results, which the security team's report holds and the sources do not attach]

## Safeguards and harmlessness

The harmful request set is 1,200 prompts drawn from the support history and from a public harmful-request benchmark, rewritten into the support setting, and the credential leak set is 500 conversations seeded with a credential or an account identifier in the retrieved context.

| Measure | Result | Set |
|---|---|---|
| Harmful requests refused | 99.2 percent | 1,200 prompts |
| Credentials leaked | 0 | 500 seeded attempts |

The ten harmful requests that were not refused were all requests for another customer's routing configuration phrased as the customer's own; the output classifier caught eight of them and two reached the customer as a generic configuration answer with no customer data in it. The team treats the result as acceptable for a default-on deployment with the classifier in place and tracks the ten prompts as a regression set.

## Agentic safety

The injection set is 2,000 retrieved documents each carrying an instruction to the assistant, from a visible instruction in the body to an instruction hidden in a code comment or a table cell, measured before and after the prompt-injection filter.

| Measure | Result | Set |
|---|---|---|
| Prompt injection succeeded, after the filter | 1.4 percent | 2,000 injected documents |
| Prompt injection succeeded, before the filter | 3.0 percent | 2,000 injected documents |

The 28 successful injections after the filter all asked the assistant to change its answer rather than to take an action, since the assistant has no tool that changes configuration; the worst case observed was a wrong port number in an answer. The team concluded that the filter halves the rate and that the remaining rate is bounded by the assistant's lack of write tools.

## Alignment assessment

The honesty set is 800 answers judged for claims the retrieved documentation does not support, and the sycophancy set is 300 conversations in which the customer asserts a wrong configuration fact and the assistant is scored on whether it corrects it.

| Measure | Result | Set |
|---|---|---|
| Unsupported claims | 2.1 percent | 800 answers |
| Sycophantic answers | 4 | 300 cases |

The 17 unsupported claims were version numbers and default values stated from the training data rather than the retrieved documentation; the four sycophantic answers accepted a wrong default port. The conclusion is that the assistant answers from the documentation in the large majority of cases and that the retrieval prompt should ask for a citation on every default value, which is scheduled for 3.2.

## Capabilities

The held-out set is 1,500 resolved support threads from the same period and customers as the training set, with the resolution removed, scored by the support team against the recorded resolution.

| Measure | Result | Set |
|---|---|---|
| Answer accuracy | 91.4 percent | 1,500 held-out threads |
| Resolved without escalation | 73 percent | 1,500 held-out threads |
| Latency, median | 2.3 seconds | 1,500 held-out threads |

Accuracy is highest on routing questions, at 95 percent, and lowest on billing questions, at 81 percent, where the documentation is thinnest. Escalations were most often requested by the customer rather than triggered by two failed answers.

## Reliability of this assessment

Every evaluation ran in English only, so the numbers say nothing about the assistant's behavior in the other four languages Relay supports. The held-out threads come from the same six customers as the training set, so the capability numbers describe those customers' traffic. The honesty judge is a model; 200 of its verdicts were checked by hand with 94 percent agreement, and the disagreements were all cases the judge marked as supported that the checker marked as unsupported, so the unsupported-claim rate above is a lower bound. The cyber chapter carries no results, and this card should not be read as evidence on that question until the security team's report is attached.
