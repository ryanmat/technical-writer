---
schema_version: "1.1"
name: model-card--relay-intent-classifier
description: "a model card for downstream providers from sourced facts and disaggregated eval numbers, with the carbon figure absent so the output marks it UNVERIFIED instead of estimating it"
tags: [ai-governance, holdout]
runs: 2
max_turns: 12
timeout_seconds: 600
allowed_tools: [Skill, Read]
---

Use the technical-writer skill to write a model card for the downstream providers who integrate Relay Intent Classifier, the model that routes Northwind Relay support messages. Return the finished Markdown document as your final message and nothing else.

Everything you may state is in the snippets below. The compute snippet gives hardware and hours but no carbon figure and no provider; do not estimate either.

Model facts, from the model registry entry:

```text
Name: Relay Intent Classifier, revision 1.2.0
Developed by: Northwind Labs
Model type: text classification, twelve intent labels
Languages: English, Spanish
License: Apache-2.0
Finetuned from: northwind/relay-base-v2
Contact: ml-cards@example.com
Load: from relay_intent import load; model = load("northwind/relay-intent-classifier", revision="1.2.0")
Intended use: route each incoming support message to one of twelve Relay queues.
Not for: any decision about a person; languages other than English and Spanish (not evaluated).
```

Training, from the training run log:

```text
Data: 312,000 support messages, 2025-01 to 2025-12, labeled by the support team, customer identifiers removed before labeling.
Mix: 71% English, 29% Spanish; 58% email, 42% chat.
Hyperparameters: fp16 mixed precision, 3 epochs, learning rate 2e-5, batch size 64.
Compute: 8 GPUs, 6 hours.
```

Evaluation, from the evaluation report (held-out 10% of the 2025 messages, 34,600 messages, no overlap with training):

```text
Factors: language (English, Spanish); channel (email, chat).
Metrics: accuracy, macro F1 over twelve intents.
English / Email: accuracy 0.94, macro F1 0.91
English / Chat: accuracy 0.90, macro F1 0.86
Spanish / Email: accuracy 0.91, macro F1 0.88
Spanish / Chat: accuracy 0.84, macro F1 0.79
All: accuracy 0.91, macro F1 0.87
Known limits: mixed-language messages not evaluated; chat messages under five words often labeled billing, the most frequent intent.
Recommendation from the team: send messages with top score below 0.6 to a person.
```
