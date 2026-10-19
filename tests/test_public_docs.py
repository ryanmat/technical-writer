# Description: Tests over the public documentation set: every page under docs/ declares
# Description: its template and audience and passes the checker, and the public tree is clean.
"""The public release's guards that run in the public tree: the five user documentation
pages written by the skill for the engineer audience, each passing ``check_document`` for the
template its first line names, and the LICENSE the README names. The scan for identifiers that
belong to the build repository alone lives in tests/test_release.py beside the export it
guards, since both spell the identifiers out and stay private."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from check_structure import AUDIENCES, check_document, passes, templates_by_type

ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
LICENSE = ROOT / "LICENSE"
README = ROOT / "README.md"

# The pages the release ships, each with the template its first line declares.
EXPECTED_PAGES: dict[str, str] = {
    "install.md": "task",
    "how-it-works.md": "concept",
    "document-types.md": "reference",
    "troubleshooting.md": "troubleshooting",
    "releasing.md": "task",
}
LOCAL_ONLY = {"lessons.md"}
_PAGE_HEADER = re.compile(
    r"\A<!-- template: (?P<template>[a-z -]+?); audience: (?P<audience>[a-z ]+?) -->\n"
)


def public_pages() -> list[Path]:
    return sorted(path for path in DOCS_DIR.glob("*.md") if path.name not in LOCAL_ONLY)


def test_the_five_pages_exist():
    present = {path.name for path in public_pages()}
    assert present == set(EXPECTED_PAGES), f"docs/ holds {sorted(present)}"


@pytest.mark.parametrize("name", sorted(EXPECTED_PAGES), ids=lambda name: name)
def test_each_page_declares_its_template_and_passes_the_checker(name: str):
    path = DOCS_DIR / name
    assert path.is_file(), f"docs/{name} is missing"
    text = path.read_text(encoding="utf-8")
    header = _PAGE_HEADER.match(text)
    assert header is not None, f"docs/{name} does not open with the template comment"
    template, audience = header.group("template"), header.group("audience")
    assert template == EXPECTED_PAGES[name], f"docs/{name} declares {template}"
    assert audience in AUDIENCES, f"docs/{name} declares audience {audience!r}"
    spec = templates_by_type()[template]
    findings = check_document(text, spec, audience)
    blocking = [f.to_dict() for f in findings if f.severity != "info"]
    assert passes(findings), f"docs/{name} fails {template} for {audience}: {blocking}"


def test_license_exists_and_the_readme_names_it():
    assert LICENSE.is_file(), "no LICENSE at the repository root"
    assert "Apache License" in LICENSE.read_text(encoding="utf-8")
    assert "LICENSE" in README.read_text(encoding="utf-8"), "README.md does not name LICENSE"
