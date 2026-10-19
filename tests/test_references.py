# Description: Shape tests over the skill's reference files: contents lists resolve, every
# Description: style rule carries a source, the audiences match the checker, and no dashes.
"""Tests over ``skills/technical-writer/references/*.md``.

The reference files are prose the skill loads at run time, so these tests assert their shape
(sections, sources, the audience roster) rather than their wording.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from check_structure import AUDIENCES, TemplateSpec, load_template

ROOT = Path(__file__).resolve().parents[1]
REFERENCES_DIR = ROOT / "skills" / "technical-writer" / "references"
STYLE_RULES = REFERENCES_DIR / "style-rules.md"
PROCEDURE_RULES = REFERENCES_DIR / "procedure-rules.md"
AUDIENCES_FILE = REFERENCES_DIR / "audiences.md"

# The 24 document types of spec R2 with their domain and the default audience spec
# Assumption 1 gives them: engineer for user documentation, engineering and API types, with
# operator for runbooks and advisories; regulator for Annex IV and the GPAI form; downstream
# provider for model cards; executive for system cards; data subject for privacy notices;
# auditor for DPIAs.
SPEC_TYPES: dict[str, tuple[str, str]] = {
    "concept": ("user documentation", "engineer"),
    "task": ("user documentation", "engineer"),
    "multiple-task procedure": ("user documentation", "engineer"),
    "reference": ("user documentation", "engineer"),
    "tutorial": ("user documentation", "engineer"),
    "troubleshooting": ("user documentation", "engineer"),
    "release notes": ("user documentation", "engineer"),
    "architecture decision record": ("engineering", "engineer"),
    "architecture description": ("engineering", "engineer"),
    "design doc or RFC": ("engineering", "engineer"),
    "postmortem": ("engineering", "engineer"),
    "runbook": ("engineering", "operator"),
    "changelog entry": ("engineering", "engineer"),
    "endpoint or field description": ("API", "engineer"),
    "error catalog entry": ("API", "engineer"),
    "model card": ("AI governance", "downstream provider"),
    "system card": ("AI governance", "executive"),
    "Annex IV technical file": ("AI governance", "regulator"),
    "GPAI Model Documentation Form": ("AI governance", "regulator"),
    "vulnerability advisory": ("security", "operator"),
    "disclosure notification": ("security", "operator"),
    "SECURITY.md": ("security", "engineer"),
    "privacy notice": ("privacy", "data subject"),
    "data protection impact assessment": ("privacy", "auditor"),
}

# The guides a style rule may cite, and the licenses or markings that may follow the guide.
# A verbatim rule carries the license it is quoted under; a paraphrased rule says so, since
# its guide publishes no reuse license (spec R12); a house rule names itself.
GUIDES = (
    "Google developer documentation style guide",
    "Google Technical Writing",
    "Grafana Writers' Toolkit",
    "Splunk Style Guide",
    "Splunk Vale ruleset",
    "Microsoft Writing Style Guide",
    "Kubernetes style guide",
    "Red Hat supplementary style guide",
    "WP260",
    "GPAI Model Documentation Form",
    "Keep a Changelog",
    "house rule",
)
LICENSES = ("CC BY 4.0", "Apache-2.0", "MIT", "CC0", "statutory", "standards")
SOURCE_MARKINGS = (*LICENSES, "paraphrased", "house rule")

_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
_CONTENTS_LINK = re.compile(r"^- \[(?P<text>[^\]]+)\]\(#(?P<anchor>[^)]+)\)\s*$")
_LIST_ITEM = re.compile(r"^(?:[-*]|\d+\.)\s+")
_TRAILING_SOURCE = re.compile(r"\((?P<source>[^()]*)\)\.?\s*$")
_ENTRY = re.compile(r"^- (?P<key>Register|Length|Precision):\s+\S")
_TABLE_ROW = re.compile(r"^\|(?P<cells>.*)\|\s*$")
EM_DASH = chr(0x2014)
EN_DASH = chr(0x2013)
# Emoji and symbol blocks: miscellaneous symbols and dingbats, the supplementary symbol and
# pictograph planes, regional indicators, and the variation selector and joiner that
# compose them.
_EMOJI = re.compile(
    "["
    + "".join(
        f"{chr(start)}-{chr(end)}"
        for start, end in ((0x2600, 0x27BF), (0x2B00, 0x2BFF), (0x1F000, 0x1FAFF))
    )
    + chr(0xFE0F)
    + chr(0x200D)
    + "]"
)
# The standard's initials, but not the checker's STEP_* and STEM_* codes, plus its full name.
_FORBIDDEN_STE = re.compile(r"\bSTE(?![A-Za-z])|\bASD\b")
_FORBIDDEN_STE_NAME = re.compile(r"simplified technical english", re.I)


def reference_files() -> list[Path]:
    """Every Markdown file under references/, the templates included, in a stable order."""
    return sorted(REFERENCES_DIR.rglob("*.md"))


def top_level_references() -> list[Path]:
    """The reference files beside the templates directory, which the skill reads as prose."""
    return sorted(REFERENCES_DIR.glob("*.md"))


def relative_id(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def slug(heading: str) -> str:
    """The GitHub anchor for a heading: lowercased, punctuation dropped, spaces as hyphens."""
    text = re.sub(r"[^\w\s-]", "", heading.strip().lower())
    return re.sub(r"\s+", "-", text)


def headings(lines: list[str]) -> list[tuple[int, str]]:
    """Every heading outside fenced blocks as (level, text)."""
    found: list[tuple[int, str]] = []
    fenced = False
    for line in lines:
        if line.startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        match = _HEADING.match(line)
        if match:
            found.append((len(match.group(1)), match.group(2)))
    return found


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def table_rows(lines: list[str], heading: str) -> list[list[str]]:
    """The body rows of the first Markdown table under the named heading, cells stripped."""
    rows: list[list[str]] = []
    in_section = False
    for line in lines:
        match = _HEADING.match(line)
        if match:
            if in_section:
                break
            in_section = match.group(2) == heading
            continue
        if not in_section:
            continue
        row = _TABLE_ROW.match(line)
        if row is None:
            if rows:
                break
            continue
        cells = [cell.strip() for cell in row.group("cells").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        rows.append(cells)
    return rows[1:]  # the header row is first


@pytest.mark.parametrize(
    "path",
    [p for p in top_level_references() if len(read_lines(p)) > 100],
    ids=relative_id,
)
def test_long_reference_files_open_with_a_contents_list_that_resolves(path: Path):
    lines = read_lines(path)
    first_h2 = next((i for i, line in enumerate(lines) if line.startswith("## ")), None)
    assert first_h2 is not None, f"{path.name}: no H2 heading"
    assert lines[first_h2] == "## Contents", f"{path.name}: the first H2 is not Contents"
    links: list[str] = []
    for line in lines[first_h2 + 1 :]:
        if _HEADING.match(line):
            break
        match = _CONTENTS_LINK.match(line)
        if match:
            links.append(match.group("anchor"))
        else:
            assert not line.strip(), f"{path.name}: non-link line under Contents: {line!r}"
    assert links, f"{path.name}: Contents has no links"
    anchors = {slug(text) for _, text in headings(lines)}
    unresolved = [link for link in links if link not in anchors]
    assert not unresolved, f"{path.name}: Contents links resolve to no heading: {unresolved}"


def test_every_style_rule_ends_with_a_guide_and_a_license_or_house_rule():
    lines = read_lines(STYLE_RULES)
    rule_lines: list[tuple[int, str]] = []
    section: str | None = None
    fenced = False
    for number, line in enumerate(lines, start=1):
        if line.startswith("```"):
            fenced = not fenced
            continue
        match = _HEADING.match(line)
        if match:
            section = match.group(2)
            continue
        if fenced or section in (None, "Contents") or not _LIST_ITEM.match(line):
            continue
        rule_lines.append((number, line))
    assert rule_lines, "style-rules.md has no rule lines"
    bad: list[str] = []
    for number, line in rule_lines:
        match = _TRAILING_SOURCE.search(line)
        source = match.group("source") if match else ""
        names_guide = any(guide in source for guide in GUIDES)
        marked = any(marking in source for marking in SOURCE_MARKINGS)
        if not (match and names_guide and marked):
            bad.append(f"line {number}: {line}")
    assert not bad, "rule lines without a parenthesized guide and license: " + "; ".join(bad)


def test_audiences_file_names_the_seven_audiences_with_register_length_and_precision():
    lines = read_lines(AUDIENCES_FILE)
    named = [text for level, text in headings(lines) if level == 3]
    assert named == list(AUDIENCES), "the H3 roster differs from check_structure.AUDIENCES"
    entries: dict[str, set[str]] = {}
    current: str | None = None
    for line in lines:
        match = _HEADING.match(line)
        if match:
            current = match.group(2) if match.group(1) == "###" else None
            continue
        entry = _ENTRY.match(line)
        if entry and current is not None:
            entries.setdefault(current, set()).add(entry.group("key"))
    missing = {
        audience: {"Register", "Length", "Precision"} - entries.get(audience, set())
        for audience in AUDIENCES
    }
    missing = {audience: keys for audience, keys in missing.items() if keys}
    assert not missing, f"audience entries missing: {missing}"


def test_audiences_defaults_table_matches_spec_assumption_1():
    rows = table_rows(read_lines(AUDIENCES_FILE), "Defaults by document type")
    assert rows, "audiences.md has no Defaults by document type table"
    found = {row[0]: row[1] for row in rows}
    expected = {doc_type: audience for doc_type, (_, audience) in SPEC_TYPES.items()}
    assert found == expected
    assert set(found.values()) <= set(AUDIENCES)


def test_procedure_rules_never_name_the_controlled_language_standard():
    text = PROCEDURE_RULES.read_text(encoding="utf-8")
    hits = [match.group(0) for match in _FORBIDDEN_STE.finditer(text)]
    hits += [match.group(0) for match in _FORBIDDEN_STE_NAME.finditer(text)]
    assert not hits, f"procedure-rules.md names the standard: {hits}"


@pytest.mark.parametrize("path", reference_files(), ids=relative_id)
def test_reference_files_carry_no_dashes_or_emoji(path: Path):
    text = path.read_text(encoding="utf-8")
    assert EM_DASH not in text, f"{path.name}: em dash"
    assert EN_DASH not in text, f"{path.name}: en dash"
    emoji = sorted({match.group(0) for match in _EMOJI.finditer(text)})
    assert not emoji, f"{path.name}: emoji {emoji}"


# ---- taxonomy, checklists, attribution ----------------------------------------

TAXONOMY = REFERENCES_DIR / "taxonomy.md"
CHECKLISTS = REFERENCES_DIR / "checklists.md"
ATTRIBUTION = REFERENCES_DIR / "attribution.md"
TEMPLATES_DIR = REFERENCES_DIR / "templates"
SKILL_FILE = REFERENCES_DIR.parent / "SKILL.md"
OUT_OF_SCOPE_OWNERS = {"github", "pentest-report"}

_MD_LINK = re.compile(r"\[[^\]]*\]\((?P<target>[^)#\s]+)(?:#[^)]*)?\)")


def shipped_templates() -> list[TemplateSpec]:
    """Every real template under references/templates, loaded."""
    return [load_template(path) for path in sorted(TEMPLATES_DIR.glob("*.md"))]


def section_items(lines: list[str], heading: str) -> list[str]:
    """The list items under the first heading with that text, up to the next heading of the
    same or a shallower level, with nested items included."""
    items: list[str] = []
    level: int | None = None
    for line in lines:
        match = _HEADING.match(line)
        if match:
            if level is not None and len(match.group(1)) <= level:
                break
            if match.group(2).lower() == heading.lower():
                level = len(match.group(1))
            continue
        if level is not None and _LIST_ITEM.match(line.lstrip()):
            items.append(line.strip())
    return items


def test_taxonomy_has_one_row_per_spec_type_with_domain_audience_and_status():
    rows = table_rows(read_lines(TAXONOMY), "Supported types")
    assert rows, "taxonomy.md has no Supported types table"
    found = {row[0]: (row[1], row[2], row[3]) for row in rows}
    assert set(found) == set(SPEC_TYPES), "the taxonomy rows differ from spec R2's 24 types"
    shipped = {spec.type for spec in shipped_templates()}
    for doc_type, (domain, audience, status) in found.items():
        assert (domain, audience) == SPEC_TYPES[doc_type], doc_type
        if doc_type in shipped:
            assert status == "shipped", f"{doc_type}: template exists, status {status!r}"
        else:
            assert status == "planned", f"{doc_type}: no template, status {status!r}"


def test_taxonomy_out_of_scope_rows_name_the_owning_skills():
    rows = table_rows(read_lines(TAXONOMY), "Out of scope by ownership")
    owners = {row[1].strip("`") for row in rows}
    assert owners >= OUT_OF_SCOPE_OWNERS, f"owners named: {owners}"


@pytest.mark.parametrize("spec", shipped_templates(), ids=lambda spec: spec.type)
def test_every_template_source_is_in_attribution_with_a_license_or_paraphrased(
    spec: TemplateSpec,
):
    lines = read_lines(ATTRIBUTION)
    carrying = [line for line in lines if spec.source in line]
    assert carrying, f"{spec.type}: its source value is not in attribution.md"
    line = carrying[0]
    quoted = "quoted" in line and any(license_ in line for license_ in LICENSES)
    assert quoted or "paraphrased" in line, f"{spec.type}: no license and use on: {line}"


@pytest.mark.parametrize("spec", shipped_templates(), ids=lambda spec: spec.type)
def test_checklists_has_a_section_per_shipped_template_naming_its_required_sections(
    spec: TemplateSpec,
):
    items = section_items(read_lines(CHECKLISTS), spec.type)
    assert items, f"checklists.md has no section for {spec.type}"
    text = "\n".join(items)
    required = [s.heading for s in spec.sections if not s.optional and s.heading]
    missing = [heading for heading in required if heading not in text]
    assert not missing, f"{spec.type}: checklist items name no {missing}"


def test_checklists_prose_section_lists_the_timeless_words_to_check_by_hand():
    items = section_items(read_lines(CHECKLISTS), "Prose, every type")
    assert items, "checklists.md has no Prose, every type section"
    text = "\n".join(items)
    assert re.search(r"`now`", text), "the prose checklist does not list now"
    assert re.search(r"`new`", text), "the prose checklist does not list new"


def test_every_reference_file_is_linked_from_the_skill_or_another_reference_file():
    files = reference_files()
    linking = [*files]
    if SKILL_FILE.is_file():
        linking.append(SKILL_FILE)
    linked: set[Path] = set()
    for source in linking:
        for match in _MD_LINK.finditer(source.read_text(encoding="utf-8")):
            target = match.group("target")
            if "://" in target:
                continue
            resolved = (source.parent / target).resolve()
            if resolved != source.resolve():
                linked.add(resolved)
    unlinked = [relative_id(f) for f in files if f.resolve() not in linked]
    assert not unlinked, f"reference files no other file links: {unlinked}"
