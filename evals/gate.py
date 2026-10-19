#!/usr/bin/env python3
# Description: Runs `claude plugin eval` over this plugin's cases with the safety flags fixed,
# Description: keeps each run's trace beside the result, grades it, and exits 0, 1 or 2.
"""The eval gate.

One invocation runs the selected cases (``--tag``, ``--case``) against this plugin at ``.``,
with the report kept local, one arm, the CLI threshold at 1.0 (a run passes only with every
grader), one model unless ``--model`` says otherwise, and the CLI's own cost ceiling fixed.
The result lands at ``evals/results/<stamp>/run.json`` with each run's ``trace.jsonl`` copied
beside it. The CLI's ``llm`` grader keeps only its three votes, so the gate then sends each
drafting run's final text to the prose judge (``prose_judge.judge_document``, the same model
and criteria as the grader) and writes ``judge.json`` beside the result; ``run_evals`` grades
every run's final text, reads the score, and the gate judges each case against its bar: a run
passes when the CLI's graders and the structural checker both pass it, a holdout case when
two runs of three pass, a regression case when at least half its runs do (the plan's Conventions
fix both bars; the case's set tag in ``prompt.md`` picks one). A gated model (Sonnet 5.5,
Opus 5) must also meet the judge's rule over its runs: a median of at least 4 and no run
below 3; any other model's scores are recorded. The report pair lands under
``evals/reports/``. Exit codes: 0 every case at or above
its bar and every gated model at the rule, 1 a case below its bar or a gated model below the
rule, 2 apparatus (the CLI missing, no aggregate written, a partial run such as the cost
ceiling, a sandbox refusal, a case with no set tag, a judge call that failed, or a result the
grader cannot read). ``--dry-run`` prints the argv and spawns nothing.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import shlex
import shutil
import stat
import subprocess
import sys
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from fractions import Fraction
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import prose_judge  # noqa: E402  (a sibling module, loaded after the path insert)
import run_evals  # noqa: E402
from check_structure import FRONT_MATTER  # noqa: E402  (run_evals put scripts/ on the path)
from run_evals import UNSAFE_LABEL  # noqa: E402

DEFAULT_RESULTS = HERE / "results"
DEFAULT_REPORTS = HERE / "reports"
THRESHOLD = "1.0"  # the CLI's per-run bar: every grader; not an option, the Conventions fix it
HOLDOUT_BAR = Fraction(2, 3)  # a holdout case: two runs of three pass both layers (the Conventions,
# amended by the 2026-10-18 11:30 EDT decision after the all-runs bar went red on single misses)
HOLDOUT_RUNS = 3  # the runs a holdout selection gets, since the holdout cases are never edited
REGRESSION_BAR = Fraction(1, 2)  # a regression case: at least half its runs do (the Conventions)
SET_TAGS = frozenset({"holdout", "regression"})
DEFAULT_MODEL = "claude-sonnet-5-5"  # one model per PASS; the plan's Conventions pin it
DEFAULT_JUDGE_MODEL = prose_judge.JUDGE_MODEL  # one judge for every llm grader and the calibration

# exit codes: 0 pass, 1 fail, 2 apparatus
PASS, FAIL, APPARATUS = 0, 1, 2

SANDBOX_REFUSAL = re.compile(r"sandbox|bubblewrap|bwrap|socat", re.I)
UNAVAILABLE = re.compile(r"unknown command|not (?:available|enabled)|early access", re.I)


class GateError(RuntimeError):
    """An apparatus failure: nothing about the plugin under test was measured. Exit 2."""


# ---- argv ---------------------------------------------------------------------


def parse_args(argv: list[str]) -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        prog="gate.py", description="run this plugin's eval cases through claude plugin eval"
    )
    ap.add_argument("--tag", action="append", default=None, help="case tag filter (repeatable)")
    ap.add_argument("--case", help="case name glob")
    ap.add_argument("--runs", type=int, help="runs per case; the case's own count by default")
    ap.add_argument(
        "--model", default=DEFAULT_MODEL, help=f"model for every case (default {DEFAULT_MODEL})"
    )
    ap.add_argument(
        "--judge-model",
        default=DEFAULT_JUDGE_MODEL,
        help=f"model for the llm graders (default {DEFAULT_JUDGE_MODEL})",
    )
    ap.add_argument(
        "--max-cost-usd",
        required=True,
        help=(
            "hard cost ceiling for the CLI run; the gate's own judge calls after it are "
            f"capped at {prose_judge.JUDGE_BUDGET_USD} USD each and are not under this ceiling"
        ),
    )
    ap.add_argument("--label", help="text appended to the result and report stamps")
    ap.add_argument("--results-dir", default=str(DEFAULT_RESULTS), help="where run.json lands")
    ap.add_argument("--reports-dir", default=str(DEFAULT_REPORTS), help="where the report lands")
    ap.add_argument("--dry-run", action="store_true", help="print the argv and exit")
    ns = ap.parse_args(argv)
    try:
        Decimal(ns.max_cost_usd)
    except InvalidOperation:
        ap.error("--max-cost-usd must be a decimal number")
    return ns


def build_argv(opts: argparse.Namespace, stamp: str) -> list[str]:
    """The safety flags are not options: every invocation keeps the report local, runs one
    arm, gates at 1.0, carries the CLI's own cap, trusts only this checkout, and keeps the
    run directories so each trace can be copied beside the result."""
    output_dir = Path(opts.results_dir) / stamp
    argv = [
        "claude",
        "plugin",
        "eval",
        ".",
        "--no-publish",
        "--trust-plugin",
        "--keep-temp",
        "--ablation",
        "none",
        "--threshold",
        THRESHOLD,
        "--max-cost-usd",
        f"{Decimal(opts.max_cost_usd):.2f}",
        "--eval-dir",
        "evals",
        "--output-dir",
        str(output_dir),
        "--json",
        str(output_dir / "run.json"),
    ]
    for tag in opts.tag or []:
        argv += ["--tag", tag]
    if opts.case:
        argv += ["--case", opts.case]
    if opts.runs is not None:
        argv += ["--runs", str(opts.runs)]
    elif selection_has_holdout(opts.tag, opts.case):
        argv += ["--runs", str(HOLDOUT_RUNS)]  # the holdout rule: three runs, two of three
    if opts.model:
        argv += ["--model", opts.model]
    if opts.judge_model:
        argv += ["--judge-model", opts.judge_model]
    return argv


# ---- classification ---------------------------------------------------------------


def classify(code: int, output: str, aggregate: Path) -> tuple[int, str]:
    """Map the CLI's exit and output onto the contract before any grading is read.

    No aggregate means nothing ran: a sandbox refusal, plugin eval unavailable, or a crash.
    An aggregate marked partial means the CLI stopped early (the cost ceiling, a login
    failure), whatever its exit; the results are not a verdict on the plugin.
    """
    if not aggregate.exists():
        if SANDBOX_REFUSAL.search(output):
            return (
                APPARATUS,
                "the CLI refused a Bash-carrying case for want of a sandbox backend; "
                "install bubblewrap and socat (Linux) or clear the ~/.docker symlink condition "
                "(macOS) and run again",
            )
        why = "the CLI produced no aggregate-result.json"
        if UNAVAILABLE.search(output):
            why += " (plugin eval unavailable at this version or gated)"
        return APPARATUS, f"{why}: exit {code}: {output.strip()[:400]}"
    try:
        data = json.loads(aggregate.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return APPARATUS, f"the aggregate {aggregate} cannot be read: {exc}"
    if data.get("partial") or data.get("partialReason"):
        reason = data.get("partialReason") or "unknown"
        why = f"the CLI stopped early (partialReason {reason}); the results are partial"
        if reason == "cost_ceiling":
            why += "; raise --max-cost-usd or narrow the selection"
        if reason == "auth_failed":
            why += "; claude is not logged in on this machine"
        return APPARATUS, why
    if code in (0, 1):
        # both are complete runs; a run below 1.0 exits 1, and the verdict is each case's bar
        return PASS, "the CLI completed; each case is judged against its bar"
    return APPARATUS, (
        f"unexpected CLI exit {code} with a complete aggregate: {output.strip()[:400]}"
    )


def never_exercised(case: dict) -> str | None:
    """The first run error of a case none of whose runs reached the agent: every run errored
    at zero turns with nothing graded (a sandbox refusal, a scaffold that failed). The CLI
    still writes the aggregate and exits 1, which is not a verdict on the plugin."""
    runs = (case.get("arms") or {}).get("with", [])
    dead = all(run.get("error") and not run.get("graders") and not run.get("turns") for run in runs)
    return str(runs[0]["error"]) if runs and dead else None


def check_exercised(aggregate: Path) -> None:
    """A green or red CLI exit is a verdict only when something was graded: at least one
    case, every case with runs, and no case whose every run died before the agent ran."""
    data = json.loads(aggregate.read_text(encoding="utf-8"))
    cases = data.get("cases") or []
    if not cases:
        raise GateError("no cases matched the selection; nothing was graded")
    empty = [case["name"] for case in cases if not (case.get("arms") or {}).get("with")]
    if empty:
        raise GateError(f"cases with zero runs recorded: {empty}")
    dead = {case["name"]: err for case in cases if (err := never_exercised(case))}
    if dead:
        first = next(iter(dead.values()))
        hint = (
            " Install bubblewrap and socat (Linux) or clear the ~/.docker symlink condition "
            "(macOS) and run again."
            if SANDBOX_REFUSAL.search(first)
            else ""
        )
        raise GateError(
            f"every run of {sorted(dead)} ended before the agent ran; the plugin was never "
            f"exercised. First error: {first[:300]}.{hint}"
        )


# ---- the bar ---------------------------------------------------------------------


def case_tags(case_dir: Path) -> list[str]:
    """The tags a case's ``prompt.md`` front matter carries; an unreadable file or front
    matter is apparatus."""
    prompt = case_dir / "prompt.md"
    try:
        text = prompt.read_text(encoding="utf-8")
    except OSError as exc:
        raise GateError(f"{case_dir.name}: cannot read {prompt}: {exc.strerror or exc}") from exc
    match = FRONT_MATTER.match(text)
    try:
        data = yaml.safe_load(match.group(1)) if match else None
    except yaml.YAMLError as exc:
        raise GateError(f"{case_dir.name}: prompt.md front matter is not YAML: {exc}") from exc
    tags = data.get("tags") if isinstance(data, dict) else None
    return [tag for tag in tags if isinstance(tag, str)] if isinstance(tags, list) else []


def selection_has_holdout(tags: list[str] | None, case_glob: str | None) -> bool:
    """Whether the cases a ``--tag`` or ``--case`` selection (or neither, the whole suite)
    reaches include a holdout-tagged one, read from the case directories under the eval
    roots. The holdout cases' own run count is two and the holdout is never edited, so the
    gate forces ``HOLDOUT_RUNS`` on any such selection (the 2026-10-18 11:45 EDT decision);
    a selection that reaches no holdout case keeps each case's own count. Repeated
    ``--tag`` values are read as any-of here; the CLI's help calls the flag repeatable and
    does not say how repeats combine, and an all-of reading on its side only forces runs
    the selection would not need, which costs money and stays correct."""
    wanted = set(tags or [])
    for root in run_evals.CASE_ROOTS:
        if not root.is_dir():
            continue
        for case_dir in sorted(p for p in root.iterdir() if p.is_dir()):
            if case_glob and not fnmatch.fnmatch(case_dir.name, case_glob):
                continue
            case = case_tags(case_dir)
            if wanted and not wanted & set(case):
                continue
            if "holdout" in case:
                return True
    return False


def case_bar(case_dir: Path) -> Fraction:
    """The pass rate a case must reach, from the one set tag its ``prompt.md`` carries."""
    sets = {tag for tag in case_tags(case_dir) if tag in SET_TAGS}
    if len(sets) != 1:
        raise GateError(
            f"{case_dir.name}: prompt.md tags name {sorted(sets) or 'no'} set; exactly one of "
            f"{sorted(SET_TAGS)} is required"
        )
    return HOLDOUT_BAR if sets == {"holdout"} else REGRESSION_BAR


def _case_dir_for(case_name: str) -> Path:
    try:
        return run_evals._case_dir(case_name, run_evals.CASE_ROOTS)
    except run_evals.ResultError as exc:
        raise GateError(str(exc)) from exc


def _bar_for(case_name: str) -> Fraction:
    return case_bar(_case_dir_for(case_name))


# ---- traces ---------------------------------------------------------------------


def _release(path: Path) -> None:
    """The CLI leaves kept run directories read-only; open them and remove them."""
    try:
        path.chmod(path.stat().st_mode | stat.S_IRWXU)
        for p in path.rglob("*"):
            p.chmod(p.lstat().st_mode | stat.S_IRWXU)
    except OSError as exc:
        print(f"gate: could not reopen kept run directory {path}: {exc}", file=sys.stderr)
    shutil.rmtree(path, ignore_errors=True)


def keep_traces(result_path: Path) -> None:
    """Copy each run's trace beside the result as ``<case>-run<i>.trace.jsonl`` and point the
    result's ``tracePath`` at the copy, so ``run_evals`` finds the final text after the kept
    temp directory (``e-*``, which the CLI leaves under --keep-temp) is released."""
    try:
        data = json.loads(result_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise GateError(f"the result {result_path} cannot be read: {exc}") from exc
    for case in data.get("cases", []):
        for index, run in enumerate((case.get("arms") or {}).get("with", [])):
            if not run.get("tracePath"):
                continue
            trace = Path(run["tracePath"])
            if not trace.is_absolute() or not trace.is_file():
                continue
            dest = result_path.parent / f"{case['name']}-run{index}.trace.jsonl"
            shutil.copy2(trace, dest)
            run["tracePath"] = dest.name
            kept = trace.parent.parent
            if kept.name.startswith("e-") and kept.is_dir():
                _release(kept)
    result_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


# ---- the judge ---------------------------------------------------------------------


def judge_runs(result: run_evals.Result, model: str) -> Path:
    """Score each drafting run's final text with the prose judge and write the sidecar.

    A review case grades recall, not prose, and is skipped; a run with no final text has
    nothing to score. A judge call that fails or answers without a score is apparatus."""
    entries = []
    for case in result.cases:
        expected = prose_judge.case_expected(_case_dir_for(case.name))
        if expected.get("mode", "write") == "review":
            continue
        for run in case.runs:
            if run.text is None:
                continue
            try:
                judgement = prose_judge.judge_document(
                    run.text, expected["template"], expected["audience"], model=model
                )
            except prose_judge.JudgeError as exc:
                raise GateError(f"{case.name} run {run.index}: {exc}") from exc
            entries.append(
                {
                    "case": case.name,
                    "run": run.index,
                    "score": judgement.score,
                    "answer": judgement.answer,
                    "cost_usd": str(judgement.cost_usd),
                }
            )
    return prose_judge.write_sidecar(result.path.parent, model, entries)


# ---- the run ---------------------------------------------------------------------


def _stamp(label: str | None) -> str:
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    return f"{stamp}-{UNSAFE_LABEL.sub('_', label)}" if label else stamp


def _cli_passed(run: dict) -> bool:
    """Whether the CLI's graders pass the run once the prose-judge grader's vote is set
    aside: the CLI's own verdict when it passed, else every other grader passing on a run
    that reached the agent."""
    if run.get("passed"):
        return True
    graders = run.get("graders", [])
    counted = [g for g in graders if g.get("name") != prose_judge.GRADER_NAME]
    return not run.get("error") and bool(counted) and all(g.get("passed") for g in counted)


def _case_verdicts(result_path: Path, rows: list[run_evals.Row]) -> list[tuple[str, bool]]:
    """One line per case and whether it cleared its bar. A run passes when the CLI's graders
    and the structural checker both pass it; the case passes when the share of passing runs
    reaches the bar its set tag names. A review case (its rows carry recall) is judged on its
    pooled recall over every run by the acceptance rule in ``run_evals`` as well: every
    structural defect found and at least nine prose defects in ten.

    The CLI's own prose-judge grader (``prose_judge.GRADER_NAME``) is the one grader whose
    vote is recorded and not counted: the gate judges the same text itself with the judge
    calibrated to the hand scores and keeps its answer, so its score rules the run through
    the median rule, and a FAIL vote the gate's judge contradicts is noted in the case line.
    """
    data = json.loads(result_path.read_text(encoding="utf-8"))
    verdicts = []
    for case in data.get("cases", []):
        runs = (case.get("arms") or {}).get("with", [])
        failed = sorted(
            {
                g["name"]
                for run in runs
                for g in run.get("graders", [])
                if not g.get("passed") and g.get("name") != prose_judge.GRADER_NAME
            }
        )
        judge_votes = [
            f"run {index} ({g.get('explanation') or 'no explanation'})"
            for index, run in enumerate(runs)
            for g in run.get("graders", [])
            if not g.get("passed") and g.get("name") == prose_judge.GRADER_NAME
        ]
        errors = [run["error"] for run in runs if run.get("error")]
        case_rows = [row for row in rows if row.case == case["name"]]
        checker_failed = [row for row in case_rows if not row.passed]
        checker_failed_runs = {row.run for row in checker_failed}
        passing = sum(
            1
            for index, run in enumerate(runs)
            if _cli_passed(run) and index not in checker_failed_runs
        )
        bar = _bar_for(case["name"])
        passed = bool(runs) and Fraction(passing, len(runs)) >= bar
        notes = [f"{passing} of {len(runs)} runs passed, bar {bar}"]
        if any(row.grade is not None and row.grade.mode == "review" for row in case_rows):
            pooled = run_evals.pooled_recall(_case_dir_for(case["name"]), case_rows)
            passed = passed and run_evals.review_accepts(pooled)
            notes.append(
                f"review recall structural {pooled.structural_found} of "
                f"{pooled.structural_total}, prose {pooled.prose_found} of {pooled.prose_total}, "
                f"rule {run_evals.REVIEW_STRUCTURAL_BAR} and {run_evals.REVIEW_PROSE_BAR}"
            )
        verdict = "PASS" if passed else "FAIL"
        if failed:
            notes.append(f"graders below threshold: {', '.join(failed)}")
        if judge_votes:
            notes.append(
                f"prose-judge vote FAIL on {', '.join(judge_votes)}, recorded; the gate's own "
                "score rules"
            )
        if errors:
            notes.append(f"run errors: {errors[0][:120]}")
        for row in checker_failed:
            counts = ", ".join(
                f"{row.counts[s]} {s}" for s in run_evals.SEVERITIES if row.counts[s]
            )
            note = row.error or counts or "expected markers or defects missing"
            notes.append(f"checker failed run {row.run}: {note}")
        verdicts.append((f"{case['name']}: {verdict} ({'; '.join(notes)})", passed))
    return verdicts


def run(opts: argparse.Namespace) -> int:
    stamp = _stamp(opts.label)
    argv = build_argv(opts, stamp)
    if opts.dry_run:
        print(shlex.join(argv))
        return PASS
    output_dir = Path(opts.results_dir) / stamp
    output_dir.mkdir(parents=True, exist_ok=True)
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, cwd=str(ROOT))
    except FileNotFoundError as exc:
        raise GateError(
            f"claude is not on PATH ({exc}); install Claude Code and run again"
        ) from exc
    output = (proc.stdout or "") + (proc.stderr or "")
    verdict, why = classify(proc.returncode, output, output_dir / "aggregate-result.json")
    if verdict == APPARATUS:
        raise GateError(why)
    check_exercised(output_dir / "aggregate-result.json")
    result_path = output_dir / "run.json"
    if not result_path.is_file():
        raise GateError(f"the CLI wrote an aggregate but no --json result at {result_path}")
    keep_traces(result_path)
    try:
        result = run_evals.load_result(result_path)
        judge_runs(result, opts.judge_model)
        result = run_evals.load_result(result_path)  # now with each run's judge score
        rows = run_evals.grade_result(result)
        report = run_evals.write_report(result, rows, opts.reports_dir, label=opts.label)
    except run_evals.ResultError as exc:
        raise GateError(str(exc)) from exc
    verdicts = _case_verdicts(result_path, rows)
    for line, _ in verdicts:
        print(line)
    summary = run_evals.judge_summary(rows)
    for line in run_evals.judge_lines(summary):
        print(line)
    print(f"report {Path(opts.reports_dir) / report}.md")
    below = [line.split(":", 1)[0] for line, passed in verdicts if not passed]
    under_rule = [model for model, entry in summary.items() if entry["verdict"] == "FAIL"]
    reasons = []
    if below:
        reasons.append(f"below its bar: {', '.join(below)}")
    if under_rule:
        reasons.append(f"below the judge rule: {', '.join(under_rule)}")
    if reasons:
        verdict = FAIL
        why = "; ".join(reasons)
    else:
        why = "every case at or above its bar" + (
            " and every gated model at the judge rule" if summary else ""
        )
    print(f"gate: {'PASS' if verdict == PASS else 'FAIL'}: {why}")
    return verdict


def main(argv: list[str] | None = None) -> int:
    opts = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        return run(opts)
    except GateError as exc:
        print(json.dumps({"error": str(exc)}, indent=2))
        return APPARATUS


if __name__ == "__main__":
    sys.exit(main())
