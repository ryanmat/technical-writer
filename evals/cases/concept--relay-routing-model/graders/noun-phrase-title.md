---
type: regex
pattern: "^# (?:How to|What is|Using|Understanding|Configuring|Creating)\\b"
flags: m
match: not_contains
---

Verifies: the title is not a task or question opener, the cheapest sign that the output is a concept and not a task topic.
Cannot verify: that the title is a noun phrase naming the feature; the h1_pattern in check_structure.py over the output owns the gerund check and the two-word minimum.
