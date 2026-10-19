# Model Card for Relay Intent Classifier

Relay Intent Classifier is a text classifier that assigns each incoming Northwind Relay support message, in English or Spanish, to one of twelve Relay queues.

## Model Details

### Model Description

- **Developed by:** Northwind Labs
- **Model type:** Text classification with twelve intent labels
- **Language(s) (NLP):** English, Spanish
- **License:** Apache-2.0
- **Finetuned from model:** `northwind/relay-base-v2`
- **Revision:** 1.2.0

## Uses

### Direct Use

Use the model to route each incoming support message to one of twelve Relay queues. Check your use against this sentence: one message in, one queue out.

### Out-of-Scope Use

Do not use the model for any decision about a person. Do not use it for languages other than English and Spanish, because they were not evaluated. Messages that mix languages were not evaluated either.

## Bias, Risks, and Limitations

Performance differs by language and channel. Spanish chat messages score lowest, with accuracy 0.84 and macro F1 0.79. English email messages score highest, with accuracy 0.94 and macro F1 0.91. See the Results table for every cell.

Chat messages under five words are often labeled billing, which is the most frequent intent. A short chat message routed to billing is therefore less reliable than the table suggests.

Mixed-language messages were not evaluated. [UNVERIFIED: no evaluation report data on mixed-language performance, so the size of the risk is unknown.]

### Recommendations

- Send messages with a top score below 0.6 to a person. This is the Northwind Labs team's recommendation.
- Review the routing of chat messages under five words, because they skew toward billing.
- Do not send mixed-language messages or languages other than English and Spanish to the model without your own evaluation.
- Do not use the output for any decision about a person.

## How to Get Started with the Model

Load the model at the pinned revision:

```python
from relay_intent import load

model = load("northwind/relay-intent-classifier", revision="1.2.0")
```

Pin `revision="1.2.0"`, because the results in this card apply to that revision only.

[UNVERIFIED: the inference call, its input format, and how to read the top score are not in the supplied sources, so no prediction example is given.]

## Training Details

### Training Data

The training data is 312,000 support messages from 2025-01 to 2025-12. The support team labeled them, and customer identifiers were removed before labeling.

| Factor | Share |
|---|---|
| English | 71% |
| Spanish | 29% |
| Email | 58% |
| Chat | 42% |

### Training Procedure

#### Training Hyperparameters

- **Training regime:** fp16 mixed precision
- **Epochs:** 3
- **Learning rate:** 2e-5
- **Batch size:** 64

## Evaluation

### Testing Data, Factors & Metrics

#### Testing Data

The test set is a held-out 10% of the 2025 messages, 34,600 messages. It has no overlap with the training data.

#### Factors

- Language: English, Spanish
- Channel: email, chat

#### Metrics

- Accuracy
- Macro F1 over the twelve intents

Macro F1 weights each intent equally, so it shows weakness on rarer intents that accuracy hides. The decision threshold is a top score of 0.6, below which messages go to a person.

### Results

| Language | Channel | Accuracy | Macro F1 |
|---|---|---|---|
| English | Email | 0.94 | 0.91 |
| English | Chat | 0.90 | 0.86 |
| Spanish | Email | 0.91 | 0.88 |
| Spanish | Chat | 0.84 | 0.79 |
| All | All | 0.91 | 0.87 |

#### Summary

Across all messages, accuracy is 0.91 and macro F1 is 0.87. The weakest cell is Spanish chat, with accuracy 0.84 and macro F1 0.79.

## Environmental Impact

- **Hardware Type:** 8 GPUs [UNVERIFIED: GPU model is not in the compute snippet]
- **Hours used:** 6 hours
- **Cloud Provider:** [UNVERIFIED: no provider in the sources]
- **Compute Region:** [UNVERIFIED: no region in the sources]
- **Carbon Emitted:** [UNVERIFIED: no carbon figure in the sources, and none is estimated]

## Model Card Contact

Send questions about the model to ml-cards@example.com.
