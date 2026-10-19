# Description: Shared enumeration helpers for the template and eval-case harnesses: every
# Description: template, its pass and fail fixtures, and every eval case directory.
"""Collection-time helpers reused by tests/test_templates.py and tests/test_eval_cases.py.

The real template and eval directories are empty until later steps fill them, so every
enumerator also yields the synthetic fixtures under ``tests/fixtures/_harness/``; a
parametrized test therefore always has at least one case and never skips.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from check_structure import FRONT_MATTER, TemplateSpec, load_template

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = ROOT / "skills" / "technical-writer" / "references" / "templates"
FIXTURES_DIR = ROOT / "tests" / "fixtures"
HARNESS_DIR = FIXTURES_DIR / "_harness"
HARNESS_TEMPLATE = HARNESS_DIR / "template.md"
HARNESS_CASE = HARNESS_DIR / "case"
EVAL_CASE_ROOTS = (ROOT / "evals" / "holdout", ROOT / "evals" / "cases")

_FAIL_FIXTURE = re.compile(r"^fail-([A-Z0-9_]+)\.md$")
_AUDIENCE_COMMENT = re.compile(r"\A<!--\s*audience:\s*([a-z ]+?)\s*-->")


def template_paths() -> list[Path]:
    """Every real template plus the synthetic harness template, in a stable order."""
    return [*sorted(TEMPLATES_DIR.glob("*.md")), HARNESS_TEMPLATE]


def fixture_dir(spec: TemplateSpec) -> Path:
    """The directory holding a template's pass and fail fixtures.

    A template that lives under ``tests/fixtures/`` keeps its fixtures beside it; a real
    template's fixtures live under ``tests/fixtures/<type>/`` with the type's spaces as
    hyphens, so ``model card`` reads ``tests/fixtures/model-card/``.
    """
    if spec.path.is_relative_to(FIXTURES_DIR):
        return spec.path.parent
    return FIXTURES_DIR / spec.type.replace(" ", "-")


def case_dirs() -> list[Path]:
    """Every eval case directory under evals/holdout and evals/cases, plus the harness case."""
    found: list[Path] = []
    for root in EVAL_CASE_ROOTS:
        if root.is_dir():
            found.extend(sorted(p for p in root.iterdir() if p.is_dir()))
    return [*found, HARNESS_CASE]


def read_expected(case: Path) -> dict[str, Any]:
    return json.loads((case / "expected.json").read_text(encoding="utf-8"))


@dataclass(frozen=True)
class PassFixture:
    path: Path
    audience: str | None  # None means the template's default audience


def pass_fixtures(spec: TemplateSpec) -> list[PassFixture]:
    """The documents that must pass the template: its pass.md and every case reference.

    A case reference counts when the sibling expected.json names this template's type, and
    is checked at that file's audience. A review case's reference is a findings list over a
    seeded document, not a document of the type, so a case whose mode is review is skipped.
    """
    fixtures: list[PassFixture] = []
    pass_doc = fixture_dir(spec) / "pass.md"
    if pass_doc.is_file():
        fixtures.append(PassFixture(path=pass_doc, audience=fixture_audience(pass_doc)))
    for case in case_dirs():
        expected_path = case / "expected.json"
        reference = case / "reference.md"
        if not expected_path.is_file() or not reference.is_file():
            continue
        expected = read_expected(case)
        if expected.get("mode") == "review":
            continue
        if expected.get("template") == spec.type:
            fixtures.append(PassFixture(path=reference, audience=expected.get("audience")))
    return fixtures


@dataclass(frozen=True)
class FailFixture:
    template: Path
    path: Path
    code: str


def fail_fixtures() -> list[FailFixture]:
    """Every ``fail-<CODE>.md`` fixture with the template it must fail against."""
    fixtures: list[FailFixture] = []
    for template in template_paths():
        spec = load_template(template)
        for path in sorted(fixture_dir(spec).glob("fail-*.md")):
            match = _FAIL_FIXTURE.match(path.name)
            if match is None:
                raise ValueError(f"{path}: fail fixtures are named fail-<CODE>.md")
            fixtures.append(FailFixture(template=template, path=path, code=match.group(1)))
    return fixtures


def fixture_audience(path: Path) -> str | None:
    """The audience a fixture names in an ``<!-- audience: executive -->`` comment on its
    first line, or None for the template's default."""
    with path.open(encoding="utf-8") as handle:
        first_line = handle.readline()
    match = _AUDIENCE_COMMENT.match(first_line)
    return match.group(1) if match else None


def split_front_matter(text: str) -> tuple[dict[str, Any] | None, str]:
    """The YAML front matter mapping and the body, or (None, text) when there is none."""
    match = FRONT_MATTER.match(text)
    if match is None:
        return None, text
    data = yaml.safe_load(match.group(1))
    return (data if isinstance(data, dict) else None), match.group(2)


def relative_id(path: Path) -> str:
    """A short, stable test id for a path under the repository."""
    return path.relative_to(ROOT).as_posix()
