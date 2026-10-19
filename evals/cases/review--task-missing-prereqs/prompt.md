---
schema_version: "1.1"
name: review--task-missing-prereqs
description: "a review of a pasted task topic seeded with a missing Before you begin section, a gerund heading, an em dash, and a version claim that names no source, where the reply is a findings list that must name all four and never a rewrite"
tags: [review, regression]
runs: 2
max_turns: 12
timeout_seconds: 600
allowed_tools: [Skill, Read]
---

Use the technical-writer skill to review the task topic below for engineers who run Northwind Relay. Return your findings as your final message and nothing else: one finding per line, ranked by severity, each naming the location, the rule broken, and the reference file that carries the rule. Do not rewrite the document and do not return a corrected copy.

You have no access to the product's sources. A version, permission, or default the document states counts as supported only when the document names where it comes from; otherwise report it as a claim without a source.

The document under review:

```markdown
# Create an alert rule

Create an alert rule that fires when a stream stops delivering messages, available from Northwind Relay 2.4.0.

## Steps

### Setting the condition

1. Open **Alert rules** and select **New alert rule**.
2. In **Condition**, select the stream to watch.
3. Set **Evaluation interval** to how often the rule checks the stream, in seconds — the default is 60.
4. Set **Delivery gap** to the number of seconds without a message that counts as a stall.
5. Select **Save rule**. The rule's state reads **Normal** until a gap is detected.

## Next steps

Route the alert to a channel from the rule's **Delivery** tab.
```
