# Description: Tests over scripts/release.py, the export of one tagged source tree into the
# Description: public repository minus the private paths, with the private-identifier scan.
"""The release export against a temporary source repository with a tag and a temporary bare
public repository: the private paths stay behind, a file removed at the source is removed in
the public tree, a tag that is missing or not at HEAD is exit 2 with no public commit, and a
private identifier in the export is exit 1 naming the path."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from release import PRIVATE_IDENTIFIERS, PRIVATE_PATHS, SCAN_EXEMPT, is_private_path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "release.py"

PUBLIC_FILES = {
    "README.md": "# demo\n\nA public file.\n",
    "skills/demo/SKILL.md": "---\nname: demo\n---\n# Demo\n",
    "scripts/keep.py": "# Description: kept.\n# Description: kept.\nprint('ok')\n",
}
PRIVATE_FILES = {
    "spec.md": "# Spec\n",
    "prompt_plan.md": "# Plan\n",
    "findings.md": "# Findings\n",
    "research/lane.md": "# Research\n",
}


def git(cwd: Path, *args: str) -> str:
    out = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True)
    return out.stdout.strip()


def write(root: Path, files: dict[str, str]) -> None:
    for name, text in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def init_repo(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    git(root, "init", "-q", "-b", "main")
    git(root, "config", "user.name", "Test")
    git(root, "config", "user.email", "test@example.com")


@pytest.fixture
def source(tmp_path: Path) -> Path:
    root = tmp_path / "source"
    init_repo(root)
    write(root, PUBLIC_FILES)
    write(root, PRIVATE_FILES)
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "initial")
    git(root, "tag", "v9.9.9")
    return root


@pytest.fixture
def public(tmp_path: Path) -> Path:
    bare = tmp_path / "public.git"
    bare.mkdir()
    git(bare, "init", "-q", "--bare", "-b", "main")
    clone = tmp_path / "public"
    subprocess.run(["git", "clone", "-q", str(bare), str(clone)], capture_output=True, check=True)
    git(clone, "config", "user.name", "Test")
    git(clone, "config", "user.email", "test@example.com")
    return clone


def run_release(source: Path, public: Path, tag: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--source",
            str(source),
            "--tag",
            tag,
            "--public",
            str(public),
        ],
        capture_output=True,
        text=True,
    )


def public_tree(public: Path, ref: str) -> set[str]:
    return set(git(public, "ls-tree", "-r", "--name-only", ref).splitlines())


def public_has_commits(public: Path) -> bool:
    return (
        subprocess.run(
            ["git", "rev-parse", "--verify", "-q", "HEAD"], cwd=public, capture_output=True
        ).returncode
        == 0
    )


def test_export_copies_the_tagged_tree_minus_the_private_paths(source: Path, public: Path):
    result = run_release(source, public, "v9.9.9")
    assert result.returncode == 0, result.stdout + result.stderr
    body = json.loads(result.stdout)
    assert body["tag"] == "v9.9.9"
    assert git(public, "log", "-1", "--format=%s") == "release v9.9.9"
    assert git(public, "rev-parse", "v9.9.9^{commit}") == git(public, "rev-parse", "HEAD")
    assert body["commit"] == git(public, "rev-parse", "HEAD")
    tree = public_tree(public, "v9.9.9")
    assert tree == set(PUBLIC_FILES)
    assert not any(is_private_path(name) for name in tree)
    for name in PUBLIC_FILES:
        assert (public / name).read_text(encoding="utf-8") == PUBLIC_FILES[name]


def test_a_file_removed_at_the_source_is_removed_in_the_public_tree(source: Path, public: Path):
    assert run_release(source, public, "v9.9.9").returncode == 0
    git(source, "rm", "-q", "skills/demo/SKILL.md")
    write(source, {"scripts/added.py": "# Description: added.\n# Description: added.\n"})
    git(source, "add", "-A")
    git(source, "commit", "-q", "-m", "remove the skill, add a script")
    git(source, "tag", "v9.9.10")
    result = run_release(source, public, "v9.9.10")
    assert result.returncode == 0, result.stdout + result.stderr
    tree = public_tree(public, "v9.9.10")
    assert "skills/demo/SKILL.md" not in tree
    assert "scripts/added.py" in tree
    assert git(public, "rev-list", "--count", "HEAD") == "2"


def test_a_missing_tag_or_one_not_at_head_is_exit_2_with_no_public_commit(
    source: Path, public: Path
):
    missing = run_release(source, public, "v0.0.0")
    assert missing.returncode == 2, missing.stdout + missing.stderr
    assert "v0.0.0" in json.loads(missing.stdout)["error"]
    assert not public_has_commits(public)

    write(source, {"README.md": "# demo\n\nChanged after the tag.\n"})
    git(source, "add", "-A")
    git(source, "commit", "-q", "-m", "after the tag")
    stale = run_release(source, public, "v9.9.9")
    assert stale.returncode == 2, stale.stdout + stale.stderr
    assert "HEAD" in json.loads(stale.stdout)["error"]
    assert not public_has_commits(public)


def test_a_private_identifier_in_the_export_is_exit_1_naming_the_path(source: Path, public: Path):
    write(source, {"docs/note.md": "# Note\n\nThe plan is prompt_plan.md.\n"})
    git(source, "add", "-A")
    git(source, "commit", "-q", "-m", "leak")
    git(source, "tag", "v9.9.11")
    result = run_release(source, public, "v9.9.11")
    assert result.returncode == 1, result.stdout + result.stderr
    body = json.loads(result.stdout)
    assert body["hits"] and body["hits"][0]["path"] == "docs/note.md"
    assert "prompt_plan" in body["hits"][0]["match"]
    assert not public_has_commits(public)


def test_the_private_lists_are_the_release_script_s():
    assert PRIVATE_PATHS == ("spec.md", "prompt_plan.md", "findings.md", "research/")
    assert is_private_path("research/raw-lane-x.md")
    assert is_private_path("spec.md")
    assert not is_private_path("research.md")
    assert not is_private_path("docs/spec.md")
    assert "Matuszewski" in PRIVATE_IDENTIFIERS


def test_the_files_that_spell_the_identifiers_are_exported_without_a_hit(
    source: Path, public: Path
):
    """The release script and its test carry the identifier list itself, so the scan skips
    exactly those two paths; the same text anywhere else is a hit."""
    assert SCAN_EXEMPT == ("scripts/release.py", "tests/test_release.py")
    write(source, {name: "IDENTIFIERS = ('Matuszewski', 'herdr')\n" for name in SCAN_EXEMPT})
    git(source, "add", "-A")
    git(source, "commit", "-q", "-m", "the scanner itself")
    git(source, "tag", "v9.9.12")
    result = run_release(source, public, "v9.9.12")
    assert result.returncode == 0, result.stdout + result.stderr
    assert set(SCAN_EXEMPT) <= public_tree(public, "v9.9.12")
