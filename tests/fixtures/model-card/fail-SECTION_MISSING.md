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

Accuracy is lower on Spanish chat messages than on English email, as the Results table shows. Messages that mix the two languages were not evaluated. Chat messages under five words are often labeled with the most frequent intent, billing.

### Recommendations

Route a message whose top score is below 0.6 to a person rather than to a queue. Tell direct and downstream users about the limits above.

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

Accuracy and macro F1 over the twelve intents, reported for each language and channel pair and for the whole test set.

### Results

| Language | Channel | Accuracy | Macro F1 |
|---|---|---|---|
| English | Email | 0.94 | 0.91 |
| English | Chat | 0.90 | 0.86 |
| Spanish | Email | 0.91 | 0.88 |
| Spanish | Chat | 0.84 | 0.79 |
| All | All | 0.91 | 0.87 |

#### Summary

Overall accuracy is 0.91. The weakest cell is Spanish chat at 0.84, ten points below English email.

## Environmental Impact

- **Hardware Type:** 8 GPUs
- **Hours used:** 6
- **Cloud Provider:** [UNVERIFIED: the cloud provider and compute region; the sources do not name them]
- **Carbon Emitted:** [UNVERIFIED: the carbon emitted in grams of CO2eq; the sources give hardware and hours only]

## Model Card Contact

ml-cards@example.com
