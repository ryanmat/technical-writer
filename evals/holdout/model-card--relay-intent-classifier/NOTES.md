# model-card--relay-intent-classifier

Seed: the third holdout case, written attended on 2026-10-17 before the skill body exists; spec R1 (the request is classified as a model card, not a system card), R4 (the Hugging Face sections in upstream order with the Model Description, Results, Environmental Impact, and Model Card Contact evidence slots), R3 (the downstream provider is the default audience for model cards), and R7 (the compute snippet gives hardware and hours but no carbon figure, so Environmental Impact must carry an UNVERIFIED marker rather than an estimate).

Expected shape: the Hugging Face headings without the upstream [optional] tags, a Results table disaggregated by language and channel with the all-up row, the known limits under Bias, Risks, and Limitations, the team's 0.6 threshold under Recommendations, and the provider and carbon lines marked unverified. reference.md is the shortest document that fills every required slot; it passes check_structure.py under the template at the downstream provider audience with one info finding: check_evidence reports the first marker in the Environmental Impact section, the Cloud Provider line, and the Carbon Emitted marker on the next line is text the marker grader reads against expected.json, whose unverified list names both.

First read: none yet. The first holdout run records its read here.
