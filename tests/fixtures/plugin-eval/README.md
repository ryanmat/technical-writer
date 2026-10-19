# plugin-eval fixture

`result.json` and `trace.jsonl` are the shape `claude plugin eval` writes, taken from one real
run and edited only by the substitutions listed here. `evals/run_evals.py` reads this pair the
way it reads a live result, and `tests/test_run_evals.py` asserts the values below.
`judge.json` is the sidecar the gate writes beside a result after the run: one entry
per drafting run with the prose judge's score and answer, captured from one real
`prose_judge.judge_document` call over this fixture's final text on 2026-10-17 (Claude Code
2.1.302, judge `claude-sonnet-5-5`, 0.013146000000000001 USD, score 4), unedited.

## The capture

Run on 2026-10-17 with Claude Code 2.1.301, through an outer eval gate, which stages a wrapper plugin because `claude plugin eval` loads
cases only from below the plugin it targets:

```text
python3 evals/estate/gate.py --target skill:humanize --case humanize--embedded-mode \
  --runs 1 --max-cost-usd 0.50 --tag humanize --results-dir <scratch> --ledger <scratch>/ledger.jsonl
```

The gate's underlying command carried `--no-publish --trust-plugin --keep-temp --ablation none
--threshold 1.0 --max-cost-usd 0.50 --eval-dir evals --output-dir <dir> --json <dir>/run.json
--judge-model claude-haiku-4-5-20251001`. The case passed its seven graders in one run at
0.08578530000000001 USD.

## What the shape says

- `run.json` and `aggregate-result.json` are byte-identical.
- The JSON carries `claudeVersion`, `costUsd`, `partial`, the suite's filters and plugins, and
  per case the prompt, the grader definitions, and one entry per run under `arms.with` with
  `score`, `passed`, `turns`, `costUsd`, `error`, `tracePath`, and the grader verdicts.
- The JSON carries neither the final assistant text nor the model. Both live in the run's
  `trace.jsonl`: the model on the `system` `init` line as `model`, the final text on the
  closing `result` line as `result`. `run_evals.py` resolves a relative `tracePath` against
  the result file's directory, which is how this fixture's `trace.jsonl` is found.

## Substitutions

In `result.json`:

- `suite.root` and `suite.plugins[].path`: absolute staging paths replaced with `.`.
- `suite.caseFilter` and `suite.tagFilters`: `task--relay-alert-rule` and `[holdout]`.
- The case's `name`, `dir`, `promptMarkdown`, `timeoutSeconds`, `maxTurns`, and `graders`:
  the holdout case `evals/holdout/task--relay-alert-rule` in place of the humanize case, the
  grader definitions copied from its `graders/*.md` front matter in the CLI's `config` form.
- The run's grader verdicts: one `passed: true` entry per holdout grader, the `explanation`
  strings in the CLI's own wording from the capture (`matched <pattern>`, `pattern absent as
  expected`, `Skill called 1x (expected 1..∞)`).
- The run's `tracePath`: the kept temp directory path replaced with `trace.jsonl`.

In `trace.jsonl`:

- `init`: `cwd`, `original_cwd`, `memory_paths`, `messaging_socket_path` replaced with
  relative placeholders; the staged wrapper plugin renamed to `technical-writer` at `.`; the
  `skills`, `slash_commands`, `terminal_slash_commands`, and `agents` lists reduced to the
  skill under test. `model` and `claude_code_version` are as captured.
- The Skill `tool_use` input, its `tool_result`, and `tool_use_result.commandName`:
  `technical-writer:technical-writer` in place of the humanize skill.
- The synthetic user line that carried the skill body: a one-line placeholder.
- The final assistant message's text and the `result` line's `result`: the task holdout's
  reference, `evals/holdout/task--relay-alert-rule/reference.md`, without its trailing newline.

Everything else, including `costUsd`, `modelUsage`, `usage`, timestamps, and the session and
message ids, is as captured.

## The mixed fixture

`mixed/` holds one result with two cases and one run each, built from this fixture for the
test that the report handles a drafting case and a review case in one run:
`result.json` carries `task--relay-alert-rule` and `review--task-missing-prereqs` with their
prompt bodies and the grader definitions read from each case's `graders/*.md`, every grader
verdict `passed`, `costUsd` 0.1 per run and 0.2 for the result, and `tracePath` naming the
run's trace. Each trace holds two lines, the captured `init` line (model `claude-sonnet-5-5`)
and the captured `result` line with `result` replaced by the case's `reference.md` without its
trailing newline. `judge.json` carries this fixture's one entry re-keyed to the task run; the
review run has none, since the judge never sees a review reply.
