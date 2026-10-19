#!/usr/bin/env python3
# Description: Grades every run in a claude plugin eval result deterministically: the final
# Description: text against its case's template through check_structure, the markers, the report.
"""Deterministic grading over `claude plugin eval` results.

The result JSON the CLI writes (``--json``) carries the cost, the Claude version, and the
grader verdicts per run, but neither the final assistant text nor the model; both are read
from the run's ``trace.jsonl`` at the ``tracePath`` the result names, a relative path
resolving against the result file's directory. In write mode (the default) each run's text is
checked against the template and audience its case's ``expected.json`` names, every
``unverified`` entry, a case-insensitive pattern, must match inside an ``[UNVERIFIED: ...]``
marker, and every ``defects``
entry must match a finding. In review mode (``"mode": "review"``) the text is a findings
list over a seeded document, never a document: each ``defects`` entry is a pattern the reply
must contain, and the grade is recall, split into structural and prose defects. The report
pair, ``<stamp>.md`` and ``<stamp>.json``, lands under ``--out``.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(HERE))

import prose_judge  # noqa: E402  (a sibling module, loaded after the path insert)
from check_structure import (  # noqa: E402  (scripts/ is on no import path before the insert)
    SEVERITIES,
    UNVERIFIED,
    check_document,
    passes,
    templates_by_type,
)

CASE_ROOTS = (ROOT / "evals" / "holdout", ROOT / "evals" / "cases")
PLUGIN_JSON = ROOT / ".claude-plugin" / "plugin.json"
DEFAULT_OUT = ROOT / "evals" / "reports"

# exit codes: 0 pass, 1 fail, 2 apparatus
PASS, FAIL, APPARATUS = 0, 1, 2

# a label becomes part of a file name, so anything outside this set is replaced
UNSAFE_LABEL = re.compile(r"[^A-Za-z0-9._-]+")

MODES = frozenset({"write", "review"})
# review mode: the defect codes that count as structural; every other code is prose
STRUCTURAL_CODES = frozenset({"EVIDENCE_MISSING", "H1_COUNT"})
STRUCTURAL_PREFIX = "SECTION_"
# review mode's acceptance rule, applied per case over its pooled runs
REVIEW_STRUCTURAL_BAR = Decimal("1")
REVIEW_PROSE_BAR = Decimal("0.9")
# the prose judge's acceptance rule (spec, Acceptance): over a model's judged runs the median
# score is at least 4 and no run scores below 3; applied to the gated models, recorded for the rest
JUDGE_MEDIAN_BAR = Decimal("4")
JUDGE_RUN_FLOOR = 3
GATED_MODELS = frozenset({"claude-sonnet-5-5", "claude-opus-5"})


class ResultError(ValueError):
    """A result, trace, case directory, or template the grader cannot read. Exit 2."""


@dataclass(frozen=True)
class Run:
    index: int
    model: str | None
    cost_usd: Decimal | None
    claude_version: str | None
    text: str | None
    error: str | None
    judge_score: int | None = None  # from the judge sidecar; None with an answer is Unknown
    judge_answer: str | None = None


@dataclass(frozen=True)
class Case:
    name: str
    dir: str
    runs: tuple[Run, ...]


@dataclass(frozen=True)
class Result:
    path: Path
    claude_version: str | None
    started_at: str
    cost_usd: Decimal | None
    partial: bool
    partial_reason: str | None
    cases: tuple[Case, ...]


@dataclass(frozen=True)
class Recall:
    """Review-mode recall: defects found of defects listed, by class."""

    structural_found: int
    structural_total: int
    prose_found: int
    prose_total: int

    @property
    def structural(self) -> Decimal | None:
        return _fraction(self.structural_found, self.structural_total)

    @property
    def prose(self) -> Decimal | None:
        return _fraction(self.prose_found, self.prose_total)


def _fraction(found: int, total: int) -> Decimal | None:
    return None if total == 0 else Decimal(found) / Decimal(total)


def is_structural(code: str) -> bool:
    """Whether a defect code counts as structural in review recall: the SECTION_* codes,
    EVIDENCE_MISSING and H1_COUNT. BANNED_PATTERN and the heading-form codes are prose."""
    return code.startswith(STRUCTURAL_PREFIX) or code in STRUCTURAL_CODES


def review_accepts(recall: Recall) -> bool:
    """The acceptance rule: every structural defect found, at least nine prose in ten."""
    structural = recall.structural
    prose = recall.prose
    return (structural is None or structural >= REVIEW_STRUCTURAL_BAR) and (
        prose is None or prose >= REVIEW_PROSE_BAR
    )


@dataclass(frozen=True)
class Grade:
    template: str
    audience: str
    passed: bool
    findings: list[dict[str, Any]]
    counts: dict[str, int]
    unverified_found: list[str]
    unverified_missing: list[str]
    defects_found: list[str]
    defects_missing: list[str]
    mode: str = "write"
    recall: Recall | None = None


@dataclass(frozen=True)
class Row:
    case: str
    model: str | None
    run: int
    passed: bool
    counts: dict[str, int]
    cost_usd: Decimal | None
    grade: Grade | None
    error: str | None
    judge: int | None = None  # the prose judge's score; None when unjudged or Unknown
    judged: bool = False  # whether the judge saw the run; a review run never is


def judge_median(scores: list[int]) -> Decimal:
    """The median of the scores: the middle one, or the mean of the two middle ones."""
    ordered = sorted(scores)
    half = len(ordered) // 2
    if len(ordered) % 2:
        return Decimal(ordered[half])
    return (Decimal(ordered[half - 1]) + Decimal(ordered[half])) / 2


def judge_accepts(scores: list[int]) -> bool:
    """The acceptance rule: a median of at least 4 and no run below 3. No scores never accepts."""
    return (
        bool(scores) and judge_median(scores) >= JUDGE_MEDIAN_BAR and min(scores) >= JUDGE_RUN_FLOOR
    )


def judge_summary(rows: list[Row]) -> dict[str, dict[str, Any]]:
    """Per model, over the rows the judge saw: the scored count, the rows the judge answered
    Unknown, the median, the minimum, whether the spec gates the model, and the verdict (PASS
    or FAIL for a gated model, recorded otherwise). A model the judge never saw is absent; a
    gated model whose every judged run is Unknown has no score to meet the rule with and
    fails; an unjudged row (a review run, a run with no text) counts nowhere."""
    by_model: dict[str, list[Row]] = {}
    for row in rows:
        by_model.setdefault(str(row.model), []).append(row)
    summary: dict[str, dict[str, Any]] = {}
    for model, model_rows in by_model.items():
        judged = [row for row in model_rows if row.judged]
        if not judged:
            continue
        scores = [row.judge for row in judged if row.judge is not None]
        gated = model in GATED_MODELS
        summary[model] = {
            "runs": len(scores),
            "unknown": len(judged) - len(scores),
            "median": format(judge_median(scores).normalize(), "f") if scores else None,
            "min": min(scores) if scores else None,
            "gated": gated,
            "verdict": ("PASS" if judge_accepts(scores) else "FAIL") if gated else "recorded",
        }
    return summary


def judge_lines(summary: dict[str, dict[str, Any]]) -> list[str]:
    lines = []
    for model, entry in summary.items():
        runs = f"{entry['runs']} run" + ("" if entry["runs"] == 1 else "s")
        unknown = f", {entry['unknown']} unknown" if entry["unknown"] else ""
        figures = f"median {entry['median']}, min {entry['min']}" if entry["runs"] else "no score"
        lines.append(f"judge {model}: {figures} over {runs}{unknown}, {entry['verdict']}")
    return lines


# ---- loading ------------------------------------------------------------------


def _money(value: Any) -> Decimal | None:
    """The CLI reports costs as floats; ``Decimal(str(...))`` keeps the digits it printed."""
    return None if value is None else Decimal(str(value))


def _read_json(path: Path, what: str) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ResultError(f"cannot read {what} {path}: {exc.strerror or exc}") from exc
    except ValueError as exc:
        raise ResultError(f"{what} {path} is not JSON: {exc}") from exc


def _read_trace(path: Path) -> tuple[str | None, str | None]:
    """The run's model from the ``system`` ``init`` line and its final text from the closing
    ``result`` line, which carries ``result`` only when the run ended as ``success``."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise ResultError(f"cannot read trace {path}: {exc.strerror or exc}") from exc
    model = text = None
    for number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except ValueError as exc:
            raise ResultError(f"trace {path} line {number} is not JSON: {exc}") from exc
        if event.get("type") == "system" and event.get("subtype") == "init":
            model = event.get("model")
        elif event.get("type") == "result" and event.get("subtype") == "success":
            text = event.get("result")
    return model, text


def load_result(path: str | Path) -> Result:
    """Read a ``claude plugin eval --json`` result and each run's trace."""
    path = Path(path)
    data = _read_json(path, "result")
    if not isinstance(data, dict) or not isinstance(data.get("cases"), list):
        raise ResultError(f"result {path} carries no cases list")
    try:
        judged = prose_judge.read_sidecar(path.parent)
    except prose_judge.JudgeError as exc:
        raise ResultError(str(exc)) from exc
    cases: list[Case] = []
    for case in data["cases"]:
        runs: list[Run] = []
        for index, run in enumerate((case.get("arms") or {}).get("with", [])):
            model = text = None
            if run.get("tracePath"):
                model, text = _read_trace(path.parent / run["tracePath"])
            judgement = judged.get((case["name"], index), {})
            runs.append(
                Run(
                    index=index,
                    model=model,
                    cost_usd=_money(run.get("costUsd")),
                    claude_version=data.get("claudeVersion"),
                    text=text,
                    error=run.get("error"),
                    judge_score=judgement.get("score"),
                    judge_answer=judgement.get("answer"),
                )
            )
        cases.append(Case(name=case["name"], dir=case.get("dir", ""), runs=tuple(runs)))
    return Result(
        path=path,
        claude_version=data.get("claudeVersion"),
        started_at=data.get("startedAt", ""),
        cost_usd=_money(data.get("costUsd")),
        partial=bool(data.get("partial")),
        partial_reason=data.get("partialReason"),
        cases=tuple(cases),
    )


# ---- grading ------------------------------------------------------------------


def grade_run(case_dir: str | Path, text: str) -> Grade:
    """Grade one run's final text against its case.

    ``expected.json`` names the template and audience; each ``unverified`` entry is a
    case-insensitive pattern, found when it matches inside an ``[UNVERIFIED: ...]`` marker in
    the text, so an entry may list the words a marker could name the missing fact by
    (``retention|keep|kept|expire``); an entry that does not compile is a ``ResultError``. In
    write mode ``defects`` entries are found when a finding with that code has a message the pattern
    matches, and the run passes when the checker passes and nothing expected is missing. In
    review mode the text is findings, not a document: the checker never runs over it, each
    ``defects`` pattern is searched in the text (case-insensitively), and the run passes when
    its recall meets the acceptance rule.
    """
    case_dir = Path(case_dir)
    expected = _read_json(case_dir / "expected.json", "expected")
    specs = templates_by_type()
    template = expected.get("template")
    if template not in specs:
        raise ResultError(f"{case_dir.name}: expected.json template {template!r} names no template")
    mode = expected.get("mode", "write")
    if mode not in MODES:
        raise ResultError(
            f"{case_dir.name}: expected.json mode {mode!r} is not one of {sorted(MODES)}"
        )
    markers = UNVERIFIED.findall(text)
    found = []
    missing = []
    for entry in expected.get("unverified", []):
        try:
            pattern = re.compile(entry, re.IGNORECASE)
        except re.error as exc:
            raise ResultError(
                f"{case_dir.name}: expected.json unverified entry {entry!r} is not a pattern: {exc}"
            ) from exc
        (found if any(pattern.search(marker) for marker in markers) else missing).append(entry)
    defects = expected.get("defects", [])
    counts = {severity: 0 for severity in SEVERITIES}
    if mode == "review":
        defects_found, defects_missing = _review_defects(defects, text)
        recall = _recall(defects, defects_found)
        return Grade(
            template=template,
            audience=expected.get("audience"),
            passed=review_accepts(recall) and not missing,
            findings=[],
            counts=counts,
            unverified_found=found,
            unverified_missing=missing,
            defects_found=defects_found,
            defects_missing=defects_missing,
            mode=mode,
            recall=recall,
        )
    findings = check_document(text, specs[template], expected.get("audience"))
    for finding in findings:
        counts[finding.severity] += 1
    defects_found = []
    defects_missing = []
    for defect in defects:
        matched = any(
            finding.code == defect["code"] and re.search(defect["pattern"], finding.message)
            for finding in findings
        )
        (defects_found if matched else defects_missing).append(defect["code"])
    return Grade(
        template=template,
        audience=expected.get("audience"),
        passed=passes(findings) and not missing and not defects_missing,
        findings=[finding.to_dict() for finding in findings],
        counts=counts,
        unverified_found=found,
        unverified_missing=missing,
        defects_found=defects_found,
        defects_missing=defects_missing,
    )


def _review_defects(defects: list[dict[str, str]], text: str) -> tuple[list[str], list[str]]:
    """Each defect's pattern searched in the reply; the codes found and the codes missing."""
    found: list[str] = []
    missing: list[str] = []
    for defect in defects:
        matched = re.search(defect["pattern"], text, re.IGNORECASE) is not None
        (found if matched else missing).append(defect["code"])
    return found, missing


def _recall(defects: list[dict[str, str]], defects_found: list[str]) -> Recall:
    """Recall by class from the listed defects and the codes found, in list order."""
    structural = [is_structural(defect["code"]) for defect in defects]
    found_flags = _found_flags(defects, defects_found)
    return Recall(
        structural_found=sum(1 for s, f in zip(structural, found_flags, strict=True) if s and f),
        structural_total=sum(structural),
        prose_found=sum(1 for s, f in zip(structural, found_flags, strict=True) if not s and f),
        prose_total=sum(1 for s in structural if not s),
    )


def _found_flags(defects: list[dict[str, str]], defects_found: list[str]) -> list[bool]:
    """Which listed defects were found, matching codes in order since a code may repeat."""
    remaining = list(defects_found)
    flags = []
    for defect in defects:
        if defect["code"] in remaining:
            remaining.remove(defect["code"])
            flags.append(True)
        else:
            flags.append(False)
    return flags


def pooled_recall(case_dir: str | Path, rows: list[Row]) -> Recall:
    """A review case's recall over all its runs: the found and listed counts summed. A run
    with no grade (it errored, or left no text) found nothing and lists every defect."""
    expected = _read_json(Path(case_dir) / "expected.json", "expected")
    listed = _recall(expected.get("defects", []), [])
    totals = [0, 0, 0, 0]
    for row in rows:
        recall = row.grade.recall if row.grade is not None else None
        if recall is None:
            recall = listed
        totals[0] += recall.structural_found
        totals[1] += recall.structural_total
        totals[2] += recall.prose_found
        totals[3] += recall.prose_total
    return Recall(*totals)


def _case_dir(name: str, roots: tuple[Path, ...] | list[Path]) -> Path:
    for root in roots:
        candidate = Path(root) / name
        if (candidate / "expected.json").is_file():
            return candidate
    searched = ", ".join(str(root) for root in roots)
    raise ResultError(f"no case directory named {name!r} with an expected.json under {searched}")


def grade_result(result: Result, roots: tuple[Path, ...] | list[Path] = CASE_ROOTS) -> list[Row]:
    """One row per run. A run with no final text (it errored, or its trace is not named)
    fails with the run's error as its note and is never passed to the checker."""
    rows: list[Row] = []
    for case in result.cases:
        case_dir = _case_dir(case.name, roots)
        for run in case.runs:
            if run.text is None:
                rows.append(
                    Row(
                        case=case.name,
                        model=run.model,
                        run=run.index,
                        passed=False,
                        counts={severity: 0 for severity in SEVERITIES},
                        cost_usd=run.cost_usd,
                        grade=None,
                        error=run.error or "the run left no final text in its trace",
                        judge=run.judge_score,
                        judged=run.judge_answer is not None,
                    )
                )
                continue
            grade = grade_run(case_dir, run.text)
            rows.append(
                Row(
                    case=case.name,
                    model=run.model,
                    run=run.index,
                    passed=grade.passed,
                    counts=grade.counts,
                    cost_usd=run.cost_usd,
                    grade=grade,
                    error=run.error,
                    judge=run.judge_score,
                    judged=run.judge_answer is not None,
                )
            )
    return rows


# ---- the report -----------------------------------------------------------------


def _stamp(started_at: str) -> str:
    try:
        return datetime.fromisoformat(started_at).strftime("%Y%m%dT%H%M%SZ")
    except ValueError as exc:
        raise ResultError(f"result startedAt {started_at!r} is not an ISO timestamp") from exc


def _git_head() -> str:
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=ROOT, check=False
        )
    except OSError as exc:
        raise ResultError(f"git is not available to stamp the report: {exc}") from exc
    if proc.returncode != 0:
        raise ResultError(f"git rev-parse HEAD failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


def _git_dirty(repo: Path = ROOT) -> bool:
    """Whether the working tree carries uncommitted changes, from ``git status --porcelain``.

    A report stamped with HEAD alone cannot say whether the skill it graded was the committed
    one; a run inside a step grades the tree, and this flag says so."""
    try:
        proc = subprocess.run(
            ["git", "status", "--porcelain"], capture_output=True, text=True, cwd=repo, check=False
        )
    except OSError as exc:
        raise ResultError(f"git is not available to stamp the report: {exc}") from exc
    if proc.returncode != 0:
        raise ResultError(f"git status --porcelain failed: {proc.stderr.strip()}")
    return bool(proc.stdout.strip())


def _plugin_version() -> str:
    data = _read_json(PLUGIN_JSON, "plugin manifest")
    version = data.get("version") if isinstance(data, dict) else None
    if not isinstance(version, str):
        raise ResultError(f"plugin manifest {PLUGIN_JSON} carries no version")
    return version


def _result_label(path: Path) -> str:
    resolved = path.resolve()
    return resolved.relative_to(ROOT).as_posix() if resolved.is_relative_to(ROOT) else str(path)


def _row_dict(row: Row) -> dict[str, Any]:
    data = asdict(row)
    data["pass"] = data.pop("passed")
    data["cost_usd"] = None if row.cost_usd is None else str(row.cost_usd)
    return data


def _note(row: Row) -> str:
    if row.error:
        return row.error
    if row.grade is None:
        return ""
    parts = []
    if row.grade.recall is not None:
        recall = row.grade.recall
        parts.append(
            f"review: structural {recall.structural_found} of {recall.structural_total}, "
            f"prose {recall.prose_found} of {recall.prose_total}"
        )
    if row.grade.unverified_missing:
        parts.append(f"markers missing: {', '.join(row.grade.unverified_missing)}")
    if row.grade.defects_missing:
        parts.append(f"defects missing: {', '.join(row.grade.defects_missing)}")
    return "; ".join(parts)


def write_report(
    result: Result, rows: list[Row], out_dir: str | Path, label: str | None = None
) -> str:
    """Write ``<stamp>.md`` and ``<stamp>.json`` under ``out_dir`` and return the stamp."""
    out_dir = Path(out_dir)
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise ResultError(
            f"cannot create report directory {out_dir}: {exc.strerror or exc}"
        ) from exc
    stamp = _stamp(result.started_at) + (f"-{UNSAFE_LABEL.sub('_', label)}" if label else "")
    header = {
        "claude_version": result.claude_version,
        "plugin_version": _plugin_version(),
        "git_head": _git_head(),
        "git_dirty": _git_dirty(),
        "label": label,
        "result": _result_label(result.path),
        "started_at": result.started_at,
        "cost_usd": None if result.cost_usd is None else str(result.cost_usd),
        "partial": result.partial,
    }
    summary = judge_summary(rows)
    report_json = json.dumps(
        {"header": header, "judge": summary, "rows": [_row_dict(row) for row in rows]}, indent=2
    )
    _write(out_dir / f"{stamp}.json", report_json + "\n")
    lines = [
        f"# Eval report {stamp}",
        "",
        f"claude {header['claude_version']}, plugin {header['plugin_version']}, "
        f"git HEAD {header['git_head']}, dirty {str(header['git_dirty']).lower()}",
        f"result {header['result']}, started {header['started_at']}, "
        f"cost USD {header['cost_usd']}, partial {str(result.partial).lower()}",
        "",
        "| case | model | run | pass | high | medium | low | info | cost USD | judge | note |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        counts = " | ".join(str(row.counts[severity]) for severity in SEVERITIES)
        judge = "" if row.judge is None else str(row.judge)
        lines.append(
            f"| {row.case} | {row.model} | {row.run} | {'PASS' if row.passed else 'FAIL'} | "
            f"{counts} | {row.cost_usd} | {judge} | {_note(row)} |"
        )
    if summary:
        lines += ["", *judge_lines(summary)]
    failing = [row for row in rows if row.grade is not None and row.grade.findings]
    for row in failing:
        lines += ["", f"## {row.case} run {row.run}", ""]
        for finding in row.grade.findings:
            where = f" line {finding['line']}" if finding["line"] is not None else ""
            lines.append(f"- {finding['severity']} {finding['code']}{where}: {finding['message']}")
    _write(out_dir / f"{stamp}.md", "\n".join(lines) + "\n")
    return stamp


def _write(path: Path, text: str) -> None:
    try:
        path.write_text(text, encoding="utf-8")
    except OSError as exc:
        raise ResultError(f"cannot write report {path}: {exc.strerror or exc}") from exc


# ---- the command line ------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    """Grade one result file and write its report. Exit 0 when every run passes and every
    gated model meets the judge's acceptance rule, 1 when a run fails or a gated model does
    not, 2 when the result, a trace, a case, or a template cannot be read."""
    parser = argparse.ArgumentParser(
        prog="run_evals.py", description="Grade a claude plugin eval result deterministically."
    )
    parser.add_argument("--result", required=True, help="the result JSON the CLI wrote")
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="directory for the report pair")
    parser.add_argument("--label", help="text appended to the report stamp")
    args = parser.parse_args(argv)
    try:
        result = load_result(args.result)
        rows = grade_result(result)
        stamp = write_report(result, rows, args.out, label=args.label)
    except ResultError as exc:
        print(json.dumps({"error": str(exc)}, indent=2))
        return APPARATUS
    for row in rows:
        verdict = "PASS" if row.passed else "FAIL"
        note = f" ({_note(row)})" if _note(row) else ""
        print(f"{row.case} run {row.run}: {verdict}{note}")
    summary = judge_summary(rows)
    for line in judge_lines(summary):
        print(line)
    print(f"report {Path(args.out) / stamp}.md")
    judged = all(entry["verdict"] != "FAIL" for entry in summary.values())
    return PASS if all(row.passed for row in rows) and judged else FAIL


if __name__ == "__main__":
    sys.exit(main())
