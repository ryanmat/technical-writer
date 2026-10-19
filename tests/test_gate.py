# Description: Tests evals/gate.py, the eval gate around `claude plugin eval`: the fixed argv, the
# Description: the exit codes, trace capture beside the result, and the deterministic layer.
"""Tests over the gate. subprocess.run is replaced by a fake whose exit codes and aggregate layout
come from the capture under tests/fixtures/plugin-eval and the gate's classification:
a CLI missing from PATH, a grader below threshold (exit 1), no aggregate written, a partial
run, and a green CLI whose output the structural checker fails."""

import json
import shlex
import subprocess
from fractions import Fraction
from pathlib import Path

import pytest
from conftest import ROOT
from plugin_eval import PLUGIN_EVAL_DIR, load_evals_module

gate = load_evals_module("gate")

FIXTURE_RESULT = PLUGIN_EVAL_DIR / "result.json"
FIXTURE_TRACE = PLUGIN_EVAL_DIR / "trace.jsonl"
CASE = "task--relay-alert-rule"
REGRESSION_CASE = "concept--relay-routing-model"
REVIEW_CASE = "review--task-missing-prereqs"
ARGS = ["--tag", "holdout", "--max-cost-usd", "10"]
REAL_RUN = subprocess.run
JUDGE_RESULT = {  # the keys of a `claude -p --output-format json` result the judge reads
    "type": "result",
    "subtype": "success",
    "is_error": False,
    "result": "ok",
    "total_cost_usd": 0.000126,
    "num_turns": 1,
}


def _flag(argv: list[str], flag: str) -> str:
    return argv[argv.index(flag) + 1]


def fake_cli(scenario: str, calls: list[list[str]]):
    """A stand-in for subprocess.run that behaves as `claude plugin eval` did in the capture:
    it writes run.json (and the kept trace) where --json and --output-dir point, and exits
    with the CLI's code for the scenario."""

    def run(argv, **kwargs):
        if argv[0] != "claude":  # the grader's git rev-parse is real
            return REAL_RUN(argv, **kwargs)
        calls.append(list(argv))
        if scenario == "cli-missing":
            raise FileNotFoundError(2, "No such file or directory", "claude")
        if argv[1] == "-p":
            # the gate's judge call after the run: a context-free `claude -p` answering with
            # the Score: line first, in the JSON shape the 2026-10-17 smoke call printed
            score = 2 if scenario == "judge-low" else 4
            body = dict(
                JUDGE_RESULT, result=f"Score: {score}\n\nLeads with the point: the first line."
            )
            if scenario == "judge-broken":
                body["result"] = "I would call this a four."
            return subprocess.CompletedProcess(argv, 0, json.dumps(body), "")
        output_dir = Path(_flag(argv, "--output-dir"))
        output_dir.mkdir(parents=True, exist_ok=True)
        if scenario == "no-aggregate":
            return subprocess.CompletedProcess(argv, 0, "", "")
        if scenario == "empty-selection":
            empty = json.loads(FIXTURE_RESULT.read_text(encoding="utf-8"))
            empty["cases"] = []
            empty["aggregates"] = {
                "casesTotal": 0,
                "casesPassed": 0,
                "overallScore": 0,
                "overallPassRate": 0,
            }
            for path in (Path(_flag(argv, "--json")), output_dir / "aggregate-result.json"):
                path.write_text(json.dumps(empty, indent=2), encoding="utf-8")
            return subprocess.CompletedProcess(argv, 0, "", "")
        if scenario == "sandbox-refused":
            return subprocess.CompletedProcess(
                argv, 1, "", "no sandbox backend: install bubblewrap and socat"
            )
        data = json.loads(FIXTURE_RESULT.read_text(encoding="utf-8"))
        trace_lines = FIXTURE_TRACE.read_text(encoding="utf-8").splitlines()
        lines = [json.loads(line) for line in trace_lines]
        texts_by_run: dict[int, str] = {}
        code = 0
        if scenario == "grader-failed":
            run0 = data["cases"][0]["arms"]["with"][0]
            run0["graders"][0].update(passed=False, explanation="no match for ^## Steps")
            run0.update(score=0.67, passed=False)
            data["cases"][0]["aggregates"] = {"score": 0.67, "passRate": 0}
            data["aggregates"].update(casesPassed=0, overallScore=0.67, overallPassRate=0)
            code = 1
        elif scenario == "judge-grader-failed":
            # the CLI's prose-judge grader votes FAIL on a run the checker passes while the
            # gate's own judge call (the default answer below) scores it 4: the vote is
            # recorded in the case line and the gate's score rules (by ruling)
            run0 = data["cases"][0]["arms"]["with"][0]
            # the record's keys and shape are a live prose-judge grader record's
            # (evals/results/20261018T153327Z/run.json): no type and no score key
            run0["graders"].append(
                {
                    "name": "prose-judge",
                    "passed": False,
                    "weight": 1,
                    "explanation": "judge votes: FAIL FAIL FAIL",
                    "withOnly": False,
                    "scored": True,
                    "judgeVotes": [False, False, False],
                    "evidence": lines[-1]["result"],
                }
            )
            run0.update(score=0.75, passed=False)
            data["cases"][0]["aggregates"] = {"score": 0.75, "passRate": 0}
            data["aggregates"].update(casesPassed=0, overallScore=0.75, overallPassRate=0)
            code = 1
        elif scenario == "partial":
            data["partial"] = True
            data["partialReason"] = "cost_ceiling"
        elif scenario == "partial-flag-only":
            data["partial"] = True
        elif scenario == "never-exercised":
            run0 = data["cases"][0]["arms"]["with"][0]
            run0.update(
                error="sandbox backend unavailable: install bubblewrap and socat",
                graders=[],
                turns=0,
                passed=False,
                score=0,
            )
            code = 1
        elif scenario == "high-finding":
            text = lines[-1]["result"].replace("## Before you begin", "## Prerequisites")
            lines[-1]["result"] = text
            lines[5]["message"]["content"][0]["text"] = text
        elif scenario == "review-graders-failed":
            # a review case whose two runs name every defect while the CLI's graders fail
            # both: full recall does not lift a case over its set bar
            data["cases"][0]["name"] = REVIEW_CASE
            text = (ROOT / "evals" / "cases" / REVIEW_CASE / "reference.md").read_text(
                encoding="utf-8"
            )
            lines[-1]["result"] = text
            lines[5]["message"]["content"][0]["text"] = text
            run0 = data["cases"][0]["arms"]["with"][0]
            run0["graders"][0].update(passed=False, explanation="no match")
            run0.update(score=0.67, passed=False)
            data["cases"][0]["arms"]["with"].append(json.loads(json.dumps(run0)))
            code = 1
        elif scenario == "review-miss":
            # a review case, two runs: the first names every seeded defect, the second misses
            # the structural one; pooled structural recall is 3 of 4, under the rule's 1.0
            data["cases"][0]["name"] = REVIEW_CASE
            text = (ROOT / "evals" / "cases" / REVIEW_CASE / "reference.md").read_text(
                encoding="utf-8"
            )
            lines[-1]["result"] = text
            lines[5]["message"]["content"][0]["text"] = text
            run0 = data["cases"][0]["arms"]["with"][0]
            data["cases"][0]["arms"]["with"].append(json.loads(json.dumps(run0)))
            texts_by_run[1] = text.replace("Before you begin", "prerequisites")
        elif scenario in ("regression-half", "holdout-half"):
            # two runs, the second one failing a grader: a regression case clears its bar of
            # 1/2 on the first run; a holdout case fails at one of two under its 2/3 bar
            if scenario == "regression-half":
                data["cases"][0]["name"] = REGRESSION_CASE
                text = (ROOT / "evals" / "cases" / REGRESSION_CASE / "reference.md").read_text(
                    encoding="utf-8"
                )
                lines[-1]["result"] = text
                lines[5]["message"]["content"][0]["text"] = text
            run0 = data["cases"][0]["arms"]["with"][0]
            run1 = json.loads(json.dumps(run0))
            run1["graders"][0].update(passed=False, explanation="no match for ^## Steps")
            run1.update(score=0.67, passed=False)
            data["cases"][0]["arms"]["with"].append(run1)
            code = 1
        elif scenario in ("holdout-two-of-three", "holdout-one-of-three"):
            # The 2026-10-18 11:30 EDT decision: a holdout case runs three times and passes
            # at two of three, so one synonym miss is not a red gate and a repeated one is
            run0 = data["cases"][0]["arms"]["with"][0]
            failing = json.loads(json.dumps(run0))
            failing["graders"][0].update(passed=False, explanation="no match for ^## Steps")
            failing.update(score=0.67, passed=False)
            extra = [failing] if scenario == "holdout-two-of-three" else [failing, failing]
            while len(data["cases"][0]["arms"]["with"]) < 3:
                run = extra.pop(0) if extra else run0
                data["cases"][0]["arms"]["with"].append(json.loads(json.dumps(run)))
            code = 1
        for index, run in enumerate(data["cases"][0]["arms"]["with"]):
            # the CLI's kept directories are e-*; the first keeps the name older tests read
            kept = output_dir / ("e-fake" if index == 0 else f"e-fake{index}") / "out"
            kept.mkdir(parents=True)
            run_lines = json.loads(json.dumps(lines))
            if index in texts_by_run:
                run_lines[-1]["result"] = texts_by_run[index]
                run_lines[5]["message"]["content"][0]["text"] = texts_by_run[index]
            (kept / "trace.jsonl").write_text(
                "".join(json.dumps(line) + "\n" for line in run_lines), encoding="utf-8"
            )
            run["tracePath"] = str(kept / "trace.jsonl")
        Path(_flag(argv, "--json")).write_text(json.dumps(data, indent=2), encoding="utf-8")
        (output_dir / "aggregate-result.json").write_text(
            json.dumps(data, indent=2), encoding="utf-8"
        )
        return subprocess.CompletedProcess(argv, code, "", "")

    return run


@pytest.fixture
def dirs(tmp_path: Path) -> list[str]:
    return [
        "--results-dir",
        str(tmp_path / "results"),
        "--reports-dir",
        str(tmp_path / "reports"),
    ]


def _main(monkeypatch, scenario: str, argv: list[str]) -> tuple[int, list[list[str]]]:
    calls: list[list[str]] = []
    monkeypatch.setattr(gate.subprocess, "run", fake_cli(scenario, calls))
    return gate.main(argv), calls


def test_dry_run_prints_the_fixed_argv_and_never_spawns(monkeypatch, capsys, dirs):
    code, calls = _main(monkeypatch, "pass", ["--dry-run", *ARGS, *dirs])
    assert code == 0
    assert calls == []
    argv = shlex.split(capsys.readouterr().out.strip())
    assert argv[:4] == ["claude", "plugin", "eval", "."]
    for flag in ("--no-publish", "--trust-plugin", "--keep-temp"):
        assert flag in argv
    assert _flag(argv, "--ablation") == "none"
    assert _flag(argv, "--threshold") == "1.0"
    assert _flag(argv, "--eval-dir") == "evals"
    assert _flag(argv, "--max-cost-usd") == "10.00"
    assert _flag(argv, "--tag") == "holdout"
    assert _flag(argv, "--json").endswith("/run.json")
    assert Path(_flag(argv, "--json")).parent == Path(_flag(argv, "--output-dir"))


def test_the_model_is_pinned_to_sonnet_when_no_model_is_passed(monkeypatch, capsys, dirs):
    """Finding: an unpinned run mixed Opus and Sonnet, so a PASS was two models. The
    gate's default is the pin the plan Conventions name; --model still overrides it."""
    code, _ = _main(monkeypatch, "pass", ["--dry-run", *ARGS, *dirs])
    assert code == 0
    argv = shlex.split(capsys.readouterr().out.strip())
    assert _flag(argv, "--model") == "claude-sonnet-5-5"
    assert gate.DEFAULT_MODEL == "claude-sonnet-5-5"


def test_tag_model_runs_and_judge_model_pass_through_unchanged(monkeypatch, capsys, dirs):
    code, _ = _main(
        monkeypatch,
        "pass",
        [
            "--dry-run",
            "--tag",
            "holdout",
            "--model",
            "claude-opus-5-5",
            "--runs",
            "2",
            "--judge-model",
            "X",
            "--max-cost-usd",
            "10",
            *dirs,
        ],
    )
    assert code == 0
    argv = shlex.split(capsys.readouterr().out.strip())
    assert _flag(argv, "--tag") == "holdout"
    assert _flag(argv, "--model") == "claude-opus-5-5"
    assert _flag(argv, "--runs") == "2"
    assert _flag(argv, "--judge-model") == "X"


def test_cli_missing_from_path_exits_2_with_a_json_error(monkeypatch, capsys, dirs):
    code, _ = _main(monkeypatch, "cli-missing", [*ARGS, *dirs])
    assert code == 2
    body = json.loads(capsys.readouterr().out)
    assert set(body) == {"error"}
    assert "claude" in body["error"]


def test_a_failed_grader_exits_1_and_the_report_names_the_case(monkeypatch, capsys, dirs, tmp_path):
    code, _ = _main(monkeypatch, "grader-failed", [*ARGS, *dirs])
    assert code == 1
    out = capsys.readouterr().out
    assert f"{CASE}: FAIL" in out
    assert "headings" in out
    reports = list((tmp_path / "reports").glob("*.md"))
    assert len(reports) == 1
    assert CASE in reports[0].read_text(encoding="utf-8")


def test_no_aggregate_exits_2(monkeypatch, capsys, dirs):
    code, _ = _main(monkeypatch, "no-aggregate", [*ARGS, *dirs])
    assert code == 2
    body = json.loads(capsys.readouterr().out)
    assert "aggregate" in body["error"]


def test_a_partial_run_exits_2_even_when_the_cli_exits_0(monkeypatch, capsys, dirs):
    code, _ = _main(monkeypatch, "partial", [*ARGS, *dirs])
    assert code == 2
    body = json.loads(capsys.readouterr().out)
    assert "cost_ceiling" in body["error"]


def test_a_high_finding_fails_a_run_the_cli_graders_passed(monkeypatch, capsys, dirs, tmp_path):
    code, _ = _main(monkeypatch, "high-finding", [*ARGS, *dirs])
    assert code == 1
    assert f"{CASE}: FAIL" in capsys.readouterr().out
    (report,) = (tmp_path / "reports").glob("*.json")
    (row,) = json.loads(report.read_text(encoding="utf-8"))["rows"]
    assert row["pass"] is False
    assert row["counts"]["high"] >= 1


def test_a_green_run_keeps_the_trace_beside_the_result_and_exits_0(
    monkeypatch, capsys, dirs, tmp_path
):
    code, calls = _main(monkeypatch, "pass", [*ARGS, *dirs])
    assert code == 0
    assert [argv[1] for argv in calls] == ["plugin", "-p"]  # the eval run, then the judge
    out = capsys.readouterr().out
    assert f"{CASE}: PASS" in out
    (result_dir,) = (tmp_path / "results").iterdir()
    data = json.loads((result_dir / "run.json").read_text(encoding="utf-8"))
    trace = data["cases"][0]["arms"]["with"][0]["tracePath"]
    assert trace == f"{CASE}-run0.trace.jsonl"
    assert (result_dir / trace).is_file()
    assert len(list((tmp_path / "reports").glob("*.md"))) == 1


def test_a_partial_flag_alone_exits_2(monkeypatch, capsys, dirs):
    code, _ = _main(monkeypatch, "partial-flag-only", [*ARGS, *dirs])
    assert code == 2
    assert "partial" in json.loads(capsys.readouterr().out)["error"]


def test_an_empty_selection_is_apparatus_not_a_pass(monkeypatch, capsys, dirs):
    code, _ = _main(monkeypatch, "empty-selection", [*ARGS, *dirs])
    assert code == 2
    assert "no cases" in json.loads(capsys.readouterr().out)["error"]


def test_runs_that_never_reached_the_agent_are_apparatus(monkeypatch, capsys, dirs):
    code, _ = _main(monkeypatch, "never-exercised", [*ARGS, *dirs])
    assert code == 2
    body = json.loads(capsys.readouterr().out)["error"]
    assert CASE in body
    assert "never exercised" in body
    assert "bubblewrap" in body


def test_the_kept_run_directory_is_released_after_the_trace_is_copied(
    monkeypatch, capsys, dirs, tmp_path
):
    code, _ = _main(monkeypatch, "pass", [*ARGS, *dirs])
    assert code == 0
    (result_dir,) = (tmp_path / "results").iterdir()
    assert (result_dir / f"{CASE}-run0.trace.jsonl").is_file()
    assert not (result_dir / "e-fake").exists()


def test_the_threshold_is_not_an_option(monkeypatch, capsys, dirs):
    with pytest.raises(SystemExit) as exit_info:
        gate.main(["--dry-run", "--threshold", "0", *ARGS, *dirs])
    assert exit_info.value.code == 2
    assert "--threshold" in capsys.readouterr().err


def test_classify_names_the_sandbox_refusal_as_apparatus(tmp_path):
    code, reason = gate.classify(
        1, "no sandbox backend: install bubblewrap and socat", tmp_path / "aggregate-result.json"
    )
    assert code == 2
    assert "sandbox" in reason


def test_the_cli_judge_vote_is_recorded_and_the_gate_s_own_score_rules(monkeypatch, capsys, dirs):
    """Ruling: over six reads the CLI's prose-judge
    grader and the gate's judge disagreed once in 72 runs (the runbook run 0 of
    20261018T142400Z, three FAIL votes against a gate score of 4). The gate's judge is the one
    calibrated to the hand scores and the one whose answer is kept, so its score rules the
    run; the CLI grader's vote is recorded in the case line and counted nowhere, while every
    other grader keeps its veto (the grader-failed test above)."""
    code, _ = _main(monkeypatch, "judge-grader-failed", [*ARGS, *dirs])
    out = capsys.readouterr().out
    assert code == 0, out
    assert f"{CASE}: PASS (1 of 1 runs passed, bar 2/3" in out
    assert "prose-judge vote FAIL on run 0 (judge votes: FAIL FAIL FAIL), recorded" in out
    assert "graders below threshold" not in out


def test_a_regression_case_passes_its_bar_with_one_run_of_two(monkeypatch, capsys, dirs):
    """The 2026-10-17 ruling: regression-tagged cases pass at half their runs; the CLI's
    own exit (1, a run below 1.0) is not the verdict."""
    code, _ = _main(
        monkeypatch, "regression-half", ["--tag", "user-docs", "--max-cost-usd", "15", *dirs]
    )
    out = capsys.readouterr().out
    assert code == 0, out
    assert f"{REGRESSION_CASE}: PASS (1 of 2 runs passed, bar 1/2" in out
    assert "gate: PASS" in out


def test_a_holdout_case_fails_its_bar_with_one_run_of_two(monkeypatch, capsys, dirs):
    code, _ = _main(monkeypatch, "holdout-half", [*ARGS, *dirs])
    out = capsys.readouterr().out
    assert code == 1, out
    assert f"{CASE}: FAIL (1 of 2 runs passed, bar 2/3" in out
    assert "gate: FAIL" in out


def test_a_holdout_case_passes_at_two_of_three_and_fails_at_one_of_three(monkeypatch, capsys, dirs):
    """The 2026-10-18 11:30 EDT decision: a
    holdout case passes at two runs of three, so a single synonym miss is not a red gate while
    a repeated one still is."""
    code, _ = _main(monkeypatch, "holdout-two-of-three", [*ARGS, *dirs])
    out = capsys.readouterr().out
    assert code == 0, out
    assert f"{CASE}: PASS (2 of 3 runs passed, bar 2/3" in out
    code, _ = _main(monkeypatch, "holdout-one-of-three", [*ARGS, *dirs])
    out = capsys.readouterr().out
    assert code == 1, out
    assert f"{CASE}: FAIL (1 of 3 runs passed, bar 2/3" in out


def test_a_selection_with_a_holdout_case_runs_three_times_unless_runs_is_passed(
    monkeypatch, capsys, dirs
):
    """The 2026-10-18 11:30 and 11:45 EDT decisions: the holdout cases' own run count is
    two and the holdout is never edited, so the gate forces three runs whenever the selection
    (a tag, a case glob, or the whole suite) includes a holdout-tagged case, a domain read's
    included; a selection with no holdout case keeps each case's own count, and an explicit
    --runs passes through."""

    def argv_for(*selection: str) -> list[str]:
        code, _ = _main(
            monkeypatch, "pass", ["--dry-run", *selection, "--max-cost-usd", "10", *dirs]
        )
        assert code == 0
        return shlex.split(capsys.readouterr().out.strip())

    assert _flag(argv_for("--tag", "holdout"), "--runs") == str(gate.HOLDOUT_RUNS) == "3"
    assert _flag(argv_for("--tag", "engineering"), "--runs") == "3", (
        "the ADR holdout is engineering"
    )
    assert _flag(argv_for("--case", "adr--*"), "--runs") == "3"
    assert _flag(argv_for(), "--runs") == "3", "the whole suite includes the holdout"
    assert "--runs" not in argv_for("--tag", "api"), "no holdout case carries the api tag"
    assert "--runs" not in argv_for("--tag", "review")
    assert "--runs" not in argv_for("--case", "concept--*")
    assert _flag(argv_for("--tag", "holdout", "--runs", "2"), "--runs") == "2"


def test_case_bar_reads_the_set_tag_and_refuses_a_case_without_one(tmp_path):
    def case(tags: str) -> Path:
        d = tmp_path / tags.replace(" ", "").replace(",", "-").replace("[", "").replace("]", "")
        d.mkdir()
        (d / "prompt.md").write_text(
            f'---\nschema_version: "1.1"\ntags: {tags}\n---\n\nprompt\n', encoding="utf-8"
        )
        return d

    assert gate.case_bar(case("[user-docs, holdout]")) == gate.HOLDOUT_BAR == Fraction(2, 3)
    assert gate.case_bar(case("[user-docs, regression]")) == gate.REGRESSION_BAR
    assert gate.Decimal("0.5") == gate.REGRESSION_BAR
    with pytest.raises(gate.GateError, match="exactly one"):
        gate.case_bar(case("[user-docs]"))
    with pytest.raises(gate.GateError, match="exactly one"):
        gate.case_bar(case("[holdout, regression]"))


def test_the_gate_reads_front_matter_with_the_checker_s_one_pattern():
    """Done check: the gate carried its own copy of the front matter pattern. One
    shared helper; the gate imports the checker's."""
    import check_structure

    assert gate.FRONT_MATTER is check_structure.FRONT_MATTER
    # re.compile caches, so identity alone would pass a local copy; read the source
    source = Path(gate.__file__).read_text(encoding="utf-8")
    assert "from check_structure import FRONT_MATTER" in source
    assert "FRONT_MATTER = re.compile" not in source


def test_a_review_case_is_judged_by_pooled_recall_and_fails_under_the_rule(
    monkeypatch, capsys, dirs
):
    """The acceptance rule (structural 1.0, prose at least 0.9) is applied per
    case over the pooled runs; one structural miss in two runs fails the case, although the
    regression bar alone would pass it at one run of two."""
    code, _ = _main(monkeypatch, "review-miss", ["--tag", "review", "--max-cost-usd", "10", *dirs])
    out = capsys.readouterr().out
    assert code == 1, out
    assert f"{REVIEW_CASE}: FAIL (" in out
    assert "review recall structural 3 of 4, prose 4 of 4" in out
    assert "gate: FAIL" in out


def test_a_review_case_with_full_recall_still_fails_its_set_bar_when_the_graders_fail(
    monkeypatch, capsys, dirs
):
    code, _ = _main(
        monkeypatch, "review-graders-failed", ["--tag", "review", "--max-cost-usd", "10", *dirs]
    )
    out = capsys.readouterr().out
    assert code == 1, out
    assert f"{REVIEW_CASE}: FAIL (0 of 2 runs passed, bar 1/2" in out
    assert "review recall structural 4 of 4, prose 4 of 4" in out


def test_case_bar_refuses_malformed_front_matter_as_apparatus_naming_the_case(tmp_path):
    """Preflight style finding at c221cd7: malformed YAML in a case's
    prompt.md escaped as a traceback; the apparatus contract is exit 2 through GateError."""
    case = tmp_path / "broken--front-matter"
    case.mkdir()
    (case / "prompt.md").write_text(
        '---\nschema_version: "1.1"\ntags: [user-docs, holdout\n---\n\nprompt\n', encoding="utf-8"
    )
    with pytest.raises(gate.GateError, match="broken--front-matter") as info:
        gate.case_bar(case)
    assert "YAML" in str(info.value) or "yaml" in str(info.value)


def test_the_gate_pins_the_judge_model_to_the_prose_judge_s_one_constant(tmp_path):
    """An llm grader's judge is the CLI's background model unless --judge-model says
    otherwise; the gate passes the prose judge's model by default so every PASS, and the
    calibration set, are one judge's verdict."""
    prose_judge = load_evals_module("prose_judge")
    opts = gate.parse_args(ARGS)
    argv = gate.build_argv(opts, "stamp")
    assert _flag(argv, "--judge-model") == prose_judge.JUDGE_MODEL == "claude-sonnet-5-5"
    assert gate.DEFAULT_JUDGE_MODEL == prose_judge.JUDGE_MODEL
    opts = gate.parse_args([*ARGS, "--judge-model", "claude-haiku-5-5"])
    assert _flag(gate.build_argv(opts, "stamp"), "--judge-model") == "claude-haiku-5-5"


def test_the_gate_judges_every_drafting_run_after_the_cli_and_the_report_carries_the_verdict(
    monkeypatch, capsys, dirs, tmp_path
):
    """The CLI keeps only the judge's votes, so the gate sends each drafting run's
    final text to the prose judge through the stripped `claude -p`, writes judge.json beside
    run.json, and the report and the gate line carry the per-model median, minimum and verdict."""
    prose_judge = load_evals_module("prose_judge")
    code, calls = _main(monkeypatch, "pass", [*ARGS, *dirs])
    out = capsys.readouterr().out
    assert code == 0, out
    judge_calls = [argv for argv in calls if argv[1] == "-p"]
    assert len(judge_calls) == 1
    assert _flag(judge_calls[0], "--model") == prose_judge.JUDGE_MODEL
    (sidecar,) = (tmp_path / "results").glob("*/judge.json")
    data = json.loads(sidecar.read_text(encoding="utf-8"))
    assert data["judge_model"] == prose_judge.JUDGE_MODEL
    assert [(r["case"], r["run"], r["score"]) for r in data["runs"]] == [(CASE, 0, 4)]
    assert "judge claude-sonnet-5-5: median 4, min 4 over 1 run, PASS" in out
    (report,) = (tmp_path / "reports").glob("*.json")
    assert json.loads(report.read_text(encoding="utf-8"))["judge"]["claude-sonnet-5-5"]["min"] == 4


def test_a_gated_model_below_the_judge_rule_fails_the_gate(monkeypatch, capsys, dirs):
    code, _ = _main(monkeypatch, "judge-low", [*ARGS, *dirs])
    out = capsys.readouterr().out
    assert code == 1, out
    assert f"{CASE}: PASS" in out, "the case clears its bar; the judge rule is the failure"
    assert "judge claude-sonnet-5-5: median 2, min 2 over 1 run, FAIL" in out
    assert "gate: FAIL" in out and "judge" in out.split("gate: FAIL")[1]


def test_a_judge_answer_without_a_score_is_apparatus(monkeypatch, capsys, dirs):
    code, _ = _main(monkeypatch, "judge-broken", [*ARGS, *dirs])
    assert code == 2
    body = json.loads(capsys.readouterr().out)
    assert "Score" in body["error"]


def test_a_review_run_is_never_sent_to_the_judge(monkeypatch, capsys, dirs):
    code, calls = _main(monkeypatch, "review-miss", [*ARGS, *dirs])
    assert code == 1
    assert [argv for argv in calls if argv[1] == "-p"] == []
