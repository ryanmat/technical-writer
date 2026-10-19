# Description: Template harness: every template loads, has a passing fixture, and every
# Description: fail-<CODE>.md fixture yields that finding code against its template.
"""Tests over every template and its fixtures, the harness template included."""

from pathlib import Path

import pytest
from check_structure import check_document, load_template, passes
from conftest import (
    FIXTURES_DIR,
    HARNESS_DIR,
    ROOT,
    TEMPLATES_DIR,
    case_dirs,
    fail_fixtures,
    fixture_audience,
    fixture_dir,
    pass_fixtures,
    read_expected,
    relative_id,
    template_paths,
)
from plugin_eval import PLUGIN_EVAL_DIR

# The Vale release record the opt-in end-to-end test reads; a tool fixture, not a template's.
VALE_DIR = FIXTURES_DIR / "vale"

TEMPLATES = template_paths()
FAIL_FIXTURES = fail_fixtures()

# The document types the plugin ships, one added per template step. Each needs its template,
# at least one fail fixture, and one eval case naming it under either eval root. The three
# original types also need a holdout case; later types ship with regression cases only.
SHIPPED_TYPES = frozenset(
    {
        "task",
        "architecture decision record",
        "model card",
        "concept",
        "reference",
        "multiple-task procedure",
        "tutorial",
        "troubleshooting",
        "release notes",
        "architecture description",
        "design doc or RFC",
        "postmortem",
        "runbook",
        "changelog entry",
        "endpoint or field description",
        "error catalog entry",
        "vulnerability advisory",
        "disclosure notification",
        "SECURITY.md",
        "system card",
        "Annex IV technical file",
        "GPAI Model Documentation Form",
        "privacy notice",
        "data protection impact assessment",
    }
)
HOLDOUT_TYPES = frozenset({"task", "architecture decision record", "model card"})


@pytest.mark.parametrize("template", TEMPLATES, ids=relative_id)
def test_every_template_loads(template: Path):
    spec = load_template(template)
    assert spec.type
    assert spec.sections


@pytest.mark.parametrize("template", TEMPLATES, ids=relative_id)
def test_every_template_has_a_pass_fixture_and_each_one_passes(template: Path):
    spec = load_template(template)
    fixtures = pass_fixtures(spec)
    assert fixtures, f"{relative_id(template)}: no pass.md and no case reference names it"
    for fixture in fixtures:
        findings = check_document(
            fixture.path.read_text(encoding="utf-8"), spec, audience=fixture.audience
        )
        blocking = [f for f in findings if f.severity != "info"]
        assert passes(findings), (
            f"{relative_id(fixture.path)} fails the {spec.type} template: "
            + "; ".join(f"{f.code}: {f.message}" for f in blocking)
        )


@pytest.mark.parametrize("fixture", FAIL_FIXTURES, ids=[relative_id(f.path) for f in FAIL_FIXTURES])
def test_every_fail_fixture_yields_its_code(fixture):
    spec = load_template(fixture.template)
    text = fixture.path.read_text(encoding="utf-8")
    findings = check_document(text, spec, audience=fixture_audience(fixture.path))
    codes = {f.code for f in findings}
    assert fixture.code in codes, (
        f"{relative_id(fixture.path)} yields {sorted(codes) or 'no findings'}, not {fixture.code}"
    )


def test_the_harness_fail_fixture_is_in_the_parametrization():
    assert any(f.path.name == "fail-SECTION_MISSING.md" for f in FAIL_FIXTURES)
    assert any(f.template.name == "template.md" for f in FAIL_FIXTURES)


def test_every_fixture_directory_belongs_to_a_template():
    tool_dirs = (HARNESS_DIR, PLUGIN_EVAL_DIR, VALE_DIR)
    directories = sorted(p for p in FIXTURES_DIR.iterdir() if p.is_dir() and p not in tool_dirs)
    owned = {fixture_dir(load_template(template)) for template in TEMPLATES}
    orphans = [relative_id(d) for d in directories if d not in owned]
    assert orphans == [], f"fixture directories no template owns: {orphans}"


@pytest.mark.parametrize("doc_type", sorted(SHIPPED_TYPES))
def test_every_shipped_type_has_its_template_fixtures_and_eval_case(doc_type: str):
    specs = {load_template(template).type: template for template in TEMPLATES}
    assert doc_type in specs, f"no template declares type {doc_type!r}"
    assert any(f.template == specs[doc_type] for f in FAIL_FIXTURES), (
        f"{doc_type}: no fail-<CODE>.md fixture"
    )
    cases = [case for case in case_dirs() if read_expected(case).get("template") == doc_type]
    assert cases, f"{doc_type}: no eval case names it"


@pytest.mark.parametrize("doc_type", sorted(HOLDOUT_TYPES))
def test_every_holdout_type_has_a_holdout_case(doc_type: str):
    assert doc_type in SHIPPED_TYPES
    holdout = [
        case
        for case in case_dirs()
        if "holdout" in case.parts and read_expected(case).get("template") == doc_type
    ]
    assert holdout, f"{doc_type}: no holdout case names it"


def test_fixture_audience_reads_the_first_line_comment(tmp_path):
    named = tmp_path / "fail-LENGTH_EXCEEDED.md"
    named.write_text("<!-- audience: executive -->\n# Title\n", encoding="utf-8")
    assert fixture_audience(named) == "executive"
    plain = tmp_path / "pass.md"
    plain.write_text("# Title\n<!-- audience: executive -->\n", encoding="utf-8")
    assert fixture_audience(plain) is None, "the comment counts only on the first line"


def test_pass_fixtures_skips_a_review_case_reference():
    """Finding: a review case's reference is a findings list over a
    seeded document, not a document of the template its expected.json names, so pass_fixtures
    leaves it out and no caller filters it again."""
    task = load_template(TEMPLATES_DIR / "task.md")
    paths = [fixture.path for fixture in pass_fixtures(task)]
    review = ROOT / "evals" / "cases" / "review--task-missing-prereqs" / "reference.md"
    assert review.is_file() and read_expected(review.parent).get("mode") == "review"
    assert review not in paths
    assert ROOT / "evals" / "holdout" / "task--relay-alert-rule" / "reference.md" in paths


def test_conftest_reads_front_matter_with_the_checker_s_one_pattern():
    """Review round 2: conftest carried its own copy of the
    front matter pattern check_structure exports; the harness imports the checker's."""
    import check_structure
    import conftest

    assert conftest.FRONT_MATTER is check_structure.FRONT_MATTER
    source = Path(conftest.__file__).read_text(encoding="utf-8")
    assert "from check_structure import" in source and "FRONT_MATTER" in source
    assert "FRONT_MATTER = re.compile" not in source


def test_advisory_severity_slot_requires_the_rating_and_a_score_outside_the_vector():
    """Review round 1: the score lookahead was satisfied by the 4.0 inside the
    required CVSS:4.0/ vector and nothing read the rating word, so vector and label alone
    filled the slot its missing text promised would carry the score and the rating too."""
    spec = load_template(TEMPLATES_DIR / "vulnerability-advisory.md")
    reference = (
        ROOT / "evals" / "cases" / "vulnerability-advisory--relay-auth-bypass" / "reference.md"
    )
    text = reference.read_text(encoding="utf-8")
    full = (
        "High, 8.7 (CVSS-B). The Base score describes the flaw; Threat and Environmental "
        "metrics were not assessed, so it is not the risk to a given deployment."
    )
    assert full in text
    assert not [f for f in check_document(text, spec) if f.code == "EVIDENCE_MISSING"]
    vector_and_label = text.replace(full, "CVSS-B. The Base score describes the flaw.")
    missing = [f for f in check_document(vector_and_label, spec) if f.code == "EVIDENCE_MISSING"]
    assert [f.heading for f in missing] == ["Severity"], "the vector's 4.0 is not a score"
    no_rating = text.replace(full, "8.7 (CVSS-B). The Base score describes the flaw.")
    assert [f.heading for f in check_document(no_rating, spec) if f.code == "EVIDENCE_MISSING"] == [
        "Severity"
    ]
    no_score = text.replace(full, "High (CVSS-B). The Base score describes the flaw.")
    assert [f.heading for f in check_document(no_score, spec) if f.code == "EVIDENCE_MISSING"] == [
        "Severity"
    ]
