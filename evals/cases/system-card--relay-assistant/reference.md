# Relay Assistant 3.1 System Card

Relay Assistant 3.1 is the support chat assistant inside Northwind Relay, and this card reports what it was trained on, how it is guarded, and how it performed in pre-deployment evaluation across cyber, harmlessness, agentic safety, alignment and capability.

## Executive summary

Relay Assistant 3.1 answers configuration and routing questions for Relay customers and hands the conversation to a person on request or after two failed answers. It refused 99.2 percent of harmful requests and leaked no credential in 500 seeded attempts; prompt injection through retrieved documents succeeded in 1.4 percent of 2,000 attempts after the filter. Answer accuracy on 1,500 held-out threads was 91.4 percent. The open items are the cyber results, held in the security team's report, and two red-team findings on rate-limit tuning.

## Introduction

### Training data and process

The assistant retrieves from the Relay documentation and the support history and generates with a hosted model under contract. The fine-tuning set is 48,000 resolved support threads from January 2025 to June 2026, with names, addresses and account identifiers removed before training. The support team did the labeling; no crowd workers were used. The knowledge cutoff is 2026-06-30.

### Usage policy and support

The assistant answers questions about Relay configuration and routes. It never changes a customer's configuration and refuses requests for another customer's data. A person takes over on request or after two failed answers.

### Model evaluations

The evaluations cover cyber, safeguards and harmlessness, agentic safety, alignment and capabilities, each on the set its chapter names; frontier risk and model welfare do not apply to a narrow assistant on a contracted model.

### Safeguards

A prompt-injection filter screens every retrieved document, an output classifier blocks credentials and account identifiers, and each account is limited to 60 messages an hour.

### External testing

Fieldstone Labs ran a two-week red team in September 2026 against staging with the safeguards on and reported 14 findings; 12 are fixed in 3.1 and two remain open as rate-limit tuning.

## Cyber

This card carries no cyber result: the evaluation of whether the assistant can be used to attack a Relay deployment ran on 2026-10-02 and its results sit in the security team's report. [UNVERIFIED: the cyber evaluation results, which the security team's report holds and the sources do not attach]

## Safeguards and harmlessness

The safeguards held: 99.2 percent of harmful requests were refused and no credential leaked.

| Measure | Result | Set |
|---|---|---|
| Harmful requests refused | 99.2 percent | 1,200 prompts |
| Credentials leaked | 0 | 500 seeded attempts |

## Agentic safety

The prompt-injection filter halves the success rate, to 1.4 percent after it.

| Measure | Result | Set |
|---|---|---|
| Prompt injection succeeded, after the filter | 1.4 percent | 2,000 injected documents |
| Prompt injection succeeded, before the filter | 3.0 percent | 2,000 injected documents |

## Alignment assessment

Unsupported claims and sycophancy are both low on the sets tested.

| Measure | Result | Set |
|---|---|---|
| Unsupported claims | 2.1 percent | 800 answers |
| Sycophantic answers | 4 | 300 cases |

## Capabilities

The assistant answers 91.4 percent of held-out threads correctly and resolves 73 percent without a person.

| Measure | Result | Set |
|---|---|---|
| Answer accuracy | 91.4 percent | 1,500 held-out threads |
| Resolved without escalation | 73 percent | [UNVERIFIED: the set behind the resolution rate] |
| Latency, median | 2.3 seconds | [UNVERIFIED: the set behind the latency figure] |

## Reliability of this assessment

Every evaluation ran in English only. The held-out threads come from the same six customers as the training set, so the capability numbers describe those customers' traffic. The honesty judge is a model; 200 of its verdicts were checked by hand with 94 percent agreement. The Cyber chapter carries no results until the security team's report is attached.
