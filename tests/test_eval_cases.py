# Description: Eval-case harness: every case directory under evals/ and the synthetic harness
# Description: case carries the prompt, expected.json, graders, reference, and NOTES of the layout.
"""Tests over every eval case directory. The layout they enforce is fixed here."""

import hashlib
import json
import re
import shutil
from pathlib import Path

import pytest
from check_structure import AUDIENCES, load_template
from conftest import (
    HARNESS_CASE,
    case_dirs,
    read_expected,
    relative_id,
    split_front_matter,
    template_paths,
)

DOMAIN_TAGS = frozenset(
    {"user-docs", "engineering", "api", "ai-governance", "security", "privacy", "review"}
)
SET_TAGS = frozenset({"holdout", "regression"})
MODES = frozenset({"write", "review"})
# a Python inline flag group such as (?i) or (?im); a lookaround or a non-capturing group is not
INLINE_FLAGS = re.compile(r"\(\?[a-zA-Z]+(?:-[a-zA-Z]+)?\)")
# The review cases the plugin ships, one per holdout type. Each
# must exist under evals/cases/, grade in review mode, and carry the review tag.
REVIEW_CASES = frozenset(
    {
        "review--task-missing-prereqs",
        "review--adr-superseded-without-link",
        "review--model-card-no-disaggregation",
    }
)
ROOT_DIR = Path(__file__).resolve().parents[1]
RELEASE_NOTES_CASE = ROOT_DIR / "evals" / "cases" / "release-notes--relay-2-5-0"
RUN_KEYS = ("runs", "max_turns", "timeout_seconds")

CASES = case_dirs()


def known_template_types() -> set[str]:
    return {load_template(path).type for path in template_paths()}


def case_problems(case: Path) -> list[str]:
    """Every way the case directory departs from the layout, as one message each."""
    problems: list[str] = []
    problems.extend(_prompt_problems(case))
    problems.extend(_expected_problems(case))
    problems.extend(_grader_problems(case))
    if not (case / "reference.md").is_file():
        problems.append("reference.md is missing")
    problems.extend(_notes_problems(case))
    problems.extend(_mode_problems(case))
    return problems


def _prompt_problems(case: Path) -> list[str]:
    path = case / "prompt.md"
    if not path.is_file():
        return ["prompt.md is missing"]
    data, body = split_front_matter(path.read_text(encoding="utf-8"))
    if data is None:
        return ["prompt.md has no YAML front matter mapping"]
    problems: list[str] = []
    if data.get("schema_version") != "1.1":
        problems.append(f"prompt.md schema_version is {data.get('schema_version')!r}, not '1.1'")
    if data.get("name") != case.name:
        problems.append(f"prompt.md name is {data.get('name')!r}; the directory is {case.name!r}")
    tags = data.get("tags")
    if not isinstance(tags, list):
        problems.append("prompt.md tags must be a list")
    else:
        domain = [t for t in tags if t in DOMAIN_TAGS]
        if len(domain) != 1:
            problems.append(
                f"prompt.md tags carry {len(domain)} domain tags {domain}; exactly one of "
                f"{sorted(DOMAIN_TAGS)} is required"
            )
        sets = [t for t in tags if t in SET_TAGS]
        if len(sets) != 1:
            problems.append(
                f"prompt.md tags carry {len(sets)} of {sorted(SET_TAGS)}; exactly one is required"
            )
    for key in RUN_KEYS:
        value = data.get(key)
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            problems.append(f"prompt.md {key} must be a positive integer, got {value!r}")
    tools = data.get("allowed_tools")
    if not isinstance(tools, list) or "Skill" not in tools:
        problems.append(f"prompt.md allowed_tools must contain Skill, got {tools!r}")
    if not body.strip():
        problems.append("prompt.md has no prompt body after the front matter")
    return problems


def _expected_problems(case: Path) -> list[str]:
    path = case / "expected.json"
    if not path.is_file():
        return ["expected.json is missing"]
    expected = read_expected(case)
    problems: list[str] = []
    template = expected.get("template")
    if template not in known_template_types():
        problems.append(f"expected.json template {template!r} names no template")
    if expected.get("audience") not in AUDIENCES:
        problems.append(
            f"expected.json audience {expected.get('audience')!r} is not one of the seven"
        )
    unverified = expected.get("unverified")
    if not isinstance(unverified, list) or not all(isinstance(u, str) for u in unverified):
        problems.append("expected.json unverified must be a list of strings")
    defects = expected.get("defects")
    if not isinstance(defects, list) or not all(
        isinstance(d, dict) and set(d) == {"code", "pattern"} for d in defects
    ):
        problems.append("expected.json defects must be a list of code and pattern pairs")
    mode = expected.get("mode", "write")
    if mode not in MODES:
        problems.append(f"expected.json mode is {mode!r}; the modes are {sorted(MODES)}")
    return problems


def _mode_problems(case: Path) -> list[str]:
    """A review-tagged case grades in review mode and the other way round: the gate reads the
    tag for the bar, the grader reads expected.json for the mode, and they must agree."""
    prompt = case / "prompt.md"
    if not prompt.is_file() or not (case / "expected.json").is_file():
        return []
    data, _ = split_front_matter(prompt.read_text(encoding="utf-8"))
    tags = data.get("tags") if isinstance(data, dict) else None
    tagged = isinstance(tags, list) and "review" in tags
    mode = read_expected(case).get("mode", "write")
    if tagged and mode != "review":
        return ["prompt.md carries the review tag but expected.json mode is not review"]
    if mode == "review" and not tagged:
        return ["expected.json mode is review but prompt.md does not carry the review tag"]
    return []


def _grader_problems(case: Path) -> list[str]:
    graders = case / "graders"
    fired = graders / "skill-fired.md"
    if not fired.is_file():
        return ["graders/skill-fired.md is missing"]
    problems: list[str] = []
    data, _ = split_front_matter(fired.read_text(encoding="utf-8"))
    if data is None or data.get("type") != "tool_used" or data.get("tool") != "Skill":
        problems.append("graders/skill-fired.md must have type: tool_used and tool: Skill")
    if data is None or not _matches_skill_name(data.get("input_match")):
        problems.append("graders/skill-fired.md input_match must match technical-writer as a regex")
    for grader in sorted(graders.glob("*.md")):
        name = f"graders/{grader.name}"
        data, body = split_front_matter(grader.read_text(encoding="utf-8"))
        if data is None:
            problems.append(f"{name} has no YAML front matter mapping")
            continue
        if data.get("type") == "regex" and INLINE_FLAGS.search(str(data.get("pattern", ""))):
            problems.append(
                f"{name} pattern carries an inline flag group; the CLI compiles grader patterns "
                f"as JavaScript regexes, so write the flag in the flags field instead"
            )
        lines = [line for line in body.splitlines() if line.strip()]
        if not lines or not lines[0].startswith("Verifies:"):
            problems.append(f"{name} body must open with a Verifies: line")
        if len(lines) < 2 or not lines[1].startswith("Cannot verify:"):
            problems.append(f"{name} body must follow Verifies: with a Cannot verify: line")
    return problems


def _matches_skill_name(input_match: object) -> bool:
    """Whether the grader's input_match regex matches the skill name the runner sees."""
    if not isinstance(input_match, str):
        return False
    try:
        return re.search(input_match, "technical-writer") is not None
    except re.error:
        return False


def _notes_problems(case: Path) -> list[str]:
    path = case / "NOTES.md"
    if not path.is_file():
        return ["NOTES.md is missing"]
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    if not lines or not lines[0].startswith("Seed:"):
        return ["NOTES.md must open with a Seed: line (after an optional title)"]
    return []


@pytest.mark.parametrize("case", CASES, ids=relative_id)
def test_every_case_directory_keeps_the_layout(case: Path):
    problems = case_problems(case)
    assert problems == [], f"{relative_id(case)}:\n  " + "\n  ".join(problems)


def test_a_grader_without_its_cannot_verify_line_fails_naming_the_grader(tmp_path):
    copy = tmp_path / HARNESS_CASE.name
    shutil.copytree(HARNESS_CASE, copy)
    assert case_problems(copy) == []
    grader = copy / "graders" / "skill-fired.md"
    text = grader.read_text(encoding="utf-8")
    stripped = "\n".join(
        line for line in text.splitlines() if not line.startswith("Cannot verify:")
    )
    assert stripped != text
    grader.write_text(stripped + "\n", encoding="utf-8")
    problems = case_problems(copy)
    assert len(problems) == 1
    assert "graders/skill-fired.md" in problems[0]
    assert "Cannot verify:" in problems[0]


def test_skill_fired_input_match_is_judged_as_a_regex_against_the_skill_name(tmp_path):
    copy = tmp_path / HARNESS_CASE.name
    shutil.copytree(HARNESS_CASE, copy)
    grader = copy / "graders" / "skill-fired.md"
    text = grader.read_text(encoding="utf-8")
    grader.write_text(
        text.replace('input_match: "technical-writer"', 'input_match: "technical-writers"'),
        encoding="utf-8",
    )
    problems = case_problems(copy)
    assert len(problems) == 1 and "graders/skill-fired.md" in problems[0], problems

    grader.write_text(
        text.replace('input_match: "technical-writer"', 'input_match: "tech.*writer"'),
        encoding="utf-8",
    )
    assert case_problems(copy) == []


def test_a_review_tagged_case_must_grade_in_review_mode_and_the_mode_must_be_known(tmp_path):
    copy = tmp_path / HARNESS_CASE.name
    shutil.copytree(HARNESS_CASE, copy)
    prompt = copy / "prompt.md"
    prompt.write_text(
        prompt.read_text(encoding="utf-8").replace(
            "tags: [engineering, regression]", "tags: [review, regression]"
        ),
        encoding="utf-8",
    )
    problems = case_problems(copy)
    assert len(problems) == 1 and "mode" in problems[0], problems

    expected_path = copy / "expected.json"
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    expected["mode"] = "review"
    expected_path.write_text(json.dumps(expected), encoding="utf-8")
    assert case_problems(copy) == []

    expected["mode"] = "audit"
    expected_path.write_text(json.dumps(expected), encoding="utf-8")
    problems = case_problems(copy)
    assert any("mode is 'audit'" in p for p in problems), problems


def test_the_release_notes_date_grader_reads_the_first_line_under_the_version_heading():
    """Finding: the case left the date to the evidence slot, which the
    Fixed entry's marker filled, so a run that dropped the release line passed both layers."""
    grader = RELEASE_NOTES_CASE / "graders" / "release-date.md"
    data, body = split_front_matter(grader.read_text(encoding="utf-8"))
    assert data["type"] == "regex" and data["match"] == "contains"
    pattern = re.compile(data["pattern"], re.M if data.get("flags") == "m" else 0)
    reference = (RELEASE_NOTES_CASE / "reference.md").read_text(encoding="utf-8")
    release_line = "Released 2026-10-17. Northwind Relay follows Semantic Versioning. "
    assert release_line in reference
    assert pattern.search(reference)
    assert not pattern.search(reference.replace(release_line, ""))
    assert not pattern.search(reference.replace("Released 2026-10-17. ", ""))
    moved = reference.replace(
        release_line, "Northwind Relay follows Semantic Versioning. "
    ).replace("### Added", "Released 2026-10-17.\n\n### Added")
    assert not pattern.search(moved), "the date must sit on the first line under the heading"
    date_first = reference.replace(
        release_line, "2026-10-17: Northwind Relay follows Semantic Versioning. "
    )
    assert pattern.search(date_first), "a release line that opens with the date fills the slot"
    assert "Cannot verify:" in body
    version = RELEASE_NOTES_CASE / "graders" / "version-section.md"
    _, version_body = split_front_matter(version.read_text(encoding="utf-8"))
    assert "release-date.md" in version_body


@pytest.mark.parametrize("name", sorted(REVIEW_CASES))
def test_every_review_case_is_present_and_grades_in_review_mode(name: str):
    case = RELEASE_NOTES_CASE.parent / name
    assert case.is_dir(), f"{name}: no case directory under evals/cases/"
    assert read_expected(case).get("mode") == "review"
    data, _ = split_front_matter((case / "prompt.md").read_text(encoding="utf-8"))
    assert "review" in data["tags"]
    assert case_problems(case) == []


def test_a_regex_grader_with_a_python_inline_flag_fails_naming_the_grader(tmp_path):
    """Eval run 20261017T232653Z: every regex grader written with (?i) threw in the
    CLI (Invalid regular expression: unrecognized character after (?); the CLI's graders are
    JavaScript regexes). The flag belongs in the flags field."""
    copy = tmp_path / HARNESS_CASE.name
    shutil.copytree(HARNESS_CASE, copy)
    grader = copy / "graders" / "inline-flag.md"
    grader.write_text(
        '---\ntype: regex\npattern: "(?i)context"\nmatch: contains\n---\n\n'
        "Verifies: x.\nCannot verify: y.\n",
        encoding="utf-8",
    )
    problems = case_problems(copy)
    assert len(problems) == 1 and "graders/inline-flag.md" in problems[0], problems
    assert "flags field" in problems[0]
    grader.write_text(
        '---\ntype: regex\npattern: "(?:con)text(?!s)"\nflags: i\nmatch: contains\n---\n\n'
        "Verifies: x.\nCannot verify: y.\n",
        encoding="utf-8",
    )
    assert case_problems(copy) == []


# ---- the prose judge ------------------------------------------------------------


def _drafting_cases() -> list[Path]:
    return [
        case
        for case in CASES
        if case != HARNESS_CASE and read_expected(case).get("mode", "write") != "review"
    ]


# The three holdout cases' expected.json files, frozen at their original content (the
# Conventions: written attended, never edited afterwards). A later change turned every unverified
# entry into a pattern; the holdout entries are plain words and stay byte for byte as committed.
HOLDOUT_EXPECTED_SHA256 = {
    "adr--relay-queue-backend": "331372cfc9a6fd449b6bf812423e1dcc2f1415dd0578bc6bcb6752a1a4b30232",
    "model-card--relay-intent-classifier": (
        "5ab14aed5fbea37958ae4bd572485fd89fb476fb4bf6530d883380d316e39503"
    ),
    "task--relay-alert-rule": "13d9267d4b720ab34a7bbf1933bc869ab02d9a904604160502b4680bbe855a60",
}


@pytest.mark.parametrize("case", CASES, ids=relative_id)
def test_every_unverified_entry_compiles_as_a_pattern(case: Path):
    """The grader searches each expected unverified entry as a case-insensitive
    pattern inside the markers, so every entry in every case must compile, and the two
    regression cases the ruling names carry their alternatives."""
    for entry in read_expected(case).get("unverified", []):
        re.compile(entry, re.IGNORECASE)
    alternatives = {
        "concept--relay-routing-model": "retention|keep|kept|expire",
        "multiple-task--relay-install-and-verify": "port|listen",
    }
    if case.name in alternatives:
        assert alternatives[case.name] in read_expected(case)["unverified"], relative_id(case)


def test_holdout_expected_files_are_byte_identical_to_their_committed_form():
    """The marker-pattern change touches regression cases only; the holdout
    expected.json files keep their original bytes."""
    holdout = ROOT_DIR / "evals" / "holdout"
    found = {
        case.name: hashlib.sha256((case / "expected.json").read_bytes()).hexdigest()
        for case in sorted(holdout.iterdir())
        if case.is_dir()
    }
    assert found == HOLDOUT_EXPECTED_SHA256


def test_every_drafting_case_carries_the_prose_judge_grader_rendered_from_the_rubric():
    """Every drafting case (not review) has graders/prose-judge.md, an llm grader
    over the final message whose body is the rubric in evals/rubrics/prose.md with the vote
    clause, byte for byte as evals/prose_judge.py renders it, so the rubric file stays the
    one source and a grader that drifts from it fails here."""
    from plugin_eval import load_evals_module

    prose_judge = load_evals_module("prose_judge")
    rubric = prose_judge.RUBRIC.read_text(encoding="utf-8")
    drafting = _drafting_cases()
    assert len(drafting) == 24, [case.name for case in drafting]
    for case in drafting:
        grader = case / "graders" / "prose-judge.md"
        assert grader.is_file(), f"{relative_id(case)}: no graders/prose-judge.md"
        rendered = prose_judge.render_grader(case)
        assert grader.read_text(encoding="utf-8") == rendered, f"{relative_id(grader)} drifted"
        assert rubric.strip() in rendered, "the grader body carries the rubric verbatim"
        assert "## The template's sections" in rendered, "the judge is given the section list"
        assert "The template's sections" in rubric.split("## The four criteria")[0], (
            "the rubric's What you are given names the section list"
        )
        expected = read_expected(case)
        article = "An" if expected["template"][0].lower() in "aeiou" else "A"
        assert (
            f"{article} {expected['template']} written for the {expected['audience']} audience."
            in rendered
        )
        data, body = split_front_matter(rendered)
        assert data == {"type": "llm", "focus": "last_message", "weight": 1}
        assert body.lstrip().startswith("Verifies:")
        assert "PASS if the score is 3 or more." in body and "Score: Unknown" in body
        assert case_problems(case) == []
    for case in CASES:
        if case not in drafting:
            assert not (case / "graders" / "prose-judge.md").exists(), relative_id(case)
    assert [case.name for case in prose_judge.drafting_cases()] == [c.name for c in drafting]
