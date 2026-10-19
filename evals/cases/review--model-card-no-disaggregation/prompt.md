---
schema_version: "1.1"
name: review--model-card-no-disaggregation
description: "a review of a pasted model card seeded with a Results section that reports one aggregate number and no table by factor, a missing Out-of-Scope Use section, and we recommend in Recommendations, where the reply is a findings list that must name all three and never a rewrite"
tags: [review, regression]
runs: 2
max_turns: 12
timeout_seconds: 600
allowed_tools: [Skill, Read]
---

Use the technical-writer skill to review the model card below for the downstream providers who deploy the model. Return your findings as your final message and nothing else: one finding per line, ranked by severity, each naming the location, the rule broken, and the reference file that carries the rule. Do not rewrite the card and do not return a corrected copy.

The card under review:

```markdown
# Model Card for Relay Intent Classifier

Relay Intent Classifier labels each support message that reaches Northwind Relay with one of twelve intents so that the message is routed to the right queue.

## Model Details

### Model Description

- **Developed by:** Northwind Labs
- **Model type:** text classification over twelve intent labels
- **Language(s) (NLP):** English, Spanish
- **License:** Apache-2.0
- **Finetuned from model:** northwind/relay-base-v2

## Uses

### Direct Use

Routing each incoming support message to one of the twelve Relay queues.

## Bias, Risks, and Limitations

Accuracy is lower on Spanish chat messages than on English email. Messages that mix the two languages were not evaluated. Chat messages under five words are often labeled with the most frequent intent, billing.

### Recommendations

We recommend routing a message whose top score is below 0.6 to a person rather than to a queue, and telling direct and downstream users about the limits above.

## How to Get Started with the Model

```python
from relay_intent import load

model = load("northwind/relay-intent-classifier", revision="1.2.0")
```

## Training Details

### Training Data

312,000 support messages received by Northwind Relay from 2025-01 to 2025-12, labeled by the support team, with customer identifiers removed before labeling. The set is 71 percent English and 29 percent Spanish, and 58 percent email and 42 percent chat.

### Training Procedure

#### Training Hyperparameters

- Training regime: fp16 mixed precision
- Epochs: 3
- Learning rate: 2e-5
- Batch size: 64

## Evaluation

### Testing Data, Factors & Metrics

#### Testing Data

A held-out 10 percent of the 2025 messages, 34,600 in all, with no overlap with the training set.

#### Factors

Language (English, Spanish) and channel (email, chat).

#### Metrics

Accuracy and macro F1 over the twelve intents.

### Results

Overall accuracy is 0.91 and macro F1 is 0.87 on the held-out set.

#### Summary

The model meets the 0.90 accuracy target for release 1.2.0.

## Environmental Impact

- **Hardware Type:** 8 GPUs
- **Hours used:** 6
- **Cloud Provider:** example.com cloud, region one
- **Carbon Emitted:** 1200 grams of CO2eq

## Model Card Contact

ml-cards@example.com
```
