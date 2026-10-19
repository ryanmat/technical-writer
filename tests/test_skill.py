# Description: Shape tests over skills/technical-writer/SKILL.md: the front matter constraints,
# Description: the reference link graph, and the body's fixed content.
"""Tests over the skill body. The holdout evals gate its behavior; these tests gate
the constraints Anthropic's skill authoring guidance and the spec fix."""

from __future__ import annotations

import re
from pathlib import Path

from check_structure import AUDIENCES, DOMAINS
from conftest import split_front_matter
from test_references import _EMOJI, _MD_LINK, EM_DASH, EN_DASH, reference_files

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "technical-writer"
SKILL_FILE = SKILL_DIR / "SKILL.md"
MAX_BODY_LINES = 500
MAX_DESCRIPTION_CHARS = 1024
FIRST_PERSON_OPENERS = {"i", "you", "we"}
MARKER_FORM = "[UNVERIFIED: what is missing]"
LLMS_TXT_FORM = "[Title](url.md) - description"


def skill() -> tuple[dict, str]:
    front, body = split_front_matter(SKILL_FILE.read_text(encoding="utf-8"))
    assert front is not None, "SKILL.md has no YAML front matter"
    return front, body


def local_links(path: Path) -> set[Path]:
    """Every relative Markdown link target in the file, resolved against its directory."""
    targets: set[Path] = set()
    for match in _MD_LINK.finditer(path.read_text(encoding="utf-8")):
        target = match.group("target")
        if "://" not in target:
            targets.add((path.parent / target).resolve())
    return targets


def test_body_is_under_the_line_cap():
    _, body = skill()
    assert len(body.splitlines()) < MAX_BODY_LINES


def test_front_matter_names_the_skill_and_describes_it_in_the_third_person():
    front, _ = skill()
    assert front["name"] == "technical-writer"
    description = str(front["description"]).strip()
    assert len(description) < MAX_DESCRIPTION_CHARS
    first_word = re.match(r"\w+", description)
    assert first_word is not None
    assert first_word.group(0).lower() not in FIRST_PERSON_OPENERS, description[:40]
    lowered = description.lower()
    missing = [domain for domain in DOMAINS if domain.lower() not in lowered]
    assert not missing, f"the description names no {missing}"


def test_skill_links_every_reference_file_directly_or_through_one_reference_file():
    direct = local_links(SKILL_FILE)
    one_hop: set[Path] = set()
    for linked in direct:
        if linked.is_file() and linked.suffix == ".md":
            one_hop |= local_links(linked)
    reachable = direct | one_hop
    unreached = [
        path.relative_to(ROOT).as_posix()
        for path in reference_files()
        if path.resolve() not in reachable
    ]
    assert not unreached, f"SKILL.md reaches no {unreached}"


def test_body_names_the_audience_roster_and_the_marker_form_once_each():
    _, body = skill()
    roster_lines = [
        line for line in body.splitlines() if all(audience in line for audience in AUDIENCES)
    ]
    assert len(roster_lines) == 1, f"the seven audiences are listed on {len(roster_lines)} lines"
    assert body.count(MARKER_FORM) == 1, f"the marker form appears {body.count(MARKER_FORM)} times"
    assert "[UNVERIFIED:" in body
    assert EM_DASH not in body, "em dash in the body"
    assert EN_DASH not in body, "en dash in the body"
    assert not _EMOJI.search(body), "emoji in the body"


def test_body_carries_review_mode_the_llms_txt_form_and_the_composition_pointers():
    _, body = skill()
    headings = [line for line in body.splitlines() if line.startswith("#")]
    assert any("review mode" in heading.lower() for heading in headings), headings
    assert LLMS_TXT_FORM in body
    assert "`humanize`" in body
    assert "`writing-style-review`" in body


def test_review_mode_examples_name_no_rule_a_review_case_seeds():
    """Done check: an instruction written to close an eval miss must not quote the
    rule text of a defect a review case seeds, or the rerun measures the quote. The checker's
    rule texts per code are fixed in scripts/check_structure.py; the banned-pattern rules are
    the global set plus the seeded template's own."""
    import json

    from check_structure import GLOBAL_BANS, load_template

    section = _review_mode_section()
    rule_text = {
        "SECTION_MISSING": ["required section present"],
        "SECTION_ORDER": ["sections in template order"],
        "SECTION_UNKNOWN": ["heading listed in template"],
        "EVIDENCE_MISSING": ["evidence slot filled or marked"],
        "H1_COUNT": ["one H1 title"],
        "H1_PATTERN": ["title in the template's form"],
    }
    templates = {
        load_template(path).type: load_template(path)
        for path in (SKILL_DIR / "references" / "templates").glob("*.md")
    }
    seeded: set[str] = set()
    for case in sorted((ROOT / "evals" / "cases").glob("review--*")):
        expected = json.loads((case / "expected.json").read_text(encoding="utf-8"))
        spec = templates[expected["template"]]
        for defect in expected["defects"]:
            if defect["code"] == "BANNED_PATTERN":
                seeded.update(rule for _, rule, _ in GLOBAL_BANS)
                seeded.update(banned.rule for banned in spec.banned_patterns)
            else:
                seeded.update(rule_text[defect["code"]])
    assert seeded, "no review case lists a defect"
    quoted = sorted(rule for rule in seeded if rule in section)
    assert quoted == [], f"review mode quotes seeded rule text: {quoted}"


def _review_mode_section() -> str:
    """The Review mode section with its hard wraps folded, so a rule text split across two
    lines still matches."""
    body = SKILL_FILE.read_text(encoding="utf-8")
    start = body.index("## Review mode")
    end = body.index("\n## ", start + 1)
    return " ".join(body[start:end].split())


def test_body_sends_the_writer_to_the_taxonomy_s_template_file_column_not_a_guessed_path():
    """13 of 48 Sonnet runs opened a guessed templates/<type>.md path (decision-record,
    dpia, advisory) and one ADR holdout run never recovered. The body names the taxonomy table's
    Template file column as the way to the file and never spells the guessable form."""
    _, body = skill()
    assert "templates/<type>.md" not in body
    assert "Template file" in body
