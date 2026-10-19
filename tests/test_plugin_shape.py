# Description: Tests the plugin's manifest and packaging shape: the two
# Description: .claude-plugin manifests, pyproject.toml, and .gitignore.
"""Tests for the technical-writer plugin scaffold."""

import json
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN_JSON = ROOT / ".claude-plugin" / "plugin.json"
MARKETPLACE_JSON = ROOT / ".claude-plugin" / "marketplace.json"
PYPROJECT = ROOT / "pyproject.toml"
GITIGNORE = ROOT / ".gitignore"


def _plugin() -> dict:
    return json.loads(PLUGIN_JSON.read_text())


def _marketplace() -> dict:
    return json.loads(MARKETPLACE_JSON.read_text())


def _pyproject() -> dict:
    return tomllib.loads(PYPROJECT.read_text())


def test_manifests_parse_and_name_the_plugin():
    plugin = _plugin()
    marketplace = _marketplace()
    assert plugin["name"] == "technical-writer"
    assert marketplace["name"] == "technical-writer"


def test_marketplace_has_one_entry_sourced_at_repo_root():
    plugins = _marketplace()["plugins"]
    assert len(plugins) == 1
    assert plugins[0]["name"] == "technical-writer"
    assert plugins[0]["source"] == "./"


def test_version_is_identical_across_the_three_files():
    plugin_version = _plugin()["version"]
    marketplace_version = _marketplace()["plugins"][0]["version"]
    pyproject_version = _pyproject()["project"]["version"]
    assert plugin_version == "0.2.1"
    assert plugin_version == marketplace_version == pyproject_version


def test_pyproject_matches_the_rm_agents_layout():
    pyproject = _pyproject()
    project = pyproject["project"]
    assert project["requires-python"] == ">=3.12"
    assert any(dep.startswith("pyyaml") for dep in project["dependencies"])
    dev = pyproject["dependency-groups"]["dev"]
    assert any(dep.startswith("pytest") for dep in dev)
    assert any(dep.startswith("ruff") for dep in dev)
    assert pyproject["tool"]["pytest"]["ini_options"]["pythonpath"] == ["scripts"]


def test_gitignore_covers_the_generated_paths():
    lines = {line.strip() for line in GITIGNORE.read_text().splitlines()}
    for path in (".venv/", "__pycache__/", "evals/results/", ".next-auto/"):
        assert path in lines, f"{path} missing from .gitignore"
