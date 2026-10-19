# Description: Step 46 tests over the public documentation set: every page under docs/ declares
# Description: its template and audience and passes the checker, and the public tree is clean.
"""The public release's guards: the five user documentation pages written by the skill for
the engineer audience, each passing ``check_document`` for the template its first line names;
a scan over the tracked tree minus the private paths for the identifiers that belong to the
build repository alone; and the LICENSE the README names."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest
from check_structure import AUDIENCES, check_document, passes, templates_by_type
from release import PRIVATE_IDENTIFIERS, SCAN_EXEMPT, is_private_path

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

_PRIVATE = re.compile("|".join(PRIVATE_IDENTIFIERS))


def tracked_public_files() -> list[Path]:
    """Every tracked file outside the private paths, as the export would copy it."""
    out = subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True, text=True
    )
    files: list[Path] = []
    for name in out.stdout.split("\0"):
        if not name or is_private_path(name):
            continue
        files.append(ROOT / name)
    return files


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


def test_the_public_tree_carries_no_private_identifier():
    hits: list[str] = []
    for path in tracked_public_files():
        if path.relative_to(ROOT).as_posix() in SCAN_EXEMPT:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for number, line in enumerate(text.splitlines(), start=1):
            match = _PRIVATE.search(line)
            if match:
                hits.append(f"{path.relative_to(ROOT).as_posix()}:{number}: {match.group(0)}")
    assert hits == [], "private identifiers in the public tree:\n" + "\n".join(hits)


def test_license_exists_and_the_readme_names_it():
    assert LICENSE.is_file(), "no LICENSE at the repository root"
    assert "Apache License" in LICENSE.read_text(encoding="utf-8")
    assert "LICENSE" in README.read_text(encoding="utf-8"), "README.md does not name LICENSE"
