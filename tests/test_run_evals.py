# Description: Tests evals/run_evals.py, the deterministic grader over a claude plugin eval
# Description: result: loading a run, grading its final text against the case, and the report.
"""Tests for load_result, grade_run, write_report, and main."""

import json
import shutil
import subprocess
from decimal import Decimal
from pathlib import Path

import pytest
from conftest import FIXTURES_DIR, ROOT
from plugin_eval import PLUGIN_EVAL_DIR, load_evals_module

run_evals = load_evals_module("run_evals")

RESULT = PLUGIN_EVAL_DIR / "result.json"
TASK_CASE = ROOT / "evals" / "holdout" / "task--relay-alert-rule"
TASK_REFERENCE = TASK_CASE / "reference.md"
REVIEW_CASE = ROOT / "evals" / "cases" / "review--task-missing-prereqs"
REVIEW_REFERENCE = REVIEW_CASE / "reference.md"
STEP_TOO_LONG = FIXTURES_DIR / "task" / "fail-STEP_TOO_LONG.md"


def test_load_result_yields_one_case_with_one_graded_run():
    result = run_evals.load_result(RESULT)
    assert [case.name for case in result.cases] == ["task--relay-alert-rule"]
    (run,) = result.cases[0].runs
    assert run.index == 0
    assert run.model == "claude-sonnet-5-5"
    assert isinstance(run.cost_usd, Decimal)
    assert run.cost_usd == Decimal("0.08578530000000001")
    assert run.claude_version == "2.1.301"
    assert run.text == TASK_REFERENCE.read_text(encoding="utf-8").rstrip("\n")
    assert run.error is None


def test_grade_run_passes_the_holdout_reference_and_finds_its_markers():
    grade = run_evals.grade_run(TASK_CASE, TASK_REFERENCE.read_text(encoding="utf-8"))
    assert grade.passed is True
    assert grade.unverified_found == ["permission"]
    assert grade.unverified_missing == []
    assert grade.counts["high"] == grade.counts["medium"] == grade.counts["low"] == 0


def test_grade_run_fails_when_an_expected_marker_is_absent():
    text = TASK_REFERENCE.read_text(encoding="utf-8").replace(
        " [UNVERIFIED: the permission or role that grants access to Alert rules]", ""
    )
    assert "[UNVERIFIED:" not in text
    grade = run_evals.grade_run(TASK_CASE, text)
    assert grade.passed is False
    assert grade.unverified_found == []
    assert grade.unverified_missing == ["permission"]


def _marker_case(tmp_path: Path, unverified: list[str]) -> Path:
    """A write-mode task case whose expected markers are the given entries."""
    case = tmp_path / "task--unit"
    case.mkdir(exist_ok=True)
    (case / "expected.json").write_text(
        json.dumps(
            {"template": "task", "audience": "engineer", "unverified": unverified, "defects": []}
        ),
        encoding="utf-8",
    )
    return case


def test_marker_entries_are_patterns_searched_inside_each_marker(tmp_path: Path):
    """The 2026-10-17 22:36 EDT ruling: an expected ``unverified`` entry is a
    case-insensitive pattern searched inside each ``[UNVERIFIED: ...]`` marker, so a marker
    that names the missing fact in other words is found when the entry lists them; a plain
    word behaves as before; a pattern no marker matches is still missing."""
    text = TASK_REFERENCE.read_text(encoding="utf-8").replace(
        "[UNVERIFIED: the permission or role that grants access to Alert rules]",
        "[UNVERIFIED: how long a stream keeps a message before it expires]",
    )
    assert "[UNVERIFIED: how long a stream keeps" in text
    grade = run_evals.grade_run(_marker_case(tmp_path, ["retention|keep|kept|expire"]), text)
    assert grade.unverified_found == ["retention|keep|kept|expire"]
    assert grade.unverified_missing == []

    reference = TASK_REFERENCE.read_text()
    grade = run_evals.grade_run(_marker_case(tmp_path, ["Permission"]), reference)
    assert grade.unverified_found == ["Permission"], "a plain word still matches, case aside"
    assert grade.unverified_missing == []

    grade = run_evals.grade_run(_marker_case(tmp_path, ["retention|ttl"]), reference)
    assert grade.unverified_found == []
    assert grade.unverified_missing == ["retention|ttl"]
    assert grade.passed is False


def test_marker_entry_that_is_not_a_pattern_is_a_result_error(tmp_path: Path):
    """An entry that does not compile is the case's defect, raised as ResultError
    naming the case and the entry, never a traceback from the grader."""
    with pytest.raises(run_evals.ResultError, match=r"task--unit.*\(unbalanced"):
        run_evals.grade_run(_marker_case(tmp_path, ["(unbalanced"]), TASK_REFERENCE.read_text())


def test_grade_run_fails_the_long_step_fixture_with_its_code():
    grade = run_evals.grade_run(TASK_CASE, STEP_TOO_LONG.read_text(encoding="utf-8"))
    assert grade.passed is False
    assert "STEP_TOO_LONG" in [finding["code"] for finding in grade.findings]
    assert grade.counts["medium"] >= 1


def test_write_report_writes_markdown_and_json_with_a_header_and_one_row_per_run(
    tmp_path: Path,
):
    result = run_evals.load_result(RESULT)
    rows = run_evals.grade_result(result, [TASK_CASE.parent])
    stamp = run_evals.write_report(result, rows, tmp_path, label="unit")
    assert stamp == "20261017T172249Z-unit"
    markdown = (tmp_path / f"{stamp}.md").read_text(encoding="utf-8")
    report = json.loads((tmp_path / f"{stamp}.json").read_text(encoding="utf-8"))
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True, cwd=ROOT
    ).stdout.strip()
    plugin_version = json.loads(
        (ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
    )["version"]
    dirty = bool(
        subprocess.run(
            ["git", "status", "--porcelain"], capture_output=True, text=True, check=True, cwd=ROOT
        ).stdout.strip()
    )
    assert report["header"] == {
        "claude_version": "2.1.301",
        "plugin_version": plugin_version,
        "git_head": head,
        "git_dirty": dirty,
        "label": "unit",
        "result": RESULT.relative_to(ROOT).as_posix(),
        "started_at": "2026-10-17T17:22:49.646Z",
        "cost_usd": "0.08578530000000001",
        "partial": False,
    }
    (row,) = report["rows"]
    assert row["case"] == "task--relay-alert-rule"
    assert row["model"] == "claude-sonnet-5-5"
    assert row["run"] == 0
    assert row["pass"] is True
    # The reference's one marker sits in a section whose slot the version line already fills;
    # the checker still lists it at info, and the grader reads it from the text.
    assert row["counts"] == {"high": 0, "medium": 0, "low": 0, "info": 1}
    assert row["grade"]["unverified_found"] == ["permission"]
    assert row["cost_usd"] == "0.08578530000000001"
    assert "| task--relay-alert-rule | claude-sonnet-5-5 | 0 | PASS |" in markdown
    assert f"git HEAD {head}, dirty {str(dirty).lower()}" in markdown


def test_git_dirty_reads_the_working_tree_of_the_repository_it_is_given(tmp_path: Path):
    """Finding: a report stamped with HEAD alone cannot say whether the skill it graded
    was the committed one. The flag is git status --porcelain non-empty, read from the tree."""
    repo = tmp_path / "repo"
    repo.mkdir()
    git = ["git", "-c", "user.name=t", "-c", "user.email=t@example.com", "-C", str(repo)]
    subprocess.run([*git, "init", "-q"], check=True)
    (repo / "a.txt").write_text("a\n", encoding="utf-8")
    subprocess.run([*git, "add", "a.txt"], check=True)
    subprocess.run([*git, "commit", "-q", "-m", "a"], check=True)
    assert run_evals._git_dirty(repo) is False
    (repo / "b.txt").write_text("b\n", encoding="utf-8")
    assert run_evals._git_dirty(repo) is True
    (repo / "a.txt").write_text("changed\n", encoding="utf-8")
    (repo / "b.txt").unlink()
    assert run_evals._git_dirty(repo) is True


def test_grade_run_matches_expected_defects_by_code_and_message_pattern(tmp_path: Path):
    expected = json.loads((TASK_CASE / "expected.json").read_text(encoding="utf-8"))
    expected["defects"] = [
        {"code": "STEP_TOO_LONG", "pattern": r"the cap is 20"},
        {"code": "STEP_TOO_LONG", "pattern": r"no such message"},
        {"code": "STEM_MISSING", "pattern": r"."},
    ]
    case = tmp_path / "task--defects"
    case.mkdir()
    (case / "expected.json").write_text(json.dumps(expected), encoding="utf-8")
    grade = run_evals.grade_run(case, STEP_TOO_LONG.read_text(encoding="utf-8"))
    assert grade.defects_found == ["STEP_TOO_LONG"]
    assert grade.defects_missing == ["STEP_TOO_LONG", "STEM_MISSING"]
    assert grade.passed is False


def test_write_report_sanitizes_the_label_in_the_stamp(tmp_path: Path):
    result = run_evals.load_result(RESULT)
    rows = run_evals.grade_result(result, [TASK_CASE.parent])
    stamp = run_evals.write_report(result, rows, tmp_path, label="a/b c")
    assert stamp == "20261017T172249Z-a_b_c"
    assert (tmp_path / f"{stamp}.md").is_file()
    assert (tmp_path / f"{stamp}.json").is_file()


def test_main_exits_2_with_a_json_error_body_on_a_missing_result(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
):
    missing = tmp_path / "absent" / "run.json"
    code = run_evals.main(["--result", str(missing), "--out", str(tmp_path / "reports")])
    assert code == 2
    body = json.loads(capsys.readouterr().out)
    assert set(body) == {"error"}
    assert str(missing) in body["error"]


def test_main_exits_2_with_a_json_error_body_when_the_out_path_is_a_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
):
    occupied = tmp_path / "reports"
    occupied.write_text("", encoding="utf-8")
    code = run_evals.main(["--result", str(RESULT), "--out", str(occupied)])
    assert code == 2
    body = json.loads(capsys.readouterr().out)
    assert set(body) == {"error"}
    assert str(occupied) in body["error"]


def test_main_grades_the_fixture_and_writes_a_report(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
):
    code = run_evals.main(["--result", str(RESULT), "--out", str(tmp_path)])
    assert code == 0
    written = sorted(p.name for p in tmp_path.iterdir())
    assert written == ["20261017T172249Z.json", "20261017T172249Z.md"]
    out = capsys.readouterr().out
    assert "task--relay-alert-rule run 0: PASS" in out


# ---- review mode --------------------------------------------------------------

REVIEW_DEFECTS = [
    {"code": "SECTION_MISSING", "pattern": r"Before you begin"},
    {"code": "EVIDENCE_MISSING", "pattern": r"unverified|source"},
    {"code": "BANNED_PATTERN", "pattern": r"gerund|-ing|infinitive"},
    {"code": "BANNED_PATTERN", "pattern": r"em dash"},
]
FULL_REPLY = """\
Findings for the Northwind Relay task topic, ranked by severity.

- high: the required Before you begin section is missing (templates/task.md).
- high: the version claim in the summary names no source; mark it [UNVERIFIED: the release]
  or cite the release line (templates/task.md, evidence slot).
- low: the heading Configuring the route is a gerund; task headings start with a bare
  infinitive (templates/task.md, banned patterns).
- low: line 9 carries an em dash; write a comma or two sentences (style-rules.md).
"""


def _review_case(tmp_path: Path, defects: list[dict[str, str]]) -> Path:
    case = tmp_path / "review--unit"
    case.mkdir()
    (case / "expected.json").write_text(
        json.dumps(
            {
                "template": "task",
                "audience": "engineer",
                "mode": "review",
                "unverified": [],
                "defects": defects,
            }
        ),
        encoding="utf-8",
    )
    return case


def test_review_grade_splits_recall_into_structural_and_prose(tmp_path: Path):
    """Defects listed on a review case are patterns the reply must contain, and
    recall is the fraction found, split by code class: SECTION_*, EVIDENCE_MISSING and
    H1_COUNT are structural; BANNED_PATTERN and the heading-form codes are prose."""
    case = _review_case(tmp_path, REVIEW_DEFECTS)
    grade = run_evals.grade_run(case, FULL_REPLY)
    assert grade.mode == "review"
    assert grade.recall.structural_found == 2 and grade.recall.structural_total == 2
    assert grade.recall.prose_found == 2 and grade.recall.prose_total == 2
    assert grade.recall.structural == Decimal(1)
    assert grade.recall.prose == Decimal(1)
    assert grade.passed is True

    shouted = FULL_REPLY.replace("em dash", "EM DASH").replace("gerund", "Gerund")
    grade = run_evals.grade_run(case, shouted)
    assert grade.recall.prose == Decimal(1), "patterns match the reply case-insensitively"

    missing_structural = FULL_REPLY.replace("Before you begin", "prerequisites")
    grade = run_evals.grade_run(case, missing_structural)
    assert grade.recall.structural_found == 1 and grade.recall.structural_total == 2
    assert grade.recall.prose_found == 2
    assert grade.defects_missing == ["SECTION_MISSING"]
    assert grade.passed is False


def test_review_grade_of_the_case_reference_is_full_recall_in_both_classes():
    """The first review case's reference names every seeded defect."""
    grade = run_evals.grade_run(REVIEW_CASE, REVIEW_REFERENCE.read_text(encoding="utf-8"))
    assert grade.mode == "review"
    assert grade.recall.structural == Decimal(1)
    assert grade.recall.prose == Decimal(1)
    assert grade.defects_missing == []
    assert grade.passed is True


def test_review_grade_missing_one_prose_defect_shows_both_numbers_in_the_report(
    tmp_path: Path,
):
    """A reply missing one prose defect yields the right fraction, and the
    report row says review and carries both numbers."""
    case = _review_case(tmp_path, REVIEW_DEFECTS)
    reply = FULL_REPLY.replace("carries an em dash", "carries a long dash")
    grade = run_evals.grade_run(case, reply)
    assert grade.recall.structural == Decimal(1)
    assert grade.recall.prose == Decimal("0.5")
    assert grade.defects_missing == ["BANNED_PATTERN"]
    assert grade.passed is False
    row = run_evals.Row(
        case=case.name,
        model="claude-sonnet-5-5",
        run=0,
        passed=grade.passed,
        counts=grade.counts,
        cost_usd=Decimal("0.1"),
        grade=grade,
        error=None,
    )
    result = run_evals.load_result(RESULT)
    stamp = run_evals.write_report(result, [row], tmp_path / "reports", label="review")
    markdown = (tmp_path / "reports" / f"{stamp}.md").read_text(encoding="utf-8")
    report = json.loads((tmp_path / "reports" / f"{stamp}.json").read_text(encoding="utf-8"))
    assert "| review--unit | claude-sonnet-5-5 | 0 | FAIL |" in markdown
    assert "review: structural 2 of 2, prose 1 of 2" in markdown
    (json_row,) = report["rows"]
    assert json_row["grade"]["mode"] == "review"
    assert json_row["grade"]["recall"] == {
        "structural_found": 2,
        "structural_total": 2,
        "prose_found": 1,
        "prose_total": 2,
    }


def test_review_grade_never_runs_the_checker_over_the_reply(tmp_path: Path, monkeypatch):
    """The reply is findings, not a document; check_document is not called, the
    counts are zero, and the row's note says review."""

    def forbidden(*args, **kwargs):
        raise AssertionError("check_document ran over a review reply")

    monkeypatch.setattr(run_evals, "check_document", forbidden)
    case = _review_case(tmp_path, REVIEW_DEFECTS)
    grade = run_evals.grade_run(case, FULL_REPLY)
    assert grade.findings == []
    assert grade.counts == {"high": 0, "medium": 0, "low": 0, "info": 0}
    row = run_evals.Row(
        case=case.name,
        model=None,
        run=0,
        passed=True,
        counts=grade.counts,
        cost_usd=None,
        grade=grade,
        error=None,
    )
    assert run_evals._note(row).startswith("review: structural 2 of 2, prose 2 of 2")


def test_review_accepts_structural_at_one_and_prose_at_nine_tenths():
    """The rule itself: structural recall must be 1.0 and prose at least 0.9."""
    recall = run_evals.Recall
    assert run_evals.review_accepts(recall(2, 2, 9, 10)) is True
    assert run_evals.review_accepts(recall(2, 2, 8, 10)) is False
    assert run_evals.review_accepts(recall(9, 10, 10, 10)) is False
    assert run_evals.review_accepts(recall(0, 0, 0, 0)) is True
    assert Decimal(1) == run_evals.REVIEW_STRUCTURAL_BAR
    assert Decimal("0.9") == run_evals.REVIEW_PROSE_BAR


def test_pooled_recall_sums_the_case_runs_and_counts_a_run_with_no_text_as_all_missing(
    tmp_path: Path,
):
    case = _review_case(tmp_path, REVIEW_DEFECTS)
    full = run_evals.grade_run(case, FULL_REPLY)
    partial = run_evals.grade_run(case, FULL_REPLY.replace("em dash", "long dash"))
    rows = [
        run_evals.Row(case.name, None, 0, full.passed, full.counts, None, full, None),
        run_evals.Row(case.name, None, 1, partial.passed, partial.counts, None, partial, None),
    ]
    pooled = run_evals.pooled_recall(case, rows)
    assert pooled == run_evals.Recall(4, 4, 3, 4)
    dead = run_evals.Row(case.name, None, 2, False, full.counts, None, None, "timed out")
    assert run_evals.pooled_recall(case, [*rows, dead]) == run_evals.Recall(4, 6, 3, 6)


def test_an_unknown_mode_in_expected_json_is_apparatus(tmp_path: Path):
    case = _review_case(tmp_path, REVIEW_DEFECTS)
    expected = json.loads((case / "expected.json").read_text(encoding="utf-8"))
    expected["mode"] = "audit"
    (case / "expected.json").write_text(json.dumps(expected), encoding="utf-8")
    with pytest.raises(run_evals.ResultError, match="mode"):
        run_evals.grade_run(case, FULL_REPLY)


# ---- the prose judge ------------------------------------------------------------

CALIBRATION_DIR = ROOT / "evals" / "calibration"


def test_the_judge_agrees_with_the_hand_scores_within_one_point_on_every_calibration_document():
    """The 2026-10-17 10:22 EDT ruling: the hand scores in scores.yaml and the
    judge's scores over the same six documents in judge.json must land within one point of
    each other, and no hand score may be null. A disagreement is fixed in the rubric wording,
    never in scores.yaml."""
    import yaml

    hand = yaml.safe_load((CALIBRATION_DIR / "scores.yaml").read_text(encoding="utf-8"))
    assert hand["scored_on"] is not None, "scores.yaml is not scored yet (scored_on is null)"
    hand_scores = {entry["file"]: entry["score"] for entry in hand["documents"]}
    unscored = sorted(name for name, score in hand_scores.items() if score is None)
    assert unscored == [], f"hand scores still null: {unscored}"
    assert len(hand_scores) == 6
    judge_path = CALIBRATION_DIR / "judge.json"
    assert judge_path.is_file(), "evals/calibration/judge.json is missing; run evals/calibrate.py"
    judge = json.loads(judge_path.read_text(encoding="utf-8"))
    assert judge["rubric"] == hand["rubric"] == "evals/rubrics/prose.md"
    prose_judge = load_evals_module("prose_judge")
    assert judge["rubric_sha256"] == prose_judge.rubric_sha256(), (
        "judge.json was scored against another rubric; run evals/calibrate.py again"
    )
    stale = [
        entry["file"]
        for entry in judge["documents"]
        if entry.get("criteria_sha256")
        != prose_judge.criteria_sha256(entry["template"], entry["audience"])
    ]
    assert stale == [], (
        f"judge.json was scored against other criteria for {stale} (the rubric or a template "
        "body changed); run evals/calibrate.py again"
    )
    judge_scores = {entry["file"]: entry["score"] for entry in judge["documents"]}
    assert set(judge_scores) == set(hand_scores)
    disagreements = []
    for name, hand_score in sorted(hand_scores.items()):
        judge_score = judge_scores[name]
        if not isinstance(judge_score, int) or abs(judge_score - hand_score) > 1:
            disagreements.append(f"{name}: hand {hand_score}, judge {judge_score}")
    assert disagreements == [], "\n".join(disagreements)


def test_parse_score_reads_the_judge_s_score_line_and_refuses_an_answer_without_one():
    """The judge answers with a Score: line first, 1 to 5 or Unknown; anything else is the
    apparatus, not a low score."""
    prose_judge = load_evals_module("prose_judge")
    assert prose_judge.parse_score("Score: 4\n\nLeads with the point: ...") == 4
    assert prose_judge.parse_score("  score: 1 \nfiller") == 1
    assert prose_judge.parse_score("Score: Unknown. The text is a refusal.") is None
    assert prose_judge.parse_score("Reasoning first.\nScore: 5") == 5
    with pytest.raises(prose_judge.JudgeError, match="Score"):
        prose_judge.parse_score("The document is fine, I would give it a four.")
    with pytest.raises(prose_judge.JudgeError, match="Score"):
        prose_judge.parse_score("Score: 7")


def test_the_judge_criteria_carry_the_template_s_sections_with_what_each_asks_for():
    """The 2026-10-18 09:38 EDT ruling: the rubric exempts a required section for
    doing its job, which the judge can apply only if it knows the sections, so the criteria
    list the template's sections in order with the template body's first paragraph under
    each heading, its Required or Optional opener dropped; an optional section says so; a
    pattern section with no body heading of its own carries its label alone; a type naming
    no template is a JudgeError, since every case's expected.json names a shipped one."""
    prose_judge = load_evals_module("prose_judge")
    text = prose_judge.criteria("postmortem", "engineer")
    assert "A postmortem written for the engineer audience." in text
    assert "## The template's sections" in text
    summary = "- Summary: The incident in one paragraph for a reader who reads nothing else"
    assert summary in text, text
    assert "Required." not in text.split("## The template's sections")[1]
    assert text.index("- Summary:") < text.index("- Impact:") < text.index("- Lessons learned:")
    runbook = prose_judge.criteria("runbook", "operator")
    assert "- Rollback (optional): How to undo a mitigation step" in runbook, runbook
    tutorial = prose_judge.criteria("tutorial", "engineer")
    assert "- Before you begin: Required, and the only prerequisites section" in tutorial, (
        "a comma opener is a clause of the sentence and stays, so the judge gets no fragment"
    )
    adr = prose_judge.criteria("architecture decision record", "engineer")
    assert "in Nygard's active voice:\n" not in adr, "a purpose cut at a code block loses its colon"
    assert "in Nygard's active voice\n" in adr
    notes = prose_judge.criteria("release notes", "engineer")
    assert "\n- the version section\n" in notes, notes
    with pytest.raises(prose_judge.JudgeError, match="names no template"):
        prose_judge.criteria("memo", "engineer")


SMOKE_RESULT = {
    # the keys a `claude -p --output-format json` result carried on 2026-10-17 (claude 2.1.302,
    # a stripped call: no tools, no MCP, no settings); the calibration driver reads result,
    # is_error, total_cost_usd and modelUsage
    "type": "result",
    "subtype": "success",
    "is_error": False,
    "result": "ok",
    "total_cost_usd": 0.000126,
    "num_turns": 1,
    "session_id": "0",
    "stop_reason": "end_turn",
    "usage": {"input_tokens": 2, "output_tokens": 4},
    "modelUsage": {"claude-sonnet-5-5": {"costUSD": 0.000126, "costBasis": "list"}},
}


def _fake_judge(answers: dict[str, str], calls: list[list[str]]):
    """A stand-in for subprocess.run that answers `claude -p` as the stripped smoke call did,
    picking the answer by the calibration document whose text the prompt carries."""

    def run(argv, **kwargs):
        if argv[0] != "claude":
            return subprocess.run(argv, **kwargs)
        calls.append(list(argv))
        prompt = kwargs["input"]
        name = next(
            name
            for name in answers
            if (CALIBRATION_DIR / name).read_text(encoding="utf-8").strip() in prompt
        )
        body = dict(SMOKE_RESULT, result=answers[name])
        return subprocess.CompletedProcess(argv, 0, json.dumps(body), "")

    return run


def _hand_scores() -> dict[str, int]:
    import yaml

    hand = yaml.safe_load((CALIBRATION_DIR / "scores.yaml").read_text(encoding="utf-8"))
    return {entry["file"]: entry["score"] for entry in hand["documents"]}


def test_calibrate_judges_each_document_with_the_stripped_call_and_writes_judge_json(
    tmp_path: Path, monkeypatch, capsys
):
    """evals/calibrate.py sends the same criteria the grader carries, plus the document, to
    the judge model through a context-free `claude -p`, writes judge.json beside scores.yaml,
    and exits 0 when every judge score is within one point of the hand score."""
    calibrate = load_evals_module("calibrate")
    prose_judge = load_evals_module("prose_judge")
    hand = _hand_scores()
    answers = {
        name: f"Score: {score}\n\nLeads with the point: held." for name, score in hand.items()
    }
    calls: list[list[str]] = []
    monkeypatch.setattr(calibrate.subprocess, "run", _fake_judge(answers, calls))
    out = tmp_path / "judge.json"
    code = calibrate.main(["--out", str(out)])
    assert code == 0, capsys.readouterr().out
    assert len(calls) == 6
    for argv in calls:
        assert argv[:2] == ["claude", "-p"]
        assert _arg(argv, "--model") == prose_judge.JUDGE_MODEL
        assert _arg(argv, "--output-format") == "json"
        assert _arg(argv, "--tools") == ""
        assert _arg(argv, "--setting-sources") == ""
        assert "--strict-mcp-config" in argv and "--no-session-persistence" in argv
        assert "--system-prompt" in argv
    judge = json.loads(out.read_text(encoding="utf-8"))
    assert judge["rubric"] == "evals/rubrics/prose.md"
    assert judge["judge_model"] == prose_judge.JUDGE_MODEL
    assert judge["scored_on"]
    assert {d["file"]: d["score"] for d in judge["documents"]} == hand
    doc = judge["documents"][0]
    assert set(doc) >= {"file", "case", "template", "audience", "score", "answer", "cost_usd"}
    for doc in judge["documents"]:
        assert doc["criteria_sha256"] == prose_judge.criteria_sha256(
            doc["template"], doc["audience"]
        ), "each document records the hash of the full criteria text it was judged against"
    assert doc["cost_usd"] == "0.000126"
    printed = capsys.readouterr().out
    assert "agree" in printed


def test_calibrate_exits_1_on_a_disagreement_beyond_one_point_and_names_it(
    tmp_path: Path, monkeypatch, capsys
):
    calibrate = load_evals_module("calibrate")
    hand = _hand_scores()
    answers = {name: f"Score: {score}\nevidence" for name, score in hand.items()}
    first = next(iter(hand))
    answers[first] = f"Score: {hand[first] - 2}\nevidence"
    monkeypatch.setattr(calibrate.subprocess, "run", _fake_judge(answers, []))
    out = tmp_path / "judge.json"
    code = calibrate.main(["--out", str(out)])
    assert code == 1
    assert out.is_file(), "the scores are written even when they disagree; the rubric is fixed"
    printed = capsys.readouterr().out
    assert first in printed and "disagree" in printed


def test_calibrate_treats_a_failed_or_unparseable_judge_call_as_apparatus(
    tmp_path: Path, monkeypatch, capsys
):
    calibrate = load_evals_module("calibrate")
    hand = _hand_scores()
    answers = {name: "I would give this a four." for name in hand}
    monkeypatch.setattr(calibrate.subprocess, "run", _fake_judge(answers, []))
    code = calibrate.main(["--out", str(tmp_path / "judge.json")])
    assert code == 2
    body = json.loads(capsys.readouterr().out)
    assert "Score" in body["error"]
    assert not (tmp_path / "judge.json").exists()


def _arg(argv: list[str], flag: str) -> str:
    return argv[argv.index(flag) + 1]


JUDGE_SIDECAR = PLUGIN_EVAL_DIR / "judge.json"


def test_load_result_reads_the_judge_sidecar_and_the_report_carries_median_and_minimum_per_model(
    tmp_path: Path,
):
    """The gate judges each run's final text after the CLI run and writes
    judge.json beside run.json (the CLI keeps only the three votes); run_evals reads the score
    per run and the report carries the median and the minimum per model with the verdict."""
    result = run_evals.load_result(RESULT)
    (run,) = result.cases[0].runs
    assert run.judge_score == 4
    assert run.judge_answer.startswith("Score: 4")
    rows = run_evals.grade_result(result, [TASK_CASE.parent])
    (row,) = rows
    assert row.judge == 4 and row.judged is True
    summary = run_evals.judge_summary(rows)
    assert summary == {
        "claude-sonnet-5-5": {
            "runs": 1,
            "unknown": 0,
            "median": "4",
            "min": 4,
            "gated": True,
            "verdict": "PASS",
        }
    }
    stamp = run_evals.write_report(result, rows, tmp_path, label="judge")
    report = json.loads((tmp_path / f"{stamp}.json").read_text(encoding="utf-8"))
    assert report["judge"] == summary
    assert report["rows"][0]["judge"] == 4
    markdown = (tmp_path / f"{stamp}.md").read_text(encoding="utf-8")
    assert "| judge |" in markdown.splitlines()[5]
    assert "| task--relay-alert-rule | claude-sonnet-5-5 | 0 | PASS |" in markdown
    assert "judge claude-sonnet-5-5: median 4, min 4 over 1 run, PASS" in markdown


def test_a_result_with_no_judge_sidecar_loads_with_no_score_and_an_empty_summary(tmp_path: Path):
    copy = tmp_path / "plugin-eval"
    shutil.copytree(PLUGIN_EVAL_DIR, copy)
    (copy / "judge.json").unlink()
    result = run_evals.load_result(copy / "result.json")
    (run,) = result.cases[0].runs
    assert run.judge_score is None and run.judge_answer is None
    rows = run_evals.grade_result(result, [TASK_CASE.parent])
    assert rows[0].judge is None and rows[0].judged is False
    assert run_evals.judge_summary(rows) == {}
    stamp = run_evals.write_report(result, rows, tmp_path / "reports", label="nojudge")
    report = json.loads((tmp_path / "reports" / f"{stamp}.json").read_text(encoding="utf-8"))
    assert report["judge"] == {}


def test_a_judge_score_of_2_fails_the_rule_for_the_gated_models_and_is_recorded_for_haiku(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
):
    """Median at least 4 and no run below 3, applied to Sonnet 5.5 and Opus 5;
    Haiku 5.5 is recorded, never gated (spec, Acceptance)."""
    assert frozenset({"claude-sonnet-5-5", "claude-opus-5"}) == run_evals.GATED_MODELS
    assert run_evals.judge_accepts([4, 5, 3]) is True
    assert run_evals.judge_accepts([4, 4, 2]) is False, "no run below 3"
    assert run_evals.judge_accepts([3, 3, 4]) is False, "median below 4"
    assert run_evals.judge_accepts([5, 4]) is True, "an even count averages the two middles"
    assert run_evals.judge_accepts([4, 3]) is False
    assert run_evals.judge_accepts([5, 3]) is True, "median 4 of two middles 5 and 3"
    assert run_evals.judge_median([5, 4]) == run_evals.Decimal("4.5")
    assert run_evals.judge_accepts([]) is False, "no scores is not acceptance"

    def rows_for(model: str, scores: list[int | None]) -> list[run_evals.Row]:
        return [
            run_evals.Row("c", model, i, True, {}, None, None, None, judge=score, judged=True)
            for i, score in enumerate(scores)
        ]

    for model in ("claude-sonnet-5-5", "claude-opus-5"):
        (entry,) = run_evals.judge_summary(rows_for(model, [4, 5, 2])).values()
        assert entry["verdict"] == "FAIL" and entry["gated"] is True and entry["min"] == 2
    (entry,) = run_evals.judge_summary(rows_for("claude-haiku-5-5", [4, 5, 2])).values()
    assert entry["verdict"] == "recorded" and entry["gated"] is False
    (entry,) = run_evals.judge_summary(rows_for("claude-sonnet-5-5", [4, None, 5])).values()
    assert entry["unknown"] == 1 and entry["median"] == "4.5" and entry["verdict"] == "PASS"
    # the Sonnet arm 20261018T010341Z counted its six review runs as Unknown: a row the judge
    # never saw (a review run, a run with no text) counts nowhere
    review = run_evals.Row("review--x", "claude-sonnet-5-5", 0, True, {}, None, None, None)
    (entry,) = run_evals.judge_summary([*rows_for("claude-sonnet-5-5", [4, 5]), review]).values()
    assert entry["unknown"] == 0 and entry["runs"] == 2
    # Review round 1: a gated model whose every judged run came back Unknown has no
    # score to meet the rule with, so it stays in the summary and fails; a model the judge
    # never saw stays absent (the no-sidecar test above)
    (entry,) = run_evals.judge_summary(rows_for("claude-opus-5", [None, None])).values()
    assert entry == {
        "runs": 0,
        "unknown": 2,
        "median": None,
        "min": None,
        "gated": True,
        "verdict": "FAIL",
    }
    (entry,) = run_evals.judge_summary(rows_for("claude-haiku-5-5", [None])).values()
    assert entry["verdict"] == "recorded" and entry["runs"] == 0
    assert run_evals.judge_lines({"claude-opus-5": entry | {"gated": True, "verdict": "FAIL"}}) == [
        "judge claude-opus-5: no score over 0 runs, 1 unknown, FAIL"
    ]

    copy = tmp_path / "plugin-eval"
    shutil.copytree(PLUGIN_EVAL_DIR, copy)
    sidecar = json.loads((copy / "judge.json").read_text(encoding="utf-8"))
    sidecar["runs"][0]["score"] = 2
    (copy / "judge.json").write_text(json.dumps(sidecar), encoding="utf-8")
    code = run_evals.main(["--result", str(copy / "result.json"), "--out", str(tmp_path / "r")])
    out = capsys.readouterr().out
    assert code == 1, out
    assert "task--relay-alert-rule run 0: PASS" in out, "the checker still passes the run"
    assert "judge claude-sonnet-5-5: median 2, min 2 over 1 run, FAIL" in out


# ---- one result with a drafting case and a review case ---------------------------

MIXED_RESULT = PLUGIN_EVAL_DIR / "mixed" / "result.json"


def test_a_result_holding_a_drafting_case_and_a_review_case_reports_both_in_one_run(
    tmp_path: Path,
):
    """The v0.2.0 reports hold both kinds; the drafting row is graded by the checker
    and the judge, the review row by recall and never by the judge, and the judge summary
    counts only the drafting run."""
    result = run_evals.load_result(MIXED_RESULT)
    assert [case.name for case in result.cases] == [
        "task--relay-alert-rule",
        "review--task-missing-prereqs",
    ]
    rows = run_evals.grade_result(result, [TASK_CASE.parent, REVIEW_CASE.parent])
    drafting, review = rows
    assert drafting.grade.mode == "write" and drafting.passed is True
    assert drafting.judged is True and drafting.judge == 4
    assert review.grade.mode == "review" and review.passed is True
    assert review.judged is False and review.judge is None
    assert review.grade.recall.structural == Decimal(1)
    assert review.grade.recall.prose == Decimal(1)
    assert run_evals.judge_summary(rows)["claude-sonnet-5-5"]["runs"] == 1
    stamp = run_evals.write_report(result, rows, tmp_path, label="mixed")
    markdown = (tmp_path / f"{stamp}.md").read_text(encoding="utf-8")
    assert "| task--relay-alert-rule | claude-sonnet-5-5 | 0 | PASS |" in markdown
    assert "| review--task-missing-prereqs | claude-sonnet-5-5 | 0 | PASS |" in markdown
    assert "review: structural 2 of 2, prose 2 of 2" in markdown
    assert "judge claude-sonnet-5-5: median 4, min 4 over 1 run, PASS" in markdown
    report = json.loads((tmp_path / f"{stamp}.json").read_text(encoding="utf-8"))
    assert [row["grade"]["mode"] for row in report["rows"]] == ["write", "review"]
    assert report["header"]["cost_usd"] == "0.2"
