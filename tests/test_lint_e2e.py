# Description: The opt-in end-to-end run of lint.sh with a real Vale binary, plus the
# Description: shape of the VERSION fixture and the marker that keeps it out of the default suite.
"""The two tests marked ``vale`` download the Vale release recorded in
``tests/fixtures/vale/VERSION`` only when ``TW_VALE_URL`` is set, verify its checksum, sync the
Google package into the skill's StylesPath (gitignored) and run ``scripts/lint.sh``. The default
suite deselects them through ``-m 'not vale'`` in pyproject.toml; the skill itself never touches
the network (spec N4), only this test does."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import re
import subprocess
import tarfile
import tomllib
import urllib.request
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
LINT_SH = ROOT / "scripts" / "lint.sh"
VERSION_FILE = ROOT / "tests" / "fixtures" / "vale" / "VERSION"
VALE_INI = ROOT / "skills" / "technical-writer" / "references" / "vale" / ".vale.ini"
PASSING_DOCUMENT = ROOT / "evals" / "holdout" / "task--relay-alert-rule" / "reference.md"
FAILING_DOCUMENT = ROOT / "tests" / "fixtures" / "task" / "fail-BANNED_PATTERN.md"
DASH_RULE = "TechnicalWriter.Dashes"
OPT_IN = "TW_VALE_URL"
SYSTEMS = {"Darwin": "macOS", "Linux": "Linux"}
MACHINES = {"arm64": "arm64", "aarch64": "arm64", "x86_64": "64-bit", "AMD64": "64-bit"}


def version_fixture() -> dict:
    return yaml.safe_load(VERSION_FILE.read_text(encoding="utf-8"))


def platform_key() -> str:
    return f"{SYSTEMS[platform.system()]}_{MACHINES[platform.machine()]}"


def test_version_fixture_records_the_release_its_url_and_a_checksum_per_platform():
    fixture = version_fixture()
    assert re.fullmatch(r"\d+\.\d+\.\d+", fixture["version"]), fixture
    assert fixture["version"] in fixture["url"]
    assert "{platform}" in fixture["url"]
    assert fixture["url"].startswith("https://github.com/errata-ai/vale/releases/download/")
    for key, digest in fixture["sha256"].items():
        assert re.fullmatch(r"[0-9a-f]{64}", digest), key
    assert platform_key() in fixture["sha256"], fixture["sha256"]


def test_pyproject_registers_the_marker_and_deselects_it_by_default():
    config = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    options = config["tool"]["pytest"]["ini_options"]
    assert "-m 'not vale'" in options["addopts"], options["addopts"]
    assert any(marker.startswith("vale:") for marker in options["markers"]), options


@pytest.fixture(scope="module")
def vale_env(tmp_path_factory: pytest.TempPathFactory) -> dict[str, str]:
    """PATH with a verified Vale binary first, the Google package synced; skips without
    TW_VALE_URL, which is the opt-in switch: the URL and the checksum come from VERSION."""
    if not os.environ.get(OPT_IN, ""):
        pytest.skip(f"{OPT_IN} is not set; the Vale download is opt-in")
    fixture = version_fixture()
    key = platform_key()
    url = fixture["url"].format(platform=key)
    download_dir = tmp_path_factory.mktemp("vale-download")
    archive = download_dir / "vale.tar.gz"
    with urllib.request.urlopen(url, timeout=120) as response:
        archive.write_bytes(response.read())
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    assert digest == fixture["sha256"][key], f"{url}: sha256 {digest}"
    bin_dir = tmp_path_factory.mktemp("vale-bin")
    with tarfile.open(archive) as tar:
        tar.extractall(bin_dir, filter="data")
    binary = bin_dir / "vale"
    assert binary.is_file(), sorted(p.name for p in bin_dir.iterdir())
    binary.chmod(0o755)
    env = {**os.environ, "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}"}
    sync = subprocess.run(
        [str(binary), "--config", str(VALE_INI), "sync"],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert sync.returncode == 0, sync.stdout + sync.stderr
    return env


def lint(env: dict[str, str], document: Path) -> tuple[int, dict, dict]:
    """lint.sh's exit, its report, and Vale's alerts parsed from the report, by file."""
    result = subprocess.run(
        ["/bin/sh", str(LINT_SH), str(document)],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    report = json.loads(result.stdout)
    assert "vale" in report["ran"], report
    alerts = json.loads(report["results"]["vale"]["output"] or "{}")
    return result.returncode, report, alerts


@pytest.mark.vale
def test_the_task_holdout_reference_has_no_vale_error(vale_env):
    _, report, alerts = lint(vale_env, PASSING_DOCUMENT)
    errors = [a for file_alerts in alerts.values() for a in file_alerts if a["Severity"] == "error"]
    assert errors == [], errors
    assert report["results"]["vale"]["exit"] == 0, report["results"]["vale"]


@pytest.mark.vale
def test_the_em_dash_fixture_is_caught_by_the_dash_rule_by_name(vale_env):
    code, report, alerts = lint(vale_env, FAILING_DOCUMENT)
    checks = [a["Check"] for file_alerts in alerts.values() for a in file_alerts]
    assert DASH_RULE in checks, checks
    assert report["results"]["vale"]["exit"] != 0
    assert code == 1
