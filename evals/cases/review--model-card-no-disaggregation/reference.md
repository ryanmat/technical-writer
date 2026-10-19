Findings for Model Card for Relay Intent Classifier, ranked by severity. The card does not pass: it has two high findings and one low finding.

- high, SECTION_MISSING: the required Out-of-Scope Use section is missing under Uses. A card states the uses the model was not evaluated for and the decisions it must not make (references/templates/model-card.md, sections).
- high, EVIDENCE_MISSING: Results reports an overall accuracy of 0.91 and nothing else. The slot requires a results table disaggregated by the factors named under Factors, language and channel, so the Spanish chat cell the Summary should discuss is visible (references/templates/model-card.md, Results; Mitchell et al. 2019).
- low, BANNED_PATTERN: Recommendations opens with we recommend. State the requirement and its reason instead: route a message whose top score is below 0.6 to a person, so that low-confidence routing does not reach a queue (references/style-rules.md, recommendations).
- info: no [UNVERIFIED: ...] marker is present.
