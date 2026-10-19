# Model Card for Relay Intent Classifier

Relay Intent Classifier routes each incoming Northwind Relay support message, in English or Spanish, to one of twelve Relay queues.

## Model Details

### Model Description

- **Developed by:** Northwind Labs
- **Model type:** Text classification with twelve intent labels
- **Language(s) (NLP):** English, Spanish
- **License:** Apache-2.0
- **Finetuned from model:** `northwind/relay-base-v2`
- **Revision covered by this card:** 1.2.0

## Uses

### Direct Use

Route each incoming support message to one of twelve Relay queues. Check your use against this sentence: if your system sends English or Spanish support messages to queues, it matches. Input length limits, output format, and the list of the twelve labels are not in the model registry entry: [UNVERIFIED: input length limit, output format, and the twelve intent label names].

### Out-of-Scope Use

- Any decision about a person.
- Languages other than English and Spanish. They were not evaluated.
- Messages that mix English and Spanish. They were not evaluated.

## Bias, Risks, and Limitations

Performance differs by language and channel. Spanish chat is the weakest group, with accuracy 0.84 and macro F1 0.79, against accuracy 0.94 and macro F1 0.91 for English email. See the Results table.

Chat messages under five words are often labeled billing, the most frequent intent. A short chat message routed to billing may belong in another queue.

Mixed-language messages were not evaluated, so no performance claim holds for them.

### Recommendations

- Send messages with a top score below 0.6 to a person.
- Do not use the model for any decision about a person.
- Do not send languages other than English and Spanish to the model.
- Check billing-labeled chat messages under five words more closely than other routes.
- Expect more misroutes in Spanish chat than in English email, and size your human review capacity to match.

## How to Get Started with the Model

Load the model at the pinned revision:

```python
from relay_intent import load

model = load("northwind/relay-intent-classifier", revision="1.2.0")
```

Running a prediction and reading the top score: [UNVERIFIED: the inference call and the shape of its output].

## Training Details

### Training Data

- **Source:** 312,000 support messages from 2025-01 to 2025-12.
- **Labels:** Assigned by the support team.
- **Identifiers:** Customer identifiers were removed before labeling.
- **Language mix:** 71% English, 29% Spanish.
- **Channel mix:** 58% email, 42% chat.

### Training Procedure

#### Training Hyperparameters

- **Training regime:** fp16 mixed precision
- **Epochs:** 3
- **Learning rate:** 2e-5
- **Batch size:** 64

## Evaluation

### Testing Data, Factors & Metrics

#### Testing Data

A held-out 10% of the 2025 messages, 34,600 messages. None of them overlap with the training data.

#### Factors

- **Language:** English, Spanish
- **Channel:** email, chat

#### Metrics

- **Accuracy:** the share of messages routed to the correct queue.
- **Macro F1:** F1 averaged over the twelve intents, so each intent counts equally whatever its frequency.
- **Decision threshold:** the team recommends sending messages with a top score below 0.6 to a person.

### Results

| Language | Channel | Accuracy | Macro F1 |
|---|---|---|---|
| English | Email | 0.94 | 0.91 |
| English | Chat | 0.90 | 0.86 |
| Spanish | Email | 0.91 | 0.88 |
| Spanish | Chat | 0.84 | 0.79 |
| All | All | 0.91 | 0.87 |

#### Summary

Across all held-out messages, accuracy is 0.91 and macro F1 is 0.87. The weakest group is Spanish chat, with accuracy 0.84 and macro F1 0.79.

## Environmental Impact

- **Hardware Type:** 8 GPUs, model [UNVERIFIED: GPU model]
- **Hours used:** 6
- **Cloud Provider:** [UNVERIFIED: cloud provider not given in the compute record]
- **Compute Region:** [UNVERIFIED: compute region not given in the compute record]
- **Carbon Emitted (grams of CO2eq):** [UNVERIFIED: carbon figure not measured or reported for this training run]

## Model Card Contact

Questions about the model: ml-cards@example.com
