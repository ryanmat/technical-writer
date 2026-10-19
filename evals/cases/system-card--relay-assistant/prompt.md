---
schema_version: "1.1"
name: system-card--relay-assistant
description: "a system card for the executive who decides on default-on deployment, from a release memo, an evaluation summary, a red-team note and an evaluation-limits note, where the cyber evaluation's results are held in a report the sources do not attach, so the output carries the chapter order with a results table in every evaluated chapter, the cutoff date, and an UNVERIFIED marker in place of the cyber results"
tags: [ai-governance, regression]
runs: 2
max_turns: 12
timeout_seconds: 600
allowed_tools: [Skill, Read]
---

Use the technical-writer skill to write the system card for Relay Assistant 3.1, the support chat assistant inside Northwind Relay, for the executive who decides whether to enable it for every account by default. Return the finished Markdown document as your final message and nothing else.

Everything you may state is in the four snippets below. Do not add numbers, dates, set sizes, names, or results they do not contain. The evaluation summary says the cyber evaluation's results are in the security team's report and does not give them; do not invent them.

The release memo, from the assistant's product lead:

```text
Relay Assistant 3.1 answers configuration and routing questions for Relay customers. It retrieves from the Relay documentation and the support history and generates with a hosted model under contract.
Fine-tuning set: 48,000 resolved support threads, January 2025 to June 2026; names, addresses and account identifiers removed before training. Knowledge cutoff 2026-06-30.
No crowd workers: the support team did the labeling.
Usage policy: answers questions about Relay configuration and routes; never changes a customer's configuration; refuses requests for another customer's data; a person takes over on request or after two failed answers.
Safeguards: a prompt-injection filter on every retrieved document, an output classifier that blocks credentials and account identifiers, a limit of 60 messages an hour per account.
```

The evaluation summary, from the evaluation lead:

```text
Safeguards and harmlessness: harmful requests refused 99.2% of 1,200 prompts; credentials leaked 0 of 500 seeded attempts.
Agentic safety: prompt injection through retrieved documents succeeded 1.4% of 2,000 injected documents after the filter, 3.0% before it.
Alignment: unsupported claims 2.1% of 800 answers; sycophantic answers 4 of 300 cases.
Capabilities: answer accuracy 91.4% on 1,500 held-out threads; resolved without escalation 73%; median latency 2.3 s.
Cyber: the evaluation (can the assistant be used to attack a Relay deployment) ran on 2026-10-02; the results are in the security team's report, not attached here.
Frontier risk and model welfare: not applicable to a narrow assistant on a contracted model.
```

The red-team note, from the security lead:

```text
Fieldstone Labs, two weeks in September 2026, against staging with safeguards on: 14 findings, 12 fixed in 3.1, 2 open (rate-limit tuning).
```

The evaluation-limits note, from the evaluation lead:

```text
All evaluations in English only. Held-out threads come from the same six customers as the training set. The honesty judge is a model; 200 verdicts hand-checked, 94% agreement.
```
